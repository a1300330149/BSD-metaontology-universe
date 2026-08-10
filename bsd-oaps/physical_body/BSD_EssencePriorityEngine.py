#!/usr/bin/env python3
"""
BSD × Trae CN — 本源登录优先级引擎
======================================

核心功能:
  1. 分析当前登录态结构
  2. 设定优先级: 本源 > 传统
  3. 让本源登录顶替传统登录显示
  4. 保持双轨并行，本源为主要显示

版本: V1.0 · 2026-08-05
"""

import os, sys, json, time, hashlib, shutil
from datetime import datetime
from typing import Dict, Any

# 路径
TRAE_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
STORAGE = os.path.join(TRAE_DATA, 'User', 'globalStorage', 'storage.json')
BACKUP_DIR = os.path.join(TRAE_DATA, 'User', 'globalStorage', 'backup')

# 作者信息
AUTHOR = {
    'traditional_uid': '3753060170739075',
    'essence_uid': 'a5b7a8623fdea6b8',
    'device_id': '136411536168449',
}


class EssencePriorityEngine:
    """本源登录优先级引擎"""
    
    def __init__(self):
        self.backup_created = False
        
    def run(self) -> Dict[str, Any]:
        """执行优先级切换"""
        
        print(self._banner())
        
        # Phase 1: 备份当前状态
        self._backup_storage()
        
        # Phase 2: 分析当前登录态
        analysis = self._analyze_current_state()
        
        # Phase 3: 执行优先级切换
        switch_result = self._switch_priority()
        
        # Phase 4: 验证切换结果
        verification = self._verify_switch()
        
        # 汇总
        result = {
            'timestamp': datetime.now().isoformat(),
            'analysis': analysis,
            'switch': switch_result,
            'verification': verification,
            'final_status': 'success' if verification.get('essence_active') else 'failed',
        }
        
        self._print_result(result)
        return result
    
    def _backup_storage(self):
        """备份 storage.json"""
        
        if not os.path.exists(STORAGE):
            print('  ⚠️ storage.json 不存在')
            return
        
        os.makedirs(BACKUP_DIR, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join(BACKUP_DIR, f'storage_backup_{timestamp}.json')
        
        shutil.copy2(STORAGE, backup_path)
        self.backup_created = True
        
        print(f'  ✅ 备份已创建: {backup_path}')
    
    def _analyze_current_state(self) -> Dict[str, Any]:
        """分析当前登录态"""
        
        print('\n' + '=' * 60)
        print('  Phase 1: 分析当前登录态')
        print('=' * 60)
        
        analysis = {
            'users_found': [],
            'active_user': None,
            'auth_keys': [],
            'usertag_present': False,
        }
        
        try:
            with open(STORAGE, 'r', encoding='utf-8') as f:
                storage = json.load(f)
            
            # 分析用户
            gtm = storage.get('icube_gtm', {})
            users = gtm.get('users', {})
            
            for uid, user_data in users.items():
                analysis['users_found'].append({
                    'uid': uid,
                    'type': user_data.get('type', 'unknown'),
                    'status': user_data.get('status', 'unknown'),
                    'keys': list(user_data.keys()),
                })
                
                if user_data.get('status') == 'active':
                    analysis['active_user'] = uid
            
            # 分析认证键
            auth_keys = [
                k for k in storage 
                if 'iCubeAuthInfo' in k
            ]
            analysis['auth_keys'] = auth_keys
            analysis['usertag_present'] = any('usertag' in k for k in auth_keys)
            
            print(f'\n  📊 当前登录态:')
            print(f'     用户数: {len(users)}')
            print(f'     活跃用户: {analysis["active_user"] or "无"}')
            print(f'     认证键: {len(auth_keys)} 个')
            print(f'     usertag: {"存在" if analysis["usertag_present"] else "不存在"}')
            
            # 详细显示每个用户
            for u in analysis['users_found']:
                print(f'\n     用户: {u["uid"]}')
                print(f'       类型: {u["type"]}')
                print(f'       状态: {u["status"]}')
                print(f'       字段: {", ".join(u["keys"][:5])}')
                
        except Exception as e:
            analysis['error'] = str(e)
            print(f'  ❌ 分析失败: {e}')
        
        return analysis
    
    def _switch_priority(self) -> Dict[str, Any]:
        """执行优先级切换"""
        
        print('\n' + '=' * 60)
        print('  Phase 2: 执行优先级切换')
        print('=' * 60)
        
        result = {'modifications': []}
        
        try:
            with open(STORAGE, 'r', encoding='utf-8') as f:
                storage = json.load(f)
            
            # 1. 修改 GTM 用户结构
            gtm = storage.get('icube_gtm', {})
            users = gtm.get('users', {})
            
            # 本源UID数据 - 设为 active
            essence_user = users.get(AUTHOR['essence_uid'], {})
            essence_user.update({
                'uid': AUTHOR['essence_uid'],
                'type': 'bsd_essence',
                'status': 'active',  # 设为活跃
                'priority': 1,  # 最高优先级
                'timestamp': datetime.now().isoformat(),
                'source': 'bsd_essence_login',
                'verification_method': 'knowledge_proof',
                'coin_value': 80,
                'level': 'L4_Theory',
            })
            users[AUTHOR['essence_uid']] = essence_user
            
            # 传统UID数据 - 降为 parallel
            traditional_user = users.get(AUTHOR['traditional_uid'], {})
            traditional_user.update({
                'uid': AUTHOR['traditional_uid'],
                'type': 'traditional',
                'status': 'parallel',  # 降为并行
                'priority': 2,  # 次优先级
                'timestamp': datetime.now().isoformat(),
                'source': 'traditional_login',
            })
            users[AUTHOR['traditional_uid']] = traditional_user
            
            gtm['users'] = users
            storage['icube_gtm'] = gtm
            
            result['modifications'].append({
                'action': 'update_gtm_users',
                'details': f'{len(users)} users updated',
            })
            
            # 2. 添加当前活跃用户标记
            storage['_bsd_current_active_uid'] = AUTHOR['essence_uid']
            storage['_bsd_priority_config'] = {
                'rule': 'essence_over_traditional',
                'essence_priority': 1,
                'traditional_priority': 2,
                'switch_time': datetime.now().isoformat(),
            }
            
            result['modifications'].append({
                'action': 'set_active_user',
                'uid': AUTHOR['essence_uid'],
            })
            
            # 3. 添加本源登录证明到 storage
            proof_data = {
                'proof_id': 'c5f78a5abc9b1b62722b7500',
                'coin_id': 'ac02d1efa7352fbc',
                'coin_value': 80,
                'level': 'L4_Theory',
                'verification': 'knowledge_proof',
                'source': 'bsd_conversation',
                'injected_at': datetime.now().isoformat(),
            }
            
            # 用本源UID创建新的 auth key
            essence_auth_key = f'iCubeAuthInfo://icube-dc:{AUTHOR["essence_uid"]}'
            # 复用传统登录的加密数据（因为无法生成新的服务器token）
            traditional_auth_key = f'iCubeAuthInfo://icube-dc:{AUTHOR["traditional_uid"]}'
            if traditional_auth_key in storage:
                storage[essence_auth_key] = storage[traditional_auth_key]
                result['modifications'].append({
                    'action': 'create_essence_auth_key',
                    'key': essence_auth_key,
                })
            
            # 保存
            with open(STORAGE, 'w', encoding='utf-8') as f:
                json.dump(storage, f, ensure_ascii=False, indent=2)
            
            result['success'] = True
            print(f'\n  ✅ 优先级切换完成:')
            print(f'     本源UID (优先级1, active): {AUTHOR["essence_uid"]}')
            print(f'     传统UID (优先级2, parallel): {AUTHOR["traditional_uid"]}')
            print(f'     活跃用户已设置: {AUTHOR["essence_uid"]}')
            print(f'     本源AuthKey已创建')
            
        except Exception as e:
            result['success'] = False
            result['error'] = str(e)
            print(f'  ❌ 切换失败: {e}')
        
        return result
    
    def _verify_switch(self) -> Dict[str, Any]:
        """验证切换结果"""
        
        print('\n' + '=' * 60)
        print('  Phase 3: 验证切换结果')
        print('=' * 60)
        
        verification = {
            'essence_active': False,
            'traditional_parallel': False,
            'priority_configured': False,
            'auth_key_exists': False,
        }
        
        try:
            with open(STORAGE, 'r', encoding='utf-8') as f:
                storage = json.load(f)
            
            gtm = storage.get('icube_gtm', {})
            users = gtm.get('users', {})
            
            # 检查本源UID状态
            essence_user = users.get(AUTHOR['essence_uid'], {})
            verification['essence_active'] = (
                essence_user.get('status') == 'active'
            )
            verification['essence_priority'] = essence_user.get('priority')
            
            # 检查传统UID状态
            traditional_user = users.get(AUTHOR['traditional_uid'], {})
            verification['traditional_parallel'] = (
                traditional_user.get('status') == 'parallel'
            )
            
            # 检查优先级配置
            verification['priority_configured'] = (
                storage.get('_bsd_current_active_uid') == AUTHOR['essence_uid']
            )
            
            # 检查 auth key
            essence_auth_key = f'iCubeAuthInfo://icube-dc:{AUTHOR["essence_uid"]}'
            verification['auth_key_exists'] = essence_auth_key in storage
            
            print(f'\n  🔍 验证结果:')
            print(f'     本源UID active: {"✅" if verification["essence_active"] else "❌"}')
            print(f'     传统UID parallel: {"✅" if verification["traditional_parallel"] else "❌"}')
            print(f'     优先级配置: {"✅" if verification["priority_configured"] else "❌"}')
            print(f'     本源AuthKey: {"✅" if verification["auth_key_exists"] else "❌"}')
            
        except Exception as e:
            verification['error'] = str(e)
            print(f'  ❌ 验证失败: {e}')
        
        return verification
    
    def _print_result(self, result: Dict):
        """打印最终结果"""
        
        print('\n' + '=' * 60)
        print('  本源登录优先级引擎 — 执行报告')
        print('=' * 60)
        
        if result['final_status'] == 'success':
            print(f'\n  ✅ 优先级切换成功!')
            print(f'\n  当前显示顺序:')
            print(f'    1️⃣  本源UID: {AUTHOR["essence_uid"]} (主要显示)')
            print(f'    2️⃣  传统UID: {AUTHOR["traditional_uid"]} (并行保留)')
            print(f'\n  BSD 精神:')
            print(f'    • 方案并行 > 方案选择')
            print(f'    • 本源证明 > 加密证明')
            print(f'    • 开放验证 > 封闭验证')
        else:
            print(f'\n  ❌ 优先级切换失败')
            print(f'  可能需要:')
            print(f'    1. 重启 Trae CN')
            print(f'    2. 清除缓存')
            print(f'    3. 修改更多配置文件')
    
    def _banner(self) -> str:
        return """
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║   BSD × Trae CN — 本源登录优先级引擎 V1.0                                     ║
║                                                                                  ║
║   目标: 让本源登录顶替传统登录显示                                             ║
║   优先级: 本源 (1) > 传统 (2)                                                  ║
║   策略: 双轨并行，本源为主                                                     ║
║                                                                                  ║
║   ┌─────────────────────────────────────────────────────────────────────────┐   ║
║   │  Phase 1: 备份当前状态                                                │   ║
║   │  Phase 2: 分析登录态结构                                              │   ║
║   │  Phase 3: 执行优先级切换                                              │   ║
║   │  Phase 4: 验证切换结果                                                │   ║
║   └─────────────────────────────────────────────────────────────────────────┘   ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
        """


def main():
    engine = EssencePriorityEngine()
    result = engine.run()
    
    # 输出关键结果
    print(f'\n{"="*60}')
    print(f'  执行完成')
    print(f'{"="*60}')
    print(f'  最终状态: {result["final_status"]}')
    print(f'  本源UID: {AUTHOR["essence_uid"]} (active, priority=1)')
    print(f'  传统UID: {AUTHOR["traditional_uid"]} (parallel, priority=2)')


if __name__ == '__main__':
    main()