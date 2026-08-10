"""
归属基底：L0_总本源层·0元本体论大一统 / L2_分形维象层·化学
对应公理：公理8·意义守恒公理 / 公理10·闭递归公理 / 结构熵公理
对应九维维度：元理维·物质维·能量维·验证维·时间流
理论出处：theory_base/L2_分形维象层/化学/BSD化学统一理论
固定数理常量：κ=0.35 (KAPPA)、γ=0.92 (GAMMA)、α=0.18 (ALPHA)、E1=0.35, E2=0.65, E3=0.90

BSD-OAPS 化学全域难题验证
—— 14个化学难题（7个基础理论+7个工程悬赏）统一验证
"""

from bsd_verify.chemistry.verifier_protein_folding import ProteinFoldingVerifier
from bsd_verify.chemistry.verifier_high_tc_superconduct import HighTcSuperconductVerifier
from bsd_verify.chemistry.verifier_quantum_many_body import QuantumManyBodyVerifier
from bsd_verify.chemistry.verifier_origin_of_life import OriginOfLifeVerifier
from bsd_verify.chemistry.verifier_self_assembly import SelfAssemblyVerifier
from bsd_verify.chemistry.verifier_nonequilibrium_chem import NonequilibriumChemVerifier
from bsd_verify.chemistry.verifier_catalysis_mechanism import CatalysisMechanismVerifier
from bsd_verify.chemistry.verifier_artificial_photo import ArtificialPhotoVerifier
from bsd_verify.chemistry.verifier_room_temp_super import RoomTempSuperVerifier
from bsd_verify.chemistry.verifier_inverse_catalyst import InverseCatalystVerifier
from bsd_verify.chemistry.verifier_carbon_capture import CarbonCaptureVerifier
from bsd_verify.chemistry.verifier_high_energy_battery import HighEnergyBatteryVerifier
from bsd_verify.chemistry.verifier_green_chemistry import GreenChemistryVerifier
from bsd_verify.chemistry.verifier_precision_synthesis import PrecisionSynthesisVerifier


__all__ = [
    "ProteinFoldingVerifier",
    "HighTcSuperconductVerifier",
    "QuantumManyBodyVerifier",
    "OriginOfLifeVerifier",
    "SelfAssemblyVerifier",
    "NonequilibriumChemVerifier",
    "CatalysisMechanismVerifier",
    "ArtificialPhotoVerifier",
    "RoomTempSuperVerifier",
    "InverseCatalystVerifier",
    "CarbonCaptureVerifier",
    "HighEnergyBatteryVerifier",
    "GreenChemistryVerifier",
    "PrecisionSynthesisVerifier",
]


def get_all_chemistry_verifiers():
    """获取所有14个化学难题验证器实例。"""
    return {
        "protein_folding": ProteinFoldingVerifier(),
        "high_tc_superconduct": HighTcSuperconductVerifier(),
        "quantum_many_body": QuantumManyBodyVerifier(),
        "origin_of_life": OriginOfLifeVerifier(),
        "self_assembly": SelfAssemblyVerifier(),
        "nonequilibrium_chem": NonequilibriumChemVerifier(),
        "catalysis_mechanism": CatalysisMechanismVerifier(),
        "artificial_photo": ArtificialPhotoVerifier(),
        "room_temp_super": RoomTempSuperVerifier(),
        "inverse_catalyst": InverseCatalystVerifier(),
        "carbon_capture": CarbonCaptureVerifier(),
        "high_energy_battery": HighEnergyBatteryVerifier(),
        "green_chemistry": GreenChemistryVerifier(),
        "precision_synthesis": PrecisionSynthesisVerifier(),
    }
