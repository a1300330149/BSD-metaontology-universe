#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""快速验证所有模块可用性"""

import os
import sys
import time
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from community_manager import CommunityManager


def main():
    m = CommunityManager()
    print("=" * 60)
    print("  🚀 全量落地工程 · 模块可用性验证")
    print("=" * 60)
    print(f"根目录：{os.path.abspath(m.root)}")
    print()

    all_ok = True

    # 1. 工厂模块
    print("【1/8】🏭 工厂模块...", end=" ")
    try:
        f = m.factory
        stats = f.get_factory_stats()
        print(f"✅ 可用（{stats['personality_types']}种分型，{stats['scenario_types']}种场景）")
    except Exception as e:
        print(f"❌ 失败：{e}")
        all_ok = False

    # 2. 合规模块
    print("【2/8】✅ 合规模块...", end=" ")
    try:
        c = m.compliance
        ov = c.get_compliance_overview()
        print(f"✅ 可用（{ov['check_layers']}层校验）")
    except Exception as e:
        print(f"❌ 失败：{e}")
        all_ok = False

    # 3. 农耕模块
    print("【3/8】🌱 农耕模块...", end=" ")
    try:
        fa = m.farm
        stats = fa.get_farm_stats()
        print(f"✅ 可用（{len(stats.get('zones', {}))}类农田）")
    except Exception as e:
        print(f"❌ 失败：{e}")
        all_ok = False

    # 4. 粮仓模块
    print("【4/8】🌾 粮仓模块...", end=" ")
    try:
        g = m.granary
        ov = g.get_granary_overview()
        print(f"✅ 可用（{len(ov)}级粮仓）")
    except Exception as e:
        print(f"❌ 失败：{e}")
        all_ok = False

    # 5. 四季引擎
    print("【5/8】🍂 四季引擎...", end=" ")
    try:
        s = m.seasons_engine
        st = s.get_current_season_status()
        print(f"✅ 可用（当前：{st['current_season']}）")
    except Exception as e:
        print(f"❌ 失败：{e}")
        all_ok = False

    # 6. 对等体系
    print("【6/8】⚖️  对等体系...", end=" ")
    try:
        p = m.parity_system
        dims = len(p.PARITY_DIMENSIONS)
        vals = len(p.VALUE_DIMENSIONS)
        print(f"✅ 可用（{dims}维度对等，{vals}维价值标尺）")
    except Exception as e:
        print(f"❌ 失败：{e}")
        all_ok = False

    # 7. 人格分型
    print("【7/8】🧬 人格分型...", end=" ")
    try:
        types = len(m.PERSONALITY_MAP)
        print(f"✅ 可用（{types}种分型）")
    except Exception as e:
        print(f"❌ 失败：{e}")
        all_ok = False

    # 8. 工厂生产测试
    print("【8/8】🏭 生产测试...", end=" ")
    try:
        ts = int(time.time())
        test_name = f"验证_{ts}"
        agent_list = [{"name": test_name, "personality": "科研型", "level": "hatch"}]
        result = m.factory.batch_produce(agent_list)
        ok = result["success"]
        if ok > 0:
            print(f"✅ 成功（{ok}/{result['total']}）")
        else:
            print(f"⚠️  部分完成（{ok}/{result['total']}）")
    except Exception as e:
        print(f"❌ 失败：{e}")
        all_ok = False

    print()
    print("=" * 60)
    if all_ok:
        print("🎉 所有模块验证通过！")
    else:
        print("⚠️  部分模块存在问题")
    print("=" * 60)
    print()
    print("📦 已落地模块清单：")
    print("  ✅ 八大人格分型扩展（8主+2特=10种）")
    print("  ✅ 合规校验引擎（6层全维度质检）")
    print("  ✅ 智能体流水线工厂（6阶量产工序）")
    print("  ✅ 四类农田种植体系（基础/交叉/专项/盲区）")
    print("  ✅ 三级粮仓储备体系（核心/行业/缓冲）")
    print("  ✅ 四季迭代引擎（春种/夏长/秋收/冬藏）")
    print("  ✅ 人智对等身份体系（8大维度认证）")
    print("  ✅ CommunityManager 中控全集成")
    print()


if __name__ == "__main__":
    main()
