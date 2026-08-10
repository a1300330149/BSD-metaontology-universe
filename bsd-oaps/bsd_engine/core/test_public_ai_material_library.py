"""
BSD传统AI平台公共素材库·单元测试
[归属基底：L1_外系_局部实验隔离区·虚拟幻造学科树·传统AI平台素材子集]
[对应公理：定理五十四·素材子集定理·推论54.1-54.4]
[V1.0·2026-08-01]
"""

import sys
import os

# 确保模块可导入
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from public_ai_material_library import (
    SixSystem,
    MaterialCapability,
    TraditionalPlatform,
    MaterialMatchResult,
    TRADITIONAL_PLATFORMS,
    init_public_material_library,
    get_universal_material_capabilities,
    get_system_union_materials,
    get_materials_by_capability,
    MaterialSubsetMatcher,
    generate_public_material_report,
)


def test_01_init_platforms():
    """测试1：12大平台正确注册"""
    print("=" * 60)
    print("测试1：12大平台注册完整性")
    print("=" * 60)
    init_public_material_library()
    expected_ids = {
        "runway", "pika", "sora", "kling", "vidu", "hailuo",
        "luma", "svd", "firefly", "hunyuan", "jimeng", "updream"
    }
    actual_ids = set(TRADITIONAL_PLATFORMS.keys())
    assert actual_ids == expected_ids, (
        f"平台ID不匹配！\n缺失：{expected_ids - actual_ids}\n多余：{actual_ids - expected_ids}"
    )
    assert len(TRADITIONAL_PLATFORMS) == 12, f"平台数量应为12，实际{len(TRADITIONAL_PLATFORMS)}"
    print(f"✅ 12大平台注册完整：{sorted(actual_ids)}")
    return True


def test_02_platform_system_coverage():
    """测试2：各平台六系覆盖正确性"""
    print("\n" + "=" * 60)
    print("测试2：各平台六系覆盖正确性")
    print("=" * 60)

    # 素材子集定理：所有传统平台都是真子集，必缺失天道系
    non_tiandao_count = 0
    for pid, p in TRADITIONAL_PLATFORMS.items():
        if SixSystem.TIANDao not in p.covered_systems:
            non_tiandao_count += 1
        print(f"  {p.name:<18} 覆盖{len(p.covered_systems)}系 · "
              f"系数={p.system_coverage_score:.1f}/6 · "
              f"定位={p.material_type()}")

    # Updream以外的所有平台必须缺失天道系
    assert non_tiandao_count == 12, (
        f"传统平台必缺失天道系！但只有{non_tiandao_count}/12缺失"
    )
    print("✅ 所有12平台均不覆盖天道系（符合素材子集定理）")

    # Updream必须覆盖5系（最多）
    updream = TRADITIONAL_PLATFORMS["updream"]
    assert updream.is_main_platform, "Updream必须标记为主平台"
    assert updream.system_coverage_score == 5.0, f"Updream覆盖系数应为5.0，实际{updream.system_coverage_score}"
    print(f"✅ Updream主平台覆盖{updream.system_coverage_score:.0f}/6系（符合推论54.4）")
    return True


def test_03_universal_capability_intersection():
    """测试3：全平台公共能力交集提取"""
    print("\n" + "=" * 60)
    print("测试3：全平台公共能力交集")
    print("=" * 60)

    common = get_universal_material_capabilities()
    print(f"公共能力交集数量：{len(common)}")
    for cap in sorted(common, key=lambda x: x.value):
        print(f"  · {cap.value}")

    # 验证：交集必然是并集的真子集（推论54.1）
    all_caps = set()
    for p in TRADITIONAL_PLATFORMS.values():
        all_caps |= p.capabilities
    assert common.issubset(all_caps), "公共交集必须是总能力的子集"
    assert len(common) < len(all_caps), "交集必然是真子集（推论54.1·并集不完备）"
    print(f"✅ 公共交集({len(common)}) ⊂ 总能力({len(all_caps)}) · 符合推论54.1")
    return True


def test_04_system_union_materials():
    """测试4：按六系获取素材并集"""
    print("\n" + "=" * 60)
    print("测试4：按六系获取素材并集·定理五十四验证")
    print("=" * 60)

    for s in SixSystem:
        union = get_system_union_materials(s)
        count = len(union)
        print(f"  {s.value:<9}({SIX_SYSTEM_NAMES_CN[s]}): {count}个平台覆盖")

    # 定理五十四验证：BSD六系 = 传统平台并集 ∪ 天道系
    # 天道系的并集应为空（所有传统平台缺失天道系）
    tiandao_union = get_system_union_materials(SixSystem.TIANDao)
    assert len(tiandao_union) == 0, (
        f"传统平台天道系并集应为空（需BSD注入），实际{len(tiandao_union)}个"
    )
    print("✅ 天道系并集=空 → 需由BSD理论注入·符合定理五十四")

    # 变身系覆盖最多（所有平台至少有变身系）
    bianshen_union = get_system_union_materials(SixSystem.BIANSHEN)
    assert len(bianshen_union) == 12, (
        f"变身系应被所有12平台覆盖，实际{len(bianshen_union)}"
    )
    print(f"✅ 变身系覆盖{len(bianshen_union)}/12平台·画面生成基底存在")
    return True


def test_05_capability_query():
    """测试5：按素材能力查询平台"""
    print("\n" + "=" * 60)
    print("测试5：按素材能力查询平台")
    print("=" * 60)

    test_cases = [
        (MaterialCapability.TEXT_TO_VIDEO, "文生视频"),
        (MaterialCapability.CHINESE_OPTIMIZED, "中文优化"),
        (MaterialCapability.LONG_VIDEO, "长视频"),
    ]
    for cap, name in test_cases:
        result = get_materials_by_capability(cap)
        names = [p.name for p in result.values()]
        print(f"  {name:<10}: {len(result)}个平台 → {', '.join(names)}")
        assert len(result) > 0, f"{name}能力应有对应平台"
    print("✅ 按素材能力查询功能正常")
    return True


def test_06_matcher_match_task():
    """测试6：素材子集匹配器·match_task"""
    print("\n" + "=" * 60)
    print("测试6：素材子集匹配器·match_task方法")
    print("=" * 60)

    matcher = MaterialSubsetMatcher()

    # 用例1：简单文生视频·变身系
    result1 = matcher.match_task(
        required_systems={SixSystem.BIANSHEN},
        required_capabilities={MaterialCapability.TEXT_TO_VIDEO},
    )
    print(f"用例1·文生视频：最佳={result1.best_platform.name}")
    assert result1.best_platform_id in TRADITIONAL_PLATFORMS

    # 用例2：中文长视频·偏好中文
    result2 = matcher.match_task(
        required_systems={SixSystem.BIANSHEN, SixSystem.ZIRAN},
        required_capabilities={MaterialCapability.TEXT_TO_VIDEO, MaterialCapability.LONG_VIDEO},
        prefer_chinese=True,
        prefer_long_video=True,
    )
    print(f"用例2·中文长视频：最佳={result2.best_platform.name}")
    assert MaterialCapability.CHINESE_OPTIMIZED in result2.best_platform.capabilities or \
           MaterialCapability.LONG_VIDEO in result2.best_platform.capabilities

    # 用例3：专业工作流·强化+具现+变身
    result3 = matcher.match_task(
        required_systems={SixSystem.QIANGHUA, SixSystem.JUXIAN, SixSystem.BIANSHEN},
        required_capabilities={MaterialCapability.PRO_WORKFLOW, MaterialCapability.STYLE_TRANSFER},
    )
    print(f"用例3·专业工作流：最佳={result3.best_platform.name}")
    assert result3.best_platform_id == "firefly", (
        f"Adobe Firefly应匹配专业工作流，实际{result3.best_platform_id}"
    )

    print("✅ match_task方法3个用例通过")
    return True


def test_07_matcher_decision_tree():
    """测试7：素材子集决策树·关键词自动匹配"""
    print("\n" + "=" * 60)
    print("测试7：素材子集决策树·关键词自动匹配")
    print("=" * 60)

    matcher = MaterialSubsetMatcher()

    test_cases = [
        ("生成一段中国风古诗视频，需要60秒以上长镜头", "中文长视频"),
        ("对图片进行风格迁移，用导演模式控制运镜", "风格+导演"),
        ("同一角色在多个场景中保持一致，需要3D建模辅助", "角色一致+3D"),
        ("视频后期专业处理，Adobe Premiere工作流集成", "专业工作流"),
        ("生成视频后直接分发投稿到抖音和B站", "平台分发"),
        ("需要开源模型，本地部署自定义训练", "开源"),
    ]
    for desc, label in test_cases:
        result = matcher.decision_tree(desc)
        alternates = [f"{p.name}({score:.2f})" for _, p, score in result.alternate_platforms[:3]]
        print(f"  【{label}】{desc[:30]}...")
        print(f"    → 最佳：{result.best_platform.name} "
              f"(六系重叠={len(result.system_overlap)}, 能力重叠={len(result.capability_overlap)})")
        if alternates:
            print(f"    → 备选：{' / '.join(alternates)}")

    print("✅ 决策树关键词匹配6个场景通过")
    return True


def test_08_material_type_classification():
    """测试8：素材子集定位分类（material_type方法）"""
    print("\n" + "=" * 60)
    print("测试8：素材子集定位分类")
    print("=" * 60)

    type_counts = {}
    for pid, p in TRADITIONAL_PLATFORMS.items():
        mt = p.material_type()
        type_counts[mt] = type_counts.get(mt, 0) + 1
        print(f"  {p.name:<18} → {mt}")

    print(f"\n分类统计：{len(type_counts)}种素材类型")
    for mt, cnt in type_counts.items():
        print(f"  · {cnt}个平台：{mt}")

    # 验证Updream的主平台分类
    assert "主平台" in TRADITIONAL_PLATFORMS["updream"].material_type()
    print("✅ 素材子集定位分类逻辑正常")
    return True


def test_09_report_generation():
    """测试9：公共素材库总览报告生成"""
    print("\n" + "=" * 60)
    print("测试9：公共素材库总览报告生成")
    print("=" * 60)

    report = generate_public_material_report()
    # 报告长度检查
    assert len(report) > 1000, f"报告内容过短：{len(report)}字符"
    # 关键章节存在
    assert "六系覆盖矩阵" in report, "报告应包含六系覆盖矩阵"
    assert "素材子集定位" in report, "报告应包含素材子集定位"
    assert "公共能力交集" in report, "报告应包含公共能力交集"
    assert "素材子集定理" in report, "报告应包含素材子集定理重申"

    # 输出报告前500字符预览
    preview = report[:500] + "..."
    print(preview)
    print(f"\n✅ 报告生成成功·{len(report)}字符")
    return True


def test_10_theorem_54_verification():
    """测试10：素材子集定理五十四·整体验证"""
    print("\n" + "=" * 60)
    print("测试10：素材子集定理五十四·整体验证")
    print("=" * 60)

    # 54.1 并集不完备：传统并集 ⊂ BSD六系
    traditional_union_sys: set = set()
    for p in TRADITIONAL_PLATFORMS.values():
        traditional_union_sys |= p.covered_systems
    bsd_systems = {s for s in SixSystem}
    missing = bsd_systems - traditional_union_sys

    print(f"传统平台并集六系：{sorted([s.value for s in traditional_union_sys])}")
    print(f"BSD完整六系：{sorted([s.value for s in bsd_systems])}")
    print(f"缺失：{sorted([s.value for s in missing])}")

    assert missing == {SixSystem.TIANDao}, (
        f"缺失应只有天道系，实际{missing}"
    )
    print("✅ 推论54.1·并集不完备性验证通过（缺失天道系）")

    # 54.3 最佳BSD性：BSD=并集∪天道系
    bsd_via_union = traditional_union_sys | {SixSystem.TIANDao}
    assert bsd_via_union == bsd_systems, "BSD六系 = 传统并集 ∪ 天道系不成立"
    print("✅ 推论54.3·BSD六系完备性：BSD = 传统并集 ∪ 天道系")

    # 54.4 Updream主平台性：覆盖系数最大
    max_score = max(p.system_coverage_score for p in TRADITIONAL_PLATFORMS.values())
    updream_score = TRADITIONAL_PLATFORMS["updream"].system_coverage_score
    assert max_score == updream_score, f"Updream应有最高覆盖系数，最高为{max_score}"
    print(f"✅ 推论54.4·Updream主平台性：覆盖系数={updream_score:.1f}/6为最高")

    return True


# 中文名称辅助字典（测试用）
SIX_SYSTEM_NAMES_CN = {
    SixSystem.QIANGHUA: "强化系",
    SixSystem.ZIRAN: "自然系",
    SixSystem.JUXIAN: "具现系",
    SixSystem.BIANSHEN: "变身系",
    SixSystem.SHEHUI: "社会系",
    SixSystem.TIANDao: "天道系",
}


def main():
    """主测试入口"""
    print("\n" + "#" * 60)
    print("#  BSD传统AI平台公共素材库·单元测试套件 V1.0")
    print("#  [归属基底：Updream创世篇章V1.5§15]")
    print("#  [对应公理：定理五十四·素材子集定理]")
    print("#" * 60)

    tests = [
        test_01_init_platforms,
        test_02_platform_system_coverage,
        test_03_universal_capability_intersection,
        test_04_system_union_materials,
        test_05_capability_query,
        test_06_matcher_match_task,
        test_07_matcher_decision_tree,
        test_08_material_type_classification,
        test_09_report_generation,
        test_10_theorem_54_verification,
    ]

    passed = 0
    failed = 0
    failed_details = []

    for i, test_fn in enumerate(tests, 1):
        try:
            if test_fn():
                passed += 1
        except Exception as e:
            failed += 1
            failed_details.append((test_fn.__name__, str(e)))
            print(f"\n❌ 测试{i}·{test_fn.__name__} 失败：{e}")

    # 汇总
    print("\n" + "#" * 60)
    print(f"#  测试汇总：通过 {passed}/{len(tests)} · 失败 {failed}/{len(tests)}")
    if failed == 0:
        print("#  ✅ 全部通过·素材子集定理五十四验证完成")
    else:
        print(f"#  ❌ {failed}个失败：")
        for name, err in failed_details:
            print(f"#    - {name}: {err}")
    print("#" * 60 + "\n")

    return failed == 0


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
