# Research Plan (Phase 0 output — provisional, pending user review)

This plan reflects the audit in `EXISTING_WORK_AUDIT.md` and the literature
gate in `NOVELTY_LEDGER.md`. It revises the master prompt's framing where
the audit changed the picture (see "Changes from the original framing"
below) rather than restating it unchanged.

## Changes from the original framing

1. **Study A exists and has been added to the repository**
   (`Smeaheia_AVO_error_propagation.ipynb`, supplied by the user after the
   first Phase 0 pass, which had incorrectly found no trace of it). It is a
   validated, symbolic (sympy) Vp-error → Shuey A/B sensitivity analysis at
   the Smeaheia top reservoir, benchmarked to 5 decimals against an
   independent Mathematica implementation. Per the master prompt's own
   caution, it is an **elastic-model-level Vp perturbation** study, not a
   processing-induced (NMO/RMO/migration-velocity/angle-error) uncertainty
   study — no moveout or time/offset representation exists in it. Full
   detail in `EXISTING_WORK_AUDIT.md` §3 and `NOVELTY_LEDGER.md` C7. The
   task ahead is **extension, not construction**: propagate perturbations
   in φ/Vsh/Sw (not Vp directly) through the same Gassmann rock-physics
   model already used in the other two notebooks, so Study A's sensitivity
   result is stated in terms of the actual reservoir properties this PhD
   is about.
2. **Objective 3 is narrower than originally scoped.** Li et al. (2024,
   Geophysics ×2) already publish field-validated probabilistic/Bayesian
   physics-guided petrophysical inversion. Objective 3 must center on
   calibration + resolvability-linkage + controlled multi-source
   degradation, not on "build a probabilistic PGNN" as such (see
   NOVELTY_LEDGER C5).
3. **RW-PGNN's name/paradigm is not the contribution.** Vashisth & Mukerji
   (2022) already own "rock- and wave-physics-informed NN." Existing
   notebooks should be relabeled internally as "the RW-PGNN prototype" (a
   baseline research tool this PhD builds on and stress-tests), not as
   itself the finding.
4. **A cross-notebook baseline inconsistency (PetroNet φ R² 0.956 vs 0.991
   between the two notebooks) must be resolved before Phase 1 reproduction
   is considered complete.**

## Central research question (unchanged, and it survives the audit)

*Which reservoir properties does prestack seismic genuinely constrain under
realistic uncertainty, and can quantitative inversion recognize when the
information required for a particular reservoir prediction is no longer
sufficient?*

## Hypotheses (unchanged from task description; still falsifiable, still not yet tested)

H1–H4 as stated in the task description. None are supported or refuted by
anything in this repository yet — no resolvability or uncertainty-
degradation experiment has been run. Treat them as fully open.

## Three-paper architecture (revised emphasis)

**Paper 1 — load-bearing.** Rock-physics and AVA controls on property
resolvability. This is now the paper the PhD's novelty case most depends
on (NOVELTY_LEDGER C4). Study A already provides a validated Vp→Shuey-A/B
sensitivity result at Smeaheia (NOVELTY_LEDGER C7) and should be preserved,
cited, and **extended** — not rebuilt — in two directions: (a) push the
perturbation one physical layer back, from Vp directly to φ/Vsh/Sw through
Gassmann, so sensitivity is stated in the properties the thesis is about;
(b) add the complementary, currently-absent processing-induced mechanism
(moveout/velocity-analysis error → AVO gradient bias, anchored on Sarkar,
Baumel & Larner 2002) as a second, distinct uncertainty source alongside
the elastic-model-level one Study A already covers — the two must not be
conflated (see EXISTING_WORK_AUDIT.md §3). Only after both are in hand
should this move to a formal property-specific resolvability metric (built
from first principles — Objective 1's instruction not to "invent an
arbitrary index" before investigating established methods still stands).

**Paper 2 — re-scoped.** Not "a new probabilistic PGNN" (largely done by
Li et al. 2024). Instead: does a physics-guided inversion's predictive
uncertainty (i) calibrate correctly under a controlled AVA-uncertainty
ladder, and (ii) track the resolvability Paper 1 predicts? This reframes
the existing RW-PGNN prototype as the test article, not the deliverable.
Requires reading the full text of Li et al. (2024) ×2 and Wu et al. (2024)
before finalizing scope (see Immediate Next Actions).

**Paper 3 — field validation, contingent on data audit.** Volve blind-well
test of Papers 1–2's findings. Search evidence suggests full elastic
(Vp/Vs/ρ) + petrophysical log coverage may be as sparse as ~2 wells in
some processing pipelines — if confirmed, this constrains (but does not
kill) Paper 3: it may need to be framed around 1–2 blind wells with
explicit small-sample caveats, or supplemented by a second open field
dataset. **A real DATA_AUDIT.md against the actual Volve data room (not
just literature descriptions of it) is a Phase-1/pre-Phase-6 gating task.**

## Phases (per task spec, unchanged structure; Phase 0 is this deliverable)

- Phase 0 (this report) — audit, literature gate, plan. **STOP for review.**
- Phase 1 — reproduce existing notebooks in a controlled environment;
  resolve the PetroNet inconsistency; pin the Seis2Rock dependency version;
  add `environment.yml`; add `data/README.md` documenting the Smeaheia
  `.npz` provenance and a checksum.
- Phase 2 — rock-physics/QI foundation notebooks (00–03 in the master
  prompt's numbering), including extending Study A: (a) φ/Vsh/Sw → Gassmann
  → Vp/Vs/ρ → Shuey/Zoeppritz sensitivity chain, and (b) a new,
  complementary processing-induced (moveout/velocity-analysis) uncertainty
  notebook anchored on Sarkar, Baumel & Larner (2002).
- Phase 3 — property-resolvability experiments (Objective 1 formalized).
- Phase 4 — uncertainty-aware inversion, re-scoped per Paper 2 above.
- Phase 5 — synthetic benchmark integrating Phases 3–4.
- Phase 6 — Volve field validation, gated on a real DATA_AUDIT.md.
- Phase 7–9 — manuscripts, thesis integration, defense prep.

Each phase ends with a decision report before proceeding, per the task
spec. Nothing beyond Phase 0 is started here.

## Data required (status as currently known — all "verify" items are unresolved)

| Item | Status |
|---|---|
| Smeaheia synthetic `.npz` | Used throughout both notebooks; not committed to repo; provenance/version not pinned |
| Volve prestack gathers, angle/offset info, near/mid/far stacks | Reported to exist (ST0202/ST10010, PSDM-processed) — verify directly, do not trust this summary |
| Volve wells with Vp+Vs+ρ+checkshots | Reported possibly as few as ~2 wells with full elastic+petrophysical logs; most wells reportedly lack Vs — **verify against the actual data room before committing Paper 3 to a blind-well design** |
| Volve horizons/faults/production data | Not checked in this pass |

## Risks and kill criteria

- **Kill Paper 2 as scoped** if full-text reading of Li et al. (2024) ×2
  shows they already report calibration diagrams / confident-error rates
  tied to resolvability — then Paper 2 must pivot to a narrower gap or be
  dropped in favor of expanding Paper 1.
- **Kill/redesign Paper 3's blind-well design** if Volve elastic-log
  coverage is confirmed at ≤2 wells — a single-digit-well blind test has
  limited statistical power and must be presented with that caveat, or a
  second field dataset sought.
- **Kill H1–H3 as stated** if the resolvability index (once built, per
  Objective 1) does not predict the *order* in which φ/Vsh/Sw degrade
  under the uncertainty ladder — report as a negative result per the
  task's Negative Results policy, do not re-engineer the index until it
  agrees with expectation.

## Skills needed before each phase (abbreviated; full three-level teaching happens in-notebook per phase)

- Phase 2: Hertz-Mindlin/Gassmann/Batzle-Wang rock physics (already used
  correctly in existing notebooks — needs explanation, not re-derivation);
  Shuey/Aki-Richards approximations vs. exact Zoeppritz; AVO classes;
  symbolic sensitivity analysis (already demonstrated correctly in Study
  A — needs extending to φ/Vsh/Sw via Gassmann, not re-deriving). Phase 2
  also needs, as new material: NMO/RMO mechanics and stacking-velocity
  error propagation into the Shuey gradient (Sarkar, Baumel & Larner 2002)
  — this is the processing-induced mechanism Study A does not cover.
- Phase 3: sensitivity analysis, Fisher information basics, nonuniqueness/
  crossplot separability.
- Phase 4: variational inference / MC dropout / ensembles basics (already
  partially used); calibration metrics (coverage, CRPS, reliability
  diagrams) — new to this codebase, needs to be taught from scratch.
- Phase 6: well-log QC, well-to-seismic tie, Volve-specific processing
  history literacy.

## Immediate next 10 actions (in order)

1. User reviews this Phase 0 package (`PHASE0_REPORT.md` + this file +
   `EXISTING_WORK_AUDIT.md` + `NOVELTY_LEDGER.md` +
   `literature/novelty_matrix.csv`) and either confirms or redirects scope.
2. Study A is now in the repository (`Smeaheia_AVO_error_propagation.ipynb`)
   — confirm with the user whether any other prior work (e.g. a
   petrophysical-property-level sensitivity study, or a processing/RMO
   study) exists before assuming Objective 1 starts from Study A alone.
3. Read the full text (not abstracts) of Li et al. (2024, geo2023-0214.1),
   Li et al. (2024, geo2023-0737.1), and Wu et al. (2024, geo2023-0135.1)
   — this is required before Paper 2's scope can be finalized, and is
   explicitly flagged as unfinished in this Phase 0 pass.
4. Resolve the PetroNet cross-notebook inconsistency (pick one canonical
   train/test protocol and re-run both baselines under it).
5. Pin the `DeepWave-KAUST/Seis2Rock` dependency to a specific commit hash;
   add `environment.yml`.
6. Write `data/README.md` for the Smeaheia `.npz` (provenance, checksum,
   units, coordinate convention).
7. Independently verify Volve prestack + well-log availability against the
   actual Equinor data room (not literature summaries) and write a real
   `DATA_AUDIT.md`.
8. Do a full systematic literature search (not the ~15-query bounded scan
   done here) before any manuscript claims novelty, per the task's
   Literature Review Protocol.
9. Design the Study A + Objective 1 experiment plan in detail (hypothesis,
   independent/dependent variables, controls, seeds) before writing code,
   per the Statistical Discipline section of the task instructions.
10. Only after 1–9: begin Phase 1 (reproduction) notebooks.
