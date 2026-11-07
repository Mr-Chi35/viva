"""References, closing slide and the defence appendix."""
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

from deck_lib import *
from deck_lib import run_text

CHARTS = "charts"

REFS_1 = [
    ("Afchar, D., Melchiorre, A.B., Schedl, M., Hennequin, R., Epure, E.V. and Moussallam, M. "
     "(2022) \u2018Explainability in music recommender systems\u2019, AI Magazine, 43(2), "
     "pp. 190\u2013208."),
    ("Alvarez-Melis, D. and Jaakkola, T.S. (2018) \u2018On the robustness of interpretability "
     "methods\u2019, ICML Workshop on Human Interpretability in Machine Learning."),
    ("Arrieta, A.B. et al. (2020) \u2018Explainable Artificial Intelligence (XAI): concepts, "
     "taxonomies, opportunities and challenges toward responsible AI\u2019, Information "
     "Fusion, 58, pp. 82\u2013115."),
    ("Celma, O. (2010) Music Recommendation and Discovery: The Long Tail, Long Fail, and Long "
     "Play in the Digital Music Space. Berlin: Springer."),
    ("Chen, C.-W., Lamere, P., Schedl, M. and Zamani, H. (2018) \u2018RecSys Challenge 2018: "
     "automatic music playlist continuation\u2019, Proceedings of the 12th ACM Conference on "
     "Recommender Systems, pp. 527\u2013528."),
    ("Ferwerda, B., Schedl, M. and Tkalcic, M. (2015) \u2018Personality and emotional states: "
     "understanding users\u2019 music listening needs\u2019, UMAP 2015 Extended Proceedings."),
    ("He, X., Liao, L., Zhang, H., Nie, L., Hu, X. and Chua, T.-S. (2017) \u2018Neural "
     "collaborative filtering\u2019, Proceedings of the 26th International Conference on "
     "World Wide Web, pp. 173\u2013182."),
    ("Jain, S. and Wallace, B.C. (2019) \u2018Attention is not explanation\u2019, Proceedings "
     "of NAACL-HLT 2019, Volume 1, pp. 3543\u20133556."),
    ("Knijnenburg, B.P., Willemsen, M.C., Gantner, Z., Soncu, H. and Newell, C. (2012) "
     "\u2018Explaining the user experience of recommender systems\u2019, User Modeling and "
     "User-Adapted Interaction, 22(4\u20135), pp. 441\u2013504."),
    ("Koren, Y., Bell, R. and Volinsky, C. (2009) \u2018Matrix factorization techniques for "
     "recommender systems\u2019, Computer, 42(8), pp. 30\u201337."),
    ("Lipton, Z.C. (2018) \u2018The mythos of model interpretability\u2019, Communications of "
     "the ACM, 61(10), pp. 36\u201343."),
    ("Lundberg, S.M. and Lee, S.-I. (2017) \u2018A unified approach to interpreting model "
     "predictions\u2019, Advances in Neural Information Processing Systems, 30, "
     "pp. 4765\u20134774."),
]

REFS_2 = [
    ("Melchiorre, A.B., Rekabsaz, N., Ganh\u00f6r, C. and Schedl, M. (2022) \u2018ProtoMF: "
     "prototype-based matrix factorization for effective and explainable "
     "recommendations\u2019, Proceedings of the 16th ACM Conference on Recommender Systems, "
     "pp. 246\u2013256."),
    ("Oramas, S., Ostuni, V.C., Di Noia, T., Serra, X. and Di Sciascio, E. (2017) \u2018Sound "
     "and music recommendation with knowledge graphs\u2019, ACM Transactions on Intelligent "
     "Systems and Technology, 8(2), pp. 21.1\u201321.21."),
    ("Ribeiro, M.T., Singh, S. and Guestrin, C. (2016) \u2018\u201cWhy should I trust "
     "you?\u201d: explaining the predictions of any classifier\u2019, Proceedings of the 22nd "
     "ACM SIGKDD, pp. 1135\u20131144."),
    ("Schedl, M., Zamani, H., Chen, C.-W., Deldjoo, Y. and Elahi, M. (2018) \u2018Current "
     "challenges and visions in music recommender systems research\u2019, International "
     "Journal of Multimedia Information Retrieval, 7(2), pp. 95\u2013116."),
    ("Shashaani, S. (2024) \u2018Explainability in music recommender system\u2019, Proceedings "
     "of the 18th ACM Conference on Recommender Systems, pp. 1395\u20131401."),
    ("Tintarev, N. and Masthoff, J. (2007) \u2018A survey of explanations in recommender "
     "systems\u2019, Proceedings of the 2007 IEEE 23rd International Conference on Data "
     "Engineering Workshop, pp. 801\u2013810."),
    ("Tintarev, N. and Masthoff, J. (2015) \u2018Explaining recommendations: design and "
     "evaluation\u2019, in Ricci, F., Rokach, L. and Shapira, B. (eds) Recommender Systems "
     "Handbook. 2nd edn. Boston, MA: Springer US, pp. 353\u2013382."),
    ("van den Oord, A., Dieleman, S. and Schrauwen, B. (2013) \u2018Deep content-based music "
     "recommendation\u2019, Advances in Neural Information Processing Systems, 26, "
     "pp. 2643\u20132651."),
    ("Wang, H., Zhao, M., Xie, X., Li, W. and Guo, M. (2019) \u2018Knowledge graph "
     "convolutional networks for recommender systems\u2019, Proceedings of the 2019 World Wide "
     "Web Conference, pp. 3307\u20133313."),
    ("Zhang, Y. and Chen, X. (2020) \u2018Explainable recommendation: a survey and new "
     "perspectives\u2019, Foundations and Trends in Information Retrieval, 14(1), "
     "pp. 1\u2013101."),
    ("Zhang, Y., Lai, G., Zhang, M., Zhang, Y., Liu, Y. and Ma, S. (2014) \u2018Explicit "
     "factor models for explainable recommendation based on phrase-level sentiment "
     "analysis\u2019, Proceedings of SIGIR 2014, pp. 83\u201392."),
    ("Zhou, F., Ji, Y. and Jiao, R.J. (2013) \u2018Affective and cognitive design for mass "
     "personalization: status and prospect\u2019, Journal of Intelligent Manufacturing, "
     "24(5), pp. 1047\u20131069."),
]


def _ref_column(s, x, y, w, h, entries, size=9.3):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    marL = int(Inches(0.24))
    for i, e in enumerate(entries):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = 1.10
        p.space_after = Pt(11)
        pPr = p._p.get_or_add_pPr()
        pPr.set("marL", str(marL))
        pPr.set("indent", str(-marL))
        run_text(p, e, size, BODY, False, False, FONT)


def s_references(prs, page, part, entries, total_pages=2):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "References", f"References  ({part} of {total_pages})", page,
           lede="Harvard style, as in the report. Full list, split across two slides.")

    n = (len(entries) + 1) // 2
    _ref_column(s, ML, 2.18, 5.80, 4.50, entries[:n])
    notes(s, "REFERENCE SLIDE. Do not read it out; say only 'full references are in the "
             "report' if you pass it, or skip it entirely. It exists so that no citation "
             "used in the talk is unsupported. If asked about a source, quote the author and "
             "year and then describe the method, not the title.")
    _ref_column(s, ML + 6.28, 2.18, 5.80, 4.50, entries[n:], size=9.3)
    return page + 1


def s_thanks(prs, page):
    s = blank(prs)
    bg_gradient(s, DARK_BG, RGBColor(0x1C, 0x20, 0x4E), 35)
    rings(s, 11.7, 2.4, [3.6, 5.2, 6.8], DARK_RING, 0.9)

    text(s, ML, 1.34, 8.0, 0.28, "End of presentation", size=9.4, color=TEAL, bold=True,
         spc=190, caps=True, check=False)
    text(s, ML, 1.70, 10.60, 0.75, "Thank you \u2014 questions welcome", size=34, color=WHITE,
         bold=True, line_spacing=1.05, check=False)
    rect(s, ML + 0.02, 2.52, 0.90, 0.05, fill=TEAL)

    text(s, ML, 2.80, 8.6, 0.90,
         "I would particularly welcome challenge on the surrogate-fidelity argument in "
         "\u00a74.3, and on whether the SVD-MF result is a training artefact or an "
         "architectural finding.",
         size=13.2, color=DARK_TXT, line_spacing=1.35)

    stats = [("0.0384", "hybrid NDCG@10"), ("+12.3%", "over NCF"),
             ("0.008", "SHAP\u2013LIME \u03c1"), ("5", "models benchmarked")]
    x = ML
    for v, l in stats:
        text(s, x, 4.18, 2.9, 0.44, v, size=24, color=WHITE, bold=True, check=False)
        text(s, x, 4.66, 2.9, 0.24, l, size=8.8, color=RGBColor(0x7C, 0x82, 0xAC),
             caps=True, spc=110, check=False)
        x += 2.92

    hline(s, ML, 5.44, CW, RGBColor(0x2C, 0x31, 0x66), 1.0)
    text(s, ML, 5.64, 6.0, 0.28,
         "Chike Egonu  \u00b7  MSc Dissertation  \u00b7  August 2026",
         size=11.4, color=WHITE, check=False)
    text(s, ML, 5.94, 6.0, 0.28, "Supervisor: Aoife Curran", size=10.2, color=DARK_TXT,
         check=False)

    text(s, 8.30, 5.60, 4.4, 0.62,
         "Appendix follows: eight likely examiner questions with prepared answers, plus "
         "definitions and a full results table.",
         size=9.6, color=RGBColor(0x7C, 0x82, 0xAC), line_spacing=1.25)

    notes(s, """
END OF TALK. Say thank you, then stop talking. Do not fill silence.

"Thank you. I would particularly welcome challenge on the surrogate-fidelity
argument, because I know it is the weakest link in the explainability results, and
on whether the SVD-MF result is a training artefact or an architectural finding.

The appendix slides that follow are there if you want to look at any of it."

Leave this slide up during questions.
""")
    return page + 1


def s_q_and_a(prs, page, title, pairs, tag="Appendix"):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, f"{tag}  \u00b7  defence preparation", title, page,
           lede="Prepared answers \u2014 each one is also in the speaker notes in full.")

    y = 2.02
    for i, (q, a) in enumerate(pairs):
        shape(s, ML, y, CW, 1.04, fill=WHITE, line=LINE, radius=0.05)
        rect(s, ML, y, 0.05, 1.04, fill=ACCENT)
        text(s, ML + 0.26, y + 0.13, 0.42, 0.24, f"Q{i+1}", size=8.6, color=ACCENT,
             bold=True, spc=60, check=False)
        text(s, ML + 0.76, y + 0.10, CW - 1.06, 0.28, q, size=11.2, color=INK, bold=True,
             check=False)
        text(s, ML + 0.76, y + 0.40, CW - 1.06, 0.56, a, size=9.3, color=BODY,
             line_spacing=1.16)
        y += 1.12

    text(s, ML, 6.52, CW, 0.24,
         "Figures quoted here match those in the deck and the report; if a number is "
         "challenged, the source table is in Appendix D.", size=8.8, color=MUTED,
         italic=True, check=False)

    full = "APPENDIX \u2014 prepared answers. Only show this if the examiner asks to see it, "\
           "or if you need to check your own answer.\n\n"
    for i, (q, a) in enumerate(pairs, 1):
        full += f"Q{i}. {q}\nA: {a}\n\n"
    full += ("Delivery note: answer in one sentence first, then stop. If the examiner wants "
             "more, they will ask, and you can then give the second sentence. Rambling is "
             "what turns a good answer into a doubtful one.")
    notes(s, full)
    return page + 1


QA_A = [
    ("SVD-MF beats both neural models. Why should I trust the hybrid result?",
     "I would not ask you to trust it as a final ranking. Five epochs, and neither loss curve "
     "has plateaued, while SVD-MF is closed-form. What Objective 1 actually needs \u2014 hybrid "
     "versus NCF \u2014 is like-for-like, because the schedule is identical. The absolute "
     "model ranking is provisional, and the rerun is the first item on the roadmap."),
    ("Your surrogate has R\u00b2 = 0.105. Aren't you explaining the wrong model?",
     "Partly, yes \u2014 and that is stated rather than hidden. The gap is itself informative: "
     "acoustic content accounts for about a tenth of the variance, so the rest lives in "
     "latent collaborative signal a content-only surrogate cannot see. So the explanations "
     "describe a content view of the model. It is also candidate cause (i) for the "
     "SHAP\u2013LIME disagreement, which is why a higher-fidelity surrogate is the next test."),
    ("Why a random split rather than temporal \u2014 doesn't that leak information?",
     "The MPD has no reliable interaction-level timestamps, so a temporal split would be "
     "arbitrary rather than principled. The cost is that drift and novelty are not modelled, "
     "which I list under external and conclusion validity. It does not affect the relative "
     "ranking of models, which is what every claim rests on."),
    ("Is \u03c1 \u2248 0 just noise from 200 instances?",
     "No. Noise around a genuine agreement would centre above zero with dispersion. What I "
     "observe is a mean indistinguishable from zero (0.008) with SD 0.359 \u2014 the absence of "
     "systematic agreement, not measurement error. I also report the per-instance "
     "distribution so the reader can see it is not driven by outliers."),
]

QA_B = [
    ("Precision@10 of 0.018 looks unusable. Are these models any good?",
     "They are not deployable systems, and I do not claim they are. At 99.93% sparsity with "
     "four sampled negatives per positive, absolute values in the hundredths are expected "
     "under sampled-negative offline evaluation. The study is designed for relative "
     "comparison under one fixed protocol, not for absolute quality claims."),
    ("What is novel, if SHAP, LIME and NCF are all existing methods?",
     "The combination, and the measurement. Joint attribution across a hybrid neural "
     "recommender \u2014 latent collaborative plus explicit acoustic features \u2014 is largely "
     "unexplored in music; the SHAP\u2013LIME consistency measurement in this domain is "
     "original; and the evaluation uses music-specific explanation metrics rather than "
     "accuracy alone."),
    ("Why only 150,000 playlists instead of the full million?",
     "Compute and memory. The 150-slice graph is already 1.93 million edges at 99.93% "
     "sparsity. Scaling to the full set is a rerun of the same pipeline, not a redesign \u2014 "
     "and I would rather report an internally consistent sample than an inconsistent full "
     "run."),
    ("Where does fairness and popularity bias fit?",
     "Not yet modelled directly, and I say so. Feature-level attribution offers a diagnostic: "
     "if a popularity proxy dominates an attribution, the recommendation is "
     "popularity-driven. That is a planned analysis and a natural extension of the fairness "
     "dimension in Afchar et al. (2022)."),
]


def s_glossary(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Appendix  \u00b7  definitions", "Metrics and methods, in one place", page,
           lede="Short definitions, in case a term needs pinning down mid-question.")

    rows = [["Term", "Definition", "Where used"],
            ["Precision@K", "Share of the top-K recommendations that are relevant", "\u00a74.2"],
            ["Recall@K", "Share of a user's held-out items recovered in the top K", "\u00a74.2"],
            ["NDCG@K", "Rank-weighted gain, normalised against the ideal ordering", "\u00a74.2"],
            ["MRR", "Mean of the reciprocal rank of the first relevant item", "\u00a74.2"],
            ["SHAP", "Shapley-value attribution; satisfies local accuracy, missingness, "
                     "consistency", "\u00a73.3, \u00a74.3"],
            ["LIME", "Locally faithful linear surrogate fitted around one prediction",
             "\u00a73.3, \u00a74.3"],
            ["Surrogate fidelity", "Held-out R\u00b2 of the approximation to the target model",
             "\u00a73.3"],
            ["k-core filtering", "Iterative removal of users and items below a minimum "
                                 "interaction count", "\u00a73.1"],
            ["Matrix sparsity", "Share of the user\u2013item matrix with no observed "
                                "interaction", "\u00a74.1"],
            ["Spearman \u03c1", "Rank correlation between two importance orderings",
             "\u00a74.3"]]
    table(s, ML, 2.06, CW, rows, col_w=[2.34, 7.45, 2.30], row_h=0.37, header_h=0.36,
          font_size=9.6, header_size=8.6, aligns=["l", "l", "c"], first_bold=True,
          rule_color="FFFFFF")

    text(s, ML, 6.32, CW, 0.30,
         "All definitions are the ones used in the report; no metric has been redefined "
         "between sections.", size=9.0, color=MUTED, italic=True, check=False)

    notes(s, """
BACKUP SLIDE. Only show if a definition is contested.

The one to be ready for is NDCG: if asked, say it is a graded, rank-discounted
gain normalised against the ideal ordering for that user, which is why it is the
primary metric here \u2014 it rewards putting relevant tracks higher, not just
anywhere in the top ten.

Second one to be ready for is surrogate fidelity: it is the held-out R-squared of
the surrogate against the target model's score, and it is the reason the
explanation results are described as provisional.
""")
    return page + 1


def s_numbers(prs, page):
    s = blank(prs)
    bg(s, WHITE)
    chrome(s, "Appendix  \u00b7  full results", "Every reported number, on one slide", page,
         lede="The accuracy table and the global attribution ranking, for reference during "
              "questions.")

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

    text(s, ML, 4.68, 6.10, 0.30,
         "Best per column in every case: SVD-MF.", size=8.8, color=MUTED, check=False)

    label(s, ML, 5.06, 5.8, "Derived comparisons quoted in the discussion")
    derived = [("Hybrid \u2212 NCF", "NDCG@10  +0.0042  (+12.3% relative)"),
               ("SVD-MF \u2212 Hybrid", "NDCG@10  +0.0385  (2.0\u00d7 the hybrid)"),
               ("SHAP vs LIME", "\u03c1 = 0.008  \u00b7  SD 0.359  \u00b7  n = 200"),
               ("Surrogate fidelity", "held-out R\u00b2 = 0.105  \u00b7  3,000 instances")]
    for i, (k, v) in enumerate(derived):
        y = 5.34 + i * 0.33
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

    text(s, x2, 6.32, 5.67, 0.30,
         "Attributions of the gradient-boosting surrogate, not of the network directly.",
         size=8.8, color=MUTED, italic=True, check=False)

    notes(s, """
BACKUP SLIDE. Pure reference \u2014 do not present unless asked to confirm a number.

If an examiner reads out a value, confirm it from this table rather than from
memory. The two blocks are the accuracy table from \u00a74.2 and the global
attribution table from \u00a74.3.

If challenged on the SHAP numbers, restate immediately that they are attributions
of the gradient-boosting surrogate (R\u00b2 = 0.105), not of the hybrid network
directly.
""")
    return page + 1


def build(prs, page):
    page = s_references(prs, page, 1, REFS_1)
    page = s_references(prs, page, 2, REFS_2)
    page = s_thanks(prs, page)
    page = s_q_and_a(prs, page, "Likely questions \u2014 methodology", QA_A)
    page = s_q_and_a(prs, page, "Likely questions \u2014 claims and scope", QA_B)
    page = s_glossary(prs, page)
    page = s_numbers(prs, page)
    return page
