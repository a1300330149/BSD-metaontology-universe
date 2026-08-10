"""
搜索本源登录/匿名模式的现有机制
找出代码中是否已存在"不显示用户信息"的模式
"""
import re

MAIN_JS = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app\out\main.js'

with open(MAIN_JS, 'r', encoding='utf-8') as f:
    code = f.read()

print("=" * 60)
print("1. 搜索 SOLO/匿名/无用户 登录模式")
print("=" * 60)

for term in ['SOLO_Lite', 'solo_lite', 'solo-mode', 'soloMode', 'SOLO_MODE',
             'anonymous', 'Anonymous', 'anonymous_login', 'no_user',
             'ESSENCE', 'essence_mode', 'essenceMode', 'bsd_essence']:
    count = code.count(term)
    if count > 0 and count < 50:
        print(f"\n  [{term}] 出现 {count} 次")
        for i, m in enumerate(re.finditer(re.escape(term), code)):
            if i >= 5:
                print(f"    ...共 {count} 处")
                break
            pos = m.start()
            ctx = code[max(0,pos-40):pos+60].replace('\n', ' ')
            print(f"    @{pos}: {ctx}")

print("\n" + "=" * 60)
print("2. 搜索 account.username 的所有使用")
print("=" * 60)

for m in re.finditer(r'account\.username[^;]{0,80}', code):
    pos = m.start()
    ctx = code[max(0,pos-50):pos+100].replace('\n', ' ')
    print(f"  @{pos}: {m.group(0)}")
    print(f"    context: ...{ctx}...")
    print()

print("=" * 60)
print("3. 搜索 account 中与显示相关的属性")
print("=" * 60)

# 搜索构建 account 对象的所有位置
for m in re.finditer(r'account:\{[^}]{0,300}\}', code):
    pos = m.start()
    content = m.group(0)
    if len(content) > 50:
        print(f"  @{pos}: {content[:200]}")
        print()

print("=" * 60)
print("4. 搜索 SOLO 产品类型判断")
print("=" * 60)

# SOLO_Lite 似乎是没有账户显示的模式
# 搜索 packageType / productCode 相关
for term in ['packageType', 'productCode', 'vo.SOLO_Lite', 'vo.TRAE', 
             'Nh.SOLO_CN', 'Nh.TRAE_CN']:
    count = code.count(term)
    if count > 0 and count < 30:
        print(f"\n  [{term}] 出现 {count} 次")
        for i, m in enumerate(re.finditer(re.escape(term), code)):
            if i >= 4:
                break
            pos = m.start()
            ctx = code[max(0,pos-40):pos+60].replace('\n', ' ')
            print(f"    @{pos}: {ctx}")

print("\n" + "=" * 60)
print("5. 搜索 isLogin / isAuthenticated 用于UI判断")
print("=" * 60)

for term in ['isLoginTraeUser', 'isLoginBytedanceUser', 'isBusinessUser', 
             'isI18nUser', 'isLogin', 'isAuthenticated', 
             'get isLogin', 'get isAuthenticated']:
    count = code.count(term)
    if count > 0 and count < 20:
        print(f"\n  [{term}] 出现 {count} 次")
        for m in re.finditer(re.escape(term), code):
            pos = m.start()
            ctx = code[max(0,pos-50):pos+80].replace('\n', ' ')
            print(f"    @{pos}: {ctx}")

print("\n" + "=" * 60)
print("6. 搜索 '账号' / '账户' 相关中文UI文本")
print("=" * 60)

# 搜索设置面板的账号相关文本
for pattern in ['账号', '账户', '个人资料', '用户信息', '个人账户']:
    count = code.count(pattern)
    if count > 0:
        print(f"\n  [{pattern}] 出现 {count} 次")
        for i, m in enumerate(re.finditer(pattern, code)):
            if i >= 3:
                break
            pos = m.start()
            ctx = code[max(0,pos-30):pos+30].replace('\n', ' ')
            print(f"    @{pos}: {ctx}")
