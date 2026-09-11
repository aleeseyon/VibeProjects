# Existing Work Audit

Date: 2026-09-11
Scope: everything currently committed to this repository on `main` /
`claude/phd-qi-resolvability-framework-ou8o1u`. Nothing was modified to
produce this audit — it is read-only.

## 0. What is actually in the repository

```
README.md                                        (1 line: "ML 592 KFUPM Term Project")
GEOP592_RWPGNN_FINAL.ipynb                        (54 cells, ~12 MB with embedded figures)
Seis2Rock_Complete_Project_with_ML_audit.ipynb    (48 cells, ~13 MB with embedded figures)
```

`git log` shows a long history of iterative Colab notebook uploads and
deletions (e.g. `Physics_guided_RWPGNN_FIXED_4.ipynb`,
`Physics_guided_RWPGNN+Seis2Rock_.ipynb`, `Seis2Rock_AVORPINN_multip_fixed_train_val.ipynb`,
etc.) converging on the two notebooks above. Only these two survive on the
current branch; the deleted intermediates are recoverable from git history
if needed but are not treated as "current" work here.

**Important scope correction.** The task description refers to a preliminary
"Existing Study A" — a velocity-perturbation → Shuey A/B coefficient
experiment. **No such notebook, script, or figure exists anywhere in this
repository or its git history.** I searched both notebooks' full text for
`Shuey`, `velocity perturbation`, `RMO`, and `migration velocity` — the only
hits are unrelated variable names (`PoststackLinearModelling`'s `nt0`
argument, coincidentally matched by a bad regex). If Study A exists, it is
either in a different repository, a local/uncommitted file, or was described
conceptually but not yet implemented. **Treat Study A as NOT YET PART OF
THIS CODEBASE** until the user supplies it. The PHASE0_REPORT reflects this
as a gap, not an oversight on my part.

## 1. `Seis2Rock_Complete_Project_with_ML_audit.ipynb` — the earlier stream

**What it does, in order:**

- **Part 0–1**: Loads the Smeaheia synthetic dataset (φ, Vsh, Sw, depth,
  x_axis; 225×174 grid, 3500–6000 m depth). Exactly replicates Corrales,
  Hoteit & Ravasi (2024) "Seis2Rock": Hertz-Mindlin + Gassmann + Batzle-Wang
  rock physics → Zoeppritz AVO gather (PyLops) → SVD of the
  background-subtracted gather (p=5 basis functions, captures ~100% of
  energy) → Laplacian-regularized post-stack-style inversion of
  petrophysical reflectivities.
  **Result (reproduced):** φ RMSE=0.0222, R²=0.933; Vsh RMSE=0.0879,
  R²=0.947; Sw RMSE=0.0603, R²=0.947.
- **Part 2 — AVONet**: A 2D CNN over 45-angle × 41-depth-sample patches,
  predicting a single (φ, Vsh, Sw) triple at the patch centre, with a PINN
  loss comparing forward-modeled seismic (HM+Gassmann decoder, **flat/
  constant-φ-per-patch** approximation) against observed data. Trained with
  1 well.
- **Part 2.5 — well-count sweep**: N ∈ {1,2,4,8,16} training wells. AVONet
  **never catches Seis2Rock** in this notebook (best φ R²=0.874 at N=16 vs.
  Seis2Rock 0.933, Δ=−0.060). This is the opposite qualitative conclusion
  from the companion GEOP592 notebook (see below) — the difference is the
  architecture (patch CNN + flat-φ decoder vs. full-trace CNN + exact
  layered Zoeppritz), not a contradiction in either result.
- **Part 2.6 — "ML Audit"** (the most methodologically valuable section):
  systematically re-examines the Part 2 pipeline for exactly the failure
  modes this PhD is designed to study:
  1. Train-only normalization (was previously computed globally).
  2. Interleaved-every-5th split → spatially contiguous 60/20/20 block
     split.
  3. PINN loss silently falling back to leaking ground-truth φ at non-well
     traces when a batch had no well sample — **found and fixed**.
  4. AVO context-window sweep WIN∈{1,5,41}: **WIN=1 is architecturally
     impossible** for AVONet (MaxPool2d collapses the depth dimension to
     0) — reported as a finding, not patched.
  5. Buffered 5-fold spatial CV (Roberts et al. 2017; Ploton et al. 2020):
     φ R²=0.769±0.018, Vsh R²=0.866±0.014, Sw R²=0.680±0.076 — **large
     fold-to-fold variance, explicitly flagged as evidence of limited true
     spatial generalization**.
  6. **Sw label-permutation test**: shuffling training Sw labels destroys
     81% of test-set Sw R² (baseline 0.602 → permuted 0.118, "19.57%
     survives") — i.e. most of AVONet's apparent Sw skill is genuine AVO
     signal, not exploited correlation with φ/Vsh. This is, in effect, an
     early, informal property-resolvability/identifiability probe and is
     directly relevant to Objective 1.
  7. CO₂ (Sw<0.5) binary classification head added alongside regression:
     ROC-AUC=0.924, PR-AUC=0.750 vs. a derived classifier thresholding the
     regression Sw at 0.5 (ROC-AUC=0.892) — classification head modestly
     better.
- **Part 3 — Das & Mukerji (2020) baselines**: PetroNet (end-to-end CNN) and
  Cascaded (ElasticNet→ElasticPetroNet), trained on **all-trace** synthetic
  labels (not realistic — every trace supervised), MC Dropout (p=0.10, 50
  passes) for epistemic UQ.
- **Part 4 — 5-method comparison** on identical test traces: Seis2Rock,
  AVONet (1-well, 2-well), PetroNet, Cascaded. PetroNet/Cascaded dominate
  (φ R²=0.991/0.982) because they are trained on all-trace labels, which is
  an unfair advantage not controlled for in this notebook's final table —
  **this inconsistency is not flagged in the notebook itself and should be
  in the audit going forward.**

**Stated limitations (from the notebook's own summary cell):** single-
property decoder (background Vsh/Sw fixed inside the physics constraint),
synthetic-only, amplitude fidelity (NMO stretch, migration, gain) not
modeled, MC Dropout = epistemic only.

## 2. `GEOP592_RWPGNN_FINAL.ipynb` — the more mature stream

This is the notebook the task description calls "the RW-PGNN notebook." It
supersedes the AVONet architecture with a full-trace approach and is
substantially more careful about forward-model consistency and leakage.

- **Part 1**: Identical Seis2Rock replication (φ R²=0.933, Vsh R²=0.948,
  Sw R²=0.947 — matches the companion notebook to 3 decimal places, good
  sign of internal consistency).
- **Part 2 — trace-level RWPGNN**: A dilated 1D CNN (4 blocks, 64 channels,
  dilation 2^k, GroupNorm, GELU, dropout 0.10; **73,603 parameters**) that
  ingests a full (35-angle × 225-depth) gather and outputs (φ, Vsh, Sw) at
  **every depth sample** via sigmoid heads denormalized to physical ranges.
  The forward operator (`TraceForwardOperator`) is a **differentiable,
  exact analytic layered Zoeppritz PP** implementation (complex-valued to
  handle post-critical angles; Aki & Richards 2002 Box 5.1 / Sheriff &
  Geldart 1995 eq. 3.20a closed form), driving a full-trace, all-angle
  seismic-consistency loss `Ls`, plus a supervised well loss `Lw`
  (variance-normalized per property) and a Tikhonov first-difference
  smoothness term `Lr`.
  **Verified in-notebook**: forward-operator sanity check at the training
  well gives syn-vs-obs RMSE/amplitude ratio = 0.000% — i.e. the forward
  operator and the Zoeppritz data generator are numerically identical.
  This is explicitly and correctly acknowledged in the notebook as **the
  same forward model used to generate the data** — a matched-physics
  ("inverse crime") setup, not an independent validation of the forward
  operator.
- **Part 2.5 — well-count sweep** (N∈{1,2,4,8,16,100,174}, single seed,
  interleaved every-5th holdout): RWPGNN **beats Seis2Rock at every N≥1**,
  including Sw (Seis2Rock Sw R²=0.947; RWPGNN N=1 gives only 0.806, but
  N=16 already reaches 0.985, N=174 reaches 0.997).
- **Part 2.8 — buffered, 3-seed well-count sweep**: repeats the sweep with
  a spatial buffer (B=13 traces, the empirical 1/e lateral autocorrelation
  length of the property fields) between train/val/test blocks and 3 random
  seeds. **Qualitative conclusion survives**: crossover N* (smallest N at
  which RWPGNN mean φ R² ≥ Seis2Rock) is still N*=1 under the stricter
  protocol, though absolute R² at low N drops slightly relative to the
  interleaved split (e.g. N=1: 0.956→0.963 mean, i.e. actually *higher*
  here — seed variance dominates at low N, exactly as the notebook's own
  caveat states).
- **Part 3–4**: Same Das & Mukerji baselines and 4-method comparison as
  above, this time with PetroNet at φ R²=0.956 (RWPGNN N=174: 0.990,
  Seis2Rock: 0.931) — **note this contradicts the companion notebook's
  PetroNet φ R²=0.991**, because the two notebooks use different Das &
  Mukerji training conventions (all-trace vs. matching RWPGNN's
  train/test split). **This inconsistency between the two notebooks is a
  reproducibility issue that must be resolved (state one canonical
  PetroNet protocol) before PetroNet is used as a citable baseline number.**

**Stated limitations (from the notebook's own summary — verbatim, this is
already an honest and usable limitations list):** synthetic-only;
forward-model-in-the-loss = data-generating forward model (matched
physics); constant-angle gather convention (no true ray-traced angle
gathers); amplitude fidelity (NMO stretch, migration, gain) unmodeled;
stationary 20 Hz Ricker wavelet (no wavelet uncertainty); UQ is partial
(RWPGNN itself is a point estimator — only the Das & Mukerji MC-Dropout
baseline has any UQ, and that is epistemic-only); property identifiability
is asymmetric (φ has the strongest AVO sensitivity in this rock-physics
regime, Vsh/Sw rely more on the well-supervision term at low N).

## 3. Reproducibility status

| Item | Status |
|---|---|
| Code runs top-to-bottom | Not verified in this audit — no execution was attempted (no GPU, no `smeaheia_synthetic.npz` present in repo; the notebooks assume Colab + manual upload). **Cannot currently be re-run as committed.** |
| Random seeds | Fixed (`torch.manual_seed(42)`) in the base runs; Part 2.8 patches per-seed reproducibility via monkey-patch because `train_RWPGNN` hardcodes seed 42 internally — flagged in-notebook as a real limitation ("Bit-exact reproducibility holds only on the same GPU+CUDA+cuDNN combination"). |
| Data provenance | Smeaheia synthetic `.npz` is not committed to the repo (must be uploaded manually per the notebook header) — **no `data/README.md` or checksum exists**, so the exact dataset version cannot currently be verified independently of the notebook's own printed ranges. |
| Cross-notebook consistency | Seis2Rock numbers match to 3 decimals between both notebooks (good). PetroNet/Cascaded numbers do NOT match between the two notebooks (bad — different train/test protocol, not flagged). |
| Dependency on external package | Both notebooks `git clone` the `DeepWave-KAUST/Seis2Rock` GitHub repo at run time — an unpinned external dependency; no version/commit hash is pinned, so results could silently drift if that repo changes. |
| Environment file | None (`requirements.txt`/`environment.yml` absent). |
| Tests | None. No unit test for the Zoeppritz implementation, the rock-physics chain, or the forward operator beyond the single in-notebook gradient-flow sanity check and the syn-vs-obs sanity check at the training well. |

## 4. Scientific strengths (worth preserving, not rewriting)

1. The full-trace, all-angle, exact-Zoeppritz seismic-consistency loss in
   GEOP592 is a genuine, non-trivial physics-guided architecture — it is
   not a "Frankenstein benchmark" (the notebook's own, correct, self-
   criticism of the earlier patch-based AVONet design).
2. The buffered spatial-CV correction (Part 2.8) and the Sw label-
   permutation test (Part 2.6) are exactly the right instincts for a QI
   PhD — they are early, informal versions of the leakage-audit and
   property-resolvability questions this PhD should formalize.
3. Limitations sections in both notebooks are already unusually honest
   (explicitly naming inverse-crime risk, matched-physics, asymmetric
   identifiability) — this lowers the risk of the PhD being built on
   self-deceived baselines.
4. Comparison against two independently published baselines (Seis2Rock,
   Das & Mukerji/PetroNet) rather than only against a self-built strawman.

## 5. Scientific weaknesses / open risks

1. **Matched-forward-physics (inverse crime).** The single most important
   weakness: RWPGNN's forward operator is bit-identical to the Smeaheia
   data generator. Every R² number in Parts 2/2.5/2.8/4 is therefore an
   upper bound under idealized conditions, not evidence of real-world
   resolvability. This is exactly Objective 2/3's job to break.
2. **Naming/paradigm precedent.** "RW-PGNN" (rock- and wave-physics-guided
   neural network) is not a new paradigm name: Vashisth & Mukerji (2022,
   *The Leading Edge*) already published "RW-PINN" (rock and wave physics
   informed neural network) for porosity-only, normal-incidence inversion.
   See `literature/novelty_matrix.csv`.
3. **No uncertainty quantification on the flagship method.** RWPGNN itself
   is a deterministic point estimator; only the Das & Mukerji comparison
   baseline has (epistemic-only) MC Dropout. The PhD's own Objective 3 is
   therefore not yet represented anywhere in the current code.
4. **Cross-notebook baseline inconsistency** (PetroNet φ R² 0.956 vs.
   0.991) must be resolved before any baseline number is quoted in a
   paper.
5. **No spatial-leakage-safe evaluation of Seis2Rock itself** — the
   Seis2Rock SVD "has no train/test split" (explicitly noted in-notebook)
   and is evaluated on the full section including well locations, while
   RWPGNN is evaluated only on held-out traces. This is an apples-to-
   oranges comparison baked into every current benchmark table.
6. **No amplitude-fidelity, wavelet, or velocity/RMO uncertainty exists in
   the code at all** (confirmed by text search) — Objective 2 has zero
   existing implementation to build on; it starts from scratch.
7. **Study A (velocity → Shuey A/B) does not exist in this repository.**
