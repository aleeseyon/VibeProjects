# Error propagation from velocity uncertainty to AVO attribute misclassification: A validated closed-form framework applied to CO₂-storage monitoring at Smeaheia

**[Author names and affiliations — to be completed]**

*Draft manuscript formatted for GEOPHYSICS (SEG). Every numerical value in this draft is printed by a cell of `chapter1_extended.ipynb`; the source cell is given in square brackets, e.g. [nb §9.4], and the machine-readable values are in `chapter1_numbers.json`. Bracketed source tags are for internal verification and should be removed before submission.*

---

## ABSTRACT

Amplitude-variation-with-offset (AVO) classification of the top of a CO₂-charged reservoir depends on the P-wave velocities assigned to the caprock and the reservoir. We derive closed-form sensitivities of the two-term Shuey intercept *A* and gradient *B* to relative P-velocity errors. We validate the symbolic implementation against an independent Mathematica derivation and apply it to a Draupne shale over CO₂-saturated Sognefjord sand model of the Smeaheia storage site, northern North Sea. The baseline response is Class III (*A*₀ = −0.214, *B*₀ = −0.021). *A* stays negative for all errors within ±10%, but *B* is close to zero and highly sensitive. Two-term Shuey reflectivity predicts an apparent Class III → IV transition at a minimum error-vector magnitude of 4.44%. We recompute the threshold with exact Zoeppritz reflectivity, implemented twice and validated to ≤2 × 10⁻¹⁵ against the closed-form solution, energy conservation, and two open-source libraries. The exact normal-incidence tangent gradient raises the minimum threshold to 5.58%. A two-term least-squares fit over 0°–30° raises it to 8.23%. Two-term Shuey therefore understates the error needed for misclassification by about 20%, yet the misclassification is physical. We also show that common-mode velocity errors do not cancel in *B*, because Poisson's ratio depends on *V*_P. The frequently quoted fixed-Poisson's-ratio sensitivity is therefore not the operative one. Published seismic-to-well prediction errors for Sognefjord *V*_P at Smeaheia are 13%–17% of the mean log velocity. At that level, model-based AVO class assignment at this interface is not robust.

---

## INTRODUCTION

AVO analysis is routinely used to infer pore-fluid content from the angle dependence of P-wave reflectivity (Rutherford and Williams, 1989; Castagna and Backus, 1993; Castagna et al., 1998). The intercept–gradient crossplot and the classification of Rutherford and Williams (1989), extended by Castagna et al. (1998), give the interpreter a compact vocabulary. A Class III response (negative intercept, negative gradient; brightening with offset) is the classical signature of a low-impedance gas or CO₂ sand beneath shale. A Class IV response (negative intercept, positive gradient; dimming with offset) arises when a soft sand is capped by a lithology of relatively high S-wave velocity, so that the S-wave contrast reverses the sign of the gradient (Castagna et al., 1998).

AVO-compliant processing aims to preserve relative amplitudes with angle, but interpretation still rests on an elastic model. That model is used to build fluid-substitution templates, forward-model expected responses, and decide whether an observed anomaly is consistent with CO₂. The P-wave velocities of the model are among its least certain inputs. They are taken from sonic logs that may not represent the seismic-scale interval, from seismic inversion, or from machine-learning property prediction. At Smeaheia, the published multi-attribute-regression and probabilistic-neural-network predictions of *V*_P have validation RMS errors of 380.91 m/s and 461.3 m/s, respectively (Hema et al., 2027, their Table 12). Relative to the mean Sognefjord log velocities of the two wells, these errors equal 12.80%–16.95% [nb §9.7].

For CO₂-storage monitoring the consequences of misclassification are asymmetric. If velocity errors turn a genuine Class III CO₂ response into an apparent Class IV, the interpreter may reject a correct CO₂ interpretation or misplace the plume boundary. Conversely, the brine-sand reference at Smeaheia is itself close to *B* = 0 [nb §3], so the fluid discrimination relies on small gradient differences.

This paper asks a narrow question. How large must relative errors in the caprock and reservoir P-velocities be before the AVO class of the Smeaheia top reservoir changes, and how much of the answer depends on the reflectivity approximation? We proceed in three steps. First, we derive linear sensitivity coefficients for the Shuey (1985) attributes in the Wiggins et al. (1983) formulation and cross-validate the symbolic code against an independent Mathematica derivation. Second, we map the nonlinear response of *A*, *B*, and *A*·*B* over a ±10% error plane. Third, we recompute the class boundary with exact Zoeppritz (1919) reflectivity, validated at machine precision, to separate approximation artifacts from physical effects.

---

## THEORY AND METHOD

### Elastic model

The reference model is summarised in Table 1. It represents the Draupne Formation shale caprock over Sognefjord Formation sandstone at approximately 1200 m TVDSS in the Smeaheia area (Fawad et al., 2021; Hema et al., 2027). The CO₂-sand properties were obtained upstream of this study by Gassmann fluid substitution with pore-fluid properties following Batzle and Wang (1992). We treat the model as fixed and do not re-derive it here. As a consistency check, a Gassmann substitution with unchanged shear modulus predicts *V*_S,CO₂ = *V*_S,brine (ρ_brine/ρ_CO₂)^½ = 1183.5 m/s, compared with the model value of 1180 m/s [nb §9.7].

**Table 1.** Reference elastic model (fixed input).

| Property | Caprock (Draupne shale) | Brine sand | CO₂ sand (active) |
|---|---|---|---|
| *V*_P (m/s) | 2600 | 2200 | 1950 |
| *V*_S (m/s) | 1200 | 1150 | 1180 |
| ρ (kg/m³) | 2350 | 2150 | 2030 |

The active scenario, shale over CO₂ sand, has contrasts Δ*V*_P/*V̄*_P = −0.2857, Δ*V*_S/*V̄*_S = −0.0168 and Δρ/ρ̄ = −0.1461 [nb §9.2]. These are not small, so the accuracy of weak-contrast reflectivity cannot be taken for granted. This is the motivation for the Zoeppritz cross-check below.

### Two-term Shuey attributes

Following Shuey (1985) in the form given by Castagna and Backus (1993), the intercept, gradient, and P-velocity contrast are

$$A = \frac{\rho_2 V_{P2}-\rho_1 V_{P1}}{\rho_2 V_{P2}+\rho_1 V_{P1}}, \qquad C = \frac{V_{P2}-V_{P1}}{V_{P2}+V_{P1}}, \tag{1}$$

$$B = A\left[D - \frac{2(1+D)(1-2\bar\sigma)}{1-\bar\sigma}\right] + \frac{\Delta\sigma}{(1-\bar\sigma)^2}, \qquad D = \left[1 + \frac{(\rho_2-\rho_1)/(\rho_2+\rho_1)}{(V_{P2}-V_{P1})/(V_{P2}+V_{P1})}\right]^{-1}, \tag{2}$$

where $\bar\sigma = (\sigma_1+\sigma_2)/2$, $\Delta\sigma = \sigma_2-\sigma_1$, and

$$\sigma_i = \frac{V_{Pi}^2 - 2V_{Si}^2}{2\left(V_{Pi}^2 - V_{Si}^2\right)}. \tag{3}$$

Subscripts 1 and 2 denote the caprock and the reservoir. The intercept *A* in equation 1 is the exact normal-incidence plane-wave reflection coefficient. We verified this against the Zoeppritz solution to 5.6 × 10⁻¹⁷ [nb §9.1].

### Linear error propagation

Let relative P-velocity errors be $r_i = \delta V_{Pi}/V_{Pi}$. To first order,

$$\frac{\delta X}{X} = k_X\,(r_1 - r_2), \qquad X\in\{A, B, C\}. \tag{4}$$

Equation 4 is exact in form for *A* and *C*, which depend on *V*_P only through the ratio *V*_P2/*V*_P1. For *B* it holds only if $\bar\sigma$ and $\Delta\sigma$ are held fixed when differentiating. The implementation (the Python port of the Mathematica notebook) makes exactly this assumption: σ enters the symbolic derivative as an independent variable. We return to the physical consequence of this choice in the Results.

### Cross-validation against the Mathematica derivation

The symbolic code (SymPy) was checked against the original Mathematica derivation. For the Mathematica notebook's own test model (*V*_P1 = 3599 m/s, *V*_P2 = 3930 m/s, *V*_S1 = 2341.45 m/s, *V*_S2 = 2304.5 m/s, ρ₁ = 2313.9 kg/m³, ρ₂ = 2388.72 kg/m³), the Python port reproduces all six Mathematica outputs to the printed precision (Table 2) [nb §2.1].

**Table 2.** Cross-validation of the symbolic engine against the Mathematica notebook.

| Quantity | Python (SymPy) | Mathematica |
|---|---|---|
| *A* | +0.059832 | +0.0598318 |
| *B* | +0.041834 | +0.0418341 |
| *C* | +0.043963 | +0.0439633 |
| *k*_A | −8.32684827 | −8.32685 |
| *k*_B | +24.87862148 | +24.8786 |
| *k*_C | −11.35113011 | −11.3511 |

### Nonlinear error mapping

To go beyond equation 4, we re-evaluate equations 1–3 exactly at perturbed velocities. Here σ is recomputed from equation 3 at each perturbed *V*_P, and *V*_S and ρ are unperturbed. We use (i) one-dimensional slices (caprock only, reservoir only, and *r*₁ = −*r*₂), (ii) the full error plane (*r*₁, *r*₂) ∈ [−10%, 10%]², and (iii) radial spokes $r_1 = |r|\cos\phi$, $r_2 = |r|\sin\phi$ with $|r|$ ≤ 10%. The AVO class boundary of interest is *B* = 0 at *A* < 0 (Class III ↔ Class IV; Castagna et al., 1998). We locate it by bracketed root finding (Brent's method, tolerance 10⁻¹²) along each spoke, and find its minimum radius by bounded minimisation over φ.

### Exact Zoeppritz cross-check

We implemented the exact plane-wave P-P reflection coefficient twice, independently. The first implementation solves the 4 × 4 Zoeppritz system for $[R_{PP}, R_{PS}, T_{PP}, T_{PS}]$ at each angle. The second evaluates the explicit closed form of Aki and Richards (1980, their equation 5.39), written in terms of vertical slownesses with a complex square-root branch so that it remains valid beyond critical angles. Before either implementation was used, we required agreement at better than 10⁻¹³ on four models (the two Smeaheia scenarios, the Mathematica test model, and a model with a P critical angle at 41.8°) on 0°–60° [nb §9.1]:

- matrix versus explicit solution: maximum difference 1.86 × 10⁻¹⁵;
- normal incidence versus (*Z*₂ − *Z*₁)/(*Z*₂ + *Z*₁): ≤ 1.73 × 10⁻¹⁶;
- energy-flux conservation of the full four-wave solution: |Σ*E* − 1| ≤ 7.77 × 10⁻¹⁶;
- PyLops (`zoeppritz_pp`; pre-critical angles, where it is defined): ≤ 5.41 × 10⁻¹⁶;
- bruges (`zoeppritz_rpp`, conjugated post-critically to match our Fourier sign convention): ≤ 1.26 × 10⁻¹⁵.

An "exact" gradient is not uniquely defined, because exact *R*_PP is not linear in sin²θ. We therefore use two definitions:

1. **Exact tangent gradient**, $B_Z^{\tan} = \partial R_{PP}/\partial(\sin^2\theta)|_{\theta=0}$. We obtain it from a degree-6 least-squares polynomial in sin²θ fitted to exact *R*_PP on 0°–20°. Between polynomial degrees 6 and 10 the result changes by 1.0 × 10⁻⁹ [nb §9.2]. This is the exact counterpart of the Shuey gradient, which is also a normal-incidence slope.
2. **Two-term least-squares gradient**, $B_Z^{\mathrm{LSQ}}$: the slope of $R_{PP} \approx A + B\sin^2\theta$ fitted to exact *R*_PP on 0°–30°. This is the gradient a two-term AVO inversion of noise-free, ideally processed gathers would recover.

We also evaluate the Aki and Richards (1980) linearised gradient $B_{AR} = \tfrac12 \Delta V_P/\bar V_P - 2(\bar V_S/\bar V_P)^2(\Delta\rho/\bar\rho + 2\Delta V_S/\bar V_S)$. Shuey's expression is a re-parameterisation of the same first-order theory. Both first-order gradients converge to $B_Z^{\tan}$ as the contrasts vanish, with relative deviation proportional to the contrast. For contrast parameters of 10⁻¹, 10⁻² and 10⁻³ the deviation is 9.5 × 10⁻², 1.3 × 10⁻² and 1.4 × 10⁻³ (Aki–Richards) and 6.9 × 10⁻², 1.3 × 10⁻² and 1.4 × 10⁻³ (Shuey) [nb §9.2].

---

## RESULTS

### Baseline response and linear sensitivities

The shale/CO₂-sand baseline gives *A*₀ = −0.2137, *B*₀ = −0.0211 and *C*₀ = −0.1429, a Class III response. The shale/brine-sand reference gives *A*₀ = −0.1273 and *B*₀ = +0.0023 [nb §3]. The linear sensitivity coefficients of equation 4 at the Smeaheia baseline are *k*_A = +2.233, *k*_B = −31.277 and *k*_C = +3.429 [nb §3]. The relative sensitivity of *B* is an order of magnitude larger than that of *A*. This follows directly from *B*₀ being small: the absolute sensitivity ∂*B*/∂ln*V*_P1 = +0.660 is not unusual, but it is divided by |*B*₀| = 0.021 [nb §9.6].

### Nonlinear response over the ±10% error plane

The intercept is nearly linear in the velocity errors, and it remains negative over the entire ±10% error plane (maximum *A* = −0.116) [nb §9.8]. The stack-amplitude bright spot is therefore robust. The gradient is strongly nonlinear (Figure 1). The product *A*·*B* changes from its baseline of +0.00451 to values between −0.00676 and +0.01444 over the error plane, changing sign across the *B* = 0 contour (Figure 2) [nb §5].

Along the eight labelled spokes of Figure 3, the Shuey gradient at |*r*| = 10% ranges from −0.0554 (caprock-only positive error, φ = 0°) to +0.0304 (φ = 135°, caprock slow and reservoir fast) [nb §9.3]. With two-term Shuey, the *B* = 0 boundary is crossed at |*r*| = 4.752% along φ = 135° (*r*₁ − *r*₂ = −6.721%). Its closest approach to the baseline is |*r*| = 4.444% at φ = 156.6°, i.e. *r*₁ = −4.079%, *r*₂ = +1.765% [nb §9.3].

### Exact Zoeppritz versus two-term Shuey

At the baseline, the gradient estimators differ substantially (Figure 4; Table 3) [nb §9.2]. The two-term Shuey gradient (−0.0211) is 0.705 times the exact tangent gradient (−0.0299), i.e. about 30% closer to the class boundary. The Aki–Richards gradient (−0.0445) errs in the opposite direction. The 0°–30° least-squares gradient (−0.0513) is steeper than the tangent because exact *R*_PP curves downward in sin²θ at this interface (Figure 4).

**Table 3.** Baseline gradient and *B* = 0 thresholds (|*r*|, %) by estimator [nb §9.2, §9.4]. "—" = no crossing within |*r*| ≤ 10%.

| Estimator | *B*₀ | φ = 90° | φ = 135° | φ = 180° | φ = 225° | Minimum |*r*| (φ) | Error-plane fraction with *B* > 0 |
|---|---|---|---|---|---|---|---|
| Two-term Shuey | −0.0211 | 9.900 | 4.752 | 4.802 | 8.826 | 4.444 (156.6°) | 29.55% |
| Aki–Richards | −0.0445 | — | 6.206 | 7.064 | — | 6.035 (148.5°) | 16.95% |
| Zoeppritz, tangent | −0.0299 | — | 5.755 | 6.484 | — | 5.580 (149.2°) | 19.05% |
| Zoeppritz, LSQ 0°–30° | −0.0513 | — | 8.455 | 9.628 | — | 8.225 (148.5°) | 8.75% |

No estimator crosses *B* = 0 along φ = 0°, 45°, 270° or 315° within 10% [nb §9.4].

Three results follow (Figure 5):

1. **The misclassification is physical.** Every exact-reflectivity estimator predicts a Class III → IV transition within ±10% errors when the caprock velocity is underestimated relative to the reservoir velocity.
2. **Two-term Shuey places the threshold too low.** Along φ = 135° the exact tangent threshold is 5.755% versus 4.752% for Shuey. Shuey is therefore 1.003 percentage points, or 17.4%, low. At the closest-approach point the exact value is 5.580% versus 4.444% (1.136 points, 20.4% low) [nb §9.4]. The bias comes mainly from the baseline *B*₀, which Shuey places too close to zero.
3. **Some Shuey crossings are pure artifacts.** Two-term Shuey predicts *B* = 0 crossings for reservoir-only errors (φ = 90°, at 9.900%) and for common-mode errors (φ = 225°, at 8.826%). No exact estimator reproduces these crossings.

### Sensitivity of the practical threshold to aperture

When *B* is estimated by a two-term fit to exact reflectivity, both the baseline gradient and the threshold depend on the angle aperture [nb §9.4]:

| Aperture | *B*₀ (LSQ) | Threshold along φ = 135° |
|---|---|---|
| 0°–20° | −0.0389 | 6.993% |
| 0°–25° | −0.0443 | 7.662% |
| 0°–30° | −0.0513 | 8.455% |
| 0°–35° | −0.0601 | 9.355% |
| 0°–40° | −0.0711 | — |

### Poisson's ratio and the failure of common-mode cancellation

Because σ depends on *V*_P through equation 3, the total derivative of *B* differs from the fixed-σ derivative behind *k*_B [nb §9.6]:

- fixed σ: ∂*B*/∂ln*V*_P1 = +0.6603 and ∂*B*/∂ln*V*_P2 = −0.6603. The two sum to zero, so common-mode errors cancel.
- total: d*B*/dln*V*_P1 = −0.4050 and d*B*/dln*V*_P2 = +0.1114. The sum is −0.2936, so common-mode errors do not cancel.

The caprock sensitivity even changes sign. To first order along φ = 135°, the fixed-σ sensitivity predicts that *B* becomes *more* negative (no crossing). The total derivative predicts a crossing at 5.782%, compared with 4.752% for the full nonlinear Shuey evaluation [nb §9.6]. Common-mode errors of ±10% move *B* in both Shuey and exact Zoeppritz. For example, the exact tangent gradient goes from −0.0299 to −0.0433 (+10%) and −0.0117 (−10%), while *A* is exactly invariant [nb §9.6]. The physical reason is that exact *R*_PP depends only on velocity *ratios*. Scaling *V*_P in both layers while holding *V*_S fixed changes *V*_S/*V*_P, and hence σ, in both layers.

---

## DISCUSSION

**What the Zoeppritz check changes.** The earlier conclusion drawn from two-term Shuey alone, that differential *V*_P errors of a few percent can flip the apparent AVO class at the Smeaheia top reservoir, survives exact reflectivity. Its magnitude does not. At the contrasts of this interface (Δ*V*_P/*V̄*_P ≈ −0.29), second-order terms in the contrasts are not negligible. The two first-order parameterisations, Shuey and Aki–Richards, bracket the exact tangent gradient from opposite sides (Table 3). Using two-term Shuey therefore overstates the vulnerability of the classification by about 17%–20% in required error magnitude. It also creates spurious crossings for reservoir-only and common-mode errors. We did not decompose the Shuey–Aki–Richards difference into individual second-order terms. The statement that it arises from second-order contrast terms rests on the small-contrast convergence test [nb §9.2], not on an explicit expansion.

**Which gradient should define the class?** The answer depends on how *B* is measured. The tangent gradient is the correct reference for judging the Shuey formula itself. A two-term inversion of real gathers, however, returns an aperture-dependent slope. For this interface that slope is steeper than the tangent, which moves the practical threshold to 7%–9.4% for apertures of 20°–35°, and beyond 10% for a 0°–40° aperture. A class label obtained from a two-term fit is therefore partly a property of the acquisition aperture, not only of the rocks. We recommend reporting the aperture with any AVO class assignment near *B* ≈ 0.

**Is ±10% realistic?** The Smeaheia seismic-to-well *V*_P predictions of Hema et al. (2027) have validation RMS errors of 12.80%–16.95% of the mean Sognefjord log velocity [nb §9.7]. These are errors of a property-prediction workflow, not of processing velocities, and they refer to the reservoir interval rather than to the caprock–reservoir differential. They nevertheless indicate that *V*_P uncertainties of several percent to more than 10% are plausible at Smeaheia. At that level the exact thresholds of 5.6%–8.2% (minimum |*r*|) lie within the uncertainty.

**Scope of "velocity error".** The framework propagates errors in the layer P-velocities that enter the reflection coefficient, i.e. errors in the elastic model used for interpretation. Processing-velocity errors in AVO-compliant processing act mainly through a different mechanism, namely the incidence angle assigned to each offset. That mechanism is not modelled here. Density and *V*_S errors are also not propagated, and we hold them fixed. Because σ depends on *V*_S, a *V*_S error would interact with the *V*_P effects described above.

**Model consistency.** The brine-sand *V*_P of the fixed reference model (2200 m/s) is 19.2% and 26.1% below the mean Sognefjord log velocities of wells 32/2-1 and 32/4-1, and below the minimum log values in both wells [nb §9.7]. The CO₂-sand model inherits this offset. The absolute *A* and *B* values of this study should therefore be regarded as representative of a soft-sand end member, not as calibrated Smeaheia values. The methodology and the relative conclusions (Shuey versus Zoeppritz, the role of σ) do not depend on this calibration. The numerical thresholds do.

**Limitations.** The analysis assumes isotropic, elastic, planar interfaces, a single interface without tuning, and noise-free reflectivity. It does not include anisotropy, attenuation, thin-bed interference, or angle-dependent wavelet effects, all of which can change the observed gradient.

---

## CONCLUSIONS

1. A symbolic implementation of the Shuey intercept and gradient reproduces the six outputs of an independent Mathematica derivation to printed precision.
2. At the Smeaheia top reservoir, the Class III baseline (*A*₀ = −0.214, *B*₀ = −0.021) has a robust intercept but a gradient near zero. A Class III → IV misclassification is physically possible within ±10% P-velocity errors when the caprock velocity is underestimated relative to the reservoir.
3. The two-term Shuey threshold, with a minimum error magnitude of 4.44%, is biased low. With the exact tangent gradient it is 5.58%, and with a 0°–30° two-term fit to exact reflectivity it is 8.23%. The Shuey threshold is thus 17%–20% lower than the exact tangent threshold (along φ = 135° and at closest approach). This offset is an approximation artifact; the crossing itself is not.
4. The widely used fixed-Poisson's-ratio sensitivity (*k*_B = −31.28) does not describe the physical response. Common-mode *V*_P errors do not cancel in *B*, and the first-order caprock sensitivity changes sign when σ is allowed to vary with *V*_P.
5. For CO₂-monitoring interpretation at interfaces with *B* near zero, AVO classes should be assigned with exact reflectivity and a stated aperture, and their robustness should be tested against the velocity uncertainty of the elastic model.

---

## ACKNOWLEDGMENTS

[To be completed.]

## DATA AND MATERIALS AVAILABILITY

All computations are contained in the Jupyter notebook `chapter1_extended.ipynb` (Python, NumPy, SymPy, SciPy, Matplotlib; third-party checks with PyLops 2.8.0 and bruges 0.5.4). Well statistics are taken from Hema et al. (2027).

---

## REFERENCES

*(DOIs to be added and verified at submission; the two entries marked † are additional to the notebook's citation list and were checked for existence.)*

† Aki, K., and P. G. Richards, 1980, Quantitative seismology: Theory and methods: W. H. Freeman and Company.

Batzle, M., and Z. Wang, 1992, Seismic properties of pore fluids: Geophysics, **57**, 1396–1408.

Castagna, J. P., and M. M. Backus, eds., 1993, Offset-dependent reflectivity — Theory and practice of AVO analysis: SEG Investigations in Geophysics 8.

Castagna, J. P., H. W. Swan, and D. J. Foster, 1998, Framework for AVO gradient and intercept interpretation: Geophysics, **63**, 948–956.

Fawad, M., M. J. Rahman, and N. H. Mondol, 2021, Seismic reservoir characterization of potential CO₂ storage reservoir sandstones in Smeaheia area, Northern North Sea: Journal of Petroleum Science and Engineering, **205**, 108812. *[Replaces the notebook's unverifiable citation "Fawad, Hansen & Mondol (2021), IJGGC 109, 103378" — see summary, flagged item F4.]*

Hema, G., S. P. Maurya, R. Kant, and A. P. Singh, 2027, Seismic inversion driven reservoir characterization and subsurface property prediction in the Smeaheia Field, northern North Sea: Implications for CO₂ storage: Geoenergy Science and Engineering, **268**, 214769, doi: 10.1016/j.geoen.2026.214769.

Rutherford, S. R., and R. H. Williams, 1989, Amplitude-versus-offset variations in gas sands: Geophysics, **54**, 680–688.

Shuey, R. T., 1985, A simplification of the Zoeppritz equations: Geophysics, **50**, 609–614.

Wiggins, R., G. S. Kenny, and C. D. McClure, 1983, A method for determining and displaying the shear-velocity reflectivities of a geologic formation: European Patent Application 0113944.

† Zoeppritz, K., 1919, Erdbebenwellen VII. VIIb. Über Reflexion und Durchgang seismischer Wellen durch Unstetigkeitsflächen: Nachrichten von der Königlichen Gesellschaft der Wissenschaften zu Göttingen, Mathematisch-Physikalische Klasse, 66–84.

---

## FIGURE CAPTIONS

**Figure 1.** (a) Intercept *A* and (b) gradient *B* versus relative *V*_P error for caprock-only, reservoir-only, and *r*₁ = −*r*₂ perturbations, evaluated with two-term Shuey reflectivity and σ(*V*_P). Shale over CO₂ sand. File: `fig_AB_slices.png` [nb §4].

**Figure 2.** *A*·*B* over the (*r*₁, *r*₂) error plane. The green line is *B* = 0 (apparent Class III/IV boundary); the star marks the baseline. File: `fig_GI_map.png` [nb §5].

**Figure 3.** Radial error spokes in the *A*–*B* crossplot, coloured by error magnitude |*r*|, with envelopes at |*r*| = 2%, 5%, and 10%. File: `AB_spokes.png` [nb §7]. *Note: the original notebook's reading of this figure contains two numerical statements that do not reproduce (see summary F1, F3). The caption and text of this draft use the recomputed values.*

**Figure 4.** Exact Zoeppritz *R*_PP at the baseline compared with the two-term Shuey curve, the exact normal-incidence tangent, and the two-term least-squares fit over 0°–30° (shaded). File: `fig_rpp_baseline.png` [nb §9.2].

**Figure 5.** *B* = 0 contours in the error plane for two-term Shuey, Aki–Richards, the exact Zoeppritz tangent, and the 0°–30° least-squares Zoeppritz gradient. Dots mark each contour's closest approach to the baseline (star); grey circles are |*r*| = 2%–10%. File: `fig_B0_contours.png` [nb §9.5].

---

## APPENDIX A — EXACT P-P REFLECTION COEFFICIENT

With ray parameter $p = \sin\theta/V_{P1}$ and vertical slownesses $q_{\alpha i} = (V_{Pi}^{-2} - p^2)^{1/2}$ and $q_{\beta i} = (V_{Si}^{-2} - p^2)^{1/2}$ (principal complex branch), define (Aki and Richards, 1980, equation 5.39)

$$a = \rho_2(1-2V_{S2}^2p^2) - \rho_1(1-2V_{S1}^2p^2),\quad b = \rho_2(1-2V_{S2}^2p^2) + 2\rho_1V_{S1}^2p^2,$$
$$c = \rho_1(1-2V_{S1}^2p^2) + 2\rho_2V_{S2}^2p^2,\quad d = 2(\rho_2V_{S2}^2 - \rho_1V_{S1}^2),$$
$$E = b\,q_{\alpha1} + c\,q_{\alpha2},\quad F = b\,q_{\beta1} + c\,q_{\beta2},\quad G = a - d\,q_{\alpha1}q_{\beta2},\quad H = a - d\,q_{\alpha2}q_{\beta1},$$
$$D = EF + GHp^2, \qquad R_{PP} = \frac{(b\,q_{\alpha1} - c\,q_{\alpha2})F - (a + d\,q_{\alpha1}q_{\beta2})Hp^2}{D}.$$

At *p* = 0 this reduces to $R_{PP} = (\rho_2V_{P2} - \rho_1V_{P1})/(\rho_2V_{P2} + \rho_1V_{P1})$. The independent 4 × 4 matrix solution and all validation checks are in `chapter1_extended.ipynb`, §9.1.
