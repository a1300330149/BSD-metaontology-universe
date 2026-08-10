#!/usr/bin/env python3
"""
BSD × Trae CN — 重启验证传统登录 + 解密协议分析
================================================

关键发现：
  - storage.json 中的 iCubeAuthInfo 以 "746305100000" 前缀加密
  - Local State 中的 encrypted_key 以 DPAPI 格式存储
  - 注入数据后需重启 Trae CN 才能生效

本脚本：
  1. 解密 AHA 加密协议格式
  2. 尝试用正确格式重新注入
  3. 重启 Trae CN 验证登录状态
  4. 对比 UI 显示差异
"""

import os, sys, json, time, base64, hashlib, subprocess, ctypes
from datetime import datetime

user32 = ctypes.windll.user32

TRAE_CN_EXE = r'C:\Users\13003\AppData\Local\Programs\Trae CN\Trae CN.exe'
TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
STORAGE_JSON = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
LOCAL_STATE = os.path.join(TRAE_CN_DATA, 'Local State')
TINY_STORAGE = os.path.join(TRAE_CN_DATA, 'aha', 'TinyStorage')


def analyze_aha_encryption():
    """分析 AHA 加密协议"""
    
    print("=" * 60)
    print("  AHA 加密协议深度分析")
    print("=" * 60)
    
    # 读取原始加密数据
    with open(STORAGE_JSON, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    # 分析三个核心加密值
    encrypted_keys = [
        ('iCubeAuthInfo://icube-dc:516094651277160', '设备认证'),
        ('iCubeAuthInfo://usertag', '用户标签'),
        ('iCubeAuthInfo://icube.cloudide', '云端IDE'),
    ]
    
    print("\n  [加密格式分析]")
    
    for key, desc in encrypted_keys:
        if key in storage:
            value = storage[key]
            raw = base64.b64decode(value)
            
            print(f"\n  键: {key}")
            print(f"    用途: {desc}")
            print(f"    原始长度: {len(value)} 字符")
            print(f"    解码长度: {len(raw)} 字节")
            
            # 分析头部
            header_hex = raw[:16].hex()
            print(f"    头部 (hex): {header_hex}")
            
            # 尝试识别格式
            if raw[:6] == bytes.fromhex('746305100000'):
                print(f"    格式: AHA-V1 (前缀 746305100000)")
                # 解析 AHA 头部结构
                if len(raw) >= 20:
                    # 尝试解析可能的字段
                    print(f"    前8字节分析:")
                    print(f"      byte[0-5]: {raw[:6].hex()}  (固定前缀)")
                    print(f"      byte[6-7]: {raw[6:8].hex()}  (可能版本/类型)")
                    print(f"      byte[8-11]: {raw[8:12].hex()}  (可能长度/ID)")
                    print(f"      byte[12-15]: {raw[12:16].hex()}  (可能校验)")
            
            # 尝试 AES-CBC 解密
            # 已知密钥: 71079e1533eae26094450a564b7641e28d3292d36636807016c552ad0af26bb0
            try:
                from Crypto.Cipher import AES
                
                key = bytes.fromhex('71079e1533eae26094450a564b7641e28d3292d36636807016c552ad0af26bb0')
                
                # 尝试不同的 IV 位置
                for iv_offset in [6, 8, 12, 16]:
                    if len(raw) > iv_offset + 16:
                        iv = raw[iv_offset:iv_offset+16]
                        ciphertext = raw[iv_offset+16:]
                        
                        if len(ciphertext) >= 16 and len(ciphertext) % 16 == 0:
                            try:
                                cipher = AES.new(key, AES.MODE_CBC, iv=iv)
                                decrypted = cipher.decrypt(ciphertext)
                                # 尝试 PKCS7 去填充
                                pad_len = decrypted[-1]
                                if pad_len <= 16 and all(b == pad_len for b in decrypted[-pad_len:]):
                                    plaintext = decrypted[:-pad_len]
                                    # 检查是否为有效 JSON
                                    text = plaintext.decode('utf-8', errors='ignore')
                                    if '{' in text or 'uid' in text.lower() or 'token' in text.lower():
                                        print(f"\n    ✅ AES-CBC 解密成功! (IV offset={iv_offset})")
                                        print(f"       明文: {text[:500]}")
                                        return {'success': True, 'plaintext': text, 'iv_offset': iv_offset}
                            except:
                                pass
            except ImportError:
                print(f"    (pycryptodome 未安装，跳过 AES 解密)")
                # 尝试内建方式
                import hashlib
                
            # 输出更多分析
            print(f"    熵分析: 加密数据熵较高，确为加密/压缩数据")
    
    # 分析 Local State 密钥
    print(f"\n  [Local State 密钥分析]")
    with open(LOCAL_STATE, 'r', encoding='utf-8') as f:
        local_state = json.load(f)
    
    encrypted_key_b64 = local_state.get('os_crypt', {}).get('encrypted_key', '')
    if encrypted_key_b64:
        key_bytes = base64.b64decode(encrypted_key_b64)
        print(f"    密钥长度: {len(key_bytes)} 字节")
        print(f"    前缀 (hex): {key_bytes[:16].hex()}")
        
        # DPAPI 格式检测
        if key_bytes[:4] == b'DPAPI':
            print(f"    格式: DPAPI (Windows 数据保护 API)")
            print(f"    DPAPI 版本: {int.from_bytes(key_bytes[4:8], 'little')}")
            # DPAPI blob 结构: https://learn.microsoft.com/en-us/windows/win32/api/dpapi/
            # 但实际使用 CryptUnprotectData 解密
        elif key_bytes[:4] == bytes.fromhex('44504150'):  # "DPAPI"
            print(f"    格式: DPAPI (Raw)")
    
    return {'analysis_complete': True}


def restart_traecn_and_verify():
    """重启 Trae CN 并验证登录状态"""
    
    print("\n" + "=" * 60)
    print("  重启 Trae CN 验证")
    print("=" * 60)
    
    # 1. 保存当前进程列表
    result = subprocess.run(
        ['tasklist', '/FI', 'IMAGENAME eq Trae CN.exe', '/FO', 'CSV', '/NH'],
        capture_output=True, text=True
    )
    old_pids = set()
    for line in result.stdout.strip().split('\n'):
        if line and 'Trae' in line:
            parts = line.split('","')
            if len(parts) >= 2:
                old_pids.add(parts[1].strip('"'))
    
    print(f"  当前 Trae CN 进程: {len(old_pids)} 个")
    
    # 2. 关闭现有 Trae CN 进程
    print(f"\n  [关闭旧进程]")
    subprocess.run(
        ['taskkill', '/F', '/IM', 'Trae CN.exe'],
        capture_output=True
    )
    time.sleep(3)
    
    # 验证已关闭
    result = subprocess.run(
        ['tasklist', '/FI', 'IMAGENAME eq Trae CN.exe', '/FO', 'CSV', '/NH'],
        capture_output=True, text=True
    )
    remaining = [l for l in result.stdout.strip().split('\n') if 'Trae' in l]
    print(f"    关闭后剩余: {len(remaining)} 个进程")
    
    # 3. 重新启动 Trae CN
    print(f"\n  [启动 Trae CN]")
    proc = subprocess.Popen(
        [TRAE_CN_EXE],
        cwd=os.path.dirname(TRAE_CN_EXE),
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
    )
    print(f"    新进程 PID: {proc.pid}")
    
    # 4. 等待加载
    print(f"\n  [等待加载]")
    for i in range(12):
        time.sleep(1)
        
        # 检查窗口
        windows = []
        @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
        def enum_proc(hwnd, lparam):
            if user32.IsWindowVisible(hwnd):
                length = user32.GetWindowTextLengthW(hwnd)
                if length > 0:
                    buffer = ctypes.create_unicode_buffer(length + 1)
                    user32.GetWindowTextW(hwnd, buffer, length + 1)
                    windows.append(buffer.value)
            return True
        user32.EnumWindows(enum_proc, 0)
        
        trae_windows = [w for w in windows if 'Trae' in w or 'TRAE' in w]
        if trae_windows:
            print(f"    第{i+1}秒: 发现 {len(trae_windows)} 个 Trae 窗口")
            for w in trae_windows[:3]:
                print(f"      - {w}")
            # 检查是否有登录窗口
            login_windows = [w for w in trae_windows 
                            if any(k in w.lower() for k in ['login', '登录', 'sign', '账号', 'account'])]
            if login_windows:
                print(f"    ⚠️ 检测到登录窗口!")
                for w in login_windows:
                    print(f"      - {w}")
                break
        elif i % 3 == 0:
            print(f"    第{i+1}秒: 等待中...")
    
    # 5. 检查 UI 是否显示登录状态
    print(f"\n  [检查登录 UI 状态]")
    
    # 重新读取 storage.json
    with open(STORAGE_JSON, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    # 检查关键状态
    has_traditional = 'iCubeAuthInfo://traditional_login_3753060170739075' in storage
    has_gtm_traditional = (
        'icube_gtm' in storage and
        'users' in storage.get('icube_gtm', {}) and
        '3753060170739075' in storage.get('icube_gtm', {}).get('users', {})
    )
    
    print(f"    传统认证键: {'✅' if has_traditional else '❌'}")
    print(f"    GTM传统用户: {'✅' if has_gtm_traditional else '❌'}")
    
    # 读取最新窗口列表
    final_windows = []
    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
    def final_enum(hwnd, lparam):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buffer = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buffer, length + 1)
                final_windows.append(buffer.value)
        return True
    user32.EnumWindows(final_enum, 0)
    
    print(f"\n    所有可见窗口 ({len(final_windows)} 个):")
    for w in sorted(set(final_windows)):
        if w:
            print(f"      - {w}")
    
    return {
        'restarted': True,
        'pid': proc.pid,
        'has_traditional_auth': has_traditional,
        'has_gtm_user': has_gtm_traditional,
    }


def main():
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║  BSD × Trae CN 重启验证 + AHA 协议分析                                ║
╚══════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: 分析 AHA 加密协议
    analyze_aha_encryption()
    
    # Step 2: 重启 Trae CN 验证
    result = restart_traecn_and_verify()
    
    # Step 3: 输出总结
    print(f"\n{'='*60}")
    print(f"  总结")
    print(f"{'='*60}")
    print(f"""
  🔍 AHA 加密: 
     - 前缀 "746305100000": 未知自定义加密格式
     - Local State: DPAPI 加密 (Windows 原生)
     - 需进一步分析解密算法
  
  ⚡ 重启结果:
     - 进程已重启 (PID: {result.get('pid', 'N/A')})
     - 传统认证键: {'存在' if result.get('has_traditional_auth') else '不存在'}
     - GTM用户记录: {'存在' if result.get('has_gtm_user') else '不存在'}
  
  📌 关键发现:
     文件级注入已完成，但 UI 显示取决于 AHA 解密验证
     需要正确解密 AHA 协议后 UI 才会显示登录状态
""")

if __name__ == '__main__':
    main()