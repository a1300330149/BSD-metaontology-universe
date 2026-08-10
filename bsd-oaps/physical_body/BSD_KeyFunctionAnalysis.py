"""
分析关键函数实现：Nee(密钥派生)、O9e(签名)、this.j(DeviceInfo加密)
目标：理解完整的加密链路，为复刻做准备
"""
import os, json, re, base64

TRAE_CN_APP = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app'
main_js = os.path.join(TRAE_CN_APP, 'out', 'main.js')

with open(main_js, 'r', encoding='utf-8') as f:
    content = f.read()

print('=' * 70)
print('  关键函数深度分析')
print('=' * 70)

# 1. 分析密钥派生函数Nee
print('\n=== 1. 密钥派生函数 Nee ===')
print('  功能：从随机IV派生出AES密钥')
print('  调用：Nee(r,e,i) → {aesKey:s, iv:n}')
print('  参数：r=随机IV, e=输入, i=AES128')

# 搜索Nee函数定义
nee_funcs = list(re.finditer(r'async function Nee\(t,e,i\)\{', content))
for m in nee_funcs[:2]:
    start = m.start()
    brace_count = 0
    end = start
    for idx in range(start, min(start + 800, len(content))):
        if content[idx] == '{':
            brace_count += 1
        elif content[idx] == '}':
            brace_count -= 1
            if brace_count == 0 and idx > start + 100:
                end = idx + 1
                break
    
    ctx = content[start:end]
    print(f'\n  Nee @{m.start()}:')
    print(ctx[:600])

# 2. 分析加密头部常量定义
print('\n=== 2. 加密头部常量定义 ===')

# 找AI=16, Kd, vw, II, PI, NI, RI, $I, OI等常量
constants_pattern = r'AI\s*=\s*16.*?OI\s*='
constants_match = re.search(constants_pattern, content, re.DOTALL)
if constants_match:
    print(f'\n  常量定义:')
    print(constants_match.group()[:800])

# 单独搜索每个常量
for const_name in ['AI', 'Kd', 'vw', 'TI', 'cm', 'II', 'PI', 'NI', 'RI', '$I', 'OI']:
    pattern = rf'var\s+{const_name}\s*=|const\s+{const_name}\s*='
    matches = list(re.finditer(pattern, content))
    if matches:
        for m in matches[:2]:
            ctx = content[max(0,m.start()-30):m.end()+100]
            print(f'  {const_name} @{m.start()}: {ctx.replace(chr(10), " ")[:200]}')

# 3. 分析O9e签名生成函数
print('\n=== 3. 签名生成函数 O9e ===')
print('  功能：生成DeviceProof签名')
print('  调用：O9e("POST", path, clientID, refreshToken, privateKeyPEM)')
print('  返回：{signature, timestamp, nonce}')

o9e_funcs = list(re.finditer(r'function O9e\(t,e,i,r,s\)\{', content))
for m in o9e_funcs[:2]:
    start = m.start()
    brace_count = 0
    end = start
    for idx in range(start, min(start + 1000, len(content))):
        if content[idx] == '{':
            brace_count += 1
        elif content[idx] == '}':
            brace_count -= 1
            if brace_count == 0 and idx > start + 100:
                end = idx + 1
                break
    
    ctx = content[start:end]
    print(f'\n  O9e @{m.start()}:')
    print(ctx[:800])

# 4. 分析RSA加密DeviceInfo的this.j函数
print('\n=== 4. DeviceInfo RSA加密函数 ===')
print('  功能：用公钥加密设备信息')
print('  调用：this.j(publicKeyPEM) → 加密后的DeviceInfo')

# 搜索publicKeyPEM相关代码
public_key_usage = [(m.start(), content[max(0,m.start()-100):m.end()+300]) 
                    for m in re.finditer(r'publicKeyPEM|privateKeyPEM', content)]
if public_key_usage:
    print(f'\n  找到 {len(public_key_usage)} 处公钥/私钥引用:')
    for pos, ctx in public_key_usage[:5]:
        ctx_clean = ctx.replace('\n', ' ')[:400]
        print(f'    @{pos}: {ctx_clean}')

# 搜索j函数实现（加密DeviceInfo）
j_func = list(re.finditer(r'async j\(t\)\{', content))
for m in j_func[:1]:
    start = m.start()
    brace_count = 0
    end = start
    for idx in range(start, min(start + 800, len(content))):
        if content[idx] == '{':
            brace_count += 1
        elif content[idx] == '}':
            brace_count -= 1
            if brace_count == 0 and idx > start + 50:
                end = idx + 1
                break
    
    ctx = content[start:end]
    print(f'\n  j函数 @{m.start()}:')
    print(ctx[:600])

# 5. 分析密钥对生成
print('\n=== 5. RSA密钥对生成 ===')

# 搜索generateKeyPair或subtle.generateKey
key_gen_patterns = [
    r'generateKeyPair|subtle\.generateKey',
    r'RSA.*generate|generate.*RSA',
    r'publicKeyPEM\s*=|privateKeyPEM\s*=',
]

for pat in key_gen_patterns:
    matches = [(m.start(), content[max(0,m.start()-50):m.end()+300]) 
               for m in re.finditer(pat, content, re.IGNORECASE)]
    if matches:
        print(f'\n  [{pat}] 找到 {len(matches)} 处:')
        for pos, ctx in matches[:3]:
            ctx_clean = ctx.replace('\n', ' ')[:400]
            print(f'    @{pos}: {ctx_clean}')

# 6. 分析Vv函数（生成ClientID）
print('\n=== 6. ClientID生成函数 Vv ===')

vv_func = list(re.finditer(r'function Vv\(t\)\{', content))
for m in vv_func[:1]:
    start = m.start()
    brace_count = 0
    end = start
    for idx in range(start, min(start + 500, len(content))):
        if content[idx] == '{':
            brace_count += 1
        elif content[idx] == '}':
            brace_count -= 1
            if brace_count == 0 and idx > start + 50:
                end = idx + 1
                break
    
    ctx = content[start:end]
    print(f'\n  Vv @{m.start()}:')
    print(ctx[:400])

# 7. 分析完整OAuth流程中的密钥存储
print('\n=== 7. 密钥存储位置 ===')

# 搜索密钥文件路径
key_paths = re.findall(r'\.pem|\.key|privateKey|publicKey', content)
print(f'\n  密钥相关引用 ({len(key_paths)}):')
for kp in key_paths[:15]:
    print(f'    {kp}')

# 搜索os_crypt/key相关路径
os_crypt_paths = [(m.start(), content[max(0,m.start()-30):m.end()+100]) 
                  for m in re.finditer(r'os_crypt.*key|key.*os_crypt', content, re.IGNORECASE)]
if os_crypt_paths:
    print(f'\n  os_crypt路径引用:')
    for pos, ctx in os_crypt_paths[:5]:
        ctx_clean = ctx.replace('\n', ' ')[:200]
        print(f'    @{pos}: {ctx_clean}')

print('\n' + '=' * 70)
print('  分析总结')
print('=' * 70)
print('''
  加密链路总结:
  
  1. 密钥派生 (Nee函数)
     - 输入: 16字节随机IV + 某种输入
     - 输出: AES-128密钥 + IV
     - 用途: 解密iCubeAuthInfo
  
  2. 加密流程 (XIe/ZIe函数)
     - 生成16字节随机IV: KIe(vw)
     - 派生AES密钥: Nee(iv, input, AES128)
     - 加密数据: JIe(key, iv, plaintext)
     - 添加头部: YIe(encrypted_data)
  
  3. 头部格式 (6字节)
     - II, PI, NI, RI, $I, OI
     - 标记加密类型和版本
  
  4. DeviceProof签名 (O9e函数)
     - 输入: 方法、路径、ClientID、RefreshToken、私钥
     - 输出: {signature, timestamp, nonce}
     - 用途: ExchangeToken API认证
  
  5. DeviceInfo加密 (this.j函数)
     - 使用RSA公钥加密
     - 用途: ExchangeToken API设备认证

  复刻关键点:
  1. 需要找到RSA公钥/私钥的生成和存储位置
  2. 理解Nee函数的完整密钥派生逻辑
  3. 复刻O9e签名生成逻辑
  4. 生成本源端独立的密钥对
''')