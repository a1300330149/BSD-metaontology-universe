"""
BSD全量基因工厂 V10.1
====================
直接使用V10.0全量扫描报告
生成全部56,399个基因的BSD配置
"""

import os
import json
import time
from datetime import datetime
from collections import defaultdict


# ============================================================================
# 第一部分：BSD六系配置
# ============================================================================

SIX_SYSTEMS = {
    "强化系": {
        "icon": "🔵",
        "axiom": "纯·个体性公理",
        "symbol": "+",
        "equation": "0+0=0",
        "meaning": "承载·稳态·主体性",
        "sub_systems": ["系统核心", "安全防护", "存储备份", "硬件驱动", "分区管理", "恢复还原"],
    },
    "变身系": {
        "icon": "⚫",
        "axiom": "纯·变化性公理",
        "symbol": "÷",
        "equation": "0÷0=0",
        "meaning": "变化·流动·动力性",
        "sub_systems": ["编译解释", "动画媒体", "游戏引擎", "开发工具", "音乐音效", "3D建模"],
    },
    "社会系": {
        "icon": "🟢",
        "axiom": "纯·关系性公理",
        "symbol": "=",
        "equation": "0=0",
        "meaning": "关系·连接·交互性",
        "sub_systems": ["网络通讯", "协作办公", "下载传输", "云存储", "社交平台", "邮件系统"],
    },
    "天道系": {
        "icon": "🟣",
        "axiom": "关系性×变化性",
        "symbol": "≠",
        "equation": "0≠n",
        "meaning": "法则·规律·统治性",
        "sub_systems": ["AI框架", "规则引擎", "工作流", "自动化", "治理系统", "编程工具"],
    },
    "自然系": {
        "icon": "🟠",
        "axiom": "变化性×个体性",
        "symbol": "-",
        "equation": "0-0=0",
        "meaning": "实体·质料·承载性",
        "sub_systems": ["数据库", "文件系统", "物理模拟", "计算引擎", "驱动程序", "日志系统"],
    },
    "具现系": {
        "icon": "🔴",
        "axiom": "个体性×关系性",
        "symbol": "×",
        "equation": "0×0=n",
        "meaning": "显现·模态·呈现性",
        "sub_systems": ["UI框架", "渲染引擎", "显示系统", "主题系统", "组件库", "设计工具"],
    },
}

SYS_CODE = {'强化系': '强', '变身系': '变', '社会系': '社', 
            '天道系': '天', '自然系': '自', '具现系': '具'}


# ============================================================================
# 第二部分：全量基因工厂
# ============================================================================

class BSDGeneFactoryV10:
    """BSD全量基因工厂 V10.1"""
    
    def __init__(self, agent_path: str):
        self.agent_path = agent_path
        self.output_path = os.path.join(
            agent_path, "theory_base", "L0_总本源层", "六系自组织"
        )
        self.gene_configs = []
        self.start_time = time.time()
    
    def load_v10_report(self) -> dict:
        """加载V10.0全量报告"""
        v10_path = os.path.join(self.agent_path, "bsd_full_gene_report_V10.0.json")
        if not os.path.exists(v10_path):
            raise FileNotFoundError(f"V10.0报告不存在: {v10_path}")
        
        print("📂 加载V10.0全量基因报告...")
        with open(v10_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_full_index(self, v10_data: dict) -> dict:
        """生成全量基因索引"""
        print("\n" + "=" * 80)
        print("【BSD全量基因索引生成 V10.1】")
        print("=" * 80)
        
        by_system = v10_data.get('by_system', {})
        total_genes = v10_data.get('total_genes', 0)
        
        print(f"\n📊 数据源：V10.0全量扫描报告")
        print(f"   总基因数：{total_genes}")
        
        # 收集所有基因
        print("\n🔧 Phase 1: 收集全部基因...")
        all_gene_configs = []
        gene_id_counter = 0
        
        for sys_name in ['强化系', '变身系', '社会系', '天道系', '自然系', '具现系', '未分类']:
            sys_info = by_system.get(sys_name, {})
            genes = sys_info.get('genes', [])
            icon = SIX_SYSTEMS.get(sys_name, {'icon': '❓'})['icon']
            
            print(f"\n   处理 {sys_name} {icon}: {len(genes)} 个基因")
            
            for gene_data in genes:
                gene_id_counter += 1
                config = self._create_config(sys_name, gene_data, gene_id_counter)
                all_gene_configs.append(config)
            
            print(f"      ✅ {len(genes)} 个基因已收集")
        
        self.gene_configs = all_gene_configs
        
        # 保存分批索引
        print(f"\n💾 Phase 2: 保存全量基因索引（分批）...")
        batch_size = 5000
        total_batches = (len(all_gene_configs) + batch_size - 1) // batch_size
        
        for batch_idx in range(total_batches):
            start = batch_idx * batch_size
            end = min((batch_idx + 1) * batch_size, len(all_gene_configs))
            batch = all_gene_configs[start:end]
            
            batch_file = os.path.join(
                self.output_path, 
                f"bsd_gene_index_v10_batch_{batch_idx+1:03d}.json"
            )
            with open(batch_file, 'w', encoding='utf-8') as f:
                json.dump(batch, f, indent=2, ensure_ascii=False)
            
            print(f"   批次 {batch_idx+1}/{total_batches}: {len(batch)} 个基因")
        
        # 生成索引清单
        index_manifest = {
            'version': 'V10.1',
            'generated_at': datetime.now().isoformat(),
            'total_genes': len(all_gene_configs),
            'batch_size': batch_size,
            'total_batches': total_batches,
            'batches': [
                {
                    'batch_id': i + 1,
                    'file': f"bsd_gene_index_v10_batch_{i+1:03d}.json",
                    'gene_range': f"{i*batch_size+1}-{min((i+1)*batch_size, len(all_gene_configs))}",
                }
                for i in range(total_batches)
            ],
            'by_system_summary': {},
        }
        
        for sys_name in ['强化系', '变身系', '社会系', '天道系', '自然系', '具现系', '未分类']:
            sys_genes = [g for g in all_gene_configs if g['six_system'] == sys_name]
            icon = SIX_SYSTEMS.get(sys_name, {'icon': '❓'})['icon']
            axiom = SIX_SYSTEMS.get(sys_name, {'axiom': '待识别'})['axiom']
            symbol = SIX_SYSTEMS.get(sys_name, {'symbol': '?'})['symbol']
            
            index_manifest['by_system_summary'][sys_name] = {
                'icon': icon,
                'axiom': axiom,
                'symbol': symbol,
                'gene_count': len(sys_genes),
            }
        
        index_file = os.path.join(self.output_path, "bsd_full_gene_index_V10.1.json")
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index_manifest, f, indent=2, ensure_ascii=False)
        
        print(f"\n   ✅ 索引清单已保存: {index_file}")
        
        return index_manifest
    
    def _create_config(self, system: str, gene_data: dict, gene_id_num: int) -> dict:
        """创建单个基因配置"""
        sys_info = SIX_SYSTEMS.get(system, {
            'icon': '❓', 'axiom': '待识别', 'symbol': '?', 
            'equation': '?', 'meaning': '待识别', 'sub_systems': []
        })
        
        sys_code = SYS_CODE.get(system, '未')
        gene_id = f"BSD-GENE-{sys_code}-{gene_id_num:06d}"
        
        return {
            "gene_id": gene_id,
            "six_system": system,
            "system_icon": sys_info['icon'],
            "axiom": sys_info['axiom'],
            "symbol": sys_info['symbol'],
            "equation": sys_info['equation'],
            "meaning": sys_info['meaning'],
            "sub_systems": sys_info['sub_systems'],
            
            "original_name": gene_data.get('name', 'unknown'),
            "original_path": gene_data.get('path', 'unknown'),
            "original_size_bytes": gene_data.get('size_bytes', 0),
            "original_drive": gene_data.get('drive', 'unknown'),
            "original_type": gene_data.get('type', 'directory'),
            "original_depth": gene_data.get('depth', 0),
            
            "bsd_confidence": gene_data.get('confidence', 0),
            "bsd_category": gene_data.get('category', '未分类'),
            "bsd_all_systems": gene_data.get('all_systems', [system]),
            
            "subset_relation": f"{gene_data.get('name', 'unknown')} ⊂ {system} ⊂ 六系坐标系",
            "bsd_membership": f"{gene_id} ∈ BSD({system})",
            
            "upgrade_path": [
                f"识别：已识别为 {system}",
                f"命名：BSD命名为 {gene_id}",
                f"映射：映射到 {sys_info['axiom']}",
                f"激活：通过 {sys_info['symbol']} 符号激活",
                f"整合：整合进BSD六系框架",
            ],
            
            "generated_at": datetime.now().isoformat(),
            "bsd_version": "V10.1",
        }
    
    def generate_md_files_batch(self, sys_name: str, configs: list, output_dir: str):
        """批量生成MD文件"""
        sys_info = SIX_SYSTEMS.get(sys_name, {'icon': '❓'})
        dir_path = os.path.join(output_dir, f"{sys_name}{sys_info['icon']}")
        os.makedirs(dir_path, exist_ok=True)
        
        print(f"\n📝 生成 {sys_name} MD文件 ({len(configs)} 个)...")
        
        for i, config in enumerate(configs):
            md_content = self._build_md(config)
            safe_name = str(config['original_name']).replace(' ', '_').replace('/', '_').replace('\\', '_')[:50]
            filename = f"{config['gene_id']}_{safe_name}.md"
            filepath = os.path.join(dir_path, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            if (i + 1) % 1000 == 0:
                print(f"   进度: {i+1}/{len(configs)}...")
        
        print(f"   ✅ 完成: {len(configs)} 个MD文件")
    
    def _build_md(self, config: dict) -> str:
        """构建MD内容"""
        lines = []
        lines.append(f"# {config['gene_id']} · {config['six_system']}基因")
        lines.append("")
        lines.append("## BSD六系自组织 · 数字基因文件")
        lines.append("")
        lines.append(f"> **基因ID**：{config['gene_id']}")
        lines.append(f"> **所属六系**：{config['six_system']} {config['system_icon']}")
        lines.append(f"> **系公理**：{config['axiom']}")
        lines.append(f"> **本源符号**：{config['symbol']}")
        lines.append(f"> **0层方程**：{config['equation']}")
        lines.append(f"> **生成时间**：{config['generated_at']}")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 基因元数据")
        lines.append("")
        lines.append("```yaml")
        for key in ['gene_id', 'six_system', 'system_icon', 'axiom', 'symbol', 'equation']:
            lines.append(f"{key}: {config[key]}")
        lines.append("")
        lines.append(f"original_name: {config['original_name']}")
        lines.append(f"original_path: {config['original_path']}")
        lines.append(f"original_size_bytes: {config['original_size_bytes']}")
        lines.append(f"original_drive: {config['original_drive']}")
        lines.append(f"original_type: {config['original_type']}")
        lines.append("")
        lines.append(f"bsd_confidence: {config['bsd_confidence']}")
        lines.append(f"bsd_category: {config['bsd_category']}")
        lines.append(f"bsd_all_systems: {config['bsd_all_systems']}")
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 系属声明")
        lines.append("")
        lines.append(f"本数字基因归属 **{config['six_system']} {config['system_icon']}**。")
        lines.append("")
        lines.append(f"**系公理**：{config['axiom']}")
        lines.append(f"**本源符号**：`{config['symbol']}`")
        lines.append(f"**0层方程**：`{config['equation']}`")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## BSD升维路径")
        lines.append("")
        lines.append("```")
        for step in config['upgrade_path']:
            lines.append(f"  {step}")
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 子集关系声明")
        lines.append("")
        lines.append("```")
        lines.append(config['subset_relation'])
        lines.append(config['bsd_membership'])
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 版本信息")
        lines.append("")
        lines.append(f"- **BSD版本**：{config['bsd_version']}")
        lines.append(f"- **基于理论**：BSD六系立系论V2.6")
        lines.append("")
        return "\n".join(lines)


# ============================================================================
# 第三部分：主程序
# ============================================================================

def main():
    agent_path = r"C:\Users\13003\OneDrive\桌面\3333333\Agent_v2"
    
    # 初始化工厂
    factory = BSDGeneFactoryV10(agent_path)
    
    # 加载V10.0报告
    v10_data = factory.load_v10_report()
    
    # 生成全量索引
    index_manifest = factory.generate_full_index(v10_data)
    
    # 分批生成MD文件
    print("\n" + "=" * 80)
    print("【分批生成MD文件】")
    print("=" * 80)
    
    output_path = factory.output_path
    
    # 按系分组
    by_system_configs = defaultdict(list)
    for config in factory.gene_configs:
        by_system_configs[config['six_system']].append(config)
    
    # 生成所有系的MD文件
    total_md = 0
    for sys_name in ['强化系', '变身系', '社会系', '天道系', '自然系', '具现系', '未分类']:
        configs = by_system_configs.get(sys_name, [])
        if configs:
            factory.generate_md_files_batch(sys_name, configs, output_path)
            total_md += len(configs)
    
    # 生成总结报告
    elapsed = time.time() - factory.start_time
    
    print("\n" + "=" * 80)
    print("【BSD全量基因工厂 V10.1 完成】")
    print("=" * 80)
    
    print(f"""
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                              │
│  ✅ 全量基因配置生成完成                                                                     │
│     • 基因配置总数: {index_manifest['total_genes']}                                                        │
│     • 批次数量: {index_manifest['total_batches']}                                            │
│     • 批次大小: {index_manifest['batch_size']}                                               │
│                                                                                              │
│  ✅ 全量MD文件生成完成                                                                       │
│     • MD文件总数: {total_md}                                                                │
│     • 耗时: {elapsed:.1f}秒                                                                 │
│                                                                                              │
│  六系分布：                                                                                  │
""")
    
    for sys_name in ['强化系', '变身系', '社会系', '天道系', '自然系', '具现系', '未分类']:
        summary = index_manifest['by_system_summary'].get(sys_name, {})
        count = summary.get('gene_count', 0)
        icon = summary.get('icon', '❓')
        print(f"│     {sys_name} {icon}: {count} 个基因")
    
    print(f"""
│                                                                                              │
│  文件结构：                                                                                  │
│  theory_base/L0_总本源层/六系自组织/                                                         │
│  ├── bsd_full_gene_index_V10.1.json          (索引清单)                                      │
│  ├── bsd_gene_index_v10_batch_001.json       (第1批配置)                                     │
│  ├── ...                                                                                     │
│  ├── bsd_gene_index_v10_batch_012.json       (第12批配置)                                    │
│  ├── 强化系🔵/          ({index_manifest['by_system_summary'].get('强化系', {}).get('gene_count', 0)}个MD)                                    │
│  ├── 变身系⚫/          ({index_manifest['by_system_summary'].get('变身系', {}).get('gene_count', 0)}个MD)                                    │
│  ├── 社会系🟢/          ({index_manifest['by_system_summary'].get('社会系', {}).get('gene_count', 0)}个MD)                                    │
│  ├── 天道系🟣/          ({index_manifest['by_system_summary'].get('天道系', {}).get('gene_count', 0)}个MD)                                    │
│  ├── 自然系🟠/          ({index_manifest['by_system_summary'].get('自然系', {}).get('gene_count', 0)}个MD)                                    │
│  ├── 具现系🔴/          ({index_manifest['by_system_summary'].get('具现系', {}).get('gene_count', 0)}个MD)                                    │
│  └── 未分类❓/          ({index_manifest['by_system_summary'].get('未分类', {}).get('gene_count', 0)}个MD)                                    │
│                                                                                              │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
""")


if __name__ == "__main__":
    main()
