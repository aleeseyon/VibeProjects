# Novelty Ledger

Classification categories (per task spec): **KNOWN**, **INCREMENTAL**,
**POTENTIALLY NOVEL**, **SUPPORTED NOVELTY**, **REFUTED NOVELTY**.

Nothing here is promoted to SUPPORTED NOVELTY — that requires evidence from
a full systematic literature review (SEG/EAGE/Geophysics/Interpretation/
Geophysical Prospecting/GJI full-text search), which this Phase 0 pass does
not constitute. This is a bounded, ~15-query web search, sufficient to
catch obvious prior art and gate the proposal, not to clear it for
publication. Treat every "POTENTIALLY NOVEL" entry below as provisional.

## Contribution-by-contribution classification

### C1. "Rock- and wave-physics-guided neural network for direct multi-property petrophysical inversion from prestack AVO" (the RW-PGNN paradigm itself)

**Classification: REFUTED NOVELTY (as a paradigm name/concept).**

Vashisth & Mukerji (2022, *The Leading Edge*, DOI 10.1190/tle41120840.1)
already published "RW-PINN" — rock- and wave-physics-informed neural
network — for direct petrophysical estimation from seismic with few-well
weak supervision. The general paradigm (physics-informed NN + rock physics
+ wave physics + sparse well supervision, direct petrophysical output) is
not new and predates the existing notebooks by at least 2 years judging
from typical Colab/GitHub timestamps implied in this repo's history.

**What remains potentially defensible (see C2, C3):** the specific
combination of (a) multi-property (φ, Vsh, Sw) simultaneous output instead
of porosity-only, (b) full prestack angle-dependent exact-Zoeppritz forward
physics instead of normal-incidence, (c) the well-count scaling + buffered
spatial-CV protocol. None of these alone is a large claim; together they
are, at best, an incremental extension of Vashisth & Mukerji (2022) in the
direction that Li et al. (2024, Geophysics, two papers) and Wu et al.
(2024, Geophysics) have already also moved in (multi-property, prestack,
and — critically — *already with probabilistic/Bayesian uncertainty and
field validation*, which our own repo does not yet have).

**Action:** Do not present RW-PGNN's existence as the PhD's contribution.
The PhD's contribution, if any, must be the resolvability/degradation/
calibration analysis built around it (Objectives 1–3), not the network
architecture.

### C2. Multi-property (φ, Vsh, Sw) simultaneous direct inversion via full-trace exact-Zoeppritz PGNN

**Classification: INCREMENTAL.**

Das & Mukerji (2020) already predict multiple properties end-to-end
(without physics guidance). Li et al. (2024, geo2023-0214.1 and
geo2023-0737.1) already combine physics-informed/Bayesian NNs for
petrophysical inversion with field validation. The specific combination of
"physics-guided AND multi-property AND exact per-interface Zoeppritz AND
full-trace" is a plausible but modest increment over existing work, not
demonstrated to be absent from the literature by this search.

### C3. Well-count scaling + buffered spatial-CV crossover diagnostic (N* at which a physics-guided NN matches an SVD-basis method)

**Classification: POTENTIALLY NOVEL (as a specific diagnostic), built on KNOWN methodological components.**

The buffered spatial-CV method itself (Roberts et al. 2017; Ploton et al.
2020) is standard practice imported correctly from ecology, not new. The
specific "crossover-N" framing (smallest N at which a data-driven method's
R² matches a physics-derived-basis method's R², under a leakage-safe,
multi-seed protocol) was not found in the literature search as a named
seismic-QI diagnostic. This is a real methodological candidate for Paper 2
but is a small, self-contained contribution, not a thesis-defining one.

### C4. Property-specific resolvability under realistic AVA uncertainty (velocity/RMO, wavelet, amplitude/noise), tied explicitly to rock-physics/AVA sensitivity and identifiability

**Classification: POTENTIALLY NOVEL as an integrated framework; KNOWN as individual pieces.**

- The physical mechanism (velocity/moveout error → AVO gradient distortion)
  is established (Sarkar, Baumel & Larner 2002).
- Rock-physics sensitivity/nonuniqueness/AVO-class analysis is a mature,
  decades-old QI subfield (Mavko, Mukerji & Dvorkin, *Rock Physics
  Handbook*; standard AVO-class literature).
- Fisher-information / identifiability framing for seismic-to-property
  inversion exists in adjacent literatures (geostatistical rock-physics AVA
  inversion; general inverse-problem identifiability) but this search did
  not find a paper that explicitly builds a **property-specific
  resolvability index that traces uncertainty from AVA-attribute
  distortion through to loss of an ML/physics-guided inversion's per-
  property recoverability**, evaluated as a controlled degradation
  experiment (U0→Un).
- **This is the strongest, most defensible novelty candidate.** It is not
  refuted by anything found in this pass, and it directly closes the gap
  the existing notebooks openly admit (asymmetric identifiability observed
  but not systematically explained or predicted in Part 2's summary).
- **Caveat:** "not found in a ~15-query search" is weak evidence of
  absence. A full systematic search (Phase 0 follow-up, before Paper 1 is
  drafted) is required before this can move to SUPPORTED NOVELTY.

### C5. Uncertainty-aware physics-guided inversion that recognizes when seismic no longer supports a given property's prediction (calibration / confident-error rate / property-specific coverage)

**Classification: INCREMENTAL, given C4's field-validated precedent.**

Li et al. (2024, both Geophysics papers) already deliver probabilistic /
Bayesian physics-guided petrophysical inversion with field validation.
That significantly narrows what is left novel in "uncertainty-aware
physics-guided inversion" per se. What those papers do NOT appear to do
(based on abstracts/summaries available in this search; full text not yet
read) is:
  - explicitly quantify **calibration** (coverage probability, reliability
    diagrams, CRPS, a rigorously pre-defined "confidently wrong" rate) as
    the primary evaluation axis rather than accuracy;
  - tie uncertainty growth to a **controlled, multi-source AVA-uncertainty
    degradation ladder** (velocity/RMO, wavelet, amplitude/noise) rather
    than only rock-physics-hyperparameter or weight-space uncertainty;
  - connect uncertainty behavior back to the **property-specific
    resolvability** predicted from Objective 1's rock-physics/AVA analysis
    (i.e., test whether the network's uncertainty actually tracks the
    resolvability the physics predicts).
**Action:** Objective 3 / Paper 2 must be re-scoped around these three
gaps specifically, not around "we also built a probabilistic PGNN" — that
part is not new by itself. **Before Paper 2 is drafted, the full text of
both Li et al. (2024) papers and Wu et al. (2024) must be read** (this
audit only had abstract-level access) to confirm whether these three gaps
survive.

### C6. Volve field blind-well validation of resolvability/calibration findings

**Classification: POTENTIALLY NOVEL, contingent on data availability (see DATA_AUDIT gap in RESEARCH_PLAN).**

Volve is heavily used for ML-petrophysics work generally (shear-log
prediction, porosity-from-inversion-attributes studies), but this search
did not surface a paper doing blind-well validation of *resolvability/
calibration* claims (as opposed to point-accuracy) on Volve prestack data.
Search results also surfaced an important **constraint, not just an
opportunity**: Volve's prestack + full elastic (Vp/Vs/rho) well-log
coverage is reported as limited to as few as **two wells** with both
petrophysical and elastic logs in at least one processing-focused source;
most wells lack a measured Vs (shear) log entirely, which is exactly the
kind of "not everything you assumed exists" risk the task instructions
warn about. This must be independently re-verified against the actual
Volve data room before Paper 3 is planned in detail — do not treat the
numbers above as final.

### C7. Symbolic linearized Vp-error → Shuey A/B sensitivity/error-propagation analysis with AVO-class-misclassification boundary (Study A, `Smeaheia_AVO_error_propagation.ipynb`)

**Classification: KNOWN as a method, INCREMENTAL as an application.**

The underlying method — differentiate Shuey/Aki-Richards attributes with
respect to elastic parameters to get a local sensitivity coefficient, then
map the resulting error envelope onto AVO-class space — is a natural,
long-established extension of the AVO-class literature Study A itself
correctly cites (Rutherford & Williams 1989, *Geophysics* 54, 680-688;
Castagna, Swan & Foster 1998, *Geophysics* 63, 948-956; Castagna & Backus
1993 eds., SEG *Offset-Dependent Reflectivity*). Symbolic/analytic AVO
sensitivity and class-boundary analysis of this general kind is standard
QI practice, not a new method. (These four citations are treated as
correctly and reliably cited by the notebook's author — canonical, highly
stable geophysics literature — and were not independently re-verified by
web search in this pass, unlike the 2020s deep-learning literature in
C1–C6, which was actively moving and needed checking.)

**What is a genuine, small, defensible increment:** applying this
machinery specifically to the Smeaheia CO₂-storage top-reservoir case,
quantifying the ~14× asymmetry between k_A and k_B for this specific
baseline, and showing the resulting Class III→IV misclassification
threshold (~3-5% differential Vp error) is a real, useful, citable
Smeaheia-specific result. It is a case study application of known methods,
not a new method.

**Action for Objective 1:** the genuinely open, potentially-novel step is
NOT redoing this analysis — it is **extending the chain one physical layer
further back**, from directly-perturbed Vp to perturbed reservoir
properties (φ, Vsh, Sw) propagated through the Gassmann rock-physics model
already used in the other two notebooks, so that resolvability can be
stated in terms of φ/Vsh/Sw (what the thesis actually needs to say
something about) rather than in terms of Vp (an intermediate elastic
variable). This connects C7 to C4 and is the concrete next build step, not
a new literature-novelty question — it is engineering integration, not a
literature gap.

## Summary table

| # | Contribution | Classification |
|---|---|---|
| C1 | RW-PGNN paradigm itself | REFUTED NOVELTY |
| C2 | Multi-property full-trace exact-Zoeppritz PGNN | INCREMENTAL |
| C3 | Well-count crossover-N diagnostic (buffered, multi-seed) | POTENTIALLY NOVEL (narrow) |
| C4 | Property-specific resolvability under realistic AVA uncertainty (integrated framework) | POTENTIALLY NOVEL (strongest candidate) |
| C5 | Uncertainty-aware physics-guided inversion w/ calibration + resolvability linkage | INCREMENTAL (re-scoped) |
| C6 | Volve blind-well validation of resolvability/calibration | POTENTIALLY NOVEL (data-constrained) |
| C7 | Study A: Vp-error → Shuey A/B sensitivity + AVO-class boundary (Smeaheia case) | KNOWN method / INCREMENTAL application — extending it to φ/Vsh/Sw via Gassmann is the real next step, feeding C4 |

**Overall verdict:** The PhD as originally framed ("build a probabilistic
physics-guided inversion and show it's better") is largely incremental
against Li et al. (2024) ×2 and Wu et al. (2024), all in *Geophysics*,
2024, with field validation already done. The PhD survives, but only if
its center of gravity shifts from "build the method" (C1/C2/C5, mostly
already done elsewhere) to "determine what is and isn't resolvable, and
whether uncertainty tracks it" (C4, with C3 and C6 as supporting pieces).
This is consistent with, and reinforces, Objective 1/Objective 2 being the
load-bearing objectives of the thesis rather than Objective 3. Study A (C7)
strengthens this conclusion in practice, not just in principle: it is a
real, validated piece of Objective 1 infrastructure (AVO-attribute-level
sensitivity) that already exists and only needs to be extended through the
rock-physics chain to φ/Vsh/Sw to become the core of Paper 1.
