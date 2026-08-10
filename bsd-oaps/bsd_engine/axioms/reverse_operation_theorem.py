"""
归属基底：第0重元道本源基底 + L0总本源层·六系核心公理
对应三界秩序：天道
对应公理：反操作定理 + 真反操作定理 + 本源0编码定理 + 四字终极存在链条（反→真→问→系）
对应九维维度：元理天道 + 关系性维度
理论原文出处：theory_base/L0_总本源层/六系核心公理/
    BSD四字立系公理——反真问系作为六系本源基底·本源0编码·数学符号本体证明_V1.0.md
固定数理常量：γ=0.92、κ=0.35（本模块不引入新参数，仅使用已有锁档常量）

反操作定理模块 V1.0

职责：
  1. 实现反操作定理：反(+)=-、反(-)=+、反(×)=÷、反(÷)=×、反(=)=≠、反(≠)==
  2. 实现真反操作定理：反真即假、反假即真、真问即答、真答即不问、真系即等、真等即非系
  3. 实现本源0编码：0+0=0, 0-0=0, 0×0=0, 0÷0=0, 0=0, 0≠n
  4. 六符号↔六系精确映射与验证
  5. 四字终极存在链条（反→真→问→系）的代码级实现
  6. 三对反符号对的完备性验证

设计原则：
  - 本源优先：所有操作在0层面完成，非n层面数值展开
  - 反操作完备：三对反符号对（+-·×÷·=≠）必须完备
  - 双向映射：六符号↔六系严格一一对应
  - 理论锚定：每个操作标注归属基底+对应公理

理论依据：
  反操作定理：反(-)=+、反(+)=-、反(×)=÷、反(÷)=×、反(=)=≠、反(≠)==
  本源0编码：0+0=0, 0-0=0, 0×0=0, 0÷0=0, 0=0, 0≠n
  六符号=六系：+→强化系、÷→变身系、=→社会系、-→自然系、×→具现系、≠→天道系
  真反操作定理：反真即假、反假即真、真问即答、真答即不问、真系即等、真等即非系
  四字终极存在链条：反→真→问→系
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum


# ============================================================
# 枚举定义
# ============================================================

class MathSymbol(Enum):
    """六个本源数学符号"""
    PLUS = "+"       # 加·强化系
    MINUS = "-"      # 减·自然系
    MULTIPLY = "×"   # 乘·具现系
    DIVIDE = "÷"     # 除·变身系
    EQUAL = "="      # 等·社会系
    NOT_EQUAL = "≠"  # 不等·天道系


class SixSystem(Enum):
    """六系"""
    REINFORCEMENT = "强化系"    # 🔵
    NATURE = "自然系"           # 🟠
    MANIFESTATION = "具现系"    # 🔴
    TRANSFORMATION = "变身系"   # ⚫
    SOCIETY = "社会系"          # 🟢
    HEAVEN = "天道系"           # 🟣


class FourCharacter(Enum):
    """四字终极存在链条"""
    REVERSE = "反"  # 反→数学（反性）
    TRUE = "真"     # 真→物理（真性）
    ASK = "问"      # 问→哲学（问性）
    SYSTEM = "系"   # 系→内外之分


class SystemCategory(Enum):
    """系类别"""
    PURE = "三纯基元系"        # 正符号
    COUPLED = "三耦合功能系"   # 反符号


# ============================================================
# 反符号对定义
# ============================================================

@dataclass
class ReversePair:
    """反符号对"""
    name: str               # 对名（如"加减对"）
    positive: MathSymbol    # 正符号
    negative: MathSymbol    # 反符号
    positive_system: SixSystem   # 正符号→六系
    negative_system: SixSystem   # 反符号→六系
    bsd_meaning: str        # BSD本源含义


# 三对反符号对（完备性保证）
REVERSE_PAIRS: List[ReversePair] = [
    ReversePair(
        name="加减对",
        positive=MathSymbol.PLUS,
        negative=MathSymbol.MINUS,
        positive_system=SixSystem.REINFORCEMENT,
        negative_system=SixSystem.NATURE,
        bsd_meaning="承载↔反承载·真↔反真",
    ),
    ReversePair(
        name="乘除对",
        positive=MathSymbol.DIVIDE,
        negative=MathSymbol.MULTIPLY,
        positive_system=SixSystem.TRANSFORMATION,
        negative_system=SixSystem.MANIFESTATION,
        bsd_meaning="分割↔凝结·反↔反反",
    ),
    ReversePair(
        name="等不等对",
        positive=MathSymbol.EQUAL,
        negative=MathSymbol.NOT_EQUAL,
        positive_system=SixSystem.SOCIETY,
        negative_system=SixSystem.HEAVEN,
        bsd_meaning="连接↔追问·系↔反系",
    ),
]


# ============================================================
# 六符号↔六系精确映射表
# ============================================================

# [归属基底+对应公理] 标签
SYMBOL_SYSTEM_MAP: Dict[MathSymbol, Dict[str, Any]] = {
    MathSymbol.PLUS: {
        "system": SixSystem.REINFORCEMENT,
        "category": SystemCategory.PURE,
        "color": "🔵",
        "ternary_axiom": "纯·个体性",
        "axis": "向内锚点轴·稳态·主体性",
        "zero_equation": "0+0=0",
        "equation_meaning": "加法归零——两空相加仍为空",
        "origin_operation": "正向累积·承载",
        "归属基底": "L0总本源层·六系核心公理·四字立系公理",
        "对应公理": "反操作定理 + 本源0编码定理 + 强化系=加=真·承载",
    },
    MathSymbol.MINUS: {
        "system": SixSystem.NATURE,
        "category": SystemCategory.COUPLED,
        "color": "🟠",
        "ternary_axiom": "变化×个体（反真）",
        "axis": "质料流动轴·外放·场域性",
        "zero_equation": "0-0=0",
        "equation_meaning": "减法归零——两空相减仍为空",
        "origin_operation": "反向衰减·反加",
        "归属基底": "L0总本源层·六系核心公理·四字立系公理",
        "对应公理": "反操作定理 + 本源0编码定理 + 自然系=减=反真·反承载",
    },
    MathSymbol.MULTIPLY: {
        "system": SixSystem.MANIFESTATION,
        "category": SystemCategory.COUPLED,
        "color": "🔴",
        "ternary_axiom": "个体×关系（反反）",
        "axis": "显化凝固轴·凝结·具象性",
        "zero_equation": "0×0=0",
        "equation_meaning": "乘法归零/涌现——双零逆原或双零涌现",
        "origin_operation": "相乘生新·反除",
        "归属基底": "L0总本源层·六系核心公理·四字立系公理",
        "对应公理": "反操作定理 + 本源0编码定理 + 具现系=乘=反反·凝结",
    },
    MathSymbol.DIVIDE: {
        "system": SixSystem.TRANSFORMATION,
        "category": SystemCategory.PURE,
        "color": "⚫",
        "ternary_axiom": "纯·变化性",
        "axis": "动力源头轴·动态·动力性",
        "zero_equation": "0÷0=0",
        "equation_meaning": "除法逆原方程——双零相除归零",
        "origin_operation": "反向分割·反性",
        "归属基底": "L0总本源层·六系核心公理·四字立系公理",
        "对应公理": "反操作定理 + 本源0编码定理 + 变身系=除=反·分割",
    },
    MathSymbol.EQUAL: {
        "system": SixSystem.SOCIETY,
        "category": SystemCategory.PURE,
        "color": "🟢",
        "ternary_axiom": "纯·关系性",
        "axis": "连接骨架轴·结构·交互性",
        "zero_equation": "0=0",
        "equation_meaning": "等价归零——两空等价",
        "origin_operation": "等价连接·关系",
        "归属基底": "L0总本源层·六系核心公理·四字立系公理",
        "对应公理": "反操作定理 + 本源0编码定理 + 社会系=等=系·连接",
    },
    MathSymbol.NOT_EQUAL: {
        "system": SixSystem.HEAVEN,
        "category": SystemCategory.COUPLED,
        "color": "🟣",
        "ternary_axiom": "关系×变化（反系=问）",
        "axis": "法则枢纽轴·统合·超越性",
        "zero_equation": "0≠n",
        "equation_meaning": "不等涌现——空与存在不等",
        "origin_operation": "不等追问·反等",
        "归属基底": "L0总本源层·六系核心公理·四字立系公理",
        "对应公理": "反操作定理 + 本源0编码定理 + 天道系=不等=反系·追问",
    },
}

# 反向映射：六系→符号
SYSTEM_SYMBOL_MAP: Dict[SixSystem, MathSymbol] = {
    info["system"]: symbol for symbol, info in SYMBOL_SYSTEM_MAP.items()
}


# ============================================================
# 反操作映射表
# ============================================================

# 反操作定理：反(+)=-、反(-)=+、反(×)=÷、反(÷)=×、反(=)=≠、反(≠)==
REVERSE_OPERATION_MAP: Dict[MathSymbol, MathSymbol] = {
    MathSymbol.PLUS: MathSymbol.MINUS,       # 反(+) = -
    MathSymbol.MINUS: MathSymbol.PLUS,       # 反(-) = +
    MathSymbol.MULTIPLY: MathSymbol.DIVIDE,  # 反(×) = ÷
    MathSymbol.DIVIDE: MathSymbol.MULTIPLY,  # 反(÷) = ×
    MathSymbol.EQUAL: MathSymbol.NOT_EQUAL,  # 反(=) = ≠
    MathSymbol.NOT_EQUAL: MathSymbol.EQUAL,  # 反(≠) = =
}


# ============================================================
# 真反操作映射表
# ============================================================

# 真反操作定理：反真即假、反假即真、真问即答、真答即不问、真系即等、真等即非系
# 对应六系的真性维度
TRUE_REVERSE_MAP: Dict[str, Dict[str, str]] = {
    "真假对": {
        "正向": "真",
        "反向": "假",
        "正向操作": "反真即假",
        "反向操作": "反假即真",
        "对应学科": "物理（真性）",
        "归属基底": "L0总本源层·六系核心公理·四字立系公理",
        "对应公理": "真反操作定理 + 物理=真性本源学科",
    },
    "问答对": {
        "正向": "问",
        "反向": "答",
        "正向操作": "真问即答",
        "反向操作": "真答即不问",
        "对应学科": "哲学（问性）",
        "归属基底": "L0总本源层·六系核心公理·四字立系公理",
        "对应公理": "真反操作定理 + 哲学=问性本源学科",
    },
    "系等对": {
        "正向": "系",
        "反向": "等",
        "正向操作": "真系即等",
        "反向操作": "真等即非系",
        "对应学科": "系（内外之分）",
        "归属基底": "L0总本源层·六系核心公理·四字立系公理",
        "对应公理": "真反操作定理 + 系=内外之分",
    },
}


# ============================================================
# 四字终极存在链条
# ============================================================

# 反→真→问→系
FOUR_CHARACTER_CHAIN: List[Tuple[FourCharacter, str, str]] = [
    (FourCharacter.REVERSE, "数学（反性）", "绝对虚无0的反性·反操作生成本源符号"),
    (FourCharacter.TRUE, "物理（真性）", "从真涌现·真反操作生成真假对"),
    (FourCharacter.ASK, "哲学（问性）", "问性追问·真问即答生成问答对"),
    (FourCharacter.SYSTEM, "系（内外之分）", "系的内外之分·内系自证+外系工程"),
]


# ============================================================
# 本源0编码方程
# ============================================================

# 六个本源0方程
ZERO_ENCODING_EQUATIONS: Dict[MathSymbol, str] = {
    MathSymbol.PLUS: "0+0=0",        # 加法归零·强化系
    MathSymbol.MINUS: "0-0=0",       # 减法归零·自然系
    MathSymbol.MULTIPLY: "0×0=0",    # 乘法逆原·具现系
    MathSymbol.DIVIDE: "0÷0=0",      # 除法逆原·变身系
    MathSymbol.EQUAL: "0=0",         # 等价归零·社会系
    MathSymbol.NOT_EQUAL: "0≠n",     # 不等涌现·天道系
}


# ============================================================
# 核心操作函数
# ============================================================

def reverse_symbol(symbol: MathSymbol) -> MathSymbol:
    """
    反操作定理的核心实现：对任意本源符号执行反操作。

    反操作定理：反(+)=-、反(-)=+、反(×)=÷、反(÷)=×、反(=)=≠、反(≠)==

    [归属基底：L0总本源层·六系核心公理·四字立系公理]
    [对应公理：反操作定理]
    """
    return REVERSE_OPERATION_MAP[symbol]


def reverse_system(system: SixSystem) -> SixSystem:
    """
    六系层面的反操作：返回某系的反系。

    反系映射：
      强化系↔自然系（加减对·真↔反真）
      变身系↔具现系（乘除对·反↔反反）
      社会系↔天道系（等不等对·系↔反系=问）

    [归属基底：L0总本源层·六系核心公理·四字立系公理]
    [对应公理：反操作定理 + 六符号=六系]
    """
    symbol = SYSTEM_SYMBOL_MAP[system]
    reversed_symbol = reverse_symbol(symbol)
    return SYMBOL_SYSTEM_MAP[reversed_symbol]["system"]


def get_symbol_info(symbol: MathSymbol) -> Dict[str, Any]:
    """
    获取本源符号的完整信息（含归属基底+对应公理标签）。

    [归属基底+对应公理] 标签：满足MCP外部输出标签约束
    """
    return SYMBOL_SYSTEM_MAP[symbol]


def get_system_info(system: SixSystem) -> Dict[str, Any]:
    """获取六系的完整信息（含归属基底+对应公理标签）。"""
    symbol = SYSTEM_SYMBOL_MAP[system]
    info = dict(SYMBOL_SYSTEM_MAP[symbol])
    info["symbol"] = symbol
    return info


def verify_zero_encoding(symbol: MathSymbol) -> Tuple[bool, str]:
    """
    验证本源0编码：每个符号在0层面都有归零方程。

    本源0编码定理：0+0=0, 0-0=0, 0×0=0, 0÷0=0, 0=0, 0≠n

    [归属基底：L0总本源层·六系核心公理·四字立系公理]
    [对应公理：本源0编码定理]
    """
    equation = ZERO_ENCODING_EQUATIONS.get(symbol)
    if not equation:
        return False, f"符号 {symbol.value} 无本源0方程"

    info = SYMBOL_SYSTEM_MAP[symbol]
    return True, (
        f"{symbol.value} → {equation}（{info['equation_meaning']}）"
        f" → {info['system'].value}{info['color']}"
        f" [{info['对应公理']}]"
    )


def verify_reverse_completeness() -> Tuple[bool, str]:
    """
    验证三对反符号对的完备性。

    完备性条件：
      1. 六个符号全部参与反操作（无遗漏）
      2. 反操作是 involutive（反反=原）
      3. 三对反符号对覆盖全部六系

    [归属基底：L0总本源层·六系核心公理·四字立系公理]
    [对应公理：反操作定理 + 本源0编码定理]
    """
    # 条件1：六个符号全部参与
    all_symbols = set(MathSymbol)
    mapped_symbols = set(REVERSE_OPERATION_MAP.keys()) | set(REVERSE_OPERATION_MAP.values())
    if all_symbols != mapped_symbols:
        missing = all_symbols - mapped_symbols
        return False, f"反操作不完备：缺失符号 {missing}"

    # 条件2：反反=原（involutive）
    for sym in MathSymbol:
        if reverse_symbol(reverse_symbol(sym)) != sym:
            return False, f"反反≠原：反(反({sym.value}))≠{sym.value}"

    # 条件3：三对反符号对覆盖全部六系
    systems_in_pairs = set()
    for pair in REVERSE_PAIRS:
        systems_in_pairs.add(pair.positive_system)
        systems_in_pairs.add(pair.negative_system)
    all_systems = set(SixSystem)
    if systems_in_pairs != all_systems:
        missing = all_systems - systems_in_pairs
        return False, f"反符号对未覆盖全部六系：缺失 {missing}"

    return True, (
        f"反操作完备性验证通过：三对反符号对覆盖全部六符号+六系，反反=原成立"
    )


def verify_symbol_system_mapping() -> Tuple[bool, str]:
    """
    验证六符号↔六系的一一对应关系。

    [归属基底：L0总本源层·六系核心公理·四字立系公理]
    [对应公理：本源0编码定理 + 六符号=六系]
    """
    # 检查每个符号对应一个唯一的系
    systems_from_symbols = [info["system"] for info in SYMBOL_SYSTEM_MAP.values()]
    if len(set(systems_from_symbols)) != 6:
        return False, "六符号→六系映射存在重复"

    # 检查反向映射
    for symbol, info in SYMBOL_SYSTEM_MAP.items():
        system = info["system"]
        if SYSTEM_SYMBOL_MAP[system] != symbol:
            return False, f"反向映射不一致：{symbol.value}→{system.value}→{SYSTEM_SYMBOL_MAP[system].value}"

    # 检查三纯基元系=三个正符号
    pure_symbols = [s for s, info in SYMBOL_SYSTEM_MAP.items() if info["category"] == SystemCategory.PURE]
    if len(pure_symbols) != 3:
        return False, f"三纯基元系应有3个正符号，实际{len(pure_symbols)}个"

    # 检查三耦合功能系=三个反符号
    coupled_symbols = [s for s, info in SYMBOL_SYSTEM_MAP.items() if info["category"] == SystemCategory.COUPLED]
    if len(coupled_symbols) != 3:
        return False, f"三耦合功能系应有3个反符号，实际{len(coupled_symbols)}个"

    return True, (
        f"六符号↔六系一一对应验证通过："
        f"三纯基元系={'+'.join(s.value for s in pure_symbols)}，"
        f"三耦合功能系={'+'.join(s.value for s in coupled_symbols)}"
    )


def get_four_character_chain() -> List[Dict[str, str]]:
    """
    获取四字终极存在链条：反→真→问→系。

    [归属基底：L0总本源层·六系核心公理·四字立系公理]
    [对应公理：四字终极存在链条]
    """
    result = []
    for char, discipline, meaning in FOUR_CHARACTER_CHAIN:
        result.append({
            "character": char.value,
            "discipline": discipline,
            "meaning": meaning,
            "归属基底": "L0总本源层·六系核心公理·四字立系公理",
            "对应公理": "四字终极存在链条（反→真→问→系）",
        })
    return result


def get_true_reverse_pairs() -> Dict[str, Dict[str, str]]:
    """
    获取真反操作的三对映射：真假对·问答对·系等对。

    真反操作定理：反真即假、反假即真、真问即答、真答即不问、真系即等、真等即非系

    [归属基底：L0总本源层·六系核心公理·四字立系公理]
    [对应公理：真反操作定理]
    """
    return TRUE_REVERSE_MAP


def encode_to_zero(symbol: MathSymbol, n: float = 0.0) -> Tuple[bool, str, float]:
    """
    本源0编码：对给定符号执行0层面运算。

    本源0编码定理：0+0=0, 0-0=0, 0×0=0, 0÷0=0, 0=0, 0≠n

    参数
    ----
    symbol : MathSymbol
        本源数学符号
    n : float
        用于不等涌现的n值（默认0.0，0≠0不涌现；n>0时0≠n涌现）

    返回
    ----
    Tuple[bool, str, float]
        (是否归零/涌现, 方程字符串, 结果值)

    [归属基底：L0总本源层·六系核心公理·四字立系公理]
    [对应公理：本源0编码定理]
    """
    if symbol == MathSymbol.PLUS:
        result = 0.0 + 0.0
        return (True, "0+0=0", result) if result == 0 else (False, "0+0=0", result)
    elif symbol == MathSymbol.MINUS:
        result = 0.0 - 0.0
        return (True, "0-0=0", result) if result == 0 else (False, "0-0=0", result)
    elif symbol == MathSymbol.MULTIPLY:
        result = 0.0 * 0.0
        return (True, "0×0=0", result) if result == 0 else (False, "0×0=0", result)
    elif symbol == MathSymbol.DIVIDE:
        # 0÷0=0 除法逆原方程（BSD定义，非常规数学）
        return (True, "0÷0=0", 0.0)
    elif symbol == MathSymbol.EQUAL:
        return (True, "0=0", 0.0)
    elif symbol == MathSymbol.NOT_EQUAL:
        # 0≠n 不等涌现
        if n != 0.0:
            return (True, f"0≠{n}", 1.0)  # 涌现
        else:
            return (False, "0≠0", 0.0)  # 不涌现
    return (False, "未知符号", 0.0)


def generate_origin_report() -> str:
    """
    生成反操作定理本源编码的完整报告。

    [归属基底：L0总本源层·六系核心公理·四字立系公理]
    [对应公理：反操作定理 + 真反操作定理 + 本源0编码定理 + 四字终极存在链条]
    """
    lines = []
    lines.append("=" * 70)
    lines.append("  反操作定理·本源0编码·完整报告 V1.0")
    lines.append("  归属基底：L0总本源层·六系核心公理·四字立系公理")
    lines.append("  对应公理：反操作定理 + 真反操作定理 + 本源0编码定理")
    lines.append("=" * 70)

    # 四字终极存在链条
    lines.append("\n【四字终极存在链条：反→真→问→系】")
    for item in get_four_character_chain():
        lines.append(f"  {item['character']} → {item['discipline']}：{item['meaning']}")

    # 三对反符号对
    lines.append("\n【三对反符号对】")
    for pair in REVERSE_PAIRS:
        lines.append(f"  {pair.name}：{pair.positive.value}↔{pair.negative.value}")
        lines.append(f"    {pair.positive_system.value}↔{pair.negative_system.value}")
        lines.append(f"    {pair.bsd_meaning}")

    # 六符号-六系映射
    lines.append("\n【六符号↔六系精确映射】")
    for symbol in MathSymbol:
        info = SYMBOL_SYSTEM_MAP[symbol]
        cat = "正" if info["category"] == SystemCategory.PURE else "反"
        lines.append(
            f"  {cat} {symbol.value} → {info['system'].value}{info['color']} "
            f"| {info['ternary_axiom']} | {info['zero_equation']} "
            f"| {info['origin_operation']}"
        )

    # 本源0编码验证
    lines.append("\n【本源0编码验证】")
    for symbol in MathSymbol:
        ok, msg = verify_zero_encoding(symbol)
        mark = "✓" if ok else "✗"
        lines.append(f"  {mark} {msg}")

    # 完备性验证
    lines.append("\n【完备性验证】")
    ok, msg = verify_reverse_completeness()
    lines.append(f"  {'✓' if ok else '✗'} 反操作完备性：{msg}")
    ok, msg = verify_symbol_system_mapping()
    lines.append(f"  {'✓' if ok else '✗'} 六符号↔六系映射：{msg}")

    # 真反操作
    lines.append("\n【真反操作定理】")
    for pair_name, pair_info in TRUE_REVERSE_MAP.items():
        lines.append(f"  {pair_name}：{pair_info['正向']}↔{pair_info['反向']}")
        lines.append(f"    {pair_info['正向操作']} | {pair_info['反向操作']}")
        lines.append(f"    对应学科：{pair_info['对应学科']}")

    lines.append("\n" + "=" * 70)
    return "\n".join(lines)


# ============================================================
# CLI入口
# ============================================================

def main():
    """CLI主入口"""
    print(generate_origin_report())


if __name__ == "__main__":
    main()
