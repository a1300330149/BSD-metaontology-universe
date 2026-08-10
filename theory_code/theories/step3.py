# 读取文件
with open('t79_author_conjecture.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 要插入的新类代码（猜想3-5）
new_classes = r'''
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

'''

# 在MilitaryAccountIsomorphism类之后，因果闭环之前插入
# 使用一个唯一的标记
marker = '    def get_verdict(self) -> str:\n        """返回结论"""\n        iso = self.calculate_isomorphism_degree()\n        if iso["total_isomorphism"] > 0.7 and iso["interface_entropy"] > 0.6:\n            return "猜想2成立：军事账号体系与科研体系同构，只有宣传接口无认证通道"\n        return "猜想2待验证"'

if marker in content:
    content = content.replace(marker, marker + '\n\n' + new_classes)
    print('Successfully added conjecture 3, 4, 5')
else:
    print('Marker not found')

# 写入文件
with open('t79_author_conjecture.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('File saved')
