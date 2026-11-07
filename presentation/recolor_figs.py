"""
Re-tone the figures lifted from the report PDF so they sit in the deck palette.

Only hue is changed: every figure keeps its geometry, labels, values and legends.
Each source colour is decomposed against the white background, the coverage alpha is
recovered, and the same alpha is re-applied in the target colour, so anti-aliased
edges stay clean.

Source                                  Target
  steel blue   #4682B4 / #6294BF   ->   warm taupe #A8998B (single-series plots)
  steel blue   #4682B4             ->   graphite   #3A3330 (negative bars, fig 6)
  tomato       #FF6347             ->   accent     #D55816
  dark orange  #FF8C00             ->   accent     #D55816
"""
import os

from PIL import Image

ASSETS = os.path.join(os.path.dirname(__file__), "assets")

STEEL = (0x46, 0x82, 0xB4)
STEEL2 = (0x62, 0x94, 0xBF)
TOMATO = (0xFF, 0x63, 0x47)
DORANGE = (0xFF, 0x8C, 0x00)

TAUPE = (0xA8, 0x99, 0x8B)
GRAPHITE = (0x3A, 0x33, 0x30)
ACCENT = (0xD5, 0x58, 0x16)

JOBS = [
    ("fig2_acoustic_dists.png", "fig2_acoustic_dist_warm.png",
     {STEEL: TAUPE, STEEL2: TAUPE}),
    ("fig7_spearman.png", "fig7_spearman_warm.png",
     {STEEL: TAUPE, TOMATO: ACCENT}),
    ("fig4_loss_curves.png", "fig4_loss_curves_warm.png",
     {STEEL: (0x6E, 0x62, 0x59), DORANGE: ACCENT}),
    ("fig6_pair_crop.png", "fig6_pair_warm.png",
     {STEEL: GRAPHITE, TOMATO: ACCENT}),
]


def coverage(px, src):
    """Fraction of `src` mixed into white that produced `px` (0..1)."""
    num = den = 0.0
    for p, s in zip(px, src):
        d = 255.0 - s
        if d > 12:
            num += (255.0 - p) / d
            den += 1.0
    return max(0.0, min(1.0, num / den)) if den else 0.0


def residual(px, src):
    """How far `px` sits off the white->src line, in RGB units."""
    a = coverage(px, src)
    return sum(abs(p - (255.0 - a * (255.0 - s))) for p, s in zip(px, src)) / 3.0


def recolor(img, mapping):
    out = Image.new("RGB", img.size)
    src_px = img.load()
    dst = out.load()
    items = list(mapping.items())
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            p = src_px[x, y]
            best, best_res = None, 1e9
            for src, tgt in items:
                r = residual(p, src)
                if r < best_res:
                    best, best_res = (src, tgt), r
            if best is None or best_res > 26 or coverage(p, best[0]) < 0.04:
                dst[x, y] = p
                continue
            src, tgt = best
            a = coverage(p, src)
            dst[x, y] = tuple(int(round(255.0 - a * (255.0 - t))) for t in tgt)
    return out


def main():
    for name, out_name, mapping in JOBS:
        src = os.path.join(ASSETS, name)
        img = Image.open(src).convert("RGB")
        recolor(img, mapping).save(os.path.join(ASSETS, out_name))
        print("wrote", out_name)


if __name__ == "__main__":
    main()
