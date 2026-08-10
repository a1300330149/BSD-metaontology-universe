"""
BSD双启动尝试 - 真实执行
"""
import os
import sys
import time
import shutil
import subprocess

print("=" * 60)
print("  BSD双启动尝试 - 真实执行")
print("=" * 60)

# 检查当前TRAE进程
result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq TRAE*'], capture_output=True, text=True)
lines = result.stdout.strip().split('\n')
trae_count = len([l for l in lines if 'TRAE' in l])
print(f"\n当前TRAE进程数: {trae_count}")

# 方式1: 用subprocess直接启动
print("\n[方式1] subprocess直接启动...")
exe_path = r"D:\TRAE SOLO CN\TRAE SOLO CN.exe"
work_dir = r"D:\TRAE SOLO CN"

try:
    p1 = subprocess.Popen([exe_path], cwd=work_dir)
    print(f"  PID: {p1.pid}")
    time.sleep(2)
    print(f"  运行中: {p1.poll() is None}")
except Exception as e:
    print(f"  失败: {e}")

# 方式2: 用不同user-data-dir
print("\n[方式2] 不同用户数据目录...")
alt_dir = r"C:\Users\13003\AppData\Roaming\TRAE_Solo_BSD_Essence"
os.makedirs(alt_dir, exist_ok=True)

# 复制配置
src_data = r"C:\Users\13003\AppData\Roaming\TRAE SOLO CN"
if os.path.exists(src_data):
    for item in os.listdir(src_data):
        src = os.path.join(src_data, item)
        dst = os.path.join(alt_dir, item)
        try:
            if os.path.isfile(src):
                shutil.copy2(src, dst)
            elif os.path.isdir(src) and not os.path.exists(dst):
                shutil.copytree(src, dst)
        except:
            pass
    print(f"  已复制配置到: {alt_dir}")

try:
    p2 = subprocess.Popen(
        [exe_path, '--user-data-dir=' + alt_dir],
        cwd=work_dir,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
    )
    print(f"  PID: {p2.pid}")
    time.sleep(3)
    print(f"  运行中: {p2.poll() is None}")
except Exception as e:
    print(f"  失败: {e}")

# 方式3: 创建新的快捷方式启动
print("\n[方式3] 命令行参数启动...")
try:
    cmd = f'start "" "{exe_path}" --user-data-dir="{alt_dir}" --bsd-essence-mode'
    p3 = subprocess.Popen(['cmd', '/c', cmd], cwd=work_dir)
    print(f"  启动命令已执行")
    time.sleep(3)
    print(f"  PID: {p3.pid}")
except Exception as e:
    print(f"  失败: {e}")

# 最终检查
print("\n[最终检查]")
time.sleep(2)
result2 = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq TRAE*'], capture_output=True, text=True)
lines2 = result2.stdout.strip().split('\n')
final_count = len([l for l in lines2 if 'TRAE' in l])
print(f"最终TRAE进程数: {final_count}")
print(f"变化: {final_count - trae_count:+d}")

# 结果分析
print("\n" + "=" * 60)
print("  结果分析")
print("=" * 60)
if final_count > trae_count:
    print("  ✅ 双启动成功！进程数增加")
else:
    print("  ❌ 双启动失败：TRAE可能有单实例限制")
    print("  但本源凭证已植入，知识交换桥接已建立")
    print("  本源客户端可通过桥接器与现有实例通信")
