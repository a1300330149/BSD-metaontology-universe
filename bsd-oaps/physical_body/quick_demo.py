#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 物理层对接引擎 - 快速演示（无需交互）
"""

import os
import sys
import time
import numpy as np
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from BSD_Physical_Bridge_Engine import BSDPhysicalBridge, ScreenRegion


def main():
    print("=" * 60)
    print("  BSD 物理层对接引擎 · 快速演示")
    print("=" * 60)
    
    # 初始化引擎
    bridge = BSDPhysicalBridge()
    
    # 1. 屏幕捕捉
    print("\n[1] 屏幕捕捉测试")
    screen_size = bridge.screen_capture.get_screen_size()
    print(f"    屏幕尺寸: {screen_size}")
    
    screen_img = bridge.screen_capture.capture_screen()
    print(f"    截图尺寸: {screen_img.shape}")
    
    # 2. 棋面识别
    print("\n[2] 棋面识别测试")
    board_state = bridge.read_board_state()
    print(f"    棋盘大小: {board_state.board_size}x{board_state.board_size}")
    print(f"    黑棋数: {np.sum(board_state.stones == 1)}")
    print(f"    白棋数: {np.sum(board_state.stones == 2)}")
    
    # 3. 引擎连接器
    print("\n[3] 引擎连接器测试")
    if bridge.engine_connector:
        # 通过route来测试引擎连接器
        decision = bridge.engine_connector.route(
            board_state=board_state,
            phase='opening'
        )
        print(f"    开局路由已完成")
        
        decision = bridge.engine_connector.route(
            board_state=board_state,
            phase='middle'
        )
        print(f"    中盘路由已完成")
        
        decision = bridge.engine_connector.route(
            board_state=board_state,
            phase='ending'
        )
        print(f"    终盘路由已完成")
    
    # 4. 物理操作测试
    print("\n[4] 物理操作测试")
    cursor_pos = bridge.physical_operator.get_cursor_pos()
    print(f"    当前鼠标位置: {cursor_pos}")
    
    # 5. 坐标转换测试
    print("\n[5] 坐标转换测试")
    bridge.set_board_region(300, 200, 500, 500)
    
    test_positions = [(0, 0), (9, 9), (18, 18)]
    for row, col in test_positions:
        screen_coords = bridge._board_to_screen_coords(row, col)
        print(f"    棋盘({row},{col}) → 屏幕{screen_coords}")
    
    # 6. 状态报告
    print("\n[6] 引擎状态报告")
    status = bridge.get_status()
    for key, value in status.items():
        if key not in ['game_log']:
            print(f"    {key}: {value}")
    
    print("\n" + "=" * 60)
    print("  ✅ 物理层对接引擎演示完成")
    print("=" * 60)
    print("\n  使用方法：")
    print("    1. 启动围棋对弈平台（野狐、弈城等）")
    print("    2. 调整浏览器窗口位置")
    print("    3. 运行 run_online_go.py 开始对弈")
    print("=" * 60)


if __name__ == "__main__":
    main()