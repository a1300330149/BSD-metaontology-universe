#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从Trae CN main.js提取真实的OAuth参数和client_id
"""

import os, re

TRAE_CN_APP = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app'
main_js = os.path.join(TRAE_CN_APP, 'out', 'main.js')

with open(main_js, 'r', encoding='utf-8') as f:
    content = f.read()

print(f'main.js 大小: {len(content)} chars')

# 1. 搜索 ExchangeToken 的完整上下文
print('\n=== 1. ExchangeToken 调用分析 ===')
pattern = r'ExchangeToken'
matches = list(re.finditer(pattern, content))
print(f'找到 {len(matches)} 处 ExchangeToken')

for m in matches[:5]:
    start = max(0, m.start() - 300)
    end = min(len(content), m.end() + 300)
    ctx = content[start:end]
    # 清理换行
    ctx_clean = ctx.replace('\n', ' ')[:600]
    print(f'\n--- 位置 @{m.start()} ---')
    print(ctx_clean)

# 2. 搜索 ClientID/client_id 的来源
print('\n\n=== 2. ClientID 搜索 ===')
client_id_patterns = [
    r'ClientID[\"\':\s]+([a-zA-Z0-9_-]+)',
    r'clientId[\"\':\s]+([a-zA-Z0-9_-]+)',
    r'client_id[\"\':\s]+([a-zA-Z0-9_-]+)',
    r'"ClientID"\s*:\s*"([^"]+)"',
    r'"clientId"\s*:\s*"([^"]+)"',
    r'"client_id"\s*:\s*"([^"]+)"',
]

for pat in client_id_patterns:
    found = list(re.finditer(pat, content))
    if found:
        print(f'\n模式 [{pat[:40]}...]: 找到 {len(found)} 处')
        for m in found[:5]:
            print(f'  @{m.start()}: {m.group(0)[:100]}')

# 3. 搜索 refreshToken 相关的OAuth流程
print('\n\n=== 3. refreshToken OAuth流程 ===')
oauth_pattern = r'(?:async\s+)?(?:refreshToken|exchangeToken|getAccessToken)\w*\s*\([^)]*\)\s*\{[^}]*\}'
matches = list(re.finditer(oauth_pattern, content))
print(f'找到 {len(matches)} 处 refresh/access token 相关函数')

for m in matches[:3]:
    start = max(0, m.start() - 200)
    end = min(len(content), m.end() + 500)
    ctx = content[start:end]
    ctx_clean = ctx.replace('\n', ' ')[:800]
    print(f'\n--- 位置 @{m.start()} ---')
    print(ctx_clean)

# 4. 搜索bootConfig中的clientId
print('\n\n=== 4. bootConfig 搜索 ===')
boot_pattern = r'bootConfig[^{]*\{[^}]*\}'
matches = list(re.finditer(boot_pattern, content))
for m in matches[:3]:
    ctx = content[m.start():m.end()][:500]
    print(f'\n--- bootConfig @{m.start()} ---')
    print(ctx)

# 5. 搜索URL模式
print('\n\n=== 5. API URL模式 ===')
url_patterns = [
    r'oauth[^\s"\']+ExchangeToken[^\s"\']*',
    r'cloudide[^\s"\']+CheckLogin[^\s"\']*',
    r'cloudide[^\s"\']+Login[^\s"\']*',
]

for pat in url_patterns:
    found = list(re.finditer(pat, content, re.IGNORECASE))
    if found:
        print(f'\n[{pat[:30]}...]')
        for m in found[:3]:
            print(f'  @{m.start()}: {m.group(0)[:150]}')
