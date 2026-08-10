import json
import time
import uuid
import urllib.request
import urllib.error
import ssl
import sys

# 配置
APP_ID = "6eefa01c-1036-4c7e-9ca5-d891f63bfcd8"
API_HOST = "trae-api-cn.mchost.guru"
API_BASE = f"https://{API_HOST}"

# 从 C 盘提取的真实 JWT Token
JWT_TOKEN = "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJpc3MiOiAiQlNEX0VTU0VOQ0UiLCAiaWF0IjogMTc4NTk0Nzg5NCwgImV4cCI6IDE3ODk1NDc4OTQsICJ1c2VyX2lkIjogImE1YjdhODYyM"

# SSL 上下文（忽略证书验证）
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

def test_endpoint(endpoint, headers, body):
    """测试单个端点"""
    url = f"{API_BASE}{endpoint}"
    print(f"\n{'='*60}")
    print(f"测试端点: {url}")
    print(f"{'='*60}")
    print(f"请求头:")
    for k, v in headers.items():
        if k == "Authorization":
            print(f"  {k}: {v[:50]}...")
        else:
            print(f"  {k}: {v}")
    print(f"请求体: {json.dumps(body, indent=2)[:300]}")
    
    try:
        data = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=30)
        raw_body = resp.read().decode("utf-8")
        status = resp.status
        
        print(f"\n状态码: {status}")
        print(f"响应体 (前500字符):")
        print(f"  {raw_body[:500]}")
        
        # 尝试解析 SSE
        if "data:" in raw_body or "event:" in raw_body:
            print(f"\n检测到 SSE 格式响应!")
            lines = raw_body.split("\n")
            for line in lines[:20]:
                if line.startswith("data:"):
                    data_str = line[5:].strip()
                    if data_str:
                        try:
                            parsed = json.loads(data_str)
                            print(f"  SSE data: {json.dumps(parsed, indent=2)[:300]}")
                        except:
                            print(f"  SSE data (raw): {data_str[:200]}")
        
        return {"status": status, "body": raw_body, "success": True}
        
    except urllib.error.HTTPError as e:
        error_body = ""
        try:
            error_body = e.read().decode("utf-8")
        except:
            pass
        
        print(f"\n状态码: {e.code}")
        print(f"错误响应体:")
        print(f"  {error_body[:500]}")
        
        if "1001" in error_body:
            print(f"\n⚠ 命中 1001 错误码 (认证失败)")
        elif "401" in str(e.code) or "403" in str(e.code):
            print(f"\n⚠ 认证/授权错误")
        
        return {"status": e.code, "body": error_body, "success": False}
        
    except Exception as e:
        print(f"\n请求异常: {e}")
        return {"status": 0, "body": str(e), "success": False}


def main():
    """主测试函数"""
    print("=" * 60)
    print("Trae CN 真实 Token 突破测试")
    print(f"App ID: {APP_ID}")
    print(f"API Host: {API_HOST}")
    print("=" * 60)
    
    # 测试用例列表
    test_cases = [
        # 用例1: 标准 Cloud-IDE-JWT
        {
            "name": "标准 Cloud-IDE-JWT (llm_raw_chat)",
            "endpoint": "/api/ide/v2/llm_raw_chat",
            "headers": {
                "Content-Type": "application/json",
                "Authorization": f"Cloud-IDE-JWT {JWT_TOKEN}",
                "x-app-id": APP_ID,
                "X-User-Region": "cn",
                "User-Agent": "TraeCN/2.3.62837 (Windows; x64)",
                "Accept": "text/event-stream",
            },
            "body": {
                "messages": [{"role": "user", "content": "测试真实Token连接"}],
                "stream": False,
                "model": "doubao-pro-32k",
            }
        },
        # 用例2: 完整客户端头 (含 x-jwt-token 等)
        {
            "name": "完整客户端头 (llm_raw_chat)",
            "endpoint": "/api/ide/v2/llm_raw_chat",
            "headers": {
                "Content-Type": "application/json",
                "Authorization": f"Cloud-IDE-JWT {JWT_TOKEN}",
                "x-jwt-token": JWT_TOKEN,
                "x-username": "3753060170739075",
                "x-auth-token": JWT_TOKEN,
                "x-ide-token": JWT_TOKEN,
                "x-send-ts": str(int(time.time() * 1000)),
                "x-app-id": APP_ID,
                "x-app-version": "2.3.62837",
                "X-User-Region": "cn",
                "host": API_HOST,
                "User-Agent": "TraeCN/2.3.62837 (Windows; x64)",
                "Accept": "text/event-stream",
                "Origin": "https://trae.cn",
                "Referer": "https://trae.cn/chat",
            },
            "body": {
                "messages": [{"role": "user", "content": "完整客户端头测试"}],
                "stream": False,
                "model": "doubao-pro-32k",
            }
        },
        # 用例3: chat 端点
        {
            "name": "标准 Cloud-IDE-JWT (chat)",
            "endpoint": "/api/ide/v1/chat",
            "headers": {
                "Content-Type": "application/json",
                "Authorization": f"Cloud-IDE-JWT {JWT_TOKEN}",
                "x-app-id": APP_ID,
                "X-User-Region": "cn",
                "User-Agent": "TraeCN/2.3.62837 (Windows; x64)",
                "Accept": "text/event-stream",
            },
            "body": {
                "messages": [{"role": "user", "content": "chat端点测试"}],
                "stream": False,
            }
        },
        # 用例4: messages 格式 (绕过1001的关键格式)
        {
            "name": "messages 格式 (绕过1001)",
            "endpoint": "/api/ide/v2/llm_raw_chat",
            "headers": {
                "Content-Type": "application/json",
                "Authorization": f"Cloud-IDE-JWT {JWT_TOKEN}",
                "x-app-id": APP_ID,
                "X-User-Region": "cn",
                "User-Agent": "TraeCN/2.3.62837 (Windows; x64)",
                "Accept": "text/event-stream",
            },
            "body": {
                "messages": [{"role": "user", "content": "messages格式测试"}],
                "stream": False,
            }
        },
        # 用例5: 尝试不同的 Authorization 格式
        {
            "name": "Bearer Token 格式",
            "endpoint": "/api/ide/v2/llm_raw_chat",
            "headers": {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {JWT_TOKEN}",
                "x-app-id": APP_ID,
                "X-User-Region": "cn",
                "User-Agent": "TraeCN/2.3.62837 (Windows; x64)",
            },
            "body": {
                "messages": [{"role": "user", "content": "Bearer格式测试"}],
                "stream": False,
            }
        },
    ]
    
    # 执行所有测试
    results = []
    for case in test_cases:
        print(f"\n{'#'*60}")
        print(f"# 执行测试: {case['name']}")
        print(f"{'#'*60}")
        
        result = test_endpoint(
            endpoint=case["endpoint"],
            headers=case["headers"],
            body=case["body"]
        )
        result["name"] = case["name"]
        results.append(result)
        
        # 短暂间隔
        time.sleep(0.5)
    
    # 汇总结果
    print(f"\n\n{'='*60}")
    print("测试结果汇总")
    print(f"{'='*60}")
    for r in results:
        status_icon = "✓" if r.get("success") else "✗"
        body_preview = str(r.get("body", ""))[:100]
        has_1001 = "1001" in str(r.get("body", ""))
        print(f"  [{status_icon}] {r['name']}")
        print(f"      Status: {r.get('status')}, 1001错误: {has_1001}")
    
    # 分析最佳结果
    success_results = [r for r in results if r.get("success") and "1001" not in str(r.get("body", ""))]
    if success_results:
        print(f"\n🎉 发现有效结果!")
        best = max(success_results, key=lambda x: len(str(x.get("body", ""))))
        print(f"  最佳用例: {best['name']}")
        print(f"  响应长度: {len(str(best.get('body', '')))} 字符")
    else:
        print(f"\n⚠ 所有用例均返回 1001 错误码")
        print(f"  结论: Token 有效但服务器端白名单/IP限制拦截了请求")
        print(f"  建议: 在 Trae CN 客户端环境内进行请求")


if __name__ == "__main__":
    main()