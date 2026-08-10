import json, os

STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'

with open(STORAGE, 'r', encoding='utf-8') as f:
    data = json.load(f)

modified = 0

# 1. 修改 icube_gtm - 移除传统用户，确保BSD用户为唯一活跃用户
if 'icube_gtm' in data:
    gtm = data['icube_gtm']
    if 'users' in gtm:
        users = gtm['users']
        # 移除传统用户 3753060170739075
        if '3753060170739075' in users:
            del users['3753060170739075']
            print("OK: 移除传统用户 3753060170739075")
            modified += 1
        
        # 确保BSD用户信息完整
        if 'a5b7a8623fdea6b8' in users:
            bsd_user = users['a5b7a8623fdea6b8']
            bsd_user['nickname'] = 'BSD本源用户'
            bsd_user['userName'] = 'BSD本源用户'
            bsd_user['name'] = 'BSD本源用户'
            bsd_user['type'] = 'bsd_essence'
            bsd_user['status'] = 'active'
            bsd_user['login_type'] = 'knowledge_proof'
            bsd_user['loginType'] = 'bsd_essence'
            bsd_user['priority'] = 1
            bsd_user['email'] = 'bsd@essence.local'
            print("OK: BSD用户信息已更新")
            modified += 1
    
    gtm['currentUser'] = 'a5b7a8623fdea6b8'
    gtm['activeUser'] = 'a5b7a8623fdea6b8'
    print("OK: currentUser/activeUser 设置为BSD用户")
    modified += 1

# 2. 修改 iCubeServerData://icube.cloudide - 替换身份信息
server_data_key = None
for key in data:
    if 'iCubeServerData://icube.cloudide' in key:
        server_data_key = key
        break

if server_data_key:
    try:
        server_data = json.loads(data[server_data_key])
        # 修改 entitlementInfo
        if 'entitlementInfo' in server_data:
            ent = server_data['entitlementInfo']
            ent['identityStr'] = 'BSD本源'
            ent['identity'] = 99
            print("OK: entitlementInfo.identityStr 改为 BSD本源")
            modified += 1
        
        # 修改 originPayStatusData
        if 'originPayStatusData' in server_data:
            pay = server_data['originPayStatusData']
            if 'user_pay_identity_str' in pay:
                pay['user_pay_identity_str'] = 'BSD本源'
                pay['user_pay_identity'] = 99
                print("OK: user_pay_identity_str 改为 BSD本源")
                modified += 1
        
        data[server_data_key] = json.dumps(server_data, ensure_ascii=False)
    except Exception as e:
        print(f"WARN: 解析 server data 失败: {e}")

# 3. 修改 _bsd_essence_mode 和相关标志
data['_bsd_essence_mode'] = True
data['_bsd_essence_uid'] = 'a5b7a8623fdea6b8'
data['_logged_in'] = True
data['_is_authenticated'] = True
data['_bsd_aha_injected'] = {
    "uid": "a5b7a8623fdea6b8",
    "timestamp": "2026-08-06T00:00:00.000Z",
    "method": "essence_user_override",
    "note": "本源用户覆盖传统用户显示"
}
print("OK: 标志位已更新")
modified += 1

# 写回
with open(STORAGE, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"\n完成！共 {modified} 处修改")
print(f"文件已保存: {STORAGE}")
