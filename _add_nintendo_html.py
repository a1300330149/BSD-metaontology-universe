# -*- coding: utf-8 -*-
"""
在HTML的BSD数理模块中插入第十二章：应用案例——任天堂生态拓扑场论严格建模
并将原第十二章改为第十三章
"""

import re

html_path = r"c:\Users\13003\OneDrive\桌面\3333333\Agent_v2\新六系本体论_人类易懂版.html"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# 要插入的HTML内容
new_section = '''
      <!-- ================================================== -->
      <!-- 十二、应用案例：任天堂生态拓扑场论严格建模 -->
      <!-- ================================================== -->
      <div style="background:linear-gradient(135deg,rgba(76,175,80,0.12),rgba(0,150,136,0.08));padding:20px;border-radius:12px;border:1px solid rgba(76,175,80,0.3);margin-bottom:25px;">
        <div style="font-weight:bold;color:#81c784;margin-bottom:15px;font-size:1.1em;text-align:center;">🎮 十二、应用案例：任天堂生态的拓扑场论严格建模</div>

        <div style="font-size:0.82em;color:#c8e6c9;line-height:1.9;margin-bottom:15px;text-align:center;">
          任天堂生态是全球游戏产业中唯一达到非平庸拓扑闭流形层级的完整生态系统，是BSD四层四场框架在产业端的典型具象
        </div>

        <!-- 12.1 核心定位 -->
        <div style="background:rgba(0,0,0,0.25);padding:14px;border-radius:10px;margin-bottom:15px;">
          <div style="color:#81c784;font-weight:bold;margin-bottom:10px;font-size:0.92em;">12.1 核心定位：非平庸拓扑闭流形的生态级样本</div>
          <div style="font-size:0.78em;color:#e0e0e0;line-height:1.9;">
            <p>任天堂生态是全球游戏产业中唯一达到<strong>非平庸拓扑闭流形</strong>层级的完整生态系统。其跨数十年的IP生命周期、极强的抗扰动能力、跨世代的生态延续性，本质是<strong>拓扑保护</strong>的动力学结果，而非单纯商业运营的产物。</p>
            <p>从0元本源视角看，任天堂生态完整契合<strong>后天存在生成性</strong>与<strong>稳态优先性</strong>两大本源特征：体拓扑的非平庸性保障了生态的稳态基底，边界态的开放性支撑了持续的创新与增殖，最终形成"闭环而不死板、开放而不涣散"的拓扑稳态结构。</p>
          </div>
        </div>

        <!-- 12.2 六系纤维丛构造 -->
        <div style="background:rgba(0,0,0,0.25);padding:14px;border-radius:10px;margin-bottom:15px;">
          <div style="color:#81c784;font-weight:bold;margin-bottom:10px;font-size:0.92em;">12.2 生态拓扑的六系纤维丛构造</div>
          <div style="font-size:0.78em;color:#e0e0e0;line-height:1.9;">
            <p style="color:#a5d6a7;font-weight:bold;margin-bottom:8px;">▸ 纤维丛三要素定义</p>
            <p><strong>底流形 B</strong>：任天堂硬件标准体系（Switch融合形态+自研引擎+Nintendo Account+平台规则），对应<strong>实体奠基场</strong>核心载体。</p>
            <p><strong>结构群 G</strong>：第一方研发范式与品控规则，"玩法优先、体验闭环"的设计公理，对应<strong>公理规范场</strong>产业具象。</p>
            <p><strong>六系纤维 Fⱼ</strong>：生态的六大结构分支，每支具备独立动力学属性，通过结构群实现拓扑连通。</p>
            <div style="overflow-x:auto;margin:12px 0;">
              <table style="width:100%;border-collapse:collapse;font-size:0.78em;">
                <tr style="background:rgba(76,175,80,0.15);">
                  <th style="padding:8px 6px;border:1px solid rgba(76,175,80,0.3);text-align:center;">纤维</th>
                  <th style="padding:8px 6px;border:1px solid rgba(76,175,80,0.3);text-align:center;">六系对应</th>
                  <th style="padding:8px 6px;border:1px solid rgba(76,175,80,0.3);text-align:left;">任天堂具象</th>
                </tr>
                <tr><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;">F₁</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;">公理系</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);">自研引擎、硬件交互标准、关卡设计范式、易上手难精通公理</td></tr>
                <tr><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;">F₂</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;">实体系</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);">Switch主机、Joy-Con、Ring-Con、Amiibo、主题乐园、周边</td></tr>
                <tr><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;">F₃</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;">模态系</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);">马里奥、塞尔达、宝可梦、动物森友会等数十个长青IP矩阵</td></tr>
                <tr><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;">F₄</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;">认知系</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);">品牌认知、童年情感锚点、家庭友好心智、任天堂式乐趣文化认同</td></tr>
                <tr><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;">F₅</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;">社会系</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);">本地多人、在线社群、家庭聚会、同人创作、玩家社区共识</td></tr>
                <tr><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;">F₆</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;">混沌系</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);">Wii体感、LABO、健身环、Switch融合形态、玩法革命实验</td></tr>
              </table>
            </div>
            <p style="color:#a5d6a7;font-weight:bold;margin:12px 0 8px 0;">▸ 拓扑连通强度矩阵</p>
            <div style="overflow-x:auto;">
              <table style="width:100%;border-collapse:collapse;font-size:0.75em;text-align:center;">
                <tr style="background:rgba(76,175,80,0.15);">
                  <th style="padding:6px;border:1px solid rgba(76,175,80,0.3);"> </th>
                  <th style="padding:6px;border:1px solid rgba(76,175,80,0.3);">公理系</th>
                  <th style="padding:6px;border:1px solid rgba(76,175,80,0.3);">实体系</th>
                  <th style="padding:6px;border:1px solid rgba(76,175,80,0.3);">模态系</th>
                  <th style="padding:6px;border:1px solid rgba(76,175,80,0.3);">认知系</th>
                  <th style="padding:6px;border:1px solid rgba(76,175,80,0.3);">社会系</th>
                  <th style="padding:6px;border:1px solid rgba(76,175,80,0.3);">混沌系</th>
                </tr>
                <tr><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);font-weight:bold;">公理系</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">1.0</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.9</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.95</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.8</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.75</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.6</td></tr>
                <tr><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);font-weight:bold;">实体系</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.9</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">1.0</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.85</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.85</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.9</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.7</td></tr>
                <tr><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);font-weight:bold;">模态系</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.95</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.85</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">1.0</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.95</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.8</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.55</td></tr>
                <tr><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);font-weight:bold;">认知系</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.8</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.85</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.95</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">1.0</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.85</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.5</td></tr>
                <tr><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);font-weight:bold;">社会系</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.75</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.9</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.8</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.85</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">1.0</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.65</td></tr>
                <tr><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);font-weight:bold;">混沌系</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.6</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.7</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.55</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.5</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">0.65</td><td style="padding:5px;border:1px solid rgba(76,175,80,0.2);">1.0</td></tr>
              </table>
            </div>
            <p style="margin-top:10px;"><strong style="color:#a5d6a7;">核心特征</strong>：公理-实体-模态-认知-社会五系形成强连通核心环，混沌系与核心环弱连通，既保障稳态闭环，又保留创新扰动入口，完美匹配稳态优先+后天生成的双重本源要求。</p>
          </div>
        </div>

        <!-- 12.3 拓扑不变量定量计算 -->
        <div style="background:rgba(0,0,0,0.25);padding:14px;border-radius:10px;margin-bottom:15px;">
          <div style="color:#81c784;font-weight:bold;margin-bottom:10px;font-size:0.92em;">12.3 拓扑不变量定量计算</div>
          <div style="font-size:0.78em;color:#e0e0e0;line-height:1.9;">
            <p style="color:#a5d6a7;font-weight:bold;margin-bottom:8px;">▸ 第一陈数：拓扑非平庸度</p>
            <p>第一陈数 C₁ 表征生态纤维丛的拓扑非平庸程度与闭环完整度，为整数拓扑不变量。公式：$$C_1 = \frac{i}{2\pi} \oint_{\mathcal{M}_N} \text{Tr}(F)$$</p>
            <div style="background:rgba(76,175,80,0.08);padding:10px;border-radius:8px;margin:10px 0;border-left:3px solid #81c784;">
              <p><strong>任天堂全生态总陈数：</strong><span style="color:#81c784;font-size:1.1em;">C₁ = +1</span>（非平庸拓扑闭流形，存在完整内生闭环）</p>
              <p style="margin-top:6px;"><strong>分域陈数：</strong></p>
              <ul style="margin:4px 0 4px 20px;">
                <li>第一方核心生态：C₁ = +1.5（强非平庸，完全自洽闭环）</li>
                <li>第三方开发者生态：C₁ = +0.3（弱非平庸，依附核心闭环生长）</li>
                <li>跨界衍生生态：C₁ = +0.2（极弱非平庸，核心生态的边界延伸）</li>
              </ul>
            </div>
            <p style="color:#ef9a9a;font-weight:bold;margin:10px 0 6px 0;">行业对标参考：</p>
            <ul style="margin:4px 0 4px 20px;">
              <li>腾讯游戏生态：C₁ ≈ 0（拓扑平庸，无内生闭环，依赖外部社交流量）</li>
              <li>米哈游生态：C₁ ≈ +0.4（单纤维非平庸，整体拓扑平庸）</li>
              <li>网易游戏生态：C₁ ≈ +0.6（多纤维半连通，未形成闭流形）</li>
            </ul>
            <p style="color:#a5d6a7;font-weight:bold;margin:12px 0 8px 0;">▸ 欧拉示性数：生态韧性指标</p>
            <p>欧拉示性数 χ 表征流形整体连通性与抗扰动能力，值越高、亏格越低，韧性越强。公式：χ = V - E + F</p>
            <p>任天堂：V≈120（IP产品节点），E≈210（联动边），F≈95（生态子域面）</p>
            <div style="background:rgba(76,175,80,0.08);padding:10px;border-radius:8px;margin:10px 0;border-left:3px solid #81c784;">
              <p><strong>计算结果：</strong><span style="color:#81c784;font-size:1.1em;">χ ≈ 5</span>（低亏格定向闭流形，连通性强，抗局部扰动能力极强）</p>
            </div>
            <p style="color:#a5d6a7;font-weight:bold;margin:12px 0 8px 0;">▸ 拓扑纠缠熵：生态内聚度</p>
            <p>拓扑纠缠熵衡量生态各部分之间的非局域关联强度。任天堂生态远高于行业平均——玩家购买的不是单一硬件或游戏，而是整个生态的入场权；单个IP、单款作品的波动，不会动摇整体生态的内聚性。</p>
          </div>
        </div>

        <!-- 12.4 体-边对应原理 -->
        <div style="background:rgba(0,0,0,0.25);padding:14px;border-radius:10px;margin-bottom:15px;">
          <div style="color:#81c784;font-weight:bold;margin-bottom:10px;font-size:0.92em;">12.4 体-边对应原理的生态显化</div>
          <div style="font-size:0.78em;color:#e0e0e0;line-height:1.9;">
            <p>拓扑场论核心定理<strong>体-边对应</strong>在任天堂生态中完全显现：体系统的非平庸拓扑，唯一决定边界上存在受拓扑保护的稳定边界态。这是任天堂生态数十年长青的核心数学根源。</p>
            <p style="color:#a5d6a7;font-weight:bold;margin:12px 0 8px 0;">▸ 三类受拓扑保护的边界态</p>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin:10px 0;">
              <div style="background:rgba(66,165,245,0.08);padding:10px;border-radius:8px;border:1px solid rgba(66,165,245,0.2);">
                <div style="color:#64b5f6;font-weight:bold;margin-bottom:6px;font-size:0.85em;">第一方IP边界态</div>
                <div style="font-size:0.75em;line-height:1.7;">马里奥、塞尔达、宝可梦三大头部IP是最内层边界态，受体拓扑严格保护，生命周期远超行业平均水平。</div>
              </div>
              <div style="background:rgba(255,152,0,0.08);padding:10px;border-radius:8px;border:1px solid rgba(255,152,0,0.2);">
                <div style="color:#ffb74d;font-weight:bold;margin-bottom:6px;font-size:0.85em;">第三方开发者边界态</div>
                <div style="font-size:0.75em;line-height:1.7;">依托硬件标准的第三方生态是中间层边界态。即便个别厂商退出，整体稳定性不受破坏，系统自发填补空缺。</div>
              </div>
              <div style="background:rgba(156,39,176,0.08);padding:10px;border-radius:8px;border:1px solid rgba(156,39,176,0.2);">
                <div style="color:#ba68c8;font-weight:bold;margin-bottom:6px;font-size:0.85em;">玩家社群衍生边界态</div>
                <div style="font-size:0.75em;line-height:1.7;">玩家文化、同人创作、线下衍生是最外层边界态。受体拓扑保护，跨世代延续，是生态最外层的韧性屏障。</div>
              </div>
            </div>
            <p style="color:#a5d6a7;font-weight:bold;margin:12px 0 8px 0;">▸ 拓扑保护的商业实证</p>
            <ul style="margin:4px 0 4px 20px;">
              <li><strong>抗扰动性</strong>：Wii U商业失败并未瓦解生态，Switch推出后快速回归增长——拓扑缺陷的自修复过程</li>
              <li><strong>跨世代连续性</strong>：每次硬件迭代，IP、账号、订阅、存档可平滑传承——拓扑连续性的直接体现</li>
              <li><strong>失败产品的拓扑回归</strong>：Virtual Boy、Wii U属于拓扑亚稳态缺陷，不改变体拓扑非平庸性，最终自发回归主分支</li>
            </ul>
          </div>
        </div>

        <!-- 12.5 拓扑相变 -->
        <div style="background:rgba(0,0,0,0.25);padding:14px;border-radius:10px;margin-bottom:15px;">
          <div style="color:#81c784;font-weight:bold;margin-bottom:10px;font-size:0.92em;">12.5 拓扑相变：任天堂世代演化的本质</div>
          <div style="font-size:0.78em;color:#e0e0e0;line-height:1.9;">
            <p>任天堂每一次硬件世代交替，本质都是<strong>拓扑相变</strong>过程——由创新序参量驱动，从一个拓扑稳态跃迁到另一个拓扑稳态，陈数与欧拉示性数随相变发生阶跃式变化。</p>
            <p style="color:#a5d6a7;font-weight:bold;margin:10px 0 6px 0;">▸ 历次世代的拓扑相变路径</p>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:10px 0;">
              <div style="background:rgba(76,175,80,0.06);padding:10px;border-radius:8px;border-left:2px solid #81c784;">
                <div style="color:#a5d6a7;font-weight:bold;margin-bottom:4px;">① FC/NES时代（1983）</div>
                <div style="font-size:0.75em;">首次拓扑闭合相变：陈数从0→+0.7，建立"硬件-软件-第三方"基础拓扑闭环</div>
              </div>
              <div style="background:rgba(76,175,80,0.06);padding:10px;border-radius:8px;border-left:2px solid #81c784;">
                <div style="color:#a5d6a7;font-weight:bold;margin-bottom:4px;">② SFC时代（1990）</div>
                <div style="font-size:0.75em;">拓扑深化相变：陈数升至+0.85，IP矩阵与品类体系成型，生态走向成熟稳态</div>
              </div>
              <div style="background:rgba(76,175,80,0.06);padding:10px;border-radius:8px;border-left:2px solid #81c784;">
                <div style="color:#a5d6a7;font-weight:bold;margin-bottom:4px;">③ N64/NGC时代</div>
                <div style="font-size:0.75em;">3D化拓扑相变：模态系大规模对称破缺，陈数稳定在+0.9左右，3D游戏范式确立</div>
              </div>
              <div style="background:rgba(76,175,80,0.06);padding:10px;border-radius:8px;border-left:2px solid #81c784;">
                <div style="color:#a5d6a7;font-weight:bold;margin-bottom:4px;">④ Wii时代（2006）</div>
                <div style="font-size:0.75em;">体感扩张相变：陈数峰值达+0.95，用户圈层从核心玩家向全年龄段扩展</div>
              </div>
              <div style="background:rgba(255,152,0,0.06);padding:10px;border-radius:8px;border-left:2px solid #ffb74d;">
                <div style="color:#ffb74d;font-weight:bold;margin-bottom:4px;">⑤ Wii U时代</div>
                <div style="font-size:0.75em;">拓扑缺陷亚稳态：陈数回落至+0.75，但体拓扑未破缺，属于可修复的亚稳态</div>
              </div>
              <div style="background:rgba(76,175,80,0.08);padding:10px;border-radius:8px;border-left:3px solid #4caf50;">
                <div style="color:#81c784;font-weight:bold;margin-bottom:4px;">⑥ Switch时代（2017）</div>
                <div style="font-size:0.75em;">融合式拓扑修复相变：陈数稳定在<strong style="color:#81c784;">+1.0</strong>，进入成熟非平庸拓扑相</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 12.6 九界五论与驻波对应 -->
        <div style="background:rgba(0,0,0,0.25);padding:14px;border-radius:10px;margin-bottom:15px;">
          <div style="color:#81c784;font-weight:bold;margin-bottom:10px;font-size:0.92em;">12.6 九界五论与驻波的拓扑对应</div>
          <div style="font-size:0.78em;color:#e0e0e0;line-height:1.9;">
            <p><strong>九界归属</strong>：主要驻在虚拟模态界（J2）+ 物质实体界（J1）+ 社会秩序界（J4），向精神意识界（J3）深度延伸，整体秩序熵基准值 S' ≈ -0.35</p>
            <p><strong>腾飞五论权重</strong>：真论15% + 正论55% + 逆论20% + 谬论5% + 悬论5%</p>
            <p><strong>驻波动力学本质</strong>：正向驻波（拓扑闭环生态复利、IP价值累积）缓慢增长；负向驻波（硬件迭代风险、市场竞争）周期涨落；净驻波长期正向主导，体拓扑保护让负向驻波永远无法击穿稳态。</p>
          </div>
        </div>

        <!-- 12.7 BSD四层四场全域对应 -->
        <div style="background:linear-gradient(135deg,rgba(76,175,80,0.1),rgba(0,150,136,0.08));padding:14px;border-radius:10px;border:1px solid rgba(76,175,80,0.25);">
          <div style="color:#81c784;font-weight:bold;margin-bottom:10px;font-size:0.92em;">12.7 BSD四层四场全域对应总览</div>
          <div style="overflow-x:auto;">
            <table style="width:100%;border-collapse:collapse;font-size:0.78em;">
              <tr style="background:rgba(76,175,80,0.15);">
                <th style="padding:8px 6px;border:1px solid rgba(76,175,80,0.3);text-align:center;">BSD层级</th>
                <th style="padding:8px 6px;border:1px solid rgba(76,175,80,0.3);text-align:center;">四场归属</th>
                <th style="padding:8px 6px;border:1px solid rgba(76,175,80,0.3);text-align:left;">任天堂对应</th>
                <th style="padding:8px 6px;border:1px solid rgba(76,175,80,0.3);text-align:center;">核心表现</th>
              </tr>
              <tr><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;font-weight:bold;">本体层</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;">拓扑场</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);">六系纤维丛拓扑结构</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;">非平庸闭流形、C₁=+1</td></tr>
              <tr><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;font-weight:bold;">规则层</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;">κ相位场</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);">研发范式、品控规则、连通矩阵</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;">强连通核心环、弱混沌系</td></tr>
              <tr><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;font-weight:bold;">现象层</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;">相变场</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);">世代交替、拓扑相变</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;">六次世代相变、朗道自由能</td></tr>
              <tr><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;font-weight:bold;">具现层</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;">涌现场</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);">生态自组织、IP衍生</td><td style="padding:6px;border:1px solid rgba(76,175,80,0.2);text-align:center;">玩家社群、跨界业态涌现</td></tr>
            </table>
          </div>
          <p style="margin-top:10px;font-size:0.78em;color:#c8e6c9;text-align:center;">本案例验证了BSD数理体系在产业生态分析中的完整适用性，从拓扑结构、相位耦合、相变演化、涌现生成四个层级完整对应，证明了四层四场框架的全域普适性。</p>
        </div>
      </div>

'''

# 找到插入点：原第十二章"统一体系总览"的开始标记
old_marker = "      <!-- ================================================== -->\n      <!-- 十二、统一体系总览 -->\n      <!-- ================================================== -->"

# 替换为：新第十二章 + 原第十二章（改为第十三章）
new_marker = new_section + "      <!-- ================================================== -->\n      <!-- 十三、统一体系总览 -->\n      <!-- ================================================== -->"

if old_marker in content:
    content = content.replace(old_marker, new_marker, 1)
    # 同时更新章节标题中的"十二"为"十三"
    content = content.replace(
        '        <div style="font-weight:bold;color:#ef5350;margin-bottom:15px;font-size:1.1em;text-align:center;">🌌 BSD全体系统一总览</div>',
        '        <div style="font-weight:bold;color:#ef5350;margin-bottom:15px;font-size:1.1em;text-align:center;">🌌 十三、BSD全体系统一总览</div>',
        1
    )
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ 成功插入第十二章（应用案例：任天堂生态拓扑场论严格建模）")
    print("   原第十二章（统一体系总览）已调整为第十三章")
else:
    print("❌ 未找到插入点标记，请检查HTML文件内容")
