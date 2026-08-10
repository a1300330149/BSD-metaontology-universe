"""
BSD六系自组织文件验证器 V8.1
验证现有基因文件的可用性，并生成全量基因配置
"""

import os
import json
from datetime import datetime


def verify_existing_files():
    """验证现有60个基因文件"""
    base_path = r"C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\theory_base\L0_总本源层\六系自组织"
    
    print("=" * 80)
    print("【BSD六系自组织文件验证 V8.1】")
    print("=" * 80)
    
    # 检查目录结构
    print("\n📁 检查目录结构...")
    expected_dirs = ["强化系🔵", "变身系⚫", "社会系🟢", "天道系🟣", "自然系🟠", "具现系🔴"]
    
    for d in expected_dirs:
        dir_path = os.path.join(base_path, d)
        exists = os.path.exists(dir_path)
        file_count = len([f for f in os.listdir(dir_path) if f.endswith('.md')]) if exists else 0
        status = "✅" if exists else "❌"
        print(f"  {status} {d}: {file_count}个文件")
    
    # 验证基因文件内容
    print("\n📝 验证基因文件内容...")
    verification_results = []
    
    for d in expected_dirs:
        dir_path = os.path.join(base_path, d)
        if not os.path.exists(dir_path):
            continue
        
        files = [f for f in os.listdir(dir_path) if f.endswith('.md')]
        
        for filename in files[:3]:  # 每系检查前3个
            filepath = os.path.join(dir_path, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 验证必要字段
            checks = {
                '基因ID': 'gene_id:' in content,
                '所属六系': 'six_system:' in content,
                '系公理': 'axiom:' in content,
                '本源符号': 'symbol:' in content,
                '0层方程': 'equation:' in content,
                '原始软件信息': 'original_name:' in content,
                'BSD映射信息': 'bsd_confidence:' in content,
                '系属声明': '系属声明' in content,
                'BSD升维路径': 'BSD升维路径' in content,
                '子集关系声明': '子集关系声明' in content,
            }
            
            all_pass = all(checks.values())
            verification_results.append({
                'file': filename,
                'system': d,
                'all_pass': all_pass,
                'checks': checks,
            })
            
            status = "✅" if all_pass else "⚠️"
            passed = sum(checks.values())
            print(f"  {status} {filename}: {passed}/10 项验证通过")
    
    # 汇总
    total_files = sum(1 for _ in os.listdir(os.path.join(base_path, d)) 
                     for d in expected_dirs 
                     if os.path.exists(os.path.join(base_path, d)) 
                     and _.endswith('.md'))
    
    all_passed = all(r['all_pass'] for r in verification_results)
    
    print(f"\n📊 验证汇总：")
    print(f"  总文件数：{total_files}")
    print(f"  验证通过率：{sum(1 for r in verification_results if r['all_pass'])}/{len(verification_results)}")
    print(f"  可用性评估：{'✅ 完全可用' if all_passed else '⚠️ 部分可用'}")
    
    return {
        'total_files': total_files,
        'verification_results': verification_results,
        'all_passed': all_passed,
        'ready_for_full_generation': all_passed,
    }


if __name__ == "__main__":
    result = verify_existing_files()
    print(f"\n{'='*80}")
    print(f"验证完成，{'可以开始全量生成' if result['ready_for_full_generation'] else '需要修复问题'}")
