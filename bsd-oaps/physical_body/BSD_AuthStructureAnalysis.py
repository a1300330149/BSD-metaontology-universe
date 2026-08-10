"""
分析传统UID的iCubeAuthInfo完整字段结构
理解加密凭证的真实形态
"""
import os, json, base64

TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'

storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
with open(storage_path, 'r', encoding='utf-8') as f:
    storage = json.load(f)

auth_keys = [k for k in storage.keys() if 'iCubeAuthInfo' in k]
print(f"共有 {len(auth_keys)} 个 iCubeAuthInfo 键\n")

for key in auth_keys:
    print(f"=== {key} ===")
    val = storage[key]
    if isinstance(val, str):
        print(f"  类型: str, 长度={len(val)}")
        print(f"  前200字符: {val[:200]}")
        # 尝试base64解码
        try:
            decoded = base64.b64decode(val)
            print(f"  base64解码后(bytes): {len(decoded)} bytes")
            print(f"  前80字节(hex): {decoded[:40].hex()}")
            # 尝试UTF-8
            try:
                txt = decoded.decode('utf-8')
                print(f"  UTF-8解码: {txt[:300]}")
            except:
                print(f"  不是UTF-8 (可能是DPAPI加密)")
                # 尝试JSON
                try:
                    obj = json.loads(decoded)
                    print(f"  JSON对象: {json.dumps(obj, ensure_ascii=False)[:500]}")
                except:
                    pass
        except Exception as e:
            print(f"  base64失败: {e}")
            # 可能就是明文JSON
            try:
                obj = json.loads(val)
                print(f"  明文JSON: {json.dumps(obj, ensure_ascii=False)[:500]}")
            except:
                pass
    elif isinstance(val, dict):
        print(f"  类型: dict, 键={list(val.keys())}")
        for k in val:
            v = val[k]
            if isinstance(v, str) and len(v) > 100:
                print(f"    {k}: {v[:150]}...")
            else:
                print(f"    {k}: {v}")
    else:
        print(f"  类型: {type(val).__name__}, 值: {str(val)[:300]}")
    print()

# 分析 argv.json
argv_path = os.path.join(TRAE_CONFIG, 'argv.json')
if os.path.exists(argv_path):
    with open(argv_path, 'r', encoding='utf-8') as f:
        argv_raw = f.read()
    print("\n=== .trae-cn/argv.json ===")
    print(argv_raw[:800])

# 分析 Local State
local_state_path = os.path.join(TRAE_CN_DATA, 'Local State')
if os.path.exists(local_state_path):
    with open(local_state_path, 'r', encoding='utf-8') as f:
        ls = json.load(f)
    print("\n=== Local State ===")
    print(json.dumps({k: v for k, v in ls.items() if k != 'os_crypt'}, ensure_ascii=False, indent=2)[:500])
    if 'os_crypt' in ls:
        encrypted_key = ls['os_crypt'].get('encrypted_key', '')
        print(f"  os_crypt.encrypted_key: {len(encrypted_key)} chars")
        print(f"  前100字符: {encrypted_key[:100]}")
        # 解码
        try:
            raw = base64.b64decode(encrypted_key)
            print(f"  base64解码后: {len(raw)} bytes")
            print(f"  前20字节(hex): {raw[:20].hex()}")
            # 检查是否以 DPAPI 签名开头
            prefix = raw[:5]
            print(f"  前5字节: {prefix}")
            if raw.startswith(b'DPAPI'):
                print("  以DPAPI签名开头 → Windows DPAPI加密")
            elif raw.startswith(b'v10') or raw.startswith(b'v11'):
                print("  以v10/v11开头 → 可能是Chrome DPAPI加密版本")
        except Exception as e:
            print(f"  解码失败: {e}")
