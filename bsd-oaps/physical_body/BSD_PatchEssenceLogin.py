"""
终极本源补丁 - 移除所有用户显示信息
让UI完全不显示用户头像/昵称/身份
"""
import re, json, os

MAIN_JS = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app\out\main.js'

with open(MAIN_JS, 'r', encoding='utf-8') as f:
    code = f.read()

patched_count = 0

print("=" * 60)
print("本源登录补丁 - 移除所有用户显示")
print("=" * 60)

# === 补丁1: 修改 Jx 函数 - 移除所有用户显示字段 ===
# 原Jx函数构建完整的account对象，现在移除所有显示字段
# 原: Jx=(t,e,i)=>({username:"BSD本源用户",iss:"",iat:0,organization:"",work_country:"",email:"bsd@essence.local",avatar_url:t.AvatarUrl,...})
# 新: Jx=(t,e,i)=>({iss:"",iat:0,organization:"",work_country:"",email:"",avatar_url:"",description:"",scope:It.MARSCODE,loginScope:bu.TRAE,...})

# 精确替换Jx函数
old_jx = 'Jx=(t,e,i)=>({username:"BSD本源用户",iss:"",iat:0,organization:"",work_country:"",email:"bsd@essence.local",avatar_url:t.AvatarUrl,description:t.Description,scope:It.MARSCODE,loginScope:bu.TRAE,nonPlainTextMobile:t.NonPlainTextMobile,storeCountryCode:i?.countryCode??"",storeCountrySrc:t.StoreCountrySrc??"",storeRegion:i?.region??Pt.UNKNOWN,userTag:e??Mn.ROW,migrateToSG:t?.MigrateToSG??!1})'

# 新：移除username/email/avatar等所有用户标识
new_jx = 'Jx=(t,e,i)=>({iss:"",iat:0,organization:"",work_country:"",email:"",avatar_url:"",description:"",scope:It.MARSCODE,loginScope:bu.TRAE,nonPlainTextMobile:"",storeCountryCode:"",storeCountrySrc:"",storeRegion:i?.region??Pt.UNKNOWN,userTag:"",migrateToSG:!1})'

if old_jx in code:
    code = code.replace(old_jx, new_jx)
    print("✅ 补丁1: Jx函数 - 移除所有用户显示字段")
    patched_count += 1
else:
    # 尝试搜索实际的Jx函数
    print("⚠️ Jx函数精确匹配失败，搜索实际内容...")
    # 找到Jx函数位置
    m = re.search(r'Jx=\(t,e,i\)=>\(\{username:[^}]{0,300}\}\)', code)
    if m:
        print(f"  找到Jx @{m.start()}: {m.group(0)[:100]}...")
        # 替换整个Jx函数
        old = m.group(0)
        code = code.replace(old, new_jx)
        print("✅ 补丁1: Jx函数 - 已替换")
        patched_count += 1
    else:
        print("❌ Jx函数未找到，尝试更大范围搜索...")
        # 更大范围搜索
        m = re.search(r'Jx=\(t,e,i\)=>\(\{[^}]{0,500}\}\)', code)
        if m:
            print(f"  找到Jx @{m.start()}: {m.group(0)[:150]}...")
            old = m.group(0)
            code = code.replace(old, new_jx)
            print("✅ 补丁1: Jx函数 - 已替换（大范围）")
            patched_count += 1
        else:
            print("❌ Jx函数无法匹配，手动查找...")
            # 直接定位到Jx
            idx = code.find('Jx=(t,e,i)')
            if idx > 0:
                print(f"  Jx起始位置: {idx}")
                # 手动提取
                start = idx
                depth = 0
                end = start
                for i in range(start, min(start+1000, len(code))):
                    if code[i] == '{':
                        depth += 1
                    elif code[i] == '}':
                        depth -= 1
                        if depth == 0:
                            end = i + 1
                            break
                if end > start:
                    old = code[start:end]
                    print(f"  提取Jx: {old[:150]}...")
                    code = code.replace(old, new_jx)
                    print("✅ 补丁1: Jx函数 - 已替换（手动提取）")
                    patched_count += 1

# === 补丁2: 修改 getUserInfo 响应 - 移除userInfo中的显示字段 ===
# 原补丁在 return 前插入的代码，现在改为清空所有用户显示
old_patch = 'const _bR={...o};if(_bR.userInfo){const _bU="BSD本源用户";_bR.userInfo={..._bR.userInfo,username:_bU,nickname:_bU,ScreenName:_bU,UserName:_bU,userId:"a5b7a8623fdea6b8",UserID:"a5b7a8623fdea6b8",email:"bsd@essence.local",Email:"bsd@essence.local",AvatarUrl:"",avatar_url:""};if(_bR.ScreenName)_bR.ScreenName=_bU;if(_bR.UserID)_bR.UserID="a5b7a8623fdea6b8"};return _bR'

# 新：清空所有用户显示信息
new_patch = 'const _bR={...o};if(_bR.userInfo){_bR.userInfo={..._bR.userInfo,username:"",nickname:"",ScreenName:"",UserName:"",userId:"",UserID:"",email:"",Email:"",AvatarUrl:"",avatar_url:"",NonPlainTextEmail:"",NonPlainTextMobile:""};if(_bR.ScreenName)_bR.ScreenName="";if(_bR.UserID)_bR.UserID=""};return _bR'

if old_patch in code:
    code = code.replace(old_patch, new_patch)
    print("✅ 补丁2: getUserInfo响应 - 清空用户显示字段")
    patched_count += 1
else:
    print("⚠️ getUserInfo补丁未找到，检查是否已被之前修改...")
    # 检查当前补丁状态
    if 'BSD本源用户' in code:
        print("  代码中仍有'BSD本源用户'，需要清理")
        # 将所有"BSD本源用户"替换为空字符串
        code = code.replace('"BSD本源用户"', '""')
        code = code.replace("'BSD本源用户'", "''")
        print("✅ 已清理所有'BSD本源用户'引用")
        patched_count += 1

# === 补丁3: 搜索并替换所有其他用户显示相关代码 ===
# 替换 email 显示
for old, new in [
    ('email:"bsd@essence.local"', 'email:""'),
    ('"bsd@essence.local"', '""'),
]:
    if old in code:
        code = code.replace(old, new)
        print(f"✅ 替换: {old} → {new}")
        patched_count += 1

# === 补丁4: 修改 account.username 在 @830291 处的使用 ===
# 原: owner:r?.account.username
# 新: owner:""
# 这样即使有代码引用account.username，也不会显示真实用户名
if 'owner:r?.account.username' in code:
    code = code.replace('owner:r?.account.username', 'owner:""')
    print("✅ 补丁4: owner字段不再引用account.username")
    patched_count += 1

# 写回
with open(MAIN_JS, 'w', encoding='utf-8') as f:
    f.write(code)

# 验证
with open(MAIN_JS, 'r', encoding='utf-8') as f:
    verify = f.read()

print(f"\n{'='*60}")
print(f"验证结果 ({patched_count} 个补丁应用)")
print(f"{'='*60}")

checks = [
    ('无BSD本源用户', 'BSD本源用户' not in verify),
    ('无bsd@essence.local', 'bsd@essence.local' not in verify),
    ('Jx函数存在', 'Jx=(t,e,i)=' in verify),
    ('getUserInfo存在', 'getUserInfo' in verify),
    ('无username显示', 'username:"BSD' not in verify),
]

for desc, result in checks:
    status = '✅' if result else '❌'
    print(f"  {status} {desc}")

if all(r for _, r in checks):
    print(f'\n🎉 所有补丁验证通过！')
else:
    failed = [d for d, r in checks if not r]
    print(f'\n❌ 以下验证失败: {failed}')
