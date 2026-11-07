# Viva speaker script

**Explainable Music Recommender Systems for Improving User Satisfaction**  
Chike Egonu · Supervisor: Aoife Curran · August 2026

42 slides: 35 presentation + 7 appendix. Target running time ≈ 19 minutes of content. Timing hints are included at the top of each note block.

---

## Slide 01 — Explainable Music Recommender Systems for Improving User Satisfaction

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

---

## Slide 02 — Six parts, mapped to the report's sections

TIMING: 30 s. Signpost only.

"Six parts. I'll spend the most time on methodology and results, because that is
where the marks are, and because two of the results need careful reading.

If you want to jump: section four is where the interesting finding is."

---

## Slide 03 — Background & Literature Review

SECTION DIVIDER 01 — Background & Literature Review. Roughly 10 seconds.

Do not read the list on the right to the audience; it is orientation, not content.

Say one sentence naming what the section establishes, then move. If you are running
long, this is the cheapest place to save 20 seconds — but keep the section break,
because it gives the examiner a place to interrupt.

---

## Slide 04 — Why explanation is now a design requirement

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

---

## Slide 05 — Music makes both problems harder

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
concepts a listener already has — genre, mood, energy, acoustic similarity."

---

## Slide 06 — Every step up in accuracy has cost interpretability

TIMING: 70 s.

"Four generations, and the same trade repeating.

Matrix factorisation in 2009 gave us latent factors. Excellent on implicit
feedback, but a recommendation is a dot product of two opaque vectors.

NCF in 2017 replaced the inner product with an MLP. Real accuracy gains, and the
representations become non-linear and entangled — two features no longer mean
two features.

Knowledge-graph convolution in 2019 is interesting because it partially buys
traceability back: a recommendation can be traced along artist, genre and sonic
relations. That is why I kept it as a planned extension rather than abandoning
it.

And the current wave — sequential models, attention, transformers — is the
least inspectable of the four. It is worth saying out loud: attention weights
look like explanations and are not; Jain and Wallace showed that convincingly in
2019.

So: the more competitive the architecture, the more the explanation has to be
bolted on afterwards."

---

## Slide 07 — What can be explained, and with what

TIMING: 80 s.

"Two families.

Intrinsic methods are interpretable by construction: a decision tree is its own
explanation. Faithful, but you pay for it in accuracy, and at catalogue scale
that price is not payable.

Post-hoc methods explain after training. LIME fits a small linear surrogate
around one prediction — local and cheap, but unstable. SHAP comes from
cooperative game theory and has three properties I care about: local accuracy,
missingness and consistency. Those properties are why it is the primary method
here rather than LIME. Attention as explanation — no, and Jain and Wallace made
that case.

The second half of this slide matters for how I evaluate. Tintarev and Masthoff
defined seven dimensions of explanation quality; Afchar and colleagues extended
it to eleven for recommender systems. The key empirical claim in that literature
is that these goals are correlated but not redundant — no single style
dominates.

So a project that only tested SHAP could only speak to a subset of those
dimensions. That is why the design has two explanation formats and a
multi-metric evaluation."

---

## Slide 08 — From the literature to four gaps

TIMING: 70 s.

"Four gaps, and I want to be explicit that each one drove a decision.

One: empirical scarcity. There is good conceptual work — Afchar and colleagues is
the anchor — but the empirical base in music is thin compared with e-commerce
and film, and the feature space is not transferable.

Two, and this is the one closest to my contribution: SHAP is well understood for
tabular and image models. What has not been done much is attributing a
recommendation jointly across latent collaborative factors and explicit acoustic
features. That is what a hybrid model forces you to confront, and it is
under-explored.

Three: the user evidence is thin — small samples, one explanation style.

Four: there are no music-specific explanation metrics, and accuracy keeps getting
conflated with explanation quality even though they are close to orthogonal.

One and four set the evaluation design. Two sets the architecture. Three is the
user study."

---

## Slide 09 — Aims & Objectives

SECTION DIVIDER 02 — Aims & Objectives. Roughly 10 seconds.

Do not read the list on the right to the audience; it is orientation, not content.

Say one sentence naming what the section establishes, then move. If you are running
long, this is the cheapest place to save 20 seconds — but keep the section break,
because it gives the examiner a place to interrupt.

---

## Slide 10 — One aim, three objectives

TIMING: 60 s.

"The aim is one sentence: design, implement and evaluate an explainable music
recommender that balances personalisation and accuracy with explanations a
listener can actually use.

Three objectives, and I want to be honest about the status of each, because the
abstract of a project can hide a lot.

Objective one — the hybrid model and the baselines — is implemented. Five
models, full offline evaluation.

Objective two — SHAP and LIME — is implemented, but with a deviation I will
explain in the methodology: it runs through a surrogate because the direct
explainer was intractable at this catalogue size.

Objective three — the trade-off — has a complete first pass. I am deliberately
withholding the conclusion, and the reason appears in the results: the neural
models are under-trained, which confounds the very comparison this objective
needs."

---

## Slide 11 — Research Description & Methodology

SECTION DIVIDER 03 — Research Description & Methodology. Roughly 10 seconds.

Do not read the list on the right to the audience; it is orientation, not content.

Say one sentence naming what the section establishes, then move. If you are running
long, this is the cheapest place to save 20 seconds — but keep the section break,
because it gives the examiner a place to interrupt.

---

## Slide 12 — The pipeline, end to end

TIMING: 60 s.

"Five stages. Data, preprocessing, five models, two explainers, evaluation —
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
independent of the neural family — and it is the best-performing model, which is
awkward and useful in equal measure."

---

## Slide 13 — Data source — and the audio-feature substitution

TIMING: 70 s.

"The dataset is the Spotify Million Playlist Dataset — the official one — and I
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

---

## Slide 14 — Preprocessing, in four steps

TIMING: 75 s.

"Four preprocessing steps, each with a purpose.

The k-core is iterative and runs three passes: drop playlists with fewer than
five matched tracks, drop tracks that appear in fewer than three playlists,
repeat until it converges. This is what stops the evaluation being dominated by
accidental one-track playlists.

The implicit matrix comes from playlist co-occurrence — that is the only signal
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
small later — it is expected in this regime.

Also worth noting now: 55.9% of unique tracks have no genre metadata, which is
why the knowledge-graph explanation path is a stretch goal rather than a
delivered component."

---

## Slide 15 — What the matched catalogue actually contains

TIMING: 55 s.

"Two things to read off this figure.

Genres are concentrated: Rock and Electronic dominate, then a long tail. And
release years peak sharply around 2005 to 2010 — the catalogue over-represents
that era relative to the whole history of recorded music.

Neither of those is a property of music. Both are properties of my catalogue, and
I would rather name them than have them found.

What it costs: popularity and recency priors are baked in, so my absolute numbers
describe this catalogue. What it does not cost: the ranking between models, which
is the basis of every claim I make in the results."

---

## Slide 16 — The acoustic feature space is skewed — and collinear

TIMING: 60 s.

"Nine acoustic features, and the shapes matter.

Three of them — speechiness, acousticness, instrumentalness — are effectively
zero-inflated with long right tails. Energy and loudness skew high. Only
danceability, valence and tempo are near-symmetric.

Now the correlation table, because this is the setup for the most important
result in the deck. Energy and loudness correlate at 0.78 — unsurprising, loud
music tends to be high-energy. Energy and acousticness at minus 0.73.

Both SHAP and LIME attribute credit among features, and when features are
strongly correlated, that credit can be split or swapped between them almost
arbitrarily. So when I show you a near-zero agreement between the two methods in
a moment, the mechanism is already on the table. What I cannot yet do is say how
much of the disagreement is collinearity and how much is surrogate fidelity."

---

## Slide 17 — Hybrid architecture — late fusion, by design

TIMING: 80 s.

"This is the model, and there is one design decision here that everything else
depends on.

Two collaborative views of the user–item pair: GMF, which is a generalised matrix
factorisation — effectively the linear interaction — and an MLP over the
concatenated embeddings, which captures non-linear interaction. They share a
32-dimensional embedding space, which is the NCF design from He and colleagues.

Then a third branch that only looks at the nine acoustic features, through a
two-layer network.

All three are concatenated and passed through a linear scoring layer.

The word I want you to hold onto is 'late'. I fused at the output rather than
fusing the representations early. Early fusion would probably be marginally
stronger, and it would destroy the thing I need: a separable content
contribution. That separability is what makes feature-level attribution possible
in the first place — and it is exactly the design choice Objective 3 exists to
test the cost of."

---

## Slide 18 — Five models, one protocol

TIMING: 60 s.

"Five models, one protocol.

Popularity is the floor — what you get with no personalisation. Content-based
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

---

## Slide 19 — How the explanation layer is wired

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

Of the three explanation formats proposed, two are built — the text generator
and the visual attributions. The knowledge-graph path is not attempted; genre
metadata is missing for 55.9% of tracks, which is part of why."

---

## Slide 20 — Evaluation protocol

TIMING: 60 s.

"Two evaluation tracks, because accuracy does not tell you whether an explanation
is good.

Accuracy: precision, recall, NDCG and MRR at five, ten and twenty.

The problem is scale. A dense score matrix is 96,827 users by 20,042 items —
about 1.94 billion cells. So I materialise scores for a fixed cohort of a
thousand users, sampled at random from the 87,663 test users who have at least
one held-out interaction, and score them against the full item set.

That is defensible because ranking metrics only depend on per-user ordering. The
same thousand users, the same held-out interactions, for all five models — so
the comparison is like-for-like.

Explanation quality: three metrics. Consistency is computed — the Spearman
correlation between SHAP and LIME rankings, across 200 instances. Fidelity and
coverage are implemented in design and scoped but not yet computed. I would
rather say that than invent numbers."

---

## Slide 21 — Preliminary Results

SECTION DIVIDER 04 — Preliminary Results. Roughly 10 seconds.

Do not read the list on the right to the audience; it is orientation, not content.

Say one sentence naming what the section establishes, then move. If you are running
long, this is the cheapest place to save 20 seconds — but keep the section break,
because it gives the examiner a place to interrupt.

---

## Slide 22 — Offline accuracy at K = 10

TIMING: 60 s.

"All five models, one cohort, one protocol. Reading left to right within each
metric block.

Two things to take away.

First, the ranking is consistent across all four metrics: SVD-MF, then the
hybrid, then NCF, then popularity, then content-only. Consistency across four
different metrics is reassuring — it is not a metric artefact.

Second, the levels are small, and I want to pre-empt the obvious objection. With
99.93% sparsity and four sampled negatives per positive, precision at ten in the
hundredths is expected. Absolute values here are not comparable to a production
system; the ordering is what the objectives rest on.

I am deliberately not going to claim the hybrid 'wins' overall, because it does
not — SVD-MF does. That is the next two slides."

---

## Slide 23 — Finding 1 — the content branch earns its place

TIMING: 60 s.

"This is the result the proposal predicted, and it holds.

The hybrid beats NCF on every metric. NDCG at ten up 12.3% relative, recall up
18.8%, precision 6.4%, MRR 2.2%.

Why this is attributable and not luck: the two models are identical except for
the content branch. Same embeddings, same training schedule, same negatives, same
cohort. The delta is the content branch.

The shape of the gains is also interpretable. Recall benefits most, which is what
you would expect if acoustic features help most on items with thin collaborative
evidence. MRR benefits least — the hybrid is not better at putting a relevant
track at the very top; it is better at covering more of what the user would
actually play.

Now the caveat I put on the slide, because it is true: relative, not absolute.
Both neural models sit below SVD-MF."

---

## Slide 24 — Finding 2 — the result that was not in the proposal

TIMING: 75 s.

"Here is the result that was not in the proposal.

SVD matrix factorisation — the classical baseline the proposal framed as inferior
— is the strongest model on this cohort. NDCG at ten is 0.0769 against 0.0384 for
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
comparison — which is what Objective 1 actually needs — is like-for-like, because
both were trained identically. The comparison against SVD-MF is not, and I am not
claiming it."

---

## Slide 25 — Global attributions — what drives the score

TIMING: 60 s.

"Global attributions. On the left, mean absolute SHAP value per feature; on the
right, the beeswarm, where each dot is one instance and colour is the feature's
raw value.

Instrumentalness dominates, at 0.0405 — roughly 60% more than the next feature,
energy. Then danceability and valence. Liveness and loudness are weakest.

Now, one thing to notice, because it sets up the next two slides. Loudness is
the eighth most important feature here, yet it correlates with energy at 0.78.
When two features carry almost the same information, attribution methods have to
choose where to put the credit — and different methods choose differently.

Which is exactly the problem."

NOTE FOR PRESENTING: if asked, say plainly that these are attributions of the
surrogate, not of the hybrid model directly (R² = 0.105), and that the
surrogate explains the acoustic view of the score.

---

## Slide 26 — Instance level — one recommendation, two explanations

TIMING: 60 s.

"Same recommendation instance, same surrogate, two explainers.

SHAP on the left: instrumentalness, danceability, energy, valence, liveness — all
positive contributions, topped by instrumentalness at 0.032.

LIME on the right: its top item is a binned rule — instrumentalness below minus
0.49 — with a negative weight of 0.055. Same feature, opposite direction. Its
number two is liveness, which SHAP ranks fifth. Number three is valence, which
SHAP ranks fourth. Ranks two and three do not overlap at all.

On the right is the artefact I actually built: the natural-language explanation
generated from the top-three SHAP values. 'This track was recommended primarily
because of its high instrumentalness, alongside danceability and energy.'

That is the deliverable for the first explanation format, and it works — it runs
straight off the attribution vector, so any recommendation can be explained.

But look at what the two panels disagree about. That is the next slide."

---

## Slide 27 — ρ = 0.008

TIMING: 75 s. This is the slide to slow down on.

"And now the result that surprised me most.

I measured the rank agreement between SHAP and LIME across 200 instances —
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
separate — and that is a real methodological question, not a bug to patch."

---

## Slide 28 — Accuracy against explainability

TIMING: 60 s.

"Objective three asked a specific question: what does it cost in accuracy to keep
the architecture decomposable — that is, to keep the content branch separable
so it can be explained?

The proposal predicted a cost of one to three percentage points on NDCG at ten,
following Zhang and colleagues.

What I observed was a small gain, not a cost: plus 0.0042, plus 12.3% relative.
The explainable design was not a handicap in this run.

Now I am going to argue against my own result. That comparison is confounded by
exactly the same thing that inflated SVD-MF. If the neural models are
under-trained, and if NCF is hurt more by a short schedule than the hybrid is,
then a proper training run could widen the gap — or invert it.

So I am not claiming explainability is free. I am claiming that on a converged
model set, the ablation on the right is what has to be run before that claim can
be made. The design is ready; the foundation underneath it is not."

---

## Slide 29 — Discussion & Next Steps

SECTION DIVIDER 05 — Discussion & Next Steps. Roughly 10 seconds.

Do not read the list on the right to the audience; it is orientation, not content.

Say one sentence naming what the section establishes, then move. If you are running
long, this is the cheapest place to save 20 seconds — but keep the section break,
because it gives the examiner a place to interrupt.

---

## Slide 30 — What held up, and what did not

TIMING: 70 s.

"Let me put the six findings side by side.

Three held up. The hybrid beats NCF — that was predicted and it is
attributable, because the content branch is the only difference. Content features
add signal. And the explanation layer works end to end: text and visual.

Three did not. No accuracy cost for explainability — that was predicted and did
not appear. Classical matrix factorisation was supposed to be the weak baseline;
it is the strongest model. And SHAP and LIME, which the proposal implicitly
treated as interchangeable well-documented tools, do not agree at all on this
model.

Here is the point I would like to defend: neither surprise is mysterious. One is
a training budget — five epochs against a closed-form solution. The other is
surrogate fidelity plus feature collinearity. Both are diagnosable, both are
testable, and neither requires me to invent a new theory. That is a good position
for a dissertation to be in at this stage."

---

## Slide 31 — Limitations, by type

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
deck supports a claim about user satisfaction — which is the title of the
project, and it is the part that has not been tested.

What I do have in place: identical cohorts and protocols, declared deviations,
and every number reported under the same conditions."

---

## Slide 32 — Anticipated outcomes, revised against the evidence

TIMING: 55 s.

"Five anticipated outcomes, each annotated with what actually happened.

One confirmed: the hybrid gain.

Two contradicted: the predicted accuracy cost did not appear.

Two pending: both about the user study, which has not run. I am not going to
claim satisfaction effects from offline metrics.

And a fifth that did not exist when the proposal was approved — the SHAP–LIME
disagreement. If that survives investigation, it is a dissertation-worthy finding
in its own right, because it argues against the assumption that these two methods
are interchangeable commodities.

It also changes the user study design: explanation method becomes a design
variable, or we commit to SHAP alone with a higher-fidelity surrogate."

---

## Slide 33 — Plan to submission

TIMING: 60 s.

"Six items, ordered by dependency rather than by how attractive they are.

One and two are the foundation: train to convergence, run the hyperparameter
search. Until that is done, every neural number in this deck is provisional, and
I have said so twice already.

Three is the interesting one: resolve the SHAP–LIME gap. That means a
higher-fidelity surrogate, TreeSHAP with explicit collinearity handling, and
reporting both methods rather than assuming they agree.

Four is completing the explanation metrics — fidelity and coverage — which are
designed but not computed.

Five is the knowledge-graph path, which stays a stretch goal because genre
coverage is 44%.

Six is the user study, and the box on the right is the rule I am holding myself
to: do not run it before the explanation method is stable. Otherwise I would be
measuring trust in a surrogate artefact instead of trust in an explanation, and
that is an expensive mistake to discover later."

---

## Slide 34 — Why this project is worth the time

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

---

## Slide 35 — Three things worth remembering

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

---

## Slide 36 — References  (1 of 2)

REFERENCE SLIDE. Do not read it out; say only 'full references are in the report' if you pass it, or skip it entirely. It exists so that no citation used in the talk is unsupported. If asked about a source, quote the author and year and then describe the method, not the title.

---

## Slide 37 — References  (2 of 2)

REFERENCE SLIDE. Do not read it out; say only 'full references are in the report' if you pass it, or skip it entirely. It exists so that no citation used in the talk is unsupported. If asked about a source, quote the author and year and then describe the method, not the title.

---

## Slide 38 — Thank you — questions welcome

END OF TALK. Say thank you, then stop talking. Do not fill silence.

"Thank you. I would particularly welcome challenge on the surrogate-fidelity
argument, because I know it is the weakest link in the explainability results, and
on whether the SVD-MF result is a training artefact or an architectural finding.

The appendix slides that follow are there if you want to look at any of it."

Leave this slide up during questions.

---

## Slide 39 — Likely questions — methodology

APPENDIX — prepared answers. Only show this if the examiner asks to see it, or if you need to check your own answer.

Q1. SVD-MF beats both neural models. Why should I trust the hybrid result?
A: I would not ask you to trust it as a final ranking. Five epochs, and neither loss curve has plateaued, while SVD-MF is closed-form. What Objective 1 actually needs — hybrid versus NCF — is like-for-like, because the schedule is identical. The absolute model ranking is provisional, and the rerun is the first item on the roadmap.

Q2. Your surrogate has R² = 0.105. Aren't you explaining the wrong model?
A: Partly, yes — and that is stated rather than hidden. The gap is itself informative: acoustic content accounts for about a tenth of the variance, so the rest lives in latent collaborative signal a content-only surrogate cannot see. So the explanations describe a content view of the model. It is also candidate cause (i) for the SHAP–LIME disagreement, which is why a higher-fidelity surrogate is the next test.

Q3. Why a random split rather than temporal — doesn't that leak information?
A: The MPD has no reliable interaction-level timestamps, so a temporal split would be arbitrary rather than principled. The cost is that drift and novelty are not modelled, which I list under external and conclusion validity. It does not affect the relative ranking of models, which is what every claim rests on.

Q4. Is ρ ≈ 0 just noise from 200 instances?
A: No. Noise around a genuine agreement would centre above zero with dispersion. What I observe is a mean indistinguishable from zero (0.008) with SD 0.359 — the absence of systematic agreement, not measurement error. I also report the per-instance distribution so the reader can see it is not driven by outliers.

Delivery note: answer in one sentence first, then stop. If the examiner wants more, they will ask, and you can then give the second sentence. Rambling is what turns a good answer into a doubtful one.

---

## Slide 40 — Likely questions — claims and scope

APPENDIX — prepared answers. Only show this if the examiner asks to see it, or if you need to check your own answer.

Q1. Precision@10 of 0.018 looks unusable. Are these models any good?
A: They are not deployable systems, and I do not claim they are. At 99.93% sparsity with four sampled negatives per positive, absolute values in the hundredths are expected under sampled-negative offline evaluation. The study is designed for relative comparison under one fixed protocol, not for absolute quality claims.

Q2. What is novel, if SHAP, LIME and NCF are all existing methods?
A: The combination, and the measurement. Joint attribution across a hybrid neural recommender — latent collaborative plus explicit acoustic features — is largely unexplored in music; the SHAP–LIME consistency measurement in this domain is original; and the evaluation uses music-specific explanation metrics rather than accuracy alone.

Q3. Why only 150,000 playlists instead of the full million?
A: Compute and memory. The 150-slice graph is already 1.93 million edges at 99.93% sparsity. Scaling to the full set is a rerun of the same pipeline, not a redesign — and I would rather report an internally consistent sample than an inconsistent full run.

Q4. Where does fairness and popularity bias fit?
A: Not yet modelled directly, and I say so. Feature-level attribution offers a diagnostic: if a popularity proxy dominates an attribution, the recommendation is popularity-driven. That is a planned analysis and a natural extension of the fairness dimension in Afchar et al. (2022).

Delivery note: answer in one sentence first, then stop. If the examiner wants more, they will ask, and you can then give the second sentence. Rambling is what turns a good answer into a doubtful one.

---

## Slide 41 — Metrics and methods, in one place

BACKUP SLIDE. Only show if a definition is contested.

The one to be ready for is NDCG: if asked, say it is a graded, rank-discounted
gain normalised against the ideal ordering for that user, which is why it is the
primary metric here — it rewards putting relevant tracks higher, not just
anywhere in the top ten.

Second one to be ready for is surrogate fidelity: it is the held-out R-squared of
the surrogate against the target model's score, and it is the reason the
explanation results are described as provisional.

---

## Slide 42 — Every reported number, on one slide

BACKUP SLIDE. Pure reference — do not present unless asked to confirm a number.

If an examiner reads out a value, confirm it from this table rather than from
memory. The two blocks are the accuracy table from §4.2 and the global
attribution table from §4.3.

If challenged on the SHAP numbers, restate immediately that they are attributions
of the gradient-boosting surrogate (R² = 0.105), not of the hybrid network
directly.

---
