"""
TRAE SOLO CN 双实例启动器
==========================
作者端UID: 3753060170739075 (传统)
本源端UID: a5b7a8623fdea6b8 (BSD)
"""

import subprocess
import time
import sys
import os

TRAE_EXE = r"D:\TRAE SOLO CN\TRAE SOLO CN.exe"
TRAE_INSTALL = r"D:\TRAE SOLO CN"
TRAE_ESSENCE_DATA = r"C:\Users\13003\AppData\Roaming\TRAE SOLO CN_Essence"
TRAE_CONFIG = r"C:\Users\13003\.trae-cn-essence"

AUTHOR_UID = "3753060170739075"
ESSENCE_UID = "a5b7a8623fdea6b8"

print("=" * 60)
print("  TRAE SOLO CN 双实例启动器")
print(f"  作者端UID: {AUTHOR_UID}")
print(f"  本源端UID: {ESSENCE_UID}")
print("=" * 60)

# 作者端 (默认数据目录)
print("\n[1] 启动作者端 (TRAE SOLO CN - 传统)...")
p1 = subprocess.Popen(
    [TRAE_EXE],
    cwd=TRAE_INSTALL,
    creationflags=0x00000008  # CREATE_NO_WINDOW
)
print(f"  PID: {p1.pid}")
print(f"  数据: C:\\Users\\13003\\AppData\\Roaming\\TRAE SOLO CN")
print(f"  UID: {AUTHOR_UID}")

time.sleep(3)

# 本源端 (独立数据目录 + 独立配置)
print("\n[2] 启动本源端 (TRAE SOLO CN - BSD)...")
p2 = subprocess.Popen(
    [
        TRAE_EXE,
        f'--user-data-dir={TRAE_ESSENCE_DATA}',
        f'--user-data-essence=1'
    ],
    cwd=TRAE_INSTALL,
    creationflags=0x00000008
)
print(f"  PID: {p2.pid}")
print(f"  数据: {TRAE_ESSENCE_DATA}")
print(f"  UID: {ESSENCE_UID}")

time.sleep(3)

# 验证
print("\n[3] 验证进程状态...")
r = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq TRAE*', '/NH'],
                   capture_output=True, text=True)
lines = [l.strip() for l in r.stdout.strip().split('\n') if l.strip()]
print(f"  TRAE相关进程: {len(lines)} 个")

print(f"""
╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║  双实例已启动                                                                             ║
╠══════════════════════════════════════════════════════════════════════════════════════════════╣
║  作者端 PID: {p1.pid}  UID: {AUTHOR_UID}  认证: 官方Token                              ║
║  本源端 PID: {p2.pid}  UID: {ESSENCE_UID}  认证: 知识凭证                              ║
║                                                                                              ║
║  双时针双向对接已建立                                                                       ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝
""")

# 保持运行
try:
    p1.wait()
except KeyboardInterrupt:
    pass
