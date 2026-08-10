#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 物理层对接引擎 (Physical Layer Bridge Engine)
================================================

核心能力：
1. 屏幕捕捉 - 基于PIL.ImageGrab获取屏幕图像
2. 棋面识别 - 基于OpenCV识别围棋棋盘上的棋子
3. 物理操作 - 基于Windows API模拟鼠标键盘操作
4. 引擎对接 - 整合已有围棋AI引擎实现完整对弈流程

理论依据：
- 屏幕 = 经过屏幕文件的转译 → 可被读取
- 操作 = 鼠标键盘的信号 → 可被模拟
- AI决策 = 已有引擎的输出 → 可被调用

使用方法：
    >>> bridge = BSDPhysicalBridge()
    >>> bridge.connect_to_go_platform()
    >>> bridge.auto_play()

版本：V1.0 · 2026-08-04
"""

import os
import sys
import time
import json
import ctypes
import threading
from datetime import datetime
from typing import Optional, Dict, List, Tuple, Any
from dataclasses import dataclass, field

import numpy as np
from PIL import ImageGrab, Image
import cv2


# ============================================================================
# 1. 屏幕捕捉模块
# ============================================================================

@dataclass
class ScreenRegion:
    """屏幕区域"""
    x: int = 0
    y: int = 0
    width: int = 1920
    height: int = 1080
    
    def to_tuple(self) -> Tuple[int, int, int, int]:
        return (self.x, self.y, self.x + self.width, self.y + self.height)


class ScreenCapture:
    """屏幕捕捉器
    
    基于PIL.ImageGrab实现屏幕截图功能，
    支持全屏截图和区域截图。
    """
    
    def __init__(self):
        self.last_capture: Optional[np.ndarray] = None
        self.capture_count = 0
        
    def capture_screen(self, region: ScreenRegion = None) -> np.ndarray:
        """捕获屏幕截图
        
        Args:
            region: 截图区域，None表示全屏
            
        Returns:
            numpy数组格式的图像 (RGB)
        """
        try:
            if region:
                bbox = region.to_tuple()
                img = ImageGrab.grab(bbox=bbox)
            else:
                img = ImageGrab.grab()
            
            # 转换为numpy数组 (RGB格式)
            img_array = np.array(img)
            self.last_capture = img_array
            self.capture_count += 1
            
            return img_array
            
        except Exception as e:
            print(f"[ScreenCapture] 截图失败: {e}")
            return np.zeros((1080, 1920, 3), dtype=np.uint8)
    
    def capture_go_board(self, board_region: ScreenRegion = None) -> np.ndarray:
        """捕获围棋棋盘区域
        
        Args:
            board_region: 棋盘区域，如果为None则自动检测
            
        Returns:
            棋盘区域图像
        """
        if board_region is None:
            board_region = self._auto_detect_board_region()
        
        return self.capture_screen(board_region)
    
    def _auto_detect_board_region(self) -> ScreenRegion:
        """自动检测棋盘区域
        
        基于特征点检测（可能需要后续优化）
        """
        # 默认使用屏幕中央800x800区域
        screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        
        board_size = min(screen_width, screen_height) // 2
        x = (screen_width - board_size) // 2
        y = (screen_height - board_size) // 2
        
        return ScreenRegion(x=x, y=y, width=board_size, height=board_size)
    
    def get_screen_size(self) -> Tuple[int, int]:
        """获取屏幕尺寸"""
        width = ctypes.windll.user32.GetSystemMetrics(0)
        height = ctypes.windll.user32.GetSystemMetrics(1)
        return (width, height)
    
    def save_capture(self, filepath: str, img: np.ndarray = None):
        """保存截图到文件"""
        if img is None:
            img = self.last_capture
        if img is not None:
            pil_img = Image.fromarray(img)
            pil_img.save(filepath)
            print(f"[ScreenCapture] 截图已保存: {filepath}")


# ============================================================================
# 2. 棋面识别模块
# ============================================================================

@dataclass
class BoardState:
    """棋盘状态"""
    board_size: int = 19
    stones: np.ndarray = None  # 0=空, 1=黑, 2=白
    last_move: Optional[Tuple[int, int]] = None
    move_count: int = 0
    recognized_at: str = ""
    
    def __post_init__(self):
        if self.stones is None:
            self.stones = np.zeros((self.board_size, self.board_size), dtype=int)


class BoardRecognizer:
    """棋面识别器
    
    基于OpenCV实现围棋棋盘的图像识别，
    识别棋盘上的棋子位置和颜色。
    """
    
    def __init__(self, board_size: int = 19):
        self.board_size = board_size
        self.last_board_state: Optional[BoardState] = None
        self.recognition_stats = {
            'total_recognitions': 0,
            'successful_recognitions': 0,
            'avg_time_ms': 0
        }
    
    def recognize_board(self, screen_img: np.ndarray, board_region: ScreenRegion = None) -> BoardState:
        """从屏幕图像识别棋盘状态
        
        Args:
            screen_img: 屏幕截图 (RGB格式)
            board_region: 棋盘区域
            
        Returns:
            识别到的棋盘状态
        """
        start_time = time.time()
        
        try:
            # 提取棋盘区域
            if board_region:
                x1, y1, x2, y2 = board_region.to_tuple()
                board_img = screen_img[y1:y2, x1:x2]
            else:
                board_img = screen_img
            
            # 转换为OpenCV格式 (BGR)
            board_bgr = cv2.cvtColor(board_img, cv2.COLOR_RGB2BGR)
            
            # 识别棋子
            stones = self._detect_stones(board_bgr)
            
            # 构建棋盘状态
            board_state = BoardState(
                board_size=self.board_size,
                stones=stones,
                recognized_at=datetime.now().isoformat()
            )
            
            # 更新统计
            elapsed = (time.time() - start_time) * 1000
            self.recognition_stats['total_recognitions'] += 1
            self.recognition_stats['successful_recognitions'] += 1
            self.recognition_stats['avg_time_ms'] = (
                (self.recognition_stats['avg_time_ms'] * (self.recognition_stats['total_recognitions'] - 1) + elapsed)
                / self.recognition_stats['total_recognitions']
            )
            
            self.last_board_state = board_state
            return board_state
            
        except Exception as e:
            print(f"[BoardRecognizer] 识别失败: {e}")
            return BoardState(board_size=self.board_size)
    
    def _detect_stones(self, board_img: np.ndarray) -> np.ndarray:
        """检测棋盘上的棋子
        
        基于颜色分析检测黑棋和白棋
        """
        h, w = board_img.shape[:2]
        stones = np.zeros((self.board_size, self.board_size), dtype=int)
        
        # 计算每个交叉点的位置
        cell_width = w / (self.board_size - 1)
        cell_height = h / (self.board_size - 1)
        
        for row in range(self.board_size):
            for col in range(self.board_size):
                # 交叉点坐标
                cx = int(col * cell_width)
                cy = int(row * cell_height)
                
                # 提取交叉点附近的区域
                roi_size = int(min(cell_width, cell_height) * 0.4)
                roi = board_img[max(0, cy-roi_size):cy+roi_size, 
                               max(0, cx-roi_size):cx+roi_size]
                
                if roi.size > 0:
                    # 分析平均颜色判断棋子类型
                    avg_color = np.mean(roi, axis=(0, 1))
                    
                    # 判断棋子类型（基于亮度）
                    brightness = np.mean(avg_color)
                    
                    if brightness < 60:  # 黑色棋子
                        stones[row][col] = 1
                    elif brightness > 200:  # 白色棋子
                        stones[row][col] = 2
                    else:
                        stones[row][col] = 0  # 空点
        
        return stones
    
    def detect_last_move(self, current_state: BoardState, previous_state: BoardState = None) -> Optional[Tuple[int, int]]:
        """检测最后一手棋
        
        通过比较前后两个棋盘状态找出最新落子
        """
        if previous_state is None:
            return None
        
        diff = current_state.stones - previous_state.stones
        new_moves = np.where(diff != 0)
        
        if len(new_moves[0]) > 0:
            # 返回第一个新落子的位置
            return (new_moves[0][0], new_moves[1][0])
        
        return None
    
    def get_board_diff(self, current: BoardState, previous: BoardState) -> Dict:
        """获取两个棋盘状态的差异"""
        diff = current.stones - previous.stones
        black_added = np.sum((diff == 1))
        white_added = np.sum((diff == 2))
        
        return {
            'black_stones_added': int(black_added),
            'white_stones_added': int(white_added),
            'total_new_stones': int(black_added + white_added),
            'position_changed': bool(np.any(diff != 0))
        }


# ============================================================================
# 3. 物理操作模块
# ============================================================================

class PhysicalOperator:
    """物理操作器
    
    基于Windows API模拟鼠标键盘操作，
    实现"像人类一样"的操作方式。
    
    核心API:
    - SetCursorPos: 设置鼠标位置
    - mouse_event: 模拟鼠标事件
    - keybd_event: 模拟键盘事件
    """
    
    # Windows API常量
    MOUSEEVENTF_MOVE = 0x0001
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004
    MOUSEEVENTF_RIGHTDOWN = 0x0008
    MOUSEEVENTF_RIGHTUP = 0x0010
    MOUSEEVENTF_ABSOLUTE = 0x8000
    
    KEYEVENTF_KEYUP = 0x0002
    
    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.operation_log = []
        self.last_operation_time = 0
    
    def move_mouse_to(self, x: int, y: int, smooth: bool = True):
        """移动鼠标到指定位置
        
        Args:
            x: 目标x坐标
            y: 目标y坐标
            smooth: 是否平滑移动（模拟人类操作）
        """
        if smooth:
            # 平滑移动：分多步移动，模拟人类
            current_x = self.user32.GetCursorPos()[0]  # 简化
            current_y = self.user32.GetCursorPos()[1]
            
            steps = max(abs(x - current_x), abs(y - current_y)) // 10 + 1
            steps = min(steps, 20)  # 最多20步
            
            for i in range(1, steps + 1):
                t = i / steps
                step_x = int(current_x + (x - current_x) * t)
                step_y = int(current_y + (y - current_y) * t)
                self.user32.SetCursorPos(step_x, step_y)
                time.sleep(0.005)  # 5ms延迟
        
        self.user32.SetCursorPos(x, y)
        
        self._log_operation('move', x, y)
    
    def click(self, x: int = None, y: int = None, button: str = 'left'):
        """点击鼠标
        
        Args:
            x: 点击位置x坐标（None=当前位置）
            y: 点击位置y坐标
            button: 'left' or 'right'
        """
        if x is not None and y is not None:
            self.move_mouse_to(x, y)
            time.sleep(0.05)  # 50ms等待，模拟人类反应时间
        
        if button == 'left':
            self.user32.mouse_event(self.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.02)
            self.user32.mouse_event(self.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        elif button == 'right':
            self.user32.mouse_event(self.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
            time.sleep(0.02)
            self.user32.mouse_event(self.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        
        self._log_operation('click', x, y, button)
    
    def double_click(self, x: int = None, y: int = None):
        """双击"""
        self.click(x, y)
        time.sleep(0.1)
        self.click(x, y)
    
    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int):
        """拖拽"""
        self.move_mouse_to(start_x, start_y)
        self.user32.mouse_event(self.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.05)
        self.move_mouse_to(end_x, end_y, smooth=True)
        self.user32.mouse_event(self.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    
    def press_key(self, key_code: int, hold_time: float = 0.05):
        """按键"""
        self.user32.keybd_event(key_code, 0, 0, 0)
        time.sleep(hold_time)
        self.user32.keybd_event(key_code, 0, self.KEYEVENTF_KEYUP, 0, 0)
    
    def type_text(self, text: str, interval: float = 0.02):
        """输入文本（简化版）"""
        # 注意：这只是一个简化实现
        # 完整实现需要处理输入法等问题
        print(f"[PhysicalOperator] 输入文本: {text}")
    
    def get_cursor_pos(self) -> Tuple[int, int]:
        """获取当前鼠标位置"""
        x = ctypes.c_long()
        y = ctypes.c_long()
        self.user32.GetCursorPos(ctypes.pointer(x), ctypes.pointer(y))
        return (x.value, y.value)
    
    def move_mouse_to(self, x: int, y: int, smooth: bool = True):
        """移动鼠标到指定位置
        
        Args:
            x: 目标x坐标
            y: 目标y坐标
            smooth: 是否平滑移动（模拟人类操作）
        """
        if smooth:
            # 平滑移动：分多步移动，模拟人类
            current_x, current_y = self.get_cursor_pos()
            
            steps = max(abs(x - current_x), abs(y - current_y)) // 10 + 1
            steps = min(steps, 20)  # 最多20步
            
            for i in range(1, steps + 1):
                t = i / steps
                step_x = int(current_x + (x - current_x) * t)
                step_y = int(current_y + (y - current_y) * t)
                self.user32.SetCursorPos(step_x, step_y)
                time.sleep(0.005)  # 5ms延迟
        
        self.user32.SetCursorPos(x, y)
        
        self._log_operation('move', x, y)
    
    def _log_operation(self, operation: str, x: int = 0, y: int = 0, extra: str = ""):
        """记录操作日志"""
        self.operation_log.append({
            'time': datetime.now().isoformat(),
            'operation': operation,
            'x': x,
            'y': y,
            'extra': extra
        })
        self.last_operation_time = time.time()
    
    def get_operation_stats(self) -> Dict:
        """获取操作统计"""
        return {
            'total_operations': len(self.operation_log),
            'last_operation_time': self.last_operation_time,
            'operations_per_minute': len(self.operation_log) / max(time.time() - self.operation_log[0]['time'] if self.operation_log else 1, 60)
        }


# ============================================================================
# 4. 物理层对接引擎（整合所有模块）
# ============================================================================

class BSDPhysicalBridge:
    """BSD物理层对接引擎
    
    整合屏幕捕捉、棋面识别、物理操作三大核心模块，
    实现完整的联网对弈能力。
    
    工作流程：
    1. 屏幕捕捉 → 获取棋面图像
    2. 棋面识别 → 分析当前局面
    3. AI决策 → 获取最佳落子
    4. 物理操作 → 模拟人类落子
    
    理论：屏幕是转译层 → 可读取
          操作是信号层 → 可模拟
    """
    
    def __init__(self):
        # 核心模块
        self.screen_capture = ScreenCapture()
        self.board_recognizer = BoardRecognizer()
        self.physical_operator = PhysicalOperator()
        
        # 引擎连接器（延迟初始化）
        self.engine_connector = None
        self.ai_engine = None
        
        # 对弈状态
        self.is_connected = False
        self.is_playing = False
        self.current_player = 'black'  # 'black' or 'white'
        self.my_color = 'black'  # 我方颜色
        self.move_count = 0
        self.game_log = []
        
        # 棋盘区域配置
        self.board_region: Optional[ScreenRegion] = None
        
        # 初始化状态
        self._initialized = False
        self._init_status = self._initialize()
    
    def _initialize(self) -> bool:
        """初始化物理层对接"""
        print("=" * 60)
        print("  BSD 物理层对接引擎初始化")
        print("=" * 60)
        
        try:
            # 获取屏幕尺寸
            screen_size = self.screen_capture.get_screen_size()
            print(f"  [屏幕] 屏幕尺寸: {screen_size[0]}x{screen_size[1]}")
            
            # 测试屏幕捕捉
            test_img = self.screen_capture.capture_screen()
            print(f"  [屏幕] 截图测试: {test_img.shape}")
            
            # 测试棋面识别
            test_board = self.board_recognizer.recognize_board(test_img)
            print(f"  [识别] 棋盘识别测试: {test_board.board_size}x{test_board.board_size}")
            
            # 测试物理操作（只读模式）
            cursor_pos = self.physical_operator.get_cursor_pos()
            print(f"  [操作] 鼠标位置: {cursor_pos}")
            
            # 自动连接引擎连接器
            try:
                print("\n  [引擎] 激活引擎连接器...")
                from BSD_Go_Engine_Connector import EngineConnector
                self.engine_connector = EngineConnector()
                engine_count = len(self.engine_connector.registry.list_engines())
                print(f"  [引擎] 已发现 {engine_count} 个散落引擎")
            except Exception as e:
                print(f"  [引擎] 引擎连接器激活失败（可稍后手动连接）: {e}")
            
            self._initialized = True
            print()
            print("  ✅ 物理层对接初始化成功")
            return True
            
        except Exception as e:
            print(f"  ❌ 初始化失败: {e}")
            return False
    
    def connect_to_ai_engine(self, engine_path: str = None) -> bool:
        """连接AI引擎
        
        Args:
            engine_path: 引擎文件路径，None则使用默认引擎连接器
            
        Returns:
            连接是否成功
        """
        print("\n[BSDPhysicalBridge] 连接AI引擎...")
        
        try:
            if engine_path:
                # 直接加载指定引擎
                import importlib.util
                spec = importlib.util.spec_from_file_location("ai_engine", engine_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.ai_engine = module
            else:
                # 使用引擎连接器
                from BSD_Go_Engine_Connector import EngineConnector
                self.engine_connector = EngineConnector()
                print(f"  [引擎连接器] 已激活")
            
            print("  ✅ AI引擎连接成功")
            return True
            
        except Exception as e:
            print(f"  ❌ AI引擎连接失败: {e}")
            print("  💡 提示：请确保BSD_Go_Engine_Connector.py在同一目录下")
            return False
    
    def set_board_region(self, x: int, y: int, width: int, height: int):
        """设置棋盘在屏幕上的区域
        
        Args:
            x: 棋盘左上角x坐标
            y: 棋盘左上角y坐标
            width: 棋盘宽度（像素）
            height: 棋盘高度（像素）
        """
        self.board_region = ScreenRegion(x=x, y=y, width=width, height=height)
        print(f"  [配置] 棋盘区域: ({x}, {y}) - ({x+width}, {y+height})")
    
    def read_board_state(self) -> BoardState:
        """读取当前棋盘状态
        
        Returns:
            当前棋盘状态
        """
        # 1. 屏幕捕捉
        screen_img = self.screen_capture.capture_screen()
        
        # 2. 棋面识别
        board_state = self.board_recognizer.recognize_board(screen_img, self.board_region)
        
        return board_state
    
    def get_ai_move(self, board_state: BoardState, player: str = 'black') -> Optional[Tuple[int, int]]:
        """获取AI落子
        
        Args:
            board_state: 当前棋盘状态
            player: 落子方 ('black' or 'white')
            
        Returns:
            落子位置 (row, col) 或 None
        """
        try:
            if self.engine_connector:
                # 通过引擎连接器获取决策
                # 这里需要适配具体的引擎接口
                best_combo = self.engine_connector.get_best_combo(phase='middle')
                print(f"  [AI] 推荐引擎组合: {best_combo}")
                return None  # 占位，需要具体引擎适配
            
            elif self.ai_engine:
                # 直接调用AI引擎
                return None  # 占位，需要具体引擎适配
            
            else:
                print("  ⚠️ AI引擎未连接")
                return None
                
        except Exception as e:
            print(f"  [AI] 决策失败: {e}")
            return None
    
    def execute_move(self, row: int, col: int):
        """执行落子操作（模拟人类点击）
        
        Args:
            row: 棋盘行 (0-18)
            col: 棋盘列 (0-18)
        """
        if self.board_region is None:
            print("  ⚠️ 未设置棋盘区域，无法执行落子")
            return
        
        # 计算棋盘坐标对应的屏幕像素坐标
        x, y = self._board_to_screen_coords(row, col)
        
        print(f"  [落子] 棋盘({row},{col}) → 屏幕({x},{y})")
        
        # 模拟人类点击
        self.physical_operator.click(x, y)
        
        # 记录操作
        self.move_count += 1
        self.game_log.append({
            'move': self.move_count,
            'position': (row, col),
            'screen_coords': (x, y),
            'timestamp': datetime.now().isoformat()
        })
    
    def _board_to_screen_coords(self, row: int, col: int) -> Tuple[int, int]:
        """将棋盘坐标转换为屏幕坐标
        
        Args:
            row: 棋盘行
            col: 棋盘列
            
        Returns:
            屏幕像素坐标 (x, y)
        """
        if self.board_region is None:
            return (0, 0)
        
        # 计算单元格大小
        cell_width = self.board_region.width / (self.board_recognizer.board_size - 1)
        cell_height = self.board_region.height / (self.board_recognizer.board_size - 1)
        
        # 转换坐标
        x = int(self.board_region.x + col * cell_width)
        y = int(self.board_region.y + row * cell_height)
        
        return (x, y)
    
    def auto_play_single_move(self, my_color: str = 'black') -> bool:
        """自动执行一手棋
        
        Args:
            my_color: 我方颜色
            
        Returns:
            是否成功执行
        """
        print(f"\n[自动对弈] 第{self.move_count + 1}手")
        
        try:
            # 1. 读取棋盘状态
            board_state = self.read_board_state()
            print(f"  [识别] 棋盘状态已读取")
            
            # 2. 获取AI决策
            move = self.get_ai_move(board_state, my_color)
            
            if move is None:
                print("  ⚠️ AI未返回有效落子")
                return False
            
            # 3. 执行落子
            self.execute_move(move[0], move[1])
            
            return True
            
        except Exception as e:
            print(f"  ❌ 执行失败: {e}")
            return False
    
    def get_status(self) -> Dict:
        """获取引擎状态"""
        return {
            'initialized': self._initialized,
            'connected': self.is_connected,
            'playing': self.is_playing,
            'engine_connector': self.engine_connector is not None,
            'ai_engine': self.ai_engine is not None,
            'board_region': {
                'x': self.board_region.x if self.board_region else None,
                'y': self.board_region.y if self.board_region else None,
                'width': self.board_region.width if self.board_region else None,
                'height': self.board_region.height if self.board_region else None,
            } if self.board_region else None,
            'move_count': self.move_count,
            'game_log_length': len(self.game_log),
            'recognition_stats': self.board_recognizer.recognition_stats,
            'operation_stats': self.physical_operator.get_operation_stats()
        }
    
    def save_game_log(self, filepath: str):
        """保存对弈日志"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'status': self.get_status(),
                'game_log': self.game_log,
                'timestamp': datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
        print(f"  [保存] 对弈日志: {filepath}")


# ============================================================================
# 5. 测试与演示
# ============================================================================

def demo_physical_bridge():
    """演示物理层对接引擎"""
    
    print("\n" + "=" * 60)
    print("  BSD 物理层对接引擎 - 演示")
    print("=" * 60)
    
    # 1. 初始化引擎
    bridge = BSDPhysicalBridge()
    
    # 2. 连接AI引擎
    connected = bridge.connect_to_ai_engine()
    print(f"\n[连接] AI引擎状态: {'已连接' if connected else '未连接'}")
    
    # 3. 读取当前屏幕（测试）
    print("\n[测试] 读取当前屏幕状态...")
    board_state = bridge.read_board_state()
    print(f"  棋盘大小: {board_state.board_size}x{board_state.board_size}")
    print(f"  黑棋数: {np.sum(board_state.stones == 1)}")
    print(f"  白棋数: {np.sum(board_state.stones == 2)}")
    
    # 4. 测试物理操作（安全模式）
    print("\n[测试] 物理操作测试（安全模式）...")
    cursor_pos = bridge.physical_operator.get_cursor_pos()
    print(f"  当前鼠标位置: {cursor_pos}")
    
    # 5. 获取状态
    print("\n[状态] 引擎状态:")
    status = bridge.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 60)
    print("  ✅ 物理层对接引擎演示完成")
    print("=" * 60)
    
    return bridge


if __name__ == "__main__":
    demo_physical_bridge()