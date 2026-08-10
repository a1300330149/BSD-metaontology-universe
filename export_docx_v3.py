# -*- coding: utf-8 -*-
"""
BSD千禧年难题统一实证论文 - 专业DOCX生成器
使用Word原生OMML数学公式（通过MathML→OMML XSLT转换）
"""
import re
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from lxml import etree

# ====== 常量定义 ======
MATHML_NS = 'http://www.w3.org/1998/Math/MathML'
OMML_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/math'

# MathML到OMML的简化映射（覆盖本论文常用结构）
# 完整XSLT转换过于复杂，这里实现核心转换

def set_cell_shading(cell, color_hex):
    shading = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color_hex)
    shading.append(shd)

def create_omml_run(parent, text):
    """创建OMML文本运行"""
    r = etree.SubElement(parent, f'{{{OMML_NS}}}r')
    rpr = etree.SubElement(r, f'{{{OMML_NS}}}rPr')
    # 设置Cambria Math字体
    rfonts = etree.SubElement(rpr, f'{{{OMML_NS}}}rFonts')
    rfonts.set('script', 'Cambria Math')
    t = etree.SubElement(r, f'{{{OMML_NS}}}t')
    t.text = text
    return r

def latex_to_omml(latex_str):
    """
    将LaTeX表达式转换为Word OMML格式
    采用简化但专业的策略：解析常见LaTeX结构生成OMML XML
    """
    # 创建根元素
    omath = etree.Element(f'{{{OMML_NS}}}oMath')
    
    # 预处理：去除空格
    s = latex_str.strip()
    
    # 处理复杂情况：多部分公式
    # 我们使用"结构化递归解析"策略
    parse_expr(omath, s)
    
    return etree.tostring(omath, encoding='unicode')

def parse_expr(parent, expr):
    """递归解析LaTeX表达式并构建OMML"""
    expr = expr.strip()
    
    # 空表达式
    if not expr:
        return
    
    # 处理 \boxed{...}
    box_match = re.match(r'\\boxed\{(.+)\}$', expr)
    if box_match:
        box = etree.SubElement(parent, f'{{{OMML_NS}}}box')
        box_pr = etree.SubElement(box, f'{{{OMML_NS}}}boxPr')
        parse_expr(box, box_match.group(1))
        return
    
    # 处理分数 \frac{a}{b}
    frac_match = re.match(r'\\dfrac\{(.+?)\}\{(.+?)\}', expr) or re.match(r'\\frac\{(.+?)\}\{(.+?)\}', expr)
    if frac_match:
        f = etree.SubElement(parent, f'{{{OMML_NS}}}f')
        f_pr = etree.SubElement(f, f'{{{OMML_NS}}}fPr')
        num = etree.SubElement(f, f'{{{OMML_NS}}}num')
        den = etree.SubElement(f, f'{{{OMML_NS}}}den')
        parse_expr(num, frac_match.group(1))
        parse_expr(den, frac_match.group(2))
        # 继续处理剩余部分
        remainder = expr[frac_match.end():]
        if remainder:
            parse_expr(parent, remainder)
        return
    
    # 处理平方根 \sqrt{x}
    sqrt_match = re.match(r'\\sqrt\{(.+?)\}', expr)
    if sqrt_match:
        rad = etree.SubElement(parent, f'{{{OMML_NS}}}rad')
        rad_pr = etree.SubElement(rad, f'{{{OMML_NS}}}radPr')
        deg = etree.SubElement(rad, f'{{{OMML_NS}}}deg')  # 空的degree = 平方根
        e = etree.SubElement(rad, f'{{{OMML_NS}}}e')
        parse_expr(e, sqrt_match.group(1))
        remainder = expr[sqrt_match.end():]
        if remainder:
            parse_expr(parent, remainder)
        return
    
    # 处理上下标 a^{b}_{c} 或 a_b^c 等
    # 先处理组合情况：先处理下标，再处理上标（或反过来）
    # 简化：逐个token处理
    
    # 处理求和 \sum_{a}^{b}
    sum_match = re.match(r'\\sum_\{(.+?)\}\^\{(.+?)\}', expr) or re.match(r'\\sum\^\{(.+?)\}_\{(.+?)\}', expr)
    if sum_match:
        nary = etree.SubElement(parent, f'{{{OMML_NS}}}nary')
        nary_pr = etree.SubElement(nary, f'{{{OMML_NS}}}naryPr')
        chr_el = etree.SubElement(nary_pr, f'{{{OMML_NS}}}chr')
        chr_el.set('val', '∑')
        sub = etree.SubElement(nary, f'{{{OMML_NS}}}sub')
        sup = etree.SubElement(nary, f'{{{OMML_NS}}}sup')
        parse_expr(sub, sum_match.group(1))
        parse_expr(sup, sum_match.group(2))
        e = etree.SubElement(nary, f'{{{OMML_NS}}}e')
        remainder = expr[sum_match.end():]
        if remainder:
            parse_expr(e, remainder)
        return
    
    # 处理积分 \int_{a}^{b}
    int_match = re.match(r'\\int_\{(.+?)\}\^\{(.+?)\}', expr) or re.match(r'\\int\^\{(.+?)\}_\{(.+?)\}', expr)
    if int_match:
        nary = etree.SubElement(parent, f'{{{OMML_NS}}}nary')
        nary_pr = etree.SubElement(nary, f'{{{OMML_NS}}}naryPr')
        chr_el = etree.SubElement(nary_pr, f'{{{OMML_NS}}}chr')
        chr_el.set('val', '∫')
        sub = etree.SubElement(nary, f'{{{OMML_NS}}}sub')
        sup = etree.SubElement(nary, f'{{{OMML_NS}}}sup')
        parse_expr(sub, int_match.group(1))
        parse_expr(sup, int_match.group(2))
        e = etree.SubElement(nary, f'{{{OMML_NS}}}e')
        remainder = expr[int_match.end():]
        if remainder:
            parse_expr(e, remainder)
        return
    
    # 处理极限 \lim_{x \to ...}
    lim_match = re.match(r'\\lim_\{(.+?)\}', expr)
    if lim_match:
        lim = etree.SubElement(parent, f'{{{OMML_NS}}}limLow')
        lim_pr = etree.SubElement(lim, f'{{{OMML_NS}}}limLowPr')
        # 极限符号
        e = etree.SubElement(lim, f'{{{OMML_NS}}}e')
        create_omml_run(e, 'lim')
        sub = etree.SubElement(lim, f'{{{OMML_NS}}}lim')
        parse_expr(sub, lim_match.group(1))
        remainder = expr[lim_match.end():]
        if remainder:
            parse_expr(parent, remainder)
        return
    
    # 处理独立上标 x^{y} (不是分数、求和的一部分)
    # 需要先检查是否以字母或括号后的上标
    # 简化：直接构建上标
    
    # 处理向量 \vec{x}
    vec_match = re.match(r'\\vec\{(.+?)\}', expr)
    if vec_match:
        acc = etree.SubElement(parent, f'{{{OMML_NS}}}acc')
        acc_pr = etree.SubElement(acc, f'{{{OMML_NS}}}accPr')
        chr_el = etree.SubElement(acc_pr, f'{{{OMML_NS}}}chr')
        chr_el.set('val', '→')
        e = etree.SubElement(acc, f'{{{OMML_NS}}}e')
        parse_expr(e, vec_match.group(1))
        remainder = expr[vec_match.end():]
        if remainder:
            parse_expr(parent, remainder)
        return
    
    # 处理 \mathbf / \boldsymbol
    bm_match = re.match(r'\\boldsymbol\{(.+?)\}', expr) or re.match(r'\\mathbf\{(.+?)\}', expr)
    if bm_match:
        # 用普通文本（OMML加粗设置较复杂，简化为普通文本）
        parse_expr(parent, bm_match.group(1))
        remainder = expr[bm_match.end():]
        if remainder:
            parse_expr(parent, remainder)
        return
    
    # 处理 \text{...}
    text_match = re.match(r'\\text\{(.+?)\}', expr) or re.match(r'\\mathrm\{(.+?)\}', expr)
    if text_match:
        create_omml_run(parent, text_match.group(1))
        remainder = expr[text_match.end():]
        if remainder:
            parse_expr(parent, remainder)
        return
    
    # 默认：作为普通文本添加，先处理希腊字母等替换
    processed = replace_greek_symbols(expr)
    create_omml_run(parent, processed)

def replace_greek_symbols(text):
    """替换希腊字母和数学符号为Unicode"""
    greek = {
        '\\alpha': 'α', '\\beta': 'β', '\\gamma': 'γ', '\\delta': 'δ',
        '\\epsilon': 'ε', '\\zeta': 'ζ', '\\eta': 'η', '\\theta': 'θ',
        '\\kappa': 'κ', '\\lambda': 'λ', '\\mu': 'μ', '\\nu': 'ν',
        '\\xi': 'ξ', '\\pi': 'π', '\\rho': 'ρ', '\\sigma': 'σ',
        '\\tau': 'τ', '\\upsilon': 'υ', '\\phi': 'φ', '\\chi': 'χ',
        '\\psi': 'ψ', '\\omega': 'ω',
        '\\Gamma': 'Γ', '\\Delta': 'Δ', '\\Theta': 'Θ', '\\Lambda': 'Λ',
        '\\Xi': 'Ξ', '\\Pi': 'Π', '\\Sigma': 'Σ', '\\Phi': 'Φ',
        '\\Psi': 'Ψ', '\\Omega': 'Ω',
        '\\partial': '∂', '\\nabla': '∇', '\\infty': '∞',
        '\\approx': '≈', '\\neq': '≠', '\\leq': '≤', '\\geq': '≥',
        '\\ll': '≪', '\\gg': '≫', '\\sim': '~', '\\simeq': '≃',
        '\\cong': '≅', '\\equiv': '≡', '\\propto': '∝',
        '\\oplus': '⊕', '\\otimes': '⊗',
        '\\to': '→', '\\rightarrow': '→', '\\leftarrow': '←',
        '\\Rightarrow': '⇒', '\\Leftarrow': '⇐', '\\leftrightarrow': '↔',
        '\\Longrightarrow': '⟹',
        '\\cdot': '·', '\\times': '×', '\\div': '÷',
        '\\pm': '±', '\\mp': '∓',
        '\\in': '∈', '\\notin': '∉', '\\subset': '⊂', '\\supset': '⊃',
        '\\subseteq': '⊆', '\\supseteq': '⊇', '\\emptyset': '∅',
        '\\forall': '∀', '\\exists': '∃', '\\perp': '⊥',
        '\\blacksquare': '■', '\\square': '□',
        '\\quad': '  ', '\\qquad': '    ',
        '\\,': ' ', '\\;': ' ', '\\!': '', '\\ ': ' ',
        '\\\\': '',
        '\\displaystyle': '',
    }
    
    result = text
    for cmd, sym in sorted(greek.items(), key=lambda x: -len(x[0])):
        result = result.replace(cmd, sym)
    
    # 处理下标和上标（简化：只处理单字符或带花括号的）
    # ^{...} 和 _{...} 转换为Unicode上标/下标字符集（有限支持）
    # 对于复杂上下标，保留原始LaTeX可读形式
    
    # 清理残留反斜杠命令
    result = re.sub(r'\\[a-zA-Z]+', '', result)
    
    # 清理花括号（简单情况）
    # 注意：这里不做复杂括号匹配，仅做基础清理
    
    return result

def add_display_equation(doc, latex_text):
    """添加块级数学公式（使用Word原生OMML）"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(10)
    
    # 创建OMML段落容器
    omath_para = OxmlElement('m:oMathPara')
    omath_para_pr = OxmlElement('m:oMathParaPr')
    omath_para.append(omath_para_pr)
    
    # 尝试构建OMML
    try:
        omml_str = latex_to_omml(latex_text)
        omath_el = etree.fromstring(omml_str)
        omath_para.append(omath_el)
    except Exception as e:
        # 降级：用Cambria Math字体显示Unicode文本
        omath_el = OxmlElement('m:oMath')
        r = OxmlElement('m:r')
        rPr = OxmlElement('m:rPr')
        rFonts = OxmlElement('m:rFonts')
        rFonts.set('script', 'Cambria Math')
        rPr.append(rFonts)
        r.append(rPr)
        t = OxmlElement('m:t')
        t.text = format_math_readable(latex_text)
        r.append(t)
        omath_el.append(r)
        omath_para.append(omath_el)
    
    p._element.append(omath_para)
    return p

def format_math_readable(latex_str):
    """将LaTeX转换为人类可读的Unicode数学文本"""
    s = latex_str
    
    # 分数：\frac{a}{b} → (a)/(b)
    s = re.sub(r'\\dfrac\{([^{}]+)\}\{([^{}]+)\}', r'(\1)/(\2)', s)
    s = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'(\1)/(\2)', s)
    
    # 平方根
    s = re.sub(r'\\sqrt\[([^\]]+)\]\{([^{}]+)\}', r'(\2)^(1/\1)', s)
    s = re.sub(r'\\sqrt\{([^{}]+)\}', r'√(\1)', s)
    
    # 求和、积分
    s = re.sub(r'\\sum_\{([^{}]+)\}\^\{([^{}]+)\}', r'Σ(\1; \2)', s)
    s = re.sub(r'\\int_\{([^{}]+)\}\^\{([^{}]+)\}', r'∫(\1; \2)', s)
    
    # 极限
    s = re.sub(r'\\lim_\{([^{}]+)\}', r'lim(\1)', s)
    
    # 上标和下标
    s = re.sub(r'\^\{([^{}]+)\}', r'^(\1)', s)
    s = re.sub(r'_\{([^{}]+)\}', r'_(\1)', s)
    
    # 希腊字母和符号
    s = replace_greek_symbols(s)
    
    # 文本命令
    s = re.sub(r'\\text\{([^{}]+)\}', r'\1', s)
    s = re.sub(r'\\mathbf\{([^{}]+)\}', r'\1', s)
    s = re.sub(r'\\boldsymbol\{([^{}]+)\}', r'\1', s)
    
    # 盒子
    s = re.sub(r'\\boxed\{([^{}]+)\}', r'【\1】', s)
    
    # 清理
    s = s.replace('$', '').strip()
    
    return s

def format_inline_math(text):
    """处理行内数学公式"""
    def replace_inline(m):
        return format_math_readable(m.group(1))
    return re.sub(r'\$([^$]+)\$', replace_inline, text)

def add_formatted_text(paragraph, text):
    """处理加粗格式"""
    parts = re.split(r'(\*\*[^*]+\*\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            run = paragraph.add_run(part[2:-2])
            run.bold = True
        else:
            if part:
                run = paragraph.add_run(part)

def add_table(doc, rows):
    """添加专业表格"""
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
    """解析markdown内容并添加到文档"""
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
    doc = Document()
    
    # 默认字体设置
    style = doc.styles['Normal']
    style.font.name = '宋体'
    style.font.size = Pt(10.5)
    style.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    
    # 标题样式
    for lvl in [1, 2, 3]:
        hs = doc.styles[f'Heading {lvl}']
        hs.font.name = '黑体'
        hs.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    
    # 页面设置
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
    
    for info in ['作者：杨腾飞', '版本：V10.0 千禧年难题全域统一实证版', '日期：2026年7月16日']:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(info)
        run.font.size = Pt(13 if info.startswith('作者') else 11)
        if info.startswith('作者'):
            run.bold = True
    
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
    
    print(f"提取章节内容：{len(chapter)} 字符")
    
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
    print(f"\n✓ DOCX已保存：{out}")
    print(f"  段落数：{len(doc.paragraphs)}")
    print(f"  表格数：{len(doc.tables)}")

if __name__ == '__main__':
    main()
