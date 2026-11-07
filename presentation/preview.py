"""Approximate PPTX rasteriser for visual QA (no LibreOffice in this sandbox).

Draws rectangles, ovals, pictures and text at the real slide geometry so that
layout problems (overlaps, clipped text, misalignment) are visible. Text metrics
use DejaVu Sans, which is wider than Segoe UI, so any overflow seen here is a
worst case.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.util import Emu

EMU = 914400.0
DPI = 110
OUT = "preview"
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
ITAL = os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf")

_cache = {}


def font(size_pt, bold=False, italic=False):
    px = max(6, int(round(size_pt * DPI / 72.0)))
    key = (px, bold, italic)
    if key not in _cache:
        path = BOLD if bold else (ITAL if italic and os.path.exists(ITAL) else REG)
        _cache[key] = ImageFont.truetype(path, px)
    return _cache[key]


def color_of(fmt, default=None):
    try:
        if fmt.type is not None and "GRADIENT" in str(fmt.type):
            c = fmt.gradient_stops[0].color.rgb
            return (c[0], c[1], c[2])
    except Exception:
        pass
    try:
        if fmt.type is not None and str(fmt.type) == "MSO_FILL_TYPE.SOLID (1)":
            c = fmt.fore_color.rgb
            return (c[0], c[1], c[2])
        if fmt.type is not None and "SOLID" in str(fmt.type):
            c = fmt.fore_color.rgb
            return (c[0], c[1], c[2])
    except Exception:
        pass
    return default


def px(v):
    return v / EMU * DPI


def measure(txt, f):
    b = f.getbbox(txt)
    return b[2] - b[0]


def wrap_runs(runs, maxw):
    """runs: list of (text, font, colour). Returns list of lines of (text,font,colour)."""
    words = []
    for t, f, c in runs:
        parts = t.replace("\n", " ").split(" ")
        for i, w in enumerate(parts):
            words.append((w + (" " if i < len(parts) - 1 else ""), f, c))
    lines, cur, curw = [], [], 0.0
    for w, f, c in words:
        ww = measure(w, f)
        if cur and curw + ww > maxw:
            lines.append(cur)
            cur, curw = [], 0.0
        cur.append((w, f, c))
        curw += ww
    if cur:
        lines.append(cur)
    return lines


def draw_text_frame(d, sh, x, y, w, h):
    tf = sh.text_frame
    anchor = str(tf.vertical_anchor)
    blocks = []
    for p in tf.paragraphs:
        runs = []
        size = 16
        for r in p.runs:
            sz = r.font.size.pt if r.font.size else 16
            f = font(sz, bool(r.font.bold), bool(r.font.italic))
            col = (60, 65, 96)
            try:
                if r.font.color and r.font.color.rgb:
                    c = r.font.color.rgb
                    col = (c[0], c[1], c[2])
            except Exception:
                pass
            runs.append((r.text, f, col))
            size = sz
        if not runs:
            continue
        marL = 0.0
        ind = 0.0
        pPr = p._p.find(
            "{http://schemas.openxmlformats.org/drawingml/2006/main}pPr")
        if pPr is not None:
            marL = float(pPr.get("marL", 0)) / EMU * DPI
            ind = float(pPr.get("indent", 0)) / EMU * DPI
        ls = p.line_spacing or 1.15
        sa = (p.space_after.pt if p.space_after else 0) * DPI / 72.0
        lines = wrap_runs(runs, max(10, w - marL))
        lh = max(f.size for _, f, _ in runs) * 1.22 * ls
        blocks.append((lines, marL, ind, lh, sa, str(p.alignment)))

    total = sum(len(b[0]) * b[3] + b[4] for b in blocks)
    cy = y
    if "MIDDLE" in anchor:
        cy = y + (h - total) / 2
    elif "BOTTOM" in anchor:
        cy = y + h - total

    for lines, marL, ind, lh, sa, align in blocks:
        for i, line in enumerate(lines):
            lw = sum(measure(t, f) for t, f, _ in line)
            if "CENTER" in align:
                cx = x + marL + (w - marL - lw) / 2
            elif "RIGHT" in align:
                cx = x + w - lw
            else:
                cx = x + marL + (ind if i == 0 else 0)
            for t, f, c in line:
                d.text((cx, cy + (lh - f.size * 1.02) / 2), t, font=f, fill=c)
                cx += measure(t, f)
            cy += lh
        cy += sa


def render(path, outdir=OUT, only=None):
    prs = Presentation(path)
    os.makedirs(outdir, exist_ok=True)
    W = int(px(prs.slide_width))
    H = int(px(prs.slide_height))
    made = []
    for i, slide in enumerate(prs.slides, start=1):
        if only and i not in only:
            continue
        img = Image.new("RGB", (W, H), (255, 255, 255))
        d = ImageDraw.Draw(img)
        # background
        try:
            bgc = color_of(slide.background.fill)
            if bgc:
                d.rectangle([0, 0, W, H], fill=bgc)
        except Exception:
            pass
        for sh in slide.shapes:
            try:
                x, y = px(sh.left), px(sh.top)
                w, h = px(sh.width), px(sh.height)
            except Exception:
                continue
            if sh.shape_type == 13:  # picture
                try:
                    im = Image.open(sh.image.blob and __import__("io").BytesIO(sh.image.blob))
                    im = im.convert("RGB").resize((max(1, int(w)), max(1, int(h))))
                    img.paste(im, (int(x), int(y)))
                except Exception:
                    d.rectangle([x, y, x + w, y + h], outline=(200, 200, 210))
                continue
            if sh.has_table:
                tw = sh.table
                cy = y
                for r, row in enumerate(tw.rows):
                    rh = px(row.height)
                    cx = x
                    for c, cell in enumerate(row.cells):
                        cw = px(tw.columns[c].width)
                        fc = color_of(cell.fill, (255, 255, 255))
                        d.rectangle([cx, cy, cx + cw, cy + rh], fill=fc)
                        txt = cell.text_frame.text
                        if txt:
                            head = r == 0
                            f = font(9.6, head)
                            d.text((cx + 6, cy + rh / 2 - f.size / 2), txt, font=f,
                                   fill=(255, 255, 255) if head else (60, 65, 96))
                        cx += cw
                    cy += rh
                continue
            if not hasattr(sh, "fill"):
                try:
                    lc = sh.line.color.rgb
                    d.line([x, y, x + w, y + h], fill=(lc[0], lc[1], lc[2]), width=2)
                except Exception:
                    pass
                continue
            fill = color_of(sh.fill)
            line = None
            try:
                if sh.line.color and sh.line.color.rgb:
                    lc = sh.line.color.rgb
                    line = (lc[0], lc[1], lc[2])
            except Exception:
                pass
            try:
                is_oval = "OVAL" in str(sh.auto_shape_type)
            except Exception:
                is_oval = False
            if is_oval:
                d.ellipse([x, y, x + w, y + h], fill=fill, outline=line,
                          width=2 if line else 0)
            elif fill or line:
                d.rectangle([x, y, x + w, y + h], fill=fill, outline=line,
                            width=2 if line else 0)
            if sh.has_text_frame and sh.text_frame.text.strip():
                draw_text_frame(d, sh, x, y, w, h)
        p = os.path.join(outdir, f"slide_{i:02d}.png")
        img.save(p)
        made.append(p)
    return made


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "/home/user/viva/Chike_Egonu_Viva_Presentation.pptx"
    only = set(int(a) for a in sys.argv[2:]) if len(sys.argv) > 2 else None
    files = render(target, only=only)
    print(f"rendered {len(files)} slides into {OUT}/")
