import json
import sqlite3
import os
import base64

# ============================================================
# 提取 C 盘 Trae CN 客户端的信息
# ============================================================

# 1. 读取 product.json 配置
product_path = r"C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app\product.json"
with open(product_path, 'r', encoding='utf-8') as f:
    product = json.load(f)

print("=" * 60)
print("C盘 Trae CN 关键配置提取:")
print("=" * 60)

# 提取认证端点
boot_config = product.get("bootConfig", {})
account_config = boot_config.get("account", {})
agent_config = boot_config.get("agent", {})
ws_config = boot_config.get("ws", {})

print(f"\n[Account 端点]")
for key, val in account_config.items():
    if isinstance(val, dict):
        for subkey, subval in val.items():
            print(f"  {key}.{subkey}: {subval}")
    else:
        print(f"  {key}: {val}")

print(f"\n[Agent 端点]")
for key, val in agent_config.items():
    print(f"  {key}: {val}")

print(f"\n[WebSocket 端点]")
for key, val in ws_config.items():
    print(f"  {key}: {val}")

# 提取 authConfig
auth_config = product.get("iCubeApp", {}).get("authConfig", {})
print(f"\n[AuthConfig]")
for pkg, envs in auth_config.items():
    if isinstance(envs, dict):
        for env, client_id in envs.items():
            print(f"  {pkg}.{env}: {client_id}")

# 2. 查找 C 盘用户的 Token
print("\n" + "=" * 60)
print("C盘用户 Token 提取:")
print("=" * 60)

c_user_paths = [
    r"C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\state.vscdb",
    r"C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json",
]

for path in c_user_paths:
    if os.path.exists(path):
        print(f"\n查找: {path}")
        try:
            if path.endswith('.vscdb'):
                conn = sqlite3.connect(path)
                cursor = conn.cursor()
                cursor.execute("SELECT key, value FROM ItemTable WHERE key LIKE '%auth%' OR key LIKE '%token%' OR key LIKE '%cloud%' OR key LIKE '%login%'")
                rows = cursor.fetchall()
                for k, v in rows[:10]:
                    print(f"  {k}: {str(v)[:150]}")
                conn.close()
            elif path.endswith('.json'):
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                auth_keys = [k for k in data.keys() if 'auth' in k.lower() or 'token' in k.lower() or 'cloud' in k.lower()]
                for key in auth_keys:
                    print(f"  {key}: {str(data[key])[:150]}...")
        except Exception as e:
            print(f"  Error: {e}")

# 3. 尝试解码加密的 Token
print("\n" + "=" * 60)
print("尝试解码加密 Token:")
print("=" * 60)

storage_path = r"C:\Users\13003\AppData\Roaming\TRAE SOLO CN\User\globalStorage\storage.json"
if os.path.exists(storage_path):
    with open(storage_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 查找加密凭据
    auth_info_keys = [k for k in data.keys() if 'iCubeAuthInfo' in k]
    for key in auth_info_keys:
        encrypted_val = data[key]
        print(f"\nKey: {key}")
        print(f"Value length: {len(encrypted_val)} chars")
        
        # 尝试 base64 解码
        try:
            decoded = base64.b64decode(encrypted_val)
            print(f"Decoded bytes (first 100): {decoded[:100]}")
            
            # 尝试解析为 protobuf 或其他格式
            # 这里只做简单分析
            if decoded[:4] == b'\x08\x05\x10\x00':
                print("  -> 可能是 protobuf 格式!")
                
        except Exception as e:
            print(f"Decode failed: {e}")
