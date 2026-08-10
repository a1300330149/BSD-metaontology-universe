"""
深度分析 loginScope 与账户显示逻辑
找出如何让UI不显示用户信息
"""
import re

MAIN_JS = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app\out\main.js'

with open(MAIN_JS, 'r', encoding='utf-8') as f:
    code = f.read()

print("=" * 60)
print("1. 分析 loginScope 的所有用法和值")
print("=" * 60)

for m in re.finditer(r'loginScope:([^,}]+)', code):
    pos = m.start()
    ctx = code[max(0,pos-40):pos+80].replace('\n', ' ')
    print(f"  @{pos}: {m.group(0)}")
    print(f"    context: ...{ctx}...")
    print()

print("=" * 60)
print("2. 搜索 It.MARSCODE / It.BYTEDANCE / bu.TRAE / bu.BYTEDANCE 定义")
print("=" * 60)

# 搜索枚举定义
for pattern in [r'MARSCODE', r'BYTEDANCE', r'bu\.TRAE', r'bu\.BYTEDANCE', r'SAAS', r'SOLO']:
    for m in re.finditer(pattern, code):
        pos = m.start()
        ctx = code[max(0,pos-60):pos+60].replace('\n', ' ')
        if len(ctx) < 200:
            print(f"  [{pattern}] @{pos}: {ctx}")

print("\n" + "=" * 60)
print("3. 分析 setUserInfo 调用逻辑")
print("=" * 60)

for m in re.finditer(r'setUserInfo\([^)]+\)', code):
    pos = m.start()
    ctx = code[max(0,pos-80):pos+80].replace('\n', ' ')
    print(f"  @{pos}: {m.group(0)}")
    print(f"    context: ...{ctx}...")
    print()

print("=" * 60)
print("4. 搜索 Die 函数 (loginScope==='trae' 逻辑)")
print("=" * 60)

# 找到 Die 函数
m = re.search(r'function Die\(t\)\{return t\?t\?\.account\?\.loginScope\?t\.account\.loginScope==="trae"\?"marscode":t\.account\.loginScope', code)
if m:
    pos = m.start()
    ctx = code[pos:pos+300].replace('\n', ' ')
    print(f"  @{pos}: {ctx}")

# 搜索 loginScope 相关的 account 判断
print("\n" + "=" * 60)
print("5. 搜索 account?.loginScope 判断")
print("=" * 60)

for m in re.finditer(r'account\?\.loginScope[^;]{0,100}', code):
    pos = m.start()
    ctx = code[max(0,pos-30):pos+100].replace('\n', ' ')
    print(f"  @{pos}: {m.group(0)}")
    print(f"    context: ...{ctx}...")
    print()

print("=" * 60)
print("6. 搜索 UI 中决定是否渲染用户头像/昵称的代码")
print("=" * 60)

# 搜索 sidebar/account/avatar 渲染相关
for term in ['renderAccount', 'renderUser', 'renderAvatar', 'accountRenderer', 'userInfoElement', 'accountElement']:
    count = code.count(term)
    if count > 0:
        print(f"\n  [{term}] 出现 {count} 次")
        for m in re.finditer(re.escape(term), code):
            pos = m.start()
            ctx = code[max(0,pos-40):pos+60].replace('\n', ' ')
            print(f"    @{pos}: {ctx}")
            break
