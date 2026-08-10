#!/usr/bin/env python3
"""搜索 main.js 中的 userInfo 存储键"""
import re

with open(r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app\out\main.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 搜索 persistedKey 附近的代码
print("=== persistedKey 上下文 ===")
for m in re.finditer(r'persistedKey', content):
    start = max(0, m.start() - 400)
    end = min(len(content), m.end() + 400)
    snippet = content[start:end]
    print(snippet)
    print("---")
    break

# 搜索 LI= (可能是 storage key 常量)
print("\n=== LI= 常量 ===")
for m in re.finditer(r'LI="', content):
    start = max(0, m.start() - 100)
    end = min(len(content), m.end() + 200)
    snippet = content[start:end]
    print(snippet)
    print("---")
    break

# 搜索 iCubeAuthInfo 读取逻辑
print("\n=== iCubeAuthInfo 读取逻辑 ===")
for m in re.finditer(r'iCubeAuthInfo://', content):
    start = max(0, m.start() - 200)
    end = min(len(content), m.end() + 200)
    snippet = content[start:end]
    print(snippet[:400])
    print("---")
    break

# 搜索 getItem 与 auth 相关
print("\n=== auth storage 读取 ===")
for m in re.finditer(r'getItem\([^)]*auth[^)]*\)', content, re.IGNORECASE):
    start = max(0, m.start() - 200)
    end = min(len(content), m.end() + 200)
    snippet = content[start:end]
    print(snippet[:400])
    print("---")
    break

# 搜索 userinfo 存储 key
print("\n=== userInfo storage key ===")
for pattern in [r'userTag', r'usertag', r'UserTag', r'persistentUser', r'persistUser']:
    for m in re.finditer(pattern, content):
        start = max(0, m.start() - 200)
        end = min(len(content), m.end() + 200)
        snippet = content[start:end]
        print(f"pattern: {pattern}")
        print(snippet[:400])
        print("---")
        break
