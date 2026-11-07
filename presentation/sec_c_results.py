"""Slides 11-19: results, validity, outcomes, plan, summary, closing."""
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

from deck_lib import *

ASSETS = "assets"
CHARTS = "charts"


def s_accuracy(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Results  \u00b7  \u00a74.2", "Offline accuracy at K = 10", page,
           lede="Five models, one fixed cohort of 1,000 users, identical protocol.")

    picture(s, f"{CHARTS}/accuracy_k10.png", ML, 2.04, w=8.30, frame=False)
    text(s, ML, 6.02, 8.2, 0.62,
         "Re-plotted from Table 2 of the report. Absolute values are small because the "
         "matrix is 99.93% sparse; the comparison between models is what matters.",
         size=8.6, color=MUTED, line_spacing=1.15)

    x2 = 9.32
    label(s, x2, 2.04, 3.4, "Hybrid vs NCF")
    table(s, x2, 2.32, 3.39,
          [["Metric", "NCF", "Hybrid", "\u0394"],
           ["P@10", "0.0173", "0.0184", "+6.4%"],
           ["R@10", "0.0453", "0.0538", "+18.8%"],
           ["NDCG@10", "0.0342", "0.0384", "+12.3%"],
           ["MRR", "0.0736", "0.0752", "+2.2%"]],
          col_w=[1.02, 0.72, 0.80, 0.85], row_h=0.36, header_h=0.34, font_size=9.4,
          header_size=8.4, aligns=["l", "r", "r", "r"], rule_color="FFFFFF")

    text(s, x2, 4.36, 3.39, 0.28, "SVD-MF leads every metric", size=9.4, color=INK,
         bold=True, check=False)
    text(s, x2, 4.68, 3.39, 0.34, "NDCG@10 0.0769 \u2014 about twice the hybrid model.",
         size=9.2, color=BODY, line_spacing=1.16)
    text(s, x2, 5.06, 3.39, 0.28, "Two baselines are near the floor", size=9.4, color=INK,
         bold=True, check=False)
    text(s, x2, 5.34, 3.39, 0.52, "Content-only reaches NDCG@10 of 0.0027.", size=9.2,
         color=BODY, line_spacing=1.16)

    notes(s, """
"All five models on one cohort. Reading within each group of bars.

The ranking is the same on all four metrics: SVD-MF first, then the hybrid, then
NCF, then popularity, then content-only. The same order on all four metrics is
not an artefact of one measure.

The right-hand table isolates the comparison the first objective needs: the
hybrid against NCF, where the content branch is the only difference. It is better
on all four metrics, and NDCG at ten improves by 12.3%.

The levels are small because the matrix is 99.93% sparse; precision in the
hundredths is normal offline. The ordering is what the objectives rest on."
""")
    return page + 1


def s_svd(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Results  \u00b7  \u00a74.2", "SVD-MF was the strongest model", page,
           lede="This was not expected: the classical baseline outperforms both neural models.")

    picture(s, f"{CHARTS}/svd_gap.png", ML, 2.16, w=6.05, frame=False)
    text(s, ML, 4.66, 6.0, 0.20, "Derived from Table 2 of the report.", size=8.6,
         color=MUTED, check=False)

    bullets(s, 6.95, 2.16, 5.72, 2.24, [
        ("The gap is large. ", "NDCG@10 0.0769 against 0.0384 for the hybrid, and the same "
         "pattern holds on precision, recall and MRR."),
        ("The likely cause is the schedule. ", "Five epochs for the neural models, against a "
         "closed-form solution for SVD-MF."),
        ("The loss curves support that. ", "Neither neural model has plateaued at epoch 5, "
         "so the comparison is not between trained equals."),
    ], size=10.4, gap=10, tag="svd")

    label(s, ML, 4.94, 4.6, "Training loss \u00b7 NCF vs hybrid \u00b7 five epochs")
    picture(s, f"{ASSETS}/fig4_loss_curves.png", ML, 5.18, w=3.34, frame=True, caption=None)

    x3 = 6.95
    shape(s, x3, 4.28, 5.72, 1.92, fill=AMBER_LT, line=None, radius=0.06)
    rect(s, x3, 4.28, 0.06, 1.92, fill=AMBER)
    text(s, x3 + 0.32, 4.42, 5.1, 0.24, "Next run", size=9, color=AMBER, bold=True,
         spc=120, caps=True, check=False)
    text(s, x3 + 0.32, 4.72, 5.10, 1.36,
         "Train the neural models to convergence and re-run all five before drawing "
         "conclusions about model choice. If the gap closes, this result is a training "
         "artefact; if it does not, it changes what I can claim about the architecture. "
         "Either outcome is reportable, but only after the rerun.",
         size=10.2, color=BODY, line_spacing=1.22)

    notes(s, """
"Here is the result the proposal did not predict.

SVD matrix factorisation, which the proposal treated as an inferior baseline, is
the strongest model on this cohort: NDCG at ten of 0.0769 against 0.0384.

I want to be careful, because the explanation is probably not that neural
collaborative filtering is worse than matrix factorisation. These two neural
models were trained for five epochs and neither loss curve has plateaued. SVD-MF
is closed-form, so it is converged by construction.

So the comparison is not between trained equals, and I am treating it as
provisional rather than as a finding about architecture. What it does not affect
is the hybrid against NCF, because both were trained identically."
""")
    return page + 1


def s_attributions(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Results  \u00b7  \u00a74.3", "What the explanations say", page,
           lede="Global importance on the left; one recommendation explained by both methods "
                "on the right.")

    picture(s, f"{CHARTS}/shap_importance.png", ML, 2.20, w=4.55, frame=False)
    text(s, ML, 4.44, 4.55, 0.40, "Figure 5 \u00b7 global importance ranking, "
         "surrogate model.", size=8.4, color=MUTED, line_spacing=1.12)

    picture(s, f"{ASSETS}/fig6_pair_crop.png", 5.82, 2.20, w=6.85, frame=True)
    text(s, 5.82, 4.24, 6.85, 0.40, "Figure 6 \u00b7 the same instance attributed by both "
         "methods. The top-ranked features do not overlap.", size=8.4, color=MUTED,
         line_spacing=1.12)

    shape(s, ML, 4.92, CW, 1.34, fill=WASH, line=None, radius=0.05)
    rect(s, ML, 4.92, 0.06, 1.34, fill=ACCENT)
    text(s, ML + 0.30, 5.04, CW - 0.60, 0.50,
         "Instrumentalness is the largest driver globally (0.0405), followed by energy and "
         "danceability. At instance level, SHAP's top driver is instrumentalness (+0.032); "
         "LIME's is a binned rule on instrumentalness with the opposite sign (\u22120.055), "
         "and ranks two and three do not overlap.", size=9.6, color=INK, line_spacing=1.18)
    text(s, ML + 0.30, 5.58, CW - 0.60, 0.58,
         "The generated text explanation uses the top three SHAP values: \u201crecommended "
         "primarily because of its high instrumentalness, alongside danceability (+0.026) and "
         "energy (+0.015).\u201d", size=9.2, color=MUTED, italic=True, line_spacing=1.16)

    notes(s, """
"Two views of the attribution.

On the left, global importance: mean absolute SHAP value per feature. Instrumentalness
dominates at 0.0405, roughly 60% above energy, then danceability and valence.
Loudness is eighth, which is worth noting given it correlates with energy at 0.78.

On the right is a single recommendation attributed by both methods. SHAP's ranking
is instrumentalness, danceability, energy, valence, liveness, all positive. LIME's
top item is a binned rule on instrumentalness with a negative weight, then
liveness and valence. Ranks two and three do not overlap.

The text at the bottom is the generated explanation, produced from the top three
SHAP values, so any recommendation can be explained this way."
""")
    return page + 1


def s_consistency(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Results  \u00b7  \u00a74.3", "SHAP and LIME do not agree", page,
           lede="Measured across 200 test instances. This is the most consequential result "
                "so far.")

    picture(s, f"{ASSETS}/fig7_crop.png", ML, 2.20, w=6.20, frame=True)
    text(s, ML, 5.28, 6.05, 0.44,
         "Figure 7 \u00b7 per-instance Spearman \u03c1 between the SHAP and LIME orderings.",
         size=8.6, color=MUTED, line_spacing=1.15)

    x2 = 7.00
    text(s, x2, 2.22, 3.0, 0.30, "\u03c1 = 0.008", size=40, color=ACCENT, bold=True,
         line_spacing=0.95, check=False)
    text(s, x2, 3.06, 5.4, 0.30, "mean Spearman correlation across 200 instances  \u00b7  "
         "SD = 0.359", size=10.2, color=BODY, check=False)

    label(s, x2, 3.48, 5.4, "Three candidate causes")
    causes = [("Surrogate fidelity", "R\u00b2 = 0.105 \u2014 both explainers are attributing "
               "a model that barely resembles the recommender's decision function."),
              ("Collinearity", "energy\u2013loudness at +0.78, energy\u2013acousticness at "
               "\u22120.73; credit can be split or swapped between near-duplicate features."),
              ("Linear misfit", "LIME's local linear approximation may not fit a non-linear, "
               "interaction-heavy gradient-boosting surface.")]
    y = 3.76
    for i, (t, b) in enumerate(causes):
        text(s, x2, y, 0.3, 0.24, str(i + 1), size=9.6, color=ACCENT, bold=True, check=False)
        text(s, x2 + 0.30, y, 5.1, 0.24, t, size=10.4, color=INK, bold=True, check=False)
        text(s, x2 + 0.30, y + 0.24, 5.0, 0.34, b, size=9.0, color=BODY, line_spacing=1.16)
        y += 0.82

    shape(s, ML, 6.06, CW, 0.66, fill=ACCENT_LT, line=None, radius=0.05)
    rect(s, ML, 6.06, 0.06, 0.66, fill=ACCENT)
    text(s, ML + 0.30, 6.16, CW - 0.60, 0.50,
         "A mean of 0.008 with a standard deviation of 0.359 means there is no consistent "
         "agreement, rather than agreement plus noise. On this model the two methods are not "
         "interchangeable.", size=9.8, color=INK, line_spacing=1.16)

    notes(s, """
"This is the result that surprised me most.

I measured rank agreement between SHAP and LIME across 200 instances \u2014 Spearman
correlation between their importance orderings, per instance.

Mean rho is 0.008. The standard deviation is 0.359, so some instances agree
strongly in either direction, but there is no systematic agreement.

If this were noise around a positive value the mean would sit above zero; it does
not, so this is absence of agreement rather than measurement error.

Three candidate causes, which I cannot separate yet. One, the surrogate's
fidelity: both explainers are working on a model that only loosely resembles the
real one. Two, collinearity \u2014 the correlations I showed earlier. Three, LIME's
linear approximation against a non-linear, interaction-heavy surface.

Separating them is the methodological question for the next iteration."
""")
    return page + 1


def s_limitations(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Discussion  \u00b7  \u00a75", "Threats to validity", page,
           lede="Four kinds of threat, and what each one requires.")

    lims = [("Internal validity", "Training budget",
             "Five epochs, manual hyperparameters, no Optuna search. Every neural result is "
             "provisional until the models converge.",
             "Next: extend the schedule, then run the scoped 50-trial search.", ACCENT),
            ("Construct validity", "The surrogate is not the model",
             "SHAP and LIME attribute a GBR surrogate with R\u00b2 = 0.105, so the "
             "explanations describe the acoustic view of the score.",
             "Next: a higher-fidelity surrogate, plus direct explainers where feasible.",
             ACCENT_DK),
            ("External validity", "One catalogue, one sample",
             "150 of 1,000 MPD slices; 55.9% of tracks missing genre; a substituted feature "
             "catalogue rather than the live API.",
             "Next: full-MPD replication as robustness work.", AMBER),
            ("Conclusion validity", "One split, no users",
             "A single random split and a single run per model. No user study has run, so no "
             "claim about satisfaction is supported.",
             "Next: multiple seeds and splits, then the user study.", INK)]
    pos = [(ML, 2.14), (ML + 6.23, 2.14), (ML, 4.12), (ML + 6.23, 4.12)]
    for (t, sub, b, nxt, c), (x, y) in zip(lims, pos):
        shape(s, x, y, 5.86, 1.82, fill=WHITE, line=LINE, radius=0.06)
        rect(s, x, y, 0.05, 1.82, fill=c)
        text(s, x + 0.28, y + 0.14, 3.0, 0.22, t, size=8.4, color=c, bold=True,
             spc=110, caps=True, check=False)
        text(s, x + 0.28, y + 0.38, 5.2, 0.28, sub, size=12.2, color=INK, bold=True,
             check=False)
        text(s, x + 0.28, y + 0.70, 5.28, 0.58, b, size=9.4, color=BODY, line_spacing=1.16)
        hline(s, x + 0.28, y + 1.32, 5.24, LINE, 0.75)
        text(s, x + 0.28, y + 1.40, 5.28, 0.30, nxt, size=9.0, color=c, italic=True,
             line_spacing=1.12)

    text(s, ML, 6.14, CW, 0.50,
         "What is already controlled: identical cohorts and protocols across models, declared "
         "deviations, and every metric reported under the same conditions.",
         size=9.8, color=MUTED, italic=True, line_spacing=1.18)

    notes(s, """
"Four kinds of threat.

Internal: five epochs and manual hyperparameters, so every neural result is
provisional.

Construct, and this is the sharpest one: the surrogate is not the model. Both
explainers attribute an approximation that explains about a tenth of the
variance, so my explanation results are about the acoustic view of the score.

External: one catalogue, 150 of a thousand slices, and a substituted feature
source.

Conclusion: one split, one run, and no users yet, so nothing in this deck
supports a claim about user satisfaction.

Cohorts and protocols are identical across models, and every deviation is
declared."
""")
    return page + 1


def s_outcomes(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Outcomes  \u00b7  \u00a76", "Anticipated outcomes and their status", page,
           lede="Each outcome from the proposal, annotated with what the evidence shows.")

    rows = [["Anticipated outcome", "What the evidence says", "Status"],
            ["Hybrid outperforms NCF on recall and NDCG",
             "Holds on every metric \u2014 NDCG@10 0.0384 vs 0.0342", "Confirmed"],
            ["A 1\u20133 pp accuracy cost for explainability",
             "Not observed: the hybrid was marginally better", "Not observed"],
            ["Explanations raise transparency and trust",
             "Not tested \u2014 user study not yet run", "Pending"],
            ["SHAP and LIME behave consistently",
             "\u03c1 = 0.008 across 200 instances", "New finding"]]
    colors = {1: (ACCENT, ACCENT_LT), 2: (ROSE, ROSE_LT), 3: (AMBER, AMBER_LT),
              4: (INK, WASH_2)}
    table(s, ML, 2.14, CW, rows, col_w=[4.60, 5.39, 2.10], row_h=0.62, header_h=0.40,
          font_size=10.0, header_size=8.6, aligns=["l", "l", "c"], rule_color="FFFFFF",
          cell_colors={(i, 2): c[0] for i, c in colors.items()},
          bold_cells={(i, 2) for i in colors})

    shape(s, ML, 5.32, CW, 1.20, fill=WASH, line=None, radius=0.05)
    rect(s, ML, 5.32, 0.06, 1.20, fill=ACCENT)
    text(s, ML + 0.30, 5.42, CW - 0.60, 1.00,
         "The fourth outcome did not exist when the proposal was written. If it holds up, it "
         "argues against treating SHAP and LIME as interchangeable explainers for hybrid "
         "music recommenders, and it changes what the user study should measure: either "
         "explanation method becomes a design variable, or the study commits to SHAP alone "
         "with a higher-fidelity surrogate.", size=10.0, color=INK, line_spacing=1.20)

    notes(s, """
"Four outcomes, each with what the evidence shows.

One confirmed: the hybrid gain.

One not observed: the predicted accuracy cost did not appear.

One pending, and it combines the two user-study expectations from the proposal,
because neither can be tested until the study runs. I am not going to claim
satisfaction effects from offline metrics.

And the fourth is new. If the SHAP-LIME disagreement holds up, it argues against
treating these two methods as interchangeable, and it changes the user study
design."
""")
    return page + 1


def s_roadmap(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Next steps  \u00b7  \u00a78", "Plan to submission", page,
           lede="Ordered by dependency: the user study cannot run until the explanation method "
                "is fixed.")

    items = [("1", "Train to convergence",
              "Extend the schedule until validation NDCG plateaus, then re-run all five "
              "models.", INK),
             ("2", "Resolve the SHAP\u2013LIME gap",
              "Raise surrogate fidelity; test TreeSHAP with collinearity handling; report "
              "both methods side by side.", AMBER),
             ("3", "Complete the explanation metrics",
              "Add fidelity and coverage; run the scoped Optuna search.", AMBER),
             ("4", "Knowledge-graph explanations",
              "Artist, genre and label pathways \u2014 optional, gated on genre coverage.",
              MUTED),
             ("5", "User study",
              "Explanation conditions against a no-explanation control; perceived "
              "transparency, trust and satisfaction.", ACCENT)]

    vline(s, ML + 0.30, 2.22, 3.70, LINE, 1.2)
    for i, (n, t, b, c) in enumerate(items):
        y = 2.14 + i * 0.78
        shape(s, ML + 0.13, y + 0.10, 0.34, 0.34, fill=c, line=None, radius=0.5,
              kind=MSO_SHAPE.OVAL)
        text(s, ML + 0.13, y + 0.16, 0.34, 0.24, n, size=9.2, color=WHITE, bold=True,
             align=PP_ALIGN.CENTER, check=False)
        text(s, ML + 0.66, y + 0.02, 4.9, 0.26, t, size=11.0, color=INK, bold=True,
             check=False)
        text(s, ML + 0.66, y + 0.30, 5.00, 0.40, b, size=9.2, color=BODY, line_spacing=1.16)

    x2 = 6.55
    shape(s, x2, 2.14, 6.16, 1.64, fill=INK, line=None, radius=0.06)
    text(s, x2 + 0.30, 2.26, 5.4, 0.24, "Why the user study is last", size=8.8, color=ACCENT,
         bold=True, spc=110, caps=True, check=False)
    text(s, x2 + 0.30, 2.54, 5.56, 1.14,
         "A study that measured trust in an artefact of surrogate fidelity would produce a "
         "result about the surrogate rather than about explanation, and it would be "
         "expensive to repeat.", size=10.4, color=DARK_TXT,
         line_spacing=1.24)

    label(s, x2, 4.06, 6.0, "User study \u2014 what it will measure")
    bullets(s, x2, 4.34, 6.10, 1.90, [
        ("Conditions  ", "no explanation \u00b7 feature-ranked text \u00b7 visual attribution."),
        ("Measures  ", "perceived transparency, trust, satisfaction and intention to act."),
        ("Design  ", "within-subject where possible, to control for music expertise."),
        ("Instrument  ", "adapted from the dimensions in Tintarev and Masthoff (2015)."),
    ], size=9.2, gap=9, bullet_color=ACCENT, glyph_size=5.0, indent=0.18, tag="userstudy")

    notes(s, """
"Five items, ordered by dependency.

One and two are the foundation: train to convergence, and resolve the SHAP-LIME
gap. Until those are done, the model numbers and the explanation results stay
provisional.

Three completes the fidelity and coverage metrics and runs the Optuna search.

Four is optional: the knowledge-graph path, which depends on genre coverage.

Five is the user study, and the box explains why it is last. If I ran it now I
would be measuring trust in a surrogate artefact rather than trust in an
explanation, and that is an expensive mistake to find later."
""")
    return page + 1


def s_summary(prs, page):
    s = blank(prs)
    bg_gradient(s, DARK_BG, DARK_BG_2, 35)
    rings(s, 13.9, 7.3, [3.2, 4.6, 6.0], DARK_RING, 0.9)
    text(s, ML, 0.72, 8.0, 0.26, "Summary", size=9.4, color=ACCENT, bold=True, spc=190,
         caps=True, check=False)
    text(s, ML, 1.04, 10.5, 0.62, "Three results and what is still open", size=30,
         color=WHITE, bold=True, check=False)

    points = [("The hybrid outperforms NCF on every metric.",
               "NDCG@10 0.0384 against 0.0342, a 12.3% relative improvement. The content "
               "branch is the only difference between the two models, so the gain is "
               "attributable."),
              ("The model comparison is not settled.",
               "SVD-MF leads on this cohort, and the likely cause is the five-epoch schedule "
               "\u2014 neither loss curve has plateaued. Re-running is the next step."),
              ("SHAP and LIME do not agree on this model.",
               "Mean \u03c1 = 0.008 across 200 instances, with three candidate causes. This is "
               "the result that most affects what the dissertation can claim.")]
    y = 2.06
    for i, (t, b) in enumerate(points):
        text(s, ML, y - 0.06, 0.60, 0.50, f"0{i+1}", size=17, color=ACCENT, bold=True,
             check=False)
        text(s, ML + 0.72, y, 10.9, 0.34, t, size=15.5, color=WHITE, bold=True,
             line_spacing=1.1, check=False)
        text(s, ML + 0.72, y + 0.38, 8.90, 0.56, b, size=11.4, color=DARK_TXT,
             line_spacing=1.26)
        y += 1.30

    hline(s, ML, 6.06, CW, DARK_RING, 1.0)
    text(s, ML, 6.16, 8.90, 0.80,
         "Finished: the pipeline, the baselines and the explanation layer. Provisional: the "
         "model ranking and the attribution results. Next: train to convergence, resolve the "
         "attribution disagreement, then test the explanations with users.",
         size=11.2, color=WHITE, line_spacing=1.3)

    notes(s, """
"Three points.

One, the hybrid beats NCF on every metric, and because the content branch is the
only difference, the gain is attributable.

Two, the model comparison is not settled. SVD-MF leads here, and the likely cause
is the training schedule rather than the architecture. That is the next thing I
run.

Three, SHAP and LIME do not agree on this model, and I have three candidate
causes but cannot yet separate them. That is the result that most affects what
the dissertation can claim.

So: finished, provisional, next."
""")
    return page + 1


def s_thanks(prs, page):
    s = blank(prs)
    bg_gradient(s, DARK_BG, DARK_BG_2, 35)
    rings(s, 11.7, 2.4, [3.6, 5.2, 6.8], DARK_RING, 0.9)

    text(s, ML, 1.34, 8.0, 0.28, "End of presentation", size=9.4, color=ACCENT, bold=True,
         spc=190, caps=True, check=False)
    text(s, ML, 1.70, 10.60, 0.75, "Thank you \u2014 questions welcome", size=34, color=WHITE,
         bold=True, line_spacing=1.05, check=False)
    rect(s, ML + 0.02, 2.52, 0.90, 0.05, fill=ACCENT)

    text(s, ML, 2.80, 8.6, 0.90,
         "I would particularly welcome questions on the surrogate in Section 4.3, and on "
         "whether the SVD-MF result is a training artefact or an architectural finding.",
         size=13.2, color=DARK_TXT, line_spacing=1.35)

    stats = [("0.0384", "hybrid NDCG@10"), ("+12.3%", "over NCF"),
             ("0.008", "SHAP\u2013LIME \u03c1"), ("5", "models benchmarked")]
    x = ML
    for v, l in stats:
        text(s, x, 4.18, 2.9, 0.44, v, size=24, color=WHITE, bold=True, check=False)
        text(s, x, 4.66, 2.9, 0.24, l, size=8.8, color=DARK_TXT,
             caps=True, spc=110, check=False)
        x += 2.92

    hline(s, ML, 5.44, CW, DARK_RING, 1.0)
    text(s, ML, 5.64, 6.0, 0.28,
         "Chike Egonu  \u00b7  MSc Dissertation  \u00b7  August 2026",
         size=11.4, color=WHITE, check=False)
    text(s, ML, 5.94, 6.0, 0.28, "Supervisor: Aoife Curran", size=10.2, color=DARK_TXT,
         check=False)

    text(s, 8.30, 5.60, 4.4, 0.62,
         "Backup slides follow: references, four likely questions and the full results table.",
         size=9.6, color=DARK_TXT, line_spacing=1.25)

    notes(s, """
Thank you, then stop talking. Do not fill the silence.

"I would particularly welcome questions on the surrogate in Section 4.3, because
I know it is the weakest link in the explanation results, and on whether the
SVD-MF result is a training artefact or an architectural finding.

The backup slides cover references, four questions I expect, and the full
results table."
""")
    return page + 1


def build(prs, page):
    page = s_accuracy(prs, page)
    page = s_svd(prs, page)
    page = s_attributions(prs, page)
    page = s_consistency(prs, page)
    page = s_limitations(prs, page)
    page = s_outcomes(prs, page)
    page = s_roadmap(prs, page)
    page = s_summary(prs, page)
    page = s_thanks(prs, page)
    return page
