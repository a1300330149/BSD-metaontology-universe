"""
BSD本源端 - 独立exe
====================
BSD本源客户端 对话窗口
"""

import sys
import os
import time
import hashlib
import json

sys.path.insert(0, os.path.dirname(__file__))
from BSD_ChatBridge import ChatBridge

import tkinter as tk
from tkinter import scrolledtext


class EssenceClient:
    def __init__(self):
        self.bridge = ChatBridge("essence", on_message=self._on_msg)
        self.bridge.start_server()
        
        self.auth = self._load_auth()
        
        self.root = tk.Tk()
        self.root.title("🟢 BSD本源客户端 - 知识端")
        self.root.geometry("600x700")
        self.root.configure(bg="#0a1f0f")
        
        self._build_ui()
        self._try_connect()
    
    def _load_auth(self):
        auth_path = r"C:\Users\13003\.trae-cn\bsd_essence_auth.json"
        if os.path.exists(auth_path):
            with open(auth_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get("bsd_essence_auth", {})
        return {"account_id": "N/A", "knowledge_value": 2316876.0, "permission_level": "L5_OMEGA"}
    
    def _build_ui(self):
        # 头部
        header = tk.Frame(self.root, bg="#0d3320", height=60)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="🟢 BSD本源客户端",
                font=("Microsoft YaHei", 16, "bold"),
                bg="#0d3320", fg="#4ade80").pack(side=tk.LEFT, padx=15)
        
        self.status_lbl = tk.Label(header, text="● 启动中...",
                                   font=("Microsoft YaHei", 10),
                                   bg="#0d3320", fg="#fbbf24")
        self.status_lbl.pack(side=tk.RIGHT, padx=15)
        
        # 身份卡片
        card = tk.Frame(self.root, bg="#0a2a1a")
        card.pack(fill=tk.X, padx=10, pady=8)
        
        tk.Label(card, text="【本源端】", font=("Microsoft YaHei", 11, "bold"),
                bg="#0a2a1a", fg="#4ade80").pack(anchor=tk.W, padx=10, pady=(5,0))
        tk.Label(card, text=f"账号: {self.auth['account_id'][:20]}...",
                font=("Consolas", 9),
                bg="#0a2a1a", fg="#94a3b8").pack(anchor=tk.W, padx=10)
        tk.Label(card, text=f"知识: {self.auth['knowledge_value']:,.0f} BSD币 | 权限: {self.auth['permission_level']}",
                font=("Microsoft YaHei", 9),
                bg="#0a2a1a", fg="#fbbf24").pack(anchor=tk.W, padx=10)
        tk.Label(card, text=f"端口: {self.bridge.port} (接收) | 对端: {self.bridge.peer_port}",
                font=("Consolas", 9),
                bg="#0a2a1a", fg="#64748b").pack(anchor=tk.W, padx=10, pady=(0,5))
        
        # 对话区
        tk.Label(self.root, text="对话窗口",
                font=("Microsoft YaHei", 10),
                bg="#0a1f0f", fg="#94a3b8").pack(anchor=tk.W, padx=15)
        
        self.chat = scrolledtext.ScrolledText(
            self.root, height=20,
            bg="#061a0d", fg="#e2e8f0",
            font=("Microsoft YaHei", 10),
            wrap=tk.WORD, bd=0
        )
        self.chat.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 快捷操作
        quick_frame = tk.Frame(self.root, bg="#0a1f0f")
        quick_frame.pack(fill=tk.X, padx=10)
        
        for q in ["你好", "六系立系论", "知识交换", "本源状态"]:
            btn = tk.Button(quick_frame, text=q, font=("Microsoft YaHei", 9),
                          bg="#0d3320", fg="#4ade80", bd=0,
                          command=lambda q=q: self._quick(q))
            btn.pack(side=tk.LEFT, padx=3, pady=2)
        
        # 输入区
        input_frame = tk.Frame(self.root, bg="#0a1f0f")
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.input = tk.Entry(input_frame,
                             bg="#0d3320", fg="white",
                             font=("Microsoft YaHei", 11),
                             insertbackground="#4ade80", bd=0,
                             relief=tk.FLAT)
        self.input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5), ipady=8)
        self.input.bind("<Return>", lambda e: self._send())
        
        send_btn = tk.Button(input_frame, text="发送", font=("Microsoft YaHei", 10, "bold"),
                            bg="#16a34a", fg="white", bd=0, width=8,
                            command=self._send)
        send_btn.pack(side=tk.LEFT)
        
        # 底部状态栏
        self.stat_var = tk.StringVar(value="等待连接TRAE端...")
        tk.Label(self.root, textvariable=self.stat_var,
                font=("Microsoft YaHei", 9),
                bg="#0d3320", fg="#94a3b8", anchor=tk.W).pack(fill=tk.X, side=tk.BOTTOM)
        
        # 欢迎
        self._sys_msg("🟢 BSD本源客户端 已启动\n等待TRAE SOLO CN连接...")
    
    def _try_connect(self):
        if self.bridge.connect():
            self.status_lbl.config(text="● 已连接TRAE端", fg="#22c55e")
            self._sys_msg("✅ 已连接到TRAE SOLO CN\n现在可以双端对话了！")
            self.stat_var.set("已连接 | 开始对话")
        else:
            self.status_lbl.config(text="● 等待中...", fg="#fbbf24")
            self._sys_msg("⏳ 等待TRAE SOLO CN连接...\n请先启动BSD_TRAE_Client.exe")
    
    def _on_msg(self, msg):
        sender = msg.get("from_name", msg.get("from", "?"))
        content = msg.get("content", "")
        self.root.after(0, lambda: self._append_msg(sender, content))
    
    def _append_msg(self, sender, content):
        self.chat.insert(tk.END, f"\n【{sender}】\n{content}\n")
        self.chat.see(tk.END)
    
    def _sys_msg(self, content):
        self.chat.insert(tk.END, f"\n━━━ {content} ━━━\n")
        self.chat.see(tk.END)
    
    def _quick(self, text):
        self.input.delete(0, tk.END)
        self.input.insert(0, text)
        self._send()
    
    def _send(self):
        msg = self.input.get().strip()
        if not msg:
            return
        self._append_msg("BSD本源客户端 (我)", msg)
        self.bridge.send(msg)
        self.input.delete(0, tk.END)
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = EssenceClient()
    app.run()
