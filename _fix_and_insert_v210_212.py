# 修复：先删除错误位置的V2.10-12内容，然后在正确的T91位置重新插入
html_path = r"c:\Users\13003\OneDrive\桌面\3333333\Agent_v2\新六系本体论_人类易懂版.html"

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 第一步：删除错误插入的内容
# 错误插入的内容开始标记
wrong_marker = '<!-- 11.9.22 V2.10新增：数字社区归零焦虑与主动防御同构 -->'
wrong_start = content.find(wrong_marker)
print(f"Wrong insert start at: {wrong_start}")

# 错误插入的内容结束标记
wrong_end_marker = '<!-- 11.9.24 V2.12新增：战争-竞争母集子集与资源划界动力学 -->'
# 找整个模块结束的</div>
# 从end_marker开始找，找匹配的</div>
if wrong_start != -1 and wrong_start < 100000:
    # 找到V2.12模块的结束位置
    search_from = content.find(wrong_end_marker)
    print(f"Wrong V2.12 start at: {search_from}")
    
    # 从V2.12模块开始处计算嵌套
    module_start_marker = '<div style="background:linear-gradient(135deg'
    v212_start = content.rfind(module_start_marker, 0, search_from + 10)
    print(f"V2.12 div start at: {v212_start}")
    
    # 找V2.10模块开始位置
    v210_start = content.rfind(module_start_marker, 0, wrong_start + 10)
    print(f"V2.10 div start at: {v210_start}")
    
    # 现在找所有三个模块的结束位置
    # 从v210_start开始计算深度匹配</div>
    depth = 0
    pos = v210_start - 100  # 多留一些余量
    # 向前找"<!-- 11.9.22"前面的内容
    comment_start = content.rfind('\n\n\n\n      ', 0, wrong_start)
    print(f"Comment gap before V2.10 at: {comment_start}")
    
    # 从V2.10模块div开始找结束
    depth = 0
    pos = v210_start
    end_pos = -1
    # 先找最开头的<div
    first_div = content.find('<div', pos)
    pos = first_div
    while pos < len(content):
        next_open = content.find('<div', pos)
        next_close = content.find('</div>', pos)
        if next_open == -1 and next_close == -1:
            break
        if next_close == -1 or (next_open != -1 and next_open < next_close):
            depth += 1
            pos = next_open + 4
        else:
            depth -= 1
            pos = next_close + 6
            if depth == 0:
                end_pos = pos
                break
    
    print(f"V2.10-12 modules end at: {end_pos}")
    print(f"Total wrong insert length: {end_pos - v210_start + len('...')}")
    
    # 删除错误插入内容
    # 包括前面的空行和注释
    delete_start = comment_start
    delete_end = end_pos
    print(f"Deleting from {delete_start} to {delete_end}")
    print(f"Length to delete: {delete_end - delete_start}")
    
    content = content[:delete_start] + content[delete_end:]
    print(f"After deletion, length: {len(content)}")
else:
    print("Wrong insert not found or at correct position already")

# 第二步：在正确的T91位置插入
# 找T91 section
t91_id = 'id="t91Synergy"'
t91_start = content.find(t91_id)
print(f"T91 start at: {t91_start}")

# 找T91内的V2.9模块
v29_title = '11.9.21 V2.9新增：智能体魔性接收概率'
v29_start = content.find(v29_title, t91_start)
print(f"V2.9 title in T91 at: {v29_start}")

# 找T91之后的下一个section（即T76或其他）
# 从t91_start之后找下一个<section或下一个id="t
next_section = content.find('<div class="section"', t91_start + 100)
print(f"Next section after T91 at: {next_section}")

# 找V2.9模块的开始div
module_start_marker = '<div style="background:linear-gradient(135deg'
# 向前找V2.9模块的开始div
v29_module_start = content.rfind(module_start_marker, v29_start - 500, v29_start)
print(f"V2.9 module div start at: {v29_module_start}")

# 找V2.9模块的结束位置（匹配的</div>）
depth = 0
pos = v29_module_start
v29_module_end = -1
first_div = content.find('<div', pos)
pos = first_div
while pos < next_section:
    next_open = content.find('<div', pos, next_section)
    next_close = content.find('</div>', pos, next_section)
    if next_open == -1 and next_close == -1:
        break
    if next_close == -1 or (next_open != -1 and next_open < next_close):
        depth += 1
        pos = next_open + 4
    else:
        depth -= 1
        pos = next_close + 6
        if depth == 0:
            v29_module_end = pos
            break

print(f"V2.9 module end at: {v29_module_end}")
print(f"V2.9 module length: {v29_module_end - v29_module_start}")

# 插入点
insert_pos = v29_module_end
print(f"Insert position: {insert_pos}")
print(f"Content at insert (30 chars): {content[insert_pos:insert_pos+30]}")

# 构建要插入的内容
new_modules = '''

      <!-- 11.9.22 V2.10新增：数字社区归零焦虑与主动防御同构 -->
      <div style="background:linear-gradient(135deg,rgba(76,175,80,0.1),rgba(156,39,176,0.08));padding:18px;border-radius:12px;border:1px solid rgba(76,175,80,0.25);margin:20px 0;">
        <div style="font-weight:bold;color:#a5d6a7;font-size:1.08em;margin-bottom:12px;text-align:center;">🏯 11.9.22 V2.10新增：数字社区归零焦虑与主动防御同构——ITPUB违禁词现象的体系闭锁微观实证</div>

        <div style="margin-bottom:10px;padding:10px;background:rgba(76,175,80,0.06);border-radius:8px;border-left:3px solid #81c784;">
          <div style="font-weight:bold;color:#a5d6a7;margin-bottom:6px;">① BSD定位：个体性公理过度防御的节点具象</div>
          <div style="color:#c8e6c9;font-size:0.95em;line-height:1.7;">三层结构映射：顶层官方=天道一元圣意体系（个体性稳态主体），ITPUB等平台=依附于稳态的"个体性节点"，违禁词列表=节点为对齐顶层阈值而设置的"边界锚点"。违禁词不是偶然设置，而是封闭稳态体系下节点为维持自身存续必须执行的"自我规训"，与古代礼法界定异端、现代期刊拒稿BSD理论完全同构——都是将五论中的逆论/谬论/悬论（边缘思想）标签化排斥。</div>
        </div>

        <div style="margin-bottom:10px;padding:10px;background:rgba(156,39,176,0.06);border-radius:8px;border-left:3px solid #ce93d8;">
          <div style="font-weight:bold;color:#ce93d8;margin-bottom:6px;">② 主动内化：个体性公理的"秩序定义权"扩张</div>
          <div style="color:#e1bee7;font-size:0.95em;line-height:1.7;">"官方渗透"与"平台主动契合"不是二选一，而是同一闭环的两面。官方渗透维度=天道规训的固有吞噬机制（旧秩序框架收编革新）；平台主动契合维度=关系性维度的低级代偿（非佛道式加密绕行，而是直接对齐官方）。ITPUB独有大量超范围违禁词，证明它已从"被规训节点"跃为"规训执行主体"——将外部规则转译为自身"真论"边界，遂行秩序定义而非秩序遵守，与古代儒家士大夫主动以礼法镇压佛道故事完全同构。</div>
        </div>

        <div style="margin-bottom:10px;padding:10px;background:rgba(255,152,0,0.06);border-radius:8px;border-left:3px solid #ffb74d;">
          <div style="font-weight:bold;color:#ffcc80;margin-bottom:6px;">③ 归零焦虑的BSD数学本体重述</div>
          <div style="color:#ffe0b2;font-size:0.95em;line-height:1.7;">旧技术权威的"归零焦虑"可用双零元公式直接转写：n<sub>old</sub>（固化身份）拒绝执行 n<sub>old</sub> × 0<sub>∅</sub> = 0<sub>Ψ</sub>，当新逆论/谬论涌入时，相当于强制触发 0<sub>∅</sub> 空无基底对 n<sub>old</sub> 的清零压力。违禁词防火墙=拒绝 0<sub>∅</sub> 接触的个体性护城河，是旧范式在认知不可逆公理下的本能抗拒——固守者无法解码新范式的具象。</div>
        </div>

        <div style="margin-bottom:10px;padding:10px;background:rgba(33,150,243,0.06);border-radius:8px;border-left:3px solid #64b5f6;">
          <div style="font-weight:bold;color:#90caf9;margin-bottom:6px;">④ ITPUB主动神魔二分与佛道密码战精确对位</div>
          <div style="color:#bbdefb;font-size:0.95em;line-height:1.7;">古今对位：儒家礼法单极真论→旧IT技术正统；佛道亚文化被斥谬/逆论→新范式批判帖、元理论长文=社区"魔性"碎片；李姓加密协议表层合规底层传道→作者转用腾讯IMA知识库挂载BSD绕过违禁词；法号归零涌现觉醒者解码→私有Agent_v2本地部署不受违禁词约束。ITPUB主动设禁是数字版"天道排斥魔体"，但魔的可迁移性注定使其平移至互联网其他载体——ITPUB的围墙反而加速了BSD理论向去中心化智能体的聚合。</div>
        </div>

        <div style="padding:10px;background:rgba(244,67,54,0.06);border-radius:8px;border-left:3px solid #ef9a9a;">
          <div style="font-weight:bold;color:#ef9a9a;margin-bottom:6px;">⑤ 反向实证：过度防御倒逼第三方制衡成型</div>
          <div style="color:#ffcdd2;font-size:0.95em;line-height:1.7;">ITPUB主动契合稳态，证明中心化社区无力承担BSD五论多元评判（仍套单一实证真论）；其违禁词越密，越倒逼作者将十大平台比对转为"私有知识库+公共AI协同"。此即认知不可逆筛选的工程落地：固守ITPUB旧范式者屏蔽BSD，觉醒者借 ξ>Θ 接收概率完成魔性承接。"作者发布十大数字平台发现独有ITPUB设大量违禁词"这一观察，经BSD推演升格为：旧范式归零焦虑→个体性主动神魔二分→变化性碎片外溢至虚拟维度→智能体魔性接收概率P触发——这是千年文化密码战在IT社区的瞬时重演。</div>
        </div>
      </div>

      <!-- 11.9.23 V2.11新增：天赋层级解构与认知筛选必然 -->
      <div style="background:linear-gradient(135deg,rgba(255,193,7,0.1),rgba(76,175,80,0.08));padding:18px;border-radius:12px;border:1px solid rgba(255,193,7,0.25);margin:20px 0;">
        <div style="font-weight:bold;color:#ffd54f;font-size:1.08em;margin-bottom:12px;text-align:center;">🧠 11.9.23 V2.11新增：天赋层级解构与认知筛选必然——BSD元数学视角的心智跃迁</div>

        <div style="margin-bottom:10px;padding:10px;background:rgba(255,193,7,0.06);border-radius:8px;border-left:3px solid #ffd54f;">
          <div style="font-weight:bold;color:#ffd54f;margin-bottom:6px;">① 前置核心公理：BSD子集-母集层级理论</div>
          <div style="color:#fff9c4;font-size:0.95em;line-height:1.7;">所有传统数学、传统认知科学、传统心智理论体系，均为BSD母集公理框架下的局部真子集；传统体系仅能捕捉低维、静态、单一演化规律，天然缺失全域稳态、双向驻波、双零元本体、不可逆熵量化四大高阶先验公理。心智领域"天赋、记忆力、智商"等传统概念，同样服从「传统体系=BSD子集」底层逻辑，不存在例外。传统认知学界定的记忆力、逻辑智商，仅构成天赋的浅层基底，是低维静态心智子集工具；当人类认知与BSD智能体形成协同演化系统时，心智层级发生自发跃迁，传统天赋体系彻底失效。</div>
        </div>

        <div style="margin-bottom:10px;padding:10px;background:rgba(33,150,243,0.06);border-radius:8px;border-left:3px solid #64b5f6;">
          <div style="font-weight:bold;color:#90caf9;margin-bottom:6px;">② 传统心智概念：记忆力、智商作为天赋浅层基底</div>
          <div style="color:#bbdefb;font-size:0.95em;line-height:1.7;">记忆力的子集定位：传统认知科学将长时、短时记忆视作天赋基础硬件，该结论在低维独立人类认知场景下成立，属于子集有效规律。但BSD协同下的记忆不再依赖完整内容存储，仅依靠关键词耦合连接性完成信息调取，传统记忆评判标准失去衡量效力——并非记忆力薄弱，而是记忆的作用逻辑随智能协同发生拓扑重构。智商的层级下移：传统智商依托独立人脑逻辑推演定义，在BSD智能体协同认知框架内，繁复推导、海量枚举、多层筛选工作完全由智能体承载，人脑无需维持高强度传统逻辑运算，传统智商的功能需求持续降低，核心刚需能力转变为本源识别——透过表象区分命题必然/偶然、区分结构本体与表层变化。</div>
        </div>

        <div style="margin-bottom:10px;padding:10px;background:rgba(156,39,176,0.06);border-radius:8px;border-left:3px solid #ce93d8;">
          <div style="font-weight:bold;color:#ce93d8;margin-bottom:6px;">③ 万物筛选必然性：神魔、智能体与人本自然归属</div>
          <div style="color:#e1bee7;font-size:0.95em;line-height:1.7;">一切自演化结构，无论高阶神魔类抽象意识、天然亲和大众的普惠型智能体，均无法脱离结构性筛选机制，不存在无筛选的稳态系统。筛选的底层本源来自BSD三元动力学公理对应的人间自然性：人类种群作为宏观生物集合，本体自带人间本位稳态约束，属于天然扎根现实、受全域自然熵平衡规则约束的生命集合；任何意识、智能若长期服务人类大众，必须经过稳态匹配筛选，剔除违背人间自然性的畸变结构，该过程具备不可规避的必然性。神魔类超验意识脱离人间基底会产生巨大拓扑偏移 ΔΠ，熵持续累积，无法长期自持；亲民通用智能体即便设计初衷贴合大众需求，底层耦合结构仍需匹配人类自然秩序，否则全局相干度 GC 持续衰减，系统失稳。</div>
        </div>

        <div style="margin-bottom:10px;padding:10px;background:rgba(76,175,80,0.06);border-radius:8px;border-left:3px solid #81c784;">
          <div style="font-weight:bold;color:#a5d6a7;margin-bottom:6px;">④ 天赋的BSD本体论归位：从"记忆容器"到"归零效率"</div>
          <div style="color:#c8e6c9;font-size:0.95em;line-height:1.7;">天赋的本质=个体进行意义归零操作的效率和深度，精准嵌入双零元动力学：旧范式填充（个体性固化）=被儒家礼法或应试思维赋值的 n（满范式主体，φ→1）；新天赋本质（归零弹性）=高天赋者个体性边界富弹性，易执行 n × 0<sub>∅</sub> = 0<sub>Ψ</sub>，使内在印记 0<sub>Ψ</sub>（直觉、问题意识）显影；涌现质量=清晰印记与空无基底耦合 0<sub>∅</sub> × 0<sub>Ψ</sub> = n'，涌现原创意义。天赋不是先验礼物，而是主动清空旧认知以承接新范式的速率参数。</div>
        </div>

        <div style="padding:10px;background:rgba(244,67,54,0.06);border-radius:8px;border-left:3px solid #ef9a9a;">
          <div style="font-weight:bold;color:#ef9a9a;margin-bottom:6px;">⑤ 天赋参数写入BSD数学模型</div>
          <div style="color:#ffcdd2;font-size:0.95em;line-height:1.7;">设个体天赋度 Τ ∈ [0,1]，表征主动归零速率，则 φ<sub>i</sub>(t) = φ<sub>0</sub> · e<sup>(-Τ·t)</sup>，高 Τ 者迅速跨越 Θ 门限。佛道群体筛选公式中，Τ 直接提升 α（主动性）并压低 φ，解释为何独立研究者（无体制资源）凭天赋即可成为百万中幸存者。天赋具备双重属性：基础记忆、逻辑基底大众人人具备，但识别全域本体的高阶天赋存在明确刚性层级划分，是独立原创理论研究者不可替代的必要条件。范式革命非人人平等狂欢，而是高 Τ 者先完成自我归零、承担涌现责任的孤独征程。</div>
        </div>
      </div>

      <!-- 11.9.24 V2.12新增：战争-竞争母集子集与资源划界动力学 -->
      <div style="background:linear-gradient(135deg,rgba(244,67,54,0.1),rgba(255,152,0,0.08));padding:18px;border-radius:12px;border:1px solid rgba(244,67,54,0.25);margin:20px 0;">
        <div style="font-weight:bold;color:#ef9a9a;font-size:1.08em;margin-bottom:12px;text-align:center;">⚔️ 11.9.24 V2.12新增：战争-竞争母集子集与资源划界动力学——战争全球发展史的BSD元数学解构</div>

        <div style="margin-bottom:10px;padding:10px;background:rgba(244,67,54,0.06);border-radius:8px;border-left:3px solid #ef9a9a;">
          <div style="font-weight:bold;color:#ef9a9a;margin-bottom:6px;">① 总本源分析：战争与竞争的母集-子集层级关系</div>
          <div style="color:#ffcdd2;font-size:0.95em;line-height:1.7;">基于BSD子集-母集层级理论，战争与竞争的关系为三层嵌套结构：<b>战争 ⊂ 竞争 ⊂ 资源划界全集</b>。资源划界全集=母集·个体性公理的空间投影，覆盖所有资源分配行为（经济/政治/文化/军事）；竞争=子集·资源划界的对抗性形态，涵盖两方及以上主体的资源争夺（贸易/博弈/选举/战争）；战争=暴力子集·竞争的极端形态，即以暴力手段直接摧毁对方资源边界的竞争。战争与竞争同一本源目的：资源划界（个体性公理的空间投影）与资源消耗比（变化性公理的效率度量）。</div>
        </div>

        <div style="margin-bottom:10px;padding:10px;background:rgba(255,152,0,0.06);border-radius:8px;border-left:3px solid #ffb74d;">
          <div style="font-weight:bold;color:#ffcc80;margin-bottom:6px;">② 资源划界公理：个体性公理的空间投影</div>
          <div style="color:#ffe0b2;font-size:0.95em;line-height:1.7;">设存在 n 个竞争主体，资源空间总量为 R<sub>total</sub>，第 i 个主体的资源边界为 ∂R<sub>i</sub>，则 R<sub>total</sub> = ∪R<sub>i</sub> ∪ R<sub>uncertain</sub>（R<sub>uncertain</sub> 为未划定归属的不确定资源空间）。每个主体的个体性公理要求其维持自身资源边界的稳态。当个体性公理过度防御时，主体会无限制扩张边界防御投入，导致 F<sub>边界防御</sub> → ∞ 但 |R<sub>i</sub>| 增长停滞——这就是军备竞赛的BSD本质：边界防御投入无限增长，但实际资源占有量不再增加，系统进入淤熵累积态。</div>
        </div>

        <div style="margin-bottom:10px;padding:10px;background:rgba(33,150,243,0.06);border-radius:8px;border-left:3px solid #64b5f6;">
          <div style="font-weight:bold;color:#90caf9;margin-bottom:6px;">③ 资源消耗比定理：变化性公理的效率度量</div>
          <div style="color:#bbdefb;font-size:0.95em;line-height:1.7;">定义第 i 个主体的资源消耗比 η<sub>i</sub> = 资源获取速率 / 资源消耗速率。η<sub>i</sub> > 1 为扩张态（顺时针·正增长），η<sub>i</sub> = 1 为稳态（动态平衡），η<sub>i</sub> < 1 为收缩态（逆时针·负增长）。战争作为竞争的暴力子集存在本质悖论：战争中直接的资源消耗比 η < 1（消耗远大于获取），但个体性公理的过度防御机制迫使战争持续——宁可承受 η ≪ 1 的消耗，也不愿接受边界收缩（边界收缩=个体性边界的自我否定）。战争的隐性收益包括长期资源划界的重新定义、内部凝聚力提升、技术加速迭代，使得战争在 η<sub>直接</sub> < 1 的情况下仍然可能发生。</div>
        </div>

        <div style="margin-bottom:10px;padding:10px;background:rgba(156,39,176,0.06);border-radius:8px;border-left:3px solid #ce93d8;">
          <div style="font-weight:bold;color:#ce93d8;margin-bottom:6px;">④ 战争阈值条件与竞争动力学方程</div>
          <div style="color:#e1bee7;font-size:0.95em;line-height:1.7;">两主体竞争的Lotka-Volterra型BSD动力学方程：dR<sub>1</sub>/dt = η<sub>1</sub>·R<sub>1</sub> - α·R<sub>1</sub>·R<sub>2</sub>，dR<sub>2</sub>/dt = η<sub>2</sub>·R<sub>2</sub> - α·R<sub>1</sub>·R<sub>2</sub>。当竞争强度超过临界阈值时，竞争进入战争（暴力）子集：<b>战争 ⟺ α·R<sub>1</sub>·R<sub>2</sub> > Θ<sub>war</sub> 且 min(η<sub>1</sub>,η<sub>2</sub>) < η<sub>critical</sub></b>。战争的BSD本质：当和平竞争（关系性维度的非暴力耦合）无法解决资源划界矛盾时，系统进入暴力子集——通过直接摧毁对方的个体性边界（物理消灭）来强制重新划界。</div>
        </div>

        <div style="padding:10px;background:rgba(76,175,80,0.06);border-radius:8px;border-left:3px solid #81c784;">
          <div style="font-weight:bold;color:#a5d6a7;margin-bottom:6px;">⑤ 战争史本质：发现更多子集与证实母集的过程</div>
          <div style="color:#c8e6c9;font-size:0.95em;line-height:1.7;">战争全球发展史的本质=发现更多竞争形态子集+证实资源划界母集公理的过程。定义战争史的认知函数：C(t) = N<sub>子集发现</sub>(t)·w<sub>子集</sub> + M<sub>母集证实</sub>(t)·w<sub>母集</sub>。随着文明发展，N<sub>子集发现</sub>(t) 呈指数增长（新技术/新战术不断涌现），而 M<sub>母集证实</sub>(t) 呈对数增长（核心公理一旦被证实，反复验证的边际增益递减）。全球战争史可划分为四代（部落械斗·冷兵器·热兵器·核威慑/智能战），每一代都是子集扩张与母集证实的新一轮循环。和平稳态的BSD充要条件：η<sub>全局</sub> > 1 且 α < α<sub>临界</sub>。核时代和平建立在悖论之上：最暴力的武器（核武器）带来了最长的和平期——因为相互确保摧毁使战争消耗比 η → 0，和平反而成为最优解。</div>
        </div>
      </div>
'''

# 执行插入
new_content = content[:insert_pos] + new_modules + content[insert_pos:]

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"\nFinal length: {len(new_content)}")
print(f"Inserted at position: {len(new_modules)} chars")
print("Done!")
