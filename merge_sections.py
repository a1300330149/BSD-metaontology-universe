with open('新六系本体论_人类易懂版.html', 'r', encoding='utf-8') as f:
    content = f.read()

def find_section(content, section_id):
    """找到section的开始和结束位置"""
    start_pattern = f'<div class="section" id="{section_id}"'
    start = content.find(start_pattern)
    if start == -1:
        return None, None
    
    pos = start
    stack = 0
    found_first = False
    
    while pos < len(content):
        div_start = content.find('<div', pos)
        div_end = content.find('</div>', pos)
        
        if div_start == -1 and div_end == -1:
            break
            
        if div_start != -1 and (div_end == -1 or div_start < div_end):
            stack += 1
            found_first = True
            pos = div_start + 4
        else:
            stack -= 1
            pos = div_end + 6
            if found_first and stack == 0:
                return start, pos
    
    return start, len(content)

def extract_inner(content, section_id):
    """提取section内部wrapper div的内容"""
    s, e = find_section(content, section_id)
    if s is None:
        return ''
    full = content[s:e]
    # 跳过section开始标签
    first_gt = full.find('>') + 1
    # 跳过内部wrapper的开始标签（第二个div开始）
    second_div_start = full.find('<div', first_gt)
    inner_start = full.find('>', second_div_start) + 1
    # 找到最后一个</div>（section的结束标签）
    last_div = full.rfind('</div>')
    # 往前找wrapper的结束标签
    wrapper_end = full.rfind('</div>', 0, last_div)
    return full[inner_start:wrapper_end].strip()

# 提取4个模块的内部内容
axioms_inner = extract_inner(content, 'axioms')
closure_inner = extract_inner(content, 'closure')
analogy_inner = extract_inner(content, 'analogy')
differentiation_inner = extract_inner(content, 'differentiation')

print(f'axioms: {len(axioms_inner)} chars')
print(f'closure: {len(closure_inner)} chars')
print(f'analogy: {len(analogy_inner)} chars')
print(f'differentiation: {len(differentiation_inner)} chars')

# 构建要插入的内容（带分隔标题）
insert_content = f'''
        <div style="margin-top:40px;padding-top:30px;border-top:2px solid rgba(100,181,246,0.2);">
          <div style="text-align:center;font-size:1.3em;color:#64b5f6;margin-bottom:25px;">🧱 二、三元公理</div>
          {axioms_inner}
        </div>

        <div style="margin-top:40px;padding-top:30px;border-top:2px solid rgba(186,104,200,0.2);">
          <div style="text-align:center;font-size:1.3em;color:#ba68c8;margin-bottom:25px;">🌱 三、六系分化</div>
          {differentiation_inner}
        </div>

        <div style="margin-top:40px;padding-top:30px;border-top:2px solid rgba(255,183,77,0.2);">
          <div style="text-align:center;font-size:1.3em;color:#ffb74d;margin-bottom:25px;">🔄 四、零元闭环</div>
          {closure_inner}
        </div>

        <div style="margin-top:40px;padding-top:30px;border-top:2px solid rgba(77,182,172,0.2);">
          <div style="text-align:center;font-size:1.3em;color:#4db6ac;margin-bottom:25px;">🏠 五、生活类比</div>
          {analogy_inner}
        </div>
'''

# 找到tripleSpectrum（原hierarchy）中hierarchy-summary结束后、hierarchy-container结束前的位置
# 先找hierarchy-summary的结束位置
hs_end_pattern = '</div>\n\n      </div>\n    </div>\n  </div>'
# 不对，让我换个方式——找到hierarchy-container的结束位置

# 找到tripleSpectrum section的开始
ts_start = content.find('<div class="section" id="tripleSpectrum"')
# 找到hierarchy-container的开始
hc_start = content.find('<div class="hierarchy-container">', ts_start)
# 找到hierarchy-container的结束位置（在tripleSpectrum内部）
# 从hierarchy-container开始往后找匹配的</div>
pos = hc_start
stack = 0
found_first = False
hc_end = -1
while pos < len(content):
    div_start = content.find('<div', pos)
    div_end = content.find('</div>', pos)
    if div_start == -1 and div_end == -1:
        break
    if div_start != -1 and (div_end == -1 or div_start < div_end):
        stack += 1
        found_first = True
        pos = div_start + 4
    else:
        stack -= 1
        pos = div_end + 6
        if found_first and stack == 0:
            hc_end = div_end
            break

print(f'hierarchy-container ends at position: {hc_end}')
print(f'line: {content[:hc_end].count(chr(10))+1}')

# 在hierarchy-container结束标签之前插入内容
new_content = content[:hc_end] + insert_content + '\n        ' + content[hc_end:]

# 现在删除4个旧section：axioms, closure, analogy, differentiation
sections_to_delete = ['differentiation', 'analogy', 'closure', 'axioms']

for sid in sections_to_delete:
    s, e = find_section(new_content, sid)
    if s is not None:
        # 还要删除前面的注释
        comment_start = new_content.rfind('<!--', 0, s)
        comment_end = new_content.find('-->', comment_start) if comment_start != -1 else -1
        if comment_start != -1 and comment_end != -1 and comment_end + 3 <= s:
            between = new_content[comment_end + 3:s]
            if between.strip() == '':
                s = comment_start
        new_content = new_content[:s] + new_content[e:]
        print(f'Deleted {sid}')
    else:
        print(f'WARNING: {sid} not found')

with open('新六系本体论_人类易懂版.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Done!')
