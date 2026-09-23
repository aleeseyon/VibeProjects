"""Cross-check of existing Smeaheia physics against published field well-log statistics.

Source of field numbers: Hema, Maurya, Kant & Singh (2027), Geoenergy Science and
Engineering 268, 214769, doi:10.1016/j.geoen.2026.214769 -- Table 1 (well 32/4-1,
Alpha) and Table 2 (well 32/2-1, Beta). Both wells are dry (brine-saturated), so the
logs represent the Sw = 1 baseline. Porosity there is density porosity (Phi_Den),
Vclay is gamma-ray derived (VCLGr). Only summary statistics are published, so every
check here is first-order: a model evaluated at the MEAN phi/Vclay is not the mean of
the model over the log (the rock-physics map is nonlinear). The sample-by-sample test
needs the actual LAS curves.

Checks:
  1. Study A two-layer elastic model vs measured Sognefjord ranges.
  2. Normal-incidence reflectivity R0 (= Shuey A) of Study A's caprock over measured sand.
  3. GEOP592 RockPhysicsTL (Hertz-Mindlin + Gassmann, verbatim constants) evaluated at
     the measured mean phi, Vclay, Sw=1 vs measured mean Vp and density, with an
     effective-pressure sensitivity (the notebook uses 24.1 MPa).
  4. Matrix density implied by the published density / density-porosity pair.
"""
import numpy as np

# ---- Field statistics, transcribed from Hema et al. (2027) Tables 1 and 2 ----
# (mean, sd, min, max, mode); Vp m/s, density g/cc, impedance (m/s)(g/cc)
FIELD = {
    ("32/4-1", "Sognefjord"): dict(vp=(2975.4836, 399.3568, 2748.2744, 5246.5649, 2840),
                                   rho=(2.18, 0.11, 2.05, 2.64, 2.10),
                                   ai=(6506.0088, 1270.7167, 5695.6787, 13856.1318, 5960),
                                   vcl=0.3741, phi=0.2923),
    ("32/4-1", "Fensfjord"):  dict(vp=(3231.1243, 319.503, 2766.1311, 5433.5654, 3080),
                                   rho=(2.2686, 0.1159, 2.09, 2.6206, 2.22),
                                   ai=(7323.8862, 965.761, 5869.8569, 12824.0205, 6680),
                                   vcl=0.4137, phi=0.2347),
    ("32/2-1", "Sognefjord"): dict(vp=(2721.751, 358.2066, 2436.4805, 5570.9248, 2650),
                                   rho=(2.2353, 0.1351, 1.9733, 2.6846, 2.3),
                                   ai=(6033.7744, 850.5203, 5113.6079, 10800.5791, 5720),
                                   vcl=0.4052, phi=0.2628),
    ("32/2-1", "Fensfjord"):  dict(vp=(2896.5974, 534.6521, 2498.8472, 5422.1797, 2650),
                                   rho=(2.2871, 0.123, 2.0433, 2.6765, None),
                                   ai=(6589.6821, 1406.1144, 5418.3521, 13620.8418, 6200),
                                   vcl=0.3703, phi=0.2256),
}

# ---- Study A (Smeaheia_AVO_error_propagation.ipynb) two-layer model ----
SHALE = dict(vp=2600.0, vs=1200.0, rho=2350.0)          # "Draupne" caprock
BRINE_SAND = dict(vp=2200.0, vs=1150.0, rho=2150.0)
CO2_SAND = dict(vp=1950.0, vs=1180.0, rho=2030.0)

# ---- GEOP592 RockPhysicsTL constants (verbatim) ----
K_A, MU_A, RHO_A = 37.6e9, 44.6e9, 2650.0
K_B, MU_B, RHO_B = 20.9e9, 30.6e9, 2580.0
K_BRINE, RHO_BRINE = 2.5511e9, 1004.8
P_NOTEBOOK = 2.41e7


def rock_physics_tl(phi, vsh, P):
    """GEOP592 RockPhysicsTL.forward at Sw = 1 (brine only). Returns Vp (m/s), rho (kg/m3)."""
    Kv = vsh * K_A + (1 - vsh) * K_B
    Kr = 1.0 / (vsh / K_A + (1 - vsh) / K_B)
    mv = vsh * MU_A + (1 - vsh) * MU_B
    mr = 1.0 / (vsh / MU_A + (1 - vsh) / MU_B)
    K_min, mu_min = 0.5 * (Kv + Kr), 0.5 * (mv + mr)
    rho_min = vsh * RHO_A + (1 - vsh) * RHO_B
    nu = (3 * K_min - 2 * mu_min) / (2 * (3 * K_min + mu_min))
    C = 4.46 + 9.7 * max(0.384 - phi, 1e-6) ** 0.4
    onu2 = (1 - nu) ** 2
    K_dry = (C**2 * (1 - phi)**2 * mu_min**2 * P / (18 * np.pi**2 * onu2)) ** (1 / 3)
    mu_dry = (5 - 4 * nu) / (5 * (2 - nu)) * (3 * C**2 * (1 - phi)**2 * mu_min**2 * P / (2 * np.pi**2 * onu2)) ** (1 / 3)
    K_sat = K_dry + (1 - K_dry / K_min)**2 / (phi / K_BRINE + (1 - phi) / K_min - K_dry / K_min**2)
    rho = (1 - phi) * rho_min + phi * RHO_BRINE
    return np.sqrt((K_sat + 4 / 3 * mu_dry) / rho), rho


def r0(z1, z2):
    return (z2 - z1) / (z2 + z1)


print("=" * 88)
print("1. Study A elastic model vs measured Sognefjord ranges (both wells brine-saturated)")
print("=" * 88)
ai_bs = BRINE_SAND["vp"] * BRINE_SAND["rho"] / 1000.0          # (m/s)(g/cc)
for (well, fm), d in FIELD.items():
    if fm != "Sognefjord":
        continue
    vmean, _, vmin, vmax, vmode = d["vp"]
    amean, _, amin, amax, amode = d["ai"]
    print(f"{well} Sognefjord  Vp mean {vmean:7.1f}  mode {vmode:6.0f}  min {vmin:7.1f} | "
          f"Study A brine sand Vp {BRINE_SAND['vp']:.0f}  -> {100*(BRINE_SAND['vp']/vmean-1):+.1f}% vs mean, "
          f"{'BELOW' if BRINE_SAND['vp'] < vmin else 'within'} measured min")
    print(f"{'':20s}AI mean {amean:7.1f}  mode {amode:6.0f}  min {amin:7.1f} | "
          f"Study A brine sand AI {ai_bs:.1f}  -> {100*(ai_bs/amean-1):+.1f}% vs mean, "
          f"{'BELOW' if ai_bs < amin else 'within'} measured min")
    rmean, _, rmin, rmax, _ = d["rho"]
    print(f"{'':20s}rho mean {rmean:.3f}  range [{rmin:.3f}, {rmax:.3f}] | Study A brine sand rho {BRINE_SAND['rho']/1000:.3f}")

print()
print("=" * 88)
print("2. Normal-incidence R0 (= Shuey A) of Study A caprock over the measured sand")
print("   (caprock values themselves are NOT reported by Hema et al.; unverified)")
print("=" * 88)
z_sh = SHALE["vp"] * SHALE["rho"] / 1000.0
print(f"Study A: caprock AI {z_sh:.1f}; A(brine sand, Study A) = {r0(z_sh, ai_bs):+.4f}; "
      f"A(CO2 sand, Study A) = {r0(z_sh, CO2_SAND['vp']*CO2_SAND['rho']/1000):+.4f}")
for (well, fm), d in FIELD.items():
    if fm != "Sognefjord":
        continue
    amean, _, _, _, amode = d["ai"]
    print(f"{well}: A using measured sand AI mean = {r0(z_sh, amean):+.4f}; using mode = {r0(z_sh, amode):+.4f}")

print()
print("=" * 88)
print("3. GEOP592 RockPhysicsTL at measured mean (phi, Vclay), Sw=1, vs measured mean Vp, rho")
print("=" * 88)
print(f"{'well / formation':24s} {'phi':>6s} {'Vcl':>6s} | {'Vp meas':>8s} | "
      f"{'Vp@10MPa':>9s} {'Vp@15MPa':>9s} {'Vp@24.1MPa':>10s} | {'rho meas':>8s} {'rho mod':>8s}")
for (well, fm), d in FIELD.items():
    phi, vcl = d["phi"], d["vcl"]
    vps = [rock_physics_tl(phi, vcl, P)[0] for P in (10e6, 15e6, P_NOTEBOOK)]
    rho_mod = rock_physics_tl(phi, vcl, P_NOTEBOOK)[1] / 1000.0
    vmeas = d["vp"][0]
    print(f"{well+' '+fm:24s} {phi:6.3f} {vcl:6.3f} | {vmeas:8.1f} | "
          f"{vps[0]:9.1f} {vps[1]:9.1f} {vps[2]:10.1f} | {d['rho'][0]:8.3f} {rho_mod:8.3f}   "
          f"(Vp error @24.1MPa {100*(vps[2]/vmeas-1):+.1f}%)")

print()
print("=" * 88)
print("4. Matrix density implied by published density & density-porosity means (rho_fl = 1.0 g/cc)")
print("=" * 88)
for (well, fm), d in FIELD.items():
    rho_b, phi = d["rho"][0], d["phi"]
    print(f"{well} {fm:11s}: rho_ma = (rho_b - phi*rho_fl)/(1-phi) = {(rho_b - phi*1.0)/(1-phi):.3f} g/cc")
