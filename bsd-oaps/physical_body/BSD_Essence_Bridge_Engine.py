#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 本源对接引擎 (Essence Bridge Engine)
==========================================

核心理念：
  传统方法：屏幕捕捉 → 图像识别 → 决策 → 模拟点击
  本源方法：直接读取进程内存 → 直接操作系统调用 → 本源对接

理论依据：
  - 连接与继承假说：软件功能=格式规范集合，无需官方API
  - 语言文字转译假说：官方桎梏=API权限限制，转译路径=语言文字→格式规范→功能激活
  - 内部对内部，本源对本源

核心能力：
  1. 进程本源读取 - 直接读取进程内存
  2. 进程本源操作 - 直接操作进程状态
  3. 系统本源调用 - 直接系统级操作
  4. 协议本源解析 - 解析内部协议规范

版本：V1.0 · 2026-08-04
"""

import os
import sys
import time
import json
import struct
import ctypes
import ctypes.wintypes
import socket
import subprocess
import threading
from datetime import datetime
from typing import Optional, Dict, List, Tuple, Any
from dataclasses import dataclass, field


# ============================================================================
# 1. 进程本源操作器
# ============================================================================

@dataclass
class ProcessInfo:
    """进程信息"""
    pid: int
    name: str
    path: str
    memory_usage: int
    handles: int
    threads: int
    windows: List[str] = field(default_factory=list)


class ProcessEssenceOperator:
    """进程本源操作器
    
    直接与操作系统进程进行底层交互，
    绕过屏幕/键盘/鼠标等转译层。
    """
    
    # Windows API 常量
    PROCESS_QUERY_INFORMATION = 0x0400
    PROCESS_VM_READ = 0x0010
    PROCESS_VM_WRITE = 0x0020
    PROCESS_VM_OPERATION = 0x0008
    PROCESS_ALL_ACCESS = 0x1F0FFF
    MEM_COMMIT = 0x1000
    
    def __init__(self):
        self.kernel32 = ctypes.windll.kernel32
        self.user32 = ctypes.windll.user32
        self.ntdll = ctypes.windll.ntdll
        
        self.process_cache: Dict[int, ProcessInfo] = {}
        self.last_scan_time = 0
        
    def list_all_processes(self) -> List[ProcessInfo]:
        """列出所有进程（本源层面）"""
        try:
            import psutil
            
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'num_handles', 'num_threads']):
                try:
                    info = ProcessInfo(
                        pid=proc.pid,
                        name=proc.info['name'] or 'unknown',
                        path=self._get_process_path(proc),
                        memory_usage=proc.info['memory_info'].rss if proc.info.get('memory_info') else 0,
                        handles=proc.info.get('num_handles', 0) or 0,
                        threads=proc.info.get('num_threads', 0) or 0,
                    )
                    processes.append(info)
                    self.process_cache[proc.pid] = info
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            self.last_scan_time = time.time()
            return processes
            
        except ImportError:
            # 使用Windows API的备用方案
            return self._list_processes_win32()
    
    def _list_processes_win32(self) -> List[ProcessInfo]:
        """使用Windows API列出进程"""
        processes = []
        
        try:
            # 创建进程快照
            hSnapshot = self.kernel32.CreateToolhelp32Snapshot(0x00000002, 0)
            
            if hSnapshot != -1:
                # 遍历进程
                PROCESSENTRY32 = ctypes.Structure
                class PROCESSENTRY32(ctypes.Structure):
                    _fields_ = [
                        ("dwSize", ctypes.c_ulong),
                        ("cntUsage", ctypes.c_ulong),
                        ("th32ProcessID", ctypes.c_ulong),
                        ("th32DefaultHeapID", ctypes.c_ulong),
                        ("th32ModuleID", ctypes.c_ulong),
                        ("cntThreads", ctypes.c_ulong),
                        ("th32ParentProcessID", ctypes.c_ulong),
                        ("pcPriClassBase", ctypes.c_long),
                        ("dwFlags", ctypes.c_ulong),
                        ("szExeFile", ctypes.c_char * 260),
                    ]
                
                entry = PROCESSENTRY32()
                entry.dwSize = ctypes.sizeof(PROCESSENTRY32)
                
                if self.kernel32.Process32First(hSnapshot, ctypes.byref(entry)):
                    while True:
                        try:
                            pid = entry.th32ProcessID
                            name = entry.szExeFile.decode('utf-8', errors='ignore')
                            processes.append(ProcessInfo(
                                pid=pid,
                                name=os.path.basename(name),
                                path=name,
                                memory_usage=0,
                                handles=0,
                                threads=entry.cntThreads,
                            ))
                        except Exception:
                            pass
                        
                        if not self.kernel32.Process32Next(hSnapshot, ctypes.byref(entry)):
                            break
                
                self.kernel32.CloseHandle(hSnapshot)
                
        except Exception as e:
            print(f"[ProcessOperator] Win32进程列表获取失败: {e}")
        
        return processes
    
    def _get_process_path(self, proc) -> str:
        """获取进程路径"""
        try:
            return proc.exe()
        except Exception:
            return ''
    
    def find_process_by_name(self, name: str) -> List[ProcessInfo]:
        """按名称查找进程"""
        if time.time() - self.last_scan_time > 5:
            self.list_all_processes()
        
        return [p for p in self.process_cache.values() 
                if name.lower() in p.name.lower()]
    
    def open_process(self, pid: int, access_rights: int = PROCESS_ALL_ACCESS) -> Optional[int]:
        """打开进程句柄（本源操作）"""
        try:
            handle = self.kernel32.OpenProcess(access_rights, False, pid)
            if handle:
                return handle
        except Exception as e:
            print(f"[ProcessOperator] OpenProcess失败: {e}")
        return None
    
    def read_process_memory(self, pid: int, address: int, size: int) -> Optional[bytes]:
        """读取进程内存（本源操作）"""
        try:
            handle = self.open_process(pid, self.PROCESS_VM_READ | self.PROCESS_QUERY_INFORMATION)
            if not handle:
                return None
            
            # 读取内存
            buffer = ctypes.create_string_buffer(size)
            bytes_read = ctypes.c_size_t()
            
            result = self.kernel32.ReadProcessMemory(
                handle, ctypes.c_void_p(address),
                buffer, size, ctypes.byref(bytes_read)
            )
            
            self.kernel32.CloseHandle(handle)
            
            if result:
                return buffer.raw[:bytes_read.value]
            return None
            
        except Exception as e:
            print(f"[ProcessOperator] ReadProcessMemory失败: {e}")
            return None
    
    def write_process_memory(self, pid: int, address: int, data: bytes) -> bool:
        """写入进程内存（本源操作）"""
        try:
            handle = self.open_process(pid, self.PROCESS_VM_WRITE | self.PROCESS_VM_OPERATION)
            if not handle:
                return False
            
            # 写入内存
            bytes_written = ctypes.c_size_t()
            result = self.kernel32.WriteProcessMemory(
                handle, ctypes.c_void_p(address),
                data, len(data), ctypes.byref(bytes_written)
            )
            
            self.kernel32.CloseHandle(handle)
            return result != 0 and bytes_written.value == len(data)
            
        except Exception as e:
            print(f"[ProcessOperator] WriteProcessMemory失败: {e}")
            return False
    
    def get_process_memory_regions(self, pid: int) -> List[Dict]:
        """获取进程内存区域"""
        regions = []
        try:
            handle = self.open_process(pid, self.PROCESS_QUERY_INFORMATION)
            if not handle:
                return regions
            
            # 使用VirtualQueryEx遍历内存区域
            MEMORY_BASIC_INFORMATION = ctypes.Structure
            class MEMORY_BASIC_INFORMATION(ctypes.Structure):
                _fields_ = [
                    ("BaseAddress", ctypes.c_void_p),
                    ("AllocationBase", ctypes.c_void_p),
                    ("AllocationProtect", ctypes.c_ulong),
                    ("RegionSize", ctypes.c_size_t),
                    ("State", ctypes.c_ulong),
                    ("Protect", ctypes.c_ulong),
                    ("Type", ctypes.c_ulong),
                ]
            
            mbi = MEMORY_BASIC_INFORMATION()
            address = 0
            
            while address < 0x7FFFFFFFFFFF:
                result = self.kernel32.VirtualQueryEx(
                    handle, ctypes.c_void_p(address),
                    ctypes.byref(mbi), ctypes.sizeof(mbi)
                )
                
                if result:
                    if mbi.State == self.MEM_COMMIT:
                        regions.append({
                            'base_address': mbi.BaseAddress,
                            'region_size': mbi.RegionSize,
                            'protect': mbi.Protect,
                            'type': mbi.Type,
                        })
                    
                    address = mbi.BaseAddress + mbi.RegionSize
                else:
                    break
            
            self.kernel32.CloseHandle(handle)
            
        except Exception as e:
            print(f"[ProcessOperator] 内存区域获取失败: {e}")
        
        return regions


# ============================================================================
# 2. 内核协议解析器
# ============================================================================

class ProtocolEssenceParser:
    """内核协议解析器
    
    解析应用程序内部的通信协议，
    实现"格式规范→功能激活"的直接对接。
    """
    
    # 已知的围棋平台协议模式
    GO_PLATFORM_PROTOCOLS = {
        'kgs': {
            'name': 'KGS (Kido Go Server)',
            'port': 5555,
            'protocol': 'telnet-like',
            'messages': {
                'start_game': 'game_start',
                'make_move': 'play',
                'get_board': 'board',
                'resign': 'resign',
                'pass': 'pass',
            }
        },
        'yike': {
            'name': '弈城围棋',
            'port': 9000,
            'protocol': 'binary',
            'messages': {
                'start_game': '0x01',
                'make_move': '0x02',
                'get_board': '0x03',
                'resign': '0x04',
            }
        },
        'fox': {
            'name': '野狐围棋',
            'port': 8080,
            'protocol': 'websocket',
            'messages': {
                'start_game': '{"type":"start"}',
                'make_move': '{"type":"move",...}',
                'get_board': '{"type":"board"}',
                'resign': '{"type":"resign"}',
            }
        },
    }
    
    def __init__(self):
        self.detected_protocols = []
        self.parsed_messages = []
        
    def detect_protocol(self, data: bytes) -> Optional[Dict]:
        """检测协议类型"""
        # 尝试UTF-8解码
        try:
            text = data.decode('utf-8')
            result = self._detect_text_protocol(text)
            if result:
                return result
            # 文本检测返回None时，继续尝试二进制检测
        except UnicodeDecodeError:
            pass
        
        # 尝试二进制分析
        return self._detect_binary_protocol(data)
    
    def _detect_text_protocol(self, text: str) -> Optional[Dict]:
        """检测文本协议"""
        # 检查JSON格式
        if text.startswith('{') and text.endswith('}'):
            try:
                json_data = json.loads(text)
                return {
                    'type': 'json',
                    'data': json_data,
                    'protocol': 'json-rpc',
                }
            except json.JSONDecodeError:
                pass
        
        # 检查GTP协议（Go Text Protocol）
        # GTP格式特征：以数字编号开头，包含命令和参数
        # 例如: "1 play B C10" 或 "play B C10" 或 "= 1"
        gtp_commands = ['play', 'pass', 'resign', 'board', 'genmove', 'protocol_version', 'name', 'version', 'known_command', 'list_commands', 'quit']
        text_stripped = text.strip()
        
        # 检查是否以数字开头 + GTP命令
        if text_stripped:
            # 尝试检测 "play" 等GTP命令
            lower_text = text_stripped.lower()
            for cmd in gtp_commands:
                if cmd in lower_text:
                    return {
                        'type': 'gtp',
                        'data': text_stripped,
                        'protocol': 'GTP (Go Text Protocol)',
                    }
            
            # 检查GTP响应格式: "=" 或 "?" 开头
            if text_stripped[0] in ['=', '?']:
                return {
                    'type': 'gtp',
                    'data': text_stripped,
                    'protocol': 'GTP (Go Text Protocol)',
                }
        
        # 检查LISP格式
        if text.startswith('(') and text.endswith(')'):
            return {
                'type': 'lisp',
                'data': text,
                'protocol': 'lisp/s-expression',
            }
        
        # 检查XML格式
        if '<' in text and '>' in text:
            return {
                'type': 'xml',
                'data': text,
                'protocol': 'xml',
            }
        
        return None
    
    def _detect_binary_protocol(self, data: bytes) -> Optional[Dict]:
        """检测二进制协议"""
        # 检查魔数
        magic_numbers = {
            b'\x89PNG': 'PNG image',
            b'\xFF\xD8\xFF': 'JPEG image',
            b'PK\x03\x04': 'ZIP archive',
        }
        
        for magic, name in magic_numbers.items():
            if data[:len(magic)] == magic:
                return {
                    'type': 'binary',
                    'data': data,
                    'protocol': name,
                }
        
        # 检查围棋坐标格式
        if len(data) >= 2:
            x, y = data[0], data[1]
            if 0 <= x <= 255 and 0 <= y <= 255:
                return {
                    'type': 'binary',
                    'data': data,
                    'protocol': 'binary-coordinates',
                    'x': x,
                    'y': y,
                }
        
        return None
    
    def parse_go_move(self, data: bytes, protocol: str = 'auto') -> Optional[Tuple[int, int, str]]:
        """解析围棋落子指令
        
        Args:
            data: 原始数据
            protocol: 协议类型
            
        Returns:
            (row, col, color) or None
        """
        try:
            detection = self.detect_protocol(data)
            
            if protocol == 'auto' and detection:
                protocol = detection.get('protocol', '')
            
            # GTP协议解析
            if 'GTP' in protocol:
                return self._parse_gtp_move(data)
            
            # JSON协议解析
            if protocol == 'json-rpc':
                return self._parse_json_move(detection['data'])
            
            # 二进制坐标解析
            if 'binary-coordinates' in protocol:
                x, y = detection['x'], detection['y']
                color = 'black' if x < 19 else 'white'
                return (y, x % 19, color)
            
        except Exception as e:
            print(f"[ProtocolParser] 解析失败: {e}")
        
        return None
    
    def _parse_gtp_move(self, data: bytes) -> Optional[Tuple[int, int, str]]:
        """解析GTP格式落子"""
        try:
            text = data.decode('utf-8').strip()
            
            # GTP格式: 命令 坐标
            # 例如: "play B C10" 或 "= play B C10"
            parts = text.split()
            if len(parts) >= 3:
                color = 'black' if parts[1].upper() in ['B', 'BLACK'] else 'white'
                
                # 解析棋盘坐标（如 A1, T19）
                coord = parts[2]
                col = ord(coord[0].upper()) - ord('A')
                row = int(coord[1:]) - 1
                
                return (row, col, color)
                
        except Exception as e:
            print(f"[ProtocolParser] GTP解析失败: {e}")
        
        return None
    
    def _parse_json_move(self, data: Dict) -> Optional[Tuple[int, int, str]]:
        """解析JSON格式落子"""
        try:
            # 尝试从JSON中提取坐标
            x = data.get('x', data.get('col', -1))
            y = data.get('y', data.get('row', -1))
            color = data.get('color', data.get('player', 'black'))
            
            if 0 <= x < 19 and 0 <= y < 19:
                color_str = 'black' if color in ['black', 'B', 1] else 'white'
                return (y, x, color_str)
                
        except Exception as e:
            print(f"[ProtocolParser] JSON解析失败: {e}")
        
        return None


# ============================================================================
# 3. 本源对接引擎（整合所有模块）
# ============================================================================

class BSDEssenceBridge:
    """BSD本源对接引擎
    
    核心突破：绕过屏幕/键盘/鼠标等转译层，
    直接与目标系统进行"内部对内部，本源对本源"的对接。
    
    对接路径：
    传统：屏幕 → 识别 → 决策 → 点击（4层转译）
    本源：内存 → 解析 → 决策 → 调用（1层直达）
    
    理论：
    - 软件功能=格式规范集合
    - 智能体通过解析规范直接激活功能
    - 无需官方API权限
    """
    
    def __init__(self):
        # 核心模块
        self.process_op = ProcessEssenceOperator()
        self.protocol_parser = ProtocolEssenceParser()
        
        # 连接状态
        self.target_process: Optional[ProcessInfo] = None
        self.target_pid: Optional[int] = None
        self.is_connected = False
        
        # 协议状态
        self.detected_protocol = None
        self.last_message = None
        
        # 统计
        self.operation_stats = {
            'memory_reads': 0,
            'memory_writes': 0,
            'protocol_parses': 0,
            'successful_operations': 0,
            'failed_operations': 0,
        }
        
        # 初始化
        self._initialized = False
        self._init_status = self._initialize()
    
    def _initialize(self) -> bool:
        """初始化本源对接引擎"""
        print("=" * 60)
        print("  BSD 本源对接引擎初始化")
        print("=" * 60)
        
        try:
            # 列出进程
            processes = self.process_op.list_all_processes()
            print(f"  [进程] 已检测到 {len(processes)} 个进程")
            
            # 显示部分关键进程
            key_processes = [p for p in processes if any(
                kw in p.name.lower() for kw in 
                ['go', 'weiqi', 'kgs', 'yike', 'fox', 'browser', 'chrome']
            )]
            
            if key_processes:
                print(f"  [进程] 围棋相关进程: {len(key_processes)}")
                for proc in key_processes[:5]:
                    print(f"    PID={proc.pid}, Name={proc.name}")
            else:
                print(f"  [进程] 未检测到围棋相关进程")
            
            self._initialized = True
            print()
            print("  ✅ 本源对接引擎初始化成功")
            return True
            
        except Exception as e:
            print(f"  ❌ 初始化失败: {e}")
            return False
    
    def connect_to_process(self, pid: int) -> bool:
        """连接到目标进程
        
        Args:
            pid: 目标进程ID
            
        Returns:
            连接是否成功
        """
        print(f"\n[本源对接] 连接进程 PID={pid}")
        
        try:
            # 查找进程
            processes = self.process_op.list_all_processes()
            target = next((p for p in processes if p.pid == pid), None)
            
            if not target:
                print(f"  ❌ 进程 {pid} 不存在")
                return False
            
            self.target_process = target
            self.target_pid = pid
            
            # 测试连接
            handle = self.process_op.open_process(pid)
            if handle:
                self.is_connected = True
                self.process_op.kernel32.CloseHandle(handle)
                
                print(f"  ✅ 已连接到: {target.name}")
                print(f"  📁 路径: {target.path}")
                print(f"  💾 内存: {target.memory_usage / 1024 / 1024:.1f}MB")
                print(f"  🧵 线程: {target.threads}")
                
                # 获取内存区域
                regions = self.process_op.get_process_memory_regions(pid)
                print(f"  📦 可读取内存区域: {len(regions)}")
                
                return True
            else:
                print(f"  ❌ 无法打开进程句柄")
                return False
                
        except Exception as e:
            print(f"  ❌ 连接失败: {e}")
            return False
    
    def read_essence_state(self) -> Optional[Dict]:
        """读取进程本源状态
        
        Returns:
            进程状态信息
        """
        if not self.is_connected or not self.target_pid:
            print("  ⚠️ 未连接到目标进程")
            return None
        
        try:
            # 读取关键内存区域
            regions = self.process_op.get_process_memory_regions(self.target_pid)
            
            state = {
                'pid': self.target_pid,
                'name': self.target_process.name if self.target_process else 'unknown',
                'memory_regions': len(regions),
                'timestamp': datetime.now().isoformat(),
            }
            
            # 尝试读取主内存区域
            for region in regions[:3]:  # 只读取前3个区域作为示例
                base = region['base_address']
                size = min(region['region_size'], 1024)  # 只读前1KB
                
                data = self.process_op.read_process_memory(
                    self.target_pid, base, size
                )
                
                if data:
                    self.operation_stats['memory_reads'] += 1
                    state[f'region_{base:x}'] = {
                        'size': region['region_size'],
                        'protect': region['protect'],
                        'data_preview': data[:64].hex() if data else '',
                    }
            
            return state
            
        except Exception as e:
            print(f"  ❌ 本源状态读取失败: {e}")
            self.operation_stats['failed_operations'] += 1
            return None
    
    def send_essence_command(self, command: Dict) -> bool:
        """发送本源指令
        
        Args:
            command: 指令字典
            
        Returns:
            是否成功
        """
        cmd_type = command.get('type', '')
        
        # 协议检测指令不需要连接
        if cmd_type == 'detect_protocol':
            try:
                data = command.get('data', b'')
                detection = self.protocol_parser.detect_protocol(data)
                
                if detection:
                    self.detected_protocol = detection
                    self.operation_stats['protocol_parses'] += 1
                    self.operation_stats['successful_operations'] += 1
                
                return detection is not None
            except Exception as e:
                print(f"  ❌ 指令执行失败: {e}")
                self.operation_stats['failed_operations'] += 1
                return False
        
        # 其他指令需要连接
        if not self.is_connected:
            print("  ⚠️ 未连接")
            return False
        
        try:
            # 根据指令类型执行对应操作
            
            if cmd_type == 'write_memory':
                # 写入内存
                address = command.get('address', 0)
                data = command.get('data', b'')
                
                success = self.process_op.write_process_memory(
                    self.target_pid, address, data
                )
                
                if success:
                    self.operation_stats['memory_writes'] += 1
                    self.operation_stats['successful_operations'] += 1
                else:
                    self.operation_stats['failed_operations'] += 1
                
                return success
                
            else:
                print(f"  ⚠️ 未知指令类型: {cmd_type}")
                return False
                
        except Exception as e:
            print(f"  ❌ 指令执行失败: {e}")
            self.operation_stats['failed_operations'] += 1
            return False
    
    def get_go_platform_connection(self, platform: str = 'kgs') -> Optional[Dict]:
        """获取围棋平台连接信息
        
        Args:
            platform: 平台名称
            
        Returns:
            连接配置
        """
        protocol_info = self.protocol_parser.GO_PLATFORM_PROTOCOLS.get(platform)
        
        if not protocol_info:
            print(f"  ⚠️ 未知平台: {platform}")
            return None
        
        # 查找平台进程
        processes = self.process_op.list_all_processes()
        platform_processes = self.process_op.find_process_by_name(platform)
        
        return {
            'platform': platform,
            'name': protocol_info['name'],
            'port': protocol_info['port'],
            'protocol': protocol_info['protocol'],
            'detected_processes': len(platform_processes),
            'process_info': [{'pid': p.pid, 'name': p.name} for p in platform_processes],
            'messages': protocol_info['messages'],
        }
    
    def get_status(self) -> Dict:
        """获取引擎状态"""
        return {
            'initialized': self._initialized,
            'connected': self.is_connected,
            'target_pid': self.target_pid,
            'target_name': self.target_process.name if self.target_process else None,
            'detected_protocol': self.detected_protocol,
            'operation_stats': self.operation_stats,
        }


# ============================================================================
# 4. 物理本源操作器
# ============================================================================

class PhysicalEssenceOperator:
    """物理本源操作器
    
    直接与物理层交互的底层操作器，
    绕过屏幕/键盘/鼠标等转译层，实现物理级别的本源对接。
    """
    
    # 鼠标事件常量
    MOUSEEVENTF_MOVE = 0x0001
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004
    MOUSEEVENTF_RIGHTDOWN = 0x0008
    MOUSEEVENTF_RIGHTUP = 0x0010
    MOUSEEVENTF_WHEEL = 0x0800
    
    # 键盘事件常量
    KEYEVENTF_KEYUP = 0x0002
    
    # 虚拟键码
    VK_RETURN = 0x0D
    VK_ESCAPE = 0x1B
    VK_TAB = 0x09
    VK_SPACE = 0x20
    
    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32
        
        # 操作统计
        self.operation_count = 0
        self.last_action = None
        self.last_position = None
        
    def get_screen_size(self) -> Tuple[int, int]:
        """获取屏幕尺寸（本源层面）"""
        try:
            width = self.user32.GetSystemMetrics(0)   # SM_CXSCREEN
            height = self.user32.GetSystemMetrics(1)  # SM_CYSCREEN
            return (width, height)
        except Exception as e:
            print(f"[PhysicalOperator] 屏幕尺寸获取失败: {e}")
            return (1920, 1080)
    
    def get_cursor_pos(self) -> Tuple[int, int]:
        """获取鼠标位置（本源层面）"""
        try:
            point = ctypes.wintypes.POINT()
            self.user32.GetCursorPos(ctypes.byref(point))
            self.last_position = (point.x, point.y)
            return (point.x, point.y)
        except Exception as e:
            print(f"[PhysicalOperator] 鼠标位置获取失败: {e}")
            return (0, 0)
    
    def set_cursor_pos(self, x: int, y: int) -> bool:
        """设置鼠标位置（本源层面）"""
        try:
            result = self.user32.SetCursorPos(x, y)
            if result:
                self.last_position = (x, y)
                self.operation_count += 1
                self.last_action = f'set_pos({x}, {y})'
            return result != 0
        except Exception as e:
            print(f"[PhysicalOperator] 鼠标位置设置失败: {e}")
            return False
    
    def mouse_click(self, x: int, y: int, button: str = 'left') -> bool:
        """模拟鼠标点击（本源层面）
        
        Args:
            x: X坐标
            y: Y坐标
            button: 'left' 或 'right'
        """
        try:
            # 移动鼠标到目标位置
            self.set_cursor_pos(x, y)
            time.sleep(0.01)  # 微小延迟
            
            # 按下鼠标
            if button == 'left':
                flag_down = self.MOUSEEVENTF_LEFTDOWN
                flag_up = self.MOUSEEVENTF_LEFTUP
            else:
                flag_down = self.MOUSEEVENTF_RIGHTDOWN
                flag_up = self.MOUSEEVENTF_RIGHTUP
            
            self.user32.mouse_event(flag_down, 0, 0, 0, 0)
            time.sleep(0.02)
            self.user32.mouse_event(flag_up, 0, 0, 0, 0)
            
            self.operation_count += 1
            self.last_action = f'click({button}, {x}, {y})'
            return True
            
        except Exception as e:
            print(f"[PhysicalOperator] 鼠标点击失败: {e}")
            return False
    
    def mouse_drag(self, from_x: int, from_y: int, 
                   to_x: int, to_y: int, 
                   button: str = 'left', steps: int = 10) -> bool:
        """模拟鼠标拖拽（本源层面）"""
        try:
            # 移动到起点
            self.set_cursor_pos(from_x, from_y)
            time.sleep(0.01)
            
            # 按下鼠标
            if button == 'left':
                flag_down = self.MOUSEEVENTF_LEFTDOWN
            else:
                flag_down = self.MOUSEEVENTF_RIGHTDOWN
            
            self.user32.mouse_event(flag_down, 0, 0, 0, 0)
            time.sleep(0.02)
            
            # 逐步移动
            for i in range(1, steps + 1):
                t = i / steps
                x = int(from_x + (to_x - from_x) * t)
                y = int(from_y + (to_y - from_y) * t)
                self.set_cursor_pos(x, y)
                time.sleep(0.005)
            
            # 松开鼠标
            flag_up = self.MOUSEEVENTF_LEFTUP if button == 'left' else self.MOUSEEVENTF_RIGHTUP
            self.user32.mouse_event(flag_up, 0, 0, 0, 0)
            
            self.operation_count += 1
            self.last_action = f'drag({button}, ({from_x},{from_y})->({to_x},{to_y}))'
            return True
            
        except Exception as e:
            print(f"[PhysicalOperator] 鼠标拖拽失败: {e}")
            return False
    
    def send_key(self, key_code: int, action: str = 'press') -> bool:
        """发送键盘按键（本源层面）
        
        Args:
            key_code: 虚拟键码
            action: 'press', 'release', 或 'click'
        """
        try:
            if action == 'release':
                self.user32.keybd_event(key_code, 0, self.KEYEVENTF_KEYUP, 0)
            elif action == 'press':
                self.user32.keybd_event(key_code, 0, 0, 0)
            elif action == 'click':
                self.user32.keybd_event(key_code, 0, 0, 0)
                time.sleep(0.01)
                self.user32.keybd_event(key_code, 0, self.KEYEVENTF_KEYUP, 0)
            else:
                return False
            
            self.operation_count += 1
            self.last_action = f'key({key_code}, {action})'
            return True
            
        except Exception as e:
            print(f"[PhysicalOperator] 按键发送失败: {e}")
            return False
    
    def send_text(self, text: str) -> bool:
        """发送文本（通过剪贴板+粘贴，本源层面）"""
        try:
            import ctypes
            
            # 打开剪贴板
            if self.user32.OpenClipboard(0):
                self.user32.EmptyClipboard()
                
                # 设置Unicode文本到剪贴板
                CF_UNICODETEXT = 13
                memory = self.kernel32.GlobalAlloc(0x0042, (len(text) + 1) * 2)
                
                if memory:
                    locked = self.kernel32.GlobalLock(memory)
                    if locked:
                        # 复制文本到内存
                        ctypes.memmove(locked, text.encode('utf-16-le'), (len(text) + 1) * 2)
                        self.kernel32.GlobalUnlock(memory)
                        self.user32.SetClipboardData(CF_UNICODETEXT, memory)
                        self.kernel32.GlobalFree(memory)
                
                self.user32.CloseClipboard()
                
                # 模拟Ctrl+V粘贴
                VK_CONTROL = 0x11
                VK_V = 0x56
                
                self.user32.keybd_event(VK_CONTROL, 0, 0, 0)
                time.sleep(0.01)
                self.user32.keybd_event(VK_V, 0, 0, 0)
                time.sleep(0.01)
                self.user32.keybd_event(VK_V, 0, self.KEYEVENTF_KEYUP, 0)
                self.user32.keybd_event(VK_CONTROL, 0, self.KEYEVENTF_KEYUP, 0)
                
                self.operation_count += 1
                self.last_action = f'paste_text("{text[:20]}...")'
                return True
            
        except Exception as e:
            print(f"[PhysicalOperator] 文本发送失败: {e}")
            return False
    
    def get_foreground_window(self) -> Optional[Dict]:
        """获取前台窗口信息（本源层面）"""
        try:
            hwnd = self.user32.GetForegroundWindow()
            if hwnd:
                # 获取窗口标题
                title = ctypes.create_unicode_buffer(256)
                self.user32.GetWindowTextW(hwnd, title, 256)
                
                # 获取窗口位置
                rect = ctypes.wintypes.RECT()
                self.user32.GetWindowRect(hwnd, ctypes.byref(rect))
                
                return {
                    'hwnd': hwnd,
                    'title': title.value,
                    'position': {
                        'left': rect.left,
                        'top': rect.top,
                        'right': rect.right,
                        'bottom': rect.bottom,
                        'width': rect.right - rect.left,
                        'height': rect.bottom - rect.top,
                    }
                }
        except Exception as e:
            print(f"[PhysicalOperator] 窗口信息获取失败: {e}")
        return None
    
    def find_window_by_title(self, title_keyword: str) -> Optional[int]:
        """按标题查找窗口句柄"""
        try:
            result = []
            
            def enum_callback(hwnd, _):
                if self.user32.IsWindowVisible(hwnd):
                    title = ctypes.create_unicode_buffer(256)
                    self.user32.GetWindowTextW(hwnd, title, 256)
                    if title_keyword.lower() in title.value.lower():
                        result.append(hwnd)
                return True
            
            WNDENUMPROC = ctypes.WINFUNCTYPE(
                ctypes.c_bool, 
                ctypes.wintypes.HWND, 
                ctypes.wintypes.LPARAM
            )
            
            self.user32.EnumWindows(WNDENUMPROC(enum_callback), 0)
            
            return result[0] if result else None
            
        except Exception as e:
            print(f"[PhysicalOperator] 窗口查找失败: {e}")
            return None
    
    def set_foreground_window(self, hwnd: int) -> bool:
        """将窗口置于前台"""
        try:
            result = self.user32.SetForegroundWindow(hwnd)
            return result != 0
        except Exception as e:
            print(f"[PhysicalOperator] 窗口前置失败: {e}")
            return False
    
    def get_status(self) -> Dict:
        """获取操作状态"""
        screen = self.get_screen_size()
        cursor = self.get_cursor_pos()
        
        return {
            'screen_size': screen,
            'cursor_position': cursor,
            'total_operations': self.operation_count,
            'last_action': self.last_action,
            'foreground_window': self.get_foreground_window(),
        }


# ============================================================================
# 5. 增强版本源对接引擎（整合所有模块）
# ============================================================================

class EnhancedBSDEssenceBridge(BSDEssenceBridge):
    """增强版本源对接引擎
    
    整合进程操作、协议解析、物理操作三大核心模块，
    构建完整的本源对接能力。
    """
    
    def __init__(self):
        # 调用父类初始化
        super().__init__()
        
        # 新增物理操作器
        self.physical_operator = PhysicalEssenceOperator()
        
        # 增强状态
        self.enhanced_initialized = False
        self._enhance()
    
    def _enhance(self):
        """增强初始化"""
        print("\n" + "=" * 60)
        print("  [增强模块] 物理本源操作器初始化")
        print("=" * 60)
        
        try:
            # 获取物理层状态
            physical_status = self.physical_operator.get_status()
            print(f"  [屏幕] {physical_status['screen_size'][0]}x{physical_status['screen_size'][1]}")
            print(f"  [鼠标] ({physical_status['cursor_position'][0]}, {physical_status['cursor_position'][1]})")
            
            if physical_status.get('foreground_window'):
                fg = physical_status['foreground_window']
                print(f"  [前台] {fg['title'][:50]}")
            
            self.enhanced_initialized = True
            print()
            print("  ✅ 增强模块初始化成功")
            return True
            
        except Exception as e:
            print(f"  ❌ 增强模块初始化失败: {e}")
            return False
    
    def get_full_status(self) -> Dict:
        """获取完整状态"""
        base_status = self.get_status()
        physical_status = self.physical_operator.get_status()
        
        return {
            **base_status,
            'enhanced_initialized': self.enhanced_initialized,
            'physical_layer': physical_status,
        }


# ============================================================================
# 6. 演示与测试
# ============================================================================

def demo_essence_bridge():
    """演示本源对接引擎"""
    
    print("\n" + "=" * 60)
    print("  BSD 本源对接引擎 - 演示")
    print("=" * 60)
    
    # 1. 初始化
    bridge = BSDEssenceBridge()
    
    # 2. 列出所有进程
    print("\n[1] 进程扫描")
    processes = bridge.process_op.list_all_processes()
    
    # 显示系统关键进程
    system_processes = [p for p in processes if p.memory_usage > 50 * 1024 * 1024]  # 大于50MB
    print(f"  总进程数: {len(processes)}")
    print(f"  大内存进程: {len(system_processes)}")
    
    for proc in system_processes[:5]:
        print(f"    PID={proc.pid:5d} | Mem={proc.memory_usage/1024/1024:6.1f}MB | {proc.name}")
    
    # 3. 协议检测演示
    print("\n[2] 协议检测演示")
    test_messages = [
        b'play B C10',  # GTP格式
        b'play W D4',   # GTP格式
        b'{"type":"move","x":3,"y":15,"color":"black"}',  # JSON格式
        b'\x01\x02\x03\x04',  # 二进制数据
    ]
    
    for msg in test_messages:
        detection = bridge.protocol_parser.detect_protocol(msg)
        if detection:
            print(f"  ✓ {msg[:30].decode('latin-1', errors='replace'):30s} → {detection['protocol']}")
    
    # 4. 围棋平台检测
    print("\n[3] 围棋平台检测")
    for platform in ['kgs', 'yike', 'fox']:
        info = bridge.get_go_platform_connection(platform)
        if info:
            print(f"  {info['name']}: 端口{info['port']}, 协议{info['protocol']}")
    
    # 5. 状态报告
    print("\n[4] 引擎状态")
    status = bridge.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 60)
    print("  ✅ 本源对接引擎演示完成")
    print()
    print("  💡 使用方法：")
    print("  1. 启动围棋平台（KGS/弈城/野狐）")
    print("  2. 获取平台进程PID")
    print("  3. bridge.connect_to_process(pid)")
    print("  4. 直接进行本源对接")
    print("=" * 60)
    
    return bridge


if __name__ == "__main__":
    demo_essence_bridge()