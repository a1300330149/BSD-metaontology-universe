"""
BSD全量基因工厂 V9.0
====================
直接用BSD生成全部69,882个基因的参数配置
支持：
  1. 全量基因索引生成（JSON配置）
  2. 按系批量生成MD文件
  3. 增量生成（支持随时扩展）
  4. 统计报表
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


# ============================================================================
# 第二部分：BSD基因工厂
# ============================================================================

class BSDGeneFactory:
    """BSD全量基因工厂"""
    
    def __init__(self, agent_path: str):
        self.agent_path = agent_path
        self.output_path = os.path.join(
            agent_path, "theory_base", "L0_总本源层", "六系自组织"
        )
        self.gene_configs = []  # 所有基因配置
        self.gene_counter = 0
        self.start_time = time.time()
    
    def load_v6_report(self) -> dict:
        """加载V6.0扫描报告"""
        v6_path = os.path.join(self.agent_path, "bsd_full_disk_report_V6.0.json")
        if not os.path.exists(v6_path):
            raise FileNotFoundError(f"V6.0报告不存在: {v6_path}")
        
        with open(v6_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_full_gene_index(self, v6_data: dict) -> dict:
        """生成全量基因索引（配置文件）"""
        print("\n" + "=" * 80)
        print("【BSD全量基因索引生成 V9.0】")
        print("=" * 80)
        
        by_system = v6_data.get('by_system', {})
        total_genes = v6_data.get('total_genes', 0)
        
        print(f"\n📊 数据源：V6.0全盘扫描报告")
        print(f"   总基因数：{total_genes}")
        print(f"   六系分布：")
        for sys_name, sys_info in by_system.items():
            count = sys_info.get('count', 0)
            print(f"      {sys_name} {sys_info.get('icon', '?')}: {count}")
        
        # Phase 1: 生成全量基因配置
        print("\n🔧 Phase 1: 生成全量基因配置...")
        all_gene_configs = []
        
        for sys_name in ['强化系', '变身系', '社会系', '天道系', '自然系', '具现系']:
            sys_info = by_system.get(sys_name, {})
            icon = SIX_SYSTEMS[sys_name]['icon']
            top_genes = sys_info.get('top_genes', [])
            
            print(f"\n   处理 {sys_name} {icon}:")
            
            for i, gene in enumerate(top_genes):
                self.gene_counter += 1
                
                # 生成基因配置
                config = self._create_gene_config(sys_name, gene, self.gene_counter)
                all_gene_configs.append(config)
                
                if (i + 1) % 1000 == 0:
                    print(f"      已处理 {i+1} 个...")
            
            print(f"      ✅ {len(top_genes)} 个基因配置已生成")
        
        self.gene_configs = all_gene_configs
        
        # Phase 2: 保存全量基因索引
        print("\n💾 Phase 2: 保存全量基因索引...")
        index_file = os.path.join(self.output_path, "bsd_full_gene_index_V9.0.json")
        
        # 分批保存（避免大文件）
        batch_size = 10000
        total_batches = (len(all_gene_configs) + batch_size - 1) // batch_size
        
        for batch_idx in range(total_batches):
            start = batch_idx * batch_size
            end = min((batch_idx + 1) * batch_size, len(all_gene_configs))
            batch = all_gene_configs[start:end]
            
            batch_file = os.path.join(
                self.output_path, 
                f"bsd_gene_index_batch_{batch_idx+1:03d}.json"
            )
            with open(batch_file, 'w', encoding='utf-8') as f:
                json.dump(batch, f, indent=2, ensure_ascii=False)
            
            print(f"   批次 {batch_idx+1}/{total_batches}: {len(batch)} 个基因 → {batch_file}")
        
        # 保存索引清单
        index_manifest = {
            'version': 'V9.0',
            'generated_at': datetime.now().isoformat(),
            'total_genes': len(all_gene_configs),
            'batch_size': batch_size,
            'total_batches': total_batches,
            'batches': [
                {
                    'batch_id': i + 1,
                    'file': f"bsd_gene_index_batch_{i+1:03d}.json",
                    'gene_range': f"{i*batch_size+1}-{min((i+1)*batch_size, len(all_gene_configs))}",
                }
                for i in range(total_batches)
            ],
            'by_system': {
                sys_name: {
                    'icon': SIX_SYSTEMS[sys_name]['icon'],
                    'axiom': SIX_SYSTEMS[sys_name]['axiom'],
                    'symbol': SIX_SYSTEMS[sys_name]['symbol'],
                    'equation': SIX_SYSTEMS[sys_name]['equation'],
                    'gene_count': sum(
                        1 for g in all_gene_configs 
                        if g['six_system'] == sys_name
                    ),
                }
                for sys_name in ['强化系', '变身系', '社会系', '天道系', '自然系', '具现系']
            },
        }
        
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index_manifest, f, indent=2, ensure_ascii=False)
        
        print(f"\n   ✅ 索引清单已保存: {index_file}")
        
        return index_manifest
    
    def _create_gene_config(self, system: str, gene_data: dict, gene_id_num: int) -> dict:
        """创建单个基因配置"""
        sys_info = SIX_SYSTEMS[system]
        
        # 生成基因ID
        sys_code = {'强化系': '强', '变身系': '变', '社会系': '社', 
                    '天道系': '天', '自然系': '自', '具现系': '具'}
        gene_id = f"BSD-GENE-{sys_code[system]}-{gene_id_num:06d}"
        
        return {
            "gene_id": gene_id,
            "six_system": system,
            "system_icon": sys_info['icon'],
            "axiom": sys_info['axiom'],
            "symbol": sys_info['symbol'],
            "equation": sys_info['equation'],
            "meaning": sys_info['meaning'],
            "sub_systems": sys_info['sub_systems'],
            
            # 原始软件信息
            "original_name": gene_data.get('name', 'unknown'),
            "original_path": gene_data.get('path', 'unknown'),
            "original_size_bytes": gene_data.get('size_bytes', 0),
            "original_drive": gene_data.get('drive', 'unknown'),
            "original_type": gene_data.get('type', 'directory'),
            "original_depth": gene_data.get('depth', 0),
            
            # BSD映射信息
            "bsd_confidence": gene_data.get('confidence', 0),
            "bsd_category": gene_data.get('category', '未分类'),
            "bsd_all_systems": gene_data.get('all_systems', [system]),
            
            # 子集关系
            "subset_relation": f"{gene_data.get('name', 'unknown')} ⊂ {system} ⊂ 六系坐标系",
            "bsd_membership": f"{gene_id} ∈ BSD({system})",
            
            # 升维路径
            "upgrade_path": [
                f"识别：已识别为 {system}",
                f"命名：BSD命名为 {gene_id}",
                f"映射：映射到 {sys_info['axiom']}",
                f"激活：通过 {sys_info['symbol']} 符号激活",
                f"整合：整合进BSD六系框架",
            ],
            
            "generated_at": datetime.now().isoformat(),
            "bsd_version": "V9.0",
        }
    
    def batch_generate_md_files(self, sys_name: str, max_files: int = None):
        """按系批量生成MD文件"""
        print(f"\n📝 批量生成 {sys_name} MD文件...")
        
        sys_info = SIX_SYSTEMS[sys_name]
        dir_path = os.path.join(self.output_path, f"{sys_name}{sys_info['icon']}")
        os.makedirs(dir_path, exist_ok=True)
        
        # 加载该系的基因配置
        sys_configs = [g for g in self.gene_configs if g['six_system'] == sys_name]
        
        if max_files:
            sys_configs = sys_configs[:max_files]
        
        print(f"   待生成: {len(sys_configs)} 个文件")
        
        for i, config in enumerate(sys_configs):
            # 生成MD文件
            md_content = self._build_md_content(config)
            safe_name = config['original_name'].replace(' ', '_').replace('/', '_').replace('\\', '_')
            filename = f"{config['gene_id']}_{safe_name}.md"
            filepath = os.path.join(dir_path, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            if (i + 1) % 500 == 0:
                print(f"   进度: {i+1}/{len(sys_configs)}...")
        
        print(f"   ✅ 完成: {len(sys_configs)} 个MD文件已生成")
    
    def _build_md_content(self, config: dict) -> str:
        """构建MD文件内容"""
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
        lines.append(f"gene_id: {config['gene_id']}")
        lines.append(f"six_system: {config['six_system']}")
        lines.append(f"system_icon: {config['system_icon']}")
        lines.append(f"axiom: {config['axiom']}")
        lines.append(f"symbol: {config['symbol']}")
        lines.append(f"equation: {config['equation']}")
        lines.append(f"")
        lines.append(f"original_name: {config['original_name']}")
        lines.append(f"original_path: {config['original_path']}")
        lines.append(f"original_size_bytes: {config['original_size_bytes']}")
        lines.append(f"original_drive: {config['original_drive']}")
        lines.append(f"original_type: {config['original_type']}")
        lines.append(f"")
        lines.append(f"bsd_confidence: {config['bsd_confidence']}")
        lines.append(f"bsd_category: {config['bsd_category']}")
        lines.append(f"bsd_all_systems: {config['bsd_all_systems']}")
        lines.append("```")
        lines.append("")
        
        lines.append("---")
        lines.append("")
        lines.append("## 系属声明")
        lines.append("")
        lines.append(f"本数字基因经BSD六系自组织系统识别，归属 **{config['six_system']} {config['system_icon']}**。")
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
        lines.append(f"- **BSD六系自组织版本**：{config['bsd_version']}")
        lines.append(f"- **基因文件版本**：V1.0")
        lines.append(f"- **基于理论**：BSD六系立系论V2.6")
        lines.append("")
        lines.append("```")
        lines.append("数字基因 = 文件落地的BSD子集")
        lines.append("```")
        
        return "\n".join(lines)
    
    def generate_summary_report(self, index_manifest: dict) -> str:
        """生成全量基因统计报告"""
        elapsed = time.time() - self.start_time
        
        lines = []
        lines.append("# BSD全量基因工厂 V9.0 · 生成报告")
        lines.append("")
        lines.append(f"> **生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"> **耗时**：{elapsed:.1f}秒")
        lines.append(f"> **基因总数**：{index_manifest['total_genes']}")
        lines.append("")
        
        lines.append("---")
        lines.append("")
        lines.append("## 六系基因分布")
        lines.append("")
        lines.append("| 六系 | 图标 | 公理 | 符号 | 基因数 |")
        lines.append("|:---|:---:|:---|:---:|:---:|")
        
        for sys_name in ['强化系', '变身系', '社会系', '天道系', '自然系', '具现系']:
            sys_info = index_manifest['by_system'].get(sys_name, {})
            lines.append(
                f"| {sys_name} | {sys_info.get('icon', '?')} | "
                f"{sys_info.get('axiom', '')} | "
                f"{sys_info.get('symbol', '')} | "
                f"{sys_info.get('gene_count', 0)} |"
            )
        lines.append("")
        
        lines.append("---")
        lines.append("")
        lines.append("## 批次信息")
        lines.append("")
        lines.append(f"- **批次大小**：{index_manifest['batch_size']}")
        lines.append(f"- **批次总数**：{index_manifest['total_batches']}")
        lines.append("")
        
        lines.append("---")
        lines.append("")
        lines.append("## 使用说明")
        lines.append("")
        lines.append("```")
        lines.append("1. 加载基因配置：")
        lines.append("   python -c \"import json; data=json.load(open('bsd_gene_index_batch_001.json'))\"")
        lines.append("")
        lines.append("2. 按需生成MD文件：")
        lines.append("   factory.batch_generate_md_files('强化系', max_files=100)")
        lines.append("")
        lines.append("3. 全量生成MD文件：")
        lines.append("   for sys in ['强化系','变身系','社会系','天道系','自然系','具现系']:")
        lines.append("       factory.batch_generate_md_files(sys)")
        lines.append("```")
        lines.append("")
        
        return "\n".join(lines)


# ============================================================================
# 第三部分：主程序
# ============================================================================

def main():
    agent_path = r"C:\Users\13003\OneDrive\桌面\3333333\Agent_v2"
    
    # 初始化工厂
    factory = BSDGeneFactory(agent_path)
    
    # 加载V6.0报告
    print("📂 加载V6.0全盘扫描报告...")
    v6_data = factory.load_v6_report()
    
    # 生成全量基因索引
    index_manifest = factory.generate_full_gene_index(v6_data)
    
    # 生成统计报告
    print("\n📊 生成统计报告...")
    report_content = factory.generate_summary_report(index_manifest)
    report_file = os.path.join(factory.output_path, "BSD全量基因工厂_V9.0_生成报告.md")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    print(f"   ✅ 报告已保存: {report_file}")
    
    # 可选：批量生成MD文件（每系限制数量以避免文件爆炸）
    print("\n" + "=" * 80)
    print("【可选】批量生成MD文件")
    print("=" * 80)
    
    # 生成核心基因（每系前50个）
    print("\n📝 生成核心基因MD文件（每系Top 50）...")
    for sys_name in ['强化系', '变身系', '社会系', '天道系', '自然系', '具现系']:
        factory.batch_generate_md_files(sys_name, max_files=50)
    
    print("\n" + "=" * 80)
    print("【BSD全量基因工厂 V9.0 完成】")
    print("=" * 80)
    
    total_configs = index_manifest['total_genes']
    total_md = sum(
        len([f for f in os.listdir(os.path.join(factory.output_path, f"{s}{SIX_SYSTEMS[s]['icon']}")) 
             if f.endswith('.md')])
        for s in ['强化系', '变身系', '社会系', '天道系', '自然系', '具现系']
        if os.path.exists(os.path.join(factory.output_path, f"{s}{SIX_SYSTEMS[s]['icon']}"))
    )
    
    print(f"""
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                              │
│  ✅ 全量基因配置生成完成                                                                     │
│     • 基因配置总数: {total_configs}                                                          │
│     • 批次数量: {index_manifest['total_batches']}                                            │
│     • 批次大小: {index_manifest['batch_size']}                                               │
│                                                                                              │
│  ✅ 核心基因MD文件生成完成                                                                   │
│     • MD文件总数: {total_md}                                                                │
│     • 每系50个核心基因                                                                      │
│                                                                                              │
│  文件结构：                                                                                  │
│  theory_base/L0_总本源层/六系自组织/                                                         │
│  ├── bsd_full_gene_index_V9.0.json          (索引清单)                                      │
│  ├── bsd_gene_index_batch_001.json          (第1批基因配置)                                 │
│  ├── ...                                                                                     │
│  ├── bsd_gene_index_batch_007.json          (第7批基因配置)                                 │
│  ├── 强化系🔵/          (50个核心MD文件)                                                     │
│  ├── 变身系⚫/          (50个核心MD文件)                                                     │
│  ├── 社会系🟢/          (50个核心MD文件)                                                     │
│  ├── 天道系🟣/          (50个核心MD文件)                                                     │
│  ├── 自然系🟠/          (50个核心MD文件)                                                     │
│  ├── 具现系🔴/          (50个核心MD文件)                                                     │
│  └── BSD全量基因工厂_V9.0_生成报告.md                                                         │
│                                                                                              │
│  全量生成方法：                                                                              │
│  factory = BSDGeneFactory(agent_path)                                                       │
│  factory.batch_generate_md_files('强化系')  # 生成全部强化系基因                              │
│                                                                                              │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
""")


if __name__ == "__main__":
    main()
