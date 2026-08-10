"""
终极本源UI补丁 - 完全移除账户显示和引导
让设置面板直接显示通用设置
"""
import re

MAIN_JS = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app\out\main.js'

with open(MAIN_JS, 'r', encoding='utf-8') as f:
    code = f.read()

patched_count = 0

print("=" * 60)
print("本源登录 - 移除账户显示和引导")
print("=" * 60)

# === 补丁1: 移除"账户信息"引导区域的渲染 ===
# 搜索与账户引导相关的代码
for term in ['账户信息', '账户', '账号', '登录 TRAE', '提升您的编码', '解锁', '智能工具']:
    count = code.count(term)
    if count > 0 and count < 20:
        print(f"\n  [{term}] 出现 {count} 次")
        for m in re.finditer(term, code):
            pos = m.start()
            ctx = code[max(0,pos-60):pos+60].replace('\n', ' ')
            print(f"    @{pos}: {ctx[:120]}...")

# === 补丁2: 搜索"账号"菜单项的渲染 ===
print("\n" + "=" * 60)
print("搜索设置面板中'账号'菜单的渲染")
print("=" * 60)

# 搜索账号菜单相关
for term in ['"账号"', '账号', 'showAccountMenu', 'accountMenu', 'accountItem',
             'showAccounts', 'accountsItem', 'accountManagement']:
    count = code.count(term)
    if count > 0 and count < 30:
        print(f"\n  [{term}] 出现 {count} 次")

# === 补丁3: 搜索设置面板的初始化逻辑 ===
print("\n" + "=" * 60)
print("搜索设置面板初始化")
print("=" * 60)

# 搜索设置相关的初始化
for term in ['createSettings', 'initSettings', 'setupSettings', 'settingsInit',
             'SettingsPanel', 'settingsPanel', 'settingsView', 'SettingsView']:
    count = code.count(term)
    if count > 0 and count < 30:
        print(f"\n  [{term}] 出现 {count} 次")
        for m in re.finditer(re.escape(term), code):
            pos = m.start()
            ctx = code[max(0,pos-40):pos+80].replace('\n', ' ')
            print(f"    @{pos}: {ctx[:120]}...")
            if count > 3:
                break

# === 补丁4: 搜索'isLogin'在UI渲染中的使用 ===
print("\n" + "=" * 60)
print("搜索 isLogin/isAuthenticated 在UI判断中的使用")
print("=" * 60)

# 关键：搜索 account?.scope 判断，用于控制UI显示
for m in re.finditer(r'account\?\.scope[^;]{0,150}', code):
    pos = m.start()
    content = m.group(0)
    if len(content) > 30:
        ctx = code[max(0,pos-50):pos+150].replace('\n', ' ')
        print(f"  @{pos}: {content[:120]}")
        print(f"    context: ...{ctx[:200]}...")
        print()

# === 补丁5: 修改 isLoginTraeUser 强制返回 false ===
# 这样UI会认为没有用户登录，不显示用户信息卡片
print("\n" + "=" * 60)
print("修改 isLoginTraeUser 返回值")
print("=" * 60)

# 搜索 isLoginTraeUser getter
for term in ['get isLoginTraeUser', 'isLoginTraeUser()']:
    for m in re.finditer(re.escape(term), code):
        pos = m.start()
        ctx = code[max(0,pos):pos+100].replace('\n', ' ')
        print(f"  [{term}] @{pos}: {ctx[:100]}")
        
        # 找到getter并修改
        # 原: get isLoginTraeUser(){return this.a?.account?.scope===It.MARSCODE}
        # 或: get isLoginTraeUser(){return this.d?.account?.scope===It.MARSCODE}
        # 新: get isLoginTraeUser(){return false}
        
        # 找到完整的getter
        pattern = r'get isLoginTraeUser\(\)\{return (this\.[ad])\??\.account\??\.scope===It\.MARSCODE\}'
        match = re.search(pattern, code)
        if match:
            old = match.group(0)
            new = 'get isLoginTraeUser(){return!1}'
            code = code.replace(old, new)
            print(f"    ✅ 已修改: isLoginTraeUser -> return false")
            patched_count += 1
        else:
            # 尝试另一种模式
            pattern2 = r'get isLoginTraeUser\(\)\{return [^}]+}'
            match2 = re.search(pattern2, code)
            if match2:
                old = match2.group(0)
                new = 'get isLoginTraeUser(){return!1}'
                code = code.replace(old, new)
                print(f"    ✅ 已修改: isLoginTraeUser -> return false (模式2)")
                patched_count += 1
            else:
                print(f"    ⚠️ 未能精确匹配，手动修改...")

# === 补丁6: 修改 isBytedanceUser 和 isBusinessUser ===
for term, getter_name in [
    ('get isBytedanceUser', 'isBytedanceUser'),
    ('get isBusinessUser', 'isBusinessUser'),
    ('get isTraeUser', 'isTraeUser'),
]:
    pattern = rf'{re.escape(term)}\(\)\{{return [^}}]+\}}'
    match = re.search(pattern, code)
    if match:
        old = match.group(0)
        new = f'{term}(){{return!1}}'
        code = code.replace(old, new)
        print(f"    ✅ 已修改: {getter_name} -> return false")
        patched_count += 1

# 写回
with open(MAIN_JS, 'w', encoding='utf-8') as f:
    f.write(code)

print(f"\n共 {patched_count} 个补丁应用")
