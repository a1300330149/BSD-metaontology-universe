"""测试KataGo引擎连接"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from katago_gtp_client import KataGoGTPClient, GTPEngineConfig

print("=" * 60)
print("测试KataGo引擎连接")
print("=" * 60)

# 配置KataGo
config = GTPEngineConfig(
    executable_path=r"c:\Users\13003\OneDrive\桌面\3333333\go_ai_tools\katago\katago.exe",
    model_path=r"c:\Users\13003\OneDrive\桌面\3333333\go_ai_tools\katago\default_model.bin.gz",
    config_path=r"c:\Users\13003\OneDrive\桌面\3333333\go_ai_tools\katago\bsd_match.cfg",
    board_size=9,
    komi=7.5,
    time_control=5  # 5秒/步
)

print(f"可执行文件: {config.executable_path}")
print(f"模型文件: {config.model_path}")
print(f"配置文件: {config.config_path}")
print()

# 创建客户端
client = KataGoGTPClient(config)

# 连接
print("连接KataGo引擎...")
success = client.connect()

if success:
    print("✓ 连接成功!")
    print()
    
    # 获取引擎信息
    print(f"引擎名称: {client.get_name()}")
    print(f"引擎版本: {client.get_version()}")
    print(f"协议版本: {client.get_protocol_version()}")
    print()
    
    # 列出支持的命令
    commands = client.list_commands()
    print(f"支持的命令 ({len(commands)}个):")
    for cmd in commands[:10]:
        print(f"  - {cmd}")
    if len(commands) > 10:
        print(f"  ... 还有{len(commands) - 10}个命令")
    print()
    
    # 设置棋盘
    client.set_board_size(9)
    client.clear_board()
    print("棋盘已设置为9路")
    print()
    
    # 测试落子
    print("测试落子...")
    move = client.generate_move("black")
    print(f"黑方落子: {move}")
    
    if move and move not in ["PASS", "resign"]:
        client.play("black", move)
        print(f"  已执行: {move}")
    
    move = client.generate_move("white")
    print(f"白方落子: {move}")
    
    if move and move not in ["PASS", "resign"]:
        client.play("white", move)
        print(f"  已执行: {move}")
    
    print()
    print("测试成功！KataGo引擎正常工作。")
    
else:
    print("✗ 连接失败!")
    print("将使用内置StrongGoAI进行测试。")

# 断开连接
client.disconnect()
print("\n已断开连接")
print("=" * 60)
