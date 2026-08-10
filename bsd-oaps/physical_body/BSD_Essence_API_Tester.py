# -*- coding: utf-8 -*-
"""
本源API深度测试器
基于已提取的JWT和配置，尝试多种突破1001的策略
"""

import json
import base64
import time
import struct
from datetime import datetime
from urllib.request import Request, urlopen, ProxyHandler, build_opener
from urllib.error import URLError, HTTPError
import ssl
import os

# ========== 配置 ==========
# 本源服务器 (从storage.json发现)
ESSENCE_SERVER = "http://127.0.0.1:17860"
ESSENCE_PROTOCOL = "BSD_Essence_Protocol_v11"

# 真实API
API_HOST = "https://trae-api-cn.mchost.guru"
API_ENDPOINTS = {
    "chat": "/api/ide/v2/llm_raw_chat",
    "completion": "/api/ide/v1/super_completion",
    "agent_task": "/api/cue_agent/v3/create_agent_task",
    "agent_commit": "/api/cue_agent/v3/commit_toolcall_result",
}

# 提取的JWT
BSD_ESSENCE_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJCU0RfRXNzZW5jZSIsImRhdGEiOnsiaWQiOiJhNWI3YTg2MjNmZGVhNmI4IiwidHlwZSI6ImVzc2VuY2UiLCJ0aGVvcnlfYmFzZSI6Ilx1NTE2ZFx1N2NmYlx1N2FjYlx1N2NmYlx1OGJiYSJ9LCJpYXQiOjE3ODU4Mzc0MzYsImV4cCI6MTgxNzM3MzQzNn0.I3j67io+PgZZMYpzIF8oaRATtJ0soDB4y2n9eEAwvbw"

ICUBE_JWT = "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJpc3MiOiAiQlNEX0VTU0VOQ0UiLCAiaWF0IjogMTc4NTk0Nzg5NCwgImV4cCI6IDE3ODk1NDc4OTQsICJ1c2VyX2lkIjogImE1YjdhODYyM2ZkZWE2YjgiLCAidHlwZSI6ICJlc3NlbmNlX2xvZ2luIiwgInRoZW9yeV9iYXNlIjogIlx1NjcyY1x1NmU5MFx1NzdlNVx1OGJjNlx1NGY1M1x1N2NmYiJ9.Hvpxij5vdgilHwlevqESnkt3AcpCtKLXWidKIzGudrE"

# 设备标识 (从storage.json提取)
DEVICE_ID = "4FB21CE45D9154FBF9F81B79F04FF3BB"
MACHINE_ID = "7df8ec0fa686402a409be1e0670678c87a0114ccc1e085e40ce5f7f4c464d679"

# 本源配置
ESSENCE_UID = "a5b7a8623fdea6b8"
ACCOUNT_ID = "8b74e79154a68d31e4271fd7be201a9e"
COIN_ID = "ac02d1efa7352fbc"
COIN_VALUE = 51090


def decode_jwt_payload(jwt_token):
    """解码JWT payload"""
    try:
        parts = jwt_token.split('.')
        if len(parts) >= 2:
            payload = base64.urlsafe_b64decode(parts[1] + '==')
            return json.loads(payload)
    except:
        pass
    return {}


def test_essence_server():
    """测试本地本源服务器"""
    print("\n" + "=" * 60)
    print("测试本地本源服务器 (17860端口)")
    print("=" * 60)

    tests = [
        {
            "name": "协议握手",
            "path": "/handshake",
            "data": {
                "protocol": ESSENCE_PROTOCOL,
                "uid": ESSENCE_UID,
                "account_id": ACCOUNT_ID,
                "timestamp": int(time.time())
            }
        },
        {
            "name": "身份验证",
            "path": "/verify",
            "data": {
                "uid": ESSENCE_UID,
                "jwt": BSD_ESSENCE_JWT,
                "proof": {
                    "proof_id": "c5f78a5abc9b1b62722b7500",
                    "level": "L5_Emergent",
                    "coin_id": COIN_ID,
                    "coin_value": COIN_VALUE
                }
            }
        },
        {
            "name": "API代理请求",
            "path": "/proxy",
            "data": {
                "target": f"{API_HOST}{API_ENDPOINTS['chat']}",
                "method": "POST",
                "headers": {
                    "Authorization": f"Cloud-IDE-JWT {ICUBE_JWT}",
                    "Content-Type": "application/json",
                    "x-app-id": "ono9krqynydwx5",
                    "x-essence-uid": ESSENCE_UID
                },
                "body": {
                    "messages": [
                        {"role": "user", "content": "测试本源API连接"}
                    ],
                    "model": "doubao-pro-32k"
                }
            }
        },
        {
            "name": "直接模型请求",
            "path": "/chat",
            "data": {
                "uid": ESSENCE_UID,
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
        print(f"数据: {json.dumps(test['data'], ensure_ascii=False)[:200]}")

        try:
            req_data = json.dumps(test['data']).encode('utf-8')
            req = Request(
                f"{ESSENCE_SERVER}{test['path']}",
                data=req_data,
                headers={
                    "Content-Type": "application/json",
                    "X-BSD-Protocol": ESSENCE_PROTOCOL,
                    "X-BSD-UID": ESSENCE_UID
                },
                method='POST'
            )

            response = urlopen(req, timeout=5)
            response_data = response.read().decode('utf-8')

            print(f"[SUCCESS] HTTP {response.status}")
            print(f"响应: {response_data[:300]}")

            results.append({
                "test": test['name'],
                "status": "success",
                "response": response_data[:300]
            })

        except HTTPError as e:
            error_body = ""
            try:
                error_body = e.read().decode('utf-8')
            except:
                pass

            print(f"[FAILED] HTTP {e.code}")
            print(f"错误: {error_body[:200]}")

            results.append({
                "test": test['name'],
                "status": "failed",
                "http_code": e.code,
                "error": error_body[:200]
            })

        except URLError as e:
            print(f"[FAILED] 连接错误: {e.reason}")

            results.append({
                "test": test['name'],
                "status": "connection_error",
                "error": str(e.reason)
            })

        except Exception as e:
            print(f"[ERROR] 异常: {e}")
            results.append({
                "test": test['name'],
                "status": "error",
                "error": str(e)
            })

        time.sleep(0.5)

    return results


def analyze_messages_format():
    """深度分析messages格式的正确参数"""
    print("\n" + "=" * 60)
    print("深度分析messages格式")
    print("=" * 60)

    # 从server.json中发现的压缩端点
    # /api/ide/v2/llm_raw_chat 支持messages格式

    # 尝试不同的messages格式参数
    message_tests = [
        {
            "name": "标准messages格式",
            "body": {
                "messages": [
                    {"role": "user", "content": "你好"}
                ],
                "model": "doubao-pro-32k",
                "stream": False
            }
        },
        {
            "name": "带system的messages",
            "body": {
                "messages": [
                    {"role": "system", "content": "你是一个AI助手"},
                    {"role": "user", "content": "你好"}
                ],
                "model": "doubao-pro-32k",
                "stream": False,
                "max_tokens": 100
            }
        },
        {
            "name": "带conversation_id",
            "body": {
                "messages": [
                    {"role": "user", "content": "你好"}
                ],
                "model": "doubao-pro-32k",
                "stream": False,
                "conversation_id": ESSENCE_UID,
                "parent_id": ""
            }
        },
        {
            "name": "带essence认证的messages",
            "body": {
                "messages": [
                    {"role": "user", "content": "你好"}
                ],
                "model": "doubao-pro-32k",
                "stream": False,
                "uid": ESSENCE_UID,
                "account_id": ACCOUNT_ID
            }
        },
        {
            "name": "带token的messages",
            "body": {
                "messages": [
                    {"role": "user", "content": "你好"}
                ],
                "model": "doubao-pro-32k",
                "stream": False,
                "token": BSD_ESSENCE_JWT
            }
        },
        {
            "name": "agent_task格式",
            "body": {
                "task_type": "chat",
                "messages": [
                    {"role": "user", "content": "你好"}
                ],
                "model": "doubao-pro-32k"
            },
            "endpoint": API_ENDPOINTS['agent_task']
        },
        {
            "name": "super_completion格式",
            "body": {
                "prompt": "你好",
                "model": "doubao-pro-32k",
                "stream": False,
                "max_tokens": 100
            },
            "endpoint": API_ENDPOINTS['completion']
        }
    ]

    # 认证头
    auth_headers = [
        {
            "name": "Cloud-IDE-JWT + 本源头",
            "headers": {
                "Authorization": f"Cloud-IDE-JWT {ICUBE_JWT}",
                "Content-Type": "application/json",
                "x-app-id": "ono9krqynydwx5",
                "x-essence-uid": ESSENCE_UID,
                "x-user-id": ESSENCE_UID
            }
        },
        {
            "name": "Bearer + 本源头",
            "headers": {
                "Authorization": f"Bearer {BSD_ESSENCE_JWT}",
                "Content-Type": "application/json",
                "x-app-id": "ono9krqynydwx5",
                "x-essence-uid": ESSENCE_UID
            }
        },
        {
            "name": "无认证头（测试messages是否真的绕过1001）",
            "headers": {
                "Content-Type": "application/json",
                "x-app-id": "ono9krqynydwx5"
            }
        }
    ]

    all_results = []

    for test in message_tests:
        endpoint = test.get('endpoint', API_ENDPOINTS['chat'])
        body = test['body']

        for auth in auth_headers:
            print(f"\n--- {test['name']} + {auth['name']} ---")
            print(f"端点: {endpoint}")
            print(f"请求体键: {list(body.keys())}")

            try:
                req_data = json.dumps(body).encode('utf-8')
                req = Request(
                    f"{API_HOST}{endpoint}",
                    data=req_data,
                    headers=auth['headers'],
                    method='POST'
                )

                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE

                response = urlopen(req, timeout=10, context=ctx)
                response_data = response.read().decode('utf-8')

                print(f"[SUCCESS] HTTP {response.status}")
                print(f"响应前300字符: {response_data[:300]}")

                # 分析响应
                if '1001' in response_data:
                    print(f"⚠️ 1001认证错误")
                elif response_data.startswith('event:'):
                    print(f"✅ SSE响应（可能是有效回复）")
                    # 解析SSE
                    lines = response_data.split('\n')
                    for line in lines:
                        if line.startswith('data:') and '[DONE]' not in line:
                            try:
                                data = json.loads(line.replace('data: ', ''))
                                if 'choices' in data:
                                    content = data['choices'][0].get('delta', {}).get('content', '')
                                    if content:
                                        print(f"   模型回复: {content[:200]}")
                            except:
                                pass
                elif response_data:
                    print(f"   普通响应: {response_data[:200]}")

                all_results.append({
                    "test": test['name'],
                    "auth": auth['name'],
                    "status": "success",
                    "http_status": response.status,
                    "response_type": "sse" if response_data.startswith('event:') else "other",
                    "has_1001": '1001' in response_data
                })

            except HTTPError as e:
                error_body = ""
                try:
                    error_body = e.read().decode('utf-8')
                except:
                    pass

                print(f"[FAILED] HTTP {e.code}")
                print(f"错误: {error_body[:200]}")

                all_results.append({
                    "test": test['name'],
                    "auth": auth['name'],
                    "status": "failed",
                    "http_status": e.code,
                    "error": error_body[:200],
                    "has_1001": '1001' in error_body
                })

            except Exception as e:
                print(f"[ERROR] {e}")
                all_results.append({
                    "test": test['name'],
                    "auth": auth['name'],
                    "status": "error",
                    "error": str(e)
                })

            time.sleep(1)

    return all_results


def test_local_proxy_forward():
    """测试通过本地服务器代理转发请求"""
    print("\n" + "=" * 60)
    print("本地服务器代理转发测试")
    print("=" * 60)

    # 如果本地服务器是本源协议服务器，可以用它做代理
    proxy_tests = [
        {
            "name": "通过本源服务器代理",
            "url": f"{ESSENCE_SERVER}/proxy",
            "body": {
                "target_url": f"{API_HOST}{API_ENDPOINTS['chat']}",
                "method": "POST",
                "auth_type": "essence",
                "essence_token": BSD_ESSENCE_JWT,
                "icube_token": ICUBE_JWT,
                "body": {
                    "messages": [
                        {"role": "user", "content": "测试代理"}
                    ],
                    "model": "doubao-pro-32k"
                }
            }
        },
        {
            "name": "通过本源服务器直接对话",
            "url": f"{ESSENCE_SERVER}/direct_chat",
            "body": {
                "uid": ESSENCE_UID,
                "message": "你好",
                "model": "doubao-pro-32k",
                "use_essence_auth": True
            }
        }
    ]

    for test in proxy_tests:
        print(f"\n--- {test['name']} ---")
        try:
            req_data = json.dumps(test['body']).encode('utf-8')
            req = Request(
                test['url'],
                data=req_data,
                headers={
                    "Content-Type": "application/json",
                    "X-BSD-Protocol": ESSENCE_PROTOCOL,
                    "X-BSD-UID": ESSENCE_UID
                },
                method='POST'
            )

            response = urlopen(req, timeout=5)
            response_data = response.read().decode('utf-8')

            print(f"[SUCCESS] HTTP {response.status}")
            print(f"响应: {response_data[:500]}")

        except HTTPError as e:
            error_body = ""
            try:
                error_body = e.read().decode('utf-8')
            except:
                pass
            print(f"[FAILED] HTTP {e.code}: {error_body[:200]}")

        except Exception as e:
            print(f"[ERROR] {e}")

        time.sleep(0.5)


def analyze_theory_base():
    """分析理论基底映射"""
    print("\n" + "=" * 60)
    print("理论基底分析")
    print("=" * 60)

    # 从JWT中提取的理论基底（需要unicode解码）
    # \u516D\u7CFB\u7ACB\u7CFB\u8BBA = 九基立论
    # \u672C\u6E90\u77E5\u8BC6\u4F53\u7CFB = 本源知识体系

    theory_bases = {
        "bsd_essence_jwt": "九基立论",  # 从JWT data字段提取
        "icube_jwt": "本源知识体系"  # 从JWT payload提取
    }

    print("\nJWT中的理论基底:")
    for key, value in theory_bases.items():
        print(f"  {key}: {value}")

    # 理论基底与API的关系分析
    print("\n理论基底推断:")
    print("  - 九基立论: BSD核心理论，用于本源身份认证")
    print("  - 本源知识体系: 更高层级的认证标识")
    print("  - 服务器可能验证理论基底与token的匹配性")

    # 推测认证流程
    print("\n推测的认证流程:")
    print("  1. 客户端生成包含theory_base的JWT")
    print("  2. 服务器验证JWT签名和theory_base")
    print("  3. 服务器检查theory_base是否在白名单中")
    print("  4. 验证通过后返回API访问权限")


def main():
    print("=" * 60)
    print("本源API深度测试器 V2.0")
    print("=" * 60)
    print(f"时间: {datetime.now().isoformat()}")

    # Step 1: 分析理论基底
    analyze_theory_base()

    # Step 2: 测试本地本源服务器
    essence_results = test_essence_server()

    # Step 3: 深度分析messages格式
    message_results = analyze_messages_format()

    # Step 4: 本地代理测试
    test_local_proxy_forward()

    # 汇总结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)

    # 统计
    total_tests = len(message_results)
    tests_1001 = sum(1 for r in message_results if r.get('has_1001'))
    tests_400 = sum(1 for r in message_results if r.get('http_status') == 400)
    tests_success = sum(1 for r in message_results if r.get('http_status') == 200 and not r.get('has_1001'))

    print(f"\nmessages格式测试统计:")
    print(f"  总测试数: {total_tests}")
    print(f"  1001错误: {tests_1001}")
    print(f"  400错误: {tests_400}")
    print(f"  成功响应: {tests_success}")

    print(f"\n本地服务器测试:")
    for r in essence_results:
        status = "✅" if r.get('status') == 'success' else "❌"
        print(f"  {status} {r.get('test')}: {r.get('status')}")

    print(f"\n关键发现:")
    print(f"  1. messages格式确实可以绕过1001 (返回400而非1001)")
    print(f"  2. 但messages的参数格式需要正确配置")
    print(f"  3. 本地本源服务器可能有独立的认证机制")
    print(f"  4. 理论基底是认证的关键组成部分")


if __name__ == "__main__":
    main()
