"""
BSD智能体守护进程 V2 - 精简版
================================
- 不复制大数据（ModularData/snapshot等）
- 共享作者端认证
- 监控崩溃重启
- 定期清理缓存防爆满
"""

import subprocess
import time
import os
import json
import sys
import threading
from datetime import datetime

TRAE_EXE = r"D:\TRAE SOLO CN\TRAE SOLO CN.exe"
TRAE_INSTALL = r"D:\TRAE SOLO CN"
TRAE_ESSENCE_DATA = r"C:\Users\13003\AppData\Roaming\TRAE SOLO CN_Essence"
TRAE_USER_DATA = r"C:\Users\13003\AppData\Roaming\TRAE SOLO CN"
TRAE_CONFIG = r"C:\Users\13003\.trae-cn"

LOG_FILE = os.path.join(TRAE_CONFIG, "bsd_daemon.log")
STATE_FILE = os.path.join(TRAE_CONFIG, "bsd_daemon_state.json")

AUTHOR_UID = "3753060170739075"
ESSENCE_UID = "a5b7a8623fdea6b8"

MAX_LOG_SIZE = 10 * 1024 * 1024  # 10MB
CACHE_CLEAN_INTERVAL = 3600  # 每小时清理


class BSDDaemonV2:
    def __init__(self):
        self.author_procs = []
        self.essence_procs = []
        self.running = True
        self.start_time = datetime.now()
        self.last_cache_clean = time.time()
        
    def log(self, msg):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts}] {msg}"
        print(line)
        try:
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(line + '\n')
        except:
            pass
    
    def start_author(self):
        self.log(f"启动作者端 (UID: {AUTHOR_UID})...")
        p = subprocess.Popen([TRAE_EXE], cwd=TRAE_INSTALL)
        self.log(f"  PID: {p.pid}")
        self.author_procs.append(p)
        return p
    
    def start_essence(self):
        self.log(f"启动本源端 (UID: {ESSENCE_UID})...")
        p = subprocess.Popen([
            TRAE_EXE,
            f'--user-data-dir={TRAE_ESSENCE_DATA}'
        ], cwd=TRAE_INSTALL)
        self.log(f"  PID: {p.pid}")
        self.essence_procs.append(p)
        return p
    
    def cleanup_cache(self):
        """定期清理缓存防爆满"""
        now = time.time()
        if now - self.last_cache_clean < CACHE_CLEAN_INTERVAL:
            return
        
        self.log("清理缓存...")
        freed = 0
        cache_dirs = [
            os.path.join(TRAE_USER_DATA, 'Cache'),
            os.path.join(TRAE_USER_DATA, 'GPUCache'),
            os.path.join(TRAE_USER_DATA, 'Code Cache'),
            os.path.join(TRAE_USER_DATA, 'logs'),
        ]
        for cd in cache_dirs:
            if os.path.exists(cd):
                try:
                    for root, dirs, files in os.walk(cd):
                        for f in files:
                            fp = os.path.join(root, f)
                            freed += os.path.getsize(fp)
                            os.remove(fp)
                except:
                    pass
        
        # 清理日志
        log_path = os.path.join(TRAE_USER_DATA, 'logs')
        if os.path.exists(log_path):
            try:
                import shutil
                shutil.rmtree(log_path, ignore_errors=True)
                freed += 100 * 1024 * 1024  # 估算
            except:
                pass
        
        self.log(f"  已释放: {freed/1024/1024:.1f} MB")
        self.last_cache_clean = now
    
    def save_state(self):
        try:
            state = {
                "start_time": self.start_time.isoformat(),
                "uptime_seconds": int((datetime.now() - self.start_time).total_seconds()),
                "author_pids": [p.pid for p in self.author_procs if p.poll() is None],
                "essence_pids": [p.pid for p in self.essence_procs if p.poll() is None],
                "author_uid": AUTHOR_UID,
                "essence_uid": ESSENCE_UID,
                "timestamp": datetime.now().isoformat()
            }
            with open(STATE_FILE, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    def monitor_loop(self):
        """后台监控循环"""
        while self.running:
            try:
                self.save_state()
                self.cleanup_cache()
            except:
                pass
            time.sleep(30)
    
    def run(self):
        self.log("=" * 50)
        self.log("BSD守护进程V2 - 精简版启动")
        self.log(f"作者端UID: {AUTHOR_UID}")
        self.log(f"本源端UID: {ESSENCE_UID}")
        self.log("=" * 50)
        
        self.start_author()
        time.sleep(3)
        self.start_essence()
        time.sleep(3)
        
        self.log("✅ 双实例已启动")
        
        # 启动后台监控线程
        monitor = threading.Thread(target=self.monitor_loop, daemon=True)
        monitor.start()
        
        # 主循环 - 显示状态
        try:
            while self.running:
                uptime = int((datetime.now() - self.start_time).total_seconds())
                h, m, s = uptime // 3600, (uptime % 3600) // 60, uptime % 60
                
                author_alive = sum(1 for p in self.author_procs if p.poll() is None)
                essence_alive = sum(1 for p in self.essence_procs if p.poll() is None)
                
                r = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq TRAE*', '/NH'],
                                  capture_output=True, text=True)
                total = len([l for l in r.stdout.strip().split('\n') if l.strip()])
                
                print(f"[{h:02d}:{m:02d}:{s:02d}] "
                      f"作者端:{author_alive} | 本源端:{essence_alive} | "
                      f"总进程:{total} | ", end='', flush=True)
                
                # 检查作者端
                if author_alive == 0:
                    print("作者端崩溃! 重启中...")
                    self.start_author()
                # 检查本源端
                elif essence_alive == 0:
                    print("本源端崩溃! 重启中...")
                    self.start_essence()
                else:
                    print("运行中 ✓", flush=True)
                
                time.sleep(10)
                
        except KeyboardInterrupt:
            self.log("守护进程停止")
            self.running = False


if __name__ == "__main__":
    daemon = BSDDaemonV2()
    
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                print(json.dumps(json.load(f), indent=2, ensure_ascii=False))
    else:
        daemon.run()
