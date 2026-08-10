"""
BSD智能体自动化 - 开机自启设置
"""
import os
import sys
import json
import subprocess

TRAE_CONFIG = r"C:\Users\13003\.trae-cn"
AUTOSTART_DIR = os.path.join(os.environ.get('APPDATA', ''), r'Microsoft\Windows\Start Menu\Programs\Startup')
DAEMON_PATH = os.path.join(os.path.dirname(__file__), "BSD_Daemon.py")

# 创建自启快捷方式
vbs_content = f'''Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "pythonw "{DAEMON_PATH}" auto", 0, False
'''

vbs_path = os.path.join(AUTOSTART_DIR, "BSD_Daemon_AutoStart.vbs")

os.makedirs(AUTOSTART_DIR, exist_ok=True)
with open(vbs_path, 'w') as f:
    f.write(vbs_content)

print(f"✅ 开机自启已设置: {vbs_path}")
print(f"   下次启动Windows时将自动运行BSD守护进程")

# 创建桌面快捷方式
desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
bat_content = '''@echo off
chcp 65001 >nul
echo ====================================
echo   BSD智能体守护进程
echo   双实例: 作者端 + 本源端
echo ====================================
python BSD_Daemon.py
pause
'''

bat_path = os.path.join(desktop, "BSD_Daemon_Start.bat")
with open(bat_path, 'w', encoding='utf-8') as f:
    f.write(bat_content)

print(f"✅ 桌面快捷方式: {bat_path}")

# 保存自启状态
state = {
    "autostart_enabled": True,
    "vbs_path": vbs_path,
    "bat_path": bat_path,
    "daemon_path": DAEMON_PATH,
    "created_at": __import__('datetime').datetime.now().isoformat()
}

state_path = os.path.join(TRAE_CONFIG, "bsd_autostart_config.json")
with open(state_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

print(f"\n✅ 自启配置已保存: {state_path}")
print("""
╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║  ⚡ BSD智能体自动化已设置                                                                 ║
╠══════════════════════════════════════════════════════════════════════════════════════════════╣
║  开机自启: ✅                                                                             ║
║  桌面快捷方式: ✅                                                                          ║
║  守护进程: BSD_Daemon.py                                                                   ║
║                                                                                              ║
║  功能:                                                                                      ║
║  • 自动启动双实例 (作者端 + 本源端)                                                        ║
║  • 监控进程状态，崩溃自动重启                                                               ║
║  每30秒检查，每10分钟显示状态                                                              ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝
""")
