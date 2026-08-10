#!/usr/bin/env python3
"""
BSD × Trae CN — 使用已知密钥的 AHA 注入
========================================

使用之前成功获取的 AES-256 密钥:
  71079e1533eae26094450a564b7641e28d3292d36636807016c552ad0af26bb0

版本: V1.0 · 2026-08-05
"""

import os, json, base64, hashlib, time
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# 路径
TRAE_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
LOCAL_STATE = os.path.join(TRAE_DATA, 'Local State')
STORAGE = os.path.join(TRAE_DATA, 'User', 'globalStorage', 'storage.json')
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'
JWT_PATH = os.path.join(TRAE_CONFIG, 'trae-jwt-token')

# UIDs
TRAD_UID = '3753060170739075'
ESS_UID = 'a5b7a8623fdea6b8'

# AHA 前缀
AHA_PREFIX = bytes.fromhex('746305100000')

# 已知的 AES-256 密钥 (之前成功解密得到)
KNOWN_AES_KEY = bytes.fromhex('71079e1533eae26094450a564b7641e28d3292d36636807016c552ad0af26bb0')


class KnownKeyAHAEngine:
    """使用已知密钥的 AHA 引擎"""
    
    def __init__(self):
        self.aes_key = KNOWN_AES_KEY
        self.results = {}
    
    def run(self) -> dict:
        """执行注入"""
        
        print(self._banner())
        
        # Phase 0: 关闭 Trae CN
        self._stop_trae_cn()
        
        # Phase 1: 读取原始 AHA 数据作为参考
        orig_auth = self._read_original_auth()
        
        # Phase 2: 解密原始数据分析结构
        if orig_auth:
            orig_structure = self._analyze_original(orig_auth)
        else:
            orig_structure = None
        
        # Phase 3: 构造本源认证数据
        auth_data = self._construct_essence_auth(orig_structure)
        
        # Phase 4: AHA 加密
        encrypted = self._aha_encrypt(auth_data)
        
        # Phase 5: 验证加解密
        self._verify(encrypted, auth_data)
        
        # Phase 6: 注入到 storage.json
        self._inject(encrypted)
        
        # Phase 7: 创建 JWT
        self._create_jwt()
        
        # Phase 8: 启动 Trae CN
        self._start()
        
        return self.results
    
    def _stop_trae_cn(self):
        """关闭 Trae CN"""
        print('\n' + '='*60)
        print('  Phase 0: 关闭 Trae CN')
        print('='*60)
        os.system('taskkill /F /IM "Trae CN.exe" 2>nul')
        time.sleep(2)
    
    def _read_original_auth(self) -> dict:
        """读取原始认证数据"""
        print('\n' + '='*60)
        print('  Phase 1: 读取原始认证数据')
        print('='*60)
        
        try:
            with open(STORAGE, 'r', encoding='utf-8') as f:
                storage = json.load(f)
            
            # 查找原始 AHA 数据
            auth_keys = [k for k in storage if 'iCubeAuthInfo' in k]
            
            if auth_keys:
                key = auth_keys[0]
                value = storage[key]
                
                print(f'  找到原始认证数据: {key}')
                print(f'  长度: {len(value)} 字符')
                
                return {'key': key, 'value': value}
            else:
                print('  ⚠️ 未找到原始认证数据')
                return None
                
        except Exception as e:
            print(f'  ❌ 读取失败: {e}')
            return None
    
    def _analyze_original(self, orig_auth: dict) -> dict:
        """分析原始数据结构"""
        print('\n' + '='*60)
        print('  Phase 2: 分析原始 AHA 结构')
        print('='*60)
        
        try:
            encrypted_b64 = orig_auth['value']
            
            # Base64 解码
            raw = base64.b64decode(encrypted_b64)
            print(f'  解码后长度: {len(raw)} 字节')
            
            # 检查前缀
            prefix = raw[:6]
            print(f'  前缀: {prefix.hex()}')
            if prefix == AHA_PREFIX:
                print('  ✅ AHA 前缀匹配')
            else:
                print('  ⚠️ 前缀不匹配')
            
            # 提取 IV 和密文
            iv = raw[6:22]
            ciphertext = raw[22:]
            
            print(f'  IV: {iv.hex()}')
            print(f'  密文长度: {len(ciphertext)} 字节')
            
            # 解密
            cipher = AES.new(self.aes_key, AES.MODE_CBC, iv=iv)
            decrypted = cipher.decrypt(ciphertext)
            
            # 去填充
            plaintext = unpad(decrypted, AES.block_size)
            
            print(f'  解密后长度: {len(plaintext)} 字节')
            print(f'  前 100 字节: {plaintext[:100]}...')
            
            # 尝试解析 JSON
            try:
                data = json.loads(plaintext)
                print(f'  ✅ JSON 解析成功!')
                print(f'  键: {list(data.keys())[:10]}')
                return {'structure': 'json', 'data': data}
            except:
                # 可能是 Protobuf 或其他格式
                print(f'  ⚠️ 不是 JSON，可能是 Protobuf')
                print(f'  原始文本: {plaintext[:200]}')
                return {'structure': 'binary', 'raw': plaintext}
                
        except Exception as e:
            print(f'  ❌ 分析失败: {e}')
            return None
    
    def _construct_essence_auth(self, structure: dict = None) -> dict:
        """构造本源认证数据"""
        print('\n' + '='*60)
        print('  Phase 3: 构造本源认证数据')
        print('='*60)
        
        if structure and structure.get('structure') == 'json':
            # 基于原始结构修改
            data = structure['data'].copy()
            
            # 替换为本源 UID
            data['uid'] = ESS_UID
            data['userId'] = ESS_UID
            data['nickname'] = 'BSD本源用户'
            data['loginType'] = 'bsd_essence'
            
            # 更新用户信息
            if 'userInfo' in data:
                data['userInfo']['id'] = ESS_UID
                data['userInfo']['nickname'] = 'BSD本源用户'
                data['userInfo']['level'] = 'L4_Theory'
                data['userInfo']['coinValue'] = 80
            
            print(f'  ✅ 基于原始结构修改')
        else:
            # 创建新结构
            data = {
                'uid': ESS_UID,
                'userId': ESS_UID,
                'nickname': 'BSD本源用户',
                'loginType': 'bsd_essence',
                'userInfo': {
                    'id': ESS_UID,
                    'nickname': 'BSD本源用户',
                    'avatar': '',
                    'email': 'bsd@essence.local',
                    'level': 'L4_Theory',
                    'coinValue': 80,
                },
                'token': self._gen_token(),
                'expireAt': int(datetime.now().timestamp()) + 86400 * 365,
                'createdAt': int(datetime.now().timestamp()),
            }
            
            print(f'  ✅ 创建新结构')
        
        print(f'     uid: {data.get("uid")}')
        print(f'     loginType: {data.get("loginType")}')
        
        self.results['authData'] = data
        return data
    
    def _gen_token(self) -> str:
        """生成 Token"""
        header = base64.b64encode(json.dumps({
            'alg': 'HS256', 'typ': 'JWT',
        }).encode()).decode().rstrip('=')
        
        payload = base64.b64encode(json.dumps({
            'sub': ESS_UID,
            'name': 'BSD本源用户',
            'type': 'bsd_essence',
            'iat': int(datetime.now().timestamp()),
            'exp': int(datetime.now().timestamp()) + 86400 * 365,
        }).encode()).decode().rstrip('=')
        
        sig = hashlib.sha256(
            f"{header}.{payload}.bsd_essence".encode()
        ).hexdigest()[:32]
        
        return f"{header}.{payload}.{sig}"
    
    def _aha_encrypt(self, data: dict) -> str:
        """AHA 加密"""
        print('\n' + '='*60)
        print('  Phase 4: AHA 加密')
        print('='*60)
        
        # 序列化
        json_data = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
        print(f'  JSON 长度: {len(json_data)} 字节')
        
        # PKCS7 填充
        padded = pad(json_data, AES.block_size)
        
        # 随机 IV
        iv = os.urandom(AES.block_size)
        
        # AES-256-CBC 加密
        cipher = AES.new(self.aes_key, AES.MODE_CBC, iv=iv)
        ciphertext = cipher.encrypt(padded)
        
        # 组合 AHA 格式
        aha_data = AHA_PREFIX + iv + ciphertext
        
        # Base64 编码
        encrypted = base64.b64encode(aha_data).decode('utf-8')
        
        print(f'  ✅ 加密完成')
        print(f'     IV: {iv.hex()}')
        print(f'     密文: {len(ciphertext)} 字节')
        print(f'     加密后: {len(encrypted)} 字符')
        
        self.results['encrypted'] = encrypted
        return encrypted
    
    def _verify(self, encrypted_b64: str, expected: dict):
        """验证加解密"""
        print('\n' + '='*60)
        print('  Phase 5: 验证加解密')
        print('='*60)
        
        try:
            # 解密
            raw = base64.b64decode(encrypted_b64)
            iv = raw[6:22]
            ciphertext = raw[22:]
            
            cipher = AES.new(self.aes_key, AES.MODE_CBC, iv=iv)
            decrypted = cipher.decrypt(ciphertext)
            plaintext = unpad(decrypted, AES.block_size)
            
            # 解析
            actual = json.loads(plaintext)
            
            # 比较关键字段
            uid_match = actual.get('uid') == expected.get('uid')
            type_match = actual.get('loginType') == expected.get('loginType')
            
            print(f'  uid 匹配: {"✅" if uid_match else "❌"}')
            print(f'  type 匹配: {"✅" if type_match else "❌"}')
            
            if uid_match and type_match:
                print(f'  ✅ 验证通过!')
                self.results['verified'] = True
            else:
                print(f'  ⚠️ 验证未通过')
                self.results['verified'] = False
                
        except Exception as e:
            print(f'  ❌ 验证失败: {e}')
            self.results['verified'] = False
    
    def _inject(self, encrypted_b64: str):
        """注入到 storage.json"""
        print('\n' + '='*60)
        print('  Phase 6: 注入到 storage.json')
        print('='*60)
        
        with open(STORAGE, 'r', encoding='utf-8') as f:
            storage = json.load(f)
        
        # 更新所有认证键
        auth_keys = [
            'iCubeAuthInfo://icube-dc:516094651277160',
            'iCubeAuthInfo://usertag',
            'iCubeAuthInfo://icube.cloudide',
        ]
        
        for key in auth_keys:
            storage[key] = encrypted_b64
        
        # 更新 GTM
        gtm = storage.get('icube_gtm', {})
        gtm['currentUser'] = ESS_UID
        
        users = gtm.get('users', {})
        users[ESS_UID] = {
            'uid': ESS_UID,
            'type': 'bsd_essence',
            'status': 'active',
            'priority': 1,
        }
        gtm['users'] = users
        storage['icube_gtm'] = gtm
        
        # 标记
        storage['_bsd_aha_injected'] = {
            'uid': ESS_UID,
            'timestamp': datetime.now().isoformat(),
        }
        
        with open(STORAGE, 'w', encoding='utf-8') as f:
            json.dump(storage, f, ensure_ascii=False, indent=2)
        
        print(f'  ✅ 注入完成')
        print(f'     认证键: {len(auth_keys)} 个已更新')
    
    def _create_jwt(self):
        """创建 JWT"""
        print('\n' + '='*60)
        print('  Phase 7: 创建 JWT Token')
        print('='*60)
        
        os.makedirs(TRAE_CONFIG, exist_ok=True)
        
        token = self._gen_token()
        
        with open(JWT_PATH, 'w', encoding='utf-8') as f:
            f.write(token)
        
        print(f'  ✅ JWT 已创建')
        print(f'     路径: {JWT_PATH}')
    
    def _start(self):
        """启动 Trae CN"""
        print('\n' + '='*60)
        print('  Phase 8: 启动 Trae CN')
        print('='*60)
        
        exe = r'C:\Users\13003\AppData\Local\Programs\Trae CN\Trae CN.exe'
        os.startfile(exe)
        
        print('  ✅ 已启动')
        print('\n  💡 请查看 Trae CN 界面')
    
    def _banner(self) -> str:
        return f"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║   BSD × Trae CN — 使用已知密钥的 AHA 注入 V1.0                                  ║
║                                                                                  ║
║   AES-256 密钥: {self.aes_key.hex()[:32]}...                                    ║
║                                                                                  ║
║   流程:                                                                          ║
║   1. 读取原始 AHA 数据 → 分析结构                                                ║
║   2. 构造本源认证数据                                                            ║
║   3. AHA 加密 (AES-256-CBC)                                                     ║
║   4. 验证加解密                                                                  ║
║   5. 注入 storage.json                                                           ║
║   6. 创建 JWT Token                                                              ║
║   7. 启动 Trae CN                                                                ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
        """


def main():
    engine = KnownKeyAHAEngine()
    result = engine.run()
    
    if result.get('verified'):
        print('\n  ✅ AHA 本源登录注入成功!')
    else:
        print('\n  ⚠️ 注入完成但验证未通过')


if __name__ == '__main__':
    main()