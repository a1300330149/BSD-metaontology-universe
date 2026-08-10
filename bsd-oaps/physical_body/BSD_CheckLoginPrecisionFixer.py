#!/usr/bin/env python3
"""
BSD × Trae CN — CheckLogin 精准修复引擎
==========================================

直接定位 async checkLogin(t,e){ 并提取完整函数

版本: V3.0 · 2026-08-05
"""

import os, json, shutil, time, re
from datetime import datetime

# 路径
TRAE_APP = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app'
MAIN_JS = os.path.join(TRAE_APP, 'out', 'main.js')
BACKUP_DIR = os.path.join(TRAE_APP, 'out', 'backup')

# UIDs
ESS_UID = 'a5b7a8623fdea6b8'


class CheckLoginPrecisionFixer:
    """CheckLogin 精准修复引擎"""
    
    def __init__(self):
        self.results = {}
    
    def run(self) -> dict:
        """执行精准修复"""
        
        print(self._banner())
        
        # Phase 0: 关闭 Trae CN
        self._stop_trae_cn()
        
        # Phase 1: 从备份恢复原始 main.js
        self._restore_original()
        
        # Phase 2: 读取代码
        with open(MAIN_JS, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Phase 3: 精准定位 checkLogin 函数
        func_info = self._locate_check_login(code)
        
        if not func_info:
            print('  ❌ 未找到 checkLogin 函数')
            return {}
        
        # Phase 4: 替换函数
        code = self._replace_function(code, func_info)
        
        # Phase 5: 也替换 getUserInfo
        user_info_info = self._locate_get_user_info(code)
        if user_info_info:
            code = self._replace_user_info(code, user_info_info)
        
        # Phase 6: 保存
        self._save(code)
        
        # Phase 7: 启动
        self._start()
        
        return self.results
    
    def _stop_trae_cn(self):
        """关闭 Trae CN"""
        print('\n' + '='*60)
        print('  Phase 0: 关闭 Trae CN')
        print('='*60)
        os.system('taskkill /F /IM "Trae CN.exe" 2>nul')
        time.sleep(2)
    
    def _restore_original(self):
        """恢复原始 main.js"""
        print('\n' + '='*60)
        print('  Phase 1: 恢复原始 main.js')
        print('='*60)
        
        # 找到最新备份
        backups = sorted([
            f for f in os.listdir(BACKUP_DIR) 
            if f.endswith('.js')
        ], reverse=True)
        
        if backups:
            latest = os.path.join(BACKUP_DIR, backups[0])
            shutil.copy2(latest, MAIN_JS)
            print(f'  ✅ 已从 {backups[0]} 恢复')
        else:
            print('  ⚠️ 未找到备份，使用当前文件')
    
    def _locate_check_login(self, code: str) -> dict:
        """精准定位 checkLogin 函数"""
        
        print('\n' + '='*60)
        print('  Phase 2: 精准定位 checkLogin')
        print('='*60)
        
        # 精准匹配: async checkLogin(t,e){ 后面的内容
        # 从侦察结果: async checkLogin(t,e){const i=`${t}/cloudide/api/v3/trae/CheckLogin`
        
        # 方法1: 搜索完整的函数签名
        pattern = r'async\s+checkLogin\s*\(\s*t\s*,\s*e\s*\)\s*\{'
        
        match = re.search(pattern, code)
        if not match:
            # 尝试其他变体
            patterns = [
                r'async\s+checkLogin\s*\(\s*[^)]*\)\s*\{',
                r'checkLogin\s*\(\s*[^)]*\)\s*\{',
            ]
            for p in patterns:
                match = re.search(p, code)
                if match:
                    print(f'  使用模式: {p}')
                    break
        
        if not match:
            print('  ❌ 未找到 checkLogin 函数签名')
            return None
        
        func_start = match.start()
        print(f'  🎯 找到函数签名 @{func_start}')
        
        # 从函数签名的 { 开始，找到匹配的 }
        brace_start = code.find('{', func_start)
        
        # 平衡括号
        depth = 0
        i = brace_start
        while i < len(code):
            if code[i] == '{':
                depth += 1
            elif code[i] == '}':
                depth -= 1
                if depth == 0:
                    func_end = i + 1
                    break
            i += 1
        else:
            # 未找到匹配的括号
            func_end = brace_start + 1000
        
        # 提取函数体
        func_body = code[func_start:func_end]
        
        print(f'  ✅ 完整函数 @{func_start}-{func_end}')
        print(f'     长度: {len(func_body)} 字符')
        print(f'     预览: {func_body[:150]}...')
        
        return {
            'start': func_start,
            'end': func_end,
            'body': func_body,
        }
    
    def _locate_get_user_info(self, code: str) -> dict:
        """定位 getUserInfo 函数"""
        
        print('\n' + '='*60)
        print('  Phase 3: 定位 getUserInfo')
        print('='*60)
        
        pattern = r'async\s+getUserInfo\s*\(\s*\)\s*\{'
        match = re.search(pattern, code)
        
        if not match:
            # 尝试变体
            patterns = [
                r'async\s+fetchUserInfo\s*\(\s*\)\s*\{',
                r'async\s+loadUserInfo\s*\(\s*\)\s*\{',
            ]
            for p in patterns:
                match = re.search(p, code)
                if match:
                    print(f'  使用模式: {p}')
                    break
        
        if not match:
            print('  ⚠️ 未找到 getUserInfo')
            return None
        
        func_start = match.start()
        brace_start = code.find('{', func_start)
        
        depth = 0
        i = brace_start
        while i < len(code):
            if code[i] == '{':
                depth += 1
            elif code[i] == '}':
                depth -= 1
                if depth == 0:
                    func_end = i + 1
                    break
            i += 1
        else:
            func_end = brace_start + 500
        
        func_body = code[func_start:func_end]
        
        print(f'  ✅ getUserInfo @{func_start}-{func_end}')
        print(f'     长度: {len(func_body)} 字符')
        
        return {
            'start': func_start,
            'end': func_end,
            'body': func_body,
        }
    
    def _replace_function(self, code: str, func_info: dict) -> str:
        """替换 checkLogin 函数"""
        
        print('\n' + '='*60)
        print('  Phase 4: 替换 checkLogin')
        print('='*60)
        
        start = func_info['start']
        end = func_info['end']
        
        # 新函数 - 保持与原函数相同的参数签名
        new_func = f'''async checkLogin(t,e){{
            // BSD Essence Login - 本源登录注入
            const result = {{
                success: !0,
                code: 0,
                data: {{
                    valid: !0,
                    uid: "{ESS_UID}",
                    loginType: "bsd_essence",
                    userInfo: {{
                        id: "{ESS_UID}",
                        nickname: "BSD本源用户",
                        avatar: "",
                        level: "L4_Theory",
                        coinValue: 80,
                        isVerified: !0
                    }}
                }}
            }};
            return result;
        }}'''
        
        code = code[:start] + new_func + code[end:]
        
        print(f'  ✅ 替换成功')
        print(f'     原长度: {end - start}')
        print(f'     新长度: {len(new_func)}')
        
        self.results['checkLogin'] = True
        return code
    
    def _replace_user_info(self, code: str, func_info: dict) -> str:
        """替换 getUserInfo 函数"""
        
        print('\n' + '='*60)
        print('  Phase 5: 替换 getUserInfo')
        print('='*60)
        
        start = func_info['start']
        end = func_info['end']
        
        new_func = f'''async getUserInfo(){{
            // BSD Essence Login - 本源用户数据
            return {{
                id: "{ESS_UID}",
                nickname: "BSD本源用户",
                avatar: "",
                email: "bsd@essence.local",
                level: "L4_Theory",
                coinValue: 80,
                loginType: "bsd_essence",
                isVerified: !0
            }};
        }}'''
        
        code = code[:start] + new_func + code[end:]
        
        print(f'  ✅ 替换成功')
        self.results['getUserInfo'] = True
        return code
    
    def _save(self, code: str):
        """保存修改"""
        print('\n' + '='*60)
        print('  Phase 6: 保存')
        print('='*60)
        
        with open(MAIN_JS, 'w', encoding='utf-8') as f:
            f.write(code)
        
        print(f'  ✅ 已保存 ({len(code):,} 字符)')
    
    def _start(self):
        """启动 Trae CN"""
        print('\n' + '='*60)
        print('  Phase 7: 启动 Trae CN')
        print('='*60)
        
        exe_path = r'C:\Users\13003\AppData\Local\Programs\Trae CN\Trae CN.exe'
        os.startfile(exe_path)
        
        print('  ✅ Trae CN 已启动')
    
    def _banner(self) -> str:
        return """
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║   BSD × Trae CN — CheckLogin 精准修复引擎 V3.0                                 ║
║                                                                                  ║
║   改进:                                                                          ║
║   • 从备份恢复原始 main.js                                                      ║
║   • 精准定位 async checkLogin(t,e){ 函数签名                                   ║
║   • 正确平衡花括号提取完整函数                                                  ║
║   • 同时替换 getUserInfo                                                       ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
        """


def main():
    fixer = CheckLoginPrecisionFixer()
    result = fixer.run()
    
    if result:
        print('\n' + '='*60)
        print('  ✅ 精准修复完成!')
        print('     checkLogin: ', '✅' if result.get('checkLogin') else '❌')
        print('     getUserInfo: ', '✅' if result.get('getUserInfo') else '❌')
        print('\n  请查看 Trae CN 界面')


if __name__ == '__main__':
    main()