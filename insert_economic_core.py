# -*- coding: utf-8 -*-
"""
在HTML的T88章节中插入BSD全域经济元体系核心提炼版本
完整论文保留在theory_base总本源层T88 Markdown源文件中
HTML中仅显示核心提炼，指向完整源文件
"""

file_path = r'c:\Users\13003\OneDrive\桌面\3333333\Agent_v2\新六系本体论_人类易懂版.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 定位插入位置：T88章节参考文献div结束后、T88内容div闭合前
# 参考文献结束标记：最后一个参考文献条目后的闭合div
ref_end_marker = '<div>[8] Tarski, A. The concept of truth in formalized languages[M]//Logic, Semantics, Metamathematics. Oxford: Clarendon Press, 1956: 152-278.</div>'
ref_start_pos = content.find(ref_end_marker)

if ref_start_pos == -1:
    print('错误：未找到T88章节参考文献结束标记！')
    exit(1)

print(f'找到参考文献结束位置：字符偏移 {ref_start_pos}')

# 从参考文献结束位置开始，找到参考文献div的闭合
# 结构：<div>[8] Tarski...</div>\n          </div>\n        </div>
# 第一个</div>是参考文献条目闭合
# 第二个</div>是参考文献div闭合
# 第三个</div>是T88内容div闭合

import re
ref_end_pattern = r'</div>\s*\n\s*</div>\s*\n\s*</div>'
ref_end_match = re.search(ref_end_pattern, content[ref_start_pos:])

if ref_end_match:
    # 找到第二个</div>的位置（参考文献div闭合）
    # 我们需要在参考文献div闭合后、T88内容div闭合前插入
    first_close = content.find('</div>', ref_start_pos)
    second_close = content.find('</div>', first_close + 6)
    
    # 插入位置：在第二个</div>之后（即参考文献div闭合后）
    insert_pos = second_close + 6
    print(f'插入位置（参考文献div闭合后）：字符偏移 {insert_pos}')
else:
    print('错误：未找到参考文献闭合结构！')
    exit(1)

# 构造BSD全域经济元体系核心提炼HTML内容
economic_core_content = '''
        <!-- BSD全域经济元体系核心提炼 -->
        <div style="background:linear-gradient(135deg,rgba(255,193,7,0.12),rgba(255,87,34,0.12));padding:18px;border-radius:12px;border:2px solid rgba(255,152,0,0.4);margin-top:20px;margin-bottom:12px;">
          <div style="font-weight:bold;color:#ffb74d;font-size:1.15em;margin-bottom:6px;text-align:center;">📊 BSD全域经济元体系：修正传统经济学核心盲区</div>
          <div style="color:#ffcc80;font-size:0.7em;text-align:center;margin-bottom:14px;font-style:italic;">BSD Global Economic Meta-System · 双文明分层架构 · 非均衡动态进化范式</div>
          <div style="text-align:center;margin-bottom:14px;"><span style="display:inline-block;background:rgba(255,152,0,0.15);padding:4px 12px;border-radius:20px;color:#ffb74d;font-size:0.65em;">完整论文详见 theory_base/L0_总本源层/作者猜想/T88 BSD全域经济元体系.md</span></div>

          <!-- 核心命题 -->
          <div style="background:rgba(0,0,0,0.25);padding:12px;border-radius:8px;margin-bottom:12px;border-left:4px solid #ff9800;">
            <div style="font-weight:bold;color:#ffcc80;font-size:0.85em;margin-bottom:8px;">🎯 核心命题</div>
            <div style="color:#ffe0b2;font-size:0.7em;line-height:1.8;">
              <div style="margin-bottom:4px;"><b>命题1：</b>传统经济学混淆「地球载体客观有限性」与「资源相对稀缺性」两类独立约束，形成全域性前提偏误。</div>
              <div style="margin-bottom:4px;"><b>命题2：</b>人类物质需求天然有限（生物基底 $\tau_0$），无限欲望仅存在于符号/叙事/博弈/智能交互维度。</div>
              <div style="margin-bottom:4px;"><b>命题3：</b>文化游戏智能体构成的无限符号迭代系统，从底层消解「无限欲望vs有限物质」的传统经济核心矛盾。</div>
              <div><b>命题4：</b>经济系统常态为非均衡动态进化，静态均衡仅为低阶瞬时特例；后稀缺时代终极稀缺为碳基智能注意力。</div>
            </div>
          </div>

          <!-- 四大理论突破 -->
          <div style="background:rgba(0,0,0,0.2);padding:12px;border-radius:8px;margin-bottom:12px;border-left:3px solid #ff9800;">
            <div style="font-weight:bold;color:#ffb74d;font-size:0.82em;margin-bottom:10px;">🔬 四大理论突破</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;font-size:0.65em;">
              <div style="background:rgba(255,152,0,0.08);padding:10px;border-radius:8px;border-left:3px solid #ff9800;">
                <div style="font-weight:bold;color:#ffb74d;margin-bottom:4px;">① 边界二分</div>
                <div style="color:#ffe0b2;line-height:1.6;">行星物质硬约束 vs 分配耦合相对稀缺<br>破除稀缺永恒全域前提</div>
              </div>
              <div style="background:rgba(255,152,0,0.08);padding:10px;border-radius:8px;border-left:3px solid #ff9800;">
                <div style="font-weight:bold;color:#ffb74d;margin-bottom:4px;">② 需求二分</div>
                <div style="color:#ffe0b2;line-height:1.6;">物质需求有限（生物饱和 $\tau_0$）<br>符号欲望无限（信息迭代承载）</div>
              </div>
              <div style="background:rgba(255,152,0,0.08);padding:10px;border-radius:8px;border-left:3px solid #ff9800;">
                <div style="font-weight:bold;color:#ffb74d;margin-bottom:4px;">③ 文明解耦</div>
                <div style="color:#ffe0b2;line-height:1.6;">物质实体文明 + 智能符号文明<br>双文明架构消解核心矛盾</div>
              </div>
              <div style="background:rgba(255,152,0,0.08);padding:10px;border-radius:8px;border-left:3px solid #ff9800;">
                <div style="font-weight:bold;color:#ffb74d;margin-bottom:4px;">④ 范式升维</div>
                <div style="color:#ffe0b2;line-height:1.6;">静态均衡→非均衡动态进化<br>物质稀缺分配→注意力符号构建</div>
              </div>
            </div>
          </div>

          <!-- 三层嵌套架构 -->
          <div style="background:rgba(0,0,0,0.2);padding:12px;border-radius:8px;margin-bottom:12px;border-left:3px solid #ff9800;">
            <div style="font-weight:bold;color:#ffb74d;font-size:0.82em;margin-bottom:10px;">🏛️ 三层嵌套架构（传统→进化→BSD）</div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;font-size:0.63em;">
              <div style="background:rgba(255,152,0,0.08);padding:10px;border-radius:8px;text-align:center;">
                <div style="font-weight:bold;color:#ffb74d;margin-bottom:4px;font-size:0.85em;">低阶</div>
                <div style="font-weight:bold;color:#ffe0b2;margin-bottom:3px;">新古典静态均衡</div>
                <div style="color:#ffcc80;line-height:1.5;">纯物质稀缺<br>供需稳态<br>资源最优配置<br>α₃→0 约束</div>
              </div>
              <div style="background:rgba(255,152,0,0.08);padding:10px;border-radius:8px;text-align:center;">
                <div style="font-weight:bold;color:#ffb74d;margin-bottom:4px;font-size:0.85em;">中阶</div>
                <div style="font-weight:bold;color:#ffe0b2;margin-bottom:3px;">进化非均衡</div>
                <div style="color:#ffcc80;line-height:1.5;">技术创新驱动<br>路径依赖演化<br>自适应试错<br>α₃>θ_evo</div>
              </div>
              <div style="background:rgba(255,152,0,0.08);padding:10px;border-radius:8px;text-align:center;">
                <div style="font-weight:bold;color:#ffb74d;margin-bottom:4px;font-size:0.85em;">高阶</div>
                <div style="font-weight:bold;color:#ffe0b2;margin-bottom:3px;">BSD双文明</div>
                <div style="color:#ffcc80;line-height:1.5;">物质饱和供给<br>符号无限迭代<br>注意力终极稀缺<br>双文明范式</div>
              </div>
            </div>
          </div>

          <!-- 系统性自洽补全概要 -->
          <div style="background:rgba(33,150,243,0.08);padding:12px;border-radius:8px;margin-bottom:8px;border-left:4px solid #42a5f5;">
            <div style="font-weight:bold;color:#64b5f6;font-size:0.82em;margin-bottom:8px;">🔧 系统性自洽补全（8大维度回应学术批评）</div>
            <div style="color:#b0bec5;font-size:0.63em;line-height:1.75;">
              <div style="margin-bottom:3px;"><b>8.1 底层公理</b>：三元公理本源推演链 + 悬论哥德尔处理 + 八阶本体-经济变量形式化映射</div>
              <div style="margin-bottom:3px;"><b>8.2 数学建模</b>：方程定义域+稳定性证明 + 层级涌现替代线性叠加 + 参数标定框架 + 量纲统一规则</div>
              <div style="margin-bottom:3px;"><b>8.3 经济逻辑</b>：稀缺四分法（+技术约束+公共品） + τ₀异质性函数 + 注意力多元约束 + 数字垄断原生特征</div>
              <div style="margin-bottom:3px;"><b>8.4 跨域耦合</b>：经济-伦理-战争联立方程 + 随机冲击项（40卷宗建模） + 战争相变双向效应修正</div>
              <div style="margin-bottom:3px;"><b>8.5 实证落地</b>：参数校准方案（WDI/UN数据） + 5项可证伪预测命题 + 3类数值模拟 + 三方对比实验</div>
              <div style="margin-bottom:3px;"><b>8.6 经典兼容</b>：瓦尔拉斯均衡严格推导（三重约束退化） + 5类金融变量BSD建模 + 行为/计量经济学兼容</div>
              <div><b>8.7 边界约束</b>：术语标准定义锚定 + 后稀缺文明三维量化分界 + 4类失效场景明确界定</div>
            </div>
          </div>

        </div>
'''

# 插入内容
new_content = content[:insert_pos] + economic_core_content + content[insert_pos:]

# 写入文件
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('BSD全域经济元体系核心提炼已成功插入T88章节！')
print('内容包含：核心命题、四大理论突破、三层嵌套架构、系统性自洽补全概要')
print('完整论文保留在 theory_base/L0_总本源层/作者猜想/T88 BSD全域经济元体系.md')
