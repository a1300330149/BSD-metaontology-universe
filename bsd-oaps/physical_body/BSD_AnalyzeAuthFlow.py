"""
深度分析 Trae CN 本源登录认证逻辑
目标：找出传统登录 vs 本源登录的判断逻辑
"""
import re, json, os

MAIN_JS = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app\out\main.js'

with open(MAIN_JS, 'r', encoding='utf-8') as f:
    code = f.read()

print("=" * 60)
print("1. 搜索登录类型判断逻辑")
print("=" * 60)

# 搜索 login_type / loginType / loginScope
for term in ['login_type', 'loginType', 'loginScope', 'LoginType', 'LoginScope']:
    count = code.count(term)
    print(f"\n  [{term}] 出现 {count} 次")
    for i, m in enumerate(re.finditer(re.escape(term), code)):
        if i >= 5:  # 只显示前5个
            print(f"    ... 共 {count} 处，仅显示前5处")
            break
        pos = m.start()
        ctx = code[max(0, pos-40):pos+80].replace('\n', ' ')
        print(f"    @{pos}: {ctx}")

print("\n" + "=" * 60)
print("2. 搜索 iCubeAuthInfo 认证信息结构")
print("=" * 60)

# 搜索 AuthInfo / authInfo / iCubeAuth
for term in ['iCubeAuthInfo', 'AuthInfo', 'authInfo']:
    count = code.count(term)
    print(f"\n  [{term}] 出现 {count} 次")

print("\n" + "=" * 60)
print("3. 搜索 getAuthUserInfo / getUserInfo / fetchUser")
print("=" * 60)

for term in ['getAuthUserInfo', 'getUserInfo', 'fetchUserInfo', 'fetchAccountInfo', 'getAccountInfo']:
    count = code.count(term)
    if count > 0:
        print(f"\n  [{term}] 出现 {count} 次")
        for i, m in enumerate(re.finditer(re.escape(term), code)):
            if i >= 3:
                break
            pos = m.start()
            ctx = code[max(0,pos-60):pos+120].replace('\n', ' ')
            print(f"    @{pos}: {ctx}")

print("\n" + "=" * 60)
print("4. 搜索 UI 中判断是否显示用户信息的逻辑")
print("=" * 60)

# 搜索 showUserInfo / showAvatar / showAccount / hideUser / isLoggedIn
for term in ['showUserInfo', 'showAvatar', 'showAccount', 'hideUser', 'isLoggedIn', 'isAuthenticated', 'showUser', 'hideAvatar']:
    count = code.count(term)
    if count > 0 and count < 50:
        print(f"\n  [{term}] 出现 {count} 次")

print("\n" + "=" * 60)
print("5. 搜索 'traditional' 和 'essence' 相关逻辑")
print("=" * 60)

for term in ['traditional', 'essence', 'bsd_essence', 'knowledge_proof']:
    count = code.count(term)
    if count > 0:
        print(f"\n  [{term}] 出现 {count} 次")
        for i, m in enumerate(re.finditer(term, code)):
            if i >= 3:
                print(f"    ...")
                break
            pos = m.start()
            ctx = code[max(0,pos-30):pos+60].replace('\n', ' ')
            print(f"    @{pos}: {ctx}")

print("\n" + "=" * 60)
print("6. 搜索头像/昵称/ScreenName 渲染逻辑")
print("=" * 60)

# 搜索 AvatarUrl / avatar / nickname 的渲染
for term in ['AvatarUrl', 'setUserInfo', 'setAccountInfo', 'updateUserInfo', 'refreshUserInfo']:
    count = code.count(term)
    if count > 0 and count < 30:
        print(f"\n  [{term}] 出现 {count} 次")
        for i, m in enumerate(re.finditer(re.escape(term), code)):
            if i >= 3:
                break
            pos = m.start()
            ctx = code[max(0,pos-50):pos+100].replace('\n', ' ')
            print(f"    @{pos}: {ctx}")

print("\n" + "=" * 60)
print("7. 搜索 IPC 通信中与账户相关的 channel")
print("=" * 60)

for m in re.finditer(r'icube.*auth|icube.*account|icube.*user|icube.*login', code, re.IGNORECASE):
    pos = m.start()
    ctx = code[max(0,pos-20):pos+80].replace('\n', ' ')
    if len(ctx) > 30:
        print(f"  @{pos}: {ctx.strip()}")
