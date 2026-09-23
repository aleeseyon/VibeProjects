# Hema, Maurya, Kant & Singh (2027) — Smeaheia field inversion

**Citation.** Hema, G., Maurya, S.P., Kant, R. & Singh, A.P. (2027). Seismic inversion
driven reservoir characterization and subsurface property prediction in the Smeaheia
Field, northern North Sea: Implications for CO₂ storage. *Geoenergy Science and
Engineering* 268, 214769. doi:10.1016/j.geoen.2026.214769 (received 23 Dec 2025,
accepted 20 Aug 2026, online 25 Aug 2026).

Read in full from the PDF supplied by the user (30 pages, image-only scan; read visually).
Numbers below are transcribed from the paper's tables; check against the original before
quoting them.

## What they did

| Item | Content |
|---|---|
| Data | GN1101 3D **post-stack** seismic (Gassnova, 2011, to 5000 ms TWT); wells 32/4-1 (Alpha, 1996, TD 3199 m) and 32/2-1 (Beta, 2008, TD 1238 m), ~15 km apart, both **dry** |
| Logs | GR, density, sonic (Vp), resistivity, neutron (32/2-1 only); derived AI, GR-based Vclay, density porosity. **No shear logs are reported.** |
| Inversion | Post-stack model-based inversion (Hampson-Russell); statistical wavelet; low-frequency model interpolated from **both** wells along horizons |
| Property prediction | Multi-attribute regression (MAR) and a GRNN-type "probabilistic" neural network (PNN) predicting Vp, density, porosity; leave-one-well-out cross-validation (2 wells) |
| Data availability | co2datashare.org |

**Key numbers.**

- Sognefjord (68–110 m thick) log means: Vp 2975 m/s (32/4-1) and 2722 m/s (32/2-1);
  density 2.18 and 2.235 g/cc; density porosity 0.29 and 0.26; GR-Vclay 0.37 and 0.41.
- Inverted AI: Sognefjord 5500–6700, Fensfjord 6400–8000 (m/s)(g/cc).
- Inversion at the wells: CC 0.94 / 0.92, R² 0.88 / 0.86. Seismic bandwidth ~5–90 Hz,
  dominant 25–30 Hz.
- Validation (Table 12): MAR — φ RMSE 0.093 (CC 0.86), Vp 380.9 m/s (0.84), ρ 0.088 g/cc
  (0.90). PNN — φ 0.097 (0.70), Vp 461.3 m/s (0.78), ρ 0.144 g/cc (0.74).

## What it can and cannot validate for RW-PGNN

RW-PGNN inverts **prestack** gathers for **φ, Vsh, Sw**. This paper uses **post-stack**
data and predicts **Vp, ρ, φ**. So it is **not** a direct validation target for
RW-PGNN's outputs:

- **Sw:** both wells are dry (Sw = 1), and the paper makes no Sw prediction. The wells
  can only test false positives (the method predicting CO₂ or hydrocarbons where there is
  none), not Sw resolvability.
- **Vsh:** available only as GR-derived Vclay from the logs, which is itself a model.
- **Vs, AVO gradient:** no shear logs are reported, so gradient/Vp-Vs physics can't be
  checked from this paper.
- **φ:** the only property both methods predict. Table 12 gives a published field
  baseline with the same leave-one-well-out protocol.
- Their volumes are model outputs, not ground truth. Comparing two inversions checks
  consistency, not correctness. Ground truth exists only at the two wells.

## Field cross-check of existing physics (`hema2027_field_crosscheck.py`)

Full output: `hema2027_field_crosscheck_output.txt`. These are first-order checks using
published means only.

1. **Study A's brine-sand elastic model lies outside the measured range at both wells.**
   Vp 2200 m/s is 19–26% below the measured means and below the measured minima
   (2748 and 2436 m/s). AI 4730 is 22–27% below the means and below the minima
   (5696 and 5114). Density (2.15 g/cc) is consistent.
2. **Consequence for Study A's AVO baseline.** With Study A's own caprock (AI 6110) over the
   measured sand AI, the brine intercept A moves from −0.127 to between −0.033 and +0.031.
   That is near zero (Class II/IIp-like) rather than the Study A value. **Caveat:** Hema et
   al. report no caprock logs, so Study A's caprock values (2600 m/s, 2350 kg/m³) are also
   unverified, and in places Heather rather than Draupne sits directly on the Sognefjord.
3. **GEOP592 `RockPhysicsTL` under-predicts brine-sand Vp.** At the measured mean φ and
   Vclay with Sw = 1, it gives Vp 12–24% below the measured means even at the notebook's
   24.1 MPa effective pressure. The shortfall grows at lower pressures. Density agrees
   within ~2%. The unconsolidated Hertz–Mindlin model is too soft for these wells, or the
   mineral end-members or GR-Vclay inputs are off. Only the actual log curves can separate
   those causes.
4. **Matrix density** implied by the density/density-porosity pairs is 2.66–2.68 g/cc
   (quartz-dominated). This is consistent with the 2650 kg/m³ end-member.

Why this matters for the inversion: RW-PGNN's seismic-consistency loss uses exactly this
rock-physics model. Applied to real Smeaheia data, the network would have to absorb a
12–24% Vp misfit by distorting φ, Vsh and Sw. That is the forward-model-mismatch
(F ≠ F̂) failure the PhD is designed to study, now shown with field numbers.

## Other checks on the synthetic's realism (flags, unverified causes)

- Real Sognefjord depth is ~0.7–2.2 km (their Fig. 7). The synthetic grid spans
  3500–6000 m. Its depth axis may be arbitrary; check Corrales et al. (2024).
- Real seismic peaks at 25–30 Hz; the synthetic uses a 20 Hz Ricker. At the measured
  Sognefjord Vp, λ/4 is 22.7–29.8 m at 25–30 Hz and 34–37 m at 20 Hz. The 68–110 m
  Sognefjord is above tuning thickness either way.
- `SMEAHEIA_P_PA = 24.1 MPa` is passed both as fluid pressure to Batzle–Wang and as
  effective pressure to Hertz–Mindlin. These are different physical quantities. The right
  value should be computed from Smeaheia overburden and pore pressure.

## Critical appraisal (how much weight to put on it)

- **Well validation of the inversion is not blind.** The low-frequency model was built
  from both wells and then validated at the same wells, so the CC 0.94 / 0.92 are not
  independent evidence. The leave-one-well-out MAR/PNN inherits this through the
  impedance attribute.
- **Two wells, highly autocorrelated samples.** Correlation coefficients over hundreds of
  samples from one well greatly overstate the effective sample size.
- **Log QC.** Table 8 reports density down to 1.2495 g/cc and porosity up to 0.873,
  which is not physical for rock. Several columns in Tables 8–11 have mode = minimum,
  suggesting constant-padded or extrapolated values were included in the statistics
  (compare the flat segments in Figs 18 and 22).
- **"Probabilistic" network with no reported uncertainty.** The GRNN gives point
  estimates, so the paper offers no uncertainty-calibration benchmark.
- **Useful independent confirmation:** its reference list gives Fawad, Rahman & Mondol
  (2021a) *J. Pet. Sci. Eng.* 205, 108812 and (2021b) *The Leading Edge* 40(4), 254–260.
  This supports the earlier finding that Study A's "Fawad, Hansen & Mondol (2021) IJGGC
  109, 103378" citation is incorrect.

## Open items (not actioned)

1. Check on co2datashare.org whether **prestack** gathers, shear logs, checkshots and
   the actual LAS curves for 32/4-1 and 32/2-1 are available. The paper used post-stack
   "due to the availability of post-stack processed seismic data". If prestack data are
   absent, this dataset cannot field-test a prestack AVO method.
2. Re-run cross-check 3 sample-by-sample on the real logs before choosing a
   recalibrated rock-physics model (e.g. constant-cement or stiff-sand).
3. Revisit Study A's end-member elastic values and its citation.
