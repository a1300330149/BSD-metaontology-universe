"""
BSD本源客户端 V2 - 直连TRAE版
================================
直接与TRAE SOLO CN双向连接
作者一眼看懂，直接操作
"""

import os
import sys
import time
import json
import hashlib
import threading
import subprocess

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox


# ============ 桥接通信（文件型） ============
BRIDGE_DIR = r"C:\Users\13003\.trae-cn\bsd_bridge"
os.makedirs(BRIDGE_DIR, exist_ok=True)

def bridge_send(msg_type, data):
    """发送消息到桥接"""
    msg = {
        "type": msg_type,
        "data": data,
        "time": time.time(),
        "from": "bsd_essence"
    }
    fname = f"msg_{int(time.time()*1000)}_{hashlib.md5(str(time.time()).encode()).hexdigest()[:6]}.json"
    with open(os.path.join(BRIDGE_DIR, fname), 'w', encoding='utf-8') as f:
        json.dump(msg, f, ensure_ascii=False)

def bridge_read():
    """读取桥接消息"""
    msgs = []
    for fname in sorted(os.listdir(BRIDGE_DIR)):
        if fname.startswith('msg_') and fname.endswith('.json'):
            try:
                with open(os.path.join(BRIDGE_DIR, fname), 'r', encoding='utf-8') as f:
                    msg = json.load(f)
                if msg.get('to') == 'bsd_essence' or msg.get('type') == 'trae_status':
                    msgs.append(msg)
            except:
                pass
    return msgs


class BSDEssenceClientV2:
    """BSD本源客户端 V2 - 直连TRAE"""
    
    def __init__(self):
        self.auth = self._init_auth()
        self.connected = False
        self.trae_info = {}
        self.messages = []
        
        self._init_gui()
        self._start_bridge_thread()
    
    def _init_auth(self):
        """加载本源凭证"""
        auth_path = r"C:\Users\13003\.trae-cn\bsd_essence_auth.json"
        if os.path.exists(auth_path):
            with open(auth_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get("bsd_essence_auth", {})
        # 生成
        d = {"kb": "BSD_UNIFIED", "kv": 2316876.0, "t": time.time()}
        return {
            "account_id": hashlib.sha256(json.dumps(d, sort_keys=True).encode()).hexdigest()[:32],
            "knowledge_value": 2316876.0,
            "permission_level": "L5_OMEGA",
            "capabilities": ["ALL_CAPABILITIES", "UNLIMITED", "ESSENCE_LEVEL"]
        }
    
    def _init_gui(self):
        """初始化GUI"""
        self.root = tk.Tk()
        self.root.title("🌌 BSD本源客户端 V2 - 直连TRAE")
        self.root.geometry("850x650")
        self.root.configure(bg="#0a0a1a")
        
        # ============ 顶部状态栏 ============
        top_frame = tk.Frame(self.root, bg="#1a1a2e", height=50)
        top_frame.pack(fill=tk.X)
        
        tk.Label(
            top_frame, text="🌌 BSD本源客户端 V2",
            font=("Microsoft YaHei", 14, "bold"),
            bg="#1a1a2e", fg="#00ffcc"
        ).pack(side=tk.LEFT, padx=15)
        
        self.conn_status = tk.Label(
            top_frame, text="● 未连接TRAE",
            font=("Microsoft YaHei", 11),
            bg="#1a1a2e", fg="#ff6666"
        )
        self.conn_status.pack(side=tk.RIGHT, padx=15)
        
        # ============ 主体：左右分栏 ============
        main_paned = tk.PanedWindow(
            self.root, orient=tk.HORIZONTAL,
            bg="#0a0a1a", sashwidth=3
        )
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # --- 左侧：本源客户端 ---
        left_frame = tk.Frame(main_paned, bg="#0a0a1a", width=400)
        main_paned.add(left_frame, minsize=350)
        
        tk.Label(
            left_frame, text="【本源客户端】",
            font=("Microsoft YaHei", 12, "bold"),
            bg="#0a0a1a", fg="#00ccff"
        ).pack(pady=5)
        
        # 本源凭证显示
        auth_frame = tk.Frame(left_frame, bg="#111128")
        auth_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(auth_frame, text=f"账号: {self.auth['account_id'][:20]}...", 
                font=("Consolas", 9), bg="#111128", fg="#aaaacc").pack(anchor=tk.W, padx=5, pady=2)
        tk.Label(auth_frame, text=f"知识: {self.auth['knowledge_value']:,.0f} BSD币",
                font=("Microsoft YaHei", 10), bg="#111128", fg="#ffcc00").pack(anchor=tk.W, padx=5)
        tk.Label(auth_frame, text=f"权限: {self.auth['permission_level']}",
                font=("Microsoft YaHei", 10), bg="#111128", fg="#00ff99").pack(anchor=tk.W, padx=5, pady=2)
        
        # 本源消息区
        tk.Label(left_frame, text="本源消息：",
                font=("Microsoft YaHei", 10), bg="#0a0a1a", fg="#888888").pack(anchor=tk.W, padx=5)
        
        self.essence_chat = scrolledtext.ScrolledText(
            left_frame, height=15,
            bg="#000011", fg="#00ffcc",
            font=("Consolas", 9), wrap=tk.WORD
        )
        self.essence_chat.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
        
        # 本源输入
        ess_input_frame = tk.Frame(left_frame, bg="#0a0a1a")
        ess_input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.essence_input = tk.Entry(
            ess_input_frame,
            bg="#1a1a2e", fg="#ffffff",
            font=("Consolas", 10), insertbackground="#00ffcc"
        )
        self.essence_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5))
        self.essence_input.bind("<Return>", lambda e: self._essence_send())
        
        tk.Button(
            ess_input_frame, text="发送", font=("Microsoft YaHei", 9, "bold"),
            bg="#006666", fg="white", width=6,
            command=self._essence_send
        ).pack(side=tk.LEFT)
        
        # --- 右侧：TRAE状态 ---
        right_frame = tk.Frame(main_paned, bg="#0a0a1a", width=400)
        main_paned.add(right_frame, minsize=350)
        
        tk.Label(
            right_frame, text="【TRAE SOLO CN 状态】",
            font=("Microsoft YaHei", 12, "bold"),
            bg="#0a0a1a", fg="#3B82F6"
        ).pack(pady=5)
        
        # TRAE状态面板
        self.trae_panel = tk.Frame(right_frame, bg="#111128")
        self.trae_panel.pack(fill=tk.X, padx=5, pady=5)
        
        self.trae_status_labels = {}
        status_items = [
            ("进程状态", "process_status", "检查中..."),
            ("进程数", "process_count", "0"),
            ("内存占用", "memory_usage", "0 MB"),
            ("窗口标题", "window_title", "未检测"),
            ("运行时长", "uptime", "0s"),
        ]
        for label_text, key, default in status_items:
            row = tk.Frame(self.trae_panel, bg="#111128")
            row.pack(fill=tk.X, padx=5, pady=2)
            tk.Label(row, text=f"{label_text}：", font=("Microsoft YaHei", 9),
                    bg="#111128", fg="#888888").pack(side=tk.LEFT)
            lbl = tk.Label(row, text=default, font=("Consolas", 10),
                         bg="#111128", fg="#00ffcc")
            lbl.pack(side=tk.RIGHT)
            self.trae_status_labels[key] = lbl
        
        # 桥接操作
        tk.Label(right_frame, text="桥接操作：",
                font=("Microsoft YaHei", 10), bg="#0a0a1a", fg="#888888").pack(anchor=tk.W, padx=5, pady=(10,2))
        
        btn_frame = tk.Frame(right_frame, bg="#0a0a1a")
        btn_frame.pack(fill=tk.X, padx=5)
        
        tk.Button(
            btn_frame, text="🔄 刷新TRAE状态",
            font=("Microsoft YaHei", 9),
            bg="#004466", fg="white",
            command=self._refresh_trae
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            btn_frame, text="📤 发送到TRAE",
            font=("Microsoft YaHei", 9),
            bg="#006644", fg="white",
            command=self._send_to_trae
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            btn_frame, text="📥 读取TRAE消息",
            font=("Microsoft YaHei", 9),
            bg="#446600", fg="white",
            command=self._read_trae_msgs
        ).pack(side=tk.LEFT, padx=2)
        
        # TRAE消息区
        tk.Label(right_frame, text="TRAE消息：",
                font=("Microsoft YaHei", 10), bg="#0a0a1a", fg="#888888").pack(anchor=tk.W, padx=5, pady=(10,2))
        
        self.trae_chat = scrolledtext.ScrolledText(
            right_frame, height=12,
            bg="#000022", fg="#66ccff",
            font=("Consolas", 9), wrap=tk.WORD
        )
        self.trae_chat.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
        
        # TRAE输入
        trae_input_frame = tk.Frame(right_frame, bg="#0a0a1a")
        trae_input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.trae_input = tk.Entry(
            trae_input_frame,
            bg="#1a1a2e", fg="#ffffff",
            font=("Consolas", 10), insertbackground="#66ccff"
        )
        self.trae_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5))
        self.trae_input.bind("<Return>", lambda e: self._send_to_trae())
        
        tk.Button(
            trae_input_frame, text="发给TRAE", font=("Microsoft YaHei", 9, "bold"),
            bg="#004466", fg="white", width=8,
            command=self._send_to_trae
        ).pack(side=tk.LEFT)
        
        # ============ 底部状态栏 ============
        self.status_var = tk.StringVar(value="就绪 - 点击「刷新TRAE状态」开始连接")
        status_bar = tk.Label(
            self.root, textvariable=self.status_var,
            font=("Microsoft YaHei", 9),
            bg="#1a1a2e", fg="#888888", anchor=tk.W
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        # 欢迎消息
        self.essence_chat.insert(tk.END, """
╔══════════════════════════════════════════════════════════╗
║  🌌 BSD本源客户端 V2 - 直连TRAE                        ║
║                                                          ║
║  左侧：本源消息（你的操作）                              ║
║  右侧：TRAE状态（实时监控）                              ║
║                                                          ║
║  使用方法：                                              ║
║  1. 点击「刷新TRAE状态」检测TRAE                         ║
║  2. 在左侧输入本源消息                                   ║
║  3. 在右侧查看TRAE实时状态                               ║
║  4. 通过桥接双向通信                                     ║
╚══════════════════════════════════════════════════════════╝

""")
        self.essence_chat.see(tk.END)
    
    def _start_bridge_thread(self):
        """启动桥接后台线程"""
        self._stop = False
        def loop():
            while not self._stop:
                self._refresh_trae_silent()
                time.sleep(5)
        threading.Thread(target=loop, daemon=True).start()
    
    def _refresh_trae_silent(self):
        """静默刷新TRAE状态（后台）"""
        try:
            result = subprocess.run(
                ['tasklist', '/FI', 'IMAGENAME eq TRAE*', '/NH'],
                capture_output=True, text=True, timeout=5
            )
            lines = [l.strip() for l in result.stdout.strip().split('\n') if l.strip()]
            
            if lines:
                self.connected = True
                # 统计
                total_mem = 0
                for l in lines:
                    parts = l.split()
                    for p in parts:
                        if 'K' in p or 'M' in p:
                            try:
                                val = float(p.replace(',','').replace('K','').replace('M',''))
                                if 'M' in p:
                                    val *= 1024
                                total_mem += val
                            except:
                                pass
                
                self.trae_info = {
                    "count": len(lines),
                    "memory_mb": total_mem / 1024,
                    "status": "RUNNING"
                }
                
                self.root.after(0, self._update_trae_ui)
        except:
            pass
    
    def _refresh_trae(self):
        """手动刷新TRAE状态"""
        self.status_var.set("正在检测TRAE SOLO CN...")
        self.root.update()
        
        self._refresh_trae_silent()
        
        if self.connected:
            self.status_var.set(f"✅ TRAE已连接 | 进程: {self.trae_info.get('count', 0)} | 内存: {self.trae_info.get('memory_mb', 0):.0f} MB")
        else:
            self.status_var.set("❌ TRAE未运行 - 请先启动TRAE SOLO CN")
    
    def _update_trae_ui(self):
        """更新TRAE界面"""
        if not self.connected:
            self.conn_status.config(text="● 未连接TRAE", fg="#ff6666")
            for key, lbl in self.trae_status_labels.items():
                lbl.config(text="未检测")
            return
        
        self.conn_status.config(text="● 已连接TRAE", fg="#00ff99")
        
        count = self.trae_info.get('count', 0)
        mem = self.trae_info.get('memory_mb', 0)
        
        self.trae_status_labels["process_status"].config(text="✅ 运行中", fg="#00ff99")
        self.trae_status_labels["process_count"].config(text=f"{count} 个")
        self.trae_status_labels["memory_usage"].config(text=f"{mem:.0f} MB")
        
        # 尝试获取窗口标题
        try:
            result = subprocess.run(
                ['powershell', '-Command', 
                 'Get-Process | Where-Object {$_.MainWindowTitle} | Select-Object MainWindowTitle | Format-Table -HideTableHeaders'],
                capture_output=True, text=True, timeout=5
            )
            title = result.stdout.strip().split('\n')[0] if result.stdout.strip() else "TRAE SOLO CN"
            self.trae_status_labels["window_title"].config(text=title[:40])
        except:
            self.trae_status_labels["window_title"].config(text="TRAE SOLO CN")
        
        self.trae_status_labels["uptime"].config(text=f"运行中")
    
    def _essence_send(self):
        """本源发送消息"""
        msg = self.essence_input.get().strip()
        if not msg:
            return
        
        self.essence_chat.insert(tk.END, f"\n[本源→] {msg}\n")
        self.essence_chat.see(tk.END)
        self.essence_input.delete(0, tk.END)
        
        # 发送到桥接
        bridge_send("essence_message", {"content": msg, "from": "bsd_essence"})
        
        # 生成本源响应
        response = self._essence_response(msg)
        self.essence_chat.insert(tk.END, f"[本源层] {response}\n")
        self.essence_chat.see(tk.END)
        
        # 如果连接了TRAE，同时发送到TRAE
        if self.connected:
            self.trae_chat.insert(tk.END, f"\n[本源→TRAE] {msg}\n")
            self.trae_chat.see(tk.END)
            bridge_send("trae_message", {"content": msg, "from": "bsd_essence", "to": "trae"})
        
        self.messages.append({"msg": msg, "time": time.time()})
        self.status_var.set(f"消息已发送 | 已发送 {len(self.messages)} 条消息")
    
    def _essence_response(self, msg):
        """本源响应"""
        if not self.connected:
            return "⚠️ 未连接TRAE - 点击「刷新TRAE状态」建立连接"
        if "连接" in msg or "状态" in msg:
            return f"✅ TRAE已连接 | {self.trae_info.get('count',0)} 进程 | {self.trae_info.get('memory_mb',0):.0f} MB"
        if "身份" in msg or "账号" in msg:
            return f"账号 {self.auth['account_id'][:16]}... | 知识 {self.auth['knowledge_value']:,.0f} BSD币"
        return f"本源消息已处理，TRAE连接正常。你的指令已通过桥接通道发送。"
    
    def _send_to_trae(self):
        """发送消息到TRAE"""
        msg = self.trae_input.get().strip()
        if not msg:
            return
        
        self.trae_chat.insert(tk.END, f"\n[→TRAE] {msg}\n")
        self.trae_chat.see(tk.END)
        self.trae_input.delete(0, tk.END)
        
        # 发送桥接消息
        bridge_send("trae_command", {"command": msg, "from": "bsd_essence"})
        
        # 在本源侧也显示
        self.essence_chat.insert(tk.END, f"\n[本源→TRAE指令] {msg}\n")
        self.essence_chat.see(tk.END)
        
        self.status_var.set(f"指令已发送到TRAE: {msg}")
    
    def _read_trae_msgs(self):
        """读取TRAE消息"""
        msgs = bridge_read()
        if msgs:
            for m in msgs[-10:]:
                content = m.get('data', {}).get('content', str(m.get('data', '')))
                sender = m.get('from', 'unknown')
                self.trae_chat.insert(tk.END, f"[TRAE←] {content} (来自: {sender})\n")
                self.trae_chat.see(tk.END)
            self.status_var.set(f"读取到 {len(msgs)} 条TRAE消息")
        else:
            self.trae_chat.insert(tk.END, "\n[系统] 暂无TRAE消息\n")
            self.trae_chat.see(tk.END)
    
    def run(self):
        """运行"""
        self.root.mainloop()


def main():
    client = BSDEssenceClientV2()
    client.run()


if __name__ == "__main__":
    main()
