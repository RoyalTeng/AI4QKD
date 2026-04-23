"""SymPy verify: log_neg of qubit erasure channel Choi state."""
import sympy as sp

p = sp.Symbol('p', positive=True, real=True)

# Erasure channel: |i⟩_A → √(1-p)|i⟩_B + √p|e⟩_B (|e⟩ ⊥ |0⟩,|1⟩)
# Output Hilbert space dim = 3: basis {|0⟩, |1⟩, |e⟩}
# Kraus: K0 = √(1-p) [[1,0],[0,1],[0,0]] (2→3 isometry, identity on qubit, zero on |e⟩)
# K1 = √p [[0,0],[0,0],[1,0]] (maps |0⟩→|e⟩)
# K2 = √p [[0,0],[0,0],[0,1]] (maps |1⟩→|e⟩)
# Wait, standard erasure has single Kraus per |i⟩→|e⟩. Let me redo.
# K0 = √(1-p) (|0⟩⟨0| + |1⟩⟨1|) (preserve), K_e0 = √p |e⟩⟨0|, K_e1 = √p |e⟩⟨1|

K0 = sp.sqrt(1-p) * sp.Matrix([[1,0],[0,1],[0,0]])  # 3x2: identity on qubit, zero in |e⟩
Ke0 = sp.sqrt(p) * sp.Matrix([[0,0],[0,0],[1,0]])    # 3x2: |0⟩ → |e⟩
Ke1 = sp.sqrt(p) * sp.Matrix([[0,0],[0,0],[0,1]])    # 3x2: |1⟩ → |e⟩

# Verify CPTP: sum K† K = I_2
sum_KK = K0.T*K0 + Ke0.T*Ke0 + Ke1.T*Ke1
print(f"Sum K†K = {sp.simplify(sum_KK)} (should be I_2)")

# Choi state on H_A ⊗ H_B = C^2 ⊗ C^3 = C^6
# |Φ⁺⟩ = (|00⟩+|11⟩)/√2 in C^2 ⊗ C^2 (input, all qubit basis)
# After channel applied to B: |Ψ⟩ = (I ⊗ K)|Φ⁺⟩, Choi = sum_K |Ψ⟩⟨Ψ|

# Basis ordering for output: A in {0,1}, B in {0,1,e}: 6-dim, index = 3*a + b
# |0⟩_A: indices 0,1,2 (B = 0, 1, e)
# |1⟩_A: indices 3,4,5

phi_plus_in = sp.Matrix([sp.Rational(1)/sp.sqrt(2),0,0,sp.Rational(1)/sp.sqrt(2)])  # in C^2 ⊗ C^2

I2 = sp.eye(2)
from sympy.physics.quantum import TensorProduct as TP

def choi_contrib(K):
    """Apply (I_A ⊗ K_B) to |Φ⁺⟩ (4-dim input) → 6-dim output."""
    # K is 3x2 (B input → B output)
    # I_A ⊗ K: maps C^2 ⊗ C^2 → C^2 ⊗ C^3
    M = TP(I2, K)
    v = M * phi_plus_in
    return v * v.T

rho = choi_contrib(K0) + choi_contrib(Ke0) + choi_contrib(Ke1)
rho = sp.simplify(rho)
print("\nChoi state (6x6):")
print(rho)

# Partial transpose on B (dim 3)
def ptB_2x3(rho):
    """Partial transpose on B subsystem of dim_A=2, dim_B=3."""
    new = [[0]*6 for _ in range(6)]
    for a in range(2):
        for b in range(3):
            for c in range(2):
                for d in range(3):
                    old_i = 3*a + b
                    old_j = 3*c + d
                    new_i = 3*a + d
                    new_j = 3*c + b
                    new[new_i][new_j] = rho[old_i, old_j]
    return sp.Matrix(new)

rho_pt = ptB_2x3(rho)
print("\nρ^{T_B}:")
print(sp.simplify(rho_pt))

eigs = sp.simplify(rho_pt).eigenvals()
print("\nPT eigenvalues:")
total = 0
for e, m in eigs.items():
    print(f"  {sp.simplify(e)} × {m}")
    total += e * m
print(f"  Sum (should be 1): {sp.simplify(total)}")

# Predicted: ρ = (1-p)|Φ⁺⟩⟨Φ⁺| (in 2⊗2 sub-block, padded to 2⊗3 by zeros)
#            + p·(I_A/2) ⊗ |e⟩⟨e|
# PT eigenvalues:
#   - From (1-p)|Φ⁺⟩⟨Φ⁺|: as before, ±(1-p)/2 with mults 3 and 1 in the 4-dim sub-block
#     But in 6-dim, the |e⟩ rows/cols are zero; eigenvalues from 2⊗2 sub-block: ±(1-p)/2
#   - From p·(I_A/2) ⊗ |e⟩⟨e|: 2-dim sub-block with eigenvalue p/2 each
# Total: {(1-p)/2 × 3, -(1-p)/2 × 1, p/2 × 2}
# Trace norm = 3*(1-p)/2 + (1-p)/2 + 2*(p/2) = 2(1-p) + p = 2 - p

trace_norm = sp.Rational(3) * (1-p)/2 + (1-p)/2 + p
trace_norm = sp.simplify(trace_norm)
print(f"\nPredicted trace norm = {trace_norm} (should be 2-p)")

print(f"\nlog_neg(erasure, p) = log₂(2 - p)")
print(f"  At p=0: {sp.log((2-p).subs(p,0), 2)} (expect 1)")
print(f"  At p=1: {sp.log((2-p).subs(p,1), 2)} (expect 0)")
print(f"  At p=0.5: {sp.simplify(sp.log((2-p).subs(p,sp.Rational(1,2)), 2))}")
