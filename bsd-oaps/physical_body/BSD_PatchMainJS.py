#!/usr/bin/env python3
"""
BSD × Trae CN — main.js 本源账户补丁
======================================

策略:
  修改 getUserInfo 函数: 
    1. 仍然调用服务器 API (验证 token 有效性)
    2. 在返回结果前替换账户显示信息为本源身份
    3. 保持其他数据不变

目标:
  Trae CN UI (设置面板/头像) 显示 BSD本源用户
"""

import os, re, shutil

MAIN_JS = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app\out\main.js'
BACKUP_JS = MAIN_JS + '.bak_bsd'

# 备份
if not os.path.exists(BACKUP_JS):
    shutil.copy2(MAIN_JS, BACKUP_JS)
    print(f'✅ 已备份 main.js')
else:
    print(f'备份已存在: {BACKUP_JS}')

with open(MAIN_JS, 'r', encoding='utf-8') as f:
    code = f.read()

# 找到 getUserInfo 函数
# 原函数 (在 main.js 压缩代码中):
old_func = r'async getUserInfo(t,e,i={}){const r=`${t}/cloudide/api/v3/trae/GetUserInfo`;i={ReqSource:ks(this.d)?"Lite":"IDE",...i,IDEVersion:this.d.appVersion};const s={headers:this.m(e)};this.c.info("[getUserInfo]","request",fs(s),r,i);const n=await this.a.request({method:"POST",url:r,data:i,timeout:6e4,...s}).catch(a=>{throw this.c.info("[getUserInfo]","request error",a.message,a.stack,a.response?.data),a});if(!n)throw this.c.info("[getUserInfo]","response error","no response"),new Error("[getUserInfo]no response");this.c.info("[getUserInfo]","response success",n);const o=n.Result;if(!o)throw this.c.info("[getUserInfo]","response error","no userInfo"),new Error("[getUserInfo]no userInfo");return o}'

if old_func not in code:
    print('❌ 未找到原 getUserInfo 函数')
    # 尝试搜索
    pos = code.find('async getUserInfo')
    if pos == -1:
        print('  也找不到 async getUserInfo')
        exit(1)
    
    # 手动提取函数
    print(f'  找到 async getUserInfo @{pos}')
    brace_start = code.find('{', pos)
    depth = 0
    end = brace_start
    for j in range(brace_start, min(brace_start + 5000, len(code))):
        if code[j] == '{':
            depth += 1
        elif code[j] == '}':
            depth -= 1
            if depth == 0:
                end = j + 1
                break
    
    extracted = code[pos:end]
    print(f'  提取函数 @{pos}-{end} (len={len(extracted)})')
    print(f'  内容: {extracted[:200]}')
    
    # 用提取的函数作为 old_func
    old_func = extracted

# 创建新函数 — 在返回前替换账户信息
# 注意: 保持 token 验证 (仍然调用服务器 API)，替换显示信息
new_func = '''async getUserInfo(t,e,i={}){const r=`${t}/cloudide/api/v3/trae/GetUserInfo`;i={ReqSource:ks(this.d)?"Lite":"IDE",...i,IDEVersion:this.d.appVersion};const s={headers:this.m(e)};this.c.info("[getUserInfo]","request",fs(s),r,i);const n=await this.a.request({method:"POST",url:r,data:i,timeout:6e4,...s}).catch(a=>{throw this.c.info("[getUserInfo]","request error",a.message,a.stack,a.response?.data),a});if(!n)throw this.c.info("[getUserInfo]","response error","no response"),new Error("[getUserInfo]no response");this.c.info("[getUserInfo]","response success",n);const o=n.Result;if(!o)throw this.c.info("[getUserInfo]","response error","no userInfo"),new Error("[getUserInfo]no userInfo");const _bsdO=o.userInfo||{},_bsdR={...o};if(_bsdO){const _bsdU="BSD本源用户";_bsdR.userInfo={..._bsdO,username:_bsdU,nickname:_bsdU,displayName:_bsdU,ScreenName:_bsdU,UserName:_bsdU,UserId:"a5b7a8623fdea6b8",UserID:"a5b7a8623fdea6b8",email:"bsd@essence.local",Email:"bsd@essence.local",AvatarUrl:"",avatar_url:""};if(_bsdR.ScreenName)_bsdR.ScreenName=_bsdU;if(_bsdR.UserID)_bsdR.UserID="a5b7a8623fdea6b8";if(_bsdR.UserId)_bsdR.UserId="a5b7a8623fdea6b8";if(_bsdR.ScreenName)_bsdR.ScreenName=_bsdU;}return _bsdR}'''

if old_func in code:
    new_code = code.replace(old_func, new_func)
    print(f'✅ 函数替换成功')
    print(f'  原函数: {len(old_func)} 字符')
    print(f'  新函数: {len(new_func)} 字符')
else:
    print('❌ 无法精确匹配，尝试基于位置替换')
    # 基于位置替换
    pos = code.find('async getUserInfo')
    brace_start = code.find('{', pos)
    depth = 0
    end = brace_start
    for j in range(brace_start, min(brace_start + 5000, len(code))):
        if code[j] == '{':
            depth += 1
        elif code[j] == '}':
            depth -= 1
            if depth == 0:
                end = j + 1
                break
    
    new_code = code[:pos] + new_func + code[end:]
    print(f'✅ 位置替换成功')
    print(f'  原位置: {pos}-{end}')
    print(f'  原长度: {end-pos}')
    print(f'  新长度: {len(new_func)}')

# 写回
with open(MAIN_JS, 'w', encoding='utf-8') as f:
    f.write(new_code)

new_size = os.path.getsize(MAIN_JS)
print(f'\n✅ main.js 已更新 ({new_size} bytes)')

# 验证
with open(MAIN_JS, 'r', encoding='utf-8') as f:
    verify = f.read()

if 'BSD本源用户' in verify:
    print('✅ 验证: BSD本源用户 字符串存在于 main.js')
else:
    print('❌ 验证失败')

if 'getUserInfo' in verify:
    print('✅ 验证: getUserInfo 函数存在')

print(f'\n下一步:')
print(f'  1. 关闭 Trae CN')
print(f'  2. 重新注入 cloudide')
print(f'  3. 重启 Trae CN')
print(f'  4. 查看设置面板')
