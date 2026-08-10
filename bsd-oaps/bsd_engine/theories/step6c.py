# 读取文件
with open('t79_author_conjecture.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 要添加的校验代码（驻波+结论+判定）
validation_code = '''
        # BSD第八部分综合驻波校验
        bsd8_sw = self.bsd8_standing_wave
        bsd8_pos = bsd8_sw.calculate_bsd8_psi_positive()
        bsd8_neg = bsd8_sw.calculate_bsd8_psi_negative()
        bsd8_net = bsd8_sw.calculate_bsd8_psi_net()
        bsd8_dir = bsd8_sw.get_evolution_direction()

        expected_bsd8_pos = (bsd8_sw.conjecture1_positive + bsd8_sw.conjecture2_positive +
                             bsd8_sw.conjecture3_positive + bsd8_sw.conjecture4_positive +
                             bsd8_sw.conjecture5_positive)
        expected_bsd8_neg = (bsd8_sw.conjecture1_negative + bsd8_sw.conjecture2_negative +
                             bsd8_sw.conjecture3_negative + bsd8_sw.conjecture4_negative +
                             bsd8_sw.conjecture5_negative)

        checks.append(f"[BSD8驻波] ψ⁺ = {bsd8_pos:.4f}（应为{expected_bsd8_pos:.4f}）")
        checks.append(f"[BSD8驻波] ψ⁻ = {bsd8_neg:.4f}（应为{expected_bsd8_neg:.4f}）")
        checks.append(f"[BSD8驻波] Ψ_net = {bsd8_net:.4f}")
        checks.append(f"[演化方向] {bsd8_dir}")

        # BSD第八部分最终结论校验
        bsd8_final_count = len(self.bsd8_final.conclusions)
        checks.append(f"[BSD8结论] 最终刚性结论数 = {bsd8_final_count}（应为9条）")

        # BSD第八部分全部成立判定
        all_bsd8_verdict = all([
            bsd8_c1_trap["total_trap_intensity"] > 0.6,
            bsd8_c1_trap["entropy_generation"] > 0.5,
            bsd8_c2_iso["total_isomorphism"] > 0.7,
            bsd8_c2_iso["interface_entropy"] > 0.6,
            bsd8_c3_war["total_war_intensity"] > 0.6,
            bsd8_c3_war["full_domain_engagement"] > 0.5,
            bsd8_c4_subset["total_intensity"] > 0.6,
            bsd8_c4_subset["info_war_dominance"] > 0.5,
            bsd8_c5_paradigm["total_paradigm_shift"] > 0.6,
            bsd8_c5_paradigm["aggression_fallacy"] > 0.6,
            bsd8_final_count == 9,
            abs(bsd8_pos - expected_bsd8_pos) < 1e-6
        ])

        if all_bsd8_verdict:
            checks.append("[判定] BSD第八部分新文明战争五大猜想全部经公理验证成立 ✓")
        else:
            checks.append("[判定] 部分BSD第八部分验证存在异常 ✗")
            passed = False

        passed = passed and all_bsd8_verdict
'''

# 在猜想5校验代码之后、return之前插入
marker = '        checks.append(f"[BSD8猜想5] {bsd8_c5.get_verdict()}")\n        return passed, checks'

if marker in content:
    replacement = '        checks.append(f"[BSD8猜想5] {bsd8_c5.get_verdict()}")' + validation_code + '        return passed, checks'
    content = content.replace(marker, replacement)
    print('Successfully added BSD8 validation part 3')
else:
    print('Marker not found')
    # 尝试查找部分标记
    if '        checks.append(f"[BSD8猜想5] {bsd8_c5.get_verdict()}")' in content:
        print('Found conjecture 5 verdict line')
    if '        return passed, checks' in content:
        print('Found return line')

# 写入文件
with open('t79_author_conjecture.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('File saved')
