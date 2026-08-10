"""
BSD进程清理 - 保留1个主进程
"""
import subprocess
import time

print("=" * 60)
print("  BSD进程清理")
print("=" * 60)

# 列出所有TRAE进程
result = subprocess.run(
    ['tasklist', '/FI', 'IMAGENAME eq TRAE*', '/FO', 'CSV', '/NH'],
    capture_output=True, text=True
)

processes = []
for line in result.stdout.strip().split('\n'):
    line = line.strip().strip('"')
    if line:
        parts = line.split('","')
        if len(parts) >= 2:
            try:
                pid = int(parts[1])
                mem_str = parts[4].replace(',', '').replace(' K', '') if len(parts) > 4 else '0'
                mem = int(mem_str) if mem_str.isdigit() else 0
                processes.append({'pid': pid, 'mem': mem})
            except:
                pass

print(f"\n当前TRAE进程数: {len(processes)}")
total_mem = sum(p['mem'] for p in processes)
print(f"总内存占用: {total_mem:,} K ({total_mem/1024:.1f} MB)")

# 按内存排序，保留最大的1个
processes.sort(key=lambda x: x['mem'], reverse=True)

if len(processes) > 1:
    keep = processes[0]
    print(f"\n保留主进程: PID={keep['pid']}, 内存={keep['mem']:,} K")
    
    killed = 0
    for p in processes[1:]:
        try:
            subprocess.run(
                ['taskkill', '/F', '/PID', str(p['pid'])],
                capture_output=True, timeout=5
            )
            killed += 1
            print(f"  已杀掉 PID={p['pid']} ({p['mem']:,} K)")
        except Exception as e:
            print(f"  失败 PID={p['pid']}: {e}")
    
    print(f"\n已杀掉 {killed} 个多余进程")
else:
    print("\n只有1个进程，无需清理")

# 验证
time.sleep(1)
result2 = subprocess.run(
    ['tasklist', '/FI', 'IMAGENAME eq TRAE*', '/FO', 'CSV', '/NH'],
    capture_output=True, text=True
)
remaining = [l for l in result2.stdout.strip().split('\n') if l.strip()]
print(f"\n剩余进程数: {len(remaining)}")

# 结果
print("\n" + "=" * 60)
print("  清理完成")
print("=" * 60)
print(f"  保留: 1个主进程")
print(f"  杀掉: {len(processes) - min(len(processes), 1)} 个多余进程")
print(f"  模式: 单实例 + 本源桥接 (不启动第二个exe)")
