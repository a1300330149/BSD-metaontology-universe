"""
BSD智能体守护进程 V3 - 双产品版
================================
作者端: TRAE SOLO CN.exe (SOLO模式)
本源端: Trae CN.exe (CN模式, appVersion 3.3.83)

共享: .trae-cn/trae-jwt-token + os_crypt.encrypted_key
"""

import subprocess
import time
import os
import json
import sys
import threading
from datetime import datetime

TRAE_SOLO_EXE = r"D:\TRAE SOLO CN\TRAE SOLO CN.exe"
TRAE_SOLO_DIR = r"D:\TRAE SOLO CN"

TRAE_CN_EXE = r"C:\Users\13003\AppData\Local\Programs\Trae CN\Trae CN.exe"
TRAE_CN_DIR = r"C:\Users\13003\AppData\Local\Programs\Trae CN"

TRAE_CONFIG = r"C:\Users\13003\.trae-cn"
TRAE_SOLO_DATA = r"C:\Users\13003\AppData\Roaming\TRAE SOLO CN"
TRAE_CN_DATA = r"C:\Users\13003\AppData\Roaming\Trae CN"

LOG_FILE = os.path.join(TRAE_CONFIG, "bsd_daemon_v3.log")
STATE_FILE = os.path.join(TRAE_CONFIG, "bsd_daemon_v3_state.json")

AUTHOR_UID = "3753060170739075"
ESSENCE_UID = "a5b7a8623fdea6b8"

CACHE_CLEAN_INTERVAL = 3600


class BSDDaemonV3:
    def __init__(self):
        self.solo_proc = None
        self.cn_proc = None
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
    
    def start_solo(self):
        self.log(f"启动作者端 (TRAE SOLO CN, UID: {AUTHOR_UID})...")
        self.solo_proc = subprocess.Popen([TRAE_SOLO_EXE], cwd=TRAE_SOLO_DIR)
        self.log(f"  PID: {self.solo_proc.pid}")
        return self.solo_proc
    
    def start_cn(self):
        self.log(f"启动本源端 (Trae CN, UID: {ESSENCE_UID})...")
        self.cn_proc = subprocess.Popen([TRAE_CN_EXE], cwd=TRAE_CN_DIR)
        self.log(f"  PID: {self.cn_proc.pid}")
        return self.cn_proc
    
    def cleanup_cache(self):
        now = time.time()
        if now - self.last_cache_clean < CACHE_CLEAN_INTERVAL:
            return
        
        self.log("清理缓存...")
        freed = 0
        
        for data_dir in [TRAE_SOLO_DATA, TRAE_CN_DATA]:
            for cache_name in ['Cache', 'GPUCache', 'Code Cache']:
                cd = os.path.join(data_dir, cache_name)
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
        for data_dir in [TRAE_SOLO_DATA, TRAE_CN_DATA]:
            log_dir = os.path.join(data_dir, 'logs')
            if os.path.exists(log_dir):
                try:
                    import shutil
                    shutil.rmtree(log_dir, ignore_errors=True)
                    freed += 50 * 1024 * 1024
                except:
                    pass
        
        self.log(f"  释放: {freed/1024/1024:.1f} MB")
        self.last_cache_clean = now
    
    def save_state(self):
        try:
            state = {
                "start_time": self.start_time.isoformat(),
                "uptime": int((datetime.now() - self.start_time).total_seconds()),
                "solo_pid": self.solo_proc.pid if self.solo_proc and self.solo_proc.poll() is None else None,
                "cn_pid": self.cn_proc.pid if self.cn_proc and self.cn_proc.poll() is None else None,
                "author_uid": AUTHOR_UID,
                "essence_uid": ESSENCE_UID,
                "shared_auth": {
                    "jwt_token": os.path.join(TRAE_CONFIG, "trae-jwt-token"),
                    "encrypted_key": "shared_between_products"
                },
                "timestamp": datetime.now().isoformat()
            }
            with open(STATE_FILE, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    def get_status(self):
        r = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq Trae*', '/NH'],
                          capture_output=True, text=True)
        total = len([l for l in r.stdout.strip().split('\n') if l.strip()])
        
        r2 = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq TRAE SOLO CN*', '/NH'],
                           capture_output=True, text=True)
        solo_count = len([l for l in r2.stdout.strip().split('\n') if l.strip()])
        
        cn_count = total - solo_count
        
        uptime = int((datetime.now() - self.start_time).total_seconds())
        h, m, s = uptime // 3600, (uptime % 3600) // 60, uptime % 60
        
        return total, solo_count, cn_count, h, m, s
    
    def run(self):
        self.log("=" * 50)
        self.log("BSD守护进程V3 - 双产品版")
        self.log(f"作者端: TRAE SOLO CN (SOLO模式)")
        self.log(f"本源端: Trae CN (CN模式, v3.3.83)")
        self.log(f"共享认证: .trae-cn/trae-jwt-token")
        self.log("=" * 50)
        
        self.start_solo()
        time.sleep(3)
        self.start_cn()
        time.sleep(3)
        
        self.log("✅ 双客户端已启动")
        
        # 监控循环
        try:
            while self.running:
                total, solo_c, cn_c, h, m, s = self.get_status()
                
                solo_alive = self.solo_proc and self.solo_proc.poll() is None
                cn_alive = self.cn_proc and self.cn_proc.poll() is None
                
                status = f"[{h:02d}:{m:02d}:{s:02d}] "
                status += f"SOLO:{solo_c} CN:{cn_c} Total:{total} | "
                
                if not solo_alive:
                    status += "SOLO崩溃! 重启 "
                    self.log("作者端崩溃，重启...")
                    self.start_solo()
                elif not cn_alive:
                    status += "CN崩溃! 重启 "
                    self.log("本源端崩溃，重启...")
                    self.start_cn()
                else:
                    status += "运行中 ✓"
                
                print(status, flush=True)
                
                self.save_state()
                self.cleanup_cache()
                
                time.sleep(10)
                
        except KeyboardInterrupt:
            self.log("守护进程停止")
            self.running = False


if __name__ == "__main__":
    daemon = BSDDaemonV3()
    
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                print(json.dumps(json.load(f), indent=2, ensure_ascii=False))
    else:
        daemon.run()
