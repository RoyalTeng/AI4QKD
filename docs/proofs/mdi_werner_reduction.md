# MDI-QKD Werner reduction — ideal symmetric entanglement-swap 下 post-BSM state 的 Bell-diagonal form 推导

**版本**：v0.2 **[CONJ]**（autonomous session 2026-04-22，Round 2 FIX 响应 dev-reviewer Round 1 双 Codex verdict）
**对应 RESEARCH_PLAN 动作**：§2.2 R2.1 Level 3 → Level 4 升级
**对应实现**：[qkdx/numerics/kamin_sdp_mdi.py](../../qkdx/numerics/kamin_sdp_mdi.py) line 23-28 docstring 所述 reduction
**预备知识**：[docs/literature/MDI-QKD.md](../literature/MDI-QKD.md) §3.1-§3.4

**严谨性分级**：**[CONJ]**。本文档为本项目独立推导；**并非** Lo-Curty-Qi 2012 原文明写内容。所有子引理均 [CONJ] 或 [RECALLED]，**不含** [THM] 级自评。

**触发本修订的 review verdict**：
- [Agent 1 diff review (xhigh)](../workflow/werner-reduction/review-diff-1.json)：REJECTED (1 CRITICAL + 4 MAJOR)
- [Agent 2 holistic review (high)](../workflow/werner-reduction/review-holistic-1.md)：FAIL (overlapping issues + 2 minor)

**CRITICAL 修复** (Round 2)：v0.1 错误地声称 BSM 任何 outcome 都给 Φ⁺-centered Werner。**实际** BSM outcome 给对应 Bell-centered Werner（例如 Ψ⁻ outcome → Ψ⁻-centered）。MDI-QKD 通过 Table I 的**分类 bit-flip 规则**把各 outcome 映射到相同 key agreement frame（Φ⁺-frame for QBER readout）。v0.2 加入**新 Lemma W2.5** 显式这一 Pauli correction。

---

## 0. 目的与 scope

### 0.1 目的

验证 [qkdx/numerics/kamin_sdp_mdi.py:23-28](../../qkdx/numerics/kamin_sdp_mdi.py) 的 docstring 核心 reduction claim：

> "In the virtual-EB picture (Lo-Curty-Qi §II), after Charlie's successful Bell projection the conditional Alice-Bob state has the Werner form $\text{Tr}[|\Phi^+\rangle\langle\Phi^+| \cdot \rho_{AB}] = 1 - 3 \cdot \text{qber}/2$ (for the basis-matched-correct BSM). This is structurally identical to qubit BB84's Werner state at effective QBER, allowing DIRECT reuse of `kamin_choi_sdp_qubit_bb84`."

**注**：docstring 说 "Lo-Curty-Qi §II"，但 virtual-EB picture 在 Lo-Curty-Qi 2012 实际写在 **Appendix A**，不在 §II。本文件按 Appendix A 文本支持；docstring 措辞待未来 cleanup commit 修正。

### 0.2 用户 review decision 来源

用户 2026-04-21 session 审阅项 1，决定选项 **(b)**：要求 Werner form 形式化证明（见 [AUTONOMOUS_SESSION_2026-04-21_CONCLUSIONS.md §4](../AUTONOMOUS_SESSION_2026-04-21_CONCLUSIONS.md)）。**此决定为 scope 性指示**，**不**构成 R0.2 C2 的 upgrade sign-off。C2 sign-off 需用户归来后逐项确认本文件的具体 rigor grade。

### 0.3 Scope 严格限定

本推导**仅覆盖以下严格假设下的 ideal symmetric MDI-QKD**：

| 假设 ID | 假设内容 | 违反后果 |
|---|---|---|
| A1 | $\eta_A = \eta_B = \eta_\text{arm}$（两臂透过率对称） | 两 Werner 参数不同 → 输出非 Werner |
| A2 | Alice / Bob 使用理想 single-photon EB 源（virtual-qubit picture） | 诱骗态 + WCP 情形需更广义推导 |
| A3 | 两臂 depolarizing 噪声参数相同 $\lambda_A = \lambda_B = \lambda$ | 两 Werner 参数不同 → 输出非 Werner |
| A4a | Charlie 用理想 50:50 BS + 理想 PBS + 完美 HOM 干涉 | 非理想 linear-optic BSM → 需修正 |
| A4b | Charlie 探测器理想（单位量子效率，零 dark count，零 after-pulsing） | 真实探测器需扩展 POVM |
| A4c | 两臂光子完美 indistinguishable（spectral / temporal / polarization） | 非完美 HOM → 修正 interference visibility |
| A5 | 无 basis misalignment（Alice-Bob-Charlie 的 Z/X 基完美对齐） | 非对称 QBER $q_Z \neq q_X$ → 不可简化为单参数 Werner |
| A6 | Alice-Bob **post-select 所有成功 BSM outcome**（Table I 全接受）+ **按 Table I 的 bit-flip 规则** 做 key agreement correction | 若只接受部分 outcome 或不做 flip correction → 不同的条件态 / 不同 p_sift |

**非覆盖情形**（需独立工作，不在本文件 scope 内）：
- 非对称 MDI（A1 / A3 violation）
- WCP + 诱骗态 extension（Ma-Razavi 2012 Fig.3）
- Misalignment > 0
- Dark count + after-pulsing
- Finite-key / entropy accumulation（Kamin 2025 framework 单独处理）

---

## 1. 符号约定

- $|\Phi^\pm\rangle = \frac{1}{\sqrt{2}}(|00\rangle \pm |11\rangle)$，$|\Psi^\pm\rangle = \frac{1}{\sqrt{2}}(|01\rangle \pm |10\rangle)$：标准 Bell 基
- Alice：qubit A（virtual key register） + A'（发送 Charlie 的光子 mode）
- Bob：qubit B + B'
- Charlie 对 (A', B') 做 BSM
- $\mathcal{E}_\lambda$：qubit depolarizing channel，$\mathcal{E}_\lambda(\rho) = (1-\lambda)\rho + \lambda I/2$，$\lambda \in [0, 1]$
- **$B$-centered Werner state**：$W_F^B = F|B\rangle\langle B| + \frac{1-F}{3}\sum_{B' \neq B}|B'\rangle\langle B'|$，$B \in \{\Phi^+, \Phi^-, \Psi^+, \Psi^-\}$
- 默认 $W_F := W_F^{\Phi^+}$（$\Phi^+$-centered）
- $q$：effective MDI QBER

---

## 2. Concept map

```
               Lo-Curty-Qi 2012 Appendix A
               virtual-EB picture (Alice / Bob 持 EB Bell pair)
                          │
                          ▼
       [Ideal symmetric depolarizing channel on A', B']
                          │
                          ▼
                  Lemma W1 (each arm)
         (depolarizing → $\Phi^+$-centered Werner $W_{F_1}$)
                          │
                          ▼
                 Charlie BSM on (A', B')
              outcome-dependent projection
                          │
                          ▼
                   Lemma W2 (new v0.2)
          Bell-outcome-dependent Werner output
     $W_{F'}^{B_k}$ centered on $k$-th Bell outcome
                          │
                          ▼
                  Lemma W2.5 (new v0.2)
            MDI Table I bit-flip 规则 (Pauli correction)
     把 $W_{F'}^{B_k}$ 映射到 $\Phi^+$-frame for key agreement
                          │
                          ▼
                   Lemma W3 (Werner QBER)
          $q_Z = q_X = 2(1-F')/3$
                          │
                          ▼
                   Lemma W4 [CONJ]
      qubit BB84 Kamin Choi SDP 的 delegation validity
               (条件 + scope 列出)
```

---

## 3. Key results

| 标签 | 陈述 | 严谨性 |
|---|---|---|
| W1 | depolarizing on Bell pair → $\Phi^+$-centered Werner $W_{F_1}$ where $F_1 = 1 - 3\lambda/4$ | **[VERIFIED against Nielsen-Chuang 2010 §8.3.4 + §2.4]** |
| W2 | entanglement swap of two $W_{F_1}$ inputs with BSM outcome $B_k$ → $B_k$-centered Werner $W_{F'}^{B_k}$ with $F' = F_1^2 + (1-F_1)^2/3$ | **[RECALLED]** + **本项目数值验证**（§7 numerical check 显示四个 Bell outcome 各给对应 Bell-centered Werner） |
| W2.5 | Table I bit-flip 规则把 $W_{F'}^{B_k}$ 映射到 $\Phi^+$-frame for QBER readout（key agreement 角度） | **[CONJ]** — Table I flip 规则解读独立推导；需 PDF precise verification |
| W3 | $\Phi^+$-centered Werner $W_F$ 满足 $q_Z = q_X = 2(1-F)/3$ | **[VERIFIED, elementary]**（纯 Bell 基测量概率代数） |
| W4 | ideal symmetric MDI post-Table-I-correction conditional Alice-Bob state 与 qubit BB84 Werner post-channel state 有相同 $F'$ 参数化，therefore `kamin_choi_sdp_qubit_bb84(qber=q)` delegation **可能**给出正确 h_per_sift | **[CONJ conditional on A1-A6 + W2.5 PDF 校验 + Kamin SDP 结构等价性]** |

---

## 4. Virtual-EB 归约（Lo-Curty-Qi 2012 Appendix A）

**陈述**（源自 Lo-Curty-Qi 2012 Appendix A，PDF 第 4 页右栏第 2-3 段，已 PDF 核对）：

MDI-QKD 的 prepare-and-measure 形式与以下 virtual-EB 形式**安全等价**：

1. Alice 准备 $|\Phi^+\rangle_{AA'}$，A 存量子存储，A' 送 Charlie
2. Bob 准备 $|\Phi^+\rangle_{BB'}$，B 存量子存储，B' 送 Charlie
3. Charlie 公告 BSM 结果 $r \in \{\Phi^+, \Phi^-, \Psi^+, \Psi^-, \bot\}$
4. Alice-Bob post-select 成功 $r \neq \bot$ 且同基
5. **延迟测量**：Alice-Bob 在 Charlie 公告后才对各自 virtual qubit A / B 做 Z 或 X 基测量

**依据原文逐字引用**（Lo-Curty-Qi 2012 Appendix A，page 4）：
- "In such virtual qubits setting, the protocol is directly equivalent to an entanglement based protocol [refs 2, 3, 33]. Alice and Bob share a pair of qubits in their quantum memories and they simply compute the QBER on their virtual qubits in the XX and ZZ bases."

**Bearing**：本文件后续 §5-§7 在 virtual-EB picture 中推导 conditional 态。

---

## 5. Lemma W1：depolarizing channel on one half of Bell pair → $\Phi^+$-centered Werner

**引理**：设 $|\Phi^+\rangle_{AA'}$，对 A' 施加 depolarizing channel $\mathcal{E}_\lambda$，则 (A, A') 的输出态为 **$\Phi^+$-centered Werner state**：

$$\rho_{AA'} = W_{F_1}^{\Phi^+}, \quad F_1 = 1 - \frac{3\lambda}{4}.$$

**证明**：

$$(\mathcal{I}_A \otimes \mathcal{E}_\lambda)(|\Phi^+\rangle\langle\Phi^+|) = (1-\lambda)|\Phi^+\rangle\langle\Phi^+| + \lambda (I_A/2 \otimes I_{A'}/2)$$

利用 $I/2 \otimes I/2 = \frac{1}{4}(|\Phi^+\rangle\langle\Phi^+| + |\Phi^-\rangle\langle\Phi^-| + |\Psi^+\rangle\langle\Psi^+| + |\Psi^-\rangle\langle\Psi^-|)$（Bell basis 完备性 + 2-qubit maximally mixed state 展开）：

$$\rho_{AA'} = \left(1 - \frac{3\lambda}{4}\right)|\Phi^+\rangle\langle\Phi^+| + \frac{\lambda}{4}\sum_{B \neq \Phi^+}|B\rangle\langle B| = W_{F_1}^{\Phi^+}.$$ □

**严谨性**：**[VERIFIED against Nielsen-Chuang 2010 §8.3.4 (depolarizing channel) + §2.4 (Bell basis)]**（教科书级别标准结果；本项目独立复现但非 [THM] 原创性）

---

## 6. Lemma W2：outcome-dependent Werner after entanglement swap

**引理**（**本引理替代 v0.1 的错误版本**）：设 $\rho_{AA'} = W_{F_1}^{\Phi^+}$ 与 $\rho_{BB'} = W_{F_1}^{\Phi^+}$（两 $\Phi^+$-centered Werner 同参数）。Charlie 在 (A', B') 做 BSM。

**对每个** Bell 投影 outcome $B_k \in \{\Phi^+, \Phi^-, \Psi^+, \Psi^-\}$，

1. outcome 概率 $p_k^\text{BSM} = 1/4$（与 outcome label 无关，由对称性）
2. 条件态 on (A, B)：**$B_k$-centered Werner**：

$$\rho_{AB}^{(k)} = W_{F'}^{B_k}, \quad F' = F_1^2 + \frac{(1-F_1)^2}{3}.$$

**证据**：

**(a) 本项目数值验证**（2026-04-22 autonomous session，独立 Python script）：

对 $\lambda = 0.1$（$F_1 = 0.925$，$F'$ 理论预测 $= 0.8575$），四个 Bell outcome 的 conditional state fidelity 分别为：

| BSM outcome | $F(\Phi^+)$ | $F(\Phi^-)$ | $F(\Psi^+)$ | $F(\Psi^-)$ |
|---|---|---|---|---|
| $\Phi^+$ | **0.8575** | 0.0475 | 0.0475 | 0.0475 |
| $\Phi^-$ | 0.0475 | **0.8575** | 0.0475 | 0.0475 |
| $\Psi^+$ | 0.0475 | 0.0475 | **0.8575** | 0.0475 |
| $\Psi^-$ | 0.0475 | 0.0475 | 0.0475 | **0.8575** |

（dominant Bell-component fidelity 恰为预测 $F'$，其他 Bell 权重为 $(1-F')/3 \approx 0.0475$ — 每 outcome 都给 $B_k$-centered Werner）

**(b) 文献引用**：entanglement-swap 下 Werner → Werner 是 quantum repeater 文献标准结果。**具体引用未 PDF 级核对**，仅作方向性指认：
- Briegel-Dür-Cirac-Zoller 1998, *"Quantum Repeaters: The Role of Imperfect Local Operations"*, Phys. Rev. Lett. 81:5932, arXiv:quant-ph/9803056 — 含 swap 下 depolarization 参数更新公式（**具体 Eq. 编号待 PDF 核对**）
- Dür-Briegel-Cirac-Zoller 1999, *"Quantum repeaters based on entanglement purification"*, Phys. Rev. A 59:169, arXiv:quant-ph/9808065 — 含 Werner-under-swap 的进一步讨论（**具体 Eq. 编号待 PDF 核对**）

**严谨性**：**[RECALLED]** for 代数 + **[VERIFIED numerically for single probe λ=0.1]**。公式 $F' = F_1^2 + (1-F_1)^2/3$ 的代数独立复现**未**在本 memo 内完成（这是 Level 4 升级所需）。

**Round 1 Agent 2 的指认**：Briegel 1998 Eq.(5) specialized to perfect ops + L=2 才是相关表达；v0.1 引用 "Eq.(8)" 和 Dür 1999 "Eq.(12)" 均错误。v0.2 去除错误 Eq. 号，仅保留文献方向性引用。

---

## 7. Lemma W2.5（新增 v0.2）：MDI Table I bit-flip correction → $\Phi^+$-frame

**引理**：Lo-Curty-Qi 2012 Table I 给出的 MDI bit-flip 规则将 $B_k$-centered Werner 条件态**等效映射**到 $\Phi^+$-centered frame for key agreement 目的。

**背景**：[docs/literature/MDI-QKD.md](../literature/MDI-QKD.md) §3.2 - §3.3 已明确 Table I 的规则：

| Alice-Bob 基 | Charlie outcome $|\Psi^-\rangle$ | Charlie outcome $|\Psi^+\rangle$ |
|---|---|---|
| 直线基 (Z / rectilinear) | bit flip | bit flip |
| 对角基 (X / diagonal) | bit flip | - (不 flip / 也可能 discard depending on paper text) |

（A6 重新修正：按 Table I，**同基 + 成功 Bell outcome** 都 kept；flip rule 依 outcome 分类）

**推导**：

$|\Psi^-\rangle_{AB}$ 和 $|\Psi^+\rangle_{AB}$ 在 Z 基（computational basis）下都是**反关联态**（Alice-Bob outcomes are anti-correlated）。Alice-Bob 若都直接读出 Z 基：他们的 raw key 会**反相关**。

Bit-flip correction（在 Alice 或 Bob 一边 XOR 1）把 raw anti-correlation 变成 correlation。对 Werner state $W_{F'}^{\Psi^-}$ 做 bit-flip on Bob side $\Leftrightarrow$ 作用 local Pauli $X_B$ $\Leftrightarrow$ 变换 Bell-outcome label：

$$X_B |\Psi^-\rangle_{AB} = -|\Phi^-\rangle_{AB} \quad \text{(up to global phase)}$$

一般性地，$(I \otimes X)$ 映射 Bell basis 如下（global phase 忽略）：
- $|\Phi^+\rangle \to |\Psi^+\rangle$
- $|\Phi^-\rangle \to |\Psi^-\rangle$
- $|\Psi^+\rangle \to |\Phi^+\rangle$
- $|\Psi^-\rangle \to |\Phi^-\rangle$

**对 $\Phi^-$ / $\Psi^\pm$ outcome**：加适当的 Pauli correction（ $X$, $Z$, 或 $XZ$）将 $B_k$-centered Werner 映射到 $\Phi^+$-centered frame。具体对 MDI Table I：

- $|\Psi^-\rangle$ outcome：$X_B$ flip → **但** 也可能需要 phase 修正；具体 flip rule 看 Alice-Bob convention
- $|\Psi^+\rangle$ outcome：$X_B$ flip（因为同样 anti-correlated in Z basis）
- $|\Phi^\pm\rangle$ outcome：Lo-Curty-Qi 2012 Table I 未含（HOM 干涉抑制 linear-optic BSM of $\Phi^\pm$）

**严谨性**：**[CONJ]**. 本引理**未经 PDF 级 Table I 精确核对** — 只依赖 [docs/literature/MDI-QKD.md](../literature/MDI-QKD.md) §3.2 转述 + 一般性 Pauli correction 逻辑。Level 4 升级需：
- PDF 级 Table I 逐行 verification
- bit-flip rule 的 outcome-by-outcome 明写（含 Ψ⁻ vs Ψ⁺ 的具体差异）
- phase rotation 补充（如 $Z$ correction 在何时需要）

**关键 bearing**：post-correction conditional state（对每个接受的 outcome）**都是** $\Phi^+$-centered Werner $W_{F'}^{\Phi^+}$（假设 W2.5 的 correction 逻辑正确）。此 $\Phi^+$-frame state 为 §8 后续 QBER readout 的起点。

---

## 8. Lemma W3：Werner state 的 QBER 参数化

**引理**：$\Phi^+$-centered Werner state $W_F^{\Phi^+}$ 在 Z 基 / X 基下均有相同 QBER：

$$q_Z = q_X = \frac{2(1-F)}{3}.$$

**证明**（与 v0.1 相同）：

Z 基测量概率：
- $|\Phi^\pm\rangle$：$P(00) = P(11) = 1/2$（Alice Bob **同结果**）
- $|\Psi^\pm\rangle$：$P(01) = P(10) = 1/2$（**反结果**）

对 $W_F^{\Phi^+}$：$P(\text{different}|Z) = \frac{1-F}{3} + \frac{1-F}{3} = \frac{2(1-F)}{3}$（来自两个 $\Psi$ 权重）。

X 基（$|\pm\rangle = (|0\rangle \pm |1\rangle)/\sqrt{2}$）展开：
- $|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|++\rangle + |--\rangle)$（X 基 same）
- $|\Phi^-\rangle = \frac{1}{\sqrt{2}}(|+-\rangle + |-+\rangle)$（X 基 different）
- $|\Psi^+\rangle = \frac{1}{\sqrt{2}}(|++\rangle - |--\rangle)$（X 基 same）
- $|\Psi^-\rangle = -\frac{1}{\sqrt{2}}(|+-\rangle - |-+\rangle)$（X 基 different）

对 $W_F^{\Phi^+}$：$P(\text{different}|X) = \frac{1-F}{3} + \frac{1-F}{3} = \frac{2(1-F)}{3}$（来自 $\Phi^-$ 和 $\Psi^-$）。

$\therefore q_Z = q_X = \frac{2(1-F)}{3}$. □

**逆映射**：$F = 1 - \frac{3q}{2}$。此数值**与** `kamin_sdp_mdi.py:26` docstring `Tr[|Φ⁺⟩⟨Φ⁺|·ρ_AB] = 1 - 3q/2` **一致**（前提是 W2.5 post-correction 给出 $\Phi^+$-centered Werner）。

**严谨性**：**[VERIFIED, elementary algebra]**（纯 Bell 基测量概率展开；本项目独立复现但非 [THM] 原创性）

---

## 9. Lemma W4：qubit BB84 Kamin SDP delegation — [CONJ]

**引理**（**关键的 reduction claim，停在 [CONJ]**）：在 §0.3 假设 A1-A6 下，ideal symmetric MDI-QKD 经 virtual-EB + BSM + Table I bit-flip correction 后的 conditional Alice-Bob state 为 $\Phi^+$-centered Werner $W_{F'}^{\Phi^+}$，$F' = 1 - 3q/2$。

**声称**：`kamin_choi_sdp_qubit_bb84(qber=q)` 的 `h_per_sift` 给出 MDI 对应 asymptotic conditional entropy。

**推导 chain**：

1. W1：depolarizing 给 $\Phi^+$-centered Werner $W_{F_1}^{\Phi^+}$
2. W2：entanglement swap 给 $B_k$-centered Werner（outcome $k$）
3. W2.5：Table I bit-flip correction 映射到 $\Phi^+$-frame
4. W3：Werner QBER 参数化 $q = 2(1-F)/3$
5. W4 claim：Kamin BB84 SDP 于 Werner 参数化下 output 同 `h_per_sift`

**关键 gap**（Agent 1 MAJOR-3 原意）：W4 需要证明 Kamin BB84 SDP 的 G-map / Z-map / Choi-state 结构（见 [qkdx/numerics/kamin_sdp.py](../../qkdx/numerics/kamin_sdp.py) 第 297-335, 359-380 行）在以下两情景**数值产物相同**：

- **情景 A**：输入是 BB84 protocol 的 Z-basis key-generation round conditional state（由 BB84 source-replacement 给出）
- **情景 B**：输入是 MDI protocol 经 Table I correction 的 Z-basis post-BSM conditional state

本 memo **未**证明情景 A ↔ B 的结构等价。仅**断言** —— 在 Werner 参数化 + QBER 匹配的前提下 —— 数值结果相同。此断言的**严格证明**需要 match BB84 Kamin SDP 的具体 POVM / G-map / Z-map 到 MDI post-correction conditional measurement 的等价。

**严谨性**：**[CONJ conditional on]**：
- A1-A6 假设
- W2.5 Table I 修正逻辑正确（未经 PDF 精确核对）
- Kamin SDP 结构等价性（BB84 ↔ post-corrected MDI，未证）

**Round 1 Agent 1 的合理批评**（MAJOR-3）：本 memo 的 "Kamin SDP 只操作于 conditional state 本身" 过于松散；完整 delegation 需要 G/Z-map 结构等价推导。v0.2 显式列 W4 为 **[CONJ]** 并明示 gap，不声称已 close。

---

## 10. 数值 sanity check

### 10.1 极限 1：无噪声（$\lambda = 0$）

$F_1 = 1$，$F' = 1$，$q = 0$，$h_\text{per_sift} = 1$. ✓

### 10.2 极限 2：完全去极化（$\lambda = 1$）

$F_1 = 1/4$，$F' = 1/4$，$q = 1/2$，$h_\text{per_sift} = 0$. ✓

### 10.3 数值 probe：$\lambda = 0.1$

$F_1 = 0.925$，$F' = 0.8575$，$q = 0.095$.

**Python 独立脚本复现**（非 LLM 代码，纯 NumPy 线性代数）：本项目在 2026-04-22 session 内跑了独立 4-qubit 纠缠态构建 + depolarization + BSM projection + 部分trace 计算，for $\lambda = 0.1$ 四个 outcome 都给 F(dominant) = 0.8575 ± 数值误差。**这是同代码库的数值一致性检查**，**不构成** R0.2 C1 独立验证（参见 §11.2）。

### 10.4 与 `kamin_sdp_mdi.py` 测试对照

[tests/test_numerics/test_kamin_sdp_mdi.py](../../tests/test_numerics/test_kamin_sdp_mdi.py)（修正自 v0.1 的 typo `test_kamin_mdi.py`）的 5/5 测试已验证：
- `h_per_sift` 在同 QBER 下 MDI 数值 = BB84 数值（`abs < 1e-6`）
- $n=10^{12}, 0$ dB, $q=0.01$: rate $\approx 0.22 \approx$ qubit BB84 $\times 1/4$ p_sift

**这些测试** 使用同一 Kamin SDP codebase 的同一 `kamin_choi_sdp_qubit_bb84` 函数 + `kamin_mdi_h_per_sift` 函数（后者 delegate 前者）。**本质是 codebase 自洽性测试**，**不**构成独立验证。

---

## 11. Scope limits 与 upgrade path

### 11.1 本文件 **不** 证明的东西

1. 非对称 MDI（A1 / A3 violation） — Werner form 破坏
2. Misalignment > 0 (A5 violation) — 非对称 QBER
3. WCP + 诱骗态 extension — 需 $Y_{1,1}^L, e_{1,1}^U$ 估计
4. Finite-size / GEAT — Kamin 2025 finite-key formula 单独处理
5. W2 公式的代数独立复现（本 memo 只 numerical verify 一个 λ probe）
6. W2.5 Table I bit-flip correction 的 outcome-by-outcome PDF 核对
7. W4 Kamin SDP 结构等价性的 G-map / Z-map 层 derivation

### 11.2 Upgrade to [COROLLARY] — R0.2 C1 ∧ C2 ∧ C3

**C1 independent validation**（**目前未满足**）：
- (a) 另一家族 AI（如 GPT / Gemini）读以下 PDF 独立复核：
  - Lo-Curty-Qi 2012 Appendix A + Table I（virtual-EB + bit-flip rule）
  - Briegel-Dür-Cirac-Zoller 1998（Werner-under-swap 公式的确切 Eq.编号）
  - Nielsen-Chuang 2010 §8.3.4 + §2.4（depolarizing + Bell basis — 仅 W1 用）
- (b) 人类研究者纸笔复核 W2 代数展开（16-dim 张量 → 4-dim partial trace）
- (c) 非 AI 工具（Mathematica / SymPy symbolic）独立验证 $F' = F_1^2 + (1-F_1)^2/3$ 公式

**目前项目内的数值 Python probe**（§10.3）**不计入** C1(c)，因为：
- 代码本身为 autonomous session 起草，属"同家族 AI 输出"
- numpy 库只作为线性代数工具，**非**"独立符号验证"

**C2 用户签字**：用户 2026-04-21 的 review decision 1b 是 **scope 指示**，**不** 是 C2 upgrade sign-off。用户归来后需逐项确认本文件分级。

**C3 dev-reviewer PASS**：本 session 已发起（v0.1 被 REJECTED，v0.2 Round 2 待评）。

### 11.3 本文件 **不** 做的动作

- 不升级 `kamin_sdp_mdi.py:23-28` docstring 的声称（保留原声称作为 [CONJ]，本文件仅**提供 conditional 分析**，不执行 upgrade）
- 不改 FINDINGS v2 分级
- 不改 Log 07 umr 上界 [CONJ] 状态

---

## 12. 与本项目的 Bearing

### 12.1 对 Sub-Q2 Phase 1 S2.5 的直接用途

- 现 `kamin_sdp_mdi.py` 的 docstring "Werner form" 声称**在 [CONJ] + A1-A6 scope 下有 conditional 分析支持**
- 测试 5/5 pass 为 codebase 自洽性证据（非独立验证）
- 本文件**不升级** S2.5 硬验收状态

### 12.2 对 Sub-Q3 path α / β / γ 的间接 bearing

- Lemma W1 + W2 是 MDI 纯态操作级 analysis
- 与 Pirandola 2019 / Log 07 network capacity 级 analysis 不同层级
- 本文件**不影响** umr 上界 [CONJ] 状态

### 12.3 对 PROSPECTUS 主问题的 bearing

无直接 bearing。Sub-Q1 / Sub-Q2 基础设施级论证，不改变主问题答案。

---

## 13. Changelog

- **v0.2**（2026-04-22 autonomous session Round 2 FIX）：响应 dev-reviewer Round 1 双 Codex verdict（REJECTED + FAIL）：
  - 数学 CRITICAL 修复：加入 W2 outcome-dependent Bell-centered Werner + W2.5 Table I bit-flip correction
  - A6 修正按 Lo-Curty-Qi Table I：同基 + 成功 Bell outcome 全接受，flip rule 依 outcome 分类
  - 去除 W1 / W3 的 [THM] 自评，改为 **[VERIFIED against textbook]** 以及 **[VERIFIED, elementary algebra]**
  - 去除 Briegel-Dür-Cirac-Zoller 1998 Eq.(5/8) 具体 Eq. 号（Agent 2 指出 PDF 级实际为 Eq.(5) + L=2，不是 Eq.(8)）；去除 Dür 1999 Eq.(12) 错误引用
  - 去除 v0.1 "[CONJ] 但 tests 已提供 C1(c)" 的 C1(c) overclaim；明确标注"同代码库自洽性检查，**非** C1(c)"
  - 去除"用户 2026-04-21 session 签字" 歧义措辞（CLAUDE.md R0.2 下 "签字" 是 loaded C2 term）改为 "user review decision 1b"
  - 修 test 文件路径：`test_kamin_mdi.py` → `test_kamin_sdp_mdi.py`
  - 添加 §2 Concept map + §3 Key results（RESEARCH_PLAN §7.1 模板要求）
  - 本 memo 内的 kamin_sdp_mdi.py "Lo-Curty-Qi §II" 措辞 vs 实际 Appendix A 注记（待未来 docstring cleanup）
- **v0.1**（2026-04-22 autonomous session，draft commit 20d99d4）：**已撤回**。v0.1 错误：
  - W2 缺 outcome-dependent correction → 数学不对
  - A6 misread Table I
  - W1/W3 [THM] labels 违反 R0.3
  - BDCZ equation citations 未 PDF 验证
  - C1(c) overclaim via same-codebase tests
  - "用户签字" 误用 C2 措辞

---

## 14. 下一步

1. **T1.4 Round 2** dev-reviewer 双 Codex 再评审 v0.2（C3 闸门）
2. 若 PASS：保留 [CONJ]，等用户归来做 C1 + C2（不自主升级）
3. 若 FAIL：按 verdict 修订 Round 3（dev-reviewer 最多 5 轮）
4. 无论结果如何：**不** 升级 `kamin_sdp_mdi.py` docstring；**不** 改 FINDINGS 任何分级

---

*END of v0.2 — [CONJ]*
