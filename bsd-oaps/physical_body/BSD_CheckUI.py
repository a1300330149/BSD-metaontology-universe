#!/usr/bin/env python3
"""Check Trae CN UI state"""
import json, sqlite3

VSCDB = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\state.vscdb'
conn = sqlite3.connect(VSCDB)
cursor = conn.cursor()

cursor.execute("SELECT key, value FROM ItemTable WHERE key LIKE '%agent%'")
rows = cursor.fetchall()
for key, value in rows:
    val_str = str(value)[:500] if value else 'None'
    print(f'{key}: {val_str}')
    print()

cursor.execute("SELECT key, value FROM ItemTable WHERE key LIKE '%Agent%'")
rows = cursor.fetchall()
for key, value in rows:
    val_str = str(value)[:500] if value else 'None'
    print(f'{key}: {val_str}')
    print()

cursor.execute("SELECT key, value FROM ItemTable WHERE key LIKE '%solo%'")
rows = cursor.fetchall()
for key, value in rows[:10]:
    val_str = str(value)[:300] if value else 'None'
    print(f'{key}: {val_str}')
    print()

conn.close()
