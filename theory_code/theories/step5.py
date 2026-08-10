# 读取文件
with open('t79_author_conjecture.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 要添加的字段
new_fields = '''
    # BSD第八部分五大猜想验证
    bsd8_c1: StaticPeaceTrap = field(default_factory=StaticPeaceTrap)
    bsd8_c2: MilitaryAccountIsomorphism = field(default_factory=MilitaryAccountIsomorphism)
    bsd8_c3: HybridWarAlreadyStarted = field(default_factory=HybridWarAlreadyStarted)
    bsd8_c4: HistoryInfoWarSubset = field(default_factory=HistoryInfoWarSubset)
    bsd8_c5: CulturalAggressionFallacy = field(default_factory=CulturalAggressionFallacy)

    # BSD第八部分综合驻波
    bsd8_standing_wave: NewCivilizationWarStandingWave = field(default_factory=NewCivilizationWarStandingWave)

    # BSD第八部分最终结论
    bsd8_final: NewCivilizationWarFinalConclusions = field(default_factory=NewCivilizationWarFinalConclusions)
'''

# 在bsd7_final字段之后插入
marker = '    bsd7_final: BSDPart7FinalConclusions = field(default_factory=BSDPart7FinalConclusions)'

if marker in content:
    content = content.replace(marker, marker + new_fields)
    print('Successfully added BSD8 fields')
else:
    print('Marker not found')

# 写入文件
with open('t79_author_conjecture.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('File saved')
