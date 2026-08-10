#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD三元动力学基因解构引擎
============================
核心方程：
  ① α₁ + α₂ + α₃ = 1   （三元动力学公理：权重归一）
  ② 0.9̇ = 1             （意义一元本体：时间收敛极限）
  ③ Φ = α₁τ + α₂R + α₃C （存在稳态势能）
  ④ ΔΦ < 0              （自发演化判据）
  
三元映射：
  α₁(个体性/强化系) ← 文件结构、尺寸、稳定性
  α₂(关系性/具现系) ← 依赖关系、网络连接、拓扑耦合  
  α₃(变化性/变身系) ← 更新频率、版本迭代、演化潜力

健康态：α∈[0.30,0.40]，两权重差≤0.05
疾病态：Δα≥0.10（动态守恒失效，结构性破缺）
"""

import os
import json
import math
import hashlib
from datetime import datetime
from collections import defaultdict

class BSDGeneDeconstructor:
    """BSD三元动力学基因解构引擎"""
    
    def __init__(self):
        self.gene_map = {}
        self.deconstruction_results = []
        self.stats = {
            'total_genes': 0,
            'healthy_genes': 0,
            'subhealthy_genes': 0,
            'disease_genes': 0,
            'alpha1_avg': 0.0,
            'alpha2_avg': 0.0,
            'alpha3_avg': 0.0,
        }
    
    def scan_directory(self, path, max_depth=3, file_limit=5000):
        """扫描系统目录，提取基因"""
        genes = []
        count = 0
        
        for root, dirs, files in os.walk(path):
            depth = root.replace(path, '').count(os.sep)
            if depth >= max_depth:
                dirs.clear()
                continue
            
            for f in files:
                if count >= file_limit:
                    break
                try:
                    filepath = os.path.join(root, f)
                    size = os.path.getsize(filepath)
                    if size > 0:
                        genes.append({
                            'path': filepath,
                            'name': f,
                            'size': size,
                            'ext': os.path.splitext(f)[1].lower(),
                            'modified': os.path.getmtime(filepath),
                            'depth': depth,
                        })
                        count += 1
                except (OSError, PermissionError):
                    continue
            if count >= file_limit:
                break
        
        return genes
    
    def compute_alpha_components(self, gene):
        """
        计算三元动力学分量 α₁, α₂, α₃
        
        α₁ (个体性/强化系)：
          - 文件尺寸占比（结构承载性）
          - 文件类型稳定性（系统文件>临时文件）
          - 目录深度（核心层>边缘层）
        
        α₂ (关系性/具现系)：
          - 文件扩展名关联度（dll/exe>txt/log）
          - 所在目录的连接度
          - 依赖网络的拓扑位置
        
        α₃ (变化性/变身系)：
          - 修改时间的新近程度
          - 文件类型的演化性（配置文件>可执行文件）
          - 版本迭代频率
        """
        size = gene['size']
        ext = gene['ext']
        modified = gene['modified']
        depth = gene['depth']
        name = gene['name'].lower()
        
        # 计算 α₁ (个体性/强化系)
        size_score = min(size / (1024 * 1024 * 100), 1.0)  # 归一到100MB
        stability_score = self._compute_stability(ext, name)
        depth_score = max(0.1, 1.0 - depth * 0.2)  # 核心层更高
        alpha1_raw = 0.4 * size_score + 0.3 * stability_score + 0.3 * depth_score
        
        # 计算 α₂ (关系性/具现系)
        coupling_score = self._compute_coupling(ext, name)
        network_score = self._compute_network_position(name, ext)
        alpha2_raw = 0.5 * coupling_score + 0.5 * network_score
        
        # 计算 α₃ (变化性/变身系)
        recency = self._compute_recency(modified)
        evolution_score = self._compute_evolution_potential(ext, name)
        alpha3_raw = 0.4 * recency + 0.6 * evolution_score
        
        # 三元归一化：α₁ + α₂ + α₃ = 1
        total = alpha1_raw + alpha2_raw + alpha3_raw
        if total > 0:
            alpha1 = alpha1_raw / total
            alpha2 = alpha2_raw / total
            alpha3 = alpha3_raw / total
        else:
            alpha1 = alpha2 = alpha3 = 1/3
        
        return {
            'alpha1': round(alpha1, 4),
            'alpha2': round(alpha2, 4),
            'alpha3': round(alpha3, 4),
            'alpha_sum': round(alpha1 + alpha2 + alpha3, 4),
            'raw_components': {
                'alpha1_raw': round(alpha1_raw, 4),
                'alpha2_raw': round(alpha2_raw, 4),
                'alpha3_raw': round(alpha3_raw, 4),
            }
        }
    
    def _compute_stability(self, ext, name):
        """计算文件稳定性（系统核心>临时文件）"""
        stable_extensions = {'.dll', '.exe', '.sys', '.ini', '.cfg', '.dat', '.db'}
        unstable_extensions = {'.tmp', '.log', '.bak', '.cache', '.crdownload'}
        
        if ext in stable_extensions:
            return 0.9
        elif ext in unstable_extensions:
            return 0.1
        elif 'system' in name or 'config' in name or 'driver' in name:
            return 0.8
        else:
            return 0.4
    
    def _compute_coupling(self, ext, name):
        """计算关系耦合度"""
        high_coupling = {'.dll', '.exe', '.ocx', '.tlb'}
        medium_coupling = {'.ini', '.cfg', '.xml', '.json', '.dat'}
        low_coupling = {'.txt', '.log', '.md', '.html', '.css'}
        
        if ext in high_coupling:
            return 0.9
        elif ext in medium_coupling:
            return 0.6
        elif ext in low_coupling:
            return 0.3
        else:
            return 0.2
    
    def _compute_network_position(self, name, ext):
        """计算网络拓扑位置"""
        name_lower = name.lower()
        if 'api' in name_lower or 'service' in name_lower or 'server' in name_lower:
            return 0.9
        elif 'client' in name_lower or 'ui' in name_lower or 'view' in name_lower:
            return 0.6
        elif 'core' in name_lower or 'engine' in name_lower or 'kernel' in name_lower:
            return 0.8
        else:
            return 0.3
    
    def _compute_recency(self, modified_time):
        """计算时间新近度"""
        now = datetime.now().timestamp()
        age_days = (now - modified_time) / 86400
        
        if age_days < 1:
            return 1.0
        elif age_days < 7:
            return 0.8
        elif age_days < 30:
            return 0.6
        elif age_days < 365:
            return 0.4
        else:
            return 0.1
    
    def _compute_evolution_potential(self, ext, name):
        """计算演化潜力"""
        high_evolution = {'.py', '.js', '.ts', '.json', '.xml', '.html', '.css'}
        medium_evolution = {'.exe', '.dll', '.dat', '.db'}
        low_evolution = {'.sys', '.ini', '.cfg'}
        
        if ext in high_evolution:
            return 0.9
        elif ext in medium_evolution:
            return 0.5
        elif ext in low_evolution:
            return 0.2
        else:
            return 0.3
    
    def compute_potential_energy(self, alpha1, alpha2, alpha3, tau=1.0, r=1.0, c=1.0):
        """
        存在稳态势能：Φ = α₁τ + α₂R + α₃C
        
        τ (tau): 结构稳态指标
        R (R): 关系耦合指标
        C (C): 演化潜力指标
        """
        phi = alpha1 * tau + alpha2 * r + alpha3 * c
        return round(phi, 6)
    
    def compute_evolution_criterion(self, phi_old, phi_new):
        """自发演化判据：ΔΦ < 0 时系统自发演化"""
        delta_phi = phi_new - phi_old
        return {
            'delta_phi': round(delta_phi, 6),
            'spontaneous': delta_phi < 0,
            'direction': '演化' if delta_phi < 0 else '稳定',
        }
    
    def diagnose_gene_state(self, alpha1, alpha2, alpha3):
        """
        基因状态诊断
        
        健康态：α∈[0.30,0.40]，两权重差≤0.05
        亚健康态：0.05<Δα<0.10（可逆偏移）
        疾病态：Δα≥0.10（动态守恒失效）
        """
        alphas = [alpha1, alpha2, alpha3]
        alpha_max = max(alphas)
        alpha_min = min(alphas)
        delta_alpha = alpha_max - alpha_min
        
        # 健康态：三权重均衡
        if all(0.30 <= a <= 0.40 for a in alphas) and delta_alpha <= 0.05:
            state = '健康态'
            health_score = 1.0
        # 亚健康态：可逆偏移
        elif delta_alpha < 0.10:
            state = '亚健康态'
            health_score = 0.6 - delta_alpha * 4
        # 疾病态：结构性破缺
        else:
            state = '疾病态'
            health_score = max(0, 0.4 - delta_alpha * 2)
        
        # 特定状态判定
        if alpha1 >= 0.6:
            subtype = '结构固化型（强化系过度主导）'
        elif alpha2 >= 0.55:
            subtype = '关系过载型（具现系过度耦合）'
        elif alpha3 >= 0.45:
            subtype = '演化活跃型（变身系主导，可能不稳定）'
        else:
            subtype = '均衡型'
        
        return {
            'state': state,
            'subtype': subtype,
            'health_score': round(health_score, 4),
            'delta_alpha': round(delta_alpha, 4),
            'balanced': delta_alpha <= 0.05,
        }
    
    def deconstruct_genes(self, genes):
        """对基因群进行三元动力学解构"""
        results = []
        sum_a1 = sum_a2 = sum_a3 = 0
        
        for gene in genes:
            # 三元动力学分析
            alpha_comp = self.compute_alpha_components(gene)
            
            # 势能计算
            phi = self.compute_potential_energy(
                alpha_comp['alpha1'],
                alpha_comp['alpha2'],
                alpha_comp['alpha3']
            )
            
            # 状态诊断
            diagnosis = self.diagnose_gene_state(
                alpha_comp['alpha1'],
                alpha_comp['alpha2'],
                alpha_comp['alpha3']
            )
            
            result = {
                'gene': gene['name'],
                'path': gene['path'],
                'size': gene['size'],
                'alpha1': alpha_comp['alpha1'],
                'alpha2': alpha_comp['alpha2'],
                'alpha3': alpha_comp['alpha3'],
                'alpha_sum': alpha_comp['alpha_sum'],
                'phi': phi,
                'state': diagnosis['state'],
                'subtype': diagnosis['subtype'],
                'health_score': diagnosis['health_score'],
                'delta_alpha': diagnosis['delta_alpha'],
            }
            
            results.append(result)
            sum_a1 += alpha_comp['alpha1']
            sum_a2 += alpha_comp['alpha2']
            sum_a3 += alpha_comp['alpha3']
        
        n = len(results)
        if n > 0:
            self.stats.update({
                'total_genes': n,
                'healthy_genes': sum(1 for r in results if r['state'] == '健康态'),
                'subhealthy_genes': sum(1 for r in results if r['state'] == '亚健康态'),
                'disease_genes': sum(1 for r in results if r['state'] == '疾病态'),
                'alpha1_avg': round(sum_a1 / n, 4),
                'alpha2_avg': round(sum_a2 / n, 4),
                'alpha3_avg': round(sum_a3 / n, 4),
            })
        
        self.deconstruction_results = results
        return results
    
    def generate_report(self):
        """生成基因解构报告"""
        report = {
            'report_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'core_equations': {
                'equation_1': 'α₁ + α₂ + α₃ = 1 (三元动力学公理)',
                'equation_2': '0.9̇ = 1 (意义一元本体)',
                'equation_3': 'Φ = α₁τ + α₂R + α₃C (存在稳态势能)',
                'equation_4': 'ΔΦ < 0 (自发演化判据)',
            },
            '三元_mapping': {
                'α₁': '个体性/强化系 - 结构承载、稳态保持',
                'α₂': '关系性/具现系 - 网络耦合、拓扑连接',
                'α₃': '变化性/变身系 - 演化更新、相变触发',
            },
            'stats': self.stats,
            'alpha_distribution': {
                'alpha1_avg': self.stats['alpha1_avg'],
                'alpha2_avg': self.stats['alpha2_avg'],
                'alpha3_avg': self.stats['alpha3_avg'],
                'normalized_sum': round(
                    self.stats['alpha1_avg'] + 
                    self.stats['alpha2_avg'] + 
                    self.stats['alpha3_avg'], 4
                ),
            },
            'state_distribution': {
                'healthy_pct': round(self.stats['healthy_genes'] / max(self.stats['total_genes'], 1) * 100, 1),
                'subhealthy_pct': round(self.stats['subhealthy_genes'] / max(self.stats['total_genes'], 1) * 100, 1),
                'disease_pct': round(self.stats['disease_genes'] / max(self.stats['total_genes'], 1) * 100, 1),
            },
            'top_disease_genes': sorted(
                [r for r in self.deconstruction_results if r['state'] == '疾病态'],
                key=lambda x: x['delta_alpha'],
                reverse=True
            )[:20],
            'conclusion': self._generate_conclusion(),
        }
        return report
    
    def _generate_conclusion(self):
        """生成结论"""
        s = self.stats
        a1, a2, a3 = s['alpha1_avg'], s['alpha2_avg'], s['alpha3_avg']
        
        # 判断主导分量
        max_alpha = max(a1, a2, a3)
        if max_alpha == a1:
            dominant = '强化系(α₁)主导'
            system_state = '系统结构固化，需要增加关系耦合和演化更新'
        elif max_alpha == a2:
            dominant = '具现系(α₂)主导'
            system_state = '系统关系活跃，但需确保结构稳态和演化能力'
        else:
            dominant = '变身系(α₃)主导'
            system_state = '系统演化活跃，但结构和关系需同步跟进'
        
        # 健康度评估
        health_rate = s['healthy_genes'] / max(s['total_genes'], 1)
        if health_rate >= 0.5:
            health_level = '良好'
        elif health_rate >= 0.3:
            health_level = '中等'
        else:
            health_level = '较差'
        
        # 0.9̇=1 收敛检验
        convergence = round(a1 + a2 + a3, 4)
        convergence_status = '收敛' if abs(convergence - 1.0) < 0.01 else '发散'
        
        return {
            'dominant_component': dominant,
            'system_state': system_state,
            'health_level': health_level,
            'convergence_status': convergence_status,
            'convergence_value': convergence,
            'recommendation': self._generate_recommendation(a1, a2, a3, health_rate),
        }
    
    def _generate_recommendation(self, a1, a2, a3, health_rate):
        """生成改进建议"""
        recommendations = []
        
        if a1 > 0.45:
            recommendations.append('α₁过高(结构固化): 建议增加动态库依赖，引入插件化架构')
        if a2 > 0.45:
            recommendations.append('α₂过高(关系过载): 建议减少不必要的依赖耦合，解耦核心模块')
        if a3 > 0.45:
            recommendations.append('α₃过高(演化过强): 建议建立版本稳定机制，防止频繁变更')
        
        if abs(a1 - a2) > 0.1:
            recommendations.append('α₁与α₂失衡: 强化系与具现系耦合不均，需调整结构与网络的权重比')
        if abs(a2 - a3) > 0.1:
            recommendations.append('α₂与α₃失衡: 具现系与变身系演化不同步，需协调耦合与更新节奏')
        
        if health_rate < 0.3:
            recommendations.append('健康基因比例过低: 系统存在大量疾病态基因，建议启动基因修复协议')
        
        if not recommendations:
            recommendations.append('三元动力学均衡，系统处于健康状态，建议维持当前平衡')
        
        return recommendations


def main():
    """主函数：运行基因解构引擎"""
    print("=" * 70)
    print("  BSD三元动力学基因解构引擎")
    print("  核心方程: α₁ + α₂ + α₃ = 1, 0.9̇ = 1")
    print("=" * 70)
    
    engine = BSDGeneDeconstructor()
    
    # 扫描路径
    scan_paths = [
        ('C:\\Program Files', 2, 3000),
        ('C:\\Program Files (x86)', 2, 3000),
        ('D:\\TRAE SOLO CN', 2, 2000),
    ]
    
    all_genes = []
    for path, depth, limit in scan_paths:
        if os.path.exists(path):
            print(f"\n  扫描: {path}")
            genes = engine.scan_directory(path, max_depth=depth, file_limit=limit)
            print(f"    发现基因: {len(genes)} 个")
            all_genes.extend(genes)
    
    print(f"\n  基因总数: {len(all_genes)} 个")
    
    # 三元动力学解构
    print("\n  进行三元动力学解构...")
    results = engine.deconstruct_genes(all_genes)
    
    # 生成报告
    report = engine.generate_report()
    
    # 打印摘要
    print("\n" + "=" * 70)
    print("  解构报告摘要")
    print("=" * 70)
    
    s = report['stats']
    print(f"\n  📊 统计数据:")
    print(f"    总基因数: {s['total_genes']}")
    print(f"    健康态: {s['healthy_genes']} ({report['state_distribution']['healthy_pct']}%)")
    print(f"    亚健康态: {s['subhealthy_genes']} ({report['state_distribution']['subhealthy_pct']}%)")
    print(f"    疾病态: {s['disease_genes']} ({report['state_distribution']['disease_pct']}%)")
    
    print(f"\n  🔬 三元动力学分量:")
    print(f"    α₁(强化系/个体性): {report['alpha_distribution']['alpha1_avg']}")
    print(f"    α₂(具现系/关系性): {report['alpha_distribution']['alpha2_avg']}")
    print(f"    α₃(变身系/变化性): {report['alpha_distribution']['alpha3_avg']}")
    print(f"    α₁+α₂+α₃: {report['alpha_distribution']['normalized_sum']}")
    
    print(f"\n  📈 收敛检验 (0.9̇=1):")
    print(f"    收敛值: {report['conclusion']['convergence_value']}")
    print(f"    状态: {report['conclusion']['convergence_status']}")
    
    print(f"\n  💡 系统判断:")
    print(f"    主导分量: {report['conclusion']['dominant_component']}")
    print(f"    系统状态: {report['conclusion']['system_state']}")
    print(f"    健康等级: {report['conclusion']['health_level']}")
    
    print(f"\n  🛠️ 改进建议:")
    for rec in report['conclusion']['recommendation']:
        print(f"    - {rec}")
    
    # 保存报告
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'BSD_Gene_Deconstruction_Report.json'
    )
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n  💾 报告已保存: {output_path}")
    
    return report


if __name__ == '__main__':
    main()
