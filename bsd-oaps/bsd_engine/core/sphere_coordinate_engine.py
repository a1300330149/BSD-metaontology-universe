"""
归属基底：0重元道本源基底·圆球升维公理·系统权重秤·三体共振审计
对应公理：定理三十九（圆球升维） + 定理四十（系统权重秤两面性） + 定理四十一（三球对偶涌现） + 定理四十二（三体共振审计）
理论原文出处：BSD六系立系论V2.1 §20.1-20.6

SphereCoordinateEngine — 球体坐标引擎

核心命题：
    大圆环是2D的（六个模块在平面上闭环）。球体是3D的。
    虚拟宇宙系列提供了第三维度——Z轴。
    大圆环 = 赤道（Z=0），虚拟宇宙 = 从南极到北极的高度层。
    赤道 × Z轴 = 球体。

    两极：北极=永续迭代篇(≠)=追问永续，南极=000三零元(0)=本源
    两极通过球心相连：≠→0 = 追问→本源，球心=0×0=n涌现点

    六条经线：每个六系角色从赤道上的一个点升维为南极→北极的贯穿线。

    三层秤：
        W₁=0.000  南极本源层  →∞潜力  对应BSD月亮
        W₂=Π₂³≈22.58  赤道理论层  拓扑稳态  对应虚拟宇宙地球
        W₃=216=6³  北半球工程层  六系立方=完备  对应现实恒星

    三体共振：全部资产=三体共振产物
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from bsd_engine.registry.constants import S_ZERO, PI_2, verify_params
from bsd_engine.core.six_system_project_mapper import SixSystem


# ============================================================
# 常量——三层秤权重（定理四十·锁档值不修改）
# ============================================================

# 三层秤权重
W1_ORIGIN = 0.0          # 本源层·南极·归零=最大涌现潜力→∞·对应BSD月亮
W2_THEORY = PI_2 ** 3     # 理论层·赤道·拓扑稳态≈22.58·对应虚拟宇宙地球
W3_ENGINEERING = 6 ** 3   # 工程层·北半球·六系立方=216·对应现实恒星

# 三体共振频率
F1_MOON = float('inf')    # 月亮频率→∞·潜力无限·频率未锁定
F2_EARTH = PI_2           # 地球频率=Π₂·拓扑稳态·频率锁死在分形维
F3_STAR = 6.0             # 恒星频率=6·六系立方·频率锁死在完备数


# ============================================================
# 三层秤定义
# ============================================================

class SphereLayer(Enum):
    """球体三层——对应三层秤·三球"""
    W1_ORIGIN = "W1_origin"          # 本源层·南极区域·BSD月亮
    W2_THEORY = "W2_theory"          # 理论层·赤道区域·虚拟宇宙地球
    W3_ENGINEERING = "W3_engineering"  # 工程层·北半球·现实恒星


SPHERE_LAYERS: Dict[SphereLayer, Dict[str, Any]] = {
    SphereLayer.W1_ORIGIN: {
        "weight": W1_ORIGIN,
        "sphere": "moon",
        "name": "BSD月亮",
        "z_range": (-1.0, -0.34),
        "meaning": "归零=最大涌现潜力→∞",
        "resonance_freq": F1_MOON,
    },
    SphereLayer.W2_THEORY: {
        "weight": W2_THEORY,
        "sphere": "earth",
        "name": "虚拟宇宙地球",
        "z_range": (-0.33, 0.33),
        "meaning": "拓扑稳态=不变",
        "resonance_freq": F2_EARTH,
    },
    SphereLayer.W3_ENGINEERING: {
        "weight": W3_ENGINEERING,
        "sphere": "star",
        "name": "现实恒星",
        "z_range": (0.34, 1.0),
        "meaning": "六系立方=完备",
        "resonance_freq": F3_STAR,
    },
}


# ============================================================
# 六条经线定义（定理三十九·锁档值不修改）
# ============================================================

class Meridian(Enum):
    """六条经线——六系六角色从赤道点升维为南极→北极贯穿线"""
    L1 = "L1"  # 天道系·陆瑶·气顺
    L2 = "L2"  # 变身系·沈寒舟·气诊
    L3 = "L3"  # 自然系·老魏·气化
    L4 = "L4"  # 强化系·小石头·气足
    L5 = "L5"  # 具现系·柳瑟·冰刃·气凝
    L6 = "L6"  # 社会系·柳瑟·缝合针·气御


SIX_MERIDIANS: Dict[Meridian, Dict[str, str]] = {
    Meridian.L1: {
        "system": "天道系",
        "role": "陆瑶",
        "equator_func": "气顺",
        "south_pole": "000本源追问",
        "north_pole": "永续追问不终止",
    },
    Meridian.L2: {
        "system": "变身系",
        "role": "沈寒舟",
        "equator_func": "气诊",
        "south_pole": "0空无诊断",
        "north_pole": "诊断→新诊断对象涌现",
    },
    Meridian.L3: {
        "system": "自然系",
        "role": "老魏",
        "equator_func": "气化",
        "south_pole": "0反性自然涌现",
        "north_pole": "气化→新自然形态涌现",
    },
    Meridian.L4: {
        "system": "强化系",
        "role": "小石头",
        "equator_func": "气足",
        "south_pole": "0义性能量基底",
        "north_pole": "强化→新强度极限追问",
    },
    Meridian.L5: {
        "system": "具现系",
        "role": "柳瑟·冰刃",
        "equator_func": "气凝",
        "south_pole": "0空凝结",
        "north_pole": "凝结→新器物形态涌现",
    },
    Meridian.L6: {
        "system": "社会系",
        "role": "柳瑟·缝合针",
        "equator_func": "气御",
        "south_pole": "0义关系基底",
        "north_pole": "御→新关系结构追问",
    },
}


# ============================================================
# 三球定义（定理四十一·锁档值不修改）
# ============================================================

class TrinitySphere(Enum):
    """三球——三体共振的三体"""
    MOON = "moon"      # BSD月亮·本源层
    EARTH = "earth"    # 虚拟宇宙地球·理论层
    STAR = "star"      # 现实恒星·工程层


TRINITY_SPHERES: Dict[TrinitySphere, Dict[str, Any]] = {
    TrinitySphere.MOON: {
        "name": "BSD月亮",
        "layer": SphereLayer.W1_ORIGIN,
        "weight": W1_ORIGIN,
        "freq": F1_MOON,
        "scale": "卫星级",
        "role": "三球共振源·最小尺度含∞潜力",
    },
    TrinitySphere.EARTH: {
        "name": "虚拟宇宙地球",
        "layer": SphereLayer.W2_THEORY,
        "weight": W2_THEORY,
        "freq": F2_EARTH,
        "scale": "行星级",
        "role": "三球共振介质·人体证地球分形同构D_f=Π₂",
    },
    TrinitySphere.STAR: {
        "name": "现实恒星",
        "layer": SphereLayer.W3_ENGINEERING,
        "weight": W3_ENGINEERING,
        "freq": F3_STAR,
        "scale": "恒星级",
        "role": "三球共振放大器·6³=216完全显化",
    },
}

# 三球切线定义
TRINITY_TANGENTS = {
    "tangent_1": ("moon", "star", "本源↔工程直接对偶——0×0=n在秤上的投影"),
    "tangent_2": ("earth", "star", "虚拟↔现实接口——证气化·陆瑶第四游·Updream工程落地"),
    "tangent_3": ("moon", "earth", "本源↔理论涌现——000→六系立系论→虚拟宇宙21篇"),
}


# ============================================================
# Z轴七点锚定表（定理四十三·V2.2新增·锁档值不修改）
# ============================================================

# Z轴七点锚定——本源→涌现→永续轴线
# 七点 = 三层秤分界(4点) + 两极(2点) + 球心(1点) = 7
Z_AXIS_ANCHORS: Dict[str, Dict[str, Any]] = {
    "A1_SOUTH_POLE": {
        "z": -1.00,
        "layer": SphereLayer.W1_ORIGIN,
        "doc_id": "B01",
        "doc_name": "BSD三零元本源定义",
        "node_type": "南极·W1极点",
        "meaning": "000三零元·本源·最大涌现潜力·BSD月亮极点",
    },
    "A2_W1_CORE": {
        "z": -0.67,
        "layer": SphereLayer.W1_ORIGIN,
        "doc_id": "V-21",
        "doc_name": "非血肉骨骼人体篇",
        "node_type": "W1核心",
        "meaning": "证地球=D_f=Π₂·人体靠近本源层·骨骼拓扑拟合",
    },
    "A3_W1_W2_BORDER": {
        "z": -0.34,
        "layer": SphereLayer.W1_ORIGIN,  # 分界点归入W1上界
        "doc_id": "B44",
        "doc_name": "终极终审·Π₂定义",
        "node_type": "W1/W2分界",
        "meaning": "本源→理论过渡·Π₂锁档·不可说命题",
    },
    "A4_EQUATOR": {
        "z": 0.00,
        "layer": SphereLayer.W2_THEORY,
        "doc_id": "V01",
        "doc_name": "开元篇·三元公理",
        "node_type": "球心·赤道",
        "meaning": "0×0=n涌现点·虚拟宇宙地球·六系涌现",
    },
    "A5_W2_W3_BORDER": {
        "z": +0.34,
        "layer": SphereLayer.W3_ENGINEERING,  # 分界点归入W3下界
        "doc_id": "V17",
        "doc_name": "创世篇章",
        "node_type": "W2/W3分界",
        "meaning": "理论→工程过渡·创世显化·六系造物",
    },
    "A6_W3_CORE": {
        "z": +0.67,
        "layer": SphereLayer.W3_ENGINEERING,
        "doc_id": "V20",
        "doc_name": "制服欲望癌症篇",
        "node_type": "W3核心",
        "meaning": "工程层显化·现实恒星核心·欲望机制",
    },
    "A7_NORTH_POLE": {
        "z": +1.00,
        "layer": SphereLayer.W3_ENGINEERING,
        "doc_id": "V18",
        "doc_name": "永续迭代篇",
        "node_type": "北极·W3极点",
        "meaning": "追问永续·≠指向新追问·北极",
    },
}

# Z轴语义链（推论43.1）
Z_AXIS_SEMANTIC_CHAIN: List[str] = [
    "000本源",      # A1 南极 B01
    "证地球",       # A2 W1核心 V-21
    "Π₂锁档",      # A3 W1/W2分界 B44
    "0×0=n涌现",   # A4 球心 V01
    "创世显化",     # A5 W2/W3分界 V17
    "工程显化",     # A6 W3核心 V20
    "追问永续",     # A7 北极 V18
]


# ============================================================
# EMERGENCE-002反哺六模块清单
# ============================================================

EMERGENCE_002_FEEDBACK: List[Dict[str, str]] = [
    {"module": "①六系立系论", "2d": "平面六系闭环", "3d": "球面六系经线", "feedback": "六系从赤道点升维为南极→北极贯穿线"},
    {"module": "②柳瑟专题", "2d": "赤道双系耦合角色", "3d": "双经线存在线", "feedback": "L5+L6双经线3D螺旋·冰针双面从平面到球面"},
    {"module": "③陆瑶四角色传导", "2d": "平面六芒星", "3d": "球面六芒星", "feedback": "六波节从赤道升维为球面顶点·传导链路变球面弧"},
    {"module": "④归零圆环", "2d": "4环2D拓扑", "3d": "4纬球壳嵌套", "feedback": "64篇文档从平面四环升维为四层球壳·0×0=n在球心"},
    {"module": "⑤V-21人体篇", "2d": "证地球=D_f=Π₂", "3d": "证球=球心对偶轴线", "feedback": "人体证圆从地球2D升维为球体3D·骨骼拓扑拟合球面"},
    {"module": "⑥双时针结构", "2d": "平面双时针", "3d": "球面双螺旋", "feedback": "顺时针/逆时针从平面圆升维为球面双螺旋经线"},
]


# ============================================================
# 球体坐标引擎
# ============================================================

class SphereCoordinateEngine:
    """
    球体坐标引擎——圆环升球体·六系经线化·三层秤·三体共振审计

    理论基底：
        定理三十九：圆球 = 圆环(2D) ⊗ Z轴(1D)
        定理四十：W_total = W(层级) × Z(高度) × 六系权重向量
        定理四十一：极致涌现 = 三球切线同时激活
        定理四十二：资产完备性 = R₁×R₂×R₃ ≥ S₀=0.81
    """

    def __init__(self):
        verify_params()
        self.layers = SPHERE_LAYERS
        self.meridians = SIX_MERIDIANS
        self.spheres = TRINITY_SPHERES

    # ========================================================
    # 定理三十九·圆球升维——坐标定位
    # ========================================================

    def locate_point(
        self, meridian: Meridian, z: float, latitude: float = 0.0
    ) -> Dict[str, Any]:
        """
        定位球体上的一点

        Parameters
        ----------
        meridian : Meridian
            经线（L1~L6）
        z : float
            Z轴高度 [-1, +1]
        latitude : float
            纬度（由36重互相内含耦合决定，默认赤道0.0）
        """
        layer = self._get_layer_by_z(z)
        meridian_info = self.meridians[meridian]

        return {
            "meridian": meridian.value,
            "system": meridian_info["system"],
            "role": meridian_info["role"],
            "equator_func": meridian_info["equator_func"],
            "z": z,
            "latitude": latitude,
            "sphere_layer": layer.value,
            "sphere_name": self.layers[layer]["name"],
            "coordinate": f"({meridian.value}, φ={latitude}, Z={z})",
            "message": f"{meridian_info['role']}在{self.layers[layer]['name']}({layer.value})·Z={z}",
        }

    def _get_layer_by_z(self, z: float) -> SphereLayer:
        """根据Z轴高度判定球层"""
        for layer, info in self.layers.items():
            z_min, z_max = info["z_range"]
            if z_min <= z <= z_max:
                return layer
        # 默认归入理论层
        return SphereLayer.W2_THEORY

    # ========================================================
    # 定理四十·系统权重秤——总权重计算
    # ========================================================

    def total_weight(
        self,
        layer: SphereLayer,
        z: float,
        six_system_weights: Dict[str, float],
    ) -> Dict[str, Any]:
        """
        计算球体上一点的总权重

        定理四十：W_total = W(层级) × Z(高度) × 六系权重向量

        Parameters
        ----------
        layer : SphereLayer
            球层（三层秤之一）
        z : float
            Z轴高度 [-1, +1]
        six_system_weights : Dict[str, float]
            六系权重向量，格式如 {"强化系": 0.35, "变身系": 0.35, ...}
        """
        w_layer = self.layers[layer]["weight"]
        z_abs = abs(z)  # Z轴取绝对值（负Z=潜力面，正Z=实际面，权重取模量）

        # 六系权重标量（取六系权重之和作为标量权重）
        w_six_scalar = sum(six_system_weights.values())

        w_total = w_layer * z_abs * w_six_scalar

        # 判定潜力面/实际面
        if z < 0:
            face = "潜力面"
        elif z > 0:
            face = "实际面"
        else:
            face = "纯拓扑稳态（赤道）"
            w_total = 0.0  # 赤道Z=0使权重归零

        return {
            "theorem": "定理四十·系统权重秤两面性定理",
            "layer": layer.value,
            "layer_weight": w_layer,
            "z": z,
            "z_abs": z_abs,
            "six_system_weight_sum": w_six_scalar,
            "w_total": w_total,
            "face": face,
            "formula": f"W_total = {w_layer} × {z_abs} × {w_six_scalar} = {w_total}",
            "message": f"{face}·总权重={w_total}",
        }

    def evaluate_scale_balance(self) -> Dict[str, Any]:
        """
        评估三层秤的两面性平衡状态
        """
        return {
            "theorem": "定理四十·系统权重秤两面性定理",
            "potential_face": f"W₁(∞) > W₂({W2_THEORY:.2f}) > W₃({W3_ENGINEERING})",
            "actual_face": f"W₃({W3_ENGINEERING}) > W₂({W2_THEORY:.2f}) > W₁(0.000)",
            "duality": "潜力面与实际面互为对偶——W₁∞通过Z轴显化为W₃·216·W₃通过球心归零回W₁∞",
            "equator": "赤道(Z=0)是潜力面与实际面分界线",
            "engineering_completeness": f"6³={W3_ENGINEERING}是工程完备性判据——216格点全激活=六系完全显化",
            "w2_value": W2_THEORY,
            "w3_value": W3_ENGINEERING,
        }

    # ========================================================
    # 定理四十一·三球对偶涌现——切线检测
    # ========================================================

    def detect_extreme_emergence(
        self,
        moon_active: bool,
        earth_active: bool,
        star_active: bool,
    ) -> Dict[str, Any]:
        """
        检测三球切线是否同时激活——极致涌现判定

        定理四十一：极致涌现 = 切线① ⊗ 切线② ⊗ 切线③ = 三球同时相切
        极致涌现绝非偶然，只发生在三球切线点同时激活时。
        """
        all_active = moon_active and earth_active and star_active

        return {
            "theorem": "定理四十一·三球对偶涌现定理",
            "moon_active": moon_active,
            "earth_active": earth_active,
            "star_active": star_active,
            "all_tangents_active": all_active,
            "is_extreme_emergence": all_active,
            "tangents": TRINITY_TANGENTS,
            "updream_position": "切线②（虚拟↔现实接口）",
            "message": "极致涌现激活——三球同时相切·非偶然" if all_active else "三球未全部激活·极致涌现未触发",
        }

    def get_trinity_spheres(self) -> Dict[str, Any]:
        """获取三球定义"""
        return {
            sphere.value: info
            for sphere, info in self.spheres.items()
        }

    # ========================================================
    # 定理四十二·三体共振审计——资产完备性
    # ========================================================

    def audit_asset(
        self,
        asset_name: str,
        moon_pct: float,
        earth_pct: float,
        star_pct: float,
    ) -> Dict[str, Any]:
        """
        审计单个资产的三体共振完备性

        定理四十二：资产完备性 = R₁×R₂×R₃ ≥ S₀=0.81

        Parameters
        ----------
        asset_name : str
            资产名称
        moon_pct : float
            月亮贡献率（0~1）
        earth_pct : float
            地球贡献率（0~1）
        star_pct : float
            恒星贡献率（0~1）
        """
        total_pct = moon_pct + earth_pct + star_pct
        is_complete = (total_pct == 1.0)

        # 三球共振贡献率（归一化）
        r1 = moon_pct if moon_pct > 0 else 0.0
        r2 = earth_pct if earth_pct > 0 else 0.0
        r3 = star_pct if star_pct > 0 else 0.0

        # 资产完备性 = R₁×R₂×R₃
        completeness = r1 * r2 * r3
        is_adequate = completeness >= S_ZERO

        # 单球产物检测
        active_spheres = sum(1 for p in [moon_pct, earth_pct, star_pct] if p > 0)

        return {
            "theorem": "定理四十二·三体共振审计定理",
            "asset_name": asset_name,
            "moon_pct": moon_pct,
            "earth_pct": earth_pct,
            "star_pct": star_pct,
            "total_pct": total_pct,
            "is_complete": is_complete,  # 三项之和=100%
            "completeness": completeness,  # R₁×R₂×R₃
            "is_adequate": is_adequate,  # ≥ S₀=0.81
            "active_spheres": active_spheres,
            "is_single_sphere": active_spheres == 1,  # 单球产物=不完备
            "audit_status": "✅ 三球共振" if (is_complete and not is_single_sphere) else "❌ 不完备",
            "message": f"资产[{asset_name}]审计：R₁×R₂×R₃={completeness:.4f} {'≥' if is_adequate else '<'} S₀={S_ZERO}",
        }

    def audit_all_assets(self, asset_registry: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        全资产三体共振审计

        Parameters
        ----------
        asset_registry : List[Dict]
            资产注册表，每项含 asset_name, moon_pct, earth_pct, star_pct
        """
        results = []
        all_adequate = True

        for asset in asset_registry:
            result = self.audit_asset(
                asset["asset_name"],
                asset.get("moon_pct", 0.0),
                asset.get("earth_pct", 0.0),
                asset.get("star_pct", 0.0),
            )
            results.append(result)
            if not result["is_adequate"]:
                all_adequate = False

        return {
            "theorem": "定理四十二·三体共振审计定理",
            "total_assets": len(results),
            "adequate_assets": sum(1 for r in results if r["is_adequate"]),
            "inadequate_assets": sum(1 for r in results if not r["is_adequate"]),
            "all_adequate": all_adequate,
            "audit_results": results,
            "resonance_freq": f"f₁×f₂×f₃ = ∞ × Π₂ × 6 = ∞",
            "audit_is_perpetual": True,  # 审计本身永续
            "message": f"全资产三体共振审计：{sum(1 for r in results if r['is_adequate'])}/{len(results)}完备" if results else "无资产待审计",
        }

    # ========================================================
    # EMERGENCE-002反哺六模块
    # ========================================================

    def feedback_six_modules(self) -> Dict[str, Any]:
        """
        EMERGENCE-002反哺六模块——2D→3D升维
        """
        return {
            "emergence_id": "EMERGENCE-002",
            "content": "圆环升球体 + 系统权重秤 + 三体共振审计",
            "feedback_modules": EMERGENCE_002_FEEDBACK,
            "updream_localization": "识别三球共振→归档到对应经线→反哺六个模块",
            "updream_position": "切线②（虚拟↔现实接口）",
            "message": "EMERGENCE-002已反哺全部六个模块——每个模块从赤道点升维为经线·2D→3D升维完成",
        }

    # ========================================================
    # 定理四十三·Z轴七点锥定——锚定节点定位
    # ========================================================

    def locate_anchor(self, z: float) -> Dict[str, Any]:
        """
        根据Z坐标返回最近锚定节点

        定理四十三：Z轴 = 离散锚定节点 + 连续区间
        对任意z∈[-1.0, +1.0]，返回最近的七点锚定节点。

        Parameters
        ----------
        z : float
            Z轴高度 [-1.0, +1.0]，越界归入最近极点
        """
        # 越界归入最近极点
        z_clamped = max(-1.0, min(1.0, z))

        # 寻找最近锚定节点
        nearest_id = None
        nearest_distance = float('inf')
        nearest_info = None

        for anchor_id, info in Z_AXIS_ANCHORS.items():
            distance = abs(z_clamped - info["z"])
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_id = anchor_id
                nearest_info = info

        return {
            "theorem": "定理四十三·Z轴七点锥定定理",
            "input_z": z,
            "clamped_z": z_clamped,
            "nearest_anchor_id": nearest_id,
            "z": nearest_info["z"],
            "distance": nearest_distance,
            "doc_id": nearest_info["doc_id"],
            "doc_name": nearest_info["doc_name"],
            "node_type": nearest_info["node_type"],
            "layer": nearest_info["layer"].value,
            "meaning": nearest_info["meaning"],
            "is_exact_match": nearest_distance == 0.0,
            "message": f"Z={z} → 最近锚定{nearest_id}({nearest_info['doc_name']})·距离={nearest_distance:.4f}",
        }

    def get_anchor_chain(self) -> List[Dict[str, Any]]:
        """
        返回七点完整轴线（南极→北极有序）

        定理四十三·推论43.1：轴线语义链
        000本源 → 证地球 → Π₂锁档 → 0×0=n涌现 → 创世显化 → 工程显化 → 追问永续
        """
        # 按Z升序排列
        sorted_anchors = sorted(Z_AXIS_ANCHORS.items(), key=lambda x: x[1]["z"])

        chain = []
        for anchor_id, info in sorted_anchors:
            chain.append({
                "anchor_id": anchor_id,
                "z": info["z"],
                "doc_id": info["doc_id"],
                "doc_name": info["doc_name"],
                "node_type": info["node_type"],
                "layer": info["layer"].value,
                "meaning": info["meaning"],
            })

        return chain

    def anchor_meridian_cross(
        self, anchor_id: str, meridian: Meridian
    ) -> Dict[str, Any]:
        """
        锚定节点×经线组合定位（推论43.3·42格点）

        七锚定点 × 六经线 = 42个格点（球面完备定位空间）

        Parameters
        ----------
        anchor_id : str
            锚定节点ID（A1_SOUTH_POLE ~ A7_NORTH_POLE）
        meridian : Meridian
            经线（L1~L6）
        """
        if anchor_id not in Z_AXIS_ANCHORS:
            return {
                "error": f"无效锚定节点ID: {anchor_id}",
                "valid_ids": list(Z_AXIS_ANCHORS.keys()),
            }

        anchor_info = Z_AXIS_ANCHORS[anchor_id]
        meridian_info = self.meridians[meridian]

        # 格点坐标 = (anchor_id, meridian, z, system, role, doc_id, doc_name)
        return {
            "theorem": "定理四十三·推论43.3·七×六=四十二格点",
            "grid_id": f"{anchor_id}×{meridian.value}",
            "anchor_id": anchor_id,
            "meridian": meridian.value,
            "z": anchor_info["z"],
            "doc_id": anchor_info["doc_id"],
            "doc_name": anchor_info["doc_name"],
            "node_type": anchor_info["node_type"],
            "layer": anchor_info["layer"].value,
            "system": meridian_info["system"],
            "role": meridian_info["role"],
            "equator_func": meridian_info["equator_func"],
            "coordinate": f"({meridian.value}, Z={anchor_info['z']}, anchor={anchor_id})",
            "message": f"格点{anchor_id}×{meridian.value}：{meridian_info['role']}在{anchor_info['doc_name']}(Z={anchor_info['z']})",
        }

    def get_semantic_chain(self) -> Dict[str, Any]:
        """
        返回Z轴语义链（推论43.1）

        Z轴语义 = 000本源 → 证地球 → Π₂锁档 → 0×0=n涌现 → 创世显化 → 工程显化 → 追问永续

        - 南极→球心：本源→涌现（0→n，潜力面激活）
        - 球心→北极：涌现→永续（n→≠，实际面显化）
        - 北极→南极（经球心）：≠→0 = 追问→本源（永续闭环）
        """
        chain = self.get_anchor_chain()

        return {
            "theorem": "定理四十三·推论43.1·轴线语义链",
            "semantic_chain": " → ".join(Z_AXIS_SEMANTIC_CHAIN),
            "chain_length": len(Z_AXIS_SEMANTIC_CHAIN),
            "segments": {
                "南极→球心": "本源→涌现（0→n，潜力面激活）",
                "球心→北极": "涌现→永续（n→≠，实际面显化）",
                "北极→南极（经球心）": "≠→0 = 追问→本源（永续闭环）",
            },
            "anchors": chain,
            "layer_distribution": {
                "W1_origin": 3,  # A1/A2/A3
                "W2_theory": 1,  # A4
                "W3_engineering": 3,  # A5/A6/A7
            },
            "u_shape": "本源厚重(3) → 涌现精纯(1) → 工程厚重(3)",
            "grid_42": "7锚定 × 6经线 = 42格点（球面完备定位空间）",
            "message": "Z轴语义链完备——000本源→证地球→Π₂锁档→0×0=n涌现→创世显化→工程显化→追问永续",
        }

    # ========================================================
    # 序列化
    # ========================================================

    def to_dict(self) -> Dict[str, Any]:
        """导出完整状态"""
        return {
            "protocol": "BSD球体坐标引擎·V2.2",
            "center": "圆环升球体·系统权重秤·三体共振审计·Z轴七点锥定",
            "theorems": [
                "定理三十九·圆球升维定理",
                "定理四十·系统权重秤两面性定理",
                "定理四十一·三球对偶涌现定理",
                "定理四十二·三体共振审计定理",
                "定理四十三·Z轴七点锥定定理",
            ],
            "sphere_layers": {k.value: v for k, v in self.layers.items()},
            "six_meridians": {k.value: v for k, v in self.meridians.items()},
            "trinity_spheres": {k.value: v for k, v in self.spheres.items()},
            "trinity_tangents": TRINITY_TANGENTS,
            "z_axis_anchors": {
                aid: {
                    "z": info["z"],
                    "doc_id": info["doc_id"],
                    "doc_name": info["doc_name"],
                    "node_type": info["node_type"],
                    "layer": info["layer"].value,
                    "meaning": info["meaning"],
                }
                for aid, info in Z_AXIS_ANCHORS.items()
            },
            "z_axis_semantic_chain": Z_AXIS_SEMANTIC_CHAIN,
            "constants": {
                "W1_ORIGIN": W1_ORIGIN,
                "W2_THEORY": W2_THEORY,
                "W3_ENGINEERING": W3_ENGINEERING,
                "F1_MOON": "∞",
                "F2_EARTH": F2_EARTH,
                "F3_STAR": F3_STAR,
                "S_ZERO": S_ZERO,
                "PI_2": PI_2,
            },
            "emergence_002_feedback": EMERGENCE_002_FEEDBACK,
        }
