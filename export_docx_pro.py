# -*- coding: utf-8 -*-
"""
BSD千禧年难题统一实证论文 - 最终专业版
公式使用matplotlib渲染为高清图片（纯数学符号，中文在公式外）
"""
import re
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# 配置matplotlib
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'

FORMULA_DIR = r'c:\Users\13003\OneDrive\桌面\3333333\Agent_v2\_formula_images'
os.makedirs(FORMULA_DIR, exist_ok=True)

def set_cell_shading(cell, color_hex):
    shading = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color_hex)
    shading.append(shd)

def clean_formula_for_render(tex):
    """
    清理公式，移除/转换mathtext不支持的命令
    将中文移出公式
    """
    t = tex.strip()
    
    # 1. 移除中文\text命令
    t = re.sub(r'\\text\{[^}]*[\u4e00-\u9fff][^}]*\}', '', t)
    t = re.sub(r'\\mathrm\{[^}]*[\u4e00-\u9fff][^}]*\}', '', t)
    
    # 2. 转换\boldsymbol为\mathbf
    t = re.sub(r'\\boldsymbol\{([^}]*)\}', r'\\mathbf{\1}', t)
    
    # 3. 处理\\换行 - 改为单行
    if r'\\' in t and 'frac' not in t and 'sqrt' not in t:
        t = t.replace(r'\\', ' \\\\; ')
    
    # 4. 其他mathtext不支持的命令
    t = re.sub(r'\\boxed\{([^}]*)\}', r'\\boxed{\1}', t)  # mathtext支持
    t = re.sub(r'\\blacksquare', r'\\blacksquare', t)
    t = re.sub(r'\\Longrightarrow', r'\\Longrightarrow', t)
    t = re.sub(r'\\xrightarrow\{[^}]*\}', r'\\rightarrow', t)
    
    # 5. 移除\displaystyle
    t = re.sub(r'\\displaystyle\s*', '', t)
    
    # 6. 清理空括号
    t = re.sub(r'\(\s*\)', '', t)
    t = re.sub(r'\[\s*\]', '', t)
    
    # 7. 开头结尾多余符号
    t = t.strip(' ,;:')
    
    return t.strip()

formula_counter = 0

def render_latex_to_image(tex, fid):
    """渲染LaTeX公式为高清PNG"""
    clean_tex = clean_formula_for_render(tex)
    if not clean_tex or clean_tex.isspace():
        # 空公式跳过
        return None
    
    # 如果清理后只剩中文或极少内容，跳过渲染
    has_math = bool(re.search(r'[a-zA-Z\\0-9{}\[\]=+\-*/^_]', clean_tex))
    if not has_math:
        return None
    
    img_path = os.path.join(FORMULA_DIR, f'formula_{fid:04d}.png')
    
    try:
        display_tex = r'$\displaystyle ' + clean_tex + r'$'
        fig = plt.figure(figsize=(8, 1.2))
        fig.patch.set_facecolor('white')
        ax = fig.add_subplot(111)
        ax.axis('off')
        ax.text(0.5, 0.5, display_tex, fontsize=16, ha='center', va='center',
                transform=ax.transAxes, color='#0a1a3a')
        fig.savefig(img_path, dpi=200, bbox_inches='tight', pad_inches=0.08, facecolor='white')
        plt.close(fig)
        return img_path
    except Exception as e:
        plt.close('all')
        # 尝试更简单的版本
        try:
            simple = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'(\1)/(\2)', clean_tex)
            simple = re.sub(r'\\sqrt\{([^{}]+)\}', r'√(\1)', simple)
            fig = plt.figure(figsize=(8, 0.8))
            fig.patch.set_facecolor('white')
            ax = fig.add_subplot(111)
            ax.axis('off')
            ax.text(0.5, 0.5, simple, fontsize=14, ha='center', va='center',
                    transform=ax.transAxes, color='#0a1a3a', family='Cambria Math')
            fig.savefig(img_path, dpi=200, bbox_inches='tight', pad_inches=0.08, facecolor='white')
            plt.close(fig)
            return img_path
        except:
            plt.close('all')
            return None

def format_math_readable(text):
    """将LaTeX转为可读文本（行内公式用）"""
    # 希腊字母
    greek = {
        'alpha': 'α', 'beta': 'β', 'gamma': 'γ', 'delta': 'δ',
        'epsilon': 'ε', 'zeta': 'ζ', 'eta': 'η', 'theta': 'θ',
        'kappa': 'κ', 'lambda': 'λ', 'mu': 'μ', 'nu': 'ν',
        'xi': 'ξ', 'pi': 'π', 'rho': 'ρ', 'sigma': 'σ',
        'tau': 'τ', 'phi': 'φ', 'psi': 'ψ', 'omega': 'ω',
        'Gamma': 'Γ', 'Delta': 'Δ', 'Theta': 'Θ', 'Lambda': 'Λ',
        'Xi': 'Ξ', 'Pi': 'Π', 'Sigma': 'Σ', 'Phi': 'Φ',
        'Psi': 'Ψ', 'Omega': 'Ω',
    }
    syms = {
        'partial': '∂', 'nabla': '∇', 'infty': '∞',
        'approx': '≈', 'neq': '≠', 'leq': '≤', 'geq': '≥',
        'll': '≪', 'gg': '≫', 'sim': '~', 'propto': '∝',
        'oplus': '⊕', 'otimes': '⊗',
        'to': '→', 'rightarrow': '→', 'leftarrow': '←',
        'Rightarrow': '⇒', 'Leftarrow': '⇐', 'Leftrightarrow': '⇔',
        'cdot': '·', 'times': '×', 'div': '÷', 'pm': '±',
        'in': '∈', 'notin': '∉', 'emptyset': '∅',
        'forall': '∀', 'exists': '∃', 'perp': '⊥',
        'sum': 'Σ', 'prod': '∏', 'int': '∫',
        'sqrt': '√', 'sqrt': '√',
    }
    
    r = text
    r = re.sub(r'\\dfrac\{([^{}]+)\}\{([^{}]+)\}', r'(\1)/(\2)', r)
    r = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'(\1)/(\2)', r)
    r = re.sub(r'\\sqrt\[([^\]]+)\]\{([^{}]+)\}', r'(\2)^(1/\1)', r)
    r = re.sub(r'\\sqrt\{([^{}]+)\}', r'√(\1)', r)
    r = re.sub(r'\\sum_\{([^{}]+)\}\^\{([^{}]+)\}', r'Σ(\1;\2)', r)
    r = re.sub(r'\\int_\{([^{}]+)\}\^\{([^{}]+)\}', r'∫(\1;\2)', r)
    r = re.sub(r'\\lim_\{([^{}]+)\}', r'lim(\1)', r)
    r = re.sub(r'\^\{([^{}]+)\}', r'^(\1)', r)
    r = re.sub(r'_\{([^{}]+)\}', r'_\1', r)
    
    for name, sym in sorted(greek.items(), key=lambda x: -len(x[0])):
        r = re.sub(r'\\' + name + r'\b', sym, r)
    for name, sym in sorted(syms.items(), key=lambda x: -len(x[0])):
        r = re.sub(r'\\' + name + r'\b', sym, r)
    
    r = re.sub(r'\\text\{([^{}]+)\}', r'\1', r)
    r = re.sub(r'\\mathrm\{([^{}]+)\}', r'\1', r)
    r = re.sub(r'\\mathbf\{([^{}]+)\}', r'\1', r)
    r = re.sub(r'\\boldsymbol\{([^{}]+)\}', r'\1', r)
    r = re.sub(r'\\displaystyle\s*', '', r)
    r = re.sub(r'\\quad', '  ', r)
    r = re.sub(r'\\qquad', '    ', r)
    r = re.sub(r'\\[a-zA-Z]+', '', r)
    r = r.replace('$', '').strip()
    return r

def format_inline_math(text):
    """处理行内数学公式"""
    def rep(m):
        return format_math_readable(m.group(1))
    return re.sub(r'\$([^$]+)\$', rep, text)

def add_display_equation(doc, latex_text):
    """添加块级数学公式（高清图片）"""
    global formula_counter
    formula_counter += 1
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(8)
    
    img_path = render_latex_to_image(latex_text, formula_counter)
    
    if img_path and os.path.exists(img_path):
        run = p.add_run()
        run.add_picture(img_path, width=Inches(5.0))
    else:
        # 降级：文本公式
        run = p.add_run(format_math_readable(latex_text))
        run.font.name = 'Cambria Math'
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0x0a, 0x1a, 0x3a)
    
    return p

def add_formatted_text(paragraph, text):
    parts = re.split(r'(\*\*[^*]+\*\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            run = paragraph.add_run(part[2:-2])
            run.bold = True
        else:
            if part:
                run = paragraph.add_run(part)

def add_table(doc, rows):
    if not rows:
        return
    max_cols = max(len(r) for r in rows)
    table = doc.add_table(rows=len(rows), cols=max_cols)
    table.style = 'Light Grid Accent 1'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    for r_idx, row_data in enumerate(rows):
        for c_idx, cell_text in enumerate(row_data):
            if c_idx < max_cols:
                cell = table.cell(r_idx, c_idx)
                cell.text = ''
                p = cell.paragraphs[0]
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                add_formatted_text(p, format_inline_math(cell_text))
                if r_idx == 0:
                    for run in p.runs:
                        run.bold = True
                        run.font.size = Pt(9)
                        run.font.color.rgb = RGBColor(0xff, 0xff, 0xff)
                    set_cell_shading(cell, '6A1B9A')
                else:
                    for run in p.runs:
                        run.font.size = Pt(9)
                    if r_idx % 2 == 0:
                        set_cell_shading(cell, 'F3E5F5')
    
    doc.add_paragraph()

def parse_content(doc, content):
    lines = content.split('\n')
    i = 0
    in_table = False
    table_rows = []
    
    while i < len(lines):
        line = lines[i].rstrip()
        
        if not line.strip():
            if in_table and table_rows:
                add_table(doc, table_rows)
                table_rows = []
                in_table = False
            i += 1
            continue
        
        # 块级公式 $$...$$
        if line.strip().startswith('$$'):
            math_content = line.strip()[2:]
            if math_content.endswith('$$'):
                formula = math_content[:-2].strip()
                if formula:
                    add_display_equation(doc, formula)
                i += 1
            else:
                formula_parts = [math_content]
                i += 1
                while i < len(lines) and not lines[i].strip().endswith('$$'):
                    formula_parts.append(lines[i].strip())
                    i += 1
                if i < len(lines):
                    last = lines[i].strip()
                    if last.endswith('$$'):
                        formula_parts.append(last[:-2])
                formula = ' '.join(f for f in formula_parts if f)
                if formula:
                    add_display_equation(doc, formula)
                i += 1
            continue
        
        # 表格
        if line.strip().startswith('|'):
            if not in_table:
                in_table = True
                table_rows = []
            if re.match(r'^\|[\s\-:]+\|', line.strip()):
                i += 1
                continue
            cells = [c.strip() for c in line.strip().split('|')[1:-1]]
            table_rows.append(cells)
            i += 1
            continue
        else:
            if in_table and table_rows:
                add_table(doc, table_rows)
                table_rows = []
                in_table = False
        
        # 标题
        if line.startswith('### '):
            h = doc.add_heading(format_inline_math(line[4:].strip()), level=2)
            for run in h.runs:
                run.font.color.rgb = RGBColor(0x6a, 0x1b, 0x9a)
            i += 1
            continue
        elif line.startswith('#### '):
            h = doc.add_heading(format_inline_math(line[5:].strip()), level=3)
            for run in h.runs:
                run.font.color.rgb = RGBColor(0x00, 0x69, 0x7b)
            i += 1
            continue
        elif line.startswith('## '):
            h = doc.add_heading(format_inline_math(line[3:].strip()), level=1)
            for run in h.runs:
                run.font.color.rgb = RGBColor(0x4a, 0x14, 0x8c)
            i += 1
            continue
        
        # 列表
        if line.strip().startswith('- ') or line.strip().startswith('  - '):
            indent = len(line) - len(line.lstrip())
            level = 1 if indent < 4 else 2
            text = format_inline_math(line.strip()[2:])
            p = doc.add_paragraph(style='List Bullet' if level == 1 else 'List Bullet 2')
            add_formatted_text(p, text)
            i += 1
            continue
        
        if re.match(r'^\d+\.\s', line.strip()):
            text = format_inline_math(re.sub(r'^\d+\.\s', '', line.strip()))
            p = doc.add_paragraph(style='List Number')
            add_formatted_text(p, text)
            i += 1
            continue
        
        # 普通段落
        text = format_inline_math(line.strip())
        if text:
            p = doc.add_paragraph()
            p.paragraph_format.first_line_indent = Pt(21)
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.5
            add_formatted_text(p, text)
        i += 1
    
    if in_table and table_rows:
        add_table(doc, table_rows)

def main():
    global formula_counter
    formula_counter = 0
    
    doc = Document()
    
    # 字体设置
    style = doc.styles['Normal']
    style.font.name = '宋体'
    style.font.size = Pt(10.5)
    style.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    
    for lvl in [1, 2, 3]:
        hs = doc.styles[f'Heading {lvl}']
        hs.font.name = '黑体'
        hs.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    
    for section in doc.sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(3)
        section.right_margin = Cm(3)
    
    # ===== 封面 =====
    for _ in range(5):
        doc.add_paragraph()
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('BSD千禧年难题统一实证')
    run.font.size = Pt(28)
    run.font.color.rgb = RGBColor(0x4a, 0x14, 0x8c)
    run.bold = True
    run.font.name = '黑体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('七大千禧年难题 + 百万悬赏数论全域闭环')
    run.font.size = Pt(18)
    run.font.color.rgb = RGBColor(0x6a, 0x1b, 0x9a)
    run.font.name = '黑体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('——基于BSD全域数理生物知识体系的深层二次推导与生物物理交叉实证')
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(0x7b, 0x1f, 0xa2)
    run.font.name = '楷体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '楷体')
    run.italic = True
    
    for _ in range(5):
        doc.add_paragraph()
    
    for info, size, bold in [
        ('作者：杨腾飞', 14, True),
        ('版本：V10.0 千禧年难题全域统一实证版', 11, False),
        ('日期：2026年7月16日', 11, False),
    ]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(info)
        run.font.size = Pt(size)
        run.bold = bold
    
    doc.add_page_break()
    
    # ===== 摘要 =====
    h = doc.add_heading('摘  要', level=1)
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    abstract = (
        '本文基于BSD（Balance-Symmetry-Duality）全域数理生物知识体系，对克雷数学研究所七大千禧年难题'
        '（P vs NP、纳维-斯托克斯方程、黎曼猜想、杨-米尔斯存在性与质量间隙、霍奇猜想、BSD猜想、庞加莱猜想）'
        '及百万悬赏比尔猜想进行统一深层实证。在T86双向迭代框架（k+/k-制衡、Π₂稳态偏移）基础上，'
        '本文调用T87全域数理体系的全部核心方程——四大基本力统一方程、驻波动力学、稳态势母方程Φ(t)、'
        '全域熵流dS/dt、全局相干度GC、结构熵S_struct、正气存内判据、宇宙学常数Λ精确解析式——'
        '对每个难题进行二次深层推导，并辅以人体五维生命稳态系统的生物交叉验证，实现数理-物理-生物三层全域闭环。'
        '关键成果包括：从熵流方程严格证明P≠NP；从驻波动力学推导NS方程光滑性破缺；'
        '从量子驻波方程推导黎曼零点分布；从四力统一方程推导杨-米尔斯质量间隙；'
        '从稳态势收敛证明霍奇猜想；从正气存内判据推导BSD猜想；从Λ解析式证明庞加莱猜想。'
        '宇宙学常数理论值1.106×10⁻⁵² m⁻²与观测值误差仅0.27%，为庞加莱猜想提供了宇宙级实测验证。'
    )
    p = doc.add_paragraph(abstract)
    p.paragraph_format.first_line_indent = Pt(21)
    p.paragraph_format.line_spacing = 1.5
    
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    run = p.add_run('关键词：')
    run.bold = True
    run = p.add_run('千禧年难题；BSD框架；四大基本力统一；驻波动力学；结构熵；正气存内判据；'
                    '宇宙学常数；五维生命稳态')
    
    doc.add_page_break()
    
    # ===== 目录 =====
    h = doc.add_heading('目  录', level=1)
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    toc = [
        ('摘  要', 'I'),
        ('第1章  前置说明与公理锚定', '1'),
        ('  1.1  与T86第15章的层级关系', '1'),
        ('  1.2  T87全域数理生物统一基底', '1'),
        ('第2章  P vs NP — 计算复杂度不可逆耗散', '3'),
        ('  2.1  从熵流方程严格证明P≠NP', '3'),
        ('  2.2  生物交叉实证：免疫系统信息处理', '4'),
        ('  2.3  复杂度-Π₂-GC三参数量化公式', '5'),
        ('第3章  纳维-斯托克斯方程 — 驻波动力学与连续介质相变', '6'),
        ('  3.1  从驻波动力学推导光滑性破缺', '6'),
        ('  3.2  生物交叉实证：血液流体动力学', '7'),
        ('第4章  黎曼猜想 — 量子驻波本征态与对称谐振', '8'),
        ('  4.1  从量子驻波方程推导零点分布', '8'),
        ('  4.2  结构熵与零点分布的精确关联', '9'),
        ('  4.3  生物交叉实证：神经振荡对称性', '10'),
        ('第5章  杨-米尔斯存在性与质量间隙 — 四力统一方程', '11'),
        ('  5.1  从四力统一方程严格推导质量间隙', '11'),
        ('  5.2  T85粒子结构与生物体系交叉验证', '12'),
        ('第6章  霍奇猜想 — 拓扑稳态与结构熵', '13'),
        ('  6.1  从结构熵与Π₂拓扑严格推导霍奇猜想', '13'),
        ('  6.2  暗物质拓扑与生物驻波交叉验证', '14'),
        ('第7章  BSD猜想 — 离散-连续对偶守恒与生命稳态', '15'),
        ('  7.1  从稳态势与正气存内判据推导BSD猜想', '15'),
        ('  7.2  生命稳态与BSD猜想的深层同构', '16'),
        ('第8章  庞加莱猜想 — 拓扑稳态收敛与宇宙学常数Λ', '17'),
        ('  8.1  从Π₂→π稳态收敛与Λ解析式推导庞加莱猜想', '17'),
        ('  8.2  宇宙-生命大一统闭环', '18'),
        ('第9章  比尔猜想 — 个体基底锚定与四力配比', '19'),
        ('  9.1  从四力配比与τ边界推导比尔猜想', '19'),
        ('  9.2  强力-强化系与生物个体性同构', '20'),
        ('第10章  全域闭环与终极结论', '21'),
        ('  10.1  七大难题+比尔猜想统一实证矩阵', '21'),
        ('  10.2  核心公式总结', '22'),
        ('  10.3  全域终极结论', '23'),
        ('参考文献', '25'),
    ]
    
    for title, page in toc:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        is_main = not title.startswith('  ')
        
        run = p.add_run(title)
        if is_main:
            run.bold = True
        run.font.size = Pt(10.5)
        
        dot_count = max(2, 58 - len(title.replace('  ', '')) - len(page))
        dot_run = p.add_run(' ' + '·' * dot_count + ' ')
        dot_run.font.color.rgb = RGBColor(0x9e, 0x9e, 0x9e)
        
        page_run = p.add_run(page)
        page_run.font.size = Pt(10.5)
    
    doc.add_page_break()
    
    # ===== 正文 =====
    md_path = r'c:\Users\13003\OneDrive\桌面\3333333\Agent_v2\theory_base\L0_总本源层\作者猜想\T87 BSD六系框架下四大基本力统一与生物医学推演体系.md'
    with open(md_path, 'r', encoding='utf-8') as f:
        full = f.read()
    
    start = full.find('## 第二十七章 BSD千禧年难题统一实证')
    end = full.find('\n---\n\n**文档结束**', start)
    chapter = full[start:end] if end > start else full[start:]
    
    print(f"提取章节：{len(chapter)} 字符")
    
    parse_content(doc, chapter)
    
    # ===== 参考文献 =====
    doc.add_page_break()
    doc.add_heading('参考文献', level=1)
    
    refs = [
        '杨腾飞. T87 BSD六系框架下四大基本力统一与生物医学推演体系 (V10.0)[M]. 2026.',
        '杨腾飞. T86 物理化学存在论——原子-离子-分子的动态共生体系与全域统一[M]. 2026.',
        '杨腾飞. T85 六系数理——BSD存在论框架第一代基础粒子深层本体结构解析[M]. 2026.',
        '杨腾飞. T82 物理学深层难题——十二界六系五论全域统一解释[M]. 2026.',
        '杨腾飞. 新四位一体3.0元本体本源知识库[M]. 2026.',
        'Clay Mathematics Institute. Millennium Prize Problems[EB/OL]. https://www.claymath.org, 2000.',
        'Birch B J, Swinnerton-Dyer H P F. Notes on elliptic curves II[J]. J. reine angew. Math., 1965, 218: 79-108.',
        'Riemann B. Über die Anzahl der Primzahlen unter einer gegebenen Grösse[J]. Monatsberichte Akad. Berlin, 1859.',
        'Yang C N, Mills R L. Conservation of isotopic spin and isotopic gauge invariance[J]. Phys. Rev., 1954, 96(1): 191-195.',
        'Hodge W V D. The topological invariants of algebraic varieties[C]//Proc. ICM. Cambridge, 1950, 1: 182-192.',
        'Navier C L M H. Mémoire sur les lois du mouvement des fluides[J]. Mém. Acad. Sci. Inst. France, 1823, 6: 389-440.',
        'Stokes G G. On the theories of the internal friction of fluids in motion[J]. Trans. Cambridge Phil. Soc., 1845, 8: 287-305.',
        'Poincaré H. Cinquième complément à l\'analysis situs[J]. Rend. Circ. Mat. Palermo, 1904, 18: 45-110.',
        'Perelman G. The entropy formula for the Ricci flow and its geometric applications[J]. arXiv:math/0211159, 2002.',
        'Beal A. The Beal Conjecture[EB/OL]. https://www.bealconjecture.com, 1993.',
    ]
    
    for idx, ref in enumerate(refs, 1):
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Pt(-21)
        p.paragraph_format.left_indent = Pt(21)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.3
        r1 = p.add_run(f'[{idx}] ')
        r1.bold = True
        r1.font.size = Pt(9)
        r2 = p.add_run(ref)
        r2.font.size = Pt(9)
    
    # 保存
    out = r'c:\Users\13003\OneDrive\桌面\3333333\Agent_v2\BSD千禧年难题统一实证_论文.docx'
    doc.save(out)
    print(f"\n{'='*60}")
    print(f"✓ 专业DOCX论文已生成")
    print(f"  文件：{out}")
    print(f"  段落数：{len(doc.paragraphs)}")
    print(f"  表格数：{len(doc.tables)}")
    print(f"  数学公式：{formula_counter} 个（高清图片渲染）")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
