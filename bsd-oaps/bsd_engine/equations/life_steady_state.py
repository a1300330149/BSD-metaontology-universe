"""
归属基底：L0_总本源层·0元本体论大一统
对应公理：公理9·意义涌现公理 / 公理6·双极性创生公理
对应九维维度：意识维·能量场·信息维·物质维·时空维
理论出处：theory_base/L0_总本源层/全域大一统理论/生命五维稳态与中西医统一
固定数理常量：κ=0.35 (KAPPA)、α=0.18 (ALPHA)、γ=0.92 (GAMMA)、健康α∈[0.30,0.40]

BSD生命五维稳态判据求解器
—— 描述五维生命稳态、气全局场、健康α范围与中西医统一范式的核心数理引擎
"""

import numpy as np
from bsd_engine.registry.constants import (
    KAPPA,
    ALPHA,
    GAMMA,
    E1,
    E2,
    E3,
    HEALTH_ALPHA_MIN,
    HEALTH_ALPHA_MAX,
    HEALTH_ALPHA_DIFF_MAX,
    SUB_HEALTH_ALPHA_DIFF,
)


def five_dim_steady_state(qi, blood, body, mind, dao):
    """
    五维生命稳态评估

    基于BSD五维生命模型（气·血·身·心·道）综合评估生命稳态水平。

    Parameters
    ----------
    qi : float or np.ndarray
        气维度值（强化系全局生命稳态场）
    blood : float or np.ndarray
        血维度值（物质基础）
    body : float or np.ndarray
        身维度值（肉身结构）
    mind : float or np.ndarray
        心维度值（精神意识）
    dao : float or np.ndarray
        道维度值（本源连接）

    Returns
    -------
    overall_score : float or np.ndarray
        综合稳态评分（0-100）
    dim_scores : dict
        各维度评分
    steady_level : str or np.ndarray
        稳态等级："holy" / "sage" / "excellent" / "good" / "fair" / "poor" / "critical"
    balance_index : float or np.ndarray
        五维均衡指数
    """
    qi = np.asarray(qi, dtype=float)
    blood = np.asarray(blood, dtype=float)
    body = np.asarray(body, dtype=float)
    mind = np.asarray(mind, dtype=float)
    dao = np.asarray(dao, dtype=float)

    qi_s = np.clip(qi, 0.0, 1.0)
    blood_s = np.clip(blood, 0.0, 1.0)
    body_s = np.clip(body, 0.0, 1.0)
    mind_s = np.clip(mind, 0.0, 1.0)
    dao_s = np.clip(dao, 0.0, 1.0)

    w_qi = 0.25
    w_blood = 0.20
    w_body = 0.20
    w_mind = 0.20
    w_dao = 0.15

    overall = w_qi * qi_s + w_blood * blood_s + w_body * body_s + w_mind * mind_s + w_dao * dao_s
    overall_score = overall * 100.0

    dim_scores = {
        "qi": qi_s * 100.0,
        "blood": blood_s * 100.0,
        "body": body_s * 100.0,
        "mind": mind_s * 100.0,
        "dao": dao_s * 100.0,
    }

    mean_val = overall
    deviations = (
        np.abs(qi_s - mean_val)
        + np.abs(blood_s - mean_val)
        + np.abs(body_s - mean_val)
        + np.abs(mind_s - mean_val)
        + np.abs(dao_s - mean_val)
    )
    balance_index = np.maximum(0.0, 1.0 - deviations / (4.0 + 1e-12))

    def get_level(score):
        if score >= E3 * 100:
            return "holy"
        elif score >= E2 * 100:
            return "sage"
        elif score >= E1 * 100:
            return "excellent"
        elif score >= 60:
            return "good"
        elif score >= 40:
            return "fair"
        elif score >= 20:
            return "poor"
        else:
            return "critical"

    if np.isscalar(overall_score) or overall_score.ndim == 0:
        steady_level = get_level(float(overall_score))
    else:
        steady_level = np.array([get_level(s) for s in overall_score.flatten()]).reshape(overall_score.shape)

    return overall_score, dim_scores, steady_level, balance_index


def qi_global_field(params):
    """
    气 = 强化系全局生命稳态场

    计算气的全局场分布，描述强化系生命能量场的空间分布特征。

    Parameters
    ----------
    params : dict
        参数字典，可包含：
        - center: 场中心坐标
        - radius: 场作用半径
        - strength: 场强度
        - coherence: 相干度
        - kappa: 衰减系数

    Returns
    -------
    field_profile : callable
        场分布函数 f(x, y, z)
    field_strength : float
        总场强度
    penetration_depth : float
        穿透深度
    field_type : str
        场类型："point_source" / "dipole" / "multipole" / "coherent_field"
    """
    center = params.get("center", np.array([0.0, 0.0, 0.0]))
    radius = params.get("radius", 1.0)
    strength = params.get("strength", 1.0)
    coherence = params.get("coherence", E2)
    kappa_val = params.get("kappa", KAPPA)

    def field_profile(x, y, z):
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)
        z = np.asarray(z, dtype=float)

        r = np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2 + (z - center[2]) ** 2)

        envelope = strength * np.exp(-kappa_val * r / (radius + 1e-12))

        modulation = 1.0 + coherence * np.sin(r / (radius + 1e-12) * 2.0 * np.pi)

        field = envelope * modulation

        return np.clip(field, 0.0, strength * (1.0 + coherence))

    field_strength = strength * (1.0 + coherence) * radius**2 / (kappa_val + 1e-12)
    penetration_depth = radius / (kappa_val + 1e-12)

    if coherence >= E2:
        field_type = "coherent_field"
    elif coherence >= E1:
        field_type = "multipole"
    elif coherence >= KAPPA:
        field_type = "dipole"
    else:
        field_type = "point_source"

    return field_profile, field_strength, penetration_depth, field_type


def health_alpha_range(alpha1, alpha2, alpha3):
    """
    健康态α∈[0.30,0.40]判据

    判断三元权重是否处于健康态范围，并计算健康度评分。

    Parameters
    ----------
    alpha1 : float or np.ndarray
        第一权重（如：物质/肉身）
    alpha2 : float or np.ndarray
        第二权重（如：精神/意识）
    alpha3 : float or np.ndarray
        第三权重（如：道心/本源）

    Returns
    -------
    is_healthy : bool or np.ndarray
        是否处于健康态
    health_score : float or np.ndarray
        健康度评分（0-100）
    alpha_norm : tuple
        归一化后的三权重
    deviation_from_ideal : float or np.ndarray
        与理想值(1/3)的偏差
    """
    alpha1 = np.asarray(alpha1, dtype=float)
    alpha2 = np.asarray(alpha2, dtype=float)
    alpha3 = np.asarray(alpha3, dtype=float)

    total = alpha1 + alpha2 + alpha3
    a1 = alpha1 / (total + 1e-12)
    a2 = alpha2 / (total + 1e-12)
    a3 = alpha3 / (total + 1e-12)

    in_range = (
        (a1 >= HEALTH_ALPHA_MIN)
        & (a1 <= HEALTH_ALPHA_MAX)
        & (a2 >= HEALTH_ALPHA_MIN)
        & (a2 <= HEALTH_ALPHA_MAX)
        & (a3 >= HEALTH_ALPHA_MIN)
        & (a3 <= HEALTH_ALPHA_MAX)
    )

    max_diff = np.maximum(
        np.abs(a1 - a2),
        np.maximum(np.abs(a2 - a3), np.abs(a1 - a3)),
    )

    is_healthy = in_range & (max_diff <= HEALTH_ALPHA_DIFF_MAX)

    ideal = 1.0 / 3.0
    deviation = np.abs(a1 - ideal) + np.abs(a2 - ideal) + np.abs(a3 - ideal)
    health_score = np.maximum(0.0, 1.0 - deviation / (2.0 / 3.0)) * 100.0

    deviation_from_ideal = deviation

    alpha_norm = (a1, a2, a3)

    return is_healthy, health_score, alpha_norm, deviation_from_ideal


def disease_level(delta_alpha):
    """
    健康/亚健康/疾病三级阈值

    根据三元权重偏离度判断疾病等级。

    Parameters
    ----------
    delta_alpha : float or np.ndarray
        三元权重偏离度（最大权重差）

    Returns
    -------
    level : str or np.ndarray
        等级："health" / "sub_health" / "disease" / "severe_disease" / "critical"
    level_score : float or np.ndarray
        等级评分（0-100，越高越健康）
    recommendation : str or np.ndarray
        建议措施
    recovery_path : list
        恢复路径建议
    """
    delta_alpha = np.asarray(delta_alpha, dtype=float)

    def get_level_and_score(delta):
        if delta <= HEALTH_ALPHA_DIFF_MAX:
            return "health", 100.0, "维持健康生活方式"
        elif delta <= SUB_HEALTH_ALPHA_DIFF:
            score = 100.0 * (1.0 - (delta - HEALTH_ALPHA_DIFF_MAX) / (SUB_HEALTH_ALPHA_DIFF - HEALTH_ALPHA_DIFF_MAX) * 0.3)
            return "sub_health", score, "调整作息，适度运动，放松心情"
        elif delta <= 0.20:
            score = 70.0 * (1.0 - (delta - SUB_HEALTH_ALPHA_DIFF) / (0.20 - SUB_HEALTH_ALPHA_DIFF) * 0.4)
            return "disease", score, "建议就医检查，系统调理"
        elif delta <= 0.35:
            score = 30.0 * (1.0 - (delta - 0.20) / (0.35 - 0.20) * 0.5)
            return "severe_disease", score, "需积极治疗，全面干预"
        else:
            return "critical", 10.0, "紧急治疗，生命支持"

    if np.isscalar(delta_alpha) or delta_alpha.ndim == 0:
        level, level_score, recommendation = get_level_and_score(float(delta_alpha))
    else:
        results = [get_level_and_score(d) for d in delta_alpha.flatten()]
        level = np.array([r[0] for r in results]).reshape(delta_alpha.shape)
        level_score = np.array([r[1] for r in results]).reshape(delta_alpha.shape)
        recommendation = np.array([r[2] for r in results]).reshape(delta_alpha.shape)

    recovery_path = [
        {"stage": "emergency", "description": "紧急救治，维持生命体征", "target_delta": 0.35},
        {"stage": "stabilization", "description": "稳定病情，控制恶化", "target_delta": 0.20},
        {"stage": "recovery", "description": "系统调理，功能恢复", "target_delta": SUB_HEALTH_ALPHA_DIFF},
        {"stage": "health_promotion", "description": "健康促进，提升品质", "target_delta": HEALTH_ALPHA_DIFF_MAX},
        {"stage": "optimization", "description": "持续优化，臻于至善", "target_delta": 0.0},
    ]

    return level, level_score, recommendation, recovery_path


def qi_purity(entropy, coherence):
    """
    气的纯净度计算

    基于结构熵和全局相干度计算气的纯净度指数。

    Parameters
    ----------
    entropy : float or np.ndarray
        结构熵值
    coherence : float or np.ndarray
        全局相干度值（0-1）

    Returns
    -------
    purity : float or np.ndarray
        气的纯净度（0-1）
    purity_level : str or np.ndarray
        纯净等级："purest" / "pure" / "clear" / "turbid" / "murky"
    qi_grade : str or np.ndarray
        气的品级："先天一气" / "浩然正气" / "平和之气" / "混浊之气" / "邪气"
    purification_rate : float or np.ndarray
        净化速率估计
    """
    entropy = np.asarray(entropy, dtype=float)
    coherence = np.asarray(coherence, dtype=float)

    S_norm = 1.0 - np.exp(-entropy * KAPPA)
    C_norm = np.clip(coherence, 0.0, 1.0)

    purity = C_norm * (1.0 - ALPHA * S_norm) / (1.0 + KAPPA * S_norm * (1.0 - C_norm))
    purity = np.clip(purity, 0.0, 1.0)

    def get_levels(p):
        if p >= E3:
            return "purest", "先天一气"
        elif p >= E2:
            return "pure", "浩然正气"
        elif p >= E1:
            return "clear", "平和之气"
        elif p >= KAPPA:
            return "turbid", "混浊之气"
        else:
            return "murky", "邪气"

    if np.isscalar(purity) or purity.ndim == 0:
        purity_level, qi_grade = get_levels(float(purity))
    else:
        results = [get_levels(p) for p in purity.flatten()]
        purity_level = np.array([r[0] for r in results]).reshape(purity.shape)
        qi_grade = np.array([r[1] for r in results]).reshape(purity.shape)

    purification_rate = GAMMA * purity * (1.0 - KAPPA * (1.0 - purity))

    return purity, purity_level, qi_grade, purification_rate


def bsd_medicine_unified(traditional_western, traditional_chinese):
    """
    中西医统一范式映射

    将西医指标和中医指标映射到BSD统一医学范式中。

    Parameters
    ----------
    traditional_western : dict
        西医指标字典，可包含：
        - blood_test: 血液检测指标
        - imaging: 影像检查结果
        - vital_signs: 生命体征
        - pathology: 病理指标
    traditional_chinese : dict
        中医指标字典，可包含：
        - pulse: 脉象
        - tongue: 舌象
        - symptoms: 症状
        - constitution: 体质类型

    Returns
    -------
    unified_diagnosis : dict
        统一诊断结果
    five_dim_mapping : dict
        五维映射结果
    treatment_strategy : dict
        治疗策略（中西医结合）
    harmony_index : float
        中西医和谐指数
    """
    tw = traditional_western or {}
    tc = traditional_chinese or {}

    vital_signs = tw.get("vital_signs", {})
    blood_test = tw.get("blood_test", {})
    pulse = tc.get("pulse", {})
    tongue = tc.get("tongue", {})
    symptoms = tc.get("symptoms", [])

    heart_rate = vital_signs.get("heart_rate", 75.0)
    bp_systolic = vital_signs.get("bp_systolic", 120.0)
    bp_diastolic = vital_signs.get("bp_diastolic", 80.0)
    temperature = vital_signs.get("temperature", 36.5)

    heart_rate_score = 1.0 - np.abs(heart_rate - 75.0) / 50.0
    bp_score = 1.0 - (np.abs(bp_systolic - 120.0) / 60.0 + np.abs(bp_diastolic - 80.0) / 40.0) / 2.0
    temp_score = 1.0 - np.abs(temperature - 36.5) / 3.0

    western_body = np.clip(np.mean([heart_rate_score, bp_score, temp_score]), 0.0, 1.0)

    pulse_rate = pulse.get("rate", "medium")
    pulse_strength = pulse.get("strength", "medium")
    tongue_color = tongue.get("color", "pale_red")
    tongue_coat = tongue.get("coat", "thin_white")

    pulse_score = 0.5 if pulse_rate == "medium" else 0.3 if pulse_rate in ["fast", "slow"] else 0.1
    strength_score = 0.5 if pulse_strength == "medium" else 0.3
    tongue_score = 0.5 if tongue_color == "pale_red" else 0.3
    coat_score = 0.5 if tongue_coat == "thin_white" else 0.3

    chinese_qi = np.clip(np.mean([pulse_score, strength_score, tongue_score, coat_score]), 0.0, 1.0)

    n_symptoms = len(symptoms)
    symptom_score = max(0.0, 1.0 - n_symptoms * 0.1)

    five_dim_mapping = {
        "qi": chinese_qi,
        "blood": western_body * 0.7 + chinese_qi * 0.3,
        "body": western_body,
        "mind": symptom_score * 0.6 + chinese_qi * 0.4,
        "dao": (chinese_qi + symptom_score) / 2.0,
    }

    overall_score = np.mean(list(five_dim_mapping.values())) * 100.0

    unified_diagnosis = {
        "overall_score": overall_score,
        "western_evaluation": {
            "vital_stability": western_body,
            "inflammation_markers": blood_test.get("inflammation", 0.5),
            "organ_function": blood_test.get("organ_function", 0.7),
        },
        "chinese_evaluation": {
            "qi_blood_balance": chinese_qi,
            "yin_yang_harmony": (chinese_qi + symptom_score) / 2.0,
            "zang_fu_state": symptom_score,
        },
        "pattern_identification": _identify_pattern(tc, tw),
    }

    treatment_strategy = {
        "western_medicine": {
            "pharmacology": _western_pharma(tw),
            "surgery": "not_indicated" if overall_score > 60 else "consider",
            "physiotherapy": "recommended" if overall_score < 80 else "maintenance",
        },
        "chinese_medicine": {
            "herbal": _herbal_prescription(tc),
            "acupuncture": "recommended" if chinese_qi < E1 else "health_maintenance",
            "qigong": "highly_recommended",
            "dietary_therapy": _dietary_advice(tc),
        },
        "integrated_approach": {
            "synergy_level": min(western_body, chinese_qi),
            "priority": "chinese_main" if chinese_qi > western_body else "western_main",
            "expected_efficacy": overall_score * GAMMA,
        },
    }

    harmony_index = 1.0 - abs(western_body - chinese_qi) / (western_body + chinese_qi + 1e-12)

    return unified_diagnosis, five_dim_mapping, treatment_strategy, harmony_index


def _identify_pattern(tc, tw):
    symptoms = tc.get("symptoms", [])
    pulse = tc.get("pulse", {})
    patterns = []

    if "fatigue" in symptoms or "weakness" in symptoms:
        patterns.append("qi_deficiency")
    if "dizziness" in symptoms or pulse.get("strength") == "weak":
        patterns.append("blood_deficiency")
    if "insomnia" in symptoms or "anxiety" in symptoms:
        patterns.append("yin_deficiency")
    if "cold_limbs" in symptoms or pulse.get("rate") == "slow":
        patterns.append("yang_deficiency")
    if "pain" in symptoms or pulse.get("quality") == "wiry":
        patterns.append("qi_stagnation")
    if not patterns:
        patterns.append("balanced")

    return patterns


def _western_pharma(tw):
    vital = tw.get("vital_signs", {})
    hr = vital.get("heart_rate", 75)
    bp_sys = vital.get("bp_systolic", 120)

    meds = []
    if hr > 100:
        meds.append("beta_blocker")
    elif hr < 50:
        meds.append("pacemaker_consideration")
    if bp_sys > 140:
        meds.append("antihypertensive")

    return meds if meds else ["none_needed"]


def _herbal_prescription(tc):
    pulse = tc.get("pulse", {})
    symptoms = tc.get("symptoms", [])

    herbs = []
    if "fatigue" in symptoms or pulse.get("strength") == "weak":
        herbs.append("huangqi")
        herbs.append("dangshen")
    if "dizziness" in symptoms:
        herbs.append("danggui")
        herbs.append("shudi")
    if "insomnia" in symptoms:
        herbs.append("suanzaoren")
        herbs.append("baiziren")
    if "cold_limbs" in symptoms:
        herbs.append("fuzi")
        herbs.append("ganjiang")

    return herbs if herbs else ["siwu_tang_base"]


def _dietary_advice(tc):
    symptoms = tc.get("symptoms", [])
    advice = []

    if "fatigue" in symptoms:
        advice.append("red_dates")
        advice.append("longan")
    if "cold_limbs" in symptoms:
        advice.append("ginger")
        advice.append("mutton")
    if "dizziness" in symptoms:
        advice.append("spinach")
        advice.append("black_sesame")
    if "insomnia" in symptoms:
        advice.append("lily_bulb")
        advice.append("poria")

    return advice if advice else ["balanced_diet"]
