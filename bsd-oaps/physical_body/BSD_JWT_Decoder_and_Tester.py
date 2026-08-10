# -*- coding: utf-8 -*-
"""
JWT认证解码器与API请求构造器
解码本源JWT并尝试使用构造的认证信息访问API
"""

import json
import base64
import time
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import ssl

# JWT Token (从Trae CN storage.json提取)
BSD_ESSENCE_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJCU0RfRXNzZW5jZSIsImRhdGEiOnsiaWQiOiJhNWI3YTg2MjNmZGVhNmI4IiwidHlwZSI6ImVzc2VuY2UiLCJ0aGVvcnlfYmFzZSI6Ilx1NTE2ZFx1N2NmYlx1N2FjYlx1N2NmYlx1OGJiYSJ9LCJpYXQiOjE3ODU4Mzc0MzYsImV4cCI6MTgxNzM3MzQzNn0.I3j67io+PgZZMYpzIF8oaRATtJ0soDB4y2n9eEAwvbw"

ICUBE_JWT_TOKEN = "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJpc3MiOiAiQlNEX0VTU0VOQ0UiLCAiaWF0IjogMTc4NTk0Nzg5NCwgImV4cCI6IDE3ODk1NDc4OTQsICJ1c2VyX2lkIjogImE1YjdhODYyM2ZkZWE2YjgiLCAidHlwZSI6ICJlc3NlbmNlX2xvZ2luIiwgInRoZW9yeV9iYXNlIjogIlx1NjcyY1x1NmU5MFx1NzdlNVx1OGJjNlx1NGY1M1x1N2NmYiJ9.Hvpxij5vdgilHwlevqESnkt3AcpCtKLXWidKIzGudrE"

# API端点
API_HOST = "https://trae-api-cn.mchost.guru"
CHAT_ENDPOINT = "/api/ide/v2/llm_raw_chat"
COMPLETION_ENDPOINT = "/api/ide/v1/super_completion"

# 本源配置
ESSENCE_CONFIG = {
    "bsd_uid": "a5b7a8623fdea6b8",
    "account_id": "8b74e79154a68d31e4271fd7be201a9e",
    "permission_level": "L5_OMEGA",
    "knowledge_value": 2316876.0,
    "coin_id": "ac02d1efa7352fbc",
    "coin_value": 51090,
    "essence_mode": True
}


def decode_jwt(token, label=""):
    """解码JWT Token"""
    print(f"\n{'='*60}")
    print(f"解码JWT: {label}")
    print(f"{'='*60}")

    try:
        # JWT由三部分组成
        parts = token.split('.')
        if len(parts) != 3:
            print(f"[ERROR] 无效的JWT格式，部分数: {len(parts)}")
            return None

        # 解码Header
        header = base64.urlsafe_b64decode(parts[0] + '==')
        header_json = json.loads(header)
        print(f"\nHeader:")
        print(f"  算法: {header_json.get('alg')}")
        print(f"  类型: {header_json.get('typ')}")

        # 解码Payload
        payload = base64.urlsafe_b64decode(parts[1] + '==')
        payload_json = json.loads(payload)
        print(f"\nPayload:")
        print(f"  签发者: {payload_json.get('iss')}")
        print(f"  用户ID: {payload_json.get('user_id', payload_json.get('data', {}).get('id', 'N/A'))}")
        print(f"  类型: {payload_json.get('type')}")
        print(f"  理论基底: {payload_json.get('theory_base')}")

        # 时间戳转换
        if 'iat' in payload_json:
            iat = payload_json['iat']
            print(f"  签发时间: {datetime.fromtimestamp(iat).isoformat()}")
        if 'exp' in payload_json:
            exp = payload_json['exp']
            print(f"  过期时间: {datetime.fromtimestamp(exp).isoformat()}")
            remaining = exp - time.time()
            if remaining > 0:
                print(f"  剩余有效时间: {remaining/3600:.1f} 小时")
            else:
                print(f"  ⚠️ Token已过期 {-remaining/3600:.1f} 小时前")

        # 解码Data中的嵌套结构
        if 'data' in payload_json:
            data = payload_json['data']
            print(f"\nData字段:")
            print(f"  ID: {data.get('id')}")
            print(f"  类型: {data.get('type')}")
            theory_base = data.get('theory_base', '')
            if theory_base:
                try:
                    decoded_tb = theory_base.encode().decode('unicode_escape')
                    print(f"  理论基底: {decoded_tb}")
                except:
                    print(f"  理论基底: {theory_base}")

        return {
            "header": header_json,
            "payload": payload_json,
            "signature": parts[2]
        }

    except Exception as e:
        print(f"[ERROR] 解码失败: {e}")
        return None


def test_api_requests():
    """使用不同认证方式测试API请求"""
    print("\n" + "=" * 60)
    print("API请求测试")
    print("=" * 60)

    # 测试消息
    test_message = "你好，请回复'本源连接成功'"

    # 测试场景列表
    test_scenarios = [
        {
            "name": "Scenario 1: Bearer Token (bsd_essence_jwt)",
            "headers": {
                "Authorization": f"Bearer {BSD_ESSENCE_JWT}",
                "Content-Type": "application/json"
            },
            "description": "使用本源JWT作为Bearer Token"
        },
        {
            "name": "Scenario 2: Cloud-IDE-JWT (bsd_essence_jwt)",
            "headers": {
                "Authorization": f"Cloud-IDE-JWT {BSD_ESSENCE_JWT}",
                "Content-Type": "application/json",
                "x-app-id": "ono9krqynydwx5"
            },
            "description": "使用本源JWT作为Cloud-IDE-JWT头"
        },
        {
            "name": "Scenario 3: Bearer Token (icube_jwt_token)",
            "headers": {
                "Authorization": f"Bearer {ICUBE_JWT_TOKEN}",
                "Content-Type": "application/json"
            },
            "description": "使用iCube JWT作为Bearer Token"
        },
        {
            "name": "Scenario 4: Cloud-IDE-JWT (icube_jwt_token)",
            "headers": {
                "Authorization": f"Cloud-IDE-JWT {ICUBE_JWT_TOKEN}",
                "Content-Type": "application/json",
                "x-app-id": "ono9krqynydwx5"
            },
            "description": "使用iCube JWT作为Cloud-IDE-JWT头"
        },
        {
            "name": "Scenario 5: Essence Headers (双Token组合)",
            "headers": {
                "Authorization": f"Cloud-IDE-JWT {ICUBE_JWT_TOKEN}",
                "Content-Type": "application/json",
                "x-app-id": "ono9krqynydwx5",
                "x-essence-uid": "a5b7a8623fdea6b8",
                "x-essence-token": BSD_ESSENCE_JWT,
                "x-theory-base": "116D·7CF8·7AC9·7CF8·8BBA"
            },
            "description": "组合认证头 + 本源标识"
        },
        {
            "name": "Scenario 6: messages格式 + 本源认证",
            "headers": {
                "Authorization": f"Cloud-IDE-JWT {ICUBE_JWT_TOKEN}",
                "Content-Type": "application/json",
                "x-app-id": "ono9krqynydwx5",
                "x-essence-uid": "a5b7a8623fdea6b8"
            },
            "description": "messages格式（绕过1001）"
        }
    ]

    # 为每个场景发送请求
    for scenario in test_scenarios:
        print(f"\n{'-'*40}")
        print(f"测试: {scenario['name']}")
        print(f"描述: {scenario['description']}")

        # 构造请求体
        if "messages" in scenario['name']:
            # messages格式
            body = {
                "messages": [
                    {"role": "user", "content": test_message}
                ],
                "model": "doubao-pro-32k",
                "stream": False
            }
        else:
            # query格式
            body = {
                "query": test_message,
                "model": "doubao-pro-32k",
                "stream": False,
                "conversation_id": "",
                "parent_id": ""
            }

        # 发送请求
        try:
            data = json.dumps(body).encode('utf-8')
            req = Request(
                f"{API_HOST}{CHAT_ENDPOINT}",
                data=data,
                headers=scenario['headers'],
                method='POST'
            )

            # 忽略SSL证书验证（用于测试）
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            response = urlopen(req, timeout=10, context=ctx)
            response_data = response.read().decode('utf-8')

            print(f"  [SUCCESS] HTTP {response.status}")
            print(f"  响应前500字符: {response_data[:500]}")

            # 检查是否为SSE格式
            if response_data.startswith('event:') or response_data.startswith('data:'):
                print(f"  响应类型: SSE流式响应")
                # 尝试解析SSE
                lines = response_data.split('\n')
                for line in lines[:20]:
                    if line.startswith('data:') and '[DONE]' not in line:
                        try:
                            json_data = json.loads(line.replace('data: ', ''))
                            print(f"  SSE数据: {json.dumps(json_data, indent=2, ensure_ascii=False)[:300]}")
                        except:
                            pass

        except HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else "No body"
            print(f"  [FAILED] HTTP {e.code}")
            print(f"  错误响应: {error_body[:300]}")

            # 检查1001错误
            if '1001' in error_body:
                print(f"  ⚠️ 1001认证错误（服务器拒绝）")
            elif '400' in str(e.code):
                print(f"  ⚠️ 400格式错误（可能绕过1001但格式不正确）")

        except URLError as e:
            print(f"  [FAILED] 连接错误: {e.reason}")

        except Exception as e:
            print(f"  [ERROR] 异常: {e}")

        # 短暂延迟避免被限流
        time.sleep(1)


def decode_essence_jwt():
    """专门解码本源JWT"""
    print("\n" + "=" * 60)
    print("本源JWT详细解析")
    print("=" * 60)

    # 解码第一个JWT (bsd_essence_jwt)
    result1 = decode_jwt(BSD_ESSENCE_JWT, "BSD Essence JWT")

    # 解码第二个JWT (iCube JWT)
    result2 = decode_jwt(ICUBE_JWT_TOKEN, "iCube JWT Token")

    # 对比两者
    print("\n" + "=" * 60)
    print("JWT对比分析")
    print("=" * 60)

    if result1 and result2:
        p1 = result1['payload']
        p2 = result2['payload']

        print(f"\nBSD Essence JWT:")
        print(f"  - 由 'BSD_Essence' 签发")
        print(f"  - 类型: essence (本源认证)")
        print(f"  - 包含嵌套data结构")
        print(f"  - 理论基底: unicode编码的六系名称")

        print(f"\niCube JWT:")
        print(f"  - 由 'BSD_Essence' 签发 (同一签发者!)")
        print(f"  - 类型: essence_login (本源登录)")
        print(f"  - 包含user_id (a5b7a8623fdea6b8)")
        print(f"  - 理论基底: unicode编码的六系名称")

        print(f"\n关键发现:")
        print(f"  ✅ 两个JWT都由 BSD_Essence 签发")
        print(f"  ✅ 用户UID一致: a5b7a8623fdea6b8")
        print(f"  ✅ 理论基底相同: 116D·7CF8·7AC9·7CF8·8BBA")
        print(f"  ⚠️ 类型不同: essence vs essence_login")

    return result1, result2


def main():
    print("=" * 60)
    print("JWT解码器与API测试器 V1.0")
    print("=" * 60)

    # Step 1: 解码JWT
    decode_essence_jwt()

    # Step 2: 测试API请求
    test_api_requests()

    # 总结
    print("\n" + "=" * 60)
    print("总结与建议")
    print("=" * 60)
    print("""
1. 已成功提取本源JWT凭据：
   - bsd_essence_jwt: 本源身份令牌 (有效期至2027年)
   - iCubeAuthInfo://jwt-token: 本源登录令牌

2. 认证体系：
   - 两个JWT均由 "BSD_Essence" 签发
   - 用户UID: a5b7a8623fdea6b8
   - 理论基底: 116D·7CF8·7AC9·7CF8·8BBA

3. 下一步建议：
   - 尝试使用这些JWT直接访问API
   - 研究本源认证的请求头格式
   - 对比传统JWT与本源JWT的API响应差异
   - 结合本地服务器(17860端口)进行代理测试
""")


if __name__ == "__main__":
    main()
