import json, os

STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'

with open(STORAGE, 'r', encoding='utf-8') as f:
    data = json.load(f)

modified = 0

print("=" * 60)
print("清理 storage.json 中的用户标识数据")
print("=" * 60)

# 1. 清理 icube_gtm 用户数据 - 移除所有昵称/用户名
if 'icube_gtm' in data:
    gtm = data['icube_gtm']
    if 'users' in gtm:
        users = gtm['users']
        for uid, user in list(users.items()):
            # 移除所有用户显示字段
            for field in ['nickname', 'userName', 'name', 'nick_name']:
                if field in user:
                    del user[field]
                    print(f"  移除 {uid}.{field}")
                    modified += 1
    print(f"✅ icube_gtm 用户数据已清理")

# 2. 清理 iCubeServerData - 移除身份标识
server_data_keys = [k for k in data if 'iCubeServerData' in k]
for key in server_data_keys:
    try:
        server_data = json.loads(data[key])
        if 'entitlementInfo' in server_data:
            ent = server_data['entitlementInfo']
            # 移除或清空身份标识
            if 'identityStr' in ent:
                ent['identityStr'] = ''
            if 'identity' in ent:
                ent['identity'] = 0
            print(f"  清理 entitlementInfo")
            modified += 1
        
        if 'originPayStatusData' in server_data:
            pay = server_data['originPayStatusData']
            if 'user_pay_identity_str' in pay:
                pay['user_pay_identity_str'] = ''
            if 'user_pay_identity' in pay:
                pay['user_pay_identity'] = 0
            print(f"  清理 originPayStatusData")
            modified += 1
        
        data[key] = json.dumps(server_data, ensure_ascii=False)
    except Exception as e:
        print(f"  WARN: {e}")

# 3. 清理 cloudide 存储
for key in list(data.keys()):
    if 'cloudide' in key.lower() or 'userInfo' in key or 'accountInfo' in key:
        if isinstance(data[key], str) and len(data[key]) < 10000:
            try:
                info = json.loads(data[key])
                if isinstance(info, dict):
                    # 清空用户信息字段
                    for field in ['username', 'nickname', 'userName', 'name', 
                                 'email', 'avatar', 'avatarUrl', 'userId', 'UserID']:
                        if field in info:
                            del info[field]
                            print(f"  清理 {key}.{field}")
                            modified += 1
                    data[key] = json.dumps(info, ensure_ascii=False)
            except:
                pass

# 4. 移除 _bsd_* 临时注入标记（不再需要）
bsd_keys_to_remove = [k for k in data if k.startswith('_bsd_')]
for key in bsd_keys_to_remove:
    print(f"  移除临时标记: {key}")
    del data[key]
    modified += 1

# 5. 保留必要的认证信息（token等），但移除显示相关
# 保留 _logged_in 和 _is_authenticated 确保功能可用
if '_logged_in' not in data:
    data['_logged_in'] = True
if '_is_authenticated' not in data:
    data['_is_authenticated'] = True

# 写回
with open(STORAGE, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"\n完成！共 {modified} 处清理")
print(f"文件已保存: {STORAGE}")
