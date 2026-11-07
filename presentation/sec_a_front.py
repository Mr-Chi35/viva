"""Slides 1-5: title, aim, motivation, frameworks, research gaps."""
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

from deck_lib import *

ASSETS = "assets"
CHARTS = "charts"


def title_slide(prs):
    s = blank(prs)
    bg_gradient(s, DARK_BG, RGBColor(0x1C, 0x20, 0x4E), 35)
    rings(s, 11.9, 1.55, [3.4, 4.9, 6.4, 7.9], DARK_RING, 0.9)

    text(s, ML, 0.90, 10.0, 0.26,
         "MSc dissertation  \u00b7  viva  \u00b7  august 2026",
         size=9.4, color=TEAL, bold=True, spc=190, caps=True, check=False)
    rect(s, ML + 0.02, 1.34, 0.86, 0.05, fill=TEAL)

    text(s, ML, 1.74, 10.40, 1.15,
         "Explainable Music Recommender Systems for Improving User Satisfaction",
         size=32, color=WHITE, bold=True, line_spacing=1.08, check=False)
    text(s, ML, 2.96, 8.15, 0.80,
         "A hybrid neural recommender with post-hoc SHAP and LIME explanations, "
         "evaluated on the Spotify Million Playlist Dataset.",
         size=14, color=DARK_TXT, line_spacing=1.35)

    waveform(s, ML, 3.94, 5.6, 0.62,
             RGBColor(0x35, 0x3A, 0x7C), TEAL,
             [0.28, 0.52, 0.34, 0.78, 0.46, 0.98, 0.62, 0.4, 0.86, 0.5, 0.3, 0.7,
              0.44, 0.9, 0.36, 0.6, 0.26, 0.74, 0.42])

    hline(s, ML, 5.40, CW, RGBColor(0x2C, 0x31, 0x66), 1.0)

    metas = [("Presented by", "Chike Egonu"), ("Supervisor", "Aoife Curran"),
             ("Programme", "MSc dissertation")]
    x, widths = ML, [3.6, 3.4, 3.6]
    for (k, v), w in zip(metas, widths):
        text(s, x, 5.62, w, 0.22, k, size=8.4, color=RGBColor(0x6E, 0x74, 0x9A),
             bold=True, spc=120, caps=True, check=False)
        text(s, x, 5.88, w, 0.30, v, size=14, color=WHITE, bold=True, check=False)
        x += w

    notes(s, """
"Good morning. I'm Chike Egonu, supervised by Aoife Curran. My project is an
explainable music recommender system, evaluated on the Spotify Million Playlist
Dataset.

The short version: I built a hybrid recommender across five models, added an
explanation layer using SHAP and LIME, and evaluated both the accuracy and the
explanations themselves. Two of the results were not what the proposal expected,
and I will be explicit about what is finished and what is still provisional."
""")
    return s


def s_aim(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Aims  \u00b7  \u00a72", "One aim, three objectives", page,
           lede="Status of each objective at the time of writing.")

    shape(s, ML, 2.10, CW, 1.24, fill=ACCENT_LT, line=None, radius=0.05)
    rect(s, ML, 2.10, 0.07, 1.24, fill=ACCENT)
    text(s, ML + 0.34, 2.20, 1.6, 0.24, "AIM", size=8.8, color=ACCENT_DK, bold=True,
         spc=150, check=False)
    text(s, ML + 0.34, 2.46, CW - 0.80, 0.78,
         "Design, implement and evaluate an explainable music recommender system that "
         "balances personalisation and accuracy with transparent, user-interpretable "
         "explanations.", size=15.2, color=INK, line_spacing=1.22)

    objs = [
        ("Objective 1", "Hybrid recommender, benchmarked",
         "Develop a hybrid model combining NCF with content-based acoustic and metadata "
         "features, benchmarked against established accuracy baselines on the Spotify MPD.",
         "Implemented", TEAL, TEAL_LT, 1.62),
        ("Objective 2", "SHAP and LIME, evaluated",
         "Integrate model-agnostic post-hoc explainers and evaluate their suitability for "
         "the music domain, including agreement between them.",
         "Implemented \u00b7 surrogate", AMBER, AMBER_LT, 2.24),
        ("Objective 3", "Accuracy\u2013explainability trade-off",
         "Measure the trade-off between accuracy and explainability through ablation, "
         "quantifying the cost of a feature-decomposable architecture.",
         "First pass", AMBER, AMBER_LT, 1.30),
    ]
    for i, (num, title, body, status, col, colbg, pw) in enumerate(objs):
        x = ML + i * 4.13
        shape(s, x, 3.62, 3.83, 2.34, fill=WHITE, line=LINE, radius=0.06)
        text(s, x + 0.26, 3.76, 3.3, 0.24, num, size=8.8, color=col, bold=True,
             spc=130, caps=True, check=False)
        text(s, x + 0.26, 4.00, 3.32, 0.56, title, size=13, color=INK, bold=True,
             line_spacing=1.05)
        text(s, x + 0.26, 4.58, 3.32, 0.92, body, size=9.8, color=BODY, line_spacing=1.16)
        pill(s, x + 0.26, 5.56, pw, 0.29, status, fg=col, bg=colbg, size=7.8)
        x += 0

    text(s, ML, 6.14, CW, 0.44,
         "Objective 3 is a first pass because the trade-off cannot be settled while the "
         "neural models are under-trained (Section 4.5 of the report).",
         size=10.2, color=MUTED, italic=True, line_spacing=1.15)

    notes(s, """
"The aim is on the slide: an explainable recommender that balances accuracy with
explanations a listener can use.

Three objectives. One, the hybrid model and the baselines: implemented. Two,
SHAP and LIME: implemented, but through a surrogate, and I will explain why in
the methodology. Three, the accuracy-explainability trade-off: a first pass only,
because the neural models are under-trained, and that is the same issue that
affects the model comparison later."
""")
    return page + 1


def s_motivation(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Background  \u00b7  \u00a71.1", "Why explanation matters in music recommendation", page,
           lede="The recommender is the interface to the catalogue, and the feedback it "
                "learns from is ambiguous.")

    label(s, ML, 2.18, 5.9, "Three reasons")
    bullets(s, ML, 2.46, 5.95, 3.30, [
        ("Catalogue scale. ", "Streaming catalogues run to tens of millions of tracks, so "
         "the recommender is the only practical way to navigate them "
         "(Schedl et al., 2018)."),
        ("User expectation. ", "Users now expect to know why an item was recommended, and "
         "transparency affects trust in the system (Zhang and Chen, 2020; "
         "Afchar et al., 2022)."),
        ("Music is different. ", "Preferences are contextual and emotional, and the "
         "feedback is implicit \u2014 a skip may be a mismatch of context rather than "
         "dislike (Ferwerda et al., 2015; Schedl et al., 2018)."),
    ], size=11.6, gap=22, tag="motiv")

    x2 = 6.85
    label(s, x2, 2.18, 5.8, "What the feedback actually means")
    table(s, x2, 2.46, 5.86,
          [["Observed signal", "What it may actually mean"],
           ["Skip", "Dislike \u00b7 wrong context \u00b7 wrong moment"],
           ["Full play", "Preference \u00b7 passive background listening"],
           ["Playlist co-occurrence", "Shared taste \u00b7 one curator's taste"]],
          col_w=[1.94, 3.92], row_h=0.48, header_h=0.34, font_size=9.6, header_size=8.6,
          first_bold=True, rule_color="FFFFFF")

    label(s, x2, 4.72, 5.8, "Where this differs from film and e-commerce")
    bullets(s, x2, 5.00, 5.86, 1.50, [
        ("Acoustic features. ", "Explanations have to be expressed in musical terms, not "
         "product metadata."),
        ("Popularity bias. ", "Mainstream artists are over-exposed and the long tail is "
         "under-recommended (Celma, 2010)."),
    ], size=10.1, gap=10, tag="differs")

    notes(s, """
"Three reasons explanation matters here.

Catalogue scale: at tens of millions of tracks the recommender is the only
navigation layer.

User expectation: users ask why something was recommended, and the literature in
e-commerce and film shows transparency affects trust.

And music is different. Preferences are contextual, and the feedback is implicit:
a skip can mean dislike or wrong context, a full play can mean preference or
passive listening.

The same ambiguity affects explanation too: if the signal is unclear, the
explanation has to help resolve it, which is why these explanations are in
musical terms rather than model internals."
""")
    return page + 1


def s_frameworks(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Background  \u00b7  \u00a71.3", "Explaining recommendations: intrinsic and post-hoc", page,
           lede="Two families of method, and a definition of explanation quality that is "
                "deliberately multi-dimensional.")

    shape(s, ML, 2.12, 5.86, 2.55, fill=WHITE, line=LINE, radius=0.06)
    rect(s, ML, 2.12, 0.055, 2.55, fill=MUTED)
    text(s, ML + 0.30, 2.28, 5.2, 0.26, "Intrinsic \u2014 interpretable by design",
         size=13.4, color=INK, bold=True, check=False)
    text(s, ML + 0.30, 2.62, 5.25, 1.30,
         "Decision trees, linear models, rule lists. Faithful by construction, but rarely "
         "competitive with deep recommenders on accuracy, which is why the field moved away "
         "from them (Lipton, 2018; Arrieta et al., 2020).",
         size=11, color=BODY, line_spacing=1.22)
    text(s, ML + 0.30, 3.96, 5.25, 0.52,
         "So intrinsic interpretability is a constraint on the architecture here, not a "
         "candidate solution.", size=9.8, color=MUTED, italic=True, line_spacing=1.18)

    x2 = ML + 6.23
    shape(s, x2, 2.12, 5.86, 2.55, fill=WHITE, line=ACCENT, line_w=1.4, radius=0.06)
    rect(s, x2, 2.12, 0.055, 2.55, fill=ACCENT)
    text(s, x2 + 0.30, 2.28, 5.2, 0.26, "Post-hoc \u2014 after the fact",
         size=13.4, color=INK, bold=True, check=False)
    bullets(s, x2 + 0.30, 2.64, 5.28, 1.86, [
        ("LIME  ", "a locally faithful linear surrogate around one prediction "
                   "(Ribeiro et al., 2016)."),
        ("SHAP  ", "Shapley values from cooperative game theory; local accuracy, "
                   "missingness and consistency (Lundberg and Lee, 2017)."),
        ("Attention  ", "has been used as an explanation, but is not reliably faithful "
                        "(Jain and Wallace, 2019)."),
    ], size=10.4, gap=8, bullet_color=ACCENT, glyph_size=5.4, indent=0.18)

    shape(s, ML, 4.94, CW, 1.42, fill=WASH, line=None, radius=0.05)
    rect(s, ML, 4.94, 0.06, 1.42, fill=TEAL)
    text(s, ML + 0.32, 5.04, 4.2, 0.24, "Explanation quality", size=8.8, color=TEAL,
         bold=True, spc=110, caps=True, check=False)
    text(s, ML + 0.32, 5.34, CW - 0.66, 0.92,
         "Explanation quality is multi-dimensional: transparency, scrutability, "
         "trustworthiness, effectiveness, persuasiveness, efficiency and satisfaction "
         "(Tintarev and Masthoff, 2007; 2015). No single format satisfies all of them, so "
         "two are evaluated here rather than one.", size=10.6, color=BODY, line_spacing=1.22)

    notes(s, """
"Two families.

Intrinsic methods are interpretable by construction, but you pay for that in
accuracy, and at catalogue scale that price is not payable.

Post-hoc methods explain after training. LIME fits a small linear model around a
single prediction. SHAP comes from cooperative game theory and satisfies local
accuracy, missingness and consistency, which is why it is the main method here.
Attention has been tried; Jain and Wallace showed it is not reliable.

The bottom block is the definition of quality I am working to: Tintarev and
Masthoff's dimensions, extended by Afchar and colleagues. No one style covers all
of them, so I evaluate two formats."
""")
    return page + 1


def s_gaps(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Background  \u00b7  \u00a71.5", "Four gaps in the literature", page,
           lede="Each gap drove a decision in the design.")

    gaps = [
        ("Empirical scarcity", "There is conceptual work on explainability in music "
         "recommendation, but empirical studies lag behind e-commerce and film, domains "
         "with a different feature space (Afchar et al., 2022; Schedl et al., 2018)."),
        ("SHAP and hybrid models", "SHAP is well established for tabular and image data. "
         "Attributing a recommendation jointly to latent collaborative embeddings and "
         "explicit acoustic features is largely unexplored."),
        ("Thin user evidence", "Existing explanation studies use small samples and a single "
         "explanation style, which limits what can be generalised "
         "(Knijnenburg et al., 2012; Tintarev and Masthoff, 2007)."),
        ("No music-specific metrics", "Explanation quality lacks domain metrics and is "
         "often conflated with accuracy, although the two are largely orthogonal "
         "(Afchar et al., 2022)."),
    ]
    pos = [(ML, 2.14), (ML + 6.23, 2.14), (ML, 4.16), (ML + 6.23, 4.16)]
    for i, ((t, b), (x, y)) in enumerate(zip(gaps, pos)):
        card(s, x, y, 5.86, 1.94, num=i + 1, title=t, body=b, title_size=13.6,
             body_size=10.2, accent=ACCENT, pad=0.24)

    text(s, ML, 6.32, CW, 0.44,
         "Gaps 1 and 4 set the evaluation design; gap 2 set the architecture and the "
         "explainer; gap 3 is what the planned user study addresses.",
         size=9.8, color=MUTED, italic=True, line_spacing=1.15)

    notes(s, """
"Four gaps.

One: the empirical base in music is thin compared with e-commerce and film, and
the feature space is not transferable.

Two, and this is the one closest to my contribution: SHAP is well understood for
tabular models, but attributing a recommendation jointly across latent
collaborative factors and acoustic features has not been done much in music.

Three: user studies are small and usually test one explanation style.

Four: there are no music-specific explanation metrics, and accuracy keeps getting
conflated with explanation quality."
""")
    return page + 1


def build(prs, page):
    title_slide(prs)
    page = s_aim(prs, page)
    page = s_motivation(prs, page)
    page = s_frameworks(prs, page)
    page = s_gaps(prs, page)
    return page
