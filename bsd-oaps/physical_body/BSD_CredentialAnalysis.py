"""
深入分析 credential 存储完整流程: serverKey, tokens(), 加密写入
"""
import os, json, re

TRAE_CN_APP = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app'
MAIN_JS = os.path.join(TRAE_CN_APP, 'out', 'main.js')

with open(MAIN_JS, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. serverKey 分析
print("=== 1. serverKey 读写 ===")
for pat in [r'serverKey[^,;]{0,200}', r'read\(this\.serverKey\)[^}]{0,300}', r'write\(.*serverKey[^,;]{0,200}']:
    matches = [(m.start(), content[max(0, m.start()-50):m.end()+350])
               for m in re.finditer(pat, content)]
    if matches and len(matches) < 15:
        print(f"\n  [{pat}] 命中 {len(matches)} 处:")
        for pos, ctx in matches[:2]:
            ctx_clean = ctx.replace('\n', ' ')[:500]
            print(f"    @{pos}: {ctx_clean}")

# 2. 分析 tokens() 方法完整实现
print("\n=== 2. tokens() 方法完整实现 ===")
pattern = r'async tokens\(\)\{await this\.h\.whenReady\(\)'
matches = list(re.finditer(pattern, content))
for m in matches[:1]:
    # 找大括号匹配
    start = m.start()
    brace_count = 0
    end = start
    for i in range(start, min(start + 2000, len(content))):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0 and i > start + 100:
                end = i + 1
                break
    print(f"  tokens() 实现 @{start}-{end}:")
    print(content[start:end][:1000])

# 3. 分析 X3/iCubeAuthInfo 作为 key 的存储
print("\n=== 3. iCubeAuthInfo 存储 ===")
# X3 作为变量名
x3_def = re.finditer(r'X3\s*=\s*"iCubeAuthInfo"', content)
for m in x3_def:
    print(f"  X3 定义 @{m.start()}")

# 查找 setItem(X3 或 setItem.*iCubeAuthInfo
for pat in [r'setItem\(X3[^)]+\)', r'setItem\("iCubeAuthInfo[^)]+\)',
            r'setItem\(Py\.a[^)]+\)', r'getItem\(X3[^)]+\)']:
    matches = [(m.start(), content[max(0, m.start()-100):m.end()+300])
               for m in re.finditer(pat, content)]
    if matches and len(matches) < 20:
        print(f"\n  [{pat}] 命中 {len(matches)} 处:")
        for pos, ctx in matches[:2]:
            ctx_clean = ctx.replace('\n', ' ')[:500]
            print(f"    @{pos}: {ctx_clean}")

# 4. Py.a 是什么
print("\n=== 4. Py.a 定义 ===")
py_a = re.finditer(r'Py\.a\s*=', content)
for m in list(py_a)[:3]:
    ctx = content[max(0, m.start()-100):m.end()+200]
    print(f"  @{m.start()}: {ctx.replace(chr(10), ' ')[:300]}")
