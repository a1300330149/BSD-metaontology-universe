"""
归属基底：L0_总本源层·0元本体论大一统 / L2_分形维象层·制度经济学
对应公理：好坏对偶性公理 / 顶点对立公理 / 驻波动力学公理 / 三元存在分化公理
对应九维维度：元理维·制度维·经济维·验证维·时间流
理论出处：theory_base/L2_分形维象层/制度经济学/T88制度经济学理论
固定数理常量：κ=0.35 (KAPPA)、γ=0.92 (GAMMA)、α=0.18 (ALPHA)、E1=0.35, E2=0.65, E3=0.90

BSD-OAPS 制度经济学验证器集合
—— 基于T88理论框架的制度经济学验证体系
"""

from bsd_verify.economics.verifier_institutional_paradigm import InstitutionalParadigmVerifier
from bsd_verify.economics.verifier_standing_wave import InstitutionalStandingWaveVerifier
from bsd_verify.economics.verifier_industrial_policy import IndustrialPolicyWaveVerifier
from bsd_verify.economics.verifier_tariff_policy import TariffPolicyWaveVerifier
from bsd_verify.economics.verifier_quality_assessment import InstitutionalQualityVerifier


__all__ = [
    "InstitutionalParadigmVerifier",
    "InstitutionalStandingWaveVerifier",
    "IndustrialPolicyWaveVerifier",
    "TariffPolicyWaveVerifier",
    "InstitutionalQualityVerifier",
]


def get_all_economics_verifiers():
    """获取所有制度经济学验证器实例。"""
    return {
        "institutional_paradigm": InstitutionalParadigmVerifier(),
        "standing_wave": InstitutionalStandingWaveVerifier(),
        "industrial_policy": IndustrialPolicyWaveVerifier(),
        "tariff_policy": TariffPolicyWaveVerifier(),
        "quality_assessment": InstitutionalQualityVerifier(),
    }