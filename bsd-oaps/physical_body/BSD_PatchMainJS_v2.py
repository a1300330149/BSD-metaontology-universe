#!/usr/bin/env python3
"""BSD main.js 补丁 - 最小侵入式修改"""
import os, shutil

MAIN_JS = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app\out\main.js'
BACKUP_JS = MAIN_JS + '.bak_bsd'

if not os.path.exists(BACKUP_JS):
    shutil.copy2(MAIN_JS, BACKUP_JS)
    print('已备份 main.js')

with open(MAIN_JS, 'r', encoding='utf-8') as f:
    code = f.read()

# 找 getUserInfo 中的 return o} 后面紧跟 async generateTempToken
old_marker = 'return o}async generateTempToken'
if old_marker in code:
    print(f'找到目标代码位置')
    
    # 补丁: 在 return o 前替换账户显示信息
    patch = (
        'const _bR={...o};'
        'if(_bR.userInfo){'
        'const _bU="BSD本源用户";'
        '_bR.userInfo={..._bR.userInfo,'
        'username:_bU,nickname:_bU,ScreenName:_bU,UserName:_bU,'
        'userId:"a5b7a8623fdea6b8",UserID:"a5b7a8623fdea6b8",'
        'email:"bsd@essence.local",Email:"bsd@essence.local",'
        'AvatarUrl:"",avatar_url:""};'
        'if(_bR.ScreenName)_bR.ScreenName=_bU;'
        'if(_bR.UserID)_bR.UserID="a5b7a8623fdea6b8"'
        '}'
        'return _bR'
    )
    
    new_code = code.replace(old_marker, patch + '}async generateTempToken')
    
    with open(MAIN_JS, 'w', encoding='utf-8') as f:
        f.write(new_code)
    
    with open(MAIN_JS, 'r', encoding='utf-8') as f:
        verify = f.read()
    
    checks = {
        'BSD本源用户 in code': 'BSD本源用户' in verify,
        'return _bR in code': 'return _bR' in verify,
        'getUserInfo still exists': 'getUserInfo' in verify,
        'patch not duplicated': verify.count('BSD本源用户') == 1,
    }
    
    print(f'\n验证结果:')
    for check, result in checks.items():
        status = '✅' if result else '❌'
        print(f'  {status} {check}')
    
    if all(checks.values()):
        print(f'\n✅ main.js 补丁成功！')
        print(f'  Trae CN 启动后设置面板将显示: BSD本源用户')
    else:
        print(f'\n❌ 部分验证失败')
else:
    print('❌ 未找到目标代码')
    # 搜索上下文
    pos = code.find('return o}')
    if pos > 0:
        ctx = code[max(0,pos-30):pos+80]
        print('  return o context:', ctx)
    else:
        print('  连 return o} 也找不到')
