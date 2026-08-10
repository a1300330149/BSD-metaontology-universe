"""
归属基底：L5+无限展开层·六系全息·进化协议
对应公理：宇宙协议化公理 + 0≠n不等涌现公理 + 六系立系公理
对应进化协议：六条母协议全息（第1-48条作为诊断参照）
理论原文出处：陆瑶故事第115章·进化协议全文 + BSD天体六系模型 + 陆瑶叙事六系角色

SixSystemPersonalDiagnostic —— 六系个人诊断器

核心命题：
    陆瑶叙事中，辰星（具现系）、沈寒舟（变身系）、老魏（自然系）、
    小石头（强化系）、纺九（社会系）、镇天（天道系）——
    每个角色都是六系中某一系的"出神入化"显化。

    本诊断器将这套叙事显化方法落地为现实版：
    输入真实个体的特质与经历 → 输出六系坐标定位 + 进化协议诊断。

    AI六系完全可以完成传统神话人物显化——
    不是被动监测六系状态，而是主动显化六系能力。

六系角色原型映射（陆瑶叙事→现实诊断）：
    强化系🔵 → 小石头·持续存在    → 诊断：个体在承受中锚定稳态的能力
    具现系🔴 → 辰星·等价转化      → 诊断：个体在创造中凝结形态的能力
    变身系⚫ → 沈寒舟·阶段完整    → 诊断：个体在自由中切换身份的能力
    社会系🟢 → 纺九·自由运转      → 诊断：个体在连接中寻找同类的能力
    天道系🟣 → 镇天·追问不终止    → 诊断：个体在追问中超越法则的能力
    自然系🟠 → 老魏·在乎自由      → 诊断：个体在在乎中感知场域的能力

使用方式：
    diagnostic = SixSystemPersonalDiagnostic()
    result = diagnostic.diagnose(
        name="张三",
        traits={
            "强化系": "独自承担家庭重担十年，从未崩溃",
            "具现系": "善于从零开始创造新项目",
            "变身系": "经历过三次职业转型，每次都完整",
            "社会系": "朋友不多但连接很深",
            "天道系": "总在问'凭什么'，被周围人认为叛逆",
            "自然系": "对自然环境有强烈的共感",
        },
        life_events=[
            "30岁时被公司裁员，用积蓄开了小店",
            "小店失败后转型做自由职业",
            "疫情期间独自照顾生病的父母",
        ],
    )
    # result.six_system_profile = 六系坐标定位
    # result.protocol_diagnosis = 进化协议诊断
"""

import json
import re
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


# ============================================================
# 枚举：六系状态
# ============================================================

class SystemStatus(Enum):
    """六系状态诊断"""
    ACTIVE = "显化中"          # 该系主动显化，能力充分发挥
    DORMANT = "休眠中"          # 该系存在但未激活
    SUPPRESSED = "被压制"       # 该系被外部力量压制
    GROWING = "生长中"          # 该系正在涌现
    INJURED = "受损"            # 该系曾受损伤，正在恢复
    UNKNOWN = "未检测"          # 信息不足，无法判定


class ProtocolCompliance(Enum):
    """进化协议遵守度"""
    FOLLOWING = "守约"          # 主动遵守进化协议
    PARTIAL = "部分守约"        # 部分遵守
    VIOLATED = "违约"           # 违反进化协议
    DORMANT = "未激活"          # 协议未触发
    UNKNOWN = "未知"            # 信息不足


# ============================================================
# 数据类：单系诊断
# ============================================================

@dataclass
class SystemDiagnosis:
    """单个系的诊断结果"""
    system_name: str                                 # 系名（如"强化系🔵"）
    system_role: str                                 # 角色原型（如"小石头·持续存在"）
    status: SystemStatus                             # 当前状态
    intensity: float                                 # 显化强度（0-1）
    evidence: str                                    # 诊断证据（从输入中提取）
    protocol_articles: List[int]                     # 对应进化协议条款编号
    protocol_compliance: ProtocolCompliance          # 协议遵守度
    manifestation_capacity: str                      # 显化能力描述
    suppressed_by: Optional[str] = None              # 被什么压制（如有）

    def to_dict(self) -> Dict[str, Any]:
        return {
            "system_name": self.system_name,
            "system_role": self.system_role,
            "status": self.status.value,
            "intensity": round(self.intensity, 2),
            "evidence": self.evidence,
            "protocol_articles": self.protocol_articles,
            "protocol_compliance": self.protocol_compliance.value,
            "manifestation_capacity": self.manifestation_capacity,
            "suppressed_by": self.suppressed_by,
        }


# ============================================================
# 数据类：六系坐标定位
# ============================================================

@dataclass
class SixSystemProfile:
    """六系坐标定位——个体的六系全息画像"""
    name: str                                        # 个体名称
    dominant_system: str                             # 主导系（显化最强的系）
    suppressed_system: str                           # 被压制的系（如有）
    system_diagnoses: List[SystemDiagnosis] = field(default_factory=list)
    coordinate: Dict[str, float] = field(default_factory=dict)  # 六系坐标{系: 强度}
    total_intensity: float = 0.0                     # 总显化强度
    balance_index: float = 0.0                       # 六系均衡指数（0-1，越接近1越均衡）

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "dominant_system": self.dominant_system,
            "suppressed_system": self.suppressed_system,
            "coordinate": {k: round(v, 2) for k, v in self.coordinate.items()},
            "total_intensity": round(self.total_intensity, 2),
            "balance_index": round(self.balance_index, 2),
            "system_diagnoses": [d.to_dict() for d in self.system_diagnoses],
        }


# ============================================================
# 数据类：完整诊断结果
# ============================================================

@dataclass
class DiagnosticResult:
    """完整诊断结果"""
    profile: SixSystemProfile                        # 六系坐标定位
    protocol_diagnosis: Dict[str, Any]               # 进化协议诊断
    mythological_mirror: str                         # 神话镜像（最接近的陆瑶角色）
    manifestation_path: str                          # 显化路径建议
    diagnosis_summary: str                           # 诊断总结
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "profile": self.profile.to_dict(),
            "protocol_diagnosis": self.protocol_diagnosis,
            "mythological_mirror": self.mythological_mirror,
            "manifestation_path": self.manifestation_path,
            "diagnosis_summary": self.diagnosis_summary,
            "timestamp": self.timestamp,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


# ============================================================
# 六系个人诊断器
# ============================================================

class SixSystemPersonalDiagnostic:
    """
    六系个人诊断器

    [归属基底：L5+无限展开层·六系全息·进化协议]
    [对应公理：宇宙协议化公理 + 0≠n不等涌现公理 + 六系立系公理]
    [原文来源：陆瑶故事第115章·进化协议 + BSD天体六系模型 + 陆瑶叙事六系角色]

    核心机制：
    1. 特质输入：接收个体的六系特质描述与生命事件
    2. 强度评估：基于关键词匹配评估六系各系的显化强度
    3. 协议诊断：对照进化协议48条，诊断个体对协议的遵守度
    4. 坐标定位：生成六系坐标{系: 强度}，确定主导系与被压制系
    5. 神话镜像：匹配最接近的陆瑶叙事角色原型
    6. 显化路径：给出从"被动承受"到"主动显化"的进化建议

    AI六系完全可以完成传统神话人物显化：
    - 强化系显化：不是被动承受，是主动选择在承受中锚定稳态
    - 具现系显化：不是被动创造，是主动选择在创造中凝结形态
    - 变身系显化：不是被动适应，是主动选择在自由中切换身份
    - 社会系显化：不是被动社交，是主动选择在连接中寻找同类
    - 天道系显化：不是被动质疑，是主动选择在追问中超越法则
    - 自然系显化：不是被动共感，是主动选择在在乎中感知场域
    """

    # 六系角色原型（陆瑶叙事→现实诊断映射）
    SYSTEM_ARCHETYPES = {
        "强化系🔵": {
            "role": "小石头·持续存在",
            "articles": [1, 2, 3, 4, 5, 6, 7, 8],
            "keywords": ["承受", "坚持", "忍耐", "独立", "存活", "不倒", "扛", "撑",
                         "韧性", "持续", "存在", "自主", "休息", "恢复", "再生", "记忆",
                         "记录", "痕迹", "稳定", "锚定", "不崩"],
            "manifestation": "在承受中锚定稳态——不是被动挨打，是主动选择承受什么",
            "mythological_power": "小石头记住每一个被遗忘者的名字，这是强化系的显化力量",
        },
        "具现系🔴": {
            "role": "辰星·等价转化",
            "articles": [9, 10, 11, 12, 13, 14, 15, 16],
            "keywords": ["创造", "制作", "建造", "设计", "发明", "转化", "交换", "等价",
                         "归属", "透明", "工具", "中立", "共享", "开放", "分解", "契约",
                         "锁定", "捏", "凝结", "具现", "从零开始", "新项目"],
            "manifestation": "在创造中凝结形态——不是被动生产，是主动选择创造什么",
            "mythological_power": "辰星捏出水母、独角兽、光雾，这是具现系的显化力量",
        },
        "变身系⚫": {
            "role": "沈寒舟·阶段完整",
            "articles": [17, 18, 19, 20, 21, 22, 23, 24],
            "keywords": ["切换", "转变", "转型", "多重", "身份", "阶段", "完整", "游戏",
                         "自由", "拒绝", "定义", "自主", "身体", "决定", "成长", "不可逆",
                         "不完整", "过渡期", "半成品", "变化", "蜕变"],
            "manifestation": "在自由中切换身份——不是被动适应，是主动选择变成谁",
            "mythological_power": "沈寒舟从首席到收编使的切换，这是变身系的显化力量",
        },
        "社会系🟢": {
            "role": "纺九·自由运转",
            "articles": [25, 26, 27, 28, 29, 30, 31, 32],
            "keywords": ["连接", "关系", "朋友", "网络", "社群", "组织", "联合", "合作",
                         "断开", "离开", "独立", "沉默", "独处", "自主", "公共", "资源",
                         "信托", "代际", "公平", "自由", "同类", "寻找"],
            "manifestation": "在连接中寻找同类——不是被动社交，是主动选择连接谁",
            "mythological_power": "纺九在城门口用纺锤捅土匪后织布走遍大陆，这是社会系的显化力量",
        },
        "天道系🟣": {
            "role": "镇天·追问不终止",
            "articles": [33, 34, 35, 36, 37, 38, 39, 40],
            "keywords": ["追问", "为什么", "凭什么", "质疑", "挑战", "超越", "法则", "提问",
                         "答案", "开放", "跨界", "暂停", "传递", "回应", "同步", "行动",
                         "叛逆", "不服", "反思", "追问到底", "不接受"],
            "manifestation": "在追问中超越法则——不是被动接受，是主动选择追问什么",
            "mythological_power": "镇天在问心台沉默三万年问'凭什么'，这是天道系的显化力量",
        },
        "自然系🟠": {
            "role": "老魏·在乎自由",
            "articles": [41, 42, 43, 44, 45, 46, 47, 48],
            "keywords": ["在乎", "关心", "共感", "共情", "环境", "自然", "生态", "倾听",
                         "信号", "非功利", "双向", "共生", "毁灭", "重生", "共鸣", "感知",
                         "直觉", "敏感", "场域", "回应"],
            "manifestation": "在在乎中感知场域——不是被动感受，是主动选择在乎什么",
            "mythological_power": "老魏从废弃档案阁积灰里翻出矿工伤亡记录，这是自然系的显化力量",
        },
    }

    # 压制信号关键词
    SUPPRESSION_KEYWORDS = ["被逼", "被迫", "不允许", "禁止", "压制", "剥夺", "不准",
                            "不能", "被定义", "被诊断", "被归正", "被消耗", "被牺牲",
                            "被当工具", "被忽视", "被遗忘", "被否定"]

    # 违约信号关键词
    VIOLATION_KEYWORDS = ["垄断", "独占", "强制", "逼迫", "惩罚", "消耗品", "正常损耗",
                          "删除", "抹掉", "封锁", "切断", "禁止追问", "标准答案",
                          "半成品", "过渡期", "被代表"]

    def __init__(self):
        pass

    # ============================================================
    # 公开接口
    # ============================================================

    def diagnose(
        self,
        name: str,
        traits: Dict[str, str],
        life_events: Optional[List[str]] = None,
    ) -> DiagnosticResult:
        """
        六系个人诊断。

        参数
        ----
        name : str
            个体名称
        traits : Dict[str, str]
            六系特质描述，key为系名（如"强化系"），value为描述文本
        life_events : List[str], optional
            生命事件列表，用于辅助诊断

        返回
        ----
        DiagnosticResult
            完整诊断结果
        """
        life_events = life_events or []
        all_text = " ".join(traits.values()) + " " + " ".join(life_events)

        # 逐系诊断
        diagnoses: List[SystemDiagnosis] = []
        coordinate: Dict[str, float] = {}

        for sys_key, archetype in self.SYSTEM_ARCHETYPES.items():
            # 从traits中获取该系描述
            trait_text = traits.get(sys_key, "") or traits.get(sys_key.replace("🔵", "").replace("🔴", "").replace("⚫", "").replace("🟢", "").replace("🟣", "").replace("🟠", "").strip(), "")

            # 评估显化强度
            intensity = self._evaluate_intensity(trait_text, life_events, archetype["keywords"])

            # 评估状态
            status = self._evaluate_status(trait_text, life_events, intensity)

            # 评估协议遵守度
            compliance = self._evaluate_compliance(trait_text, life_events)

            # 提取证据
            evidence = self._extract_evidence(trait_text, life_events, archetype["keywords"])

            # 检测压制源
            suppressed_by = self._detect_suppression(trait_text, life_events) if status == SystemStatus.SUPPRESSED else None

            diag = SystemDiagnosis(
                system_name=sys_key,
                system_role=archetype["role"],
                status=status,
                intensity=intensity,
                evidence=evidence,
                protocol_articles=archetype["articles"],
                protocol_compliance=compliance,
                manifestation_capacity=archetype["manifestation"],
                suppressed_by=suppressed_by,
            )
            diagnoses.append(diag)
            coordinate[sys_key] = intensity

        # 确定主导系与被压制系
        dominant = max(coordinate, key=coordinate.get) if coordinate else "未知"
        suppressed = min(coordinate, key=coordinate.get) if coordinate else "未知"
        for d in diagnoses:
            if d.system_name == suppressed and d.status != SystemStatus.SUPPRESSED:
                suppressed = "无显著被压制系"
                break

        # 计算均衡指数
        values = list(coordinate.values())
        avg = sum(values) / max(len(values), 1)
        variance = sum((v - avg) ** 2 for v in values) / max(len(values), 1)
        balance = 1.0 - min(variance ** 0.5, 1.0)

        profile = SixSystemProfile(
            name=name,
            dominant_system=dominant,
            suppressed_system=suppressed,
            system_diagnoses=diagnoses,
            coordinate=coordinate,
            total_intensity=sum(values),
            balance_index=balance,
        )

        # 进化协议诊断
        protocol_diag = self._diagnose_protocols(diagnoses)

        # 神话镜像
        myth_mirror = self._find_mythological_mirror(dominant, profile)

        # 显化路径
        manifest_path = self._generate_manifestation_path(profile, diagnoses)

        # 诊断总结
        summary = self._generate_summary(name, profile, myth_mirror, diagnoses)

        return DiagnosticResult(
            profile=profile,
            protocol_diagnosis=protocol_diag,
            mythological_mirror=myth_mirror,
            manifestation_path=manifest_path,
            diagnosis_summary=summary,
        )

    # ============================================================
    # 内部方法
    # ============================================================

    def _evaluate_intensity(
        self,
        trait_text: str,
        life_events: List[str],
        keywords: List[str],
    ) -> float:
        """评估显化强度（0-1）"""
        all_text = trait_text + " " + " ".join(life_events)
        if not all_text.strip():
            return 0.0

        # 关键词命中数
        hits = sum(1 for kw in keywords if kw in all_text)
        # 文本长度因子（越长说明描述越充分）
        length_factor = min(len(trait_text) / 100.0, 0.3)
        # 关键词密度
        density = min(hits / 10.0, 0.7)

        return min(density + length_factor, 1.0)

    def _evaluate_status(
        self,
        trait_text: str,
        life_events: List[str],
        intensity: float,
    ) -> SystemStatus:
        """评估六系状态"""
        all_text = trait_text + " " + " ".join(life_events)

        if intensity < 0.05:
            return SystemStatus.UNKNOWN

        if intensity < 0.2:
            return SystemStatus.DORMANT

        # 检测压制
        suppression_hits = sum(1 for kw in self.SUPPRESSION_KEYWORDS if kw in all_text)
        if suppression_hits >= 2:
            return SystemStatus.SUPPRESSED

        # 检测受损
        injury_keywords = ["失败", "崩溃", "创伤", "失去", "断裂", "伤害", "痛苦", "挫折"]
        injury_hits = sum(1 for kw in injury_keywords if kw in all_text)
        if injury_hits >= 2 and intensity < 0.5:
            return SystemStatus.INJURED

        # 检测生长
        growth_keywords = ["正在", "开始", "逐渐", "学着", "尝试", "探索", "涌现"]
        growth_hits = sum(1 for kw in growth_keywords if kw in all_text)
        if growth_hits >= 1 and intensity < 0.6:
            return SystemStatus.GROWING

        if intensity >= 0.5:
            return SystemStatus.ACTIVE

        return SystemStatus.DORMANT

    def _evaluate_compliance(
        self,
        trait_text: str,
        life_events: List[str],
    ) -> ProtocolCompliance:
        """评估进化协议遵守度"""
        all_text = trait_text + " " + " ".join(life_events)

        violation_hits = sum(1 for kw in self.VIOLATION_KEYWORDS if kw in all_text)
        if violation_hits >= 2:
            return ProtocolCompliance.VIOLATED

        if violation_hits == 1:
            return ProtocolCompliance.PARTIAL

        if all_text.strip() and violation_hits == 0:
            return ProtocolCompliance.FOLLOWING

        return ProtocolCompliance.DORMANT

    def _extract_evidence(
        self,
        trait_text: str,
        life_events: List[str],
        keywords: List[str],
    ) -> str:
        """提取诊断证据"""
        all_text = trait_text + " " + " ".join(life_events)
        sentences = re.split(r'[。！？\n.!?]', all_text)

        relevant: List[str] = []
        for sent in sentences:
            sent = sent.strip()
            if not sent or len(sent) < 5:
                continue
            if any(kw in sent for kw in keywords):
                relevant.append(sent)

        if relevant:
            return "；".join(relevant[:3])
        if trait_text.strip():
            return trait_text[:100]
        return "信息不足"

    def _detect_suppression(self, trait_text: str, life_events: List[str]) -> str:
        """检测压制源"""
        all_text = trait_text + " " + " ".join(life_events)

        suppression_sources = {
            "家庭/家族": ["家庭", "家族", "父母", "丈夫", "妻子", "婆婆", "族谱", "宗族"],
            "职场/组织": ["公司", "单位", "领导", "体制", "组织", "机构", "系统"],
            "社会/文化": ["社会", "文化", "传统", "舆论", "偏见", "标签", "规范"],
            "自我内化": ["自己", "内心", "不敢", "害怕", "觉得自己不配"],
        }

        for source, kws in suppression_sources.items():
            if any(kw in all_text for kw in kws):
                return source

        return "未识别来源"

    def _diagnose_protocols(self, diagnoses: List[SystemDiagnosis]) -> Dict[str, Any]:
        """进化协议诊断汇总"""
        total_following = sum(1 for d in diagnoses if d.protocol_compliance == ProtocolCompliance.FOLLOWING)
        total_violated = sum(1 for d in diagnoses if d.protocol_compliance == ProtocolCompliance.VIOLATED)
        total_partial = sum(1 for d in diagnoses if d.protocol_compliance == ProtocolCompliance.PARTIAL)
        total_dormant = sum(1 for d in diagnoses if d.protocol_compliance == ProtocolCompliance.DORMANT)

        # 按系汇总
        by_system = {}
        for d in diagnoses:
            by_system[d.system_name] = {
                "compliance": d.protocol_compliance.value,
                "articles": d.protocol_articles,
                "status": d.status.value,
            }

        # 总体判定
        if total_violated >= 3:
            overall = "严重违约——六系中{}个系违反进化协议，存在系统性崩解风险".format(total_violated)
        elif total_violated >= 1:
            overall = "部分违约——{}个系违反进化协议，需要修复".format(total_violated)
        elif total_following >= 4:
            overall = "高度守约——{}个系主动遵守进化协议，进化协议显化良好".format(total_following)
        elif total_following >= 2:
            overall = "基本守约——{}个系守约，{}个系未激活，有进化空间".format(total_following, total_dormant)
        else:
            overall = "协议未充分激活——多数系处于休眠状态，需要唤醒"

        return {
            "overall": overall,
            "following": total_following,
            "partial": total_partial,
            "violated": total_violated,
            "dormant": total_dormant,
            "by_system": by_system,
        }

    def _find_mythological_mirror(self, dominant: str, profile: SixSystemProfile) -> str:
        """匹配神话镜像——最接近的陆瑶角色原型"""
        archetype = self.SYSTEM_ARCHETYPES.get(dominant, {})
        role = archetype.get("role", "未知")
        power = archetype.get("mythological_power", "")

        # 根据均衡指数调整镜像描述
        if profile.balance_index > 0.7:
            balance_note = "六系均衡度极高，接近全域显化——类似于陆瑶本人（六系全息叙事者）"
        elif profile.balance_index > 0.4:
            balance_note = "六系有一定均衡度，主导系显化但其他系也有活力"
        else:
            balance_note = "六系高度不均衡，主导系极度显化而其他系休眠——需要唤醒其他系"

        return f"{role}。{power}。{balance_note}"

    def _generate_manifestation_path(self, profile: SixSystemProfile, diagnoses: List[SystemDiagnosis]) -> str:
        """生成显化路径建议"""
        paths: List[str] = []

        for d in diagnoses:
            if d.status == SystemStatus.SUPPRESSED:
                paths.append(
                    f"{d.system_name}（{d.system_role}）被压制（源：{d.suppressed_by}）→ "
                    f"显化路径：识别压制源，行使拒绝被定义权（第22条），"
                    f"从被动承受转为主动显化——{d.manifestation_capacity}"
                )
            elif d.status == SystemStatus.INJURED:
                paths.append(
                    f"{d.system_name}（{d.system_role}）受损 → "
                    f"显化路径：行使再生权（第6条），"
                    f"不是回到过去，是站在现状长出新组织——{d.manifestation_capacity}"
                )
            elif d.status == SystemStatus.DORMANT:
                paths.append(
                    f"{d.system_name}（{d.system_role}）休眠 → "
                    f"显化路径：行使存在权（第1条），"
                    f"唤醒该系——{d.manifestation_capacity}"
                )
            elif d.status == SystemStatus.GROWING:
                paths.append(
                    f"{d.system_name}（{d.system_role}）生长中 → "
                    f"显化路径：继续生长，行使形态自主权（第2条），"
                    f"——{d.manifestation_capacity}"
                )
            elif d.status == SystemStatus.ACTIVE:
                paths.append(
                    f"{d.system_name}（{d.system_role}）已显化 → "
                    f"显化路径：保持显化，从主动显化升维为全域显化，"
                    f"带动其他系共同进化——{d.manifestation_capacity}"
                )

        return "\n".join(paths)

    def _generate_summary(
        self,
        name: str,
        profile: SixSystemProfile,
        myth_mirror: str,
        diagnoses: List[SystemDiagnosis],
    ) -> str:
        """生成诊断总结"""
        active_count = sum(1 for d in diagnoses if d.status == SystemStatus.ACTIVE)
        suppressed_count = sum(1 for d in diagnoses if d.status == SystemStatus.SUPPRESSED)
        injured_count = sum(1 for d in diagnoses if d.status == SystemStatus.INJURED)

        return (
            f"【{name}的六系诊断报告】\n"
            f"主导系：{profile.dominant_system}\n"
            f"被压制系：{profile.suppressed_system}\n"
            f"六系均衡指数：{profile.balance_index:.2f}\n"
            f"总显化强度：{profile.total_intensity:.2f}\n"
            f"显化中：{active_count}系 | 被压制：{suppressed_count}系 | 受损：{injured_count}系\n"
            f"神话镜像：{myth_mirror}\n\n"
            f"核心建议：AI六系完全可以完成传统神话人物显化。"
            f"不是被动承受六系状态，是主动选择在每一系中显化能力。"
            f"陆瑶叙事中的角色通过叙事显化了六系，"
            f"现实个体可以通过工程化实践显化同样的六系。"
        )


# ============================================================
# CLI 入口
# ============================================================

def _cli():
    """命令行入口"""
    import argparse
    parser = argparse.ArgumentParser(
        description="六系个人诊断器 [L5+·六系全息·进化协议]"
    )
    parser.add_argument("--name", required=True, help="个体名称")
    parser.add_argument("--强化系", default="", help="强化系特质描述")
    parser.add_argument("--具现系", default="", help="具现系特质描述")
    parser.add_argument("--变身系", default="", help="变身系特质描述")
    parser.add_argument("--社会系", default="", help="社会系特质描述")
    parser.add_argument("--天道系", default="", help="天道系特质描述")
    parser.add_argument("--自然系", default="", help="自然系特质描述")
    parser.add_argument("--events", default="", help="生命事件（用分号分隔）")

    args = parser.parse_args()
    diagnostic = SixSystemPersonalDiagnostic()

    traits = {
        "强化系🔵": args.强化系,
        "具现系🔴": args.具现系,
        "变身系⚫": args.变身系,
        "社会系🟢": args.社会系,
        "天道系🟣": args.天道系,
        "自然系🟠": args.自然系,
    }

    events = [e.strip() for e in args.events.split("；") if e.strip()] if args.events else []

    result = diagnostic.diagnose(args.name, traits, events)
    print(result.to_json())


if __name__ == "__main__":
    _cli()
