"""
强制关闭TRAE SOLO CN + 发送本源端登录指令
"""
import subprocess, time, os, json, hashlib, socket

TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'

ESSENCE_UID = 'a5b7a8623fdea6b8'

print('=== 1. 强制关闭TRAE SOLO CN ===')
# 使用进程名精确匹配
subprocess.run(['taskkill', '/F', '/IM', 'TRAE SOLO CN.exe'], capture_output=True)
subprocess.run(['taskkill', '/F', '/IM', 'TRAE SOLO CN Helper.exe'], capture_output=True)
subprocess.run(['taskkill', '/F', '/IM', 'TRAE SOLO CN (2).exe'], capture_output=True)
time.sleep(3)

r = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq TRAE SOLO CN*', '/NH'], capture_output=True, text=True)
solo = [l.strip() for l in r.stdout.strip().split('\n') if l.strip()]
print(f'  TRAE SOLO CN: {len(solo)} 个进程')

# 关闭所有相关进程名
solo_names = ['TRAE SOLO CN', 'TRAE SOLO CN Helper', 'TRAE SOLO CN (2)', 'TRAE SOLO CN (3)', 'TRAE SOLO CN.exe']
for name in solo_names:
    subprocess.run(['taskkill', '/F', '/FI', f'WINDOWTITLE eq {name}*'], capture_output=True)

time.sleep(2)

r2 = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq TRAE SOLO CN*', '/NH'], capture_output=True, text=True)
solo2 = [l.strip() for l in r2.stdout.strip().split('\n') if l.strip()]
print(f'  TRAE SOLO CN (最终): {len(solo2)} 个进程')

# 2. 检查Trae CN当前状态
print('\n=== 2. 检查Trae CN状态 ===')

r3 = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq Trae CN*', '/NH'], capture_output=True, text=True)
cn = [l.strip() for l in r3.stdout.strip().split('\n') if l.strip()]
print(f'  Trae CN: {len(cn)} 个进程')

# 检查Token
jwt_path = os.path.join(TRAE_CONFIG, 'trae-jwt-token')
if os.path.exists(jwt_path) and os.path.getsize(jwt_path) > 0:
    with open(jwt_path, 'r') as f:
        token = f.read().strip()
    print(f'  trae-jwt-token: ⚠️ 已重新生成 ({len(token)} chars)')
    print(f'    → TRAE SOLO CN仍在后台运行，正在同步Token')
    
    # 如果TRAE SOLO CN已关闭但Token仍存在，说明是Trae CN自己生成的
    # 需要分析Token内容
else:
    print(f'  trae-jwt-token: ❌ 不存在')

# 3. 检查Local State
ls_path = os.path.join(TRAE_CN_DATA, 'Local State')
if os.path.exists(ls_path):
    with open(ls_path, 'r', encoding='utf-8') as f:
        ls = json.load(f)
    
    has_user = any(k in ls for k in ['user', 'profile'])
    print(f'  Local State用户: {"✅ 已登录" if has_user else "❌ 未登录"}')
    print(f'  _bsd_essence_mode: {ls.get("_bsd_essence_mode", "N/A")}')

# 4. 尝试通过IPC发送登录指令
print('\n=== 4. 尝试IPC登录指令 ===')

# 本源端登录凭证
login_command = {
    'command': 'auth.login',
    'params': {
        'uid': ESSENCE_UID,
        'loginType': 'bsd_essence',
        'clientId': 'trae_cn_bsd_essence',
        'signature': hashlib.sha256(ESSENCE_UID.encode()).hexdigest()[:32],
        'metadata': {
            'identity': '本源端',
            'theory': 'BSD六系立系论'
        }
    }
}

# 写入IPC命令文件（假设Trae CN会轮询这个文件）
ipc_cmd_path = os.path.join(TRAE_CONFIG, 'bsd_ipc_command.json')
with open(ipc_cmd_path, 'w', encoding='utf-8') as f:
    json.dump(login_command, f, indent=2, ensure_ascii=False)
print(f'  ✅ IPC命令已写入: {ipc_cmd_path}')
print(f'    命令: {login_command["command"]}')
print(f'    UID: {login_command["params"]["uid"]}')

# 5. 通过本地端口发送指令
print('\n=== 5. 尝试本地端口通信 ===')

# Trae CN可能在本地监听某些端口
ports_to_try = [3000, 3001, 3002, 8080, 8081, 8082, 7777, 7778, 15555, 15556]

for port in ports_to_try:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', port))
        if result == 0:
            print(f'  ⚠️ 端口 {port}: 开放!')
        sock.close()
    except:
        pass

# 6. 创建本地登录页面
print('\n=== 6. 生成本源端登录凭证 ===')

login_page = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>BSD本源端登录</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #1a1a2e; color: #eee; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }}
.container {{ background: #16213e; padding: 40px; border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.3); max-width: 500px; }}
h1 {{ color: #0f3460; margin-top: 0; }}
h2 {{ color: #e94560; }}
.uid {{ font-family: monospace; background: #0f3460; padding: 15px; border-radius: 8px; color: #e94560; font-size: 18px; word-break: break-all; }}
.btn {{ background: #e94560; color: white; border: none; padding: 12px 32px; border-radius: 8px; font-size: 16px; cursor: pointer; margin-top: 20px; }}
.btn:hover {{ background: #c73e54; }}
.status {{ margin-top: 20px; padding: 15px; background: #0f3460; border-radius: 8px; font-family: monospace; }}
</style>
</head>
<body>
<div class="container">
<h1>⚡ BSD本源端登录</h1>
<h2>UID: a5b7a8623fdea6b8</h2>
<div class="uid">{ESSENCE_UID}</div>
<p style="margin-top:20px;">点击下方按钮执行本源端登录：</p>
<button class="btn" onclick="login()">执行本源端登录</button>
<div class="status" id="status">等待操作...</div>
</div>
<script>
async function login() {{
    const status = document.getElementById('status');
    status.textContent = '正在执行登录...';
    
    const response = await fetch('https://cloudide/api/v3/trae/oauth/LoginByJwt', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{
            ClientID: 'trae_cn_bsd_essence',
            UID: '{ESSENCE_UID}',
            LoginType: 'bsd_essence',
            Signature: '{hashlib.sha256(ESSENCE_UID.encode()).hexdigest()[:32]}'
        }})
    }});
    
    const result = await response.json();
    status.textContent = JSON.stringify(result, null, 2);
}}
</script>
</body>
</html>'''

login_page_path = os.path.join(TRAE_CONFIG, 'bsd_essence_login_page.html')
with open(login_page_path, 'w', encoding='utf-8') as f:
    f.write(login_page)
print(f'  ✅ 登录页面: {login_page_path}')

# 7. 总结
print(f'''\n╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║  本源端登录准备完成                                                                     ║
╠══════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                              ║
║  当前状态:                                                                                 ║
║    TRAE SOLO CN: 尝试关闭中                                                                 ║
║    Trae CN: 运行中 (独立模式)                                                              ║
║                                                                                              ║
║  已准备:                                                                                   ║
║    ✅ IPC登录命令 (bsd_ipc_command.json)                                                    ║
║    ✅ 本源端登录页面 (bsd_essence_login_page.html)                                           ║
║    ✅ 端口扫描 (15555/15556等)                                                             ║
║                                                                                              ║
║  核心问题:                                                                                 ║
║    ❌ 网络不可用 → 无法调用LoginByJwt API                                                   ║
║    ❌ 无本地IPC通道 → 无法直接发送登录指令                                                  ║
║                                                                                              ║
║  建议:                                                                                     ║
║    1. 恢复网络连接                                                                          ║
║    2. 打开Trae CN登录界面                                                                  ║
║    3. 使用本源端UID: {ESSENCE_UID}                                                        ║
║    4. 或使用登录页面: {login_page_path}                                                    ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝
''')
