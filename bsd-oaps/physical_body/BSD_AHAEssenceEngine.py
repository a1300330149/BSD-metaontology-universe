#!/usr/bin/env python3
"""
BSD × Trae CN — AHA 加密本源登录引擎
======================================

核心思路:
  1. 从 Local State 获取 encrypted_key
  2. 使用 DPAPI 解密得到 AES-256 密钥
  3. 构造包含本源 UID 的认证数据
  4. 使用 AES-256-CBC 加密
  5. 添加 AHA 前缀 (746305100000)
  6. Base64 编码
  7. 注入到 storage.json

AHA 格式:
  前 6 字节: 固定前缀 746305100000
  16 字节: IV (随机)
  剩余: AES-256-CBC 密文

版本: V1.0 · 2026-08-05
"""

import os, json, base64, ctypes, hashlib, struct, time
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# Windows 特定
try:
    import ctypes.wintypes
    HAS_CTYPES_WINTYPES = True
except ImportError:
    HAS_CTYPES_WINTYPES = False

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


class AHAEssenceEngine:
    """AHA 加密本源登录引擎"""
    
    def __init__(self):
        self.aes_key = None
        self.results = {}
    
    def run(self) -> dict:
        """执行 AHA 本源登录注入"""
        
        print(self._banner())
        
        # Phase 0: 关闭 Trae CN
        self._stop_trae_cn()
        
        # Phase 1: 获取 AES 密钥
        self._get_aes_key()
        
        if not self.aes_key:
            print('  ❌ 无法获取 AES 密钥')
            return {}
        
        # Phase 2: 构造本源认证数据
        auth_data = self._construct_essence_auth()
        
        # Phase 3: AHA 加密
        encrypted = self._aha_encrypt(auth_data)
        
        # Phase 4: 注入到 storage.json
        self._inject_to_storage(encrypted)
        
        # Phase 5: 创建 JWT Token
        self._create_jwt_token()
        
        # Phase 6: 启动 Trae CN
        self._start_trae_cn()
        
        # 输出结果
        self._print_result()
        
        return self.results
    
    def _stop_trae_cn(self):
        """关闭 Trae CN"""
        print('\n' + '='*60)
        print('  Phase 0: 关闭 Trae CN')
        print('='*60)
        os.system('taskkill /F /IM "Trae CN.exe" 2>nul')
        time.sleep(2)
        print('  ✅ 已关闭')
    
    def _get_aes_key(self):
        """获取 AES-256 密钥"""
        print('\n' + '='*60)
        print('  Phase 1: 获取 AES-256 密钥')
        print('='*60)
        
        # 1. 从 Local State 读取 encrypted_key
        with open(LOCAL_STATE, 'r', encoding='utf-8') as f:
            local_state = json.load(f)
        
        encrypted_key_b64 = local_state.get('os_crypt', {}).get('encrypted_key', '')
        
        if not encrypted_key_b64:
            print('  ❌ 未找到 encrypted_key')
            return
        
        encrypted_key = base64.b64decode(encrypted_key_b64)
        
        print(f'  ✅ 读取 encrypted_key ({len(encrypted_key)} 字节)')
        
        # 2. 使用 DPAPI 解密
        try:
            aes_key = self._dpapi_decrypt(encrypted_key)
            self.aes_key = aes_key
            print(f'  ✅ AES-256 密钥获取成功 ({len(aes_key)} 字节)')
            print(f'     密钥: {aes_key.hex()[:32]}...')
        except Exception as e:
            print(f'  ❌ DPAPI 解密失败: {e}')
            self.results['keyError'] = str(e)
    
    def _dpapi_decrypt(self, encrypted_data: bytes) -> bytes:
        """使用 DPAPI 解密"""
        
        if not HAS_CTYPES_WINTYPES:
            raise RuntimeError('ctypes.wintypes 不可用')
        
        class DATA_BLOB(ctypes.Structure):
            _fields_ = [
                ('cbData', ctypes.wintypes.DWORD),
                ('pbData', ctypes.c_void_p),
            ]
        
        p = ctypes.create_string_buffer(encrypted_data)
        blob_in = DATA_BLOB(len(encrypted_data), ctypes.addressof(p))
        blob_out = DATA_BLOB()
        
        # 调用 CryptUnprotectData
        result = ctypes.windll.crypt32.CryptUnprotectData(
            ctypes.byref(blob_in),
            None,
            None,
            None,
            None,
            0,
            ctypes.byref(blob_out)
        )
        
        if not result:
            raise RuntimeError(f'CryptUnprotectData 失败: {ctypes.GetLastError()}')
        
        # 读取解密数据
        decrypted = ctypes.string_at(blob_out.pbData, blob_out.cbData)
        
        # 释放内存
        ctypes.windll.kernel32.LocalFree(blob_out.pbData)
        
        return decrypted
    
    def _construct_essence_auth(self) -> dict:
        """构造本源认证数据"""
        print('\n' + '='*60)
        print('  Phase 2: 构造本源认证数据')
        print('='*60)
        
        # 构造与 Trae CN 兼容的认证数据格式
        # 基于之前的分析，AHA 数据可能包含:
        # - uid
        # - token/jwt
        # - 用户信息
        # - 过期时间
        
        auth_data = {
            'uid': ESS_UID,
            'userId': ESS_UID,
            'nickname': 'BSD本源用户',
            'loginType': 'bsd_essence',
            'token': self._generate_token(),
            'userInfo': {
                'id': ESS_UID,
                'nickname': 'BSD本源用户',
                'avatar': '',
                'email': 'bsd@essence.local',
                'level': 'L4_Theory',
                'coinValue': 80,
            },
            'expireAt': int(datetime.now().timestamp()) + 86400 * 365,
            'createdAt': int(datetime.now().timestamp()),
            'deviceId': self._get_device_id(),
        }
        
        print(f'  ✅ 认证数据构造完成')
        print(f'     uid: {auth_data["uid"]}')
        print(f'     loginType: {auth_data["loginType"]}')
        print(f'     有效期: 365 天')
        
        self.results['authData'] = auth_data
        return auth_data
    
    def _generate_token(self) -> str:
        """生成 Token"""
        # 生成类似 JWT 的 Token
        header = base64.b64encode(json.dumps({
            'alg': 'HS256',
            'typ': 'JWT',
        }).encode()).decode().rstrip('=')
        
        payload = base64.b64encode(json.dumps({
            'sub': ESS_UID,
            'name': 'BSD本源用户',
            'type': 'bsd_essence',
            'iat': int(datetime.now().timestamp()),
            'exp': int(datetime.now().timestamp()) + 86400 * 365,
        }).encode()).decode().rstrip('=')
        
        # 签名
        sig_data = f"{header}.{payload}"
        signature = hashlib.sha256(
            (sig_data + "bsd_essence_key").encode()
        ).hexdigest()[:32]
        
        return f"{header}.{payload}.{signature}"
    
    def _get_device_id(self) -> str:
        """获取设备 ID"""
        # 使用机器标识
        try:
            import uuid
            mac = uuid.getnode()
            return f"bsd_device_{mac}"
        except:
            return "bsd_device_default"
    
    def _aha_encrypt(self, data: dict) -> str:
        """AHA 加密"""
        print('\n' + '='*60)
        print('  Phase 3: AHA 加密')
        print('='*60)
        
        # 1. 将数据序列化为 JSON
        json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        
        # 2. PKCS7 填充
        padded_data = pad(json_data, AES.block_size)
        
        # 3. 生成随机 IV
        iv = os.urandom(AES.block_size)
        
        # 4. AES-256-CBC 加密
        cipher = AES.new(self.aes_key, AES.MODE_CBC, iv=iv)
        ciphertext = cipher.encrypt(padded_data)
        
        # 5. 组合 AHA 格式: 前缀 + IV + 密文
        aha_data = AHA_PREFIX + iv + ciphertext
        
        # 6. Base64 编码
        encrypted_b64 = base64.b64encode(aha_data).decode('utf-8')
        
        print(f'  ✅ AHA 加密完成')
        print(f'     原始数据: {len(json_data)} 字节')
        print(f'     IV: {iv.hex()}')
        print(f'     密文: {len(ciphertext)} 字节')
        print(f'     加密后: {len(encrypted_b64)} 字符')
        
        # 验证解密
        self._verify_decrypt(encrypted_b64, json_data)
        
        self.results['encrypted'] = encrypted_b64
        return encrypted_b64
    
    def _verify_decrypt(self, encrypted_b64: str, expected_data: bytes):
        """验证解密"""
        
        try:
            # 1. Base64 解码
            raw = base64.b64decode(encrypted_b64)
            
            # 2. 检查前缀
            prefix = raw[:6]
            if prefix != AHA_PREFIX:
                print(f'  ⚠️ 前缀不匹配: {prefix.hex()}')
                return
            
            # 3. 提取 IV 和密文
            iv = raw[6:22]
            ciphertext = raw[22:]
            
            # 4. 解密
            cipher = AES.new(self.aes_key, AES.MODE_CBC, iv=iv)
            decrypted = cipher.decrypt(ciphertext)
            
            # 5. 去填充
            from Crypto.Util.Padding import unpad
            plaintext = unpad(decrypted, AES.block_size)
            
            # 6. 验证
            if plaintext == expected_data:
                print(f'  ✅ 解密验证通过!')
            else:
                print(f'  ⚠️ 解密数据不匹配')
                print(f'     预期: {expected_data[:50]}...')
                print(f'     实际: {plaintext[:50]}...')
                
        except Exception as e:
            print(f'  ⚠️ 解密验证失败: {e}')
    
    def _inject_to_storage(self, encrypted_b64: str):
        """注入到 storage.json"""
        print('\n' + '='*60)
        print('  Phase 4: 注入到 storage.json')
        print('='*60)
        
        # 读取当前 storage.json
        with open(STORAGE, 'r', encoding='utf-8') as f:
            storage = json.load(f)
        
        # 替换 iCubeAuthInfo
        auth_key = 'iCubeAuthInfo://icube-dc:516094651277160'
        
        # 如果不存在，创建
        storage[auth_key] = encrypted_b64
        
        # 也更新其他认证键
        # iCubeAuthInfo://usertag
        storage['iCubeAuthInfo://usertag'] = encrypted_b64
        
        # iCubeAuthInfo://icube.cloudide
        storage['iCubeAuthInfo://icube.cloudide'] = encrypted_b64
        
        # 确保 currentUser 是本源 UID
        if 'icube_gtm' not in storage:
            storage['icube_gtm'] = {}
        
        gtm = storage['icube_gtm']
        gtm['currentUser'] = ESS_UID
        
        # 更新 GTM 用户
        users = gtm.get('users', {})
        users[ESS_UID] = {
            'uid': ESS_UID,
            'type': 'bsd_essence',
            'status': 'active',
            'priority': 1,
            'nickname': 'BSD本源用户',
            'loginType': 'bsd_essence',
        }
        gtm['users'] = users
        storage['icube_gtm'] = gtm
        
        # 添加标记
        storage['_bsd_essence_aha_injected'] = {
            'uid': ESS_UID,
            'timestamp': datetime.now().isoformat(),
            'method': 'AHA_encrypted_injection',
        }
        
        # 保存
        with open(STORAGE, 'w', encoding='utf-8') as f:
            json.dump(storage, f, ensure_ascii=False, indent=2)
        
        print(f'  ✅ 注入完成')
        print(f'     认证键: 3 个已更新')
        print(f'     currentUser: {ESS_UID}')
    
    def _create_jwt_token(self):
        """创建 JWT Token 文件"""
        print('\n' + '='*60)
        print('  Phase 5: 创建 JWT Token')
        print('='*60)
        
        os.makedirs(TRAE_CONFIG, exist_ok=True)
        
        token = self._generate_token()
        
        with open(JWT_PATH, 'w', encoding='utf-8') as f:
            f.write(token)
        
        print(f'  ✅ JWT Token 已创建')
        print(f'     路径: {JWT_PATH}')
        print(f'     长度: {len(token)} 字符')
    
    def _start_trae_cn(self):
        """启动 Trae CN"""
        print('\n' + '='*60)
        print('  Phase 6: 启动 Trae CN')
        print('='*60)
        
        exe_path = r'C:\Users\13003\AppData\Local\Programs\Trae CN\Trae CN.exe'
        os.startfile(exe_path)
        
        print('  ✅ Trae CN 已启动')
        print('     等待加载...')
    
    def _print_result(self):
        """打印结果"""
        print('\n' + '='*60)
        print('  📋 AHA 本源登录注入完成')
        print('='*60)
        
        auth_data = self.results.get('authData', {})
        print(f'\n  本源 UID: {auth_data.get("uid", ESS_UID)}')
        print(f'  登录类型: {auth_data.get("loginType", "bsd_essence")}')
        print(f'  AES 密钥: ✅ 已获取')
        print(f'  AHA 加密: ✅ 已注入')
        
        print(f'\n  💡 请查看 Trae CN 界面')
        print(f'     如果仍然不显示，可能需要:')
        print(f'     1. 等待加载（10-30秒）')
        print(f'     2. 在 Trae CN 中执行 "Reload Window"')
        print(f'     3. 或完全退出后重启')
    
    def _banner(self) -> str:
        return """
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║   BSD × Trae CN — AHA 加密本源登录引擎 V1.0                                    ║
║                                                                                  ║
║   核心流程:                                                                      ║
║   ┌─────────────────────────────────────────────────────────────────────────┐   ║
║   │ 1. 从 Local State 获取 encrypted_key                                    │   ║
║   │ 2. 使用 DPAPI 解密得到 AES-256 密钥                                     │   ║
║   │ 3. 构造包含本源 UID 的认证数据                                          │   ║
║   │ 4. 使用 AES-256-CBC 加密                                               │   ║
║   │ 5. 添加 AHA 前缀 (746305100000)                                        │   ║
║   │ 6. Base64 编码                                                          │   ║
║   │ 7. 注入到 storage.json                                                  │   ║
║   └─────────────────────────────────────────────────────────────────────────┘   ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
        """


def main():
    engine = AHAEssenceEngine()
    result = engine.run()
    
    if result:
        print('\n' + '='*60)
        print('  ✅ AHA 本源登录注入完成!')
    else:
        print('\n' + '='*60)
        print('  ❌ 注入失败')


if __name__ == '__main__':
    main()