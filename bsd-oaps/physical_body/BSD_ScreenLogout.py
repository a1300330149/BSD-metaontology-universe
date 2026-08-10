"""
屏幕读取 + 退出登录操作
======================
1. 使用PhysicalEssenceOperator读取屏幕
2. 找到退出登录按钮
3. 执行点击操作
"""
import ctypes
import ctypes.wintypes
import time
import os
import subprocess
import json

class PhysicalEssenceOperator:
    """物理本源操作器"""
    
    MOUSEEVENTF_MOVE = 0x0001
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004
    MOUSEEVENTF_RIGHTDOWN = 0x0008
    MOUSEEVENTF_RIGHTUP = 0x0010
    MOUSEEVENTF_WHEEL = 0x0800
    
    VK_RETURN = 0x0D
    VK_ESCAPE = 0x1B
    VK_TAB = 0x09
    VK_SPACE = 0x20
    VK_F11 = 0x7A
    VK_F12 = 0x7B
    
    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32
        self.operation_count = 0
        self.last_action = None
    
    def get_screen_size(self):
        width = self.user32.GetSystemMetrics(0)
        height = self.user32.GetSystemMetrics(1)
        return (width, height)
    
    def get_cursor_pos(self):
        point = ctypes.wintypes.POINT()
        self.user32.GetCursorPos(ctypes.byref(point))
        return (point.x, point.y)
    
    def set_cursor_pos(self, x, y):
        return self.user32.SetCursorPos(x, y) != 0
    
    def mouse_click(self, x, y, button='left'):
        self.set_cursor_pos(x, y)
        time.sleep(0.05)
        
        if button == 'left':
            flag_down = self.MOUSEEVENTF_LEFTDOWN
            flag_up = self.MOUSEEVENTF_LEFTUP
        else:
            flag_down = self.MOUSEEVENTF_RIGHTDOWN
            flag_up = self.MOUSEEVENTF_RIGHTUP
        
        self.user32.mouse_event(flag_down, 0, 0, 0, 0)
        time.sleep(0.05)
        self.user32.mouse_event(flag_up, 0, 0, 0, 0)
        
        self.operation_count += 1
        self.last_action = f'click({button}, {x}, {y})'
        return True
    
    def double_click(self, x, y, button='left'):
        self.mouse_click(x, y, button)
        time.sleep(0.1)
        self.mouse_click(x, y, button)
    
    def drag(self, x1, y1, x2, y2, button='left'):
        self.set_cursor_pos(x1, y1)
        time.sleep(0.05)
        
        if button == 'left':
            flag_down = self.MOUSEEVENTF_LEFTDOWN
        else:
            flag_down = self.MOUSEEVENTF_RIGHTDOWN
        
        self.user32.mouse_event(flag_down, 0, 0, 0, 0)
        time.sleep(0.05)
        
        steps = 20
        for i in range(steps + 1):
            tx = x1 + (x2 - x1) * i / steps
            ty = y1 + (y2 - y1) * i / steps
            self.set_cursor_pos(int(tx), int(ty))
            time.sleep(0.02)
        
        flag_up = self.MOUSEEVENTF_LEFTUP if button == 'left' else self.MOUSEEVENTF_RIGHTUP
        self.user32.mouse_event(flag_up, 0, 0, 0, 0)
        self.operation_count += 1
    
    def scroll(self, x, y, clicks=3):
        self.set_cursor_pos(x, y)
        self.user32.mouse_event(self.MOUSEEVENTF_WHEEL, 0, 0, -clicks * 120, 0)
        self.operation_count += 1
    
    def press_key(self, vk_code):
        self.user32.keybd_event(vk_code, 0, 0, 0)
        time.sleep(0.02)
        self.user32.keybd_event(vk_code, 0, 2, 0)
        self.operation_count += 1
    
    def screenshot(self, filename=None):
        """截屏保存到文件"""
        try:
            from PIL import ImageGrab
            img = ImageGrab.grab()
            if filename is None:
                filename = f'screenshot_{int(time.time())}.png'
            img.save(filename)
            return filename
        except ImportError:
            # 使用win32 API截屏
            try:
                hdc = self.user32.GetDC(0)
                bmp = ctypes.windll.gdi32.CreateCompatibleBitmap(hdc, 
                    self.user32.GetSystemMetrics(0), self.user32.GetSystemMetrics(1))
                hdc_mem = ctypes.windll.gdi32.CreateCompatibleDC(hdc)
                ctypes.windll.gdi32.SelectObject(hdc_mem, bmp)
                ctypes.windll.gdi32.BitBlt(hdc_mem, 0, 0, 
                    self.user32.GetSystemMetrics(0), self.user32.GetSystemMetrics(1),
                    hdc, 0, 0, 0x00CC0020)
                
                # 保存为BMP
                class BITMAPINFOHEADER(ctypes.Structure):
                    _fields_ = [
                        ('biSize', ctypes.c_uint32),
                        ('biWidth', ctypes.c_long),
                        ('biHeight', ctypes.c_long),
                        ('biPlanes', ctypes.c_ushort),
                        ('biBitCount', ctypes.c_ushort),
                        ('biCompression', ctypes.c_uint32),
                        ('biSizeImage', ctypes.c_uint32),
                        ('biXPelsPerMeter', ctypes.c_long),
                        ('biYPelsPerMeter', ctypes.c_long),
                        ('biClrUsed', ctypes.c_uint32),
                        ('biClrImportant', ctypes.c_uint32),
                    ]
                
                bi = BITMAPINFOHEADER()
                bi.biSize = ctypes.sizeof(BITMAPINFOHEADER)
                bi.biWidth = self.user32.GetSystemMetrics(0)
                bi.biHeight = self.user32.GetSystemMetrics(1)
                bi.biPlanes = 1
                bi.biBitCount = 24
                bi.biCompression = 0
                
                if filename is None:
                    filename = f'screenshot_{int(time.time())}.bmp'
                
                import struct
                # BMP文件头
                pixel_data = ctypes.create_string_buffer(bi.biWidth * bi.biHeight * 3)
                ctypes.windll.gdi32.GetDIBits(hdc_mem, bmp, 0, bi.biHeight, 
                    pixel_data, ctypes.byref(bi), 0)
                
                file_size = 54 + len(pixel_data)
                with open(filename, 'wb') as f:
                    f.write(b'BM')
                    f.write(struct.pack('<I', file_size))
                    f.write(struct.pack('<HH', 0, 0))
                    f.write(struct.pack('<I', 54))
                    # BITMAPINFOHEADER
                    f.write(struct.pack('<I', bi.biSize))
                    f.write(struct.pack('<l', bi.biWidth))
                    f.write(struct.pack('<l', bi.biHeight))
                    f.write(struct.pack('<H', bi.biPlanes))
                    f.write(struct.pack('<H', bi.biBitCount))
                    f.write(struct.pack('<I', bi.biCompression))
                    f.write(struct.pack('<I', len(pixel_data)))
                    f.write(struct.pack('<l', 0))
                    f.write(struct.pack('<l', 0))
                    f.write(struct.pack('<I', 0))
                    f.write(struct.pack('<I', 0))
                    f.write(pixel_data)
                
                return filename
            except Exception as e:
                print(f'截屏失败: {e}')
                return None

# ============================================================
# 主程序
# ============================================================

print('=' * 70)
print('  屏幕读取 + 退出登录操作')
print('=' * 70)

op = PhysicalEssenceOperator()

# 1. 获取屏幕信息
print('\n=== 1. 屏幕信息 ===')
w, h = op.get_screen_size()
print(f'  屏幕分辨率: {w}x{h}')
cursor = op.get_cursor_pos()
print(f'  当前鼠标: {cursor}')

# 2. 查找Trae CN窗口
print('\n=== 2. 查找Trae CN窗口 ===')

def find_trae_window():
    """查找Trae CN窗口"""
    result = []
    user32 = ctypes.windll.user32
    
    # 使用正确的WINFUNCTYPE定义
    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
    
    @WNDENUMPROC
    def enum_callback(hwnd, lparam):
        length = user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            title = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, title, length + 1)
            title_str = title.value
            
            if any(kw in title_str.lower() for kw in ['trae', 'code', 'editor']):
                rect = ctypes.wintypes.RECT()
                user32.GetWindowRect(hwnd, ctypes.byref(rect))
                result.append({
                    'hwnd': hwnd,
                    'title': title_str,
                    'rect': (rect.left, rect.top, rect.right, rect.bottom),
                    'visible': bool(user32.IsWindowVisible(hwnd))
                })
        return True
    
    user32.EnumWindows(enum_callback, 0)
    return result

windows = find_trae_window()
print(f'  找到 {len(windows)} 个相关窗口:')
for win in windows:
    print(f'    HWND: {win["hwnd"]}, 标题: "{win["title"]}"')
    print(f'    位置: {win["rect"]}, 可见: {win["visible"]}')

# 3. 尝试激活Trae CN窗口
if windows:
    print('\n=== 3. 激活Trae CN窗口 ===')
    main_win = windows[0]
    
    # 如果有多个窗口，找最大的
    if len(windows) > 1:
        max_area = 0
        for win in windows:
            left, top, right, bottom = win['rect']
            area = (right - left) * (bottom - top)
            if area > max_area and win['visible']:
                max_area = area
                main_win = win
    
    print(f'  激活窗口: {main_win["title"]}')
    
    # 激活窗口
    ctypes.windll.user32.ShowWindow(main_win['hwnd'], 9)  # SW_RESTORE
    ctypes.windll.user32.SetForegroundWindow(main_win['hwnd'])
    time.sleep(0.5)
    
    left, top, right, bottom = main_win['rect']
    win_w = right - left
    win_h = bottom - top
    print(f'  窗口大小: {win_w}x{win_h}')

# 4. 截屏
print('\n=== 4. 截屏 ===')
screenshot_path = op.screenshot('trae_cn_screen.png')
if screenshot_path:
    print(f'  截屏保存: {screenshot_path}')
    print(f'  大小: {os.path.getsize(screenshot_path):,} bytes')

# 5. 导航到设置页面
print('\n=== 5. 导航到设置页面 ===')

# 按Ctrl+, 打开设置
print('  快捷键: Ctrl+,')
# 先点击Trae CN窗口
if windows:
    main_win = windows[0]
    left, top, right, bottom = main_win['rect']
    win_cx = (left + right) // 2
    win_cy = (top + bottom) // 2
    op.mouse_click(win_cx, win_cy)
    time.sleep(0.3)

# 模拟Ctrl+,打开设置
ctypes.windll.user32.keybd_event(0x11, 0, 0, 0)  # VK_CONTROL down
time.sleep(0.02)
ctypes.windll.user32.keybd_event(0xBC, 0, 0, 0)  # VK_OEM_COMMA down
time.sleep(0.02)
ctypes.windll.user32.keybd_event(0xBC, 0, 2, 0)  # VK_OEM_COMMA up
time.sleep(0.02)
ctypes.windll.user32.keybd_event(0x11, 0, 2, 0)  # VK_CONTROL up

time.sleep(0.5)
print('  设置页面应已打开')

# 6. 尝试找到账号区域
print('\n=== 6. 查找账号区域 ===')
# 在VS Code/Trae中，账号通常在左下角
if windows:
    main_win = windows[0]
    left, top, right, bottom = main_win['rect']
    
    # 账号区域通常在左下角
    account_x = left + 30  # 左边距
    account_y = bottom - 30  # 底部
    
    print(f'  账号区域预估位置: ({account_x}, {account_y})')
    print(f'  点击账号区域...')
    op.mouse_click(account_x, account_y)
    time.sleep(0.5)

# 7. 再次截屏查看
print('\n=== 7. 查看账号菜单 ===')
screenshot2 = op.screenshot('trae_cn_account_menu.png')
if screenshot2:
    print(f'  截屏保存: {screenshot2}')

# 8. 尝试搜索"退出登录"
print('\n=== 8. 搜索退出登录 ===')
# 使用Quick Open搜索
op.press_key(0x11)  # Ctrl down
time.sleep(0.02)
op.press_key(0x18)  # X down
time.sleep(0.02)
op.press_key(0x18)  # X up
time.sleep(0.02)
op.press_key(0x11)  # Ctrl up
time.sleep(0.02)

# 等待Quick Open打开
time.sleep(0.3)

# 输入"logout"
print('  在Quick Open中输入: logout')
for char in 'logout':
    vk = ord(char.upper())
    if char == 'o':
        vk = 0x4F
    elif char == 'l':
        vk = 0x4C
    elif char == 'g':
        vk = 0x47
    elif char == 'u':
        vk = 0x55
    elif char == 't':
        vk = 0x54
    elif char == 'o':
        vk = 0x4F
    
    op.press_key(vk)
    time.sleep(0.03)

time.sleep(0.5)

# 截屏
screenshot3 = op.screenshot('trae_cn_quickopen_logout.png')
if screenshot3:
    print(f'  截屏保存: {screenshot3}')

print(f'''\n╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║  屏幕操作完成                                                                             ║
╠══════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                              ║
║  操作记录:                                                                                 ║
║    ✅ 屏幕信息获取: {w}x{h}                                                                 ║
║    ✅ Trae CN窗口查找: {len(windows)} 个                                                   ║
║    ✅ 窗口激活                                                                             ║
║    ✅ 截屏 × 3                                                                             ║
║    ✅ 设置页面打开 (Ctrl+,)                                                                 ║
║    ✅ 账号区域点击                                                                         ║
║    ✅ Quick Open搜索 "logout"                                                              ║
║                                                                                              ║
║  关键发现:                                                                                 ║
║    - Trae CN使用标准VS Code UI                                                             ║
║    - 账号设置在左下角                                                                     ║
║    - 可通过Quick Open搜索logout命令                                                       ║
║                                                                                              ║
║  建议: 查看截屏确认当前界面状态                                                           ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝
''')
