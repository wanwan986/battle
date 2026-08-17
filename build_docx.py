# -*- coding: utf-8 -*-
"""由 Markdown 终稿生成中文学术论文格式的 .docx，并在对应位置插入插图。"""
import re
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC = '/home/user/battle/论文终稿-非战争军事行动中智能无人作战的策略战法研究.md'
OUT = '/home/user/battle/非战争军事行动中智能无人作战的策略战法研究.docx'
FIG = '/home/user/battle/figs/'

SONG, HEI, KAI, TIMES = '宋体', '黑体', '楷体', 'Times New Roman'


def cjk(run, font_cjk, size, bold=False, western=TIMES):
    """设置中西文字体（python-docx 需显式写 w:eastAsia）"""
    run.font.name = western
    run.font.size = Pt(size)
    run.font.bold = bold
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts'); rPr.append(rFonts)
    rFonts.set(qn('w:eastAsia'), font_cjk)
    rFonts.set(qn('w:ascii'), western)
    rFonts.set(qn('w:hAnsi'), western)


def straight_to_curly(t):
    """直双引号成对转中文弯引号"""
    out, open_q = [], True
    for ch in t:
        if ch == '"':
            out.append('“' if open_q else '”')
            open_q = not open_q
        else:
            out.append(ch)
    return ''.join(out)


def para(doc, text='', align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=True,
         font=SONG, size=12, bold=False, space_before=0, space_after=0,
         line=1.5):
    p = doc.add_paragraph()
    p.alignment = align
    pf = p.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = line
    if indent:
        pf.first_line_indent = Pt(size * 2)
    if text:
        add_rich(p, text, font, size, bold)
    return p


def add_rich(p, text, font, size, bold):
    """解析 **粗体** 与 【n】上标引用"""
    for seg in re.split(r'(\*\*[^*]+\*\*|【\d+】)', text):
        if not seg:
            continue
        if seg.startswith('**') and seg.endswith('**'):
            r = p.add_run(seg[2:-2]); cjk(r, HEI, size, True)
        elif re.fullmatch(r'【\d+】', seg):
            r = p.add_run('[' + seg[1:-1] + ']')
            cjk(r, font, size, False)
            r.font.superscript = True
        else:
            r = p.add_run(seg); cjk(r, font, size, bold)


def figure(doc, fname, caption, width_cm=15.0):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p.paragraph_format
    pf.space_before = Pt(8); pf.space_after = Pt(2)
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
    p.add_run().add_picture(FIG + fname, width=Cm(width_cm))
    c = doc.add_paragraph(); c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cf = c.paragraph_format
    cf.space_before = Pt(0); cf.space_after = Pt(12)
    cf.line_spacing_rule = WD_LINE_SPACING.SINGLE
    r = c.add_run(caption); cjk(r, HEI, 10.5)


# ═══════════════ 解析 Markdown ═══════════════
md = open(SRC, encoding='utf-8').read()
md = straight_to_curly(md)
lines = md.split('\n')

doc = Document()
sec = doc.sections[0]
sec.top_margin = Cm(2.8); sec.bottom_margin = Cm(2.5)
sec.left_margin = Cm(3.0); sec.right_margin = Cm(3.0)

st = doc.styles['Normal']
st.font.name = TIMES; st.font.size = Pt(12)
st.element.rPr.rFonts.set(qn('w:eastAsia'), SONG)

# 图在正文中的插入点：小节标题出现后，其第 n 个段落之后
FIGS_AFTER_PARA = {
    ('一、引言', 2): ('fig1_framework.png', '图1　研究框架与逻辑主线', 15.0),
    ('（一）侦控一体：三源复合侦测与圈层分区管控', 1): ('fig2_three_sources.png', '图2　“图—谱—链”三源复合侦测融合', 15.0),
    ('（一）侦控一体：三源复合侦测与圈层分区管控', 2): ('fig3_zoning.png', '图3　“圈层—网格—白名单”分区管控', 13.0),
    ('（二）梯次处置：法律授权前置的分级响应', 2): ('fig4_legal_response.png', '图4　法律授权前置的分级响应模型', 15.2),
    ('四、非对抗性行动的策略战法：抢险救灾应急运用', 2): ('fig5_rescue_four_steps.png', '图5　“侦救一体”四步应急战法', 15.5),
    ('五、双场景比较：四条共性规律', 1): ('fig6_comparison_laws.png', '图6　双场景比较与四条共性规律', 14.0),
}

def add_formula(doc, img, number='1'):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p.paragraph_format
    pf.space_before = Pt(6); pf.space_after = Pt(6)
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
    p.add_run().add_picture(FIG + img, width=Cm(5.6))
    r = p.add_run('　　（' + number + '）'); cjk(r, SONG, 11)


def add_table(doc, rows, caption=None):
    if caption:
        c = doc.add_paragraph(); c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cf = c.paragraph_format
        cf.space_before = Pt(8); cf.space_after = Pt(3)
        cf.line_spacing_rule = WD_LINE_SPACING.SINGLE
        r = c.add_run(caption); cjk(r, HEI, 10.5, True)
    tbl = doc.add_table(rows=len(rows), cols=len(rows[0]))
    tbl.style = 'Table Grid'
    tbl.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for ri, row in enumerate(rows):
        for ci, cell in enumerate(row):
            tc = tbl.cell(ri, ci)
            tc.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER if ri == 0 else WD_ALIGN_PARAGRAPH.LEFT
            rr = tc.paragraphs[0].add_run(cell)
            cjk(rr, HEI if ri == 0 else SONG, 9, bold=(ri == 0))
            tc.paragraphs[0].paragraph_format.line_spacing = 1.15
            tc.paragraphs[0].paragraph_format.space_after = Pt(1)


cur_head = None
para_idx = 0
in_refs = False
i = 0
while i < len(lines):
    ln = lines[i].rstrip()
    i += 1
    if not ln.strip() or ln.strip() == '---':
        continue

    # 显示公式（$$...$$ 单行）
    if ln.strip().startswith('$$'):
        add_formula(doc, 'formula1.png', '1')
        continue

    # 表格标题行（**表1...**）：读取其后的 markdown 管道表
    if ln.startswith('**表') and '|' not in ln:
        cap = re.sub(r'\*\*', '', ln).strip()
        while i < len(lines) and not lines[i].strip():
            i += 1  # 跳过标题与表之间的空行
        rows = []
        while i < len(lines) and lines[i].lstrip().startswith('|'):
            cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
            i += 1
            if all(set(c) <= set('-: ') for c in cells):
                continue  # 分隔行
            rows.append(cells)
        if rows:
            add_table(doc, rows, cap)
        continue

    # 防护：漏网的管道表行不作为正文渲染
    if ln.lstrip().startswith('|'):
        continue

    # 标题
    if ln.startswith('# '):
        p = para(doc, '', WD_ALIGN_PARAGRAPH.CENTER, indent=False,
                 space_after=6, line=1.3)
        r = p.add_run(ln[2:].strip()); cjk(r, HEI, 18, True)
        continue
    if ln.startswith('## ——'):
        p = para(doc, '', WD_ALIGN_PARAGRAPH.CENTER, indent=False,
                 space_after=14, line=1.3)
        r = p.add_run(ln[3:].strip()); cjk(r, HEI, 13.5)
        continue
    if ln.startswith('### '):
        t = ln[4:].strip()
        cur_head, para_idx = t, 0
        p = para(doc, '', WD_ALIGN_PARAGRAPH.LEFT, indent=False,
                 space_before=10, space_after=5, line=1.4)
        r = p.add_run(t); cjk(r, HEI, 12, True)
        continue
    if ln.startswith('## '):
        t = ln[3:].strip()
        if t.startswith('参考文献'):
            in_refs = True
        cur_head, para_idx = t, 0
        if t == '摘　要':
            p = para(doc, '', WD_ALIGN_PARAGRAPH.CENTER, indent=False,
                     space_before=6, space_after=5, line=1.4)
            r = p.add_run('摘　要'); cjk(r, HEI, 13, True)
        else:
            p = para(doc, '', WD_ALIGN_PARAGRAPH.LEFT, indent=False,
                     space_before=13, space_after=6, line=1.4)
            r = p.add_run(t); cjk(r, HEI, 13.5, True)
        continue

    # 文末说明（斜体行）
    if ln.startswith('*') and ln.endswith('*') and not ln.startswith('**'):
        p = para(doc, '', WD_ALIGN_PARAGRAPH.JUSTIFY, indent=False,
                 space_before=10, line=1.35)
        r = p.add_run(ln.strip('*').strip()); cjk(r, KAI, 10.5)
        r.font.color.rgb = RGBColor(0x44, 0x44, 0x44)
        continue

    # 参考文献条目
    if in_refs and re.match(r'^\[\d+\]', ln):
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pf = p.paragraph_format
        pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE; pf.line_spacing = 1.25
        pf.space_after = Pt(2); pf.left_indent = Pt(24); pf.first_line_indent = Pt(-24)
        r = p.add_run(ln); cjk(r, SONG, 10.5)
        continue

    # 摘要 / 关键词 / Abstract
    if ln.startswith('**摘'):
        continue
    if ln.startswith('**关键词**') or ln.startswith('**Keywords**'):
        p = para(doc, '', WD_ALIGN_PARAGRAPH.JUSTIFY, indent=False,
                 size=10.5, space_before=4, line=1.4)
        head, rest = ln.split('：', 1) if '：' in ln else ln.split(':', 1)
        r = p.add_run(head.strip('*') + '：'); cjk(r, HEI, 10.5, True)
        r2 = p.add_run(rest.strip()); cjk(r2, SONG, 10.5)
        continue
    if ln.startswith('**Abstract**'):
        body = ln.replace('**Abstract**:', '').strip()
        p = para(doc, '', WD_ALIGN_PARAGRAPH.JUSTIFY, indent=False,
                 size=10.5, space_before=8, line=1.4)
        r = p.add_run('Abstract: '); cjk(r, HEI, 10.5, True)
        r2 = p.add_run(body); cjk(r2, SONG, 10.5)
        continue
    if ln.startswith('**作者**') or ln.startswith('**中图分类号**'):
        p = para(doc, '', WD_ALIGN_PARAGRAPH.CENTER, indent=False,
                 size=11, line=1.4, space_after=3)
        r = p.add_run(re.sub(r'\*\*', '', ln)); cjk(r, KAI, 11)
        continue

    # 摘要正文
    if cur_head == '摘　要':
        para(doc, ln, size=10.5, line=1.45)
        para_idx += 1
        continue

    # 正文段落
    para(doc, ln, size=12, line=1.55, space_after=2)
    para_idx += 1

    key = (cur_head, para_idx)
    if key in FIGS_AFTER_PARA:
        fn, cap, wd = FIGS_AFTER_PARA[key]
        figure(doc, fn, cap, wd)

doc.save(OUT)
print('saved:', OUT)
