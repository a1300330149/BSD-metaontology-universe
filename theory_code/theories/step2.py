# 读取文件
with open('t79_author_conjecture.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 要插入的新类代码（前2个猜想）
new_classes = r'''

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

'''

# 在CausalClosedLoop之前插入
marker = '# ============================================================================\n# 因果闭环推导\n# ============================================================================'
if marker in content:
    content = content.replace(marker, new_classes + marker)
    print('Successfully added conjecture 1 and 2')
else:
    print('Marker not found')

# 写入文件
with open('t79_author_conjecture.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('File saved')
