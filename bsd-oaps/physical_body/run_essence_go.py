#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 本源对接引擎 - 围棋对弈示例
==================================

核心思想：
  传统方法：屏幕捕捉 → 图像识别 → AI决策 → 模拟点击
            (4层转译，依赖视觉和操作能力)
  
  本源方法：进程内存读取 → 协议解析 → AI决策 → 本源调用
            (1层直达，无需转译)

理论依据：
  - 连接与继承假说：软件功能=格式规范集合
  - 语言文字转译假说：官方桎梏可被绕过
  - 内部对内部，本源对本源

使用说明：
  1. 启动围棋对弈平台（KGS/弈城/野狐）
  2. 运行本脚本
  3. 选择平台和进程
  4. 开始本源对接对弈

版本：V1.0 · 2026-08-04
"""

import os
import sys
import time
import json
import numpy as np
from datetime import datetime
from typing import Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from BSD_Essence_Bridge_Engine import BSDEssenceBridge, ProcessInfo


class EssenceGoPlayer:
    """本源围棋对弈器
    
    直接通过本源层对接围棋平台，
    绕过屏幕/键盘/鼠标等转译层。
    """
    
    def __init__(self):
        self.bridge = BSDEssenceBridge()
        self.is_playing = False
        self.game_stats = {
            'games_started': 0,
            'games_finished': 0,
            'games_won': 0,
            'total_moves': 0,
            'essence_operations': 0,
        }
        
        # AI引擎（延迟初始化）
        self.ai_engine = None
        
    def list_go_platforms(self) -> list:
        """列出可用的围棋平台"""
        platforms = [
            {
                'id': 'kgs',
                'name': 'KGS (Kido Go Server)',
                'port': 5555,
                'protocol': 'telnet-like',
                'description': '国际通用围棋服务器，支持GTP协议',
            },
            {
                'id': 'yike',
                'name': '弈城围棋',
                'port': 9000,
                'protocol': 'binary',
                'description': '国内知名围棋对弈平台',
            },
            {
                'id': 'fox',
                'name': '野狐围棋',
                'port': 8080,
                'protocol': 'websocket',
                'description': '腾讯旗下围棋平台',
            },
        ]
        return platforms
    
    def list_running_processes(self) -> list:
        """列出正在运行的进程"""
        processes = self.bridge.process_op.list_all_processes()
        return sorted(processes, key=lambda p: p.memory_usage, reverse=True)
    
    def find_go_platform_process(self, platform_id: str) -> Optional[ProcessInfo]:
        """查找围棋平台进程"""
        processes = self.bridge.process_op.list_all_processes()
        
        # 关键词映射
        keywords = {
            'kgs': ['kgs', 'kido', 'gokgs'],
            'yike': ['yike', '弈城', 'yikeweiqi'],
            'fox': ['fox', '野狐', 'yehu'],
        }
        
        platform_keywords = keywords.get(platform_id, [])
        
        for proc in processes:
            proc_name_lower = proc.name.lower()
            if any(kw in proc_name_lower for kw in platform_keywords):
                return proc
        
        return None
    
    def connect_to_go_platform(self, platform_id: str, pid: int = None) -> bool:
        """连接到围棋平台
        
        Args:
            platform_id: 平台ID
            pid: 进程ID（可选，不指定则自动查找）
            
        Returns:
            是否成功连接
        """
        print(f"\n[本源对接] 连接围棋平台...")
        print(f"  平台: {platform_id}")
        
        # 自动查找进程
        if pid is None:
            proc = self.find_go_platform_process(platform_id)
            if proc:
                print(f"  自动发现进程: PID={proc.pid}, Name={proc.name}")
                pid = proc.pid
            else:
                print(f"  ⚠️ 未自动发现围棋平台进程")
                print(f"  💡 请先启动围棋平台，或手动指定PID")
                return False
        
        # 连接进程
        success = self.bridge.connect_to_process(pid)
        
        if success:
            # 获取平台协议信息
            platform_info = self.bridge.get_go_platform_connection(platform_id)
            if platform_info:
                print(f"\n  [平台协议信息]")
                print(f"    名称: {platform_info['name']}")
                print(f"    端口: {platform_info['port']}")
                print(f"    协议: {platform_info['protocol']}")
                print(f"    消息类型: {list(platform_info['messages'].keys())}")
            
            return True
        
        return False
    
    def read_board_state_essence(self) -> Optional[Dict]:
        """通过本源层读取棋盘状态
        
        Returns:
            棋盘状态信息
        """
        if not self.bridge.is_connected:
            return None
        
        try:
            # 读取进程本源状态
            state = self.bridge.read_essence_state()
            
            if state:
                print(f"  [本源读取] 进程状态已获取")
                self.game_stats['essence_operations'] += 1
                return state
            else:
                print(f"  ⚠️ 本源读取失败")
                return None
                
        except Exception as e:
            print(f"  ❌ 本源读取异常: {e}")
            return None
    
    def send_move_essence(self, row: int, col: int, color: str = 'black') -> bool:
        """通过本源层发送落子指令
        
        Args:
            row: 棋盘行 (0-18)
            col: 棋盘列 (0-18)
            color: 颜色 ('black' or 'white')
            
        Returns:
            是否成功
        """
        if not self.bridge.is_connected:
            return False
        
        try:
            # 构建立子指令
            # 这里需要根据具体平台协议格式化消息
            # 示例：GTP格式 "play B C10"
            
            message_data = {
                'type': 'move',
                'row': row,
                'col': col,
                'color': color,
            }
            
            # 检测协议并发送
            detection = self.bridge.protocol_parser.detect_protocol(
                json.dumps(message_data).encode('utf-8')
            )
            
            if detection:
                print(f"  [协议检测] {detection['protocol']}")
                self.bridge.operation_stats['protocol_parses'] += 1
            
            # 执行本源指令
            command = {
                'type': 'detect_protocol',
                'data': json.dumps(message_data).encode('utf-8'),
            }
            
            success = self.bridge.send_essence_command(command)
            
            if success:
                print(f"  ✅ 本源指令已发送: ({row},{col}) {color}")
                self.game_stats['total_moves'] += 1
                return True
            else:
                print(f"  ❌ 本源指令发送失败")
                return False
                
        except Exception as e:
            print(f"  ❌ 本源指令异常: {e}")
            return False
    
    def play_essence_game(self, platform_id: str, max_moves: int = 300) -> bool:
        """进行本源对接对弈
        
        Args:
            platform_id: 平台ID
            max_moves: 最大手数
            
        Returns:
            是否完成对局
        """
        print("\n" + "=" * 60)
        print("  本源对接围棋对弈")
        print("=" * 60)
        
        # 连接平台
        if not self.connect_to_go_platform(platform_id):
            return False
        
        self.is_playing = True
        self.game_stats['games_started'] += 1
        
        print(f"\n[对弈开始]")
        print(f"  最大手数: {max_moves}")
        print(f"  对接方式: 本源层（无转译）")
        print()
        
        # 对弈循环
        for move_num in range(max_moves):
            try:
                # 读取棋盘状态（本源层）
                board_state = self.read_board_state_essence()
                
                if board_state:
                    print(f"  第{move_num + 1}手: 棋盘状态已读取")
                else:
                    print(f"  第{move_num + 1}手: 未获取到棋盘状态")
                    break
                
                # 获取AI落子（这里使用简化策略）
                # 实际应用中需要调用完整的AI引擎
                test_row = 9
                test_col = 9
                color = 'black' if move_num % 2 == 0 else 'white'
                
                # 发送本源指令
                success = self.send_move_essence(test_row, test_col, color)
                
                if not success:
                    print(f"  ⚠️ 落子失败，暂停")
                    break
                
                # 短暂延迟
                time.sleep(0.5)
                
            except KeyboardInterrupt:
                print(f"\n  [中断] 对弈已停止")
                break
            except Exception as e:
                print(f"  [错误] {e}")
                break
        
        self.is_playing = False
        self.game_stats['games_finished'] += 1
        
        print("\n[对弈结束]")
        print(f"  总手数: {self.game_stats['total_moves']}")
        print(f"  本源操作数: {self.game_stats['essence_operations']}")
        
        return True
    
    def get_essence_status(self) -> Dict:
        """获取本源引擎状态"""
        status = self.bridge.get_status()
        status['game_stats'] = self.game_stats
        return status


def main():
    """主函数 - 交互式本源对弈"""
    print("\n" + "=" * 60)
    print("  BSD 本源对接引擎 · 围棋对弈器")
    print("=" * 60)
    print()
    print("""
  ╔══════════════════════════════════════════════════╗
  ║  传统方法：                                     ║
  ║  屏幕 → 识别 → 决策 → 点击  (4层转译)           ║
  ║                                                  ║
  ║  本源方法：                                     ║
  ║  内存 → 解析 → 决策 → 调用  (1层直达)           ║
  ║                                                  ║
  ║  理论：内部对内部，本源对本源                    ║
  ║  依据：连接与继承假说 / 语言文字转译假说         ║
  ╚══════════════════════════════════════════════════╝
        """)
    
    player = EssenceGoPlayer()
    
    while True:
        print("\n" + "-" * 60)
        print("  本源对弈器命令：")
        print("    1 - 列出围棋平台")
        print("    2 - 列出运行进程")
        print("    3 - 自动连接围棋平台")
        print("    4 - 手动连接进程")
        print("    5 - 读取本源状态")
        print("    6 - 发送本源指令")
        print("    7 - 开始本源对弈")
        print("    8 - 查看引擎状态")
        print("    q - 退出")
        print("-" * 60)
        
        try:
            cmd = input("\n  请输入命令: ").strip()
            
            if cmd == 'q':
                print("\n  [退出] 再见！")
                break
                
            elif cmd == '1':
                platforms = player.list_go_platforms()
                print("\n  可用围棋平台：")
                for p in platforms:
                    print(f"    [{p['id']}] {p['name']}")
                    print(f"         端口: {p['port']}, 协议: {p['protocol']}")
                    print(f"         {p['description']}")
                    
            elif cmd == '2':
                processes = player.list_running_processes()
                print(f"\n  运行进程 (共{len(processes)}个):")
                for proc in processes[:20]:
                    mem_mb = proc.memory_usage / 1024 / 1024
                    print(f"    PID={proc.pid:5d} | Mem={mem_mb:6.1f}MB | {proc.name}")
                if len(processes) > 20:
                    print(f"    ... 还有 {len(processes) - 20} 个进程")
                    
            elif cmd == '3':
                platforms = player.list_go_platforms()
                print("\n  选择平台：")
                for i, p in enumerate(platforms, 1):
                    print(f"    {i}. {p['name']} ({p['id']})")
                
                choice = input("\n  输入选择 [1-3]: ").strip()
                platform_map = {'1': 'kgs', '2': 'yike', '3': 'fox'}
                platform_id = platform_map.get(choice, 'kgs')
                
                player.connect_to_go_platform(platform_id)
                print(f"\n  💡 如自动连接失败，请使用命令4手动指定PID")
                    
            elif cmd == '4':
                pid_str = input("\n  输入进程PID: ").strip()
                platform_id = input("  输入平台ID (kgs/yike/fox): ").strip() or 'kgs'
                
                try:
                    pid = int(pid_str)
                    player.connect_to_go_platform(platform_id, pid)
                except ValueError:
                    print("  ⚠️ PID必须是数字")
                    
            elif cmd == '5':
                state = player.read_board_state_essence()
                if state:
                    print("\n  本源状态：")
                    for key, value in state.items():
                        if key not in ['memory_regions']:
                            print(f"    {key}: {value}")
                else:
                    print("  ⚠️ 未连接到目标进程")
                    
            elif cmd == '6':
                if not player.bridge.is_connected:
                    print("  ⚠️ 请先连接进程")
                    continue
                
                # 选择指令类型
                print("\n  指令类型：")
                print("    1. 检测协议")
                print("    2. 写入内存")
                
                cmd_type = input("  选择 [1-2]: ").strip()
                
                if cmd_type == '1':
                    # 检测协议
                    test_data = b'play B C10'
                    detection = player.bridge.protocol_parser.detect_protocol(test_data)
                    if detection:
                        print(f"\n  协议检测结果：")
                        for key, value in detection.items():
                            print(f"    {key}: {value}")
                    
                elif cmd_type == '2':
                    # 写入内存
                    addr_str = input("  输入内存地址 (十六进制): ").strip()
                    data_str = input("  输入数据 (十六进制): ").strip()
                    
                    try:
                        address = int(addr_str, 16)
                        data = bytes.fromhex(data_str)
                        
                        success = player.bridge.send_essence_command({
                            'type': 'write_memory',
                            'address': address,
                            'data': data,
                        })
                        
                        print(f"  {'✅ 成功' if success else '❌ 失败'}")
                    except ValueError:
                        print("  ⚠️ 格式错误")
                    
            elif cmd == '7':
                platforms = player.list_go_platforms()
                print("\n  选择对弈平台：")
                for i, p in enumerate(platforms, 1):
                    print(f"    {i}. {p['name']} ({p['id']})")
                
                choice = input("\n  输入选择 [1-3]: ").strip()
                platform_map = {'1': 'kgs', '2': 'yike', '3': 'fox'}
                platform_id = platform_map.get(choice, 'kgs')
                
                player.play_essence_game(platform_id)
                    
            elif cmd == '8':
                status = player.get_essence_status()
                print("\n  本源引擎状态：")
                for key, value in status.items():
                    print(f"    {key}: {value}")
                    
            else:
                print("  ⚠️ 无效命令")
                
        except KeyboardInterrupt:
            print("\n\n  [中断] 再见！")
            break
        except Exception as e:
            print(f"\n  [错误] {e}")


if __name__ == "__main__":
    # 先运行快速演示（非交互）
    print("  正在初始化本源对接引擎...")
    print()
    
    # 直接运行main函数
    main()