"""Section 02 (aims & objectives) and section 03 (methodology)."""
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

from deck_lib import *

ASSETS = "assets"
CHARTS = "charts"


# ---------------------------------------------------------------- aims
def s_aim(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Aims  \u00b7  \u00a72", "One aim, three objectives", page,
           lede="With status as of this submission \u2014 I would rather flag a partial result "
                "than overstate a finished one.")

    shape(s, ML, 2.14, CW, 1.30, fill=ACCENT_LT, line=None, radius=0.05)
    rect(s, ML, 2.14, 0.07, 1.30, fill=ACCENT)
    text(s, ML + 0.34, 2.24, 1.6, 0.24, "AIM", size=8.8, color=ACCENT_DK, bold=True,
         spc=150, check=False)
    text(s, ML + 0.34, 2.50, CW - 0.80, 0.84,
         "Design, implement and evaluate an explainable music recommender system that "
         "balances personalisation and accuracy with transparent, user-interpretable "
         "explanations.", size=15.2, color=INK, line_spacing=1.22)

    objs = [
        ("Objective 1", "Hybrid recommender, benchmarked",
         "Develop a hybrid model combining NCF with content-based acoustic and metadata "
         "features, benchmarked against established accuracy baselines on the "
         "Spotify MPD.",
         "Implemented", TEAL, TEAL_LT, 1.62),
        ("Objective 2", "SHAP and LIME, evaluated",
         "Integrate model-agnostic post-hoc explainers (SHAP, LIME) and rigorously evaluate "
         "their suitability for the music domain \u2014 including attribution agreement.",
         "Implemented \u00b7 surrogate", AMBER, AMBER_LT, 2.28),
        ("Objective 3", "Accuracy\u2013explainability trade-off",
         "Measure the trade-off between accuracy and explainability through systematic "
         "ablation, quantifying the cost of preserving a feature-decomposable architecture.",
         "Complete \u00b7 first pass", AMBER, AMBER_LT, 2.28),
    ]
    for i, (num, title, body, status, col, colbg, pw) in enumerate(objs):
        x = ML + i * 4.13
        shape(s, x, 3.66, 3.83, 2.28, fill=WHITE, line=LINE, radius=0.06)
        text(s, x + 0.26, 3.80, 3.3, 0.24, num, size=8.8, color=col if col != AMBER else AMBER,
             bold=True, spc=130, caps=True, check=False)
        text(s, x + 0.26, 4.04, 3.32, 0.56, title, size=13, color=INK, bold=True,
             line_spacing=1.05)
        text(s, x + 0.26, 4.62, 3.32, 0.92, body, size=9.8, color=BODY, line_spacing=1.16)
        pill(s, x + 0.26, 5.60, pw, 0.29, status, fg=col, bg=colbg, size=7.8)

    text(s, ML, 6.10, CW, 0.30,
         "Objective 3's conclusion is deliberately withheld: the trade-off cannot be called "
         "settled while the neural models are under-trained (Section 4.5).",
         size=10.2, color=MUTED, italic=True, check=False)

    notes(s, """
TIMING: 60 s.

"The aim is one sentence: design, implement and evaluate an explainable music
recommender that balances personalisation and accuracy with explanations a
listener can actually use.

Three objectives, and I want to be honest about the status of each, because the
abstract of a project can hide a lot.

Objective one \u2014 the hybrid model and the baselines \u2014 is implemented. Five
models, full offline evaluation.

Objective two \u2014 SHAP and LIME \u2014 is implemented, but with a deviation I will
explain in the methodology: it runs through a surrogate because the direct
explainer was intractable at this catalogue size.

Objective three \u2014 the trade-off \u2014 has a complete first pass. I am deliberately
withholding the conclusion, and the reason appears in the results: the neural
models are under-trained, which confounds the very comparison this objective
needs."
""")
    return page + 1


# ---------------------------------------------------------------- methodology
def s_pipeline(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Methodology  \u00b7  \u00a73", "The pipeline, end to end", page,
           lede="Five stages, each of which produces an artefact the next stage consumes \u2014 "
                "and the whole path runs offline.")

    stages = [
        ("Data", "Spotify MPD. First 150,000 playlists \u2014 150 of the 1,000 official "
                 "slices \u2014 parsed from the archive."),
        ("Preprocess", "Normalised artist\u2013title join to the catalogue, three-pass "
                       "k-core, z-scoring, 70/10/20 split."),
        ("Models", "Five models: popularity, content cosine, SVD-MF, NCF, and the hybrid "
                   "NCF + content model."),
        ("Explainers", "SHAP (TreeExplainer) and LIME (tabular) applied to a gradient-"
                       "boosting surrogate of the hybrid model."),
        ("Evaluation", "P/R/NDCG/MRR at K \u2208 {5, 10, 20} on a 1,000-user cohort; "
                       "SHAP\u2013LIME consistency on 200 instances."),
    ]
    for i, (t, b) in enumerate(stages):
        x = ML + i * 2.47
        shape(s, x, 2.22, 2.22, 2.26, fill=WHITE, line=LINE, radius=0.06)
        rect(s, x, 2.22, 2.22, 0.05, fill=ACCENT if i < 4 else TEAL)
        text(s, x + 0.22, 2.40, 0.9, 0.22, f"0{i+1}", size=9, color=ACCENT if i < 4 else TEAL,
             bold=True, spc=90, check=False)
        text(s, x + 0.22, 2.64, 1.80, 0.30, t, size=12.6, color=INK, bold=True, check=False)
        text(s, x + 0.22, 2.98, 1.80, 1.36, b, size=9.1, color=BODY, line_spacing=1.16)
        if i < 4:
            arrow(s, x + 2.26, 3.35, x + 2.43, 3.35, MUTED, 1.1)

    label(s, ML, 4.72, 8.0, "Deviations from the approved proposal \u2014 declared, not buried")
    devs = [
        ("Audio features", "Spotify restricted public access to the audio-features "
         "endpoint, so records are matched to a pre-fetched catalogue instead of pulled "
         "live. Same nine dimensions; cross-domain validation deferred."),
        ("SHAP pathway", "DeepExplainer was intractable over the full cohort at 20,042 "
         "items. A gradient-boosting surrogate carries the attribution \u2014 with "
         "consequences discussed in \u00a74.3."),
        ("A fifth baseline", "SVD-MF was added as a classical reference independent of the "
         "neural family. It turned out to be the strongest model, which is itself a finding."),
    ]
    for i, (t, b) in enumerate(devs):
        x = ML + i * 4.13
        shape(s, x, 5.02, 3.83, 1.52, fill=WHITE, line=LINE, radius=0.05)
        rect(s, x, 5.02, 0.05, 1.52, fill=AMBER)
        text(s, x + 0.24, 5.14, 3.4, 0.24, t, size=10.6, color=INK, bold=True, check=False)
        text(s, x + 0.24, 5.40, 3.42, 1.04, b, size=8.9, color=BODY, line_spacing=1.16)

    notes(s, """
TIMING: 60 s.

"Five stages. Data, preprocessing, five models, two explainers, evaluation \u2014
the whole thing runs offline, which matters for reproducibility.

I want to spend my time on the three deviations, because a viva is the wrong
place to discover them later.

One: Spotify closed the public audio-features endpoint, so pulling features for
roughly two million unique tracks was not possible. I match to a pre-fetched
catalogue instead. I keep the same nine acoustic dimensions. What I lose is the
cross-domain validation corpus, and I have deferred that.

Two: SHAP's DeepExplainer over the full evaluation cohort at this catalogue size
was computationally intractable. So attribution currently runs through a
gradient-boosting surrogate. That single decision shapes the whole explainability
result, and I will be explicit about that when we get there.

Three: I added SVD-MF. That was not in the plan. It is a classical reference
independent of the neural family \u2014 and it is the best-performing model, which is
awkward and useful in equal measure."
""")
    return page + 1


def s_data_source(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Methodology  \u00b7  \u00a73.1", "Data source \u2014 and the audio-feature substitution", page,
           lede="A deliberate design decision, driven by an API restriction rather than "
                "convenience.")

    label(s, ML, 2.18, 5.8, "Source and sampling")
    bullets(s, ML, 2.46, 5.85, 2.36, [
        ("Spotify MPD. ", "The official Million Playlist Dataset (Chen et al., 2018); the "
         "first 150,000 playlists \u2014 150 of 1,000 slices \u2014 are parsed for compute "
         "tractability."),
        ("The obstacle. ", "Spotify restricts the public audio-features endpoint, and the "
         "MPD contains roughly two million unique tracks. Bulk per-track retrieval is "
         "infeasible."),
        ("The substitution. ", "Records are matched to a pre-fetched Music Info.csv "
         "catalogue on normalised artist\u2013title pairs \u2014 leading and trailing "
         "whitespace removed, both fields lowercased, then an exact inner join."),
    ], size=10.9, gap=10, tag="datasource")

    x2 = ML + 6.23
    shape(s, x2, 2.18, 5.86, 2.42, fill=AMBER_LT, line=AMBER_LT, radius=0.06)
    rect(s, x2, 2.18, 0.06, 2.42, fill=AMBER)
    text(s, x2 + 0.32, 2.32, 5.2, 0.24, "Consequence, stated plainly", size=9, color=AMBER,
         bold=True, spc=120, caps=True, check=False)
    text(s, x2 + 0.32, 2.62, 5.22, 1.84,
         "The catalogue is now the acoustic-feature source in its own right \u2014 not the "
         "secondary cross-domain validation corpus the proposal described. The nine acoustic "
         "dimensions are preserved (danceability, energy, key, loudness, speechiness, "
         "acousticness, instrumentalness, liveness, valence, tempo), and no live API "
         "dependency remains. Cross-domain validation is deferred to future work.",
         size=10.6, color=BODY, line_spacing=1.24)

    label(s, ML, 4.86, 6.0, "What the substitution costs")
    costs = [("Feature freshness", "Catalogue features are pre-computed, not re-derived."),
             ("Coverage", "Only tracks present in the catalogue survive the join."),
             ("Domain check", "No second corpus to test generalisation against.")]
    for i, (t, b) in enumerate(costs):
        x = ML + i * 4.13
        text(s, x, 5.16, 3.6, 0.24, t, size=10.2, color=ROSE, bold=True, check=False)
        text(s, x, 5.42, 3.66, 0.60, b, size=9.4, color=BODY, line_spacing=1.18)

    hline(s, ML, 6.24, CW, LINE, 0.75)
    text(s, ML, 6.34, CW, 0.34,
         "Mitigation: every downstream number is reported against the matched catalogue, so "
         "the comparison between models is internally valid even where absolute values are "
         "not comparable to the full MPD.", size=9.8, color=MUTED, italic=True,
         line_spacing=1.15)

    notes(s, """
TIMING: 70 s.

"The dataset is the Spotify Million Playlist Dataset \u2014 the official one \u2014 and I
parse the first 150,000 playlists, which is 150 of the thousand slices. That is a
compute decision, not a conceptual one.

Now the part I want to be transparent about. My proposal said I would pull
track-level acoustic features live from the Spotify web API. I could not: the
audio-features endpoint is restricted for public use, and the MPD has roughly
two million unique tracks. Bulk retrieval is not feasible.

So I match records into a pre-fetched catalogue on normalised artist and title
strings, then do an exact inner join. Nine acoustic dimensions, no live
dependency.

The honest consequence is on the right: that catalogue is now my acoustic source,
not a secondary corpus for cross-domain validation. I have lost the second-corpus
check, and I say so in the report.

What I keep is internal validity: every model is evaluated against exactly the
same matched catalogue, so the comparison holds even where the absolute values
are modest."
""")
    return page + 1


def s_preprocess(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Methodology  \u00b7  \u00a73.1", "Preprocessing, in four steps", page,
           lede="Each step is there for a reason that shows up later in the results.")

    steps = [
        ("Three-pass iterative k-core", "Playlists with fewer than 5 matched tracks are "
         "removed; tracks appearing in fewer than 3 distinct playlists are removed. Three "
         "passes, so the removals converge.", "Suppresses near-empty playlists and "
         "singleton tracks"),
        ("Implicit feedback matrix", "A user (playlist) \u00d7 track matrix is built from "
         "playlist co-occurrence \u2014 the only signal MPD actually provides.",
         "No explicit ratings exist"),
        ("Z-score normalisation", "All 9 continuous acoustic features are standardised "
         "before entering the content branch.", "Loudness is in dB; tempo in BPM \u2014 "
         "incomparable raw"),
        ("70 / 10 / 20 split", "Random split rather than temporal: MPD playlists carry no "
         "reliable interaction-level timestamp.", "Stated as a limitation in \u00a75"),
    ]
    for i, (t, b, why) in enumerate(steps):
        y = 2.16 + i * 1.12
        shape(s, ML, y, 6.05, 0.96, fill=WHITE, line=LINE, radius=0.05)
        shape(s, ML + 0.22, y + 0.26, 0.40, 0.40, fill=WASH_2, line=None, radius=0.5,
              kind=MSO_SHAPE.OVAL)
        text(s, ML + 0.22, y + 0.33, 0.40, 0.26, str(i + 1), size=10.4, color=ACCENT,
             bold=True, align=PP_ALIGN.CENTER, check=False)
        text(s, ML + 0.76, y + 0.12, 3.3, 0.26, t, size=11.2, color=INK, bold=True,
             check=False)
        text(s, ML + 0.76, y + 0.38, 4.05, 0.52, b, size=8.9, color=BODY, line_spacing=1.14)
        text(s, ML + 4.86, y + 0.30, 1.10, 0.44, why, size=7.8, color=TEAL, italic=True,
             line_spacing=1.10)

    # right: resulting graph
    x2 = ML + 6.23
    label(s, x2, 2.18, 5.8, "Resulting interaction graph")
    tiles = [("96,827", "playlists (users)"), ("20,042", "tracks (items)"),
             ("1,931,105", "interactions"), ("99.93%", "matrix sparsity")]
    for i, (v, l) in enumerate(tiles):
        x = x2 + (i % 2) * 3.00
        y = 2.48 + (i // 2) * 1.02
        shape(s, x, y, 2.86, 0.92, fill=WHITE, line=LINE, radius=0.06)
        rect(s, x, y, 0.05, 0.92, fill=ACCENT if i < 3 else ROSE)
        text(s, x + 0.20, y + 0.10, 2.5, 0.40, v, size=20, color=INK, bold=True,
             line_spacing=0.95, check=False)
        text(s, x + 0.20, y + 0.56, 2.5, 0.24, l, size=8.6, color=MUTED, caps=True,
             spc=40, check=False)

    # split bar
    label(s, x2, 4.62, 5.6, "Random 70 / 10 / 20 split")
    segs = [(1351773, "Train", RGBColor(0x2E, 0x2A, 0x7A)), (191179, "", ACCENT),
            (388153, "Test", TEAL)]
    tot = sum(x[0] for x in segs)
    bx, bw = x2, 5.86
    left = 0.0
    for v, lab_txt, col in segs:
        w = bw * v / tot
        rect(s, bx + left, 4.92, w - 0.02, 0.34, fill=col)
        if lab_txt:
            text(s, bx + left, 4.99, w - 0.02, 0.22, lab_txt, size=8.4, color=WHITE,
                 bold=True, align=PP_ALIGN.CENTER, caps=True, spc=60, check=False)
        left += w
    legend = [("Train", "1,351,773", "70%", RGBColor(0x2E, 0x2A, 0x7A)),
              ("Validation", "191,179", "10%", ACCENT), ("Test", "388,153", "20%", TEAL)]
    for i, (n, v, p, col) in enumerate(legend):
        x = x2 + i * 1.96
        rect(s, x, 5.38, 0.10, 0.10, fill=col)
        text(s, x + 0.18, 5.33, 1.76, 0.20, n, size=8.4, color=BODY, bold=True, check=False)
        text(s, x + 0.18, 5.52, 1.76, 0.20, f"{v}  \u00b7  {p}", size=8.2, color=MUTED,
             check=False)

    text(s, x2, 5.88, 5.86, 0.56,
         "Top-10 tracks account for only 2.1% of interactions \u2014 the matched catalogue is "
         "not popularity-concentrated. Genre metadata is missing for 28,335 of 50,683 unique "
         "tracks (55.9%).", size=9.2, color=BODY, line_spacing=1.18)

    notes(s, """
TIMING: 75 s.

"Four preprocessing steps, each with a purpose.

The k-core is iterative and runs three passes: drop playlists with fewer than
five matched tracks, drop tracks that appear in fewer than three playlists,
repeat until it converges. This is what stops the evaluation being dominated by
accidental one-track playlists.

The implicit matrix comes from playlist co-occurrence \u2014 that is the only signal
the dataset gives me.

Z-scoring matters more than it looks: loudness is in decibels and tempo is in
BPM. Without standardisation the content branch is dominated by whichever
feature has the largest raw range.

And the split is random, not temporal. I want to address this before you ask:
MPD does not give a reliable interaction-level timestamp, so a temporal split
would be arbitrary. The cost is that I do not model drift or novelty. I list it
as a limitation.

The result on the right: 96,827 playlists, 20,042 tracks, 1.93 million
interactions, 99.93% sparse. That sparsity figure is why precision at ten looks
small later \u2014 it is expected in this regime.

Also worth noting now: 55.9% of unique tracks have no genre metadata, which is
why the knowledge-graph explanation path is a stretch goal rather than a
delivered component."
""")
    return page + 1


def s_catalogue(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Methodology  \u00b7  \u00a74.1", "What the matched catalogue actually contains", page,
           lede="Genre and release-year composition, and why it constrains what I can claim.")

    picture(s, f"{ASSETS}/fig1_genre_year.png", ML, 2.22, w=7.75,
            caption="Figure 1  \u00b7  Genre distribution (top 12) and release-year distribution "
                    "of the matched catalogue.", caption_size=8.8)

    x2 = ML + 8.40
    bullets(s, x2, 2.28, 3.68, 2.70, [
        ("Two genres dominate. ", "Rock and Electronic account for the bulk of the top-12 "
         "distribution; the remaining ten form a long tail."),
        ("The catalogue is dated. ", "Release years peak sharply between roughly 2005 and "
         "2010 and thin out towards both the 1960s and the 2020s."),
        ("Both are artefacts. ", "The match is to a catalogue, not to the full history of "
         "recorded music."),
    ], size=9.8, gap=9, tag="catalogue")

    # implications
    label(s, ML, 5.38, 6.0, "What this means for the project")
    imps = [("For modelling", "Popularity and recency priors are absorbed into the matched "
             "catalogue. Rankings between models remain fair; absolute scores are not "
             "generalisable.", TEAL),
            ("For validity", "Replication on the full MPD or a second catalogue is the "
             "correct robustness check, and is listed as external-validity work.", ROSE)]
    for i, (t, b, c) in enumerate(imps):
        x = ML + i * 4.13
        shape(s, x, 5.66, 3.83, 1.02, fill=WASH, line=None, radius=0.05)
        rect(s, x, 5.66, 0.05, 1.02, fill=c)
        text(s, x + 0.24, 5.74, 3.4, 0.22, t, size=9.4, color=c, bold=True,
             spc=90, caps=True, check=False)
        text(s, x + 0.24, 5.98, 3.42, 0.62, b, size=8.8, color=BODY, line_spacing=1.14)

    notes(s, """
TIMING: 55 s.

"Two things to read off this figure.

Genres are concentrated: Rock and Electronic dominate, then a long tail. And
release years peak sharply around 2005 to 2010 \u2014 the catalogue over-represents
that era relative to the whole history of recorded music.

Neither of those is a property of music. Both are properties of my catalogue, and
I would rather name them than have them found.

What it costs: popularity and recency priors are baked in, so my absolute numbers
describe this catalogue. What it does not cost: the ranking between models, which
is the basis of every claim I make in the results."
""")
    return page + 1


def s_acoustic(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Methodology  \u00b7  \u00a74.1", "The acoustic feature space is skewed \u2014 and collinear", page,
           lede="This is not a detail. It is the most likely explanation for the SHAP\u2013LIME "
                "instability reported later.")

    picture(s, f"{ASSETS}/fig2_acoustic_dists.png", ML, 2.12, h=4.42,
            w=None, caption=None, caption_size=8.6)
    text(s, ML, 6.62, 6.0, 0.22,
         "Figure 2  \u00b7  Distributions of the nine acoustic features (matched catalogue).",
         size=8.4, color=MUTED, check=False)

    x2 = 6.98
    bullets(s, x2, 2.16, 5.72, 1.62, [
        ("Heavy skew, not normality. ", "Speechiness, acousticness and instrumentalness pile "
         "up near zero with long right tails; energy and loudness skew high."),
        ("Closer to symmetric. ", "Danceability, valence and tempo are roughly unimodal."),
    ], size=9.9, gap=8, tag="acoustic")

    label(s, x2, 3.86, 5.6, "Pairwise correlations  |r| \u2265 0.4")
    table(s, x2, 4.14, 5.72,
          [["Feature pair", "r"],
           ["Energy \u2013 Loudness", "+0.78"],
           ["Energy \u2013 Acousticness", "\u22120.73"],
           ["Acousticness \u2013 Loudness", "\u22120.61"],
           ["Danceability \u2013 Valence", "+0.54"]],
          col_w=[3.96, 1.76], row_h=0.32, header_h=0.32, font_size=10, header_size=8.6,
          aligns=["l", "r"], rule_color="FFFFFF")

    shape(s, x2, 5.96, 5.72, 0.86, fill=AMBER_LT, line=None, radius=0.05)
    rect(s, x2, 5.96, 0.05, 0.86, fill=AMBER)
    text(s, x2 + 0.24, 6.06, 5.30, 0.68,
         "Attribution methods redistribute credit among correlated features. Both SHAP and "
         "LIME are known to do this \u2014 so \u00a74.3's disagreement has a plausible mechanism "
         "before it has a cause.", size=9.4, color=BODY, line_spacing=1.16)

    notes(s, """
TIMING: 60 s.

"Nine acoustic features, and the shapes matter.

Three of them \u2014 speechiness, acousticness, instrumentalness \u2014 are effectively
zero-inflated with long right tails. Energy and loudness skew high. Only
danceability, valence and tempo are near-symmetric.

Now the correlation table, because this is the setup for the most important
result in the deck. Energy and loudness correlate at 0.78 \u2014 unsurprising, loud
music tends to be high-energy. Energy and acousticness at minus 0.73.

Both SHAP and LIME attribute credit among features, and when features are
strongly correlated, that credit can be split or swapped between them almost
arbitrarily. So when I show you a near-zero agreement between the two methods in
a moment, the mechanism is already on the table. What I cannot yet do is say how
much of the disagreement is collinearity and how much is surrogate fidelity."
""")
    return page + 1


def s_architecture(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Methodology  \u00b7  \u00a73.2", "Hybrid architecture \u2014 late fusion, by design", page,
           lede="Separability is the architectural choice that makes feature-level attribution "
                "possible at all.")

    # inputs
    dbox(s, ML, 2.52, 1.72, 0.60, "Playlist ID", fill=WASH, border=LINE, title_size=10.4)
    dbox(s, ML, 3.30, 1.72, 0.60, "Track ID", fill=WASH, border=LINE, title_size=10.4)
    dbox(s, ML, 4.62, 1.72, 0.86, "9 acoustic features", "z-scored", fill=TEAL_LT,
         border=TEAL_LT, title_size=9.8, sub_size=8.2, accent=TEAL)

    # embedding
    dbox(s, 2.82, 2.52, 2.06, 1.38, "Shared embeddings", "d = 32", fill=WHITE, border=ACCENT,
         title_size=10.8, sub_size=8.6, accent=ACCENT, dashed=False)

    # branches
    dbox(s, 5.36, 2.36, 2.34, 0.82, "GMF", "element-wise product", fill=WHITE, border=LINE,
         title_size=11, sub_size=8.2)
    dbox(s, 5.36, 3.40, 2.34, 0.82, "MLP", "6 \u2192 32 \u2192 16 \u00b7 ReLU \u00b7 drop 0.3",
         fill=WHITE, border=LINE, title_size=11, sub_size=8.2)
    dbox(s, 5.36, 4.62, 2.34, 0.86, "Content MLP", "9 \u2192 32 \u2192 16", fill=TEAL_LT,
         border=TEAL_LT, title_size=10.4, sub_size=8.2, accent=TEAL)

    # fusion
    dbox(s, 8.22, 3.30, 1.48, 1.24, "Concat", fill=WASH_2, border=LINE, title_size=10.6)
    dbox(s, 10.20, 3.30, 2.50, 0.72, "Linear layer", fill=WHITE, border=ACCENT, title_size=10.6,
         accent=ACCENT)
    dbox(s, 10.20, 4.22, 2.50, 0.62, "score  \u0177 \u2208 (0,1)", fill=ACCENT_LT,
         border=ACCENT, title_size=9.6)

    # arrows
    arrow(s, 2.38, 2.82, 2.80, 3.02, MUTED, 1.1)
    arrow(s, 2.38, 3.60, 2.80, 3.42, MUTED, 1.1)
    arrow(s, 4.90, 2.96, 5.34, 2.82, MUTED, 1.1)
    arrow(s, 4.90, 3.48, 5.34, 3.74, MUTED, 1.1)
    arrow(s, 2.38, 5.05, 5.34, 5.05, TEAL, 1.1)
    arrow(s, 7.72, 2.78, 8.20, 3.62, MUTED, 1.1)
    arrow(s, 7.72, 3.82, 8.20, 3.82, MUTED, 1.1)
    arrow(s, 7.72, 5.02, 8.20, 4.24, TEAL, 1.1)
    arrow(s, 9.72, 3.92, 10.18, 3.72, MUTED, 1.1)
    arrow(s, 11.45, 4.04, 11.45, 4.20, MUTED, 1.1)

    label(s, ML, 5.62, 5.0, "Read as three parallel views of the same pair")
    text(s, ML, 5.90, 11.9, 0.56,
         "GMF captures linear interaction, the MLP captures non-linear interaction, and the "
         "content branch sees the acoustic properties of the track. Their outputs are "
         "concatenated and scored \u2014 so the content contribution stays separable from the "
         "collaborative one, which is what allows a feature-level explanation to exist.",
         size=10.6, color=BODY, line_spacing=1.22)

    pills = ["\u2248 7.49M parameters", "Adam \u00b7 lr 1e-3 \u00b7 wd 1e-5",
             "BCE \u00b7 4 negatives per positive", "5 epochs \u00b7 PyTorch"]
    x = ML
    for p in pills:
        w = 0.078 * len(p) + 0.30
        pill(s, x, 6.52, w, 0.29, p, fg=MUTED, bg=WASH_2, size=8.0)
        x += w + 0.16

    notes(s, """
TIMING: 80 s.

"This is the model, and there is one design decision here that everything else
depends on.

Two collaborative views of the user\u2013item pair: GMF, which is a generalised matrix
factorisation \u2014 effectively the linear interaction \u2014 and an MLP over the
concatenated embeddings, which captures non-linear interaction. They share a
32-dimensional embedding space, which is the NCF design from He and colleagues.

Then a third branch that only looks at the nine acoustic features, through a
two-layer network.

All three are concatenated and passed through a linear scoring layer.

The word I want you to hold onto is 'late'. I fused at the output rather than
fusing the representations early. Early fusion would probably be marginally
stronger, and it would destroy the thing I need: a separable content
contribution. That separability is what makes feature-level attribution possible
in the first place \u2014 and it is exactly the design choice Objective 3 exists to
test the cost of."
""")
    return page + 1


def s_baselines(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Methodology  \u00b7  \u00a73.2", "Five models, one protocol", page,
           lede="The comparison set spans non-personalised, content-only, classical "
                "collaborative and neural families.")

    table(s, ML, 2.14, CW,
          [["Model", "Family", "Role in the study"],
           ["Popularity", "Non-personalised", "Lower-bound reference \u2014 what a "
            "non-personalised system achieves"],
           ["Content-based (cosine)", "Content only", "The acoustic signal in isolation, "
            "with no collaborative information"],
           ["SVD-MF", "Classical collaborative", "Classical reference independent of the "
            "neural family \u2014 added beyond the proposal"],
           ["NCF", "Neural collaborative", "Ablation reference: the hybrid minus content"],
           ["Hybrid NCF + Content", "Neural hybrid", "Proposed model"]],
          col_w=[3.30, 3.30, 5.49], row_h=0.44, header_h=0.40, font_size=10.6,
          header_size=8.8, first_bold=True, rule_color="FFFFFF",
          row_fills={5: ACCENT_LT})

    card(s, ML, 4.86, 5.86, 1.84, title="Training configuration", body=None,
         title_size=12.6, pad=0.26)
    bullets(s, ML + 0.26, 5.46, 5.34, 1.18, [
        ("Loss  ", "binary cross-entropy over implicit-feedback pairs."),
        ("Negatives  ", "4 uniform negatives per positive; estimated false-negative rate "
                        "\u2248 0.07% at 20,042 items."),
        ("Optimiser  ", "Adam, lr 1e-3, weight decay 1e-5, 5 epochs, PyTorch."),
    ], size=9.5, gap=6, bullet_color=ACCENT, glyph_size=5.2, indent=0.18)

    x2 = ML + 6.23
    shape(s, x2, 4.86, 5.86, 1.84, fill=AMBER_LT, line=AMBER_LT, radius=0.06)
    rect(s, x2, 4.86, 0.06, 1.84, fill=AMBER)
    text(s, x2 + 0.30, 4.98, 5.2, 0.24, "What is deliberately not tuned yet", size=9,
         color=AMBER, bold=True, spc=120, caps=True, check=False)
    text(s, x2 + 0.30, 5.26, 5.28, 1.34,
         "Hyperparameters are manually set. A 50-trial Optuna search was scoped but has not "
         "been run against the full model set. Combined with a five-epoch schedule, this is "
         "the single largest caveat on the model comparison \u2014 and it is the first item on "
         "the roadmap, not a footnote.",
         size=10.4, color=BODY, line_spacing=1.22)

    notes(s, """
TIMING: 60 s.

"Five models, one protocol.

Popularity is the floor \u2014 what you get with no personalisation. Content-based
cosine is the acoustic signal with no collaborative information. SVD-MF is the
classical reference, and I added it after the proposal because I wanted a
collaborative model from outside the neural family.

Then NCF, and the hybrid. That pairing is the ablation for Objective 1: the
hybrid is NCF plus content, so the difference between the two rows is the content
branch's contribution, all else held equal.

Training: BCE over implicit pairs, four uniform negatives per positive. At this
catalogue size I can bound the false-negative rate at about 0.07%, which is why
uniform sampling is defensible here.

And the honest caveat on the right. Five epochs, manual hyperparameters. The
Optuna search is scoped and not run. That is the biggest threat to the model
comparison and I am not going to pretend otherwise."
""")
    return page + 1


def s_explainers(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Methodology  \u00b7  \u00a73.3", "How the explanation layer is wired", page,
           lede="A deviation with real consequences \u2014 so here is the pathway, and what it "
                "buys and costs.")

    boxes = [
        (ML, 1.94, "Hybrid model", "the thing we want to explain", WHITE, LINE, None),
        (ML + 2.62, 1.94, "DeepExplainer", "intractable over the cohort", WHITE, ROSE, None),
        (ML + 5.24, 1.94, "GBR surrogate", "9 features \u00b7 3,000 instances", AMBER_LT, AMBER_LT, AMBER),
        (ML + 7.86, 1.94, "SHAP  +  LIME", "TreeExplainer \u00b7 tabular", ACCENT_LT, ACCENT_LT, ACCENT),
    ]
    for (x, y, t, sub, fill, border, acc) in boxes:
        dbox(s, x, y, 2.32, 0.94, t, sub, fill=fill, border=border, title_size=10.8,
             sub_size=8.2, accent=acc)
    arrow(s, ML + 2.36, 2.41, ML + 2.58, 2.41, MUTED, 1.1)
    arrow(s, ML + 2.36 + 2.62, 2.41, ML + 2.58 + 2.62, 2.41, ROSE, 1.1)
    arrow(s, ML + 2.36 + 5.24, 2.41, ML + 2.58 + 5.24, 2.41, MUTED, 1.1)
    text(s, ML + 2.70, 2.92, 2.2, 0.24, "not used: too slow", size=8, color=ROSE,
         italic=True, check=False)
    text(s, ML + 5.32, 2.92, 2.2, 0.24, "held-out R\u00b2 = 0.105", size=8, color=AMBER,
         bold=True, check=False)

    # formats
    label(s, ML, 3.36, 5.6, "Explanation formats")
    fmts = [("Feature-ranked text", "A working natural-language generator, produced directly "
             "from an instance's top SHAP attributions.", TEAL, "built"),
            ("Visual attribution", "Top-5 SHAP bar charts plus the global beeswarm summary.",
             TEAL, "built"),
            ("Knowledge-graph paths", "Artist / genre / label pathways through the "
             "catalogue.", MUTED, "not attempted")]
    for i, (t, b, c, st) in enumerate(fmts):
        y = 3.62 + i * 0.76
        shape(s, ML, y, 5.86, 0.66, fill=WHITE, line=LINE, radius=0.05)
        rect(s, ML, y, 0.05, 0.66, fill=c)
        text(s, ML + 0.24, y + 0.09, 2.6, 0.24, t, size=10.2, color=INK, bold=True,
             check=False)
        text(s, ML + 0.24, y + 0.34, 3.9, 0.28, b, size=8.5, color=BODY, line_spacing=1.12)
        pill(s, ML + 4.42, y + 0.19, 1.22, 0.27, st, fg=c if c != MUTED else MUTED,
             bg=TEAL_LT if c == TEAL else WASH_2, size=7.6)

    # why R2 matters
    x2 = ML + 6.23
    shape(s, x2, 3.36, 5.86, 2.44, fill=INK, line=None, radius=0.06)
    text(s, x2 + 0.32, 3.50, 5.2, 0.24, "The R\u00b2 is a result, not a caveat", size=9,
         color=TEAL, bold=True, spc=120, caps=True, check=False)
    text(s, x2 + 0.32, 3.80, 5.24, 1.86,
         "A surrogate that explains only 10.5% of the hybrid model's score is telling us "
         "something: acoustic content alone accounts for a small share of the prediction, "
         "and the remainder lives in latent collaborative signal that a content-only "
         "surrogate cannot see. That has a direct consequence for Objective 2 \u2014 the "
         "explanations currently describe a content view of the model, not the model.",
         size=10.4, color=RGBColor(0xD5, 0xD8, 0xE8), line_spacing=1.24)

    text(s, ML, 5.94, CW, 0.30,
         "Both built formats are domain-grounded: they speak in instrumentalness, energy and "
         "danceability rather than in embedding dimensions.",
         size=10.2, color=MUTED, italic=True, check=False)

    notes(s, """
TIMING: 70 s.

"Here is the pathway, and I want to draw attention to the second box, because it
is the one that did not work.

The plan was SHAP's DeepExplainer directly on the hybrid network. Over the
evaluation cohort at 20,042 items that is not tractable in the compute I had.

So I train a gradient-boosting surrogate to reproduce the hybrid model's score
from the nine acoustic features, on 3,000 sampled test instances, and run both
SHAP's TreeExplainer and LIME's tabular explainer against that surrogate.

Held-out R-squared is 0.105.

Now, I could present that as a limitation and move on. I think it is better read
as a result: acoustic content explains about a tenth of the variance in the
model's score. The rest is collaborative signal that a content-only surrogate
structurally cannot see.

Which means the explanations I am about to show you are a content view of the
model, not the whole model. That is the honest framing, and it is the first
thing I fix next.

Of the three explanation formats proposed, two are built \u2014 the text generator
and the visual attributions. The knowledge-graph path is not attempted; genre
metadata is missing for 55.9% of tracks, which is part of why."
""")
    return page + 1


def s_evaluation(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Methodology  \u00b7  \u00a73.4", "Evaluation protocol", page,
           lede="Two independent evaluation tracks: does the ranking work, and does the "
                "explanation hold up.")

    # accuracy card
    shape(s, ML, 2.14, 5.86, 2.72, fill=WHITE, line=LINE, radius=0.06)
    rect(s, ML, 2.14, 5.86, 0.05, fill=ACCENT)
    text(s, ML + 0.28, 2.30, 5.2, 0.26, "Offline accuracy", size=13, color=INK, bold=True,
         check=False)
    bullets(s, ML + 0.28, 2.66, 5.30, 2.06, [
        ("Metrics  ", "Precision@K, Recall@K, NDCG@K and MRR at K \u2208 {5, 10, 20}."),
        ("The obstacle  ", "a dense users \u00d7 items matrix is 96,827 \u00d7 20,042 "
                           "\u2248 1.94 billion cells."),
        ("The cohort  ", "scores are materialised for 1,000 randomly sampled users drawn "
                         "from the 87,663 test users with at least one held-out "
                         "interaction, against all 20,042 items."),
    ], size=9.5, gap=6, bullet_color=ACCENT, glyph_size=5.2, indent=0.18)

    # explainability card
    x2 = ML + 6.23
    shape(s, x2, 2.14, 5.86, 2.72, fill=WHITE, line=LINE, radius=0.06)
    rect(s, x2, 2.14, 5.86, 0.05, fill=TEAL)
    text(s, x2 + 0.28, 2.30, 5.2, 0.26, "Explanation quality", size=13, color=INK, bold=True,
         check=False)
    expl = [("Consistency", "Spearman \u03c1 between SHAP and LIME importance orderings, "
             "200 test instances", "computed", TEAL),
            ("Fidelity", "SHAP rank against perturbation sensitivity", "scoped", AMBER),
            ("Coverage", "share of top-K recommendations with a non-trivial explanation",
             "scoped", AMBER)]
    for i, (t, b, st, c) in enumerate(expl):
        y = 2.68 + i * 0.70
        text(s, x2 + 0.28, y, 4.0, 0.22, t, size=10.2, color=INK, bold=True, check=False)
        text(s, x2 + 0.28, y + 0.22, 4.24, 0.40, b, size=8.6, color=BODY, line_spacing=1.12)
        pill(s, x2 + 4.66, y + 0.04, 0.90, 0.26, st, fg=c, bg=TEAL_LT if c == TEAL else AMBER_LT,
             size=7.4)

    # rationale
    shape(s, ML, 5.06, CW, 1.04, fill=WASH, line=None, radius=0.05)
    rect(s, ML, 5.06, 0.06, 1.04, fill=ACCENT)
    text(s, ML + 0.30, 5.16, 4.2, 0.24, "Why sample the cohort", size=9,
         color=ACCENT_DK, bold=True, spc=110, caps=True, check=False)
    text(s, ML + 0.30, 5.44, CW - 0.60, 0.60,
         "Ranking metrics depend only on the per-user ordering of scores. Materialising 1.94 "
         "billion scores would cost roughly 15 GB at float64 and change no ranking \u2014 so "
         "the cohort is sampled once, fixed, and reused by every model. The same 1,000 users "
         "for all five, with the same held-out interactions.",
         size=9.8, color=BODY, line_spacing=1.20)

    notes(s, """
TIMING: 60 s.

"Two evaluation tracks, because accuracy does not tell you whether an explanation
is good.

Accuracy: precision, recall, NDCG and MRR at five, ten and twenty.

The problem is scale. A dense score matrix is 96,827 users by 20,042 items \u2014
about 1.94 billion cells. So I materialise scores for a fixed cohort of a
thousand users, sampled at random from the 87,663 test users who have at least
one held-out interaction, and score them against the full item set.

That is defensible because ranking metrics only depend on per-user ordering. The
same thousand users, the same held-out interactions, for all five models \u2014 so
the comparison is like-for-like.

Explanation quality: three metrics. Consistency is computed \u2014 the Spearman
correlation between SHAP and LIME rankings, across 200 instances. Fidelity and
coverage are implemented in design and scoped but not yet computed. I would
rather say that than invent numbers."
""")
    return page + 1


def build(prs, page):
    divider(prs, "02", "Aims & Objectives",
            "What the project set out to do \u2014 and an honest status line for each "
            "objective at the point of submission.",
            ["The aim", "Objective 1 \u00b7 hybrid model",
             "Objective 2 \u00b7 SHAP and LIME", "Objective 3 \u00b7 trade-off"], page)
    page += 1
    page = s_aim(prs, page)

    divider(prs, "03", "Research Description & Methodology",
            "Data, five models, two explainers, and a protocol designed so that the "
            "comparisons hold even where the absolute numbers are modest.",
            ["Dataset and substitution", "Preprocessing",
             "Hybrid architecture", "Explainability integration",
             "Evaluation protocol"], page)
    page += 1
    page = s_pipeline(prs, page)
    page = s_data_source(prs, page)
    page = s_preprocess(prs, page)
    page = s_catalogue(prs, page)
    page = s_acoustic(prs, page)
    page = s_architecture(prs, page)
    page = s_baselines(prs, page)
    page = s_explainers(prs, page)
    page = s_evaluation(prs, page)
    return page
