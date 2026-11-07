# Viva speaker script

**Explainable Music Recommender Systems for Improving User Satisfaction**  
Chike Egonu · Supervisor: Aoife Curran · August 2026

22 slides: 19 presented and 3 backup. The script runs about 13 minutes at a measured pace, which leaves roughly 2 minutes of slack in a 15-minute slot.

## Beat sheet

| Slide | Seconds | Cumulative | The sentence that has to land |
| --- | --- | --- | --- |
| 01 | 31 | 0:31 | Who I am, what the project is, and that two results were not expected. |
| 02 | 29 | 1:00 | One aim, three objectives, and Objective 3 is only a first pass. |
| 03 | 40 | 1:40 | Implicit feedback is ambiguous, so explanation is about interpretation, not decoration. |
| 04 | 43 | 2:23 | Intrinsic models are a constraint here; SHAP and LIME are the post-hoc route. |
| 05 | 34 | 2:57 | Four gaps in the literature, each one tied to a design decision. |
| 06 | 51 | 3:48 | 150,000 playlists reduce to 96,827 users and 1.93 million interactions. |
| 07 | 47 | 4:35 | The acoustic features are skewed and correlated, which matters for Section 4.3. |
| 08 | 44 | 5:19 | Late fusion keeps the content contribution separable, which is what makes attribution possible. |
| 09 | 46 | 6:05 | Five models, one protocol, so every difference is a model difference. |
| 10 | 51 | 6:56 | The surrogate replaces DeepExplainer, and R-squared of 0.105 is the price. |
| 11 | 44 | 7:40 | The hybrid beats NCF on all four metrics at K = 10. |
| 12 | 47 | 8:27 | SVD-MF is ahead, but the neural models are at five epochs, so that ranking is provisional. |
| 13 | 45 | 9:12 | Instrumentalness dominates globally, and the two methods order features differently on one item. |
| 14 | 53 | 10:05 | Mean rho of 0.008 across 200 instances: no consistent agreement between SHAP and LIME. |
| 15 | 40 | 10:45 | Four validity threats, and each one has a stated remedy. |
| 16 | 33 | 11:18 | One outcome confirmed, one not observed, one pending, one new. |
| 17 | 40 | 11:58 | Training to convergence is first, and the user study is last for a reason. |
| 18 | 36 | 12:34 | Three results and what is still open. |
| 19 | 25 | 12:59 | Hand over to questions. |

Spoken total 12:59. The 15-minute slot leaves roughly 2:01 for the walk to the lectern, transitions and the handover to questions.

Slides 20-22 are backup only. They stay in the file so a question can be answered with a slide, but they are never presented: 20 References; 21 Four questions I expect; 22 Reported numbers.

---

## Slide 01 — Title (template cover)

"Good morning. I'm Chike Egonu, supervised by Aoife Curran. My project is an
explainable music recommender system, evaluated on the Spotify Million Playlist
Dataset.

The short version: I built a hybrid recommender across five models, added an
explanation layer using SHAP and LIME, and evaluated both the accuracy and the
explanations themselves. Two of the results were not what the proposal expected,
and I will be explicit about what is finished and what is still provisional."

---

## Slide 02 — One aim, three objectives

"The aim is on the slide: an explainable recommender that balances accuracy with
explanations a listener can use.

Three objectives. One, the hybrid model and the baselines: implemented. Two,
SHAP and LIME: implemented, but through a surrogate, and I will explain why in
the methodology. Three, the accuracy-explainability trade-off: a first pass only,
because the neural models are under-trained, and that is the same issue that
affects the model comparison later."

---

## Slide 03 — Why explanation matters in music recommendation

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

---

## Slide 04 — Explaining recommendations: intrinsic and post-hoc

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

---

## Slide 05 — Four gaps in the literature

"Four gaps.

One: the empirical base in music is thin compared with e-commerce and film, and
the feature space is not transferable.

Two, and this is the one closest to my contribution: SHAP is well understood for
tabular models, but attributing a recommendation jointly across latent
collaborative factors and acoustic features has not been done much in music.

Three: user studies are small and usually test one explanation style.

Four: there are no music-specific explanation metrics, and accuracy keeps getting
conflated with explanation quality."

---

## Slide 06 — Preprocessing and the resulting interaction graph

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

---

## Slide 07 — The acoustic features are skewed and correlated

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

---

## Slide 08 — Hybrid architecture — late fusion

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

---

## Slide 09 — Five models, one protocol

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

---

## Slide 10 — How SHAP and LIME are applied

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

---

## Slide 11 — Offline accuracy at K = 10

"All five models on one cohort. Reading within each group of bars.

The ranking is the same on all four metrics: SVD-MF first, then the hybrid, then
NCF, then popularity, then content-only. The same order on all four metrics is
not an artefact of one measure.

The right-hand table isolates the comparison the first objective needs: the
hybrid against NCF, where the content branch is the only difference. It is better
on all four metrics, and NDCG at ten improves by 12.3%.

The levels are small because the matrix is 99.93% sparse; precision in the
hundredths is normal offline. The ordering is what the objectives rest on."

---

## Slide 12 — SVD-MF was the strongest model

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

---

## Slide 13 — What the explanations say

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

---

## Slide 14 — ρ = 0.008

"This is the result that surprised me most.

I measured rank agreement between SHAP and LIME across 200 instances — Spearman
correlation between their importance orderings, per instance.

Mean rho is 0.008. The standard deviation is 0.359, so some instances agree
strongly in either direction, but there is no systematic agreement.

If this were noise around a positive value the mean would sit above zero; it does
not, so this is absence of agreement rather than measurement error.

Three candidate causes, which I cannot separate yet. One, the surrogate's
fidelity: both explainers are working on a model that only loosely resembles the
real one. Two, collinearity — the correlations I showed earlier. Three, LIME's
linear approximation against a non-linear, interaction-heavy surface.

Separating them is the methodological question for the next iteration."

---

## Slide 15 — Threats to validity

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

---

## Slide 16 — Anticipated outcomes and their status

"Four outcomes, each with what the evidence shows.

One confirmed: the hybrid gain.

One not observed: the predicted accuracy cost did not appear.

One pending, and it combines the two user-study expectations from the proposal,
because neither can be tested until the study runs. I am not going to claim
satisfaction effects from offline metrics.

And the fourth is new. If the SHAP-LIME disagreement holds up, it argues against
treating these two methods as interchangeable, and it changes the user study
design."

---

## Slide 17 — Plan to submission

"Five items, ordered by dependency.

One and two are the foundation: train to convergence, and resolve the SHAP-LIME
gap. Until those are done, the model numbers and the explanation results stay
provisional.

Three completes the fidelity and coverage metrics and runs the Optuna search.

Four is optional: the knowledge-graph path, which depends on genre coverage.

Five is the user study, and the box explains why it is last. If I ran it now I
would be measuring trust in a surrogate artefact rather than trust in an
explanation, and that is an expensive mistake to find later."

---

## Slide 18 — Three results and what is still open

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

---

## Slide 19 — Thank you — questions welcome

Thank you, then stop talking. Do not fill the silence.

"I would particularly welcome questions on the surrogate in Section 4.3, because
I know it is the weakest link in the explanation results, and on whether the
SVD-MF result is a training artefact or an architectural finding.

The backup slides cover references, four questions I expect, and the full
results table."

---

## Slide 20 — References  ·  BACKUP, not presented

Backup slide. Do not present it. If a citation is challenged, give the author and
year, then describe the method rather than the title.

---

## Slide 21 — Four questions I expect  ·  BACKUP, not presented

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

---

## Slide 22 — Reported numbers  ·  BACKUP, not presented

Backup slide. Confirm numbers from here rather than from memory.

If the SHAP values are challenged, restate immediately that they are attributions
of the surrogate (R² = 0.105), not of the hybrid network directly.

---
