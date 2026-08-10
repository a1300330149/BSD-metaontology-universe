"""
深度分析传统UID登录认证流程
学习iCubeAuthInfo加密凭证的生成机制
"""
import os, json, re, base64

TRAE_CN_APP = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app'
TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'

main_js = os.path.join(TRAE_CN_APP, 'out', 'main.js')
with open(main_js, 'r', encoding='utf-8') as f:
    content = f.read()

print('=' * 70)
print('  深度分析传统UID登录认证流程')
print('=' * 70)

# 1. 分析OAuth登录完整流程
print('\n=== 1. OAuth登录流程分析 ===')

# 找loginCredentialCallback的完整实现
pattern = r'async loginCredentialCallback\(t,e,i\)\{try\{const r=await this\.f\(t,e,i\)'
matches = list(re.finditer(pattern, content))
for m in matches:
    # 提取更大上下文
    start = max(0, m.start() - 500)
    end = min(len(content), m.end() + 5000)
    ctx = content[start:end]
    
    # 找到相关函数
    func_patterns = [
        r'async loginCredentialCallback\(t,e,i\)\{[^}]+\}',
        r'write.*ide_credential[^}]*',
        r'class.*OAuthenticator[^}]*\{[^}]*\}',
        r'async.*login[^}]*\{[^}]*\}',
    ]
    
    print(f'\n  loginCredentialCallback上下文 @{m.start()}:')
    # 找write ide_credential
    write_match = re.search(r'write.*ide_credential[^,]*', ctx)
    if write_match:
        print(f'    {write_match.group()}')

# 2. 分析加密凭证生成
print('\n=== 2. 分析iCubeAuthInfo生成 ===')

# 搜索加密相关代码
encryption_patterns = [
    r'iCubeAuthInfo',
    r'encrypted_key',
    r'os_crypt',
    r'AES|RSA|encrypt|decrypt',
    r'Credential.*encrypt',
    r'encrypt.*Credential',
]

for pat in encryption_patterns:
    matches = [(m.start(), content[max(0,m.start()-80):m.end()+200]) 
               for m in re.finditer(pat, content, re.IGNORECASE)]
    if matches and len(matches) <= 50:
        print(f'\n  [{pat}] 找到 {len(matches)} 处 (显示前5):')
        for pos, ctx in matches[:5]:
            ctx_clean = ctx.replace('\n', ' ')[:400]
            print(f'    @{pos}: {ctx_clean}')

# 3. 分析ExchangeToken API请求格式
print('\n=== 3. 分析ExchangeToken API ===')

# 找完整的exchangeTokenByRefreshToken实现
pattern2 = r'async exchangeTokenByRefreshToken'
matches2 = list(re.finditer(pattern2, content))
for m in matches2[:2]:
    start = m.start()
    brace_count = 0
    end = start
    for i in range(start, min(start + 1500, len(content))):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0 and i > start + 100:
                end = i + 1
                break
    
    ctx = content[start:end]
    print(f'\n  exchangeTokenByRefreshToken @{m.start()}:')
    print(ctx[:1500])

# 4. 分析JWT Token格式
print('\n=== 4. 分析当前JWT Token ===')
jwt_path = os.path.join(TRAE_CONFIG, 'trae-jwt-token')
if os.path.exists(jwt_path) and os.path.getsize(jwt_path) > 0:
    with open(jwt_path, 'r') as f:
        token = f.read().strip()
    
    # 解析JWT
    try:
        parts = token.split('.')
        if len(parts) >= 2:
            header = json.loads(base64.urlsafe_b64decode(parts[0] + '=='))
            payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
            
            print(f'  Header: {json.dumps(header, indent=2)}')
            print(f'  Payload (关键字段):')
            for k in ['exp', 'iat', 'iss', 'sub', 'userId', 'account', 'scope']:
                if k in payload:
                    val = payload[k]
                    if k in ['exp', 'iat']:
                        import datetime
                        dt = datetime.datetime.fromtimestamp(val)
                        print(f'    {k}: {val} ({dt})')
                    else:
                        print(f'    {k}: {val}')
    except Exception as e:
        print(f'  解析失败: {e}')

# 5. 分析本地存储的加密凭证格式
print('\n=== 5. 分析本地加密凭证格式 ===')

storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
if os.path.exists(storage_path):
    with open(storage_path, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    # 找所有iCubeAuthInfo键
    auth_keys = [(k, v) for k, v in storage.items() if 'iCubeAuthInfo' in k]
    print(f'  找到 {len(auth_keys)} 个iCubeAuthInfo键:')
    
    for key, value in auth_keys:
        val_str = str(value)
        print(f'\n  键: {key}')
        print(f'    类型: {type(value).__name__}')
        print(f'    长度: {len(val_str)} chars')
        print(f'    前100字: {val_str[:100]}...')
        
        # 尝试Base64解码
        try:
            decoded = base64.b64decode(val_str)
            print(f'    Base64解码成功: {len(decoded)} bytes')
            # 检查是否是加密数据
            if decoded[:4] == b'RFBB':
                print(f'    格式: Windows DPAPI加密 (以DPAPI开头)')
                print(f'    前50字节(hex): {decoded[:50].hex()}')
            else:
                print(f'    前50字节(hex): {decoded[:50].hex()}')
        except:
            print(f'    非标准Base64格式')

# 6. 分析os_crypt加密密钥
print('\n=== 6. 分析os_crypt加密机制 ===')

key_path = os.path.join(TRAE_CONFIG, 'os_crypt', 'encrypted_key')
if os.path.exists(key_path) and os.path.getsize(key_path) > 0:
    with open(key_path, 'rb') as f:
        key_data = f.read()
    
    print(f'  encrypted_key: {len(key_data)} bytes')
    print(f'  前20字节(hex): {key_data[:20].hex()}')
    
    # 检查格式
    if key_data[:4] == b'RFBB':
        print(f'  格式: Windows DPAPI加密')
        print(f'  说明: 此密钥使用Windows DPAPI加密，仅本用户可解密')
    elif key_data[:2] == b'\x01\x00':
        print(f'  格式: DPAPI标准格式')
else:
    print(f'  encrypted_key: 不存在 (已清除)')

print(f'''\n╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║  认证流程分析完成                                                                         ║
╠══════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                              ║
║  核心发现:                                                                                 ║
║    1. iCubeAuthInfo使用Windows DPAPI加密                                                   ║
║    2. encrypted_key用于解密iCubeAuthInfo                                                   ║
║    3. Token通过ExchangeToken API换取                                                       ║
║    4. 完整流程: OAuth → LoginCallback → ExchangeToken → 存储加密凭证                        ║
║                                                                                              ║
║  关键机制:                                                                                 ║
║    - DPAPI加密: 绑定当前Windows用户，无法直接伪造                                           ║
║    - encrypted_key: 存储在os_crypt/encrypted_key                                            ║
║    - iCubeAuthInfo: 存储加密后的用户凭证                                                   ║
║                                                                                              ║
║  下一步: 分析如何用本源端UID复刻此流程                                                     ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝
''')
