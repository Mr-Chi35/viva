"""Title, roadmap, section 01 (background & literature)."""
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

from deck_lib import *

ASSETS = "assets"
CHARTS = "charts"


def title_slide(prs):
    s = blank(prs)
    bg_gradient(s, DARK_BG, RGBColor(0x1C, 0x20, 0x4E), 35)
    rings(s, 11.9, 1.55, [3.4, 4.9, 6.4, 7.9], DARK_RING, 0.9)

    text(s, ML, 0.86, 10.0, 0.26,
         "MSc dissertation  \u00b7  scientific report defence  \u00b7  august 2026",
         size=9.4, color=TEAL, bold=True, spc=190, caps=True, check=False)
    rect(s, ML + 0.02, 1.30, 0.86, 0.05, fill=TEAL)

    text(s, ML, 1.66, 10.40, 1.15,
         "Explainable Music Recommender Systems for Improving User Satisfaction",
         size=32, color=WHITE, bold=True, line_spacing=1.08, check=False)
    text(s, ML, 2.88, 8.15, 0.80,
         "A hybrid neural recommender with post-hoc SHAP and LIME explanations, "
         "benchmarked on the Spotify Million Playlist Dataset.",
         size=14, color=DARK_TXT, line_spacing=1.35)

    waveform(s, ML, 3.86, 5.6, 0.62,
             RGBColor(0x35, 0x3A, 0x7C), TEAL,
             [0.28, 0.52, 0.34, 0.78, 0.46, 0.98, 0.62, 0.4, 0.86, 0.5, 0.3, 0.7,
              0.44, 0.9, 0.36, 0.6, 0.26, 0.74, 0.42])

    hline(s, ML, 5.32, CW, RGBColor(0x2C, 0x31, 0x66), 1.0)

    metas = [("Presented by", "Chike Egonu"), ("Supervisor", "Aoife Curran"),
             ("Report", "3,300 words \u00b7 20 pages"), ("Study scale", "1.93M interactions")]
    x = ML
    widths = [2.9, 2.7, 3.1, 2.9]
    for (k, v), w in zip(metas, widths):
        text(s, x, 5.52, w, 0.22, k, size=8.4, color=RGBColor(0x6E, 0x74, 0x9A),
             bold=True, spc=120, caps=True, check=False)
        text(s, x, 5.78, w, 0.30, v, size=13.5, color=WHITE, bold=True, check=False)
        x += w

    chip_flow(s, ML, 6.38, 11.0,
              ["5 models benchmarked", "3 research objectives", "SHAP + LIME",
               "1,000-user evaluation cohort"],
              h=0.30, size=8.2, fg=RGBColor(0xC7, 0xCB, 0xE4),
              bg=RGBColor(0x21, 0x25, 0x52))

    notes(s, """
TIMING: 45 s. Do not read the title aloud.

"Good morning. I'm Chike Egonu, supervised by Aoife Curran. This is my progress
defence for 'Explainable Music Recommender Systems for Improving User
Satisfaction'.

The short version of the story: I have built a hybrid music recommender across
five models, wired an explanation layer on top of it with SHAP and LIME, and I
have preliminary results. Two of those results were not what the proposal
predicted, and one of them I think is the most interesting thing in the project
so far. I want to be direct about what is finished, what is provisional, and
what changes in the next iteration."

Set expectations: content is ~19 minutes, then questions.
""")
    return s


def roadmap(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Presentation roadmap", "Six parts, mapped to the report's sections", page,
           lede="About 19 minutes of content, then questions. Report sections are shown "
                "on each card so you can cross-reference as we go.")

    items = [
        ("01", "Background & Literature", "\u00a71  \u2192  \u00a71.1 \u2013 1.5",
         "Why explanation became a design requirement in music, and where the literature stops.", "3 min"),
        ("02", "Aims & Objectives", "\u00a72",
         "One aim, three objectives, and their status as of this submission.", "1.5 min"),
        ("03", "Methodology", "\u00a73  \u2192  \u00a73.1 \u2013 3.4",
         "Data, five models, two explainers, and the evaluation protocol.", "4 min"),
        ("04", "Preliminary Results", "\u00a74  \u2192  \u00a74.1 \u2013 4.4",
         "Accuracy, global and instance-level attributions, and the SHAP\u2013LIME surprise.", "5 min"),
        ("05", "Discussion", "\u00a75 \u2013 \u00a77",
         "What holds, what is provisional, and what changes in the next iteration.", "3 min"),
        ("06", "Outcomes & Next Steps", "\u00a76 \u2013 \u00a78",
         "Anticipated outcomes, dissertation plan, contributions.", "2.5 min"),
    ]
    x1, x2 = ML, ML + 6.16
    ys = [2.12, 3.62, 5.12]
    for i, (num, title, ref, sub, t) in enumerate(items):
        x = x1 if i % 2 == 0 else x2
        y = ys[i // 2]
        shape(s, x, y, 5.93, 1.36, fill=WHITE, line=LINE, radius=0.07)
        shape(s, x + 0.26, y + 0.30, 0.40, 0.40, fill=ACCENT, line=None, radius=0.5,
              kind=MSO_SHAPE.OVAL)
        text(s, x + 0.26, y + 0.36, 0.40, 0.28, num, size=10.4, color=WHITE, bold=True,
             align=PP_ALIGN.CENTER, check=False)
        text(s, x + 0.84, y + 0.22, 3.9, 0.22, ref, size=8.4, color=ACCENT,
             bold=True, spc=90, check=False)
        text(s, x + 0.84, y + 0.44, 4.10, 0.30, title, size=13.6, color=INK, bold=True,
             check=False)
        text(s, x + 0.84, y + 0.78, 4.55, 0.50, sub, size=10.3, color=BODY,
             line_spacing=1.16, check=False)
        text(s, x + 5.93 - 0.86, y + 0.22, 0.66, 0.22, t, size=9.2, color=MUTED,
             align=PP_ALIGN.RIGHT, bold=True, check=False)
    notes(s, """
TIMING: 30 s. Signpost only.

"Six parts. I'll spend the most time on methodology and results, because that is
where the marks are, and because two of the results need careful reading.

If you want to jump: section four is where the interesting finding is."
""")
    return page + 1


def s_importance(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Background  \u00b7  \u00a71.1", "Why explanation is now a design requirement", page,
           lede="Three forces have moved explanation from a nice-to-have to something a "
                "recommender is judged on.")

    cards = [
        ("Scale", "Catalogues now run to tens of millions of tracks. The recommender is the "
                  "only practical navigation layer between a listener and the catalogue "
                  "(Schedl et al., 2018).", ACCENT),
        ("Demand", "Awareness of algorithmic transparency has grown, and users now expect "
                   "to understand why an item was put in front of them "
                   "(Zhang and Chen, 2020).", TEAL),
        ("Retention", "Accuracy drives immediate satisfaction, but trust and forgiveness \u2014 "
                      "what keeps a user on a platform \u2014 are built by explanation "
                      "(Afchar et al., 2022).", AMBER),
    ]
    for i, (t, b, c) in enumerate(cards):
        card(s, ML + i * 4.13, 2.28, 3.83, 2.18, title=t, body=b, accent=c,
             title_size=15, body_size=11.6, top_bar=True)

    label(s, ML, 4.70, 6.0, "What explanation buys, in the literature")
    chip_flow(s, ML, 4.98, CW,
              ["Trust", "Forgiveness after a bad recommendation", "Perceived transparency",
               "Willingness to act on a suggestion", "Scrutability of preferences",
               "Fairer exposure for long-tail artists"])

    statement(s, ML, 5.92, CW, 0.82,
              "Explanation is not a cosmetic layer on top of the recommender. It is the "
              "mechanism through which a platform earns continued use \u2014 and in music, "
              "where switching cost is close to zero, that is what compounds.",
              size=13.2, accent=ACCENT)

    notes(s, """
TIMING: 60 s.

"Three reasons explanation has become first-order.

Scale: we are past the point where a user can browse a catalogue. Tens of
millions of tracks means the recommender is the interface.

Demand: users have become aware that these systems are algorithmic, and the
question 'why this track?' is now a reasonable user expectation rather than a
research curiosity (Zhang and Chen, 2020).

Retention, and this is the commercial argument: accuracy buys the immediate
click, but trust and forgiveness buy the relationship (Afchar et al., 2022). A
user who understands a bad recommendation forgives it; a user who does not,
leaves.

The point I want to land: explanation is load-bearing, not decoration."
""")
    return page + 1


def s_domain(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Background  \u00b7  \u00a71.1", "Music makes both problems harder", page,
           lede="The domain differs from film and e-commerce in ways that affect "
                "recommendation and explanation equally.")

    bullets(s, ML, 2.24, 6.15, 4.2, [
        ("Context, not just taste. ",
         "Mood, activity, time of day and social setting each change what a listener "
         "wants to hear (Schedl et al., 2018; Ferwerda et al., 2015)."),
        ("Implicit and ambiguous feedback. ",
         "Signals come from skips, likes and playlist co-occurrence. A skip may be a "
         "contextual mismatch rather than dislike; a full play may be passive."),
        ("Structural popularity bias. ",
         "Mainstream artists receive disproportionate exposure while long-tail artists "
         "are systematically under-recommended (Celma, 2010)."),
        ("A different feature space. ",
         "Acoustic and emotional attributes rather than text or product metadata \u2014 so "
         "explanations have to be expressed in musical terms, not abstract weights."),
    ], size=12.4, gap=13, tag="domain")

    card(s, 7.05, 2.24, 5.66, 1.36,
         body="If the listener cannot say why they skipped, and the system cannot say why it "
              "recommended, there is no common language for the loop. Explanation is that "
              "missing interface.",
         accent=ACCENT, fill=ACCENT_LT, border=ACCENT_LT, body_size=12.4, pad=0.30,
         title_size=13)

    label(s, 7.05, 3.80, 5.6, "One signal, several possible meanings")
    table(s, 7.05, 4.08, 5.66,
          [["Observed signal", "What it may actually mean"],
           ["Skip", "Dislike \u00b7 wrong context \u00b7 wrong moment"],
           ["Full play", "Preference \u00b7 passive background listening"],
           ["Playlist co-occurrence", "Shared taste \u00b7 one curator's own taste"]],
          col_w=[1.86, 3.80], row_h=0.50, header_h=0.34, font_size=9.6, header_size=8.6,
          first_bold=True, rule_color="FFFFFF")

    text(s, 7.05, 5.95, 5.66, 0.6,
         "Every ambiguity here is a modelling problem and an explanation problem at the "
         "same time.", size=10.4, color=MUTED, italic=True, line_spacing=1.2)

    notes(s, """
TIMING: 75 s.

"Music is not just another recommendation domain, and I want to be precise about
why.

First, listening is contextual. Mood, activity, time of day, who you are with:
all of it modulates what a user wants. A recommender that models stable taste
misses most of what drives a session.

Second, the feedback is implicit and ambiguous. This is the crux. A skip can
mean 'I dislike this' or 'not now'. A full play can mean 'I love this' or 'my
hands were busy'. There is no explicit rating to anchor the model.

Third, popularity bias is structural, not incidental: mainstream artists get
disproportionate exposure, and the long tail is under-served (Celma, 2010).

Fourth, the feature space is acoustic and emotional, not text.

Now put the explanation hat on. Each of those ambiguities is also an
explanation problem: if the signal is ambiguous, the 'why' has to help resolve
the ambiguity. That is why I argue explanations should be grounded in musical
concepts a listener already has \u2014 genre, mood, energy, acoustic similarity."
""")
    return page + 1


def s_architectures(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Background  \u00b7  \u00a71.2", "Every step up in accuracy has cost interpretability", page,
           lede="Four generations of recommender architecture, each more accurate and less "
                "inspectable than the last.")

    stages = [
        ("2009", "Matrix factorisation", "Low-rank latent factors over the user\u2013item "
         "matrix. Strong on implicit feedback (Koren et al., 2009).",
         "Latent factors only \u2014 no feature-level story."),
        ("2017", "Neural collaborative filtering", "Replaces the inner product with a "
         "multi-layer perceptron; statistically significant gains (He et al., 2017).",
         "Non-linear, entangled representations."),
        ("2019", "Knowledge-graph CF", "KGCN propagates preferences through artist, genre "
         "and sonic relations (Wang et al., 2019).",
         "Paths are traceable \u2014 a partial escape route."),
        ("2024", "Deep sequential", "LSTM, CNN-LSTM, attention and transformer recommenders "
         "over listening sequences.", "Attention weights are not faithful explanations."),
    ]
    for i, (yr, name, desc, note) in enumerate(stages):
        x = ML + i * 3.06
        shape(s, x, 2.58, 2.86, 2.12, fill=WHITE, line=LINE, radius=0.06)
        text(s, x + 0.22, 2.72, 1.0, 0.24, yr, size=9.4, color=ACCENT, bold=True, spc=90,
             check=False)
        text(s, x + 0.22, 2.99, 2.46, 0.52, name, size=12.8, color=INK, bold=True,
             line_spacing=1.05)
        text(s, x + 0.22, 3.54, 2.46, 0.72, desc, size=9.3, color=BODY, line_spacing=1.12)
        hline(s, x + 0.22, 4.28, 2.42, LINE, 0.75)
        text(s, x + 0.22, 4.31, 2.46, 0.32, note, size=8.5, color=AMBER, line_spacing=1.10)

    # directional guides
    arrow(s, ML + 0.05, 2.34, ML + CW - 0.05, 2.34, TEAL, 1.2)
    text(s, ML + 0.05, 2.06, 3.2, 0.24, "recommendation performance", size=8.4, color=TEAL,
         bold=True, spc=100, caps=True, check=False)
    arrow(s, ML + CW - 0.05, 5.02, ML + 0.05, 5.02, ROSE, 1.2)
    text(s, ML + CW - 3.3, 4.72, 3.3, 0.24, "explainability", size=8.4, color=ROSE,
         bold=True, spc=100, caps=True, align=PP_ALIGN.RIGHT, check=False)

    statement(s, ML, 5.50, CW, 0.92,
              "Complexity is a prerequisite for competitive accuracy, and the price is that a "
              "single recommendation can no longer be attributed by inspection "
              "(Shashaani, 2024). Explainability stops being desirable and becomes structural.",
              size=13, accent=ROSE)

    notes(s, """
TIMING: 70 s.

"Four generations, and the same trade repeating.

Matrix factorisation in 2009 gave us latent factors. Excellent on implicit
feedback, but a recommendation is a dot product of two opaque vectors.

NCF in 2017 replaced the inner product with an MLP. Real accuracy gains, and the
representations become non-linear and entangled \u2014 two features no longer mean
two features.

Knowledge-graph convolution in 2019 is interesting because it partially buys
traceability back: a recommendation can be traced along artist, genre and sonic
relations. That is why I kept it as a planned extension rather than abandoning
it.

And the current wave \u2014 sequential models, attention, transformers \u2014 is the
least inspectable of the four. It is worth saying out loud: attention weights
look like explanations and are not; Jain and Wallace showed that convincingly in
2019.

So: the more competitive the architecture, the more the explanation has to be
bolted on afterwards."
""")
    return page + 1


def s_frameworks(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Background  \u00b7  \u00a71.3", "What can be explained, and with what", page,
           lede="Two families of method, and a definition of 'good explanation' that is "
                "deliberately multi-dimensional.")

    # intrinsic
    shape(s, ML, 2.20, 5.86, 2.30, fill=WHITE, line=LINE, radius=0.06)
    rect(s, ML, 2.20, 0.055, 2.30, fill=MUTED)
    text(s, ML + 0.30, 2.36, 5.2, 0.26, "Intrinsic \u2014 interpretable by design",
         size=13.4, color=INK, bold=True, check=False)
    text(s, ML + 0.30, 2.70, 5.25, 1.10,
         "Decision trees, linear models, rule lists. Faithful by construction, but rarely "
         "competitive with deep recommenders on accuracy \u2014 which is why the field moved "
         "away from them (Lipton, 2018; Arrieta et al., 2020).",
         size=11, color=BODY, line_spacing=1.22)
    text(s, ML + 0.30, 3.88, 5.25, 0.54,
         "So intrinsic interpretability becomes a constraint on the architecture here, not a "
         "candidate solution.", size=10, color=MUTED, italic=True, line_spacing=1.2)

    # post-hoc
    x2 = ML + 6.23
    shape(s, x2, 2.20, 5.86, 2.30, fill=WHITE, line=ACCENT, line_w=1.4, radius=0.06)
    rect(s, x2, 2.20, 0.055, 2.30, fill=ACCENT)
    text(s, x2 + 0.30, 2.36, 5.2, 0.26, "Post-hoc \u2014 after the fact",
         size=13.4, color=INK, bold=True, check=False)
    bullets(s, x2 + 0.30, 2.70, 5.28, 1.66, [
        ("LIME  ", "locally faithful linear surrogate around one prediction "
                   "(Ribeiro et al., 2016)."),
        ("SHAP  ", "Shapley values from cooperative game theory; local accuracy, "
                   "missingness, consistency (Lundberg and Lee, 2017)."),
        ("Attention  ", "explored, but not reliably faithful (Jain and Wallace, 2019)."),
    ], size=10.4, gap=5, bullet_color=ACCENT, glyph_size=5.4, indent=0.18)

    label(s, ML, 4.68, 8.0, "Explanation quality \u2014 seven dimensions, extended to eleven")
    chip_flow(s, ML, 4.94, CW,
              ["Transparency", "Scrutability", "Trustworthiness", "Effectiveness",
               "Persuasiveness", "Efficiency", "Satisfaction", "Informativeness",
               "Fairness", "Causality", "Interactivity"], h=0.32, size=8.8)

    text(s, ML, 5.74, 7.6, 0.22,
         "First seven: Tintarev and Masthoff (2007, 2015).  Further four: Afchar et al. (2022).",
         size=8.6, color=MUTED, check=False)

    statement(s, ML, 5.98, CW, 0.78,
              "No single explanation style dominates across those dimensions \u2014 which is "
              "precisely why this project evaluates more than one format, rather than "
              "declaring SHAP the winner in advance.",
              size=12.6, accent=TEAL)

    notes(s, """
TIMING: 80 s.

"Two families.

Intrinsic methods are interpretable by construction: a decision tree is its own
explanation. Faithful, but you pay for it in accuracy, and at catalogue scale
that price is not payable.

Post-hoc methods explain after training. LIME fits a small linear surrogate
around one prediction \u2014 local and cheap, but unstable. SHAP comes from
cooperative game theory and has three properties I care about: local accuracy,
missingness and consistency. Those properties are why it is the primary method
here rather than LIME. Attention as explanation \u2014 no, and Jain and Wallace made
that case.

The second half of this slide matters for how I evaluate. Tintarev and Masthoff
defined seven dimensions of explanation quality; Afchar and colleagues extended
it to eleven for recommender systems. The key empirical claim in that literature
is that these goals are correlated but not redundant \u2014 no single style
dominates.

So a project that only tested SHAP could only speak to a subset of those
dimensions. That is why the design has two explanation formats and a
multi-metric evaluation."
""")
    return page + 1


def s_gaps(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Background  \u00b7  \u00a71.5", "From the literature to four gaps", page,
           lede="Four specific absences in the literature, each of which maps onto a "
                "design decision in this project.")

    gaps = [
        ("Empirical scarcity", "Conceptual treatments of explainability in music "
         "recommendation exist, but empirical studies lag far behind e-commerce and film \u2014 "
         "domains with a qualitatively different feature space (Afchar et al., 2022; "
         "Schedl et al., 2018).", "gap 1"),
        ("SHAP meets the hybrid", "SHAP is mature for tabular and image data. Joint "
         "attribution of a recommendation to latent collaborative embeddings and explicit "
         "acoustic features at the same time is largely unexplored.", "gap 2"),
        ("Thin user evidence", "Existing explanation studies use small samples and a single "
         "explanation style, which limits generalisability (Knijnenburg et al., 2012; "
         "Tintarev and Masthoff, 2007).", "gap 3"),
        ("No music-specific metrics", "Explanation quality lacks domain metrics and is "
         "routinely conflated with accuracy, even though the two are largely orthogonal "
         "(Afchar et al., 2022).", "gap 4"),
    ]
    pos = [(ML, 2.18), (ML + 6.23, 2.18), (ML, 4.24), (ML + 6.23, 4.24)]
    for i, ((t, b, tag), (x, y)) in enumerate(zip(gaps, pos)):
        card(s, x, y, 5.86, 1.98, num=i + 1, title=t, body=b, title_size=13.6,
             body_size=10.2, accent=ACCENT, pad=0.24)

    pill(s, ML, 6.32, 3.06, 0.34, "this project is designed against all four",
         fg=WHITE, bg=ACCENT, size=8.4)
    text(s, ML + 3.24, 6.36, 8.6, 0.28,
         "Gaps 1 and 4 set the evaluation design; gap 2 sets the architecture and explainer; "
         "gap 3 is what the planned user study addresses.", size=9.6, color=MUTED,
         check=False)

    notes(s, """
TIMING: 70 s.

"Four gaps, and I want to be explicit that each one drove a decision.

One: empirical scarcity. There is good conceptual work \u2014 Afchar and colleagues is
the anchor \u2014 but the empirical base in music is thin compared with e-commerce
and film, and the feature space is not transferable.

Two, and this is the one closest to my contribution: SHAP is well understood for
tabular and image models. What has not been done much is attributing a
recommendation jointly across latent collaborative factors and explicit acoustic
features. That is what a hybrid model forces you to confront, and it is
under-explored.

Three: the user evidence is thin \u2014 small samples, one explanation style.

Four: there are no music-specific explanation metrics, and accuracy keeps getting
conflated with explanation quality even though they are close to orthogonal.

One and four set the evaluation design. Two sets the architecture. Three is the
user study."
""")
    return page + 1


def build(prs, page):
    title_slide(prs)
    page = roadmap(prs, page)
    divider(prs, "01", "Background & Literature Review",
            "Why explanation became a requirement, what the architectures cost, and the "
            "four gaps this project is built against.",
            ["The explainability imperative", "Recommender architectures",
             "XAI and explanation frameworks", "Trust, transparency and fairness",
             "Four identified research gaps"], page)
    page += 1
    page = s_importance(prs, page)
    page = s_domain(prs, page)
    page = s_architectures(prs, page)
    page = s_frameworks(prs, page)
    page = s_gaps(prs, page)
    return page
