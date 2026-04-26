"""Path α Lemma A sub-gap L1.G4 — C1(c) numerical verification.

Sub-gap statement (per docs/proofs/umr_path_alpha_lemma_skeletons_v0_1.md §3.2):
    L1.G4 — Output state equivalence metric: trace distance / fidelity criterion
    for ι-image of umr protocol Π under embedding to trusted-relay Π_tr.

Concrete claim being verified:
    For any density operators ρ, σ on H_AB ⊗ H_C ⊗ H_E (where H_C is the
    Charlie-internal subsystem that umr Eve controls but trusted-relay Eve
    does not), the trace distance between ρ and σ contracts under partial
    trace over H_C:

        || Tr_C(ρ) - Tr_C(σ) ||_1  ≤  || ρ - σ ||_1

    Equivalently, trace distance is non-increasing under any CPTP map; partial
    trace is a CPTP map; hence the inequality.

Citation (textbook):
    - Nielsen-Chuang, *Quantum Computation and Quantum Information*, Theorem 9.2
    - Khatri-Wilde 2024 (arXiv:2011.04672), §9 (Quantum Information Measures),
      generalized data-processing inequality for trace distance under any CPTP map

Implication for path α Lemma A.4:
    The umr-Eve view ρ^Π_{ABCE_int} maps under ι to the trusted-relay-Eve view
    ρ^{Π_tr}_{ABE_int} = Tr_C( ρ^Π_{ABCE_int} ), and the security distance
        || ρ^{Π_tr}_{ABE_int} - σ_target ⊗ τ_E_int ||_1
    is upper-bounded by the corresponding umr distance
        || ρ^Π_{ABCE_int} - σ_target ⊗ τ_CE_int ||_1
    when τ_E_int = Tr_C( τ_CE_int ). So an ε-secure umr protocol Π yields,
    via the embedding ι, an ε-secure trusted-relay protocol ι(Π).

C1 path: C1(c) — non-AI numerical tool (numpy + scipy.linalg).
    This file performs the numerical verification across N random states.
    Codex C1(a) cross-family citation accuracy is invoked separately.

Status: [SYN candidate-for-COROLLARY-pending-C1(a) Codex citation verify + C2 user signature]

Strict scope:
    - This closes ONLY L1.G4 (output state metric criterion).
    - L1.G1 (Hilbert space alignment), L1.G2 (embedding ι construction),
      L1.G3 (Stinespring gauge), L2.G1-G4, L3.G1-G3 remain open.
"""
from __future__ import annotations

import json
import warnings
from dataclasses import dataclass
from pathlib import Path

import numpy as np

# Random density generation produces transient overflow warnings on degenerate
# samples; we re-normalize via Tr → finite values. Suppress to keep logs clean.
warnings.filterwarnings("ignore", category=RuntimeWarning)


def random_density_operator(rng: np.random.Generator, dim: int) -> np.ndarray:
    """Generate a Haar-random mixed density operator via QR construction.

    Strategy: sample G ∈ C^{d×d} with iid standard-complex-normal entries,
    form ρ = G G^† / Tr(G G^†). This gives a generic full-rank mixed state.
    """
    G = (rng.standard_normal((dim, dim)) + 1j * rng.standard_normal((dim, dim))) / np.sqrt(2.0)
    M = G @ G.conj().T
    M = (M + M.conj().T) / 2
    tr = np.trace(M).real
    return M / tr


def trace_norm(M: np.ndarray) -> float:
    """Schatten-1 norm = sum of singular values."""
    M = (M + M.conj().T) / 2
    s = np.linalg.eigvalsh(M)
    return float(np.sum(np.abs(s)))


def partial_trace(rho: np.ndarray, dims: tuple[int, int, int], traced: int) -> np.ndarray:
    """Trace out subsystem `traced` (0=A, 1=C, 2=E) from ρ on H_A ⊗ H_C ⊗ H_E."""
    dA, dC, dE = dims
    rho_tensor = rho.reshape(dA, dC, dE, dA, dC, dE)
    if traced == 1:
        return np.einsum("acedce->ade", rho_tensor.transpose(0, 1, 2, 3, 4, 5)).reshape(dA * dE, dA * dE)
    if traced == 0:
        return np.einsum("acedce->cde", rho_tensor).reshape(dC * dE, dC * dE)
    if traced == 2:
        return np.einsum("acdec->acd", rho_tensor.transpose(0, 1, 2, 3, 4, 5)).reshape(dA * dC, dA * dC)
    raise ValueError(traced)


def partial_trace_C(rho_ACE: np.ndarray, dA: int, dC: int, dE: int) -> np.ndarray:
    """Trace out the middle subsystem C, returning ρ_AE on H_A ⊗ H_E."""
    rho_t = rho_ACE.reshape(dA, dC, dE, dA, dC, dE)
    out = np.zeros((dA, dE, dA, dE), dtype=complex)
    for c in range(dC):
        out += rho_t[:, c, :, :, c, :]
    return out.reshape(dA * dE, dA * dE)


@dataclass
class TrialResult:
    dA: int
    dC: int
    dE: int
    td_full: float
    td_traced: float
    contraction_holds: bool
    margin: float  # td_full - td_traced; should be >= 0


def run_one_trial(rng: np.random.Generator, dA: int, dC: int, dE: int) -> TrialResult:
    dim = dA * dC * dE
    rho = random_density_operator(rng, dim)
    sigma = random_density_operator(rng, dim)

    diff_full = rho - sigma
    td_full = trace_norm(diff_full)

    rho_AE = partial_trace_C(rho, dA, dC, dE)
    sigma_AE = partial_trace_C(sigma, dA, dC, dE)
    diff_traced = rho_AE - sigma_AE
    td_traced = trace_norm(diff_traced)

    margin = td_full - td_traced
    return TrialResult(
        dA=dA,
        dC=dC,
        dE=dE,
        td_full=td_full,
        td_traced=td_traced,
        contraction_holds=margin >= -1e-10,  # numerical floor
        margin=margin,
    )


def main() -> None:
    rng = np.random.default_rng(seed=20260426)
    cases = [
        (2, 2, 2),
        (2, 3, 2),
        (3, 2, 3),
        (2, 4, 2),
        (4, 2, 4),
        (3, 3, 3),
    ]
    n_trials_per_case = 50

    results: list[TrialResult] = []
    for (dA, dC, dE) in cases:
        for _ in range(n_trials_per_case):
            results.append(run_one_trial(rng, dA, dC, dE))

    n_total = len(results)
    n_violations = sum(1 for r in results if not r.contraction_holds)
    margins = np.array([r.margin for r in results])
    min_margin = float(margins.min())
    mean_margin = float(margins.mean())
    max_td_full = max(r.td_full for r in results)

    summary = {
        "lemma": "L1.G4 (output-state equivalence metric: trace distance contraction under partial trace)",
        "claim_text": (
            "For all ρ,σ on H_A⊗H_C⊗H_E and partial trace over H_C: "
            "||Tr_C(ρ)-Tr_C(σ)||_1 ≤ ||ρ-σ||_1"
        ),
        "n_total_trials": n_total,
        "n_violations": n_violations,
        "min_margin_td_full_minus_td_traced": min_margin,
        "mean_margin": mean_margin,
        "max_td_full_observed": max_td_full,
        "pass": n_violations == 0,
        "rng_seed": 20260426,
        "case_dims_AxCxE": [list(c) for c in cases],
        "trials_per_case": n_trials_per_case,
        "numerical_floor": 1e-10,
    }

    out_dir = Path("docs/research/data")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_json = out_dir / "path_alpha_l1g4_trace_distance_contraction.json"
    out_csv = out_dir / "path_alpha_l1g4_trace_distance_contraction.csv"

    with out_json.open("w") as f:
        json.dump(summary, f, indent=2)

    import csv
    with out_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dA", "dC", "dE", "td_full", "td_traced", "margin", "contraction_holds"])
        for r in results:
            w.writerow([r.dA, r.dC, r.dE, f"{r.td_full:.10f}", f"{r.td_traced:.10f}", f"{r.margin:.10e}", r.contraction_holds])

    print("=" * 60)
    print(f"L1.G4 numerical verification — C1(c) path")
    print("=" * 60)
    print(f"Total trials: {n_total}")
    print(f"Violations:   {n_violations}")
    print(f"Min margin (td_full - td_traced): {min_margin:.6e}")
    print(f"Mean margin:                       {mean_margin:.6e}")
    print(f"Max observed td_full:              {max_td_full:.6f}")
    print(f"PASS: {summary['pass']}")
    print(f"Outputs: {out_json}, {out_csv}")


if __name__ == "__main__":
    main()
