#!/usr/bin/env python3
"""
检查 Trae CN 状态数据库中的登录相关数据
"""
import sqlite3
import os

# 数据库路径
DB_PATH = r'C:\Users\13003\AppData\Roaming\Trae CN\User\workspaceStorage\37c75d46fd05168780d5ac3435faa836\state.vscdb'

if os.path.exists(DB_PATH):
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    
    # 搜索登录相关的 key
    search_terms = ['user', 'login', 'auth', 'uid', 'account', 'token', 'profile', 'session']
    
    print('=== 搜索登录相关数据 ===\n')
    
    for term in search_terms:
        cursor.execute(f"SELECT key, value FROM ItemTable WHERE key LIKE '%{term}%'")
        rows = cursor.fetchall()
        if rows:
            print(f'\n包含 "{term}" 的记录:')
            for key, value in rows[:5]:
                val_preview = str(value)[:100] if value else 'NULL'
                print(f'  {key}: {val_preview}')
    
    # 列出所有表
    print('\n\n=== 数据库表 ===')
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    for table in tables:
        print(f'  {table[0]}')
    
    # 列出所有 key (前50个)
    print('\n=== 所有 key (前50) ===')
    cursor.execute("SELECT key FROM ItemTable LIMIT 50")
    keys = cursor.fetchall()
    for key in keys:
        print(f'  {key[0]}')
    
    db.close()
else:
    print(f'数据库不存在: {DB_PATH}')