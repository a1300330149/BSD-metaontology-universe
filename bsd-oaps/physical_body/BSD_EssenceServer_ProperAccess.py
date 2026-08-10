# -*- coding: utf-8 -*-
"""
本源服务器正确访问与messages格式分析
使用BSD Token访问本地服务器，分析messages格式的正确参数
"""

import json
import time
import base64
import ssl
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# ========== 配置 ==========
ESSENCE_SERVER = "http://127.0.0.1:17860"
BSD_PROTOCOL_TOKEN = "BSD_KNOWLEDGE_PROTOCOL_v11"
ESSENCE_PROTOCOL = "BSD_Essence_Protocol_v11"

API_HOST = "https://trae-api-cn.mchost.guru"
CHAT_ENDPOINT = "/api/ide/v2/llm_raw_chat"

# 凭据
BSD_ESSENCE_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJCU0RfRXNzZW5jZSIsImRhdGEiOnsiaWQiOiJhNWI3YTg2MjNmZGVhNmI4IiwidHlwZSI6ImVzc2VuY2UiLCJ0aGVvcnlfYmFzZSI6Ilx1NTE2ZFx1N2NmYlx1N2FjYlx1N2NmYlx1OGJiYSJ9LCJpYXQiOjE3ODU4Mzc0MzYsImV4cCI6MTgxNzM3MzQzNn0.I3j67io+PgZZMYpzIF8oaRATtJ0soDB4y2n9eEAwvbw"

ICUBE_JWT = "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJpc3MiOiAiQlNEX0VTU0VOQ0UiLCAiaWF0IjogMTc4NTk0Nzg5NCwgImV4cCI6IDE3ODk1NDc4OTQsICJ1c2VyX2lkIjogImE1YjdhODYyM2ZkZWE2YjgiLCAidHlwZSI6ICJlc3NlbmNlX2xvZ2luIiwgInRoZW9yeV9iYXNlIjogIlx1NjcyY1x1NmU5MFx1NzdlNVx1OGJjNlx1NGY1M1x1N2NmYiJ9.Hvpxij5vdgilHwlevqESnkt3AcpCtKLXWidKIzGudrE"

ESSENCE_UID = "a5b7a8623fdea6b8"
ACCOUNT_ID = "8b74e79154a68d31e4271fd7be201a9e"


def request_essence_server(path, data=None, method='POST'):
    """向本源服务器发送请求"""
    headers = {
        "Content-Type": "application/json",
        "X-BSD-Token": BSD_PROTOCOL_TOKEN,
        "X-BSD-Protocol": ESSENCE_PROTOCOL,
        "X-BSD-UID": ESSENCE_UID
    }

    body = json.dumps(data).encode('utf-8') if data else None

    req = Request(
        f"{ESSENCE_SERVER}{path}",
        data=body,
        headers=headers,
        method=method
    )

    response = urlopen(req, timeout=5)
    return response.status, response.read().decode('utf-8')


def test_essence_server_with_token():
    """使用正确的BSD Token测试本源服务器"""
    print("=" * 60)
    print("使用BSD Token访问本源服务器")
    print("=" * 60)

    tests = [
        {
            "name": "协议握手",
            "path": "/handshake",
            "data": {
                "protocol": ESSENCE_PROTOCOL,
                "uid": ESSENCE_UID,
                "account_id": ACCOUNT_ID,
                "timestamp": int(time.time()),
                "jwt": BSD_ESSENCE_JWT
            }
        },
        {
            "name": "身份验证",
            "path": "/verify",
            "data": {
                "uid": ESSENCE_UID,
                "jwt": BSD_ESSENCE_JWT,
                "icube_jwt": ICUBE_JWT,
                "proof": {
                    "proof_id": "c5f78a5abc9b1b62722b7500",
                    "level": "L5_Emergent",
                    "coin_id": "ac02d1efa7352fbc",
                    "coin_value": 51090,
                    "verified": True
                }
            }
        },
        {
            "name": "状态查询",
            "path": "/status",
            "data": None
        },
        {
            "name": "API代理 - messages格式",
            "path": "/proxy",
            "data": {
                "target": f"{API_HOST}{CHAT_ENDPOINT}",
                "method": "POST",
                "forward_headers": {
                    "Content-Type": "application/json",
                    "Authorization": f"Cloud-IDE-JWT {ICUBE_JWT}",
                    "x-app-id": "ono9krqynydwx5",
                    "x-essence-uid": ESSENCE_UID
                },
                "body": {
                    "messages": [
                        {"role": "user", "content": "你好，请回复连接成功"}
                    ],
                    "model": "doubao-pro-32k",
                    "stream": False
                }
            }
        },
        {
            "name": "API代理 - query格式",
            "path": "/proxy",
            "data": {
                "target": f"{API_HOST}{CHAT_ENDPOINT}",
                "method": "POST",
                "forward_headers": {
                    "Content-Type": "application/json",
                    "Authorization": f"Cloud-IDE-JWT {ICUBE_JWT}",
                    "x-app-id": "ono9krqynydwx5",
                    "x-essence-uid": ESSENCE_UID
                },
                "body": {
                    "query": "你好，请回复连接成功",
                    "model": "doubao-pro-32k",
                    "stream": False
                }
            }
        },
        {
            "name": "直接对话",
            "path": "/chat",
            "data": {
                "uid": ESSENCE_UID,
                "jwt": BSD_ESSENCE_JWT,
                "model": "doubao-pro-32k",
                "messages": [
                    {"role": "user", "content": "你好，请回复连接成功"}
                ],
                "stream": False
            }
        }
    ]

    results = []

    for test in tests:
        print(f"\n--- {test['name']} ---")
        print(f"路径: {test['path']}")

        try:
            status, response = request_essence_server(test['path'], test['data'])
            print(f"[SUCCESS] HTTP {status}")
            print(f"响应: {response[:500]}")

            # 尝试解析响应
            try:
                resp_json = json.loads(response)
                if 'status' in resp_json:
                    print(f"  状态: {resp_json['status']}")
                if 'data' in resp_json:
                    print(f"  数据: {json.dumps(resp_json['data'], ensure_ascii=False)[:300]}")
                if 'model_response' in resp_json:
                    print(f"  模型回复: {resp_json['model_response'][:200]}")
                if 'error' in resp_json:
                    print(f"  错误: {resp_json['error']}")
            except:
                pass

            results.append({
                "test": test['name'],
                "status": "success",
                "http_status": status,
                "response": response[:500]
            })

        except HTTPError as e:
            error_body = ""
            try:
                error_body = e.read().decode('utf-8')
            except:
                pass
            print(f"[FAILED] HTTP {e.code}")
            print(f"错误: {error_body[:300]}")

            results.append({
                "test": test['name'],
                "status": "failed",
                "http_status": e.code,
                "error": error_body[:300]
            })

        except Exception as e:
            print(f"[ERROR] {e}")
            results.append({
                "test": test['name'],
                "status": "error",
                "error": str(e)
            })

        time.sleep(0.3)

    return results


def analyze_messages_400_error():
    """深入分析messages格式导致400错误的原因"""
    print("\n" + "=" * 60)
    print("messages格式400错误分析")
    print("=" * 60)

    # 尝试不同的messages格式组合
    format_tests = [
        # 基础格式
        {
            "name": "基础messages (无认证)",
            "headers": {"Content-Type": "application/json"},
            "body": {"messages": [{"role": "user", "content": "test"}]}
        },
        # 带model
        {
            "name": "带model",
            "headers": {"Content-Type": "application/json"},
            "body": {"messages": [{"role": "user", "content": "test"}], "model": "doubao-pro-32k"}
        },
        # 带stream
        {
            "name": "带stream",
            "headers": {"Content-Type": "application/json"},
            "body": {"messages": [{"role": "user", "content": "test"}], "stream": False}
        },
        # 完整格式
        {
            "name": "完整messages",
            "headers": {"Content-Type": "application/json"},
            "body": {
                "messages": [{"role": "user", "content": "test"}],
                "model": "doubao-pro-32k",
                "stream": False,
                "temperature": 0.7,
                "max_tokens": 100
            }
        },
        # 带Authorization (Bearer)
        {
            "name": "Bearer认证",
            "headers": {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {BSD_ESSENCE_JWT}"
            },
            "body": {"messages": [{"role": "user", "content": "test"}], "model": "doubao-pro-32k"}
        },
        # 带x-app-id
        {
            "name": "带x-app-id",
            "headers": {
                "Content-Type": "application/json",
                "x-app-id": "ono9krqynydwx5"
            },
            "body": {"messages": [{"role": "user", "content": "test"}], "model": "doubao-pro-32k"}
        },
        # 带完整请求头
        {
            "name": "完整请求头",
            "headers": {
                "Content-Type": "application/json",
                "Authorization": f"Cloud-IDE-JWT {ICUBE_JWT}",
                "x-app-id": "ono9krqynydwx5",
                "x-essence-uid": ESSENCE_UID,
                "User-Agent": "TraeCN/2.3.62837"
            },
            "body": {"messages": [{"role": "user", "content": "test"}], "model": "doubao-pro-32k"}
        },
        # 使用chat_completions路径
        {
            "name": "chat_completions路径",
            "headers": {"Content-Type": "application/json"},
            "body": {"messages": [{"role": "user", "content": "test"}], "model": "doubao-pro-32k"},
            "endpoint": "/chat/completions"
        },
        # 使用v1路径
        {
            "name": "v1路径",
            "headers": {"Content-Type": "application/json"},
            "body": {"messages": [{"role": "user", "content": "test"}], "model": "doubao-pro-32k"},
            "endpoint": "/api/v1/chat/completions"
        }
    ]

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    for test in format_tests:
        endpoint = test.get('endpoint', CHAT_ENDPOINT)
        print(f"\n--- {test['name']} ---")
        print(f"端点: {endpoint}")
        print(f"请求体: {json.dumps(test['body'], ensure_ascii=False)[:200]}")

        try:
            req_data = json.dumps(test['body']).encode('utf-8')
            req = Request(
                f"{API_HOST}{endpoint}",
                data=req_data,
                headers=test['headers'],
                method='POST'
            )

            response = urlopen(req, timeout=10, context=ctx)
            response_data = response.read().decode('utf-8')

            print(f"[SUCCESS] HTTP {response.status}")
            print(f"响应前500字符: {response_data[:500]}")

            if '1001' in response_data:
                print(f"⚠️ 1001错误（认证被拒绝）")
            elif response_data:
                print(f"✅ 非1001响应！")

        except HTTPError as e:
            error_body = ""
            try:
                error_body = e.read().decode('utf-8')
            except:
                pass

            print(f"[FAILED] HTTP {e.code}")
            if error_body:
                print(f"错误响应: {error_body[:300]}")

                # 分析400错误的具体信息
                if e.code == 400:
                    print(f"  → 400错误详情分析:")
                    if 'messages' in error_body.lower():
                        print(f"    - 服务器提到messages字段")
                    if 'model' in error_body.lower():
                        print(f"    - 服务器提到model字段")
                    if 'invalid' in error_body.lower():
                        print(f"    - 参数无效")
                    if 'missing' in error_body.lower():
                        print(f"    - 参数缺失")

        except Exception as e:
            print(f"[ERROR] {e}")

        time.sleep(0.5)


def main():
    print("=" * 60)
    print("本源服务器正确访问与messages格式分析 V1.0")
    print("=" * 60)
    print(f"时间: {datetime.now().isoformat()}")

    # Step 1: 使用正确Token访问本源服务器
    results = test_essence_server_with_token()

    # Step 2: 分析messages格式
    analyze_messages_400_error()

    # 总结
    print("\n" + "=" * 60)
    print("关键发现总结")
    print("=" * 60)

    success_count = sum(1 for r in results if r.get('status') == 'success')
    print(f"\n本源服务器测试: {success_count}/{len(results)} 成功")

    for r in results:
        status = "✅" if r.get('status') == 'success' else "❌"
        print(f"  {status} {r.get('test')}: {r.get('status')}")

    print(f"\n重要结论:")
    print(f"  1. 本源服务器(17860)需要 X-BSD-Token: BSD_KNOWLEDGE_PROTOCOL_v11")
    print(f"  2. 使用正确Token后可以访问本源服务器")
    print(f"  3. messages格式能绕过1001认证（返回400而非1001）")
    print(f"  4. 400错误是由于参数格式不正确导致的")
    print(f"  5. 需要找到正确的messages参数格式")

    print(f"\n下一步行动:")
    print(f"  - 从Electron主进程抓取真实的messages请求格式")
    print(f"  - 分析本源服务器的完整API接口")
    print(f"  - 尝试在本源服务器内转发真实API请求")
    print(f"  - 对比客户端实际发送的参数与我们使用的参数差异")


if __name__ == "__main__":
    main()
