#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 批量引擎生成管道
====================

整合系统：
  1. 双时针（逆时针理论→引擎 + 顺时针引擎→理论）
  2. 三引擎涌现（基因×黑客×围棋 的权重动态平衡）
  3. 理论落地系统（扫描→映射→欠债→生成→连接→激活→验证）

核心流程：
  Step 0: 环境准备
  Step 1: 理论扫描（扫描 theory_base）
  Step 2: 引擎映射与欠债检测
  Step 3: 权重涌现计算（三引擎竞技场）
  Step 4: 批量代码生成（融合权重分布）
  Step 5: 连接激活验证
  Step 6: 生成报告

版本：V1.0 · 2026-08-05
"""

import sys
import os
import json
import time
import traceback
from datetime import datetime
from typing import Dict, List, Any, Optional

# ============================================================
# 路径设置
# ============================================================
_PHYSICAL_PATH = os.path.dirname(os.path.abspath(__file__))
_BSD_OAPS_PATH = os.path.dirname(_PHYSICAL_PATH)
_AGENT_V2_PATH = os.path.dirname(_BSD_OAPS_PATH)  # Agent_v2 目录
sys.path.insert(0, _BSD_OAPS_PATH)
sys.path.insert(0, _PHYSICAL_PATH)

os.chdir(_BSD_OAPS_PATH)

# 修正路径：theory_base 在 Agent_v2 下，不在 bsd-oaps 下
_THEORY_BASE_PATH = os.path.join(_AGENT_V2_PATH, 'theory_base')
_BSD_ENGINE_PATH = os.path.join(_BSD_OAPS_PATH, 'bsd_engine')


class BSDBatchEngineGenerator:
    """BSD批量引擎生成管道
    
    整合双时针系统与三引擎涌现，实现理论到引擎的批量转化。
    """
    
    def __init__(self):
        # 组件
        self.landing_system = None
        self.emergence_engine = None
        
        # 结果
        self.generation_report = {}
        self.start_time = None
        self.end_time = None
        
        # 统计
        self.stats = {
            'theories_scanned': 0,
            'debts_identified': 0,
            'engines_generated': 0,
            'engines_verified': 0,
            'generation_time': 0,
        }
    
    def run_pipeline(self, 
                     scan_files: int = 500,
                     max_engines: int = 50,
                     use_emergence: bool = True) -> Dict[str, Any]:
        """运行完整的批量生成管道
        
        Args:
            scan_files: 最大扫描理论文件数
            max_engines: 最大生成引擎数
            use_emergence: 是否使用三引擎涌现计算权重
        
        Returns:
            完整生成报告
        """
        self.start_time = datetime.now()
        
        print("=" * 70)
        print("【BSD 批量引擎生成管道 V1.0】")
        print(f"  启动时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  扫描上限: {scan_files} 理论文件")
        print(f"  生成上限: {max_engines} 引擎")
        print(f"  权重涌现: {'启用' if use_emergence else '禁用'}")
        print("=" * 70)
        
        try:
            # Step 0: 环境准备
            self._step0_prepare()
            
            # Step 1: 理论扫描
            self._step1_scan(scan_files)
            
            # Step 2: 引擎映射与欠债检测
            self._step2_map_and_debt()
            
            # Step 3: 权重涌现计算
            emergence_weights = None
            if use_emergence:
                emergence_weights = self._step3_emergence()
            
            # Step 4: 批量代码生成
            self._step4_generate(max_engines, emergence_weights)
            
            # Step 5: 连接激活验证
            self._step5_verify()
            
            # Step 6: 生成报告
            report = self._step6_report(emergence_weights)
            
            return report
            
        except Exception as e:
            error_report = {
                'status': 'failed',
                'error': str(e),
                'traceback': traceback.format_exc(),
                'partial_stats': self.stats,
            }
            print(f"\n  ❌ 管道执行失败: {e}")
            traceback.print_exc()
            return error_report
    
    def _step0_prepare(self):
        """Step 0: 环境准备"""
        print("\n【Step 0】环境准备")
        
        # 检查 theory_base（使用修正后的路径）
        theory_path = _THEORY_BASE_PATH
        if not os.path.isdir(theory_path):
            # 回退：尝试其他可能的位置
            alt_paths = [
                os.path.join(_BSD_OAPS_PATH, 'theory_base'),
                os.path.join(_AGENT_V2_PATH, 'theory_base'),
            ]
            for alt in alt_paths:
                if os.path.isdir(alt):
                    theory_path = alt
                    break
        
        if not os.path.isdir(theory_path):
            raise RuntimeError(f"theory_base 不存在，尝试路径: {_THEORY_BASE_PATH}")
        
        # 同时修正 theory_landing_system 中的路径
        import theory_landing_system
        theory_landing_system._THEORY_BASE_PATH = theory_path
        
        # 检查 bsd_engine
        engine_path = _BSD_ENGINE_PATH
        if not os.path.isdir(engine_path):
            raise RuntimeError(f"bsd_engine 不存在: {engine_path}")
        
        # 扫描现有引擎数量
        existing_engines = 0
        for root, dirs, files in os.walk(engine_path):
            for f in files:
                if f.endswith('.py') and not f.startswith('__'):
                    existing_engines += 1
        
        # 理论文件数量
        theory_files = 0
        for root, dirs, files in os.walk(theory_path):
            for f in files:
                if f.endswith('.py') or f.endswith('.md'):
                    theory_files += 1
        
        print(f"  ✅ theory_base: {theory_files} 理论文件")
        print(f"  ✅ bsd_engine: {existing_engines} 引擎文件")
        
        # 初始化理论落地系统
        from theory_landing_system import TheoryLandingSystem, LandingMode
        self.landing_system = TheoryLandingSystem(mode=LandingMode.FULL)
        print(f"  ✅ 理论落地系统已初始化")
    
    def _step1_scan(self, max_files: int):
        """Step 1: 理论扫描"""
        print("\n【Step 1】理论扫描")
        
        result = self.landing_system.stage_scan(max_files=max_files)
        self.stats['theories_scanned'] = result.get('scanned', 0)
        
        scanned = result.get('scanned', 0)
        skipped = result.get('skipped', 0)
        checked = result.get('checked', 0)
        
        print(f"  扫描完成: {scanned} 理论节点 (检查: {checked}, 跳过: {skipped})")
        
        # 层级分布
        layers = {}
        for node in self.landing_system.theory_nodes:
            layers[node.layer] = layers.get(node.layer, 0) + 1
        print(f"  层级分布: {layers}")
        
        # 六系分布
        systems = {}
        for node in self.landing_system.theory_nodes:
            sys_name = node.six_system[:6] if node.six_system else '未知'
            systems[sys_name] = systems.get(sys_name, 0) + 1
        print(f"  六系分布: {systems}")
    
    def _step2_map_and_debt(self):
        """Step 2: 引擎映射与欠债检测"""
        print("\n【Step 2】引擎映射与欠债检测")
        
        result = self.landing_system.stage_map_and_debt()
        
        landed = result.get('landed', 0)
        debts = result.get('debts', 0)
        targets = result.get('targets', 0)
        
        self.stats['debts_identified'] = debts
        
        print(f"  已落地理论: {landed}")
        print(f"  理论欠债: {debts}")
        print(f"  生成落地目标: {targets}")
        
        # 按欠债级别分类
        if self.landing_system.landing_targets:
            priority_dist = {}
            for t in self.landing_system.landing_targets:
                p = t.priority
                priority_dist[p] = priority_dist.get(p, 0) + 1
            print(f"  欠债级别分布: {priority_dist}")
    
    def _step3_emergence(self) -> Dict[str, Any]:
        """Step 3: 权重涌现计算"""
        print("\n【Step 3】三引擎权重涌现计算")
        
        try:
            from BSD_GeneHackerGo_EmergenceEngine import BSDEmergenceEngine
            
            engine = BSDEmergenceEngine()
            engine.initialize()
            emergence_report = engine.run_emergence(target_iterations=30)
            
            # 提取关键权重
            final_state = emergence_report.get('final_state', {})
            system_weights = emergence_report.get('system_weights', {})
            attractors = emergence_report.get('attractors', {})
            
            print(f"  α权重: α₁={final_state.get('alpha1', 0):.3f}, "
                  f"α₂={final_state.get('alpha2', 0):.3f}, "
                  f"α₃={final_state.get('alpha3', 0):.3f}")
            
            print(f"  六系权重:")
            for sys_name, weight in sorted(system_weights.items(), key=lambda x: -x[1]):
                bar = "█" * int(weight * 40)
                print(f"    {sys_name}: {weight:.4f} {bar}")
            
            print(f"  稳定性: {final_state.get('stability', 0):.4f}")
            
            return {
                'alpha1': final_state.get('alpha1', 0.33),
                'alpha2': final_state.get('alpha2', 0.33),
                'alpha3': final_state.get('alpha3', 0.34),
                'system_weights': system_weights,
                'attractors': attractors,
                'stability': final_state.get('stability', 0),
            }
            
        except Exception as e:
            print(f"  ⚠️ 权重涌现计算失败: {e}")
            print(f"  使用默认权重分布")
            return {
                'alpha1': 0.33,
                'alpha2': 0.33,
                'alpha3': 0.34,
                'system_weights': {},
                'attractors': {},
                'stability': 0,
            }
    
    def _step4_generate(self, max_engines: int, 
                         emergence_weights: Dict[str, Any] = None):
        """Step 4: 批量代码生成
        
        根据权重涌现结果调整生成优先级
        """
        print("\n【Step 4】批量代码生成")
        
        # 根据权重调整生成目标优先级
        if emergence_weights and emergence_weights.get('attractors'):
            attractors = emergence_weights['attractors']
            # 将六系吸引子映射到落地目标
            priority_boost = {}
            for sys_name, strength in attractors.items():
                if strength > 0.15:
                    priority_boost[sys_name] = 'CRITICAL'
                elif strength > 0.10:
                    priority_boost[sys_name] = 'HIGH'
            
            # 调整目标优先级
            for target in self.landing_system.landing_targets:
                sys_name = target.theory_node.six_system[:6]
                if sys_name in priority_boost:
                    if target.priority != 'CRITICAL':
                        target.priority = priority_boost[sys_name]
        
        # 限制生成数量
        targets_to_generate = self.landing_system.landing_targets[:max_engines]
        
        if len(targets_to_generate) < len(self.landing_system.landing_targets):
            print(f"  ⚠️ 目标数量({len(self.landing_system.landing_targets)})超过上限({max_engines})")
            print(f"  将仅生成前 {max_engines} 个引擎")
        
        # 执行生成
        self.landing_system.landing_targets = targets_to_generate
        result = self.landing_system.stage_generate()
        
        generated = result.get('generated', 0)
        failed = result.get('failed', 0)
        
        self.stats['engines_generated'] = generated
        
        print(f"  成功生成: {generated} 个引擎")
        print(f"  生成失败: {failed} 个")
        
        # 展示生成的引擎
        for r in self.landing_system.landing_results:
            if r['status'] == 'generated':
                eng_path = r.get('path', '')
                print(f"    ✅ {r['engine_name']}")
                print(f"       → {os.path.basename(os.path.dirname(eng_path))}/{os.path.basename(eng_path)}")
    
    def _step5_verify(self):
        """Step 5: 连接激活验证"""
        print("\n【Step 5】连接激活验证")
        
        result = self.landing_system.stage_connect_and_activate()
        
        connected = result.get('connected', 0)
        activated = result.get('activated', 0)
        verified = result.get('verified', 0)
        total = result.get('total', 0)
        
        self.stats['engines_verified'] = verified
        
        print(f"  连接通过: {connected}/{total}")
        print(f"  激活通过: {activated}/{connected}")
        print(f"  验证通过: {verified}/{activated}")
        
        # 展示验证失败的引擎
        failed_landings = [r for r in self.landing_system.landing_results 
                          if r['status'] not in ('landed', 'generated')]
        if failed_landings:
            print(f"\n  ⚠️ 验证详情:")
            for r in self.landing_system.landing_results:
                if r['status'] == 'landed':
                    print(f"    ✅ {r['engine_name']} → 落地成功")
                elif r['status'] == 'generated':
                    print(f"    ⚠️ {r['engine_name']} → 未通过连接")
                else:
                    print(f"    ❌ {r['engine_name']} → {r['status']}")
    
    def _step6_report(self, emergence_weights: Dict[str, Any] = None) -> Dict[str, Any]:
        """Step 6: 生成完整报告"""
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        self.stats['generation_time'] = duration
        
        print("\n" + "=" * 70)
        print("【批量引擎生成报告】")
        print("=" * 70)
        
        # 生成报告
        report = {
            'report_id': f"BATCH_{int(time.time())}",
            'timestamp': self.end_time.isoformat(),
            'duration_seconds': round(duration, 2),
            
            # 统计
            'statistics': {
                'theories_scanned': self.stats['theories_scanned'],
                'debts_identified': self.stats['debts_identified'],
                'engines_generated': self.stats['engines_generated'],
                'engines_verified': self.stats['engines_verified'],
                'verification_rate': (
                    round(self.stats['engines_verified'] / max(self.stats['engines_generated'], 1), 4)
                ),
            },
            
            # 权重涌现
            'emergence_weights': emergence_weights or {},
            
            # 生成的引擎清单
            'generated_engines': [],
            
            # 理论节点分布
            'theory_distribution': {
                'by_layer': {},
                'by_system': {},
            },
            
            # 引擎清单
            'engine_catalog': [],
        }
        
        # 引擎清单
        for r in self.landing_system.landing_results:
            if r['status'] in ('generated', 'landed'):
                report['engine_catalog'].append({
                    'engine_name': r['engine_name'],
                    'status': r['status'],
                    'path': r.get('path', ''),
                })
        
        # 理论分布
        for node in self.landing_system.theory_nodes:
            layer = node.layer
            report['theory_distribution']['by_layer'][layer] = \
                report['theory_distribution']['by_layer'].get(layer, 0) + 1
            
            sys_name = node.six_system[:6] if node.six_system else '未知'
            report['theory_distribution']['by_system'][sys_name] = \
                report['theory_distribution']['by_system'].get(sys_name, 0) + 1
        
        # 打印报告摘要
        print(f"\n  执行时间: {duration:.2f} 秒")
        print(f"  理论扫描: {self.stats['theories_scanned']} 节点")
        print(f"  理论欠债: {self.stats['debts_identified']}")
        print(f"  引擎生成: {self.stats['engines_generated']}")
        print(f"  验证通过: {self.stats['engines_verified']}")
        print(f"  验证率: {report['statistics']['verification_rate']:.2%}")
        
        print(f"\n  引擎清单 (前10个):")
        for eng in report['engine_catalog'][:10]:
            status_icon = "✅" if eng['status'] == 'landed' else "⚠️"
            print(f"    {status_icon} {eng['engine_name']} → {eng['status']}")
        
        # 保存报告
        report_path = os.path.join(
            _PHYSICAL_PATH,
            f'BSD_BatchEngineGeneration_Report_{int(time.time())}.json'
        )
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"\n  报告已保存: {report_path}")
        
        self.generation_report = report
        return report


# ============================================================================
# 启动
# ============================================================================

def main():
    """启动批量引擎生成"""
    
    generator = BSDBatchEngineGenerator()
    
    # 配置参数
    scan_files = 500     # 扫描500个理论文件
    max_engines = 50     # 最多生成50个引擎
    use_emergence = True  # 启用三引擎权重涌现
    
    # 运行管道
    report = generator.run_pipeline(
        scan_files=scan_files,
        max_engines=max_engines,
        use_emergence=use_emergence,
    )
    
    # 输出最终总结
    print("\n" + "=" * 70)
    print("【批量引擎生成 · 执行完成】")
    print("=" * 70)
    
    stats = report.get('statistics', {})
    print(f"""
  📊 核心数据:
     理论节点: {stats.get('theories_scanned', 0)}
     理论欠债: {stats.get('debts_identified', 0)}
     引擎生成: {stats.get('engines_generated', 0)}
     验证通过: {stats.get('engines_verified', 0)}
     验证率:   {stats.get('verification_rate', 0):.2%}

  🔗 双时针闭环:
     逆时针(理论→引擎): {stats.get('engines_generated', 0)} 个引擎已生成
     顺时针(引擎→理论): 映射关系已建立

  ⚖️ 三引擎权重:
     α₁(个体性): {report.get('emergence_weights', {}).get('alpha1', 0):.3f}
     α₂(关系性): {report.get('emergence_weights', {}).get('alpha2', 0):.3f}
     α₃(变化性): {report.get('emergence_weights', {}).get('alpha3', 0):.3f}

  📁 输出文件:
     报告: BSD_BatchEngineGeneration_Report_*.json
     引擎: bsd_engine/core/*.py
""")
    
    return report


if __name__ == '__main__':
    main()