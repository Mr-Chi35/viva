"""
Regenerate the report's data charts from the numbers reported in its tables,
using a single consistent visual language that matches the slide deck.

Figures taken directly from the PDF are kept in assets/ and are only the
genuine analysis artefacts (SHAP beeswarm, SHAP-vs-LIME, Spearman histogram,
catalogue/acoustic distributions).
"""
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch

OUT = os.path.join(os.path.dirname(__file__), "charts")
os.makedirs(OUT, exist_ok=True)

INK = "#231F20"
BODY = "#4A4340"
MUTED = "#8B847E"
GRID = "#E6E1DB"
ACCENT = "#D55816"
ACCENT2 = "#9E3E0D"
AMBER = "#B8791E"
ROSE = "#8E3A2C"
SLATE = "#CFC7BF"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.edgecolor": GRID,
    "axes.labelcolor": BODY,
    "text.color": INK,
    "xtick.color": BODY,
    "ytick.color": BODY,
    "axes.titleweight": "bold",
    "figure.dpi": 100,
    "savefig.dpi": 220,
})


def clean(ax, grid_axis="y", spines=("top", "right")):
    for s in spines:
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)
    if grid_axis:
        ax.grid(axis=grid_axis, color=GRID, linewidth=0.9, alpha=0.9)
        ax.set_axisbelow(True)


def save(fig, name, transparent=False):
    path = os.path.join(OUT, name)
    fig.savefig(path, bbox_inches="tight", pad_inches=0.06,
                transparent=transparent, facecolor="none" if transparent else "white")
    plt.close(fig)
    print("wrote", path)


# ----------------------------------------------------------------------------
# 1. Offline accuracy at K = 10  (report Table, Section 4.2)
# ----------------------------------------------------------------------------
models = ["Popularity", "Content-based\n(cosine)", "SVD-MF", "NCF", "Hybrid\nNCF + Content"]
metrics = ["P@10", "R@10", "NDCG@10", "MRR"]
data = {
    "Popularity":          [0.0104, 0.0349, 0.0239, 0.0458],
    "Content-based\n(cosine)": [0.0014, 0.0037, 0.0027, 0.0095],
    "SVD-MF":              [0.0424, 0.1225, 0.0769, 0.1121],
    "NCF":                 [0.0173, 0.0453, 0.0342, 0.0736],
    "Hybrid\nNCF + Content": [0.0184, 0.0538, 0.0384, 0.0752],
}
colors = [SLATE, "#E2DCD5", "#3A3330", "#A8998B", ACCENT]

fig, ax = plt.subplots(figsize=(9.6, 4.0))
x = np.arange(len(metrics))
w = 0.16
for i, (m, c) in enumerate(zip(models, colors)):
    vals = data[m]
    off = (i - 2) * w
    bars = ax.bar(x + off, vals, w * 0.92, label=m.replace("\n", " "),
                  color=c, edgecolor="none", zorder=3)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.0022, f"{v:.3f}",
                ha="center", va="bottom", fontsize=6.4, color=BODY, rotation=90)

ax.set_xticks(x)
ax.set_xticklabels(metrics, fontsize=10.5, color=INK)
ax.set_ylim(0, 0.155)
ax.set_ylabel("score", fontsize=10)
clean(ax)
ax.legend(frameon=False, ncol=5, fontsize=8.2, loc="upper center",
          bbox_to_anchor=(0.5, 1.14), handlelength=1.1, columnspacing=1.4)
ax.tick_params(axis="y", labelsize=9)
save(fig, "accuracy_k10.png")


# ----------------------------------------------------------------------------
# 2. Hybrid over NCF: relative gain per metric
# ----------------------------------------------------------------------------
gains = [("Precision@10", 0.0184, 0.0173), ("Recall@10", 0.0538, 0.0453),
         ("NDCG@10", 0.0384, 0.0342), ("MRR", 0.0752, 0.0736)]
labels = [g[0] for g in gains]
rel = [(h / n - 1) * 100 for _, h, n in gains]

fig, ax = plt.subplots(figsize=(7.4, 2.9))
y = np.arange(len(rel))[::-1]
bars = ax.barh(y, rel, height=0.52, color=[ACCENT] * len(rel), edgecolor="none", zorder=3)
for b, v in zip(bars, rel):
    ax.text(v + 0.45, b.get_y() + b.get_height() / 2, f"+{v:.1f}%",
            va="center", ha="left", fontsize=11, fontweight="bold", color=INK)
ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=10.5, color=INK)
ax.set_xlim(0, max(rel) * 1.28)
ax.set_xlabel("relative improvement over NCF-only (%)", fontsize=9.5)
clean(ax, grid_axis="x")
ax.tick_params(axis="x", labelsize=9)
save(fig, "hybrid_gain.png")


# ----------------------------------------------------------------------------
# 3. The SVD-MF anomaly -- NDCG@10
# ----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.0, 2.75))
names = ["Popularity", "NCF", "Hybrid", "SVD-MF"]
vals = [0.0239, 0.0342, 0.0384, 0.0769]
cols = ["#CFC7BF", "#A8998B", ACCENT, "#3A3330"]
bars = ax.bar(names, vals, width=0.5, color=cols, edgecolor="none", zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.0025, f"{v:.4f}",
            ha="center", fontsize=9.5, color=INK, fontweight="bold")
ax.annotate("2.0× the hybrid model",
            xy=(3, 0.0785), xytext=(1.15, 0.068),
            fontsize=9.2, color=ACCENT, ha="left", va="center",
            arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.1,
                            shrinkA=6, shrinkB=4,
                            connectionstyle="arc3,rad=-0.18"))
ax.set_ylim(0, 0.092)
ax.set_xlim(-0.55, 3.45)
ax.set_ylabel("NDCG@10", fontsize=10)
clean(ax)
ax.tick_params(axis="both", labelsize=10)
save(fig, "svd_gap.png")


# ----------------------------------------------------------------------------
# 4. Global SHAP importance (report Table, Section 4.3)
# ----------------------------------------------------------------------------
feats = ["Instrumentalness", "Energy", "Danceability", "Valence", "Speechiness",
         "Tempo", "Acousticness", "Loudness", "Liveness"]
imps = [0.04047, 0.02512, 0.02348, 0.01719, 0.01693, 0.01626, 0.01553, 0.01301, 0.01270]

fig, ax = plt.subplots(figsize=(6.9, 3.5))
y = np.arange(len(feats))[::-1]
ramp = ["#A8490F", "#B8510F", "#C9560F", "#D55816", "#DD6A2C",
        "#E47E45", "#EA9361", "#F0A87D", "#F6BD9A"]
bars = ax.barh(y, imps, height=0.62, color=ramp, edgecolor="none", zorder=3)
for b, v in zip(bars, imps):
    ax.text(v + 0.0009, b.get_y() + b.get_height() / 2, f"{v:.4f}",
            va="center", fontsize=8.8, color=BODY)
ax.set_yticks(y)
ax.set_yticklabels(feats, fontsize=10, color=INK)
ax.set_xlim(0, 0.047)
ax.set_xlabel("mean |SHAP value|  (surrogate model)", fontsize=9.5)
clean(ax, grid_axis="x")
ax.tick_params(axis="x", labelsize=8.5)
save(fig, "shap_importance.png")


# ----------------------------------------------------------------------------
# 5. Train / validation / test split
# ----------------------------------------------------------------------------
tr, va, te = 1351773, 191179, 388153
tot = tr + va + te
fig, ax = plt.subplots(figsize=(9.0, 1.15))
segs = [(tr, "Train", "#3A3330"), (va, "Validation", ACCENT), (te, "Test", "#B4A296")]
left = 0
for v, lab, c in segs:
    ax.barh(0, v / tot * 100, left=left, height=0.55, color=c, edgecolor="white", lw=1.6)
    ax.text(left + v / tot * 50, 0, f"{lab}\n{v:,}  ({v/tot*100:.0f}%)",
            ha="center", va="center", color="white", fontsize=9.6, fontweight="bold")
    left += v / tot * 100
ax.set_xlim(0, 100)
ax.set_ylim(-0.6, 0.6)
ax.axis("off")
save(fig, "split.png")
