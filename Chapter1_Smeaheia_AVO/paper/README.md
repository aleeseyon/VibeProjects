# Manuscript: velocity errors and AVO misclassification at Smeaheia

## Contents
| File | Purpose |
|---|---|
| `main.tex` | Manuscript (GEOPHYSICS style: abstract ≤250 words, 242 used; double-spaced; line-numbered; SEG author–year references with DOIs) |
| `main.pdf` | Compiled manuscript, 17 pages |
| `figures/fig0[1-5]_*.pdf` | Vector figures written by `../chapter1_extended.ipynb` §10; `.png` previews alongside |

## Build
```
latexmk -pdf main.tex
```
Only standard TeX Live packages are needed. For SEG's official class, replace the preamble with `\documentclass[manuscript]{geophysics}` (SEGTeX) and keep the body unchanged. Grey `[nb §…]` tags link each number to the notebook cell that printed it. Set `\shownbfalse` in the preamble to hide them before submission.

## Which journal?

**Recommendation: GEOPHYSICS (SEG), Rock Physics and AVO / Reservoir Geophysics sections.**

Why it fits:
1. **Lineage.** The paper tests and corrects results from the core AVO papers, all published in GEOPHYSICS: Shuey (1985), Rutherford & Williams (1989) and Castagna et al. (1998). Its main claims speak directly to that literature: the Shuey threshold bias, the fixed-σ sensitivity pitfall, and the aperture dependence of class labels.
2. **Contribution type.** GEOPHYSICS publishes method and verification papers with closed-form theory, appendices of derivations and reproducible code. That is the structure of this manuscript (Appendices A–B, machine-precision verification, one notebook that reproduces every number).
3. **Readership.** AVO practitioners who assign classes from two-term fits are the readers who need the practical message.

Alternatives, in order:
- **Geophysical Prospecting (EAGE).** A strong fit for a focused North Sea / CCS case study. It is more tolerant of a single-site synthetic analysis. This is the best fallback if GEOPHYSICS reviewers ask for more generality than you want to add.
- **Interpretation (SEG/AAPG).** Choose this if the paper is reframed around interpretation risk in CCS monitoring rather than reflectivity theory.
- **International Journal of Greenhouse Gas Control.** This is the right CCS audience, but it values monitoring outcomes over reflectivity approximations. It would need a time-lapse or plume-detection framing.
- **The Leading Edge.** Suitable only for a condensed tutorial (for example, "Your AVO class may be an approximation artifact").

**Honest assessment of acceptance risk at GEOPHYSICS.** As written, this is a careful, well-verified single-interface synthetic study. Expect reviewers to ask for:
1. **Generality.** Show when the Shuey bias matters across a range of contrasts and Vp/Vs, not only at one interface.
2. **A probabilistic statement.** Give the probability of misclassification under the published velocity-error statistics (Hema et al., 2027), not only deterministic thresholds.
3. **Vs and density errors.** These are held fixed here.
4. **A calibrated model.** The brine-sand Vp is below the minimum Sognefjord log value in both wells (see Discussion, "Model calibration").

Items 1–2 are the most important and can be computed with the existing notebook engine.

## Before submission (red `Author note` items in the PDF)
1. Authors, affiliations, corresponding e-mail.
2. The CO₂ fluid-property source and the conditions used in the Gassmann substitution. The source notebook cites Batzle & Wang (1992), which does not provide a CO₂ equation of state.
3. Justify the soft-sand end member, or recalibrate to the well data and re-run the notebook.
4. Acknowledgments. Archive the notebook with a DOI and cite it in the Data and Materials Availability section.
5. Proof-read the Hema et al. (2027) table values against the original: they were transcribed from a scanned PDF.
6. The DOI of the Castagna & Backus (1993) book could not be verified from this environment and is omitted. All other DOIs were checked.
