Reviewed [§2 memo](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/findings/beta_G3_golden_ratio_crossover_2026-04-23.md:95>), [analytic test class](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/tests/test_numerics/test_upper_bound.py:165>), [CLAUDE rules](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/CLAUDE.md:22>), and the repo’s [partial-transpose](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/qkdx/numerics/upper_bound.py:47>) and [Choi-state](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/qkdx/numerics/upper_bound.py:193>) conventions.

## MATH_CORRECTNESS
1. **Step 1: Choi state**
   Yes. With `|Φ⁺⟩ = (|00⟩+|11⟩)/√2`,
   `(I⊗K₀)|Φ⁺⟩ = (|00⟩ + √η |11⟩)/√2` and `(I⊗K₁)|Φ⁺⟩ = √(1-η)|10⟩/√2`.
   Summing the two projectors gives
   \[
   \rho_{AD}(\eta)=\frac12\begin{pmatrix}
   1&0&0&\sqrt\eta\\
   0&0&0&0\\
   0&0&1-\eta&0\\
   \sqrt\eta&0&0&\eta
   \end{pmatrix},
   \]
   exactly as stated in the memo.

2. **Step 2: Partial transpose**
   Yes. Under `T_B`, the off-diagonal terms move as `|00⟩⟨11| -> |01⟩⟨10|` and `|11⟩⟨00| -> |10⟩⟨01|`, so
   \[
   \rho^{T_B}=\frac12\begin{pmatrix}
   1&0&0&0\\
   0&0&\sqrt\eta&0\\
   0&\sqrt\eta&1-\eta&0\\
   0&0&0&\eta
   \end{pmatrix}
   \]
   is correct.
   Minor notation point: in the displayed basis `|00⟩,|01⟩,|10⟩,|11⟩`, this is `1x1 ⊕ 2x2 ⊕ 1x1`; the stated `{|00⟩,|11⟩}` and `{|01⟩,|10⟩}` block split is correct up to a basis permutation.

3. **Step 3: Eigenvalues**
   Yes. For
   \[
   B=\begin{pmatrix}0&\sqrt\eta/2\\ \sqrt\eta/2&(1-\eta)/2\end{pmatrix},
   \]
   the characteristic polynomial is
   \[
   \lambda^2-\frac{1-\eta}{2}\lambda-\frac{\eta}{4}=0.
   \]
   The discriminant is
   \[
   \Delta=\frac{(1-\eta)^2}{4}+\eta=\frac{(1+\eta)^2}{4},
   \]
   so `sqrt(Δ)=(1+η)/2` on `[0,1]`, and
   \[
   \lambda_\pm=\frac{(1-\eta)\pm(1+\eta)}{4}
   \]
   gives `λ₊=1/2`, `λ₋=-η/2`.

4. **Step 4: Trace norm**
   Yes. The full spectrum is `{1/2, η/2, 1/2, -η/2}` up to ordering, hence
   \[
   \|\rho^{T_B}\|_1=\frac12+\frac{\eta}{2}+\frac12+\frac{\eta}{2}=1+\eta.
   \]
   Therefore
   \[
   \log\text{-neg}(\mathcal E_{AD}(\eta))=\log_2(1+\eta)
   \]
   for this normalized qubit Choi state.

5. **Step 5: Crossover equation**
   Mostly yes, but one clarification is needed. From
   \[
   2\log_2(1+\eta)=-\log_2(1-\eta)
   \]
   we get
   \[
   (1+\eta)^2(1-\eta)=1 \iff \eta(1-\eta-\eta^2)=0.
   \]
   So the equality solutions on `[0,1]` are `η=0` and `η=(√5-1)/2=1/φ`.
   Thus `1/φ` is the **nontrivial interior crossover**, while `η=0` is the trivial boundary equality.
   The memo should say that explicitly.

## SCOPE_LIMITATIONS
- This proves the formula only for the **qubit amplitude-damping channel with the stated Kraus pair**, not for bosonic pure-loss. The memo itself correctly warns that bosonic analysis is separate.
- It does not establish any general rule `log_neg = log₂(1+parameter)` for other channel families. A new Choi/PT spectrum calculation would be needed for each family.
- In repo API terms, note the parameterization mismatch: [upper_bound.py](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/qkdx/numerics/upper_bound.py:279>) uses `gamma = damping probability`, so the same formula there would read `log_neg = log₂(2-γ)`, not `log₂(1+γ)`.
- This does **not** close the umr structural gaps `β.G4` or `β.G5`. The memo itself still marks those as open in [§3](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/findings/beta_G3_golden_ratio_crossover_2026-04-23.md:155>).
- It also does not prove additivity of `E_R^PPT`; §1.5 is explicitly conditional `[CONJ-DRAFT]`.

## RIGOR_COMPLIANCE
- `[SYN]` is an appropriate live label. The claim is an internal AI-derived derivation, not yet a literature-anchored theorem/corollary under [R0.3](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/CLAUDE.md:52>).
- The memo is correct that any upgrade requires `C1 + C2 + C3` under [R0.2](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/CLAUDE.md:28>) and [§3.2](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/CLAUDE.md:127>). Human paper-and-pencil review can satisfy only `C1(b)`, not the full upgrade by itself.
- The phrase “用户纸笔复核可升至 [COROLLARY]” is too compressed. Even after `C1+C2+C3`, the claim still needs to fit the **semantic** definition of `[COROLLARY]` in R0.3, namely a mechanical derivation from an existing `[THM]`. As written, §2 reads more like a correct in-project derivation that should remain `[SYN]` unless that corollary anchor is made explicit.

## VERDICT
**SOUND** for the stated **qubit** channel and normalized Choi-state definition.

The linear algebra in §2 is correct. The changes I would require are only clarificatory: state that `η=1/φ` is the nontrivial interior crossover while `η=0` is the trivial boundary solution, keep the qubit-only scope explicit, and soften the implication that paper review alone would make the result a `[COROLLARY]`.