
# ============================================================================
# 大基建案例：六系变量定义
# ============================================================================

@dataclass
class SixSystemsInfraContext:
    """本世纪大基建六系变量定义（2001-2026）"""

    S1: Dict[str, Any] = field(default_factory=lambda: {
        "name": "强化系",
        "description": "顶层现代化发展认知、统筹基建顶层设计、高质量发展、双循环战略主观势能",
        "role": "个体顶层尺度：发展认知"
    })

    S2: Dict[str, Any] = field(default_factory=lambda: {
        "name": "变身系",
        "description": "新型城镇化、供给侧改革、新基建、产业升级、区域协调体制革新、内源排熵通道",
        "role": "逆时针：制度革新"
    })

    S3: Dict[str, Any] = field(default_factory=lambda: {
        "name": "天道系",
        "description": "中央顶层治理架构、全国统一基建规划、财政统筹顶层规则",
        "role": "群体尺度：顶层治理"
    })

    S4: Dict[str, Any] = field(default_factory=lambda: {
        "name": "社会系",
        "description": "地方政府、城乡居民、制造业、服务业、区域城乡中层群体",
        "role": "群体尺度：社会产业"
    })

    S5: Dict[str, Any] = field(default_factory=lambda: {
        "name": "具现系",
        "description": "高铁/高速/特高压/水利/算力等实体基建、产业链产能、财政资产、实体国力核心载体",
        "role": "星体尺度：物质国力"
    })

    S6: Dict[str, Any] = field(default_factory=lambda: {
        "name": "自然系",
        "description": "全球海外经济体、一带一路跨境基建、国际贸易、全球地缘竞争外部星体",
        "role": "星体尺度：外部环境"
    })


# ============================================================================
# 大基建案例：本源初始势能
# ============================================================================

@dataclass
class InfraOriginPotential:
    """大基建本源初始裸势能赋值（2001-2026周期）"""

    S1_0: float = 0.33  # 中等偏强正向本源势能
    T1_to_3_positive: float = 0.33  # 核心正向维稳/发展本源
    delta_S1_to_2_negative: float = -0.14  # 基建投资债务约束
    delta_S1_self: float = -0.11  # 地方过度举债自熵


# ============================================================================
# 大基建案例：五组动态相生/相克顶点
# ============================================================================

@dataclass
class InfraVertexRecognition:
    """大基建五组动态顶点识别（相生+弱相克并存）"""

    vertices: List[VertexOpposition] = field(default_factory=list)

    def __post_init__(self):
        # 顶点1：顶层规划 vs 全国治理（相生）
        self.vertices.append(VertexOpposition(
            vertex_id="V1",
            poles=["S1_顶层规划", "S3_全国治理"],
            vertex_type="相生",
            cause="全局均衡长期发展范式与全国统筹治理秩序势能高度匹配",
            entropy_contribution=0.2046
        ))

        # 顶点2：债务约束 vs 体制革新（弱相克）
        self.vertices.append(VertexOpposition(
            vertex_id="V2",
            poles=["S1_债务约束", "S2_建设革新"],
            vertex_type="相克",
            cause="基建扩张短期债务压力与长期产业革新需求存在小幅势能差",
            entropy_contribution=-0.1932
        ))

        # 顶点3：基建规划 vs 城乡民生（相生为主，含弱相克）
        self.vertices.append(VertexOpposition(
            vertex_id="V3",
            poles=["S3_基建规划", "S4_城乡民生"],
            vertex_type="相生",
            cause="基建落地带动城乡就业、公共服务均等化，同时东西部财政承载力有差距",
            entropy_contribution=0.186
        ))

        # 顶点4：顶层设计 vs 实体产业（最强相生）
        self.vertices.append(VertexOpposition(
            vertex_id="V4",
            poles=["S3_顶层设计", "S5_实体产业"],
            vertex_type="相生",
            cause="顶层规划与实体基建产能高度适配，持续放大国家星体物质稳态势能",
            entropy_contribution=0.2356
        ))

        # 顶点5：国内基建 vs 全球互联（相生为主，含弱相克）
        self.vertices.append(VertexOpposition(
            vertex_id="V5",
            poles=["国内基建网络", "S6_全球互联互通"],
            vertex_type="相生",
            cause="一带一路跨境基建与国内基建网络形成跨星体巨型相生顶点，地缘博弈有轻度相克",
            entropy_contribution=0.26
        ))

    def get_total_positive_entropy(self) -> float:
        """计算所有相生顶点总正熵"""
        return sum(v.entropy_contribution for v in self.vertices if v.is_spawn_vertex())

    def get_total_negative_entropy(self) -> float:
        """计算所有相克顶点总负熵"""
        return sum(v.entropy_contribution for v in self.vertices if v.is_kill_vertex())

    def get_vertex_count(self) -> int:
        return len(self.vertices)


# ============================================================================
# 大基建案例：驻波动力学计算
# ============================================================================

@dataclass
class InfraStandingWave:
    """大基建驻波动力学计算（相生为主，弱克对冲）"""

    LAMBDA_POSITIVE: float = 0.62
    LAMBDA_NEGATIVE: float = 1.38

    # 初始势能
    S1_0: float = 0.33
    DELTA_S1_TO_2: float = -0.14
    PSI_POSITIVE_4: float = 0.30
    PSI_NEGATIVE_4: float = -0.13
    PSI_POSITIVE_5: float = 0.38
    PSI_POSITIVE_6: float = 0.26
    PSI_NEGATIVE_6: float = -0.10
    DELTA_S1_SELF: float = -0.11

    # 计算结果
    T1_to_3: float = field(init=False)
    T1_to_2_negative: float = field(init=False)
    T3_to_4_positive: float = field(init=False)
    T3_to_4_negative: float = field(init=False)
    T3_to_5_positive: float = field(init=False)
    S6_positive: float = field(init=False)
    S6_negative: float = field(init=False)

    # 五组顶点
    vertices: InfraVertexRecognition = field(default_factory=InfraVertexRecognition)

    def __post_init__(self):
        # 链路1：S1→S3（正向衰减）
        self.T1_to_3 = self.S1_0 * (self.LAMBDA_POSITIVE ** 1)

        # 链路2：S1→S2（负向放大）
        self.T1_to_2_negative = self.DELTA_S1_TO_2 * (self.LAMBDA_NEGATIVE ** 1)

        # 链路3：S3→S4（正向+负向双向）
        self.T3_to_4_positive = self.PSI_POSITIVE_4 * self.LAMBDA_POSITIVE
        self.T3_to_4_negative = self.PSI_NEGATIVE_4 * self.LAMBDA_NEGATIVE

        # 链路4：S3→S5（正向衰减）
        self.T3_to_5_positive = self.PSI_POSITIVE_5 * self.LAMBDA_POSITIVE

        # 外部S6：无层级衰减，双向耦合
        self.S6_positive = self.PSI_POSITIVE_6
        self.S6_negative = self.PSI_NEGATIVE_6

    def calculate_psi_positive(self) -> float:
        """正向稳态驻波ψ+（全部相生顶点）"""
        return self.T1_to_3 + self.T3_to_4_positive + self.T3_to_5_positive + self.S6_positive

    def calculate_psi_negative(self) -> float:
        """负向解构驻波ψ-（全部弱相克顶点 + 自耗熵）"""
        # 顶点相克总势能（仅相克项）
        vertex_negative = self.vertices.get_total_negative_entropy()

        # 顶层自耗熵
        self_entropy = self.DELTA_S1_SELF

        # 外部负向 + S3→S4负向
        other_negative = self.S6_negative + self.T3_to_4_negative

        # V2 = T1→2负向 = -0.1932
        return vertex_negative + self_entropy + other_negative

    def calculate_psi_net(self) -> float:
        """净谐振驻波Ψ_net"""
        return self.calculate_psi_positive() + self.calculate_psi_negative()

    def get_evolution_direction(self) -> str:
        """演化方向判定"""
        psi_net = self.calculate_psi_net()
        if psi_net > 0:
            return "dΨ_net/dt > 0：星体持续扩张、稳态强化"
        elif psi_net < 0:
            return "dΨ_net/dt < 0：星体秩序持续失稳、解构加速"
        else:
            return "dΨ_net/dt = 0：临界状态"


# ============================================================================
# 大基建案例：基准对照模型
# ============================================================================

@dataclass
class InfraBaselineComparison:
    """大基建基准对照模型（取消顶层全局统筹，放任地方无序基建）"""

    standing_wave: InfraStandingWave = None

    baseline_psi_positive: float = field(init=False)
    baseline_psi_negative: float = field(init=False)
    baseline_psi_net: float = field(init=False)
    actual_psi_net: float = field(init=False)
    delta_psi: float = field(init=False)

    def __post_init__(self):
        if self.standing_wave is None:
            self.standing_wave = InfraStandingWave()

        sw = self.standing_wave

        # 基准：取消顶层统筹，V1相生顶点消失（T1→3=0），负向增加（债务放大）
        # 正向去掉 T1→3 = 0.2046
        self.baseline_psi_positive = sw.calculate_psi_positive() - sw.T1_to_3

        # 负向增加：地方无序举债，债务风险放大（假设ΔS1→2翻倍至-0.28，对应T1→2加倍）
        # 简化：去掉顶层统筹后，负向增加 = 原T1→2负向的绝对值（即更糟）
        extra_negative = abs(sw.T1_to_2_negative)  # 额外增加的负向
        self.baseline_psi_negative = sw.calculate_psi_negative() - extra_negative

        # 基准净驻波
        self.baseline_psi_net = self.baseline_psi_positive + self.baseline_psi_negative

        # 实际完整净驻波
        self.actual_psi_net = sw.calculate_psi_net()

        # ΔΨ = 实际 - 基准
        self.delta_psi = self.actual_psi_net - self.baseline_psi_net


# ============================================================================
# 大基建案例：因果闭环推导
# ============================================================================

@dataclass
class InfraCausalLoop:
    """大基建全套公理联立因果闭环推导"""

    derivations: Dict[str, str] = field(default_factory=lambda: {
        "1_0_元本体同源": "六系势能同源双向转化；顶层现代化认知持续向S2革新、S5实体基建传导，实体基建积累反向赋能产业升级、对外开放，势能正向循环再生，不存在透支本体存量",

        "2_0_三元相位均衡": "意义相（现代化革新）、秩序相（全国统筹治理）、物质相（全域基建实体）三相同步均衡发展，批量生成强相生顶点，星体长期均衡基础稳固；仅局部区域、财政层面存在轻度相位失衡，可通过顶层政策调节",

        "3_0_双时针正向循环": "逆时针现代化、体制革新链路全程通畅，支撑顺时针大规模基建物质积累；实体国力提升进一步开放革新空间，双时针形成正向自强化循环，稳态谐振持续放大",

        "4_0_层级衰减与对冲": "顶层正向建设红利虽经多层传导存在损耗，但总量规模极大，民生、产业正向收益覆盖层级损耗；地方债务、区域失衡负势能虽经传导放大，但中央转移支付、化债改革持续对冲相克熵；基层诉求反馈存在衰减，但常态化巡视、专项债调节机制弥补反馈滞后缺陷",

        "5_0_顶点相生为主": "不存在先天固定六系生克，本世纪星体演化以多组巨型相生顶点为主：顶层统筹—全国治理、基建规划—城乡民生、顶层设计—实体产业、国内基建—全球互联互通；仅存在四组弱相克顶点（债务与改革、东西财政差距、海外地缘风险、顶层统筹地方压力），且全部具备顶层政策对冲渠道，势能差可控、不会持续无限扩张；相生势能总量远高于全部相克解构势能",

        "6_0_驻波正向增益": "正向稳态驻波数值显著高于负向解构驻波，国家星体谐振长期正向增益，综合国力、国内循环、国际联通持续扩张",

        "7_0_熵变双向调控": "唯一内源排熵通道S2全程开放，供给侧改革、区域协调、新型基建、地方化债持续消解债务、区域失衡产生的全域熵，体系具备持续自主修复、自我优化能力",

        "8_0_尺度分层匹配": "顶层全局尺度现代化规划统筹群体尺度地方政府、星体尺度实体产业与对外开放，跨尺度势能匹配催生核心相生顶点；层级传导带来的局部失衡可通过跨尺度转移支付、专项政策抹平",

        "9_0_时序刚性正向循环": "顶层先行确立现代化、高质量发展革新范式，再落地大规模基建实体建设，不属于短期透支行为；基建完成的实体底座反过来支撑长期产业、科技、制度迭代，形成可持续正向时序循环"
    })


# ============================================================================
# 大基建案例：最终刚性结论
# ============================================================================

@dataclass
class InfraFinalConclusions:
    """大基建完整数理刚性结论（统一对标晚清、文革两套模型）"""

    conclusions: Dict[int, str] = field(default_factory=lambda: {
        1: "短期与长周期全域观测：正向驻波ψ+=0.8862规模远超负向解构驻波ψ-=-0.5826，净驻波Ψ_net=0.3036恒为正值，演化导数dΨ_net/dt>0；本世纪大基建完整构建多组全域强相生顶点，国家星体稳态、综合国力持续扩张",

        2: "与无顶层统筹放任基建的基准模型对比，全局统一规划的大基建范式额外引入规模ΔΨ=0.3978的星体正向扩张势能，有效对冲地方债务、区域发展不平衡、国际地缘竞争全部解构熵",

        3: "横向跨案例对标数值直观区分三类历史周期核心差异：慈禧晚清Ψ_net=-1.6318（深度失稳，加速解体）；文革十年Ψ_net=-1.3884（全域严重解构，全方位损耗）；本世纪中国大基建周期Ψ_net=0.3036（正向扩张，星体持续变强）",

        4: "剥离顶点相生相克公理，则无法解释为何大基建同时存在债务、区域分化等负向问题，却能实现国家整体长期发展变强；整套数理推演逻辑、定量数值、演化趋势完全自洽统一",

        5: "全域星体演化最终判定：本世纪顶层统筹推进的全域大基建，打通双时针正向循环，生成多组跨尺度巨型相生顶点，虽伴随地方财政、区域差距、海外风险等弱相克熵增，但相生发展势能占据绝对主导；从国家星体完整生命周期、全域熵调控、多尺度顶点势能均衡四维定量严格证明：大基建持续强化国内治理秩序、夯实实体国力、拓展全球联通通道，持续推动本国文明星体扩张、稳态增强，是长期正向增益的核心发展路径"
    })


