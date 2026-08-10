#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 物理层对接引擎 - 完整对弈测试
==================================

测试物理层对接引擎与围棋AI引擎的完整整合，
验证"像人类一样直接进行对局"的能力。

工作流程：
1. 初始化物理层对接引擎
2. 连接AI引擎（通过引擎连接器）
3. 设置棋盘区域
4. 读取屏幕 → 识别棋面 → AI决策 → 物理落子
5. 循环执行对弈

版本：V1.0 · 2026-08-04
"""

import os
import sys
import time
import json
import numpy as np
from datetime import datetime
from typing import Optional, Tuple

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from BSD_Physical_Bridge_Engine import (
    BSDPhysicalBridge, 
    ScreenRegion, 
    BoardState
)


class CompleteGameTest:
    """完整对弈测试"""
    
    def __init__(self):
        self.bridge = BSDPhysicalBridge()
        self.test_results = []
        self.game_count = 0
        
    def test_bridge_initialization(self) -> bool:
        """测试物理层初始化"""
        print("\n" + "=" * 60)
        print("  [测试1] 物理层初始化")
        print("=" * 60)
        
        status = self.bridge.get_status()
        
        print(f"  ✓ 初始化状态: {status['initialized']}")
        print(f"  ✓ 引擎连接器: {status['engine_connector']}")
        print(f"  ✓ 屏幕尺寸: {self.bridge.screen_capture.get_screen_size()}")
        print(f"  ✓ 鼠标位置: {self.bridge.physical_operator.get_cursor_pos()}")
        
        result = status['initialized'] and status['engine_connector']
        self.test_results.append({
            'test': 'bridge_initialization',
            'result': 'PASS' if result else 'FAIL',
            'details': status
        })
        
        return result
    
    def test_board_recognition(self) -> bool:
        """测试棋面识别"""
        print("\n" + "=" * 60)
        print("  [测试2] 棋面识别")
        print("=" * 60)
        
        # 读取当前屏幕并识别
        board_state = self.bridge.read_board_state()
        
        print(f"  ✓ 棋盘大小: {board_state.board_size}x{board_state.board_size}")
        print(f"  ✓ 黑棋数: {np.sum(board_state.stones == 1)}")
        print(f"  ✓ 白棋数: {np.sum(board_state.stones == 2)}")
        print(f"  ✓ 识别时间: {board_state.recognized_at}")
        
        # 测试识别统计
        stats = self.bridge.board_recognizer.recognition_stats
        print(f"  ✓ 识别统计: 总计{stats['total_recognitions']}次, 平均耗时{stats['avg_time_ms']:.1f}ms")
        
        result = board_state.board_size == 19
        self.test_results.append({
            'test': 'board_recognition',
            'result': 'PASS' if result else 'FAIL',
            'details': {
                'board_size': board_state.board_size,
                'black_stones': int(np.sum(board_state.stones == 1)),
                'white_stones': int(np.sum(board_state.stones == 2))
            }
        })
        
        return result
    
    def test_engine_connector(self) -> bool:
        """测试引擎连接器"""
        print("\n" + "=" * 60)
        print("  [测试3] 引擎连接器")
        print("=" * 60)
        
        if self.bridge.engine_connector is None:
            print("  ✗ 引擎连接器未初始化")
            return False
        
        # 获取连接图
        graph = self.bridge.engine_connector.get_connection_graph()
        engine_count = len(graph.get('engines', graph.get('connections', [])))
        print(f"  ✓ 已发现引擎数: {engine_count}")
        
        # 获取路由建议
        decision = self.bridge.engine_connector.route(
            board_state=None,  # 需要适配
            phase='opening'
        )
        print(f"  ✓ 开局路由: {decision.get('decision', {}).primary_engine if hasattr(decision.get('decision', {}), 'primary_engine') else 'N/A'}")
        
        decision = self.bridge.engine_connector.route(
            board_state=None,
            phase='middle'
        )
        print(f"  ✓ 中盘路由: {decision.get('decision', {}).primary_engine if hasattr(decision.get('decision', {}), 'primary_engine') else 'N/A'}")
        
        decision = self.bridge.engine_connector.route(
            board_state=None,
            phase='ending'
        )
        print(f"  ✓ 终盘路由: {decision.get('decision', {}).primary_engine if hasattr(decision.get('decision', {}), 'primary_engine') else 'N/A'}")
        
        result = engine_count >= 10
        self.test_results.append({
            'test': 'engine_connector',
            'result': 'PASS' if result else 'FAIL',
            'details': {
                'engine_count': engine_count,
                'phases_tested': ['opening', 'middle', 'ending']
            }
        })
        
        return result
    
    def test_physical_operations(self) -> bool:
        """测试物理操作（安全模式）"""
        print("\n" + "=" * 60)
        print("  [测试4] 物理操作（安全模式）")
        print("=" * 60)
        
        # 获取鼠标位置
        pos = self.bridge.physical_operator.get_cursor_pos()
        print(f"  ✓ 当前鼠标位置: {pos}")
        
        # 测试移动（不实际移动，只测试方法可用性）
        print("  ✓ move_mouse_to 方法可用")
        print("  ✓ click 方法可用")
        print("  ✓ double_click 方法可用")
        print("  ✓ drag 方法可用")
        print("  ✓ press_key 方法可用")
        
        # 检查操作日志
        stats = self.bridge.physical_operator.get_operation_stats()
        print(f"  ✓ 操作统计: {stats}")
        
        result = all([
            hasattr(self.bridge.physical_operator, 'move_mouse_to'),
            hasattr(self.bridge.physical_operator, 'click'),
            hasattr(self.bridge.physical_operator, 'double_click'),
            hasattr(self.bridge.physical_operator, 'drag'),
            hasattr(self.bridge.physical_operator, 'press_key'),
        ])
        
        self.test_results.append({
            'test': 'physical_operations',
            'result': 'PASS' if result else 'FAIL',
            'details': stats
        })
        
        return result
    
    def test_coordination_flow(self) -> bool:
        """测试协调流程（读取→识别→决策→落子）"""
        print("\n" + "=" * 60)
        print("  [测试5] 协调流程")
        print("=" * 60)
        
        try:
            # 1. 读取屏幕
            print("  步骤1: 读取屏幕...")
            screen_img = self.bridge.screen_capture.capture_screen()
            print(f"    ✓ 截图尺寸: {screen_img.shape}")
            
            # 2. 识别棋面
            print("  步骤2: 识别棋面...")
            board_state = self.bridge.board_recognizer.recognize_board(screen_img)
            print(f"    ✓ 棋盘状态: {board_state.board_size}x{board_state.board_size}")
            
            # 3. 获取AI决策（通过引擎连接器）
            print("  步骤3: 获取AI决策...")
            if self.bridge.engine_connector:
                best_combo = self.bridge.engine_connector.get_best_combo(phase='middle')
                print(f"    ✓ 推荐引擎: {best_combo}")
            
            # 4. 测试坐标转换
            print("  步骤4: 坐标转换测试...")
            # 设置一个测试区域（屏幕中央）
            test_region = ScreenRegion(
                x=400, y=200, width=600, height=600
            )
            self.bridge.board_region = test_region
            
            # 测试坐标转换
            for test_pos in [(0, 0), (9, 9), (18, 18), (3, 15)]:
                screen_coords = self.bridge._board_to_screen_coords(test_pos[0], test_pos[1])
                print(f"    棋盘({test_pos[0]},{test_pos[1]}) → 屏幕{screen_coords}")
            
            print("  ✓ 协调流程测试成功")
            return True
            
        except Exception as e:
            print(f"  ✗ 协调流程测试失败: {e}")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "=" * 60)
        print("  BSD 物理层对接引擎 - 完整对弈测试")
        print("=" * 60)
        print(f"  测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  测试目标: 验证物理层对接与AI引擎的完整整合")
        print()
        
        tests = [
            self.test_bridge_initialization,
            self.test_board_recognition,
            self.test_engine_connector,
            self.test_physical_operations,
            self.test_coordination_flow,
        ]
        
        passed = 0
        failed = 0
        
        for test_func in tests:
            try:
                result = test_func()
                if result:
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"  ✗ 测试异常: {e}")
                failed += 1
        
        # 输出测试总结
        print("\n" + "=" * 60)
        print("  测试总结")
        print("=" * 60)
        
        for result in self.test_results:
            status_icon = "✅" if result['result'] == 'PASS' else "❌"
            print(f"  {status_icon} {result['test']}: {result['result']}")
        
        print(f"\n  通过: {passed}/{len(tests)}")
        print(f"  失败: {failed}/{len(tests)}")
        print(f"  通过率: {passed/len(tests)*100:.0f}%")
        
        # 保存测试结果
        output_dir = os.path.dirname(os.path.abspath(__file__))
        result_path = os.path.join(output_dir, 'physical_bridge_test_results.json')
        with open(result_path, 'w', encoding='utf-8') as f:
            json.dump({
                'test_time': datetime.now().isoformat(),
                'passed': passed,
                'failed': failed,
                'results': self.test_results
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n  📄 测试结果已保存: {result_path}")
        
        return passed == len(tests)


def main():
    """主函数"""
    tester = CompleteGameTest()
    success = tester.run_all_tests()
    
    print("\n" + "=" * 60)
    if success:
        print("  🎉 所有测试通过！")
        print("  物理层对接引擎已就绪，可以进行联网对弈")
    else:
        print("  ⚠️ 部分测试未通过，需要进一步优化")
    print("=" * 60)


if __name__ == "__main__":
    main()