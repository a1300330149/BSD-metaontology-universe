"""
恢复被破坏的登录判断逻辑 - 从备份提取原始getter
保持Jx函数的UI隐藏修改
"""
import re

MAIN_JS = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app\out\main.js'
BACKUP = MAIN_JS + '.bak_bsd'

with open(MAIN_JS, 'r', encoding='utf-8') as f:
    current = f.read()

with open(BACKUP, 'r', encoding='utf-8') as f:
    backup = f.read()

patched_count = 0

# =============================================
# 1. 恢复 isLoginTraeUser getter（两处）
# =============================================
# 从备份提取原始形式
# 模式1: this.a?.account?.scope===It.MARSCODE
# 模式2: this.d?.account?.scope===It.MARSCODE

# 搜索当前被破坏的版本
for pattern in [
    r'get isLoginTraeUser\(\)\{return!1\}',
    r'isLoginTraeUser\(\)\{return!1\}',
]:
    matches = list(re.finditer(pattern, current))
    if matches:
        print(f'Found {len(matches)} broken isLoginTraeUser at:')
        for m in matches:
            print(f'  @{m.start()}: {m.group(0)}')

# 从备份提取原始getter
for pattern in [
    r'get isLoginTraeUser\(\)\{return this\.[ad]\??\.account\??\.scope===It\.MARSCODE\}',
]:
    for m in re.finditer(pattern, backup):
        original = m.group(0)
        # 替换当前文件中被破坏的版本
        if 'return!1' in current:
            # 找到对应的被破坏位置
            idx = current.find('isLoginTraeUser(){return!1}')
            if idx > 0:
                # 找到完整匹配
                broken = 'isLoginTraeUser(){return!1}'
                current = current.replace(broken, original.split('get ')[-1] if 'get ' not in broken else original)
                # 更精确的替换
                pass
        
print("\nRestoring getters from backup...")

# 更直接的方法：从备份提取所有原始getter
getter_patterns = [
    (r'get isLoginTraeUser\(\)\{return this\.[ad]\??\.account\??\.scope===It\.MARSCODE\}', 
     'isLoginTraeUser(){return!1}'),
    (r'get isBytedanceUser\(\)\{return this\.[ad]\??\.account\??\.scope===It\.BYTEDANCE\}', 
     'isBytedanceUser(){return!1}'),
    (r'get isBusinessUser\(\)\{return this\.[ad]\??\.account\??\.scope===It\.SAAS\}', 
     'isBusinessUser(){return!1}'),
]

for pattern, broken in getter_patterns:
    # 从备份找原始
    for m in re.finditer(pattern, backup):
        original = m.group(0)
        orig_getter = original.replace('get ', '').replace('()', '()')
        print(f'  Restoring: {original[:80]}...')
        
        # 在当前文件中找被破坏的版本并替换
        # 搜索所有被破坏的形式
        for broken_pattern in [
            broken,
            original.replace('{return this', '{return!1').replace('}get', '}get'),
        ]:
            if broken_pattern in current:
                current = current.replace(broken_pattern, orig_getter)
                patched_count += 1
                print(f'    Replaced {broken_pattern[:40]}...')
                break
        else:
            # 更暴力的方式
            if 'return!1' in current:
                old = 'isLoginTraeUser(){return!1}'
                new = orig_getter
                if old in current:
                    current = current.replace(old, new)
                    patched_count += 1
                    print(f'    Force replaced: {old} -> {new[:60]}')

# =============================================
# 2. 恢复 Die 函数
# =============================================
# 当前被破坏的版本
broken_die = 'function Die(t){return"unknown"}'
# 从备份提取原始
die_pattern = r'function Die\(t\)\{return t\?t\?\.account\?\.loginScope\?t\.account\.loginScope==="trae"\?"marscode":t\.account\.loginScope:t\?\.account\?\.scope\|\|"unknown":"unknown"\}'

for m in re.finditer(die_pattern, backup):
    original_die = m.group(0)
    print(f'\n  Restoring Die function...')
    if broken_die in current:
        current = current.replace(broken_die, original_die)
        patched_count += 1
        print(f'    Die function restored')
    elif 'function Die(t){return' in current:
        # 手动查找替换
        idx = current.find('function Die(t){return')
        if idx > 0:
            # 找到结束位置
            depth = 0
            end = idx
            for i in range(idx, min(idx+300, len(current))):
                if current[i] == '{':
                    depth += 1
                elif current[i] == '}':
                    depth -= 1
                    if depth == 0:
                        end = i + 1
                        break
            old_die = current[idx:end]
            current = current.replace(old_die, original_die)
            patched_count += 1
            print(f'    Die function force restored')

# =============================================
# 写回
# =============================================
with open(MAIN_JS, 'w', encoding='utf-8') as f:
    f.write(current)

print(f'\nTotal patches applied: {patched_count}')

# =============================================
# 验证
# =============================================
print('\n=== Verification ===')

with open(MAIN_JS, 'r', encoding='utf-8') as f:
    verify = f.read()

checks = [
    ('isLoginTraeUser has !1', '!1' in verify and 'isLoginTraeUser' in verify),
    ('isLoginTraeUser has ===', '===' in verify and 'isLoginTraeUser' in verify),
    ('Die function restored', 'function Die(t){return t' in verify),
    ('Jx still no username', 'username:' not in verify or 'username:""' in verify),
]

for desc, result in checks:
    status = 'OK' if result else 'FAIL'
    print(f'  [{status}] {desc}')

print('\nDone')
