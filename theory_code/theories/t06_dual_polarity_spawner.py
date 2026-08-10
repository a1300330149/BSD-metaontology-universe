"""
【归属基底：L0_总本源层·双极性创生公理】
【对应公理：双极性创生公理】

T6 —— 双极性创生机制
阴阳/动静/虚实双极性，万物从二元对立中创生
一阴一阳之谓道，阴阳不测之谓神
"""

import math
from typing import Dict, List, Tuple, Optional, Any
from ..core.base_theory_module import BaseTheoryModule


class DualPolaritySpawner(BaseTheoryModule):
    """
    双极性创生机制
    
    核心要义：
    - 双极性三定律：对立律、互根律、转化律
    - 极性转化：阳极生阴，阴极生阳
    - 极性平衡：阴阳调和，动态平衡
    - 极性创生：阴阳合和，万物化生
    """

    module_id = "T6"
    module_name = "双极性创生机制"
    version = "V1.0_终版"
    cosmic_level = 0
    base_belong = "L0_总本源层·双极性创生公理"
    corresponding_axiom = "双极性创生公理"
    is_origin_locked = True
    dependencies = ["T2", "T5"]

    def __init__(self):
        super().__init__()
        self.three_polarity_pairs = {
            "yin_yang": "阴阳",
            "dong_jing": "动静",
            "xu_shi": "虚实"
        }
        self._polarity_balance = 0.5
        self._conversion_rate = 0.0
        self._creation_efficiency = 0.0

    def dual_polarity_three_laws(self) -> Dict[str, Dict[str, Any]]:
        """双极性三定律推演"""
        return {
            "opposition_law": {
                "name": "对立律",
                "description": "阴阳对立，相反相成",
                "principle": "阴阳互为对立面，相互制约、相互斗争"
            },
            "interdependence_law": {
                "name": "互根律",
                "description": "阴阳互根，互为根基",
                "principle": "阴生于阳，阳生于阴，无阴则阳无以生，无阳则阴无以化"
            },
            "transformation_law": {
                "name": "转化律",
                "description": "阴阳转化，物极必反",
                "principle": "阳极生阴，阴极生阳，重阴必阳，重阳必阴"
            }
        }

    def polarity_conversion(self, initial_yang: float, steps: int = 10) -> Dict[str, Any]:
        """极性转化推演"""
        yang = initial_yang
        history = []
        for _ in range(steps):
            history.append({"yang": yang, "yin": 1.0 - yang})
            if yang > 0.9:
                yang = yang - self.constants.alpha
            elif yang < 0.1:
                yang = yang + self.constants.alpha
            else:
                yang = yang + self.constants.kappa * (0.5 - yang) * 0.1
            yang = max(0.0, min(1.0, yang))
        self._conversion_rate = abs(history[-1]["yang"] - history[0]["yang"]) / steps
        return {
            "conversion_history": history,
            "conversion_rate": self._conversion_rate,
            "extreme_conversion": True,
            "cycle_complete": abs(yang - initial_yang) < self.constants.theta_neg
        }

    def polarity_balance(self) -> Dict[str, Any]:
        """极性平衡推演"""
        balance = self._polarity_balance
        yin = 1.0 - balance
        return {
            "yang_level": balance,
            "yin_level": yin,
            "balance_degree": 1.0 - abs(balance - 0.5) * 2,
            "dynamic_equilibrium": True,
            "harmony_state": abs(balance - 0.5) < self.constants.theta_neg
        }

    def polarity_creation(self, yang_energy: float, yin_energy: float) -> Dict[str, Any]:
        """极性创生推演"""
        total = yang_energy + yin_energy
        balance_factor = 1.0 - abs(yang_energy - yin_energy) / total if total > 0 else 0
        self._creation_efficiency = self.constants.gamma * balance_factor
        created = total * self._creation_efficiency
        return {
            "yang_input": yang_energy,
            "yin_input": yin_energy,
            "balance_factor": balance_factor,
            "creation_efficiency": self._creation_efficiency,
            "created_quantity": created,
            "principle": "阴阳合和，万物化生"
        }

    def set_polarity_balance(self, yang_ratio: float) -> bool:
        """设置极性平衡点"""
        if 0.0 <= yang_ratio <= 1.0:
            self._polarity_balance = yang_ratio
            return True
        return False

    def validate(self) -> Tuple[bool, List[str]]:
        """T6 自检验证"""
        ok, errors = super().validate()
        if not ok:
            return ok, errors
        if len(self.three_polarity_pairs) != 3:
            errors.append("双极性对必须恰好3组")
        if "yin_yang" not in self.three_polarity_pairs:
            errors.append("必须包含阴阳极性对")
        if "dong_jing" not in self.three_polarity_pairs:
            errors.append("必须包含动静极性对")
        if "xu_shi" not in self.three_polarity_pairs:
            errors.append("必须包含虚实极性对")
        if "T2" not in self.dependencies:
            errors.append("T6必须依赖T2")
        if "T5" not in self.dependencies:
            errors.append("T6必须依赖T5")
        if self.cosmic_level != 0:
            errors.append("T6必须位于L0本源层")
        if not self.is_origin_locked:
            errors.append("T6本源理论必须锁定")
        if not hasattr(self, 'dual_polarity_three_laws'):
            errors.append("必须实现双极性三定律方法")
        if not hasattr(self, 'polarity_conversion'):
            errors.append("必须实现极性转化方法")
        if not hasattr(self, 'polarity_creation'):
            errors.append("必须实现极性创生方法")
        return (len(errors) == 0, errors)


if __name__ == "__main__":
    t6 = DualPolaritySpawner()
    print(f"模块: {t6.module_id} - {t6.module_name}")
    print(f"版本: {t6.version}")
    print(f"层级: L{t6.cosmic_level}")
    print(f"依赖: {t6.dependencies}")
    print(f"锁定: {t6.is_origin_locked}")
    print(f"哈希: {t6.sha256}")
    print()
    
    print("双极性三定律:")
    laws = t6.dual_polarity_three_laws()
    for key, val in laws.items():
        print(f"  {val['name']}: {val['description']}")
    print()
    
    print("极性平衡:")
    balance = t6.polarity_balance()
    print(f"  阳: {balance['yang_level']:.4f}")
    print(f"  阴: {balance['yin_level']:.4f}")
    print(f"  平衡度: {balance['balance_degree']:.4f}")
    print()
    
    print("极性创生:")
    creation = t6.polarity_creation(0.6, 0.4)
    print(f"  创生效率: {creation['creation_efficiency']:.6f}")
    print(f"  创生量: {creation['created_quantity']:.6f}")
    print()
    
    valid, errs = t6.validate()
    print(f"验证通过: {valid}")
    if not valid:
        for e in errs:
            print(f"  错误: {e}")
