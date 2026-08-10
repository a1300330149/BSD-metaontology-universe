"""
BSD 深度分析 main.js 中的加密实现
找到encryptString的完整定义和数据格式
"""
import os, re, json

TRAE_CN_APP = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app'
MAIN_JS = os.path.join(TRAE_CN_APP, 'out', 'main.js')

print("=" * 70)
print("  BSD main.js 加密实现深度分析")
print("=" * 70)

with open(MAIN_JS, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 找到encryptString的完整实现
print("\n[1] 查找encryptString完整实现...")

# 从之前的分析，我们知道Cu = k4e
# 搜索k4e的定义
pattern_k4e = r'k4e\s*='
matches_k4e = list(re.finditer(pattern_k4e, content))
print(f"  k4e定义位置: {len(matches_k4e)}")

# 搜索包含encryptString的更大上下文
pattern_encrypt = r'encryptString'
matches_encrypt = list(re.finditer(pattern_encrypt, content))
print(f"  encryptString引用次数: {len(matches_encrypt)}")

# 2. 分析EncryptionMainService的完整实现
print("\n[2] 分析EncryptionMainService...")

# 搜索encryptionMainService
pattern_ems = r'encryptionMainService|EncryptionMainService'
matches_ems = list(re.finditer(pattern_ems, content))
print(f"  EncryptionMainService引用次数: {len(matches_ems)}")

# 获取更大的上下文来分析
if matches_ems:
    # 找到第一个匹配的更大上下文
    m = matches_ems[0]
    start = max(0, m.start() - 2000)
    end = min(len(content), m.end() + 5000)
    ctx = content[start:end]
    
    # 查找关键函数
    func_patterns = [
        r'encryptString\s*[:=][^}]*',
        r'decryptString\s*[:=][^}]*',
        r'async.*encrypt[^}]*\{[^}]*\}',
        r'async.*decrypt[^}]*\{[^}]*\}',
        r'isEncryptionAvailable[^}]*',
    ]
    
    for pat in func_patterns:
        found = list(re.finditer(pat, ctx))
        if found:
            print(f"\n  [{pat[:50]}] 找到 {len(found)} 处:")
            for f in found[:1]:
                func_ctx = ctx[max(0,f.start()-100):min(f.end()+300, len(ctx))]
                func_clean = func_ctx.replace('\n', ' ')[:500]
                print(f"    {func_clean}")

# 3. 分析导入的加密模块
print("\n[3] 分析加密模块导入...")

# 查找与加密相关的import
import_patterns = [
    r'import.*crypto[^;]*',
    r'import.*keytar[^;]*',
    r'import.*encrypt[^;]*',
    r'import.*decrypt[^;]*',
    r'require.*crypto[^;]*',
    r'require.*keytar[^;]*',
]

for pat in import_patterns:
    matches = list(re.finditer(pat, content, re.IGNORECASE))
    if matches and len(matches) < 10:
        print(f"\n  [{pat[:50]}] 找到 {len(matches)} 处:")
        for m in matches[:2]:
            ctx = content[max(0,m.start()-50):m.end()+200]
            ctx_clean = ctx.replace('\n', ' ')[:300]
            print(f"    @{m.start()}: {ctx_clean}")

# 4. 查找数据格式定义
print("\n[4] 查找加密数据格式定义...")

# 搜索版本号或格式标识
format_patterns = [
    r'version.*[0-9]|format.*[0-9]',
    r'header.*encrypt|encrypt.*header',
    r'magic.*number|magicNumber',
    r'buffer.*format|format.*buffer',
    r'serialize.*encrypt|encrypt.*serialize',
    r'encode.*encrypt|encrypt.*encode',
]

for pat in format_patterns:
    matches = list(re.finditer(pat, content, re.IGNORECASE))
    if matches and len(matches) < 10:
        print(f"\n  [{pat[:50]}] 找到 {len(matches)} 处:")
        for m in matches[:2]:
            ctx = content[max(0,m.start()-50):m.end()+200]
            ctx_clean = ctx.replace('\n', ' ')[:300]
            print(f"    @{m.start()}: {ctx_clean}")

# 5. 搜索AES-CBC的具体使用方式
print("\n[5] 分析AES-CBC具体使用方式...")

# 深入分析找到的AES-CBC代码
aes_pattern = r'AES.*CBC|CBC.*AES|aes-cbc|AES-CBC'
aes_matches = list(re.finditer(aes_pattern, content, re.IGNORECASE))
print(f"  AES-CBC引用次数: {len(aes_matches)}")

# 获取每个AES-CBC引用的上下文
for i, m in enumerate(aes_matches[:5]):
    start = max(0, m.start() - 500)
    end = min(len(content), m.end() + 500)
    ctx = content[start:end]
    
    print(f"\n  AES-CBC引用#{i+1} @{m.start()}:")
    print(f"    {ctx.replace(chr(10), ' ')[:600]}")

# 6. 分析密钥派生过程
print("\n[6] 分析密钥派生...")

# 查找SHA-512的使用
sha_pattern = r'SHA.*512|sha.*512|digest.*512'
sha_matches = list(re.finditer(sha_pattern, content, re.IGNORECASE))
print(f"  SHA-512引用次数: {len(sha_matches)}")

for i, m in enumerate(sha_matches[:3]):
    start = max(0, m.start() - 300)
    end = min(len(content), m.end() + 300)
    ctx = content[start:end]
    
    print(f"\n  SHA-512引用#{i+1} @{m.start()}:")
    print(f"    {ctx.replace(chr(10), ' ')[:500]}")

# 7. 综合分析
print(f"\n\n{'='*70}")
print(f"  综合分析")
print(f"{'='*70}")
print(f"""
  加密流程总结（基于代码分析）:
  
  1. encrypted_key存储在Local State的os_crypt.encrypted_key
  2. encrypted_key使用DPAPI加密（跳过5字节签名后解密）
  3. 解密后的密钥通过某种方式派生出AES密钥
  4. iCubeAuthInfo使用AES-CBC加密
  5. 加密数据有特定的格式（头部+IV+密文）
  
  需要进一步分析:
  - 数据格式的确切结构（头部有哪些字段？）
  - IV是如何生成的？在哪里？
  - 密文后面是否有认证标签？
  - 密钥派生的具体过程
""")

# 保存分析结果
os.makedirs(r'C:\Users\13003\.bsd-essence', exist_ok=True)
analysis_result = {
    'aes_key': '71079e1533eae26094450a564b7641e28d3292d36636807016c552ad0af26bb0',
    'findings': {
        'dpapi_decrypt': '成功，跳过5字节签名',
        'aes_algorithm': 'AES-256-CBC',
        'data_format': '以7463051000开头，可能包含头部+IV+密文',
        'iv_location': '未知，需要进一步分析'
    }
}
with open(r'C:\Users\13003\.bsd-essence\encryption_analysis.json', 'w') as f:
    json.dump(analysis_result, f, indent=2)
print("  分析结果已保存")
