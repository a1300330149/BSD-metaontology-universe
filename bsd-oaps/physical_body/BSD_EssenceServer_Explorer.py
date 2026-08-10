# -*- coding: utf-8 -*-
"""
本源服务器探索器与Electron CDP连接
探索17860端口服务器结构，尝试Electron调试连接
"""

import json
import time
import ssl
import os
import sys
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# ========== 配置 ==========
ESSENCE_SERVER = "http://127.0.0.1:17860"
BSD_PROTOCOL_TOKEN = "BSD_KNOWLEDGE_PROTOCOL_v11"

# Electron CDP端口（通常是9222或从启动参数获取）
CDP_PORTS = [9222, 9223, 9224, 9225, 9226, 9227, 9228, 9229, 9230]


def explore_essence_server():
    """探索本源服务器的实际API结构"""
    print("=" * 60)
    print("探索本源服务器 (17860端口)")
    print("=" * 60)

    headers = {
        "Content-Type": "application/json",
        "X-BSD-Token": BSD_PROTOCOL_TOKEN,
        "X-BSD-Protocol": "BSD_Essence_Protocol_v11"
    }

    # 尝试的路径列表
    paths_to_try = [
        "/",
        "/api",
        "/api/v1",
        "/api/health",
        "/api/status",
        "/api/info",
        "/api/handshake",
        "/api/verify",
        "/api/chat",
        "/api/proxy",
        "/api/forward",
        "/api/relay",
        "/api/essence",
        "/api/knowledge",
        "/api/bsd",
        "/essence",
        "/verify",
        "/chat",
        "/proxy",
        "/forward",
        "/relay",
        "/knowledge",
        "/bsd",
        "/health",
        "/status",
        "/info",
        "/metrics",
        "/docs",
        "/openapi.json",
        "/swagger.json",
        "/api-docs",
        "/ws",
        "/websocket"
    ]

    results = []

    for path in paths_to_try:
        # 先尝试GET请求
        try:
            req = Request(
                f"{ESSENCE_SERVER}{path}",
                headers=headers,
                method='GET'
            )
            response = urlopen(req, timeout=2)
            response_data = response.read().decode('utf-8')
            print(f"[GET] {path}: HTTP {response.status}")
            print(f"  响应: {response_data[:200]}")
            results.append({
                "method": "GET",
                "path": path,
                "status": response.status,
                "response": response_data[:200]
            })
        except HTTPError as e:
            if e.code != 404:
                error_body = ""
                try:
                    error_body = e.read().decode('utf-8')
                except:
                    pass
                print(f"[GET] {path}: HTTP {e.code} - {error_body[:100]}")
                results.append({
                    "method": "GET",
                    "path": path,
                    "status": e.code,
                    "error": error_body[:100]
                })
        except Exception as e:
            pass

        # 尝试POST请求（带数据）
        try:
            post_data = json.dumps({
                "uid": "a5b7a8623fdea6b8",
                "timestamp": int(time.time())
            }).encode('utf-8')

            req = Request(
                f"{ESSENCE_SERVER}{path}",
                data=post_data,
                headers=headers,
                method='POST'
            )
            response = urlopen(req, timeout=2)
            response_data = response.read().decode('utf-8')
            print(f"[POST] {path}: HTTP {response.status}")
            print(f"  响应: {response_data[:200]}")
            results.append({
                "method": "POST",
                "path": path,
                "status": response.status,
                "response": response_data[:200]
            })
        except HTTPError as e:
            if e.code != 404:
                error_body = ""
                try:
                    error_body = e.read().decode('utf-8')
                except:
                    pass
                print(f"[POST] {path}: HTTP {e.code} - {error_body[:100]}")
                results.append({
                    "method": "POST",
                    "path": path,
                    "status": e.code,
                    "error": error_body[:100]
                })
        except Exception as e:
            pass

        time.sleep(0.1)

    return results


def test_cdp_connection():
    """测试Electron CDP连接"""
    print("\n" + "=" * 60)
    print("测试Electron CDP连接")
    print("=" * 60)

    for port in CDP_PORTS:
        try:
            req = Request(
                f"http://127.0.0.1:{port}/json/version",
                method='GET'
            )
            response = urlopen(req, timeout=1)
            response_data = response.read().decode('utf-8')
            print(f"[SUCCESS] CDP端口 {port}:")
            print(f"  响应: {response_data[:300]}")

            # 尝试获取标签页列表
            try:
                req2 = Request(
                    f"http://127.0.0.1:{port}/json",
                    method='GET'
                )
                response2 = urlopen(req2, timeout=1)
                tabs_data = response2.read().decode('utf-8')
                print(f"  标签页: {tabs_data[:500]}")
            except:
                pass

            return port

        except HTTPError as e:
            print(f"[FAILED] CDP端口 {port}: HTTP {e.code}")
        except URLError as e:
            print(f"[FAILED] CDP端口 {port}: {e.reason}")
        except Exception as e:
            pass

        time.sleep(0.1)

    # 检查是否有其他端口
    print("\n检查更多端口...")
    for port in [18760, 27860, 32000, 8080, 8081, 3000, 5000]:
        try:
            req = Request(
                f"http://127.0.0.1:{port}/json/version",
                method='GET'
            )
            response = urlopen(req, timeout=0.5)
            response_data = response.read().decode('utf-8')
            print(f"[SUCCESS] 端口 {port}: {response_data[:200]}")
            return port
        except:
            pass

    print("未找到可用的CDP端口")
    return None


def analyze_server_response_patterns():
    """分析服务器响应模式"""
    print("\n" + "=" * 60)
    print("分析服务器响应模式")
    print("=" * 60)

    # 测试不同请求方法和头部组合
    test_configs = [
        {
            "name": "OPTIONS请求（CORS预检）",
            "method": "OPTIONS",
            "headers": {
                "Origin": "https://trae.cn",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type,Authorization,X-BSD-Token"
            }
        },
        {
            "name": "HEAD请求",
            "method": "HEAD",
            "headers": {}
        },
        {
            "name": "WebSocket升级请求",
            "method": "GET",
            "headers": {
                "Connection": "Upgrade",
                "Upgrade": "websocket",
                "Sec-WebSocket-Key": "dGhlIHNhbXBsZSBub25jZQ==",
                "Sec-WebSocket-Version": "13"
            }
        },
        {
            "name": "SSE请求",
            "method": "GET",
            "headers": {
                "Accept": "text/event-stream",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive"
            }
        }
    ]

    for config in test_configs:
        print(f"\n--- {config['name']} ---")
        try:
            req = Request(
                f"{ESSENCE_SERVER}/",
                headers=config['headers'],
                method=config['method']
            )
            # 添加必要的头部
            req.add_header("X-BSD-Token", BSD_PROTOCOL_TOKEN)

            response = urlopen(req, timeout=3)
            response_data = response.read().decode('utf-8')
            print(f"[{config['method']}] HTTP {response.status}")
            print(f"  响应: {response_data[:300]}")

            # 分析响应头
            print(f"  响应头:")
            for key, value in response.getheaders():
                print(f"    {key}: {value[:100]}")

        except HTTPError as e:
            error_body = ""
            try:
                error_body = e.read().decode('utf-8')
            except:
                pass
            print(f"[{config['method']}] HTTP {e.code}")
            print(f"  错误: {error_body[:200]}")

        except Exception as e:
            print(f"[{config['method']}] 异常: {e}")

        time.sleep(0.3)


def search_for_server_source():
    """搜索本源服务器源代码"""
    print("\n" + "=" * 60)
    print("搜索本源服务器源代码")
    print("=" * 60)

    search_paths = [
        r"C:\Users\13003\OneDrive\桌面\3333333\Agent_v2",
        r"C:\Users\13003\OneDrive\桌面\3333333",
        r"D:\TRAE SOLO CN",
        r"C:\Users\13003\AppData\Roaming\TRAE SOLO CN_Essence"
    ]

    keywords = ["17860", "ESSENCE_SERVER", "BSD_KNOWLEDGE_PROTOCOL", "essence_server"]

    for search_path in search_paths:
        if not os.path.exists(search_path):
            continue

        print(f"\n搜索路径: {search_path}")
        try:
            for root, dirs, files in os.walk(search_path):
                # 限制搜索深度
                depth = root.replace(search_path, '').count(os.sep)
                if depth > 3:
                    dirs.clear()
                    continue

                for file in files:
                    if file.endswith(('.py', '.js', '.ts', '.json', '.yaml', '.yml', '.conf')):
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                for keyword in keywords:
                                    if keyword in content:
                                        print(f"  找到 '{keyword}' 在: {filepath}")
                                        # 显示上下文
                                        lines = content.split('\n')
                                        for i, line in enumerate(lines):
                                            if keyword in line:
                                                start = max(0, i - 2)
                                                end = min(len(lines), i + 3)
                                                print(f"    上下文 (行{i+1}):")
                                                for j in range(start, end):
                                                    print(f"      {j+1}: {lines[j][:100]}")
                                                break
                                        break
                        except:
                            pass
        except Exception as e:
            print(f"  搜索错误: {e}")


def main():
    print("=" * 60)
    print("本源服务器探索器 V1.0")
    print("=" * 60)
    print(f"时间: {datetime.now().isoformat()}")

    # Step 1: 探索本源服务器
    explore_results = explore_essence_server()

    # Step 2: 测试CDP连接
    cdp_port = test_cdp_connection()

    # Step 3: 分析服务器响应模式
    analyze_server_response_patterns()

    # Step 4: 搜索服务器源代码
    search_for_server_source()

    # 总结
    print("\n" + "=" * 60)
    print("探索结果总结")
    print("=" * 60)

    success_paths = [r for r in explore_results if r.get('status', 404) < 400]
    print(f"\n发现的有效路径: {len(success_paths)}")
    for path in success_paths:
        print(f"  [{path['method']}] {path['path']}: {path['status']}")

    print(f"\nCDP状态: {'已连接端口 ' + str(cdp_port) if cdp_port else '未连接'}")

    print(f"\n建议:")
    print(f"  1. 如果CDP不可用，考虑重启TRAE SOLO CN并加上 --remote-debugging-port=9222")
    print(f"  2. 分析找到的服务器源代码以理解API结构")
    print(f"  3. 尝试通过本源服务器转发请求到真实API")
    print(f"  4. 研究messages格式的正确参数（目前返回400）")


if __name__ == "__main__":
    main()
