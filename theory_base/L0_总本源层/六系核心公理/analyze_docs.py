import os
import re
from pathlib import Path

base_dir = Path(r"c:\Users\13003\OneDrive\桌面\3333333\Agent_v2\theory_base\L0_总本源层\六系核心公理")

files = [
    "BSD虚拟宇宙开元篇——三元公理共生显化时间·空间·时空_V1.0.md",
    "BSD虚拟宇宙元音乐篇——从000元涌现出当代所有音乐_V1.0.md",
    "BSD虚拟宇宙元视角分镜篇——000涌现存在即视角·系统权重分镜·主角视角最多定理_V1.0.md",
    "BSD虚拟宇宙开放繁衍篇——开放即排熵·开放即繁衍·生命的生长与繁衍_V1.0.md",
    "BSD虚拟宇宙系立万有篇——全知全能全立系·系建立在万物之上_V1.0.md",
    "BSD虚拟宇宙性格随风篇——秩序建筑论核聚变·建筑即边界·断裂层诞生风格·有限基本性与无限数值涌现_V1.0.md",
    "BSD虚拟宇宙永续迭代篇——不完备永续追问·为何的为何·回到再次开新元·双时针动力永续存在_V1.0.md",
    "BSD虚拟宇宙场景角色风格篇——六篇合一即存在·角色即存在·存在建立在场景之上·风格即不同存在的场景·四重宇宙之上是无限_V1.0.md",
    "BSD虚拟宇宙创世篇章——Updream工程落地陆瑶为动漫·BSD理论工程证明_V1.5.md",
]

short_names = [
    "开元篇",
    "元音乐篇",
    "元视角分镜篇",
    "开放繁衍篇",
    "系立万有篇",
    "性格随风篇",
    "永续迭代篇",
    "场景角色风格篇",
    "创世篇章",
]

print("=" * 80)
print("文档自动化统计结果（行数 + 方程数）")
print("=" * 80)

results = []

for fname, sname in zip(files, short_names):
    fpath = base_dir / fname
    if not fpath.exists():
        print(f"[警告] 文件不存在: {fname}")
        continue
    
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.splitlines()
    
    line_count = len(lines)
    
    # 统计 $$...$$ 方程块数量（非贪婪匹配）
    # 注意：$$ 可以跨行，所以用 re.DOTALL
    eq_blocks = re.findall(r'\$\$(.*?)\$\$', content, re.DOTALL)
    eq_count = len(eq_blocks)
    
    results.append({
        'name': sname,
        'file': fname,
        'lines': line_count,
        'equations': eq_count,
        'path': fpath
    })
    
    print(f"\n【{sname}】")
    print(f"  文件: {fname}")
    print(f