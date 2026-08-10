"""测试KataGo直接启动"""
import subprocess
import os
import sys
import time

exe = r"c:\Users\13003\OneDrive\桌面\3333333\go_ai_tools\katago\katago.exe"
model = r"c:\Users\13003\OneDrive\桌面\3333333\go_ai_tools\katago\default_model.bin.gz"
cfg = r"c:\Users\13003\OneDrive\桌面\3333333\go_ai_tools\katago\default_gtp.cfg"

# 初始化Winsock
if sys.platform == "win32":
    import ctypes
    try:
        ws2_32 = ctypes.windll.ws2_32
        ws2_32.WSAStartup(0x0202, ctypes.byref(ctypes.c_void_p()))
        print("Winsock初始化成功")
    except Exception as e:
        print(f"Winsock初始化失败: {e}")

# 尝试简单的命令
print("启动KataGo...")
try:
    cmd = [exe, "gtp", "-model", model, "-config", cfg, "-override-config", "logToStderr=false"]
    cmd_str = " ".join(cmd[:5]) + " ..."
    print(f"命令: {cmd_str}")
    
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    time.sleep(3)
    
    if process.poll() is None:
        print("KataGo启动成功!")
        
        # 发送name命令
        process.stdin.write("1 name\n")
        process.stdin.flush()
        time.sleep(0.5)
        
        response = []
        start = time.time()
        while time.time() - start < 2:
            line = process.stdout.readline()
            if line:
                response.append(line.rstrip())
                if line.strip() == "":
                    break
            else:
                break
        
        print(f"name响应: {response}")
        
        # 发送boardsize命令
        process.stdin.write("2 boardsize 9\n")
        process.stdin.flush()
        time.sleep(0.5)
        
        response2 = []
        start = time.time()
        while time.time() - start < 2:
            line = process.stdout.readline()
            if line:
                response2.append(line.rstrip())
                if line.strip() == "":
                    break
            else:
                break
        
        print(f"boardsize响应: {response2}")
        
        # 发送genmove命令
        print("请求落子(思考5秒)...")
        process.stdin.write("3 genmove black\n")
        process.stdin.flush()
        time.sleep(6)
        
        response3 = []
        start = time.time()
        while time.time() - start < 3:
            line = process.stdout.readline()
            if line:
                response3.append(line.rstrip())
                if line.strip() == "":
                    break
            else:
                break
        
        print(f"genmove响应: {response3}")
        
        # 退出
        process.stdin.write("4 quit\n")
        process.stdin.flush()
        process.wait(timeout=5)
        print("KataGo已退出")
        
    else:
        # 读取错误输出
        stderr = process.stderr.read()
        print(f"KataGo启动失败!")
        print(f"错误输出: {stderr[:1000]}")
        print(f"退出码: {process.returncode}")
        
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
