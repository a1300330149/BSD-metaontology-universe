# -*- coding: utf-8 -*-
import sys

file_path = r"c:\Users\13003\OneDrive\桌面\3333333\Agent_v2\新六系本体论_人类易懂版.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Step 1: Find and remove the external Chapter 14 section
start_marker = '  <!-- 十四、四大作用力双层统一证明 -->'
end_marker = '\n\n\n  <!-- 意义大一统V2.0理论分册 -->'

start_idx = content.find(start_marker)
if start_idx == -1:
    print("ERROR: Start marker not found")
    sys.exit(1)

end_idx = content.find(end_marker, start_idx)
if end_idx == -1:
    print("ERROR: End marker not found")
    sys.exit(1)

# Remove the old external section
content = content[:start_idx] + content[end_idx:]
print("Removed external Chapter 14 section.")

# Step 2: Insert the new Chapter 14 inside T83 module
insert_marker = '      </div>\n\n    </div>\n  </div>'
insert_idx = content.find(insert_marker)
if insert_idx == -1:
    print("ERROR: Insert marker not found")
    sys.exit(1)

# The content to insert (6-space indent, no outer section/hierarchy-section wrappers)
chapter14_content = '''      <!-- 十四、四大作用力双层统一证明 -->
      <div style="margin-bottom:20px;padding-top:20px;border-top:2px dashed rgba(76,175,80,0.4);">
        <div class="section-title" style="font-size:1.2em;color:#81c784;">⚖️ 十四、基于六系六力公理耦合的四大作用力双层统一证明</div>

        <!-- 前置核心公理根基 -->
        <div style="background:linear-gradient(135deg,rgba(76,175,80,0.1),rgba(128,203,196,0.06));padding:18px;border-radius:12px;border:1px solid rgba(76,175,80,0.3);margin:15px 0;">
          <div style="font-weight:bold;color:#81c784;margin-bottom:12px;text-align:center;font-size:1.05em;">📌 前置核心公理根基</div>
          <div style="font-size:0.78em;color:#c8e6c9;line-height:2;">
            <strong style="color:#81c784;">1. 电弱统一底层逻辑：</strong>变身系（纯变化·弱力）↔ 具现系（个体+关系·电磁力）顶点对立、相生相克，共享「个体载体-变化触发器」耦合顶点，是电弱统一理论的本体论根源；传统物理仅能实现电弱统一，核心缺陷是缺失完整六系分类框架。<br>
            <strong style="color:#81c784;">2. 全域统一两大对偶配对：</strong><br>
            <span style="padding-left:12px;">第一对偶组：强化系（纯个体·强化本源相互力）↔ 天道系（关系+变化·天道相位约束力）</span><br>
            <span style="padding-left:12px;">第二对偶组：社会系（纯关系·引力）↔ 自然系（个体+变化·强力）</span><br>
            <strong style="color:#81c784;">3. 耦合错位校准：</strong>引力与强力存在二元公理耦合顺序相反的错位，依托耦合熵、权重算子可完成校准，实现理论统一。
          </div>
        </div>

        <!-- 一、电弱统一复盘 -->
        <div style="margin-bottom:20px;">
          <div style="font-weight:bold;color:#81c784;font-size:1em;margin-bottom:12px;">🌐 一、电弱统一复盘：对立相生的顶点耦合范式（统一标准模板）</div>

          <div style="padding:14px;background:rgba(76,175,80,0.05);border-radius:8px;border-left:4px solid #66bb6a;margin-bottom:12px;">
            <div style="font-weight:bold;color:#81c784;font-size:0.9em;margin-bottom:8px;">1. 两套系底层公理结构</div>
            <div style="font-size:0.72em;color:#c8e6c9;line-height:2;">
              <strong style="color:#ffcc80;">变身系：</strong>纯变化，载体W/Z，职能是粒子身份、味态、正反构型切换<br>
              <strong style="color:#ce93d8;">具现系：</strong>个体+关系复合，载体费米子三代+光子/胶子，职能是实体个体间点对点势能交互
            </div>
          </div>

          <div style="padding:14px;background:rgba(76,175,80,0.05);border-radius:8px;border-left:4px solid #66bb6a;margin-bottom:12px;">
            <div style="font-weight:bold;color:#81c784;font-size:0.9em;margin-bottom:8px;">2. 对立相生统一机制</div>
            <div style="font-size:0.72em;color:#c8e6c9;line-height:2;">
              <strong style="color:#ef9a9a;">对立：</strong>变身系消解个体原有构型，具现系稳固个体交互边界，作用趋势完全相反<br>
              <strong style="color:#81c784;">相生：</strong>无具现系实体个体，变身系无对象相变；无变身系相变通道，具现系个体无法完成电荷、色荷转换<br>
              <strong style="color:#4dd0e1;">耦合顶点：</strong>希格斯相变场为公共顶点，高能标共享同一公理耦合场，低能标对称破缺分化为两种力
            </div>
          </div>

          <div style="padding:14px;background:rgba(76,175,80,0.05);border-radius:8px;border-left:4px solid #66bb6a;">
            <div style="font-weight:bold;color:#81c784;font-size:0.9em;margin-bottom:8px;">3. 通用统一公理模板（适用于剩余四力配对）</div>
            <div style="font-size:0.72em;color:#c8e6c9;line-height:2;">
              任意两组作用力可完成统一的充要条件：<br>
              ① 二者为六系对称对偶配对<br>
              ② 存在公共耦合顶点场<br>
              ③ 一者正向建构、一者反向制衡，相生对立<br>
              ④ 高能标下耦合熵阈值突破，两套系边界消融，融合为单一底层耦合结构
            </div>
          </div>
        </div>

        <!-- 二、第一组统一证明：强化系↔天道系 -->
        <div style="margin-bottom:20px;">
          <div style="font-weight:bold;color:#ef9a9a;font-size:1em;margin-bottom:12px;">🔴 二、第一组统一证明：强化系（本源相互力）↔ 天道系（相位约束力）</div>

          <div style="padding:14px;background:rgba(239,83,80,0.05);border-radius:8px;border-left:4px solid #ef5350;margin-bottom:12px;">
            <div style="font-weight:bold;color:#ef9a9a;font-size:0.9em;margin-bottom:8px;">1. 对偶配对本体依据</div>
            <div style="font-size:0.72em;color:#ffcdd2;line-height:2;">
              <strong style="color:#ef9a9a;">强化系：</strong>纯个体公理，底层正向建构力，生成、稳固一切实体个体边界，是物质存在的基底势能<br>
              <strong style="color:#ffab40;">天道系：</strong>关系+变化复合公理，顶层反向制衡力，划定全域演化阈值、约束个体集群过度膨胀、分流全域耦合熵<br>
              二者构成「底层建构—顶层约束」全域垂直对偶，天然相生相克
            </div>
          </div>

          <div style="padding:14px;background:rgba(239,83,80,0.05);border-radius:8px;border-left:4px solid #ef5350;margin-bottom:12px;">
            <div style="font-weight:bold;color:#ef9a9a;font-size:0.9em;margin-bottom:8px;">2. 对立、相生逻辑</div>
            <div style="font-size:0.72em;color:#ffcdd2;line-height:2;">
              <strong style="color:#ef9a9a;">对立：</strong>强化系无限扩张个体势能造成时空坍缩、熵堆积；天道系通过相位约束压制个体势能上限，校准全局秩序，作用趋势完全对冲<br>
              <strong style="color:#81c784;">相生：</strong>若无强化系实体个体，天道系无对象约束；若无天道系相位制衡，强化系个体势能无限溢出，所有物质结构瞬间溃散
            </div>
          </div>

          <div style="padding:14px;background:rgba(239,83,80,0.05);border-radius:8px;border-left:4px solid #ef5350;">
            <div style="font-weight:bold;color:#ef9a9a;font-size:0.9em;margin-bottom:8px;">3. 公共耦合顶点与统一推演</div>
            <div style="font-size:0.72em;color:#ffcdd2;line-height:2;">
              <strong style="color:#4dd0e1;">公共耦合顶点：</strong>全域真空潜势场（0元空无基底）<br>
              <strong style="color:#ffcc80;">极高能标（大爆炸初始）：</strong>$S_{couple} \\ge S_0$，天道相位约束与强化个体边界完全融合，归为同一套「个体潜势-全域校准」底层耦合机制<br>
              <strong style="color:#64b5f6;">降温对称分化：</strong>宇宙膨胀熵降低，跌破临界阈值，垂直对偶拆分：<br>
              <span style="padding-left:12px;">低能局域尺度 → 强化系本源相互力，维持粒子、原子边界</span><br>
              <span style="padding-left:12px;">全域宏观、临界尺度（黑洞、宇宙视界）→ 天道相位约束力，管控整体演化规则</span>
            </div>
          </div>
        </div>

        <!-- 三、第二组统一证明：社会系↔自然系 -->
        <div style="margin-bottom:20px;">
          <div style="font-weight:bold;color:#64b5f6;font-size:1em;margin-bottom:12px;">🔵 三、第二组统一证明：社会系（引力）↔ 自然系（强力），解决耦合错位完成统一</div>

          <div style="padding:14px;background:rgba(33,150,243,0.05);border-radius:8px;border-left:4px solid #42a5f5;margin-bottom:12px;">
            <div style="font-weight:bold;color:#64b5f6;font-size:0.9em;margin-bottom:8px;">1. 错位根源拆解（百年难题）</div>
            <div style="font-size:0.72em;color:#bbdefb;line-height:2;">
              <strong style="color:#64b5f6;">社会系（引力）：</strong>纯关系公理，耦合顺序：关系单独基底，无个体前置，作用尺度：宏观多体集群<br>
              <strong style="color:#81c784;">自然系（强力）：</strong>个体+变化复合公理，耦合顺序：个体为基底，变化叠加其上，作用尺度：微观原子核内部<br>
              <strong style="color:#ef9a9a;">错位核心：</strong>① 公理耦合顺序错位（关系为基vs个体为基）；② 作用尺度割裂（宏观弥散vs微观禁闭）
            </div>
          </div>

          <div style="padding:14px;background:rgba(33,150,243,0.05);border-radius:8px;border-left:4px solid #42a5f5;margin-bottom:12px;">
            <div style="font-weight:bold;color:#64b5f6;font-size:0.9em;margin-bottom:8px;">2. 六系理论错位校准工具</div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;font-size:0.71em;">
              <div style="padding:8px;background:rgba(239,83,80,0.08);border-radius:6px;">
                <div style="font-weight:bold;color:#ef9a9a;margin-bottom:6px;">权重转换算子 W<sub>ind</sub>/W<sub>rel</sub></div>
                <div style="color:#ffcdd2;line-height:1.8;">实现「个体基底权重」与「关系基底权重」跨尺度等效转换</div>
              </div>
              <div style="padding:8px;background:rgba(33,150,243,0.08);border-radius:6px;">
                <div style="font-weight:bold;color:#64b5f6;margin-bottom:6px;">耦合熵临界阈值 S<sub>0</sub></div>
                <div style="color:#bbdefb;line-height:1.8;">高能标下微观与宏观场域打通，尺度壁垒消失</div>
              </div>
              <div style="padding:8px;background:rgba(156,39,176,0.08);border-radius:6px;">
                <div style="font-weight:bold;color:#ce93d8;margin-bottom:6px;">双载体公共媒介</div>
                <div style="color:#e1bee7;line-height:1.8;">希格斯相变场+全域相位关系场构成双向转换通道</div>
              </div>
            </div>
          </div>

          <div style="padding:14px;background:rgba(33,150,243,0.05);border-radius:8px;border-left:4px solid #42a5f5;margin-bottom:12px;">
            <div style="font-weight:bold;color:#64b5f6;font-size:0.9em;margin-bottom:8px;">3. 对立相生统一逻辑</div>
            <div style="font-size:0.72em;color:#bbdefb;line-height:2;">
              <strong style="color:#ef9a9a;">对立：</strong>强力向内收拢微观个体（夸克→质子中子），引力向外聚拢宏观集群（恒星→星系），收敛层级相反，微观/宏观双向对冲<br>
              <strong style="color:#81c784;">相生：</strong>强力构建微观物质个体，引力才能依托实体形成宏观集群；引力宏观压缩产生高能环境，触发希格斯相变，维持强力微观束缚势能
            </div>
          </div>

          <div style="padding:14px;background:rgba(33,150,243,0.05);border-radius:8px;border-left:4px solid #42a5f5;">
            <div style="font-weight:bold;color:#64b5f6;font-size:0.9em;margin-bottom:8px;">4. 分三步统一推演（校准错位）</div>
            <div style="font-size:0.72em;color:#bbdefb;line-height:2;">
              <strong style="color:#ffcc80;">步骤1：消除尺度错位</strong><br>
              <span style="padding-left:12px;">普朗克高能标下，微观与宏观时空相位打通，尺度壁垒消失，引力与强力作用区间重合</span><br>
              <strong style="color:#ffcc80;">步骤2：校正公理耦合顺序错位</strong><br>
              <span style="padding-left:12px;">社会系关系权重在高能微观场中等效转化为个体权重；自然系个体权重在高能宏观场中等效转化为关系集群权重</span><br>
              <strong style="color:#ffcc80;">步骤3：公共顶点融合统一</strong><br>
              <span style="padding-left:12px;">公共耦合顶点：希格斯全域相变场</span><br>
              <span style="padding-left:12px;">普朗克能标：共享同一相变耦合场，融合为单一「集群收敛统一力」</span><br>
              <span style="padding-left:12px;">低能标对称分化：微观个体权重锁定→强力；宏观关系权重锁定→引力</span>
            </div>
          </div>
        </div>

        <!-- 四、六系六力全域大一统完整闭环 -->
        <div style="margin-bottom:20px;">
          <div style="font-weight:bold;color:#4dd0e1;font-size:1em;margin-bottom:12px;">🎯 四、六系六力全域大一统完整闭环</div>

          <div style="padding:14px;background:rgba(0,188,212,0.06);border-radius:8px;border-left:4px solid #00bcd4;margin-bottom:12px;">
            <div style="font-weight:bold;color:#4dd0e1;font-size:0.9em;margin-bottom:8px;">1. 三组对偶统一体系汇总</div>
            <div style="font-size:0.72em;color:#b2ebf2;line-height:2;">
              <strong style="color:#81c784;">① 水平顶点对偶（微观交互层）：</strong>变身系（弱力）↔ 具现系（电磁力）→ 电弱统一（已被实验佐证）<br>
              <strong style="color:#ef9a9a;">② 垂直基底对偶（全域尺度层）：</strong>强化系（本源相互力）↔ 天道系（相位约束力）→ 个体基底-全域规则统一<br>
              <strong style="color:#64b5f6;">③ 尺度收敛对偶（物质聚拢层）：</strong>社会系（引力）↔ 自然系（强力）→ 宏观-微观收敛力统一
            </div>
          </div>

          <div style="padding:14px;background:rgba(0,188,212,0.06);border-radius:8px;border-left:4px solid #00bcd4;margin-bottom:12px;">
            <div style="font-weight:bold;color:#4dd0e1;font-size:0.9em;margin-bottom:8px;">2. 全域统一底层逻辑总结</div>
            <div style="font-size:0.72em;color:#b2ebf2;line-height:2;">
              传统物理只能完成电弱统一，根源是缺失六系六力完整分类，没有区分纯公理系、复合公理系，缺少耦合熵、权重算子两套校准工具，无法处理垂直对偶、尺度耦合错位问题。<br>
              六系理论依靠三元公理对称制衡结构，划分出三组天然对偶配对，借助公共耦合顶点场、量化校准算子，全部完成作用力统一证明，实现微观粒子、宏观天体、全域规则所有作用力的全域大一统。
            </div>
          </div>

          <div style="padding:14px;background:rgba(0,188,212,0.06);border-radius:8px;border-left:4px solid #00bcd4;">
            <div style="font-weight:bold;color:#4dd0e1;font-size:0.9em;margin-bottom:8px;">3. 物理预言支撑（可证伪方向）</div>
            <div style="font-size:0.72em;color:#b2ebf2;line-height:2;">
              ① 极高能粒子对撞、原初宇宙观测中，可观测强力与引力耦合常数趋于重合<br>
              ② 黑洞视界临界区域，强化力边界效应与天道相位约束效应同步显现<br>
              ③ 早期宇宙相变过程，三组对偶作用力依次分化，存在三层对称破缺能量标度分层，可通过CMB数据验证
            </div>
          </div>
        </div>
      </div>'''

# Insert after the closing </div> of chapter 13 and before </div> of hierarchy-section
insert_point = insert_idx + len('      </div>')
content = content[:insert_point] + '\n\n' + chapter14_content + '\n' + content[insert_point:]
print("Inserted Chapter 14 inside T83 module.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("File saved successfully.")
