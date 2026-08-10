"""
补充修改 - isTraeUser + 更多UI控制
"""
import re

MAIN_JS = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app\out\main.js'

with open(MAIN_JS, 'r', encoding='utf-8') as f:
    code = f.read()

patched_count = 0

# 修改 isTraeUser getter
for m in re.finditer(r'get isTraeUser\(\)\{return [^}]+\}', code):
    old = m.group(0)
    new = 'get isTraeUser(){return!1}'
    code = code.replace(old, new)
    print(f"✅ isTraeUser -> return false")
    patched_count += 1

# 修改 isLogin getter
for m in re.finditer(r'get isLogin\(\)\{return [^}]+\}', code):
    old = m.group(0)
    new = 'get isLogin(){return!1}'
    code = code.replace(old, new)
    print(f"✅ isLogin -> return false")
    patched_count += 1

# 修改 get isAuthenticated
for m in re.finditer(r'get isAuthenticated\(\)\{return [^}]+\}', code):
    old = m.group(0)
    new = 'get isAuthenticated(){return!1}'
    code = code.replace(old, new)
    print(f"✅ isAuthenticated -> return false")
    patched_count += 1

# 修改 _logged_in 相关
# 搜索 _logged_in 的使用
for m in re.finditer(r'_logged_in[^;]{0,50}', code):
    print(f"  [_logged_in] @{m.start()}: {m.group(0)}")

# 修改 Die 函数 - 返回 "unknown" 而非具体scope
# 原: function Die(t){return t?t?.account?.loginScope?t.account.loginScope==="trae"?"marscode":t.account.loginScope:t?.account?.scope||"unknown":"unknown"}
# 新: function Die(t){return "unknown"}
for m in re.finditer(r'function Die\(t\)\{return t\?t\?\.account\?\.loginScope[^}]{0,200}\}', code):
    old = m.group(0)
    new = 'function Die(t){return"unknown"}'
    code = code.replace(old, new)
    print(f"✅ Die函数 -> return 'unknown'")
    patched_count += 1
    break

# 确保 account.scope 的检查不会导致错误
# 将所有 It.MARSCODE 替换为一个不可能匹配的值（只在关键判断处）
# 注意：这可能破坏功能，所以更安全的做法是保持scope但让getter返回false

with open(MAIN_JS, 'w', encoding='utf-8') as f:
    f.write(code)

print(f"\n共 {patched_count} 个补丁应用")
