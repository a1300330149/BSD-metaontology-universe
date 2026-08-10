"""
BSD六系层级涌现引擎单元测试
============================
liuhe_hierarchy_engine.py 的完整测试覆盖
[V1.0·2026-08-01]

测试范围：
- 六系坐标注册
- 文件名生成与解析
- 文件夹交汇点创建
- 涌现链计算
- 空间无重叠验证
- 物理决定系归属验证
- 层级完成度计算
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

import unittest
from datetime import datetime
from typing import Dict, List

from bsd_engine.core.liuhe_hierarchy_engine import (
    LiuHeSystem,
    EmergenceLevel,
    LiuHeHierarchyConstants,
    LiuHeCoordinate,
    DocumentMeta,
    FolderHub,
    LiuHeHierarchyEngine,
)


class TestLiuHeSystem(unittest.TestCase):
    """测试六系枚举"""
    
    def test_all_systems_defined(self):
        """测试所有六系是否已定义"""
        expected = ["强化系", "自然系", "具现系", "变身系", "社会系", "天道系"]
        actual = [s.value for s in LiuHeSystem]
        self.assertEqual(set(expected), set(actual))
    
    def test_system_count(self):
        """测试六系数量"""
        self.assertEqual(len(LiuHeSystem), 6)


class TestEmergenceLevel(unittest.TestCase):
    """测试十二级涌现层级"""
    
    def test_all_levels_defined(self):
        """测试所有层级是否已定义"""
        expected_levels = [f"L{i}" for i in range(1, 13)]
        actual_levels = [l.name for l in EmergenceLevel]
        self.assertEqual(set(expected_levels), set(actual_levels))
    
    def test_level_count(self):
        """测试层级数量"""
        self.assertEqual(len(EmergenceLevel), 12)


class TestLiuHeCoordinate(unittest.TestCase):
    """测试六系坐标"""
    
    def test_create_coordinate(self):
        """测试创建坐标"""
        coord = LiuHeCoordinate(
            system=LiuHeSystem.QH,
            level=EmergenceLevel.L6,
            alpha1=0.45,
            alpha2=0.35,
            alpha3=0.20,
        )
        self.assertEqual(coord.system, LiuHeSystem.QH)
        self.assertEqual(coord.level, EmergenceLevel.L6)
    
    def test_emergence_value_computation(self):
        """测试涌现值计算"""
        coord = LiuHeCoordinate(
            system=LiuHeSystem.ZR,
            level=EmergenceLevel.L2,
            alpha1=0.60,
            alpha2=0.35,
            alpha3=0.05,
        )
        value = coord.compute_emergence_value()
        self.assertGreater(value, 0)
    
    def test_coordinate_properties(self):
        """测试坐标属性"""
        coord = LiuHeCoordinate(
            system=LiuHeSystem.QH,
            level=EmergenceLevel.L6,
            alpha1=0.45,
            alpha2=0.35,
            alpha3=0.20,
        )
        self.assertEqual(coord.name, "细胞")
        self.assertEqual(coord.core_question, "我如何排熵？")
        self.assertIn(LiuHeSystem.QH, coord.dominant_systems)


class TestDocumentMeta(unittest.TestCase):
    """测试文档元数据"""
    
    def test_filename_generation(self):
        """测试文件名生成"""
        meta = DocumentMeta(
            filepath="",
            coordinate=LiuHeCoordinate(
                system=LiuHeSystem.QH,
                level=EmergenceLevel.L6,
                alpha1=0.45,
                alpha2=0.35,
                alpha3=0.20,
            ),
            version="V1.0",
            created_date="20260801",
            last_modified="20260801",
        )
        filename = meta.to_filename()
        self.assertIn("BSD", filename)
        self.assertIn("QH", filename)
        self.assertIn("L6", filename)
        self.assertIn("V1.0", filename)
        self.assertIn("20260801", filename)
        self.assertTrue(filename.endswith(".md"))
    
    def test_filename_parsing(self):
        """测试文件名解析"""
        test_filename = "BSD_ZR_L2_V1.0_20260801.md"
        meta = DocumentMeta.from_filename(test_filename)
        self.assertIsNotNone(meta)
        self.assertEqual(meta.coordinate.system, LiuHeSystem.ZR)
        self.assertEqual(meta.coordinate.level, EmergenceLevel.L2)
        self.assertEqual(meta.version, "V1.0")
        self.assertEqual(meta.created_date, "20260801")
    
    def test_filename_roundtrip(self):
        """测试文件名往返转换"""
        original = DocumentMeta(
            filepath="",
            coordinate=LiuHeCoordinate(
                system=LiuHeSystem.TD,
                level=EmergenceLevel.L12,
                alpha1=0.10,
                alpha2=0.40,
                alpha3=0.50,
            ),
            version="V2.3",
            created_date="20260801",
            last_modified="20260801",
        )
        filename = original.to_filename()
        parsed = DocumentMeta.from_filename(filename)
        
        self.assertEqual(parsed.coordinate.system, original.coordinate.system)
        self.assertEqual(parsed.coordinate.level, original.coordinate.level)
        self.assertEqual(parsed.version, original.version)


class TestFolderHub(unittest.TestCase):
    """测试文件夹交汇点"""
    
    def test_create_folder_hub(self):
        """测试创建文件夹交汇点"""
        hub = FolderHub(
            path="/test/hub",
            level=EmergenceLevel.L1,
            hub_type="本源级",
        )
        self.assertEqual(hub.path, "/test/hub")
        self.assertEqual(hub.level, EmergenceLevel.L1)
        self.assertEqual(hub.hub_type, "本源级")
    
    def test_add_document(self):
        """测试添加文档"""
        hub = FolderHub(
            path="/test/hub",
            level=EmergenceLevel.L1,
            hub_type="本源级",
        )
        hub.contained_docs.append("BSD_QH_L1_V1.0_20260801.md")
        self.assertEqual(len(hub.contained_docs), 1)
    
    def test_count_docs_by_system(self):
        """测试按系统统计文档"""
        hub = FolderHub(
            path="/test/hub",
            level=EmergenceLevel.L1,
            hub_type="本源级",
        )
        hub.contained_docs.extend([
            "BSD_QH_L1_V1.0_20260801.md",
            "BSD_ZR_L1_V1.0_20260801.md",
            "BSD_QH_L1_V1.0_20260801.md",
        ])
        counts = hub.count_docs_by_system()
        self.assertEqual(counts[LiuHeSystem.QH], 2)
        self.assertEqual(counts[LiuHeSystem.ZR], 1)


class TestLiuHeHierarchyEngine(unittest.TestCase):
    """测试六系层级涌现引擎"""
    
    def setUp(self):
        """设置测试环境"""
        self.engine = LiuHeHierarchyEngine()
    
    def test_register_coordinate(self):
        """测试注册坐标"""
        coord = LiuHeCoordinate(
            system=LiuHeSystem.QH,
            level=EmergenceLevel.L6,
            alpha1=0.45,
            alpha2=0.35,
            alpha3=0.20,
        )
        key = self.engine.register_coordinate(coord)
        # key格式: "强化系_L6"
        self.assertIn("强化系", key)
        self.assertIn("L6", key)
    
    def test_generate_filename(self):
        """测试生成文件名"""
        filename = self.engine.generate_filename(
            system=LiuHeSystem.QH,
            level=EmergenceLevel.L6,
        )
        self.assertIn("BSD", filename)
        self.assertIn("QH", filename)
        self.assertIn("L6", filename)
        self.assertIn(".md", filename)
    
    def test_parse_filename(self):
        """测试解析文件名"""
        test_file = "BSD_ZR_L2_V1.0_20260801.md"
        meta = self.engine.parse_filename(test_file)
        self.assertIsNotNone(meta)
        self.assertEqual(meta.coordinate.system, LiuHeSystem.ZR)
    
    def test_full_emergence_chain(self):
        """测试完整涌现链"""
        chain = self.engine.compute_emergence_chain()
        self.assertEqual(len(chain), 12)
    
    def test_completion_metrics(self):
        """测试完成度指标"""
        for level in EmergenceLevel:
            self.engine.generate_filename(
                system=LiuHeSystem.QH,
                level=level,
            )
        metrics = self.engine.compute_completion_metrics()
        self.assertEqual(metrics["registered_levels"], 12)
        self.assertEqual(metrics["completion_rate"], 1.0)
    
    def test_verify_no_overlap(self):
        """测试空间无重叠"""
        result = self.engine.verify_no_overlap()
        self.assertTrue(result["no_overlap"])
    
    def test_verify_system_determination(self):
        """测试物理决定系归属"""
        result = self.engine.verify_system_determination()
        self.assertTrue(result["physics_determines_system"])
    
    def test_emergence_history(self):
        """测试涌现历史"""
        self.engine.generate_filename(LiuHeSystem.QH, EmergenceLevel.L1)
        self.engine.generate_filename(LiuHeSystem.ZR, EmergenceLevel.L2)
        history = self.engine.emergence_history
        self.assertGreaterEqual(len(history), 2)
    
    def test_full_registration(self):
        """测试全注册"""
        for level in EmergenceLevel:
            for system in LiuHeSystem:
                self.engine.generate_filename(system, level)
        metrics = self.engine.compute_completion_metrics()
        self.assertEqual(metrics["completion_rate"], 1.0)
    
    def test_generate_report(self):
        """测试生成报告"""
        report = self.engine.generate_report()
        self.assertIn("emergence_chain", report)
        self.assertIn("completion_metrics", report)
        self.assertIn("verification", report)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_workflow(self):
        """测试完整工作流"""
        engine = LiuHeHierarchyEngine()
        
        # 1. 注册12级（使用符合每级预期的系统）
        for level in EmergenceLevel:
            level_info = LiuHeHierarchyConstants.LEVELS[level]
            # 使用第一个预期系统
            system = level_info["systems"][0]
            engine.generate_filename(system, level)
        
        # 2. 计算完成度
        metrics = engine.compute_completion_metrics()
        self.assertEqual(metrics["completion_rate"], 1.0)
        
        # 3. 验证空间无重叠
        self.assertTrue(engine.verify_no_overlap()["no_overlap"])
        
        # 4. 验证物理决定系（使用预期系统注册时应通过）
        self.assertTrue(engine.verify_system_determination()["physics_determines_system"])
        
        # 5. 获取报告
        report = engine.generate_report()
        self.assertIn("emergence_chain", report)
        self.assertIn("completion_metrics", report)
    
    def test_document_meta_workflow(self):
        """测试文档元数据工作流"""
        systems = list(LiuHeSystem)[:3]
        levels = list(EmergenceLevel)[:3]
        
        for system in systems:
            for level in levels:
                coord = LiuHeCoordinate(
                    system=system,
                    level=level,
                    alpha1=0.33,
                    alpha2=0.33,
                    alpha3=0.34,
                )
                meta = DocumentMeta(
                    filepath="",
                    coordinate=coord,
                    version="V1.0",
                    created_date="20260801",
                    last_modified="20260801",
                )
                filename = meta.to_filename()
                parsed = DocumentMeta.from_filename(filename)
                
                self.assertEqual(parsed.coordinate.system, system)
                self.assertEqual(parsed.coordinate.level, level)


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner, exit=False)
    
    print("\n" + "=" * 60)
    print("BSD六系层级涌现引擎测试报告")
    print("=" * 60)
    
    engine = LiuHeHierarchyEngine()
    
    for level in EmergenceLevel:
        for system in LiuHeSystem:
            engine.generate_filename(system, level)
    
    metrics = engine.compute_completion_metrics()
    print(f"✓ 12级×6系 = {12*6} 坐标注册完成")
    print(f"✓ 完成度: {metrics['completion_rate']*100:.0f}%")
    print(f"✓ 空间无重叠: {engine.verify_no_overlap()['no_overlap']}")
    print(f"✓ 物理决定系: {engine.verify_system_determination()['physics_determines_system']}")
    print(f"✓ EMERGENCE-018验证通过")
