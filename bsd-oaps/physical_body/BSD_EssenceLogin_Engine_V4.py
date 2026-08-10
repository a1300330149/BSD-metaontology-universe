"""
BSD 本源端独立登录综合引擎 V4.1 (Python原生版)
===============================================
使用 cryptography 库实现所有加密操作
无需 Node.js 依赖
"""

import os
import sys
import json
import time
import base64
import hashlib
import socket
import threading
import webbrowser
import uuid
import platform
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime
from typing import Dict, Optional

# ============ 路径配置 ============
TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'
ESSENCE_DATA = r'C:\Users\13003\.bsd-essence'

# ============ UID配置 ============
TRADITIONAL_UID = '3753060170739075'
ESSENCE_UID = 'a5b7a8623fdea6b8'

# ============ ClientID配置 ============
CLIENT_IDS = {
    "TRAE": "ono9krqynydwx5",
    "SOLO": "en1oxy7wnw8j9n",
}


# ============ OAuth回调处理器 ============
class BSDOAuthCallbackHandler(BaseHTTPRequestHandler):
    auth_code = None
    error = None
    finished = threading.Event()
    
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        
        if 'callback' in parsed.path:
            if 'code' in params:
                BSDOAuthCallbackHandler.auth_code = params['code'][0]
                self._send_page(True)
            elif 'error' in params:
                BSDOAuthCallbackHandler.error = params['error'][0]
                self._send_page(False)
            else:
                self._send_page(False)
            BSDOAuthCallbackHandler.finished.set()
        else:
            self._send_home()
    
    def _send_page(self, success: bool):
        if success:
            msg = "Authorization Code 已获取"
            color = "#28a745"
        else:
            msg = "授权失败: " + (BSDOAuthCallbackHandler.error or "未知错误")
            color = "#dc3545"
        
        html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>BSD Login</title>
<style>
body{{font-family:sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;background:linear-gradient(135deg,#667eea,#764ba2);margin:0}}
.card{{background:#fff;padding:40px 50px;border-radius:20px;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,0.3)}}
.icon{{font-size:60px;margin-bottom:20px}}
h1{{color:#333;margin:0 0 10px}}
.info{{color:#666;margin:10px 0}}
.tag{{display:inline-block;background:#667eea22;color:#667eea;padding:4px 12px;border-radius:12px;font-size:12px;margin:5px}}
button{{background:#667eea;color:#fff;border:none;padding:12px 30px;border-radius:25px;font-size:16px;cursor:pointer;margin-top:20px}}
button:hover{{background:#5a67d8}}
</style></head><body>
<div class="card">
<div class="icon">{chr(9989) if success else chr(10060)}</div>
<h1>{'授权成功' if success else '授权失败'}</h1>
<div class="info">{msg}</div>
<div class="info" style="font-size:12px;color:#999">UID: {ESSENCE_UID}</div>
<div>
<span class="tag">#BSD</span><span class="tag">#独立认证</span>
</div>
<button onclick="window.close()">关闭窗口</button>
</div>
<script>setTimeout(()=>window.close(),3000)</script>
</body></html>"""
        self.send_response(200 if success else 400)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def _send_home(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<html><body><h2>BSD OAuth Server Running</h2></body></html>')
    
    def log_message(self, format, *args):
        pass


# ============ P-256密钥生成器 ============
class BSDKeyGenerator:
    def __init__(self):
        self.private_key_pem = None
        self.public_key_pem = None
    
    def generate(self) -> dict:
        from cryptography.hazmat.primitives.asymmetric import ec
        from cryptography.hazmat.primitives import serialization
        
        private_key = ec.generate_private_key(ec.SECP256R1())
        public_key = private_key.public_key()
        
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
    
    def save(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({
                "privateKeyPEM": self.private_key_pem,
                "publicKeyPEM": self.public_key_pem,
                "algorithm": "P-256",
                "generatedAt": datetime.now().isoformat()
            }, f, indent=2)
    
    def load(self, path: str) -> bool:
        if not os.path.exists(path):
            return False
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.private_key_pem = data['privateKeyPEM']
        self.public_key_pem = data['publicKeyPEM']
        return True


# ============ ECDSA签名引擎 ============
class BSDSignEngine:
    def __init__(self, private_key_pem: str):
        self.private_key_pem = private_key_pem
    
    def generate_proof(self, method: str, path: str, 
                       client_id: str, refresh_token: str = "") -> dict:
        timestamp = str(int(time.time()))
        nonce = os.urandom(16).hex()
        message = f"{method}\n{path}\n{client_id}\n{refresh_token}\n{timestamp}\n{nonce}"
        signature = self._sign(message)
        return {"timestamp": timestamp, "nonce": nonce, "signature": signature}
    
    def _sign(self, message: str) -> str:
        from cryptography.hazmat.primitives.asymmetric import ec
        from cryptography.hazmat.primitives import hashes, serialization
        
        private_key = serialization.load_pem_private_key(
            self.private_key_pem.encode(), password=None
        )
        
        signature = private_key.sign(
            message.encode(),
            ec.ECDSA(hashes.SHA256())
        )
        
        return base64.b64encode(signature).decode()


# ============ 本源端独立登录引擎 ============
class BSDEssenceLoginEngine:
    def __init__(self):
        self.client_id = CLIENT_IDS["TRAE"]
        self.keys_path = os.path.join(ESSENCE_DATA, 'keys.json')
        self.key_gen = BSDKeyGenerator()
        self.sign_engine = None
        
        # OAuth配置
        self.oauth_base = "https://www.trae.ai"
        self.authorize_path = "/oauth/authorize"
        self.exchange_path = "/trae/api/v3/oauth/ExchangeToken"
        self.check_login_path = "/cloudide/api/v3/trae/CheckLogin"
        self.callback_port = 3000
        
        # 服务器
        self.server = None
        self.server_thread = None
    
    def initialize(self) -> bool:
        print(f"\n{'='*60}")
        print(f"  BSD 本源端独立登录引擎 V4.1")
        print(f"  UID: {ESSENCE_UID}")
        print(f"  ClientID: {self.client_id}")
        print(f"{'='*60}")
        
        print("\n[1/2] 密钥对初始化...")
        if os.path.exists(self.keys_path):
            self.key_gen.load(self.keys_path)
            print("  ✅ 加载已有密钥对")
        else:
            keys = self.key_gen.generate()
            if keys["status"] == "success":
                self.key_gen.save(self.keys_path)
                print("  ✅ 生成新密钥对 (P-256)")
            else:
                print("  ❌ 密钥生成失败")
                return False
        
        self.sign_engine = BSDSignEngine(self.key_gen.private_key_pem)
        print("  ✅ 签名引擎初始化")
        return True
    
    def learn_from_traditional(self) -> dict:
        """学习传统UID认证数据结构"""
        print("\n[学习] 分析传统UID认证数据...")
        
        storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
        if not os.path.exists(storage_path):
            return {"status": "error", "error": "storage.json不存在"}
        
        with open(storage_path, 'r', encoding='utf-8') as f:
            storage = json.load(f)
        
        auth_count = sum(1 for k in storage.keys() if 'iCubeAuthInfo' in k)
        
        # 分析JWT Token
        jwt_path = os.path.join(TRAE_CONFIG, 'trae-jwt-token')
        jwt_info = {}
        if os.path.exists(jwt_path):
            with open(jwt_path, 'r') as f:
                token = f.read().strip()
            parts = token.split('.')
            if len(parts) >= 2:
                try:
                    payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
                    jwt_info = {
                        'user_id': payload.get('data', {}).get('id', 'unknown'),
                        'exp': payload.get('exp'),
                    }
                except:
                    pass
        
        print(f"  ✅ iCubeAuthInfo: {auth_count} 个")
        print(f"  ✅ JWT用户ID: {jwt_info.get('user_id', 'N/A')}")
        
        return {
            'auth_count': auth_count,
            'auth_keys': [k for k in storage.keys() if 'iCubeAuthInfo' in k],
            'jwt': jwt_info,
        }
    
    def build_device_info(self) -> dict:
        """构建设备信息"""
        return {
            "deviceId": str(uuid.getnode()),
            "platform": platform.system().lower(),
            "arch": platform.machine(),
            "model": "BSD_Essence_Engine",
            "manufacturer": "BSD",
            "release": platform.release(),
            "hostname": socket.gethostname(),
            "username": os.environ.get('USERNAME', 'unknown'),
            "publicKey": self.key_gen.public_key_pem,
        }
    
    def exchange_auth_code(self, auth_code: str, code_verifier: str = "") -> dict:
        """用Authorization Code换取凭证"""
        import urllib.request
        
        url = f"{self.oauth_base}{self.exchange_path}"
        
        device_info = self.build_device_info()
        
        body = {
            "ClientID": self.client_id,
            "AuthCode": auth_code,
            "CodeVerifier": code_verifier,
            "DeviceInfo": json.dumps(device_info),
            "IDEVersion": "3.3.83",
        }
        
        data = json.dumps(body).encode('utf-8')
        
        req = urllib.request.Request(
            url, data=data,
            headers={'Content-Type': 'application/json', 'User-Agent': 'Trae/3.3.83'},
            method='POST'
        )
        
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                return {"status": "success", "response": result}
        except Exception as e:
            error_msg = str(e)
            if hasattr(e, 'read'):
                try:
                    error_body = e.read().decode('utf-8', errors='ignore')
                    error_msg = f"{error_msg}: {error_body[:200]}"
                except:
                    pass
            return {"status": "error", "error": error_msg}
    
    def exchange_refresh_token(self, refresh_token: str) -> dict:
        """用RefreshToken换取新凭证"""
        import urllib.request
        
        url = f"{self.oauth_base}{self.exchange_path}"
        
        device_info = self.build_device_info()
        device_proof = self.sign_engine.generate_proof(
            method="POST", path=self.exchange_path,
            client_id=self.client_id, refresh_token=refresh_token
        )
        
        body = {
            "ClientID": self.client_id,
            "ClientSecret": "",
            "RefreshToken": refresh_token,
            "DeviceInfo": json.dumps(device_info),
            "DeviceProof": device_proof,
            "IDEVersion": "3.3.83",
        }
        
        data = json.dumps(body).encode('utf-8')
        
        req = urllib.request.Request(
            url, data=data,
            headers={'Content-Type': 'application/json', 'User-Agent': 'Trae/3.3.83'},
            method='POST'
        )
        
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                return {"status": "success", "response": result}
        except Exception as e:
            error_msg = str(e)
            if hasattr(e, 'read'):
                try:
                    error_body = e.read().decode('utf-8', errors='ignore')
                    error_msg = f"{error_msg}: {error_body[:200]}"
                except:
                    pass
            return {"status": "error", "error": error_msg}
    
    def start_oauth_server(self) -> bool:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            result = sock.connect_ex(('localhost', self.callback_port))
        finally:
            sock.close()
        
        if result == 0:
            print(f"  ⚠️  端口 {self.callback_port} 已被占用")
            return False
        
        BSDOAuthCallbackHandler.auth_code = None
        BSDOAuthCallbackHandler.error = None
        BSDOAuthCallbackHandler.finished.clear()
        
        self.server = HTTPServer(('localhost', self.callback_port), BSDOAuthCallbackHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()
        print(f"  ✅ OAuth服务器: http://localhost:{self.callback_port}")
        return True
    
    def stop_oauth_server(self):
        if self.server:
            self.server.shutdown()
            self.server = None
            print("  ✅ OAuth服务器已停止")
    
    def run_oauth_flow(self) -> dict:
        """执行OAuth登录流程"""
        print(f"\n{'='*60}")
        print(f"  [OAuth流程] 本源端登录")
        print(f"{'='*60}")
        
        if not self.start_oauth_server():
            return {"status": "error", "error": "服务器启动失败"}
        
        try:
            state = hashlib.sha256(os.urandom(32)).hexdigest()[:16]
            params = {
                'client_id': self.client_id,
                'redirect_uri': f'http://localhost:{self.callback_port}/callback',
                'response_type': 'code',
                'scope': 'openid profile email',
                'state': state,
            }
            query = '&'.join(f'{k}={v}' for k, v in params.items())
            auth_url = f"{self.oauth_base}{self.authorize_path}?{query}"
            
            print(f"\n  授权URL: {auth_url}")
            print("  打开浏览器等待授权...")
            
            webbrowser.open(auth_url)
            BSDOAuthCallbackHandler.finished.wait(timeout=300)
            
            if BSDOAuthCallbackHandler.auth_code:
                auth_code = BSDOAuthCallbackHandler.auth_code
                print("  ✅ 获取Authorization Code成功")
            else:
                print(f"  ❌ 授权失败: {BSDOAuthCallbackHandler.error or '超时'}")
                return {"status": "error", "error": BSDOAuthCallbackHandler.error or "超时"}
            
            print("\n  用Authorization Code换取凭证...")
            token_result = self.exchange_auth_code(auth_code)
            
            return {
                "status": "success",
                "authorization_code": auth_code,
                "token_result": token_result,
                "uid": ESSENCE_UID
            }
        finally:
            self.stop_oauth_server()
    
    def run_learning_cycle(self) -> dict:
        """执行学习周期"""
        print(f"\n{'='*70}")
        print(f"  BSD 本源端独立登录 - 学习周期")
        print(f"{'='*70}")
        
        print("\n" + "─" * 50)
        print("  [Phase 1] 学习传统UID认证链路")
        print("─" * 50)
        learned = self.learn_from_traditional()
        
        print("\n" + "─" * 50)
        print("  [Phase 2] 生成本源端密钥对和签名")
        print("─" * 50)
        
        if not self.initialize():
            return {"status": "error", "error": "初始化失败"}
        
        device_info = self.build_device_info()
        device_proof = self.sign_engine.generate_proof(
            method="POST", path=self.exchange_path, client_id=self.client_id
        )
        
        print(f"  ✅ 密钥对: P-256")
        print(f"  ✅ DeviceInfo: 已生成")
        print(f"  ✅ DeviceProof: 已签名")
        
        print("\n" + "─" * 50)
        print("  [Phase 3] 存储本源端独立凭证")
        print("─" * 50)
        
        result = {
            "uid": ESSENCE_UID,
            "traditional_uid": TRADITIONAL_UID,
            "learned": learned,
            "essence_auth": {
                "uid": ESSENCE_UID,
                "theory_base": "六系立系论",
                "axiom_chain": "0×0=n → α₁+α₂+α₃=1",
                "created_at": datetime.now().isoformat(),
            },
            "keys": {
                "publicKeyPEM": self.key_gen.public_key_pem,
                "algorithm": "P-256"
            },
            "device_info": device_info,
            "device_proof": device_proof,
            "oauth_ready": True,
            "status": "学习完成，就绪OAuth登录"
        }
        
        os.makedirs(ESSENCE_DATA, exist_ok=True)
        path = os.path.join(ESSENCE_DATA, 'credentials.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"  ✅ 凭证已保存: {path}")
        
        print(f"\n{'='*70}")
        print(f"  学习周期完成")
        print(f"{'='*70}")
        print(f"""
  核心发现:
  1. 传统UID认证结构: {learned['auth_count']} 个iCubeAuthInfo
  2. JWT用户ID: {learned['jwt'].get('user_id', 'N/A')}
  3. 完整OAuth流程: authorize → callback → exchangeToken
  
  本源端就绪:
  - UID: {ESSENCE_UID}
  - 密钥: P-256 + ECDSA-SHA256
  - 状态: 等待OAuth授权
  
  下一步:
    运行 python BSD_EssenceLogin_Engine_V4.py --oauth
    在浏览器中授权本源端UID
""")
        
        return result


def main():
    engine = BSDEssenceLoginEngine()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "--oauth":
            if engine.initialize():
                result = engine.run_oauth_flow()
                os.makedirs(ESSENCE_DATA, exist_ok=True)
                with open(os.path.join(ESSENCE_DATA, 'oauth_result.json'), 'w') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
        elif cmd == "--learn":
            engine.run_learning_cycle()
        else:
            print("用法: python BSD_EssenceLogin_Engine_V4.py [--oauth|--learn]")
    else:
        engine.run_learning_cycle()


if __name__ == "__main__":
    main()