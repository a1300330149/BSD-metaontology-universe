import sys

target_file = r'c:\Users\13003\OneDrive\桌面\3333333\Agent_v2\theory_code\theories\t78_xiqing_star_evolution.py'
infra_file = r'c:\Users\13003\OneDrive\桌面\3333333\Agent_v2\theory_code\infra_classes.py'

with open(target_file, 'r', encoding='utf-8') as f:
    target_content = f.read()

with open(infra_file, 'r', encoding='utf-8') as f:
    infra_content = f.read()

# 找到插入位置：在 "数值来源、标定规则、取值依据完整说明" 部分结束后，主模块类之前
# 具体锚点：数值标定类最后一行之后，主模块类注释之前
anchor = '''    ])


# ============================================================================
# 主模块类
# ============================================================================'''

if anchor not in target_content:
    print("ERROR: anchor not found")
    # 尝试找到类似的位置
    idx = target_content.find("# 主模块类")
    if idx != -1:
        print(f"Found '# 主模块类' at position {idx}")
        print(repr(target_content[idx-100:idx+100]))
    sys.exit(1)

print(f"Anchor found, inserting infra classes...")

# 插入内容
new_content = target_content.replace(anchor, infra_content + anchor, 1)

# 更新主模块类：
# 1. 版本号 V1.2 -> V1.3
# 2. 案例数 2 -> 3
# 3. 添加案例3字段
# 4. 更新__post_init__
# 5. 更新get_summary_report
# 6. 更新validate

# 更新版本和描述
new_content = new_content.replace(
    '    version: str = "V1.2"',
    '    version: str = "V1.3"'
)

new_content = new_content.replace(
    '    2. 提供两个历史案例的完整定量推演',
    '    2. 提供三个历史案例的完整定量推演'
)

new_content = new_content.replace(
    '       - 案例2：文革时期国家星体全域数理推演（1966-1976）',
    '       - 案例2：文革时期国家星体全域数理推演（1966-1976）\n       - 案例3：本世纪中国大基建国家星体全域数理推演（2001-2026）'
)

new_content = new_content.replace(
    '    5. 对比基准模型，证明顶层决策的额外解构效应',
    '    5. 对比基准模型，证明顶层决策的关键作用（解构/扩张双向验证）\n    6. 三案例横向对比，完整验证顶点相生相克公理普适性'
)

# 添加案例3字段（在案例2字段之后）
case2_fields_end = '    case2_conclusions: WengeFinalConclusions = field(default_factory=WengeFinalConclusions)'

case3_fields = '''
    case2_conclusions: WengeFinalConclusions = field(default_factory=WengeFinalConclusions)

    # ===== 案例3：大基建时期 =====
    case3_six_systems: SixSystemsInfraContext = field(default_factory=SixSystemsInfraContext)
    case3_origin: InfraOriginPotential = field(default_factory=InfraOriginPotential)
    case3_standing_wave: InfraStandingWave = field(default_factory=InfraStandingWave)
    case3_baseline: InfraBaselineComparison = field(default=None)
    case3_causal_loop: InfraCausalLoop = field(default_factory=InfraCausalLoop)
    case3_conclusions: InfraFinalConclusions = field(default_factory=InfraFinalConclusions)'''

if case2_fields_end not in new_content:
    print("ERROR: case2_fields_end not found")
    sys.exit(1)

new_content = new_content.replace(case2_fields_end, case3_fields, 1)

# 更新__post_init__
old_post_init = '''    def __post_init__(self):
        # 确保baseline正确初始化
        if self.case1_baseline is None:
            self.case1_baseline = BaselineComparison(standing_wave=self.case1_standing_wave)
        if self.case2_baseline is None:
            self.case2_baseline = WengeBaselineComparison(standing_wave=self.case2_standing_wave)'''

new_post_init = '''    def __post_init__(self):
        # 确保baseline正确初始化
        if self.case1_baseline is None:
            self.case1_baseline = BaselineComparison(standing_wave=self.case1_standing_wave)
        if self.case2_baseline is None:
            self.case2_baseline = WengeBaselineComparison(standing_wave=self.case2_standing_wave)
        if self.case3_baseline is None:
            self.case3_baseline = InfraBaselineComparison(standing_wave=self.case3_standing_wave)'''

if old_post_init not in new_content:
    print("ERROR: old_post_init not found")
    sys.exit(1)

new_content = new_content.replace(old_post_init, new_post_init, 1)

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Step 1 done: classes and fields inserted")
print(f"New file length: {len(new_content)} chars")
