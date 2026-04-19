# Solver Support for WLC SDP

## Overview

The WLC key rate computation (`qkdx/numerics/wlc.py`) supports two solver backends:

| Backend | Algorithm | Precision | Speed | Reference |
|---------|-----------|-----------|-------|-----------|
| **MOSEK** (primary) | Interior-point SDP | ~1e-9 (primal-dual gap) | Fast | WLC 2018 §V |
| **CLARABEL / SCS** (fallback) | Frank-Wolfe (WLC Alg. 1) | ~1e-5 (duality gap) | Moderate | WLC 2018 Alg. 1 |

The solver is selected automatically via `qkdx/utils/solvers.py::preferred_solver()`:
MOSEK → CLARABEL → SCS, in that order of preference.

---

## MOSEK: Primary Solver (Research Grade)

MOSEK is the solver used in WLC 2018 (Winick, Lütkenhaus, Coles, *Quantum* 2:77, 2018) for all
numerical results including Figure 3. It provides:

- **Certified primal-dual optimality gap** (typically < 1e-8)
- **Superlinear (interior-point) convergence** — not sublinear like Frank-Wolfe
- **Machine-precision reliability** across all QBER values, including near-threshold
- **CVXPY `quantum_rel_entr` one-shot SDP** — single convex program, no iteration required

For all formal research results and published key rate curves, MOSEK is **required**.
Frank-Wolfe results should be treated as preliminary estimates only.

### Acquiring an Academic License

MOSEK provides free academic licenses for researchers at accredited institutions.

1. Go to: https://www.mosek.com/products/academic-licenses/
2. Register with your institutional email address
3. Download the license file `mosek.lic`
4. Place it at: `~/mosek/mosek.lic` (MOSEK reads this path automatically)

Verification:
```bash
python -c "import mosek; print(mosek.Env().getversion())"
```

### Installation

```bash
pip install mosek
# or, if using conda:
conda install -c mosek mosek
```

CVXPY finds MOSEK automatically once installed and licensed.

### Running the Primary Test Suite

```bash
# Tests requiring MOSEK are marked @pytest.mark.requires_mosek
pytest tests/test_numerics/test_wlc_bb84.py -m requires_mosek -v
```

Expected output: 6 parametric QBER tests + threshold + facial reduction + primal status — all PASSED.

---

## Frank-Wolfe Fallback (CLARABEL / SCS)

When MOSEK is unavailable, `wlc_key_rate()` falls back to the Frank-Wolfe algorithm
(WLC 2018 Algorithm 1), implemented entirely in NumPy + SciPy with linear SDP subproblems
solved by CLARABEL or SCS via CVXPY.

### Algorithm Summary

```
Initialize: ρ₀ = feasible state (solve linear feasibility SDP)
For t = 1, 2, ..., max_iter:
    X = G(ρ_t),  Y = Z(G(ρ_t))             # apply G-map and Z-pinching
    ∇f = G†(log X − log Y)                  # gradient (NumPy/scipy.linalg.logm)
    σ* = argmin_{σ ∈ S} Tr(∇f · σ)         # linear SDP subproblem
    gap = Tr(∇f · (ρ_t − σ*))              # Frank-Wolfe duality gap
    if gap < tol: break
    γ = golden_section_line_search(ρ_t, σ*)  # exact line search on [0,1]
    ρ_{t+1} = ρ_t + γ(σ* − ρ_t)
Return: D(G(ρ*) ‖ Z(G(ρ*))) [nats] × log2(e) [bits]
```

The gradient `G†(log X − log Y) = Σᵢ Kᵢ† (log X − log Y) Kᵢ` is exact to
scipy.linalg.logm precision (~1e-14 for well-conditioned matrices, ~1e-8 near singularities).

### Precision Characteristics

- Convergence rate: O(1/t) in objective value — sublinear
- Duality gap tolerance: default `tol=1e-5`
- Gradient precision: limited by `scipy.linalg.logm` near singular states (QBER > 11%)
- Timing: ~0.08s per QBER point (BB84, 100 iterations, CLARABEL subproblem)

### Running Fallback Tests

```bash
pytest tests/test_numerics/test_wlc_bb84.py -m fallback_solver -v
```

### Known Limitations

1. **Near-threshold precision**: At QBER ≳ 10%, the sifted state approaches singularity.
   `scipy.linalg.logm` accumulates ~1e-5 relative error. MOSEK handles this exactly.

2. **Convergence speed**: 100 iterations suffices for 1e-5 gap on BB84. More complex
   protocols (higher-dimensional, asymmetric) may require 500–1000 iterations.

3. **No certified gap**: The Frank-Wolfe duality gap is a valid upper bound on the
   optimality gap but is not a primal-dual certificate in the SDP sense.

---

## Implementation Notes

### Why Not One-Shot CVXPY with CLARABEL?

A natural alternative is `cp.quantum_rel_entr(X_reg, Y_reg)` with CLARABEL as solver
(avoiding MOSEK). This was attempted but produced **644 seconds per point** due to
CVXPY's type propagation issue:

```python
# PROBLEM: CVXPY does NOT propagate is_hermitian() through scalar multiplication
rho_reg = (1 - eps) * rho + eps * tau / d    # is_hermitian() == False !
# quantum_rel_entr requires BOTH arguments hermitian → raises ValueError
```

The workaround using auxiliary `cp.Variable(hermitian=True)` with equality constraints
is mathematically correct but extremely slow (CLARABEL's complexity explodes with
the extra equality constraints). Frank-Wolfe avoids this entirely by computing
`quantum_rel_entr` in NumPy.

### G-map Construction

For BB84, `_construct_G_map(protocol)` returns:
```
GMap(map=KrausMap.identity(4), dim_key=2, dim_side=2)
```

`dim_key` is inferred from `len(set(protocol.key_map.bitmap.values()))` (= 2 for binary key).
`dim_side` = `conditional_alice_bob_dim() / dim_key` (= 2 for BB84's 4-dim AB space).

### Z-Pinching Construction

`_construct_Z_pinching(dim_key=2, dim_side=2)` creates Kraus operators:
```
K_0 = |0⟩⟨0| ⊗ I₂ = diag(1,1,0,0)
K_1 = |1⟩⟨1| ⊗ I₂ = diag(0,0,1,1)
```

This zeros out the off-diagonal 2×2 blocks of σ = G(ρ), implementing
𝒵(σ) = Σₓ (|x⟩⟨x| ⊗ I) σ (|x⟩⟨x| ⊗ I) [CML 2016 Eq. 20].

---

## Reference

- Winick, Lütkenhaus, Coles (2018). "Reliable numerical key rates for quantum key distribution."
  *Quantum* **2**, 77. arXiv:1710.05511.
- Coles, Metodiev, Lütkenhaus (2016). "Numerical approach for unstructured quantum key distribution."
  *Nat. Commun.* **7**, 11712. arXiv:1510.01294.
- Hu, Im, Lin, Lütkenhaus, Wolkowicz (2022). "Robust Interior Point Method for Quantum Key Distribution Rate Computation."
  *Quantum* **6**, 792. arXiv:2104.03847.
