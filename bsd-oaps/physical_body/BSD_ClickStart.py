"""
点击本源端 Trae CN 的 "开始" 按钮进入系统
"""
import ctypes, time

user32 = ctypes.windll.user32

# 获取屏幕尺寸
screen_w = user32.GetSystemMetrics(0)
screen_h = user32.GetSystemMetrics(1)
print(f"屏幕: {screen_w}x{screen_h}")

# 点击中央偏下的"开始"按钮位置 (根据截图位置估算)
# "开始"按钮大致位于屏幕中央
x = screen_w // 2
y = int(screen_h * 0.75)

print(f"点击位置: ({x}, {y})")

# 移动鼠标
user32.SetCursorPos(x, y)
time.sleep(0.1)

# 点击
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
time.sleep(0.02)
user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
print("✓ 已点击")
