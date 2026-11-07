"""Backup slides: references, likely questions, full results table."""
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

from deck_lib import *
from deck_lib import run_text

CHARTS = "charts"

REFS = [
    "Afchar, D., Melchiorre, A.B., Schedl, M., Hennequin, R., Epure, E.V. and Moussallam, M. "
    "(2022) \u2018Explainability in music recommender systems\u2019, AI Magazine, 43(2), "
    "pp. 190\u2013208.",
    "Alvarez-Melis, D. and Jaakkola, T.S. (2018) \u2018On the robustness of interpretability "
    "methods\u2019, ICML Workshop on Human Interpretability in Machine Learning.",
    "Arrieta, A.B. et al. (2020) \u2018Explainable Artificial Intelligence (XAI): concepts, "
    "taxonomies, opportunities and challenges toward responsible AI\u2019, Information Fusion, "
    "58, pp. 82\u2013115.",
    "Celma, O. (2010) Music Recommendation and Discovery: The Long Tail, Long Fail, and Long "
    "Play in the Digital Music Space. Berlin: Springer.",
    "Chen, C.-W., Lamere, P., Schedl, M. and Zamani, H. (2018) \u2018RecSys Challenge 2018: "
    "automatic music playlist continuation\u2019, Proceedings of the 12th ACM Conference on "
    "Recommender Systems, pp. 527\u2013528.",
    "Ferwerda, B., Schedl, M. and Tkalcic, M. (2015) \u2018Personality and emotional states: "
    "understanding users\u2019 music listening needs\u2019, UMAP 2015 Extended Proceedings.",
    "He, X., Liao, L., Zhang, H., Nie, L., Hu, X. and Chua, T.-S. (2017) \u2018Neural "
    "collaborative filtering\u2019, Proceedings of the 26th International Conference on World "
    "Wide Web, pp. 173\u2013182.",
    "Jain, S. and Wallace, B.C. (2019) \u2018Attention is not explanation\u2019, Proceedings of "
    "NAACL-HLT 2019, Volume 1, pp. 3543\u20133556.",
    "Knijnenburg, B.P., Willemsen, M.C., Gantner, Z., Soncu, H. and Newell, C. (2012) "
    "\u2018Explaining the user experience of recommender systems\u2019, User Modeling and "
    "User-Adapted Interaction, 22(4\u20135), pp. 441\u2013504.",
    "Koren, Y., Bell, R. and Volinsky, C. (2009) \u2018Matrix factorization techniques for "
    "recommender systems\u2019, Computer, 42(8), pp. 30\u201337.",
    "Lipton, Z.C. (2018) \u2018The mythos of model interpretability\u2019, Communications of the "
    "ACM, 61(10), pp. 36\u201343.",
    "Lundberg, S.M. and Lee, S.-I. (2017) \u2018A unified approach to interpreting model "
    "predictions\u2019, Advances in Neural Information Processing Systems, 30, "
    "pp. 4765\u20134774.",
    "Melchiorre, A.B., Rekabsaz, N., Ganh\u00f6r, C. and Schedl, M. (2022) \u2018ProtoMF: "
    "prototype-based matrix factorization for effective and explainable recommendations\u2019, "
    "Proceedings of the 16th ACM Conference on Recommender Systems, pp. 246\u2013256.",
    "Oramas, S., Ostuni, V.C., Di Noia, T., Serra, X. and Di Sciascio, E. (2017) \u2018Sound and "
    "music recommendation with knowledge graphs\u2019, ACM Transactions on Intelligent Systems "
    "and Technology, 8(2), pp. 21.1\u201321.21.",
    "Ribeiro, M.T., Singh, S. and Guestrin, C. (2016) \u2018\u201cWhy should I trust you?\u201d: "
    "explaining the predictions of any classifier\u2019, Proceedings of the 22nd ACM SIGKDD, "
    "pp. 1135\u20131144.",
    "Schedl, M., Zamani, H., Chen, C.-W., Deldjoo, Y. and Elahi, M. (2018) \u2018Current "
    "challenges and visions in music recommender systems research\u2019, International Journal "
    "of Multimedia Information Retrieval, 7(2), pp. 95\u2013116.",
    "Shashaani, S. (2024) \u2018Explainability in music recommender system\u2019, Proceedings of "
    "the 18th ACM Conference on Recommender Systems, pp. 1395\u20131401.",
    "Tintarev, N. and Masthoff, J. (2007) \u2018A survey of explanations in recommender "
    "systems\u2019, Proceedings of the 2007 IEEE 23rd International Conference on Data "
    "Engineering Workshop, pp. 801\u2013810.",
    "Tintarev, N. and Masthoff, J. (2015) \u2018Explaining recommendations: design and "
    "evaluation\u2019, in Ricci, F., Rokach, L. and Shapira, B. (eds) Recommender Systems "
    "Handbook. 2nd edn. Boston, MA: Springer US, pp. 353\u2013382.",
    "van den Oord, A., Dieleman, S. and Schrauwen, B. (2013) \u2018Deep content-based music "
    "recommendation\u2019, Advances in Neural Information Processing Systems, 26, "
    "pp. 2643\u20132651.",
    "Wang, H., Zhao, M., Xie, X., Li, W. and Guo, M. (2019) \u2018Knowledge graph convolutional "
    "networks for recommender systems\u2019, Proceedings of the 2019 World Wide Web Conference, "
    "pp. 3307\u20133313.",
    "Zhang, Y. and Chen, X. (2020) \u2018Explainable recommendation: a survey and new "
    "perspectives\u2019, Foundations and Trends in Information Retrieval, 14(1), pp. 1\u2013101.",
    "Zhang, Y., Lai, G., Zhang, M., Zhang, Y., Liu, Y. and Ma, S. (2014) \u2018Explicit factor "
    "models for explainable recommendation based on phrase-level sentiment analysis\u2019, "
    "Proceedings of SIGIR 2014, pp. 83\u201392.",
    "Zhou, F., Ji, Y. and Jiao, R.J. (2013) \u2018Affective and cognitive design for mass "
    "personalization: status and prospect\u2019, Journal of Intelligent Manufacturing, 24(5), "
    "pp. 1047\u20131069.",
]


def _ref_column(s, x, y, w, h, entries, size=8.4, gap=6):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    marL = int(Inches(0.24))
    for i, e in enumerate(entries):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = 1.06
        p.space_after = Pt(gap)
        pPr = p._p.get_or_add_pPr()
        pPr.set("marL", str(marL))
        pPr.set("indent", str(-marL))
        run_text(p, e, size, BODY, False, False, FONT)


def s_references(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "References", "References", page,
           lede="Twenty-four sources, Harvard style, as in the report.")
    total = sum(len(e) for e in REFS)
    cols, acc, cur = [], 0, []
    for e in REFS:
        cur.append(e)
        acc += len(e)
        if acc >= total / 3 * (len(cols) + 1) and len(cols) < 2:
            cols.append(cur)
            cur = []
    cols.append(cur)
    for i, chunk in enumerate(cols):
        _ref_column(s, ML + i * 3.99, 2.06, 3.74, 4.64, chunk, size=8.0, gap=5)

    notes(s, """
Backup slide. Do not present it. If a citation is challenged, give the author and
year, then describe the method rather than the title.
""")
    return page + 1


QA = [
    ("SVD-MF beats both neural models. Why should I trust the hybrid result?",
     "I would not ask you to trust it as a final ranking. Five epochs, and neither loss curve "
     "has plateaued, while SVD-MF is closed-form. What Objective 1 needs \u2014 hybrid versus "
     "NCF \u2014 is like-for-like, because the schedule is identical. The absolute ranking is "
     "provisional, and the rerun is the first item on the plan."),
    ("Your surrogate has R\u00b2 = 0.105. Aren't you explaining the wrong model?",
     "Partly, yes, and it is stated rather than hidden. The gap is informative: acoustic "
     "content accounts for about a tenth of the variance, so the rest is collaborative signal "
     "a content-only surrogate cannot see. So the explanations describe a content view of the "
     "model. It is also candidate cause one for the SHAP\u2013LIME disagreement, which is why a "
     "higher-fidelity surrogate is the next test."),
    ("Why a random split rather than temporal \u2014 doesn't that leak information?",
     "The MPD has no reliable interaction-level timestamps, so a temporal split would be "
     "arbitrary rather than principled. The cost is that drift and novelty are not modelled, "
     "which I list under external and conclusion validity. It does not affect the relative "
     "ranking of models, which is what the claims rest on."),
    ("Is \u03c1 \u2248 0 just noise from 200 instances?",
     "No. Noise around a genuine agreement would centre above zero. What I observe is a mean "
     "indistinguishable from zero (0.008) with SD 0.359, which is the absence of systematic "
     "agreement rather than agreement plus error. I also report the per-instance distribution "
     "so it is visible that this is not driven by a few outliers."),
]


def s_questions(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Backup", "Four questions I expect", page,
           lede="Prepared answers; the full set is in the speaker notes.")

    y = 2.06
    for i, (q, a) in enumerate(QA):
        shape(s, ML, y, CW, 1.10, fill=WHITE, line=LINE, radius=0.05)
        rect(s, ML, y, 0.05, 1.10, fill=ACCENT)
        text(s, ML + 0.26, y + 0.13, 0.42, 0.24, f"Q{i+1}", size=8.6, color=ACCENT,
             bold=True, spc=60, check=False)
        text(s, ML + 0.76, y + 0.10, CW - 1.06, 0.28, q, size=11.2, color=INK, bold=True,
             check=False)
        text(s, ML + 0.76, y + 0.40, CW - 1.06, 0.64, a, size=9.2, color=BODY,
             line_spacing=1.16)
        y += 1.20

    notes(s, """
Backup slide, for answers you have rehearsed.

Also be ready for these, which are not on the slide:

"Precision@10 of 0.018 looks unusable." It is not deployable, and I do not claim
it is. At 99.93% sparsity with four sampled negatives per positive, values in the
hundredths are expected in offline evaluation; the study compares models under
one protocol rather than claiming production quality.

"What is new, if SHAP, LIME and NCF all exist?" The combination and the
measurement: joint attribution across a hybrid recommender, the consistency
measurement in music, and a music-specific evaluation design.

"Why only 150,000 playlists?" Compute. The 150-slice graph is already 1.93
million edges; scaling is a rerun of the same pipeline, not a redesign.

"Where is fairness?" Not modelled directly, and I say so. Attribution offers a
diagnostic: if a popularity proxy dominates, the recommendation is
popularity-driven. That is planned analysis, not a delivered result.
""")
    return page + 1


def s_numbers(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Backup", "Reported numbers", page,
           lede="The accuracy table and the global attribution ranking, for reference.")

    label(s, ML, 2.06, 6.0, "Offline accuracy at K = 10")
    table(s, ML, 2.34, 6.10,
          [["Model", "P@10", "R@10", "NDCG@10", "MRR"],
           ["Popularity", "0.0104", "0.0349", "0.0239", "0.0458"],
           ["Content-based", "0.0014", "0.0037", "0.0027", "0.0095"],
           ["SVD-MF", "0.0424", "0.1225", "0.0769", "0.1121"],
           ["NCF", "0.0173", "0.0453", "0.0342", "0.0736"],
           ["Hybrid", "0.0184", "0.0538", "0.0384", "0.0752"]],
          col_w=[1.72, 1.10, 1.10, 1.16, 1.02], row_h=0.38, header_h=0.36,
          font_size=10, header_size=8.6, aligns=["l", "r", "r", "r", "r"],
          first_bold=True, rule_color="FFFFFF", row_fills={3: ACCENT_LT, 5: AMBER_LT})

    label(s, ML, 4.90, 5.8, "Derived comparisons used in the talk")
    derived = [("Hybrid \u2212 NCF", "NDCG@10 +0.0042 (+12.3% relative)"),
               ("SVD-MF \u2212 Hybrid", "NDCG@10 +0.0385 (2.0\u00d7 the hybrid)"),
               ("SHAP vs LIME", "\u03c1 = 0.008  \u00b7  SD 0.359  \u00b7  n = 200"),
               ("Surrogate fidelity", "held-out R\u00b2 = 0.105  \u00b7  3,000 instances")]
    for i, (k, v) in enumerate(derived):
        y = 5.18 + i * 0.33
        text(s, ML, y, 2.10, 0.24, k, size=9.2, color=INK, bold=True, check=False)
        text(s, ML + 2.16, y, 3.94, 0.24, v, size=9.2, color=BODY, check=False)

    x2 = ML + 6.42
    label(s, x2, 2.06, 5.6, "Global SHAP importance (mean |SHAP|)")
    table(s, x2, 2.34, 5.67,
          [["Feature", "Mean |SHAP|"],
           ["Instrumentalness", "0.04047"],
           ["Energy", "0.02512"],
           ["Danceability", "0.02348"],
           ["Valence", "0.01719"],
           ["Speechiness", "0.01693"],
           ["Tempo", "0.01626"],
           ["Acousticness", "0.01553"],
           ["Loudness", "0.01301"],
           ["Liveness", "0.01270"]],
          col_w=[3.31, 2.36], row_h=0.355, header_h=0.34, font_size=9.6,
          header_size=8.6, aligns=["l", "r"], rule_color="FFFFFF")

    text(s, x2, 6.10, 5.67, 0.30,
         "Attributions of the gradient-boosting surrogate, not of the network directly.",
         size=8.6, color=MUTED, italic=True, check=False)

    notes(s, """
Backup slide. Confirm numbers from here rather than from memory.

If the SHAP values are challenged, restate immediately that they are attributions
of the surrogate (R\u00b2 = 0.105), not of the hybrid network directly.
""")
    return page + 1


def build(prs, page):
    page = s_references(prs, page)
    page = s_questions(prs, page)
    page = s_numbers(prs, page)
    return page
