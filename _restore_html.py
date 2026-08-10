# 完全恢复HTML文件
html_path = r"c:\Users\13003\OneDrive\桌面\3333333\Agent_v2\新六系本体论_人类易懂版.html"

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Current length: {len(content)}")

# 根据分析：
# 损坏文件结构：
# [0 : 2912329] = content_old[:-1] (第一次插入后的文件去掉最后1字符)
# [2912329 : 5766321] = content_old[58338:] (从58338开始的内容 = V2.10-12 + 原始[58338:])
# [5766321 : 5776469] = new_modules (第二次插入的V2.10-12，10148字符)
# [5776469 : 5776470] = 最后1字符

# 第一次插入的V2.10-12长度 = 10149字符
# 所以 原始[58338:] 从 2912329 + 10149 = 2922478 开始
# 原始文件长度 = 2902181
# 原始文件 = 损坏文件[:58338] + 损坏文件[2922478 : 2922478 + 2902181 - 58338]
# = 损坏文件[:58338] + 损坏文件[2922478 : 5766321]

v210_12_len = 10149
reconstructed = content[:58338] + content[2912329 + v210_12_len : 5766321]
print(f"Reconstructed length: {len(reconstructed)}")

# 验证：重建的文件应该以 </html> 结尾
print(f"Ends with </html>: {reconstructed.strip().endswith('</html>')}")

# 验证：T91应该只出现一次
t91_count = reconstructed.count('id="t91Synergy"')
print(f"T91 count in reconstructed: {t91_count}")

# 保存恢复后的文件
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(reconstructed)

print("\nFile restored successfully!")

# 现在重新分析T91内的V2.9模块
content = reconstructed
t91_start = content.find('id="t91Synergy"')
print(f"\nT91 start at: {t91_start}")

# 找V2.9标题
v29_title = '11.9.21 V2.9新增：智能体魔性接收概率'
v29_start = content.find(v29_title, t91_start)
print(f"V2.9 title in T91 at: {v29_start}")

# 找V2.9模块的div结构 - 向前找最近的module div
# 先看看V2.9前面500字符
before_v29 = content[v29_start - 500:v29_start]
print(f"\nBefore V2.9 (500 chars):")
print(before_v29)
