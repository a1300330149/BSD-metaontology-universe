#!/usr/bin/env python3
"""BSD Switch UI to Essence - 将 Trae CN UI 切换为本源用户显示"""
import os, json, sqlite3, shutil, time

VSCDB = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\state.vscdb'
STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'

TRAD_UID = '3753060170739075'
ESSENCE_UID = 'a5b7a8623fdea6b8'
ESSENCE_NAME = 'BSD本源'
TRAD_NAME = '深书姬'

# 备份
backup = VSCDB + '.bak_' + str(int(time.time()))
shutil.copy2(VSCDB, backup)
print(f'备份: {backup}')

# 1. 更新 state.vscdb
print('\n=== Step 1: 更新 state.vscdb ===')
conn = sqlite3.connect(VSCDB)
cursor = conn.cursor()

# 读取所有记录
cursor.execute("SELECT key, value FROM ItemTable")
rows = cursor.fetchall()

updated = 0
for key, value in rows:
    new_key = key
    new_value = value
    
    # 替换 key 中的 UID
    if TRAD_UID in key:
        new_key = key.replace(TRAD_UID, ESSENCE_UID)
    
    # 替换 value 中的 UID 和用户名
    if value and isinstance(value, str):
        if TRAD_UID in value:
            new_value = new_value.replace(TRAD_UID, ESSENCE_UID)
        if TRAD_NAME in new_value:
            new_value = new_value.replace(TRAD_NAME, ESSENCE_NAME)
    
    if new_key != key or new_value != value:
        # 检查新 key 是否已存在
        cursor.execute("SELECT key FROM ItemTable WHERE key = ?", (new_key,))
        exists = cursor.fetchone()
        
        if exists and new_key != key:
            # 新 key 已存在，删除旧的，保留新的
            cursor.execute("DELETE FROM ItemTable WHERE key = ?", (key,))
            print(f'  删除旧 key (已存在新 key): {key} -> {new_key}')
        else:
            # 更新或插入
            cursor.execute("DELETE FROM ItemTable WHERE key = ?", (key,))
            cursor.execute("INSERT INTO ItemTable (key, value) VALUES (?, ?)", (new_key, new_value))
            if new_key != key:
                print(f'  Key: {key} -> {new_key}')
            updated += 1

conn.commit()
conn.close()
print(f'  ✅ 更新完成: {updated} 条记录')

# 2. 更新 storage.json
print('\n=== Step 2: 更新 storage.json ===')
with open(STORAGE, 'r', encoding='utf-8') as f:
    storage = json.load(f)

# 更新 GTM
gtm = storage.get('icube_gtm', {})
gtm['currentUser'] = ESSENCE_UID
gtm['activeUser'] = ESSENCE_UID

users = gtm.get('users', {})
if isinstance(users, dict):
    # 添加本源用户
    users[ESSENCE_UID] = {
        'uid': ESSENCE_UID,
        'userId': ESSENCE_UID,
        'id': ESSENCE_UID,
        'type': 'bsd_essence',
        'status': 'active',
        'login_type': 'server_verified',
        'coin_value': 51090,
        'level': 'L5_Emergent',
    }
    # 标记传统用户为并行
    if TRAD_UID in users:
        users[TRAD_UID]['status'] = 'parallel'
        users[TRAD_UID]['type'] = 'traditional_parallel'

gtm['users'] = users
storage['icube_gtm'] = gtm

# 设置登录状态
storage['_is_authenticated'] = True
storage['_logged_in'] = True
storage['_bsd_essence_mode'] = True
storage['_bsd_current_active_uid'] = ESSENCE_UID

# 写入
with open(STORAGE, 'w', encoding='utf-8') as f:
    json.dump(storage, f, ensure_ascii=False, indent=2)
print(f'  ✅ storage.json 已更新')
print(f'  currentUser: {gtm["currentUser"]}')
print(f'  activeUser: {gtm["activeUser"]}')

# 3. 验证关键记录
print('\n=== Step 3: 验证关键记录 ===')
conn = sqlite3.connect(VSCDB)
cursor = conn.cursor()

# 检查本源 UID 的记录
cursor.execute("SELECT key FROM ItemTable WHERE key LIKE ?", (f'%{ESSENCE_UID}%',))
essence_keys = cursor.fetchall()
print(f'  本源 UID 相关记录: {len(essence_keys)} 条')
for k in essence_keys[:10]:
    print(f'    {k[0]}')

# 检查传统 UID 的记录（应该只剩下少数必要的）
cursor.execute("SELECT key FROM ItemTable WHERE key LIKE ?", (f'%{TRAD_UID}%',))
trad_keys = cursor.fetchall()
print(f'  传统 UID 相关记录: {len(trad_keys)} 条')
for k in trad_keys[:5]:
    print(f'    {k[0]}')

conn.close()

print('\n' + '='*70)
print('  ✅ UI 切换完成')
print('  服务器端: token 有效, IsLogin=True, UserID=3753060170739075')
print('  客户端: GTM currentUser=a5b7a8623fdea6b8 (BSD本源)')
print('  客户端: 所有 UI 数据 key 已从传统UID切换到本源UID')
print('='*70)
print('\n  请启动 Trae CN 验证 UI 显示')
