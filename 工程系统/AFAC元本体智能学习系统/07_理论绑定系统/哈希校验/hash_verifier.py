"""
归属基底：第规则相位位（第二位）
对应三界秩序：天道秩序
对应公理：第1条（宿命/舒适双边界公理）
对应九维维度：天道原理/天道动力学
理论原文出处：《元本体理论分册》第一章
核心数理参数：SHA256锁档哈希

场3：哈希校验脚本
实现文档哈希一致性自动校验
"""

import hashlib
import datetime
import re
from pathlib import Path
from typing import Dict, List, Tuple

# ==================== 固定数理参数（锁档核心） ====================
# SHA256锁档哈希（禁止修改）
LOCK_HASH = "e62f918340dc2975108294736ac8927d90584136972485931027958740925713"


class HashVerifier:
    """
    功能：文档哈希一致性校验器
    理论映射：规则相位位（第二位）·宿命边界公理
    能级关联：E3=0.90三阶道心能级校验标准
    约束来源：宿命/舒适双边界公理（公理一）
    禁止修改：锁档哈希值，修改会破坏确权铁律
    """
    
    def __init__(self, project_root: str):
        """
        初始化哈希校验器
        
        对应公理：公理一（宿命/舒适双边界公理）
        理论映射：锁档哈希校验初始化
        
        Args:
            project_root: 项目根目录
        """
        self.project_root = Path(project_root)
        self.verification_log = []
    
    def compute_file_hash(self, file_path: Path) -> str:
        """
        计算文件SHA256哈希
        
        对应公理：公理一（宿命/舒适双边界公理）
        理论映射：哈希计算
        
        Args:
            file_path: 文件路径
        
        Returns:
            str: SHA256哈希值
        """
        content = file_path.read_bytes()
        return hashlib.sha256(content).hexdigest()
    
    def verify_lock_hash_in_file(self, file_path: Path) -> Dict:
        """
        校验文件内锁档哈希一致性
        
        对应公理：公理一（宿命/舒适双边界公理）
        理论映射：锁档哈希校验
        
        Args:
            file_path: 文件路径
        
        Returns:
            Dict: 校验结果
        """
        content = file_path.read_text(encoding='utf-8')
        
        # 检查是否包含锁档哈希
        has_lock_hash = LOCK_HASH in content
        
        # 检查是否包含其他哈希声明
        hash_pattern = r'[a-fA-F0-9]{64}'
        found_hashes = re.findall(hash_pattern, content) if 're' in dir() else []
        
        # 检查哈希一致性
        hash_consistent = True
        inconsistent_hashes = []
        
        for h in found_hashes:
            if h != LOCK_HASH:
                hash_consistent = False
                inconsistent_hashes.append(h)
        
        return {
            "file": file_path.name,
            "has_lock_hash": has_lock_hash,
            "hash_consistent": hash_consistent,
            "inconsistent_hashes": inconsistent_hashes,
            "status": "PASS" if has_lock_hash and hash_consistent else "FAIL"
        }
    
    def scan_all_files(self) -> List[Path]:
        """
        扫描所有需要校验的文件
        
        对应公理：公理一（宿命/舒适双边界公理）
        理论映射：全文件扫描
        
        Returns:
            List[Path]: 文件路径列表
        """
        all_files = []
        
        # 扫描md文档
        all_files.extend(self.project_root.glob("**/*.md"))
        
        # 扫描Python代码
        all_files.extend(self.project_root.glob("src/**/*.py"))
        
        # 扫描配置文件
        all_files.extend(self.project_root.glob("configs/*.yaml"))
        
        # 扫描规则文件
        rules_path = self.project_root / ".trae" / "rules"
        if rules_path.exists():
            all_files.extend(rules_path.glob("*.md"))
        
        return all_files
    
    def run_full_verification(self) -> Dict:
        """
        执行全量哈希校验
        
        对应公理：公理一（宿命/舒适双边界公理）
        理论映射：全量哈希校验
        
        Returns:
            Dict: 校验结果汇总
        """
        files = self.scan_all_files()
        
        results = {
            "total_files": len(files),
            "pass_files": 0,
            "fail_files": 0,
            "missing_hash_files": [],
            "inconsistent_hash_files": [],
            "verification_details": []
        }
        
        for file in files:
            verify_result = self.verify_lock_hash_in_file(file)
            results["verification_details"].append(verify_result)
            
            if verify_result["status"] == "PASS":
                results["pass_files"] += 1
            else:
                results["fail_files"] += 1
                
                if not verify_result["has_lock_hash"]:
                    results["missing_hash_files"].append(file.name)
                
                if not verify_result["hash_consistent"]:
                    results["inconsistent_hash_files"].append({
                        "file": file.name,
                        "inconsistent_hashes": verify_result["inconsistent_hashes"]
                    })
        
        return results
    
    def generate_verification_report(self) -> str:
        """
        生成哈希校验报告
        
        对应公理：公理一（宿命/舒适双边界公理）
        理论映射：哈希校验报告输出
        
        Returns:
            str: 报告文件路径
        """
        results = self.run_full_verification()
        
        report_path = self.project_root / "哈希校验报告.md"
        
        content = f"""# 哈希校验报告

## 生成时间
{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## SHA256锁档哈希
{LOCK_HASH}

## 校验结果汇总

| 指标 | 数值 |
|------|------|
| 文件总数 | {results['total_files']} |
| 通过文件 | {results['pass_files']} |
| 失败文件 | {results['fail_files']} |
| 通过率 | {results['pass_files'] / results['total_files'] * 100:.2f}% |

## 缺失哈希文件清单

"""
        
        if results["missing_hash_files"]:
            for f in results["missing_hash_files"]:
                content += f"- {f}\n"
        else:
            content += "- 无缺失哈希文件\n"
        
        content += "\n## 哈希不一致文件清单\n\n"
        
        if results["inconsistent_hash_files"]:
            for item in results["inconsistent_hash_files"]:
                content += f"- {item['file']}: 发现不一致哈希 {item['inconsistent_hashes']}\n"
        else:
            content += "- 无哈希不一致文件\n"
        
        content += "\n---\n"
        content += "本报告由哈希校验器自动生成，遵循四位一体驻波动力学框架理论约束。\n"
        
        report_path.write_text(content, encoding='utf-8')
        
        return str(report_path)
    
    def verify_rules_file(self) -> bool:
        """
        校验规则文件哈希
        
        对应公理：公理一（宿命/舒适双边界公理）
        理论映射：顶层规则哈希校验
        
        Returns:
            bool: 是否校验通过
        """
        rules_path = self.project_root / ".trae" / "rules" / "meta_theory_constraint.md"
        
        if not rules_path.exists():
            print(f"[ERROR] 规则文件不存在: {rules_path}")
            return False
        
        content = rules_path.read_text(encoding='utf-8')
        
        if LOCK_HASH in content:
            print(f"[SUCCESS] 规则文件哈希校验通过")
            return True
        else:
            print(f"[ERROR] 规则文件哈希校验失败，锁档哈希缺失")
            return False


def main():
    """
    主程序入口
    
    对应公理：公理一（宿命/舒适双边界公理）
    理论映射：哈希校验启动
    """
    import argparse
    import re
    
    parser = argparse.ArgumentParser(description="场3：哈希校验器")
    parser.add_argument("--project-root", default=".", help="项目根目录")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("场3：哈希校验器")
    print("归属基底：第规则相位位（第二位）")
    print("对应公理：公理一（宿命/舒适双边界公理）")
    print("=" * 60)
    
    verifier = HashVerifier(args.project_root)
    
    # 校验规则文件
    rules_pass = verifier.verify_rules_file()
    
    # 执行全量校验
    report_path = verifier.generate_verification_report()
    
    print(f"\n哈希校验报告: {report_path}")
    
    if rules_pass:
        print("\n✅ 顶层规则哈希校验通过")
    else:
        print("\n❌ 顶层规则哈希校验失败，请检查规则文件")
    
    print("\n" + "=" * 60)
    print("SHA256锁档哈希:", LOCK_HASH)
    print("=" * 60)


if __name__ == "__main__":
    main()