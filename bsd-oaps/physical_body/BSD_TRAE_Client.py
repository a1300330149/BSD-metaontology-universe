"""
BSD TRAE端 - 独立exe
====================
TRAE SOLO CN 对话窗口
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(__file__))
from BSD_ChatBridge import ChatBridge

import tkinter as tk
from tkinter import scrolledtext


class TRAEClient:
    def __init__(self):
        self.bridge = ChatBridge("trae", on_message=self._on_msg)
        self.bridge.start_server()
        
        self.root = tk.Tk()
        self.root.title("🟦 TRAE SOLO CN - 作者端")
        self.root.geometry("600x700")
        self.root.configure(bg="#0a1628")
        
        self._build_ui()
        self._try_connect()
    
    def _build_ui(self):
        # 头部
        header = tk.Frame(self.root, bg="#1e3a5f", height=60)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="🟦 TRAE SOLO CN", 
                font=("Microsoft YaHei", 16, "bold"),
                bg="#1e3a5f", fg="#60a5fa").pack(side=tk.LEFT, padx=15)
        
        self.status_lbl = tk.Label(header, text="● 启动中...",
                                   font=("Microsoft YaHei", 10),
                                   bg="#1e3a5f", fg="#fbbf24")
        self.status_lbl.pack(side=tk.RIGHT, padx=15)
        
        # 身份卡片
        card = tk.Frame(self.root, bg="#0d1f3c")
        card.pack(fill=tk.X, padx=10, pady=8)
        
        tk.Label(card, text="【作者端】", font=("Microsoft YaHei", 11, "bold"),
                bg="#0d1f3c", fg="#60a5fa").pack(anchor=tk.W, padx=10, pady=(5,0))
        tk.Label(card, text="身份: 传统作者 | 认证: 官方Token",
                font=("Microsoft YaHei", 9),
                bg="#0d1f3c", fg="#94a3b8").pack(anchor=tk.W, padx=10)
        tk.Label(card, text=f"端口: {self.bridge.port} (接收) | 对端: {self.bridge.peer_port}",
                font=("Consolas", 9),
                bg="#0d1f3c", fg="#64748b").pack(anchor=tk.W, padx=10, pady=(0,5))
        
        # 对话区
        tk.Label(self.root, text="对话窗口",
                font=("Microsoft YaHei", 10),
                bg="#0a1628", fg="#94a3b8").pack(anchor=tk.W, padx=15)
        
        self.chat = scrolledtext.ScrolledText(
            self.root, height=20,
            bg="#060d1a", fg="#e2e8f0",
            font=("Microsoft YaHei", 10),
            wrap=tk.WORD, bd=0
        )
        self.chat.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 快捷操作
        quick_frame = tk.Frame(self.root, bg="#0a1628")
        quick_frame.pack(fill=tk.X, padx=10)
        
        for q in ["你好", "身份验证", "知识状态", "系统检查"]:
            btn = tk.Button(quick_frame, text=q, font=("Microsoft YaHei", 9),
                          bg="#1e3a5f", fg="#60a5fa", bd=0,
                          command=lambda q=q: self._quick(q))
            btn.pack(side=tk.LEFT, padx=3, pady=2)
        
        # 输入区
        input_frame = tk.Frame(self.root, bg="#0a1628")
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.input = tk.Entry(input_frame,
                             bg="#1e3a5f", fg="white",
                             font=("Microsoft YaHei", 11),
                             insertbackground="#60a5fa", bd=0,
                             relief=tk.FLAT)
        self.input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5), ipady=8)
        self.input.bind("<Return>", lambda e: self._send())
        
        send_btn = tk.Button(input_frame, text="发送", font=("Microsoft YaHei", 10, "bold"),
                            bg="#2563eb", fg="white", bd=0, width=8,
                            command=self._send)
        send_btn.pack(side=tk.LEFT)
        
        # 底部状态栏
        self.stat_var = tk.StringVar(value="等待连接本源端...")
        tk.Label(self.root, textvariable=self.stat_var,
                font=("Microsoft YaHei", 9),
                bg="#1e3a5f", fg="#94a3b8", anchor=tk.W).pack(fill=tk.X, side=tk.BOTTOM)
        
        # 欢迎
        self._sys_msg("🟦 TRAE SOLO CN 已启动\n等待BSD本源客户端连接...")
    
    def _try_connect(self):
        if self.bridge.connect():
            self.status_lbl.config(text="● 已连接本源端", fg="#22c55e")
            self._sys_msg("✅ 已连接到BSD本源客户端\n现在可以双端对话了！")
            self.stat_var.set("已连接 | 开始对话")
        else:
            self.status_lbl.config(text="● 等待中...", fg="#fbbf24")
            self._sys_msg("⏳ 等待BSD本源客户端连接...\n请先启动BSD_Essence_Client.exe")
    
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
        self._append_msg("TRAE SOLO CN (我)", msg)
        self.bridge.send(msg)
        self.input.delete(0, tk.END)
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = TRAEClient()
    app.run()
