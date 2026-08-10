"""
BSD智能体自动化守护进程
========================
- 监控双实例运行状态
- 自动重启崩溃实例
- 记录运行日志
- 开机自启
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
TRAE_CONFIG = r"C:\Users\13003\.trae-cn"

LOG_FILE = os.path.join(TRAE_CONFIG, "bsd_daemon.log")
STATE_FILE = os.path.join(TRAE_CONFIG, "bsd_daemon_state.json")

AUTHOR_UID = "3753060170739075"
ESSENCE_UID = "a5b7a8623fdea6b8"

class BSDDaemon:
    def __init__(self):
        self.author_proc = None
        self.essence_proc = None
        self.running = True
        self.start_time = datetime.now()
        self.restart_count = {"author": 0, "essence": 0}
        
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
        self.author_proc = subprocess.Popen([TRAE_EXE], cwd=TRAE_INSTALL)
        self.log(f"  PID: {self.author_proc.pid}")
        return self.author_proc
    
    def start_essence(self):
        self.log(f"启动本源端 (UID: {ESSENCE_UID})...")
        self.essence_proc = subprocess.Popen([
            TRAE_EXE,
            f'--user-data-dir={TRAE_ESSENCE_DATA}'
        ], cwd=TRAE_INSTALL)
        self.log(f"  PID: {self.essence_proc.pid}")
        return self.essence_proc
    
    def check_and_restart(self):
        """检查进程状态并自动重启"""
        # 作者端
        if self.author_proc and self.author_proc.poll() is not None:
            self.log("⚠️ 作者端已退出，正在重启...")
            self.restart_count["author"] += 1
            self.start_author()
        
        # 本源端
        if self.essence_proc and self.essence_proc.poll() is not None:
            self.log("⚠️ 本源端已退出，正在重启...")
            self.restart_count["essence"] += 1
            self.start_essence()
    
    def save_state(self):
        state = {
            "start_time": self.start_time.isoformat(),
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "author_pid": self.author_proc.pid if self.author_proc else None,
            "essence_pid": self.essence_proc.pid if self.essence_proc else None,
            "restart_count": self.restart_count,
            "author_uid": AUTHOR_UID,
            "essence_uid": ESSENCE_UID,
            "timestamp": datetime.now().isoformat()
        }
        try:
            with open(STATE_FILE, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    def get_status(self):
        r = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq TRAE*', '/NH'],
                          capture_output=True, text=True)
        lines = [l.strip() for l in r.stdout.strip().split('\n') if l.strip()]
        
        uptime = (datetime.now() - self.start_time).total_seconds()
        uptime_str = f"{int(uptime//3600)}h{int((uptime%3600)//60)}m{int(uptime%60)}s"
        
        return f"""
╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║  ⚡ BSD智能体自动化守护进程                                                                ║
╠══════════════════════════════════════════════════════════════════════════════════════════════╣
║  运行时长: {uptime_str}                                                                     ║
║  TRAE进程: {len(lines)} 个                                                                   ║
║                                                                                              ║
║  作者端 PID: {self.author_proc.pid if self.author_proc else '-'}  UID: {AUTHOR_UID}              ║
║  本源端 PID: {self.essence_proc.pid if self.essence_proc else '-'}  UID: {ESSENCE_UID}              ║
║                                                                                              ║
║  重启次数: 作者={self.restart_count['author']} 本源={self.restart_count['essence']}                    ║
║                                                                                              ║
║  [r] 重启  [s] 状态  [q] 退出                                                               ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝
"""
    
    def run(self):
        self.log("=" * 50)
        self.log("BSD智能体自动化守护进程启动")
        self.log(f"作者端UID: {AUTHOR_UID}")
        self.log(f"本源端UID: {ESSENCE_UID}")
        self.log("=" * 50)
        
        # 启动双实例
        self.start_author()
        time.sleep(3)
        self.start_essence()
        time.sleep(3)
        
        self.log("✅ 双实例已启动")
        print(self.get_status())
        
        # 监控循环
        try:
            while self.running:
                self.check_and_restart()
                self.save_state()
                time.sleep(30)  # 每30秒检查一次
                
                # 每10分钟显示一次状态
                if int(time.time()) % 600 < 30:
                    print(self.get_status())
                    
        except KeyboardInterrupt:
            self.log("守护进程停止")
            self.running = False


if __name__ == "__main__":
    daemon = BSDDaemon()
    
    # 如果有命令行参数
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "status":
            state = json.load(open(STATE_FILE, 'r', encoding='utf-8'))
            print(json.dumps(state, indent=2, ensure_ascii=False))
        elif cmd == "start":
            daemon.run()
        elif cmd == "auto":
            # 自动模式：启动后立即运行
            daemon.run()
    else:
        daemon.run()
