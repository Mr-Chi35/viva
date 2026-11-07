"""
Design system + layout helpers for the viva deck.

Everything is drawn from primitives (shapes, text boxes, native tables,
lines) so the deck stays fully editable in PowerPoint -- no baked-in images
except the genuine analysis figures and the re-plotted charts.
"""
import math

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt
from lxml import etree

# ---------------------------------------------------------------- palette
INK        = RGBColor(0x12, 0x15, 0x2E)
INK_2      = RGBColor(0x22, 0x27, 0x4C)
BODY       = RGBColor(0x3C, 0x41, 0x60)
MUTED      = RGBColor(0x7C, 0x81, 0x9C)
LINE       = RGBColor(0xE2, 0xE4, 0xEF)
WASH       = RGBColor(0xF6, 0xF7, 0xFC)
WASH_2     = RGBColor(0xEF, 0xF0, 0xF9)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
ACCENT     = RGBColor(0x5B, 0x4B, 0xE6)
ACCENT_DK  = RGBColor(0x3B, 0x2F, 0xB8)
ACCENT_LT  = RGBColor(0xEC, 0xEA, 0xFD)
TEAL       = RGBColor(0x10, 0xA9, 0xA2)
TEAL_LT    = RGBColor(0xE2, 0xF6, 0xF5)
AMBER      = RGBColor(0xE0, 0x8B, 0x1E)
AMBER_LT   = RGBColor(0xFD, 0xF1, 0xDE)
ROSE       = RGBColor(0xD2, 0x3F, 0x6C)
ROSE_LT    = RGBColor(0xFC, 0xE6, 0xED)
DARK_BG    = RGBColor(0x0D, 0x10, 0x28)
DARK_BG_2  = RGBColor(0x1A, 0x1E, 0x45)
DARK_RING  = RGBColor(0x2A, 0x2F, 0x63)
DARK_TXT   = RGBColor(0xA9, 0xAE, 0xCB)

FONT = "Segoe UI"
MONO = "Consolas"

# ---------------------------------------------------------------- geometry
SLIDE_W, SLIDE_H = 13.333, 7.5
ML = 0.62                     # left margin
CW = SLIDE_W - 2 * ML         # content width
BODY_TOP = 1.95
BODY_BOT = 6.78

_warnings = []


def C(hexstr):
    return RGBColor.from_string(hexstr)


# ---------------------------------------------------------------- setup
def new_deck():
    prs = Presentation()
    prs.slide_width = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)
    return prs


def blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def bg(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def bg_gradient(slide, c1, c2, angle=45.0):
    """Full-bleed gradient painted as a shape, so it renders identically everywhere."""
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = c1
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0,
                                slide.part.package.presentation_part.presentation.slide_width,
                                slide.part.package.presentation_part.presentation.slide_height)
    fill = sh.fill
    fill.gradient()
    try:
        fill.gradient_angle = angle
    except Exception:
        pass
    stops = fill.gradient_stops
    stops[0].color.rgb = c1
    stops[0].position = 0.0
    stops[1].color.rgb = c2
    stops[1].position = 1.0
    sh.line.fill.background()
    sh.shadow.inherit = False
    return sh


# ---------------------------------------------------------------- shapes
def shape(slide, x, y, w, h, fill=None, line=None, line_w=1.0,
          radius=None, kind=MSO_SHAPE.ROUNDED_RECTANGLE, dash=None):
    sh = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    if radius is not None:
        try:
            sh.adjustments[0] = radius
        except Exception:
            pass
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(line_w)
        if dash:
            sh.line.dash_style = dash
    sh.shadow.inherit = False
    sh.text_frame.word_wrap = True
    return sh


def rect(slide, x, y, w, h, fill=None, line=None, line_w=1.0, dash=None):
    return shape(slide, x, y, w, h, fill=fill, line=line, line_w=line_w,
                 radius=0.0, kind=MSO_SHAPE.RECTANGLE, dash=dash)


def hline(slide, x, y, w, color=LINE, width=1.0):
    conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(y),
                                      Inches(x + w), Inches(y))
    conn.line.color.rgb = color
    conn.line.width = Pt(width)
    return conn


def vline(slide, x, y, h, color=LINE, width=1.0):
    conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(y),
                                      Inches(x), Inches(y + h))
    conn.line.color.rgb = color
    conn.line.width = Pt(width)
    return conn


def arrow(slide, x1, y1, x2, y2, color=MUTED, width=1.2, head=True, dashed=False):
    conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1),
                                      Inches(x2), Inches(y2))
    conn.line.color.rgb = color
    conn.line.width = Pt(width)
    ln = conn.line.fill._xPr.find(qn("a:ln"))
    if ln is None:
        ln = conn._element.spPr.get_or_add_ln()
    if dashed:
        d = etree.SubElement(ln, qn("a:prstDash"))
        d.set("val", "dash")
    if head:
        tail = etree.SubElement(ln, qn("a:tailEnd"))
        tail.set("type", "triangle")
        tail.set("w", "med")
        tail.set("len", "med")
    return conn


# ---------------------------------------------------------------- text
def _rgb(c):
    return c if isinstance(c, RGBColor) else C(c)


def _run(para, text, size, color, bold, italic, font, spc=None, caps=False):
    r = para.add_run()
    r.text = text
    f = r.font
    f.name = font
    f.size = Pt(size)
    f.bold = bold
    f.italic = italic
    f.color.rgb = _rgb(color)
    if spc is not None:
        r.font._rPr.set("spc", str(int(spc)))
    if caps:
        r.font._rPr.set("cap", "all")
    return r


run_text = _run


def _estimate_height(paras, size, width_in, line_spacing):
    total = 0.0
    for p in paras:
        runs = p if isinstance(p, list) else [(p, {})]
        s = "".join(t for t, _ in runs)
        cpl = max(6, int((width_in * 72.0) / (size * 0.505)))
        lines = max(1, math.ceil(len(s) / cpl))
        total += lines * size * 1.2 * line_spacing / 72.0
    return total


def text(slide, x, y, w, h, content, size=14, color=BODY, bold=False,
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, line_spacing=1.12,
         space_after=0, font=FONT, italic=False, spc=None, caps=False,
         check=True, tag=""):
    """content: str | list of (str | list of (text, style-dict))."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    paras = content if isinstance(content, list) else [content]
    # a bare list of runs is a single paragraph
    if paras and all(isinstance(x, tuple) for x in paras):
        paras = [paras]
    for i, p in enumerate(paras):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = align
        para.line_spacing = line_spacing
        para.space_after = Pt(space_after)
        runs = p if isinstance(p, list) else [(p, {})]
        for t, kw in runs:
            _run(para, t, kw.get("size", size), kw.get("color", color),
                 kw.get("bold", bold), kw.get("italic", italic),
                 kw.get("font", font), kw.get("spc", spc), kw.get("caps", caps))
    if check:
        need = _estimate_height(paras, size, w, line_spacing)
        if need > h * 1.03:
            _warnings.append(f"OVERFLOW {tag!r} need {need:.2f}in > box {h:.2f}in :: "
                             f"{str(paras[0])[:70]}")
    return tb


def bullets(slide, x, y, w, h, items, size=14.5, color=BODY, gap=10,
            bullet_color=ACCENT, lead_bold=True, line_spacing=1.14,
            indent=0.24, glyph="\u25CF", glyph_size=6.5, check=True, tag="",
            anchor=MSO_ANCHOR.TOP):
    """items: list of (lead, rest) | list of str."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    marL = int(Inches(indent))
    for i, item in enumerate(items):
        lead, rest = (item, None) if isinstance(item, str) else item
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.line_spacing = line_spacing
        para.space_after = Pt(gap if i < len(items) - 1 else 0)
        pPr = para._p.get_or_add_pPr()
        pPr.set("marL", str(marL))
        pPr.set("indent", str(-marL))
        _run(para, glyph + " ", glyph_size, bullet_color, False, False, FONT)
        if lead:
            _run(para, lead, size, INK if lead_bold else color, lead_bold, False, FONT)
        if rest:
            _run(para, rest, size, color, False, False, FONT)
    if check:
        est = sum(max(1, math.ceil((len((a or "") + (b or "")) + 2) /
                                   max(6, int((w - indent) * 72 / (size * 0.505))))
                      ) * size * 1.2 * line_spacing / 72 + gap / 72 for a, b in
                  [(it, None) if isinstance(it, str) else it for it in items])
        if est > h * 1.03:
            _warnings.append(f"OVERFLOW bullets {tag!r} need {est:.2f}in > {h:.2f}in")
    return tb


# ---------------------------------------------------------------- page furniture
def chrome(slide, eyebrow, title, page, lede=None, accent=ACCENT,
           title_size=29, lede_w=None):
    text(slide, ML, 0.40, CW, 0.24, [(eyebrow, {"color": accent, "bold": True,
                                                "spc": 130, "size": 9.5, "caps": True})],
         size=9.5, check=False)
    ty = 0.68
    th = 0.62 if not lede else 0.60
    n = len(title)
    size = title_size if n <= 46 else (27.0 if n <= 56 else 25.0)
    text(slide, ML, ty if size > 26 else ty + 0.03, CW, th, title, size=size, color=INK,
         bold=True, line_spacing=1.02, check=False)
    if lede:
        text(slide, ML, ty + th + 0.06, lede_w or CW * 0.78, 0.50, lede,
             size=13, color=MUTED, line_spacing=1.15)
    # footer
    hline(slide, ML, 6.98, CW, LINE, 0.75)
    text(slide, ML, 7.06, 8.0, 0.22,
         "Chike Egonu  \u00b7  Explainable Music Recommender Systems  \u00b7  MSc Viva",
         size=8.5, color=MUTED, spc=20, check=False)
    text(slide, SLIDE_W - ML - 1.2, 7.06, 1.2, 0.22, f"{page:02d}", size=8.5,
         color=MUTED, align=PP_ALIGN.RIGHT, bold=True, check=False)


def notes(slide, body):
    tf = slide.notes_slide.notes_text_frame
    tf.text = body.strip()


# ---------------------------------------------------------------- components
def pill(slide, x, y, w, h, label, fg=ACCENT_DK, bg=ACCENT_LT, size=8.5, bold=True):
    shape(slide, x, y, w, h, fill=bg, line=None, radius=0.5, kind=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(slide, x + 0.06, y + (h - 0.19) / 2, w - 0.12, 0.19, label, size=size,
         color=fg, bold=bold, align=PP_ALIGN.CENTER, caps=True, spc=60, check=False)


def card(slide, x, y, w, h, title=None, body=None, num=None, accent=ACCENT,
         fill=WHITE, border=LINE, title_size=14.5, body_size=11.8, pad=0.26,
         num_bg=None, top_bar=False, shadow=False):
    shape(slide, x, y, w, h, fill=fill, line=border, line_w=1.0, radius=0.07)
    cy = y + pad
    if top_bar:
        rect(slide, x + pad, y, 0.62, 0.055, fill=accent)
    if num is not None:
        d = 0.36
        shape(slide, x + pad, cy, d, d, fill=num_bg or accent, line=None,
              radius=0.5, kind=MSO_SHAPE.OVAL)
        text(slide, x + pad, cy + 0.055, d, 0.26, str(num), size=10.5, color=WHITE,
             bold=True, align=PP_ALIGN.CENTER, check=False)
        cy += d + 0.13
    if title:
        th = 0.30 if len(title) < 34 else 0.58
        text(slide, x + pad, cy, w - 2 * pad, th, title, size=title_size,
             color=INK, bold=True, line_spacing=1.05, check=False)
        cy += th + 0.05
    if body:
        text(slide, x + pad, cy, w - 2 * pad, y + h - cy - 0.14, body,
             size=body_size, color=BODY, line_spacing=1.14)


def stat(slide, x, y, w, h, value, label, accent=INK, sub=None, fill=WHITE,
         border=LINE, value_size=30):
    shape(slide, x, y, w, h, fill=fill, line=border, line_w=1.0, radius=0.08)
    rect(slide, x, y, 0.05, h, fill=accent)
    text(slide, x + 0.22, y + 0.16, w - 0.34, 0.5, value, size=value_size,
         color=INK, bold=True, line_spacing=0.95, check=False)
    ly = y + 0.16 + value_size / 72.0 * 0.95 + 0.06
    text(slide, x + 0.22, ly, w - 0.34, 0.5, label, size=9.2, color=MUTED,
         caps=True, spc=50, line_spacing=1.15)
    if sub:
        text(slide, x + 0.22, y + h - 0.36, w - 0.34, 0.26, sub, size=9.2,
             color=accent if accent != INK else MUTED, bold=True, check=False)


def _border(cell, color=None, width=9525):
    tcPr = cell._tc.get_or_add_tcPr()
    for s in ("L", "R", "T", "B"):
        for e in tcPr.findall(qn("a:ln%s" % s)):
            tcPr.remove(e)
    for s in ("B", "T", "R", "L"):
        ln = etree.Element(qn("a:ln%s" % s))
        ln.set("w", str(width))
        ln.set("cap", "flat")
        ln.set("cmpd", "sng")
        ln.set("algn", "ctr")
        if color is None:
            etree.SubElement(ln, qn("a:noFill"))
        else:
            f = etree.SubElement(ln, qn("a:solidFill"))
            c = etree.SubElement(f, qn("a:srgbClr"))
            c.set("val", str(color))
        tcPr.insert(0, ln)


def table(slide, x, y, w, data, col_w, header_h=0.40, row_h=0.36,
          font_size=10.5, header_size=9.2, aligns=None, header_fill=INK,
          band=WASH, first_bold=False, row_fills=None, header_color=WHITE,
          cell_colors=None, bold_cells=None, rule_color=None):
    rows, cols = len(data), len(data[0])
    h = header_h + row_h * (rows - 1)
    gf = slide.shapes.add_table(rows, cols, Inches(x), Inches(y), Inches(w), Inches(h))
    tbl = gf.table
    tbl.first_row = False
    tbl.horz_banding = False
    tbl.vert_banding = False
    for j, cw in enumerate(col_w):
        tbl.columns[j].width = Inches(cw)
    tbl.rows[0].height = Inches(header_h)
    for i in range(1, rows):
        tbl.rows[i].height = Inches(row_h)
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            cell = tbl.cell(i, j)
            cell.margin_left = Inches(0.09)
            cell.margin_right = Inches(0.09)
            cell.margin_top = Inches(0.02)
            cell.margin_bottom = Inches(0.02)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            if i == 0:
                cell.fill.fore_color.rgb = header_fill
            elif row_fills and row_fills.get(i):
                cell.fill.fore_color.rgb = row_fills[i]
            else:
                cell.fill.fore_color.rgb = band if i % 2 == 0 else WHITE
            _border(cell, rule_color)
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            a = (aligns[j] if aligns else "l")
            p.alignment = {"l": PP_ALIGN.LEFT, "r": PP_ALIGN.RIGHT,
                           "c": PP_ALIGN.CENTER}[a]
            p.line_spacing = 1.0
            col = header_color if i == 0 else BODY
            bold = True if i == 0 else (first_bold and j == 0)
            if cell_colors and (i, j) in cell_colors:
                col = cell_colors[(i, j)]
            if bold_cells and (i, j) in bold_cells:
                bold = True
            _run(p, str(val), header_size if i == 0 else font_size, col, bold,
                 False, FONT, spc=90 if i == 0 else None)
    return gf


def picture(slide, path, x, y, w=None, h=None, caption=None, caption_size=9.5,
            frame=True, cap_y=None):
    kw = {}
    if w:
        kw["width"] = Inches(w)
    if h:
        kw["height"] = Inches(h)
    pic = slide.shapes.add_picture(path, Inches(x), Inches(y), **kw)
    if frame:
        pic.line.color.rgb = LINE
        pic.line.width = Pt(0.75)
    if caption:
        ph = pic.height / 914400.0
        pw = pic.width / 914400.0
        text(slide, x, cap_y if cap_y is not None else y + ph + 0.09, pw, 0.30,
             caption, size=caption_size, color=MUTED, line_spacing=1.1)
    return pic


def waveform(slide, x, y, w, h, color_a, color_b, heights, n=None, gap=0.055):
    """Centred bar motif; heights is a list of 0..1 values."""
    vals = heights
    n = len(vals)
    bw = (w - gap * (n - 1)) / n
    for i, v in enumerate(vals):
        bh = max(0.035, v * h)
        col = color_a if i % 3 else color_b
        shape(slide, x + i * (bw + gap), y + (h - bh) / 2, bw, bh,
              fill=col, line=None, radius=0.5)


def rings(slide, cx, cy, diameters, color=DARK_RING, width=1.1):
    for d in diameters:
        sh = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx - d / 2), Inches(cy - d / 2),
                                    Inches(d), Inches(d))
        sh.fill.background()
        sh.line.color.rgb = color
        sh.line.width = Pt(width)
        sh.shadow.inherit = False


def grid_pattern(slide, x, y, w, h, step=0.28, color=None, size=0.018):
    color = color or RGBColor(0x18, 0x1C, 0x3E)
    ny = int(h / step)
    nx = int(w / step)
    for i in range(nx):
        for j in range(ny):
            shape(slide, x + i * step, y + j * step, size, size, fill=color,
                  line=None, radius=0.0, kind=MSO_SHAPE.OVAL)


def divider(prs, number, title, blurb, sections, page, accent=TEAL):
    slide = blank(prs)
    bg_gradient(slide, DARK_BG, DARK_BG_2, 40)
    rings(slide, 11.6, 2.2, [3.2, 4.6, 6.0, 7.4], DARK_RING, 1.0)
    # giant numeral
    text(slide, ML - 0.06, 1.62, 4.0, 1.9, number, size=118, color=RGBColor(0x25, 0x2A, 0x59),
         bold=True, line_spacing=0.9, check=False)
    rect(slide, ML + 0.03, 3.62, 0.72, 0.045, fill=accent)
    text(slide, ML, 3.86, CW * 0.60, 0.90, title, size=30, color=WHITE, bold=True,
         line_spacing=1.06, check=False)
    text(slide, ML, 5.02, CW * 0.55, 0.80, blurb, size=13.2, color=DARK_TXT,
         line_spacing=1.28)
    # section index
    ix = 8.55
    text(slide, ix, 3.62, 4.2, 0.22, "IN THIS SECTION", size=8.6, color=accent,
         bold=True, spc=130, check=False)
    idx = [[(f"{number}.{i+1}   ", {"color": accent, "bold": True, "size": 8.6}),
            (s, {"color": RGBColor(0xC9, 0xCD, 0xE2), "size": 10.5})]
           for i, s in enumerate(sections)]
    text(slide, ix, 3.94, 4.2, 1.9, idx, size=10.5, color=DARK_TXT,
         space_after=5, check=False)
    waveform(slide, SLIDE_W - ML - 2.6, 5.72, 2.6, 0.5,
             RGBColor(0x39, 0x3E, 0x86), accent,
             [0.2, 0.45, 0.3, 0.75, 0.5, 0.95, 0.6, 0.35, 0.8, 0.55, 0.25, 0.65, 0.4])
    text(slide, ML, 6.62, 6.0, 0.24,
         [(number, {"color": accent, "bold": True}),
          ("   " + title.split(",")[0].upper(), {"color": RGBColor(0x6E, 0x74, 0x9A)})],
         size=8.8, spc=120, check=False)
    notes(slide, f"""SECTION DIVIDER {number} \u2014 {title}. Roughly 10 seconds.

Do not read the list on the right to the audience; it is orientation, not content.

Say one sentence naming what the section establishes, then move. If you are running
long, this is the cheapest place to save 20 seconds \u2014 but keep the section break,
because it gives the examiner a place to interrupt.""")
    return slide


def warnings():
    return _warnings


def save(prs, path):
    prs.save(path)
    return path


# ---------------------------------------------------------------- extras
def chip_flow(slide, x, y, w, items, h=0.33, gap=0.14, size=8.6, fg=BODY,
              bg=WASH_2, per_row_h=0.14, pad=0.30):
    """Left-to-right flowing pills; returns the y after the last row."""
    cx, cy = x, y
    for it in items:
        cw = max(0.72, 0.0855 * len(str(it)) * (size / 8.6) + pad)
        if cx + cw > x + w + 0.01:
            cx = x
            cy += h + per_row_h
        shape(slide, cx, cy, cw, h, fill=bg, line=None, radius=0.5,
              kind=MSO_SHAPE.ROUNDED_RECTANGLE)
        text(slide, cx + 0.05, cy + (h - 0.2) / 2, cw - 0.10, 0.2, str(it),
             size=size, color=fg, align=PP_ALIGN.CENTER, check=False)
        cx += cw + gap
    return cy + h


def dbox(slide, x, y, w, h, title, sub=None, fill=WHITE, border=LINE,
         accent=None, title_size=11.2, sub_size=8.8, align=PP_ALIGN.CENTER,
         radius=0.08, dashed=False):
    shape(slide, x, y, w, h, fill=fill, line=border, line_w=1.1, radius=radius,
          dash=MSO_LINE_DASH_STYLE.DASH if dashed else None)
    if accent:
        rect(slide, x, y + 0.10, 0.045, h - 0.20, fill=accent)
    th = 0.24 if sub else h - 0.06
    ty = y + (h - (0.34 if sub else 0.24)) / 2 - (0.10 if sub else 0)
    text(slide, x + 0.06, ty, w - 0.12, th, title, size=title_size, color=INK,
         bold=True, align=align, line_spacing=1.0, check=False)
    if sub:
        text(slide, x + 0.06, ty + 0.26, w - 0.12, h - (ty - y) - 0.30, sub,
             size=sub_size, color=MUTED, align=align, line_spacing=1.05, check=False)


def label(slide, x, y, w, txt, color=MUTED, size=8.6):
    text(slide, x, y, w, 0.22, txt, size=size, color=color, bold=True, spc=110,
         caps=True, check=False)


def statement(slide, x, y, w, h, txt, size=14, color=INK, bg=WASH, accent=ACCENT,
              bold=False, italic=False, pad=0.30, body_color=None):
    shape(slide, x, y, w, h, fill=bg, line=None, radius=0.05)
    rect(slide, x, y, 0.06, h, fill=accent)
    text(slide, x + pad, y + 0.14, w - 2 * pad, h - 0.24, txt, size=size,
         color=body_color or color, bold=bold, italic=italic, line_spacing=1.18,
         anchor=MSO_ANCHOR.MIDDLE)
