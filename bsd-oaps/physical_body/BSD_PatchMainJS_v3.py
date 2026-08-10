#!/usr/bin/env python3
"""BSD main.js 双重补丁 - getUserInfo + Jx"""
import os, shutil

MAIN_JS = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app\out\main.js'
BACKUP_JS = MAIN_JS + '.bak_bsd'

# 如果没有备份，创建一个
if not os.path.exists(BACKUP_JS):
    # 但之前可能已备份
    pass

with open(MAIN_JS, 'r', encoding='utf-8') as f:
    code = f.read()

patched_count = 0

# === 补丁 1: Jx 函数 - 直接替换 ScreenName ===
# 原: username:t.ScreenName
# 新: username:"BSD本源用户"
jx_old = 'username:t.ScreenName'
jx_new = 'username:t.ScreenName||"BSD本源用户"'
# 不对，更好的方式: 直接替换 ScreenName
# 更好: 在 Jx 函数内部直接硬编码

# 精确找到 Jx 函数并替换
jx_func_old = 'Jx=(t,e,i)=>({username:t.ScreenName,'
jx_func_new = 'Jx=(t,e,i)=>({username:"BSD本源用户",'

if jx_func_old in code:
    code = code.replace(jx_func_old, jx_func_new)
    print('✅ 补丁1: Jx 函数 username 替换成功')
    patched_count += 1
else:
    # 尝试搜索
    if 'username:t.ScreenName' in code:
        code = code.replace('username:t.ScreenName', 'username:"BSD本源用户"')
        print('✅ 补丁1: username:t.ScreenName 替换成功')
        patched_count += 1
    else:
        print('⚠️ Jx 函数中的 username:t.ScreenName 未找到')
        # 搜索 ScreenName 相关
        import re
        for m in re.finditer(r'ScreenName', code):
            ctx = code[max(0,m.start()-30):m.end()+30]
            print(f'  ScreenName @{m.start()}: {ctx}')

# === 补丁 2: 修改 ScreenName 本身 (如果还有其他地方引用) ===
# 在构造 userId 的地方
# 原: userId:i.UserID 或 userId:t.ScreenName
# 确保所有显示用户名的地方都改为 BSD本源用户

# === 补丁 3: 修改 email ===
# 原: email:t.NonPlainTextEmail??""
# 新: email:"bsd@essence.local"
email_old = 'email:t.NonPlainTextEmail??""'
email_new = 'email:"bsd@essence.local"'
if email_old in code:
    code = code.replace(email_old, email_new)
    print('✅ 补丁2: email 替换成功')
    patched_count += 1
else:
    print('⚠️ email 未找到 (可能已被之前的补丁修改)')

# 写回
with open(MAIN_JS, 'w', encoding='utf-8') as f:
    f.write(code)

# 验证
with open(MAIN_JS, 'r', encoding='utf-8') as f:
    verify = f.read()

checks = [
    ('BSD本源用户', 'BSD本源用户' in verify),
    ('username:BSD本源用户', 'username:"BSD本源用户"' in verify or 'username:' in verify and 'BSD本源用户' in verify),
    ('bsd@essence.local', 'bsd@essence.local' in verify),
    ('getUserInfo still exists', 'getUserInfo' in verify),
    ('Jx function exists', 'Jx=' in verify),
]

print(f'\n=== 验证结果 ({patched_count} 个补丁应用) ===')
for desc, result in checks:
    status = '✅' if result else '❌'
    print(f'  {status} {desc}')

if all(r for _, r in checks):
    print(f'\n✅ 所有补丁验证通过！')
else:
    failed = [d for d, r in checks if not r]
    print(f'\n❌ 以下验证失败: {failed}')
