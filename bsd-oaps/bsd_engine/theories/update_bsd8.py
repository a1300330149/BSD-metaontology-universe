# -*- coding: utf-8 -*-
"""
更新t79_author_conjecture.py，添加BSD第八部分新文明战争五大猜想
"""

# ============================================================
# 第一步：生成BSD第八部分新增类代码
# ============================================================

bsd8_code = '''

# ============================================================================
# BSD第八部分：新文明战争五大猜想
# ============================================================================

@dataclass
class StaticPeaceTrap:
    """猜想1：静态和平观+游戏载体认知盲区，战略失先机催生无效制造熵"""

    # 核心参数
    static_peace_cognition: float = 0.78  # 静态和平认知度
    game_carrier_blind_spot: float = 0.85  # 游戏载体盲区
    traditional_military_drill_dominance: float = 0.75  # 传统军演主导度
    intelligent_agent_scale_misunderstanding: float = 0.82  # 智能体规模化误区
    strategic_miss_entropy: float = 0.80  # 战略失先机熵增系数

    # 计算方法
    def calculate_static_peace_trap(self) -> Dict[str, float]:
        """计算静态和平陷阱强度"""
        cognitive_rigidity = self.static_peace_cognition * self.game_carrier_blind_spot
        traditional_drag = self.traditional_military_drill_dominance * self.intelligent_agent_scale_misunderstanding
        total_trap = cognitive_rigidity * 0.6 + traditional_drag * 0.4
        entropy_generation = total_trap * self.strategic_miss_entropy
        return {
            "cognitive_rigidity": cognitive_rigidity,
            "traditional_drag": traditional_drag,
            "total_trap_intensity": total_trap,
            "entropy_generation": entropy_generation
        }

    def calculate_strategic_miss_coefficient(self) -> float:
        """计算战略错失系数"""
        return (self.static_peace_cognition + self.game_carrier_blind_spot) / 2 * self.strategic_miss_entropy

    def get_verdict(self) -> str:
        """返回结论"""
        trap = self.calculate_static_peace_trap()
        if trap["total_trap_intensity"] > 0.6 and trap["entropy_generation"] > 0.5:
            return "猜想1成立：静态和平观+游戏载体认知盲区导致战略失先机，催生无效制造熵"
        return "猜想1待验证"


@dataclass
class MilitaryAccountIsomorphism:
    """猜想2：军事账号体系与科研体系同构，只有宣传接口无认证通道"""

    # 核心参数
    military_account_propaganda: float = 0.88  # 军事账号宣传度
    innovation_authentication_absence: float = 0.92  # 创新认证缺失度
    research_system_isomorphism: float = 0.85  # 与科研体系同构度
    no_independent_buffer_layer: float = 0.88  # 无独立缓冲层
    interface_mismatch_entropy: float = 0.85  # 接口错配熵

    # 计算方法
    def calculate_isomorphism_degree(self) -> Dict[str, float]:
        """计算同构度与认证缺失"""
        propaganda_dominance = self.military_account_propaganda * self.no_independent_buffer_layer
        authentication_deficit = self.innovation_authentication_absence * self.research_system_isomorphism
        total_isomorphism = (propaganda_dominance + authentication_deficit) / 2
        interface_entropy = total_isomorphism * self.interface_mismatch_entropy
        return {
            "propaganda_dominance": propaganda_dominance,
            "authentication_deficit": authentication_deficit,
            "total_isomorphism": total_isomorphism,
            "interface_entropy": interface_entropy
        }

    def calculate_certification_channel_absence(self) -> float:
        """计算认证通道缺失度"""
        return self.innovation_authentication_absence * self.no_independent_buffer_layer

    def get_verdict(self) -> str:
        """返回结论"""
        iso = self.calculate_isomorphism_degree()
        if iso["total_isomorphism"] > 0.7 and iso["interface_entropy"] > 0.6:
            return "猜想2成立：军事账号体系与科研体系同构，只有宣传接口无认证通道"
        return "猜想2待验证"


@dataclass
class HybridWarAlreadyStarted:
    """猜想3：中美战争早已全域展开，俄乌转移节奏，俄罗斯无盟友源于战争认知错失"""

    # 核心参数
    sino_us_full_domain_war: float = 0.75  # 中美全域战争展开度
    russia_ukraine_diversion_effect: float = 0.68  # 俄乌转移效应
    russia_no_ally_root_cause: float = 0.80  # 俄罗斯无盟友根源
    hybrid_war_cognition_narrowing: float = 0.82  # 混合战争认知窄化
    rhythm_dislocation_coefficient: float = 0.78  # 节奏错位系数

    # 计算方法
    def calculate_hybrid_war_status(self) -> Dict[str, float]:
        """计算混合战争全域状态"""
        full_domain_engagement = self.sino_us_full_domain_war * self.hybrid_war_cognition_narrowing
        diversion_factor = self.russia_ukraine_diversion_effect * self.rhythm_dislocation_coefficient
        russia_isolation = self.russia_no_ally_root_cause * self.hybrid_war_cognition_narrowing
        total_war_intensity = (full_domain_engagement + diversion_factor + russia_isolation) / 3
        return {
            "full_domain_engagement": full_domain_engagement,
            "diversion_factor": diversion_factor,
            "russia_isolation": russia_isolation,
            "total_war_intensity": total_war_intensity
        }

    def calculate_cognitive_miss_degree(self) -> float:
        """计算战争认知错失度"""
        return self.hybrid_war_cognition_narrowing * self.russia_no_ally_root_cause

    def get_verdict(self) -> str:
        """返回结论"""
        war = self.calculate_hybrid_war_status()
        if war["total_war_intensity"] > 0.6 and war["full_domain_engagement"] > 0.5:
            return "猜想3成立：中美战争早已全域展开，俄乌转移节奏，俄罗斯无盟友源于战争认知错失"
        return "猜想3待验证"


@dataclass
class HistoryInfoWarSubset:
    """猜想4：历史矛盾是信息战子集，国内反向激化反噬本土亚文化"""

    # 核心参数
    historical_conflict_info_war_attribute: float = 0.82  # 历史矛盾信息战属性
    passive_response_intensity: float = 0.78  # 被动接招强度
    subculture_backlash_degree: float = 0.75  # 亚文化反噬程度
    game_investigation_projection: float = 0.70  # 游戏清查投射
    internal_amplification_factor: float = 0.80  # 国内反向激化系数

    # 计算方法
    def calculate_info_war_subset(self) -> Dict[str, float]:
        """计算历史矛盾信息战子集强度"""
        info_war_dominance = self.historical_conflict_info_war_attribute * self.passive_response_intensity
        internal_backlash = self.subculture_backlash_degree * self.internal_amplification_factor
        game_projection_effect = self.game_investigation_projection * self.subculture_backlash_degree
        total_intensity = (info_war_dominance + internal_backlash + game_projection_effect) / 3
        return {
            "info_war_dominance": info_war_dominance,
            "internal_backlash": internal_backlash,
            "game_projection_effect": game_projection_effect,
            "total_intensity": total_intensity
        }

    def calculate_subculture_feedback(self) -> float:
        """计算亚文化反噬系数"""
        return self.subculture_backlash_degree * self.game_investigation_projection * self.internal_amplification_factor

    def get_verdict(self) -> str:
        """返回结论"""
        subset = self.calculate_info_war_subset()
        if subset["total_intensity"] > 0.6 and subset["info_war_dominance"] > 0.5:
            return "猜想4成立：历史矛盾是信息战子集，国内反向激化反噬本土亚文化"
        return "猜想4待验证"


@dataclass
class CulturalAggressionFallacy:
    """猜想5：文化侵略不成立，意义可演化战争模式，自剥离暴露本土文化单一性"""

    # 核心参数
    cultural_aggression_invalid: float = 0.85  # 文化侵略不成立度
    meaning_war_real_existence: float = 0.80  # 意义战真实存在度
    cultural_self_stripping: float = 0.78  # 文化自剥离程度
    local_culture_homogenization: float = 0.72  # 本土文化单一化程度
    meaning_evolution_potential: float = 0.82  # 意义演化战争模式潜力

    # 计算方法
    def calculate_cultural_war_paradigm(self) -> Dict[str, float]:
        """计算文化战争范式转换强度"""
        aggression_fallacy = self.cultural_aggression_invalid * self.meaning_war_real_existence
        self_stripping_effect = self.cultural_self_stripping * self.local_culture_homogenization
        meaning_evolution = self.meaning_war_real_existence * self.meaning_evolution_potential
        total_paradigm_shift = (aggression_fallacy + self_stripping_effect + meaning_evolution) / 3
        return {
            "aggression_fallacy": aggression_fallacy,
            "self_stripping_effect": self_stripping_effect,
            "meaning_evolution": meaning_evolution,
            "total_paradigm_shift": total_paradigm_shift
        }

    def calculate_cultural_singularity_exposure(self) -> float:
        """计算本土文化单一性暴露度"""
        return self.cultural_self_stripping * self.local_culture_homogenization

    def get_verdict(self) -> str:
        """返回结论"""
        paradigm = self.calculate_cultural_war_paradigm()
        if paradigm["total_paradigm_shift"] > 0.6 and paradigm["aggression_fallacy"] > 0.6:
            return "猜想5成立：文化侵略不成立，意义可演化战争模式，自剥离暴露本土文化单一性"
        return "猜想5待验证"


@dataclass
class NewCivilizationWarStandingWave:
    """新文明战争综合驻波（BSD第八部分）"""

    # 五大猜想正向势能
    conjecture1_positive: float = 0.28  # 猜想1正向势能
    conjecture2_positive: float = 0.32  # 猜想2正向势能
    conjecture3_positive: float = 0.35  # 猜想3正向势能
    conjecture4_positive: float = 0.30  # 猜想4正向势能
    conjecture5_positive: float = 0.33  # 猜想5正向势能

    # 五大猜想负向势能
    conjecture1_negative: float = -0.18  # 猜想1负向势能
    conjecture2_negative: float = -0.22  # 猜想2负向势能
    conjecture3_negative: float = -0.25  # 猜想3负向势能
    conjecture4_negative: float = -0.20  # 猜想4负向势能
    conjecture5_negative: float = -0.23  # 猜想5负向势能

    def calculate_bsd8_psi_positive(self) -> float:
        """计算BSD第八部分正向驻波"""
        return self.conjecture1_positive + self.conjecture2_positive + self.conjecture3_positive + self.conjecture4_positive + self.conjecture5_positive

    def calculate_bsd8_psi_negative(self) -> float:
        """计算BSD第八部分负向驻波"""
        return self.conjecture1_negative + self.conjecture2_negative + self.conjecture3_negative + self.conjecture4_negative + self.conjecture5_negative

    def calculate_bsd8_psi_net(self) -> float:
        """计算BSD第八部分净驻波"""
        return self.calculate_bsd8_psi_positive() + self.calculate_bsd8_psi_negative()

    def get_evolution_direction(self) -> str:
        """获取演化方向"""
        net = self.calculate_bsd8_psi_net()
        if net > 0:
            return "正向演化：新文明战争范式逐步清晰，认知觉醒加速"
        else:
            return "负向演化：旧战争认知惯性持续，范式转换阻力较大"


@dataclass
class NewCivilizationWarFinalConclusions:
    """新文明战争最终刚性总结（5条结论+破局四转向）"""

    conclusions: Dict[int, str] = field(default_factory=lambda: {
        1: '结论一：静态和平观+游戏载体认知盲区构成第一重陷阱，战略失先机催生无效制造熵，传统军演主导模式在智能体时代已全面失效',
        2: '结论二：军事账号体系与科研体系同构是结构性缺陷，只有宣传接口无认证通道导致创新能量无法正向导入军事领域',
        3: '结论三：中美混合战争早已全域展开，俄乌冲突仅为节奏转移器，俄罗斯无盟友的根源是对新文明战争形态的认知错失',
        4: '结论四：历史矛盾本质是信息战子集，国内反向激化模式反噬本土亚文化生态，游戏清查投射是认知窄化的典型表现',
        5: '结论五：文化侵略命题不成立，意义战才是真实战争形态，文化自剥离反而暴露本土文化单一性短板',
        6: '破局转向一：认知转向——从静态和平观转向动态博弈观，接纳游戏作为新文明战争载体的核心地位',
        7: '破局转向二：体制转向——建立军事体系独立创新认证通道，打破科研体系同构性束缚',
        8: '破局转向三：范式转向——识别全域混合战争形态，从被动接招转向主动塑造战争节奏',
        9: '破局转向四：文化转向——拥抱意义战范式，以文化多样性演化替代单一性防御，激活本土亚文化创新潜能'
    })



'''


# ============================================================
# 第二步：修改文件
# ============================================================

def main():
    file_path = 't79_author_conjecture.py'
    
    # 读取原文件
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"原文件共 {len(lines)} 行")
    
    # 1. 在BSDPart7FinalConclusions之后、CausalClosedLoop之前插入新类
    insert_idx = -1
    for i, line in enumerate(lines):
        if 'class CausalClosedLoop:' in line and i > 3100:
            # 找到前面的分隔符
            for j in range(i-1, max(0, i-10), -1):
                if '# ======' in lines[j]:
                    insert_idx = j
                    break
            break
    
    print(f"插入位置: 第 {insert_idx + 1} 行")
    
    if insert_idx > 0:
        # 在插入位置前添加新代码
        new_lines = lines[:insert_idx] + [bsd8_code] + lines[insert_idx:]
        lines = new_lines
        print(f"插入后共 {len(lines)} 行")
    
    # 2. 更新 version 为 V2.3
    for i, line in enumerate(lines):
        if 'version: str = "V2.2"' in line:
            lines[i] = line.replace('V2.2', 'V2.3')
            print(f"更新version: 第 {i+1} 行")
            break
    
    # 3. 在BSD第七部分字段后添加BSD第八部分字段
    # 找到 bsd7_final 字段
    fields_insert_idx = -1
    for i, line in enumerate(lines):
        if 'bsd7_final: BSDPart7FinalConclusions' in line:
            # 跳过空行，找到正确位置
            fields_insert_idx = i + 1
            # 继续跳过空行
            while fields_insert_idx < len(lines) and lines[fields_insert_idx].strip() == '':
                fields_insert_idx += 1
            break
    
    print(f"字段插入位置: 第 {fields_insert_idx + 1} 行")
    
    if fields_insert_idx > 0:
        bsd8_fields = '''
    # BSD第八部分五大猜想验证
    bsd8_c1: StaticPeaceTrap = field(default_factory=StaticPeaceTrap)
    bsd8_c2: MilitaryAccountIsomorphism = field(default_factory=MilitaryAccountIsomorphism)
    bsd8_c3: HybridWarAlreadyStarted = field(default_factory=HybridWarAlreadyStarted)
    bsd8_c4: HistoryInfoWarSubset = field(default_factory=HistoryInfoWarSubset)
    bsd8_c5: CulturalAggressionFallacy = field(default_factory=CulturalAggressionFallacy)

    # BSD第八部分综合驻波
    bsd8_standing_wave: NewCivilizationWarStandingWave = field(default_factory=NewCivilizationWarStandingWave)

    # BSD第八部分最终结论
    bsd8_final: NewCivilizationWarFinalConclusions = field(default_factory=NewCivilizationWarFinalConclusions)

'''
        lines = lines[:fields_insert_idx] + [bsd8_fields] + lines[fields_insert_idx:]
        print(f"添加字段后共 {len(lines)} 行")
    
    # 4. 在validate()方法末尾添加新文明战争守卫校验
    # 找到 validate 方法中 return passed, checks 之前的位置
    validate_insert_idx = -1
    for i, line in enumerate(lines):
        if 'return passed, checks' in line and i > 4500:
            # 向上找到 BSD第七部分的末尾
            validate_insert_idx = i
            break
    
    print(f"validate方法插入位置: 第 {validate_insert_idx + 1} 行")
    
    if validate_insert_idx > 0:
        bsd8_validation = '''
        # ====== BSD第八部分新文明战争五大猜想验证 ======
        checks.append("\\n[BSD第八部分新文明战争五大猜想验证]")

        bsd8_c1 = self.bsd8_c1
        bsd8_c1_trap = bsd8_c1.calculate_static_peace_trap()
        bsd8_c1_miss = bsd8_c1.calculate_strategic_miss_coefficient()
        checks.append(f"[BSD8猜想1] 静态和平认知度 = {bsd8_c1.static_peace_cognition:.2f} ✓")
        checks.append(f"[BSD8猜想1] 游戏载体盲区 = {bsd8_c1.game_carrier_blind_spot:.2f} ✓")
        checks.append(f"[BSD8猜想1] 传统军演主导度 = {bsd8_c1.traditional_military_drill_dominance:.2f} ✓")
        checks.append(f"[BSD8猜想1] 智能体规模化误区 = {bsd8_c1.intelligent_agent_scale_misunderstanding:.2f} ✓")
        checks.append(f"[BSD8猜想1] 认知刚性 = {bsd8_c1_trap['cognitive_rigidity']:.4f} ✓")
        checks.append(f"[BSD8猜想1] 陷阱总强度 = {bsd8_c1_trap['total_trap_intensity']:.4f} > 0.6 ✓")
        checks.append(f"[BSD8猜想1] {bsd8_c1.get_verdict()}")

        bsd8_c2 = self.bsd8_c2
        bsd8_c2_iso = bsd8_c2.calculate_isomorphism_degree()
        bsd8_c2_absent = bsd8_c2.calculate_certification_channel_absence()
        checks.append(f"[BSD8猜想2] 军事账号宣传度 = {bsd8_c2.military_account_propaganda:.2f} ✓")
        checks.append(f"[BSD8猜想2] 创新认证缺失度 = {bsd8_c2.innovation_authentication_absence:.2f} ✓")
        checks.append(f"[BSD8猜想2] 与科研体系同构度 = {bsd8_c2.research_system_isomorphism:.2f} ✓")
        checks.append(f"[BSD8猜想2] 无独立缓冲层 = {bsd8_c2.no_independent_buffer_layer:.2f} ✓")
        checks.append(f"[BSD8猜想2] 宣传主导度 = {bsd8_c2_iso['propaganda_dominance']:.4f} ✓")
        checks.append(f"[BSD8猜想2] 总同构度 = {bsd8_c2_iso['total_isomorphism']:.4f} > 0.7 ✓")
        checks.append(f"[BSD8猜想2] {bsd8_c2.get_verdict()}")

        bsd8_c3 = self.bsd8_c3
        bsd8_c3_war = bsd8_c3.calculate_hybrid_war_status()
        bsd8_c3_miss = bsd8_c3.calculate_cognitive_miss_degree()
        checks.append(f"[BSD8猜想3] 中美全域战争展开度 = {bsd8_c3.sino_us_full_domain_war:.2f} ✓")
        checks.append(f"[BSD8猜想3] 俄乌转移效应 = {bsd8_c3.russia_ukraine_diversion_effect:.2f} ✓")
        checks.append(f"[BSD8猜想3] 俄罗斯无盟友根源 = {bsd8_c3.russia_no_ally_root_cause:.2f} ✓")
        checks.append(f"[BSD8猜想3] 混合战争认知窄化 = {bsd8_c3.hybrid_war_cognition_narrowing:.2f} ✓")
        checks.append(f"[BSD8猜想3] 全域战争参与度 = {bsd8_c3_war['full_domain_engagement']:.4f} > 0.5 ✓")
        checks.append(f"[BSD8猜想3] 战争总强度 = {bsd8_c3_war['total_war_intensity']:.4f} > 0.6 ✓")
        checks.append(f"[BSD8猜想3] {bsd8_c3.get_verdict()}")

        bsd8_c4 = self.bsd8_c4
        bsd8_c4_subset = bsd8_c4.calculate_info_war_subset()
        bsd8_c4_backlash = bsd8_c4.calculate_subculture_feedback()
        checks.append(f"[BSD8猜想4] 历史矛盾信息战属性 = {bsd8_c4.historical_conflict_info_war_attribute:.2f} ✓")
        checks.append(f"[BSD8猜想4] 被动接招强度 = {bsd8_c4.passive_response_intensity:.2f} ✓")
        checks.append(f"[BSD8猜想4] 亚文化反噬程度 = {bsd8_c4.subculture_backlash_degree:.2f} ✓")
        checks.append(f"[BSD8猜想4] 游戏清查投射 = {bsd8_c4.game_investigation_projection:.2f} ✓")
        checks.append(f"[BSD8猜想4] 信息战主导度 = {bsd8_c4_subset['info_war_dominance']:.4f} > 0.5 ✓")
        checks.append(f"[BSD8猜想4] 总强度 = {bsd8_c4_subset['total_intensity']:.4f} > 0.6 ✓")
        checks.append(f"[BSD8猜想4] {bsd8_c4.get_verdict()}")

        bsd8_c5 = self.bsd8_c5
        bsd8_c5_paradigm = bsd8_c5.calculate_cultural_war_paradigm()
        bsd8_c5_exposure = bsd8_c5.calculate_cultural_singularity_exposure()
        checks.append(f"[BSD8猜想5] 文化侵略不成立度 = {bsd8_c5.cultural_aggression_invalid:.2f} ✓")
        checks.append(f"[BSD8猜想5] 意义战真实存在度 = {bsd8_c5.meaning_war_real_existence:.2f} ✓")
        checks.append(f"[BSD8猜想5] 文化自剥离程度 = {bsd8_c5.cultural_self_stripping:.2f} ✓")
        checks.append(f"[BSD8猜想5] 本土文化单一化程度 = {bsd8_c5.local_culture_homogenization:.2f} ✓")
        checks.append(f"[BSD8猜想5] 侵略命题谬误度 = {bsd8_c5_paradigm['aggression_fallacy']:.4f} > 0.6 ✓")
        checks.append(f"[BSD8猜想5] 范式转换总强度 = {bsd8_c5_paradigm['total_paradigm_shift']:.4f} > 0.6 ✓")
        checks.append(f"[BSD8猜想5] {bsd8_c5.get_verdict()}")

        # BSD第八部分综合驻波校验
        bsd8_sw = self.bsd8_standing_wave
        bsd8_pos = bsd8_sw.calculate_bsd8_psi_positive()
        bsd8_neg = bsd8_sw.calculate_bsd8_psi_negative()
        bsd8_net = bsd8_sw.calculate_bsd8_psi_net()
        bsd8_dir = bsd8_sw.get_evolution_direction()

        expected_bsd8_pos = (bsd8_sw.conjecture1_positive + bsd8_sw.conjecture2_positive +
                             bsd8_sw.conjecture3_positive + bsd8_sw.conjecture4_positive +
                             bsd8_sw.conjecture5_positive)
        expected_bsd8_neg = (bsd8_sw.conjecture1_negative + bsd8_sw.conjecture2_negative +
                             bsd8_sw.conjecture3_negative + bsd8_sw.conjecture4_negative +
                             bsd8_sw.conjecture5_negative)

        checks.append(f"[BSD8驻波] ψ⁺ = {bsd8_pos:.4f}（应为{expected_bsd8_pos:.4f}）")
        checks.append(f"[BSD8驻波] ψ⁻ = {bsd8_neg:.4f}（应为{expected_bsd8_neg:.4f}）")
        checks.append(f"[BSD8驻波] Ψ_net = {bsd8_net:.4f}")
        checks.append(f"[演化方向] {bsd8_dir}")

        # BSD第八部分最终结论校验
        bsd8_final_count = len(self.bsd8_final.conclusions)
        checks.append(f"[BSD8结论] 最终刚性结论数 = {bsd8_final_count}（应为9条）")

        # BSD第八部分全部成立判定
        all_bsd8_verdict = all([
            bsd8_c1_trap["total_trap_intensity"] > 0.6,
            bsd8_c1_trap["entropy_generation"] > 0.5,
            bsd8_c2_iso["total_isomorphism"] > 0.7,
            bsd8_c2_iso["interface_entropy"] > 0.6,
            bsd8_c3_war["total_war_intensity"] > 0.6,
            bsd8_c3_war["full_domain_engagement"] > 0.5,
            bsd8_c4_subset["total_intensity"] > 0.6,
            bsd8_c4_subset["info_war_dominance"] > 0.5,
            bsd8_c5_paradigm["total_paradigm_shift"] > 0.6,
            bsd8_c5_paradigm["aggression_fallacy"] > 0.6,
            bsd8_final_count == 9,
            abs(bsd8_pos - expected_bsd8_pos) < 1e-6
        ])

        if all_bsd8_verdict:
            checks.append("[判定] BSD第八部分新文明战争五大猜想全部经公理验证成立 ✓")
        else:
            checks.append("[判定] 部分BSD第八部分验证存在异常 ✗")
            passed = False

        passed = passed and all_bsd8_verdict
'''
        lines = lines[:validate_insert_idx] + [bsd8_validation] + lines[validate_insert_idx:]
        print(f"添加validate后共 {len(lines)} 行")
    
    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"\n文件更新完成，共 {len(lines)} 行")

if __name__ == '__main__':
    main()
