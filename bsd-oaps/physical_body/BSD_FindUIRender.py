"""
搜索 UI 中决定是否渲染用户信息卡片的代码
目标：找到设置面板中头像+昵称的渲染逻辑
"""
import re

MAIN_JS = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app\out\main.js'

with open(MAIN_JS, 'r', encoding='utf-8') as f:
    code = f.read()

print("=" * 60)
print("1. 搜索 userInfo / accountInfo 在 UI 渲染中的使用")
print("=" * 60)

# 搜索 userInfo 如何被 UI 组件使用
for pattern in [
    r'userInfo\?\.account\?\.',
    r'userInfo\.account',
    r'account\.ScreenName',
    r'account\.username',
    r'account\.nickname',
    r'account\.avatar',
    r'\.account\s*&&',
]:
    for m in re.finditer(pattern, code):
        pos = m.start()
        ctx = code[max(0,pos-40):pos+60].replace('\n', ' ')
        if len(ctx) > 30:
            print(f"  @{pos}: {m.group(0)}")
            print(f"    context: ...{ctx}...")
            print()

print("=" * 60)
print("2. 搜索设置面板/侧边栏渲染用户信息的组件")
print("=" * 60)

# 搜索 settings / sidebar 中的 account 渲染
for term in ['SettingsAccount', 'settingsAccount', 'AccountView', 'accountView', 
             'SidebarAccount', 'sidebarAccount', 'UserAccount', 'userAccount',
             'AccountPanel', 'accountPanel', 'UserInfoView', 'userInfoView',
             'UserInfoRenderer', 'userInfoRenderer']:
    count = code.count(term)
    if count > 0:
        print(f"\n  [{term}] 出现 {count} 次")
        for m in re.finditer(re.escape(term), code):
            pos = m.start()
            ctx = code[max(0,pos-30):pos+50].replace('\n', ' ')
            print(f"    @{pos}: {ctx}")
            break

print("=" * 60)
print("3. 搜索 showUserInfo / showAccount / hideUser 相关")
print("=" * 60)

for pattern in [r'showUserInfo', r'showAccountInfo', r'hideUserInfo', 
                r'showUserCard', r'hideUserCard', r'showAccountCard',
                r'hasUserInfo', r'hasAccount', r'needShowUser']:
    count = code.count(pattern)
    if count > 0:
        print(f"\n  [{pattern}] 出现 {count} 次")
        for m in re.finditer(pattern, code):
            pos = m.start()
            ctx = code[max(0,pos-40):pos+60].replace('\n', ' ')
            print(f"    @{pos}: {ctx}")

print("=" * 60)
print("4. 搜索 loginScope 决定 UI 显示的逻辑")
print("=" * 60)

# 搜索 loginScope 用于条件判断的地方
for m in re.finditer(r'loginScope[^;]{0,200}', code):
    pos = m.start()
    ctx = code[max(0,pos-30):pos+200].replace('\n', ' ')
    print(f"  @{pos}: {m.group(0)[:150]}")
    print(f"    context: ...{ctx[:200]}...")
    print()

print("=" * 60)
print("5. 搜索 'not_login' / 'NOT_LOGIN' 等状态判断")
print("=" * 60)

for term in ['not_login', 'NOT_LOGIN', 'no_user', 'NO_USER', 'isLogin', 'isLogin',
             'isNotLogin', 'isNotLoggedIn', 'showLogin', 'hideLogin']:
    count = code.count(term)
    if count > 0 and count < 30:
        print(f"\n  [{term}] 出现 {count} 次")
        for m in re.finditer(re.escape(term), code):
            pos = m.start()
            ctx = code[max(0,pos-40):pos+60].replace('\n', ' ')
            print(f"    @{pos}: {ctx}")
            if code.count(term) > 3:
                break
