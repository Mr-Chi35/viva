"""Geometry / collision audit for the generated deck.

No renderer is available in this sandbox, so this script checks the two things a
renderer would catch first: shapes outside the canvas, and text boxes that
collide with other text boxes or with figures.
"""
import sys

from pptx import Presentation
from pptx.util import Emu

EMU = 914400.0
W, H = 13.333, 7.5


def box(sh):
    return (sh.left / EMU, sh.top / EMU, sh.width / EMU, sh.height / EMU)


def inter(a, b):
    x = max(0.0, min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0]))
    y = max(0.0, min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1]))
    return x * y


def has_text(sh):
    return sh.has_text_frame and sh.text_frame.text.strip() != ""


def main(path):
    prs = Presentation(path)
    problems = 0
    for i, slide in enumerate(prs.slides, start=1):
        items = []
        for sh in slide.shapes:
            try:
                b = box(sh)
            except Exception:
                continue
            kind = "pic" if sh.shape_type == 13 else ("txt" if has_text(sh) else "shape")
            if kind == "shape" and sh.has_table:
                kind = "table"
            items.append((kind, b, sh))

        # out of canvas
        for kind, b, sh in items:
            if b[0] < -0.02 or b[1] < -0.02 or b[0] + b[2] > W + 0.02 or b[1] + b[3] > H + 0.02:
                print(f"[{i:02d}] OFF-CANVAS {kind} {b[0]:.2f},{b[1]:.2f} "
                      f"{b[2]:.2f}x{b[3]:.2f}  {sh.text_frame.text[:40] if has_text(sh) else ''}")
                problems += 1
            if kind == "txt" and not sh.text_frame.text.strip() == "":
                t = sh.text_frame.text.strip()
                if b[0] < 0.40 or b[0] + b[2] > W - 0.35:
                    print(f"[{i:02d}] WIDE-TEXT {b[0]:.2f}..{b[0]+b[2]:.2f}  {t[:50]}")
                    problems += 1

        # collisions between text/picture items
        cand = [(k, b, sh) for (k, b, sh) in items if k in ("txt", "pic", "table")]
        for a in range(len(cand)):
            for bb in range(a + 1, len(cand)):
                k1, b1, s1 = cand[a]
                k2, b2, s2 = cand[bb]
                if k1 == "table" and k2 == "table":
                    continue
                ov = inter(b1, b2)
                if ov > 0.055:
                    t1 = s1.text_frame.text[:34].replace("\n", " ") if has_text(s1) else "<pic>"
                    t2 = s2.text_frame.text[:34].replace("\n", " ") if has_text(s2) else "<pic>"
                    print(f"[{i:02d}] COLLIDE {ov:.2f}in2  '{t1}'  x  '{t2}'")
                    problems += 1
    print(f"\n{problems} potential problems across {len(prs.slides.__iter__.__self__._sldIdLst)} slides")
    return problems


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else
                        "/home/user/viva/Chike_Egonu_Viva_Presentation.pptx") == 0 else 0)
