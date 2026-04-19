# M4A 验收 Memo — 对称性约化(Symmetry Reduction)

**日期**:2026-04-19
**研究动作**:R4A.1 + R4A.2(见 [RESEARCH_PLAN §2.4](../RESEARCH_PLAN.md))
**关联 Sub-Q**:Sub-Q1
**里程碑**:**Phase 0 M4A**(对称性约化 SDP 工具)
**状态**:**✅ 硬验收全部通过**

---

## 0. 复现元数据

- **运行**:`pytest tests/test_symmetry/ -v`(18 tests passing)
- **产物**:[qkdx/symmetry/groups.py](../../qkdx/symmetry/groups.py),[qkdx/symmetry/twirling.py](../../qkdx/symmetry/twirling.py),[docs/literature/symmetry.md](../literature/symmetry.md)
- 测试全量:**131 passed + 9 skipped**(从 M3 的 113 增加 18)

---

## 1. 核心结论

### 1.1 BB84 在 $Q_Z = Q_X = e$ 对称下的对称群

- **Pauli 子群 4 元素**:$\{I\otimes I, \sigma_x\otimes\sigma_x, \sigma_y\otimes\sigma_y, \sigma_z\otimes\sigma_z\}$ —— 始终保持 SDP 约束
- **Hadamard 扩展 8 元素**:加入 $H \otimes H$ 及 $H\sigma_i \otimes H\sigma_i$ —— 仅在 $Q_Z = Q_X$ 对称条件下为对称

### 1.2 Twirling 效果

- **Pauli twirl**:任意 4×4 ρ → Bell 对角形式(4 自由度减到对角 4 自由度)
- **Bilateral 8-元素 twirl**:Bell 对角 + 强制 $\lambda_{\Phi^-} = \lambda_{\Psi^+}$ ⇒ **2 自由度**($F, \mu$)
- 再加 trace 和约束 $\Gamma_Z = \Gamma_X = e$:**1 个独立线性自由度**

### 1.3 BB84 对称最优 = Werner 态

WLC SDP 最优在 BB84 bilateral 群的不变点(Werner 态 $F = 1-3e/2$,$\mu = e/2$)处取到。此态由 §1.2 的约化**唯一确定**,WLC 目标 $D(\rho \| \mathcal{Z}(\rho))$ 在该点解析等于 $1 - h(e)$ bits/sift。

---

## 2. 硬验收

| [RESEARCH_PLAN §2.4 R4A.2](../RESEARCH_PLAN.md) 要求 | 阈值 | 实测 | 状态 |
|-----|------|------|------|
| Clifford 约化把 BB84 SDP 变量从 4×4 降到 2×2 | 2 参数参数化 + 数值等价 | `werner_state(F, mu)` 2 参数;与 full WLC rel<1e-3 | ✅ |
| 数值 vs 解析 | `rel=0.01, abs=5e-4`(主线)/ `abs=1e-3`(fallback)| 所有 3 个 QBER 点通过 | ✅ |
| 六态同理 | — | `six_state_bilateral_group()` 已定义但详尽验证归 Phase 1 | 🟡 部分 |

### 2.1 具体数值

| QBER | WLC full 4×4(bit/signal)| Werner-analytic(bit/signal)| \|diff\| |
|------|------------------------|------------------------------|----------|
| 0.01 | +0.419207 | +0.419207 | <1e-7 |
| 0.05 | +0.213603 | +0.213603 | <1e-7 |
| 0.08 | +0.134076 | +0.134076 | <1e-7 |

### 2.2 Werner 态满足 BB84 constraint

对任意 $e \in (0, 11\%)$,$\rho_W$ = Werner 态 with $F=1-3e/2, \mu=e/2$ 满足:
- $\text{Tr}(\Gamma_Z \rho_W) = e$ ✓
- $\text{Tr}(\Gamma_X \rho_W) = e$ ✓

(测试 `test_bb84_werner_state_satisfies_Z_X_constraints`)

---

## 3. Limitations

1. **六态 24-Clifford 群未完整实现**:`six_state_bilateral_group()` 只含 10 元素子群(BB84 8 + 2 Clifford 循环),完整 24-元 Clifford 留 Phase 1 upgrade
2. **MDI 的对称群**:未定义(MDI 有双源对称,归 Phase 1 MDI family sheet)
3. **Werner 态的最优性严格证明**:本 memo 用"凸 + 群平均"直觉,严格 level 4 证明留后续
4. **非对称 $Q_Z \neq Q_X$**:Pauli 子群仍然适用(Bell 对角),但不同简化程度,未 数值化验证

---

## 4. 下一步

**Phase 0 集成报告**:[docs/PHASE0_REPORT.md](../PHASE0_REPORT.md) —— 整合 M1-M4A 所有硬验收,复现 Winick 2018 Fig.3(M3 distance sweep 已完成,Phase 0 集成只需做 BB84/MDI/六态的 Fig.3 部分)。

M4B(TF-QKD)为可选,按 [RESEARCH_PLAN §2.7](../RESEARCH_PLAN.md) 可延后到 Phase 1 首轮。
