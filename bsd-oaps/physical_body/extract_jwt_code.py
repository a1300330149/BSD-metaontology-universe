import os

file_path = r'D:\TRAE SOLO CN\resources\app\node_modules\@byted-icube\ai-modules-chat\dist\index.mjs'
keyword = 'getCloudIdeJwt'
context_lines = 30

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
else:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"Total lines: {len(lines)}")

    matches = []
    for i, line in enumerate(lines):
        if keyword in line:
            matches.append((i+1, line))

    print(f"\nFound {len(matches)} matches for '{keyword}'")

    for idx, (match_line, line_content) in enumerate(matches[:2]):
        print(f"\n{'='*60}")
        print(f"Match {idx+1} at line {match_line}")
        print(f"{'='*60}")
        
        start = max(0, match_line - context_lines)
        end = min(len(lines), match_line + context_lines)
        
        print(''.join(lines[start:end]))
