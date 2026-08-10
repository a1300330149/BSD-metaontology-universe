"""
重启本源端 Trae CN - 使用新的完整独立profile
"""
import os, sys, time, subprocess

TRAE_CN_EXE = r'C:\Users\13003\AppData\Local\Programs\Trae CN\Trae CN.exe'
ESSENCE_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN_Essence'

# 先杀掉可能存在的旧实例
print("=== 清理旧实例 ===")
import psutil
try:
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = ' '.join(proc.info.get('cmdline') or [])
            if 'Trae CN.exe' in cmdline and ESSENCE_DATA.replace('\\', '/') in cmdline.replace('\\', '/'):
                print(f"  杀掉 PID={proc.pid}: {cmdline[:200]}")
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
except ImportError:
    print("  psutil 不可用, 跳过清理")

time.sleep(2)

# 启动新实例
print("\n=== 启动新实例 ===")
cmd = [
    TRAE_CN_EXE,
    f'--user-data-dir={ESSENCE_DATA}',
    '--no-sandbox',
    '--disable-gpu',
    '--disable-software-rasterizer',
]

print(f"  命令: {' '.join(cmd)}")
proc = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
print(f"  ✓ 已启动 PID={proc.pid}")

print("\n  等待初始化 (8秒)...")
time.sleep(8)

if proc.poll() is None:
    print(f"  ✓ 进程仍在运行")
else:
    print(f"  ❌ 进程已退出 code={proc.returncode}")
