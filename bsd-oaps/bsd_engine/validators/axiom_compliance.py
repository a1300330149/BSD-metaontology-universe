"""
归属基底：第0重元道本源基底
对应三界秩序：天道
对应公理：全部39条公理合规性
对应九维维度：元理天道、天道原理
理论原文出处：theory_base/L0_总本源层/全域理论全集
固定数理常量：γ=0.92, κ=0.35

bsd-verify-axiom CLI 入口
—— 公理合规性验证命令行入口，委托 compliance_checker 执行完整检查
"""
from bsd_engine.validators.compliance_checker import run_full_compliance_check


def main():
    """主程序：执行完整公理合规性检查"""
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    results = run_full_compliance_check()
    return 0 if results["overall_pass"] else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
