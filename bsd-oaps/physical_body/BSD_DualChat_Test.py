"""
双端对话快速测试 - 验证Socket通信
"""
import sys
import os
import time
import threading

sys.path.insert(0, os.path.dirname(__file__))
from BSD_ChatBridge import ChatBridge

print("=" * 60)
print("  BSD双端对话 - Socket通信测试")
print("=" * 60)

# TRAE端
trae = ChatBridge("trae")
trae.start_server()
print(f"  TRAE端已启动: 端口 {trae.port}")

# 本源端
essence = ChatBridge("essence")
essence.start_server()
print(f"  本源端已启动: 端口 {essence.port}")

# 等待服务器就绪
time.sleep(0.5)

# 双向连接
print("\n[双向连接]")
t1 = essence.connect()
print(f"  本源→TRAE: {'✅' if t1 else '❌'}")

t2 = trae.connect()
print(f"  TRAE→本源: {'✅' if t2 else '❌'}")

# 测试对话
print("\n[对话测试]")

# 本源→TRAE
essence.send("你好，TRAE！我是BSD本源客户端。", "greeting")
time.sleep(0.3)

# TRAE→本源
trae.send("你好！TRAE SOLO CN已收到消息。", "greeting")
time.sleep(0.3)

# 本源→TRAE
essence.send("双端对话已建立。知识凭证: 2,316,876 BSD币。", "chat")
time.sleep(0.3)

# 检查消息
print("\n[消息检查]")
print(f"  TRAE端收到: {len([m for m in trae.messages if m.get('type') == 'chat' or m.get('type') == 'greeting'])} 条消息")
print(f"  本源端收到: {len([m for m in essence.messages if m.get('type') == 'chat' or m.get('type') == 'greeting'])} 条消息")

# 显示TRAE收到的消息
print("\n  TRAE端消息:")
for m in trae.messages:
    if m.get('type') in ('chat', 'greeting'):
        print(f"    [{m.get('type')}] {m.get('from_name', m.get('from'))}: {m.get('content')}")

# 显示本源收到的消息
print("\n  本源端消息:")
for m in essence.messages:
    if m.get('type') in ('chat', 'greeting'):
        print(f"    [{m.get('type')}] {m.get('from_name', m.get('from'))}: {m.get('content')}")

# 清理
trae.stop()
essence.stop()

print("\n" + "=" * 60)
if t1 and t2 and len(trae.messages) >= 2 and len(essence.messages) >= 1:
    print("  ✅ 双端对话测试通过！")
else:
    print("  ❌ 测试未通过")
print("=" * 60)
