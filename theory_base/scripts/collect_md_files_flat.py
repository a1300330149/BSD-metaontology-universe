import os
import shutil

base_path = r"c:\Users\13003\OneDrive\桌面\3333333\Agent_v2\theory_base"
output_dir = os.path.join(base_path, "_文档集导入_扁平版")

def get_all_md_files():
    results = []
    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        dirs[:] = [d for d in dirs if d not in ['_文档集导入_扁平版']]
        for f in files:
            if f.endswith('.md') and not f.startswith('~'):
                filepath = os.path.join(root, f)
                rel_path = os.path.relpath(filepath, base_path)
                results.append({
                    'original_path': filepath,
                    'relative_path': rel_path,
                    'filename': f
                })
    return results

def generate_flat_name(file_info, index):
    rel = file_info['relative_path'].replace('\\', '/')
    parts = rel.split('/')
    prefix = []
    for p in parts[:-1]:
        if p.startswith('L0_'):
            prefix.append('L0')
        elif p.startswith('L1_'):
            prefix.append('L1')
        elif p.startswith('L2_'):
            prefix.append('L2')
        elif p.startswith('L3_'):
            prefix.append('L3')
        elif p.startswith('00_'):
            prefix.append('IDX')
        elif p.startswith('_'):
            prefix.append(p.replace('_', '')[:4])
        else:
            clean = p.replace('_', '')[:4]
            prefix.append(clean)
    prefix_str = '_'.join(prefix)
    filename = file_info['filename']
    flat_name = f"{str(index).zfill(3)}_{prefix_str}_{filename}"
    return flat_name

def main():
    print("=" * 60)
    print("  理论库文档集扁平化工具")
    print("=" * 60)
    print()
    
    files = get_all_md_files()
    print(f"找到 {len(files)} 个MD文件")
    print()
    
    if os.path.exists(output_dir):
        print("清理旧目录...")
        shutil.rmtree(output_dir)
    
    os.makedirs(output_dir)
    print(f"创建目录：{output_dir}")
    print()
    
    manifest = []
    manifest.append("# 文档集导入 · 文件清单")
    manifest.append(f"> 文件总数：{len(files)} 个")
    manifest.append("")
    manifest.append("| 序号 | 扁平文件名 | 原路径 |")
    manifest.append("|:----:|-----------|--------|")
    
    for i, file_info in enumerate(files, 1):
        flat_name = generate_flat_name(file_info, i)
        dest_path = os.path.join(output_dir, flat_name)
        shutil.copy2(file_info['original_path'], dest_path)
        manifest.append(f"| {i} | `{flat_name}` | `{file_info['relative_path'].replace('\\', '/')}` |")
        if i % 50 == 0:
            print(f"  已处理 {i}/{len(files)}")
    
    manifest_path = os.path.join(output_dir, "000_文件清单与对应关系.md")
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(manifest))
    
    print(f"完成！共 {len(files)} 个文件")
    print(f"输出目录：{output_dir}")
    print()
    print("使用方法：")
    print("  1. 打开 TRAE Work CN")
    print("  2. 进入 文档集 / 知识库")
    print("  3. 选择 批量导入 / 添加文件夹")
    print(f"  4. 选择目录：{output_dir}")
    print("  5. 等待导入完成")

if __name__ == "__main__":
    main()
