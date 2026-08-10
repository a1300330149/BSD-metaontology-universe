import sqlite3
import json
import os

# Search both TRAE SOLO CN and Trae CN user data directories
search_paths = [
    r'C:\Users\13003\AppData\Roaming\TRAE SOLO CN\User\globalStorage\state.vscdb',
    r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\state.vscdb',
    r'C:\Users\13003\AppData\Roaming\TRAE SOLO CN\User\globalStorage\storage.vscdb',
    r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.vscdb',
]

keywords = ['token', 'auth', 'login', 'cookie', 'jwt', 'cloud', 'session']

for db_path in search_paths:
    if os.path.exists(db_path):
        print(f"\n{'='*60}")
        print(f"Searching in: {db_path}")
        print('='*60)
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get all table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print(f"Tables found: {tables}")
            
            if tables:
                table_name = tables[0][0]  # First table
                
                # Get all column names
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                print(f"Columns: {[col[1] for col in columns]}")
                
                # Search for auth-related keys
                for kw in keywords:
                    try:
                        cursor.execute(f"SELECT key, value FROM {table_name} WHERE key LIKE ?", (f'%{kw}%',))
                        rows = cursor.fetchall()
                        if rows:
                            print(f"\n  [{kw}] Found {len(rows)} entries:")
                            for key, value in rows:
                                val_str = str(value)[:300] if value else "NULL"
                                print(f"    {key}: {val_str}")
                                if len(str(value)) > 300:
                                    print(f"      ... ({len(str(value))} chars total)")
                    except Exception as e:
                        print(f"  [{kw}] Error: {e}")
            
            conn.close()
        except Exception as e:
            print(f"Error accessing {db_path}: {e}")
    else:
        print(f"File not found: {db_path}")
