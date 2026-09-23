# Chapter 1 — run summary

## ASSUMPTIONS
- **A1. "Shuey-linear" threshold.** Taken to mean the threshold from the notebook's two-term Shuey engine, evaluated nonlinearly with σ = σ(V_P). This is the engine behind the 4.4 % statement.
- **A2. Exact-Zoeppritz gradient.** An exact gradient is not unique, so two are reported:
  - the tangent ∂R_PP/∂sin²θ at θ = 0 (the like-for-like comparison with Shuey), taken from a degree-6 fit in sin²θ over 0–20°;
  - a two-term least-squares fit over 0–30°, with an aperture scan from 20° to 40°.
- **A3. Second Zoeppritz implementation.** The explicit Aki & Richards (1980) eq. 5.39 form is compared with a numerical 4×4 solve, plus PyLops 2.8.0 and bruges 0.5.4.
- **A4. Perturbations.** Only V_P is perturbed; V_S and ρ are held fixed, as in the notebook.
- **A5. Manuscript format.** GEOPHYSICS conventions: ≤250-word abstract (236), capitalised section heads, SEG reference style. DOIs are left for submission-time verification.
- **A6. Reference PDF.** Hema et al. (2027) is a scanned PDF. Table values were transcribed from page images and need proof-reading against the original.
- **A7. Added references.** Two were added and checked for existence: Aki & Richards (1980) and Zoeppritz (1919). Hema et al. (2027) was supplied by you.

## COMPLETED
1. **Notebook reproduction.** The original notebook runs unmodified, and every printed output reproduces bit-for-bit (A₀ = −0.2137, B₀ = −0.0211, k_A = +2.233, k_B = −31.277, k_C = +3.429, and the Mathematica validation).
2. **Exact Zoeppritz, two implementations.** Validation results:
   - matrix vs explicit: ≤1.9e-15;
   - normal incidence: ≤1.7e-16;
   - energy conservation: ≤7.8e-16;
   - PyLops: ≤5.4e-16;
   - bruges: ≤1.3e-15.

   The post-critical case is included.
3. **Threshold cross-check** (|r| = error-vector magnitude):

   | | Shuey | Zoeppritz tangent | Zoeppritz LSQ 0–30° |
   |---|---|---|---|
   | along φ = 135° | 4.752 % | 5.755 % | 8.455 % |
   | minimum over φ | 4.444 % (156.6°) | 5.580 % (149.2°) | 8.225 % (148.5°) |

   **Finding:** the Class III→IV crossing is physical. Its location is biased low by Shuey: the Shuey threshold is 17.4 % low along 135° and 20.4 % low at closest approach. With a practical two-term fit, the threshold depends on aperture: 7.0 % (0–20°) up to no crossing within 10 % (0–40°). The Shuey crossings for reservoir-only (90°) and common-mode (225°) errors are artifacts.
4. **Deliverables.**
   - `chapter1_extended.ipynb` (§9 plus an audit note)
   - `chapter1_manuscript_draft.md`
   - `chapter1_numbers.json`
   - figures: `fig_rpp_baseline.png`, `fig_B0_contours.png`, and `fig_AB_slices.png` / `fig_GI_map.png` exported from the notebook

## FLAGGED FOR REVIEW
- **F1. "4.4 % along the 135° spoke" does not reproduce as stated.** 4.44 % is the *minimum* radius of the Shuey B = 0 contour, reached at φ = 156.6°. Along 135° the crossing is at 4.75 %. The task's phrase "4.4 % differential error" is also ambiguous: |r| = 4.44 % corresponds to r₁ − r₂ = −5.84 %. The manuscript reports both values explicitly and does not use 4.4 % for the 135° spoke.
- **F2. k_B = −31.28 is a fixed-Poisson's-ratio derivative.** `spr` and `dpr` are held constant in `sp.diff`. The total derivatives are dB/dlnV_P1 = −0.405 (vs +0.660 at fixed σ, so the sign flips) and dB/dlnV_P2 = +0.111. As a result, **common-mode errors do not cancel in B**, contrary to notebook §7/§8. It also means §8 item 2 ("1 % differential error shifts B by ~30 %") is a fixed-σ statement.
- **F3. The §7 text says the 315° spoke reaches B ≈ −0.055; the computed value is −0.0351.** The −0.0554 value belongs to φ = 0°.
- **F4. The notebook's Fawad et al. (2021) citation ("Fawad, Hansen & Mondol, IJGGC 109, 103378") could not be verified.** The verified Smeaheia papers are:
  - Fawad, Rahman & Mondol (2021a), *J. Pet. Sci. Eng.* 205, 108812 — used in the manuscript;
  - Fawad, Rahman & Mondol (2021b), *The Leading Edge* 40(4), 254–260.

  Both are cited by Hema et al. Please confirm which paper was intended.
- **F5. The model brine-sand V_P = 2200 m/s is below the minimum Sognefjord log V_P in both wells** (2436 m/s in 32/2-1, 2748 m/s in 32/4-1; mean offset −19 % / −26 %, per Hema et al. Tables 1–2). The model was left unchanged as instructed. The absolute thresholds are therefore those of a soft-sand end member, not calibrated Smeaheia values.
- **F6. Notebook provenance says the CO₂ properties come from "Batzle & Wang (1992)", but that paper does not give a CO₂ equation of state.** CO₂ properties are usually taken from Span & Wagner (1996); that reference was not verified and is not added. Please confirm how the CO₂ sand was derived.
- **F7. The original notebook classifies the brine reference as "IIp / II–III boundary", but its computed values put it in Class IV** (A = −0.127, B = +0.0023: A < 0 and B > 0). The text was not edited.
- **F8. Scope.** The framework covers errors in the elastic model's V_P. It does not model processing-velocity errors, which act through angle mis-assignment. The Introduction motivates the study partly through "AVO-compliant processing", and the Discussion states this limitation. Please decide whether the framing should be narrowed.
- **F9. Environment.** ffmpeg was not installed. A static ffmpeg (imageio-ffmpeg) was linked so the original animation cell could run; the notebook code was not changed.
