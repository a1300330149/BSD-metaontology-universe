#!/usr/bin/env python3
"""探测Trae CN本地数据库中的登录状态"""
import sqlite3
import json
import os

def scan_db(path, max_rows=30):
    if not os.path.exists(path):
        print(f"  文件不存在: {path}")
        return
    print(f"\n{'='*60}")
    print(f"  数据库: {path}")
    print(f"{'='*60}")
    try:
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in cursor.fetchall()]
        print(f"  表: {tables}")
        
        for table in tables:
            cursor.execute(f"SELECT * FROM {table} LIMIT {max_rows}")
            rows = cursor.fetchall()
            print(f"\n  [{table}] ({len(rows)} 行)")
            for row in rows:
                row_str = str(row)
                if len(row_str) > 300:
                    row_str = row_str[:300] + '...'
                print(f"    {row_str}")
        conn.close()
    except Exception as e:
        print(f"  错误: {e}")

# 1. state.vscdb - 工作区状态
scan_db(r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\state.vscdb')

# 2. config.db - 本地配置
scan_db(r'C:\Users\13003\AppData\Roaming\Trae CN\Local Storage\config.db')

# 3. 检查 Local State (JSON)
local_state = r'C:\Users\13003\AppData\Roaming\Trae CN\Local State'
if os.path.exists(local_state):
    print(f"\n{'='*60}")
    print(f"  Local State")
    print(f"{'='*60}")
    with open(local_state, 'r', encoding='utf-8') as f:
        state = json.load(f)
    # 打印关键字段
    for key in ['os_crypt', 'profile', 'account', 'login', 'session']:
        if key in state:
            val = str(state[key])
            if len(val) > 300:
                val = val[:300] + '...'
            print(f"  {key}: {val}")

# 4. Cookies
cookies_db = r'C:\Users\13003\AppData\Roaming\Trae CN\Network\Cookies'
scan_db(cookies_db)

# 5. 检查本源端已有数据
print(f"\n{'='*60}")
print(f"  本源端数据目录")
print(f"{'='*60}")
essence_dir = r'C:\Users\13003\AppData\Roaming\Trae CN_Essence'
if os.path.exists(essence_dir):
    for root, dirs, files in os.walk(essence_dir):
        for f in files[:20]:
            fp = os.path.join(root, f)
            size = os.path.getsize(fp)
            rel = os.path.relpath(fp, essence_dir)
            print(f"    {rel} ({size} bytes)")
else:
    print(f"  本源端目录尚未创建")

# 6. AHA 目录
print(f"\n{'='*60}")
print(f"  AHA 认证目录")
print(f"{'='*60}")
aha_dir = r'C:\Users\13003\AppData\Roaming\Trae CN\aha'
if os.path.exists(aha_dir):
    for f in os.listdir(aha_dir):
        fp = os.path.join(aha_dir, f)
        if os.path.isfile(fp):
            size = os.path.getsize(fp)
            print(f"    {f} ({size} bytes)")
        else:
            print(f"    {f}/")
else:
    print(f"  AHA 目录不存在")

print("\n完成探测")