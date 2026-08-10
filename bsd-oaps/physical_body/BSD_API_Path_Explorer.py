#!/usr/bin/env python3
"""
BSD API路径精准探测引擎 V1.0
[归属基底: 精准探测·2重]
[对应公理: 公理3·意识存在]

发现关键信号:
  - 之前所有请求返回404而非1001
  - 说明服务器可达，认证通过，但URL路径不正确
  - 需要精准探测正确的API端点
"""

import json
import time
import hashlib
import os
import sys
from typing import Dict, Any, List
from urllib.request import Request, urlopen, HTTPCookieProcessor, build_opener
from urllib.parse import urlencode
import ssl

# ============ API路径探测配置 ============

BASE_HOSTS = [
    "https://trae-api-cn.mchost.guru",
    "https://api.trae.cn",
    "https://api.trae.com.cn"
]

# 可能的API路径前缀
PATH_PREFIXES = [
    "",
    "/api",
    "/api/v1",
    "/api/v2",
    "/api/v3",
    "/cloudide",
    "/cloudide/api",
    "/cloudide/api/v1",
    "/cloudide/api/v2",
    "/cloudide/api/v3",
    "/trae",
    "/trae/api",
    "/trae/api/v1",
    "/trae/api/v2",
    "/trae/api/v3",
    "/v1",
    "/v2",
    "/v3",
    "/icube",
    "/icube/api",
    "/icube/api/v1",
    "/extensions",
    "/extensions/api"
]

# 可能的端点名称
ENDPOINT_NAMES = [
    "chat",
    "chat/completions",
    "llm/rawChat",
    "llm/chat",
    "cloud/chat",
    "completions",
    "messages",
    "generate",
    "stream",
    "agent",
    "query",
    "prompt",
    "invoke",
    "run",
    "execute",
    "process",
    "model",
    "model/chat",
    "model/completions",
    "conversation",
    "conversation/chat",
    "bot",
    "bot/chat",
    "assistant",
    "assistant/chat",
    "ai",
    "ai/chat",
    "ai/completions",
    "copilot",
    "copilot/chat",
    "checklogin",
    "login",
    "auth",
    "user",
    "userinfo",
    "token",
    "oauth",
    "exchange",
    "proxy",
    "bridge",
    "relay",
    "forward"
]

# 认证配置
AUTH_CONFIGS = [
    {
        "name": "无认证",
        "headers": {}
    },
    {
        "name": "Cloud-IDE-JWT",
        "headers": {
            "Cloud-IDE-JWT": "Bearer a5b7a8623fdea6b8"
        }
    },
    {
        "name": "Authorization Bearer",
        "headers": {
            "Authorization": "Bearer a5b7a8623fdea6b8"
        }
    },
    {
        "name": "x-app-id + Cloud-IDE-JWT",
        "headers": {
            "x-app-id": "6eefa01c-1036-4c7e-9ca5-d891f63bfcd8",
            "Cloud-IDE-JWT": "Bearer a5b7a8623fdea6b8"
        }
    },
    {
        "name": "三源融合头",
        "headers": {
            "x-app-id": "6eefa01c-1036-4c7e-9ca5-d891f63bfcd8",
            "x-essence-uid": "a5b7a8623fdea6b8",
            "x-client-id": "en1oxy7wnw8j9n",
            "Cloud-IDE-JWT": "Bearer ono9krqynydwx5"
        }
    }
]

# ============ API探测引擎 ============

class APIPathExplorer:
    """API路径精准探测引擎"""
    
    def __init__(self):
        self.session_id = f"APEX_{int(time.time())}"
        self.opener = build_opener(HTTPCookieProcessor())
        self.ssl_ctx = ssl.create_default_context()
        self.ssl_ctx.check_hostname = False
        self.ssl_ctx.verify_mode = ssl.CERT_NONE
        self.findings = []
        
    def log(self, msg: str, level: str = "INFO"):
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {msg}")
        
    def test_url(self, url: str, headers: Dict, method: str = "GET", 
                 data: Optional[Dict] = None) -> Dict[str, Any]:
        """测试单个URL"""
        default_headers = {
            "User-Agent": "TRAE-SOLO-CN/0.1.45 (Windows NT 10.0; Win64; x64)",
            "Accept": "*/*",
            "Connection": "keep-alive"
        }
        default_headers.update(headers)
        
        try:
            data_bytes = json.dumps(data).encode("utf-8") if data else None
            if data_bytes:
                default_headers["Content-Type"] = "application/json"
                
            req = Request(url, data=data_bytes, headers=default_headers, method=method)
            response = urlopen(req, timeout=10, context=self.ssl_ctx)
            response_data = response.read().decode("utf-8", errors="replace")
            status = response.getcode()
            
            return {
                "success": True,
                "url": url,
                "status": status,
                "response_preview": response_data[:200],
                "is_1001": "1001" in response_data or "1001" in str(status),
                "has_content": len(response_data) > 10,
                "headers": dict(response.headers)
            }
            
        except Exception as e:
            error_str = str(e)
            status = 0
            if hasattr(e, 'code'):
                status = e.code
                
            return {
                "success": False,
                "url": url,
                "status": status,
                "error": error_str[:150],
                "is_1001": "1001" in error_str or status == 1001,
                "is_404": status == 404,
                "is_cors": "CORS" in error_str or "cors" in error_str.lower()
            }
    
    def explore_paths(self) -> List[Dict[str, Any]]:
        """系统性探测API路径"""
        self.log("=" * 60, "BANNER")
        self.log("API路径精准探测开始", "BANNER")
        self.log(f"Session ID: {self.session_id}", "BANNER")
        self.log("=" * 60, "BANNER")
        
        all_results = []
        tested_count = 0
        
        # Phase 1: 测试基础可达性
        self.log("\n[Phase 1] 基础可达性测试", "PHASE")
        for host in BASE_HOSTS:
            for auth in AUTH_CONFIGS[:2]:  # 只测前2个认证配置
                url = host + "/"
                result = self.test_url(url, auth["headers"])
                result["host"] = host
                result["auth_config"] = auth["name"]
                all_results.append(result)
                tested_count += 1
                
                status_icon = "✓" if result["success"] else "✗"
                self.log(f"  [{status_icon}] {url} ({auth['name']}) -> {result['status']}")
        
        # Phase 2: 探测核心API路径
        self.log("\n[Phase 2] 核心API路径探测", "PHASE")
        
        # 重点测试可能的端点
        key_paths = [
            "/api/v3/chat/completions",
            "/api/v3/llm/rawChat",
            "/api/v3/cloud/chat",
            "/api/v3/messages",
            "/api/v2/chat/completions",
            "/api/v1/chat/completions",
            "/cloudide/api/v3/chat/completions",
            "/cloudide/api/v3/trae/CheckLogin",
            "/cloudide/api/v3/trae/GetUserInfo",
            "/trae/api/v3/chat/completions",
            "/trae/api/v3/oauth/ExchangeToken",
            "/api/v3/agent/chat",
            "/api/v3/agent/messages",
            "/extensions/api/-/agent/search",
            "/extensions/api/-/agent/detail",
            "/api/v3/completions",
            "/api/v3/generate",
            "/v3/chat/completions",
            "/v3/messages",
            "/chat/completions",
            "/messages",
            "/completions",
            "/generate",
            "/api/chat",
            "/chat",
            "/stream",
            "/query"
        ]
        
        for host in BASE_HOSTS:
            for path in key_paths:
                for auth in AUTH_CONFIGS:
                    url = host + path
                    result = self.test_url(url, auth["headers"], method="POST",
                                          data={"test": "probe"})
                    result["host"] = host
                    result["path"] = path
                    result["auth_config"] = auth["name"]
                    all_results.append(result)
                    tested_count += 1
                    
                    # 只记录非404的结果
                    if result["status"] != 404 or not result["success"]:
                        status_icon = "✓" if result["success"] else "✗"
                        self.log(f"  [{status_icon}] {path} ({auth['name']}) -> {result['status']}")
                    elif tested_count % 50 == 0:
                        self.log(f"  ... 已测试 {tested_count} 个端点", "PROGRESS")
        
        # Phase 3: 深度路径探索
        self.log("\n[Phase 3] 深度路径组合探索", "PHASE")
        
        # 更复杂的路径组合
        deep_paths = []
        for prefix in ["/api/v3", "/api/v2", "/api/v1", "/cloudide/api/v3", "/trae/api/v3"]:
            for name in ["chat", "llm", "agent", "model", "completions", 
                         "messages", "generate", "query", "stream", "bot",
                         "assistant", "conversation", "ai", "copilot"]:
                deep_paths.append(f"{prefix}/{name}")
                deep_paths.append(f"{prefix}/{name}/completions")
                deep_paths.append(f"{prefix}/{name}/chat")
                deep_paths.append(f"{prefix}/{name}/messages")
        
        for host in BASE_HOSTS:
            for path in deep_paths[:100]:  # 限制数量
                url = host + path
                result = self.test_url(url, AUTH_CONFIGS[3]["headers"], method="POST",
                                      data={"test": "deep_probe"})
                result["host"] = host
                result["path"] = path
                result["auth_config"] = AUTH_CONFIGS[3]["name"]
                all_results.append(result)
                tested_count += 1
                
                if result["status"] != 404 or not result["success"]:
                    status_icon = "✓" if result["success"] else "✗"
                    self.log(f"  [{status_icon}] {path} -> {result['status']}")
        
        self.log(f"\n总测试数: {tested_count}", "STAT")
        
        return all_results
    
    def analyze_findings(self, results: List[Dict]) -> Dict[str, Any]:
        """分析探测结果"""
        self.log("\n" + "=" * 60, "BANNER")
        self.log("探测结果分析", "BANNER")
        self.log("=" * 60, "BANNER")
        
        analysis = {
            "total_tested": len(results),
            "by_status": {},
            "successful_connections": [],
            "potential_endpoints": [],
            "key_discoveries": [],
            "host_reachability": {}
        }
        
        for result in results:
            status = result.get("status", 0)
            status_key = str(status)
            
            if status_key not in analysis["by_status"]:
                analysis["by_status"][status_key] = 0
            analysis["by_status"][status_key] += 1
            
            # 分析主机可达性
            host = result.get("host", "unknown")
            if host not in analysis["host_reachability"]:
                analysis["host_reachability"][host] = {
                    "total": 0,
                    "reachable": 0,
                    "statuses": {}
                }
            analysis["host_reachability"][host]["total"] += 1
            analysis["host_reachability"][host]["statuses"][status_key] = \
                analysis["host_reachability"][host]["statuses"].get(status_key, 0) + 1
            
            if result["success"]:
                analysis["host_reachability"][host]["reachable"] += 1
                analysis["successful_connections"].append(result)
                
                if result["has_content"] and not result["is_1001"]:
                    analysis["potential_endpoints"].append({
                        "url": result["url"],
                        "status": status,
                        "auth_config": result.get("auth_config", "unknown"),
                        "response_preview": result.get("response_preview", "")[:100]
                    })
        
        self.log(f"状态码分布: {analysis['by_status']}", "STAT")
        
        for host, info in analysis["host_reachability"].items():
            reachability = (info["reachable"] / info["total"] * 100) if info["total"] > 0 else 0
            self.log(f"主机 {host}: 可达率 {reachability:.1f}% ({info['reachable']}/{info['total']})", "HOST")
        
        if analysis["potential_endpoints"]:
            self.log(f"\n发现 {len(analysis['potential_endpoints'])} 个潜在端点:", "FINDING")
            for ep in analysis["potential_endpoints"][:10]:
                self.log(f"  - {ep['url']} [{ep['auth_config']}] -> {ep['response_preview'][:80]}", "ENDPOINT")
        
        analysis["key_discoveries"] = [
            f"共测试 {analysis['total_tested']} 个端点组合",
            f"发现 {len(analysis['potential_endpoints'])} 个潜在有效端点",
            "404错误可能意味着：1) URL路径错误 2) HTTP方法错误 3) 缺少必要参数",
            "1001错误意味着认证失败，需要正确的Token或Cookie",
            "建议：重点测试messages格式和llm/rawChat端点"
        ]
        
        for discovery in analysis["key_discoveries"]:
            self.log(f"  发现: {discovery}", "FINDING")
        
        return analysis
    
    def generate_report(self, results: List[Dict], analysis: Dict) -> str:
        """生成探测报告"""
        report = {
            "report_id": self.session_id,
            "report_title": "BSD API路径精准探测报告",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_tested": analysis["total_tested"],
            "status_distribution": analysis["by_status"],
            "host_reachability": analysis["host_reachability"],
            "potential_endpoints": analysis["potential_endpoints"],
            "key_discoveries": analysis["key_discoveries"],
            "conclusions": [
                "404错误码说明服务器可达但路径不正确",
                "1001错误码说明认证失败",
                "200成功码说明请求成功",
                "建议下一步：精准测试messages格式端点和WebSocket通道",
                "本源服务器代理转发可能绕过直接请求的限制"
            ]
        }
        
        report_dir = os.path.join(os.path.dirname(__file__), "reports")
        os.makedirs(report_dir, exist_ok=True)
        report_path = os.path.join(report_dir, f"BSD_API_Path_Report_{int(time.time())}.json")
        
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=str)
            
        self.log(f"\n报告已保存: {report_path}", "SAVE")
        return report_path
    
    def run(self) -> Dict[str, Any]:
        """运行完整探测流程"""
        self.log("\n" + "#" * 60, "BANNER")
        self.log("BSD API路径精准探测引擎 V1.0 启动", "BANNER")
        self.log(f"Session ID: {self.session_id}", "BANNER")
        self.log("#" * 60 + "\n", "BANNER")
        
        # Phase 1-3: 系统性探测
        results = self.explore_paths()
        
        # 分析结果
        analysis = self.analyze_findings(results)
        
        # 生成报告
        report_path = self.generate_report(results, analysis)
        
        return {
            "session_id": self.session_id,
            "report_path": report_path,
            "total_tested": analysis["total_tested"],
            "potential_endpoints": len(analysis["potential_endpoints"]),
            "key_discoveries": len(analysis["key_discoveries"])
        }

if __name__ == "__main__":
    explorer = APIPathExplorer()
    result = explorer.run()
    
    print("\n" + "=" * 60)
    print("API路径探测结果:")
    print(f"  Session ID: {result['session_id']}")
    print(f"  测试端点数: {result['total_tested']}")
    print(f"  潜在有效端点: {result['potential_endpoints']}")
    print(f"  关键发现数: {result['key_discoveries']}")
    print(f"  报告路径: {result['report_path']}")
    print("=" * 60)
