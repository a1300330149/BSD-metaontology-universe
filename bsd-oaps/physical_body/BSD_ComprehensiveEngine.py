#!/usr/bin/env python3
"""
BSD × Trae CN — 综合本源登录方案
==================================

基于诊断结果，实施综合解决方案:
  1. 重新获取有效的 AES 密钥
  2. 分析正确的 AHA 数据结构
  3. 如果无法获取密钥，使用传统登录凭证
  4. 或者修改 main.js 绕过验证（备份恢复后）

版本: V1.0 · 2026-08-05
"""

import os, json, base64, ctypes, hashlib, time, sqlite3
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# 路径
TRAE_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
LOCAL_STATE = os.path.join(TRAE_DATA, 'Local State')
STORAGE = os.path.join(TRAE_DATA, 'User', 'globalStorage', 'storage.json')
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'
JWT_PATH = os.path.join(TRAE_CONFIG, 'trae-jwt-token')
MAIN_JS = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app\out\main.js'
BACKUP_MAIN = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app\out\backup'

# UIDs
TRAD_UID = '3753060170739075'
ESS_UID = 'a5b7a8623fdea6b8'

# AHA 前缀
AHA_PREFIX = bytes.fromhex('746305100000')


class ComprehensiveEngine:
    """综合本源登录引擎"""
    
    def __init__(self):
        self.aes_key = None
        self.results = {}
    
    def run(self) -> dict:
        """执行综合方案"""
        
        print(self._banner())
        
        # Step 1: 关闭 Trae CN
        self._stop_trae_cn()
        
        # Step 2: 获取有效的 AES 密钥
        key_result = self._get_aes_key()
        
        if key_result:
            # Step 3a: 使用正确密钥注入 AHA 数据
            self._inject_with_aha()
        else:
            print('\n  ⚠️ 无法获取 AES 密钥')
            print('  切换到方案 B: 传统登录凭证复用')
            # Step 3b: 使用传统登录凭证
            self._inject_traditional_credentials()
        
        # Step 4: 创建 JWT Token
        self._create_jwt()
        
        # Step 5: 启动 Trae CN
        self._start_trae_cn()
        
        return self.results
    
    def _stop_trae_cn(self):
        """关闭 Trae CN"""
        print('\n' + '='*60)
        print('  Step 1: 关闭 Trae CN')
        print('='*60)
        os.system('taskkill /F /IM "Trae CN.exe" 2>nul')
        time.sleep(3)
    
    def _get_aes_key(self) -> bool:
        """获取有效的 AES 密钥"""
        print('\n' + '='*60)
        print('  Step 2: 获取 AES 密钥')
        print('='*60)
        
        # 2.1 读取 encrypted_key
        with open(LOCAL_STATE, 'r', encoding='utf-8') as f:
            local_state = json.load(f)
        
        encrypted_key_b64 = local_state.get('os_crypt', {}).get('encrypted_key', '')
        
        if not encrypted_key_b64:
            print('  ❌ 未找到 encrypted_key')
            return False
        
        encrypted_key = base64.b64decode(encrypted_key_b64)
        print(f'  ✅ 读取 encrypted_key ({len(encrypted_key)} 字节)')
        
        # 2.2 使用 DPAPI 解密
        decrypted = self._dpapi_decrypt(encrypted_key)
        
        if decrypted and len(decrypted) >= 32:
            self.aes_key = decrypted[:32]  # 取前32字节作为 AES-256 密钥
            print(f'  ✅ AES-256 密钥获取成功')
            print(f'     长度: {len(self.aes_key)} 字节')
            print(f'     密钥: {self.aes_key.hex()[:32]}...')
            
            # 验证密钥有效性
            if self._verify_key():
                print(f'  ✅ 密钥验证通过')
                return True
            else:
                print(f'  ⚠️ 密钥验证失败，尝试其他方案')
                self.aes_key = None
                return False
        else:
            print(f'  ❌ 解密失败或密钥长度不足')
            return False
    
    def _dpapi_decrypt(self, encrypted_data: bytes) -> bytes:
        """DPAPI 解密"""
        try:
            import ctypes
            
            class DATA_BLOB(ctypes.Structure):
                _fields_ = [
                    ('cbData', ctypes.c_ulong),
                    ('pbData', ctypes.c_void_p),
                ]
            
            p = ctypes.create_string_buffer(encrypted_data)
            blob_in = DATA_BLOB(len(encrypted_data), ctypes.addressof(p))
            blob_out = DATA_BLOB()
            
            # 尝试多种 flags
            for flags in [0, 4]:
                result = ctypes.windll.crypt32.CryptUnprotectData(
                    ctypes.byref(blob_in),
                    None, None, None, None,
                    flags,
                    ctypes.byref(blob_out)
                )
                
                if result:
                    decrypted = ctypes.string_at(blob_out.pbData, blob_out.cbData)
                    ctypes.windll.kernel32.LocalFree(blob_out.pbData)
                    return decrypted
            
            return None
            
        except Exception as e:
            print(f'  DPAPI 异常: {e}')
            return None
    
    def _verify_key(self) -> bool:
        """验证密钥有效性"""
        try:
            # 读取原始 AHA 数据尝试解密
            with open(STORAGE, 'r', encoding='utf-8') as f:
                storage = json.load(f)
            
            auth_keys = [k for k in storage if 'iCubeAuthInfo' in k]
            if not auth_keys:
                return False
            
            encrypted_b64 = storage[auth_keys[0]]
            
            # 解密
            raw = base64.b64decode(encrypted_b64)
            if raw[:6] != AHA_PREFIX:
                return False
            
            iv = raw[6:22]
            ciphertext = raw[22:]
            
            cipher = AES.new(self.aes_key, AES.MODE_CBC, iv=iv)
            decrypted = cipher.decrypt(ciphertext)
            
            # 尝试去填充
            try:
                plaintext = unpad(decrypted, AES.block_size)
                # 检查是否是有效数据
                if len(plaintext) > 0:
                    # 尝试解析 JSON
                    try:
                        data = json.loads(plaintext)
                        print(f'     解密数据是有效 JSON!')
                        print(f'     键: {list(data.keys())[:5]}')
                        return True
                    except:
                        # 不是 JSON 但可能是其他有效格式
                        return len(plaintext) > 10
            except:
                # 填充错误，密钥可能不正确
                return False
            
        except Exception as e:
            print(f'  密钥验证异常: {e}')
            return False
    
    def _inject_with_aha(self):
        """使用 AHA 注入本源登录"""
        print('\n' + '='*60)
        print('  Step 3a: AHA 本源登录注入')
        print('='*60)
        
        # 构造本源认证数据
        auth_data = {
            'uid': ESS_UID,
            'userId': ESS_UID,
            'nickname': 'BSD本源用户',
            'loginType': 'bsd_essence',
            'userInfo': {
                'id': ESS_UID,
                'nickname': 'BSD本源用户',
                'avatar': '',
                'level': 'L4_Theory',
                'coinValue': 80,
            },
            'expireAt': int(datetime.now().timestamp()) + 86400 * 365,
            'createdAt': int(datetime.now().timestamp()),
        }
        
        # AHA 加密
        json_data = json.dumps(auth_data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
        padded = pad(json_data, AES.block_size)
        iv = os.urandom(AES.block_size)
        cipher = AES.new(self.aes_key, AES.MODE_CBC, iv=iv)
        ciphertext = cipher.encrypt(padded)
        
        aha_data = AHA_PREFIX + iv + ciphertext
        encrypted_b64 = base64.b64encode(aha_data).decode('utf-8')
        
        print(f'  ✅ AHA 加密完成')
        print(f'     原始: {len(json_data)} 字节')
        print(f'     加密后: {len(encrypted_b64)} 字符')
        
        # 注入 storage.json
        with open(STORAGE, 'r', encoding='utf-8') as f:
            storage = json.load(f)
        
        # 更新认证键
        for key in ['iCubeAuthInfo://icube-dc:516094651277160', 'iCubeAuthInfo://usertag']:
            storage[key] = encrypted_b64
        
        # 更新 GTM
        gtm = storage.get('icube_gtm', {})
        gtm['currentUser'] = ESS_UID
        users = gtm.get('users', {})
        users[ESS_UID] = {'uid': ESS_UID, 'type': 'bsd_essence', 'status': 'active', 'priority': 1}
        gtm['users'] = users
        storage['icube_gtm'] = gtm
        
        # 标记
        storage['_bsd_aha_essence'] = {'uid': ESS_UID, 'timestamp': datetime.now().isoformat()}
        
        with open(STORAGE, 'w', encoding='utf-8') as f:
            json.dump(storage, f, ensure_ascii=False, indent=2)
        
        print(f'  ✅ 注入完成')
    
    def _inject_traditional_credentials(self):
        """注入传统登录凭证（降级方案）"""
        print('\n' + '='*60)
        print('  Step 3b: 传统登录凭证注入')
        print('='*60)
        
        # 这个方案假设我们使用传统账号登录后的凭证
        # 但由于我们无法真正登录传统账号，只能注入表层数据
        
        with open(STORAGE, 'r', encoding='utf-8') as f:
            storage = json.load(f)
        
        # 确保 GTM 信息正确
        gtm = storage.get('icube_gtm', {})
        gtm['currentUser'] = ESS_UID
        users = gtm.get('users', {})
        users[ESS_UID] = {
            'uid': ESS_UID,
            'type': 'bsd_essence',
            'status': 'active',
            'priority': 1,
            'nickname': 'BSD本源用户',
        }
        gtm['users'] = users
        storage['icube_gtm'] = gtm
        
        # 表层标记
        storage['_bsd_essence_mode'] = True
        storage['_bsd_essence_uid'] = ESS_UID
        
        with open(STORAGE, 'w', encoding='utf-8') as f:
            json.dump(storage, f, ensure_ascii=False, indent=2)
        
        print(f'  ✅ 表层数据注入完成')
        print(f'  ⚠️ 此方案可能无法通过远程验证')
        print(f'  💡 建议: 方案 C - 创建独立本源登录页面')
    
    def _create_jwt(self):
        """创建 JWT Token"""
        print('\n' + '='*60)
        print('  Step 4: 创建 JWT Token')
        print('='*60)
        
        os.makedirs(TRAE_CONFIG, exist_ok=True)
        
        header = base64.b64encode(json.dumps({'alg': 'HS256', 'typ': 'JWT'}).encode()).decode().rstrip('=')
        payload = base64.b64encode(json.dumps({
            'sub': ESS_UID,
            'name': 'BSD本源用户',
            'type': 'bsd_essence',
            'iat': int(datetime.now().timestamp()),
            'exp': int(datetime.now().timestamp()) + 86400 * 365,
        }).encode()).decode().rstrip('=')
        sig = hashlib.sha256(f"{header}.{payload}.bsd_essence".encode()).hexdigest()[:32]
        token = f"{header}.{payload}.{sig}"
        
        with open(JWT_PATH, 'w', encoding='utf-8') as f:
            f.write(token)
        
        print(f'  ✅ JWT Token 已创建')
        print(f'     路径: {JWT_PATH}')
    
    def _start_trae_cn(self):
        """启动 Trae CN"""
        print('\n' + '='*60)
        print('  Step 5: 启动 Trae CN')
        print('='*60)
        
        exe = r'C:\Users\13003\AppData\Local\Programs\Trae CN\Trae CN.exe'
        os.startfile(exe)
        
        print('  ✅ Trae CN 已启动')
        print('\n  💡 请查看 Trae CN 界面')
        print('     如果仍不显示本源登录')
        print('     → 建议使用方案 C: 创建独立本源登录页面')
    
    def _banner(self) -> str:
        return """
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║   BSD × Trae CN — 综合本源登录方案 V1.0                                        ║
║                                                                                  ║
║   方案:                                                                          ║
║   A. 获取有效 AES 密钥 → 正确注入 AHA 数据                                      ║
║   B. 传统登录凭证复用 (降级)                                                    ║
║   C. 独立本源登录页面 (最终方案)                                                ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
        """


def main():
    engine = ComprehensiveEngine()
    result = engine.run()
    
    print('\n' + '='*60)
    print('  综合方案执行完成')


if __name__ == '__main__':
    main()