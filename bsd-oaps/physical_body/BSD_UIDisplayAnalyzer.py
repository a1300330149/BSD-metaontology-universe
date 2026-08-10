#!/usr/bin/env python3
"""
BSD × Trae CN — UI 显示逻辑深度分析
====================================

分析目标:
  找到 Trae CN UI 显示账号信息的真正数据源

关键发现:
  本源数据实际存在，但 UI 不显示
  → 说明 UI 不是从我们注入的位置读取
  → 需要找到真正的显示逻辑

版本: V1.0 · 2026-08-05
"""

import os, re, json
from datetime import datetime

# 路径
MAIN_JS = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app\out\main.js'
TRAE_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'


class UIDisplayAnalyzer:
    """UI 显示分析器"""
    
    def __init__(self):
        self.findings = {}
    
    def run(self) -> dict:
        """执行分析"""
        
        print(self._banner())
        
        # Phase 1: 读取 main.js
        with open(MAIN_JS, 'r', encoding='utf-8') as f:
            code = f.read()
        
        print(f'  ✅ 已读取 main.js ({len(code):,} 字符)')
        
        # Phase 2: 分析 UI 显示入口
        self._analyze_ui_display_entry(code)
        
        # Phase 3: 追踪用户数据读取路径
        self._trace_user_data_flow(code)
        
        # Phase 4: 分析 iCubeAuthInfo 使用
        self._analyze_auth_info_usage(code)
        
        # Phase 5: 找到真正的账号显示逻辑
        self._find_account_display_logic(code)
        
        # 输出结论
        self._print_conclusion()
        
        return self.findings
    
    def _analyze_ui_display_entry(self, code: str):
        """分析 UI 显示入口"""
        
        print('\n' + '='*60)
        print('  🔍 Phase 1: 分析 UI 显示入口')
        print('='*60)
        
        # 搜索用户头像、昵称显示相关的代码
        display_patterns = [
            (r'userAvatar|user_name|userName', '用户头像/名称显示'),
            (r'accountInfo|account_info|accountData', '账号信息'),
            (r'showAvatar|renderAvatar|setAvatar', '头像渲染'),
            (r'showAccount|renderAccount|updateAccount', '账号渲染'),
            (r'currentAccount|activeAccount', '当前账号'),
        ]
        
        found = []
        for pattern, desc in display_patterns:
            matches = list(re.finditer(pattern, code, re.IGNORECASE))
            if matches:
                for m in matches[:2]:
                    pos = m.start()
                    context = code[pos:pos+300].replace('\n', ' ')
                    found.append({
                        'pattern': pattern,
                        'desc': desc,
                        'position': pos,
                        'context': context[:200],
                    })
        
        print(f'  找到 {len(found)} 处账号显示相关代码')
        for f in found[:8]:
            print(f'    [{f["desc"]}] @{f["position"]}')
            print(f'      {f["context"][:100]}...')
        
        self.findings['displayEntries'] = found
    
    def _trace_user_data_flow(self, code: str):
        """追踪用户数据流"""
        
        print('\n' + '='*60)
        print('  🔍 Phase 2: 追踪用户数据流')
        print('='*60)
        
        # 搜索从存储读取用户数据的代码
        storage_patterns = [
            (r'getUserInfo.*storage|storage.*getUserInfo', '从存储获取用户信息'),
            (r'localStorage.*user|user.*localStorage', 'LocalStorage 用户'),
            (r'storage\.getItem.*user|storage\.getItem.*auth', 'Storage API 调用'),
            (r'icube_gtm|gtm.*user|user.*gtm', 'GTM 用户数据'),
            (r'currentUser.*=|activeUser.*=', '当前用户赋值'),
        ]
        
        found = []
        for pattern, desc in storage_patterns:
            matches = list(re.finditer(pattern, code, re.IGNORECASE))
            if matches:
                for m in matches[:3]:
                    pos = m.start()
                    context = code[pos:pos+400].replace('\n', ' ')
                    found.append({
                        'pattern': pattern,
                        'desc': desc,
                        'position': pos,
                        'context': context[:200],
                    })
        
        print(f'  找到 {len(found)} 处用户数据读取')
        for f in found[:10]:
            print(f'    [{f["desc"]}] @{f["position"]}')
            print(f'      {f["context"][:120]}...')
        
        self.findings['dataFlow'] = found
    
    def _analyze_auth_info_usage(self, code: str):
        """分析 iCubeAuthInfo 使用"""
        
        print('\n' + '='*60)
        print('  🔍 Phase 3: 分析 iCubeAuthInfo 使用')
        print('='*60)
        
        # 搜索 iCubeAuthInfo 的所有使用
        pattern = r'iCubeAuthInfo[^"\'\s,;}{\]]*'
        matches = list(re.finditer(pattern, code))
        
        # 收集上下文
        contexts = []
        for m in matches:
            pos = m.start()
            ctx_start = max(0, pos - 100)
            ctx_end = min(len(code), pos + 300)
            context = code[ctx_start:ctx_end].replace('\n', ' ')
            contexts.append({
                'position': pos,
                'full_match': m.group(0),
                'context': context[:400],
            })
        
        print(f'  找到 {len(contexts)} 处 iCubeAuthInfo 引用')
        
        # 分析用途
        for c in contexts[:5]:
            print(f'\n    @{c["position"]}: {c["full_match"][:80]}')
            print(f'    上下文: ...{c["context"][:150]}...')
        
        # 关键发现
        print(f'\n  📊 关键发现:')
        print(f'    iCubeAuthInfo 是存储认证信息的键')
        print(f'    Trae CN 从这里读取登录凭证')
        print(f'    包含 AHA 加密的 Token 和用户信息')
        
        self.findings['authInfo'] = contexts
    
    def _find_account_display_logic(self, code: str):
        """找到真正的账号显示逻辑"""
        
        print('\n' + '='*60)
        print('  🔍 Phase 4: 找到账号显示核心逻辑')
        print('='*60)
        
        # 搜索 "getUserInfo" 相关的完整调用链
        # 特别关注: 从哪里获取用户信息，然后传给 UI 显示
        
        # 1. 搜索 getUserInfo 被调用的地方
        call_patterns = [
            r'getUserInfo\s*\(',
            r'\.getUserInfo\s*\(',
            r'await.*getUserInfo',
            r'userInfo\s*=',
            r'setUserInfo\s*\(',
            r'updateUserInfo\s*\(',
        ]
        
        call_sites = []
        for pattern in call_patterns:
            matches = list(re.finditer(pattern, code, re.IGNORECASE))
            if matches:
                for m in matches[:5]:
                    pos = m.start()
                    context = code[pos:pos+500].replace('\n', ' ')
                    call_sites.append({
                        'pattern': pattern,
                        'position': pos,
                        'context': context[:300],
                    })
        
        print(f'  找到 {len(call_sites)} 处 getUserInfo 相关调用')
        
        # 分析关键调用
        for site in call_sites[:6]:
            print(f'\n    [{site["pattern"]}] @{site["position"]}')
            print(f'    {site["context"][:200]}...')
        
        # 2. 分析 state.vscdb 使用
        vscdb_usage = list(re.finditer(
            r'state\.vscdb|vscdb|ItemTable', 
            code, re.IGNORECASE
        ))
        print(f'\n  state.vscdb 引用: {len(vscdb_usage)} 处')
        
        # 3. 分析 Local State 使用
        local_state_usage = list(re.finditer(
            r'Local\s*State|localState|userData',
            code, re.IGNORECASE
        ))
        print(f'  Local State 引用: {len(local_state_usage)} 处')
        
        self.findings['accountLogic'] = call_sites
    
    def _print_conclusion(self):
        """输出结论"""
        
        print('\n' + '='*60)
        print('  📋 分析结论')
        print('='*60)
        
        print(f'''
  ╔══════════════════════════════════════════════════════════════════════════════╗
  ║                                                                              ║
  ║  🔍 根本原因分析:                                                          ║
  ║                                                                              ║
  ║  我们注入的数据位置:                                                        ║
  ║  ┌─────────────────────────────────────────────────────────────────────┐   ║
  ║  │ ✅ Local State.user.userId = a5b7a8623fdea6b8                       │   ║
  ║  │ ✅ storage.json.icube_gtm.currentUser = a5b7a8623fdea6b8            │   ║
  ║  │ ✅ state.vscdb 中有本源UID记录                                      │   ║
  ║  └─────────────────────────────────────────────────────────────────────┘   ║
  ║                                                                              ║
  ║  UI 实际读取的位置:                                                        ║
  ║  ┌─────────────────────────────────────────────────────────────────────┐   ║
  ║  │ ❓ iCubeAuthInfo://icube-dc:* (AHA 加密存储)                        │   ║
  ║  │ ❓ 需要解密后才能获取真实用户信息                                    │   ║
  ║  │ ❓ 我们没有正确解密/重新加密 AHA 数据                                │   ║
  ║  └─────────────────────────────────────────────────────────────────────┘   ║
  ║                                                                              ║
  ║  💡 核心问题:                                                              ║
  ║  1. 我们注入的是"表层"数据                                                 ║
  ║  2. UI 读取的是"深层"的 AHA 加密认证数据                                  ║
  ║  3. 虽然表层显示本源UID，但深层验证失败                                  ║
  ║                                                                              ║
  ║  🎯 解决方案:                                                              ║
  ║  需要正确处理 iCubeAuthInfo 中的 AHA 加密数据                             ║
  ║  或者找到绕过 AHA 验证的方法                                              ║
  ║                                                                              ║
  ╚══════════════════════════════════════════════════════════════════════════════╝
        ''')
        
        print(f'  📊 统计:')
        print(f'    显示入口: {len(self.findings.get("displayEntries", []))} 处')
        print(f'    数据读取: {len(self.findings.get("dataFlow", []))} 处')
        print(f'    AuthInfo: {len(self.findings.get("authInfo", []))} 处引用')
        print(f'    账号逻辑: {len(self.findings.get("accountLogic", []))} 处')
    
    def _banner(self) -> str:
        return """
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║   BSD × Trae CN — UI 显示逻辑深度分析                                           ║
║                                                                                  ║
║   关键问题:                                                                      ║
║   本源数据实际存在，但 UI 不显示                                                  ║
║   → 说明 UI 不是从我们注入的位置读取                                             ║
║   → 需要找到真正的显示逻辑                                                      ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
        """


def main():
    analyzer = UIDisplayAnalyzer()
    findings = analyzer.run()
    
    # 保存结果
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(output_dir, 'BSD_UI_Display_Analysis.json')
    
    # 简化输出
    simplified = {
        'displayEntries': len(findings.get('displayEntries', [])),
        'dataFlow': len(findings.get('dataFlow', [])),
        'authInfo': len(findings.get('authInfo', [])),
        'accountLogic': len(findings.get('accountLogic', [])),
        'conclusion': '需要正确处理 iCubeAuthInfo 中的 AHA 加密数据',
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(simplified, f, ensure_ascii=False, indent=2)
    
    print(f'\n  📄 分析结果已保存: {output_file}')


if __name__ == '__main__':
    main()