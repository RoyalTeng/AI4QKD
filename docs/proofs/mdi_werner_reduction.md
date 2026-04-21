# MDI-QKD Werner reduction — ideal symmetric entanglement-swap 下 raw-key 统计的 Werner 等价性

**版本**：v0.3 **[CONJ]**（autonomous session 2026-04-22，Round 3 FIX 响应 dev-reviewer Round 2 双 Codex REJECTED verdict）
**对应 RESEARCH_PLAN 动作**：§2.2 R2.1 Level 3 → Level 4 升级
**对应实现**：[qkdx/numerics/kamin_sdp_mdi.py](../../qkdx/numerics/kamin_sdp_mdi.py) line 23-28 docstring 所述 reduction
**预备知识**：[docs/literature/MDI-QKD.md](../literature/MDI-QKD.md) §3.1-§3.4

**严谨性分级**：**[CONJ]**。所有子引理标以 R0.3 四级标签 ([THM]/[COROLLARY]/[SYN]/[CONJ]/[UNKNOWN])。Round 2 verdict 指出 v0.2 使用 [VERIFIED]/[RECALLED] 作标签是**措辞错误**（provenance descriptors 不是 rigor grades）— v0.3 修正。

**触发本修订的 review verdict**（Round 2）：
- [Agent 1 diff (xhigh)](../workflow/werner-reduction/review-diff-2.json)：REJECTED (1 CRITICAL + 1 MAJOR)
- [Agent 2 holistic (high)](../workflow/werner-reduction/review-holistic-2.md)：REJECTED (NEW_REGRESSION — W2.5 内部矛盾)

**Round 3 CRITICAL 修复**：Round 2 W2.5 claim "Pauli correction 把 $W^{B_k}$ 映射到 $W^{\Phi^+}$" 是**quantum state 层错误**。实际上 Lo-Curty-Qi Table I 的 bit-flip 规则是**经典 post-processing**（对 raw key bit XOR），不是 quantum state 上的 Pauli 操作。正确 claim 是：**raw-key statistics equivalence**（QBER 数值等同于 $\Phi^+$-centered Werner），不是 quantum state equivalence。v0.3 重写 W2.5 + W4 以反映正确物理。

---

## 0. 目的与 scope

### 0.1 目的

为 [qkdx/numerics/kamin_sdp_mdi.py:23-28](../../qkdx/numerics/kamin_sdp_mdi.py) docstring 的核心 reduction claim 提供 **[CONJ] 级** conditional derivation。**不**声称 claim 已证；仅在 §0.3 的假设下给出 conditional argument。

原 docstring claim：

> "In the virtual-EB picture (Lo-Curty-Qi §II), after Charlie's successful Bell projection the conditional Alice-Bob state has the Werner form $\text{Tr}[|\Phi^+\rangle\langle\Phi^+| \cdot \rho_{AB}] = 1 - 3 \cdot \text{qber}/2$ (for the basis-matched-correct BSM). This is structurally identical to qubit BB84's Werner state at effective QBER, allowing DIRECT reuse of `kamin_choi_sdp_qubit_bb84`."

**v0.3 分析结论**：原 docstring 的"Werner form"表述**不完全正确**。正确的表述应为：

> **raw-key statistics are those of a $\Phi^+$-centered Werner state at effective QBER**。
> quantum state 本身是 **outcome-dependent Bell-centered Werner**，only the classical raw-key statistics (after Table I bit-flip correction) 与 Φ⁺-centered Werner 等同。

docstring 的 "Lo-Curty-Qi §II" 亦**错误**（virtual-EB picture 在 **Appendix A**）。这些为**docstring 措辞缺陷**；v0.3 **不**修改 docstring（避免非 scope 的 code 变动），但明确指出差异。

### 0.2 用户 review decision 来源

用户 2026-04-21 session 审阅项 1 → 选项 **(b)**：要求形式化证明。**此决定为 scope 指示**，**不**构成 R0.2 C2 sign-off。

### 0.3 Scope 严格限定（v0.2 延续 + v0.3 扩充）

| 假设 ID | 内容 | 违反后果 |
|---|---|---|
| A1 | $\eta_A = \eta_B = \eta_\text{arm}$ | Werner 参数不对称 → 输出非 Bell-diagonal |
| A2 | single-photon EB 源（virtual-qubit picture） | WCP / 诱骗态需广义 |
| A3 | 两臂 $\lambda_A = \lambda_B = \lambda$ | 输出非 Werner |
| A4a | 理想 50:50 BS + 理想 PBS + 完美 HOM 干涉 | 修正 visibility |
| A4b | Charlie 探测器理想（单位效率，零 dark count） | 扩展 POVM |
| A4c | 两臂光子完美 indistinguishable | 修正 interference |
| A5 | 无 basis misalignment | 非对称 QBER |
| A6 | Alice-Bob 按 Lo-Curty-Qi Table I 精确执行：同基 + 成功 BSM outcome 全接受；**bit-flip 规则依 basis + outcome 分类** | 不同 post-processing 给不同条件态 |

**Lo-Curty-Qi 2012 Table I 的精确内容**（PDF page 2 左栏，本文件 direct reading）：

| Alice-Bob 基 | BSM outcome $\|\Psi^-\rangle$ | BSM outcome $\|\Psi^+\rangle$ |
|---|---|---|
| **Rectilinear**（Z 基） | bit flip | bit flip |
| **Diagonal**（X 基） | bit flip | **no flip** |

（diagonal X-basis + $|\Psi^+\rangle$ **kept** but **no flip** — 即例外 case。Round 2 Agent 1 指出 v0.2 说 "也可能 discard" 是错误。v0.3 修正）

**Lo-Curty-Qi Table I 只覆盖 $\|\Psi^\pm\rangle$ outcome**，**不覆盖** $\|\Phi^\pm\rangle$ outcome — 这是因为**理想 linear-optic BSM 物理上无法 unambiguously 识别 $\Phi^\pm$**（HOM 干涉使 $\Phi^\pm$ 给两光子到同一探测器，与 vacuum + 2-photon events 混淆）。因此 A6 实际是：

**A6 精细版**：Alice-Bob post-select **only $\|\Psi^-\rangle$ or $\|\Psi^+\rangle$ outcomes**（即 $\Phi^\pm$ outcomes 被 linear-optic BSM 物理排除），并按 Table I 的 basis-dependent bit-flip 规则做 raw-key correction。

### 0.4 非覆盖情形

- 非对称 MDI（A1 / A3 violation）
- WCP + 诱骗态
- Misalignment > 0
- Dark count
- Finite-size / GEAT（由 Kamin 2025 framework 单独处理）
- **repo 代码 convention 差异**：[qkdx/core/bell_povm.py](../../qkdx/core/bell_povm.py) 使用 $\{\Phi^+, \Psi^-\}$ 作为 BSM success outcome；Lo-Curty-Qi 2012 Table I 使用 $\{\Psi^\pm\}$。两者都是**合法 MDI 变体**（Ma-Razavi 2012 允许 $\{\Phi^+, \Psi^-\}$ 通过不同实验硬件如 PNR detector + polarization-encoding）。本文件按 Lo-Curty-Qi 2012 Table I 的 $\{\Psi^\pm\}$ convention；**`bell_povm.py` convention 下需要单独 analogous derivation**，不在本 scope 内。

---

## 1. 符号约定

- $|\Phi^\pm\rangle, |\Psi^\pm\rangle$：Bell 基
- Alice：A（virtual key register） + A'（photon mode）；Bob：B + B'
- $\mathcal{E}_\lambda$：depolarizing channel
- $W_F^B$：$B$-centered Werner state ($F$ weight to $|B\rangle\langle B|$, $(1-F)/3$ to 其他 Bell)
- 默认 $W_F := W_F^{\Phi^+}$
- $q$：effective MDI QBER (Z 或 X basis, 同值 per Werner 对称性)

---

## 2. Concept map

```
   Lo-Curty-Qi Appendix A: virtual-EB picture
              │
              ▼
   Lemma W1 (§5): 每臂 depolarizing →  Φ⁺-centered Werner $W_{F_1}$
              │
              ▼
   Lemma W2 (§6): entanglement swap + BSM → outcome-dependent Werner
              $W_{F'}^{B_k}$, centered on $k$-th Bell outcome
              $F' = F_1^2 + (1-F_1)^2/3$
              │
              ▼
   Lemma W2.5 (§7): Table I bit-flip (classical post-processing on raw key bits)
              raw-key statistics 等同于 Φ⁺-centered Werner same-F'
              (NOT quantum state Pauli correction)
              │
              ▼
   Lemma W3 (§8): Φ⁺-Werner QBER_Z = QBER_X = 2(1-F')/3
              │
              ▼
   Lemma W4 (§9): Kamin BB84 Choi SDP delegation validity
              [CONJ conditional on A1-A6 + SDP structural equivalence]
```

---

## 3. Key results

| 标签 | 陈述 | 严谨性 |
|---|---|---|
| W1 | depolarizing on Bell pair → $\Phi^+$-centered Werner $W_{F_1}$, $F_1 = 1 - 3\lambda/4$ | **[THM]** (教科书：Nielsen-Chuang §8.3.4 + §2.4；本项目独立代数复现) |
| W2 | entanglement swap of two $W_{F_1}$ with BSM outcome $B_k$ → $B_k$-centered Werner $W_{F'}^{B_k}$, $F' = F_1^2 + (1-F_1)^2/3$ | **[CONJ]** (本项目数值 verify for λ=0.1 single probe；代数推导 recalled from repeater literature 但未独立复现 + 未 PDF-verify 具体 Eq.) |
| W2.5 | Table I 基 + outcome 分类的 classical bit-flip 使 raw-key statistics 等同于 Φ⁺-centered Werner same-F' | **[CONJ]** (本项目数值 verify for $F=0.857$；Lo-Curty-Qi Table I direct reading + 本项目代数分析) |
| W3 | $\Phi^+$-Werner $W_F$ has $q_Z = q_X = 2(1-F)/3$ | **[THM]** (elementary Bell basis 展开；本项目独立复现 + 数值 verify) |
| W4 | Kamin BB84 Choi SDP `kamin_choi_sdp_qubit_bb84(qber=q)` h_per_sift = MDI post-Table-I conditional h_per_sift | **[CONJ conditional on A1-A6 + W2.5 + SDP structural equivalence]** |

---

## 4. Virtual-EB 归约（Lo-Curty-Qi 2012 Appendix A）

[内容与 v0.2 相同，略]

---

## 5. Lemma W1：depolarizing on Bell pair → $\Phi^+$-centered Werner  **[THM]**

设 $|\Phi^+\rangle_{AA'}$，对 A' 施加 $\mathcal{E}_\lambda$，则：

$$\rho_{AA'} = W_{F_1}^{\Phi^+}, \quad F_1 = 1 - \frac{3\lambda}{4}.$$

证明：

$$(\mathcal{I} \otimes \mathcal{E}_\lambda)|\Phi^+\rangle\langle\Phi^+| = (1-\lambda)|\Phi^+\rangle\langle\Phi^+| + \lambda \cdot I_A/2 \otimes I_{A'}/2$$

$$I/2 \otimes I/2 = \frac{1}{4}\sum_B |B\rangle\langle B|$$

$$\Rightarrow \rho_{AA'} = (1-3\lambda/4)|\Phi^+\rangle\langle\Phi^+| + (\lambda/4)\sum_{B \neq \Phi^+}|B\rangle\langle B| = W_{F_1}^{\Phi^+}.$$ □

**等级 [THM]**：教科书级标准结果 (Nielsen-Chuang §8.3.4 + §2.4)；本项目独立代数复现。对 R0.3 grade 判断：符合 [THM] "文献定理 + 原始拓扑对齐 + 继承 lemma 验证" 三条件（原始单信道 + 继承平凡）。

---

## 6. Lemma W2：outcome-dependent Bell-centered Werner after swap  **[CONJ]**

设 $\rho_{AA'} = \rho_{BB'} = W_{F_1}^{\Phi^+}$，Charlie 在 (A', B') 做 BSM。对每个 outcome $B_k$：

1. $p_k^\text{BSM} = 1/4$（对称性）
2. conditional 条件态：$\rho_{AB}^{(k)} = W_{F'}^{B_k}$，$F' = F_1^2 + (1-F_1)^2/3$

**证据**：

**(a) 本项目数值 verify** (2026-04-22 autonomous session，独立 Python NumPy script)，$\lambda = 0.1 \Rightarrow F_1 = 0.925$，$F'$ 预测 $= 0.8575$：

| BSM outcome | $F(\Phi^+)$ | $F(\Phi^-)$ | $F(\Psi^+)$ | $F(\Psi^-)$ |
|---|---|---|---|---|
| $\Phi^+$ | **0.8575** | 0.0475 | 0.0475 | 0.0475 |
| $\Phi^-$ | 0.0475 | **0.8575** | 0.0475 | 0.0475 |
| $\Psi^+$ | 0.0475 | 0.0475 | **0.8575** | 0.0475 |
| $\Psi^-$ | 0.0475 | 0.0475 | 0.0475 | **0.8575** |

（dominant Bell weight 与预测 $F'$ 一致，其他 Bell 权重 $= (1-F')/3$）

**(b) 文献方向性引用**（**未 PDF-level 核对 Eq. 编号**）：

Werner-under-swap 公式 $F' = F_1^2 + (1-F_1)^2/3$ 在 quantum repeater 文献中是标准结果。相关文献：
- Briegel-Dür-Cirac-Zoller 1998, "Quantum Repeaters: The Role of Imperfect Local Operations", PRL 81:5932, arXiv:quant-ph/9803056 — 含 swap 下 depolarization 参数更新（本项目**未 PDF-level 核对** Eq. 编号）
- Dür-Briegel-Cirac-Zoller 1999, "Quantum repeaters based on entanglement purification", PRA 59:169, arXiv:quant-ph/9808065 — 相关主题

**等级 [CONJ]**：
- 代数未独立复现（本项目 numerical single-probe verify at $\lambda=0.1$ 不构成公式严格证明）
- 文献引用未 PDF-level 核对 Eq. 编号
- 需要 C1(a) 或 C1(b) 独立验证升级

---

## 7. Lemma W2.5：Table I classical bit-flip 等价性  **[CONJ]** (**v0.3 重写**)

### 7.1 陈述

对 W2 输出的 $W_{F'}^{B_k}$，Alice-Bob 按 Lo-Curty-Qi Table I 做**经典 post-processing**（raw-key bit XOR）。声称：**post-correction raw-key 统计分布与 $W_{F'}^{\Phi^+}$ 直接测量（无 flip）的统计分布相同**。

**关键区分**（Round 2 REJECTED 时识别的修正）：
- **错误 (Round 2)**：Table I bit-flip 对应 local Pauli 算子 $\Leftrightarrow$ quantum state $W_{F'}^{B_k} \to W_{F'}^{\Phi^+}$
- **正确 (v0.3)**：Table I bit-flip 是 **classical post-processing** on raw-key bits（Z-basis Alice bit XOR 1 or X-basis Alice bit XOR 1 per table rule）—— quantum state $W_{F'}^{B_k}$ **不变**；只是 raw-key sampling statistics 经 basis-dependent flip 后等同于 $W_{F'}^{\Phi^+}$ 的 raw statistics。

### 7.2 证明（数值 verify + algebra）

**声称**：对 Lo-Curty-Qi Table I 接受的 MDI success outcome $B_k \in \{\Psi^-, \Psi^+\}$：
- Z-basis raw QBER_Z (post Table I flip) $= 2(1-F')/3$
- X-basis raw QBER_X (post Table I flip) $= 2(1-F')/3$

即与 $W_{F'}^{\Phi^+}$ 的 $q_Z = q_X = 2(1-F')/3$（见 Lemma W3）**数值相同**。

**代数分析**：

对每个 $B_k$，$W_{F'}^{B_k}$ 的 Z/X 基测量 Alice-Bob outcome 联合分布：

$|\Psi^-\rangle = \frac{1}{\sqrt{2}}(|01\rangle - |10\rangle)$：Z 基 → $P(01)=P(10)=1/2$（**anti-correlated**）；X 基下 $|\Psi^-\rangle = -\frac{1}{\sqrt{2}}(|+-\rangle - |-+\rangle)$ → $P(+-)=P(-+)=1/2$（**anti-correlated**）

$|\Psi^+\rangle = \frac{1}{\sqrt{2}}(|01\rangle + |10\rangle)$：Z 基 → anti-correlated；X 基下 $|\Psi^+\rangle = \frac{1}{\sqrt{2}}(|++\rangle - |--\rangle)$ → **correlated**（$P(++)=P(--)=1/2$）

所以：
- $W_{F'}^{\Psi^-}$：Z anti-correlated，X anti-correlated → **两基都需 bit flip** 才能 raw-key agreement
- $W_{F'}^{\Psi^+}$：Z anti-correlated，X correlated → **Z 需 flip，X 不需 flip** 才能 raw-key agreement

**Table I 正是这样规定**！（A6 精细版，§0.3 Table）

### 7.3 数值 verify

2026-04-22 session 内独立 Python script 对 $F = 0.857$ 计算（四舍五入给 QBER $\approx 0.095$）：

| State + correction | QBER_Z (post-flip) | QBER_X (post-flip or identity) |
|---|---|---|
| $W_{F}^{\Phi^+}$ (no flip needed) | 0.0953 | 0.0953 |
| $W_{F}^{\Psi^-}$ + Z flip + X flip | 0.0953 | 0.0953 |
| $W_{F}^{\Psi^+}$ + Z flip + no-X-flip | 0.0953 | 0.0953 |

**全部 0.0953 = $2(1-F)/3$ with $F = 0.857$**（数值 agreement within float precision）✓

### 7.4 严谨性判定

**等级 [CONJ]** (not [THM])：

- 数值 verify 覆盖 $F = 0.857$ single probe（需要 analytic proof for all $F$ 才能升 [THM]）
- A6 Table I PDF-level 核对是 direct reading；**未**经 C1(a) 跨家族 AI 或 C1(b) 人类 独立 verify
- $W^{\Phi^+}$ claim 的 Lo-Curty-Qi Table I 连接 —— PDF 直接读和本项目代数分析—— 本身 sound but 依赖 **Werner state 对称性** (Z/X basis Werner QBER 相同)，此点已由 Lemma W3 建立

**降级理由**：W2.5 是本项目 Lemma W1-W3 + Table I reading 的**合成**，符合 R0.3 "AI 起草的合成陈述**默认** [SYN] 或更低" 原则。

---

## 8. Lemma W3：$\Phi^+$-Werner 的 QBER 参数化  **[THM]**

（内容与 v0.2 相同：代数 elementary）

$W_F^{\Phi^+}$ 满足 $q_Z = q_X = \frac{2(1-F)}{3}$。

**等级 [THM]**：elementary Bell basis 展开；本项目独立复现。

---

## 9. Lemma W4：Kamin BB84 Choi SDP delegation  **[CONJ]**

### 9.1 陈述

**目标 claim**：`kamin_choi_sdp_qubit_bb84(qber=q)` 的 h_per_sift 数值等同于 MDI post-Table-I conditional state 的 h_per_sift（同 $q$ 值）。

### 9.2 推导链

1. W1：$\lambda \to F_1 = 1 - 3\lambda/4$；Werner$^{\Phi^+}$ 两 arm 输出
2. W2：BSM outcome $B_k \to$ Werner$^{B_k}$ 条件态，$F' = F_1^2 + (1-F_1)^2/3$
3. W2.5：Table I 经典 flip 给 raw-key QBER_Z = QBER_X = $2(1-F')/3$（与 Werner$^{\Phi^+}$ 同 F' 的 QBER 等同）
4. W3：QBER 参数化 $q = 2(1-F')/3$

### 9.3 关键 gap（未 close）

**gap G1**：W1-W3 给的是 Werner state 参数化与 QBER 映射。**但** Kamin BB84 Choi SDP（[qkdx/numerics/kamin_sdp.py:297-335](../../qkdx/numerics/kamin_sdp.py)) 的 input 不是 "QBER 数值"，而是**full Choi state 参数化**。SDP 对 $J$ (Choi) 做约束优化 — 需要证明 **MDI post-Table-I Effective conditional Choi structure** 与 **BB84 EB-reduced Choi structure** 在 SDP 约束层**结构等价**。

具体地：
- Kamin BB84 SDP 在测试轮（X-basis）观察 QBER_X，优化 $J_1$ 以 minimize privacy rate 约束 $\Phi[\rho_{J_1}^t] = q_\text{obs}$
- MDI 测试轮（X-basis）观察 QBER_X from raw key stats post-Table-I flip
- **若 SDP "结构等价" 成立**：同 QBER 值下两者给出同 $J_1$ 优化（up to basis labeling），therefore 同 h_per_sift

"结构等价" 断言本身是 [CONJ]。未严格证；数值测试 `tests/test_numerics/test_kamin_sdp_mdi.py` pass 为 codebase 自洽性证据（**not** 独立证明）。

### 9.4 等级判定

**[CONJ conditional on]**：
- A1-A6 scope assumptions
- W1-W3 chain ([CONJ] W2, [THM] W1+W3)
- W2.5 classical correction chain ([CONJ])
- **SDP 结构等价性**（**未证**）
- 测试 5/5 pass 的 codebase 自洽性（**non-independent**）

Round 2 Agent 1 原意正确：v0.2 的"operates on conditional state itself"措辞过 loose；v0.3 显式 gap G1 并保 [CONJ]。

---

## 10. 数值 sanity check

### 10.1 极限

| $\lambda$ | $F_1$ | $F'$ | $q$ | $h_\text{per_sift}$ | |
|---|---|---|---|---|---|
| 0 | 1 | 1 | 0 | 1 | no-noise limit ✓ |
| 1 | 1/4 | 1/4 | 1/2 | 0 | full-depol limit ✓ |

### 10.2 数值 probe：$\lambda = 0.1$

$F_1 = 0.925$，$F' = 0.8575$，$q = 0.0953$.

**Python 独立 NumPy 验证** (§6 + §7.3)：BSM 四 outcome 各给对应 Bell-centered Werner ($F' = 0.8575$)；Table I flip 后各 outcome QBER_Z = QBER_X = 0.0953 ✓

### 10.3 与 Kamin SDP test 对照

[tests/test_numerics/test_kamin_sdp_mdi.py](../../tests/test_numerics/test_kamin_sdp_mdi.py) 5/5 测试：
- `h_per_sift` 在同 QBER 下 MDI 数值 = BB84 数值 (abs < 1e-6)
- $n=10^{12}, 0$ dB, $q=0.01$: rate $\approx 0.22$

**标注**：同代码库自洽性检查，**非** R0.2 C1 独立验证。

---

## 11. Scope limits 与 upgrade path

### 11.1 本文件未证的

- W2 公式代数独立复现
- W2.5 的 analytic proof for all $F$（现仅 numerical single probe）
- W4 的 SDP 结构等价性
- 非对称 / misalignment / decoy / finite-key 情形

### 11.2 Upgrade 路径 — R0.2 C1 ∧ C2 ∧ C3 (**严格 invariant**)

**C1 independent validation**：
- (a) 另一家族 AI 读 Lo-Curty-Qi PDF Appendix A + Table I + Briegel 1998 + Dür 1999 独立复核
- (b) 人类纸笔复核 W2 代数（16-dim → 4-dim 部分 trace）+ W2.5 Table I 对照
- (c) 非 AI 工具（Mathematica symbolic / Cirq / QIP library）独立 verify Werner-under-swap 公式

**C2 用户签字**：用户归来逐项确认。**未满足**。

**C3 dev-reviewer PASS**：未满足（Round 2 REJECTED, v0.3 Round 3 待评）。

### 11.3 本文件不做的

- 不升级 `kamin_sdp_mdi.py:23-28` docstring
- 不改 FINDINGS v2 分级
- 不改 Log 07 umr 上界 [CONJ] 状态
- 不修 `qkdx/core/bell_povm.py` 的 BSM convention（不在 scope）

---

## 12. 与本项目的 bearing

### 12.1 Sub-Q2 Phase 1 S2.5 直接

本 memo 提供 `kamin_sdp_mdi.py` docstring 的**conditional 正确性论证**（[CONJ] 级，A1-A6 scope）。**不**升级 S2.5 硬验收状态。

### 12.2 Sub-Q3 path α / β / γ 间接

纯态操作级 analysis，与 network capacity 级分析不同层级；不影响 umr 上界 [CONJ] 状态。

### 12.3 PROSPECTUS 主问题

无直接 bearing。

---

## 13. Changelog

- **v0.3**（2026-04-22 autonomous session Round 3 FIX，此 commit）：响应 Round 2 双 Codex REJECTED verdict：
  - **CRITICAL 数学修复**：W2.5 从 "quantum state Pauli correction" 改为 "**classical raw-key bit XOR**"；数值 verify both $\Psi^\pm$ outcome 经 Table I flip 后 QBER = $2(1-F')/3$ 一致
  - A6 精细化：Lo-Curty-Qi Table I 只覆盖 $\Psi^\pm$ outcome；$\Phi^\pm$ outcome 被 linear-optic BSM 物理排除
  - Table I 修正：X-basis $\Psi^+$ outcome 是 kept + **no flip**（不是 "可能 discard"）
  - 标签规范：W1, W3 [THM]；W2, W2.5, W4 [CONJ]（删除 [VERIFIED]/[RECALLED] 非 R0.3 标签）
  - W4 explicit gap G1：SDP 结构等价性未证
  - §0.4 明示 repo BSM convention $\{\Phi^+, \Psi^-\}$ vs Lo-Curty-Qi $\{\Psi^\pm\}$ 差异（不 in scope）
  - 去除 v0.2 的 "用户签字" 已替 "user review decision 1b"，v0.3 重申
- **v0.2**（2026-04-22 Round 2 FIX，commit fb483b4）：响应 Round 1 — 但 W2.5 仍错误（quantum Pauli 而非 classical flip）。REJECTED
- **v0.1**（2026-04-22 Round 1 draft，commit 20d99d4）：缺 outcome-dependent。REJECTED

---

## 14. 下一步

1. T1.4 Round 3 dev-reviewer 双 Codex 评审 v0.3（C3 闸门）
2. 若 PASS：保留 [CONJ]，等用户归来做 C1 + C2
3. 若连续 3 轮 FAIL 同一 issue（R1 CRITICAL, R2 CRITICAL, R3 pending）：按 dev-reviewer 规则停手 + 写 deadlock report 交用户
4. 无论结果如何：不升级任何分级；不改 FINDINGS / Log 07

---

*END of v0.3 — [CONJ]*
