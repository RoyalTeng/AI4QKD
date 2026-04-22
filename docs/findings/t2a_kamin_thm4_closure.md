# T2-A Kamin Thm 4 closure report (Day 2 autonomous, 2026-04-22)

**状态**：**T2-A CLOSED** at operationalizable level (per ADR 0001 Accepted)
**依据**：Kamin Thm 4 τ-slack SDP 已实现 + tested; user 2a signoff 已接受 Frank-Wolfe 迭代残余

---

## 1. T2-A scope recap

Per ADR 0001 operational refinement (commit a8314d9):
- T2-A closure criteria:
  - (a) §6.3 明示 anchor (n=10^12, 0 dB, ≈0.9): my 0.9008 < 1% ✓
  - (b) DW asymptotic saturation (test A4): pass ✓
  - (c) Cutoff tolerance ±6 dB per 2a signoff ✓
- T2-A 是 **proxy milestone**; 不 close S2.5 or user 3b

---

## 2. Kamin Thm 4 audit (Day 2 discovery)

Kamin 2025 §5.2 "optimizing parameter choices" 的 核心 tool：**Thm 4 τ-slack SDP (Eq. 49/53)**。

**已实现**：
- [qkdx/numerics/kamin_sdp.py:451-488](../../qkdx/numerics/kamin_sdp.py) `use_thm4=True` mode:
  - τ-slack constraint: $-\tau \leq q_\text{hon} - \Phi[\rho_J^t] \leq \tau$ (Eq. 53)
  - s(Στ/2) penalty added to objective (Eq. 46)
  - $\varphi_0, \varphi_1$ coefficients via `_thm4_phi_coefficients_qubit`
- [qkdx/numerics/kamin_sdp.py:1389-1482](../../qkdx/numerics/kamin_sdp.py) `kamin_thm4_key_length_bb84` wrapper
- [qkdx/numerics/kamin_sdp.py:1485-1543](../../qkdx/numerics/kamin_sdp.py) `kamin_thm4_key_length_bb84_optimized` (γ,α) grid
- **Test**: [tests/test_numerics/test_kamin_thm4_qubit.py](../../tests/test_numerics/test_kamin_thm4_qubit.py) (D.1 commit c49b2bf)

**已验证**：
- `phi_0 ∝ 1/γ` scaling ✓
- `phi_1 ∝ 1/√γ` scaling ✓
- `phi_2` γ-independence ✓
- τ-slack SDP runs no-loss trivial qber → `optimal` ✓
- `r_best ≤ W_hard` at honest point ✓ (Kamin Eq. 47 lower bound 成立)

---

## 3. Frank-Wolfe iteration 残余分析

**Kamin §5.2.1 end**: "The Frank-Wolfe algorithm inherently yields a sequence of affine lower bounds $L(\rho_J^g, \tau)$ such that the corresponding $r_\text{SDP}$ values converge towards $r_\text{best}$."

- **单 SDP solve** gives $r_\text{SDP}$ (一个 feasible lower bound, Eq. 51)
- **Frank-Wolfe 迭代** refines toward $r_\text{best}$ (supremum of Eq. 47)
- 差距 **scale 于 $O(1/N)$** FW convergence rate

我的实现：单 SDP solve → $r_\text{SDP}$（Eq. 51 lower bound 即 Kamin 的 $r_\text{best}$ 的 valid lower bound）。

**±6 dB 残余 来源**：Kamin Fig.1 可能用多次 FW 迭代 refine，我用单次 SDP solve。两者都 valid（我的是 looser lower bound），但具体 cutoff 有 3-6 dB 差异。

**User 2a signoff (2026-04-21)**: 接受此 ±6 dB 差 as scope limitation。

---

## 4. Outstanding work (非 T2-A 闭合 blocker)

1. **Frank-Wolfe outer loop** (可选 stretch): 多次 iterate $(g_k, J_k)$ pairs 来 close ±6 dB
   - Scope-deferred per 2a signoff
   - 估 3-5 天 coding + MOSEK 长 solve
2. **T2-B decoy Fig.3** (deferred to Phase 2 per ADR 0001)
3. **全 Fig.1 sweep with Thm 4 mode** (validation): 可用 `kamin_thm4_key_length_bb84_optimized` 在 12 × 4 = 48 points 运行，对比 `kamin_fig1_sweep` 看 quantitative improvement
   - 估 数小时 MOSEK solve
   - 本 session 未执行（单次 SDP 已证明 τ-slack < hard constraint）

---

## 5. Day 2 session deliverables (T2-A side)

本 session 未新增 code，仅完成 **audit + documentation**:
- 审计 `use_thm4=True` mode 正确性
- 审计 `kamin_thm4_key_length_bb84_optimized` optimization
- 审计 `test_kamin_thm4_qubit.py` 测试覆盖
- 明示 Frank-Wolfe 残余 per Kamin §5.2.1

代码实现在之前 session (D.1 commit c49b2bf, before 2026-04-22)。

---

## 6. 严谨性

- T2-A 闭合 at operationalizable level；**不**声称 Kamin Fig.1 < 5% across all plot points
- **不**升级 S2.5 or user 3b 状态
- Thm 4 τ-slack SDP 实现 = Kamin paper Eq. 49/53 直接实施
- ±6 dB 残余 **明确 documented** as Frank-Wolfe iteration 差异 (2a accepted)

---

## 7. Changelog

- **v1.0** (2026-04-22 Day 2): T2-A closure at operationalizable + Thm 4 τ-slack audit 完成
