import os

MAIN_JS = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app\out\main.js'
BACKUP = MAIN_JS + '.bak_bsd'

if os.path.exists(BACKUP):
    print('Found backup')
    with open(BACKUP, 'r', encoding='utf-8') as f:
        backup = f.read()
    
    checks = [
        ('isLoginTraeUser(){return this' in backup, 'original isLoginTraeUser'),
        ('isBytedanceUser(){return this' in backup, 'original isBytedanceUser'),
        ('get isBusinessUser(){return this' in backup, 'original isBusinessUser'),
        ('function Die(t){return t' in backup, 'original Die function'),
    ]
    for ok, desc in checks:
        status = 'OK' if ok else 'MISSING'
        print(f'  [{status}] {desc}')
else:
    print('No backup found')
