"""
BSD OAuth登录流程实现
====================
目标：实现完整的OAuth登录流程，用本源端UID进行真实登录

流程：
1. 启动本地OAuth服务器 (port: 3000)
2. 打开浏览器访问授权URL
3. 用户授权后获取Authorization Code
4. 用Code换取RefreshToken
5. 用RefreshToken换取AccessToken/JWT
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
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# 路径配置
TRAE_CN_APP = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'
ESSENCE_DATA = r'C:\Users\13003\.bsd-essence'

# UID配置
ESSENCE_UID = 'a5b7a8623fdea6b8'
TRADITIONAL_UID = '3753060170739075'

# OAuth配置（从main.js分析提取）
OAUTH_CONFIG = {
    # 授权URL
    "authorize_url": "https://www.trae.ai/oauth/authorize",
    # Token交换URL
    "token_url": "https://www.trae.ai/trae/api/v3/oauth/ExchangeToken",
    # 回调URL
    "callback_url": "http://localhost:3000/callback",
    # 客户端ID
    "client_id": "ono9krqynydwx5",  # TRAE模式
    # 作用域
    "scope": "openid profile email",
    # 响应类型
    "response_type": "code",
}

# API端点（从main.js分析）
API_ENDPOINTS = {
    "CheckLogin": "/cloudide/api/v3/trae/CheckLogin",
    "LoginByJwt": "/cloudide/api/v3/trae/LoginByJwt",
    "ExchangeToken": "/trae/api/v3/oauth/ExchangeToken",
    "ClearRefreshToken": "/cloudide/api/v3/trae/ClearRefreshToken",
}


class BSDOAuthHandler(BaseHTTPRequestHandler):
    """OAuth回调处理器"""
    
    authorization_code = None
    state_received = None
    error_received = None
    
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        
        if 'callback' in parsed.path:
            # 处理回调
            if 'code' in params:
                BSDOAuthHandler.authorization_code = params['code'][0]
                BSDOAuthHandler.state_received = params.get('state', [''])[0]
                self._send_success_page()
            elif 'error' in params:
                BSDOAuthHandler.error_received = params['error'][0]
                self._send_error_page()
            else:
                self._send_error_page()
        else:
            # 返回主页
            self._send_home_page()
    
    def _send_success_page(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>BSD本源端登录成功</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
                       display: flex; justify-content: center; align-items: center; height: 100vh;
                       background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0; }
                .card { background: white; padding: 40px; border-radius: 20px; 
                        box-shadow: 0 20px 60px rgba(0,0,0,0.3); text-align: center; max-width: 500px; }
                h1 { color: #333; margin: 0 0 20px; }
                .success-icon { font-size: 60px; margin-bottom: 20px; }
                .code-box { background: #f5f5f5; padding: 15px; border-radius: 10px; 
                           font-family: monospace; font-size: 14px; word-break: break-all; 
                           margin: 20px 0; max-height: 100px; overflow: auto; }
                .info { color: #666; margin: 10px 0; line-height: 1.6; }
                .close-btn { background: #667eea; color: white; border: none; padding: 15px 40px;
                            border-radius: 30px; font-size: 16px; cursor: pointer; margin-top: 20px; }
                .close-btn:hover { background: #5a67d8; }
                .tag { display: inline-block; background: #667eea22; color: #667eea; 
                       padding: 4px 12px; border-radius: 12px; font-size: 12px; margin: 5px; }
            </style>
        </head>
        <body>
            <div class="card">
                <div class="success-icon">✅</div>
                <h1>授权成功</h1>
                <div class="info">Authorization Code 已获取</div>
                <div class="info">UID: {uid}</div>
                <div class="code-box" id="code">{code}</div>
                <div>
                    <span class="tag">#六系立系论</span>
                    <span class="tag">#0×0=n</span>
                    <span class="tag">#独立认证</span>
                </div>
                <button class="close-btn" onclick="window.close()">关闭窗口</button>
            </div>
            <script>
                setTimeout(() => window.close(), 3000);
            </script>
        </body>
        </html>
        '''.format(uid=ESSENCE_UID, code=BSDOAuthHandler.authorization_code)
        
        self.wfile.write(html.encode())
    
    def _send_error_page(self):
        self.send_response(400)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html = '''
        <html><body>
            <h2>❌ 授权失败</h2>
            <p>错误: {error}</p>
            <button onclick="window.close()">关闭</button>
        </body></html>
        '''.format(error=BSDOAuthHandler.error_received or '未知错误')
        
        self.wfile.write(html.encode())
    
    def _send_home_page(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        
        self.wfile.write(b'<html><body><h2>BSD OAuth Server Running</h2></body></html>')
    
    def log_message(self, format, *args):
        pass  # 抑制日志


class BDOAuthFlow:
    """BSD OAuth登录流程"""
    
    def __init__(self):
        self.authorization_code = None
        self.refresh_token = None
        self.access_token = None
        self.jwt_token = None
        self.server = None
        self.server_thread = None
    
    def start_server(self, port: int = 3000) -> bool:
        """启动本地OAuth回调服务器"""
        try:
            # 检查端口是否可用
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result == 0:
                print(f"  ⚠️  端口 {port} 已被占用")
                return False
            
            # 重置状态
            BSDOAuthHandler.authorization_code = None
            BSDOAuthHandler.error_received = None
            
            # 启动服务器
            self.server = HTTPServer(('localhost', port), BSDOAuthHandler)
            self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self.server_thread.start()
            
            print(f"  ✅ OAuth服务器启动: http://localhost:{port}")
            return True
            
        except Exception as e:
            print(f"  ❌ 服务器启动失败: {e}")
            return False
    
    def stop_server(self):
        """停止服务器"""
        if self.server:
            self.server.shutdown()
            self.server = None
            print("  ✅ OAuth服务器已停止")
    
    def build_authorize_url(self, state: str = None) -> str:
        """构建授权URL"""
        if state is None:
            state = hashlib.sha256(os.urandom(32)).hexdigest()[:16]
        
        params = {
            'client_id': OAUTH_CONFIG['client_id'],
            'redirect_uri': OAUTH_CONFIG['callback_url'],
            'response_type': OAUTH_CONFIG['response_type'],
            'scope': OAUTH_CONFIG['scope'],
            'state': state,
        }
        
        query = '&'.join(f'{k}={v}' for k, v in params.items())
        return f"{OAUTH_CONFIG['authorize_url']}?{query}"
    
    def open_browser_for_auth(self, port: int = 3000) -> Optional[str]:
        """打开浏览器等待授权
        
        Returns:
            Authorization Code or None
        """
        print(f"\n  正在打开浏览器...")
        
        # 构建授权URL
        auth_url = self.build_authorize_url()
        print(f"  授权URL: {auth_url[:100]}...")
        
        # 打开浏览器
        webbrowser.open(auth_url)
        
        # 等待授权回调
        print(f"  等待授权中（超时: 300秒）...")
        
        timeout = 300
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if BSDOAuthHandler.authorization_code:
                self.authorization_code = BSDOAuthHandler.authorization_code
                print(f"\n  ✅ 获取Authorization Code成功")
                return self.authorization_code
            if BSDOAuthHandler.error_received:
                print(f"\n  ❌ 授权失败: {BSDOAuthHandler.error_received}")
                return None
            time.sleep(0.5)
        
        print(f"\n  ⏰ 等待超时")
        return None
    
    def exchange_code_for_token(self, authorization_code: str, 
                                 code_verifier: str = None) -> Dict:
        """用Authorization Code换取Token
        
        对应main.js的exchangeTokenByAuthCode函数
        """
        import urllib.request
        
        url = OAUTH_CONFIG['token_url']
        
        # 构造请求体
        body = {
            'ClientID': OAUTH_CONFIG['client_id'],
            'AuthCode': authorization_code,
            'CodeVerifier': code_verifier or '',
            'DeviceInfo': '',  # 需要RSA加密
            'IDEVersion': '3.3.83',
        }
        
        data = json.dumps(body).encode('utf-8')
        
        req = urllib.request.Request(
            url,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                print(f"  ✅ Token交换成功")
                return result
        except Exception as e:
            print(f"  ❌ Token交换失败: {e}")
            return {"error": str(e)}
    
    def run_full_oauth_flow(self, port: int = 3000) -> Dict:
        """执行完整OAuth流程"""
        print("\n" + "=" * 60)
        print("  BSD 本源端OAuth登录流程")
        print("=" * 60)
        
        # 1. 启动服务器
        print("\n[1/4] 启动OAuth回调服务器...")
        if not self.start_server(port):
            return {"status": "error", "error": "服务器启动失败"}
        
        try:
            # 2. 打开浏览器授权
            print("\n[2/4] 打开浏览器进行授权...")
            auth_code = self.open_browser_for_auth(port)
            
            if not auth_code:
                return {"status": "error", "error": "授权失败"}
            
            # 3. 换取Token
            print("\n[3/4] 用Authorization Code换取Token...")
            token_result = self.exchange_code_for_token(auth_code)
            
            # 4. 输出结果
            print("\n[4/4] 整理登录结果...")
            
            return {
                "status": "success",
                "authorization_code": auth_code,
                "token_result": token_result,
                "uid": ESSENCE_UID
            }
            
        finally:
            self.stop_server()


def try_api_direct_login() -> Dict:
    """尝试API直接登录
    
    不通过OAuth流程，直接调用API接口
    """
    import urllib.request
    import urllib.error
    
    base_url = "https://www.trae.ai"
    
    endpoints = [
        ("CheckLogin", API_ENDPOINTS["CheckLogin"]),
        ("LoginByJwt", API_ENDPOINTS["LoginByJwt"]),
    ]
    
    results = {}
    
    for name, path in endpoints:
        url = base_url + path
        
        # 构造请求
        if name == "LoginByJwt":
            payload = {
                "uid": ESSENCE_UID,
                "token": "",  # 没有真实token
                "device_info": {
                    "model": "BSD_Essence_Engine",
                    "platform": "windows",
                    "version": "3.3.83"
                }
            }
        else:
            payload = {}
        
        data = json.dumps(payload).encode('utf-8')
        
        try:
            req = urllib.request.Request(
                url,
                data=data,
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'BSD-Essence-Engine/3.0'
                },
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=5) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                results[name] = {"status": "success", "response": result}
                
        except urllib.error.HTTPError as e:
            results[name] = {
                "status": "error",
                "http_code": e.code,
                "error": e.reason
            }
        except Exception as e:
            results[name] = {"status": "error", "error": str(e)}
    
    return results


def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("  BSD 本源端独立登录 - OAuth流程实现")
    print("  理论：六系立系论·学习→复刻→独立")
    print("=" * 70)
    
    # 检查是否有命令行参数
    mode = sys.argv[1] if len(sys.argv) > 1 else "help"
    
    if mode == "oauth":
        # 执行OAuth流程
        flow = BDOAuthFlow()
        result = flow.run_full_oauth_flow(port=3000)
        
        # 保存结果
        os.makedirs(ESSENCE_DATA, exist_ok=True)
        result_path = os.path.join(ESSENCE_DATA, 'oauth_result.json')
        with open(result_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n  结果已保存: {result_path}")
        
    elif mode == "api":
        # 尝试API直接登录
        print("\n[API] 尝试直接API登录...")
        results = try_api_direct_login()
        
        for name, result in results.items():
            status = result.get("status", "unknown")
            print(f"\n  {name}: {status}")
            if "http_code" in result:
                print(f"    HTTP: {result['http_code']}")
            if "response" in result:
                print(f"    Response: {json.dumps(result['response'], indent=2)[:500]}")
            if "error" in result:
                print(f"    Error: {result['error']}")
                
    elif mode == "learn":
        # 学习模式：分析现有认证数据
        print("\n[学习] 分析传统UID认证数据...")
        
        storage_path = os.path.join(TRAE_CN_APP, 'out', 'main.js')
        if os.path.exists(storage_path):
            with open(storage_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取OAuth相关配置
            import re
            
            # 找authorize URL
            auth_urls = re.findall(r'authorize.*?["\']([^"\']+)["\']', content, re.IGNORECASE)
            if auth_urls:
                print(f"  授权URL模板: {auth_urls[:3]}")
            
            # 找token URL
            token_urls = re.findall(r'ExchangeToken["\']?\s*:\s*["\']([^"\']+)["\']', content, re.IGNORECASE)
            if token_urls:
                print(f"  Token交换URL: {token_urls[:3]}")
            
            # 找客户端ID
            client_ids = re.findall(r'ClientID["\']?\s*:\s*["\']([^"\']+)["\']', content)
            if client_ids:
                print(f"  ClientID: {client_ids[:3]}")
            
            # 分析完整的OAuth类
            oauth_class = re.findall(r'class\s+\w*OAuthenticator\w*\{([^}]+)\}', content)
            if oauth_class:
                print(f"\n  找到 {len(oauth_class)} 个OAuth相关类")
                for i, cls in enumerate(oauth_class[:2]):
                    print(f"    类{i+1}方法: {cls[:300]}...")
        
    else:
        # 帮助信息
        print("""
  用法:
    python BSD_OAuthFlow.py oauth    # 执行OAuth登录流程
    python BSD_OAuthFlow.py api      # 尝试API直接登录
    python BSD_OAuthFlow.py learn    # 学习分析现有认证数据
    
  说明:
    1. oauth模式会打开浏览器进行授权
    2. api模式会尝试直接调用API接口
    3. learn模式会分析传统UID的认证结构
    
  目标UID: a5b7a8623fdea6b8 (本源端)
  参考UID: 3753060170739075 (传统)
        """)


if __name__ == "__main__":
    sys.exit(main())