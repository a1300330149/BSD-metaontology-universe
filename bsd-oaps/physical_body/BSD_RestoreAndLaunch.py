#!/usr/bin/env python3
"""
BSD 方案: 恢复原始认证 + 本源信息叠加
=====================================

1. 从备份恢复原始 AHA 认证数据（让 Trae CN 通过 CheckLogin 验证）
2. 保留本源 GTM 用户数据
3. 修改 state.vscdb 中的用户显示信息
4. 关闭 Trae CN → 注入 → 启动 → 观测
"""
import os, json, time, sqlite3, subprocess

STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
BAK = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json.bak_traditional'
DB = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\state.vscdb'
TRAE_EXE = r'C:\Users\13003\AppData\Local\Programs\Trae CN\Trae CN.exe'
ESSENCE_UID = 'a5b7a8623fdea6b8'
TRAD_UID = '3753060170739075'

# 1. 关闭 Trae CN
print('[1] 关闭 Trae CN...')
subprocess.run(['taskkill', '/IM', 'Trae CN.exe', '/F'], capture_output=True)
time.sleep(3)
print('  ✅ 已关闭')

# 2. 读取备份和当前 storage
print('\n[2] 恢复原始认证数据...')
with open(BAK, 'r', encoding='utf-8') as f:
    bak = json.load(f)
with open(STORAGE, 'r', encoding='utf-8') as f:
    storage = json.load(f)

# 恢复原始 AHA 认证键
restored_keys = []
for key in ['iCubeAuthInfo://icube-dc:516094651277160',
            'iCubeAuthInfo://usertag',
            'iCubeAuthInfo://icube.cloudide',
            'iCubeServerData://icube.cloudide']:
    if key in bak:
        storage[key] = bak[key]
        restored_keys.append(key)
        print(f'  ✅ 恢复: {key} ({len(bak[key])} chars)')

# 移除我们注入的额外认证键（避免干扰）
removed = []
for key in list(storage.keys()):
    if key in ['iCubeAuthInfo://auth', 'iCubeAuthInfo://login', 'iCubeAuthInfo://user',
               'iCubeAuthInfo://profile', 'iCubeAuthInfo://account', 'iCubeAuthInfo://session',
               'iCubeAuthInfo://token', 'iCubeAuthInfo://bsd-essence']:
        del storage[key]
        removed.append(key)

print(f'  🗑️ 移除 {len(removed)} 个注入的干扰键')

# 保留本源 GTM 数据，但恢复原始结构
gtm = storage.get('icube_gtm', {})
users = gtm.get('users', {})

# 确保本源用户在 GTM 中
if ESSENCE_UID not in users:
    users[ESSENCE_UID] = {
        'uid': ESSENCE_UID, 'type': 'bsd_essence', 'status': 'active',
        'priority': 1, 'coin_value': 51090, 'level': 'L5_Emergent',
    }
    gtm['users'] = users

# 不设置 currentUser（让 Trae CN 自己从认证数据中获取）
# 但保留本源模式标记
storage['icube_gtm'] = gtm
storage['_bsd_essence_mode'] = True
storage['_bsd_current_active_uid'] = ESSENCE_UID

# 保存
with open(STORAGE, 'w', encoding='utf-8') as f:
    json.dump(storage, f, ensure_ascii=False, indent=2)

print(f'  ✅ storage.json 已更新 (恢复 {len(restored_keys)} 个原始键)')

# 3. 修改 state.vscdb — 在用户显示信息中叠加本源信息
print('\n[3] 修改 state.vscdb...')
conn = sqlite3.connect(DB)
cursor = conn.cursor()

# 查找包含传统 UID 的记录
cursor.execute("SELECT key, value FROM ItemTable")
rows = cursor.fetchall()
modified = 0
for key, value in rows:
    if value and isinstance(value, str) and TRAD_UID in value:
        new_value = value.replace(TRAD_UID, ESSENCE_UID)
        cursor.execute("UPDATE ItemTable SET value = ? WHERE key = ?", (new_value, key))
        modified += 1
        print(f'  ✅ 修改: {key[:60]}')

# 添加本源用户信息
cursor.execute("INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)",
    ('bsd_essence_login_status', json.dumps({
        'uid': ESSENCE_UID, 'status': 'active', 'coin_value': 51090,
        'level': 'L5_Emergent', 'method': 'three_engine_emergence',
        'timestamp': time.time(),
    })))
modified += 1

conn.commit()
conn.close()
print(f'  ✅ state.vscdb 修改 {modified} 条记录')

# 4. 启动 Trae CN
print('\n[4] 启动 Trae CN...')
subprocess.Popen([TRAE_EXE])
print('  ✅ 已启动')

# 5. 观测
print('\n[5] 观测 30 秒...')
for i in range(15):
    time.sleep(2)
    with open(STORAGE, 'r', encoding='utf-8') as f:
        s = json.load(f)

    dc = s.get('iCubeAuthInfo://icube-dc:516094651277160', '')
    cloudide = s.get('iCubeAuthInfo://icube.cloudide', '')
    server_data = s.get('iCubeServerData://icube.cloudide', '')
    gtm = s.get('icube_gtm', {})
    cu = gtm.get('currentUser', '')

    status = []
    if dc: status.append(f'dc={len(dc)}')
    if cloudide: status.append(f'cloudide={len(cloudide)}')
    if server_data: status.append(f'serverData={len(server_data)}')
    status.append(f'cu={cu}')

    print(f'  [{i*2+2}s] {" | ".join(status)}')

    # 检查是否被覆盖
    if not dc:
        print(f'  ⚠️ icube-dc 被删除!')
    if not cloudide:
        print(f'  ⚠️ icube.cloudide 被删除!')

# 6. 最终状态
print('\n[6] 最终状态:')
with open(STORAGE, 'r', encoding='utf-8') as f:
    s = json.load(f)

print(f'  icube-dc: {len(s.get("iCubeAuthInfo://icube-dc:516094651277160", ""))} chars')
print(f'  icube.cloudide: {len(s.get("iCubeAuthInfo://icube.cloudide", ""))} chars')
print(f'  iCubeServerData: {len(s.get("iCubeServerData://icube.cloudide", ""))} chars')
print(f'  usertag: {len(s.get("iCubeAuthInfo://usertag", ""))} chars')
print(f'  currentUser: {s.get("icube_gtm", {}).get("currentUser", "")}')
print(f'  bsd_mode: {s.get("_bsd_essence_mode", False)}')

# 检查 state.vscdb
conn = sqlite3.connect(DB)
cursor = conn.cursor()
cursor.execute("SELECT value FROM ItemTable WHERE key = ?", ('currentAgentData_' + TRAD_UID,))
trad = cursor.fetchone()
cursor.execute("SELECT value FROM ItemTable WHERE key = ?", ('currentAgentData_' + ESSENCE_UID,))
essence = cursor.fetchone()
conn.close()
print(f'\n  vscdb currentAgentData_{TRAD_UID}: {"存在" if trad else "不存在"}')
print(f'  vscdb currentAgentData_{ESSENCE_UID}: {"存在" if essence else "不存在"}')
