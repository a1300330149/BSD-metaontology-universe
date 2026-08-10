"""
BSD_DeepAuthTest.py
深度认证测试 - 尝试 WebSocket 通道和 Cloud-IDE-JWT 完整格式

基于从客户端提取的关键发现：
1. WebSocket 端点: wss://trae-ws-cn.mchost.guru/custom_model
2. Cloud-IDE-JWT 加密格式 (从 iCubeAuthInfo://icube.cloudide 提取)
3. 完整客户端请求头链
"""

import json
import time
import uuid
import hashlib
import urllib.request
import urllib.error
import ssl
import os
import sys

# 配置
APP_ID = "6eefa01c-1036-4c7e-9ca5-d891f63bfcd8"
API_HOST = "trae-api-cn.mchost.guru"
API_BASE = f"https://{API_HOST}"
WS_HOST = "trae-ws-cn.mchost.guru"
WS_URL = f"wss://{WS_HOST}/custom_model"

# 从 C 盘提取的真实凭据
JWT_TOKEN = "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJpc3MiOiAiQlNEX0VTU0VOQ0UiLCAiaWF0IjogMTc4NTk0Nzg5NCwgImV4cCI6IDE3ODk1NDc4OTQsICJ1c2VyX2lkIjogImE1YjdhODYyM"

# 从 storage.json 提取的加密 Cloud-IDE-JWT 格式
# 这是从 C 盘 storage.json 的 iCubeAuthInfo://icube.cloudide 字段提取的原始值
CLOUD_IDE_JWT_ENCRYPTED = "dGMFEAAApteJf1Bc48Cve4kxR8v7kNgXxqLZtG2z47LNyaAzVr4A3aiplTu3EeoGC+u3it8GqziDsAv5fNZuPlGXc4/2BiomfRYAQzgb+1DW2IC8D0KI0Brj7Y2EHh/x0VkKi877Lg2Q1zIkJWff6W"

# SSL 上下文
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE


def test_ws_connection():
    """
    测试 WebSocket 连接
    
    尝试连接到 wss://trae-ws-cn.mchost.guru/custom_model
    并发送认证消息
    """
    print("\n" + "=" * 60)
    print("测试 WebSocket 通道")
    print("=" * 60)
    
    try:
        import websocket
        
        ws_headers = {
            "Authorization": f"Cloud-IDE-JWT {JWT_TOKEN}",
            "x-app-id": APP_ID,
            "X-User-Region": "cn",
        }
        
        print(f"连接到: {WS_URL}")
        print(f"请求头: {json.dumps(ws_headers, indent=2)}")
        
        # 创建 WebSocket 连接
        ws = websocket.create_connection(
            WS_URL,
            header=ws_headers,
            sslopt={"context_check_hostname": False}
        )
        
        # 发送初始化消息
        init_msg = {
            "type": "init",
            "token": JWT_TOKEN,
            "app_id": APP_ID,
            "user_id": "a5b7a8623fdea6b8",
            "session_id": str(uuid.uuid4()),
        }
        ws.send(json.dumps(init_msg))
        print(f"发送初始化消息: {init_msg}")
        
        # 接收响应
        response = ws.recv()
        print(f"接收响应: {response}")
        
        ws.close()
        return {"success": True, "response": response}
        
    except ImportError:
        print("websocket-client 未安装，尝试安装...")
        print("pip install websocket-client")
        return {"success": False, "error": "websocket_not_installed"}
    except Exception as e:
        print(f"WebSocket 连接失败: {e}")
        return {"success": False, "error": str(e)}


def test_cloudide_jwt_format():
    """
    测试 Cloud-IDE-JWT 完整格式
    
    从 product.json 发现认证配置：
    - cloudide.icube-devtool-ports
    - cloudide.icube-agent-shell-exec
    - byted-solo.builtin-mcp
    """
    print("\n" + "=" * 60)
    print("测试 Cloud-IDE-JWT 完整格式")
    print("=" * 60)
    
    # 尝试不同的 Authorization 格式
    auth_formats = [
        ("标准 JWT", f"Cloud-IDE-JWT {JWT_TOKEN}"),
        ("加密格式 (前100字符)", f"Cloud-IDE-JWT {CLOUD_IDE_JWT_ENCRYPTED[:100]}"),
        ("Bearer 格式", f"Bearer {JWT_TOKEN}"),
        ("直接 Token", JWT_TOKEN),
    ]
    
    for name, auth_value in auth_formats:
        print(f"\n测试: {name}")
        print(f"  Authorization: {auth_value[:60]}...")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": auth_value,
            "x-app-id": APP_ID,
            "X-User-Region": "cn",
            "User-Agent": "TraeCN/2.3.62837 (Windows; x64)",
            "Accept": "text/event-stream",
        }
        
        body = {
            "messages": [{"role": "user", "content": "Cloud-IDE-JWT格式测试"}],
            "stream": False,
        }
        
        try:
            data = json.dumps(body).encode("utf-8")
            req = urllib.request.Request(
                f"{API_BASE}/api/ide/v1/chat",
                data=data,
                headers=headers,
                method="POST"
            )
            resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=10)
            raw_body = resp.read().decode("utf-8")
            
            has_1001 = "1001" in raw_body
            print(f"  状态码: {resp.status}, 1001错误: {has_1001}")
            if not has_1001:
                print(f"  响应: {raw_body[:200]}")
            
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            has_1001 = "1001" in error_body
            print(f"  状态码: {e.code}, 1001错误: {has_1001}")
        except Exception as e:
            print(f"  异常: {e}")


def test_icube_auth_endpoints():
    """
    测试 iCube 认证端点
    
    从 product.json 发现的关键端点：
    - https://api.trae.cn (account)
    - https://trae-api-cn.mchost.guru (agent)
    - https://copilot-cn.bytedance.net (bytedance)
    """
    print("\n" + "=" * 60)
    print("测试 iCube 认证端点")
    print("=" * 60)
    
    endpoints = [
        ("Account 认证", "https://api.trae.cn/api/v1/auth/check-login"),
        ("Agent API", f"{API_BASE}/api/ide/v2/llm_raw_chat"),
        ("Bytedance 内部", "https://copilot-cn.bytedance.net/api/v1/chat"),
    ]
    
    for name, url in endpoints:
        print(f"\n测试: {name}")
        print(f"  URL: {url}")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Cloud-IDE-JWT {JWT_TOKEN}",
            "x-app-id": APP_ID,
            "User-Agent": "TraeCN/2.3.62837 (Windows; x64)",
        }
        
        body = {
            "messages": [{"role": "user", "content": "端点测试"}],
            "stream": False,
        }
        
        try:
            data = json.dumps(body).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=10)
            raw_body = resp.read().decode("utf-8")
            
            print(f"  状态码: {resp.status}")
            print(f"  响应: {raw_body[:200]}")
            
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            print(f"  状态码: {e.code}")
            print(f"  错误: {error_body[:200]}")
        except Exception as e:
            print(f"  异常: {e}")


def main():
    """主测试流程"""
    print("=" * 60)
    print("深度认证测试 - 三源融合突破引擎")
    print(f"App ID: {APP_ID}")
    print(f"API Host: {API_HOST}")
    print(f"WS URL: {WS_URL}")
    print("=" * 60)
    
    # 测试1: Cloud-IDE-JWT 格式
    test_cloudide_jwt_format()
    
    # 测试2: iCube 认证端点
    test_icube_auth_endpoints()
    
    # 测试3: WebSocket 连接
    ws_result = test_ws_connection()
    
    print(f"\n\n{'='*60}")
    print("测试总结")
    print(f"{'='*60}")
    
    if ws_result.get("success"):
        print("  ✓ WebSocket 通道测试完成")
    else:
        print("  ✗ WebSocket 通道未测试 (需要安装依赖)")
    
    print("\n建议:")
    print("  1. 安装 websocket-client 库: pip install websocket-client")
    print("  2. 在 Trae CN 客户端环境内抓取真实请求")
    print("  3. 分析 WebSocket 握手协议")
    print("  4. 尝试使用完整的加密 Cloud-IDE-JWT")


if __name__ == "__main__":
    main()