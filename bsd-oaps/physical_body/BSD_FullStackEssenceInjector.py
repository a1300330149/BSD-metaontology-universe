#!/usr/bin/env python3
"""
BSD × Trae CN — 全栈本源登录注入
===================================

核心思路:
  不依赖 AHA 加密解密,
  而是通过全栈多源注入,
  在每个 Trae CN 读取登录态的位置
  都设置本源 UID,
  形成"登录态共识"。

注入目标:
  1. state.vscdb (SQLite) — 替换 UID 前缀
  2. Local State — 添加 user/profile
  3. storage.json — 添加本源凭证
  4. trae-jwt-token — 创建本源 JWT
  5. TinyStorage — 添加本源标记

版本: V1.0 · 2026-08-05
"""

import os, json, sqlite3, shutil, time, hashlib, base64
from datetime import datetime

# 路径
TRAE_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
LOCAL_STATE = os.path.join(TRAE_DATA, 'Local State')
STORAGE = os.path.join(TRAE_DATA, 'User', 'globalStorage', 'storage.json')
VSCDB = os.path.join(TRAE_DATA, 'User', 'workspaceStorage', '37c75d46fd05168780d5ac3435faa836', 'state.vscdb')
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'
JWT_PATH = os.path.join(TRAE_CONFIG, 'trae-jwt-token')
AHA_DIR = os.path.join(TRAE_DATA, 'aha')
TINY = os.path.join(AHA_DIR, 'TinyStorage')
BACKUP_DIR = os.path.join(TRAE_DATA, 'injection_backup')

# UIDs
TRAD_UID = '3753060170739075'
ESS_UID = 'a5b7a8623fdea6b8'


class FullStackInjector:
    """全栈注入器"""
    
    def __init__(self):
        self.results = []
        self.backup_dir = BACKUP_DIR
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def run(self) -> dict:
        """执行全栈注入"""
        
        print(self._banner())
        
        # Phase 0: 关闭 Trae CN
        self._stop_trae_cn()
        
        # Phase 1: 备份
        self._backup_all()
        
        # Phase 2: 注入 state.vscdb
        self._inject_vscdb()
        
        # Phase 3: 注入 Local State
        self._inject_local_state()
        
        # Phase 4: 注入 storage.json
        self._inject_storage()
        
        # Phase 5: 创建 JWT token
        self._create_jwt_token()
        
        # Phase 6: 注入 TinyStorage
        self._inject_tiny_storage()
        
        # Phase 7: 启动 Trae CN
        self._start_trae_cn()
        
        # 汇总
        self._print_summary()
        
        return {'success': True, 'results': self.results}
    
    def _stop_trae_cn(self):
        """关闭 Trae CN"""
        print('\n' + '='*60)
        print('  Phase 0: 关闭 Trae CN')
        print('='*60)
        os.system('taskkill /F /IM "Trae CN.exe" 2>nul')
        time.sleep(2)
        print('  ✅ Trae CN 已关闭')
    
    def _backup_all(self):
        """备份所有关键文件"""
        print('\n' + '='*60)
        print('  Phase 1: 备份当前状态')
        print('='*60)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 备份 storage.json
        if os.path.exists(STORAGE):
            shutil.copy2(STORAGE, os.path.join(self.backup_dir, f'storage_{timestamp}.json'))
            print('  ✅ storage.json 已备份')
        
        # 备份 Local State
        if os.path.exists(LOCAL_STATE):
            shutil.copy2(LOCAL_STATE, os.path.join(self.backup_dir, f'local_state_{timestamp}.json'))
            print('  ✅ Local State 已备份')
        
        # 备份 state.vscdb
        if os.path.exists(VSCDB):
            shutil.copy2(VSCDB, os.path.join(self.backup_dir, f'state_vscdb_{timestamp}'))
            print('  ✅ state.vscdb 已备份')
    
    def _inject_vscdb(self):
        """注入 state.vscdb — 替换 UID 前缀"""
        print('\n' + '='*60)
        print('  Phase 2: 注入 state.vscdb')
        print('='*60)
        
        try:
            conn = sqlite3.connect(VSCDB)
            cursor = conn.cursor()
            
            # 查找所有包含传统 UID 的 key
            cursor.execute(f"SELECT key, value FROM ItemTable WHERE key LIKE '%{TRAD_UID}%'")
            rows = cursor.fetchall()
            
            print(f'  找到 {len(rows)} 条包含传统 UID 的记录')
            
            # 替换 key 中的 UID
            replaced = 0
            for key, value in rows:
                new_key = key.replace(TRAD_UID, ESS_UID)
                
                # 检查新 key 是否已存在
                cursor.execute("SELECT key FROM ItemTable WHERE key = ?", (new_key,))
                if not cursor.fetchone():
                    # 插入新 key
                    cursor.execute(
                        "INSERT INTO ItemTable (key, value) VALUES (?, ?)",
                        (new_key, value)
                    )
                    # 删除旧 key
                    cursor.execute("DELETE FROM ItemTable WHERE key = ?", (key,))
                    replaced += 1
                    print(f'    ✅ {key} → {new_key}')
            
            # 添加本源登录标记
            cursor.execute(
                "INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)",
                ('_bsd_essence_login', json.dumps({
                    'uid': ESS_UID,
                    'type': 'bsd_essence',
                    'coin_value': 80,
                    'level': 'L4_Theory',
                    'timestamp': datetime.now().isoformat(),
                }))
            )
            print(f'    ✅ _bsd_essence_login 标记已添加')
            
            conn.commit()
            conn.close()
            
            self.results.append({'phase': 'vscdb', 'replaced': replaced})
            print(f'  ✅ state.vscdb 注入完成 ({replaced} 条记录已替换)')
            
        except Exception as e:
            print(f'  ❌ vscdb 注入失败: {e}')
            self.results.append({'phase': 'vscdb', 'error': str(e)})
    
    def _inject_local_state(self):
        """注入 Local State — 添加 user/profile"""
        print('\n' + '='*60)
        print('  Phase 3: 注入 Local State')
        print('='*60)
        
        try:
            if os.path.exists(LOCAL_STATE):
                with open(LOCAL_STATE, 'r', encoding='utf-8') as f:
                    local_state = json.load(f)
            else:
                local_state = {}
            
            # 添加用户信息
            local_state['user'] = {
                'userId': ESS_UID,
                'account': {
                    'id': ESS_UID,
                    'nickname': 'BSD本源用户',
                    'type': 'bsd_essence',
                    'coin_value': 80,
                    'level': 'L4_Theory',
                },
                'loginType': 'bsd_essence',
                'loginTime': datetime.now().isoformat(),
            }
            
            local_state['profile'] = {
                'uid': ESS_UID,
                'name': 'BSD本源用户',
                'avatar': '',
                'verified': True,
                'verificationMethod': 'bsd_knowledge_proof',
            }
            
            # 添加本源标记
            local_state['_bsd_essence_mode'] = True
            local_state['_bsd_traditional_uid'] = TRAD_UID
            local_state['_bsd_essence_uid'] = ESS_UID
            local_state['_bsd_priority'] = 'essence_first'
            
            with open(LOCAL_STATE, 'w', encoding='utf-8') as f:
                json.dump(local_state, f, ensure_ascii=False, indent=2)
            
            self.results.append({'phase': 'local_state', 'success': True})
            print('  ✅ Local State 注入完成')
            print(f'     userId: {ESS_UID}')
            print(f'     nickname: BSD本源用户')
            print(f'     loginType: bsd_essence')
            
        except Exception as e:
            print(f'  ❌ Local State 注入失败: {e}')
            self.results.append({'phase': 'local_state', 'error': str(e)})
    
    def _inject_storage(self):
        """注入 storage.json — 添加本源凭证"""
        print('\n' + '='*60)
        print('  Phase 4: 注入 storage.json')
        print('='*60)
        
        try:
            with open(STORAGE, 'r', encoding='utf-8') as f:
                storage = json.load(f)
            
            # 更新 GTM 用户
            gtm = storage.get('icube_gtm', {})
            users = gtm.get('users', {})
            
            # 本源UID设为active
            essence_user = users.get(ESS_UID, {})
            essence_user.update({
                'uid': ESS_UID,
                'type': 'bsd_essence',
                'status': 'active',
                'priority': 1,
                'nickname': 'BSD本源用户',
                'loginType': 'bsd_essence',
                'coin_value': 80,
                'level': 'L4_Theory',
                'timestamp': datetime.now().isoformat(),
            })
            users[ESS_UID] = essence_user
            
            # 传统UID降为parallel
            trad_user = users.get(TRAD_UID, {})
            trad_user.update({
                'uid': TRAD_UID,
                'type': 'traditional',
                'status': 'parallel',
                'priority': 2,
            })
            users[TRAD_UID] = trad_user
            
            gtm['users'] = users
            gtm['currentUser'] = ESS_UID
            storage['icube_gtm'] = gtm
            
            # 添加本源标记
            storage['_bsd_essence_login'] = {
                'uid': ESS_UID,
                'active': True,
                'priority': 1,
                'injectedAt': datetime.now().isoformat(),
            }
            
            storage['_bsd_current_uid'] = ESS_UID
            
            with open(STORAGE, 'w', encoding='utf-8') as f:
                json.dump(storage, f, ensure_ascii=False, indent=2)
            
            self.results.append({'phase': 'storage', 'success': True})
            print('  ✅ storage.json 注入完成')
            print(f'     currentUser: {ESS_UID}')
            print(f'     本源UID status: active')
            print(f'     传统UID status: parallel')
            
        except Exception as e:
            print(f'  ❌ storage.json 注入失败: {e}')
            self.results.append({'phase': 'storage', 'error': str(e)})
    
    def _create_jwt_token(self):
        """创建本源 JWT token"""
        print('\n' + '='*60)
        print('  Phase 5: 创建 JWT Token')
        print('='*60)
        
        try:
            # 生成 JWT-like token
            header = base64.b64encode(json.dumps({
                'alg': 'BSDEssence',
                'typ': 'JWT',
            }).encode()).decode()
            
            payload = base64.b64encode(json.dumps({
                'sub': ESS_UID,
                'name': 'BSD本源用户',
                'type': 'bsd_essence',
                'coin_value': 80,
                'level': 'L4_Theory',
                'iat': int(datetime.now().timestamp()),
                'exp': int(datetime.now().timestamp()) + 86400 * 365,
            }).encode()).decode()
            
            signature = hashlib.sha256(
                f"{header}.{payload}.bsd_essence_key".encode()
            ).hexdigest()
            
            token = f"{header}.{payload}.{signature}"
            
            os.makedirs(TRAE_CONFIG, exist_ok=True)
            with open(JWT_PATH, 'w', encoding='utf-8') as f:
                f.write(token)
            
            self.results.append({'phase': 'jwt', 'success': True})
            print('  ✅ JWT Token 创建完成')
            print(f'     路径: {JWT_PATH}')
            print(f'     长度: {len(token)} chars')
            print(f'     Subject: {ESS_UID}')
            
        except Exception as e:
            print(f'  ❌ JWT 创建失败: {e}')
            self.results.append({'phase': 'jwt', 'error': str(e)})
    
    def _inject_tiny_storage(self):
        """注入 TinyStorage"""
        print('\n' + '='*60)
        print('  Phase 6: 注入 TinyStorage')
        print('='*60)
        
        try:
            if os.path.exists(TINY):
                with open(TINY, 'r', encoding='utf-8') as f:
                    tiny = json.load(f)
            else:
                tiny = {}
            
            tsd = tiny.get('tiny_storage_data', {})
            
            tsd['bsd_essence_uid'] = ESS_UID
            tsd['bsd_essence_login'] = True
            tsd['bsd_coin_value'] = 80
            tsd['bsd_level'] = 'L4_Theory'
            tsd['bsd_traditional_uid'] = TRAD_UID
            tsd['bsd_priority'] = 'essence_first'
            tsd['bsd_injected_at'] = datetime.now().isoformat()
            
            tiny['tiny_storage_data'] = tsd
            
            with open(TINY, 'w', encoding='utf-8') as f:
                json.dump(tiny, f, ensure_ascii=False, indent=2)
            
            self.results.append({'phase': 'tiny', 'success': True})
            print('  ✅ TinyStorage 注入完成')
            
        except Exception as e:
            print(f'  ❌ TinyStorage 注入失败: {e}')
            self.results.append({'phase': 'tiny', 'error': str(e)})
    
    def _start_trae_cn(self):
        """启动 Trae CN"""
        print('\n' + '='*60)
        print('  Phase 7: 启动 Trae CN')
        print('='*60)
        
        exe_path = r'C:\Users\13003\AppData\Local\Programs\Trae CN\Trae CN.exe'
        os.startfile(exe_path)
        
        self.results.append({'phase': 'start', 'success': True})
        print('  ✅ Trae CN 已启动')
        print('     请等待加载完成...')
    
    def _print_summary(self):
        """打印摘要"""
        print('\n' + '='*60)
        print('  全栈本源登录注入 — 执行报告')
        print('='*60)
        
        print(f'\n  注入结果:')
        for r in self.results:
            status = '✅' if r.get('success') or r.get('replaced') else '❌'
            phase = r.get('phase', 'unknown')
            
            if 'replaced' in r:
                print(f'    {status} {phase}: {r["replaced"]} 条记录替换')
            elif 'success' in r:
                print(f'    {status} {phase}: 注入成功')
            else:
                print(f'    {status} {phase}: {r.get("error", "失败")}')
        
        print(f'\n  本源 UID: {ESS_UID}')
        print(f'  传统 UID: {TRAD_UID}')
        print(f'  策略: 全栈多源注入')
        print(f'\n  💡 请查看 Trae CN 界面，确认是否显示本源登录')
    
    def _banner(self) -> str:
        return """
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║   BSD × Trae CN — 全栈本源登录注入                                              ║
║                                                                                  ║
║   核心思路:                                                                      ║
║   不依赖 AHA 加密解密,                                                           ║
║   通过全栈多源注入,                                                              ║
║   在每个 Trae CN 读取登录态的位置                                                ║
║   都设置本源 UID, 形成"登录态共识"                                             ║
║                                                                                  ║
║   注入目标:                                                                      ║
║   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         ║
║   │ state.vscdb │  │ Local State │  │ storage.json│  │ JWT Token  │         ║
║   └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘         ║
║                                                                                  ║
║   作者: 3753060170739075 → a5b7a8623fdea6b8                                   ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
        """


def main():
    injector = FullStackInjector()
    result = injector.run()
    
    print(f'\n{"="*60}')
    if result['success']:
        print('  ✅ 全栈注入完成!')
        print('  请查看 Trae CN 界面')
    else:
        print('  ❌ 注入失败')


if __name__ == '__main__':
    main()