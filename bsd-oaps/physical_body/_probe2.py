import json, os, sqlite3

vscdb = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\state.vscdb'
conn = sqlite3.connect(vscdb)
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in cur.fetchall()]
print('Tables:', tables)
for t in tables:
    cur.execute(f'SELECT * FROM {t}')
    rows = cur.fetchall()
    print(f'\n[{t}] {len(rows)} rows')
    for r in rows[:30]:
        s = str(r)
        if len(s) > 300: s = s[:300]+'...'
        print(f'  {s}')
conn.close()

# Also check Local State
local = r'C:\Users\13003\AppData\Roaming\Trae CN\Local State'
with open(local, 'r', encoding='utf-8') as f:
    state = json.load(f)
print('\n=== Local State ===')
for k,v in state.items():
    sv = str(v)
    if len(sv) > 200: sv = sv[:200]+'...'
    print(f'  {k}: {sv}')

# AHA TinyStorage
tiny = r'C:\Users\13003\AppData\Roaming\Trae CN\aha\TinyStorage'
with open(tiny, 'r', encoding='utf-8') as f:
    data = json.load(f)
print('\n=== AHA TinyStorage ===')
print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])

# AHA Remote_State
remote = r'C:\Users\13003\AppData\Roaming\Trae CN\aha\Remote_State'
with open(remote, 'r', encoding='utf-8') as f:
    data = json.load(f)
print('\n=== AHA Remote_State ===')
print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])