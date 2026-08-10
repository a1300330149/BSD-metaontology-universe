import re

MAIN_JS = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app\out\main.js'

with open(MAIN_JS, 'r', encoding='utf-8') as f:
    code = f.read()

print('=== 本源登录状态验证 ===')
print()

# 1. 检查Jx函数
m = re.search(r'Jx=\(t,e,i\)=>\(\{[^}]{0,500}\}\)', code)
if m:
    jx = m.group(0)
    has_username = 'username' in jx
    print(f'1. Jx包含username: {has_username}')
    print(f'   Jx预览: {jx[:150]}...')

# 2. 检查getter
for term in ['isLoginTraeUser(){return!1', 'isBytedanceUser(){return!1', 'isBusinessUser(){return!1']:
    found = term in code
    print(f'2. {term[:25]}: {found}')

# 3. 检查Die函数
die_ok = 'function Die(t){return"unknown"}' in code
print(f'3. Die返回unknown: {die_ok}')

# 4. 检查无残留
no_bsd = 'BSD本源用户' not in code
no_email = 'bsd@essence.local' not in code
print(f'4. 无BSD本源用户: {no_bsd}')
print(f'5. 无bsd@essence.local: {no_email}')

print()
if not has_username and die_ok and no_bsd and no_email:
    print('✅ 本源登录模式正确：无用户显示信息')
else:
    print('⚠️ 需要调整')
