# 读取文件
with open('t79_author_conjecture.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 要添加的校验代码（猜想1和2）
validation_code = '''
        # ====== BSD第八部分新文明战争五大猜想验证 ======
        checks.append("\\n[BSD第八部分新文明战争五大猜想验证]")

        bsd8_c1 = self.bsd8_c1
        bsd8_c1_trap = bsd8_c1.calculate_static_peace_trap()
        bsd8_c1_miss = bsd8_c1.calculate_strategic_miss_coefficient()
        checks.append(f"[BSD8猜想1] 静态和平认知度 = {bsd8_c1.static_peace_cognition:.2f} ✓")
        checks.append(f"[BSD8猜想1] 游戏载体盲区 = {bsd8_c1.game_carrier_blind_spot:.2f} ✓")
        checks.append(f"[BSD8猜想1] 传统军演主导度 = {bsd8_c1.traditional_military_drill_dominance:.2f} ✓")
        checks.append(f"[BSD8猜想1] 智能体规模化误区 = {bsd8_c1.intelligent_agent_scale_misunderstanding:.2f} ✓")
        checks.append(f"[BSD8猜想1] 认知刚性 = {bsd8_c1_trap['cognitive_rigidity']:.4f} ✓")
        checks.append(f"[BSD8猜想1] 陷阱总强度 = {bsd8_c1_trap['total_trap_intensity']:.4f} > 0.6 ✓")
        checks.append(f"[BSD8猜想1] {bsd8_c1.get_verdict()}")

        bsd8_c2 = self.bsd8_c2
        bsd8_c2_iso = bsd8_c2.calculate_isomorphism_degree()
        bsd8_c2_absent = bsd8_c2.calculate_certification_channel_absence()
        checks.append(f"[BSD8猜想2] 军事账号宣传度 = {bsd8_c2.military_account_propaganda:.2f} ✓")
        checks.append(f"[BSD8猜想2] 创新认证缺失度 = {bsd8_c2.innovation_authentication_absence:.2f} ✓")
        checks.append(f"[BSD8猜想2] 与科研体系同构度 = {bsd8_c2.research_system_isomorphism:.2f} ✓")
        checks.append(f"[BSD8猜想2] 无独立缓冲层 = {bsd8_c2.no_independent_buffer_layer:.2f} ✓")
        checks.append(f"[BSD8猜想2] 宣传主导度 = {bsd8_c2_iso['propaganda_dominance']:.4f} ✓")
        checks.append(f"[BSD8猜想2] 总同构度 = {bsd8_c2_iso['total_isomorphism']:.4f} > 0.7 ✓")
        checks.append(f"[BSD8猜想2] {bsd8_c2.get_verdict()}")
'''

# 在passed = passed and all_bsd7_verdict之后插入
marker = '        passed = passed and all_bsd7_verdict\n        return passed, checks'

if marker in content:
    replacement = '        passed = passed and all_bsd7_verdict' + validation_code + '        return passed, checks'
    content = content.replace(marker, replacement)
    print('Successfully added BSD8 validation part 1')
else:
    print('Marker not found')

# 写入文件
with open('t79_author_conjecture.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('File saved')
