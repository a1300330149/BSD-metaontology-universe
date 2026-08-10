#!/usr/bin/env python3
"""
BSD × Trae CN — 三引擎深度侦察
================================

三引擎架构:
  1. 基因引擎 (Gene Engine)
     - 识别 Trae CN 中的登录验证基因
     - 找到 CheckLogin、getUserInfo 等核心函数
     - 绘制登录态数据流图

  2. 黑客引擎 (Hacker Engine)  
     - 逆向分析 main.js 代码
     - 定位 UI 显示登录态的真正逻辑
     - 找到"忽悠"的根源（显示逻辑 vs 实际数据）

  3. 围棋引擎 (Go Engine)
     - 分析博弈态势
     - 制定最优替换策略
     - 计算注入成功率

目标: 找到 Trae CN 登录显示的真正真相

版本: V1.0 · 2026-08-05
"""

import os, sys, re, json, hashlib
from datetime import datetime
from collections import defaultdict

# Trae CN 程序目录
TRAE_APP = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app'
MAIN_JS = os.path.join(TRAE_APP, 'out', 'main.js')

# 输出目录
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


class GeneEngine:
    """基因引擎 — 识别登录验证基因"""
    
    def __init__(self):
        self.genes = []
        self.gene_map = defaultdict(list)
    
    def scan(self, code: str) -> list:
        """扫描代码，识别登录基因"""
        
        print('\n' + '='*60)
        print('  🔬 基因引擎: 扫描登录验证基因')
        print('='*60)
        
        # 登录相关基因模式
        gene_patterns = {
            'login_check': [
                r'CheckLogin',
                r'checkLogin',
                r'verifyLogin',
                r'validateLogin',
                r'isLoggedIn',
                r'getLoginStatus',
            ],
            'user_info': [
                r'getUserInfo',
                r'getUserInfo',
                r'fetchUserInfo',
                r'loadUserInfo',
                r'currentUser',
                r'activeUser',
            ],
            'auth_token': [
                r'iCubeAuthInfo',
                r'authToken',
                r'auth_token',
                r'jwtToken',
                r'jwt_token',
                r'accessToken',
                r'access_token',
            ],
            'ui_display': [
                r'showLoginStatus',
                r'displayUser',
                r'renderUserInfo',
                r'updateUserBadge',
                r'setUserAvatar',
                r'setUserInfo',
            ],
            'state_store': [
                r'userStore',
                r'authStore',
                r'accountStore',
                r'loginStore',
                r'UserState',
                r'AuthState',
            ],
            'api_call': [
                r'/CheckLogin',
                r'/api/v3/trae/',
                r'/cloudide/api/',
                r'auth/login',
                r'auth/verify',
            ],
        }
        
        found_genes = []
        
        for gene_type, patterns in gene_patterns.items():
            for pattern in patterns:
                matches = list(re.finditer(pattern, code))
                
                for match in matches:
                    # 获取上下文
                    start = max(0, match.start() - 50)
                    end = min(len(code), match.end() + 100)
                    context = code[start:end].replace('\n', ' ')
                    
                    gene = {
                        'type': gene_type,
                        'pattern': pattern,
                        'position': match.start(),
                        'context': context[:200],
                    }
                    
                    found_genes.append(gene)
                    self.gene_map[gene_type].append(gene)
        
        # 打印统计
        print(f'\n  📊 基因扫描统计:')
        for gene_type, genes in self.gene_map.items():
            print(f'     {gene_type}: {len(genes)} 个')
        
        # 打印关键基因
        print(f'\n  🔑 关键基因详情:')
        for gene in found_genes[:15]:
            print(f'     [{gene["type"]}] {gene["pattern"]} @{gene["position"]}')
            print(f'       ...{gene["context"][:100]}...')
        
        self.genes = found_genes
        return found_genes


class HackerEngine:
    """黑客引擎 — 逆向分析主程序"""
    
    def __init__(self):
        self.discoveries = []
        self.login_flow = []
    
    def analyze(self, code: str) -> dict:
        """深度分析登录流程"""
        
        print('\n' + '='*60)
        print('  🕵️ 黑客引擎: 逆向分析登录流程')
        print('='*60)
        
        # 1. 找到 CheckLogin 实现
        check_login_impl = self._find_check_login(code)
        
        # 2. 找到 getUserInfo 实现  
        user_info_impl = self._find_user_info(code)
        
        # 3. 找到 UI 显示逻辑
        ui_display_impl = self._find_ui_display(code)
        
        # 4. 找到状态存储
        state_store_impl = self._find_state_store(code)
        
        # 5. 绘制登录态数据流
        data_flow = self._trace_data_flow(code)
        
        discoveries = {
            'checkLogin': check_login_impl,
            'getUserInfo': user_info_impl,
            'uiDisplay': ui_display_impl,
            'stateStore': state_store_impl,
            'dataFlow': data_flow,
        }
        
        self.discoveries = discoveries
        return discoveries
    
    def _find_check_login(self, code: str) -> dict:
        """找到 CheckLogin 的完整实现"""
        
        print('\n  🔍 分析 CheckLogin 实现...')
        
        # 查找函数定义
        patterns = [
            r'(?:async\s+)?CheckLogin\s*\([^)]*\)\s*\{',
            r'(?:async\s+)?checkLogin\s*\([^)]*\)\s*\{',
            r'(?:async\s+)?verifyLogin\s*\([^)]*\)\s*\{',
        ]
        
        for pattern in patterns:
            matches = list(re.finditer(pattern, code))
            for match in matches[:3]:
                # 提取函数体
                func_start = match.start()
                func_end = self._find_function_end(code, func_start)
                
                if func_end:
                    func_body = code[func_start:func_end]
                    
                    print(f'    ✅ 找到实现 @{func_start}')
                    print(f'       长度: {len(func_body)} 字符')
                    
                    # 分析函数逻辑
                    analysis = self._analyze_check_login_logic(func_body)
                    print(f'       逻辑分析: {analysis}')
                    
                    return {
                        'found': True,
                        'position': func_start,
                        'length': len(func_body),
                        'logic': analysis,
                        'preview': func_body[:500],
                    }
        
        return {'found': False}
    
    def _analyze_check_login_logic(self, func_body: str) -> str:
        """分析 CheckLogin 逻辑"""
        
        logic = []
        
        # 检查是否调用远程 API
        if 'fetch' in func_body or 'request' in func_body or 'http' in func_body:
            logic.append('调用远程API')
        
        # 检查是否读取本地存储
        if 'localStorage' in func_body or 'storage' in func_body or 'iCubeAuthInfo' in func_body:
            logic.append('读取本地存储')
        
        # 检查是否有 token 验证
        if 'token' in func_body.lower() or 'jwt' in func_body.lower():
            logic.append('Token验证')
        
        # 检查是否有 fallback
        if 'fallback' in func_body.lower() or '||' in func_body or '??' in func_body:
            logic.append('有fallback机制')
        
        # 检查是否直接返回 true
        if 'return true' in func_body:
            logic.append('直接返回true')
        
        if not logic:
            return '需要深入分析'
        
        return ' + '.join(logic)
    
    def _find_user_info(self, code: str) -> dict:
        """找到 getUserInfo 实现"""
        
        print('\n  🔍 分析 getUserInfo 实现...')
        
        patterns = [
            r'(?:async\s+)?getUserInfo\s*\([^)]*\)\s*\{',
            r'(?:async\s+)?fetchUserInfo\s*\([^)]*\)\s*\{',
            r'(?:async\s+)?loadUserInfo\s*\([^)]*\)\s*\{',
        ]
        
        for pattern in patterns:
            matches = list(re.finditer(pattern, code))
            for match in matches[:3]:
                func_start = match.start()
                func_end = self._find_function_end(code, func_start)
                
                if func_end:
                    func_body = code[func_start:func_end]
                    
                    print(f'    ✅ 找到实现 @{func_start}')
                    print(f'       长度: {len(func_body)} 字符')
                    
                    # 检查是否从本地存储读取
                    reads_local = any([
                        'storage' in func_body.lower(),
                        'local' in func_body.lower(),
                        'gtm' in func_body.lower(),
                    ])
                    
                    print(f'       数据源: {"本地存储" if reads_local else "远程API"}')
                    
                    return {
                        'found': True,
                        'position': func_start,
                        'readsLocal': reads_local,
                        'preview': func_body[:300],
                    }
        
        return {'found': False}
    
    def _find_ui_display(self, code: str) -> dict:
        """找到 UI 显示逻辑"""
        
        print('\n  🔍 分析 UI 显示逻辑...')
        
        # 搜索登录状态显示相关的代码
        display_patterns = [
            r'loginStatus',
            r'userBadge',
            r'avatar.*user',
            r'setUserAvatar',
            r'updateUserInfo',
            r'showUserInfo',
            r'isLoggedIn.*display',
            r'display.*isLoggedIn',
        ]
        
        found_displays = []
        
        for pattern in display_patterns:
            matches = list(re.finditer(pattern, code, re.IGNORECASE))
            if matches:
                for match in matches[:2]:
                    start = max(0, match.start() - 30)
                    end = min(len(code), match.end() + 100)
                    context = code[start:end].replace('\n', ' ')
                    found_displays.append({
                        'pattern': pattern,
                        'context': context[:200],
                    })
        
        if found_displays:
            print(f'    ✅ 找到 {len(found_displays)} 处显示逻辑')
            for d in found_displays[:5]:
                print(f'       • {d["pattern"]}: ...{d["context"][:80]}...')
        
        return {
            'found': len(found_displays) > 0,
            'count': len(found_displays),
            'details': found_displays[:10],
        }
    
    def _find_state_store(self, code: str) -> dict:
        """找到状态存储"""
        
        print('\n  🔍 分析状态存储...')
        
        store_patterns = [
            (r'icube_gtm', 'GTM存储'),
            (r'iCubeAuthInfo', '认证信息存储'),
            (r'trae-jwt-token', 'JWT Token'),
            (r'userStore|authStore', '状态Store'),
            (r'storage\.getItem|storage\.setItem', 'Storage API'),
        ]
        
        found_stores = []
        
        for pattern, desc in store_patterns:
            matches = list(re.finditer(pattern, code, re.IGNORECASE))
            if matches:
                found_stores.append({
                    'pattern': pattern,
                    'desc': desc,
                    'count': len(matches),
                })
                print(f'    ✅ {desc}: {len(matches)} 处引用')
        
        return {
            'found': len(found_stores) > 0,
            'stores': found_stores,
        }
    
    def _trace_data_flow(self, code: str) -> list:
        """追踪登录态数据流"""
        
        print('\n  🔍 追踪数据流...')
        
        flow = []
        
        # 1. 认证数据读取
        flow.append({
            'step': 1,
            'source': 'storage.json',
            'key': 'iCubeAuthInfo://icube-dc:*',
            'target': '解密验证',
        })
        
        # 2. 解密流程
        aha_decrypt = re.search(r'decrypt.*aha|aha.*decrypt|iCubeAuthInfo.*decrypt', code, re.IGNORECASE)
        if aha_decrypt:
            flow.append({
                'step': 2,
                'source': 'AHA加密数据',
                'process': 'AES-256-CBC解密',
                'target': 'Protobuf数据',
                'position': aha_decrypt.start(),
            })
        
        # 3. 服务器验证
        check_api = re.search(r'/CheckLogin|checkLogin.*api|api.*checkLogin', code, re.IGNORECASE)
        if check_api:
            flow.append({
                'step': 3,
                'source': '解密后的Token',
                'process': '服务器API验证',
                'target': '验证结果',
                'position': check_api.start(),
            })
        
        # 4. UI更新
        ui_update = re.search(r'setUserInfo|updateUserInfo|showLoginStatus', code, re.IGNORECASE)
        if ui_update:
            flow.append({
                'step': 4,
                'source': '验证结果',
                'process': '更新UI状态',
                'target': '显示登录状态',
                'position': ui_update.start(),
            })
        
        for f in flow:
            print(f'    Step {f["step"]}: {f.get("source", "?")} → {f.get("process", f.get("target", "?"))}')
        
        self.login_flow = flow
        return flow
    
    def _find_function_end(self, code: str, start: int) -> int:
        """找到函数结束位置"""
        
        brace_count = 0
        i = start
        
        # 找到第一个 {
        while i < len(code) and code[i] != '{':
            i += 1
        
        # 从 { 开始计数
        for j in range(i, min(i + 5000, len(code))):
            if code[j] == '{':
                brace_count += 1
            elif code[j] == '}':
                brace_count -= 1
                if brace_count == 0 and j > start + 50:
                    return j + 1
        
        return min(start + 5000, len(code))


class GoEngine:
    """围棋引擎 — 策略制定"""
    
    def __init__(self):
        self.strategies = []
    
    def analyze_and_plan(self, discoveries: dict) -> dict:
        """分析并制定策略"""
        
        print('\n' + '='*60)
        print('  ♟️ 围棋引擎: 制定本源登录策略')
        print('='*60)
        
        # 分析态势
        situation = self._assess_situation(discoveries)
        
        # 制定策略
        strategy = self._devise_strategy(situation, discoveries)
        
        print(f'\n  📊 态势评估:')
        print(f'    {situation}')
        
        print(f'\n  🎯 制定策略:')
        print(f'    {strategy["description"]}')
        for step in strategy['steps']:
            print(f'    {step}')
        
        self.strategies = strategy
        return strategy
    
    def _assess_situation(self, discoveries: dict) -> str:
        """评估当前态势"""
        
        # 检查 CheckLogin 是否存在
        has_check_login = discoveries.get('checkLogin', {}).get('found', False)
        
        # 检查 getUserInfo 是否读取本地
        reads_local = discoveries.get('getUserInfo', {}).get('readsLocal', False)
        
        # 检查数据流
        data_flow = discoveries.get('dataFlow', [])
        has_server_verify = any(
            '服务器' in str(f.get('process', '')) 
            for f in data_flow
        )
        
        # 态势分析
        if has_check_login and has_server_verify:
            return 'CLOSED: 服务器验证闭环，无本地切口'
        elif reads_local:
            return 'OPEN: 本地读取，有注入切口'
        else:
            return 'MIXED: 混合验证，需要多切口'
    
    def _devise_strategy(self, situation: str, discoveries: dict) -> dict:
        """制定策略"""
        
        if 'CLOSED' in situation:
            # 策略 A: 替换验证逻辑
            return {
                'description': '替换 CheckLogin 逻辑，绕过服务器验证',
                'steps': [
                    '1. 找到 CheckLogin 函数实现',
                    '2. 替换为直接返回 {success: true, uid: ESS_UID}',
                    '3. 找到 getUserInfo 函数',
                    '4. 替换为返回本源用户数据',
                    '5. 保存修改并重启',
                ],
                'success_rate': 0.9,
            }
        elif 'OPEN' in situation:
            # 策略 B: 强化本地注入
            return {
                'description': '强化本地数据注入，利用本地读取特性',
                'steps': [
                    '1. 确保 storage.json 中本源UID为currentUser',
                    '2. 确保 Local State 中 user.userId = ESS_UID',
                    '3. 确保 JWT Token 中 sub = ESS_UID',
                    '4. 清除所有传统UID痕迹',
                    '5. 重启 Trae CN',
                ],
                'success_rate': 0.6,
            }
        else:
            # 策略 C: 混合策略
            return {
                'description': '多源注入 + 关键路径替换',
                'steps': [
                    '1. 分析关键验证路径',
                    '2. 替换关键节点的验证逻辑',
                    '3. 在每个数据源注入本源UID',
                    '4. 添加 fallback 返回本源登录',
                    '5. 全面测试',
                ],
                'success_rate': 0.75,
            }


class TripleEngineRunner:
    """三引擎执行器"""
    
    def __init__(self):
        self.gene = GeneEngine()
        self.hacker = HackerEngine()
        self.go = GoEngine()
    
    def run(self) -> dict:
        """运行三引擎"""
        
        print(self._banner())
        
        # 读取主程序
        print('\n' + '='*60)
        print('  📂 读取 Trae CN 主程序')
        print('='*60)
        
        with open(MAIN_JS, 'r', encoding='utf-8') as f:
            code = f.read()
        
        print(f'  ✅ 已读取 main.js')
        print(f'     大小: {len(code):,} 字符')
        print(f'     行数: {code.count(chr(10)):,} 行')
        
        # 基因引擎扫描
        genes = self.gene.scan(code)
        
        # 黑客引擎分析
        discoveries = self.hacker.analyze(code)
        
        # 围棋引擎规划
        strategy = self.go.analyze_and_plan(discoveries)
        
        # 汇总
        result = {
            'timestamp': datetime.now().isoformat(),
            'genes_found': len(genes),
            'discoveries': {
                'checkLogin_found': discoveries.get('checkLogin', {}).get('found', False),
                'getUserInfo_found': discoveries.get('getUserInfo', {}).get('found', False),
                'uiDisplay_count': discoveries.get('uiDisplay', {}).get('count', 0),
                'stateStore_count': len(discoveries.get('stateStore', {}).get('stores', [])),
            },
            'strategy': strategy,
            'login_flow': discoveries.get('dataFlow', []),
        }
        
        # 打印三引擎报告
        self._print_report(result)
        
        return result
    
    def _print_report(self, result: dict):
        """打印三引擎报告"""
        
        print('\n' + '='*60)
        print('  三引擎侦察报告')
        print('='*60)
        
        d = result['discoveries']
        
        print(f'\n  🧬 基因引擎:')
        print(f'     发现基因: {result["genes_found"]} 个')
        
        print(f'\n  🕵️ 黑客引擎:')
        print(f'     CheckLogin: {"✅ 找到" if d["checkLogin_found"] else "❌ 未找到"}')
        print(f'     getUserInfo: {"✅ 找到" if d["getUserInfo_found"] else "❌ 未找到"}')
        print(f'     UI显示逻辑: {d["uiDisplay_count"]} 处')
        print(f'     状态存储: {d["stateStore_count"]} 类')
        
        print(f'\n  ♟️ 围棋引擎:')
        print(f'     推荐策略: {result["strategy"]["description"]}')
        print(f'     预估成功率: {result["strategy"]["success_rate"]:.0%}')
        
        print(f'\n  📊 登录态数据流:')
        for step in result['login_flow']:
            print(f'     Step {step["step"]}: {step.get("source", "?")} → {step.get("target", "?")}')
    
    def _banner(self) -> str:
        return """
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║   BSD × Trae CN — 三引擎深度侦察 V1.0                                          ║
║                                                                                  ║
║   🧬 基因引擎: 识别登录验证基因                                                ║
║   🕵️ 黑客引擎: 逆向分析主程序代码                                             ║
║   ♟️ 围棋引擎: 制定最优替换策略                                                ║
║                                                                                  ║
║   目标: 找到 Trae CN 登录显示的真正真相                                        ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
        """


def main():
    runner = TripleEngineRunner()
    result = runner.run()
    
    # 保存结果
    output_file = os.path.join(OUTPUT_DIR, 'BSD_TripleEngine_Report.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f'\n  📄 报告已保存: {output_file}')


if __name__ == '__main__':
    main()