#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提取 Vv() 和 O9e() 函数实现 - 获取ClientID和签名算法
"""

import os, re

TRAE_CN_APP = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app'
main_js = os.path.join(TRAE_CN_APP, 'out', 'main.js')

with open(main_js, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 查找 Vv 函数 - ClientID生成
print('=== 1. Vv 函数 (ClientID生成) ===')
# Vv(this.d) 出现在 exchangeTokenByRefreshToken 中
# 搜索 Vv 函数定义
vv_patterns = [
    r'function Vv\(',
    r'Vv\s*=\s*function',
    r'var Vv\s*=',
    r'const Vv\s*=',
    r'Vv=function',
]

for pat in vv_patterns:
    matches = list(re.finditer(pat, content))
    if matches:
        for m in matches[:3]:
            start = m.start()
            end = min(len(content), start + 500)
            ctx = content[start:end]
            print(f'\n  模式 [{pat}]: @{m.start()}')
            print(f'  {ctx[:400]}')

# 如果上面找不到，搜索更通用的模式
print('\n  --- 扩展搜索 ---')
# 查找包含 "ClientID" 的函数定义部分
ctx_search = content[1147000:1152000]
# 找到Vv函数的赋值
vv_matches = list(re.finditer(r'Vv\s*=\s*[^,;]+', ctx_search))
for m in vv_matches[:5]:
    print(f'  @{1147000+m.start()}: {m.group()[:200]}')

# 2. 查找 O9e 函数 - 签名生成
print('\n\n=== 2. O9e 函数 (签名生成) ===')
o9e_patterns = [
    r'function O9e\(',
    r'O9e\s*=\s*function',
    r'var O9e\s*=',
    r'const O9e\s*=',
    r'O9e=function',
]

for pat in o9e_patterns:
    matches = list(re.finditer(pat, content))
    if matches:
        for m in matches[:3]:
            start = m.start()
            end = min(len(content), start + 800)
            ctx = content[start:end]
            print(f'\n  模式 [{pat}]: @{m.start()}')
            print(f'  {ctx[:600]}')

# 扩展搜索 O9e
print('\n  --- 扩展搜索 ---')
o9e_matches = list(re.finditer(r'O9e\s*=\s*[^,;]+', content))
for m in o9e_matches[:5]:
    ctx_start = max(0, m.start() - 100)
    ctx_end = min(len(content), m.end() + 500)
    ctx = content[ctx_start:ctx_end]
    print(f'  @{m.start()}: {ctx[:400]}')

# 3. 搜索完整的认证相关类
print('\n\n=== 3. AuthRequest 类搜索 ===')
# 找到包含 exchangeTokenByRefreshToken 的类
class_pattern = r'class\s+\w+.*\{[^}]*exchangeTokenByRefreshToken'
matches = list(re.finditer(class_pattern, content))
for m in matches[:2]:
    start = m.start()
    end = min(len(content), start + 2000)
    ctx = content[start:end]
    print(f'\n  类 @{m.start()}')
    print(f'  {ctx[:1500]}...')

# 4. 搜索 this.d 的初始化 - 应用配置
print('\n\n=== 4. this.d 配置对象 ===')
# 在exchangeToken附近找this.d的定义
for m in re.finditer(r'this\.d\s*=', content):
    if 1146000 < m.start() < 1156000:
        start = m.start()
        end = min(len(content), start + 300)
        ctx = content[start:end]
        print(f'  @{m.start()}: {ctx[:250]}')
        print()
