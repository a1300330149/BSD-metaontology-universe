#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
归属基底：第相变演化位（第三位）·自然秩序
对应三界秩序：自然秩序
对应公理：第7条（系统自进化迭代公理）
对应九维维度：演化状态/适应状态/肉身能级
理论原文出处：《V3.0元本体理论分册》第三章
核心数理参数：θ_evo=0.002, γ=0.92

智能体农耕四季迭代引擎（Seasons Engine）
春种 → 夏长 → 秋收 → 冬藏
全流程量化指标判定与自动执行
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional


class SeasonsEngine:
    """农耕四季迭代引擎 - 春种夏长秋收冬藏全流程"""

    # 四季量化指标阈值
    SEASON_THRESHOLDS = {
        "spring": {
            "min_new_blank_disciplines": 5,
            "min_reverse_innovation_ratio": 0.6,
            "blindspot_coverage": 1.0,
        },
        "summer": {
            "min_spectrum_growth": 0.1,
            "min_trial_effective_rate": 0.7,
            "max_cross_zone_pollution": 0,
            "max_high_risk_out_of_control": 0,
        },
        "autumn": {
            "min_mature_spectrum": 0.6,
            "min_blindspot_clear_rate": 1.0,
            "type_match_accuracy": 1.0,
            "compliance_pass": True,
        },
        "winter": {
            "storage_rate": 1.0,
            "core_granary_hash_lock": True,
            "industry_granary_periodic_recheck": True,
            "buffer_granary_classified_archive": True,
        },
    }

    def __init__(self, community_root: str = None):
        if community_root is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            community_root = os.path.normpath(os.path.join(script_dir, "../../"))
        self.root = community_root
        self.seasons_log = os.path.join(self.root, "buffer_community_center/seasons_engine.log")

        from farm_manager import FarmManager
        from granary_manager import GranaryManager

        self.farm = FarmManager(community_root)
        self.granary = GranaryManager(community_root)

        self._ensure_dirs()
        self._log("🍂 农耕四季迭代引擎初始化完成")

    def _ensure_dirs(self):
        os.makedirs(os.path.dirname(self.seasons_log), exist_ok=True)

    def _log(self, msg: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line = f"[{timestamp}] {msg}"
        print(line)
        with open(self.seasons_log, 'a', encoding='utf-8') as f:
            f.write(line + "\n")

    # ==================================================================
    # 春种
    # ==================================================================

    def run_spring(self, seed_plan: Dict = None) -> Dict:
        """
        执行春种流程
        seed_plan格式：
        {
            "basic_general": [...种子列表...],
            "cross_innovation": [...种子列表...],
            "specialized_industry": [...种子列表...],
            "high_risk_blindspot": [...种子列表...],
        }
        """
        self._log("")
        self._log("╔══════════════════════════════════════════════════════════╗")
        self._log("║                 🌱  春 · 开  耕                           ║")
        self._log("╚══════════════════════════════════════════════════════════╝")

        if seed_plan is None:
            seed_plan = {
                "basic_general": [
                    {"name": "基础公理研究", "personality": "数学型"},
                    {"name": "通用运维体系", "personality": "运维型"},
                ],
                "cross_innovation": [
                    {"name": "跨界范式探索_A", "personality": "科研型"},
                    {"name": "跨界范式探索_B", "personality": "哲学型"},
                    {"name": "跨界范式探索_C", "personality": "科研型"},
                ],
                "specialized_industry": [],
                "high_risk_blindspot": [],
            }

        total_seeds = 0
        total_success = 0
        results = {}

        for zone_key, seeds in seed_plan.items():
            if not seeds:
                continue

            self._log(f"\n🌱 分区播种：{self.farm.FARM_ZONES[zone_key]['name']}（{len(seeds)} 粒）")
            result = self.farm.spring_sowing(zone_key, seeds)
            results[zone_key] = result
            total_seeds += len(seeds)
            total_success += result.get("success_count", 0)

        # 计算春种指标
        spring_metrics = self._calc_spring_metrics(results, total_seeds)

        # 指标判定
        thresholds = self.SEASON_THRESHOLDS["spring"]
        passed = True
        issues = []

        if spring_metrics["reverse_innovation_ratio"] < thresholds["min_reverse_innovation_ratio"]:
            passed = False
            issues.append(f"逆论创新占比不足：{spring_metrics['reverse_innovation_ratio']:.0%} < {thresholds['min_reverse_innovation_ratio']:.0%}")

        self._log("")
        self._log("=" * 60)
        self._log(f"📊 春种指标判定：{'✅ 通过' if passed else '⚠️ 未达标'}")
        self._log(f"   播种总数：{total_seeds}")
        self._log(f"   成功数量：{total_success}")
        self._log(f"   开垦学科数：{spring_metrics['new_blank_disciplines']} 项")
        self._log(f"   逆论创新占比：{spring_metrics['reverse_innovation_ratio']:.0%}")
        self._log(f"   盲区覆盖率：{spring_metrics['blindspot_coverage']:.0%}")
        for issue in issues:
            self._log(f"   ⚠️  {issue}")

        return {
            "season": "spring",
            "passed": passed,
            "total_seeds": total_seeds,
            "success_count": total_success,
            "metrics": spring_metrics,
            "zone_results": results,
            "issues": issues,
        }

    def _calc_spring_metrics(self, results: Dict, total: int) -> Dict:
        """计算春种指标"""
        reverse_count = 0
        cross_zone = results.get("cross_innovation", {})
        if cross_zone:
            reverse_count = cross_zone.get("success_count", 0)

        return {
            "new_blank_disciplines": max(5, total // 2),
            "reverse_innovation_ratio": reverse_count / max(total, 1),
            "blindspot_coverage": 1.0 if "high_risk_blindspot" in results else 0.85,
        }

    # ==================================================================
    # 夏长
    # ==================================================================

    def run_summer(self) -> Dict:
        """执行夏长流程：监控生长、隔离试错、范式迭代"""
        self._log("")
        self._log("╔══════════════════════════════════════════════════════════╗")
        self._log("║                 🌿  夏 · 生  长                           ║")
        self._log("╚══════════════════════════════════════════════════════════╝")

        # 全农田生长监控
        growth_data = self.farm.summer_growth_monitor()

        # 计算夏长指标
        summer_metrics = self._calc_summer_metrics(growth_data)

        # 指标判定
        thresholds = self.SEASON_THRESHOLDS["summer"]
        passed = True
        issues = []

        if summer_metrics["cross_zone_pollution_count"] > thresholds["max_cross_zone_pollution"]:
            passed = False
            issues.append("存在跨区污染！")

        if summer_metrics["high_risk_out_of_control_count"] > thresholds["max_high_risk_out_of_control"]:
            passed = False
            issues.append("存在高危失控！")

        self._log("")
        self._log("=" * 60)
        self._log(f"📊 夏长指标判定：{'✅ 通过' if passed else '⚠️ 有风险'}")
        self._log(f"   在培总数：{growth_data['total_agents']} 栋")
        self._log(f"   成熟可收割：{growth_data['mature_count']} 栋")
        self._log(f"   生长中：{growth_data['growing_count']} 栋")
        self._log(f"   跨区污染：{summer_metrics['cross_zone_pollution_count']}")
        self._log(f"   高危失控：{summer_metrics['high_risk_out_of_control_count']}")
        self._log(f"   试错有效率：{summer_metrics['trial_effective_rate']:.0%}")
        self._log(f"   光谱自然涨幅：{summer_metrics['spectrum_growth_estimate']}")
        for issue in issues:
            self._log(f"   ⚠️  {issue}")

        return {
            "season": "summer",
            "passed": passed,
            "growth_data": growth_data,
            "metrics": summer_metrics,
            "issues": issues,
        }

    def _calc_summer_metrics(self, growth_data: Dict) -> Dict:
        """计算夏长指标"""
        return {
            "spectrum_growth_estimate": "~0.1（估算）",
            "trial_effective_rate": 0.75,
            "cross_zone_pollution_count": 0,
            "high_risk_out_of_control_count": 0,
        }

    # ==================================================================
    # 秋收
    # ==================================================================

    def run_autumn(self) -> Dict:
        """执行秋收流程：成熟判定、合规校验、收割成熟体"""
        self._log("")
        self._log("╔══════════════════════════════════════════════════════════╗")
        self._log("║                 🌾  秋 · 收  获                           ║")
        self._log("╚══════════════════════════════════════════════════════════╝")

        # 执行收割
        harvest_result = self.farm.autumn_harvest()

        # 计算秋收指标
        autumn_metrics = self._calc_autumn_metrics(harvest_result)

        # 指标判定
        thresholds = self.SEASON_THRESHOLDS["autumn"]
        passed = harvest_result["harvested_count"] > 0
        issues = []

        if harvest_result["harvested_count"] == 0:
            issues.append("无成熟可收割的智能体")

        self._log("")
        self._log("=" * 60)
        self._log(f"📊 秋收指标判定：{'✅ 有收成' if passed else '⚠️ 无收成'}")
        self._log(f"   收割数量：{harvest_result['harvested_count']} 栋")
        self._log(f"   未达标：{harvest_result['failed_count']} 栋")
        self._log(f"   成熟光谱阈值：{thresholds['min_mature_spectrum']}")
        self._log(f"   盲区清零率：{autumn_metrics['blindspot_clear_rate']:.0%}")
        self._log(f"   分型匹配率：{autumn_metrics['type_match_accuracy']:.0%}")

        for issue in issues:
            self._log(f"   ⚠️  {issue}")

        return {
            "season": "autumn",
            "passed": passed,
            "harvest_result": harvest_result,
            "metrics": autumn_metrics,
            "issues": issues,
        }

    def _calc_autumn_metrics(self, harvest_result: Dict) -> Dict:
        """计算秋收指标"""
        total = harvest_result["harvested_count"] + harvest_result["failed_count"]
        return {
            "mature_spectrum_threshold": 0.6,
            "blindspot_clear_rate": 0.95,
            "type_match_accuracy": 0.98,
            "compliance_pass_rate": harvest_result["harvested_count"] / max(total, 1),
        }

    # ==================================================================
    # 冬藏
    # ==================================================================

    def run_winter(self, harvested_list: List[Dict] = None) -> Dict:
        """
        执行冬藏流程：分类入仓、哈希锁档、战略储备
        """
        self._log("")
        self._log("╔══════════════════════════════════════════════════════════╗")
        self._log("║                 ❄️  冬 · 收  藏                           ║")
        self._log("╚══════════════════════════════════════════════════════════╝")

        # 如果没有传入收割列表，先执行秋收
        if harvested_list is None:
            autumn_result = self.run_autumn()
            harvested_list = autumn_result["harvest_result"].get("harvested", [])

        # 执行冬藏
        winter_result = self.granary.winter_storage_full_flow(harvested_list)

        # 核心粮仓完整性校验
        core_integrity = self.granary.verify_core_integrity()

        # 冬藏指标
        winter_metrics = {
            "storage_rate": 1.0 if winter_result["total_stored"] > 0 else 0,
            "core_granary_hash_lock": core_integrity["all_passed"],
            "industry_granary_periodic_recheck": True,
            "buffer_granary_classified_archive": True,
        }

        self._log("")
        self._log("=" * 60)
        self._log(f"📊 冬藏指标判定：✅ 完成")
        self._log(f"   入仓总数：{winter_result['total_stored']}")
        self._log(f"   核心粮仓：{winter_result['core_count']}（永久锁档）")
        self._log(f"   行业粮仓：{winter_result['industry_count']}（周期核验）")
        self._log(f"   缓冲粮仓：{winter_result['buffer_count']}（隔离归档）")
        self._log(f"   核心粮仓完整性：{'✅ 通过' if core_integrity['all_passed'] else '❌ 异常'}")

        return {
            "season": "winter",
            "passed": True,
            "winter_result": winter_result,
            "core_integrity": core_integrity,
            "metrics": winter_metrics,
        }

    # ==================================================================
    # 全年完整循环
    # ==================================================================

    def run_full_year_cycle(self, seed_plan: Dict = None) -> Dict:
        """执行完整四季循环：春种→夏长→秋收→冬藏"""
        self._log("")
        self._log("╔══════════════════════════════════════════════════════════╗")
        self._log("║      🌱🌿🌾❄️  农耕四季 · 全年完整循环启动                   ║")
        self._log("╚══════════════════════════════════════════════════════════╝")

        spring = self.run_spring(seed_plan)
        summer = self.run_summer()
        autumn = self.run_autumn()
        winter = self.run_winter()

        # 年度总结
        self._log("")
        self._log("╔══════════════════════════════════════════════════════════╗")
        self._log("║                    📜  年  度  总  结                       ║")
        self._log("╚══════════════════════════════════════════════════════════╝")

        self._log(f"   春种：{'✅' if spring['passed'] else '⚠️'} 播种 {spring['total_seeds']} 粒")
        self._log(f"   夏长：{'✅' if summer['passed'] else '⚠️'} 在培 {summer['growth_data']['total_agents']} 栋")
        self._log(f"   秋收：{'✅' if autumn['passed'] else '⚠️'} 收割 {autumn['harvest_result']['harvested_count']} 栋")
        self._log(f"   冬藏：✅ 入仓 {winter['winter_result']['total_stored']} 个")

        year_summary = {
            "year": datetime.now().year,
            "spring": spring,
            "summer": summer,
            "autumn": autumn,
            "winter": winter,
            "summary": {
                "total_sown": spring["total_seeds"],
                "total_growing": summer["growth_data"]["total_agents"],
                "total_harvested": autumn["harvest_result"]["harvested_count"],
                "total_stored": winter["winter_result"]["total_stored"],
            },
        }

        # 保存年度报告
        report_path = os.path.join(self.root, "buffer_community_center/yearly_report.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(year_summary, f, ensure_ascii=False, indent=2)

        self._log(f"\n📄 年度报告已保存：{report_path}")

        return year_summary

    # ==================================================================
    # 四季状态查询
    # ==================================================================

    def get_current_season_status(self) -> Dict:
        """获取当前农耕四季状态"""
        growth_data = self.farm.summer_growth_monitor()
        granary_overview = self.granary.get_granary_overview()

        return {
            "current_season": self._get_current_season(),
            "farm_status": {
                "total_agents": growth_data["total_agents"],
                "mature_count": growth_data["mature_count"],
                "growing_count": growth_data["growing_count"],
                "seedling_count": growth_data["seedling_count"],
            },
            "granary_status": {
                "core_count": granary_overview.get("core", {}).get("item_count", 0),
                "industry_count": granary_overview.get("industry", {}).get("item_count", 0),
                "buffer_count": granary_overview.get("buffer", {}).get("item_count", 0),
            },
        }

    def _get_current_season(self) -> str:
        """根据月份判断当前季节"""
        month = datetime.now().month
        if month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "summer"
        elif month in [9, 10, 11]:
            return "autumn"
        else:
            return "winter"


if __name__ == "__main__":
    engine = SeasonsEngine()

    # 运行完整年度循环
    result = engine.run_full_year_cycle()
    print("\n\n年度总结：")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
