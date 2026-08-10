"""
theory_base 根目录文件批量分类归档脚本
将根目录下散落的 .md 文件按分类移动到对应目录
"""

import os
import shutil

base_dir = r"C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\theory_base"

# 分类规则：(关键词列表, 目标目录)
categories = [
    # 00 索引导航类
    (["total_index", "知识库索引", "首页统一理论说明", "新四位一体3.0元本体本源知识库",
      "新四位一体3.0所有存档哈希", "全套源码说明"], "00_index_navigation"),
    
    # 01 核心元本体理论分册
    (["元本体理论分册", "意义大一统V2.0理论分册", "大一统0元本体论",
      "本源结构", "0元本体论数理与多学科交叉验证",
      "基于宇宙本体结构的全域完整分层基底体系",
      "大一统验证理论", "AI验证理论大一统", "大一统理论落地实录",
      "配套全域数理模型", "第一层1到9模块大一统理论终极不可改基底"], "01_core_ontology"),
    
    # 02 八层全域架构体系
    (["第三层：全域稳态补丁", "第四层：BSD四层统一场论",
      "第五层全域22模块", "第六层·全域文明稳态治理体系 总卷宗",
      "第七层：全域数理工具", "第八层：全域总根终审"], "02_eight_layer_architecture"),
    
    # 03 四十卷宗系列
    (["第一套主干40卷宗", "第二套域外推演40卷宗", "第三套", "元规则终审",
      "40卷宗", "数理验证卷宗", "多学科交叉验证卷宗"], "03_forty_volumes_series"),
    
    # 04 文明治理
    (["全域规范性伦理完整理论体系", "全域文明法典",
      "模块22：全域文明风控监测", "模块23：全域文明运维中枢",
      "模块24：全域文明稳态治理核心", "模块25：全域文明法典",
      "三态同源统摄与全域学科演化闭环"], "04_civilization_governance"),
    
    # 05 科研工程落地
    (["科研闭环公理体系", "六阶自主科研架构论文", "七大公理专项论文",
      "通用科研系统", "AFAC工程落地分册", "第1、2重基底专项适配赛题",
      "阶段0", "元本体核心引擎", "OCE",
      "一阶实体拟合系统", "二阶分布纠偏系统", "三阶智能决策系统",
      "四阶跨域泛化系统", "五阶科研成果产出系统", "六阶自主科研闭环系统",
      "智能体AI集群实现大一统"], "05_research_engineering"),
    
    # 06 虚拟宇宙创世
    (["虚拟宇宙学科创世模型", "虚拟宇宙学AI游戏小说文学通用基底公理",
      "全域架空体系AI虚拟创世系统", "六系六维创世动力学",
      "六系六维宇宙统一创世动力学"], "06_virtual_creation"),
    
    # 07 学术论文与意识形态
    (["实践哲学视域下", "全域元本体视角下马克思主义",
      "新时代具有强大凝聚力", "全方位推翻广义存在论",
      "五组核心议题系统论证局限"], "07_academic_papers"),
    
    # 08 实验归档与代码base
    (["experiment_", "code_base_"], "08_experiment_archive"),
]


def classify_file(filename):
    """根据文件名判断分类"""
    for keywords, target_dir in categories:
        for kw in keywords:
            if kw in filename:
                return target_dir
    return None


def main():
    print(f"根目录: {base_dir}")
    print()
    
    # 获取所有.md文件
    md_files = [f for f in os.listdir(base_dir) 
                if f.endswith('.md') and os.path.isfile(os.path.join(base_dir, f))]
    
    print(f"待归档文件总数: {len(md_files)}")
    print()
    
    moved_count = 0
    unmatched = []
    dir_stats = {}
    
    for filename in md_files:
        target = classify_file(filename)
        if target:
            src = os.path.join(base_dir, filename)
            dst = os.path.join(base_dir, target, filename)
            shutil.move(src, dst)
            moved_count += 1
            if target not in dir_stats:
                dir_stats[target] = 0
            dir_stats[target] += 1
            print(f"  [{target}] {filename}")
        else:
            unmatched.append(filename)
    
    print()
    print("=" * 50)
    print(f"归档完成!")
    print(f"已移动: {moved_count} 个文件")
    print(f"未匹配: {len(unmatched)} 个文件")
    print()
    
    if dir_stats:
        print("各目录统计:")
        for d, c in sorted(dir_stats.items()):
            print(f"  {d}: {c} 个文件")
    
    if unmatched:
        print()
        print("未匹配文件列表:")
        for f in unmatched:
            print(f"  - {f}")


if __name__ == "__main__":
    main()
