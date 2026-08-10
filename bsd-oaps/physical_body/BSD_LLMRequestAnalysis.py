#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
逆向分析Trae CN客户端发送llm_raw_chat的完整实现
"""

import os, re

TRAE_CN_APP = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app'
main_js = os.path.join(TRAE_CN_APP, 'out', 'main.js')

with open(main_js, 'r', encoding='utf-8') as f:
    content = f.read()

print(f'main.js 大小: {len(content):,} chars')

# 1. 搜索 llm_raw_chat 的完整实现
print('\n=== 1. llm_raw_chat 请求实现 ===')
pattern = r'llm_raw_chat'
matches = list(re.finditer(pattern, content))
print(f'找到 {len(matches)} 处 llm_raw_chat')

for m in matches[:8]:
    start = max(0, m.start() - 500)
    end = min(len(content), m.end() + 500)
    ctx = content[start:end]
    ctx_clean = ctx.replace('\n', ' ')[:800]
    print(f'\n--- 位置 @{m.start()} ---')
    print(ctx_clean)

# 2. 搜索请求头构建逻辑
print('\n\n=== 2. AI请求头构建 ===')
header_patterns = [
    r'ai_assistant\.request',
    r'llm.*header',
    r'buildHeaders|getHeaders|createHeaders',
    r'marketplace-headers',
    r'solo-lite.*headers',
]

for pat in header_patterns:
    matches = list(re.finditer(pat, content, re.IGNORECASE))
    if matches:
        print(f'\n模式 [{pat}]: {len(matches)} 处')
        for m in matches[:3]:
            start = max(0, m.start() - 200)
            end = min(len(content), m.end() + 500)
            ctx = content[start:end]
            ctx_clean = ctx.replace('\n', ' ')[:600]
            print(f'  @{m.start()}: {ctx_clean}...')

# 3. 搜索 oauth 相关的请求签名
print('\n\n=== 3. 请求签名机制 ===')
sign_patterns = [
    r'x-tt-env|x-use-ppe|x-use-boe',
    r'DeviceProof|deviceProof',
    r'Signature|timestamp|nonce',
    r'SignRequest|signRequest',
]

for pat in sign_patterns:
    matches = list(re.finditer(pat, content, re.IGNORECASE))
    if matches and len(matches) < 50:
        print(f'\n模式 [{pat}]: {len(matches)} 处')
        for m in matches[:3]:
            start = max(0, m.start() - 100)
            end = min(len(content), m.end() + 300)
            ctx = content[start:end]
            ctx_clean = ctx.replace('\n', ' ')[:400]
            print(f'  @{m.start()}: {ctx_clean}...')

# 4. 查找完整的请求构造函数
print('\n\n=== 4. 请求构造函数 ===')
# 搜索包含fetch或axios调用的代码
fetch_pattern = r'(?:async\s+)?(?:\w+)?\s*\([^)]*\)\s*\{[^}]*fetch[^}]*\}'
matches = list(re.finditer(fetch_pattern, content))
print(f'包含fetch的函数: {len(matches)} 处')

# 更精确地查找llm相关的fetch
llm_fetch_pattern = r'llm[^;]{0,200}fetch[^;]{0,200}'
matches = list(re.finditer(llm_fetch_pattern, content, re.IGNORECASE))
if matches:
    print(f'llm相关fetch: {len(matches)} 处')
    for m in matches[:3]:
        ctx = content[m.start():m.end()].replace('\n', ' ')[:500]
        print(f'  @{m.start()}: {ctx}')
