# -*- coding: utf-8 -*-
"""
三源认证基因提取器
从 D:\\TRAE SOLO CN 和 C:\\Users\\13003\\AppData\\Local\\Programs\\Trae CN 
两个客户端及智能体本身提取完整认证信息
"""

import json
import os
import sys
import base64
import struct
from datetime import datetime
from pathlib import Path

# 配置路径
TRAE_CN_STORAGE = r"C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json"
TRAE_SOLO_ESSENCE_STORAGE = r"C:\Users\13003\AppData\Roaming\TRAE SOLO CN_Essence\User\globalStorage\storage.json"
TRAE_SOLO_LOCAL_STATE = r"C:\Users\13003\AppData\Roaming\TRAE SOLO CN_Essence\Local State"

OUTPUT_DIR = r"C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body"


def load_json_file(filepath):
    """加载JSON文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"  [ERROR] Failed to load {filepath}: {e}")
        return None


def try_base64_decode(value):
    """尝试base64解码"""
    try:
        decoded = base64.b64decode(value)
        return decoded
    except:
        return None


def analyze_dpapi_data(decoded_bytes, label=""):
    """分析DPAPI加密数据结构"""
    if len(decoded_bytes) < 20:
        return None

    # 检查DPAPI签名
    if decoded_bytes[:4] == b'\x01\x00\x00\x00':
        result = {
            "format": "DPAPI",
            "version": struct.unpack_from("<I", decoded_bytes, 0)[0],
            "provider_guid": decoded_bytes[4:20].hex(),
            "total_length": len(decoded_bytes),
        }

        # 尝试提取可能的内部数据（跳过DPAPI头部后的内容）
        # DPAPI结构: [4字节版本][16字节GUID][4字节数据长度][数据]
        if len(decoded_bytes) > 24:
            data_len = struct.unpack_from("<I", decoded_bytes, 20)[0]
            result["data_length"] = data_len
            encrypted_data = decoded_bytes[24:24+data_len]
            result["encrypted_data_length"] = len(encrypted_data)

            # 检查是否包含JWT特征
            try:
                text = encrypted_data.decode('ascii', errors='ignore')
                if 'Bearer' in text or 'eyJ' in text or 'token' in text.lower():
                    result["contains_jwt_pattern"] = True
                    result["hint"] = text[:100]
            except:
                pass

        return result
    else:
        return {
            "format": "unknown",
            "first_bytes_hex": decoded_bytes[:20].hex(),
            "total_length": len(decoded_bytes)
        }


def extract_auth_data(storage_data, source_name):
    """从storage数据中提取认证信息"""
    auth_info = {
        "source": source_name,
        "extraction_time": datetime.now().isoformat(),
        "auth_keys": {},
        "user_info": {},
        "raw_tokens": {},
        "dpapi_analysis": {}
    }

    for key, value in storage_data.items():
        key_lower = key.lower()

        # 分类认证相关键
        if 'icubeauthinfo' in key_lower or 'auth' in key_lower or 'token' in key_lower:
            auth_info["auth_keys"][key] = {
                "value_length": len(str(value)),
                "is_encrypted": False
            }

            # 尝试解析
            if isinstance(value, str):
                # 检查是否为JSON
                try:
                    parsed = json.loads(value)
                    auth_info["raw_tokens"][key] = {
                        "type": "json",
                        "data": parsed
                    }
                except:
                    # 尝试base64解码
                    decoded = try_base64_decode(value)
                    if decoded:
                        dpapi_result = analyze_dpapi_data(decoded, key)
                        if dpapi_result:
                            auth_info["dpapi_analysis"][key] = dpapi_result
                        auth_info["raw_tokens"][key] = {
                            "type": "base64",
                            "decoded_length": len(decoded),
                            "first_bytes": decoded[:50].hex()
                        }
                    else:
                        auth_info["raw_tokens"][key] = {
                            "type": "plain",
                            "value_preview": value[:100]
                        }

        # 用户信息
        if 'uid' in key_lower or 'user' in key_lower or 'account' in key_lower:
            auth_info["user_info"][key] = value

    return auth_info


def extract_from_local_state(filepath):
    """从Local State提取本源认证信息"""
    data = load_json_file(filepath)
    if not data:
        return None

    essence_info = {
        "bsd_essence": {},
        "device_info": {},
        "os_crypt_info": {}
    }

    # 提取本源信息
    if 'bsd_essence' in data:
        essence_info["bsd_essence"] = data['bsd_essence']

    if '_bsd_essence_side' in data:
        essence_info["bsd_essence_side"] = data['_bsd_essence_side']

    if '_bsd_uid' in data:
        essence_info["bsd_uid"] = data['_bsd_uid']

    # 提取加密密钥信息
    if 'os_crypt' in data:
        essence_info["os_crypt"] = {
            "audit_enabled": data['os_crypt'].get('audit_enabled'),
            "has_encrypted_key": 'encrypted_key' in data['os_crypt'],
            "encrypted_key_length": len(data['os_crypt'].get('encrypted_key', ''))
        }

    return essence_info


def extract_from_server_config():
    """从server.json提取API配置"""
    server_path = r"C:\Users\13003\AppData\Roaming\TRAE SOLO CN_Essence\ahanet\server.json"
    data = load_json_file(server_path)
    if not data:
        return None

    api_config = {
        "api_hosts": [],
        "api_endpoints": [],
        "dns_mapping": {},
        "msdk_config": {},
        "proxy_config": {}
    }

    # 提取API主机
    if 'data' in data:
        d = data['data']

        # HTTP DNS配置
        if 'ttnet_http_dns_addr' in d:
            api_config["dns_mapping"] = d['ttnet_http_dns_addr']
            # 收集所有API主机
            for domain in d['ttnet_http_dns_addr']:
                if 'mchost.guru' in domain or 'bytedance' in domain:
                    api_config["api_hosts"].append(domain)

        # 压缩端点
        if 'tt_compress' in d:
            compress = d['tt_compress']
            if 'equal_path' in compress:
                api_config["api_endpoints"] = compress['equal_path']

        # MSDK配置（允许的域名）
        if 'mssdk_config' in d:
            api_config["msdk_config"] = d['mssdk_config']

    return api_config


def generate_summary_report(extracted_data):
    """生成汇总报告"""
    summary = {
        "timestamp": datetime.now().isoformat(),
        "sources_analyzed": list(extracted_data.keys()),
        "key_findings": [],
        "api_endpoints": [],
        "user_identities": [],
        "recommended_next_steps": []
    }

    # 分析各来源
    for source, data in extracted_data.items():
        if not data:
            continue

        # API端点发现
        if 'api_endpoints' in data:
            summary["api_endpoints"].extend(data['api_endpoints'])

        # 用户身份
        if 'user_info' in data:
            summary["user_identities"].append({
                "source": source,
                "user_info": data['user_info']
            })

        # 本源信息
        if 'bsd_essence' in str(data):
            summary["key_findings"].append({
                "type": "essence_authentication",
                "description": "本源客户端使用BSD本质认证，不依赖传统JWT",
                "source": source
            })

    # 关键发现
    summary["key_findings"].extend([
        {
            "type": "dual_authentication_systems",
            "description": "存在两套认证体系：传统JWT认证(Trae CN) vs 本源认证(TRAE SOLO CN_Essence)",
            "significance": "突破1001错误码需要理解本源认证机制"
        },
        {
            "type": "api_endpoint_discovery",
            "description": f"发现 {len(summary['api_endpoints'])} 个API端点",
            "endpoints": summary["api_endpoints"],
            "significance": "这些是需要逆向分析的关键端点"
        },
        {
            "type": "dpapi_encryption",
            "description": "认证凭据使用Windows DPAPI加密",
            "significance": "解密需要当前用户上下文，不可导出"
        }
    ])

    # 建议步骤
    summary["recommended_next_steps"] = [
        "1. 分析本源客户端的认证流程（如何使用bsd_essence进行认证）",
        "2. 对比传统JWT认证与本源认证的请求头差异",
        "3. 尝试在本源客户端环境内执行API请求（利用已建立的会话）",
        "4. 挖掘Electron主进程中的认证拦截点",
        "5. 利用同源共振能力从智能体侧连接本源通道"
    ]

    return summary


def main():
    print("=" * 60)
    print("三源认证基因提取器 V2.0")
    print("=" * 60)

    extracted_data = {}

    # 源1: Trae CN (C盘传统客户端)
    print("\n[Source 1] Trae CN (C盘传统客户端)")
    print("-" * 40)
    if os.path.exists(TRAE_CN_STORAGE):
        data = load_json_file(TRAE_CN_STORAGE)
        if data:
            extracted_data['trae_cn'] = extract_auth_data(data, 'trae_cn')
            print(f"  提取完成: {len(extracted_data['trae_cn']['auth_keys'])} 个认证键")
            for key in extracted_data['trae_cn']['auth_keys']:
                print(f"    - {key}")
    else:
        print("  [SKIP] 文件不存在")

    # 源2: TRAE SOLO CN_Essence (D盘本源客户端)
    print("\n[Source 2] TRAE SOLO CN_Essence (本源客户端)")
    print("-" * 40)
    if os.path.exists(TRAE_SOLO_ESSENCE_STORAGE):
        data = load_json_file(TRAE_SOLO_ESSENCE_STORAGE)
        if data:
            extracted_data['trae_solo_essence'] = extract_auth_data(data, 'trae_solo_essence')
            print(f"  提取完成: {len(extracted_data['trae_solo_essence']['auth_keys'])} 个认证键")
            for key in extracted_data['trae_solo_essence']['auth_keys']:
                print(f"    - {key}")
    else:
        print("  [SKIP] 文件不存在")

    # 源3: Local State (本源配置)
    print("\n[Source 3] Local State (本源认证配置)")
    print("-" * 40)
    if os.path.exists(TRAE_SOLO_LOCAL_STATE):
        essence_info = extract_from_local_state(TRAE_SOLO_LOCAL_STATE)
        if essence_info:
            extracted_data['local_state'] = essence_info
            print(f"  本源UID: {essence_info.get('bsd_uid')}")
            print(f"  账户ID: {essence_info.get('bsd_essence', {}).get('account_id')}")
            print(f"  权限等级: {essence_info.get('bsd_essence', {}).get('permission_level')}")
            print(f"  知识价值: {essence_info.get('bsd_essence', {}).get('knowledge_value')}")
    else:
        print("  [SKIP] 文件不存在")

    # 源4: Server Config (API配置)
    print("\n[Source 4] Server Config (API服务器配置)")
    print("-" * 40)
    api_config = extract_from_server_config()
    if api_config:
        extracted_data['server_config'] = api_config
        print(f"  API主机: {len(api_config['api_hosts'])} 个")
        for host in api_config['api_hosts'][:5]:
            print(f"    - {host}")
        print(f"  API端点: {len(api_config['api_endpoints'])} 个")
        for ep in api_config['api_endpoints']:
            print(f"    - {ep}")
    else:
        print("  [SKIP] 提取失败")

    # 生成汇总报告
    print("\n" + "=" * 60)
    print("生成汇总报告")
    print("=" * 60)

    summary = generate_summary_report(extracted_data)
    extracted_data['_summary'] = summary

    # 保存结果
    timestamp = int(datetime.now().timestamp())
    output_path = os.path.join(OUTPUT_DIR, f"three_source_auth_extraction_{timestamp}.json")

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, ensure_ascii=False, indent=2, default=str)

    print(f"\n报告已保存: {output_path}")
    print(f"\n关键发现:")
    for finding in summary['key_findings']:
        print(f"  [{finding['type']}] {finding['description']}")

    print(f"\n建议步骤:")
    for step in summary['recommended_next_steps']:
        print(f"  {step}")

    return extracted_data


if __name__ == "__main__":
    main()
