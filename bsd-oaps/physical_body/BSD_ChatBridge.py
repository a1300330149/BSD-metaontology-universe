"""
BSD双端对话 - Socket通信核心
=============================
两个独立exe之间的实时通信
"""

import socket
import threading
import json
import time
import hashlib
from typing import Callable, Dict, Optional


# 共享端口池（避免冲突 - 使用高位端口）
PORTS = {"trae": 15555, "essence": 15556}


class ChatBridge:
    """双端通信桥接 - Socket实现"""
    
    def __init__(self, role: str, on_message: Callable = None):
        self.role = role  # "trae" or "essence"
        self.port = PORTS[role]
        self.peer_port = PORTS["trae" if role == "essence" else "essence"]
        self.on_message = on_message
        
        self.server_socket = None
        self.client_socket = None
        self.running = False
        self.messages = []
        
        # 身份信息
        if role == "trae":
            self.identity = {
                "name": "TRAE SOLO CN",
                "type": "traditional",
                "auth": "官方Token",
                "color": "#3B82F6"
            }
        else:
            self.identity = {
                "name": "BSD本源客户端",
                "type": "essence",
                "auth": "知识凭证 (2,316,876 BSD币)",
                "color": "#10B981"
            }
    
    def start_server(self):
        """启动服务器（接收端）"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('127.0.0.1', self.port))
        self.server_socket.listen(1)
        self.server_socket.settimeout(1.0)
        self.running = True
        
        # 接收线程
        thread = threading.Thread(target=self._accept_loop, daemon=True)
        thread.start()
    
    def _accept_loop(self):
        """接受连接"""
        while self.running:
            try:
                conn, addr = self.server_socket.accept()
                self.client_socket = conn
                # 接收线程
                thread = threading.Thread(target=self._recv_loop, args=(conn,), daemon=True)
                thread.start()
            except socket.timeout:
                continue
            except:
                break
    
    def _recv_loop(self, conn):
        """接收消息"""
        conn.settimeout(1.0)
        while self.running:
            try:
                data = conn.recv(4096)
                if not data:
                    break
                msg = json.loads(data.decode('utf-8'))
                self.messages.append(msg)
                if self.on_message:
                    self.on_message(msg)
            except socket.timeout:
                continue
            except:
                break
    
    def connect(self):
        """连接到对方"""
        for _ in range(20):  # 重试
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect(('127.0.0.1', self.peer_port))
                return True
            except:
                time.sleep(0.3)
        return False
    
    def send(self, content: str, msg_type: str = "chat"):
        """发送消息"""
        msg = {
            "type": msg_type,
            "from": self.role,
            "from_name": self.identity["name"],
            "content": content,
            "time": time.time()
        }
        if self.client_socket:
            try:
                self.client_socket.send(json.dumps(msg, ensure_ascii=False).encode('utf-8'))
            except:
                pass
        self.messages.append(msg)
    
    def stop(self):
        """停止"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        if self.client_socket:
            self.client_socket.close()
