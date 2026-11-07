# Viva presentation — build sources

The deliverable is `../Chike_Egonu_Viva_Presentation.pptx`: **22 slides — 19 presented and
3 backup**, speaker notes on every presented slide. It is built for a **15-minute defence
slot**; the script in `Viva_Speaker_Script.md` runs about 13 minutes.

```
presentation/
├── build.py                 # assembles the deck
├── deck_lib.py              # design system: colours, type, cards, tables, diagrams
├── sec_a_front.py           # slides 1–5: title, aims, motivation, frameworks, gaps
├── sec_b_method.py          # slides 6–10: preprocessing, features, architecture, models, explainers
├── sec_c_results.py         # slides 11–19: results, validity, outcomes, plan, summary, closing
├── sec_d_back.py            # slides 20–22 (backup): references, likely questions, numbers
├── make_charts.py           # re-plots the data charts from the report's tables
├── verify.py                # geometry audit: off-canvas shapes, text collisions
├── preview.py               # rough rasteriser used for visual QA (no LibreOffice here)
├── gen_script.py            # exports the speaker notes + beat sheet to Viva_Speaker_Script.md
├── charts/                  # generated data charts (regenerable)
└── assets/                  # figures lifted from the report PDF, plus cropped variants
```

## Rebuild

```bash
python -m venv .venv && .venv/bin/pip install python-pptx pillow matplotlib numpy pymupdf
cd presentation
../.venv/bin/python make_charts.py     # only if the numbers change
../.venv/bin/python build.py           # writes ../Chike_Egonu_Viva_Presentation.pptx
../.venv/bin/python verify.py          # layout audit (off-canvas rings on 1, 18, 19 are intentional)
../.venv/bin/python preview.py         # renders preview/slide_NN.png for visual QA
../.venv/bin/python gen_script.py      # refresh the printable script + beat sheet
```

## Deck structure

| Slide | Section | Content | ≈ time |
|---|---|---|---|
| 1 | — | Title, presenter, supervisor | 0:30 |
| 2 | §2 | One aim, three objectives, status of each | 0:30 |
| 3 | §1.1 | Why explanation matters in music recommendation | 0:40 |
| 4 | §1.3 | Intrinsic vs post-hoc explanation; explanation quality | 0:45 |
| 5 | §1.5 | Four gaps in the literature | 0:35 |
| 6 | §3.1 | Preprocessing and the resulting interaction graph | 0:50 |
| 7 | §4.1 | The acoustic features are skewed and correlated | 0:45 |
| 8 | §3.2 | Hybrid architecture — late fusion | 0:45 |
| 9 | §3.2 | Five models, one protocol | 0:45 |
| 10 | §3.3 | How SHAP and LIME are applied; R² = 0.105 | 0:50 |
| 11 | §4.2 | Offline accuracy at K = 10 | 0:45 |
| 12 | §4.2 | SVD-MF was the strongest model | 0:45 |
| 13 | §4.3 | What the explanations say (global + one instance) | 0:45 |
| 14 | §4.3 | SHAP and LIME do not agree, ρ = 0.008 | 0:55 |
| 15 | §5 | Threats to validity | 0:40 |
| 16 | §6 | Anticipated outcomes and their status | 0:35 |
| 17 | §8 | Plan to submission | 0:40 |
| 18 | — | Summary: three results and what is still open | 0:35 |
| 19 | — | Thank you / questions | 0:25 |
| 20–22 | — | **Backup only**: references, four likely questions, reported numbers | — |

Presented total ≈ 13:00, leaving about 2 minutes inside the slot for the walk to the
lectern, transitions and overrun.

## What changed from the 42-slide draft

The first build was a full-length walkthrough. It was cut to a defence deck:

* **Section dividers, roadmap, glossary, scoreboard and the duplicated trade-off slide were
  removed.** They cost about four minutes and added no evidence.
* **Merged**: accuracy chart + gain panel; global SHAP + instance comparison; preprocessing
  (filter → matrix → split); motivation + ambiguity table; references 2 of 2 → 1 slide.
* **Register**: rhetorical framing ("explanation is not a cosmetic layer", "three things
  worth remembering", panel labels such as "Read this in three lines") was replaced with
  report-traceable statements.
* **Claims**: any sentence the report does not make was deleted, notably causal links
  between missing genre metadata and the abandoned knowledge-graph path, "first measurement
  of SHAP–LIME agreement", and "reproducible" as an adjective on the pipeline. All derived
  numbers are arithmetic on Table 2 and are labelled as such.
* **Notes**: notes for deleted slides went with them; timing scaffolding was replaced by the
  beat sheet at the top of `Viva_Speaker_Script.md`.

## Provenance of every visual

* **Re-plotted from the report's tables** (`charts/`): model comparison at K = 10, hybrid
  delta over NCF, NDCG@10 by model, global SHAP importance. These were rebuilt because the
  report's own versions of these figures do not match its tables — see below.
* **Taken directly from the report PDF** (`assets/`): Figure 1 (genre/year), Figure 2
  (acoustic distributions), Figure 4 (loss curves), Figure 5 (SHAP beeswarm), Figure 6
  (SHAP vs LIME, one instance), Figure 7 (Spearman distribution). `fig6_pair_crop.png` and
  `fig7_crop.png` are the same figures with the redundant in-figure titles cropped so the
  plot area can be shown larger.

## Check these in the report before you present

1. **Report Figure 3** (`assets/fig3_accuracy_bars.png`) is labelled with the wrong x-axis:
   it plots a "BPR-MF" model that does not exist in the study and puts the tall bars under
   *Content-based*, which the table says is the weakest model. The deck therefore uses a
   re-plot of the table instead.
2. **Report Figure 8** (`assets/fig8_tradeoff.png`) shows NDCG@10 values around 0.02 and
   the content-based model as the *strongest* — the opposite of the table. Not used.
3. **Report Figure 4** (loss curves) plots BCE ≈ 0.50 while the text states ≈ 0.216. The
   *shape* is what the argument uses ("still descending at epoch 5"), and the deck says so
   explicitly, but the two should be reconciled.
4. **Report Figure 5** (beeswarm) ranks loudness widest, whereas the mean |SHAP| table puts
   instrumentalness first (and the plot is listed alphabetically). Worth checking which run
   each came from.

Fixing 1–4 in the PDF before submission removes the most obvious line of attack in a viva.
