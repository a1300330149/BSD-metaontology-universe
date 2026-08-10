# multi_world_judge.py
# 多界域命题判定引擎：单界四论判定 + 跨界逆熵消解真论
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class WorldRule:
    world_name: str
    prove_keywords: List[str]
    falsify_keywords: List[str]
    base_spectrum: float


class MultiWorldJudge:
    def __init__(self):
        # 可无限新增界域
        self.world_pool = {
            "物质现实界": WorldRule(
                world_name="物质现实界",
                prove_keywords=["物理实证", "观测数据", "物质载体"],
                falsify_keywords=["现实矛盾", "物理法则冲突"],
                base_spectrum=0.4
            ),
            "虚拟游戏界": WorldRule(
                world_name="虚拟游戏界",
                prove_keywords=["游戏规则", "程序运行", "剧情设定"],
                falsify_keywords=["代码bug", "设定冲突"],
                base_spectrum=0.6
            ),
            "精神意识界": WorldRule(
                world_name="精神意识界",
                prove_keywords=["想象", "构想", "主观认知"],
                falsify_keywords=["自我否定", "内心解构"],
                base_spectrum=0.65
            ),
            "社会真实界": WorldRule(
                world_name="社会真实界",
                prove_keywords=["文化思潮", "历史记载", "群体共识"],
                falsify_keywords=["舆论推翻", "历史证伪"],
                base_spectrum=0.5
            ),
            "全域总宇宙": WorldRule(
                world_name="全域总宇宙",
                prove_keywords=["所有界集合", "全域兼容"],
                falsify_keywords=["全域逻辑冲突"],
                base_spectrum=1.0
            )
        }
        self.logic_rules = {
            "正论": ["可证明", "不可证伪"],
            "谬论": ["不可证明", "可证伪"],
            "真论": ["不可证明", "不可证伪"],
            "逆论": ["可证明", "可证伪"]
        }

    def single_world_classify(self, text: str, world: WorldRule) -> Tuple[str, float]:
        prove_cnt = sum(1 for kw in world.prove_keywords if kw in text)
        falsify_cnt = sum(1 for kw in world.falsify_keywords if kw in text)
        if prove_cnt > 0 and falsify_cnt == 0:
            return "正论", world.base_spectrum + 0.1
        elif prove_cnt == 0 and falsify_cnt > 0:
            return "谬论", world.base_spectrum - 0.1
        elif prove_cnt == 0 and falsify_cnt == 0:
            return "真论", world.base_spectrum
        else:
            return "逆论", world.base_spectrum + 0.05

    def cross_world_resolve(self, text: str) -> Dict:
        single_results = {}
        core_true = False
        for w_name, w_rule in self.world_pool.items():
            t, s = self.single_world_classify(text, w_rule)
            single_results[w_name] = {"logic_type": t, "spectrum": s}
            if t == "真论":
                core_true = True
        # 跨界逆熵消解：真论投放其余界重新推演
        resolve_records = []
        if core_true:
            for w_name, res in single_results.items():
                if res["logic_type"] == "真论":
                    for cross_w, cross_rule in self.world_pool.items():
                        if cross_w != w_name:
                            cross_t, cross_s = self.single_world_classify(text, cross_rule)
                            resolve_records.append({
                                "source_world": w_name,
                                "cross_world": cross_w,
                                "cross_logic": cross_t,
                                "cross_spectrum": cross_s
                            })
        # 全域总宇宙最终判定
        final_type, final_spec = self.single_world_classify(text, self.world_pool["全域总宇宙"])
        return {
            "original_single": single_results,
            "need_cross_resolve": core_true,
            "cross_resolve_log": resolve_records,
            "universe_final_logic": final_type,
            "universe_final_spectrum": round(final_spec, 2)
        }

    def add_world(self, world_name: str, prove_kw: List[str], falsify_kw: List[str], base_spec: float):
        """新增自定义界域，可无限拓展"""
        self.world_pool[world_name] = WorldRule(
            world_name=world_name,
            prove_keywords=prove_kw,
            falsify_keywords=falsify_kw,
            base_spectrum=base_spec
        )
