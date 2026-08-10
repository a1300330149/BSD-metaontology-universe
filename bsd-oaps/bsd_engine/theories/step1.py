with open('t79_author_conjecture.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('version: str = "V2.2"', 'version: str = "V2.3"')
with open('t79_author_conjecture.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('version updated')
