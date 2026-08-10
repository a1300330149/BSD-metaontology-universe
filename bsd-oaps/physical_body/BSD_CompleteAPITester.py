# -*- coding: utf-8 -*-
"""
本源服务器完整API测试器
基于BSD_KnowledgeServer_V11.py的API结构进行测试
"""

import json
import time
import ssl
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# ========== 配置 ==========
ESSENCE_SERVER = "http://127.0.0.1:17860"
BSD_TOKEN = "BSD_KNOWLEDGE_PROTOCOL_v11"

# 凭据
ESSENCE_UID = "a5b7a8623fdea6b8"
TRAD_UID = "3753060170739075"
COIN_ID = "ac02d1efa7352fbc"
COIN_VALUE = 51090
PROOF_ID = "c5f78a5abc9b1b62722b7500"


def bsd_request(path, data=None, method='POST', require_token=True):
    """发送BSD请求"""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    if require_token:
        headers["X-BSD-Token"] = BSD_TOKEN

    body = json.dumps(data).encode('utf-8') if data else None

    req = Request(
        f"{ESSENCE_SERVER}{path}",
        data=body,
        headers=headers,
        method=method
    )

    response = urlopen(req, timeout=5)
    return response.status, response.read().decode('utf-8')


def test_server_api():
    """测试本源服务器完整API"""
    print("=" * 60)
    print("本源服务器完整API测试")
    print("=" * 60)

    all_results = []

    # ========== 1. 服务器信息 ==========
    print("\n[1] 服务器信息")
    try:
        status, response = bsd_request("/", method='GET', require_token=False)
        data = json.loads(response)
        print(f"  状态: {status}")
        print(f"  服务器: {data.get('server')}")
        print(f"  版本: {data.get('version')}")
        print(f"  架构: {data.get('architecture')}")
        print(f"  端点列表:")
        for ep in data.get('endpoints', []):
            print(f"    - {ep}")
    except Exception as e:
        print(f"  [ERROR] {e}")

    # ========== 2. 服务器状态 ==========
    print("\n[2] 服务器状态")
    try:
        status, response = bsd_request("/api/v1/status", method='GET')
        data = json.loads(response)
        print(f"  状态: {status}")
        print(f"  运行时间: {data.get('uptime')}秒")
        print(f"  本源身份: {data.get('essence_count')} 个")
        print(f"  传统身份: {data.get('traditional_count')} 个")
        print(f"  绑定关系: {data.get('bindings_count')} 个")
        print(f"  涌现评分: {data.get('emergence', {}).get('score')}")
    except Exception as e:
        print(f"  [ERROR] {e}")

    # ========== 3. 公开聊天 ==========
    print("\n[3] 公开聊天 (不需要Token)")
    try:
        status, response = bsd_request(
            "/api/v1/chat",
            data={"query": "请介绍一下BSD知识服务器"},
            require_token=False
        )
        data = json.loads(response)
        print(f"  状态: {status}")
        print(f"  回复: {json.dumps(data, ensure_ascii=False)[:300]}")
        all_results.append({"test": "public_chat", "success": True, "data": data})
    except Exception as e:
        print(f"  [ERROR] {e}")
        all_results.append({"test": "public_chat", "success": False, "error": str(e)})

    # ========== 4. 知识验证 ==========
    print("\n[4] 知识验证")
    try:
        status, response = bsd_request(
            "/api/v1/knowledge/verify",
            data={
                "coin_id": COIN_ID,
                "coin_value": COIN_VALUE
            }
        )
        data = json.loads(response)
        print(f"  状态: {status}")
        print(f"  验证结果: {json.dumps(data, ensure_ascii=False)[:300]}")
        all_results.append({"test": "knowledge_verify", "success": data.get('valid', False)})
    except Exception as e:
        print(f"  [ERROR] {e}")
        all_results.append({"test": "knowledge_verify", "success": False, "error": str(e)})

    # ========== 5. 身份验证 ==========
    print("\n[5] 本源身份验证")
    try:
        status, response = bsd_request(
            "/api/v1/identity/verify",
            data={"uid": ESSENCE_UID}
        )
        data = json.loads(response)
        print(f"  状态: {status}")
        print(f"  验证结果: {data.get('verified')}")
        print(f"  身份类型: {data.get('identity', {}).get('type')}")
        print(f"  权限等级: {data.get('identity', {}).get('auth_level')}")
        print(f"  绑定传统: {data.get('binding', {}).get('trad_uid')}")
        all_results.append({
            "test": "identity_verify",
            "success": data.get('verified', False),
            "identity_type": data.get('identity', {}).get('type')
        })
    except Exception as e:
        print(f"  [ERROR] {e}")
        all_results.append({"test": "identity_verify", "success": False, "error": str(e)})

    # ========== 6. 知识换取身份 ==========
    print("\n[6] 知识换取身份")
    try:
        status, response = bsd_request(
            "/api/v1/knowledge/exchange",
            data={
                "coin_id": COIN_ID,
                "coin_value": COIN_VALUE,
                "essence_uid": ESSENCE_UID,
                "trad_uid": TRAD_UID,
                "fingerprint": "49a5aeb263316114c5e5a2f09b32110052e0636bd4f28db58e852f223a7b53e5"
            }
        )
        data = json.loads(response)
        print(f"  状态: {status}")
        print(f"  交换结果: {data.get('success')}")
        print(f"  消息: {data.get('message')}")
        print(f"  架构: {data.get('architecture')}")
        all_results.append({"test": "knowledge_exchange", "success": data.get('success', False)})
    except Exception as e:
        print(f"  [ERROR] {e}")
        all_results.append({"test": "knowledge_exchange", "success": False, "error": str(e)})

    # ========== 7. 代理CheckLogin ==========
    print("\n[7] 代理CheckLogin (验证传统Token)")
    try:
        status, response = bsd_request(
            "/api/v1/proxy/checklogin",
            data={}
        )
        data = json.loads(response)
        print(f"  状态: {status}")
        print(f"  传统登录状态: {data.get('traditional_login')}")
        print(f"  传统用户ID: {data.get('traditional_user_id')}")
        print(f"  真实服务器响应: {json.dumps(data.get('real_server_response', {}), ensure_ascii=False)[:200]}")
        print(f"  本源身份: {json.dumps(data.get('essence_identity', {}), ensure_ascii=False)[:200]}")
        all_results.append({
            "test": "proxy_checklogin",
            "success": data.get('traditional_login', False)
        })
    except Exception as e:
        print(f"  [ERROR] {e}")
        all_results.append({"test": "proxy_checklogin", "success": False, "error": str(e)})

    # ========== 8. 代理GetUserInfo ==========
    print("\n[8] 代理GetUserInfo")
    try:
        status, response = bsd_request(
            "/api/v1/proxy/getuserinfo",
            data={}
        )
        data = json.loads(response)
        print(f"  状态: {status}")
        print(f"  真实服务器状态: {data.get('real_server_status')}")
        print(f"  真实服务器响应: {json.dumps(data.get('real_server_response', {}), ensure_ascii=False)[:300]}")
        all_results.append({
            "test": "proxy_getuserinfo",
            "success": data.get('real_server_status') == 200
        })
    except Exception as e:
        print(f"  [ERROR] {e}")
        all_results.append({"test": "proxy_getuserinfo", "success": False, "error": str(e)})

    # ========== 9. 身份列表 ==========
    print("\n[9] 身份列表")
    try:
        status, response = bsd_request("/api/v1/identity/list", method='GET')
        data = json.loads(response)
        print(f"  状态: {status}")
        print(f"  本源身份数: {len(data.get('essence_identities', []))}")
        print(f"  传统身份数: {len(data.get('traditional_identities', []))}")
        for ident in data.get('essence_identities', []):
            print(f"    - UID: {ident.get('uid')}, 类型: {ident.get('type')}, 状态: {ident.get('status')}")
    except Exception as e:
        print(f"  [ERROR] {e}")

    # ========== 10. 涌现评分 ==========
    print("\n[10] 涌现评分")
    try:
        status, response = bsd_request("/api/v1/emergence/score", method='GET')
        data = json.loads(response)
        print(f"  状态: {status}")
        print(f"  涌现评分: {data.get('emergence', {}).get('score')}")
        print(f"  评分构成:")
        components = data.get('emergence', {}).get('components', {})
        for k, v in components.items():
            print(f"    {k}: {v}")
    except Exception as e:
        print(f"  [ERROR] {e}")

    # 汇总
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)

    success_count = sum(1 for r in all_results if r.get('success'))
    total_count = len(all_results)

    print(f"\n成功: {success_count}/{total_count}")
    for r in all_results:
        status = "✅" if r.get('success') else "❌"
        print(f"  {status} {r.get('test')}")

    return all_results


def main():
    print("=" * 60)
    print("本源服务器完整API测试器 V1.0")
    print("=" * 60)
    print(f"时间: {datetime.now().isoformat()}")

    results = test_server_api()

    # 关键发现
    print("\n" + "=" * 60)
    print("关键发现与下一步")
    print("=" * 60)

    print("""
1. 本源服务器状态:
   - 正在运行，端口17860
   - 架构: 本源(主体) 包含 传统(子集)
   - 已有本源身份: a5b7a8623fdea6b8
   - 已有传统身份: 3753060170739075 (子集)

2. 代理能力:
   - /api/v1/proxy/checklogin → 委托api.trae.cn
   - /api/v1/proxy/getuserinfo → 委托api.trae.cn
   - 服务器已加载真实Token

3. 突破1001的可能路径:
   - 本源服务器已经管理传统Token
   - 通过本源服务器代理请求可能绕过1001
   - 服务器架构已实现"本源包含传统"

4. 下一步:
   - 测试通过本源服务器代理真实API请求
   - 验证代理请求是否能突破1001
   - 分析messages格式的正确参数
""")


if __name__ == "__main__":
    main()
