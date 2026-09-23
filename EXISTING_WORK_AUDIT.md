# Existing Work Audit

Date: 2026-09-11 (revised same day: Study A supplied by user and added below)
Scope: everything currently committed to this repository on `main` /
`claude/phd-qi-resolvability-framework-ou8o1u`. Nothing was modified to
produce this audit — it is read-only with respect to the pre-existing
notebooks; `Smeaheia_AVO_error_propagation.ipynb` (Study A) was added
verbatim, as supplied by the user, and is otherwise untouched.

## 0. What is actually in the repository

```
README.md                                        (1 line: "ML 592 KFUPM Term Project")
GEOP592_RWPGNN_FINAL.ipynb                        (54 cells, ~12 MB with embedded figures)
Seis2Rock_Complete_Project_with_ML_audit.ipynb    (48 cells, ~13 MB with embedded figures)
Smeaheia_AVO_error_propagation.ipynb              (23 cells, ~0.5 MB — Study A, added 2026-09-11)
```

`git log` shows a long history of iterative Colab notebook uploads and
deletions (e.g. `Physics_guided_RWPGNN_FIXED_4.ipynb`,
`Physics_guided_RWPGNN+Seis2Rock_.ipynb`, `Seis2Rock_AVORPINN_multip_fixed_train_val.ipynb`,
etc.) converging on the two notebooks above. Only these two survive on the
current branch; the deleted intermediates are recoverable from git history
if needed but are not treated as "current" work here.

**Newer copy of the RW-PGNN notebook (checked 2026-09-23).** A later version of
`GEOP592_RWPGNN_FINAL.ipynb` lives in `aleeseyon/GEOP592` (commit `6a5d942`,
2026-09-17; 65 cells vs 54 here). A source diff shows **no changes to the physics
cells** (rock physics, Zoeppritz, wavelet, loss). The additions are split-visualization,
coherence "divergence" plots and revised learning-curve plots. Its key printed results
match this copy: RW-PGNN to 4 decimals; PetroNet φ R² 0.9560 → 0.9582, which is
run-to-run nondeterminism. It also shows the synthetic is loaded from
`Seis2Rock/data/smeaheia_synthetic.npz`, i.e. it ships with the Seis2Rock repository.

**Correction to the original Phase 0 pass.** The first version of this
audit stated that "Existing Study A" did not exist anywhere in this
repository, based on a text search of the two notebooks that were present
at the time. The user has since supplied
`Smeaheia_AVO_error_propagation.ipynb` directly. It was not previously
committed to this repository or discoverable by searching it — the
original claim was correct as a statement about repository contents at
that time, but Study A does exist as separate prior work. It is audited in
§3 below and no longer treated as a gap in the PhD's existing portfolio,
though it does not yet connect to the reservoir-property (φ/Vsh/Sw)
resolvability question — see §3's "What it does NOT do" and the revised
`RESEARCH_PLAN.md`.

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

## 3. `Smeaheia_AVO_error_propagation.ipynb` — Study A (added 2026-09-11)

**What it does.** A self-contained (no external data file, no GPU) analytic
error-propagation study: how do independent relative errors in caprock and
reservoir P-wave velocity (r_ΔVp1, r_ΔVp2, each spanning ±10%) shift the
Shuey (1985) two-term AVO intercept A and gradient B at the Smeaheia top
reservoir (shale over CO₂-sand), and can that shift cause an apparent AVO
class change?

- **Model**: a single-interface, two-layer elastic model (caprock: Vp=2600,
  Vs=1200, ρ=2350; CO₂-sand: Vp=1950, Vs=1180, ρ=2030 m/s, kg/m³) built from
  the real Smeaheia CO₂-storage rock-physics literature (Gassmann fluid
  substitution with Batzle & Wang 1992 CO₂ properties, consistent with
  Fawad, Hansen & Mondol 2021, *IJGGC* 109). A brine-baseline case is
  carried alongside for reference.
- **Method**: `sympy` symbolic differentiation of the exact Shuey
  (Wiggins/Castagna–Backus 1993 parameterization) A, B (via the
  intermediate `BB` term), and C coefficients with respect to Vp1 and Vp2,
  converted to *relative*-error sensitivity coefficients k_A, k_B, k_C via
  r_ΔVp1/r_ΔVp2. This is a local (linearized) sensitivity analysis — the
  same conceptual object as a Jacobian/Fisher-information diagonal term,
  though the notebook does not use that language.
- **Validation (real, and correctly done):** Cell 8 reproduces six numeric
  outputs of a separate, pre-existing Mathematica notebook
  ("Error_propagation_from_VP_to_Shuey_2_and_3_terms") to 5 decimal places,
  using the Mathematica notebook's own model values — i.e. this Python
  implementation is an independently-checked port, not a from-scratch
  reimplementation of unknown correctness. This is exactly the kind of
  benchmark-against-a-known-source practice the task's coding-safety rules
  ask for.
- **Results (Smeaheia CO₂ case, verified in the notebook's own output):**
  baseline A₀=−0.214, B₀=−0.021 (Class III); sensitivity k_A=+2.23,
  k_B=−31.28, k_C=+3.43 — **the gradient B is ~14× more sensitive than the
  intercept A** to a differential Vp error. Common-mode errors (both layers
  shift the same way) cancel exactly in the linear theory, because A/B/C
  each propagate only the *differential* r_ΔVp1−r_ΔVp2 (a real, derivable
  property of the Shuey formulas, correctly shown symbolically). B is
  markedly nonlinear in the error (traced correctly to the impedance
  contrast sitting in the denominator of the `BB` term) — the linear k_B
  only holds within a few percent. **Class III → apparent Class IV
  misclassification occurs at ≈3–5% differential Vp error** (where the
  B=0 contour crosses the worst-case-error spoke), while the intercept A
  stays negative (bright-spot-on-stack character preserved) across the
  full ±10% grid explored.

**What kind of uncertainty this is — important classification, per the
task's own taxonomy.** This notebook perturbs the **elastic-model log
velocity** (Vp1, Vp2) directly, at the level of the two-layer Shuey
calculation itself. It does **not** simulate a processing mechanism
(NMO/RMO, migration-velocity error, or angle-estimation error) that would
*produce* such a Vp perturbation or an associated angle-dependent moveout
residual — there is no time/offset/moveout representation anywhere in the
notebook, only closed-form A/B(Vp1,Vp2). Per the task's explicit
instruction, this must **not** be described as "processing-induced
velocity uncertainty." It is an **elastic-model (rock-physics-level)
velocity-perturbation study**, directly analogous in spirit to a
petrophysical-parameter sensitivity study, but stopping one physical layer
short of full rock-physics: it perturbs Vp directly rather than perturbing
φ/Vsh/Sw and propagating through Gassmann to Vp. Sarkar, Baumel & Larner
(2002) — the moveout-error-into-AVO-gradient mechanism cited in the
original literature scan — is a *different*, complementary mechanism
(processing/velocity-analysis-induced) and is not implemented here.

**What it does NOT do (gaps relative to Objective 1):**
1. Does not connect Vp error back to the reservoir properties φ, Vsh, Sw
   (no rock-physics inversion direction; Vp is perturbed directly, not
   derived from perturbed φ/Vsh/Sw via Gassmann).
2. Perturbs Vp only — Vs and ρ are held fixed, so cross-parameter
   covariance (e.g., a Vp error correlated with a Vp/Vs or density error
   through the same rock-physics model) is not explored.
3. Uses the Shuey two-term (intercept/gradient) approximation at a single
   interface, not the full-trace, all-angle, exact Zoeppritz forward model
   used in `GEOP592_RWPGNN_FINAL.ipynb` — the two notebooks are not
   currently built on the same numerical forward model, though both use
   the same Smeaheia top-reservoir/CO₂ geological setting.
4. Does not touch the Smeaheia 2D property fields (`phi_2D`, `vsh_2D`,
   `sw_2D`) used by the other two notebooks — it is a single-interface,
   two-layer analytic case, not a 2D section.
5. Does not implement moveout/RMO, wavelet, or amplitude-fidelity
   uncertainty (consistent with the other two notebooks — none of the
   three notebooks currently touch these).

**Reproducibility:** High. No external data file, no GPU, no unpinned
external git dependency (only `numpy`, `sympy`, `matplotlib` — all
standard). The only soft dependency is `ffmpeg` for the Cell 18 animation
(`FFMpegWriter`); if `ffmpeg` is unavailable the notebook would fail at
that cell even though every quantitative result (Cells 8, 10, 12, 15, 20)
is unaffected. No `environment.yml` yet, consistent with the rest of the
repo.

**Stated limitations (from the notebook's own §8 summary, verbatim in
substance):** all conclusions are specific to the Smeaheia top-reservoir
baseline (A₀, B₀ near the Class III/IV boundary make it unusually
sensitive); the sign and magnitude of k_B depend on the baseline and the
polarity of the impedance contrast — the original Mathematica case (a
different, Class-IV-ish baseline) shows opposite-sign but similar-order-
of-magnitude sensitivity, so the *specific* numbers do not generalize
beyond Smeaheia without redoing the derivative evaluation at the new
baseline.

## 4. Reproducibility status

| Item | Status |
|---|---|
| Code runs top-to-bottom | Not verified in this audit — no execution was attempted (no GPU, no `smeaheia_synthetic.npz` present in repo; the notebooks assume Colab + manual upload). **Cannot currently be re-run as committed.** |
| Random seeds | Fixed (`torch.manual_seed(42)`) in the base runs; Part 2.8 patches per-seed reproducibility via monkey-patch because `train_RWPGNN` hardcodes seed 42 internally — flagged in-notebook as a real limitation ("Bit-exact reproducibility holds only on the same GPU+CUDA+cuDNN combination"). |
| Data provenance | Smeaheia synthetic `.npz` is not committed to the repo (must be uploaded manually per the notebook header) — **no `data/README.md` or checksum exists**, so the exact dataset version cannot currently be verified independently of the notebook's own printed ranges. |
| Cross-notebook consistency | Seis2Rock numbers match to 3 decimals between both notebooks (good). PetroNet/Cascaded numbers do NOT match between the two notebooks (bad — different train/test protocol, not flagged). |
| Dependency on external package | Both notebooks `git clone` the `DeepWave-KAUST/Seis2Rock` GitHub repo at run time — an unpinned external dependency; no version/commit hash is pinned, so results could silently drift if that repo changes. |
| Environment file | None (`requirements.txt`/`environment.yml` absent). |
| Tests | None. No unit test for the Zoeppritz implementation, the rock-physics chain, or the forward operator beyond the single in-notebook gradient-flow sanity check and the syn-vs-obs sanity check at the training well. Study A is the exception: its Cell 8 IS a real, passing benchmark test against an independent (Mathematica) implementation. |

## 5. Scientific strengths (worth preserving, not rewriting)

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
5. Study A's symbolic-derivative-plus-independent-benchmark method is a
   genuinely rigorous, correctly-validated piece of work and directly
   quantifies a real, citable geophysical result (gradient B ~14× more
   Vp-error-sensitive than intercept A, at Smeaheia) that Objective 1 can
   build on rather than re-derive.

## 6. Scientific weaknesses / open risks

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
6. **No amplitude-fidelity, wavelet, or processing-induced (NMO/RMO,
   migration-velocity, angle-estimation) uncertainty exists in any of the
   three notebooks** (confirmed by text search) — Objective 2 has zero
   existing implementation of these specific mechanisms to build on.
   Elastic-model-level Vp-error propagation into Shuey A/B (Study A) does
   now exist and is a useful starting point, but is a different
   mechanism (see §3) and does not by itself cover processing-induced
   uncertainty.
7. **Study A does not connect to reservoir properties (φ/Vsh/Sw) or to the
   full-trace exact-Zoeppritz forward model used by the RWPGNN notebook.**
   Closing this gap — rock-physics-level φ/Vsh/Sw perturbation → Vp/Vs/ρ →
   Shuey/Zoeppritz AVA sensitivity → resolvability — is now the concrete,
   well-scoped first task for Objective 1, rather than an open-ended
   "build from scratch."
