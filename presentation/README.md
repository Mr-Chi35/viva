# Viva presentation — build sources

The deliverable is `../Chike_Egonu_Viva_Presentation.pptx` (42 slides, speaker notes on
every content slide). Everything here regenerates it.

```
presentation/
├── build.py                 # assembles the deck
├── deck_lib.py              # design system: colours, type, cards, tables, diagrams
├── sec_a_front.py           # title, roadmap, section 01 (background & literature)
├── sec_b_method.py          # section 02 (aims) and 03 (methodology)
├── sec_c_results.py         # section 04 (results) and 05 (discussion, next steps)
├── sec_d_back.py            # references, closing slide, defence appendix
├── make_charts.py           # re-plots the data charts from the report's tables
├── verify.py                # geometry audit: off-canvas shapes, text collisions
├── preview.py               # rough rasteriser used for visual QA (no LibreOffice here)
├── gen_script.py            # exports the speaker notes to Viva_Speaker_Script.md
├── charts/                  # generated data charts (regenerable)
└── assets/                  # figures lifted from the report PDF
```

## Rebuild

```bash
python -m venv .venv && .venv/bin/pip install python-pptx pillow matplotlib numpy pymupdf
cd presentation
../.venv/bin/python make_charts.py     # only if the numbers change
../.venv/bin/python build.py           # writes ../Chike_Egonu_Viva_Presentation.pptx
../.venv/bin/python verify.py          # layout audit
../.venv/bin/python gen_script.py      # refresh the printable script
```

## Deck structure

| Slides | Content |
|---|---|
| 1–8 | Title, roadmap, background and literature, four research gaps |
| 9–10 | Aims and the three objectives with status |
| 11–20 | Data, preprocessing, catalogue, architecture, baselines, explainers, protocol |
| 21–28 | Results: accuracy, hybrid gain, SVD-MF anomaly, SHAP global/instance, ρ = 0.008, trade-off |
| 29–35 | Discussion, limitations, anticipated outcomes, roadmap, contributions, conclusion |
| 36–38 | References (Harvard, as in the report) and closing slide |
| 39–42 | Appendix: eight likely examiner questions, definitions, full numbers |

## Provenance of every visual

* **Re-plotted from the report's tables** (`charts/`): model comparison at K = 10, hybrid
  delta over NCF, NDCG@10 by model, global SHAP importance. These were rebuilt because the
  report's own versions of these figures do not match its tables — see below.
* **Taken directly from the report PDF** (`assets/`): Figure 1 (genre/year), Figure 2
  (acoustic distributions), Figure 4 (loss curves), Figure 5 (SHAP beeswarm), Figure 6
  (SHAP vs LIME, one instance), Figure 7 (Spearman distribution). These are the genuine
  analysis artefacts and are consistent with the reported numbers.

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
