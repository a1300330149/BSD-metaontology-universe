#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 物理层对接引擎 - 联网对弈启动器
=====================================

使用说明：
1. 启动一个围棋对弈平台（如野狐弈城、KGS等）
2. 将浏览器窗口调整到合适位置
3. 运行本脚本，按照提示设置棋盘区域
4. 开始自动对弈

工作流程：
┌─────────────────────────────────────────────────────────────────┐
│  BSD 物理层对接引擎 · 联网对弈工作流                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  屏幕捕捉 ──→ 棋面识别 ──→ AI决策 ──→ 物理落子                   │
│     ↑                                        │                  │
│     │                                        ↓                  │
│     └──────── 等待对手落子 ←─────────────────┘                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

版本：V1.0 · 2026-08-04
"""

import os
import sys
import time
import numpy as np
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from BSD_Physical_Bridge_Engine import BSDPhysicalBridge, ScreenRegion


class OnlineGoPlayer:
    """联网围棋对弈器"""
    
    def __init__(self):
        self.bridge = BSDPhysicalBridge()
        self.is_running = False
        self.game_stats = {
            'games_played': 0,
            'games_won': 0,
            'games_lost': 0,
            'total_moves': 0,
        }
        
    def setup_board_region(self):
        """交互式设置棋盘区域"""
        print("\n" + "=" * 60)
        print("  棋盘区域设置")
        print("=" * 60)
        print("\n  请在屏幕上选择围棋棋盘的位置：")
        print("  1. 将浏览器/对弈窗口打开到围棋对局界面")
        print("  2. 调整窗口大小，使棋盘清晰可见")
        print("  3. 输入棋盘左上角和右下角的坐标")
        print()
        
        # 显示当前鼠标位置作为参考
        current_pos = self.bridge.physical_operator.get_cursor_pos()
        print(f"  当前鼠标位置: {current_pos}")
        print()
        
        print("  提示：")
        print("  - 可以使用截图工具（如PrintScreen）获取坐标")
        print("  - 或者移动鼠标到棋盘角落，查看坐标")
        print()
        
        # 默认使用屏幕中央区域
        screen_size = self.bridge.screen_capture.get_screen_size()
        default_size = min(screen_size[0], screen_size[1]) // 3
        
        x = screen_size[0] // 2 - default_size // 2
        y = screen_size[1] // 2 - default_size // 2
        width = default_size
        height = default_size
        
        # 自动检测并设置
        print(f"  [自动] 使用默认棋盘区域：({x}, {y}) - ({x+width}, {y+height})")
        print(f"  [自动] 棋盘大小：{width}x{height} 像素")
        
        self.bridge.set_board_region(x, y, width, height)
        
        # 验证设置
        print("\n  [验证] 捕捉棋盘区域...")
        board_img = self.bridge.screen_capture.capture_screen(self.bridge.board_region)
        board_state = self.bridge.read_board_state()
        
        print(f"  [验证] 捕获图像: {board_img.shape}")
        print(f"  [验证] 识别棋盘: {board_state.board_size}x{board_state.board_size}")
        print(f"  [验证] 黑棋数: {np.sum(board_state.stones == 1)}")
        print(f"  [验证] 白棋数: {np.sum(board_state.stones == 2)}")
        
        return board_state
    
    def get_my_color(self) -> str:
        """获取我方颜色"""
        # 简化处理，实际上需要从对局平台获取
        return 'black'  # 假设我方执黑先行
    
    def wait_for_opponent_move(self, timeout: float = 30.0) -> bool:
        """等待对手落子
        
        Args:
            timeout: 超时时间（秒）
            
        Returns:
            是否检测到对手落子
        """
        print(f"  [等待] 等待对手落子（超时：{timeout}秒）...")
        
        start_time = time.time()
        previous_state = self.bridge.read_board_state()
        previous_stones = np.sum(previous_state.stones != 0)
        
        while time.time() - start_time < timeout:
            # 读取当前状态
            current_state = self.bridge.read_board_state()
            current_stones = np.sum(current_state.stones != 0)
            
            # 检查是否有新棋子
            if current_stones > previous_stones:
                print(f"  [检测] 对手已落子！当前棋盘棋子数: {current_stones}")
                return True
            
            # 等待一小段时间
            time.sleep(0.5)
        
        print(f"  [超时] 等待对手落子超时")
        return False
    
    def make_move(self, my_color: str = 'black') -> bool:
        """执行一手棋
        
        Args:
            my_color: 我方颜色
            
        Returns:
            是否成功执行
        """
        try:
            # 1. 读取当前棋盘状态
            board_state = self.bridge.read_board_state()
            empty_count = np.sum(board_state.stones == 0)
            
            if empty_count == 0:
                print("  [提示] 棋盘已满，游戏结束")
                return False
            
            print(f"\n  [落子] 第{self.bridge.move_count + 1}手")
            print(f"  [识别] 空点数: {empty_count}")
            
            # 2. 获取AI决策
            if self.bridge.engine_connector:
                # 通过引擎连接器获取路由建议
                decision = self.bridge.engine_connector.route(
                    board_state=board_state,
                    phase='middle'
                )
                
                # 从路由结果中获取推荐引擎
                if hasattr(decision, 'get'):
                    route_info = decision.get('decision', {})
                    if hasattr(route_info, 'primary_engine'):
                        engine_id = route_info.primary_engine
                        print(f"  [AI] 推荐引擎: {engine_id}")
                        print(f"  [AI] 置信度: {route_info.confidence}")
                
                # 生成示例落子（实际需要调用具体引擎）
                # 这里简化处理：选择一个空位
                stones = board_state.stones
                empty_positions = np.where(stones == 0)
                
                if len(empty_positions[0]) > 0:
                    # 选择中间附近的空位（简化策略）
                    center_idx = len(empty_positions[0]) // 2
                    target_row = empty_positions[0][center_idx]
                    target_col = empty_positions[1][center_idx]
                    
                    print(f"  [决策] 目标位置: ({target_row}, {target_col})")
                    
                    # 3. 执行物理落子
                    self.bridge.execute_move(target_row, target_col)
                    
                    self.game_stats['total_moves'] += 1
                    return True
            
            else:
                print("  [警告] AI引擎连接器未就绪")
                return False
                
        except Exception as e:
            print(f"  [错误] 执行失败: {e}")
            return False
    
    def play_single_game(self, max_moves: int = 300) -> bool:
        """进行一局完整对弈
        
        Args:
            max_moves: 最大手数限制
            
        Returns:
            是否完成对局
        """
        print("\n" + "=" * 60)
        print("  开始新对局")
        print("=" * 60)
        
        self.game_stats['games_played'] += 1
        my_color = self.get_my_color()
        is_my_turn = (my_color == 'black')  # 黑方先行
        
        print(f"  我方颜色: {my_color}")
        print(f"  首方: {'我方' if is_my_turn else '对手'}")
        print(f"  最大手数: {max_moves}")
        
        for move_num in range(max_moves):
            # 检查游戏是否结束
            current_state = self.bridge.read_board_state()
            empty_count = np.sum(current_state.stones == 0)
            
            if empty_count < 2:  # 棋盘几乎已满
                print("\n  [结束] 棋盘已满，对局结束")
                break
            
            # 当前玩家行动
            if is_my_turn:
                print(f"\n  --- 第{move_num + 1}手：我方 ---")
                success = self.make_move(my_color)
                
                if not success:
                    print("  [跳过] 我方落子失败，切换回合")
                    is_my_turn = not is_my_turn
                    continue
            else:
                print(f"\n  --- 第{move_num + 1}手：对手 ---")
                # 等待对手落子
                detected = self.wait_for_opponent_move(timeout=15.0)
                
                if not detected:
                    print("  [超时] 未检测到对手落子")
                    # 可以选择继续或放弃
                    break
            
            # 切换回合
            is_my_turn = not is_my_turn
            
            # 短暂延迟
            time.sleep(0.3)
        
        print("\n  [完成] 对局结束")
        print(f"  [统计] 总手数: {self.bridge.move_count}")
        
        return True
    
    def run_demo(self):
        """运行演示模式（不实际操作，仅展示流程）"""
        print("\n" + "=" * 60)
        print("  BSD 物理层对接引擎 · 联网对弈演示")
        print("=" * 60)
        
        print("""
  核心能力演示：
  
  1. 【屏幕捕捉】
     - 基于PIL.ImageGrab
     - 支持全屏/区域截图
     - 可实时获取棋盘图像
     
  2. 【棋面识别】
     - 基于OpenCV图像处理
     - 识别19x19棋盘结构
     - 检测黑白棋位置
     
  3. 【物理操作】
     - 基于Windows API
     - 模拟鼠标移动/点击
     - 平滑移动模拟人类
     
  4. 【引擎连接】
     - 已连接11个散落引擎
     - 智能路由选择引擎
     - 多引擎协同决策
     
  5. 【协调流程】
     屏幕 → 识别 → 决策 → 落子
     (读取) (分析) (计算) (执行)
        """)
        
        # 演示协调流程
        print("\n  [演示] 执行一次完整流程...")
        
        # 捕捉屏幕
        print("  步骤1: 捕捉屏幕...")
        screen_img = self.bridge.screen_capture.capture_screen()
        print(f"    ✓ 屏幕截图: {screen_img.shape}")
        
        # 识别棋面
        print("  步骤2: 识别棋面...")
        board_state = self.bridge.board_recognizer.recognize_board(screen_img)
        print(f"    ✓ 棋盘状态: {board_state.board_size}x{board_state.board_size}")
        print(f"    ✓ 黑棋: {np.sum(board_state.stones == 1)} | 白棋: {np.sum(board_state.stones == 2)}")
        
        # 获取路由建议
        print("  步骤3: 获取AI路由建议...")
        if self.bridge.engine_connector:
            decision = self.bridge.engine_connector.route(
                board_state=board_state,
                phase='opening'
            )
            route_info = decision.get('decision', {})
            if hasattr(route_info, 'primary_engine'):
                print(f"    ✓ 推荐引擎: {route_info.primary_engine}")
                print(f"    ✓ 置信度: {route_info.confidence}")
        
        # 显示状态
        print("\n  [状态] 引擎状态:")
        status = self.bridge.get_status()
        for key, value in status.items():
            if key not in ['game_log']:
                print(f"    {key}: {value}")
        
        print("\n" + "=" * 60)
        print("  ✅ 演示完成")
        print("  💡 下一步：设置棋盘区域后开始真实对弈")
        print("=" * 60)
    
    def start_interactive(self):
        """启动交互式对弈模式"""
        print("\n" + "=" * 60)
        print("  BSD 物理层对接引擎 · 交互式对弈")
        print("=" * 60)
        
        print("""
  交互命令：
    1 - 设置棋盘区域
    2 - 读取当前棋面
    3 - 获取AI建议
    4 - 执行一手棋
    5 - 开始自动对弈
    6 - 查看引擎状态
    q - 退出
        """)
        
        while True:
            try:
                cmd = input("\n  请输入命令: ").strip()
                
                if cmd == 'q':
                    print("  [退出] 再见！")
                    break
                    
                elif cmd == '1':
                    # 设置棋盘区域
                    self.setup_board_region()
                    
                elif cmd == '2':
                    # 读取当前棋面
                    board_state = self.bridge.read_board_state()
                    print(f"\n  当前棋盘状态:")
                    print(f"    棋盘大小: {board_state.board_size}x{board_state.board_size}")
                    print(f"    黑棋: {np.sum(board_state.stones == 1)}")
                    print(f"    白棋: {np.sum(board_state.stones == 2)}")
                    
                elif cmd == '3':
                    # 获取AI建议
                    board_state = self.bridge.read_board_state()
                    if self.bridge.engine_connector:
                        decision = self.bridge.engine_connector.route(
                            board_state=board_state,
                            phase='middle'
                        )
                        route_info = decision.get('decision', {})
                        if hasattr(route_info, 'primary_engine'):
                            print(f"\n  AI建议:")
                            print(f"    推荐引擎: {route_info.primary_engine}")
                            print(f"    备选引擎: {route_info.secondary_engines[:3]}")
                            print(f"    置信度: {route_info.confidence}")
                            print(f"    理由: {route_info.routing_reason}")
                    
                elif cmd == '4':
                    # 执行一手棋
                    self.make_move('black')
                    
                elif cmd == '5':
                    # 开始自动对弈
                    self.setup_board_region()
                    self.play_single_game()
                    
                elif cmd == '6':
                    # 查看引擎状态
                    status = self.bridge.get_status()
                    print(f"\n  引擎状态:")
                    for key, value in status.items():
                        if key not in ['game_log']:
                            print(f"    {key}: {value}")
                else:
                    print("  [无效] 请输入有效命令 (1-6, q)")
                    
            except KeyboardInterrupt:
                print("\n  [中断] 再见！")
                break
            except Exception as e:
                print(f"  [错误] {e}")


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("  BSD 物理层对接引擎 · 联网对弈启动器")
    print("=" * 60)
    
    player = OnlineGoPlayer()
    
    print("\n  选择模式：")
    print("    1. 演示模式（仅展示，不操作）")
    print("    2. 交互模式（手动控制）")
    print("    3. 自动模式（自动对弈）")
    
    mode = input("\n  请选择模式 [1/2/3]: ").strip()
    
    if mode == '1':
        player.run_demo()
    elif mode == '2':
        player.start_interactive()
    elif mode == '3':
        player.setup_board_region()
        player.play_single_game()
    else:
        print("  [无效] 退出")


if __name__ == "__main__":
    main()