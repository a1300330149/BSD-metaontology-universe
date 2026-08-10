# -*- coding: utf-8 -*-
"""
在HTML中新增"猜想实证"导航板块，包含T81中国游戏生态拓扑闭合路径内容
"""

html_path = r"c:\Users\13003\OneDrive\桌面\3333333\Agent_v2\新六系本体论_人类易懂版.html"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# ============================================================
# 1. 在导航栏新增"猜想实证"tab（BSD数理之后）
# ============================================================
old_nav = '    <div class="nav-tab" onclick="showSection(\'bsdMath\')">🌊 BSD数理</div>\n    <div class="nav-tab" onclick="showSection(\'hierarchy\')">🌳 层级谱系</div>'
new_nav = '    <div class="nav-tab" onclick="showSection(\'bsdMath\')">🌊 BSD数理</div>\n    <div class="nav-tab" onclick="showSection(\'conjecture\')">🧪 猜想实证</div>\n    <div class="nav-tab" onclick="showSection(\'hierarchy\')">🌳 层级谱系</div>'

if old_nav in content:
    content = content.replace(old_nav, new_nav, 1)
    print("✅ 导航栏已新增「猜想实证」tab")
else:
    print("❌ 未找到导航栏插入点")
    exit(1)

# ============================================================
# 2. 在BSD数理section后插入猜想实证section
# ============================================================

conjecture_section = '''
  <!-- 猜想实证 -->
  <div class="section" id="conjecture">
    <div class="new-section">
      <div class="section-title">🧪 猜想实证：产业生态拓扑场论对照验证</div>
      <div class="new-section-meta">
        <strong>模块编号：</strong>T80-T81 · <strong>核心定位：</strong>以任天堂非平庸拓扑为范本，实证中国游戏产业拓扑平庸判定与闭合路径 · <strong>理论框架：</strong>BSD四层四场+拓扑场论
      </div>

      <!-- T81总览 -->
      <div style="background:linear-gradient(135deg,rgba(76,175,80,0.12),rgba(0,150,136,0.08));padding:20px;border-radius:12px;border:1px solid rgba(76,175,80,0.3);margin-bottom:25px;">
        <div style="font-weight:bold;color:#81c784;margin-bottom:15px;font-size:1.1em;text-align:center;">🎮 T81猜想：中国游戏产业生态拓扑闭合路径</div>
        <div style="font-size:0.85em;color:#c8e6c9;line-height:1.9;margin-bottom:15px;text-align:center;">
          基于任天堂非平庸拓扑范本的对照实证 —— 中国头部厂商与任天堂的核心差距是拓扑层级代差，而非规模营收的量差
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:15px;margin-top:15px;">
          <div style="background:rgba(0,0,0,0.25);padding:12px;border-radius:8px;text-align:center;">
            <div style="color:#81c784;font-weight:bold;font-size:0.9em;margin-bottom:5px;">T81-1</div>
            <div style="font-size:0.78em;color:#e0e0e0;">拓扑平庸判定</div>
            <div style="font-size:0.72em;color:#a5d6a7;margin-top:4px;">置信度 95%</div>
          </div>
          <div style="background:rgba(0,0,0,0.25);padding:12px;border-radius:8px;text-align:center;">
            <div style="color:#64b5f6;font-weight:bold;font-size:0.9em;margin-bottom:5px;">T81-2</div>
            <div style="font-size:0.78em;color:#e0e0e0;">拓扑闭合路径</div>
            <div style="font-size:0.72em;color:#90caf9;margin-top:4px;">置信度 85%</div>
          </div>
          <div style="background:rgba(0,0,0,0.25);padding:12px;border-radius:8px;text-align:center;">
            <div style="color:#ba68c8;font-weight:bold;font-size:0.9em;margin-bottom:5px;">T81-3</div>
            <div style="font-size:0.78em;color:#e0e0e0;">教育人才根因</div>
            <div style="font-size:0.72em;color:#ce93d8;margin-top:4px;">置信度 90%</div>
          </div>
        </div>
      </div>

      <!-- 三家厂商总对标 -->
      <div style="background:rgba(0,0,0,0.25);padding:14px;border-radius:10px;margin-bottom:20px;">
        <div style="color:#a5d6a7;font-weight:bold;margin-bottom:10px;font-size:0.92em;">📊 三家厂商拓扑层级总对标</div>
        <div style="overflow-x:auto;">
          <table style="width:100%;border-collapse:collapse;font-size:0.76em;">
            <tr style="background:rgba(76,175,80,0.15);">
              <th style="padding:8px 6px;border:1px solid rgba(76,175,80,0.3);text-align:left;">对标维度</th>
              <th style="padding:8px 6px;border:1px solid rgba(76,175,80,0.3);text-align:center;">任天堂</th>
              <th style="padding:8px 6px;border:1px solid rgba(76,175,80,0.3);text-align:center;">网易游戏</th>
              <th style="padding:8px 6px;border:1px solid rgba(76,175,80,0.3);text-align:center;">米哈游</th>
            </tr>
            <tr><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);font-weight:bold;">拓扑定性</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;color:#81c784;">低亏格非平庸闭流形</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;color:#ffb74d;">高亏格半闭流形</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;color:#ef9a9a;">单纤维强非平庸开流形</td></tr>
            <tr><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);font-weight:bold;">全域第一陈数</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;color:#81c784;">+1.0</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;color:#ffb74d;">+0.6</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;color:#ef9a9a;">+0.4</td></tr>
            <tr><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);font-weight:bold;">欧拉示性数</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;color:#81c784;">≈ +5</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;color:#ffb74d;">≈ -1</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;color:#ef9a9a;">≈ -2</td></tr>
            <tr><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);font-weight:bold;">核心拓扑优势</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;">六系全闭环</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;">全品类自研</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;">单赛道极致</td></tr>
            <tr><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);font-weight:bold;">核心拓扑短板</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;">边界开放度不足</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;">创新+硬件缺失</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;">赛道+硬件缺失</td></tr>
            <tr><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);font-weight:bold;">对应拓扑层级</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;color:#81c784;">生态级</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;color:#ffb74d;">体系级</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;color:#ef9a9a;">赛道级</td></tr>
          </table>
        </div>
        <p style="margin-top:10px;font-size:0.78em;color:#c8e6c9;text-align:center;"><strong>核心结论：</strong>三家厂商的差距本质是拓扑层级的代差，而非营收、产能、技术的量差。量的堆砌无法改变拓扑层级，只有补全六系拓扑缺口才能实现层级跃迁。</p>
      </div>

      <!-- T81-1 拓扑平庸判定 -->
      <div style="background:rgba(0,0,0,0.25);padding:14px;border-radius:10px;margin-bottom:20px;">
        <div style="color:#81c784;font-weight:bold;margin-bottom:10px;font-size:0.92em;">🔬 T81-1 猜想：拓扑平庸判定</div>
        <div style="font-size:0.78em;color:#e0e0e0;line-height:1.9;">
          <p><strong style="color:#a5d6a7;">命题：</strong>中国头部游戏厂商均处于拓扑平庸态，第一陈数C₁≤0.6，无全维度闭环。</p>
          <p style="color:#81c784;font-weight:bold;margin:10px 0 6px 0;">▸ 任天堂范本（基准）</p>
          <p>低亏格非平庸闭流形，C₁=+1，χ≈5。公理-实体-模态-认知-社会五系强连通核心环，混沌系弱连通，稳态优先+后天生成双重本源特征完整。</p>
          <p style="color:#ffb74d;font-weight:bold;margin:10px 0 6px 0;">▸ 网易（高亏格半闭流形·过渡态）</p>
          <p>国内最接近生态级闭流形的厂商，全品类自研+双自研引擎+工业化体系完整。但受群体投票陷阱制约，混沌系创新通道不畅、IP分散、无硬件闭环，卡在"体系完备但范式不足"的过渡层级。C₁≈+0.6，χ≈-1。</p>
          <p style="color:#ef9a9a;font-weight:bold;margin:10px 0 6px 0;">▸ 米哈游（单纤维强非平庸开流形）</p>
          <p>二次元赛道内拓扑强非平庸，技术+IP+社群形成高内聚赛道级闭环。但缺失硬件基底、全品类覆盖与跨生态延展能力，整体仍属拓扑平庸态。C₁≈+0.4，χ≈-2。</p>
          <p style="color:#64b5f6;font-weight:bold;margin:10px 0 6px 0;">▸ 腾讯（开流形半闭环·流量依赖型）</p>
          <p>依托微信社交流量形成假闭环，社会系-认知系-公理系半连通，但实体系极弱、混沌系近乎断裂。核心闭环依赖外部流量输入，无内生自洽。C₁≈0，χ≈-2。</p>
        </div>
      </div>

      <!-- T81-2 拓扑闭合路径 -->
      <div style="background:rgba(0,0,0,0.25);padding:14px;border-radius:10px;margin-bottom:20px;">
        <div style="color:#64b5f6;font-weight:bold;margin-bottom:10px;font-size:0.92em;">🛤️ T81-2 猜想：拓扑闭合路径</div>
        <div style="font-size:0.78em;color:#e0e0e0;line-height:1.9;">
          <p><strong style="color:#90caf9;">命题：</strong>中国游戏产业可通过"硬件底座→IP矩阵→社群生态→范式创新"四步走实现拓扑闭合。</p>
          <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:10px;margin:12px 0;">
            <div style="background:rgba(66,165,245,0.08);padding:10px;border-radius:8px;border-left:2px solid #64b5f6;">
              <div style="color:#64b5f6;font-weight:bold;font-size:0.85em;margin-bottom:4px;">第一步</div>
              <div style="font-size:0.75em;line-height:1.7;">硬件底座筑基<br>实体系重建<br>陈数 0→+0.3</div>
            </div>
            <div style="background:rgba(66,165,245,0.08);padding:10px;border-radius:8px;border-left:2px solid #64b5f6;">
              <div style="color:#64b5f6;font-weight:bold;font-size:0.85em;margin-bottom:4px;">第二步</div>
              <div style="font-size:0.75em;line-height:1.7;">IP矩阵建构<br>模态+认知深化<br>陈数 +0.3→+0.5</div>
            </div>
            <div style="background:rgba(66,165,245,0.08);padding:10px;border-radius:8px;border-left:2px solid #64b5f6;">
              <div style="color:#64b5f6;font-weight:bold;font-size:0.85em;margin-bottom:4px;">第三步</div>
              <div style="font-size:0.75em;line-height:1.7;">社群生态闭环<br>社会系接入<br>陈数 +0.5→+0.7</div>
            </div>
            <div style="background:rgba(66,165,245,0.1);padding:10px;border-radius:8px;border-left:3px solid #2196f3;">
              <div style="color:#42a5f5;font-weight:bold;font-size:0.85em;margin-bottom:4px;">第四步</div>
              <div style="font-size:0.75em;line-height:1.7;">范式创新内生<br>公理+混沌激活<br>陈数 +0.7→+1.0</div>
            </div>
          </div>
          <p>每一步对应特定的拓扑分支补全与连通度提升，具备明确的拓扑判定指标（陈数、欧拉示性数、连通矩阵），可量化验证与分步实施。</p>
        </div>
      </div>

      <!-- T81-3 教育人才根因 -->
      <div style="background:rgba(0,0,0,0.25);padding:14px;border-radius:10px;margin-bottom:20px;">
        <div style="color:#ba68c8;font-weight:bold;margin-bottom:10px;font-size:0.92em;">🧬 T81-3 猜想：教育人才根因</div>
        <div style="font-size:0.78em;color:#e0e0e0;line-height:1.9;">
          <p><strong style="color:#ce93d8;">命题：</strong>六系教育残缺是中国无法诞生任天堂级生态的底层根因，单一计算机人才体系无法支撑生态级创新。</p>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:12px 0;">
            <div style="background:rgba(76,175,80,0.06);padding:10px;border-radius:8px;">
              <div style="color:#81c784;font-weight:bold;font-size:0.82em;margin-bottom:6px;">任天堂人才结构（六系均衡）</div>
              <div style="font-size:0.72em;line-height:1.8;color:#e0e0e0;">
                公理系：资深制作人、关卡设计大师<br>
                实体系：硬件工程师、工业设计师<br>
                模态系：游戏设计师、编剧、美术总监<br>
                认知系：品牌营销、用户研究、心理学<br>
                社会系：社区运营、线下活动策划<br>
                <span style="color:#a5d6a7;">混沌系：跨界人才（建筑/艺术/音乐等）</span>
              </div>
            </div>
            <div style="background:rgba(244,67,54,0.06);padding:10px;border-radius:8px;">
              <div style="color:#ef9a9a;font-weight:bold;font-size:0.82em;margin-bottom:6px;">国内人才结构（天道单极）</div>
              <div style="font-size:0.72em;line-height:1.8;color:#e0e0e0;">
                公理系：产品经理、数据驱动策划<br>
                实体系：几乎空白<br>
                模态系：策划、原画、3D建模<br>
                认知系：市场投放、数据分析<br>
                社会系：用户运营、内容审核<br>
                <span style="color:#ef9a9a;">混沌系：几乎全为计算机背景（同质化严重）</span>
              </div>
            </div>
          </div>
          <p style="color:#ce93d8;"><strong>拓扑闭环困境：</strong>教育六系残缺 → 人才结构单一 → 生态维度残缺 → 行业吸引力下降 → 人才进一步同质化。仅靠行业内部努力无法突破，必须与教育体系六系改革同步推进。</p>
        </div>
      </div>

      <!-- 全域总结论 -->
      <div style="background:linear-gradient(135deg,rgba(244,67,54,0.12),rgba(156,39,176,0.08));padding:16px;border-radius:10px;border:1px solid rgba(244,67,54,0.25);">
        <div style="color:#ef9a9a;font-weight:bold;margin-bottom:8px;font-size:0.92em;">💡 T81猜想全域总结论</div>
        <div style="font-size:0.78em;color:#e0e0e0;line-height:1.9;">
          <p>中国游戏产业与任天堂的差距，不是努力程度、资金投入、技术能力的量差，而是<strong style="color:#ef9a9a;">文明层级的拓扑代差</strong>——前者是工业文明规模逻辑下的拓扑平庸开流形，后者是数字文明生态逻辑下的非平庸拓扑闭流形。</p>
          <p>这种代差的跨越，无法靠堆规模、堆产能、买IP实现，必须从<strong>教育人才的根因层</strong>和<strong>生态拓扑的结构层</strong>同时发力，完成六系全维度的拓扑闭合，才能真正跃迁到生态级文明的新高度。</p>
          <p style="margin-top:8px;color:#ce93d8;text-align:center;">这不仅是游戏行业的问题，更是整个中国数字文明转型的一个缩影——从"规模取胜"转向"生态取胜"，从"天道单极"转向"六系均衡"，是所有产业在新文明时代都必须面对的拓扑相变命题。</p>
        </div>
      </div>

    </div>
  </div>

'''

# 在层级谱系section之前插入猜想实证section
old_marker = '''  <!-- 层级谱系 -->
  <div class="section" id="hierarchy">'''

new_marker = conjecture_section + '''  <!-- 层级谱系 -->
  <div class="section" id="hierarchy">'''

if old_marker in content:
    content = content.replace(old_marker, new_marker, 1)
    print("✅ 猜想实证section已插入")
else:
    print("❌ 未找到section插入点")
    exit(1)

# 保存
with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

print("\n✅ HTML更新完成：")
print("   - 导航栏新增「猜想实证」tab")
print("   - 新增猜想实证section（包含T81三大子猜想）")
print("   - 包含三家厂商拓扑层级总对标表")
