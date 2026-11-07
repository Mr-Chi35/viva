"""Section 04 (preliminary results) and section 05 (discussion, outcomes, next steps)."""
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

from deck_lib import *

ASSETS = "assets"
CHARTS = "charts"


def s_accuracy(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Preliminary results  \u00b7  \u00a74.2", "Offline accuracy at K = 10", page,
           lede="Five models, one fixed 1,000-user cohort, identical protocol.")

    picture(s, f"{CHARTS}/accuracy_k10.png", ML, 2.06, w=8.30, frame=False)
    text(s, ML, 6.02, 8.2, 0.62,
         "Figure 3 (re-plotted)  \u00b7  Precision, recall, NDCG and MRR at K = 10 for all five "
         "models. Absolute values are small because the matrix is 99.93% sparse \u2014 the "
         "informative signal is the ordering between models, not the level.",
         size=8.6, color=MUTED, line_spacing=1.15)

    x2 = 9.32
    shape(s, x2, 2.06, 3.39, 4.32, fill=WASH, line=None, radius=0.06)
    text(s, x2 + 0.26, 2.20, 3.0, 0.24, "Read this in three lines", size=8.8, color=ACCENT_DK,
         bold=True, spc=110, caps=True, check=False)

    items = [("SVD-MF leads every metric.", "NDCG@10 0.0769 \u2014 roughly twice the hybrid."),
             ("Hybrid beats NCF everywhere.", "NDCG@10 0.0384 against 0.0342."),
             ("Two baselines sit near the floor.", "Content-only scores an NDCG@10 of 0.0027.")]
    y = 2.58
    for i, (lead, rest) in enumerate(items):
        text(s, x2 + 0.26, y, 2.9, 0.20, f"{i+1}", size=9, color=ACCENT, bold=True,
             check=False)
        text(s, x2 + 0.26, y + 0.22, 2.92, 0.26, lead, size=10.2, color=INK, bold=True,
             line_spacing=1.1, check=False)
        text(s, x2 + 0.26, y + 0.56, 2.92, 0.42, rest, size=9.4, color=BODY,
             line_spacing=1.16)
        y += 1.15

    text(s, x2, 6.44, 3.39, 0.34,
         "Full table at K \u2208 {5, 10, 20} is in the notebook.", size=8.4, color=MUTED,
         italic=True, check=False)

    notes(s, """
TIMING: 60 s.

"All five models, one cohort, one protocol. Reading left to right within each
metric block.

Two things to take away.

First, the ranking is consistent across all four metrics: SVD-MF, then the
hybrid, then NCF, then popularity, then content-only. Consistency across four
different metrics is reassuring \u2014 it is not a metric artefact.

Second, the levels are small, and I want to pre-empt the obvious objection. With
99.93% sparsity and four sampled negatives per positive, precision at ten in the
hundredths is expected. Absolute values here are not comparable to a production
system; the ordering is what the objectives rest on.

I am deliberately not going to claim the hybrid 'wins' overall, because it does
not \u2014 SVD-MF does. That is the next two slides."
""")
    return page + 1


def s_hybrid(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Preliminary results  \u00b7  \u00a74.2", "Finding 1 \u2014 the content branch earns its place", page,
           lede="The hybrid model outperforms NCF-only on every metric at every K. This is "
                "the direction the proposal anticipated.")

    picture(s, f"{CHARTS}/hybrid_gain.png", ML, 2.34, w=6.30, frame=False)
    text(s, ML, 5.02, 6.2, 0.42,
         "Relative improvement of the hybrid over NCF-only at K = 10, same training "
         "schedule, same cohort.", size=8.6, color=MUTED, check=False)

    x2 = 7.30
    text(s, x2, 2.28, 5.4, 0.34,
         [("Every metric. ", {"color": INK, "bold": True, "size": 18}),
          ("Every K.", {"color": ACCENT, "bold": True, "size": 18})],
         size=18, check=False)
    text(s, x2, 2.76, 5.38, 0.62,
         "NDCG@10 improves 12.3% relative; recall@10 improves 18.8%. Because the only "
         "difference between the two models is the content branch, the gain is attributable "
         "to acoustic features.", size=10.6, color=BODY, line_spacing=1.22)

    bullets(s, x2, 3.58, 5.38, 1.60, [
        ("Recall gains most. ", "18.8% \u2014 consistent with content features helping most "
         "where collaborative signal is thin, such as sparsely observed tracks."),
        ("MRR gains least. ", "2.2% \u2014 the hybrid does not especially improve how quickly "
         "the first relevant track appears, it improves coverage."),
    ], size=9.9, gap=9, tag="hybridbullets")

    pill(s, x2, 5.24, 2.30, 0.32, "objective 1 \u00b7 confirmed", fg=WHITE, bg=TEAL, size=8.2)

    shape(s, ML, 5.86, CW, 0.80, fill=WASH, line=None, radius=0.05)
    rect(s, ML, 5.86, 0.06, 0.80, fill=AMBER)
    text(s, ML + 0.30, 5.96, CW - 0.60, 0.62,
         "Relative, not absolute. Both neural models remain well below SVD-MF \u2014 as the "
         "next slide shows, that gap is probably a training-budget artefact, not an "
         "architectural verdict.", size=10.4, color=BODY, line_spacing=1.18)

    notes(s, """
TIMING: 60 s.

"This is the result the proposal predicted, and it holds.

The hybrid beats NCF on every metric. NDCG at ten up 12.3% relative, recall up
18.8%, precision 6.4%, MRR 2.2%.

Why this is attributable and not luck: the two models are identical except for
the content branch. Same embeddings, same training schedule, same negatives, same
cohort. The delta is the content branch.

The shape of the gains is also interpretable. Recall benefits most, which is what
you would expect if acoustic features help most on items with thin collaborative
evidence. MRR benefits least \u2014 the hybrid is not better at putting a relevant
track at the very top; it is better at covering more of what the user would
actually play.

Now the caveat I put on the slide, because it is true: relative, not absolute.
Both neural models sit below SVD-MF."
""")
    return page + 1


def s_svd(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Preliminary results  \u00b7  \u00a74.2", "Finding 2 \u2014 the result that was not in the proposal", page,
           lede="SVD matrix factorisation outperforms both neural models by a wide margin. "
                "The diagnosis matters more than the number.")

    picture(s, f"{CHARTS}/svd_gap.png", ML, 2.16, w=6.05, frame=False)
    text(s, ML, 4.66, 6.0, 0.20, "NDCG@10 by model \u2014 the classical model is not the weak one.",
         size=8.6, color=MUTED, check=False)

    x2 = 6.95
    bullets(s, x2, 2.16, 5.72, 2.24, [
        ("The gap is large. ", "NDCG@10 0.0769 against 0.0384 for the hybrid \u2014 roughly "
         "double. It holds across precision, recall and MRR too."),
        ("The likely cause is the schedule. ", "Five epochs for the neural models against a "
         "closed-form solution for SVD-MF."),
        ("The evidence is the loss curve. ", "Neither model has plateaued at epoch 5, so the "
         "comparison is not between trained equals."),
    ], size=10.4, gap=10, tag="svd")

    label(s, ML, 4.90, 3.6, "Training loss \u00b7 ncf vs hybrid")
    picture(s, f"{ASSETS}/fig4_loss_curves.png", ML, 5.18, w=3.34, frame=True,
            caption=None)

    x3 = 4.42
    shape(s, x3, 4.94, 8.29, 1.80, fill=AMBER_LT, line=None, radius=0.06)
    rect(s, x3, 4.94, 0.06, 1.80, fill=AMBER)
    text(s, x3 + 0.32, 5.08, 7.6, 0.24, "Priority for the next iteration", size=9,
         color=AMBER, bold=True, spc=120, caps=True, check=False)
    text(s, x3 + 0.32, 5.36, 7.66, 1.22,
         "Extend the schedule until validation NDCG plateaus, then re-run all five models "
         "before drawing conclusions about model choice. If the neural models close the gap, "
         "the story is 'under-trained'; if they do not, the story is genuinely interesting "
         "and the proposal's framing of Koren et al. (2009) needs revising. Either outcome is "
         "reportable \u2014 but only after the rerun.",
         size=10.2, color=BODY, line_spacing=1.22)

    notes(s, """
TIMING: 75 s.

"Here is the result that was not in the proposal.

SVD matrix factorisation \u2014 the classical baseline the proposal framed as inferior
\u2014 is the strongest model on this cohort. NDCG at ten is 0.0769 against 0.0384 for
the hybrid. Not a rounding difference; roughly double.

I want to be careful about what I claim from this. The most plausible explanation
is not that neural collaborative filtering is worse than matrix factorisation.
It is that these two neural models were trained for five epochs and never
plateaued. Look at the loss curve on the left: both are still descending at
epoch five. SVD-MF is a closed-form solution, so it is 'converged' by
construction.

So the comparison is not between trained equals, and I have flagged it as the
first item on the roadmap rather than presenting it as a settled architectural
finding.

Why this matters for the viva: the honest reading is that the hybrid-versus-NCF
comparison \u2014 which is what Objective 1 actually needs \u2014 is like-for-like, because
both were trained identically. The comparison against SVD-MF is not, and I am not
claiming it."
""")
    return page + 1


def s_shap_global(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Preliminary results  \u00b7  \u00a74.3", "Global attributions \u2014 what drives the score", page,
           lede="Mean absolute SHAP value across the test cohort, computed on the "
                "gradient-boosting surrogate.")

    picture(s, f"{CHARTS}/shap_importance.png", ML, 2.14, w=6.05, frame=False)
    text(s, ML, 5.24, 6.0, 0.24, "Mean |SHAP value| per feature \u2014 global importance ranking.",
         size=8.6, color=MUTED, check=False)

    picture(s, f"{ASSETS}/fig5_shap_beeswarm.png", 7.02, 2.14, w=4.72, frame=True)
    text(s, 7.02, 5.24, 4.7, 0.24,
         "SHAP summary (beeswarm): one point per instance, coloured by feature value.",
         size=8.6, color=MUTED, check=False)

    shape(s, ML, 5.58, CW, 1.06, fill=WASH, line=None, radius=0.05)
    rect(s, ML, 5.58, 0.06, 1.06, fill=ACCENT)
    text(s, ML + 0.30, 5.68, 3.6, 0.24, "How to read it", size=9, color=ACCENT_DK,
         bold=True, spc=110, caps=True, check=False)
    text(s, ML + 0.30, 5.94, CW - 0.60, 0.64,
         "Instrumentalness is the dominant driver by a clear margin (0.0405), followed by "
         "energy and danceability. Loudness \u2014 the feature most correlated with energy "
         "(r = +0.78) \u2014 ranks eighth. That inversion is a first hint of the credit-"
         "redistribution problem that surfaces next.",
         size=9.9, color=BODY, line_spacing=1.20)

    notes(s, """
TIMING: 60 s.

"Global attributions. On the left, mean absolute SHAP value per feature; on the
right, the beeswarm, where each dot is one instance and colour is the feature's
raw value.

Instrumentalness dominates, at 0.0405 \u2014 roughly 60% more than the next feature,
energy. Then danceability and valence. Liveness and loudness are weakest.

Now, one thing to notice, because it sets up the next two slides. Loudness is
the eighth most important feature here, yet it correlates with energy at 0.78.
When two features carry almost the same information, attribution methods have to
choose where to put the credit \u2014 and different methods choose differently.

Which is exactly the problem."

NOTE FOR PRESENTING: if asked, say plainly that these are attributions of the
surrogate, not of the hybrid model directly (R\u00b2 = 0.105), and that the
surrogate explains the acoustic view of the score.
""")
    return page + 1


def s_instance(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Preliminary results  \u00b7  \u00a74.3", "Instance level \u2014 one recommendation, two explanations", page,
           lede="Identical instance, identical surrogate. SHAP on the left, LIME on the right.")

    picture(s, f"{ASSETS}/fig6_shap_vs_lime.png", ML, 2.18, w=8.05, frame=True)
    text(s, ML, 5.22, 8.0, 0.62,
         "SHAP's top driver is instrumentalness with a positive contribution (+0.032); "
         "LIME's is a binned rule on instrumentalness with the opposite sign (\u22120.055). "
         "Ranks two and three do not overlap at all.",
         size=9.4, color=BODY, line_spacing=1.18)

    x2 = 8.90
    shape(s, x2, 2.18, 3.81, 1.86, fill=INK, line=None, radius=0.06)
    text(s, x2 + 0.28, 2.30, 3.2, 0.24, "generated explanation", size=8.2, color=TEAL,
         bold=True, spc=120, caps=True, check=False)
    text(s, x2 + 0.28, 2.58, 3.26, 1.32,
         "\u201cThis track was recommended primarily because of its high instrumentalness, "
         "alongside danceability (+0.026) and energy (+0.015).\u201d",
         size=10.6, color=WHITE, italic=True, line_spacing=1.30)

    text(s, x2, 4.14, 3.75, 0.24, "Produced directly from the instance's top-3 SHAP "
         "attributions.", size=8.4, color=MUTED, check=False)

    shape(s, ML, 6.06, 8.05, 0.62, fill=WASH, line=None, radius=0.05)
    rect(s, ML, 6.06, 0.06, 0.62, fill=ACCENT)
    text(s, ML + 0.28, 6.15, 7.62, 0.46,
         "Both methods rank instrumentalness first. They disagree about what it did to the "
         "score \u2014 and that disagreement is exactly what a user would be told.",
         size=9.8, color=INK, line_spacing=1.14)

    label(s, x2, 4.58, 3.7, "Why this matters")
    bullets(s, x2, 4.86, 3.76, 1.76, [
        ("Content, not numbers. ", "The output is musical \u2014 instrumentalness, danceability, "
         "energy \u2014 not a list of embedding dimensions."),
        ("Cheap to generate. ", "Runs directly off the attribution vector, so any "
         "recommendation can be explained."),
    ], size=9.2, gap=8, tag="inst")

    notes(s, """
TIMING: 60 s.

"Same recommendation instance, same surrogate, two explainers.

SHAP on the left: instrumentalness, danceability, energy, valence, liveness \u2014 all
positive contributions, topped by instrumentalness at 0.032.

LIME on the right: its top item is a binned rule \u2014 instrumentalness below minus
0.49 \u2014 with a negative weight of 0.055. Same feature, opposite direction. Its
number two is liveness, which SHAP ranks fifth. Number three is valence, which
SHAP ranks fourth. Ranks two and three do not overlap at all.

On the right is the artefact I actually built: the natural-language explanation
generated from the top-three SHAP values. 'This track was recommended primarily
because of its high instrumentalness, alongside danceability and energy.'

That is the deliverable for the first explanation format, and it works \u2014 it runs
straight off the attribution vector, so any recommendation can be explained.

But look at what the two panels disagree about. That is the next slide."
""")
    return page + 1


def s_consistency(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Preliminary results  \u00b7  \u00a74.3", "Finding 3 \u2014 SHAP and LIME do not agree", page,
           lede="The most consequential result so far. It contradicts a working assumption in "
                "the proposal.")

    picture(s, f"{ASSETS}/fig7_spearman.png", ML, 2.32, w=6.10, frame=True)
    text(s, ML, 5.42, 6.0, 0.44,
         "Distribution of per-instance Spearman \u03c1 between SHAP and LIME importance "
         "orderings, 200 test instances.", size=8.6, color=MUTED, line_spacing=1.15)

    x2 = 7.00
    text(s, x2, 2.22, 3.0, 0.30, "\u03c1 = 0.008", size=40, color=ACCENT, bold=True,
         line_spacing=0.95, check=False)
    text(s, x2, 3.06, 5.4, 0.30, "mean Spearman correlation across 200 instances  \u00b7  "
         "SD = 0.359", size=10.2, color=BODY, check=False)

    label(s, x2, 3.48, 5.4, "Three candidate causes")
    causes = [("Surrogate fidelity", "R\u00b2 = 0.105 \u2014 both explainers are attributing a "
               "model that barely resembles the recommender's decision function."),
              ("Collinearity", "energy\u2013loudness at +0.78, energy\u2013acousticness at "
               "\u22120.73. Credit can be split or swapped between near-duplicate features."),
              ("Linear misfit", "LIME's local linear approximation may simply not fit a "
               "non-linear, interaction-heavy GBM surface.")]
    y = 3.76
    for i, (t, b) in enumerate(causes):
        text(s, x2, y, 0.3, 0.24, str(i + 1), size=9.6, color=ACCENT, bold=True, check=False)
        text(s, x2 + 0.30, y, 5.1, 0.24, t, size=10.4, color=INK, bold=True, check=False)
        text(s, x2 + 0.30, y + 0.24, 5.0, 0.34, b, size=9.0, color=BODY, line_spacing=1.16)
        y += 0.82

    shape(s, ML, 6.02, CW, 0.66, fill=ACCENT_LT, line=None, radius=0.05)
    rect(s, ML, 6.02, 0.06, 0.66, fill=ACCENT)
    text(s, ML + 0.30, 6.12, CW - 0.60, 0.50,
         "A correlation indistinguishable from zero is not measurement noise \u2014 it is the "
         "absence of systematic agreement. Two 'standard' explainers are not interchangeable "
         "on this model.", size=10.0, color=INK, line_spacing=1.16)

    notes(s, """
TIMING: 75 s. This is the slide to slow down on.

"And now the result that surprised me most.

I measured the rank agreement between SHAP and LIME across 200 instances \u2014
Spearman correlation between the two importance orderings, per instance.

Mean rho: 0.008. Essentially zero. Standard deviation 0.359, so there are
instances where they agree well in either direction, but no systematic agreement
at all.

I want to address the noise objection directly, because it is the right one to
ask: if this were noise around a positive value, we would see a mean well above
zero with dispersion. We see a mean indistinguishable from zero. That is the
absence of agreement, not measurement error.

Three candidate causes, and I can rule none of them out yet.

One, the surrogate's fidelity. R-squared 0.105 means both explainers are working
on a model that only loosely resembles the real decision function. If your
surrogate is wrong, explaining it is explaining the wrong thing.

Two, collinearity. I showed those correlations earlier. When energy, loudness and
acousticness carry overlapping information, both methods can legitimately put the
credit in different places.

Three, LIME's linear approximation against a non-linear, interaction-heavy
gradient-boosting surface.

Which of the three dominates is exactly what the next iteration has to
separate \u2014 and that is a real methodological question, not a bug to patch."
""")
    return page + 1


def s_tradeoff(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Preliminary results  \u00b7  \u00a74.4", "Accuracy against explainability", page,
           lede="Objective 3 asked what it costs to keep the architecture decomposable. In "
                "this run, it cost nothing.")

    # predicted
    shape(s, ML, 2.14, 5.50, 1.42, fill=WASH, line=None, radius=0.05)
    rect(s, ML, 2.14, 0.06, 1.42, fill=ROSE)
    text(s, ML + 0.30, 2.24, 4.8, 0.22, "What the proposal predicted", size=8.6, color=ROSE,
         bold=True, spc=110, caps=True, check=False)
    text(s, ML + 0.30, 2.48, 2.9, 0.44, "\u22121 to \u22123 pp", size=20, color=INK, bold=True,
         check=False)
    text(s, ML + 0.30, 3.00, 4.9, 0.46,
         "accuracy cost on NDCG@10 for a feature-decomposable design, following "
         "Zhang et al. (2018).", size=9.4, color=BODY, line_spacing=1.15)

    # observed
    shape(s, ML, 3.72, 5.50, 1.42, fill=TEAL_LT, line=None, radius=0.05)
    rect(s, ML, 3.72, 0.06, 1.42, fill=TEAL)
    text(s, ML + 0.30, 3.82, 4.8, 0.22, "What was observed", size=8.6, color=TEAL, bold=True,
         spc=110, caps=True, check=False)
    text(s, ML + 0.30, 4.08, 2.0, 0.5, "+0.0042", size=22, color=INK, bold=True, check=False)
    text(s, ML + 2.34, 4.20, 2.9, 0.34, "NDCG@10  \u00b7  +12.3% relative", size=10,
         color=TEAL, bold=True, check=False)
    text(s, ML + 0.30, 4.60, 4.9, 0.44,
         "the hybrid was marginally better than NCF, not worse \u2014 and better on every "
         "metric.", size=9.4, color=BODY, line_spacing=1.15)

    # right column
    x2 = 6.55
    bullets(s, x2, 2.16, 6.16, 2.72, [
        ("The cost was zero \u2014 cautiously. ", "Keeping the content branch separable did not "
         "trade accuracy for explainability in this run; the direction was the opposite."),
        ("But the comparison is confounded. ", "The same five-epoch schedule that flatters "
         "SVD-MF could be suppressing NCF more than the hybrid \u2014 in which case the gap "
         "would widen, or invert."),
        ("So the conclusion is withheld. ", "Calling explainability 'free' on this evidence "
         "would overstate a first pass on under-trained models."),
    ], size=10.6, gap=12, tag="tradeoff")

    label(s, x2, 5.02, 6.0, "What a fuller ablation has to vary")
    chip_flow(s, x2, 5.30, 6.10, ["Content-branch capacity", "Embedding dimension",
                                  "Epoch budget", "Negative sampling rate",
                                  "Fusion point (early vs late)"], h=0.30, size=8.2)

    shape(s, ML, 5.96, CW, 0.72, fill=WASH, line=None, radius=0.05)
    rect(s, ML, 5.96, 0.06, 0.72, fill=ACCENT)
    text(s, ML + 0.30, 6.04, CW - 0.60, 0.56,
         "Objective 3 status: first pass complete, conclusion deliberately withheld. The "
         "ablation is designed; it needs a converged model underneath it to mean anything.",
         size=10.2, color=INK, line_spacing=1.16)

    notes(s, """
TIMING: 60 s.

"Objective three asked a specific question: what does it cost in accuracy to keep
the architecture decomposable \u2014 that is, to keep the content branch separable
so it can be explained?

The proposal predicted a cost of one to three percentage points on NDCG at ten,
following Zhang and colleagues.

What I observed was a small gain, not a cost: plus 0.0042, plus 12.3% relative.
The explainable design was not a handicap in this run.

Now I am going to argue against my own result. That comparison is confounded by
exactly the same thing that inflated SVD-MF. If the neural models are
under-trained, and if NCF is hurt more by a short schedule than the hybrid is,
then a proper training run could widen the gap \u2014 or invert it.

So I am not claiming explainability is free. I am claiming that on a converged
model set, the ablation on the right is what has to be run before that claim can
be made. The design is ready; the foundation underneath it is not."
""")
    return page + 1


# ---------------------------------------------------------------- discussion
def s_discussion(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Discussion  \u00b7  \u00a75", "What held up, and what did not", page,
           lede="Three predictions confirmed, three contradicted \u2014 and both surprises are "
                "diagnosable rather than mysterious.")

    # confirmed column
    shape(s, ML, 2.14, 5.86, 3.42, fill=WHITE, line=LINE, radius=0.06)
    rect(s, ML, 2.14, 5.86, 0.05, fill=TEAL)
    text(s, ML + 0.28, 2.28, 4.0, 0.26, "Held up", size=13, color=INK, bold=True, check=False)
    held = [("Hybrid beats NCF", "on every metric at every K \u2014 +12.3% NDCG@10"),
            ("Content features add signal", "attributable, since the branch is the only "
             "difference"),
            ("The explanation layer works", "text and visual formats run end-to-end")]
    y = 2.68
    for t, b in held:
        text(s, ML + 0.28, y, 0.28, 0.24, "\u2713", size=11, color=TEAL, bold=True,
             check=False)
        text(s, ML + 0.60, y, 4.9, 0.24, t, size=10.6, color=INK, bold=True, check=False)
        text(s, ML + 0.60, y + 0.24, 4.86, 0.30, b, size=9.0, color=BODY, check=False)
        y += 0.90

    # contradicted
    x2 = ML + 6.23
    shape(s, x2, 2.14, 5.86, 3.42, fill=WHITE, line=LINE, radius=0.06)
    rect(s, x2, 2.14, 5.86, 0.05, fill=ROSE)
    text(s, x2 + 0.28, 2.28, 4.4, 0.26, "Did not hold", size=13, color=INK, bold=True,
         check=False)
    contradicted = [("A 1\u20133 pp accuracy cost", "no cost observed \u2014 the hybrid was "
                     "marginally better"),
                    ("Classical MF is inferior", "SVD-MF leads by roughly 2\u00d7 on NDCG@10"),
                    ("SHAP \u2248 LIME consistency", "\u03c1 = 0.008 \u2014 no systematic "
                     "agreement at all")]
    y = 2.68
    for t, b in contradicted:
        text(s, x2 + 0.28, y, 0.28, 0.24, "\u2715", size=11, color=ROSE, bold=True,
             check=False)
        text(s, x2 + 0.60, y, 4.9, 0.24, t, size=10.6, color=INK, bold=True, check=False)
        text(s, x2 + 0.60, y + 0.24, 4.86, 0.30, b, size=9.0, color=BODY, check=False)
        y += 0.90

    shape(s, ML, 5.70, CW, 0.96, fill=INK, line=None, radius=0.05)
    text(s, ML + 0.34, 5.80, 2.4, 0.24, "The unifying point", size=8.8, color=TEAL,
         bold=True, spc=110, caps=True, check=False)
    text(s, ML + 0.34, 6.06, CW - 0.70, 0.50,
         "Both surprises have a mechanism, not a mystery: one is a training-budget artefact "
         "and the other is a fidelity-plus-collinearity artefact. Neither requires a new "
         "theory \u2014 both require a rerun.", size=10.4,
         color=RGBColor(0xD5, 0xD8, 0xE8), line_spacing=1.18)

    notes(s, """
TIMING: 70 s.

"Let me put the six findings side by side.

Three held up. The hybrid beats NCF \u2014 that was predicted and it is
attributable, because the content branch is the only difference. Content features
add signal. And the explanation layer works end to end: text and visual.

Three did not. No accuracy cost for explainability \u2014 that was predicted and did
not appear. Classical matrix factorisation was supposed to be the weak baseline;
it is the strongest model. And SHAP and LIME, which the proposal implicitly
treated as interchangeable well-documented tools, do not agree at all on this
model.

Here is the point I would like to defend: neither surprise is mysterious. One is
a training budget \u2014 five epochs against a closed-form solution. The other is
surrogate fidelity plus feature collinearity. Both are diagnosable, both are
testable, and neither requires me to invent a new theory. That is a good position
for a dissertation to be in at this stage."
""")
    return page + 1


def s_limitations(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Discussion  \u00b7  \u00a75", "Limitations, by type", page,
           lede="Four kinds of threat, stated before they are asked about.")

    lims = [("Internal validity", "Training budget",
             "Five epochs, manual hyperparameters, no Optuna search. Every neural result is "
             "provisional until the models converge.",
             "Next: extend the schedule, then run the scoped 50-trial search.", AMBER),
            ("Construct validity", "The surrogate is not the model",
             "SHAP and LIME attribute a GBR surrogate with R\u00b2 = 0.105. The explanations "
             "describe the acoustic view of the score, not the score.",
             "Next: a higher-fidelity surrogate, plus direct explainers where feasible.", ROSE),
            ("External validity", "One catalogue, one sample",
             "150 of 1,000 MPD slices; 55.9% of tracks missing genre; a substituted feature "
             "catalogue rather than the live API.",
             "Next: full-MPD replication as robustness work.", ACCENT),
            ("Conclusion validity", "One split, no users",
             "A single random split and a single training run per model. No user study has "
             "run, so no claim about satisfaction is yet supported.",
             "Next: multiple seeds and splits, then the user study.", TEAL)]
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
         "Mitigations already in place: identical cohorts and protocols across models, "
         "declared deviations, and every metric reported under the same conditions. What "
         "remains open is stated on the roadmap, not hidden in a footnote.",
         size=9.8, color=MUTED, italic=True, line_spacing=1.18)

    notes(s, """
TIMING: 60 s.

"Four kinds of limitation, and I would rather lay them out than be walked into
them.

Internal: five epochs and manual hyperparameters. Every neural result is
provisional.

Construct, and this is the sharpest one: the surrogate is not the model. Both
explainers attribute a gradient-boosting approximation that explains about a
tenth of the variance. So my explanation results are about the acoustic view of
the score.

External: one catalogue, 150 of a thousand slices, 55.9% of tracks without genre,
and a substituted feature source.

Conclusion: a single split, a single run, and no users yet. So nothing in this
deck supports a claim about user satisfaction \u2014 which is the title of the
project, and it is the part that has not been tested.

What I do have in place: identical cohorts and protocols, declared deviations,
and every number reported under the same conditions."
""")
    return page + 1


def s_outcomes(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Outcomes  \u00b7  \u00a76", "Anticipated outcomes, revised against the evidence", page,
           lede="Each outcome from the proposal, annotated with its current status \u2014 "
                "including the one outcome the results added.")

    rows = [["Anticipated outcome", "What the evidence says", "Status"],
            ["Hybrid outperforms NCF on recall and NDCG",
             "Holds on every metric at every K \u2014 NDCG@10 0.0384 vs 0.0342", "Confirmed"],
            ["A 1\u20133 pp accuracy cost for explainability",
             "Not observed: the hybrid was marginally better, not worse", "Contradicted"],
            ["Explanations raise perceived transparency and trust",
             "Untested \u2014 user study not yet run", "Pending"],
            ["Visual vs textual format depends on data literacy",
             "Untested \u2014 user study not yet run", "Pending"],
            ["SHAP and LIME behave consistently",
             "\u03c1 = 0.008 across 200 instances \u2014 a new, dissertation-worthy result",
             "New finding"]]
    colors = {1: (TEAL, TEAL_LT), 2: (ROSE, ROSE_LT), 3: (AMBER, AMBER_LT),
              4: (AMBER, AMBER_LT), 5: (ACCENT, ACCENT_LT)}
    table(s, ML, 2.14, CW, rows, col_w=[4.36, 5.63, 2.10], row_h=0.62, header_h=0.40,
          font_size=9.8, header_size=8.6, aligns=["l", "l", "c"], rule_color="FFFFFF",
          cell_colors={(i, 2): c[0] for i, c in colors.items()},
          bold_cells={(i, 2) for i in colors})

    shape(s, ML, 5.90, CW, 0.78, fill=ACCENT_LT, line=None, radius=0.05)
    rect(s, ML, 5.90, 0.06, 0.78, fill=ACCENT)
    text(s, ML + 0.30, 6.00, CW - 0.60, 0.60,
         "The fifth outcome did not exist when the proposal was approved. If it survives the "
         "next iteration it argues against treating SHAP and LIME as interchangeable "
         "off-the-shelf explainers for hybrid music recommenders \u2014 and that changes what "
         "the user study should measure.", size=10.0, color=INK, line_spacing=1.18)

    notes(s, """
TIMING: 55 s.

"Five anticipated outcomes, each annotated with what actually happened.

One confirmed: the hybrid gain.

Two contradicted: the predicted accuracy cost did not appear.

Two pending: both about the user study, which has not run. I am not going to
claim satisfaction effects from offline metrics.

And a fifth that did not exist when the proposal was approved \u2014 the SHAP\u2013LIME
disagreement. If that survives investigation, it is a dissertation-worthy finding
in its own right, because it argues against the assumption that these two methods
are interchangeable commodities.

It also changes the user study design: explanation method becomes a design
variable, or we commit to SHAP alone with a higher-fidelity surrogate."
""")
    return page + 1


def s_roadmap(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Next steps  \u00b7  \u00a78", "Plan to submission", page,
           lede="Ordered by dependency, not by preference \u2014 the user study cannot run "
                "before the explanation method is fixed.")

    items = [("1", "Train to convergence", "1\u20132 weeks",
              "Extend the schedule until validation NDCG plateaus, then re-run all five "
              "models. Everything downstream inherits this.", TEAL),
             ("2", "Execute the hyperparameter search", "1\u20132 weeks",
              "Run the scoped 50-trial Optuna study against the full model set.", TEAL),
             ("3", "Resolve the SHAP\u2013LIME gap", "2 weeks",
              "Raise surrogate fidelity; test TreeSHAP with collinearity handling; report "
              "both methods side by side.", AMBER),
             ("4", "Complete explanation metrics", "1 week",
              "Fidelity (SHAP rank vs perturbation sensitivity) and coverage.", AMBER),
             ("5", "Knowledge-graph explanations", "1\u20132 weeks",
              "Artist, genre and label pathways \u2014 stretch goal, gated on genre coverage.",
              MUTED),
             ("6", "User study", "3\u20134 weeks",
              "Explanation conditions against a no-explanation control; perceived "
              "transparency, trust and satisfaction.", ACCENT)]

    vline(s, ML + 0.30, 2.22, 4.30, LINE, 1.2)
    for i, (n, t, dur, b, c) in enumerate(items):
        y = 2.14 + i * 0.76
        shape(s, ML + 0.13, y + 0.10, 0.34, 0.34, fill=c, line=None, radius=0.5,
              kind=MSO_SHAPE.OVAL)
        text(s, ML + 0.13, y + 0.16, 0.34, 0.24, n, size=9.2, color=WHITE, bold=True,
             align=PP_ALIGN.CENTER, check=False)
        text(s, ML + 0.66, y + 0.02, 3.40, 0.26, t, size=11.0, color=INK, bold=True,
             check=False)
        text(s, ML + 0.66, y + 0.28, 3.70, 0.40, b, size=8.8, color=BODY, line_spacing=1.14)
        text(s, ML + 4.42, y + 0.10, 1.36, 0.24, dur, size=8.4, color=c, bold=True,
             align=PP_ALIGN.RIGHT, check=False)

    # right panel
    x2 = 6.55
    shape(s, x2, 2.14, 6.16, 1.86, fill=INK, line=None, radius=0.06)
    text(s, x2 + 0.30, 2.26, 5.4, 0.24, "Sequencing rule", size=8.8, color=TEAL, bold=True,
         spc=110, caps=True, check=False)
    text(s, x2 + 0.30, 2.54, 5.56, 1.34,
         "Do not run the user study until the explanation method is fixed. A study that "
         "measures trust in an artefact of surrogate fidelity would produce a result about "
         "the surrogate, not about explanation \u2014 and it would be expensive to redo.",
         size=10.4, color=RGBColor(0xD5, 0xD8, 0xE8), line_spacing=1.24)

    label(s, x2, 4.24, 6.0, "User study \u2014 what it will measure")
    bullets(s, x2, 4.52, 6.10, 1.60, [
        ("Conditions  ", "no explanation \u00b7 feature-ranked text \u00b7 visual attribution "
                         "\u00b7 (if resolved) a second explainer."),
        ("Measures  ", "perceived transparency, trust, satisfaction and intention to act \u2014 "
                       "the dimensions from Tintarev and Masthoff (2015)."),
        ("Design  ", "within-subject where possible, to control for individual differences "
                     "in music expertise."),
    ], size=9.2, gap=7, bullet_color=ACCENT, glyph_size=5.0, indent=0.18, tag="userstudy")

    notes(s, """
TIMING: 60 s.

"Six items, ordered by dependency rather than by how attractive they are.

One and two are the foundation: train to convergence, run the hyperparameter
search. Until that is done, every neural number in this deck is provisional, and
I have said so twice already.

Three is the interesting one: resolve the SHAP\u2013LIME gap. That means a
higher-fidelity surrogate, TreeSHAP with explicit collinearity handling, and
reporting both methods rather than assuming they agree.

Four is completing the explanation metrics \u2014 fidelity and coverage \u2014 which are
designed but not computed.

Five is the knowledge-graph path, which stays a stretch goal because genre
coverage is 44%.

Six is the user study, and the box on the right is the rule I am holding myself
to: do not run it before the explanation method is stable. Otherwise I would be
measuring trust in a surrogate artefact instead of trust in an explanation, and
that is an expensive mistake to discover later."
""")
    return page + 1


def s_contributions(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Justification  \u00b7  \u00a77", "Why this project is worth the time", page,
           lede="Three grounds \u2014 feasibility, originality, relevance \u2014 now backed by "
                "evidence rather than intent.")

    pillars = [("Feasibility", "Demonstrated, not assumed", TEAL),
               ("Originality", "In the combination, not the components", ACCENT),
               ("Relevance", "A live gap, and a timely one", AMBER)]
    for i, (t, sub, c) in enumerate(pillars):
        y = 2.14 + i * 1.42
        shape(s, ML, y, 5.50, 1.26, fill=WHITE, line=LINE, radius=0.06)
        rect(s, ML, y, 0.05, 1.26, fill=c)
        text(s, ML + 0.28, y + 0.16, 4.8, 0.26, t, size=12.6, color=INK, bold=True,
             check=False)
        text(s, ML + 0.28, y + 0.46, 4.9, 0.24, sub, size=9.4, color=c, bold=True,
             check=False)
        body = [("A five-model offline pipeline and a working explanation-generation path "
                 "already run end-to-end on real data at realistic scale."),
                ("Multi-format, musically-grounded explanations, evaluated against "
                 "music-specific explanation metrics rather than accuracy alone."),
                ("Robust user-tested explanation frameworks for music recommendation remain "
                 "underdeveloped (Shashaani, 2024; Afchar et al., 2022).")][i]
        text(s, ML + 0.28, y + 0.70, 4.92, 0.50, body, size=9.0, color=BODY,
             line_spacing=1.16)

    x2 = 6.42
    label(s, x2, 2.14, 6.2, "Concrete contributions so far")
    contribs = [("An end-to-end pipeline at MPD scale",
                 "1.93M interactions, five models, one protocol, fully offline and "
                 "reproducible."),
                ("A working natural-language explainer",
                 "Generated directly from SHAP attribution vectors; any recommendation can "
                 "be explained."),
                ("A first measurement of SHAP\u2013LIME agreement in music",
                 "Mean \u03c1 = 0.008 across 200 instances \u2014 evidence against assuming "
                 "explainer interchangeability."),
                ("A declared accuracy\u2013explainability baseline",
                 "The ablation design and the current numbers, both reported with their "
                 "confounds stated.")]
    y = 2.46
    for t, b in contribs:
        text(s, x2, y, 0.26, 0.24, "\u25aa", size=9, color=ACCENT, bold=True, check=False)
        text(s, x2 + 0.30, y - 0.02, 5.86, 0.24, t, size=10.6, color=INK, bold=True,
             check=False)
        text(s, x2 + 0.30, y + 0.24, 5.86, 0.52, b, size=9.2, color=BODY, line_spacing=1.16)
        y += 0.90

    notes(s, """
TIMING: 55 s.

"Three grounds for the project, and I can now support them with evidence rather
than intent.

Feasibility is the easy one: a five-model pipeline and a working explanation path
already run end-to-end on real data at realistic scale. That is no longer
predicted, it is demonstrated.

Originality is in the combination. SHAP is not new; LIME is not new; NCF is not
new. What is less explored is joint attribution across a hybrid neural
recommender, measured with music-specific explanation metrics, delivered in more
than one format.

Relevance: the user-tested explanation frameworks that exist for e-commerce and
film do not transfer cleanly to music, and that gap is still open.

And the four concrete contributions on the right are what I would point to as the
deliverable of this stage."
""")
    return page + 1


def s_conclusion(prs, page):
    s = blank(prs)
    bg_gradient(s, DARK_BG, RGBColor(0x1C, 0x20, 0x4E), 35)
    rings(s, 12.2, 6.6, [3.6, 5.0, 6.4], DARK_RING, 0.9)
    text(s, ML, 0.72, 8.0, 0.26, "Conclusion", size=9.4, color=TEAL, bold=True, spc=190,
         caps=True, check=False)
    text(s, ML, 1.04, 10.5, 0.62, "Three things worth remembering", size=30, color=WHITE,
         bold=True, check=False)

    points = [("The system works, and the content branch earns its place.",
               "The hybrid beats NCF on every metric at every K, and the comparison is "
               "attributable because the content branch is the only difference."),
              ("The model comparison is not yet decided.",
               "SVD-MF leads on this cohort, and the likely cause is a five-epoch schedule. "
               "The rerun is the first item on the roadmap, not a footnote."),
              ("Two standard explainers are not interchangeable here.",
               "SHAP and LIME agree at \u03c1 = 0.008 across 200 instances \u2014 the most "
               "consequential result, and the one that changes the user study design.")]
    y = 2.06
    for i, (t, b) in enumerate(points):
        text(s, ML, y - 0.06, 0.60, 0.50, f"0{i+1}", size=17, color=TEAL, bold=True,
             check=False)
        text(s, ML + 0.72, y, 10.9, 0.34, t, size=15.5, color=WHITE, bold=True,
             line_spacing=1.1, check=False)
        text(s, ML + 0.72, y + 0.38, 10.2, 0.56, b, size=11.4, color=DARK_TXT,
             line_spacing=1.26)
        y += 1.30

    hline(s, ML, 6.06, CW, RGBColor(0x2C, 0x31, 0x66), 1.0)
    text(s, ML, 6.20, 10.6, 0.62,
         "What is finished: the pipeline, the baselines, the explanation layer. What is "
         "provisional: the model ranking and the attribution results. What is next: converge "
         "the models, then fix the explanation method, then test it with users.",
         size=11.4, color=WHITE, line_spacing=1.3)

    notes(s, """
TIMING: 40 s. Slow down, do not rush the ending.

"Three things I would like to leave with you.

One, the system works and the content branch earns its place. The hybrid beats NCF
on every metric at every K, and that comparison is attributable.

Two, the model comparison is not yet decided. SVD-MF leads on this cohort, and the
most likely cause is that I trained the neural models for five epochs. That rerun
is the first item on the roadmap.

Three, and this is the finding I would defend hardest: SHAP and LIME are not
interchangeable on this model. A correlation of 0.008 is the absence of
agreement, and it changes what the user study has to measure.

So: finished, provisional, next. I am happy to take questions."
""")
    return page + 1


def build(prs, page):
    divider(prs, "04", "Preliminary Results",
            "Five models on one cohort, global and instance-level attributions, and a "
            "result that changes what the rest of the project has to do.",
            ["Data characteristics", "Offline accuracy",
             "Explainability results", "Accuracy\u2013explainability trade-off"], page)
    page += 1
    page = s_accuracy(prs, page)
    page = s_hybrid(prs, page)
    page = s_svd(prs, page)
    page = s_shap_global(prs, page)
    page = s_instance(prs, page)
    page = s_consistency(prs, page)
    page = s_tradeoff(prs, page)

    divider(prs, "05", "Discussion & Next Steps",
            "What the evidence supports, what it does not, and the work that has to happen "
            "before the dissertation claim can be made.",
            ["What held up", "Limitations by type", "Anticipated outcomes",
             "Plan to submission", "Contributions"], page)
    page += 1
    page = s_discussion(prs, page)
    page = s_limitations(prs, page)
    page = s_outcomes(prs, page)
    page = s_roadmap(prs, page)
    page = s_contributions(prs, page)
    page = s_conclusion(prs, page)
    return page
