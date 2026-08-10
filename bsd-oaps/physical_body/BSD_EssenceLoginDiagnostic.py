#!/usr/bin/env python3
"""
BSD × Trae CN — 本源登录状态深度诊断
======================================

诊断目标:
  1. 检查用户数据目录中本源信息是否还存在
  2. 分析 Trae CN 启动时数据覆盖逻辑
  3. 确认账号信息显示的真正数据源

版本: V1.0 · 2026-08-05
"""

import os, json, sqlite3
from datetime import datetime

# 路径
TRAE_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
LOCAL_STATE = os.path.join(TRAE_DATA, 'Local State')
STORAGE = os.path.join(TRAE_DATA, 'User', 'globalStorage', 'storage.json')
VSCDB = os.path.join(TRAE_DATA, 'User', 'workspaceStorage', '37c75d46fd05168780d5ac3435faa836', 'state.vscdb')
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'
JWT_PATH = os.path.join(TRAE_CONFIG, 'trae-jwt-token')

# UIDs
TRAD_UID = '3753060170739075'
ESS_UID = 'a5b7a8623fdea6b8'


class EssenceLoginDiagnostic:
    """本源登录诊断引擎"""
    
    def __init__(self):
        self.report = {}
    
    def run(self) -> dict:
        """执行诊断"""
        
        print(self._banner())
        
        # Phase 1: 检查 Local State
        self._check_local_state()
        
        # Phase 2: 检查 storage.json
        self._check_storage()
        
        # Phase 3: 检查 state.vscdb
        self._check_vscdb()
        
        # Phase 4: 检查 JWT Token
        self._check_jwt_token()
        
        # Phase 5: 综合分析
        self._analyze_root_cause()
        
        # Phase 6: 输出报告
        self._print_report()
        
        return self.report
    
    def _check_local_state(self):
        """检查 Local State"""
        print('\n' + '='*60)
        print('  🔍 Phase 1: 检查 Local State')
        print('='*60)
        
        if os.path.exists(LOCAL_STATE):
            with open(LOCAL_STATE, 'r', encoding='utf-8') as f:
                state = json.load(f)
            
            # 检查用户相关字段
            user = state.get('user', {})
            profile = state.get('profile', {})
            
            print(f'  user.userId: {user.get("userId", "❌ 未设置")}')
            print(f'  user.nickname: {user.get("account", {}).get("nickname", "❌")}')
            print(f'  user.loginType: {user.get("loginType", "❌")}')
            print(f'  profile.uid: {profile.get("uid", "❌")}')
            
            # 检查本源标记
            has_essence = '_bsd_essence_mode' in state
            print(f'  _bsd_essence_mode: {"✅ 存在" if has_essence else "❌ 不存在"}')
            
            self.report['localState'] = {
                'userId': user.get('userId'),
                'loginType': user.get('loginType'),
                'hasEssenceMark': has_essence,
            }
        else:
            print('  ❌ Local State 不存在')
            self.report['localState'] = {'error': 'not_found'}
    
    def _check_storage(self):
        """检查 storage.json"""
        print('\n' + '='*60)
        print('  🔍 Phase 2: 检查 storage.json')
        print('='*60)
        
        if os.path.exists(STORAGE):
            with open(STORAGE, 'r', encoding='utf-8') as f:
                storage = json.load(f)
            
            # 检查 GTM
            gtm = storage.get('icube_gtm', {})
            current_user = gtm.get('currentUser', '❌ 未设置')
            users = gtm.get('users', {})
            
            print(f'  currentUser: {current_user}')
            print(f'  用户数量: {len(users)}')
            
            # 检查每个用户
            for uid, data in users.items():
                status = data.get('status', 'unknown')
                priority = data.get('priority', '?')
                type_ = data.get('type', '?')
                print(f'    {uid}: status={status}, priority={priority}, type={type_}')
            
            # 检查本源标记
            has_essence = '_bsd_essence_login' in storage
            print(f'  _bsd_essence_login: {"✅ 存在" if has_essence else "❌ 不存在"}')
            
            # 检查认证信息
            auth_keys = [k for k in storage if 'iCubeAuthInfo' in k]
            print(f'  认证键数量: {len(auth_keys)}')
            for k in auth_keys[:5]:
                print(f'    {k}')
            
            self.report['storage'] = {
                'currentUser': current_user,
                'userCount': len(users),
                'authKeyCount': len(auth_keys),
                'hasEssenceMark': has_essence,
            }
        else:
            print('  ❌ storage.json 不存在')
            self.report['storage'] = {'error': 'not_found'}
    
    def _check_vscdb(self):
        """检查 state.vscdb"""
        print('\n' + '='*60)
        print('  🔍 Phase 3: 检查 state.vscdb')
        print('='*60)
        
        if os.path.exists(VSCDB):
            try:
                conn = sqlite3.connect(VSCDB)
                cursor = conn.cursor()
                
                # 查找包含本源UID的记录
                cursor.execute(f"SELECT key, value FROM ItemTable WHERE key LIKE '%{ESS_UID}%'")
                essence_rows = cursor.fetchall()
                
                # 查找包含传统UID的记录
                cursor.execute(f"SELECT key, value FROM ItemTable WHERE key LIKE '%{TRAD_UID}%'")
                trad_rows = cursor.fetchall()
                
                # 查找本源标记
                cursor.execute("SELECT key, value FROM ItemTable WHERE key LIKE '%_bsd_%'")
                mark_rows = cursor.fetchall()
                
                print(f'  本源UID相关记录: {len(essence_rows)} 条')
                for key, val in essence_rows[:3]:
                    print(f'    {key}')
                
                print(f'  传统UID相关记录: {len(trad_rows)} 条')
                for key, val in trad_rows[:3]:
                    print(f'    {key}')
                
                print(f'  BSD标记记录: {len(mark_rows)} 条')
                for key, val in mark_rows[:3]:
                    print(f'    {key}')
                
                conn.close()
                
                self.report['vscdb'] = {
                    'essenceRows': len(essence_rows),
                    'tradRows': len(trad_rows),
                    'markRows': len(mark_rows),
                }
            except Exception as e:
                print(f'  ❌ 查询失败: {e}')
                self.report['vscdb'] = {'error': str(e)}
        else:
            print('  ❌ state.vscdb 不存在')
            self.report['vscdb'] = {'error': 'not_found'}
    
    def _check_jwt_token(self):
        """检查 JWT Token"""
        print('\n' + '='*60)
        print('  🔍 Phase 4: 检查 JWT Token')
        print('='*60)
        
        if os.path.exists(JWT_PATH):
            with open(JWT_PATH, 'r', encoding='utf-8') as f:
                token = f.read()
            
            print(f'  ✅ JWT Token 存在')
            print(f'  长度: {len(token)} 字符')
            
            # 尝试解码
            try:
                import base64
                parts = token.split('.')
                if len(parts) >= 2:
                    payload = base64.b64decode(parts[1] + '==').decode()
                    data = json.loads(payload)
                    print(f'  Subject: {data.get("sub", "?")}')
                    print(f'  Name: {data.get("name", "?")}')
                    print(f'  Type: {data.get("type", "?")}')
            except Exception as e:
                print(f'  解码失败: {e}')
            
            self.report['jwt'] = {'exists': True, 'length': len(token)}
        else:
            print('  ❌ JWT Token 不存在')
            self.report['jwt'] = {'exists': False}
    
    def _analyze_root_cause(self):
        """分析根本原因"""
        print('\n' + '='*60)
        print('  📊 Phase 5: 根因分析')
        print('='*60)
        
        issues = []
        d = self.report
        
        # 检查 Local State
        ls = d.get('localState', {})
        if ls.get('userId') != ESS_UID:
            issues.append(f'Local State userId = {ls.get("userId")}，不是本源UID')
        if not ls.get('hasEssenceMark'):
            issues.append('Local State 缺少本源标记')
        
        # 检查 storage
        st = d.get('storage', {})
        if st.get('currentUser') != ESS_UID:
            issues.append(f'storage currentUser = {st.get("currentUser")}，不是本源UID')
        if not st.get('hasEssenceMark'):
            issues.append('storage 缺少本源标记')
        
        # 检查 JWT
        jwt = d.get('jwt', {})
        if not jwt.get('exists'):
            issues.append('JWT Token 不存在')
        
        if issues:
            print(f'  ⚠️ 发现 {len(issues)} 个问题:')
            for i, issue in enumerate(issues, 1):
                print(f'    {i}. {issue}')
            
            print(f'\n  🔍 根因推断:')
            print(f'    Trae CN 启动时可能重置了登录数据')
            print(f'    导致本源注入被覆盖')
            
            self.report['rootCause'] = issues
        else:
            print('  ✅ 所有检查项通过，本源数据完整')
            self.report['rootCause'] = []
    
    def _print_report(self):
        """打印报告"""
        print('\n' + '='*60)
        print('  📋 本源登录诊断报告')
        print('='*60)
        
        d = self.report
        
        print(f'\n  Local State:')
        ls = d.get('localState', {})
        print(f'    userId: {ls.get("userId", "?")}')
        print(f'    loginType: {ls.get("loginType", "?")}')
        
        print(f'\n  Storage:')
        st = d.get('storage', {})
        print(f'    currentUser: {st.get("currentUser", "?")}')
        print(f'    用户数: {st.get("userCount", "?")}')
        print(f'    认证键: {st.get("authKeyCount", "?")}')
        
        print(f'\n  State.vscdb:')
        vs = d.get('vscdb', {})
        print(f'    本源记录: {vs.get("essenceRows", "?")} 条')
        print(f'    传统记录: {vs.get("tradRows", "?")} 条')
        
        print(f'\n  JWT Token:')
        jwt = d.get('jwt', {})
        print(f'    存在: {jwt.get("exists", "?")}')
        
        issues = d.get('rootCause', [])
        if issues:
            print(f'\n  ❌ 问题:')
            for i, issue in enumerate(issues, 1):
                print(f'    {i}. {issue}')
        else:
            print(f'\n  ✅ 所有检查通过')
    
    def _banner(self) -> str:
        return """
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║   BSD × Trae CN — 本源登录状态深度诊断                                         ║
║                                                                                  ║
║   诊断目标:                                                                      ║
║   1. 检查用户数据目录中本源信息是否还存在                                      ║
║   2. 分析 Trae CN 启动时数据覆盖逻辑                                            ║
║   3. 确认账号信息显示的真正数据源                                                ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
        """


def main():
    diagnostic = EssenceLoginDiagnostic()
    report = diagnostic.run()
    
    # 保存报告
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(output_dir, 'BSD_EssenceLogin_Diagnostic_Report.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f'\n  📄 报告已保存: {output_file}')


if __name__ == '__main__':
    main()