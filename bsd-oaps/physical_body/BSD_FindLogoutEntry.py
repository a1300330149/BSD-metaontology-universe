"""
1. 确认TRAE SOLO CN运行状态
2. 搜索Trae CN退出登录按钮代码
3. 探索屏幕操作能力
"""
import os, json, re, subprocess, time

TRAE_CN_APP = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app'
TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'

# 1. 确认TRAE SOLO CN运行状态
print('=== 1. 确认TRAE SOLO CN状态 ===')
r = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq TRAE SOLO CN*', '/NH'], capture_output=True, text=True)
solo_lines = [l.strip() for l in r.stdout.strip().split('\n') if l.strip()]
print(f'  TRAE SOLO CN: {len(solo_lines)} 个进程 (保持运行)')

# 2. 搜索Trae CN中退出登录按钮
print('\n=== 2. 搜索Trae CN退出登录按钮 ===')

main_js = os.path.join(TRAE_CN_APP, 'out', 'main.js')
with open(main_js, 'r', encoding='utf-8') as f:
    content = f.read()

# 搜索退出登录相关的UI文本和命令
logout_ui_patterns = [
    # 中文按钮文本
    r'退出登录',
    r'退出账号',
    r'注销登录',
    r'登出',
    r'切换账号',
    # 英文按钮文本
    r'Sign\s*Out',
    r'Log\s*Out',
    r'Logout',
    r'Sign\s*Out',
    r'切换用户',
    r'Switch\s*Account',
    # 命令ID
    r'auth\.logout',
    r'auth\.signout',
    r'account\.logout',
    r'user\.logout',
    r'icube\.logout',
    r'icube\.signout',
    # IPC事件
    r'logout.*click',
    r'logout.*button',
    r'logout.*action',
]

for pat in logout_ui_patterns:
    matches = [(m.start(), content[max(0,m.start()-50):m.end()+150]) 
               for m in re.finditer(pat, content, re.IGNORECASE)]
    if matches:
        print(f'\n  [{pat[:40]}] 找到 {len(matches)} 处:')
        for pos, ctx in matches[:3]:
            ctx_clean = ctx.replace('\n', ' ')[:300]
            print(f'    @{pos}: {ctx_clean}')

# 3. 搜索Trae CN命令系统
print('\n=== 3. 搜索命令系统 ===')

# 搜索command注册
cmd_patterns = [
    r'registerCommand.*logout',
    r'registerCommand.*signout',
    r'registerCommand.*account',
    r'commands\.register.*logout',
    r'commands\.register.*signout',
    r'icube.*logout.*command',
    r'command.*icube.*logout',
]

for pat in cmd_patterns:
    matches = [(m.start(), content[max(0,m.start()-50):m.end()+200]) 
               for m in re.finditer(pat, content, re.IGNORECASE)]
    if matches:
        print(f'\n  [{pat[:40]}] 找到 {len(matches)} 处:')
        for pos, ctx in matches[:3]:
            ctx_clean = ctx.replace('\n', ' ')[:400]
            print(f'    @{pos}: {ctx_clean}')

# 4. 搜索设置菜单中的退出登录
print('\n=== 4. 搜索设置菜单 ===')

setting_patterns = [
    r'setting.*account',
    r'account.*setting',
    r'user.*setting.*logout',
    r'profile.*setting',
    r'switch.*account',
    r'account.*switch',
]

for pat in setting_patterns:
    matches = [(m.start(), content[max(0,m.start()-50):m.end()+200]) 
               for m in re.finditer(pat, content, re.IGNORECASE)]
    if matches:
        print(f'\n  [{pat[:40]}] 找到 {len(matches)} 处:')
        for pos, ctx in matches[:3]:
            ctx_clean = ctx.replace('\n', ' ')[:400]
            print(f'    @{pos}: {ctx_clean}')

# 5. 搜索窗口标题和URL导航
print('\n=== 5. 搜索窗口/导航 ===')

window_patterns = [
    r'trae://settings',
    r'trae://account',
    r'trae://logout',
    r'trae://signout',
    r'vscode://settings',
    r'command:.*logout',
    r'command:.*account',
    r'settingsSync.*logout',
]

for pat in window_patterns:
    matches = [(m.start(), content[max(0,m.start()-30):m.end()+100]) 
               for m in re.finditer(pat, content, re.IGNORECASE)]
    if matches:
        print(f'\n  [{pat[:40]}] 找到 {len(matches)} 处:')
        for pos, ctx in matches[:3]:
            ctx_clean = ctx.replace('\n', ' ')[:300]
            print(f'    @{pos}: {ctx_clean}')

# 6. 检查屏幕操作模块
print('\n=== 6. 检查屏幕操作模块 ===')
physical_path = r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body'
if os.path.exists(physical_path):
    for f in os.listdir(physical_path):
        fl = f.lower()
        if any(kw in fl for kw in ['physical', 'screen', 'essence', 'operator', 'bridge']):
            fp = os.path.join(physical_path, f)
            print(f'  {f}: {os.path.getsize(fp):,} bytes')
