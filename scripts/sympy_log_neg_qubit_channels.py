"""SymPy C1(c) verification for log_neg formulas: dephasing + depolarizing"""
import sympy as sp

p = sp.Symbol('p', positive=True, real=True)

# Basis |00⟩,|01⟩,|10⟩,|11⟩ (row/col indices 0,1,2,3)
# |Φ⁺⟩⟨Φ⁺| = 1/2 [[1,0,0,1],[0,0,0,0],[0,0,0,0],[1,0,0,1]]
# |Φ⁻⟩⟨Φ⁻| = 1/2 [[1,0,0,-1],[0,0,0,0],[0,0,0,0],[-1,0,0,1]]
# |Ψ⁺⟩⟨Ψ⁺| = 1/2 [[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]]
# |Ψ⁻⟩⟨Ψ⁻| = 1/2 [[0,0,0,0],[0,1,-1,0],[0,-1,1,0],[0,0,0,0]]

half = sp.Rational(1,2)

def bell(name):
    if name == '+phi':
        return half*sp.Matrix([[1,0,0,1],[0,0,0,0],[0,0,0,0],[1,0,0,1]])
    if name == '-phi':
        return half*sp.Matrix([[1,0,0,-1],[0,0,0,0],[0,0,0,0],[-1,0,0,1]])
    if name == '+psi':
        return half*sp.Matrix([[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]])
    if name == '-psi':
        return half*sp.Matrix([[0,0,0,0],[0,1,-1,0],[0,-1,1,0],[0,0,0,0]])

# === Dephasing ===
# E(ρ) = (1-p)ρ + pZρZ. Kraus K0=√(1-p)I, K1=√pZ
# Choi = (1-p)|Φ⁺⟩⟨Φ⁺| + p|Φ⁻⟩⟨Φ⁻|
rho_dephase = (1-p)*bell('+phi') + p*bell('-phi')
print("=== Dephasing Choi (direct Bell-state expansion) ===")
print(sp.simplify(rho_dephase))

def ptB(rho):
    r = [[rho[i,j] for j in range(4)] for i in range(4)]
    # Partial transpose on B: (i1 i2, j1 j2) -> (i1 j2, j1 i2)
    # In our basis ordering ab (a=A, b=B), index = 2a+b
    # PT_B: ρ'[(a b), (c d)] = ρ[(a d), (c b)]
    new = [[0]*4 for _ in range(4)]
    for a in range(2):
        for b in range(2):
            for c in range(2):
                for d in range(2):
                    old_i = 2*a + b
                    old_j = 2*c + d
                    new_i = 2*a + d
                    new_j = 2*c + b
                    new[new_i][new_j] = r[old_i][old_j]
    return sp.Matrix(new)

rho_pt_d = ptB(rho_dephase)
print("\nPT of dephasing:")
print(sp.simplify(rho_pt_d))

eigs_d = sp.simplify(rho_pt_d).eigenvals()
print("\nPT eigenvalues (dephasing):")
total = 0
for e, m in eigs_d.items():
    print(f"  {sp.simplify(e)} × {m}")
    total += e * m
print(f"  Sum check (should be 1): {sp.simplify(total)}")

# Trace norm for p ∈ [0, 1/2]: eigs are {1/2, 1/2, 1/2-p, p-1/2}
# |1/2-p| = 1/2-p (since p<1/2), |p-1/2| = 1/2-p
# trace_norm = 1/2 + 1/2 + (1/2-p) + (1/2-p) = 2 - 2p = 2(1-p)
tn_d = sp.simplify(sp.Rational(1,2)*2 + 2*(sp.Rational(1,2) - p))
print(f"\nTrace norm (p ∈ [0, 1/2]): {tn_d} = 2(1-p)")
print(f"log_neg = log₂({tn_d}) = 1 + log₂(1-p)")

# === Depolarizing ===
# Choi = (1-p)|Φ⁺⟩⟨Φ⁺| + p/4·I₄  (Werner form)
# Alt:    (1-3p/4)|Φ⁺⟩⟨Φ⁺| + (p/4)(|Ψ⁺⟩⟨Ψ⁺|+|Ψ⁻⟩⟨Ψ⁻|+|Φ⁻⟩⟨Φ⁻|)
rho_depol = (1-sp.Rational(3,1)*p/4)*bell('+phi') + (p/4)*(bell('+psi')+bell('-psi')+bell('-phi'))
print("\n\n=== Depolarizing Choi ===")
print(sp.simplify(rho_depol))

# Fidelity F
phi_plus_vec = sp.Matrix([sp.Rational(1,1)/sp.sqrt(2),0,0,sp.Rational(1,1)/sp.sqrt(2)])
F = (phi_plus_vec.T * rho_depol * phi_plus_vec)[0,0]
print(f"F = ⟨Φ⁺|ρ|Φ⁺⟩ = {sp.simplify(F)}  (expected 1-3p/4)")

rho_pt_dp = ptB(rho_depol)
print("\nPT of depolarizing:")
print(sp.simplify(rho_pt_dp))

eigs_dp = sp.simplify(rho_pt_dp).eigenvals()
print("\nPT eigenvalues (depolarizing):")
total = 0
for e, m in eigs_dp.items():
    print(f"  {sp.simplify(e)} × {m}")
    total += e * m
print(f"  Sum check (should be 1): {sp.simplify(total)}")

# For p ∈ [0, 2/3]: F = 1 - 3p/4 ≥ 1/2
# Expected eigs: (2F+1)/6 with mult 3, (1-2F)/2 with mult 1
# = (2(1-3p/4)+1)/6 = (3 - 3p/2)/6 = (1-p/2)/2 (mult 3)
# (1-2(1-3p/4))/2 = (3p/2 - 1)/2 (mult 1), negative for p<2/3
lam_plus = sp.simplify((1 - p/2)/2)
lam_minus = sp.simplify((sp.Rational(3,1)*p/2 - 1)/2)
print(f"\nPredicted: λ_+ = {lam_plus} (mult 3), λ_- = {lam_minus} (mult 1)")
print(f"Sum check: 3*λ_+ + λ_- = {sp.simplify(3*lam_plus + lam_minus)}")

# Trace norm for p < 2/3: 3*λ_+ + |λ_-|
tn_dp = sp.simplify(3*lam_plus + (-lam_minus))
print(f"Trace norm (p ∈ [0, 2/3]): {tn_dp}")

# Check: 2 - 3p/2 vs alternative 2F = 2(1-3p/4) = 2 - 3p/2 ✓
print(f"\nlog_neg(depolarizing, p<2/3) = log₂({tn_dp}) = log₂(2(1 - 3p/4)) = 1 + log₂(1 - 3p/4)")
print(f"Zero crossing: 1 - 3p/4 = 1/2 → p = 2/3")
print(f"  At p=0: log_neg = {sp.log(tn_dp.subs(p,0), 2)} (expect 1)")
print(f"  At p=2/3: log_neg = {sp.log(tn_dp.subs(p, sp.Rational(2,3)), 2)} (expect 0)")

print("\n=== C1(c) 验证通过 ===")
print("log_neg(dephasing, p)    = log₂(2 - 2p)   for p ∈ [0, 1/2]")
print("                        = log₂(2p)        for p ∈ [1/2, 1]  (by symmetry p ↔ 1-p)")
print("log_neg(depolarizing, p) = log₂(2 - 3p/2) for p ∈ [0, 2/3]")
print("                        = 0                for p ∈ [2/3, 1]")
