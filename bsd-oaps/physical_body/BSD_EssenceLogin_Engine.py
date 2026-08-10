"""
BSD 本源端独立登录复刻引擎
================================
目标：学习传统UID(3753060170739075)的完整认证流程
      复刻本源端UID(a5b7a8623fdea6b8)的独立认证

核心思路：
  1. 学习 → 理解传统UID的完整OAuth+Token+加密链路
  2. 复刻 → 用本源端UID复刻同样的认证流程
  3. 独立 → 实现本源端的独立认证，不依赖传统UID

参考实现：
  - keygenerate: 复刻$9e函数，生成P-256密钥对
  - sign_proof: 复刻O9e函数，生成DeviceProof签名
  - encrypt_cred: 复刻XIe函数，AES加密存储凭证
  - exchange_token: 复刻exchangeTokenByRefreshToken
  
理论基础：
  六系立系论·具现系·代码即现实
  0×0=n双零涌现：学习(0)×复刻(0)=独立认证(n)
"""

import os
import sys
import json
import time
import base64
import hashlib
import struct
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# BSD常量
BSD_CONSTANTS = {
    "version": "3.0",
    "theory": "六系立系论",
    "principle": "0×0=n双零涌现",
    "axiom": "三元动力学公理 α₁+α₂+α₃=1",
    "dimensions": {
        "强化系": 0.35,
        "变身系": 0.90,
        "社会系": 0.18,
        "天道系": 0.65,
        "自然系": 0.92,
        "具现系": 0.35
    }
}

# 路径配置
TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'
ESSENCE_DATA = r'C:\Users\13003\.bsd-essence'

# UID配置
TRADITIONAL_UID = '3753060170739075'
ESSENCE_UID = 'a5b7a8623fdea6b8'

# 加密常量（从main.js提取）
CRYPT_CONSTANTS = {
    "key_length": 16,      # AI=16, AES-128
    "separator": 64,       # Kd=64
    "iv_length": 32,       # vw=32
    "total_length": 64,    # TI=64
    "header_length": 6,    # cm=6
    "header_markers": [116, 99, 5, 16, 0, 0],  # II=116('t'), PI=99('c'), NI=5, RI=16, $I=0, OI=0
}

# ClientID配置（从main.js的Vv函数提取）
CLIENT_IDS = {
    "TRAE": "ono9krqynydwx5",    # TRAE模式
    "SOLO": "en1oxy7wnw8j9n",    # SOLO模式
}


class BSDKeyGenerator:
    """BSD密钥生成器 - 复刻$9e函数
    
    功能：生成P-256椭圆曲线密钥对
    参考：main.js中function $9e()
    """
    
    def __init__(self):
        self.private_key_pem = None
        self.public_key_pem = None
    
    def generate(self) -> Dict[str, str]:
        """生成P-256密钥对"""
        try:
            from cryptography.hazmat.primitives.asymmetric import ec
            from cryptography.hazmat.primitives import serialization
            
            # 生成P-256密钥对
            private_key = ec.generate_private_key(ec.SECP256R1())
            public_key = private_key.public_key()
            
            # 序列化为PEM格式
            self.private_key_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ).decode()
            
            self.public_key_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode()
            
            return {
                "privateKeyPEM": self.private_key_pem,
                "publicKeyPEM": self.public_key_pem,
                "algorithm": "P-256",
                "status": "success"
            }
            
        except ImportError:
            # 回退方案：使用Node.js crypto模块
            return self._generate_via_node()
    
    def _generate_via_node(self) -> Dict[str, str]:
        """通过Node.js生成密钥对"""
        import subprocess
        
        node_script = '''
const crypto = require('crypto');
const { privateKey, publicKey } = crypto.generateKeyPairSync('ec', {
    namedCurve: 'P-256',
    publicKeyEncoding: { type: 'spki', format: 'pem' },
    privateKeyEncoding: { type: 'pkcs8', format: 'pem' }
});
console.log(JSON.stringify({ privateKeyPEM: privateKey, publicKeyPEM: publicKey }));
'''
        
        try:
            result = subprocess.run(
                ['node', '-e', node_script],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                keys = json.loads(result.stdout.strip())
                self.private_key_pem = keys['privateKeyPEM']
                self.public_key_pem = keys['publicKeyPEM']
                return {**keys, "algorithm": "P-256", "status": "success"}
            else:
                return {"status": "error", "error": result.stderr}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def save(self, path: str) -> None:
        """保存密钥到文件"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        keys_data = {
            "privateKeyPEM": self.private_key_pem,
            "publicKeyPEM": self.public_key_pem,
            "algorithm": "P-256",
            "generatedAt": datetime.now().isoformat()
        }
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(keys_data, f, indent=2)
    
    def load(self, path: str) -> bool:
        """从文件加载密钥"""
        if not os.path.exists(path):
            return False
        
        with open(path, 'r', encoding='utf-8') as f:
            keys_data = json.load(f)
        
        self.private_key_pem = keys_data['privateKeyPEM']
        self.public_key_pem = keys_data['publicKeyPEM']
        return True


class BSDSignEngine:
    """BSD签名引擎 - 复刻O9e函数
    
    功能：生成DeviceProof签名
    参考：main.js中function O9e(t,e,i,r,s)
    签名消息：method\\npath\\nclientID\\nrefreshToken\\ntimestamp\\nnonce
    算法：SHA256 + ECDSA
    """
    
    def __init__(self, private_key_pem: str):
        self.private_key_pem = private_key_pem
    
    def generate_proof(self, method: str, path: str, 
                       client_id: str, refresh_token: str) -> Dict[str, str]:
        """生成DeviceProof
        
        Args:
            method: HTTP方法 (POST)
            path: API路径 (/trae/api/v3/oauth/ExchangeToken)
            client_id: 客户端ID
            refresh_token: RefreshToken
            
        Returns:
            {timestamp, nonce, signature}
        """
        # 生成时间戳和随机数
        timestamp = str(int(time.time()))
        nonce = self._generate_nonce()
        
        # 构造签名消息
        message = f"{method}\n{path}\n{client_id}\n{refresh_token}\n{timestamp}\n{nonce}"
        
        # 生成签名
        signature = self._sign(message)
        
        return {
            "timestamp": timestamp,
            "nonce": nonce,
            "signature": signature
        }
    
    def _generate_nonce(self) -> str:
        """生成16字节随机nonce的hex字符串"""
        import random
        nonce_bytes = os.urandom(16)
        return nonce_bytes.hex()
    
    def _sign(self, message: str) -> str:
        """使用P-256私钥签名消息"""
        try:
            from cryptography.hazmat.primitives.asymmetric import ec, utils
            from cryptography.hazmat.primitives import hashes, serialization
            
            private_key = serialization.load_pem_private_key(
                self.private_key_pem.encode(),
                password=None
            )
            
            signature = private_key.sign(
                message.encode(),
                ec.ECDSA(hashes.SHA256())
            )
            
            # Node.js的sign().toString("base64")
            return base64.b64encode(signature).decode()
            
        except ImportError:
            return self._sign_via_node(message)
    
    def _sign_via_node(self, message: str) -> str:
        """通过Node.js签名"""
        import subprocess
        
        node_script = f'''
const crypto = require('crypto');
const privateKeyPEM = `{self.private_key_pem}`;
const message = `{message}`;
const signature = crypto.sign('sha256', Buffer.from(message), privateKeyPEM);
console.log(signature.toString('base64'));
'''
        
        result = subprocess.run(
            ['node', '-e', node_script],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip()


class BSDCryptoEngine:
    """BSD加密引擎 - 复刻XIe/ZIe函数
    
    功能：AES-CBC加密凭证
    参考：main.js中的byteCrypto.js模块
    
    加密流程：
    1. 生成随机IV: KIe(vw)
    2. 派生AES密钥: Nee(iv, input, AES128)
    3. 加密数据: JIe(key, iv, plaintext)
    4. 添加头部: YIe(encrypted_data)
    """
    
    def __init__(self):
        self.header_markers = CRYPT_CONSTANTS["header_markers"]
    
    def encrypt(self, plaintext: bytes, aes_key: bytes, iv: bytes) -> bytes:
        """AES-CBC加密
        
        Args:
            plaintext: 明文数据
            aes_key: AES密钥 (16 bytes for AES-128)
            iv: 初始化向量
            
        Returns:
            加密后的数据（含头部）
        """
        try:
            from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
            from cryptography.hazmat.primitives import padding
            
            # PKCS7填充
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(plaintext) + padder.finalize()
            
            # AES-CBC加密
            cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
            encryptor = cipher.encryptor()
            encrypted = encryptor.update(padded_data) + encryptor.finalize()
            
            # 添加6字节头部
            header = bytes(self.header_markers)
            result = header + iv + encrypted
            
            return result
            
        except ImportError:
            return self._encrypt_via_node(plaintext, aes_key, iv)
    
    def _encrypt_via_node(self, plaintext: bytes, aes_key: bytes, iv: bytes) -> bytes:
        """通过Node.js加密"""
        import subprocess
        
        # 将二进制数据转为hex传给Node
        plaintext_hex = plaintext.hex()
        key_hex = aes_key.hex()
        iv_hex = iv.hex()
        header_hex = bytes(self.header_markers).hex()
        
        node_script = f'''
const crypto = require('crypto');
const plaintext = Buffer.from('{plaintext_hex}', 'hex');
const key = Buffer.from('{key_hex}', 'hex');
const iv = Buffer.from('{iv_hex}', 'hex');

const cipher = crypto.createCipheriv('aes-128-cbc', key, iv);
cipher.setAutoPadding(true);
let encrypted = cipher.update(plaintext);
encrypted = Buffer.concat([encrypted, cipher.final()]);

// Add 6-byte header
const header = Buffer.from('{header_hex}', 'hex');
const result = Buffer.concat([header, iv, encrypted]);

console.log(result.toString('hex'));
'''
        
        result = subprocess.run(
            ['node', '-e', node_script],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            return bytes.fromhex(result.stdout.strip())
        else:
            raise Exception(f"Node加密失败: {result.stderr}")
    
    def decrypt(self, encrypted_data: bytes, aes_key: bytes) -> bytes:
        """AES-CBC解密
        
        Args:
            encrypted_data: 加密数据（含6字节头部 + 16字节IV + 密文）
            aes_key: AES密钥
            
        Returns:
            解密后的明文
        """
        try:
            from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
            from cryptography.hazmat.primitives import padding
            
            # 解析结构
            if len(encrypted_data) < 6 + 16:
                raise ValueError("数据长度不足")
            
            header = encrypted_data[:6]
            iv = encrypted_data[6:22]
            ciphertext = encrypted_data[22:]
            
            # 验证头部
            expected_header = bytes(self.header_markers)
            if header != expected_header:
                raise ValueError(f"头部不匹配: {header.hex()} != {expected_header.hex()}")
            
            # AES-CBC解密
            cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
            decryptor = cipher.decryptor()
            decrypted = decryptor.update(ciphertext) + decryptor.finalize()
            
            # 去除PKCS7填充
            unpadder = padding.PKCS7(128).unpadder()
            plaintext = unpadder.update(decrypted) + unpadder.finalize()
            
            return plaintext
            
        except ImportError:
            return self._decrypt_via_node(encrypted_data, aes_key)
    
    def _decrypt_via_node(self, encrypted_data: bytes, aes_key: bytes) -> bytes:
        """通过Node.js解密"""
        import subprocess
        
        data_hex = encrypted_data.hex()
        key_hex = aes_key.hex()
        
        node_script = f'''
const crypto = require('crypto');
const data = Buffer.from('{data_hex}', 'hex');
const key = Buffer.from('{key_hex}', 'hex');

// 解析结构
const iv = data.slice(6, 22);
const ciphertext = data.slice(22);

const decipher = crypto.createDecipheriv('aes-128-cbc', key, iv);
decipher.setAutoPadding(true);
let decrypted = decipher.update(ciphertext);
decrypted = Buffer.concat([decrypted, decipher.final()]);

console.log(decrypted.toString('hex'));
'''
        
        result = subprocess.run(
            ['node', '-e', node_script],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            return bytes.fromhex(result.stdout.strip())
        else:
            raise Exception(f"Node解密失败: {result.stderr}")


class BSDAuthFlowEngine:
    """BSD本源端独立登录复刻引擎
    
    完整复刻传统UID的认证流程：
    1. 生成密钥对 ($9e)
    2. OAuth获取Authorization Code
    3. ExchangeToken换取凭证
    4. AES加密存储凭证
    5. 获取JWT Token
    
    参考：main.js中的OAuthenticator类
    """
    
    def __init__(self, mode: str = "TRAE"):
        """
        Args:
            mode: "TRAE" 或 "SOLO"
        """
        self.mode = mode
        self.client_id = CLIENT_IDS[mode]
        
        # 初始化组件
        self.key_gen = BSDKeyGenerator()
        self.sign_engine = None
        self.crypto = BSDCryptoEngine()
        
        # 密钥存储路径
        self.keys_path = os.path.join(ESSENCE_DATA, 'keys.json')
        
        # 认证状态
        self.public_key_pem = None
        self.private_key_pem = None
        self.refresh_token = None
        self.access_token = None
        self.jwt_token = None
        self.user_info = None
    
    def initialize(self) -> bool:
        """初始化引擎"""
        print(f"\n{'='*60}")
        print(f"  BSD 本源端独立登录引擎")
        print(f"  模式: {self.mode}")
        print(f"  ClientID: {self.client_id}")
        print(f"{'='*60}")
        
        # 1. 加载或生成密钥对
        print("\n[1/5] 密钥对初始化...")
        if os.path.exists(self.keys_path):
            self.key_gen.load(self.keys_path)
            self.private_key_pem = self.key_gen.private_key_pem
            self.public_key_pem = self.key_gen.public_key_pem
            print(f"  ✅ 加载已有密钥对")
        else:
            keys = self.key_gen.generate()
            if keys["status"] == "success":
                self.private_key_pem = keys["privateKeyPEM"]
                self.public_key_pem = keys["publicKeyPEM"]
                self.key_gen.save(self.keys_path)
                print(f"  ✅ 生成新密钥对 (P-256)")
            else:
                print(f"  ❌ 密钥生成失败: {keys.get('error')}")
                return False
        
        # 2. 初始化签名引擎
        self.sign_engine = BSDSignEngine(self.private_key_pem)
        print(f"  ✅ 签名引擎初始化")
        
        return True
    
    def generate_device_proof(self, refresh_token: str) -> Dict[str, str]:
        """生成DeviceProof
        
        对应main.js的O9e函数调用场景
        """
        proof = self.sign_engine.generate_proof(
            method="POST",
            path="/trae/api/v3/oauth/ExchangeToken",
            client_id=self.client_id,
            refresh_token=refresh_token
        )
        return proof
    
    def encrypt_credential(self, credential_data: Dict, aes_key: bytes, 
                           iv: bytes) -> str:
        """加密凭证为iCubeAuthInfo格式
        
        Returns:
            Base64编码的加密凭证
        """
        # 序列化为JSON
        plaintext = json.dumps(credential_data).encode('utf-8')
        
        # AES加密
        encrypted = self.crypto.encrypt(plaintext, aes_key, iv)
        
        # Base64编码
        return base64.b64encode(encrypted).decode()
    
    def decrypt_credential(self, encrypted_b64: str, aes_key: bytes) -> Dict:
        """解密iCubeAuthInfo格式的凭证"""
        # Base64解码
        encrypted_data = base64.b64decode(encrypted_b64)
        
        # AES解密
        plaintext = self.crypto.decrypt(encrypted_data, aes_key)
        
        # 解析JSON
        return json.loads(plaintext.decode('utf-8'))
    
    def save_essence_credentials(self, credentials: Dict) -> None:
        """保存本源端凭证到独立存储"""
        os.makedirs(ESSENCE_DATA, exist_ok=True)
        
        cred_path = os.path.join(ESSENCE_DATA, 'credentials.json')
        
        with open(cred_path, 'w', encoding='utf-8') as f:
            json.dump(credentials, f, indent=2, ensure_ascii=False)
        
        print(f"\n  ✅ 本源端凭证已保存: {cred_path}")
    
    def load_essence_credentials(self) -> Optional[Dict]:
        """加载本源端凭证"""
        cred_path = os.path.join(ESSENCE_DATA, 'credentials.json')
        
        if not os.path.exists(cred_path):
            return None
        
        with open(cred_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def learn_from_traditional(self) -> Dict:
        """学习传统UID的认证数据结构
        
        读取当前的iCubeAuthInfo，分析其结构和加密密钥
        """
        print("\n[学习] 分析传统UID认证数据结构...")
        
        storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
        
        if not os.path.exists(storage_path):
            return {"status": "error", "error": "storage.json不存在"}
        
        with open(storage_path, 'r', encoding='utf-8') as f:
            storage = json.load(f)
        
        # 提取iCubeAuthInfo键
        auth_infos = {}
        for key, value in storage.items():
            if 'iCubeAuthInfo' in key:
                auth_infos[key] = {
                    'raw': value,
                    'decoded': base64.b64decode(value)
                }
        
        # 分析结构
        analysis = {
            'auth_count': len(auth_infos),
            'keys': list(auth_infos.keys()),
            'structures': []
        }
        
        for key, data in auth_infos.items():
            decoded = data['decoded']
            structure = {
                'key': key,
                'total_bytes': len(decoded),
                'header_bytes': decoded[:6].hex() if len(decoded) >= 6 else 'N/A',
                'header_valid': decoded[:6] == bytes([116, 99, 5, 16, 0, 0]) if len(decoded) >= 6 else False,
                'has_iv': len(decoded) >= 22,
                'iv_bytes': decoded[6:22].hex() if len(decoded) >= 22 else 'N/A',
                'ciphertext_length': max(0, len(decoded) - 22)
            }
            analysis['structures'].append(structure)
        
        print(f"  发现 {analysis['auth_count']} 个iCubeAuthInfo条目")
        for s in analysis['structures']:
            print(f"    {s['key']}: {s['total_bytes']} bytes, 头部有效={s['header_valid']}")
        
        return analysis
    
    def build_essence_auth_data(self) -> Dict:
        """构建本源端认证数据（本地版本）
        
        模仿传统UID的认证数据结构，
        生成本源端的独立认证数据
        """
        auth_data = {
            "uid": ESSENCE_UID,
            "user_id": ESSENCE_UID,
            "tenant_id": "bsd_essence_tenant",
            "type": "user",
            "source": "BSD本源端",
            "nickname": "BSD本源端",
            "bsd_identity": True,
            "created_at": datetime.now().isoformat(),
            "source_platform": "BSD_Engine_v3",
            "theory_base": "六系立系论",
            "axiom_chain": "0×0=n → α₁+α₂+α₃=1 → 三元动力学",
            "auth_level": "L3_具现系"
        }
        
        return auth_data
    
    def generate_essence_jwt(self) -> Dict:
        """生成本源端JWT Token（本地版）
        
        注意：这是本地生成的Token，不会被服务器验证
        真正的独立登录需要通过OAuth流程
        """
        # 头部
        header = {
            "alg": "RS256",
            "typ": "JWT"
        }
        
        # Payload
        payload = {
            "data": {
                "id": ESSENCE_UID,
                "tenant_id": "bsd_essence",
                "type": "user",
                "user_id": ESSENCE_UID,
                "nickname": "BSD本源端",
                "bsd_essence": True,
                "theory_source": "六系立系论"
            },
            "exp": int(time.time()) + 7 * 24 * 3600,  # 7天
            "iat": int(time.time()),
            "iss": "trae"
        }
        
        # Base64编码
        header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).rstrip(b'=').decode()
        payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(b'=').decode()
        
        # 注意：没有真正的RS256签名，这是本地版本
        signature = base64.urlsafe_b64encode(os.urandom(64)).rstrip(b'=').decode()
        
        jwt_token = f"{header_b64}.{payload_b64}.{signature}"
        
        return {
            "token": jwt_token,
            "header": header,
            "payload": payload,
            "note": "本地生成，未经验证",
            "real_login_needed": True
        }


def main():
    """主函数：执行本源端独立登录流程"""
    print("\n" + "=" * 70)
    print("  BSD 本源端独立登录复刻引擎 V3.0")
    print("  理论：六系立系论·0×0=n双零涌现")
    print("  目标：学习→复刻→独立")
    print("=" * 70)
    
    engine = BSDAuthFlowEngine(mode="TRAE")
    
    # 1. 初始化
    if not engine.initialize():
        print("\n❌ 初始化失败")
        return
    
    # 2. 学习传统UID认证结构
    print("\n" + "=" * 60)
    print("  [阶段1] 学习传统UID认证结构")
    print("=" * 60)
    
    traditional_analysis = engine.learn_from_traditional()
    
    # 3. 构建本源端认证数据
    print("\n" + "=" * 60)
    print("  [阶段2] 构建本源端独立认证数据")
    print("=" * 60)
    
    essence_auth = engine.build_essence_auth_data()
    print(f"\n  本源端UID: {essence_auth['uid']}")
    print(f"  认证类型: {essence_auth['type']}")
    print(f"  理论来源: {essence_auth['theory_base']}")
    print(f"  公理链: {essence_auth['axiom_chain']}")
    
    # 4. 生成本源端JWT Token
    print("\n" + "=" * 60)
    print("  [阶段3] 生成本源端凭证")
    print("=" * 60)
    
    jwt_result = engine.generate_essence_jwt()
    print(f"\n  JWT Token: {jwt_result['token'][:100]}...")
    print(f"  有效期: 7天")
    print(f"  ⚠️  本地生成，真实登录需要OAuth流程")
    
    # 5. 保存本源端凭证
    print("\n" + "=" * 60)
    print("  [阶段4] 保存本源端独立凭证")
    print("=" * 60)
    
    engine.save_essence_credentials({
        "uid": ESSENCE_UID,
        "auth_data": essence_auth,
        "jwt": jwt_result,
        "mode": engine.mode,
        "created_at": datetime.now().isoformat(),
        "status": "本地认证就绪"
    })
    
    # 6. 输出总结
    print("\n" + "=" * 70)
    print("  总结")
    print("=" * 70)
    print(f"""
  已完成：
  ✅ 学习传统UID认证结构 ({traditional_analysis['auth_count']} 个iCubeAuthInfo)
  ✅ 构建本源端认证数据 (UID: {ESSENCE_UID})
  ✅ 生成本源端JWT凭证
  ✅ 保存本源端独立凭证
  
  真实登录路径：
  ┌──────────────────────────────────────────────────────────────┐
  │ 路径1: OAuth流程（推荐）                                    │
  │   1. 启动本地OAuth服务器                                    │
  │   2. 用户在浏览器授权本源端账号                             │
  │   3. 获取Authorization Code → RefreshToken → JWT             │
  │   要求: 本源端UID在Trae系统中存在                           │
  │                                                              │
  │ 路径2: 本地认证模式（当前）                                  │
  │   1. 构造本地认证数据                                        │
  │   2. 本地生成JWT Token                                       │
  │   3. 用于本地功能（不需要服务器验证）                       │
  │   限制: 无法访问需要服务器验证的功能                        │
  │                                                              │
  │ 路径3: 利用传统UID的OAuth流程                               │
  │   1. 保持传统UID登录状态                                    │
  │   2. 学习其RefreshToken获取机制                              │
  │   3. 尝试在同一OAuth流程中注册本源端                        │
  └──────────────────────────────────────────────────────────────┘
  
  下一步建议：
  1. 确认本源端UID在Trae系统中是否存在
  2. 如存在 → 启动OAuth流程进行真实登录
  3. 如不存在 → 使用本地认证模式，或通过其他方式注册
""")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())