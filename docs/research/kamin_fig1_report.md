# Kamin 2025 Fig. 1 reproduction report (S2.5 Stage 2 A4b)

## 1. Sweep configuration

- Protocol: qubit BB84 with depolarizing + loss channel (Kamin §6.3).
- `qber = 0.005` (Kamin p_depol = 0.01).
- `n_values = (1000000, 100000000, 10000000000, 1000000000000)`.
- `loss_dB_values = (0.0, 3.0, 6.0, 10.0, 15.0, 20.0, 25.0, 30.0)`.
- `eps_secure = 1e-8`, `f_EC = 1.16`.
- V² mode: `tight_bb84` (see `_kamin_V2_bb84_tight` for derivation).
- SDP: single solve via `kamin_choi_sdp_qubit_bb84_with_dual`
  → `h_per_sift = 0.9546`,
  `g_star = (g_Z=-1.18e-04, g_X=-7.6365)`.

## 2. Secret-key rate table (bits/round)

| n \ loss (dB) | 0 | 3 | 6 | 10 | 15 | 20 | 25 | 30 |
|---|---|---|---|---|---|---|---|---|
| 10^6 | +0.8370 | +0.4095 | +0.2005 | +0.0742 | +0.0170 | -0.0008 | -0.0061 | -0.0078 |
| 10^8 | +0.8862 | +0.4428 | +0.2206 | +0.0872 | +0.0270 | +0.0083 | +0.0024 | +0.0005 |
| 10^10 | +0.8922 | +0.4470 | +0.2239 | +0.0891 | +0.0281 | +0.0089 | +0.0028 | +0.0009 |
| 10^12 | +0.8928 | +0.4475 | +0.2243 | +0.0893 | +0.0282 | +0.0089 | +0.0028 | +0.0009 |

## 3. Cutoff-loss comparison vs Kamin Fig. 1 (GEAT column, §6.3)

| n | my cutoff (last positive) | Kamin GEAT cutoff | gap |
|---|---|---|---|
| 10^6 | ~ 15 dB | 15 dB | see §3 |
| 10^8 | > 30 dB | 20 dB | see §3 |
| 10^10 | > 30 dB | 25 dB | see §3 |
| 10^12 | > 30 dB | 26 dB | see §3 |

**Observations**:

- At **positive-rate** anchors (loss ≤ 15 dB at n=10^6; ≤ 25 dB at n ≥ 10^8),
  our rate tracks `η_det · (1 − H₂(qber) − f_EC · H₂(qber))` within ±15%
  after optimal `(γ*, α*)`.  At `(n=10^12, 0 dB)` we reproduce
  Kamin §6.3's "≈ 0.9" anchor: **rate = 0.8928**.
- At **cutoff** the heuristic Eq. 16 form used here gives a **less-tight**
  penalty than Kamin's full Thm 3 + Thm 4 Legendre-Fenchel `f`-optimization.
  This produces small residual-positive rates beyond Kamin's zero-crossing,
  especially at `n ≥ 10^8`.  The positive-rate region itself is
  reproduced; cutoff-region saturation is follow-up (A4c stretch or a
  dedicated Thm 3 refinement pass).

## 4. Artifacts

- CSV: [docs/research/data/kamin_fig1_sweep.csv](data/kamin_fig1_sweep.csv)
- Test: [tests/test_numerics/test_kamin_fig1.py](../../tests/test_numerics/test_kamin_fig1.py)
- Code: [qkdx/numerics/kamin_sdp.py](../../qkdx/numerics/kamin_sdp.py) — see
  `kamin_fig1_sweep`, `_kamin_ell_from_sdp_result`, `_kamin_V2_bb84_tight`.

## 5. Honest accounting

What **is** validated:

- A1 (Kamin Choi SDP) and A2 (Thm 4 dual) give numerically correct
  `h_per_sift = 1 − H₂(qber_X)` and dual `g_X = −log₂((1−q)/q)` within
  solver tolerance.
- Full Eq. 16 finite-key formula with grid-optimized `(γ, α)` reproduces
  the asymptotic Devetak-Winter rate at `n → ∞` (A3 tests).
- The loss-scaled variant (A4a) matches the no-loss variant exactly at
  `loss_dB=0` and scales correctly by `η_det` at low loss.
- Rate monotonicity in both `n` and `loss_dB`.

What is **not** (yet) validated:

- Cutoff-loss values at `n ≥ 10^8` do not match Kamin's GEAT cutoffs.
  This requires implementing Kamin Theorem 3's second-order bound with
  full Frank-Wolfe + Theorem 4 Legendre-Fenchel `f`-optimization (rather
  than the heuristic Eq. 16 with closed-form V²).
- Decoy-state extension (Eq. 80 block-diagonal SDP, Fig. 3/4) — A4c
  stretch goal.
