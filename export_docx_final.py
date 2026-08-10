# -*- coding: utf-8 -*-
"""
BSD千禧年难题统一实证论文 - 终极专业版
使用matplotlib渲染LaTeX公式为高清图片插入Word
"""
import re
import os
import io
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import mathtext

# 公式缓存目录
FORMULA_DIR = r'c:\Users\13003\OneDrive\桌面\3333333\Agent_v2\_formula_images'
os.makedirs(FORMULA_DIR, exist_ok=True)

def set_cell_shading(cell, color_hex):
    shading = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color_hex)
    shading.append(shd)

def render_latex_to_image(latex_str, formula_id, dpi=200):
    """
    将LaTeX公式渲染为高清PNG图片
    返回图片路径
    """
    # 预处理公式
    tex = latex_str.strip()
    
    # 处理一些特殊的LaTeX命令matplotlib不支持
    tex = re.sub(r'\\boldsymbol\{([^}]*)\}', r'\\mathbf{\1}', tex)
    tex = re.sub(r'\\text\{([^}]*)\}', r'\\mathrm{\1}', tex)
    tex = re.sub(r'\\displaystyle\s*', '', tex)
    tex = re.sub(r'\\partial_t', r'\\partial_t', tex)
    tex = re.sub(r'\\blacksquare', r'\\square', tex)
    tex = re.sub(r'\\boxed\{([^}]*)\}', r'\\fbox{\1}', tex)
    
    # 处理\\换行符为多行
    if r'\\' in tex and not r'\\frac' in tex and not r'\\sqrt' in tex:
        tex = tex.replace(r'\\', r' \\ ')
    
    # 包装为display math
    if not tex.startswith('$') and not tex.startswith(r'\['):
        display_tex = r'$\displaystyle ' + tex + r'$'
    else:
        display_tex = tex
    
    img_path = os.path.join(FORMULA_DIR, f'formula_{formula_id:04d}.png')
    
    # 渲染
    try:
        fig = plt.figure(figsize=(8, 1.5))
        fig.patch.set_facecolor('white')
        ax = fig.add_subplot(111)
        ax.axis('off')
        ax.text(0.5, 0.5, display_tex, fontsize=16, ha='center', va='center',
                transform=ax.transAxes, color='#0a1a3a')
        fig.savefig(img_path, dpi=dpi, bbox_inches='tight', pad_inches=0.1, facecolor='white')
        plt.close(fig)
        return img_path, True
    except Exception as e:
        # 失败则尝试简化版
        try:
            simple_tex = r'$' + format_math_simple(tex.replace(r'\\mathrm', '').replace('{', '(').replace('}', ')')) + r'$'
            fig = plt.figure(figsize=(8, 1.2))
            fig.patch.set_facecolor('white')
            ax = fig.add_subplot(111)
            ax.axis('off')
            ax.text(0.5, 0.5, simple_tex, fontsize=14, ha='center', va='center',
                    transform=ax.transAxes, color='#0a1a3a')
            fig.savefig(img_path, dpi=dpi, bbox_inches='tight', pad_inches=0.1, facecolor='white')
            plt.close(fig)
            return img_path, True
        except:
            plt.close('all')
            return None, False

def format_math_simple(text):
    """简化的数学符号替换"""
    greek = {
        'alpha': 'α', 'beta': 'β', 'gamma': 'γ', 'delta': 'δ',
        'epsilon': 'ε', 'zeta': 'ζ', 'eta': 'η', 'theta': 'θ',
        'kappa': 'κ', 'lambda': 'λ', 'mu': 'μ', 'nu': 'ν',
        'xi': 'ξ', 'pi': 'π', 'rho': 'ρ', 'sigma': 'σ',
        'tau': 'τ', 'phi': 'φ', 'chi': 'χ', 'psi': 'ψ', 'omega': 'ω',
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
        'Rightarrow': '⇒', 'Leftarrow': '⇐',
        'cdot': '·', 'times': '×', 'div': '÷',
        'pm': '±', 'in': '∈', 'emptyset': '∅',
        'forall': '∀', 'exists': '∃', 'perp': '⊥',
        'sum': 'Σ', 'prod': '∏', 'int': '∫',
        'sqrt': '√',
    }
    
    result = text
    result = re.sub(r'\\dfrac\{([^{}]+)\}\{([^{}]+)\}', r'(\1)/(\2)', result)
    result = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'(\1)/(\2)', result)
    result = re.sub(r'\\sqrt\{([^{}]+)\}', r'√(\1)', result)
    result = re.sub(r'\^\{([^{}]+)\}', r'^(\1)', result)
    result = re.sub(r'_\{([^{}]+)\}', r'_(\1)', result)
    
    for name, sym in sorted(greek.items(), key=lambda x: -len(x[0])):
        result = re.sub(r'\\' + name + r'\b', sym, result)
    for name, sym in sorted(syms.items(), key=lambda x: -len(x[0])):
        result = re.sub(r'\\' + name + r'\b', sym, result)
    
    result = re.sub(r'\\mathrm\{([^{}]+)\}', r'\1', result)
    result = re.sub(r'\\mathbf\{([^{}]+)\}', r'\1', result)
    result = re.sub(r'\\[a-zA-Z]+', '', result)
    result = result.replace('$', '').strip()
    return result

def format_inline_math(text):
    """处理行内数学公式"""
    def replace_inline(m):
        return format_math_simple(m.group(1))
    return re.sub(r'\$([^$]+)\$', replace_inline, text)

formula_counter = 0

def add_display_equation(doc, latex_text):
    """添加块级数学公式（使用matplotlib渲染的高清图片）"""
    global formula_counter
    formula_counter += 1
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(10)
    
    img_path, success = render_latex_to_image(latex_text, formula_counter)
    
    if success and img_path and os.path.exists(img_path):
        run = p.add_run()
        run.add_picture(img_path, width=Inches(5.5))
    else:
        # 降级方案
        run = p.add_run(format_math_simple(latex_text))
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
        ('第2章  P vs NP — 计算复杂度不可逆耗散', '3'),
        ('第3章  纳维-斯托克斯方程 — 驻波动力学与连续介质相变', '5'),
        ('第4章  黎曼猜想 — 量子驻波本征态与对称谐振', '7'),
        ('第5章  杨-米尔斯存在性与质量间隙 — 四力统一方程', '9'),
        ('第6章  霍奇猜想 — 拓扑稳态与结构熵', '11'),
        ('第7章  BSD猜想 — 离散-连续对偶守恒与生命稳态', '13'),
        ('第8章  庞加莱猜想 — 拓扑稳态收敛与宇宙学常数Λ', '15'),
        ('第9章  比尔猜想 — 个体基底锚定与四力配比', '17'),
        ('第10章  全域闭环与终极结论', '19'),
        ('参考文献', '21'),
    ]
    
    for title, page in toc:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        is_main = title.startswith('第') or title.startswith('摘') or title.startswith('参')
        
        run = p.add_run(title)
        if is_main:
            run.bold = True
        run.font.size = Pt(10.5)
        
        dot_count = max(2, 55 - len(title) - len(page))
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
        'Clay Mathematics Institute. Millennium Prize Problems[EB/OL]. 2000.',
        'Birch B J, Swinnerton-Dyer H P F. Notes on elliptic curves II[J]. J. reine angew. Math., 1965, 218: 79-108.',
        'Riemann B. Über die Anzahl der Primzahlen unter einer gegebenen Grösse[J]. Monatsberichte Akad. Berlin, 1859.',
        'Yang C N, Mills R L. Conservation of isotopic spin and isotopic gauge invariance[J]. Phys. Rev., 1954, 96(1): 191-195.',
        'Hodge W V D. The topological invariants of algebraic varieties[C]//Proc. ICM. Cambridge, 1950, 1: 182-192.',
        'Navier C L M H. Mémoire sur les lois du mouvement des fluides[J]. Mém. Acad. Sci. Inst. France, 1823, 6: 389-440.',
        'Stokes G G. On the theories of the internal friction of fluids in motion[J]. Trans. Cambridge Phil. Soc., 1845, 8: 287-305.',
        'Poincaré H. Cinquième complément à l\'analysis situs[J]. Rend. Circ. Mat. Palermo, 1904, 18: 45-110.',
        'Perelman G. The entropy formula for the Ricci flow and its geometric applications[J]. arXiv:math/0211159, 2002.',
        'Beal A. The Beal Conjecture[EB/OL]. 1993.',
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
    print(f"\n{'='*50}")
    print(f"✓ DOCX论文已生成：{out}")
    print(f"  段落数：{len(doc.paragraphs)}")
    print(f"  表格数：{len(doc.tables)}")
    print(f"  公式图片：{formula_counter} 张")
    print(f"  公式图片目录：{FORMULA_DIR}")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()
