# -*- coding: utf-8 -*-
"""
修复脚本：将错误插入到第5890行的BSD全域经济元体系内容
移动到T88章节（t88InstitutionalEconomics）的正确结尾位置
"""

# 读取文件
file_path = r'c:\Users\13003\OneDrive\桌面\3333333\Agent_v2\新六系本体论_人类易懂版.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 步骤1：定位并提取错误插入的经济元体系内容
# 错误内容从 "<!-- BSD全域经济元体系 -->" 开始
economic_start_marker = '      <!-- BSD全域经济元体系 -->'
economic_start_pos = content.find(economic_start_marker)

if economic_start_pos == -1:
    print('错误：未找到BSD全域经济元体系内容起始标记！')
    exit(1)

print(f'找到经济元体系内容起始位置：字符偏移 {economic_start_pos}')

# 查找经济元体系内容的结束位置
# 内容结构：<div ...>...</div>，需要找到对应的闭合div
# 从起始位置开始，找到最后一个 </div>（经济元体系外层div的闭合）
# 经济元体系内容以 "      </div>\n      </div>" 结束（第6054-6055行）
# 其中第一个 </div> 是经济元体系外层div的闭合，第二个 </div> 是章节内容div的闭合

# 从经济元体系起始位置开始搜索
search_start = economic_start_pos

# 找到经济元体系外层div的闭合
# 经济元体系内容结束于：参考文献后的结论div闭合，然后是外层div闭合
# 结构：...结论</div>\n      </div>\n      </div>
# 我们需要找到 "最终结论" 之后的闭合div

final_conclusion_marker = 'BSD全域经济元体系为后稀缺时代的经济理论革新提供了全新的理论框架。'
final_conclusion_pos = content.find(final_conclusion_marker, search_start)

if final_conclusion_pos == -1:
    print('错误：未找到经济元体系结论标记！')
    exit(1)

print(f'找到经济元体系结论位置：字符偏移 {final_conclusion_pos}')

# 从结论位置开始，找到经济元体系外层div的闭合
# 结论后结构：</div>\n        </div>\n\n      </div>\n
# 即：结论文字</div>(内层) \n </div>(结论框) \n\n </div>(经济元体系外层)
end_search_start = final_conclusion_pos + len(final_conclusion_marker)

# 找到经济元体系外层div的闭合 "</div>" 
# 从结论文字后，依次遇到：
# 1. </div> (内层div)
# 2. </div> (结论div)  
# 3. (空行)
# 4. </div> (经济元体系外层div)

# 查找模式：</div>\n        </div>\n\n      </div>
import re
end_pattern = r'</div>\s*</div>\s*\n\s*</div>'
end_match = re.search(end_pattern, content[end_search_start:])
if end_match:
    economic_end_pos = end_search_start + end_match.end()
    print(f'找到经济元体系内容结束位置：字符偏移 {economic_end_pos}')
else:
    print('错误：未找到经济元体系内容结束位置！')
    exit(1)

# 提取经济元体系内容（包含前后的空行处理）
# 需要包含起始标记前的空行
# 查找起始标记前的空行
line_start = content.rfind('\n', 0, economic_start_pos)
# 经济元体系内容从起始标记所在行的行首开始
economic_content = content[economic_start_pos:economic_end_pos]

# 同时捕获起始标记前的空行（用于清理）
# 查找起始标记前的所有空行
pre_empty_start = line_start
while pre_empty_start > 0 and content[pre_empty_start-1:pre_empty_start+1] == '\n\n':
    pre_empty_start -= 1

print(f'经济元体系内容长度：{len(economic_content)} 字符')

# 步骤2：从错误位置删除经济元体系内容
# 删除范围：从经济元体系起始标记前的空行到经济元体系结束位置
# 但要保留章节结构，需要仔细处理

# 简化方法：直接删除从 economic_start_pos 到 economic_end_pos 的内容
# 并处理前后的空行
content_without_economic = content[:economic_start_pos] + content[economic_end_pos:]

# 清理可能的多余空行（删除位置可能有连续3个以上的空行）
content_without_economic = re.sub(r'\n{4,}', '\n\n\n', content_without_economic)

print('已从错误位置删除经济元体系内容')

# 步骤3：在T88章节的正确位置插入经济元体系内容
# T88章节的参考文献div结束后插入
# 定位T88章节的参考文献结束位置
# 参考文献结构：
# <div style="...参考文献...">
#   ...
#   <div>[8] Tarski, A. ...</div>
# </div>  <- 参考文献div闭合
# </div>  <- T88章节内容div闭合

# 查找T88章节的参考文献结束位置
# 使用Tarski参考文献条目作为定位标记
tarski_marker = '[8] Tarski, A. The concept of truth in formalized languages'
tarski_pos = content_without_economic.find(tarski_marker)

if tarski_pos == -1:
    print('错误：未找到T88章节参考文献标记！')
    exit(1)

print(f'找到T88章节参考文献位置：字符偏移 {tarski_pos}')

# 从Tarski条目开始，找到参考文献div的闭合
# 结构：<div>[8] Tarski...</div>\n          </div>\n      </div>
# 第一个 </div> 是Tarski条目div的闭合
# 第二个 </div> 是参考文献div的闭合
# 第三个 </div> 是T88章节内容div的闭合

ref_end_pattern = r'</div>\s*\n\s*</div>\s*\n\s*</div>'
ref_end_match = re.search(ref_end_pattern, content_without_economic[tarski_pos:])
if ref_end_match:
    # 参考文献div闭合位置（第二个</div>之后）
    # 我们需要在参考文献div闭合后、T88章节内容div闭合前插入
    # 即在第二个</div>之后插入
    
    # 找到第二个</div>的位置
    first_close = content_without_economic.find('</div>', tarski_pos)
    second_close = content_without_economic.find('</div>', first_close + 6)
    
    # 插入位置：在第二个</div>之后
    insert_pos = second_close + 6  # 6 = len('</div>')
    
    print(f'T88章节插入位置：字符偏移 {insert_pos}')
    
    # 在参考文献div闭合后插入经济元体系内容
    # 格式：\n\n{经济元体系内容}\n
    new_content = (
        content_without_economic[:insert_pos] + 
        '\n\n' + economic_content + 
        '\n' + 
        content_without_economic[insert_pos:]
    )
    
    print('已将经济元体系内容插入到T88章节正确位置')
else:
    print('错误：未找到T88章节参考文献闭合位置！')
    exit(1)

# 步骤4：写入文件
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('文件已保存！')
print('修复完成：BSD全域经济元体系已从错误位置移动到T88章节结尾。')
