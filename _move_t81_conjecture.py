# -*- coding: utf-8 -*-
"""
将猜想实证section从独立位置移动到T80中国猜想之后
改名为"T81猜想实证"
从导航栏移除独立的猜想实证tab
"""

html_path = r"c:\Users\13003\OneDrive\桌面\3333333\Agent_v2\新六系本体论_人类易懂版.html"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# ============================================================
# 1. 从导航栏移除独立的"猜想实证"tab
# ============================================================
old_nav = '    <div class="nav-tab" onclick="showSection(\'bsdMath\')">🌊 BSD数理</div>\n    <div class="nav-tab" onclick="showSection(\'conjecture\')">🧪 猜想实证</div>\n    <div class="nav-tab" onclick="showSection(\'hierarchy\')">🌳 层级谱系</div>'
new_nav = '    <div class="nav-tab" onclick="showSection(\'bsdMath\')">🌊 BSD数理</div>\n    <div class="nav-tab" onclick="showSection(\'hierarchy\')">🌳 层级谱系</div>'

if old_nav in content:
    content = content.replace(old_nav, new_nav, 1)
    print("✅ 已从导航栏移除独立的「猜想实证」tab")
else:
    print("❌ 未找到导航栏中的猜想实证tab")
    exit(1)

# ============================================================
# 2. 提取猜想实证section的内容（从bsdMath之后到hierarchy之前）
# ============================================================

# 找到猜想实证section的开始和结束
conj_start_marker = '  <!-- 猜想实证 -->\n  <div class="section" id="conjecture">'
conj_end_marker = '\n  <!-- 层级谱系 -->\n  <div class="section" id="hierarchy">'

start_idx = content.find(conj_start_marker)
end_idx = content.find(conj_end_marker)

if start_idx == -1 or end_idx == -1:
    print("❌ 未找到猜想实证section的边界")
    exit(1)

# 提取猜想实证section的完整内容（包括开始标记，但不包括结束的层级谱系标记）
conjecture_section = content[start_idx:end_idx]

# 从原位置删除猜想实证section
content = content[:start_idx] + content[end_idx:]
print("✅ 已从原位置移除猜想实证section")

# ============================================================
# 3. 修改猜想实证section的标题和id为"T81猜想实证"
# ============================================================

# 修改id
conjecture_section = conjecture_section.replace(
    'id="conjecture"',
    'id="t81Conjecture"'
)

# 修改标题
conjecture_section = conjecture_section.replace(
    '🧪 猜想实证：产业生态拓扑场论对照验证',
    '🧪 T81猜想实证：产业生态拓扑场论对照验证'
)

# 修改模块编号
conjecture_section = conjecture_section.replace(
    'T80-T81 · <strong>核心定位：</strong>以任天堂非平庸拓扑为范本',
    'T81 · <strong>核心定位：</strong>以任天堂非平庸拓扑为范本'
)

# 修改注释
conjecture_section = conjecture_section.replace(
    '<!-- 猜想实证 -->',
    '<!-- T81猜想实证 -->'
)

# 修改模块标题
conjecture_section = conjecture_section.replace(
    '🎮 T81猜想：中国游戏产业生态拓扑闭合路径',
    '🎮 T81 猜想实证：中国游戏产业生态拓扑闭合路径'
)

print("✅ 已将猜想实证改名为「T81猜想实证」")

# ============================================================
# 4. 将修改后的猜想实证section插入到T80中国猜想之后
# ============================================================

# 找到T80中国猜想section的结束位置（意义大一统之前）
t80_end_marker = '\n\n  <!-- 意义大一统V2.0理论分册 -->\n  <div class="section" id="meaningUnity">'

if t80_end_marker in content:
    # 在T80结束后、意义大一统前插入T81猜想实证
    content = content.replace(
        t80_end_marker,
        '\n' + conjecture_section + '\n  <!-- 意义大一统V2.0理论分册 -->\n  <div class="section" id="meaningUnity">',
        1
    )
    print("✅ 已将T81猜想实证section插入T80中国猜想之后")
else:
    print("❌ 未找到T80结束位置")
    exit(1)

# 保存
with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

print("\n✅ 全部调整完成：")
print("   - 导航栏移除了独立的猜想实证tab")
print("   - 猜想实证移动到T80中国猜想之后")
print("   - 改名为「T81猜想实证」")
print("   - id改为t81Conjecture")
