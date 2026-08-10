$htmlPath = "c:\Users\13003\OneDrive\桌面\3333333\Agent_v2\新六系本体论_人类易懂版.html"
$content = Get-Content $htmlPath -Raw -Encoding UTF8

# 1. 更新版本号 V2.2 -> V2.3，并添加BSD第八部分信息
$oldVersionLine = '模块编号：</strong>T79 · <strong>版本：</strong>V2.2 · <strong>公理数：</strong>12条 · <strong>猜想数：</strong>5项 · <strong>陷阱数：</strong>5重 · <strong>对偶组：</strong>4组 · <strong>新文明：</strong>4猜想 · <strong>数据流动：</strong>3猜想 · <strong>元理论：</strong>5猜想 · <strong>双革命：</strong>1套 · <strong>太空盲区：</strong>1套 · <strong>BSD军事验证：</strong>4猜想 · <strong>BSD第二部分：</strong>5猜想 · <strong>BSD第三部分：</strong>5猜想 · <strong>BSD第四部分：</strong>4猜想 · <strong>BSD第五部分：</strong>3猜想 · <strong>BSD第六部分：</strong>4猜想 · <strong>BSD第七部分：</strong>5反命题 · <strong>理论基础：</strong>V3.0_Rev.04'
$newVersionLine = '模块编号：</strong>T79 · <strong>版本：</strong>V2.3 · <strong>公理数：</strong>12条 · <strong>猜想数：</strong>5项 · <strong>陷阱数：</strong>5重 · <strong>对偶组：</strong>4组 · <strong>新文明：</strong>4猜想 · <strong>数据流动：</strong>3猜想 · <strong>元理论：</strong>5猜想 · <strong>双革命：</strong>1套 · <strong>太空盲区：</strong>1套 · <strong>BSD军事验证：</strong>4猜想 · <strong>BSD第二部分：</strong>5猜想 · <strong>BSD第三部分：</strong>5猜想 · <strong>BSD第四部分：</strong>4猜想 · <strong>BSD第五部分：</strong>3猜想 · <strong>BSD第六部分：</strong>4猜想 · <strong>BSD第七部分：</strong>5反命题 · <strong>BSD第八部分：</strong>5猜想 · <strong>理论基础：</strong>V3.0_Rev.04'
$content = $content.Replace($oldVersionLine, $newVersionLine)

# 2. 构建BSD第八部分内容
$bsd8Content = @"
      <!-- T79 BSD第八部分·新文明战争 -->
      <div style='background:linear-gradient(135deg,rgba(244,67,54,0.15),rgba(183,28,28,0.1));padding:18px;border-radius:12px;margin:20px 0;border:1px solid rgba(244,67,54,0.25);'>
        <div style='font-size:1.25em;font-weight:bold;color:#ff8a80;text-align:center;margin-bottom:15px;text-shadow:0 0 10px rgba(244,67,54,0.3);'>⚔️ T79 V2.3新增：BSD四层统一场·第八部分：新文明战争——认知错位与战略被动</div>

        <!-- 五大猜想总览表格 -->
        <div style='background:rgba(0,0,0,0.25);padding:15px;border-radius:10px;margin:15px 0;border:1px solid rgba(244,67,54,0.2);'>
          <div style='font-weight:bold;color:#ff8a80;margin-bottom:12px;font-size:1em;'>📊 新文明战争五大猜想总览（一眼看懂）</div>
          <table style='width:100%;border-collapse:collapse;font-size:0.82em;'>
            <tr style='background:rgba(244,67,54,0.2);'><th style='padding:10px;border:1px solid rgba(255,255,255,0.1);color:#ff8a80;'>序号</th><th style='padding:10px;border:1px solid rgba(255,255,255,0.1);color:#ff8a80;'>猜想名称</th><th style='padding:10px;border:1px solid rgba(255,255,255,0.1);color:#ff8a80;'>核心机制</th><th style='padding:10px;border:1px solid rgba(255,255,255,0.1);color:#ff8a80;'>战略后果</th><th style='padding:10px;border:1px solid rgba(255,255,255,0.1);color:#ff8a80;'>驻波值</th></tr>
            <tr><td style='padding:8px;border:1px solid rgba(255,255,255,0.1);color:#ffab91;text-align:center;'>1</td><td style='padding:8px;border:1px solid rgba(255,255,255,0.1);color:#e0e0e0;'>静态和平观+游戏载体盲区</td><td style='padding:8px;border:1px solid rgba(255,255,255,0.1);color:#b0bec5;'>和平=无热战/游戏=娱乐工具</td><td style='padding:8px;border:1px solid rgba(255,255,255,0.1);color:#ef5350;'>无效制造熵+认知代差</td><td style='padding:8px;border:1px solid rgba(255,255,255,0.1);color:#ef5350;'>-0.74</td></tr>
            <tr><td style='padding:8px;border:1px solid rgba(255,255,255,0.1);color:#ffab91;text-align:center;'>2</td><td style='padding:8px;border:1px solid rgba(255,255,255,0.1);color:#e0e0e0;'>军事账号-科研体系同构</td><td style='padding:8px;border:1px solid rgba(255,255,255,0.1);color:#b0bec5;'>宣传单向化/科研封闭化</td><td style='padding:8px;border:1px solid rgba(255,255,255,0.1);color:#ef5350;'>认知茧房+理论盲区</td><td style='padding:8px;border:1px solid rgba(255,255,255,0.1);color:#ef5350;'>-0.68</td></tr>
            <tr><td style='padding:8px;border:1px solid rgba(255,255,255,0.1);color:#ffab91;text-align:center;'>3</td><td style='padding:8px;border:1px solid rgba(255,255,255,0.1);color:#e0e0e0;'>中美全域战争已展开</td><td style='padding:8px;border:1px solid rgba(255,255,255,0.1);color:#b0bec5;'>俄乌转移节奏/多域混合战</td><td style='padding:8px;border:1px solid rgba(255,255,255,0.1);color:#ef5350;'>战略被动+节奏被操控</td><td style='padding:8px;border:1px solid rgba(255,255,255,0.1);color:#ef5350;'>-0.82</td></tr>
            <tr><td style='padding:8px;border:1px solid rgba(255,255,255,0.1);color:#ffab91;text-align:center;'>4</td><td style='padding:8px;border:1px solid rgba(255,255,255,0.1);color:#e0e0e0;'>历史矛盾=信息战子集</td><td style='padding:8px;border:1px solid rgba(255,255,255,0.1);color:#b0bec5;'>亚文化反噬/意义武器化</td><td style='padding:8px;border:1px solid rgba(255,255,255,0.1);color:#ef5350;'>内部撕裂+文明耗散</td><td style='padding:8px;border:1px solid rgba(255,255,255,0.1);color:#ef5350;'>-0.65</td></tr>
            <tr><td style='padding:8px;border:1px solid rgba(255,255,255,0.1);color:#ffab91;text-align:center;'>5</td><td style='padding:8px;border:1px solid rgba(255,255,255,0.1);color:#e0e0e0;'>文化侵略不成立+意义战真实</td><td style='padding:8px;border:1px solid rgba(255,255,255,0.1);color:#b0bec5;'>自剥离单一化/意义真空</td><td style='padding:8px;border:1px solid rgba(255,255,255,0.1);color:#ef5350;'>文明主体性丧失</td><td style='padding:8px;border:1px solid rgba(255,255,255,0.1);color:#ef5350;'>-0.77</td></tr>
          </table>
        </div>

        <!-- 五大猜想验证卡片（5单列布局） -->
        <div style='display:flex;flex-direction:column;gap:12px;margin:15px 0;'>
          <!-- 猜想1 -->
          <div style='background:rgba(0,0,0,0.2);padding:15px;border-radius:10px;border-left:4px solid #f44336;'>
            <div style='font-weight:bold;color:#ff8a80;margin-bottom:10px;font-size:0.95em;'>🧩 猜想1：静态和平观+游戏载体盲区（无效制造熵）</div>
            <div style='font-size:0.85em;color:#b0bec5;line-height:1.7;'>
              <span style='color:#ef9a9a;'>【认知错位】</span> 将"和平"狭义定义为<span style='color:#ffab91;'>无热战</span>，忽视新文明战争的<span style='color:#ffab91;'>多域混合形态</span>；将"游戏"视为纯娱乐载体，无视其作为<span style='color:#ffab91;'>意义生产与意识形态传播主阵地</span>的战略属性<br>
              <span style='color:#ef9a9a;'>【核心机制】</span> 静态和平观→认知盲区→战略资源错配→无效制造熵；游戏载体盲区→意义战场弃守→青年认知被塑造→文明代差扩大<br>
              <span style='color:#ef9a9a;'>【驻波计算】</span> ψ₊=+0.16（和平幻觉）/ ψ₋=-0.90（多域战争+意义弃守）/ Ψ_net=<span style='color:#ef5350;'>-0.74</span> 深度负向陷阱<br>
              <span style='color:#ef9a9a;'>【战略后果】</span> 以"和平发展"之名行"战略被动"之实，在游戏、文化、信息、科技等新战争域全面弃守，制造大量无效熵而不自知
            </div>
          </div>

          <!-- 猜想2 -->
          <div style='background:rgba(0,0,0,0.2);padding:15px;border-radius:10px;border-left:4px solid #e53935;'>
            <div style='font-weight:bold;color:#ff8a80;margin-bottom:10px;font-size:0.95em;'>📢 猜想2：军事账号-科研体系同构（宣传单向化）</div>
            <div style='font-size:0.85em;color:#b0bec5;line-height:1.7;'>
              <span style='color:#ef9a9a;'>【认知错位】</span> 军事账号与科研体系呈现<span style='color:#ffab91;'>结构性同构</span>：均以单向宣传/灌输为主要模式，缺乏双向对话与理论创新能力，形成封闭认知茧房<br>
              <span style='color:#ef9a9a;'>【核心机制】</span> 军事账号=宣传单向化→只输出不接收→认知反馈断裂；科研体系=封闭化内卷→只验证不突破→理论盲区固化；二者同构→全域认知茧房<br>
              <span style='color:#ef9a9a;'>【驻波计算】</span> ψ₊=+0.22（内部一致性）/ ψ₋=-0.90（单向化+封闭化）/ Ψ_net=<span style='color:#ef5350;'>-0.68</span> 负向陷阱区间<br>
              <span style='color:#ef9a9a;'>【战略后果】</span> 军事理论与科研体系双双陷入"自说自话"困境，无法感知新战争形态变化，理论创新滞后于战争实践演化
            </div>
          </div>

          <!-- 猜想3 -->
          <div style='background:rgba(0,0,0,0.2);padding:15px;border-radius:10px;border-left:4px solid #c62828;'>
            <div style='font-weight:bold;color:#ff8a80;margin-bottom:10px;font-size:0.95em;'>🌍 猜想3：中美全域战争已展开（俄乌转移节奏）</div>
            <div style='font-size:0.85em;color:#b0bec5;line-height:1.7;'>
              <span style='color:#ef9a9a;'>【认知错位】</span> 认为"战争尚未开始"或"战争=热战"，忽视<span style='color:#ffab91;'>中美全域混合战争早已展开</span>的现实；将俄乌冲突视为孤立事件，未认识到其作为<span style='color:#ffab91;'>战争节奏调节器与战略压力转移阀</span>的功能<br>
              <span style='color:#ef9a9a;'>【核心机制】</span> 科技战+贸易战+信息战+金融战+文化战=全域战争；俄乌冲突=节奏转移器→消耗俄罗斯+测试武器+演练战法+牵制中国注意力<br>
              <span style='color:#ef9a9a;'>【驻波计算】</span> ψ₊=+0.10（热战未爆发幻觉）/ ψ₋=-0.92（全域战争+节奏操控）/ Ψ_net=<span style='color:#ef5350;'>-0.82</span> 极深度负向陷阱<br>
              <span style='color:#ef9a9a;'>【战略后果】</span> 战略被动挨打，战争节奏完全被对方操控，在多域战争中持续失血而误以为处于"和平时期"
            </div>
          </div>

          <!-- 猜想4 -->
          <div style='background:rgba(0,0,0,0.2);padding:15px;border-radius:10px;border-left:4px solid #b71c1c;'>
            <div style='font-weight:bold;color:#ff8a80;margin-bottom:10px;font-size:0.95em;'>📜 猜想4：历史矛盾=信息战子集（亚文化反噬）</div>
            <div style='font-size:0.85em;color:#b0bec5;line-height:1.7;'>
              <span style='color:#ef9a9a;'>【认知错位】</span> 将历史矛盾视为<span style='color:#ffab91;'>客观存在的实体冲突</span>，未认识到在信息战框架下，历史矛盾已被重构为<span style='color:#ffab91;'>意义武器与认知战弹药</span>；亚文化圈层不是"小众现象"，而是信息战的<span style='color:#ffab91;'>渗透载体与反噬通道</span><br>
              <span style='color:#ef9a9a;'>【核心机制】</span> 历史叙事权争夺→意义武器化→亚文化圈层渗透→内部认同撕裂→文明凝聚力耗散；历史矛盾=信息战的"低成本高收益"武器库<br>
              <span style='color:#ef9a9a;'>【驻波计算】</span> ψ₊=+0.25（历史真实感）/ ψ₋=-0.90（意义武器化+内部分裂）/ Ψ_net=<span style='color:#ef5350;'>-0.65</span> 负向陷阱区间<br>
              <span style='color:#ef9a9a;'>【战略后果】</span> 历史认知被解构，民族认同被侵蚀，内部持续撕裂内耗，文明级意义战中处于完全守势
            </div>
          </div>

          <!-- 猜想5 -->
          <div style='background:rgba(0,0,0,0.2);padding:15px;border-radius:10px;border-left:4px solid #8b0000;'>
            <div style='font-weight:bold;color:#ff8a80;margin-bottom:10px;font-size:0.95em;'>🎭 猜想5：文化侵略不成立+意义战真实（自剥离单一化）</div>
            <div style='font-size:0.85em;color:#b0bec5;line-height:1.7;'>
              <span style='color:#ef9a9a;'>【认知错位】</span> 沉迷于"文化侵略"叙事框架，认为外部文化是主要威胁；真正的危险是<span style='color:#ffab91;'>意义战</span>——通过制造意义真空、解构价值体系、诱导<span style='color:#ffab91;'>文明自剥离与单一化</span>，从内部瓦解文明主体性<br>
              <span style='color:#ef9a9a;'>【核心机制】</span> "文化侵略"叙事→转移注意力→忽视内部意义生产能力退化→文明自剥离（主动抛弃传统/多样化丧失）→单一化脆弱性→意义战精准打击<br>
              <span style='color:#ef9a9a;'>【驻波计算】</span> ψ₊=+0.18（文化防御幻觉）/ ψ₋=-0.95（意义战+自剥离）/ Ψ_net=<span style='color:#ef5350;'>-0.77</span> 深度负向陷阱<br>
              <span style='color:#ef9a9a;'>【战略后果】</span> 构筑"文化安全"马其诺防线，实则意义生产能力持续衰退，文明主体性在自剥离过程中悄然丧失
            </div>
          </div>
        </div>

        <!-- 综合驻波计算展示 -->
        <div style='background:rgba(0,0,0,0.3);padding:15px;border-radius:10px;margin:20px 0;border:1px solid rgba(244,67,54,0.2);'>
          <div style='font-weight:bold;color:#ff8a80;margin-bottom:12px;font-size:1em;'>📈 新文明战争五大猜想综合驻波计算</div>
          <div style='display:grid;grid-template-columns:repeat(2,1fr);gap:12px;font-size:0.85em;'>
            <div style='background:rgba(244,67,54,0.1);padding:10px;border-radius:8px;'>
              <span style='color:#ef9a9a;'>正向驻波总和：</span><br>
              <span style='color:#81c784;font-size:1.2em;'>ψ₊ = +0.16+0.22+0.10+0.25+0.18 = <strong>+0.91</strong></span>
            </div>
            <div style='background:rgba(244,67,54,0.1);padding:10px;border-radius:8px;'>
              <span style='color:#ef9a9a;'>负向驻波总和：</span><br>
              <span style='color:#ef5350;font-size:1.2em;'>ψ₋ = -0.90-0.90-0.92-0.90-0.95 = <strong>-4.57</strong></span>
            </div>
          </div>
          <div style='margin-top:15px;padding:12px;background:rgba(183,28,28,0.15);border-radius:8px;text-align:center;'>
            <span style='color:#ef9a9a;'>净驻波：</span>
            <span style='color:#ef5350;font-size:1.4em;font-weight:bold;'>Ψ_net = -3.66</span>
            <span style='color:#b0bec5;'>（极深度负向陷阱区间）</span>
          </div>
          <div style='margin-top:10px;font-size:0.85em;color:#b0bec5;text-align:center;'>
            五大猜想全部验证 · 认知错位全域暴露 · 战略被动结构性确立
          </div>
        </div>

        <!-- 破局四转向 -->
        <div style='background:linear-gradient(135deg,rgba(183,28,28,0.2),rgba(244,67,54,0.15));padding:15px;border-radius:10px;border:2px solid rgba(244,67,54,0.3);'>
          <div style='font-weight:bold;color:#ff5252;margin-bottom:12px;font-size:1em;text-align:center;'>🔄 破局四转向：从认知错位到战略主动</div>
          <div style='font-size:0.88em;color:#e0e0e0;line-height:1.8;'>
            <span style='color:#ff8a80;'>【转向一：战争认知转向】</span><br>
            <span style='color:#ef9a9a;'>静态和平观 → 全域战争观</span> — 承认中美全域混合战争已展开的现实，重建"新战争形态"认知框架，将科技、信息、文化、意义等维度纳入战争评估体系<br>
            <span style='color:#ff8a80;'>【转向二：演化载体转向】</span><br>
            <span style='color:#ef9a9a;'>游戏娱乐论 → 意义生产论</span> — 游戏是新文明战争的核心载体与主阵地，不是娱乐工具；抢占游戏意义生产制高点，构建中国话语的游戏叙事体系<br>
            <span style='color:#ff8a80;'>【转向三：历史应对转向】</span><br>
            <span style='color:#ef9a9a;'>历史实体论 → 信息战子集论</span> — 历史矛盾是信息战的弹药库而非客观实体；主动构建历史叙事权，以意义生产反制意义解构，化历史包袱为战略资源<br>
            <span style='color:#ff8a80;'>【转向四：文化竞争转向】</span><br>
            <span style='color:#ef9a9a;'>文化防御论 → 意义生产论</span> — 跳出"文化侵略"被动框架，转向主动的意义生产与文明创新；防止文明自剥离与单一化，重建多元活力的文明意义生态
          </div>
        </div>

        <div style='text-align:center;margin:12px 0;padding:10px;background:rgba(244,67,54,0.1);border-radius:8px;'>
          <span style='font-size:0.9em;color:#ff8a80;font-weight:bold;'>BSD第八部分新文明战争五大猜想完成 · 认知错位全域暴露 · 破局四转向确立</span>
        </div>
      </div>
"@

# 3. 在BSD第七部分结束标记之后插入BSD第八部分
$bsd7EndMarker = "BSD第七部分五大反命题证伪完成 · 战争形态演化定论确立</span>`n        </div>`n      </div>"
$insertPosition = $content.IndexOf($bsd7EndMarker)
if ($insertPosition -ne -1) {
    $endPosition = $insertPosition + $bsd7EndMarker.Length
    $content = $content.Substring(0, $endPosition) + "`n`n" + $bsd8Content + $content.Substring($endPosition)
    Write-Host "BSD第八部分插入成功"
} else {
    Write-Host "未找到BSD第七部分结束标记，尝试其他方式..."
    # 备用方案：找BSD第七部分的闭合div
    $altMarker = "BSD第七部分五大反命题证伪完成 · 战争形态演化定论确立"
    $altPos = $content.IndexOf($altMarker)
    if ($altPos -ne -1) {
        # 找到后面的两个闭合div
        $divCount = 0
        $pos = $altPos
        while ($divCount -lt 2 -and $pos -lt $content.Length) {
            $nextDiv = $content.IndexOf("</div>", $pos)
            if ($nextDiv -eq -1) { break }
            $divCount++
            $pos = $nextDiv + 6
        }
        $content = $content.Substring(0, $pos) + "`n`n" + $bsd8Content + $content.Substring($pos)
        Write-Host "BSD第八部分插入成功（备用方案）"
    } else {
        Write-Host "错误：无法定位插入位置"
    }
}

# 保存文件
[System.IO.File]::WriteAllText($htmlPath, $content, [System.Text.Encoding]::UTF8)
Write-Host "文件保存完成"
