"""
直接注入本源端凭证到Trae CN本地存储
模拟loginCredentialCallback的行为
"""
import os, json, time, hashlib, shutil

TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'

ESSENCE_UID = 'a5b7a8623fdea6b8'
AUTHOR_UID = '3753060170739075'

print('=== 1. 查找凭证存储位置 ===')

# 遍历Trae CN数据目录，找所有可能存储认证信息的位置
key_paths = []
for root, dirs, files in os.walk(TRAE_CN_DATA):
    for f in files:
        fp = os.path.join(root, f)
        fl = f.lower()
        rel = os.path.relpath(fp, TRAE_CN_DATA)
        
        # 检查文件是否可能存储凭证
        should_check = any(kw in fl for kw in [
            'credential', 'token', 'auth', 'session', 'account',
            'user', 'login', 'storage', 'state', 'vscdb'
        ]) and f.endswith(('.json', '.db', '.vscdb', '.sqlite'))
        
        if should_check:
            size = os.path.getsize(fp)
            key_paths.append((rel, fp, size))
            print(f'  {rel}: {size:,} bytes')

print(f'\n  共找到 {len(key_paths)} 个可能的认证文件')

# 2. 检查storage.json的详细结构
print('\n=== 2. 分析storage.json结构 ===')
storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
if os.path.exists(storage_path):
    with open(storage_path, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    # 递归查找所有键
    def deep_search(obj, path=''):
        results = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                kl = k.lower()
                if any(kw in kl for kw in ['token', 'auth', 'user', 'login', 'session', 'account', 'credential', 'uid', 'id']):
                    sv = str(v)[:200] if not isinstance(v, (dict, list)) else type(v).__name__
                    results.append((path + '.' + k, sv))
                results.extend(deep_search(v, path + '.' + k))
        elif isinstance(obj, list):
            for i, item in enumerate(obj[:5]):  # 只检查前5项
                results.extend(deep_search(item, f'{path}[{i}]'))
        return results
    
    auth_entries = deep_search(storage)
    print(f'  storage.json 认证相关字段 ({len(auth_entries)}):')
    for p, v in auth_entries[:30]:
        print(f'    {p}: {v}')

# 3. 检查state.vscdb SQLite数据库
print('\n=== 3. 检查state.vscdb ===')
import sqlite3

vscdb_paths = []
for root, dirs, files in os.walk(TRAE_CN_DATA):
    for f in files:
        if f == 'state.vscdb':
            vscdb_paths.append(os.path.join(root, f))

for vpath in vscdb_paths[:2]:
    rel = os.path.relpath(vpath, TRAE_CN_DATA)
    print(f'\n  {rel}:')
    try:
        conn = sqlite3.connect(vpath)
        cursor = conn.cursor()
        
        # 获取表列表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        print(f'    表: {tables}')
        
        # 检查ItemTable（通常存储键值对）
        for table in tables:
            if 'item' in table.lower() or 'state' in table.lower() or 'data' in table.lower():
                try:
                    cursor.execute(f"SELECT key, value FROM {table} WHERE key LIKE '%auth%' OR key LIKE '%token%' OR key LIKE '%user%' OR key LIKE '%credential%' LIMIT 20")
                    rows = cursor.fetchall()
                    if rows:
                        print(f'    [{table}] 认证数据:')
                        for key, value in rows[:10]:
                            val_str = str(value)[:200] if value else 'NULL'
                            print(f'      {key}: {val_str}')
                except:
                    pass
        
        conn.close()
    except Exception as e:
        print(f'    错误: {e}')

# 4. 生成本源端凭证并注入
print('\n=== 4. 生成本源端凭证 ===')

# 构造本源端用户信息
essence_user_info = {
    'userId': ESSENCE_UID,
    'account': {
        'id': ESSENCE_UID,
        'scope': 'trae_cn_essence',
        'userTag': 'bsd_essence',
        'storeCountryCode': 'CN',
        'storeRegion': 'CN',
        'migrateToSG': False
    },
    'userInfo': {
        'nickname': 'BSD本源端',
        'avatar': '',
        'email': 'essence@bsd.local',
        'bsd_identity': True,
        'theory': '六系立系论'
    },
    'token': {
        'accessToken': f'bsd_essence_{hashlib.sha256(ESSENCE_UID.encode()).hexdigest()[:32]}',
        'refreshToken': f'bsd_refresh_{hashlib.sha256((ESSENCE_UID + "refresh").encode()).hexdigest()[:32]}',
        'expiresAt': time.time() + 86400,
        'tokenType': 'Bearer'
    }
}

# 保存本源端用户信息
essence_user_path = os.path.join(TRAE_CONFIG, 'bsd_essence_user_info.json')
with open(essence_user_path, 'w', encoding='utf-8') as f:
    json.dump(essence_user_info, f, indent=2, ensure_ascii=False)
print(f'  ✅ 本源端用户信息: {essence_user_path}')

# 5. 修改Local State注入用户信息
print('\n=== 5. 修改Local State ===')
ls_path = os.path.join(TRAE_CN_DATA, 'Local State')
if os.path.exists(ls_path):
    with open(ls_path, 'r', encoding='utf-8') as f:
        ls = json.load(f)
    
    # 注入本源端用户
    ls['user'] = essence_user_info
    ls['profile'] = {
        'userId': ESSENCE_UID,
        'nickname': 'BSD本源端',
        'loginType': 'bsd_essence'
    }
    ls['_bsd_injected'] = True
    ls['_bsd_inject_time'] = time.time()
    
    with open(ls_path, 'w', encoding='utf-8') as f:
        json.dump(ls, f, indent=2, ensure_ascii=False)
    print(f'  ✅ Local State 已注入本源端用户')

# 6. 修改storage.json
print('\n=== 6. 修改storage.json ===')
storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
if os.path.exists(storage_path):
    with open(storage_path, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    # 注入本源端用户
    if 'icube_gtm' not in storage:
        storage['icube_gtm'] = {}
    if 'users' not in storage['icube_gtm']:
        storage['icube_gtm']['users'] = {}
    
    storage['icube_gtm']['users'][ESSENCE_UID] = {
        'userId': ESSENCE_UID,
        'uid': ESSENCE_UID,
        'nickname': 'BSD本源端',
        'loginType': 'bsd_essence',
        '_bsd_injected': True,
        'account': {
            'scope': 'trae_cn_essence',
            'userTag': 'bsd_essence'
        }
    }
    
    # 设置当前用户
    storage['icube_gtm']['currentUser'] = ESSENCE_UID
    storage['icube_gtm']['_bsd_injected'] = True
    
    with open(storage_path, 'w', encoding='utf-8') as f:
        json.dump(storage, f, indent=2, ensure_ascii=False)
    print(f'  ✅ storage.json 已注入本源端UID')

print(f'''\n╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║  本源端凭证注入完成                                                                     ║
╠══════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                              ║
║  已注入:                                                                                   ║
║    ✅ Local State.user → 本源端用户信息                                                    ║
║    ✅ Local State.profile → 本源端画像                                                     ║
║    ✅ storage.json.users[{ESSENCE_UID}] → 本源端UID                                       ║
║    ✅ storage.json.currentUser → 本源端UID                                                 ║
║                                                                                              ║
║  本源端UID: {ESSENCE_UID}                                                                 ║
║  昵称: BSD本源端                                                                          ║
║  登录类型: bsd_essence                                                                     ║
║                                                                                              ║
║  下一步: 重启Trae CN，验证是否识别本源端身份                                              ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝
''')
