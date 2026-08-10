"""
BSD传统AI视频生成平台公共素材库
[归属基底：L1_外系_局部实验隔离区·虚拟幻造学科树·传统AI平台素材子集]
[对应公理：定理五十四·素材子集定理·推论54.1-54.4]
[V1.0·2026-08-01·基于Updream创世篇章V1.5·12大平台收集]
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional, Any
from enum import Enum


# ============================================================
# 六系枚举·与BSD全局常量保持一致
# ============================================================
class SixSystem(str, Enum):
    """六系枚举·对应强化系=0.35·自然系=0.30·具现系=0.25·变身系=0.2·社会系=0.10·天道系=0.10（虚拟宇宙核心反转）"""
    QIANGHUA = "qianghua"       # 强化系🔵·纯·个体性·承载性·稳态
    ZIRAN = "ziran"             # 自然系🟠·变化性×个体性·实体·承载性
    JUXIAN = "juxian"           # 具现系🔴·个体×关系·显化态凝固·呈现性
    BIANSHEN = "bianshen"       # 变身系⚫·纯·变化性·反性·动力·相变
    SHEHUI = "shehui"           # 社会系🟢·纯·关系性·互摄·连接·交互
    TIANDao = "tiandao"         # 天道系🟣·关系×变化·法则·规律·统治性


SIX_SYSTEM_COLORS = {
    SixSystem.QIANGHUA: "#3B82F6",    # 🔵蓝
    SixSystem.ZIRAN: "#F97316",       # 🟠橙
    SixSystem.JUXIAN: "#EF4444",      # 🔴红
    SixSystem.BIANSHEN: "#1F2937",    # ⚫黑
    SixSystem.SHEHUI: "#22C55E",      # 🟢绿
    SixSystem.TIANDao: "#A855F7",     # 🟣紫
}

SIX_SYSTEM_NAMES = {
    SixSystem.QIANGHUA: "强化系",
    SixSystem.ZIRAN: "自然系",
    SixSystem.JUXIAN: "具现系",
    SixSystem.BIANSHEN: "变身系",
    SixSystem.SHEHUI: "社会系",
    SixSystem.TIANDao: "天道系",
}


# ============================================================
# 素材能力类型枚举
# ============================================================
class MaterialCapability(str, Enum):
    """素材能力类型·与12大平台生成逻辑一一对应"""
    TEXT_TO_VIDEO = "text_to_video"                 # 文生视频
    IMAGE_TO_VIDEO = "image_to_video"               # 图生视频
    VIDEO_TO_VIDEO = "video_to_video"               # 视频生视频
    STYLE_TRANSFER = "style_transfer"               # 风格迁移
    MOTION_CONTROL = "motion_control"               # 动作控制/Motion Brush
    DIRECTOR_MODE = "director_mode"                 # 导演模式
    LOCAL_REPAINT = "local_repaint"                 # 局部重绘
    LIP_SYNC = "lip_sync"                           # 口型同步/Lip Sync
    SPECIAL_EFFECT = "special_effect"               # 特效生成
    LONG_VIDEO = "long_video"                       # 长视频生成(60s+)
    PHYSICS_SIMULATION = "physics_simulation"       # 物理模拟
    MULTI_SHOT_NARRATIVE = "multi_shot_narrative"   # 多镜头叙事
    CHINESE_OPTIMIZED = "chinese_optimized"         # 中文优化
    ROLE_CONSISTENCY = "role_consistency"           # 角色一致性
    THREE_D_GENERATION = "three_d_generation"       # 3D生成
    OPEN_SOURCE = "open_source"                     # 开源
    PRO_WORKFLOW = "pro_workflow"                   # 专业工作流集成
    PROJECT_MANAGEMENT = "project_management"       # 项目管理
    AI_DUBBING = "ai_dubbing"                       # AI配音
    AI_BGM = "ai_bgm"                               # BGM生成
    PLATFORM_DISTRIBUTION = "platform_distribution" # 平台分发/投稿


# ============================================================
# 12大传统AI视频生成平台定义（素材子集）
# ============================================================
@dataclass
class TraditionalPlatform:
    """传统AI视频生成平台·素材子集定义"""
    platform_id: str                          # 平台唯一ID
    name: str                                 # 平台名称
    vendor: str                               # 厂商
    official_url: str                         # 官方网址
    covered_systems: Set[SixSystem]           # 覆盖的六系
    capabilities: Set[MaterialCapability]     # 素材能力
    system_coverage_score: float              # 六系覆盖系数 0~6/6
    is_main_platform: bool = False            # 是否BSD主平台（Updream专用）
    material_positioning: str = ""            # 素材子集定位描述

    def material_type(self) -> str:
        """素材子集定位·根据覆盖六系判断"""
        if self.is_main_platform:
            return "BSD工程落地主平台（Updream·5/6覆盖）"
        sc = list(self.covered_systems)
        if len(sc) == 1 and SixSystem.BIANSHEN in sc:
            return "基础视频素材（仅变身系·1/6覆盖）"
        if len(sc) == 2 and SixSystem.BIANSHEN in sc and SixSystem.JUXIAN in sc:
            return "风格+角色素材（变身+具现·2/6覆盖）"
        if len(sc) == 2 and SixSystem.BIANSHEN in sc and SixSystem.ZIRAN in sc:
            return "长视频物理素材（变身+自然·2/6覆盖）"
        if len(sc) == 2 and SixSystem.BIANSHEN in sc and SixSystem.SHEHUI in sc:
            return "分发素材（变身+社会·2/6覆盖）"
        if len(sc) == 3 and SixSystem.BIANSHEN in sc and SixSystem.JUXIAN in sc and SixSystem.QIANGHUA in sc:
            return "专业工作流素材（强化+具现+变身·3/6覆盖）"
        return f"复合素材（{len(sc)}/6覆盖）"


# ============================================================
# 12大传统平台公共素材注册表
# ============================================================
TRADITIONAL_PLATFORMS: Dict[str, TraditionalPlatform] = {}


def _register_platform(p: TraditionalPlatform):
    """注册传统平台到公共素材库"""
    TRADITIONAL_PLATFORMS[p.platform_id] = p


def init_public_material_library():
    """初始化公共素材库·注册12大传统AI视频生成平台
    
    [归属基底：Updream创世篇章V1.5·§15.2·十二大主流平台生成逻辑收集]
    [对应公理：定理五十四·素材子集定理]
    """
    if len(TRADITIONAL_PLATFORMS) > 0:
        return  # 已初始化

    # 1. Runway
    _register_platform(TraditionalPlatform(
        platform_id="runway",
        name="Runway",
        vendor="Runway",
        official_url="https://runwayml.com/",
        covered_systems={SixSystem.BIANSHEN, SixSystem.JUXIAN},
        capabilities={
            MaterialCapability.TEXT_TO_VIDEO,
            MaterialCapability.IMAGE_TO_VIDEO,
            MaterialCapability.VIDEO_TO_VIDEO,
            MaterialCapability.STYLE_TRANSFER,
            MaterialCapability.MOTION_CONTROL,
            MaterialCapability.DIRECTOR_MODE,
        },
        system_coverage_score=2.0,
        material_positioning="风格迁移素材·导演模式素材"
    ))

    # 2. Pika
    _register_platform(TraditionalPlatform(
        platform_id="pika",
        name="Pika",
        vendor="Pika Labs",
        official_url="https://pika.art/",
        covered_systems={SixSystem.BIANSHEN, SixSystem.JUXIAN},
        capabilities={
            MaterialCapability.TEXT_TO_VIDEO,
            MaterialCapability.IMAGE_TO_VIDEO,
            MaterialCapability.LOCAL_REPAINT,
            MaterialCapability.LIP_SYNC,
            MaterialCapability.SPECIAL_EFFECT,
        },
        system_coverage_score=2.0,
        material_positioning="局部重绘素材·口型同步素材"
    ))

    # 3. Sora
    _register_platform(TraditionalPlatform(
        platform_id="sora",
        name="Sora",
        vendor="OpenAI",
        official_url="https://openai.com/sora",
        covered_systems={SixSystem.BIANSHEN, SixSystem.ZIRAN},
        capabilities={
            MaterialCapability.TEXT_TO_VIDEO,
            MaterialCapability.LONG_VIDEO,
            MaterialCapability.PHYSICS_SIMULATION,
            MaterialCapability.MULTI_SHOT_NARRATIVE,
        },
        system_coverage_score=2.0,
        material_positioning="长视频素材·物理模拟素材"
    ))

    # 4. Kling（可灵）
    _register_platform(TraditionalPlatform(
        platform_id="kling",
        name="Kling·可灵",
        vendor="快手",
        official_url="https://kling.kuaishou.com/",
        covered_systems={SixSystem.BIANSHEN},
        capabilities={
            MaterialCapability.TEXT_TO_VIDEO,
            MaterialCapability.IMAGE_TO_VIDEO,
            MaterialCapability.CHINESE_OPTIMIZED,
            MaterialCapability.LONG_VIDEO,
        },
        system_coverage_score=1.0,
        material_positioning="中文视频素材·长视频素材"
    ))

    # 5. Vidu
    _register_platform(TraditionalPlatform(
        platform_id="vidu",
        name="Vidu",
        vendor="生数科技",
        official_url="https://www.vidu.studio/",
        covered_systems={SixSystem.BIANSHEN, SixSystem.JUXIAN},
        capabilities={
            MaterialCapability.TEXT_TO_VIDEO,
            MaterialCapability.IMAGE_TO_VIDEO,
            MaterialCapability.ROLE_CONSISTENCY,
        },
        system_coverage_score=2.0,
        material_positioning="角色一致性素材"
    ))

    # 6. Hailuo（海螺）
    _register_platform(TraditionalPlatform(
        platform_id="hailuo",
        name="Hailuo·海螺",
        vendor="MiniMax",
        official_url="https://hailuoai.video/",
        covered_systems={SixSystem.BIANSHEN},
        capabilities={
            MaterialCapability.TEXT_TO_VIDEO,
            MaterialCapability.IMAGE_TO_VIDEO,
        },
        system_coverage_score=1.0,
        material_positioning="基础视频素材"
    ))

    # 7. Luma
    _register_platform(TraditionalPlatform(
        platform_id="luma",
        name="Luma",
        vendor="Luma AI",
        official_url="https://lumalabs.ai/",
        covered_systems={SixSystem.BIANSHEN, SixSystem.JUXIAN},
        capabilities={
            MaterialCapability.TEXT_TO_VIDEO,
            MaterialCapability.IMAGE_TO_VIDEO,
            MaterialCapability.THREE_D_GENERATION,
        },
        system_coverage_score=2.0,
        material_positioning="3D生成素材"
    ))

    # 8. SVD (Stable Video Diffusion)
    _register_platform(TraditionalPlatform(
        platform_id="svd",
        name="SVD·Stable Video Diffusion",
        vendor="Stability AI",
        official_url="https://stability.ai/news/stable-video-diffusion-open-ai-video-model",
        covered_systems={SixSystem.BIANSHEN},
        capabilities={
            MaterialCapability.IMAGE_TO_VIDEO,
            MaterialCapability.OPEN_SOURCE,
        },
        system_coverage_score=1.0,
        material_positioning="开源视频素材"
    ))

    # 9. Firefly
    _register_platform(TraditionalPlatform(
        platform_id="firefly",
        name="Firefly",
        vendor="Adobe",
        official_url="https://firefly.adobe.com/",
        covered_systems={SixSystem.QIANGHUA, SixSystem.JUXIAN, SixSystem.BIANSHEN},
        capabilities={
            MaterialCapability.TEXT_TO_VIDEO,
            MaterialCapability.PRO_WORKFLOW,
            MaterialCapability.PROJECT_MANAGEMENT,
            MaterialCapability.STYLE_TRANSFER,
        },
        system_coverage_score=3.0,
        material_positioning="专业工作流素材·项目管理素材"
    ))

    # 10. 混元
    _register_platform(TraditionalPlatform(
        platform_id="hunyuan",
        name="混元",
        vendor="腾讯",
        official_url="https://hunyuan.tencent.com/",
        covered_systems={SixSystem.BIANSHEN},
        capabilities={
            MaterialCapability.TEXT_TO_VIDEO,
            MaterialCapability.CHINESE_OPTIMIZED,
        },
        system_coverage_score=1.0,
        material_positioning="中文视频素材"
    ))

    # 11. 即梦
    _register_platform(TraditionalPlatform(
        platform_id="jimeng",
        name="即梦",
        vendor="字节跳动",
        official_url="https://jimeng.jianying.com/",
        covered_systems={SixSystem.BIANSHEN, SixSystem.SHEHUI},
        capabilities={
            MaterialCapability.TEXT_TO_VIDEO,
            MaterialCapability.IMAGE_TO_VIDEO,
            MaterialCapability.PLATFORM_DISTRIBUTION,
            MaterialCapability.CHINESE_OPTIMIZED,
        },
        system_coverage_score=2.0,
        material_positioning="抖音分发素材"
    ))

    # 12. Updream（主平台·五系覆盖）
    _register_platform(TraditionalPlatform(
        platform_id="updream",
        name="Updream",
        vendor="B站",
        official_url="https://updream.bilibili.com/",
        covered_systems={SixSystem.QIANGHUA, SixSystem.ZIRAN, SixSystem.JUXIAN,
                        SixSystem.BIANSHEN, SixSystem.SHEHUI},
        capabilities={
            MaterialCapability.TEXT_TO_VIDEO,
            MaterialCapability.IMAGE_TO_VIDEO,
            MaterialCapability.AI_DUBBING,
            MaterialCapability.AI_BGM,
            MaterialCapability.PLATFORM_DISTRIBUTION,
            MaterialCapability.LIP_SYNC,
            MaterialCapability.SPECIAL_EFFECT,
            MaterialCapability.CHINESE_OPTIMIZED,
            MaterialCapability.LONG_VIDEO,
            MaterialCapability.ROLE_CONSISTENCY,
        },
        system_coverage_score=5.0,
        is_main_platform=True,
        material_positioning="BSD工程落地主平台（五系覆盖·最接近BSD标准）"
    ))


# ============================================================
# 公共素材交集·跨平台共同能力
# ============================================================
def get_universal_material_capabilities() -> Set[MaterialCapability]:
    """获取全平台公共能力交集（12大平台共同具备的素材能力）
    
    [对应推论54.1·并集不完备性：公共交集 ⊂ 并集，仍缺失天道系]
    """
    init_public_material_library()
    if not TRADITIONAL_PLATFORMS:
        return set()
    
    platforms = list(TRADITIONAL_PLATFORMS.values())
    common = set(platforms[0].capabilities)
    for p in platforms[1:]:
        common &= p.capabilities
    return common


def get_system_union_materials(system: SixSystem) -> Dict[str, TraditionalPlatform]:
    """获取覆盖某一指定六系的所有平台素材并集
    
    [对应定理五十四：BSD六系 = 传统平台并集 ∪ 天道系]
    """
    init_public_material_library()
    result = {}
    for pid, p in TRADITIONAL_PLATFORMS.items():
        if system in p.covered_systems:
            result[pid] = p
    return result


def get_materials_by_capability(cap: MaterialCapability) -> Dict[str, TraditionalPlatform]:
    """按素材能力类型获取对应平台"""
    init_public_material_library()
    return {pid: p for pid, p in TRADITIONAL_PLATFORMS.items() if cap in p.capabilities}


# ============================================================
# 素材子集匹配器
# ============================================================
@dataclass
class MaterialMatchResult:
    """素材子集匹配结果"""
    best_platform_id: str                           # 最佳匹配平台ID
    best_platform: TraditionalPlatform              # 最佳匹配平台
    system_overlap: Set[SixSystem]                  # 六系重叠
    capability_overlap: Set[MaterialCapability]     # 能力重叠
    alternate_platforms: List[Tuple[str, TraditionalPlatform, float]] = field(default_factory=list)
    # 替代平台列表：(platform_id, platform, compatibility_score 0~1)


class MaterialSubsetMatcher:
    """素材子集匹配器·匹配BSD创世任务到传统平台素材子集
    
    [归属基底：Updream创世篇章V1.5·§15.5.3·素材子集决策树]
    [对应公理：推论54.4·Updream主平台性·推论54.2·素材性]
    """

    def __init__(self):
        init_public_material_library()

    def match_task(
        self,
        required_systems: Set[SixSystem],
        required_capabilities: Set[MaterialCapability],
        prefer_chinese: bool = False,
        prefer_long_video: bool = False,
    ) -> MaterialMatchResult:
        """匹配创世任务到传统平台素材子集
        
        Args:
            required_systems: 任务需要的六系
            required_capabilities: 任务需要的素材能力
            prefer_chinese: 是否优先中文优化平台
            prefer_long_video: 是否优先长视频平台
            
        Returns:
            MaterialMatchResult: 匹配结果
        """
        # 步骤1：根据能力初筛
        candidates = []
        for pid, p in TRADITIONAL_PLATFORMS.items():
            sys_overlap = required_systems & p.covered_systems
            cap_overlap = required_capabilities & p.capabilities
            if not cap_overlap and required_capabilities:
                continue  # 完全不满足能力要求则跳过
            compat = (
                len(sys_overlap) / max(len(required_systems), 1) * 0.5
                + len(cap_overlap) / max(len(required_capabilities), 1) * 0.5
            )
            candidates.append((pid, p, sys_overlap, cap_overlap, compat))

        # 步骤2：偏好排序
        def sort_key(x):
            pid, p, so, co, compat = x
            bonus = 0.0
            if prefer_chinese and MaterialCapability.CHINESE_OPTIMIZED in p.capabilities:
                bonus += 0.1
            if prefer_long_video and MaterialCapability.LONG_VIDEO in p.capabilities:
                bonus += 0.1
            if p.is_main_platform and SixSystem.TIANDao not in required_systems:
                bonus += 0.05  # 主平台轻度偏好（除非需要天道系·由BSD注入）
            return compat + bonus

        candidates.sort(key=sort_key, reverse=True)

        # 步骤3：组装结果
        if not candidates:
            # 无候选·返回主平台
            p = TRADITIONAL_PLATFORMS["updream"]
            return MaterialMatchResult(
                best_platform_id="updream",
                best_platform=p,
                system_overlap=required_systems & p.covered_systems,
                capability_overlap=required_capabilities & p.capabilities,
                alternate_platforms=[],
            )

        best_pid, best_p, best_so, best_co, best_compat = candidates[0]
        alternates = [
            (pid, p, compat) for pid, p, so, co, compat in candidates[1:10]
        ]

        return MaterialMatchResult(
            best_platform_id=best_pid,
            best_platform=best_p,
            system_overlap=best_so,
            capability_overlap=best_co,
            alternate_platforms=alternates,
        )

    # ------------------ 素材子集决策树 ------------------
    def decision_tree(self, task_description: str) -> MaterialMatchResult:
        """素材子集决策树·§15.5.3的工程实现
        
        根据任务描述关键词，自动匹配到对应平台的素材子集。
        """
        task_lower = task_description.lower()

        # 收集需求
        req_caps: Set[MaterialCapability] = set()
        req_sys: Set[SixSystem] = set()
        prefer_cn = False
        prefer_long = False

        # 关键词→能力映射
        KEYWORD_CAP_MAP = {
            ("风格迁移", "director", "导演", "motion brush", "运镜"): MaterialCapability.STYLE_TRANSFER,
            ("导演模式", "导演镜头"): MaterialCapability.DIRECTOR_MODE,
            ("动作控制", "motion"): MaterialCapability.MOTION_CONTROL,
            ("局部重绘", "局部修改", "局部"): MaterialCapability.LOCAL_REPAINT,
            ("口型同步", "lip", "口型", "配音对齐"): MaterialCapability.LIP_SYNC,
            ("特效", "爆炸", "粒子", "光影"): MaterialCapability.SPECIAL_EFFECT,
            ("长视频", "超过30秒", "60s", "长镜头"): MaterialCapability.LONG_VIDEO,
            ("物理模拟", "物理", "碰撞", "流体"): MaterialCapability.PHYSICS_SIMULATION,
            ("多镜头", "分镜", "叙事"): MaterialCapability.MULTI_SHOT_NARRATIVE,
            ("中文", "汉语", "古诗", "国风", "中国风"): MaterialCapability.CHINESE_OPTIMIZED,
            ("角色一致", "同一角色", "多场景角色"): MaterialCapability.ROLE_CONSISTENCY,
            ("3d生成", "三维", "3d建模", "三维生成"): MaterialCapability.THREE_D_GENERATION,
            ("开源", "本地部署", "自定义训练"): MaterialCapability.OPEN_SOURCE,
            ("专业工作流", "premiere", "adobe", "后期"): MaterialCapability.PRO_WORKFLOW,
            ("项目管理", "团队协作", "工程化"): MaterialCapability.PROJECT_MANAGEMENT,
            ("ai配音", "配音", "解说"): MaterialCapability.AI_DUBBING,
            ("bgm", "背景音乐", "配乐"): MaterialCapability.AI_BGM,
            ("分发", "投稿", "抖音", "b站", "发布"): MaterialCapability.PLATFORM_DISTRIBUTION,
            ("文生视频", "文字生成视频"): MaterialCapability.TEXT_TO_VIDEO,
            ("图生视频", "图片生成视频"): MaterialCapability.IMAGE_TO_VIDEO,
            ("视频生视频", "视频修改", "重绘视频"): MaterialCapability.VIDEO_TO_VIDEO,
        }

        # 关键词→六系映射（辅助匹配）
        KEYWORD_SYS_MAP = {
            ("承载", "个体", "稳态", "强化", "主体性"): SixSystem.QIANGHUA,
            ("变化", "演化", "自然", "实体"): SixSystem.ZIRAN,
            ("显化", "呈现", "凝结", "等价转化"): SixSystem.JUXIAN,
            ("相变", "变身", "动力", "画面生成"): SixSystem.BIANSHEN,
            ("关系", "连接", "交互", "社会", "观众"): SixSystem.SHEHUI,
            ("规则", "法则", "进化协议", "天道"): SixSystem.TIANDao,
        }

        for kws, cap in KEYWORD_CAP_MAP.items():
            if any(kw.lower() in task_lower for kw in kws):
                req_caps.add(cap)
        for kws, sys in KEYWORD_SYS_MAP.items():
            if any(kw.lower() in task_lower for kw in kws):
                req_sys.add(sys)

        # 中文偏好
        if any(kw.lower() in task_lower for kw in ("中文", "国风", "古诗", "中国风", "汉语")):
            prefer_cn = True
        if any(kw.lower() in task_lower for kw in ("长视频", "60s", "超过30秒", "长镜头")):
            prefer_long = True

        # 至少需要变身系（画面生成·最低要求）
        if not req_caps:
            req_caps.add(MaterialCapability.TEXT_TO_VIDEO)
            req_sys.add(SixSystem.BIANSHEN)

        return self.match_task(req_sys, req_caps, prefer_cn, prefer_long)


# ============================================================
# 公共素材分类报告·BSD视角下的素材子集总览
# ============================================================
def generate_public_material_report() -> str:
    """生成公共素材库总览报告
    
    [归属基底：Updream创世篇章V1.5·§15.2.2·六系覆盖矩阵]
    """
    init_public_material_library()
    lines = []
    lines.append("=" * 72)
    lines.append("BSD传统AI视频生成平台公共素材库总览报告")
    lines.append("V1.0 · 2026-08-01 · 依据Updream创世篇章V1.5§15")
    lines.append("=" * 72)

    # 1. 六系覆盖矩阵
    lines.append("")
    lines.append("【12大平台·六系覆盖矩阵】")
    lines.append(f"{'平台':<18} {'强化':<3} {'自然':<3} {'具现':<3} {'变身':<3} {'社会':<3} {'天道':<3} 覆盖系数")
    lines.append("-" * 62)
    avg_score = 0
    for pid, p in TRADITIONAL_PLATFORMS.items():
        row = [p.name[:16].ljust(18)]
        for s in [SixSystem.QIANGHUA, SixSystem.ZIRAN, SixSystem.JUXIAN,
                 SixSystem.BIANSHEN, SixSystem.SHEHUI, SixSystem.TIANDao]:
            row.append("✓  " if s in p.covered_systems else "✗  ")
        row.append(f"{p.system_coverage_score:.1f}/6")
        lines.append(" ".join(row))
        avg_score += p.system_coverage_score
    avg_score /= len(TRADITIONAL_PLATFORMS)
    lines.append("-" * 62)
    lines.append(f"传统平台平均覆盖系数：{avg_score:.2f}/6")
    lines.append(f"BSD标准：6/6（天道系由BSD理论注入）")

    # 2. 素材子集定位
    lines.append("")
    lines.append("【各平台素材子集定位】")
    for pid, p in TRADITIONAL_PLATFORMS.items():
        lines.append(f"  {p.name:<18} · {p.material_positioning}")

    # 3. 公共能力交集
    common = get_universal_material_capabilities()
    lines.append("")
    lines.append(f"【12平台公共能力交集】（共{len(common)}项）")
    for cap in sorted(common, key=lambda x: x.value):
        lines.append(f"  · {cap.value}")

    # 4. 决策树提示
    lines.append("")
    lines.append("【素材子集决策树·调用接口】")
    lines.append("  matcher = MaterialSubsetMatcher()")
    lines.append("  result = matcher.decision_tree('任务描述')")
    lines.append("  最佳平台：result.best_platform.name")
    lines.append("  替代平台：result.alternate_platforms")

    # 5. 素材子集定理重申
    lines.append("")
    lines.append("【素材子集定理·重申】")
    lines.append("  · 并集不完备：传统平台并集 ∪ 天道系 = BSD六系（推论54.1）")
    lines.append("  · 素材性：传统平台=素材（生成能力），非创世（规则约束）（推论54.2）")
    lines.append("  · 最佳BSD性：BSD六系完备+天道系注入，传统是BSD子集（推论54.3）")
    lines.append("  · Updream主平台性：5/6覆盖·最接近BSD标准（推论54.4）")

    lines.append("")
    lines.append("=" * 72)
    return "\n".join(lines)


# ============================================================
# 自动初始化
# ============================================================
init_public_material_library()


# ============================================================
# 模块公开API
# ============================================================
__all__ = [
    # 枚举
    "SixSystem",
    "MaterialCapability",
    # 数据类
    "TraditionalPlatform",
    "MaterialMatchResult",
    # 注册表
    "TRADITIONAL_PLATFORMS",
    "init_public_material_library",
    # 素材库函数
    "get_universal_material_capabilities",
    "get_system_union_materials",
    "get_materials_by_capability",
    # 匹配器
    "MaterialSubsetMatcher",
    # 报告
    "generate_public_material_report",
]
