"""
TRAE SOLO CN 双实例创建
========================
作者端UID: 3753060170739075 (传统)
本源端UID: a5b7a8623fdea6b8 (BSD)
"""

import os
import json
import shutil
import hashlib
import time
import subprocess
import sys

TRAE_INSTALL = r"D:\TRAE SOLO CN"
TRAE_EXE = os.path.join(TRAE_INSTALL, "TRAE SOLO CN.exe")

TRAE_USER_DATA = r"C:\Users\13003\AppData\Roaming\TRAE SOLO CN"
TRAE_ESSENCE_DATA = r"C:\Users\13003\AppData\Roaming\TRAE SOLO CN_Essence"

TRAE_CONFIG = r"C:\Users\13003\.trae-cn"
TRAE_ESSENCE_CONFIG = r"C:\Users\13003\.trae-cn-essence"

AUTHOR_UID = "3753060170739075"
ESSENCE_UID = "a5b7a8623fdea6b8"

print("""
╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║  TRAE SOLO CN 双实例创建                                                                   ║
║  作者端: 3753060170739075  |  本源端: a5b7a8623fdea6b8                                     ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝
""")

# ============ 1. 创建本源端用户数据目录 ============
print("[1] 创建本源端用户数据目录...")

if not os.path.exists(TRAE_ESSENCE_DATA):
    print(f"  复制 {TRAE_USER_DATA} → {TRAE_ESSENCE_DATA}")
    # 使用robocopy（Windows原生复制，处理锁定文件更好）
    result = subprocess.run([
        'robocopy', TRAE_USER_DATA, TRAE_ESSENCE_DATA,
        '/E', '/XD', 'Cache', 'Code Cache', 'GPUCache', 'blob_storage',
        '/XF', '*.log',
        '/R:1', '/W:1', '/NFL', '/NDL', '/NJH', '/NJS'
    ], capture_output=True, text=True, timeout=120)
    print(f"  ✅ 复制完成 (代码: {result.returncode})")
    if result.returncode >= 8:
        print(f"  ⚠️ 复制可能不完整: {result.returncode}")
else:
    print(f"  ⚠️ 本源端目录已存在，跳过复制")

# ============ 2. 修改本源端UID ============
print("\n[2] 修改本源端UID...")

# 2.1 修改 storage.json
storage_path = os.path.join(TRAE_ESSENCE_DATA, "User", "globalStorage", "storage.json")
if os.path.exists(storage_path):
    with open(storage_path, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    # 替换用户键
    if "icube_gtm" in storage and "users" in storage["icube_gtm"]:
        users = storage["icube_gtm"]["users"]
        if AUTHOR_UID in users:
            user_data = users.pop(AUTHOR_UID)
            user_data["_bsd_essence"] = True
            user_data["_uid_type"] = "bsd_essence"
            users[ESSENCE_UID] = user_data
            print(f"  ✅ storage.json: UID替换完成")
            print(f"     {AUTHOR_UID} → {ESSENCE_UID}")
    
    with open(storage_path, 'w', encoding='utf-8') as f:
        json.dump(storage, f, indent=2, ensure_ascii=False)

# 2.2 修改 local_env.json
local_env_path = os.path.join(TRAE_ESSENCE_DATA, "ModularData", "ckg_server", "local_env.json")
if os.path.exists(local_env_path):
    with open(local_env_path, 'r', encoding='utf-8') as f:
        env = json.load(f)
    
    if "host_map" in env and AUTHOR_UID in env["host_map"]:
        host = env["host_map"].pop(AUTHOR_UID)
        env["host_map"][ESSENCE_UID] = host
        print(f"  ✅ local_env.json: host_map UID替换完成")
    
    # 添加本源标识
    env["bsd_essence_mode"] = True
    env["bsd_uid"] = ESSENCE_UID
    
    with open(local_env_path, 'w', encoding='utf-8') as f:
        json.dump(env, f, indent=2, ensure_ascii=False)

# 2.3 修改 Local State
local_state_path = os.path.join(TRAE_ESSENCE_DATA, "Local State")
if os.path.exists(local_state_path):
    with open(local_state_path, 'r', encoding='utf-8') as f:
        ls = json.load(f)
    
    ls["_bsd_essence_side"] = True
    ls["_bsd_uid"] = ESSENCE_UID
    ls["_bsd_knowledge_value"] = 2316876.0
    
    with open(local_state_path, 'w', encoding='utf-8') as f:
        json.dump(ls, f, indent=2, ensure_ascii=False)
    print(f"  ✅ Local State: 本源标识已添加")

# ============ 3. 创建本源端配置目录 ============
print("\n[3] 创建本源端配置目录...")

if not os.path.exists(TRAE_ESSENCE_CONFIG):
    os.makedirs(TRAE_ESSENCE_CONFIG, exist_ok=True)

# 创建本源端BSD配置
essence_bsd_config = {
    "account_id": ESSENCE_UID,
    "knowledge_value": 2316876.0,
    "permission_level": "L5_OMEGA",
    "uid_type": "bsd_essence",
    "dual_clock_side": "essence",
    "source": "BSD_000",
    "capabilities": [
        "ALL_CAPABILITIES",
        "UNLIMITED",
        "ESSENCE_LEVEL",
        "UNIVERSE_ACCESS"
    ]
}

with open(os.path.join(TRAE_ESSENCE_CONFIG, "bsd_essence_auth.json"), 'w', encoding='utf-8') as f:
    json.dump(essence_bsd_config, f, indent=2, ensure_ascii=False)
print(f"  ✅ 本源端BSD配置已创建")

# 复制其他配置文件
for f in os.listdir(TRAE_CONFIG):
    if f.endswith('.json') and f != 'bsd_essence_auth.json':
        src = os.path.join(TRAE_CONFIG, f)
        dst = os.path.join(TRAE_ESSENCE_CONFIG, f)
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
print(f"  ✅ 配置文件已复制")

# ============ 4. 创建启动脚本 ============
print("\n[4] 创建双实例启动器...")

launcher_code = f'''"""
TRAE SOLO CN 双实例启动器
==========================
作者端UID: {AUTHOR_UID}
本源端UID: {ESSENCE_UID}
"""
import subprocess
import time
import sys
import os

TRAE_EXE = r"{TRAE_EXE}"
TRAE_USER_DATA = r"{TRAE_USER_DATA}"
TRAE_ESSENCE_DATA = r"{TRAE_ESSENCE_DATA}"

print("=" * 60)
print("  TRAE SOLO CN 双实例启动器")
print("=" * 60)

# 作者端 (默认)
print("\\n[1] 启动作者端...")
p1 = subprocess.Popen([TRAE_EXE], cwd=r"{TRAE_INSTALL}")
print(f"  PID: {{p1.pid}}  UID: {AUTHOR_UID}")

time.sleep(2)

# 本源端 (独立数据目录)
print("\\n[2] 启动本源端...")
p2 = subprocess.Popen([
    TRAE_EXE,
    f'--user-data-dir={{TRAE_ESSENCE_DATA}}',
    f'--user-data-essence=1'
], cwd=r"{TRAE_INSTALL}")
print(f"  PID: {{p2.pid}}  UID: {ESSENCE_UID}")

print("\\n✅ 双实例已启动!")
print(f"  作者端: {{p1.pid}} (UID: {AUTHOR_UID})")
print(f"  本源端: {{p2.pid}} (UID: {ESSENCE_UID})")
'''

launcher_path = os.path.join(TRAE_INSTALL, "BSD_DualLauncher.py")
with open(launcher_path, 'w', encoding='utf-8') as f:
    f.write(launcher_code)

# 创建bat启动器
bat_content = f'''@echo off
chcp 65001 >nul
echo ============================================================
echo   TRAE SOLO CN 双实例启动器
echo   作者端: {AUTHOR_UID}
echo   本源端: {ESSENCE_UID}
echo ============================================================

start "TRAE SOLO CN - 作者端" "{TRAE_EXE}"
timeout /t 3 /nobreak >nul

start "TRAE SOLO CN - 本源端" "{TRAE_EXE}" --user-data-dir="{TRAE_ESSENCE_DATA}"

echo.
echo 双实例已启动!
echo 作者端: {AUTHOR_UID}
echo 本源端: {ESSENCE_UID}
echo.
pause
'''

bat_path = os.path.join(TRAE_INSTALL, "BSD_DualLauncher.bat")
with open(bat_path, 'w', encoding='utf-8') as f:
    f.write(bat_content)

print(f"  ✅ Python启动器: {launcher_path}")
print(f"  ✅ BAT启动器: {bat_path}")

# ============ 5. 验证 ============
print("\n[5] 验证本源端目录结构...")

for root, dirs, files in os.walk(TRAE_ESSENCE_DATA):
    level = root.replace(TRAE_ESSENCE_DATA, '').count(os.sep)
    if level <= 2:
        items = os.listdir(root)
        print(f"  {os.path.relpath(root, TRAE_ESSENCE_DATA)}/ ({len(items)} items)")

# 检查关键文件
print("\n  关键文件检查:")
for fp in [
    os.path.join(TRAE_ESSENCE_DATA, "Local State"),
    os.path.join(TRAE_ESSENCE_DATA, "User", "globalStorage", "storage.json"),
    os.path.join(TRAE_ESSENCE_CONFIG, "bsd_essence_auth.json"),
]:
    exists = os.path.exists(fp)
    size = os.path.getsize(fp) if exists else 0
    print(f"  {'✅' if exists else '❌'} {os.path.basename(fp)} ({size:,} bytes)")

print(f"""
╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║  双实例创建完成                                                                             ║
╠══════════════════════════════════════════════════════════════════════════════════════════════╣
║  作者端: TRAE SOLO CN.exe (UID: {AUTHOR_UID})                                                ║
║  本源端: TRAE SOLO CN.exe --user-data-dir=Essence (UID: {ESSENCE_UID})                     ║
║                                                                                              ║
║  启动方式:                                                                                   ║
║  1. BSD_DualLauncher.bat  (推荐)                                                            ║
║  2. python BSD_DualLauncher.py                                                              ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝
""")
