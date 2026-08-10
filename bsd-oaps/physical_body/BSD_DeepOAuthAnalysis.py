"""
深度分析传统UID登录认证流程 V2
学习AES加密机制、ExchangeToken请求格式、DeviceInfo/DeviceProof生成
"""
import os, json, re, base64, hashlib, time

TRAE_CN_APP = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app'
TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'

main_js = os.path.join(TRAE_CN_APP, 'out', 'main.js')
with open(main_js, 'r', encoding='utf-8') as f:
    content = f.read()

print('=' * 70)
print('  深度分析传统UID登录认证流程 V2')
print('=' * 70)

# 1. 分析AES加密完整流程
print('\n=== 1. 分析AES-CBC加密机制 ===')

# 找完整的加密/解密函数
encryption_functions = [
    (r'async function JIe\(t,e,i\)', 'AES-CBC加密'),
    (r'async function XIe\(t\)', '解密函数'),
    (r'function KIe\(t\)', '生成随机IV'),
    (r'function YIe\(t\)', '加密数据包装'),
    (r'function.*II.*PI.*NI.*RI.*\$I.*OI', '加密头部标记'),
]

for pattern, name in encryption_functions:
    matches = list(re.finditer(pattern, content))
    for m in matches[:1]:
        start = max(0, m.start() - 200)
        end = min(len(content), m.end() + 500)
        ctx = content[start:end]
        print(f'\n  [{name}] @{m.start()}:')
        print(ctx[:800])

# 2. 分析加密头部标记含义
print('\n=== 2. 加密头部标记分析 ===')

# 搜索头部标记定义
header_markers = re.findall(r'II\s*=|PI\s*=|NI\s*=|RI\s*=|\$I\s*=|OI\s*=', content)
print(f'  头部标记定义: {header_markers[:20]}')

# 搜索完整的头部定义
header_def = re.search(r'const\s+II\s*=.*?const\s+OI\s*=', content, re.DOTALL)
if header_def:
    print(f'\n  完整头部定义:')
    print(header_def.group()[:500])

# 3. 分析ExchangeToken完整请求
print('\n=== 3. ExchangeToken API完整请求分析 ===')

# 找exchangeTokenByRefreshToken完整实现
pattern = r'async exchangeTokenByRefreshToken\(t,e,i,r\)\{'
matches = list(re.finditer(pattern, content))
for m in matches[:1]:
    start = m.start()
    brace_count = 0
    end = start
    for i in range(start, min(start + 2000, len(content))):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0 and i > start + 200:
                end = i + 1
                break
    
    ctx = content[start:end]
    print(f'\n  exchangeTokenByRefreshToken @{m.start()}:')
    print(ctx[:1800])

# 4. 分析DeviceInfo和DeviceProof生成
print('\n=== 4. DeviceInfo和DeviceProof生成 ===')

# 找DeviceInfo生成逻辑
device_info_patterns = [
    r'DeviceInfo.*await.*crypto',
    r'DeviceProof.*Signature',
    r'async.*DeviceInfo',
    r'DeviceInfo.*encrypt',
]

for pat in device_info_patterns:
    matches = [(m.start(), content[max(0,m.start()-100):m.end()+300]) 
               for m in re.finditer(pat, content, re.IGNORECASE)]
    if matches:
        print(f'\n  [{pat}]')
        for pos, ctx in matches[:2]:
            print(f'    @{pos}: {ctx.replace(chr(10), " ")[:500]}')

# 5. 分析OAuth登录完整流程
print('\n=== 5. OAuth登录完整流程 ===')

# 找loginCredentialCallback完整实现
login_callback = re.search(r'async loginCredentialCallback\(t,e,i\)\{', content)
if login_callback:
    start = login_callback.start()
    brace_count = 0
    end = start
    for i in range(start, min(start + 3000, len(content))):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0 and i > start + 300:
                end = i + 1
                break
    
    ctx = content[start:end]
    print(f'\n  loginCredentialCallback @{start}:')
    print(ctx[:2500])

# 6. 分析iCubeAuthInfo解密流程
print('\n=== 6. iCubeAuthInfo解密流程 ===')

# 找读取和解密iCubeAuthInfo的代码
decrypt_patterns = [
    r'read.*iCubeAuthInfo|iCubeAuthInfo.*decrypt',
    r'getAuthInfo|loadAuthInfo',
    r'readAuth|loadCredential',
]

for pat in decrypt_patterns:
    matches = [(m.start(), content[max(0,m.start()-100):m.end()+500]) 
               for m in re.finditer(pat, content, re.IGNORECASE)]
    if matches:
        print(f'\n  [{pat}]')
        for pos, ctx in matches[:2]:
            print(f'    @{pos}: {ctx.replace(chr(10), " ")[:600]}')

# 7. 分析加密密钥encrypted_key的用途
print('\n=== 7. encrypted_key加密密钥用途 ===')

# 搜索encrypted_key的使用
key_usage = [(m.start(), content[max(0,m.start()-50):m.end()+300]) 
             for m in re.finditer(r'encrypted_key|encryptedKey', content)]
if key_usage:
    print(f'\n  encrypted_key使用处 ({len(key_usage)} 处):')
    for pos, ctx in key_usage[:10]:
        ctx_clean = ctx.replace('\n', ' ')[:400]
        print(f'    @{pos}: {ctx_clean}')

# 8. 分析当前JWT Token的完整信息
print('\n=== 8. 当前JWT Token解析 ===')
jwt_path = os.path.join(TRAE_CONFIG, 'trae-jwt-token')
if os.path.exists(jwt_path):
    with open(jwt_path, 'r') as f:
        token = f.read().strip()
    
    parts = token.split('.')
    if len(parts) >= 2:
        header = json.loads(base64.urlsafe_b64decode(parts[0] + '=='))
        payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
        
        print(f'  Token长度: {len(token)} chars')
        print(f'  Header: {json.dumps(header, indent=2)}')
        print(f'  Payload:')
        for k, v in payload.items():
            if k in ['exp', 'iat']:
                import datetime
                dt = datetime.datetime.fromtimestamp(v)
                print(f'    {k}: {v} ({dt})')
            else:
                val_str = str(v)[:100]
                print(f'    {k}: {val_str}')

# 9. 解析当前加密凭证结构
print('\n=== 9. 解析iCubeAuthInfo加密结构 ===')

storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
if os.path.exists(storage_path):
    with open(storage_path, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    auth_keys = [(k, v) for k, v in storage.items() if 'iCubeAuthInfo' in k]
    
    for key, value in auth_keys:
        try:
            decoded = base64.b64decode(value)
            
            # 分析结构
            print(f'\n  键: {key}')
            print(f'    总长度: {len(decoded)} bytes')
            print(f'    前20字节(hex): {decoded[:20].hex()}')
            
            # 检查头部格式
            if len(decoded) > 6:
                # 尝试解析头部
                print(f'    头部字节: {decoded[0]:02x} {decoded[1]:02x} {decoded[2]:02x} {decoded[3]:02x} {decoded[4]:02x} {decoded[5]:02x}')
                
                # 检查是否有固定头部标记
                if decoded[0] == 0x74 and decoded[1] == 0x63:  # "tc"
                    print(f'    头部标记: 自定义AES加密格式')
                    # 尝试找到IV（通常是前16字节）
                    iv = decoded[2:18]
                    print(f'    IV (16 bytes): {iv.hex()}')
                    # 剩余部分是密文
                    ciphertext = decoded[18:]
                    print(f'    密文长度: {len(ciphertext)} bytes')
            
            # 尝试base64解码内部数据
            try:
                inner = base64.b64decode(decoded.decode('latin-1'))
                print(f'    内部Base64解码: {len(inner)} bytes')
            except:
                pass
                
        except Exception as e:
            print(f'    解析失败: {e}')

# 10. 生成本源端独立登录方案
print('\n' + '=' * 70)
print('  本源端独立登录方案')
print('=' * 70)

# 分析完整登录流程
print('''
  传统UID登录完整流程:
  ┌─────────────────────────────────────────────────────────────────┐
  │ 1. 用户点击登录 → 打开OAuth浏览器                              │
  │ 2. 用户授权 → 获取Authorization Code                          │
  │ 3. Code换RefreshToken → POST /oauth/ExchangeToken              │
  │    - ClientID: 固定值                                          │
  │    - RefreshToken: 从OAuth回调获取                             │
  │    - DeviceInfo: 公钥加密的设备信息                            │
  │    - DeviceProof: 私钥签名的证明信息                          │
  │ 4. 存储凭证 → AES-CBC加密后存入iCubeAuthInfo                   │
  │ 5. 获取JWT Token → 从ExchangeToken响应获取                    │
  └─────────────────────────────────────────────────────────────────┘

  关键发现:
  1. encrypted_key已被清除，但当前加密凭证仍有效
     → AES加密密钥可能来自其他途径
     
  2. DeviceProof包含:
     - Signature: 私钥签名
     - Timestamp: 时间戳
     - Nonce: 随机数
     
  3. DeviceInfo:
     - 使用RSA公钥加密
     
  4. ClientSecret为空字符串
     → 安全依赖DeviceProof签名

  复刻方案:
  1. 生成本源端公私钥对
  2. 使用私钥签名DeviceProof
  3. 生成本源端DeviceInfo
  4. 通过OAuth获取本源端凭证
  5. AES加密存储本源端凭证
''')

# 输出关键API端点
print('\n  关键API端点:')
print('    - /cloudide/api/v3/trae/CheckLogin')
print('    - /cloudide/api/v3/trae/LoginByJwt')
print('    - /trae/api/v3/oauth/ExchangeToken')
print('    - /cloudide/api/v3/trae/ClearRefreshToken')

print('\n  本源端UID:', 'a5b7a8623fdea6b8')
print('  传统UID:', '3753060170739075')
print('  差异:', '需要通过OAuth流程重新认证')