"""检测可用的硬件控制库"""
import sys
import importlib

libs = ['pyautogui', 'PIL', 'cv2', 'pygetwindow', 'pytesseract', 'numpy']

for lib in libs:
    try:
        importlib.import_module(lib)
        print(f'{lib}: OK')
    except:
        print(f'{lib}: NOT FOUND')

print("\n检查Windows API能力:")
try:
    import ctypes
    print("ctypes: OK (可调用Windows API)")
except:
    print("ctypes: NOT FOUND")

try:
    import win32gui
    print("win32gui: OK")
except:
    print("win32gui: NOT FOUND")

try:
    import win32api
    print("win32api: OK")
except:
    print("win32api: NOT FOUND")