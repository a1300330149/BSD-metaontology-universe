# 恢复HTML并重新正确插入
html_path = r"c:\Users\13003\OneDrive\桌面\3333333\Agent_v2\新六系本体论_人类易懂版.html"

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Current length: {len(content)}")

# 先用同样的方法恢复到原始状态
# 我们需要重新构造原始文件
# 从之前的分析，原始文件长度是2902181
# 但当前文件是2912330（插入了10149字符在错误位置）
# 让我们找到V2.10注释的位置，然后删除它以及后面的V2.10-12内容

v210_comment = '<!-- 11.9.22 V2.10新增：数字社区归零焦虑与主动防御同构 -->'
v210_pos = content.find(v210_comment)
print(f"V2.10 comment at: {v210_pos}")

if v210_pos != -1:
    # 找到V2.12模块的结束位置
    # V2.12模块和V2.9是同样的结构模式
    # 让我们找V2.12后面紧接着的原始内容特征
    # 原始内容在V2.9后面的应该是什么？
    
    # 实际上，我们知道插入了10149字符
    # 所以原始文件 = content[:v210_pos - some_offset] + content[v210_pos + 10149:]
    # 但我们需要知道插入的精确起始位置
    
    # 让我们找V2.10注释前面的内容，看看是不是原始内容的延续
    before_v210 = content[v210_pos - 200:v210_pos]
    print(f"\nBefore V2.10 (200 chars):")
    print(before_v210)
    
    # 找V2.9模块的结束：从V2.9注释开始，找匹配的</div>
    v29_comment = '<!-- 11.9.21 V2.9新增：智能体魔性接收概率'
    v29_comment_pos = content.find(v29_comment)
    print(f"\nV2.9 comment at: {v29_comment_pos}")
    
    # 方法：从V2.9注释位置开始，找到外层div，然后计算嵌套深度
    # 但这次我们要更仔细地追踪
    module_div_marker = '<div style="background:linear-gradient(135deg'
    v29_div_start = content.find(module_div_marker, v29_comment_pos)
    print(f"V2.9 outer div start: {v29_div_start}")
    
    # 我们需要知道这个div有多少层嵌套
    # 让我们直接搜索这个特定模块的结束</div>
    # 方法：从v29_div_start开始，计算到v210_pos之前有多少个<div>和</div>
    
    div_count = 0
    close_count = 0
    pos = v29_div_start
    search_end = v210_pos
    
    while pos < search_end:
        next_open = content.find('<div', pos, search_end)
        next_close = content.find('</div>', pos, search_end)
        
        if next_open == -1 and next_close == -1:
            break
        
        if next_close == -1 or (next_open != -1 and next_open < next_close):
            div_count += 1
            pos = next_open + 4
        else:
            close_count += 1
            pos = next_close + 6
    
    print(f"\nFrom V2.9 div start to V2.10 comment:")
    print(f"  <div> count: {div_count}")
    print(f"  </div> count: {close_count}")
    print(f"  Net depth at V2.10: {div_count - close_count}")
    
    # 如果net depth > 0，说明V2.10被插在了V2.9模块内部
    # V2.9模块应该在div_count == close_count的地方结束
    
    # 让我们从v29_div_start开始，精确找到V2.9模块结束的位置（depth回到0）
    depth = 0
    pos = v29_div_start
    v29_end = -1
    
    # 找到第一个<div的位置
    first_div = content.find('<div', pos)
    pos = first_div
    print(f"First <div at: {first_div}")
    
    # 搜索到T91 section结束
    t91_end = content.find('<div class="section"', content.find('id="t91Synergy"') + 100)
    print(f"T91 ends at (next section): {t91_end}")
    
    while pos < t91_end:
        next_open = content.find('<div', pos, t91_end)
        next_close = content.find('</div>', pos, t91_end)
        
        if next_open == -1 and next_close == -1:
            break
        
        if next_close == -1 or (next_open != -1 and next_open < next_close):
            depth += 1
            pos = next_open + 4
        else:
            depth -= 1
            pos = next_close + 6
            if depth == 0:
                v29_end = pos
                break
    
    print(f"V2.9 module actual end: {v29_end}")
    print(f"V2.9 module length: {v29_end - v29_div_start}")
    
    # 看看V2.9结束后面的内容
    print(f"\nAfter V2.9 end (300 chars):")
    print(content[v29_end:v29_end + 300])
    
    # 现在验证：v210_pos是否等于v29_end + some_whitespace？
    # 如果是，说明插入位置是对的？
    print(f"\nV2.10 pos: {v210_pos}")
    print(f"V2.9 end: {v29_end}")
    print(f"Difference: {v210_pos - v29_end}")
