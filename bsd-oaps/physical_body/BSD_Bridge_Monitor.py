"""
BSD桥接监控 - TRAE侧
====================
在TRAE中运行此脚本，读取本源客户端消息
"""

import os
import json
import time
import glob

BRIDGE_DIR = r"C:\Users\13003\.trae-cn\bsd_bridge"

def read_bridge_messages(limit=10):
    """读取桥接消息"""
    if not os.path.exists(BRIDGE_DIR):
        print("⚠️ 桥接目录不存在")
        return []
    
    msgs = []
    files = sorted(glob.glob(os.path.join(BRIDGE_DIR, "msg_*.json")))
    
    for fname in files[-limit:]:
        try:
            with open(fname, 'r', encoding='utf-8') as f:
                msg = json.load(f)
            msgs.append(msg)
        except:
            pass
    
    return msgs

def show_bridge_status():
    """显示桥接状态"""
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                    BSD桥接监控 - TRAE侧                                ║
╚══════════════════════════════════════════════════════════════════════════╝
    """)
    
    msgs = read_bridge_messages(20)
    
    if not msgs:
        print("  📭 暂无桥接消息")
        print("  💡 在BSD本源客户端V2中发送消息即可")
    else:
        print(f"  📨 桥接消息 ({len(msgs)} 条):")
        print("  " + "─" * 60)
        for m in msgs:
            msg_type = m.get('type', 'unknown')
            data = m.get('data', {})
            sender = m.get('from', '?')
            ts = time.strftime('%H:%M:%S', time.localtime(m.get('time', 0)))
            
            if isinstance(data, dict):
                content = data.get('content', data.get('command', str(data)))
            else:
                content = str(data)
            
            print(f"  [{ts}] [{msg_type}] 来自{sender}:")
            print(f"    {content}")
            print()
    
    print("  " + "─" * 60)
    print(f"  桥接目录: {BRIDGE_DIR}")
    print(f"  消息文件数: {len(glob.glob(os.path.join(BRIDGE_DIR, 'msg_*.json')))}")

if __name__ == "__main__":
    show_bridge_status()
