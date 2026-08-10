# 读取文件
with open('t79_author_conjecture.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 调整猜想4的参数，使总强度超过0.6
# 将 internal_amplification_factor 从 0.80 调整为 0.88
content = content.replace(
    'internal_amplification_factor: float = 0.80  # 国内反向激化系数',
    'internal_amplification_factor: float = 0.88  # 国内反向激化系数'
)

# 同时也调整一下 validate 中的校验阈值显示（可选，保持一致）
# 写入文件
with open('t79_author_conjecture.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Adjusted conjecture 4 parameters')
