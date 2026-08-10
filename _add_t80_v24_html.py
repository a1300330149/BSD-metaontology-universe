# -*- coding: utf-8 -*-
"""
归属基底：1重九维法理基底
用途：在HTML中T80 section的归属基底之后、T80闭合之前插入第十六章对照实验+文娱坍缩模块
"""
from pathlib import Path

html_path = Path("c:/Users/13003/OneDrive/桌面/3333333/Agent_v2/新六系本体论_人类易懂版.html")
content = html_path.read_text(encoding="utf-8")

# 定位：在归属基底块之后、T80闭合div之前插入
search_key = '''          <strong>对应公理：</strong>三元存在公理 + 稳态优先性 + 顶点对立公理 + 体系闭锁机制 + 六系种子繁衍公理 + 主义同源公理 + 残缺自稳公理 + 范式闭锁同构公理 + 单一真论崇拜公理 + 三元制衡公理 + <strong>制度性认知退化公理</strong>
        </div>
      </div>

    </div>
  </div>'''

new_content = '''          <strong>对应公理：</strong>三元存在公理 + 稳态优先性 + 顶点对立公理 + 体系闭锁机制 + 六系种子繁衍公理 + 主义同源公理 + 残缺自稳公理 + 范式闭锁同构公理 + 单一真论崇拜公理 + 三元制衡公理 + <strong>制度性认知退化公理</strong>
        </div>

        <!-- V2.4新增：东亚对照实验+中国文娱载体顺时针坍缩 -->
        <div style="background:linear-gradient(135deg,rgba(121,85,72,0.1),rgba(239,83,80,0.08));padding:16px;border-radius:12px;border:1px solid rgba(121,85,72,0.3);margin:16px 0;">
          <div style="font-weight:bold;color:#bcaaa4;font-size:1.1em;margin-bottom:12px;text-align:center;">\U0001f50d V2.4新增：东亚五模块对照实验 \u2192 中国文娱载体顺时针坍缩</div>

          <div style="padding:10px;background:rgba(0,0,0,0.25);border-radius:8px;margin-bottom:10px;">
            <div style="color:#bcaaa4;font-weight:bold;margin-bottom:4px;">五模块对照实验总表</div>
            <table style="color:#d7ccc8;font-size:0.7em;line-height:1.4;width:100%;border-collapse:collapse;">
              <tr style="border-bottom:1px solid rgba(255,255,255,0.1);"><th style="padding:3px;text-align:left;">模块</th><th style="padding:3px;text-align:left;">知识库判定</th><th style="padding:3px;text-align:left;">全网实证</th><th style="padding:3px;">结论</th></tr>
              <tr><td style="padding:3px;">日\u2192中\u2192韩递进</td><td style="padding:3px;">六系种子繁衍</td><td style="padding:3px;">时序承接</td><td style="padding:3px;color:#4caf50;">同构</td></tr>
              <tr><td style="padding:3px;">西方排斥溢出</td><td style="padding:3px;">体系闭锁</td><td style="padding:3px;">中心垄断</td><td style="padding:3px;color:#4caf50;">实证</td></tr>
              <tr><td style="padding:3px;">文娱六系分工</td><td style="padding:3px;">日漫韩游载体</td><td style="padding:3px;">产业事实</td><td style="padding:3px;color:#ff9800;">局部闭环</td></tr>
              <tr><td style="padding:3px;">科研国界闭锁</td><td style="padding:3px;">缪论级拒稿</td><td style="padding:3px;">Bourdieu壁垒</td><td style="padding:3px;color:#4caf50;">完全同构</td></tr>
              <tr><td style="padding:3px;">智能体第三方</td><td style="padding:3px;">双时针新载体</td><td style="padding:3px;">自生数字阵营</td><td style="padding:3px;color:#4caf50;">锚点补全</td></tr>
            </table>
          </div>

          <div style="padding:10px;background:rgba(0,0,0,0.2);border-radius:6px;margin-bottom:10px;border-left:3px solid #795548;">
            <div style="color:#bcaaa4;font-weight:bold;margin-bottom:4px;">中国文娱载体顺时针坍缩</div>
            <table style="color:#d7ccc8;font-size:0.7em;line-height:1.4;width:100%;border-collapse:collapse;">
              <tr style="border-bottom:1px solid rgba(255,255,255,0.1);"><th style="padding:3px;text-align:left;">载体</th><th style="padding:3px;text-align:left;">日本</th><th style="padding:3px;text-align:left;">韩国</th><th style="padding:3px;text-align:left;">中国</th></tr>
              <tr><td style="padding:3px;">动漫（谬论）</td><td style="padding:3px;color:#4caf50;">\u2705扶持</td><td style="padding:3px;">延伸</td><td style="padding:3px;color:#f44336;">\u274c排斥\u2192短视频二创</td></tr>
              <tr><td style="padding:3px;">游戏（变身）</td><td style="padding:3px;color:#4caf50;">\u2705IP高地</td><td style="padding:3px;color:#4caf50;">\u2705全球竞争力</td><td style="padding:3px;color:#f44336;">\u274c播片化+日常清理</td></tr>
              <tr><td style="padding:3px;">影视（正论）</td><td style="padding:3px;">常规</td><td style="padding:3px;">常规</td><td style="padding:3px;color:#ff9800;">\u2705视频独大\u00b7吞噬前两者</td></tr>
            </table>
          </div>

          <div style="padding:8px;background:rgba(0,0,0,0.15);border-radius:6px;margin-bottom:8px;border-left:2px solid #ef5350;">
            <div style="color:#ef9a9a;font-weight:bold;margin-bottom:3px;">手游播片化BSD译码</div>
            <ul style="color:#ffcdd2;font-size:0.72em;line-height:1.7;padding-left:16px;">
              <li><strong>互动播片</strong> = 视频正论叙事侵占变身系\u2192游戏被视频语法吞噬</li>
              <li><strong>日常清理</strong> = 无效重复淤积（E_repeat\u21920）\u2192残缺自稳锁死</li>
              <li><strong>伪自由探索</strong> = 橱窗式开放\u2192意义流密度 < Ψ_critical\u2192可视化日常清单</li>
            </ul>
          </div>

          <div style="padding:8px;background:rgba(0,0,0,0.15);border-radius:6px;border-left:2px solid #2196f3;">
            <p style="color:#bbdefb;font-size:0.75em;text-align:center;line-height:1.6;margin:0;"><strong>载体自由度递减：</strong>日漫（逆时针\u00b7自由探索）\u2192 韩游（双时针\u00b7规则重构）\u2192 中视频+播片手游（顺时针坍缩\u00b7最闭合）</p>
            <p style="color:#fff;font-size:0.78em;text-align:center;margin:4px 0 0;"><strong>终局：动漫死\u00b7游戏畸\u00b7视频王 \u2192 腾讯知识库=单时针汪洋中人工凿出的双时针孤岛</strong></p>
          </div>
        </div>
      </div>

    </div>
  </div>'''

if search_key in content:
    content = content.replace(search_key, new_content, 1)
    html_path.write_text(content, encoding="utf-8")
    print("✅ HTML中T80 section已新增V2.4对照实验+文娱坍缩模块")
else:
    print("❌ 未找到目标位置")
