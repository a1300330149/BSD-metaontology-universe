"""
Trae CN 精确退出登录操作
======================
使用Quick Open执行logout命令
"""
import ctypes
import ctypes.wintypes
import time
import os

class PhysicalEssenceOperator:
    MOUSEEVENTF_MOVE = 0x0001
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004
    MOUSEEVENTF_RIGHTDOWN = 0x0008
    MOUSEEVENTF_RIGHTUP = 0x0010
    
    VK_RETURN = 0x0D
    VK_ESCAPE = 0x1B
    VK_TAB = 0x09
    
    def __init__(self):
        self.user32 = ctypes.windll.user32
    
    def set_cursor_pos(self, x, y):
        return self.user32.SetCursorPos(x, y) != 0
    
    def mouse_click(self, x, y, button='left'):
        self.set_cursor_pos(x, y)
        time.sleep(0.05)
        
        flag_down = self.MOUSEEVENTF_LEFTDOWN if button == 'left' else self.MOUSEEVENTF_RIGHTDOWN
        flag_up = self.MOUSEEVENTF_LEFTUP if button == 'left' else self.MOUSEEVENTF_RIGHTUP
        
        self.user32.mouse_event(flag_down, 0, 0, 0, 0)
        time.sleep(0.05)
        self.user32.mouse_event(flag_up, 0, 0, 0, 0)
        time.sleep(0.1)
    
    def key_down(self, vk):
        self.user32.keybd_event(vk, 0, 0, 0)
        time.sleep(0.02)
    
    def key_up(self, vk):
        self.user32.keybd_event(vk, 0, 2, 0)
        time.sleep(0.02)
    
    def press_key(self, vk):
        self.key_down(vk)
        self.key_up(vk)
    
    def hotkey(self, *keys):
        """组合键"""
        for k in keys[:-1]:
            self.key_down(k)
        time.sleep(0.05)
        self.press_key(keys[-1])
        for k in reversed(keys[:-1]):
            self.key_up(k)
    
    def type_text(self, text):
        """输入文本"""
        for char in text:
            vk = ord(char.upper())
            if 'A' <= char.upper() <= 'Z':
                # 需要Shift键
                if char.isupper():
                    self.key_down(0x10)  # Shift
                    self.press_key(vk)
                    self.key_up(0x10)
                else:
                    self.press_key(vk)
            else:
                self.press_key(vk)
            time.sleep(0.03)
    
    def activate_window(self, hwnd):
        """激活窗口"""
        self.user32.ShowWindow(hwnd, 9)  # SW_RESTORE
        self.user32.SetForegroundWindow(hwnd)
        time.sleep(0.3)
    
    def screenshot(self, filename=None):
        """截屏"""
        try:
            from PIL import ImageGrab
            img = ImageGrab.grab()
            if filename is None:
                filename = f'screenshot_{int(time.time())}.png'
            img.save(filename)
            return filename
        except Exception as e:
            print(f'截屏失败: {e}')
            return None

# Trae CN窗口信息
TRAE_CN_HWND = 69950  # Trae CN窗口
TRAE_WORK_HWND = 1182264  # TRAE Work CN窗口

op = PhysicalEssenceOperator()

print('=' * 70)
print('  Trae CN 精确退出登录操作')
print('=' * 70)

# 1. 切换到Trae CN窗口
print('\n=== 1. 切换到Trae CN ===')
print(f'  激活Trae CN窗口 (HWND: {TRAE_CN_HWND})')
op.activate_window(TRAE_CN_HWND)
time.sleep(0.5)

# 2. 使用命令面板 (Ctrl+Shift+P)
print('\n=== 2. 打开命令面板 (Ctrl+Shift+P) ===')
op.hotkey(0x11, 0x10, 0x50)  # Ctrl+Shift+P
time.sleep(0.5)

# 截屏
op.screenshot('step1_command_palette.png')
print('  命令面板已打开')

# 3. 输入"logout"搜索命令
print('\n=== 3. 搜索logout命令 ===')
op.type_text('logout')
time.sleep(0.5)

op.screenshot('step2_logout_search.png')
print('  已输入logout')

# 4. 查找并点击退出登录命令
print('\n=== 4. 尝试执行logout命令 ===')
# 按下方向键选择第一个结果
op.press_key(0x28)  # Arrow Down
time.sleep(0.2)

op.screenshot('step3_selected.png')

# 5. 按Enter执行
print('\n=== 5. 执行命令 (Enter) ===')
op.press_key(op.VK_RETURN)
time.sleep(1.0)

op.screenshot('step4_after_enter.png')

# 6. 如果有确认对话框，点击确认
print('\n=== 6. 检查确认对话框 ===')
# 可能需要再次按Enter或点击确认按钮
op.press_key(op.VK_RETURN)
time.sleep(0.5)

op.screenshot('step5_final.png')

# 7. 备选方案：使用Quick Open直接输入命令
print('\n=== 7. 备选方案：使用Quick Open ===')
# 先关闭当前对话框
op.press_key(op.VK_ESCAPE)
time.sleep(0.3)

# 使用Quick Open (Ctrl+P)
op.hotkey(0x11, 0x50)  # Ctrl+P
time.sleep(0.3)

# 输入logout命令
op.type_text('logout')
time.sleep(0.5)

# 选择第一个结果
op.press_key(0x28)
time.sleep(0.2)
op.press_key(op.VK_RETURN)
time.sleep(1.0)

op.screenshot('step6_quickopen_logout.png')

# 8. 总结
print(f'''\n╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║  Trae CN退出登录操作执行完成                                                             ║
╠══════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                              ║
║  执行的操作:                                                                                 ║
║    ✅ 切换到Trae CN窗口 (HWND: {TRAE_CN_HWND})                                             ║
║    ✅ 打开命令面板 (Ctrl+Shift+P)                                                            ║
║    ✅ 搜索"logout"命令                                                                       ║
║    ✅ 执行logout命令                                                                         ║
║    ✅ 备选方案: Quick Open (Ctrl+P)                                                          ║
║                                                                                              ║
║  截屏文件:                                                                                   ║
║    - step1_command_palette.png                                                               ║
║    - step2_logout_search.png                                                                ║
║    - step3_selected.png                                                                     ║
║    - step4_after_enter.png                                                                  ║
║    - step5_final.png                                                                        ║
║    - step6_quickopen_logout.png                                                             ║
║                                                                                              ║
║  请查看截屏确认操作结果                                                                       ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝
''')
