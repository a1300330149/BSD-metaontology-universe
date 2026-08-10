# 修复HTML - 找到重复起点并删除重复内容
html_path = r"c:\Users\13003\OneDrive\桌面\3333333\Agent_v2\新六系本体论_人类易懂版.html"

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Current length: {len(content)}")

# 第一个T91位置
first_t91 = content.find('id="t91Synergy"')
second_t91 = content.find('id="t91Synergy"', first_t91 + 10)
print(f"First T91: {first_t91}")
print(f"Second T91: {second_t91}")

# 重复偏移量 = second_t91 - first_t91
offset = second_t91 - first_t91
print(f"Offset: {offset}")

# 验证：content[:len(content)-offset] 是否等于 content[offset:]
# 不对，应该是 content[offset:] 是否等于 content[:len(content)-offset]
# 让我们验证前100字符
print(f"\ncontent[:100]:")
print(content[:100])
print(f"\ncontent[offset:offset+100]:")
print(content[offset:offset+100])
print(f"\nEqual: {content[:100] == content[offset:offset+100]}")

# 如果相等，说明content = original + original[offset:] ???
# 不对，应该是 content = A + B, B = original
# 让我们看看结尾
print(f"\nLast 100 chars:")
print(content[-100:])

# 找文件结尾的</html>
html_end = content.rfind('</html>')
print(f"\nLast </html> at: {html_end}")
print(f"Length from there: {len(content) - html_end}")

# 第一个</html>的位置
first_html_end = content.find('</html>')
print(f"First </html> at: {first_html_end}")

if first_html_end + 7 < len(content) - 100:
    print(f"\nContent after first </html>:")
    print(content[first_html_end + 7:first_html_end + 107])
