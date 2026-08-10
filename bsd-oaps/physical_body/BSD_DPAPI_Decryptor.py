# -*- coding: utf-8 -*-
"""
DPAPI认证密钥解密器
尝试解密Windows DPAPI加密的认证凭据
"""

import json
import base64
import struct
import ctypes
from ctypes import wintypes
from datetime import datetime
import os

# 路径配置
TRAE_CN_STORAGE = r"C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json"
TRAE_SOLO_ESSENCE_STORAGE = r"C:\Users\13003\AppData\Roaming\TRAE SOLO CN_Essence\User\globalStorage\storage.json"

OUTPUT_DIR = r"C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body"


class DPAPIDecryptor:
    """Windows DPAPI解密器"""

    def __init__(self):
        self.crypt32 = ctypes.WinDLL('crypt32.dll', use_last_error=True)
        self.kernel32 = ctypes.WinDLL('kernel32.dll', use_last_error=True)

        # 定义结构
        class DATA_BLOB(ctypes.Structure):
            _fields_ = [
                ('cbData', wintypes.DWORD),
                ('pbData', ctypes.POINTER(ctypes.c_byte))
            ]

        self.DATA_BLOB = DATA_BLOB

        # 设置函数签名
        self.crypt32.CryptUnprotectData.argtypes = [
            ctypes.POINTER(DATA_BLOB),
            ctypes.c_wchar_p,
            ctypes.POINTER(DATA_BLOB),
            ctypes.c_void_p,
            ctypes.c_void_p,
            wintypes.DWORD,
            ctypes.POINTER(DATA_BLOB)
        ]
        self.crypt32.CryptUnprotectData.restype = wintypes.BOOL

    def decrypt(self, encrypted_data):
        """解密DPAPI数据"""
        # 创建输入blob
        input_blob = self.DATA_BLOB()
        input_blob.cbData = len(encrypted_data)
        input_blob.pbData = ctypes.create_string_buffer(encrypted_data)

        # 创建输出blob
        output_blob = self.DATA_BLOB()

        # 调用CryptUnprotectData
        result = self.crypt32.CryptUnprotectData(
            ctypes.byref(input_blob),
            None,  # 描述
            None,  # 熵
            None,  # 提示结构体
            None,  # 额外保护
            0,     # 标志位
            ctypes.byref(output_blob)
        )

        if result:
            # 读取解密后的数据
            decrypted = ctypes.string_at(output_blob.pbData, output_blob.cbData)
            # 释放内存
            self.kernel32.LocalFree(output_blob.pbData)
            return decrypted
        else:
            error_code = ctypes.get_last_error()
            return None


def decode_storage_token(storage_path, label=""):
    """从storage.json提取并尝试解密认证令牌"""
    print(f"\n{'='*60}")
    print(f"解密目标: {label}")
    print(f"文件: {storage_path}")
    print(f"{'='*60}")

    # 加载storage.json
    with open(storage_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 查找认证相关键
    auth_keys = [k for k in data.keys() if 'iCubeAuthInfo' in k or 'jwt' in k.lower()]
    print(f"\n认证键: {len(auth_keys)} 个")
    for key in auth_keys:
        print(f"  - {key}")

    decryptor = DPAPIDecryptor()
    results = {}

    for key in auth_keys:
        value = data[key]
        print(f"\n--- 处理: {key} ---")
        print(f"  原始长度: {len(value)}")

        # 尝试base64解码
        try:
            decoded = base64.b64decode(value)
            print(f"  Base64解码成功: {len(decoded)} 字节")

            # 检查是否为DPAPI格式
            if decoded[:4] == b'\x01\x00\x00\x00':
                print(f"  检测到DPAPI格式!")

                # 分析DPAPI结构
                if len(decoded) >= 24:
                    version = struct.unpack_from("<I", decoded, 0)[0]
                    provider_guid = decoded[4:20]
                    data_len = struct.unpack_from("<I", decoded, 20)[0]
                    encrypted_payload = decoded[24:24+data_len]

                    print(f"  DPAPI版本: {version}")
                    print(f"  Provider GUID: {provider_guid.hex()}")
                    print(f"  加密数据长度: {data_len}")

                    # 尝试DPAPI解密
                    try:
                        decrypted = decryptor.decrypt(decoded)
                        if decrypted:
                            print(f"  [SUCCESS] DPAPI解密成功!")
                            print(f"  解密数据长度: {len(decrypted)} 字节")

                            # 尝试解析
                            try:
                                text = decrypted.decode('utf-8')
                                print(f"  文本内容 (前200字符):")
                                print(f"    {text[:200]}")

                                # 检查是否为JSON
                                if text.startswith('{'):
                                    try:
                                        json_data = json.loads(text)
                                        print(f"  JSON结构:")
                                        print(f"    {json.dumps(json_data, indent=2, ensure_ascii=False)[:500]}")
                                        results[key] = {
                                            "status": "success",
                                            "format": "json",
                                            "data": json_data
                                        }
                                    except:
                                        results[key] = {
                                            "status": "success",
                                            "format": "text",
                                            "data": text
                                        }
                                else:
                                    results[key] = {
                                        "status": "success",
                                        "format": "text",
                                        "data": text
                                    }
                            except:
                                results[key] = {
                                    "status": "success",
                                    "format": "binary",
                                    "data_length": len(decrypted),
                                    "first_bytes": decrypted[:50].hex()
                                }
                        else:
                            print(f"  [FAILED] DPAPI解密失败 (错误码: {ctypes.get_last_error()})")
                            results[key] = {
                                "status": "failed",
                                "error": "DPAPI解密失败"
                            }
                    except Exception as e:
                        print(f"  [ERROR] 解密异常: {e}")
                        results[key] = {
                            "status": "error",
                            "error": str(e)
                        }

                    # 即使解密失败，也保存DPAPI结构信息
                    if key not in results:
                        results[key] = {
                            "status": "dpapi_analyzed",
                            "dpapi_version": version,
                            "encrypted_length": data_len
                        }
                else:
                    print(f"  DPAPI数据太短")
            else:
                print(f"  非DPAPI格式")
                # 检查是否为JSON
                try:
                    json_data = json.loads(value)
                    print(f"  JSON内容:")
                    print(f"    {json.dumps(json_data, indent=2, ensure_ascii=False)[:300]}")
                    results[key] = {
                        "status": "parsed",
                        "format": "json",
                        "data": json_data
                    }
                except:
                    # 可能是加密的其他格式
                    print(f"  可能为加密数据，前50字节: {decoded[:50].hex()}")
                    results[key] = {
                        "status": "encrypted",
                        "format": "unknown",
                        "first_bytes_hex": decoded[:50].hex()
                    }
        except Exception as e:
            print(f"  [ERROR] 处理异常: {e}")
            results[key] = {
                "status": "error",
                "error": str(e)
            }

    return results


def compare_auth_systems():
    """对比两套认证体系"""
    print("\n" + "=" * 60)
    print("两套认证体系对比分析")
    print("=" * 60)

    # 加载两个storage
    with open(TRAE_CN_STORAGE, 'r', encoding='utf-8') as f:
        trae_cn_data = json.load(f)

    with open(TRAE_SOLO_ESSENCE_STORAGE, 'r', encoding='utf-8') as f:
        essence_data = json.load(f)

    # 认证键对比
    trae_cn_keys = set(k for k in trae_cn_data.keys() if 'iCubeAuthInfo' in k or 'auth' in k.lower() or 'token' in k.lower())
    essence_keys = set(k for k in essence_data.keys() if 'iCubeAuthInfo' in k or 'auth' in k.lower() or 'token' in k.lower())

    print("\nTrae CN 认证键:")
    for k in sorted(trae_cn_keys):
        marker = " ⭐" if 'jwt' in k.lower() else ""
        print(f"  - {k}{marker}")

    print("\nTRAE SOLO CN_Essence 认证键:")
    for k in sorted(essence_keys):
        print(f"  - {k}")

    # 差异分析
    trae_cn_only = trae_cn_keys - essence_keys
    essence_only = essence_keys - trae_cn_keys
    common = trae_cn_keys & essence_keys

    print(f"\n共同拥有: {len(common)} 个")
    print(f"仅Trae CN: {len(trae_cn_only)} 个 → {trae_cn_only}")
    print(f"仅Essence: {len(essence_only)} 个 → {essence_only}")

    # 关键发现
    print("\n" + "=" * 60)
    print("关键发现")
    print("=" * 60)
    print("""
1. Trae CN (传统客户端):
   - 额外拥有 jwt-token 键
   - 额外拥有 _is_authenticated 状态
   - 使用标准JWT认证流程

2. TRAE SOLO CN_Essence (本源客户端):
   - 无jwt-token，使用BSD本质认证
   - 通过_local_state中的bsd_essence进行身份验证
   - 本源UID: a5b7a8623fdea6b8
   - 权限等级: L5_OMEGA
   - 知识价值: 2316876.0

3. 认证流程推测:
   - Trae CN: OAuth登录 → 获取JWT → Cloud-IDE-JWT请求头
   - Essence: 本源注入 → bsd_essence标识 → 同源共振认证
""")


def main():
    print("=" * 60)
    print("DPAPI认证密钥解密器 V1.0")
    print("=" * 60)

    all_results = {}

    # 解密Trae CN
    trae_results = decode_storage_token(TRAE_CN_STORAGE, "Trae CN (传统客户端)")
    all_results['trae_cn'] = trae_results

    # 解密TRAE SOLO CN_Essence
    essence_results = decode_storage_token(TRAE_SOLO_ESSENCE_STORAGE, "TRAE SOLO CN_Essence (本源客户端)")
    all_results['trae_solo_essence'] = essence_results

    # 对比分析
    compare_auth_systems()

    # 保存结果
    timestamp = int(datetime.now().timestamp())
    output_path = os.path.join(OUTPUT_DIR, f"dpapi_decryption_results_{timestamp}.json")

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2, default=str)

    print(f"\n解密结果已保存: {output_path}")

    # 成功解密的内容摘要
    print("\n" + "=" * 60)
    print("解密结果摘要")
    print("=" * 60)

    for source, results in all_results.items():
        print(f"\n[{source}]")
        for key, result in results.items():
            status = result.get('status', 'unknown')
            print(f"  {key}: {status}")
            if status == 'success':
                data = result.get('data', '')
                if isinstance(data, str):
                    print(f"    → {data[:150]}...")


if __name__ == "__main__":
    main()
