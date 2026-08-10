#!/usr/bin/env python3
"""深度观测 — Trae CN 启动后 60 秒持续监测"""
import os, json, time, hashlib

STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
ESSENCE_UID = 'a5b7a8623fdea6b8'

def read_state():
    with open(STORAGE, 'r', encoding='utf-8') as f:
        s = json.load(f)
    g = s.get('icube_gtm', {})
    eu = g.get('users', {}).get(ESSENCE_UID, {})
    return {
        'time': time.strftime('%H:%M:%S'),
        'currentUser': g.get('currentUser', ''),
        'essence_status': eu.get('status', 'MISSING'),
        'essence_loggedIn': eu.get('isLoggedIn', 'MISSING'),
        'bsd_mode': s.get('_bsd_essence_mode', False),
        'logged_in': s.get('_logged_in', False),
        'icube_dc_len': len(s.get('iCubeAuthInfo://icube-dc:516094651277160', '')),
        'usertag_len': len(s.get('iCubeAuthInfo://usertag', '')),
        'jwt_exists': 'bsd_essence_jwt' in s,
        'total_keys': len(s),
    }

print('=== 深度观测 Trae CN 启动后行为 (60秒) ===')
print()

prev = None
for i in range(30):
    curr = read_state()
    
    # 检测变化
    changed = []
    if prev:
        for k, v in curr.items():
            if k == 'time':
                continue
            if prev.get(k) != v:
                changed.append(f'{k}: {prev.get(k)} → {v}')
    
    if changed or i == 0:
        print(f'[{curr["time"]}] (第{i*2+1}次)')
        for c in changed:
            print(f'  ⚡ 变化: {c}')
        if i == 0:
            for k, v in curr.items():
                if k != 'time':
                    print(f'  {k}: {v}')
    
    prev = curr
    time.sleep(2)

print(f'\n=== 最终状态 ({curr["time"]}) ===')
for k, v in curr.items():
    if k != 'time':
        print(f'  {k}: {v}')

# 分析
print('\n=== 分析 ===')
if curr['currentUser'] == ESSENCE_UID:
    print('✅ currentUser 仍为本源 UID')
else:
    print(f'❌ currentUser 被改为: {curr["currentUser"]}')

if curr['essence_status'] == 'active':
    print('✅ 本源用户仍为 active')
else:
    print(f'❌ 本源用户状态: {curr["essence_status"]}')

if curr['icube_dc_len'] > 100:
    print(f'✅ icube-dc 数据存在 (len={curr["icube_dc_len"]})')
else:
    print(f'❌ icube-dc 数据丢失 (len={curr["icube_dc_len"]})')
