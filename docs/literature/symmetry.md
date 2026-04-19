# Symmetry Reduction for QKD SDP 精读(Level 2-3)

**论文引用**:
- Ferenczi, A., Lütkenhaus, N. (2012). *Symmetries in quantum key distribution and the connection between optimal attacks and optimal cloning.* Physical Review A **85**, 052310. arXiv:1112.3396
- (辅助)Werner, R. F. (1989). *Quantum states with Einstein-Podolsky-Rosen correlations admitting a hidden-variable model.* PRA 40:4277 —— Werner 态原始定义
- (WLC 应用)CML 2016 §V.A,WLC 2018 §IV.C

**精读日期**:2026-04-19
**精读等级**:**Level 2-3 混合**
- Level 3:twirling map + BB84 Clifford 约化 + Werner 态参数化
- Level 2:Ferenczi-Lütkenhaus 2012 §IV-V 的一般群对称理论(待 Phase 2 上界 SDP 需要 non-abelian 结构时升级)

---

## 1. 一句话总结

QKD 协议**显式具有**量子力学群对称性(例如 BB84 在 Clifford 群下不变),通过在群平均下把 SDP 变量强制到**不变子空间**,可以把 $d^2$-维 SDP 约化到参数更少的 SDP 或 **闭式公式**。对 BB84,约化后是 2 自由度参数族(Bell-对角 Werner 态),WLC 目标 D(·||Z(·)) 直接**解析可算**。

---

## 2. 概念地图

```
 Full SDP on ρ ∈ PSD(d²)           ◄── |group|^{-1} Σ_g U_g ⊗ U_g ρ U_g† ⊗ U_g† ─┐
  │                                                                              │
  │ min f(ρ) s.t. constraints                                                    │
  │                                                                              │
  │         (convex in ρ; constraints invariant under G)                         │
  │                                                                              │
  ▼                                                                              │
 By convexity + group average:                                                   │
 Optimum attained at a G-invariant state ρ_sym  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┘
  │
  ▼
 ρ_sym lives in a lower-dim convex set (by representation theory)
 ⇒ smaller, faster SDP (possibly trivial, i.e., unique ρ_sym)
```

**关键定理(Ferenczi-L 2012 Prop. 2)**:若 $G$ 的表示 $\rho \mapsto U_g \rho U_g^\dagger$ 保持目标和约束不变,则存在 optimum $\rho^*$ 满足 $\text{Twirl}_G(\rho^*) = \rho^*$。

---

## 3. BB84 的对称群 + 约化

### 3.1 BB84 对称群 $G_{\text{BB84}}$

BB84 对称去极化信道 with $Q_Z = Q_X$ 不变于以下双边(bilateral)局部算子:

1. **$I \otimes I$**(trivial)
2. **$\sigma_Z \otimes \sigma_Z$**(phase flip 双侧 — 保持 Bell 基标签)
3. **$\sigma_X \otimes \sigma_X$**(bit flip 双侧)
4. **$\sigma_Y \otimes \sigma_Y$**(= $\sigma_X \sigma_Z \otimes \sigma_X \sigma_Z$,up to phase)
5. **$H \otimes H$**(Hadamard 双侧 — 交换 Z 基和 X 基 **⇒** 若 $Q_Z = Q_X$ 则不变)

**注意**:若$Q_Z \neq Q_X$,则 $H \otimes H$ **不是对称** —— 只保留 Pauli 子群(4 元素)。

对称群 $G_{\text{BB84}}$(含 Hadamard,symmetric $Q_Z = Q_X$ 情形):**Klein 四群** $\times \langle H \otimes H \rangle \cong \mathbb{Z}_2^3$,8 元素。

### 3.2 Twirling Map

定义:
$$\mathcal{T}_G(\rho) = \frac{1}{|G|} \sum_{g \in G} (U_g \otimes V_g) \rho (U_g \otimes V_g)^\dagger$$

其中 $V_g$ 对 Bob 侧可以是 $U_g$、$U_g^*$、或 transpose (依 representation 约定)。对 BB84 用 bilateral same-matrix $V_g = U_g$。

### 3.3 Bell 基 Werner 参数化

Bell 基 $\{|\Phi^+\rangle, |\Phi^-\rangle, |\Psi^+\rangle, |\Psi^-\rangle\}$ 下,$G_{\text{BB84}}$ 作用**置换** Bell 态。具体:
- $\sigma_X \otimes \sigma_X$:$\Phi^+ \leftrightarrow \Psi^+$,$\Phi^- \leftrightarrow \Psi^-$
- $\sigma_Z \otimes \sigma_Z$:$\Phi^- \leftrightarrow \Psi^+$(其他不变)? 不对,let me recompute:
  $(\sigma_Z \otimes \sigma_Z)|00\rangle = |00\rangle$,$(\sigma_Z \otimes \sigma_Z)|11\rangle = |11\rangle$ ⇒ $\Phi^\pm$ 不变。
  $(\sigma_Z \otimes \sigma_Z)|01\rangle = -|01\rangle$,$(\sigma_Z \otimes \sigma_Z)|10\rangle = -|10\rangle$ ⇒ $\Psi^\pm$ 同号变号,整体态相等(phase 吸收)。
  So $\sigma_Z \otimes \sigma_Z$ **不** 置换 Bell 态,是 stabilizer。
- $H \otimes H$:$|\Phi^+\rangle \to |\Phi^+\rangle$(交换 Z 和 X 同态),$|\Psi^-\rangle \to |\Psi^-\rangle$(反对称保持),$|\Phi^-\rangle \leftrightarrow |\Psi^+\rangle$。

**Twirled state structure**:经 $G_{\text{BB84}}$ average 后,$\rho$ 在 Bell 基下是对角,且 $\lambda_{\Phi^-} = \lambda_{\Psi^+}$。

⇒ **2 自由度参数化** $(F, \mu)$:
$$\rho_{\text{sym}} = F \cdot |\Phi^+\rangle\langle\Phi^+| + \mu \cdot (|\Phi^-\rangle\langle\Phi^-| + |\Psi^+\rangle\langle\Psi^+|) + (1-F-2\mu) \cdot |\Psi^-\rangle\langle\Psi^-|$$

### 3.4 约束翻译

- $\text{Tr}(\Gamma_Z \rho_{\text{sym}}) = \lambda_{\Psi^+} + \lambda_{\Psi^-} = \mu + (1-F-2\mu) = 1 - F - \mu$
  ⇒ 令 $= e$:$F + \mu = 1 - e$
- $\text{Tr}(\Gamma_X \rho_{\text{sym}}) = \lambda_{\Phi^-} + \lambda_{\Psi^-} = \mu + (1-F-2\mu) = 1 - F - \mu$
  ⇒ 与 $\Gamma_Z$ **相同约束**(在对称情形下自动成立,这正是 $Q_X = Q_Z$ 的表现)
- trace $= 1$:$F + 2\mu + (1-F-2\mu) = 1$ ✓ auto

只有 **1 个独立线性约束** + PSD。2 自由度剩 1 ⇒ **单参数 SDP**:
$$\min_{F, \mu: F+\mu = 1-e,\ F, \mu, 1-F-2\mu \geq 0} D(\rho_{\text{sym}} \| \mathcal{Z}(\rho_{\text{sym}}))$$

### 3.5 BB84 的 1-参数 SDP 解析

在 §3.4 的 1-参数族中,目标函数 $D(\cdot \| \mathcal{Z}\cdot)$ 是凸 + 关于 $\mu$(或 $F$)的函数。最优在 Werner 态($\mu = e/2$,$F = 1 - 3e/2$)处取到 —— 这就是 BB84 symmetric case 的 WLC 闭式解 [CML 2016 §V.A]:

$$\min D = 1 - h(e)$$

正是 Shor-Preskill 密钥率的来源 $R = (1/2)(1 - h(e) - f_{\text{ec}} h(e))$。

### 3.6 非对称 $Q_Z \neq Q_X$ 情形

此时 $H \otimes H$ 不再是对称,$G$ 退化到 4-元 Pauli 群。twirled 形式保留 Bell-对角,但 **$\lambda_{\Phi^-} \neq \lambda_{\Psi^+}$** 一般。约化结果是 **3 自由度**(2 独立 + PSD)SDP,仍比 $d^2 = 16$ 实自由度的完整 SDP 小。

---

## 4. 与本项目的 Bearing

### 4.1 M4A 直接用途

按 [RESEARCH_PLAN §2.4](../RESEARCH_PLAN.md) R4A.2:
- `qkdx/symmetry/groups.py`:定义 BB84 的 G_BB84 (双边 Clifford 8 元素)
- `qkdx/symmetry/twirling.py`:twirling map 实现
- 验证:对 BB84 4×4 ρ 做 twirling,然后跑 WLC SDP,数值应与 full 4×4 WLC 一致到 `rel=0.01, abs=5e-4`

### 4.2 对 Phase 1 Sub-Q2 Pareto search 的用途

Pareto search 中 BB84 family 的 symmetry-reduced SDP 比 full SDP 快 ~10-100x,使能 10³ 点扫描。

### 4.3 对 Phase 2 Sub-Q3 上界 SDP 的用途

相对熵 of entanglement 的 SDP 在对称协议上常 rank-deficient + symmetric;本 M4A 的 twirling + facial reduction 组合是 Phase 2 的基础工具。

---

## 5. Limitations

1. **Ferenczi-L 2012 一般群理论未深读**:当前只做 BB84 的 Klein-Hadamard 情形。Non-abelian 群(六态 Clifford + Y 对称)留 Phase 1 family sheet。
2. **Werner 态唯一性证明**:本 memo 只用表示论直觉,严格证明"G_BB84 不变态 ⇔ Bell-diag with $\lambda_{\Phi^-} = \lambda_{\Psi^+}$" 留 Level 4 升级。
3. **MDI 的 symmetry reduction**:双源情形下 MDI 的对称群结构未讨论(归 Phase 1 MDI family sheet)。

---

## 6. 下一步

1. ✅ Memo(本文件)
2. 🔄 R4A.2 实施([qkdx/symmetry/](../../qkdx/symmetry/))
3. 🔄 硬验收:`test_twirled_bb84_equals_full_wlc`
