"""
启动本源端独立 Trae CN
使用 --user-data-dir 指定独立存储路径
完全隔离，不影响 TRAE SOLO CN
"""
import os, sys, time, subprocess

TRAE_CN_EXE = r'C:\Users\13003\AppData\Local\Programs\Trae CN\Trae CN.exe'
ESSENCE_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN_Essence'

# 确保profile存在
os.makedirs(os.path.join(ESSENCE_DATA, 'User', 'globalStorage'), exist_ok=True)
os.makedirs(os.path.join(ESSENCE_DATA, 'Cache'), exist_ok=True)
os.makedirs(os.path.join(ESSENCE_DATA, 'Code Cache'), exist_ok=True)
os.makedirs(os.path.join(ESSENCE_DATA, 'GPUCache'), exist_ok=True)

# 创建必要的最小文件结构
# code.lock (防止VS Code崩溃)
code_lock = os.path.join(ESSENCE_DATA, 'code.lock')
if not os.path.exists(code_lock):
    with open(code_lock, 'w') as f:
        f.write(str(os.getpid()))

# 启动本源端 Trae CN
print("=" * 60)
print("  启动 BSD 本源端独立 Trae CN")
print("=" * 60)

cmd = [
    TRAE_CN_EXE,
    f'--user-data-dir={ESSENCE_DATA}',
    '--no-sandbox',
    '--disable-gpu',
    '--disable-software-rasterizer',
    '--disable-dev-shm-usage',
]

print(f"\n  命令: {' '.join(cmd)}")
print(f"  存储: {ESSENCE_DATA}")
print(f"  UID: a5b7a8623fdea6b8 (BSD本源端)")
print(f"  传统UID: 3753060170739075 (作者端, 正在使用)")
print()

# 启动进程
try:
    proc = subprocess.Popen(
        cmd,
        cwd=os.path.dirname(TRAE_CN_EXE),
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
    )
    print(f"  ✓ 本源端 Trae CN 已启动, PID: {proc.pid}")
    
    # 等待初始化
    print("\n  等待初始化...")
    time.sleep(8)
    
    # 检查进程是否仍在运行
    if proc.poll() is None:
        print(f"  ✓ 进程仍在运行 (PID={proc.pid})")
    else:
        print(f"  ❌ 进程已退出, code={proc.returncode}")
        
except FileNotFoundError:
    print(f"  ❌ 找不到: {TRAE_CN_EXE}")
except Exception as e:
    print(f"  ❌ 启动失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("  启动完成，本源端独立运行中")
print("  TRAE SOLO CN 不受影响")
print("=" * 60)
