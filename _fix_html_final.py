# 完全修复HTML文件
html_path = r"c:\Users\13003\OneDrive\桌面\3333333\Agent_v2\新六系本体论_人类易懂版.html"

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Current length: {len(content)}")

# 找第二个<!DOCTYPE html>的位置（重复内容的开始）
doctype = '<!DOCTYPE html>'
first_doctype = content.find(doctype)
second_doctype = content.find(doctype, first_doctype + 10)
print(f"First doctype: {first_doctype}")
print(f"Second doctype: {second_doctype}")

if second_doctype != -1:
    # 有重复内容，说明文件是 content[:-1] + content[58338:] 的结构
    # 找到重复前的内容 = 从开头到 second_doctype 之前的部分
    # 但这个"之前的部分"本身包含了第一次错误插入的V2.10-12
    # 我们需要：从second_doctype反推原始文件的58338位置
    # 实际上 content[:-1] 的长度 = second_doctype
    # 所以 original_length = second_doctype - len(v210_12_modules) + 1 (加回被删掉的最后一个字符)
    
    # 但更简单的方法：second_doctype处的内容应该等于原始文件从58338开始的内容
    # 所以 original[58338:] = content[second_doctype:]
    # original[:58338] + v210_erroneous + original[58338:-1] = content[:second_doctype]
    # original[:58338] + v210_erroneous + original[58338:-1] + original[58338:] + new_modules + original[-1:] = content
    
    # 让我们验证：取content[second_doctype:second_doctype+100]
    # 和content[58338:58338+100] （如果58338 < second_doctype）
    # 它们应该相等
    
    print(f"\nVerification:")
    print(f"content[58338:583400] (from first half):")
    print(content[58338:58400][:200])
    print(f"\ncontent[second_doctype:second_doctype+200] (from second half):")
    print(content[second_doctype:second_doctype+200])
    
    # 如果相等，说明我们的假设正确
    # original[:58338] = content[:58338]
    # original[58338:] = content[second_doctype:]
    
    # 所以 original = content[:58338] + content[second_doctype:]
    original = content[:58338] + content[second_doctype:]
    print(f"\nReconstructed original length: {len(original)}")
    
    # 保存原始文件
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(original)
    
    print("Restored original file!")
    content = original
else:
    print("No duplicate found, file may already be original")

# 现在在正确的T91位置插入V2.10-12
# 找T91 section
t91_id = 'id="t91Synergy"'
t91_start = content.find(t91_id)
print(f"\nT91 start at: {t91_start}")

# 找T91内的V2.9模块
v29_title = '11.9.21 V2.9新增：智能体魔性接收概率'
v29_start = content.find(v29_title, t91_start)
print(f"V2.9 title in T91 at: {v29_start}")

# 找T91之后的下一个section
next_section = content.find('<div class="section"', t91_start + 100)
print(f"Next section after T91 at: {next_section}")

# 找V2.9模块的开始div - 用更宽松的搜索
# 先找V2.9标题附近的结构
v29_surrounding = content[v29_start - 500:v29_start + 100]
print(f"\nV2.9 surrounding (first 200):")
print(v29_surrounding[:300])
