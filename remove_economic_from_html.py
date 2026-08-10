# -*- coding: utf-8 -*-
"""
从HTML文件中删除BSD经济元体系内容（保留T88原有章节内容）
论文主体已迁移至theory_base总本源层T88 Markdown源文件
"""

file_path = r'c:\Users\13003\OneDrive\桌面\3333333\Agent_v2\新六系本体论_人类易懂版.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 定位BSD经济元体系内容的起始位置（HTML注释标记）
start_marker = '      <!-- BSD全域经济元体系 -->'
start_pos = content.find(start_marker)

if start_pos == -1:
    print('错误：未找到BSD经济元体系起始标记！')
    exit(1)

print(f'找到BSD经济元体系起始位置：字符偏移 {start_pos}')

# 定位BSD经济元体系内容的结束位置
# 内容结构：从起始标记开始，到结论div结束后的闭合标签
# BSD经济元体系外层div的闭合是最后一个</div>
# 我们需要找到从起始标记开始，到"BSD全域经济元体系为后稀缺时代的经济理论革新提供了全新的理论框架。"之后的闭合div

# 首先找到结论文字
conclusion_text = 'BSD全域经济元体系为后稀缺时代的经济理论革新提供了全新的理论框架。'
conclusion_pos = content.find(conclusion_text, start_pos)

if conclusion_pos == -1:
    print('错误：未找到BSD经济元体系结论文字！')
    exit(1)

print(f'找到BSD经济元体系结论文字位置：字符偏移 {conclusion_pos}')

# 从结论文字开始，找到BSD经济元体系外层div的闭合
# 结构：...结论文字</div>(内层) \n </div>(结论框) \n\n </div>(BSD经济元体系外层)
import re

# 查找模式：结论文字后的闭合div序列
end_search_start = conclusion_pos + len(conclusion_text)
end_pattern = r'</div>\s*</div>\s*\n\s*</div>'
end_match = re.search(end_pattern, content[end_search_start:])

if end_match:
    end_pos = end_search_start + end_match.end()
    print(f'找到BSD经济元体系结束位置：字符偏移 {end_pos}')
else:
    print('错误：未找到BSD经济元体系结束位置！')
    exit(1)

# 删除BSD经济元体系内容
# 同时清理前后多余空行
# 向前查找：删除起始标记前的空行
pre_start = start_pos
while pre_start > 0 and content[pre_start-1:pre_start] == '\n':
    pre_start -= 1
# 保留一个换行
if pre_start < start_pos:
    pre_start += 1

# 向后查找：删除结束位置后的多余空行
post_end = end_pos
while post_end < len(content) and content[post_end:post_end+1] == '\n':
    post_end += 1
# 保留两个换行（与后续内容分隔）
if post_end > end_pos:
    post_end = end_pos + 2

# 执行删除
new_content = content[:pre_start] + '\n' + content[post_end:]

# 清理可能的多余空行（4个以上连续换行变为3个）
new_content = re.sub(r'\n{4,}', '\n\n\n', new_content)

# 写入文件
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('BSD经济元体系内容已从HTML文件中删除！')
print(f'删除内容长度：{end_pos - start_pos} 字符')
print('T88章节原有内容保留，论文主体已迁移至theory_base总本源层T88 Markdown源文件。')
