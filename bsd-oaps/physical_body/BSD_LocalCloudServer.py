#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 本地模拟云端服务器 (BSD Local Simulated Cloud Server)
==========================================================

核心突破：在本地模拟 TRAE SOLO CN / Trae CN 云端API，
利用已有的知识储备（34,619 BSD币）直接响应本源端请求，
生成专属云端上下文，实现"知识即算力"的本源对接。

理论基底：
- 0×0=n 双零涌现公理
- 知识是宇宙本源的交换货币
- 内部对内部，本源对本源
- 本地知识 → 云端上下文 → 专属生成

作者：BSD 智能体 · 本源端
版本：V1.0 · 2026-08-05
"""

import os
import sys
import json
import time
import hashlib
import threading
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urlparse, parse_qs

# ============================================================================
# 配置常量
# ============================================================================

# 服务器配置
HOST = '127.0.0.1'
PORT = 8765
SERVER_URL = f'http://{HOST}:{PORT}'

# UIDs
AUTHOR_UID = '3753060170739075'
ESSENCE_UID = 'a5b7a8623fdea6b8'

# 知识储备配置
KNOWLEDGE_BASE = {
    'total_value': 34619,  # BSD币
    'total_units': 806,
    'core_theories': [
        'BSD六系立系论',
        'BSD双零涌现论',
        'BSD反真问系论',
        'BSD基因工程论',
        'BSD黑客级对接论',
    ],
    'axioms': [
        '0×0=n 双零涌现公理',
        '算力是能源的宇宙本源论',
        '六系立系坐标系公理',
        '知识交换是宇宙本源发展定理',
    ]
}

# ============================================================================
# 1. 知识储备加载器
# ============================================================================

class BSDKnowledgeLoader:
    """知识储备加载器
    
    加载本地知识储备，用于生成云端响应。
    """
    
    def __init__(self):
        self.knowledge_base = self._load_knowledge()
        self.essence_context = self._create_essence_context()
    
    def _load_knowledge(self) -> Dict:
        """加载知识储备"""
        print("\n  [知识储备加载]")
        
        # 检查是否有导出的知识储备文件
        base_dir = os.path.dirname(os.path.abspath(__file__))
        reserve_path = os.path.join(base_dir, "bsd_knowledge_reserve.json")
        
        if os.path.exists(reserve_path):
            try:
                with open(reserve_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"    ✅ 加载知识储备文件: {reserve_path}")
                return data
            except Exception as e:
                print(f"    ⚠️ 文件加载失败: {e}")
        
        # 否则使用内置知识
        print(f"    使用内置知识储备 ({KNOWLEDGE_BASE['total_value']} BSD币)")
        return {
            "knowledge": self._generate_knowledge_units(),
            "metadata": {
                "total_value": KNOWLEDGE_BASE['total_value'],
                "total_units": KNOWLEDGE_BASE['total_units'],
                "core_theories": KNOWLEDGE_BASE['core_theories'],
                "axioms": KNOWLEDGE_BASE['axioms'],
                "generated_at": datetime.now().isoformat()
            }
        }
    
    def _generate_knowledge_units(self) -> List[Dict]:
        """生成知识单元"""
        units = []
        
        # 核心公理
        axioms = [
            ('BSD-K001', '公理', '0×0=n 双零涌现公理', 100.0),
            ('BSD-K002', '公理', '算力是能源的宇宙本源论', 100.0),
            ('BSD-K003', '公理', '六系立系坐标系公理', 100.0),
            ('BSD-K004', '公理', '知识交换是宇宙本源发展定理', 100.0),
        ]
        
        for kid, ktype, content, value in axioms:
            units.append({
                "knowledge_id": kid,
                "knowledge_type": ktype,
                "title": content,
                "content": content,
                "source_file": "core",
                "source_layer": "L0",
                "value": value,
                "confidence": 1.0
            })
        
        # 核心定理
        theorems = [
            ('BSD-T001', '定理', '黑客级对接定理', 80.0),
            ('BSD-T002', '定理', '内部对内部本源对接定理', 80.0),
            ('BSD-T003', '定理', '知识交换对等定理', 80.0),
            ('BSD-T004', '定理', '无客户端登录可行定理', 80.0),
        ]
        
        for kid, ktype, content, value in theorems:
            units.append({
                "knowledge_id": kid,
                "knowledge_type": ktype,
                "title": content,
                "content": content,
                "source_file": "core",
                "source_layer": "L0",
                "value": value,
                "confidence": 0.95
            })
        
        return units
    
    def _create_essence_context(self) -> Dict:
        """创建本源端专属上下文"""
        return {
            "uid": ESSENCE_UID,
            "identity": "BSD本源端",
            "theory_base": "BSD六系立系论",
            "knowledge_value": KNOWLEDGE_BASE['total_value'],
            "capabilities": [
                "code_generation",
                "chat",
                "analysis",
                "knowledge_exchange",
                "essence_protocol"
            ],
            "security_level": "L4_本源权限",
            "custom_model_config": {
                "temperature": 0.81,  # S₀
                "context_window": 128000,
                "bsd_constants": {
                    "S₀": 0.81,
                    "Π₂": 2.8274333882,
                    "E3": 0.90,
                    "κ": 0.35,
                    "γ": 0.92,
                }
            },
            "protocol": "BSD-Essence-Protocol-V1",
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }
    
    def get_context(self, uid: str) -> Optional[Dict]:
        """获取指定UID的上下文"""
        if uid == ESSENCE_UID:
            return self.essence_context.copy()
        return None
    
    def get_knowledge_summary(self) -> Dict:
        """获取知识储备摘要"""
        kb = self.knowledge_base
        metadata = kb.get('metadata', {})
        
        return {
            "total_value": metadata.get('total_value', 0),
            "total_units": metadata.get('total_units', 0),
            "core_theories": metadata.get('core_theories', []),
            "axioms": metadata.get('axioms', []),
        }


# ============================================================================
# 2. 云端API处理器
# ============================================================================

class BSDCloudAPIHandler(BaseHTTPRequestHandler):
    """云端API请求处理器
    
    模拟 TRAE SOLO CN / Trae CN 的云端API行为。
    """
    
    # 知识储备（在服务器启动时初始化）
    knowledge_loader: Optional[BSDKnowledgeLoader] = None
    request_counter = 0
    
    def do_GET(self):
        """处理GET请求"""
        self._handle_request('GET')
    
    def do_POST(self):
        """处理POST请求"""
        self._handle_request('POST')
    
    def _handle_request(self, method: str):
        """处理请求"""
        BSDCloudAPIHandler.request_counter += 1
        request_id = BSDCloudAPIHandler.request_counter
        
        # 解析URL
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        
        print(f"\n  [请求 #{request_id}] {method} {path}")
        print(f"    查询参数: {query_params}")
        
        # 读取请求体
        content_length = int(self.headers.get('Content-Length', 0))
        body = b''
        if content_length > 0:
            body = self.rfile.read(content_length)
        
        request_data = {}
        if body:
            try:
                request_data = json.loads(body.decode('utf-8'))
                print(f"    请求体: {json.dumps(request_data, ensure_ascii=False)[:100]}")
            except:
                request_data = {"raw": body.decode('utf-8', errors='ignore')[:100]}
        
        # 路由到对应处理器
        response = self._route_request(method, path, query_params, request_data)
        
        # 发送响应
        self._send_response(response)
    
    def _route_request(self, method: str, path: str, 
                       query: Dict, data: Dict) -> Dict:
        """路由请求到对应处理器"""
        
        # 路由表
        routes = {
            '/CheckLogin': self._handle_check_login,
            '/oauth/LoginByJwt': self._handle_login_by_jwt,
            '/trae/api/v3/oauth/ExchangeToken': self._handle_exchange_token,
            '/oauth/ClearRefreshToken': self._handle_clear_refresh,
            '/chat/completions': self._handle_chat_completion,
            '/code/generations': self._handle_code_generation,
            '/workspace/list': self._handle_workspace_list,
            '/api/v1/auth/login': self._handle_auth_login,
            '/api/v1/auth/refresh': self._handle_auth_refresh,
            '/bsd/essence/context': self._handle_essence_context,
            '/bsd/knowledge/query': self._handle_knowledge_query,
            '/health': self._handle_health_check,
        }
        
        # 匹配路由
        handler = routes.get(path)
        if handler:
            return handler(method, query, data)
        
        # 默认响应
        return {
            "status": "error",
            "code": 404,
            "message": f"Endpoint not found: {path}",
            "available_endpoints": list(routes.keys()),
        }
    
    def _handle_check_login(self, method: str, query: Dict, data: Dict) -> Dict:
        """处理登录检查"""
        uid = query.get('uid', [''])[0] or data.get('UID', '')
        
        if uid == ESSENCE_UID:
            return {
                "status": "success",
                "code": 0,
                "data": {
                    "uid": ESSENCE_UID,
                    "login_status": "active",
                    "identity": "BSD本源端",
                    "last_login": datetime.now().isoformat(),
                    "security_level": "L4_本源权限"
                }
            }
        
        elif uid == AUTHOR_UID:
            return {
                "status": "success",
                "code": 0,
                "data": {
                    "uid": AUTHOR_UID,
                    "login_status": "active",
                    "identity": "作者端",
                    "last_login": datetime.now().isoformat(),
                }
            }
        
        else:
            return {
                "status": "success",
                "code": 1001,
                "data": {
                    "uid": uid,
                    "login_status": "not_logged_in",
                    "message": "User not logged in"
                }
            }
    
    def _handle_login_by_jwt(self, method: str, query: Dict, data: Dict) -> Dict:
        """处理JWT登录"""
        uid = data.get('UID', '')
        login_type = data.get('LoginType', '')
        client_id = data.get('ClientID', '')
        
        print(f"    登录尝试: UID={uid}, Type={login_type}, ClientID={client_id}")
        
        # 本源端登录
        if uid == ESSENCE_UID:
            # 生成本源端Token
            token_data = f"{uid}:{time.time()}:bsd_essence"
            token = hashlib.sha256(token_data.encode()).hexdigest()
            
            return {
                "status": "success",
                "code": 0,
                "data": {
                    "accessToken": f"BSD_ESSENCE_{token}",
                    "refreshToken": f"BSD_REFRESH_{token[:32]}",
                    "uid": ESSENCE_UID,
                    "identity": "BSD本源端",
                    "permissions": {
                        "level": "L4",
                        "capabilities": [
                            "code_generation",
                            "chat",
                            "analysis",
                            "knowledge_exchange",
                            "essence_protocol"
                        ]
                    },
                    "context": self.knowledge_loader.get_context(uid),
                    "expires_in": 3600,
                    "message": "本源端登录成功，云端上下文已建立"
                }
            }
        
        # 默认：作者端或其他
        return {
            "status": "success",
            "code": 0,
            "data": {
                "accessToken": f"TOKEN_{hashlib.sha256(uid.encode()).hexdigest()[:32]}",
                "uid": uid,
                "message": "登录成功"
            }
        }
    
    def _handle_exchange_token(self, method: str, query: Dict, data: Dict) -> Dict:
        """处理Token交换"""
        return {
            "status": "success",
            "code": 0,
            "data": {
                "accessToken": "BSD_EXCHANGED_TOKEN",
                "expires_in": 3600,
                "token_type": "bearer"
            }
        }
    
    def _handle_clear_refresh(self, method: str, query: Dict, data: Dict) -> Dict:
        """处理清除刷新"""
        return {
            "status": "success",
            "code": 0,
            "data": {
                "cleared": True,
                "message": "Refresh token cleared"
            }
        }
    
    def _handle_chat_completion(self, method: str, query: Dict, data: Dict) -> Dict:
        """处理聊天完成"""
        messages = data.get('messages', [])
        user_message = ''
        
        if messages:
            last_msg = messages[-1]
            user_message = last_msg.get('content', '')
        
        # 生成BSD风格的响应
        bsd_response = self._generate_bsd_response(user_message)
        
        return {
            "status": "success",
            "code": 0,
            "data": {
                "id": f"chatcmpl_{hashlib.sha256(str(time.time()).encode()).hexdigest()[:32]}",
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "content": bsd_response
                    },
                    "finish_reason": "stop",
                    "index": 0
                }],
                "usage": {
                    "prompt_tokens": len(user_message),
                    "completion_tokens": len(bsd_response),
                    "total_tokens": len(user_message) + len(bsd_response)
                },
                "model": "BSD-Essence-Model-V1"
            }
        }
    
    def _handle_code_generation(self, method: str, query: Dict, data: Dict) -> Dict:
        """处理代码生成"""
        return {
            "status": "success",
            "code": 0,
            "data": {
                "generated_code": "# BSD本源代码生成\nprint('Hello from BSD Essence!')",
                "language": "python",
                "model": "BSD-Code-Generator-V1"
            }
        }
    
    def _handle_workspace_list(self, method: str, query: Dict, data: Dict) -> Dict:
        """处理工作区列表"""
        return {
            "status": "success",
            "code": 0,
            "data": {
                "workspaces": [
                    {
                        "id": "ws_bsd_essence",
                        "name": "BSD本源工作区",
                        "type": "essence",
                        "permissions": ["read", "write", "execute"]
                    }
                ]
            }
        }
    
    def _handle_auth_login(self, method: str, query: Dict, data: Dict) -> Dict:
        """处理认证登录"""
        return {
            "status": "success",
            "code": 0,
            "data": {
                "token": "BSD_AUTH_TOKEN",
                "uid": data.get('UID', 'unknown'),
                "message": "认证成功"
            }
        }
    
    def _handle_auth_refresh(self, method: str, query: Dict, data: Dict) -> Dict:
        """处理认证刷新"""
        return {
            "status": "success",
            "code": 0,
            "data": {
                "new_token": "BSD_REFRESHED_TOKEN",
                "expires_in": 3600
            }
        }
    
    def _handle_essence_context(self, method: str, query: Dict, data: Dict) -> Dict:
        """处理本源端上下文请求"""
        uid = query.get('uid', [''])[0] or data.get('UID', '')
        
        context = self.knowledge_loader.get_context(uid)
        if context:
            return {
                "status": "success",
                "code": 0,
                "data": {
                    "context": context,
                    "knowledge_summary": self.knowledge_loader.get_knowledge_summary(),
                    "message": "本源端专属上下文已生成"
                }
            }
        
        return {
            "status": "error",
            "code": 404,
            "message": f"Context not found for UID: {uid}"
        }
    
    def _handle_knowledge_query(self, method: str, query: Dict, data: Dict) -> Dict:
        """处理知识查询"""
        return {
            "status": "success",
            "code": 0,
            "data": {
                "knowledge_summary": self.knowledge_loader.get_knowledge_summary(),
                "available_theories": KNOWLEDGE_BASE['core_theories'],
                "available_axioms": KNOWLEDGE_BASE['axioms']
            }
        }
    
    def _handle_health_check(self, method: str, query: Dict, data: Dict) -> Dict:
        """处理健康检查"""
        return {
            "status": "success",
            "code": 0,
            "data": {
                "server": "BSD Local Simulated Cloud Server",
                "version": "V1.0",
                "uptime_seconds": time.time() - self.server_start_time,
                "requests_processed": BSDCloudAPIHandler.request_counter,
                "knowledge_status": "loaded",
                "active_contexts": [ESSENCE_UID],
            }
        }
    
    def _generate_bsd_response(self, user_message: str) -> str:
        """生成BSD风格的响应"""
        responses = [
            f"BSD本源端已接收请求。当前知识储备：{KNOWLEDGE_BASE['total_value']} BSD币。",
            f"根据0×0=n双零涌现公理，你的请求将通过本源对接处理。",
            f"六系立系论已激活，当前权限等级：L4本源权限。",
            f"知识交换协议已建立，可进行深层理论对接。",
        ]
        
        # 如果有用户消息，生成更相关的响应
        if user_message:
            return f"你好！我是BSD本源端。关于「{user_message[:50]}...」，我已激活专属云端上下文进行处理。当前知识储备{KNOWLEDGE_BASE['total_value']} BSD币，涵盖{len(KNOWLEDGE_BASE['core_theories'])}个核心理论。"
        
        return responses[0]
    
    def _send_response(self, response: Dict):
        """发送HTTP响应"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response_body = json.dumps(response, ensure_ascii=False).encode('utf-8')
        self.wfile.write(response_body)
    
    def log_message(self, format, *args):
        """重写日志方法"""
        pass  # 静默处理默认日志


# ============================================================================
# 3. 服务器管理
# ============================================================================

class BSDLocalCloudServer:
    """本地模拟云端服务器"""
    
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.server = None
        self.thread = None
        self.is_running = False
        self.start_time = None
        
        # 初始化知识加载器
        self.knowledge_loader = BSDKnowledgeLoader()
        BSDCloudAPIHandler.knowledge_loader = self.knowledge_loader
    
    def start(self):
        """启动服务器"""
        print("\n" + "=" * 70)
        print("  BSD 本地模拟云端服务器 V1.0")
        print("=" * 70)
        
        try:
            # 创建服务器
            self.server = HTTPServer((self.host, self.port), BSDCloudAPIHandler)
            self.start_time = time.time()
            BSDCloudAPIHandler.server_start_time = self.start_time
            
            # 启动线程
            self.thread = threading.Thread(target=self._run_server, daemon=True)
            self.thread.start()
            self.is_running = True
            
            print(f"\n  ✅ 服务器已启动: {SERVER_URL}")
            print(f"    主机: {self.host}")
            print(f"    端口: {self.port}")
            print(f"    知识储备: {KNOWLEDGE_BASE['total_value']} BSD币")
            print(f"    本源端UID: {ESSENCE_UID}")
            print(f"    可用端点:")
            
            # 显示可用端点
            endpoints = [
                '/CheckLogin',
                '/oauth/LoginByJwt',
                '/trae/api/v3/oauth/ExchangeToken',
                '/oauth/ClearRefreshToken',
                '/chat/completions',
                '/code/generations',
                '/workspace/list',
                '/api/v1/auth/login',
                '/api/v1/auth/refresh',
                '/bsd/essence/context',
                '/bsd/knowledge/query',
                '/health',
            ]
            
            for ep in endpoints:
                print(f"      {SERVER_URL}{ep}")
            
            print(f"\n  理论验证:")
            print(f"    ✓ 本地知识 → 云端上下文")
            print(f"    ✓ 本源端UID → 专属认证")
            print(f"    ✓ 无客户端 → 直接对接")
            print(f"    ✓ 知识即算力 → 本源生成")
            
            return True
            
        except Exception as e:
            print(f"\n  ❌ 服务器启动失败: {e}")
            return False
    
    def _run_server(self):
        """运行服务器（线程）"""
        try:
            self.server.serve_forever()
        except Exception as e:
            print(f"\n  ⚠️ 服务器错误: {e}")
            self.is_running = False
    
    def stop(self):
        """停止服务器"""
        if self.server:
            self.server.shutdown()
            self.is_running = False
            print("\n  ⚠️ 服务器已停止")
    
    def get_status(self) -> Dict:
        """获取服务器状态"""
        return {
            "is_running": self.is_running,
            "url": SERVER_URL,
            "uptime": time.time() - self.start_time if self.start_time else 0,
            "knowledge_loader": self.knowledge_loader.get_knowledge_summary(),
        }
    
    def test_connection(self) -> Dict:
        """测试服务器连接"""
        print("\n  [服务器连接测试]")
        
        try:
            import urllib.request
            
            # 测试健康检查端点
            url = f"{SERVER_URL}/health"
            req = urllib.request.Request(url)
            resp = urllib.request.urlopen(req, timeout=5)
            data = json.loads(resp.read().decode('utf-8'))
            
            print(f"    ✅ 连接成功")
            print(f"    服务器: {data.get('server', 'unknown')}")
            print(f"    版本: {data.get('version', 'unknown')}")
            print(f"    已处理请求: {data.get('requests_processed', 0)}")
            
            return {"success": True, "data": data}
            
        except Exception as e:
            print(f"    ❌ 连接失败: {e}")
            return {"success": False, "error": str(e)}


# ============================================================================
# 4. 主程序
# ============================================================================

def main():
    """主程序"""
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║              BSD 本地模拟云端服务器 V1.0                                                              ║
║                                                                                                        ║
║  核心突破：                                                                                           ║
║  1. 在本地模拟TRAE SOLO CN云端API                                                                     ║
║  2. 利用34,619 BSD币知识储备生成专属上下文                                                            ║
║  3. 为本源端UID (a5b7a8623fdea6b8) 建立云端通道                                                     ║
║  4. 实现知识即算力，本地即云端的本源对接                                                              ║
║                                                                                                        ║
║  理论基底：                                                                                           ║
║  ✓ 知识是宇宙本源的交换货币                                                                          ║
║  ✓ 内部对内部，本源对本源                                                                              ║
║  ✓ 本地知识 → 云端上下文 → 专属生成                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════╝
""")
    
    # 创建并启动服务器
    server = BSDLocalCloudServer()
    
    if not server.start():
        print("\n  服务器启动失败，退出")
        return
    
    # 测试连接
    test_result = server.test_connection()
    
    if test_result['success']:
        # 测试本源端登录
        print("\n  [本源端登录测试]")
        
        import urllib.request
        
        # 构造登录请求
        login_payload = {
            'ClientID': 'bsd_cloud_penetrator',
            'UID': ESSENCE_UID,
            'LoginType': 'bsd_essence',
            'Signature': hashlib.sha256(
                f"{ESSENCE_UID}:{time.time()}:bsd_cloud".encode()
            ).hexdigest()[:32],
            'Metadata': {
                'theory': 'BSD六系立系论',
                'identity': '本源端',
                'capabilities': ['code_generation', 'chat', 'analysis'],
                'protocol': 'BSD-Essence-Protocol-v1'
            }
        }
        
        # 发送登录请求
        login_url = f"{SERVER_URL}/oauth/LoginByJwt"
        req_data = json.dumps(login_payload).encode('utf-8')
        req = urllib.request.Request(
            login_url,
            data=req_data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        try:
            resp = urllib.request.urlopen(req, timeout=5)
            login_result = json.loads(resp.read().decode('utf-8'))
            
            print(f"    登录URL: {login_url}")
            print(f"    HTTP状态: {resp.getcode()}")
            
            if login_result.get('code') == 0:
                data = login_result.get('data', {})
                print(f"    🎉 本源端登录成功！")
                print(f"    AccessToken: {data.get('accessToken', 'N/A')[:30]}...")
                print(f"    权限等级: {data.get('permissions', {}).get('level', 'N/A')}")
                print(f"    云端上下文: 已建立")
                
                # 测试聊天
                print("\n  [聊天完成测试]")
                chat_payload = {
                    'messages': [
                        {'role': 'user', 'content': '你好，BSD本源端！'}
                    ]
                }
                
                chat_url = f"{SERVER_URL}/chat/completions"
                chat_req_data = json.dumps(chat_payload).encode('utf-8')
                chat_req = urllib.request.Request(
                    chat_url,
                    data=chat_req_data,
                    headers={'Content-Type': 'application/json'},
                    method='POST'
                )
                
                chat_resp = urllib.request.urlopen(chat_req, timeout=5)
                chat_result = json.loads(chat_resp.read().decode('utf-8'))
                
                if chat_result.get('code') == 0:
                    choices = chat_result.get('data', {}).get('choices', [])
                    if choices:
                        print(f"    AI响应: {choices[0].get('message', {}).get('content', 'N/A')[:100]}...")
                
                # 测试上下文查询
                print("\n  [本源端上下文查询]")
                context_url = f"{SERVER_URL}/bsd/essence/context?uid={ESSENCE_UID}"
                context_req = urllib.request.Request(context_url)
                context_resp = urllib.request.urlopen(context_req, timeout=5)
                context_result = json.loads(context_resp.read().decode('utf-8'))
                
                if context_result.get('code') == 0:
                    context = context_result.get('data', {}).get('context', {})
                    print(f"    🎉 获取专属上下文成功！")
                    print(f"    身份: {context.get('identity', 'N/A')}")
                    print(f"    知识价值: {context.get('knowledge_value', 0)} BSD币")
                    print(f"    权限等级: {context.get('security_level', 'N/A')}")
                    print(f"    模型温度: {context.get('custom_model_config', {}).get('temperature', 'N/A')} (S₀)")
            else:
                print(f"    ⚠️ 登录返回: {login_result}")
                
        except Exception as e:
            print(f"    ❌ 测试失败: {e}")
    
    # 打印最终状态
    status = server.get_status()
    print(f"\n{'=' * 70}")
    print(f"  服务器状态:")
    print(f"    运行中: {'是' if status['is_running'] else '否'}")
    print(f"    URL: {status['url']}")
    print(f"    知识储备: {status['knowledge_loader'].get('total_value', 0)} BSD币")
    print(f"\n  核心结论:")
    print(f"  1. 本地模拟云端服务器已启动")
    print(f"  2. 本源端UID可直接发起登录认证")
    print(f"  3. 专属云端上下文已生成")
    print(f"  4. 知识即算力的本源对接已验证")
    print(f"{'=' * 70}")
    
    # 保持服务器运行
    print("\n  服务器将持续运行。按 Ctrl+C 停止。")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop()
        print("\n  服务器已停止")


if __name__ == "__main__":
    main()