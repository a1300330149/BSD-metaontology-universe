#!/usr/bin/env python3
"""搜索 getUserInfoFromLocalStorage 和加密层"""
import re

with open(r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app\out\main.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 搜索 getUserInfoFromLocalStorage
print("=== getUserInfoFromLocalStorage ===")
for m in re.finditer(r'getUserInfoFromLocalStorage', content):
    start = max(0, m.start() - 100)
    end = min(len(content), m.end() + 600)
    snippet = content[start:end]
    print(snippet[:700])
    print("---")
    break

# 搜索 X3= (前缀常量)
print("\n=== X3= 常量 ===")
for m in re.finditer(r'X3="', content):
    start = max(0, m.start() - 50)
    end = min(len(content), m.end() + 100)
    snippet = content[start:end]
    print(snippet)
    break

# 搜索 AHA 相关的存储/加密
print("\n=== AHA Storage 相关 ===")
for pattern in ['AHAStorage', 'ahaStorage', 'aha_storage', 'AhaStorage', 'encryptStorage', 'encryptedStorage', 'AHAEncrypt', 'ahaEncrypt']:
    for m in re.finditer(pattern, content):
        start = max(0, m.start() - 200)
        end = min(len(content), m.end() + 200)
        snippet = content[start:end]
        print(f"pattern: {pattern}")
        print(snippet[:400])
        print("---")
        break

# 搜索 getItem 与 iCubeAuthInfo
print("\n=== iCubeAuthInfo getItem ===")
for m in re.finditer(r'getItem.*iCube', content):
    start = max(0, m.start() - 200)
    end = min(len(content), m.end() + 400)
    snippet = content[start:end]
    print(snippet[:500])
    print("---")
    break

# 搜索 decryptStorage 或 decryptItem
print("\n=== decryptStorage/decryptItem ===")
for pattern in ['decryptStorage', 'decryptItem', 'decryptData', 'decryptValue']:
    for m in re.finditer(pattern, content):
        start = max(0, m.start() - 200)
        end = min(len(content), m.end() + 200)
        snippet = content[start:end]
        print(f"pattern: {pattern}")
        print(snippet[:400])
        print("---")
        break

# 搜索 AHA native 模块
print("\n=== AHA native ===")
for pattern in ['aha-kit', 'aha_kit', 'byted-icube', 'trae-network']:
    for m in re.finditer(pattern, content):
        start = max(0, m.start() - 100)
        end = min(len(content), m.end() + 200)
        snippet = content[start:end]
        print(f"pattern: {pattern}")
        print(snippet[:300])
        print("---")
        break
