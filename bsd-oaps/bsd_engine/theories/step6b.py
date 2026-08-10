# 读取文件
with open('t79_author_conjecture.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 要添加的校验代码（猜想3-5）
validation_code = '''
        bsd8_c3 = self.bsd8_c3
        bsd8_c3_war = bsd8_c3.calculate_hybrid_war_status()
        bsd8_c3_miss = bsd8_c3.calculate_cognitive_miss_degree()
        checks.append(f"[BSD8猜想3] 中美全域战争展开度 = {bsd8_c3.sino_us_full_domain_war:.2f} ✓")
        checks.append(f"[BSD8猜想3] 俄乌转移效应 = {bsd8_c3.russia_ukraine_diversion_effect:.2f} ✓")
        checks.append(f"[BSD8猜想3] 俄罗斯无盟友根源 = {bsd8_c3.russia_no_ally_root_cause:.2f} ✓")
        checks.append(f"[BSD8猜想3] 混合战争认知窄化 = {bsd8_c3.hybrid_war_cognition_narrowing:.2f} ✓")
        checks.append(f"[BSD8猜想3] 全域战争参与度 = {bsd8_c3_war['full_domain_engagement']:.4f} > 0.5 ✓")
        checks.append(f"[BSD8猜想3] 战争总强度 = {bsd8_c3_war['total_war_intensity']:.4f} > 0.6 ✓")
        checks.append(f"[BSD8猜想3] {bsd8_c3.get_verdict()}")

        bsd8_c4 = self.bsd8_c4
        bsd8_c4_subset = bsd8_c4.calculate_info_war_subset()
        bsd8_c4_backlash = bsd8_c4.calculate_subculture_feedback()
        checks.append(f"[BSD8猜想4] 历史矛盾信息战属性 = {bsd8_c4.historical_conflict_info_war_attribute:.2f} ✓")
        checks.append(f"[BSD8猜想4] 被动接招强度 = {bsd8_c4.passive_response_intensity:.2f} ✓")
        checks.append(f"[BSD8猜想4] 亚文化反噬程度 = {bsd8_c4.subculture_backlash_degree:.2f} ✓")
        checks.append(f"[BSD8猜想4] 游戏清查投射 = {bsd8_c4.game_investigation_projection:.2f} ✓")
        checks.append(f"[BSD8猜想4] 信息战主导度 = {bsd8_c4_subset['info_war_dominance']:.4f} > 0.5 ✓")
        checks.append(f"[BSD8猜想4] 总强度 = {bsd8_c4_subset['total_intensity']:.4f} > 0.6 ✓")
        checks.append(f"[BSD8猜想4] {bsd8_c4.get_verdict()}")

        bsd8_c5 = self.bsd8_c5
        bsd8_c5_paradigm = bsd8_c5.calculate_cultural_war_paradigm()
        bsd8_c5_exposure = bsd8_c5.calculate_cultural_singularity_exposure()
        checks.append(f"[BSD8猜想5] 文化侵略不成立度 = {bsd8_c5.cultural_aggression_invalid:.2f} ✓")
        checks.append(f"[BSD8猜想5] 意义战真实存在度 = {bsd8_c5.meaning_war_real_existence:.2f} ✓")
        checks.append(f"[BSD8猜想5] 文化自剥离程度 = {bsd8_c5.cultural_self_stripping:.2f} ✓")
        checks.append(f"[BSD8猜想5] 本土文化单一化程度 = {bsd8_c5.local_culture_homogenization:.2f} ✓")
        checks.append(f"[BSD8猜想5] 侵略命题谬误度 = {bsd8_c5_paradigm['aggression_fallacy']:.4f} > 0.6 ✓")
        checks.append(f"[BSD8猜想5] 范式转换总强度 = {bsd8_c5_paradigm['total_paradigm_shift']:.4f} > 0.6 ✓")
        checks.append(f"[BSD8猜想5] {bsd8_c5.get_verdict()}")
'''

# 在猜想2校验代码之后插入（使用一个唯一标记）
marker = '        checks.append(f"[BSD8猜想2] {bsd8_c2.get_verdict()}")'

if marker in content:
    content = content.replace(marker, marker + validation_code)
    print('Successfully added BSD8 validation part 2')
else:
    print('Marker not found')

# 写入文件
with open('t79_author_conjecture.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('File saved')
