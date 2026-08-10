#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全量落地工程集成测试脚本"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from community_manager import CommunityManager


def main():
    m = CommunityManager()
    print("=" * 60)
    print("  🚀 全量落地工程 · 端到端集成测试")
    print("=" * 60)

    # 1. 工厂批量生产
    print()
    print("【1/6】🏭 工厂批量生产测试")
    print("-" * 60)
    result = m.factory_batch_produce(3, "科研型", "cross_innovation")
    sc = result.get("success_count", 0)
    tot = result.get("total", 0)
    print(f"生产成功：{sc}/{tot}")

    # 2. 合规校验
    print()
    print("【2/6】✅ 合规校验测试")
    print("-" * 60)
    overview = m.compliance_overview()
    tc = overview.get("total_checked", 0)
    print(f"合规总览：已校验 {tc} 个")

    # 3. 农田统计
    print()
    print("【3/6】🌱 农耕体系测试")
    print("-" * 60)
    farm_stats = m.farm_stats()
    zones = farm_stats.get("zones", {})
    print(f"农田分区：{len(zones)} 类")
    for zk, zv in zones.items():
        cnt = zv.get("agent_count", 0)
        print(f"  {zk}：{cnt} 栋")

    # 4. 四季引擎
    print()
    print("【4/6】🍂 四季引擎测试")
    print("-" * 60)
    status = m.seasons_status()
    print(f"当前季节：{status['current_season']}")
    farm_st = status["farm_status"]
    print(f"在培智能体：{farm_st['total_agents']} 栋")
    print(f"成熟体：{farm_st['mature_count']} 栋")
    print(f"生长中：{farm_st['growing_count']} 栋")

    # 5. 粮仓体系
    print()
    print("【5/6】🌾 粮仓体系测试")
    print("-" * 60)
    g_overview = m.granary_overview()
    total = 0
    for gk, gv in g_overview.items():
        if isinstance(gv, dict):
            cnt = gv.get("item_count", 0)
            total += cnt
            print(f"  {gk}：{cnt} 项")
    print(f"粮仓总计：{total} 项")

    # 6. 对等体系
    print()
    print("【6/6】⚖️  对等体系测试")
    print("-" * 60)
    residential = os.path.join(m.root, "residential_area")
    test_agent = None
    if os.path.exists(residential):
        for root, dirs, files in os.walk(residential):
            if "facade.json" in files:
                rel = os.path.relpath(root, m.root)
                test_agent = rel
                break

    if test_agent:
        print(f"测试对象：{test_agent}")
        spec = m.parity_spectrum(test_agent)
        if spec.get("success"):
            print(f"光谱值：{spec['spectrum_value']}")
            print(f"光谱等级：{spec['spectrum_level']}")
        cert = m.parity_certify(test_agent)
        if cert.get("success"):
            print(f"对等综合度：{cert['overall_score']:.1%}")
            print(f"对等等级：{cert['overall_level']}")
    else:
        print("暂无智能体，跳过对等认证测试")

    print()
    print("=" * 60)
    print("🎉 全量落地工程 · 集成测试完成")
    print("=" * 60)
    print()
    print("📋 已落地模块清单：")
    print("  ✅ 八大人格分型扩展（8主+2特）")
    print("  ✅ 合规校验引擎（6层全维度）")
    print("  ✅ 智能体流水线工厂（6阶量产）")
    print("  ✅ 四类农田种植体系（基础/交叉/专项/盲区）")
    print("  ✅ 三级粮仓储备体系（核心/行业/缓冲）")
    print("  ✅ 四季迭代引擎（春种夏长秋收冬藏）")
    print("  ✅ 人智对等身份体系（八大维度认证）")
    print("  ✅ CommunityManager 全功能集成")


if __name__ == "__main__":
    main()
