# PHASE0_REPORT

Revised 2026-09-11 (same day) after the user supplied Study A, which was
missing from the first pass. Prepared as the mandatory Phase 0 gate before
any code is written or experiment is launched, per the task's explicit
instruction to STOP after this report. Companion documents:
`EXISTING_WORK_AUDIT.md`, `NOVELTY_LEDGER.md`, `RESEARCH_PLAN.md`,
`literature/novelty_matrix.csv`.

## 1. Existing work

Three notebooks now exist. `Seis2Rock_Complete_Project_with_ML_audit.ipynb`
(earlier stream, patch-based AVONet architecture, contains a valuable
"ML Audit" section — leakage checks, buffered spatial CV, Sw label-
permutation test, CO₂ classification head) and `GEOP592_RWPGNN_FINAL.ipynb`
(more mature, full-trace CNN with an exact differentiable layered-Zoeppritz
forward operator, well-count scaling experiments, and a buffered/multi-seed
version of the same scaling experiment) both replicate Seis2Rock (Corrales
et al. 2024) as a baseline and compare against Das & Mukerji (2020)
PetroNet/Cascaded baselines with MC-Dropout uncertainty.
`Smeaheia_AVO_error_propagation.ipynb` (**Study A**, supplied by the user
and added to the repo in this revision) is a validated, symbolic (sympy)
sensitivity analysis of how independent caprock/reservoir Vp errors shift
the Shuey A/B AVO attributes at the Smeaheia top reservoir, benchmarked to
5 decimals against an independent Mathematica implementation. Full detail
in `EXISTING_WORK_AUDIT.md`.

**Correction to the first Phase 0 pass:** that pass stated "Existing Study
A" was not present anywhere in the repository or its git history. That was
an accurate statement about the repository's contents *at that time* — the
notebook was not committed and not discoverable — but Study A does exist
as separate prior work, now added. Its important, correct scope limit
(flagged per the task's own taxonomy in `EXISTING_WORK_AUDIT.md` §3): it
perturbs Vp **directly** at the elastic-model level, not via a processing
mechanism (no NMO/RMO, migration-velocity, or angle-error simulation
exists in it) — it must not be described as "processing-induced velocity
uncertainty," and it does not yet connect to the reservoir properties
(φ/Vsh/Sw) the rest of this PhD is about.

## 2. Reproducibility status

Not currently re-runnable as committed: no `environment.yml`, the
Smeaheia `.npz` is not in the repo, the `Seis2Rock` GitHub dependency is
cloned unpinned at run time, and no execution was attempted in this audit
(no GPU/data available in this session). Internal consistency is good for
the Seis2Rock baseline (matches to 3 decimals across both notebooks) but
**bad for the PetroNet baseline** (φ R²=0.956 vs. 0.991 between the two
notebooks, unflagged, unresolved) — this must be fixed before either
number is used in a paper.

## 3. Scientific strengths

- The full-trace, all-angle, exact-Zoeppritz seismic-consistency loss is a
  genuine physics-guided architecture, not a patched-together benchmark.
- The buffered spatial-CV correction and the Sw-permutation test are
  already, in embryonic form, exactly the leakage-audit and property-
  resolvability instincts this PhD needs — they should be formalized, not
  discarded.
- Limitations sections in both notebooks are unusually candid (inverse-
  crime risk, matched forward physics, asymmetric identifiability all
  already named by the notebooks' own authors/AI-assistance).
- Study A is a genuinely rigorous, independently-benchmarked piece of work
  (its own validation cell reproduces a separate Mathematica notebook's
  outputs to 5 decimals) and already delivers one real, citable result:
  at Smeaheia, the AVO gradient B is ~14× more sensitive than the intercept
  A to a differential Vp error between caprock and reservoir, with Class
  III→IV misclassification possible at ~3–5% differential error.

## 4. Scientific weaknesses

Matched-forward-physics (inverse crime) inflates every existing R² number;
no uncertainty quantification exists on the flagship RWPGNN method itself
(only the comparison baseline has MC Dropout, which is epistemic-only);
the PetroNet cross-notebook inconsistency; no spatial-leakage-safe
evaluation of Seis2Rock itself (it has no train/test split at all); zero
existing code for amplitude-fidelity/wavelet/velocity uncertainty. Full
list in `EXISTING_WORK_AUDIT.md` §5.

## 5. Literature overlap (the headline finding of this Phase 0 pass)

A bounded (~15-query) literature scan found that the RW-PGNN paradigm name
and concept is **not new**: Vashisth & Mukerji (2022, *The Leading Edge*,
DOI 10.1190/tle41120840.1) already published "RW-PINN," a rock- and
wave-physics-informed neural network for porosity-only, normal-incidence
inversion with weak few-well supervision. More importantly, **the specific
target of the originally-scoped Objective 3/Paper 2 — a probabilistic,
uncertainty-aware, physics-guided petrophysical inversion network,
validated on real field (North Sea) data — already exists, twice, in
*Geophysics* (2024)**: Li, Liu, Alfarraj, Tahmasebi & Grana (geo2023-0214.1,
ABC-based uncertainty) and Li, Grana & Liu (geo2023-0737.1, variational-
inference Bayesian PINN). Both have field validation this repository's
existing work entirely lacks. Full classification of every proposed
contribution against this and eight other verified citations is in
`NOVELTY_LEDGER.md`.

**This does not kill the PhD.** It relocates the PhD's center of gravity.

## 6. Remaining gap / proposed novelty

What survives the literature gate, provisionally (see NOVELTY_LEDGER for
the full reasoning): an integrated **property-specific resolvability
framework** that (a) predicts, from rock-physics/AVA sensitivity and a
formal (not ad hoc) identifiability analysis, which of φ/Vsh/Sw should
degrade first under realistic AVA uncertainty; (b) tests that prediction
against a controlled, multi-source uncertainty degradation ladder
(velocity/RMO, wavelet, amplitude/noise) rather than only the rock-physics-
or weight-space uncertainty the existing 2024 literature already covers;
and (c) checks whether a physics-guided inversion's *calibration*
(coverage, CRPS, a rigorously pre-defined confident-error rate) actually
tracks that predicted resolvability, on both synthetic (Smeaheia) and — if
data permits — real (Volve) data. This is `NOVELTY_LEDGER.md` contribution
C4, the strongest candidate found, rated POTENTIALLY NOVEL, not yet
SUPPORTED.

## 7. Hypotheses

H1–H4 as given in the task description, unmodified, and entirely untested
by anything currently in the repository — full text in `RESEARCH_PLAN.md`.

## 8. Experiments required

Per `RESEARCH_PLAN.md`: (1) extend Study A one physical layer back — perturb
φ/Vsh/Sw and propagate through the existing Gassmann rock-physics model to
Vp/Vs/ρ and then to Shuey/Zoeppritz AVA attributes, rather than perturbing
Vp directly; (2) separately add the complementary, currently-absent
processing-induced mechanism (moveout/velocity-analysis error → AVO
gradient bias, anchored on Sarkar, Baumel & Larner 2002) — do not conflate
this with Study A's elastic-model-level mechanism; (3) extend to a full
rock-physics/AVA-class separability analysis for φ/Vsh/Sw; (4) build a
property-specific resolvability index from established methods (Fisher-
information-adjacent literature exists but no ready-made seismic-QI index
was found — this must be developed carefully, not invented arbitrarily, in
Phase 3); (5) re-scope Paper 2 around calibration + resolvability-linkage
after reading Li et al. (2024) ×2 and Wu et al. (2024) in full text
(unfinished in this pass — abstract-level access only); (6) a real Volve
data audit before any blind-well design is finalized.

## 9. Data required

Smeaheia `.npz` (used, unpinned, uncommitted) and Volve (prestack gathers,
angle stacks, wells with Vp/Vs/ρ/checkshots, horizons). Search evidence
suggests Volve's full-elastic-log well coverage may be as sparse as ~2
wells in some reported processing pipelines — **unverified against the
actual data room, flagged as a risk, not a fact**.

## 10. Risks and kill criteria

Full list in `RESEARCH_PLAN.md` §Risks. Headline risks: Paper 2 as
originally scoped may be mostly subsumed by Li et al. (2024) ×2 pending
full-text reading; Paper 3's blind-well design may be statistically
underpowered if Volve elastic-log coverage is as sparse as initial search
evidence suggests; H1–H3 may simply be false (Objective 1 might show φ,
Vsh, Sw do not degrade in the expected order) — this is a valid, reportable
outcome, not a failure of the project.

## 11. Three-paper architecture (revised)

Paper 1 (rock-physics/AVA resolvability) is now the load-bearing paper for
the novelty case. Paper 2 (uncertainty-aware inversion) is re-scoped around
calibration + resolvability-linkage specifically, not "a new probabilistic
PGNN." Paper 3 (Volve field validation) is unchanged in intent but gated on
a real data audit. Full detail in `RESEARCH_PLAN.md`.

## 12. Skills required

Rock physics (HM/Gassmann/Batzle-Wang — already used correctly, needs
teaching not re-deriving), Shuey/Aki-Richards vs. exact Zoeppritz, AVO
classes, NMO/RMO/velocity-error-to-AVO-gradient mechanics (new to this
codebase), sensitivity/identifiability analysis, variational inference/MC
dropout/ensembles (partially present), calibration metrics (coverage,
CRPS, reliability diagrams — entirely new to this codebase), well-log QC
and well-to-seismic tie for the Volve phase. Detail in `RESEARCH_PLAN.md`.

## 13. Immediate next 10 actions

See `RESEARCH_PLAN.md` §Immediate next 10 actions — headline items: (1)
user reviews this package; (2) confirm whether any further prior work
(a property-level sensitivity study, a processing/RMO study) exists beyond
Study A; (3) read the full text of the three closest 2024 Geophysics
papers before finalizing Paper 2's scope; (4) fix the PetroNet
cross-notebook inconsistency; (5) independently verify Volve data
availability against the real data room.

## STOP

Per the task's explicit instruction, no code has been changed, no notebook
has been modified, and no experiment has been launched. This report and
its three companion documents are the entire Phase 0 deliverable. Awaiting
review before Phase 1 begins.
