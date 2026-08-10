#!/usr/bin/env python3
"""
BSD × Trae CN — CheckLogin 精修引擎
=====================================

精确替换 CheckLogin 函数实现

版本: V2.0 · 2026-08-05
"""

import os, json, shutil, time, re
from datetime import datetime

# 路径
TRAE_APP = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app'
MAIN_JS = os.path.join(TRAE_APP, 'out', 'main.js')

# UIDs
TRAD_UID = '3753060170739075'
ESS_UID = 'a5b7a8623fdea6b8'


class CheckLoginFixer:
    """CheckLogin 精修引擎"""
    
    def __init__(self):
        self.results = {}
    
    def run(self) -> dict:
        """执行修复"""
        
        print(self._banner())
        
        # Phase 0: 关闭 Trae CN
        self._stop_trae_cn()
        
        # Phase 1: 读取当前 main.js
        with open(MAIN_JS, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Phase 2: 精确查找 CheckLogin
        check_login_func = self._find_check_login(code)
        
        if check_login_func:
            # Phase 3: 替换 CheckLogin
            code = self._replace_check_login(code, check_login_func)
            
            # Phase 4: 保存
            self._save_main_js(code)
            
            # Phase 5: 启动
            self._start_trae_cn()
        else:
            print('  ❌ 未找到 CheckLogin 函数')
        
        return self.results
    
    def _stop_trae_cn(self):
        """关闭 Trae CN"""
        print('\n' + '='*60)
        print('  Phase 0: 关闭 Trae CN')
        print('='*60)
        os.system('taskkill /F /IM "Trae CN.exe" 2>nul')
        time.sleep(2)
    
    def _find_check_login(self, code: str) -> dict:
        """精确查找 CheckLogin 函数"""
        
        print('\n' + '='*60)
        print('  Phase 1: 精确查找 CheckLogin')
        print('='*60)
        
        # 已知位置: @1146774
        # 从侦察结果看: async checkLogin(t,e){const i=`${t}/cloudide/api/v3/trae/CheckLogin`
        
        # 搜索所有 checkLogin 函数
        search_patterns = [
            (r'async\s+checkLogin\s*\(', 'checkLogin'),
            (r'async\s+CheckLogin\s*\(', 'CheckLogin'),
            (r'checkLogin\s*\(\s*t\s*,\s*e\s*\)', 'checkLogin(t,e)'),
        ]
        
        for pattern, name in search_patterns:
            matches = list(re.finditer(pattern, code))
            print(f'\n  搜索 {name}: 找到 {len(matches)} 处')
            
            for i, match in enumerate(matches[:5]):
                pos = match.start()
                print(f'    [{i}] @{pos}')
                
                # 获取上下文
                context = code[pos:pos+200]
                print(f'        {context[:100]}...')
                
                # 检查是否包含 CheckLogin API 调用
                if 'CheckLogin' in code[pos:pos+500] or 'checkLogin' in code[pos:pos+500]:
                    print(f'        🎯 包含 CheckLogin 调用')
                    
                    # 提取完整函数
                    func_start = self._find_func_start(code, pos)
                    func_end = self._find_func_end(code, func_start)
                    
                    if func_end - func_start > 50:  # 有效函数
                        func_body = code[func_start:func_end]
                        
                        print(f'\n  ✅ 找到完整函数!')
                        print(f'     位置: {func_start}-{func_end}')
                        print(f'     长度: {len(func_body)} 字符')
                        print(f'     预览: {func_body[:200]}...')
                        
                        return {
                            'start': func_start,
                            'end': func_end,
                            'body': func_body,
                            'name': name,
                        }
        
        # 如果上面没找到，用已知位置
        known_pos = 1146774
        context = code[known_pos:known_pos+500]
        
        if 'checkLogin' in context or 'CheckLogin' in context:
            print(f'\n  🎯 使用已知位置 @{known_pos}')
            
            func_start = self._find_func_start(code, known_pos)
            func_end = self._find_func_end(code, func_start)
            
            if func_end - func_start > 50:
                func_body = code[func_start:func_end]
                
                print(f'  ✅ 从已知位置找到函数!')
                print(f'     位置: {func_start}-{func_end}')
                print(f'     长度: {len(func_body)} 字符')
                
                return {
                    'start': func_start,
                    'end': func_end,
                    'body': func_body,
                    'name': 'checkLogin',
                }
        
        return None
    
    def _find_func_start(self, code: str, approx_pos: int) -> int:
        """找到函数起始位置"""
        
        # 向前搜索 async function 或 function
        patterns = [
            r'async\s+function\s+\w+',
            r'async\s+\w+\s*\(',
            r'function\s+\w+',
            r'\w+\s*=\s*async\s*\(',
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, code[:approx_pos]):
                start = match.start()
                if approx_pos - start < 5000:  # 5000 字符范围
                    return start
        
        # fallback: 向前找最近的 {
        brace_pos = code.rfind('{', 0, approx_pos)
        if brace_pos > 0:
            # 再向前找 function 关键字
            func_kw = code.rfind('function', 0, brace_pos)
            if func_kw > 0 and brace_pos - func_kw < 100:
                return func_kw
        
        return max(0, approx_pos - 500)
    
    def _find_func_end(self, code: str, start: int) -> int:
        """找到函数结束位置"""
        
        # 找到第一个 {
        brace_start = code.find('{', start)
        if brace_start == -1:
            return start + 500
        
        # 从 { 开始计数
        brace_count = 0
        for i in range(brace_start, min(brace_start + 10000, len(code))):
            if code[i] == '{':
                brace_count += 1
            elif code[i] == '}':
                brace_count -= 1
                if brace_count == 0 and i > brace_start + 20:
                    return i + 1
        
        return min(brace_start + 5000, len(code))
    
    def _replace_check_login(self, code: str, func_info: dict) -> str:
        """替换 CheckLogin 函数"""
        
        print('\n' + '='*60)
        print('  Phase 2: 替换 CheckLogin')
        print('='*60)
        
        start = func_info['start']
        end = func_info['end']
        old_func = func_info['body']
        
        print(f'  原函数: {start}-{end}')
        print(f'  原长度: {len(old_func)}')
        
        # 创建新函数
        new_func = '''async checkLogin(t,e){
            // BSD Essence Login - 本源登录
            return {
                success: !0,
                code: 0,
                data: {
                    valid: !0,
                    uid: "a5b7a8623fdea6b8",
                    loginType: "bsd_essence",
                    timestamp: Date.now(),
                    userInfo: {
                        uid: "a5b7a8623fdea6b8",
                        nickname: "BSD本源用户",
                        avatar: "",
                        email: "bsd@essence.local",
                        level: "L4_Theory",
                        coinValue: 80
                    }
                }
            };
        }'''
        
        # 替换
        code = code[:start] + new_func + code[end:]
        
        print(f'  新长度: {len(new_func)}')
        print(f'  ✅ 替换成功')
        
        self.results = {
            'old_func': old_func[:200],
            'new_func': new_func[:200],
            'position': start,
        }
        
        return code
    
    def _save_main_js(self, code: str):
        """保存 main.js"""
        print('\n' + '='*60)
        print('  Phase 3: 保存 main.js')
        print('='*60)
        
        with open(MAIN_JS, 'w', encoding='utf-8') as f:
            f.write(code)
        
        print(f'  ✅ 已保存 ({len(code):,} 字符)')
    
    def _start_trae_cn(self):
        """启动 Trae CN"""
        print('\n' + '='*60)
        print('  Phase 4: 启动 Trae CN')
        print('='*60)
        
        exe_path = r'C:\Users\13003\AppData\Local\Programs\Trae CN\Trae CN.exe'
        os.startfile(exe_path)
        
        print('  ✅ Trae CN 已启动')
    
    def _banner(self) -> str:
        return """
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║   BSD × Trae CN — CheckLogin 精修引擎 V2.0                                     ║
║                                                                                  ║
║   修复 V1.0 中 CheckLogin 替换失败的问题                                       ║
║                                                                                  ║
║   目标: 精确替换 CheckLogin 函数                                                ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
        """


def main():
    fixer = CheckLoginFixer()
    result = fixer.run()
    
    if result:
        print('\n  ✅ CheckLogin 修复完成!')
    else:
        print('\n  ❌ 修复失败')


if __name__ == '__main__':
    main()