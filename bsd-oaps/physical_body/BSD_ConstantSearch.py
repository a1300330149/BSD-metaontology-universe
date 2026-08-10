"""
BSD 搜索加密常量定义
从main.js中搜索Bee, Uee, jee, Wee, Kd, TI等变量
"""
import os, re, json

TRAE_CN_APP = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app'
MAIN_JS = os.path.join(TRAE_CN_APP, 'out', 'main.js')

print("=" * 70)
print("  BSD 加密常量搜索器")
print("=" * 70)

with open(MAIN_JS, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 搜索关键常量定义
constants_to_find = [
    ('Bee', 'Bee常量'),
    ('Uee', 'Uee常量'),
    ('jee', 'jee常量'),
    ('Wee', 'Wee常量'),
    ('Kd', 'Kd常量 - 密钥分割点'),
    ('TI', 'TI常量 - 密钥派生'),
    ('AI', 'AI常量 - AES块大小'),
    ('cm', 'cm常量 - 头部大小'),
    ('kn', 'kn对象 - 加密类型枚举'),
    ('Oee', 'Oee常量'),
    ('Mee', 'Mee常量'),
    ('Lee', 'Lee常量'),
    ('Fee', 'Fee常量'),
    ('Ree', 'Ree常量'),
    ('II', 'II常量'),
    ('PI', 'PI常量'),
    ('NI', 'NI常量'),
    ('RI', 'RI常量'),
    ('OI', 'OI常量'),
]

print("\n[1] 搜索常量定义...")
for name, desc in constants_to_find:
    # 搜索变量定义
    # 可能的形式: var Bee=..., const Bee=..., Bee = ...
    patterns = [
        rf'var\s+{name}\s*=\s*([^;]+)',
        rf'const\s+{name}\s*=\s*([^;]+)',
        rf'{name}\s*=\s*new\s+Uint8Array\([^)]+\)',
        rf'{name}\s*=\s*\[([^\]]+)\]',
        rf'function\s+{name}\s*\(',
        rf'{name}\s*=\s*crypto\.getRandomValues',
    ]
    
    for pat in patterns:
        matches = list(re.finditer(pat, content))
        if matches:
            print(f"\n  [{desc}] 找到 {len(matches)} 处:")
            for m in matches[:2]:
                ctx = content[max(0,m.start()-50):m.end()+100]
                ctx_clean = ctx.replace('\n', ' ')[:300]
                print(f"    @{m.start()}: {ctx_clean}")
            break

# 2. 搜索kn对象定义
print("\n[2] 搜索kn对象(加密类型枚举)...")
kn_patterns = [
    r'kn\s*=\s*\{[^}]*AES[^}]*\}',
    r'AES_PRIVATE',
    r'function\s*\w+\s*\(\)\s*\{[^}]*kn\.AES[^}]*\}',
    r'var\s+kn\s*=',
    r'const\s+kn\s*=',
]

for pat in kn_patterns:
    matches = list(re.finditer(pat, content))
    if matches and len(matches) < 20:
        print(f"\n  [{pat[:50]}] 找到 {len(matches)} 处:")
        for m in matches[:3]:
            ctx = content[max(0,m.start()-100):m.end()+200]
            ctx_clean = ctx.replace('\n', ' ')[:400]
            print(f"    @{m.start()}: {ctx_clean}")

# 3. 深入分析HIe函数
print("\n[3] 深入分析HIe函数实现...")

# 搜索完整的HIe函数
hie_pattern = r'function\s+HIe\s*\([^)]*\)\s*\{[^}]*\}'
hie_matches = list(re.finditer(hie_pattern, content))
if hie_matches:
    for m in hie_matches[:1]:
        func = content[m.start():m.end()]
        print(f"  HIe函数完整实现:")
        print(f"  {func}")
else:
    # 尝试更大范围
    hie_pattern2 = r'function\s+HIe[^}]+'
    hie_matches2 = list(re.finditer(hie_pattern2, content))
    if hie_matches2:
        for m in hie_matches2[:1]:
            func = content[m.start():min(m.end()+500, len(content))]
            print(f"  HIe函数:")
            print(f"  {func[:600]}")

# 4. 分析完整的加密流程
print("\n[4] 分析完整加密流程 - 搜索encryptString实现...")

# 查找encryptString的完整实现
# 从之前的分析，我们知道Cu = k4e
# 搜索k4e的定义和encryptString方法
k4e_pattern = r'k4e\s*='
k4e_matches = list(re.finditer(k4e_pattern, content))
print(f"  k4e定义: {len(k4e_matches)} 处")

# 搜索包含encryptString的类
encrypt_class_patterns = [
    r'encryptString\s*\([^)]*\)\s*\{[^}]*\}',
    r'decryptString\s*\([^)]*\)\s*\{[^}]*\}',
]

for pat in encrypt_class_patterns:
    matches = list(re.finditer(pat, content))
    if matches:
        print(f"\n  [{pat[:50]}] 找到 {len(matches)} 处:")
        for m in matches[:2]:
            func = content[m.start():min(m.end()+300, len(content))]
            print(f"    {func.replace(chr(10), ' ')[:500]}")

# 5. 搜索完整的类定义
print("\n[5] 搜索加密相关的完整类...")

# 找到包含encryptString的更大类
class_pattern = r'class\s+\w+[^{]*\{[^}]*encryptString[^}]*\}'
class_matches = list(re.finditer(class_pattern, content))
if class_matches:
    for m in class_matches[:1]:
        cls = content[m.start():min(m.end()+1000, len(content))]
        print(f"  加密类:")
        print(f"  {cls[:800]}")

# 6. 保存分析结果
print(f"\n\n[6] 保存搜索结果...")
os.makedirs(r'C:\Users\13003\.bsd-essence', exist_ok=True)

# 搜索Bee和Uee的定义
bee_match = re.search(r'var\s+Bee\s*=\s*new\s+Uint8Array\(([^)]+)\)', content)
if bee_match:
    print(f"  Bee定义: {bee_match.group()}")

uee_match = re.search(r'var\s+Uee\s*=\s*new\s+Uint8Array\(([^)]+)\)', content)
if uee_match:
    print(f"  Uee定义: {uee_match.group()}")

jee_match = re.search(r'var\s+jee\s*=\s*new\s+Uint8Array\(([^)]+)\)', content)
if jee_match:
    print(f"  jee定义: {jee_match.group()}")

wee_match = re.search(r'var\s+Wee\s*=\s*new\s+Uint8Array\(([^)]+)\)', content)
if wee_match:
    print(f"  Wee定义: {wee_match.group()}")

print("\n" + "=" * 70)
print("  搜索完成")
print("=" * 70)
