"""Slides 6-10: preprocessing, acoustic features, architecture, models, explainers."""
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

from deck_lib import *

ASSETS = "assets"
CHARTS = "charts"


def s_preprocess(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Methodology  \u00b7  \u00a73.1", "Preprocessing and the resulting interaction graph", page,
           lede="Four steps, and the shape of the matrix they produce.")

    steps = [
        ("Three-pass iterative k-core", "Playlists with fewer than 5 matched tracks are "
         "removed; tracks appearing in fewer than 3 distinct playlists are removed. Three "
         "passes, so the removals converge.", "Removes near-empty playlists and "
         "singleton tracks"),
        ("Implicit feedback matrix", "A user (playlist) \u00d7 track matrix is built from "
         "playlist co-occurrence, which is the only signal MPD provides.",
         "No explicit ratings"),
        ("Z-score normalisation", "All 9 continuous acoustic features are standardised "
         "before the content branch.", "Loudness in dB, tempo in BPM"),
        ("70 / 10 / 20 split", "Random split rather than temporal, because MPD playlists "
         "carry no reliable interaction-level timestamp.", "Listed as a limitation"),
    ]
    for i, (t, b, why) in enumerate(steps):
        y = 2.14 + i * 1.02
        shape(s, ML, y, 6.05, 0.94, fill=WHITE, line=LINE, radius=0.05)
        shape(s, ML + 0.22, y + 0.25, 0.40, 0.40, fill=WASH_2, line=None, radius=0.5,
              kind=MSO_SHAPE.OVAL)
        text(s, ML + 0.22, y + 0.32, 0.40, 0.26, str(i + 1), size=10.4, color=ACCENT,
             bold=True, align=PP_ALIGN.CENTER, check=False)
        text(s, ML + 0.76, y + 0.11, 3.3, 0.26, t, size=11.0, color=INK, bold=True,
             check=False)
        text(s, ML + 0.76, y + 0.37, 4.05, 0.50, b, size=9.0, color=BODY, line_spacing=1.14)
        text(s, ML + 4.86, y + 0.30, 1.10, 0.44, why, size=7.8, color=TEAL, italic=True,
             line_spacing=1.10)

    x2 = 6.85
    label(s, x2, 2.10, 5.8, "Resulting interaction graph")
    tiles = [("96,827", "playlists (users)"), ("20,042", "tracks (items)"),
             ("1,931,105", "interactions"), ("99.93%", "matrix sparsity")]
    for i, (v, l) in enumerate(tiles):
        x = x2 + (i % 2) * 3.06
        y = 2.40 + (i // 2) * 0.92
        shape(s, x, y, 2.80, 0.86, fill=WHITE, line=LINE, radius=0.06)
        rect(s, x, y, 0.05, 0.86, fill=ACCENT if i < 3 else ROSE)
        text(s, x + 0.20, y + 0.10, 2.5, 0.38, v, size=19, color=INK, bold=True,
             line_spacing=0.95, check=False)
        text(s, x + 0.20, y + 0.54, 2.5, 0.22, l, size=8.4, color=MUTED, caps=True,
             spc=40, check=False)

    label(s, x2, 4.32, 5.6, "Random 70 / 10 / 20 split")
    segs = [(1351773, "Train", RGBColor(0x3A, 0x33, 0x30)), (191179, "", ACCENT),
            (388153, "Test", TEAL)]
    tot = sum(x[0] for x in segs)
    left = 0.0
    for v, lab_txt, col in segs:
        w = 5.86 * v / tot
        rect(s, x2 + left, 4.60, w - 0.02, 0.32, fill=col)
        if lab_txt:
            text(s, x2 + left, 4.66, w - 0.02, 0.22, lab_txt, size=8.2, color=WHITE,
                 bold=True, align=PP_ALIGN.CENTER, caps=True, spc=60, check=False)
        left += w
    legend = [("Train", "1,351,773 \u00b7 70%", RGBColor(0x3A, 0x33, 0x30)),
              ("Validation", "191,179 \u00b7 10%", ACCENT), ("Test", "388,153 \u00b7 20%", TEAL)]
    for i, (n, v, col) in enumerate(legend):
        x = x2 + i * 1.96
        rect(s, x, 5.04, 0.09, 0.09, fill=col)
        text(s, x + 0.16, 4.99, 1.78, 0.20, n, size=8.2, color=BODY, bold=True, check=False)
        text(s, x + 0.16, 5.17, 1.78, 0.20, v, size=8.0, color=MUTED, check=False)

    text(s, x2, 5.52, 5.86, 0.52,
         "Top-10 tracks are 2.1% of interactions. Genre metadata is missing for 28,335 of "
         "50,683 tracks (55.9%).", size=9.0, color=BODY, line_spacing=1.16)

    hline(s, ML, 6.32, CW, LINE, 0.75)
    text(s, ML, 6.40, CW, 0.42,
         "Audio features were matched from a pre-fetched catalogue on normalised "
         "artist\u2013title pairs, because Spotify restricts the public audio-features "
         "endpoint. The same nine acoustic dimensions are used; cross-domain validation is "
         "deferred.", size=8.5, color=MUTED, italic=True, line_spacing=1.14)

    notes(s, """
"Four preprocessing steps.

The k-core is iterative and runs three passes: drop playlists with fewer than
five matched tracks, drop tracks in fewer than three playlists, repeat. That
stops the evaluation being dominated by accidental one-track playlists.

Z-scoring matters because loudness is in decibels and tempo is in BPM.

And the split is random, not temporal. MPD has no reliable interaction-level
timestamp, so a temporal split would be arbitrary; I list it as a limitation
because it means drift is not modelled.

The result is 96,827 playlists, 20,042 tracks, 1.93 million interactions, 99.93%
sparse. The footnote is the deviation I need to declare: the audio features come
from a matched catalogue rather than the live API, because that endpoint is
restricted. The nine dimensions are unchanged."
""")
    return page + 1


def s_acoustic(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Methodology  \u00b7  \u00a74.1", "The acoustic features are skewed and correlated", page,
           lede="These correlations matter for the SHAP\u2013LIME comparison in Section 4.3.")

    picture(s, f"{ASSETS}/fig2_acoustic_dists.png", ML, 2.10, h=4.28, w=None, caption=None)
    text(s, ML, 6.44, 6.0, 0.22,
         "Figure 2  \u00b7  Distributions of the nine acoustic features (matched catalogue).",
         size=8.4, color=MUTED, check=False)

    x2 = 6.85
    label(s, x2, 2.10, 5.8, "Distribution shape")
    bullets(s, x2, 2.38, 5.86, 1.04, [
        ("Heavy skew. ", "Speechiness, acousticness and instrumentalness pile up near zero "
         "with long right tails; energy and loudness skew high."),
        ("Near symmetric. ", "Danceability, valence and tempo are roughly unimodal."),
    ], size=9.8, gap=8, tag="shape")

    label(s, x2, 3.44, 5.8, "Pairwise correlations  |r| \u2265 0.4")
    table(s, x2, 3.74, 5.86,
          [["Feature pair", "r"],
           ["Energy \u2013 Loudness", "+0.78"],
           ["Energy \u2013 Acousticness", "\u22120.73"],
           ["Acousticness \u2013 Loudness", "\u22120.61"],
           ["Danceability \u2013 Valence", "+0.54"]],
          col_w=[3.96, 1.90], row_h=0.32, header_h=0.32, font_size=9.6, header_size=8.6,
          aligns=["l", "r"], rule_color="FFFFFF")

    shape(s, x2, 5.66, 5.86, 0.78, fill=AMBER_LT, line=None, radius=0.05)
    rect(s, x2, 5.66, 0.05, 0.78, fill=AMBER)
    text(s, x2 + 0.24, 5.76, 5.44, 0.60,
         "Both SHAP and LIME can split credit between correlated features, which is one "
         "plausible cause of the disagreement reported later.",
         size=9.2, color=BODY, line_spacing=1.16)

    notes(s, """
"Nine acoustic features, and the shapes matter.

Three of them are effectively zero-inflated with long right tails: speechiness,
acousticness and instrumentalness. Energy and loudness skew high; only
danceability, valence and tempo are near symmetric.

The correlation table is the important part. Energy and loudness correlate at
0.78; energy and acousticness at minus 0.73.

Both SHAP and LIME distribute credit among features, and when features are
strongly correlated that credit can be split or swapped between them. So when I
show you a near-zero agreement between the two methods, there is a mechanism on
the table. What I cannot yet say is how much of the disagreement is collinearity
and how much is the surrogate."
""")
    return page + 1


def s_architecture(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Methodology  \u00b7  \u00a73.2", "Hybrid architecture \u2014 late fusion", page,
           lede="Separability is the design choice that makes feature-level attribution possible.")

    dbox(s, ML, 2.52, 1.72, 0.60, "Playlist ID", fill=WASH, border=LINE, title_size=10.4)
    dbox(s, ML, 3.30, 1.72, 0.60, "Track ID", fill=WASH, border=LINE, title_size=10.4)
    dbox(s, ML, 4.62, 1.72, 0.86, "9 acoustic features", "z-scored", fill=ACCENT_LT,
         border=ACCENT_LT, title_size=9.8, sub_size=8.2, accent=ACCENT)

    dbox(s, 2.82, 2.52, 2.06, 1.38, "Shared embeddings", "d = 32", fill=WHITE, border=LINE,
         title_size=10.8, sub_size=8.6, accent=INK)

    dbox(s, 5.36, 2.36, 2.34, 0.82, "GMF", "element-wise product", fill=WHITE, border=LINE,
         title_size=11, sub_size=8.2)
    dbox(s, 5.36, 3.40, 2.34, 0.82, "MLP", "6 \u2192 32 \u2192 16 \u00b7 ReLU \u00b7 drop 0.3",
         fill=WHITE, border=LINE, title_size=11, sub_size=8.2)
    dbox(s, 5.36, 4.62, 2.34, 0.86, "Content MLP", "9 \u2192 32 \u2192 16", fill=ACCENT_LT,
         border=ACCENT_LT, title_size=10.4, sub_size=8.2, accent=ACCENT)

    dbox(s, 8.22, 3.30, 1.48, 1.24, "Concat", fill=WASH_2, border=LINE, title_size=10.6)
    dbox(s, 10.20, 3.30, 2.50, 0.72, "Linear layer", fill=WHITE, border=ACCENT, title_size=10.6,
         accent=ACCENT)
    dbox(s, 10.20, 4.22, 2.50, 0.62, "score  \u0177 \u2208 (0,1)", fill=ACCENT_LT,
         border=ACCENT, title_size=9.6)

    arrow(s, 2.38, 2.82, 2.80, 3.02, MUTED, 1.1)
    arrow(s, 2.38, 3.60, 2.80, 3.42, MUTED, 1.1)
    arrow(s, 4.90, 2.96, 5.34, 2.82, MUTED, 1.1)
    arrow(s, 4.90, 3.48, 5.34, 3.74, MUTED, 1.1)
    arrow(s, 2.38, 5.05, 5.34, 5.05, ACCENT, 1.1)
    arrow(s, 7.72, 2.78, 8.20, 3.62, MUTED, 1.1)
    arrow(s, 7.72, 3.82, 8.20, 3.82, MUTED, 1.1)
    arrow(s, 7.72, 5.05, 8.58, 5.05, ACCENT, 1.1, head=False)
    arrow(s, 8.58, 5.05, 8.58, 4.58, ACCENT, 1.1)
    arrow(s, 9.72, 3.92, 10.18, 3.72, MUTED, 1.1)
    arrow(s, 11.45, 4.04, 11.45, 4.20, MUTED, 1.1)

    text(s, ML, 5.72, 11.9, 0.62,
         "GMF captures linear interaction, the MLP captures non-linear interaction, and the "
         "content branch sees the track's acoustic properties. Their outputs are concatenated "
         "and scored, so the content contribution stays separable from the collaborative one.",
         size=10.4, color=BODY, line_spacing=1.22)

    pills = ["\u2248 7.49M parameters", "Adam \u00b7 lr 1e-3 \u00b7 wd 1e-5",
             "BCE \u00b7 4 negatives per positive", "5 epochs \u00b7 PyTorch"]
    x = ML
    for p in pills:
        w = 0.078 * len(p) + 0.30
        pill(s, x, 6.42, w, 0.29, p, fg=MUTED, bg=WASH_2, size=8.0)
        x += w + 0.16

    notes(s, """
"This is the model, and one design decision drives the rest.

Two collaborative views of the user-item pair: GMF, which is the linear
interaction, and an MLP over the concatenated embeddings, which captures
non-linear interaction. They share a 32-dimensional embedding space, which is the
NCF design from He and colleagues.

The third branch only sees the nine acoustic features, through a two-layer
network.

The key word is late: I fused at the output rather than fusing representations
early. Early fusion would probably be slightly stronger and would destroy the
separable content contribution that makes feature-level explanation possible.
That is exactly the design choice Objective 3 tests the cost of."
""")
    return page + 1


def s_models(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Methodology  \u00b7  \u00a73.2", "Five models, one protocol", page,
           lede="Non-personalised, content-only, classical collaborative and neural families.")

    table(s, ML, 2.10, CW,
          [["Model", "Family", "Role in the study"],
           ["Popularity", "Non-personalised", "Lower-bound reference"],
           ["Content-based (cosine)", "Content only", "The acoustic signal in isolation"],
           ["SVD-MF", "Classical collaborative", "Classical reference outside the neural "
            "family"],
           ["NCF", "Neural collaborative", "Ablation reference: the hybrid minus content"],
           ["Hybrid NCF + Content", "Neural hybrid", "Proposed model"]],
          col_w=[3.30, 3.10, 5.69], row_h=0.40, header_h=0.40, font_size=10.4,
          header_size=8.8, first_bold=True, rule_color="FFFFFF",
          row_fills={5: ACCENT_LT})

    card(s, ML, 4.72, 5.86, 1.62, title="Training", body=None, title_size=12.6, pad=0.26)
    bullets(s, ML + 0.26, 5.30, 5.40, 0.94, [
        ("Loss  ", "binary cross-entropy over implicit-feedback pairs."),
        ("Negatives  ", "4 uniform negatives per positive (false-negative rate \u2248 0.07%)."),
        ("Optimiser  ", "Adam, lr 1e-3, weight decay 1e-5, 5 epochs."),
    ], size=9.4, gap=6, bullet_color=ACCENT, glyph_size=5.2, indent=0.18)

    x2 = ML + 6.23
    card(s, x2, 4.72, 5.86, 1.62, title="Evaluation cohort", body=None, title_size=12.6,
         pad=0.26)
    text(s, x2 + 0.26, 5.30, 5.34, 0.92,
         "Scores are materialised for 1,000 users sampled from the 87,663 test users with at "
         "least one held-out interaction, against all 20,042 items. Precision, recall, NDCG "
         "and MRR at K \u2208 {5, 10, 20}. The same cohort is used by all five models.",
         size=9.4, color=BODY, line_spacing=1.18)

    notes(s, """
"Five models, one protocol.

Popularity is the floor. Content-based cosine is the acoustic signal with no
collaborative information. SVD-MF is the classical reference, added after the
proposal as a non-neural comparison.

Then NCF and the hybrid. That pairing is the ablation for Objective 1: the hybrid
is NCF plus the content branch, so the difference between those two rows is the
content contribution.

Training: binary cross-entropy, four uniform negatives per positive, Adam, five
epochs.

A fixed cohort of a thousand users, because a dense score matrix is 1.94 billion
cells, and ranking metrics only need per-user ordering.

The five epochs is the caveat, and I will come back to it in the results."
""")
    return page + 1


def s_explainers(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Methodology  \u00b7  \u00a73.3", "How SHAP and LIME are applied", page,
           lede="A deviation from the approved plan, and what it costs the explanation results.")

    boxes = [
        (ML, 1.94, "Hybrid model", "the model being explained", WHITE, LINE, None),
        (ML + 2.62, 1.94, "DeepExplainer", "intractable at this scale", WHITE, ROSE, None),
        (ML + 5.24, 1.94, "GBR surrogate", "9 features \u00b7 3,000 instances", AMBER_LT,
         AMBER_LT, AMBER),
        (ML + 7.86, 1.94, "SHAP  +  LIME", "TreeExplainer \u00b7 tabular", ACCENT_LT,
         ACCENT_LT, ACCENT),
    ]
    for (x, y, t, sub, fill, border, acc) in boxes:
        dbox(s, x, y, 2.32, 0.94, t, sub, fill=fill, border=border, title_size=10.8,
             sub_size=8.2, accent=acc)
    arrow(s, ML + 2.36, 2.41, ML + 2.58, 2.41, MUTED, 1.1)
    arrow(s, ML + 2.36 + 2.62, 2.41, ML + 2.58 + 2.62, 2.41, ROSE, 1.1)
    arrow(s, ML + 2.36 + 5.24, 2.41, ML + 2.58 + 5.24, 2.41, MUTED, 1.1)
    text(s, ML + 5.32, 2.92, 2.2, 0.24, "held-out R\u00b2 = 0.105", size=8, color=AMBER,
         bold=True, check=False)

    label(s, ML, 3.36, 5.6, "Explanation formats")
    fmts = [("Feature-ranked text", "Generated from each instance's top SHAP values.",
             ACCENT, "built"),
            ("Visual attribution", "Top-5 SHAP bar charts and the global summary.", ACCENT,
             "built"),
            ("Knowledge-graph paths", "Artist / genre / label pathways.", MUTED,
             "not attempted")]
    for i, (t, b, c, st) in enumerate(fmts):
        y = 3.62 + i * 0.80
        shape(s, ML, y, 5.86, 0.70, fill=WHITE, line=LINE, radius=0.05)
        rect(s, ML, y, 0.05, 0.70, fill=c)
        text(s, ML + 0.24, y + 0.09, 2.6, 0.24, t, size=10.2, color=INK, bold=True,
             check=False)
        text(s, ML + 0.24, y + 0.34, 3.9, 0.28, b, size=8.5, color=BODY, line_spacing=1.12)
        pill(s, ML + 4.42, y + 0.19, 1.22, 0.27, st, fg=c if c != MUTED else MUTED,
             bg=ACCENT_LT if c == ACCENT else WASH_2, size=7.6)

    x2 = ML + 6.23
    shape(s, x2, 3.36, 5.86, 2.48, fill=INK, line=None, radius=0.06)
    text(s, x2 + 0.32, 3.50, 5.2, 0.24, "Why R\u00b2 = 0.105 matters", size=9,
         color=ACCENT, bold=True, spc=120, caps=True, check=False)
    text(s, x2 + 0.32, 3.82, 5.24, 1.90,
         "The surrogate reproduces about 10% of the variance in the hybrid model's score. "
         "So the explanations describe the acoustic part of the model's decision, not the "
         "whole model. That is the main limitation of the results in the next section, and "
         "it is also one of the candidate causes of the SHAP\u2013LIME disagreement.",
         size=10.4, color=DARK_TXT, line_spacing=1.24)

    text(s, ML, 6.22, CW, 0.30,
         "Both built formats are grounded in musical features \u2014 instrumentalness, energy, "
         "danceability \u2014 rather than in embedding dimensions.",
         size=10.0, color=MUTED, italic=True, check=False)

    notes(s, """
"Here is the pathway; the second box is what did not work.

The plan was SHAP's DeepExplainer on the hybrid network; at 20,042 items that was
not tractable with the compute I had.

So I trained a gradient-boosting surrogate to reproduce the hybrid model's score
from the nine acoustic features, on 3,000 sampled test instances, and applied
SHAP's TreeExplainer and LIME's tabular explainer to that surrogate instead.

Held-out R-squared is 0.105.

It is also a result: acoustic content explains about a tenth of the variance, and
the rest is collaborative signal a content-only surrogate cannot see.

So the explanations I show next describe the acoustic part of the model's
decision. Of the three formats in the proposal, two are built; the
knowledge-graph path is not attempted."
""")
    return page + 1


def build(prs, page):
    page = s_preprocess(prs, page)
    page = s_acoustic(prs, page)
    page = s_architecture(prs, page)
    page = s_models(prs, page)
    page = s_explainers(prs, page)
    return page
