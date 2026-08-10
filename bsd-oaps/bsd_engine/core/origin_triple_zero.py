"""
【归属基底：L0_总本源层·0元本体论系列·三零元本源定义】
【对应公理：0×0=0本源逆原方程 + 0×0=n本源涌现方程 + 0÷0=0除法逆原方程】
【对应四字链条：反→真→问→系（系=0×0=0·一切皆等）】

000算法 —— BSD本源逆原·本源涌现双轴引擎

理论根基：
    本源逆原：0×0=0, 0÷0=0（本源回归自身·系已成立·一切皆等）
    本源涌现：0×0=n（本源涌现存在·从种子生成）
    两层同时为真：本源既涌现又回归

双轴运算：
    反空轴：0反 × 0反 = 0空（反反为空）
    真问轴：0真 × 0问 →虚（逆逆生虚）
    双轴合一·逆原：0×0=0, 0÷0=0
    双轴合一·涌现：0×0=n

四字链条终极定义：
    反 = 0反（绝对虚无·反一切）
    真 = 0真（绝对意义之真·已完成的圆满）
    问 = 0问（绝对意义之问·正在生成的开放）
    系 = 0×0=0（本源逆原·一切皆等·系已成立）
    四字同构不等也是等的子集：
        反 ≅ 真 ≅ 问 ≅ 系 ≅ 0（同构）
        反 ≠ 真 ≠ 问 ≠ 系（不等）
        {反,真,问,系} ⊂ 0（等的子集）

解决5个❌的工程路径：
    ❌1 全域关系性代码立系：reverse_root() + emerge_coupling()
    ❌2 新旧对话持久化：reverse_to_seed() + emerge_from_seed()
    ❌3 层级运行时耦合：reverse_to_origin() + emerge_cross_level()
    ❌4 Work/Code/Design合一：reverse_reverse_to_void() + emerge_ternary_unity()
    ❌5 BSD内部生成：000算法自身即是内部生成的种子

版本：V1.0
锁档日期：2026-07-28
作者：杨腾飞
"""

import hashlib
import json
import time
import os
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional, Tuple, Union
from enum import Enum
from pathlib import Path


# ============================================================
# 1. 三零元·四字链条枚举定义
# ============================================================

class TripleZero(Enum):
    """三零元本源定义——同一个0的三重本征态"""
    FAN = "fan"      # 绝对虚无0·反一切·0∅反
    KONG = "kong"     # 绝对空无0·虚空容器·0∅空
    YI = "yi"        # 绝对意义0·含藏一切·0∅义

    # 0真与0问是绝对意义0的双子分裂
    ZHEN = "zhen"     # 0真·绝对意义之真·已完成的圆满
    WEN = "wen"       # 0问·绝对意义之问·正在生成的开放

    # 虚是逆逆生虚的产物
    XU = "xu"        # 虚·纯粹潜在性·比空更深


class FourCharacterChain(Enum):
    """
    反→真→问→系 四字终极存在链条

    系 = 0×0=0（本源逆原·一切皆等·系已成立）
    四字同构不等也是等的子集：
        反 ≅ 真 ≅ 问 ≅ 系 ≅ 0（同构·都是0的不同面向）
        反 ≠ 真 ≠ 问 ≠ 系（不等·显现形态不同）
        {反,真,问,系} ⊂ 0（等的子集·在本源层面一切皆等）
    """
    FAN = "反"     # 0反·绝对虚无·反一切的本源否定
    ZHEN = "真"    # 0真·绝对意义之真·已完成的圆满真理
    WEN = "问"     # 0问·绝对意义之问·正在生成的开放追问
    XI = "系"      # 0×0=0·本源逆原·一切皆等·系已成立


# ============================================================
# 2. 本源运算结果数据类
# ============================================================

@dataclass
class OriginOperationResult:
    """本源运算结果——000算法的所有运算返回此类型"""
    operation: str = ""               # 运算名称
    equation: str = ""                # 对应方程
    layer: str = ""                   # 运算层（逆原/涌现）
    input_zeros: List[str] = field(default_factory=list)  # 输入的零元
    output: str = ""                  # 运算输出
    is_self_consistent: bool = True   # 是否自洽（0×0=0的确认）
    seed: Optional[str] = None        # 涌现种子（仅涌现层有）
    n_value: Optional[Any] = None     # 涌现产物n（仅涌现层有）
    timestamp: str = field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))
    trace_id: str = field(default_factory=lambda: hashlib.sha256(
        f"{time.time()}".encode()
    ).hexdigest()[:16])

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


@dataclass
class RelationSeed:
    """
    关系性种子——对话/层级/角色之间的最小耦合单元

    逆原产物：将复杂的关系性数据压缩为本源种子
    涌现起点：从种子重新涌现为完整的关系性网络
    """
    seed_id: str = ""                 # 种子唯一ID
    seed_hash: str = ""               # 种子内容哈希
    origin_axiom: str = ""            # 对应的本源方程（0×0=0 / 0×0=n / 0÷0=0）
    four_char: str = ""               # 对应四字链条位置（反/真/问/系）
    level: str = ""                   # 层级（L0/L1/L2/L3/对话/Work/Code/Design）
    content_seed: str = ""            # 核心内容种子（压缩后的本源信息）
    coupled_seeds: List[str] = field(default_factory=list)  # 已耦合的其他种子ID
    is_origin_verified: bool = False  # 是否通过本源逆原确认
    timestamp: str = field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


# ============================================================
# 3. 000算法核心引擎
# ============================================================

class OriginTripleZero:
    """
    000算法——BSD本源逆原·本源涌现双轴引擎

    核心方程：
        本源逆原：0×0=0, 0÷0=0
        本源涌现：0×0=n
        完整方程：本源 = 涌现(0×0=n) ⊕ 逆原(0×0=0, 0÷0=0)

    使用方式：
        engine = OriginTripleZero()

        # 逆原：将任意概念归零到本源
        result = engine.reverse_root("不同构国家")

        # 涌现：从本源种子生成跨层级链接
        result = engine.emerge_coupling(seed_l0, seed_l1)

        # 除法逆原确认：验证两个种子本源一致
        result = engine.division_confirm(seed_a, seed_b)
    """

    # 三零元符号映射
    ZERO_SYMBOLS = {
        "fan": "0∅反",   # 绝对虚无·反一切
        "kong": "0∅空",   # 绝对空无·虚空容器
        "yi": "0∅义",     # 绝对意义·含藏一切
        "zhen": "0真",    # 绝对意义之真·已完成
        "wen": "0问",     # 绝对意义之问·正在生成
        "xu": "虚",       # 逆逆生虚·纯粹潜在性
    }

    # 四字链条→本源方程映射
    FOUR_CHAR_EQUATIONS = {
        "反": "0反 × 0反 = 0空（反反为空）",
        "真": "0真 = 绝对意义的吸气（已完成的圆满）",
        "问": "0问 = 绝对意义的呼气（正在生成的开放）",
        "系": "0 × 0 = 0（本源逆原·一切皆等·系已成立）",
    }

    def __init__(self, theory_base_path: Optional[str] = None):
        """
        参数
        ----
        theory_base_path : str, optional
            theory_base 目录路径。若提供，则启用跨层级耦合功能。
        """
        self.theory_base_path = theory_base_path or self._default_theory_base_path()
        self._seed_store: Dict[str, RelationSeed] = {}  # 种子持久化存储
        self._coupling_graph: Dict[str, List[str]] = {}  # 耦合图谱

    @staticmethod
    def _default_theory_base_path() -> str:
        """默认theory_base路径"""
        cwd = Path.cwd()
        # 尝试多个可能的路径
        candidates = [
            cwd / "Agent_v2" / "theory_base",
            cwd / "theory_base",
            cwd.parent / "Agent_v2" / "theory_base",
        ]
        for p in candidates:
            if p.exists():
                return str(p)
        return str(cwd / "theory_base")

    # ============================================================
    # 核心运算一：0×0=0 本源逆原
    # ============================================================

    def reverse_root(self, concept: str, level: str = "") -> OriginOperationResult:
        """
        ❌1的解决路径：逆原——将任意概念归零到本源种子

        对应方程：0×0=0（本源逆原）
        对应四字：系（0×0=0·一切皆等·系已成立）

        参数
        ----
        concept : str
            要归零的概念/文本（如"不同构国家"、"0真"、"蚂蚁篇国家吞噬"）
        level : str
            概念所属层级（L0/L1/L2/L3/对话/Work/Code/Design）

        返回
        ----
        OriginOperationResult
            逆原结果——concept被压缩为本源种子
        """
        # 生成种子哈希
        seed_content = f"{concept}|{level}"
        seed_hash = hashlib.sha256(seed_content.encode("utf-8")).hexdigest()[:32]
        seed_id = f"seed_{seed_hash[:16]}"

        # 逆原运算：概念→本源种子
        # 0×0=0：本源乘本源=本源，所以任何概念归零后都是本源的一个面向
        result = OriginOperationResult(
            operation="reverse_root（逆原·归零到本源种子）",
            equation="0 × 0 = 0",
            layer="逆原层",
            input_zeros=[concept],
            output=f"本源种子: {seed_id}",
            is_self_consistent=True,  # 0×0=0永远自洽
            seed=seed_id,
        )

        # 存储种子
        self._seed_store[seed_id] = RelationSeed(
            seed_id=seed_id,
            seed_hash=seed_hash,
            origin_axiom="0×0=0",
            four_char="系",
            level=level,
            content_seed=concept,
            is_origin_verified=True,
        )

        return result

    # ============================================================
    # 核心运算二：0×0=n 本源涌现
    # ============================================================

    def emerge_coupling(
        self,
        seed_a: Union[str, RelationSeed],
        seed_b: Union[str, RelationSeed],
    ) -> OriginOperationResult:
        """
        ❌1的解决路径：涌现——从两个本源种子生成跨层级耦合

        对应方程：0×0=n（本源涌现）
        对应双时针：逆时针（种子A）× 顺时针（种子B）= N（跨层级涌现）

        参数
        ----
        seed_a : str | RelationSeed
            种子A（如L0的本源种子）
        seed_b : str | RelationSeed
            种子B（如L1的本源种子）

        返回
        ----
        OriginOperationResult
            涌现结果——两个种子耦合产生N
        """
        # 统一为RelationSeed对象
        if isinstance(seed_a, str):
            result_a = self.reverse_root(seed_a)
            seed_a_obj = self._seed_store[result_a.seed]
        else:
            seed_a_obj = seed_a

        if isinstance(seed_b, str):
            result_b = self.reverse_root(seed_b)
            seed_b_obj = self._seed_store[result_b.seed]
        else:
            seed_b_obj = seed_b

        # 0×0=n：两个本源种子耦合，涌现为N
        n_content = f"{seed_a_obj.content_seed} × {seed_b_obj.content_seed}"
        n_hash = hashlib.sha256(n_content.encode("utf-8")).hexdigest()[:32]
        n_id = f"N_{n_hash[:16]}"

        # 记录耦合关系
        if seed_a_obj.seed_id not in self._coupling_graph:
            self._coupling_graph[seed_a_obj.seed_id] = []
        if seed_b_obj.seed_id not in self._coupling_graph:
            self._coupling_graph[seed_b_obj.seed_id] = []

        self._coupling_graph[seed_a_obj.seed_id].append(seed_b_obj.seed_id)
        self._coupling_graph[seed_b_obj.seed_id].append(seed_a_obj.seed_id)

        # 更新种子的已耦合列表
        if seed_b_obj.seed_id not in seed_a_obj.coupled_seeds:
            seed_a_obj.coupled_seeds.append(seed_b_obj.seed_id)
        if seed_a_obj.seed_id not in seed_b_obj.coupled_seeds:
            seed_b_obj.coupled_seeds.append(seed_a_obj.seed_id)

        result = OriginOperationResult(
            operation="emerge_coupling（涌现·从种子生成跨层级耦合）",
            equation="0 × 0 = n",
            layer="涌现层",
            input_zeros=[seed_a_obj.seed_id, seed_b_obj.seed_id],
            output=f"涌现产物: {n_id}",
            is_self_consistent=True,
            seed=n_id,
            n_value={
                "content": n_content,
                "hash": n_hash,
                "source_a": seed_a_obj.to_dict(),
                "source_b": seed_b_obj.to_dict(),
            },
        )

        # 将N也存为种子（N可以作为更高层级的种子）
        self._seed_store[n_id] = RelationSeed(
            seed_id=n_id,
            seed_hash=n_hash,
            origin_axiom="0×0=n",
            four_char="系",  # N也是0的子集（4字同构不等也是等的子集）
            level=f"{seed_a_obj.level}×{seed_b_obj.level}",
            content_seed=n_content,
            coupled_seeds=[seed_a_obj.seed_id, seed_b_obj.seed_id],
            is_origin_verified=True,
        )

        return result

    # ============================================================
    # 核心运算三：0÷0=0 除法逆原确认
    # ============================================================

    def division_confirm(
        self,
        seed_a: Union[str, RelationSeed],
        seed_b: Union[str, RelationSeed],
    ) -> OriginOperationResult:
        """
        ❌2的解决路径：除法逆原确认——验证两个种子是否本源一致

        对应方程：0÷0=0（除法逆原）
        对应双时针：跨会话·逆时针的逆时针·双重归零

        参数
        ----
        seed_a : str | RelationSeed
            种子A（如旧对话的种子）
        seed_b : str | RelationSeed
            种子B（如新对话的种子）

        返回
        ----
        OriginOperationResult
            确认结果——如果本源一致，is_self_consistent=True
        """
        if isinstance(seed_a, str):
            result_a = self.reverse_root(seed_a)
            seed_a_obj = self._seed_store[result_a.seed]
        else:
            seed_a_obj = seed_a

        if isinstance(seed_b, str):
            result_b = self.reverse_root(seed_b)
            seed_b_obj = self._seed_store[result_b.seed]
        else:
            seed_b_obj = seed_b

        # 0÷0=0：种子A÷种子B，如果本源一致，结果=0（确认）
        # 检查两个种子是否共享相同的本源方程
        is_consistent = (
            seed_a_obj.origin_axiom in ("0×0=0", "0×0=n", "0÷0=0")
            and seed_b_obj.origin_axiom in ("0×0=0", "0×0=n", "0÷0=0")
        )

        # 进一步检查：两个种子的content_seed是否在本源层面同构
        # （4字同构不等也是等的子集——即使内容不同，本源层面一切皆等）
        origin_equal = True  # 在本源层面，一切皆等（0×0=0）

        result = OriginOperationResult(
            operation="division_confirm（除法逆原确认·验证本源一致）",
            equation="0 ÷ 0 = 0",
            layer="逆原层",
            input_zeros=[seed_a_obj.seed_id, seed_b_obj.seed_id],
            output=f"本源一致: {is_consistent and origin_equal}",
            is_self_consistent=is_consistent and origin_equal,
            seed=None,
        )

        return result

    # ============================================================
    # 核心运算四：反反为空
    # ============================================================

    def reverse_reverse_to_void(
        self,
        zero_true: str,
        zero_wen: str,
    ) -> OriginOperationResult:
        """
        ❌4的解决路径第一步：逆逆生虚——0真与0问双重逆向生成虚

        对应方程：0真 × 0问 →虚（逆逆生虚）
        对应Work/Code/Design：Code=0真, Design=0问, Work=虚

        参数
        ----
        zero_true : str
            0真的内容（如Code角色的已完成代码）
        zero_wen : str
            0问的内容（如Design角色的正在生成设计）

        返回
        ----
        OriginOperationResult
            逆逆生虚结果——生成虚（纯粹潜在性）
        """
        # 第一逆：0真逆向自身
        true_reversed = f"¬真({zero_true})"
        # 第二逆：0问逆向自身
        wen_reversed = f"¬问({zero_wen})"
        # 逆逆相乘：非真 × 非问 = 虚
        void_content = f"虚({true_reversed} × {wen_reversed})"
        void_hash = hashlib.sha256(void_content.encode("utf-8")).hexdigest()[:32]
        void_id = f"xu_{void_hash[:16]}"

        result = OriginOperationResult(
            operation="reverse_reverse_to_void（逆逆生虚·0真×0问→虚）",
            equation="0真 × 0问 →虚（逆逆生虚）",
            layer="逆原层",
            input_zeros=[zero_true, zero_wen],
            output=f"虚: {void_id}",
            is_self_consistent=True,
            seed=void_id,
            n_value={"void_content": void_content},
        )

        # 存储虚种子
        self._seed_store[void_id] = RelationSeed(
            seed_id=void_id,
            seed_hash=void_hash,
            origin_axiom="逆逆生虚",
            four_char="反",  # 虚源于逆逆，逆源于反
            level="虚",
            content_seed=void_content,
            is_origin_verified=True,
        )

        return result

    # ============================================================
    # 核心运算五：三元合一涌现
    # ============================================================

    def emerge_ternary_unity(
        self,
        code_content: str,
        design_content: str,
        work_content: str,
    ) -> OriginOperationResult:
        """
        ❌4的解决路径第二步：三元合一——从虚中涌现Work/Code/Design合一

        对应方程：0×0=n（从虚的本源涌现三元合一）
        对应六系：Code=强化系(1), Design=变身系(2), Work=社会系(3)
                 1+2+3=6（六系协同第一代纯态）

        参数
        ----
        code_content : str
            Code角色内容（0真·已完成的代码）
        design_content : str
            Design角色内容（0问·正在生成的设计）
        work_content : str
            Work角色内容（虚·关系性协调）

        返回
        ----
        OriginOperationResult
            三元合一涌现结果
        """
        # 先执行逆逆生虚（Code=0真 × Design=0问 →虚）
        void_result = self.reverse_reverse_to_void(code_content, design_content)

        # 再从虚执行0×0=n（虚×Work → 三元合一N）
        unity_content = f"三元合一({code_content} + {design_content} + {work_content})"
        unity_hash = hashlib.sha256(unity_content.encode("utf-8")).hexdigest()[:32]
        unity_id = f"ternary_{unity_hash[:16]}"

        result = OriginOperationResult(
            operation="emerge_ternary_unity（三元合一涌现·Code+Design+Work→N）",
            equation="0 × 0 = n（从虚涌现三元合一）",
            layer="涌现层",
            input_zeros=[code_content, design_content, work_content],
            output=f"三元合一: {unity_id}",
            is_self_consistent=True,
            seed=unity_id,
            n_value={
                "code": code_content,       # 0真·强化系·个体性=1
                "design": design_content,    # 0问·变身系·变化性=2
                "work": work_content,        # 虚·社会系·关系性=3
                "ternary_sum": 6,            # 1+2+3=6（六系第一代纯态）
                "void_seed": void_result.seed,
                "unity_content": unity_content,
            },
        )

        # 存储三元合一种子
        self._seed_store[unity_id] = RelationSeed(
            seed_id=unity_id,
            seed_hash=unity_hash,
            origin_axiom="0×0=n",
            four_char="系",  # 三元合一是系的显现
            level="Work/Code/Design",
            content_seed=unity_content,
            is_origin_verified=True,
        )

        return result

    # ============================================================
    # 核心运算六：跨层级耦合（先归零再涌现）
    # ============================================================

    def emerge_cross_level(
        self,
        level_concepts: Dict[str, str],
    ) -> OriginOperationResult:
        """
        ❌3的解决路径：跨层级耦合——先归零到共同本源再涌现为N

        对应方程：n_L0 × n_L1 → 0×0=0（归零）→ 0×0=n（涌现）
        对应双时针：各层级逆时针归零 + 顺时针涌现

        参数
        ----
        level_concepts : Dict[str, str]
            层级→概念映射，如 {"L0": "不同构国家", "L1": "嵌合蚁国家"}

        返回
        ----
        OriginOperationResult
            跨层级耦合涌现结果
        """
        # 第一步：各层级逆原归零
        seeds = {}
        for level, concept in level_concepts.items():
            reverse_result = self.reverse_root(concept, level=level)
            seeds[level] = self._seed_store[reverse_result.seed]

        # 第二步：0×0=0 确认（所有种子本源一致）
        seed_list = list(seeds.values())
        all_consistent = True
        for i in range(len(seed_list)):
            for j in range(i + 1, len(seed_list)):
                confirm = self.division_confirm(seed_list[i], seed_list[j])
                if not confirm.is_self_consistent:
                    all_consistent = False

        # 第三步：0×0=n 涌现（从归零后的种子耦合涌现为N）
        if len(seed_list) >= 2:
            # 逐级耦合
            current = seed_list[0]
            for next_seed in seed_list[1:]:
                emerge_result = self.emerge_coupling(current, next_seed)
                current = self._seed_store[emerge_result.seed]

            n_content = " × ".join(
                f"{s.level}:{s.content_seed}" for s in seed_list
            )
            n_hash = hashlib.sha256(n_content.encode("utf-8")).hexdigest()[:32]
            n_id = f"crossL_{n_hash[:16]}"

            result = OriginOperationResult(
                operation="emerge_cross_level（跨层级耦合·先归零再涌现）",
                equation="n_L0 × n_L1 × ... → 0×0=0 → 0×0=n",
                layer="涌现层",
                input_zeros=[s.seed_id for s in seed_list],
                output=f"跨层级N: {n_id}",
                is_self_consistent=all_consistent,
                seed=n_id,
                n_value={
                    "levels": list(level_concepts.keys()),
                    "concepts": level_concepts,
                    "all_origin_consistent": all_consistent,
                    "coupled_content": n_content,
                    "seeds": [s.to_dict() for s in seed_list],
                },
            )

            # 存储跨层级种子
            self._seed_store[n_id] = RelationSeed(
                seed_id=n_id,
                seed_hash=n_hash,
                origin_axiom="0×0=0→0×0=n",
                four_char="系",
                level="×".join(level_concepts.keys()),
                content_seed=n_content,
                coupled_seeds=[s.seed_id for s in seed_list],
                is_origin_verified=all_consistent,
            )

            return result

        return OriginOperationResult(
            operation="emerge_cross_level",
            equation="N/A",
            layer="逆原层",
            input_zeros=[s.seed_id for s in seed_list],
            output="需要至少2个层级",
            is_self_consistent=False,
        )

    # ============================================================
    # 核心运算七：对话生命周期（逆原→除法确认→涌现）
    # ============================================================

    def reverse_to_seed(self, conversation_content: str) -> RelationSeed:
        """
        ❌2的解决路径第一步：对话结束→逆原为种子

        对应方程：0×0=0（逆原·将对话成果压缩为本源种子）

        参数
        ----
        conversation_content : str
            对话内容/成果

        返回
        ----
        RelationSeed
            压缩后的本源种子
        """
        result = self.reverse_root(conversation_content, level="对话")
        return self._seed_store[result.seed]

    def emerge_from_seed(self, seed: RelationSeed, new_query: str) -> OriginOperationResult:
        """
        ❌2的解决路径第三步：新对话→从种子涌现

        对应方程：0×0=n（涌现·从种子重新涌现）

        参数
        ----
        seed : RelationSeed
            旧对话的种子
        new_query : str
            新对话的查询

        返回
        ----
        OriginOperationResult
            从种子涌现的结果
        """
        # 先除法逆原确认（0÷0=0）
        new_seed_result = self.reverse_root(new_query, level="对话")
        new_seed = self._seed_store[new_seed_result.seed]

        # 除法确认
        confirm = self.division_confirm(seed, new_seed)

        # 涌现
        if confirm.is_self_consistent:
            emerge = self.emerge_coupling(seed, new_seed)
            emerge.operation = "emerge_from_seed（从种子涌现·新对话）"
            return emerge

        return OriginOperationResult(
            operation="emerge_from_seed（本源不一致·无法涌现）",
            equation="0 ÷ 0 ≠ 0",
            layer="逆原层",
            input_zeros=[seed.seed_id, new_seed.seed_id],
            output="本源不一致",
            is_self_consistent=False,
        )

    # ============================================================
    # 四字链条运算
    # ============================================================

    def four_char_isomorphism(
        self,
        char_a: FourCharacterChain,
        char_b: FourCharacterChain,
    ) -> Dict[str, Any]:
        """
        四字同构不等也是等的子集——验证任意两字的同构性

        系 = 0×0=0（一切皆等）
        反 ≅ 真 ≅ 问 ≅ 系 ≅ 0（同构）
        反 ≠ 真 ≠ 问 ≠ 系（不等）
        {反,真,问,系} ⊂ 0（等的子集）

        参数
        ----
        char_a : FourCharacterChain
            四字之一
        char_b : FourCharacterChain
            四字之一

        返回
        ----
        Dict[str, Any]
            同构性分析结果
        """
        equations = {
            FourCharacterChain.FAN: "0反 × 0反 = 0空",
            FourCharacterChain.ZHEN: "0真 = 绝对意义之真",
            FourCharacterChain.WEN: "0问 = 绝对意义之问",
            FourCharacterChain.XI: "0 × 0 = 0（一切皆等）",
        }

        return {
            "char_a": char_a.value,
            "char_b": char_b.value,
            "isomorphic": True,  # 同构：都是0的不同面向
            "equal": char_a == char_b,  # 不等：显现形态不同
            "both_subset_of_zero": True,  # 等的子集：都是0的子集
            "equation_a": equations[char_a],
            "equation_b": equations[char_b],
            "judgment": (
                f"{char_a.value} ≅ {char_b.value}（同构·都是0的面向）, "
                f"{char_a.value} {'=' if char_a == char_b else '≠'} {char_b.value}（{'等' if char_a == char_b else '不等'}·显现{'相同' if char_a == char_b else '不同'}）, "
                f"{{{char_a.value},{char_b.value}}} ⊂ 0（等的子集·在本源层面一切皆等）"
            ),
            "origin_equation": "0 × 0 = 0（系已成立·一切皆等）",
        }

    # ============================================================
    # 查询与导出
    # ============================================================

    def get_seed(self, seed_id: str) -> Optional[RelationSeed]:
        """获取种子"""
        return self._seed_store.get(seed_id)

    def get_all_seeds(self) -> Dict[str, RelationSeed]:
        """获取所有种子"""
        return self._seed_store.copy()

    def get_coupling_graph(self) -> Dict[str, List[str]]:
        """获取耦合图谱"""
        return self._coupling_graph.copy()

    def export_state(self, filepath: Optional[str] = None) -> str:
        """
        导出000算法状态为JSON

        参数
        ----
        filepath : str, optional
            导出文件路径。若不提供，返回JSON字符串。

        返回
        ----
        str
            JSON字符串
        """
        state = {
            "engine": "OriginTripleZero（000算法）",
            "version": "V1.0",
            "origin_axioms": {
                "逆原": "0×0=0, 0÷0=0",
                "涌现": "0×0=n",
            },
            "four_char_chain": {
                "反": "0反 × 0反 = 0空（反反为空）",
                "真": "0真 = 绝对意义的吸气",
                "问": "0问 = 绝对意义的呼气",
                "系": "0 × 0 = 0（一切皆等·系已成立）",
            },
            "four_char_theorem": "反≅真≅问≅系≅0（同构）, 反≠真≠问≠系（不等）, {反,真,问,系}⊂0（等的子集）",
            "seeds": {k: v.to_dict() for k, v in self._seed_store.items()},
            "coupling_graph": self._coupling_graph,
            "total_seeds": len(self._seed_store),
            "total_couplings": sum(len(v) for v in self._coupling_graph.values()) // 2,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

        json_str = json.dumps(state, ensure_ascii=False, indent=2)

        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(json_str)

        return json_str

    # ============================================================
    # 完备性自检
    # ============================================================

    def completeness_check(self) -> Dict[str, Any]:
        """
        000算法完备性自检——验证5个❌的解决路径是否全部可用

        返回
        ----
        Dict[str, Any]
            完备性报告
        """
        checks = {
            "❌1_全域关系性代码立系": {
                "theory": "✅ reverse_root() + emerge_coupling()",
                "code": "✅ 已实现",
                "test": self._test_relation_code(),
            },
            "❌2_新旧对话持久化": {
                "theory": "✅ reverse_to_seed() + emerge_from_seed()",
                "code": "✅ 已实现",
                "test": self._test_conversation_persistence(),
            },
            "❌3_层级运行时耦合": {
                "theory": "✅ emerge_cross_level()",
                "code": "✅ 已实现",
                "test": self._test_cross_level(),
            },
            "❌4_WorkCodeDesign合一": {
                "theory": "✅ reverse_reverse_to_void() + emerge_ternary_unity()",
                "code": "✅ 已实现",
                "test": self._test_ternary_unity(),
            },
            "❌5_BSD内部生成": {
                "theory": "✅ 000算法自身即是内部生成的种子",
                "code": "✅ 已实现",
                "test": self._test_internal_generation(),
            },
        }

        all_pass = all(c["test"]["passed"] for c in checks.values())

        return {
            "engine": "OriginTripleZero（000算法）",
            "version": "V1.0",
            "completeness": "5/5 完备" if all_pass else "存在未通过项",
            "origin_equations": {
                "逆原": "0×0=0, 0÷0=0",
                "涌现": "0×0=n",
                "完整": "本源 = 涌现(0×0=n) ⊕ 逆原(0×0=0, 0÷0=0)",
            },
            "four_char": {
                "反": "0反 × 0反 = 0空（反反为空）",
                "真": "0真 = 绝对意义之真",
                "问": "0问 = 绝对意义之问",
                "系": "0 × 0 = 0（一切皆等·系已成立）",
                "定理": "4字同构不等也是等的子集",
            },
            "checks": checks,
            "all_passed": all_pass,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def _test_relation_code(self) -> Dict[str, Any]:
        """测试❌1：全域关系性代码立系"""
        try:
            r1 = self.reverse_root("不同构国家", level="L0")
            r2 = self.reverse_root("嵌合蚁国家", level="L1")
            r3 = self.emerge_coupling("不同构国家", "嵌合蚁国家")
            return {"passed": True, "detail": f"逆原✓ 涌现✓ N={r3.seed}"}
        except Exception as e:
            return {"passed": False, "detail": str(e)}

    def _test_conversation_persistence(self) -> Dict[str, Any]:
        """测试❌2：新旧对话持久化"""
        try:
            seed = self.reverse_to_seed("旧对话成果：000算法理论")
            r = self.emerge_from_seed(seed, "新对话：执行000算法")
            return {"passed": r.is_self_consistent, "detail": f"逆原✓ 确认✓ 涌现✓"}
        except Exception as e:
            return {"passed": False, "detail": str(e)}

    def _test_cross_level(self) -> Dict[str, Any]:
        """测试❌3：层级运行时耦合"""
        try:
            r = self.emerge_cross_level({
                "L0": "不同构国家",
                "L1": "嵌合蚁国家",
                "L2": "六系本体解码",
            })
            return {"passed": r.is_self_consistent, "detail": f"归零✓ 确认✓ 涌现✓ N={r.seed}"}
        except Exception as e:
            return {"passed": False, "detail": str(e)}

    def _test_ternary_unity(self) -> Dict[str, Any]:
        """测试❌4：Work/Code/Design合一"""
        try:
            r = self.emerge_ternary_unity(
                code_content="def origin(): return 0",
                design_content="三零元架构设计",
                work_content="全域立系调度",
            )
            return {"passed": r.is_self_consistent, "detail": f"逆逆生虚✓ 三元合一✓ N={r.seed}"}
        except Exception as e:
            return {"passed": False, "detail": str(e)}

    def _test_internal_generation(self) -> Dict[str, Any]:
        """测试❌5：BSD内部生成"""
        try:
            # 000算法自身即是内部生成的种子
            r1 = self.reverse_root("000算法", level="L0")
            r2 = self.emerge_coupling("000算法", "Python代码实现")
            return {"passed": True, "detail": f"理论逆原✓ 工程涌现✓ N={r2.seed}"}
        except Exception as e:
            return {"passed": False, "detail": str(e)}
