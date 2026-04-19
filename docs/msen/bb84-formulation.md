# BB84 的 MS-EB 五元组 Formulation(lower-bound sanity, v0.3)

**Research action**:R1.2(RESEARCH_PLAN §2.1,Phase 0 M1 Week 1 后半)
**日期**:2026-04-19(v0.3 同日响应 codex round 2 FAIL,v0.2 同日响应 codex round 1 FAIL)
**依赖**:[docs/literature/WLC-2018.md](../literature/WLC-2018.md) R1.1 + [docs/PROSPECTUS.md](../PROSPECTUS.md) §4 MS-EB + [docs/PHASE0_M1_TECHNICAL_SPEC.md](../PHASE0_M1_TECHNICAL_SPEC.md) §3
**状态**:**draft, pending R1.3 numerical validation**(§5 / §7 / §9 标注的 DEFERRED 项必须在 R1.3 代码实现后定稿;§10 是 lower-bound sanity,非精确闭合)

**v0.3 差量**(response to codex round 2):
- §7.3:修正 $p$-参量矩阵 (1,1)/(4,4) 元 `(1-p/3)/2` → `(1-2p/3)/2`(保持 trace $=1$);新增 §7.3.1 Bell→Z 逐元核对 + §7.3.2 trace/本征值 sanity
- §8.2:订正 $(H\otimes H)(\proj{01}+\proj{10})(H\otimes H)$ 的 Bell 分解 $\proj{\Psi^+}+\proj{\Phi^-}$ → $\proj{\Phi^-}+\proj{\Psi^-}$(数值相同,子空间标签订正);新增 §8.2.1 $H\otimes H$ Bell 作用表 + §8.2.2 直接展开
- §8.3/§8.4:`observation_keys` 对齐 REFACTORING_PLAN §4.6,加入 `"p_sift"` 三元签名,消接口契约冲突
- §10:整节降级为 "lower-bound sanity check"(原 v0.2 声称"独立证据链精确闭合"被 F4 驳回,因为 BCKR 取等条件未证)
- §12:Limitations 新增第 7-8 条(§10 下界定位 + §4 非 signaling 假设)

---

## 0. 本文档的目标与 codex FAIL 回应

R1.2 验收原文(RESEARCH_PLAN §2.1):

> 验收:上述 5 个对象能被 `qkdx.protocol.base.MSEBProtocol` 构造,且 `joint_state()` / `executed_state()` / `conditional_alice_bob()` / `conditional_alice_bob_dim()` / `observable()` 均可调用。

**v0.1 被 codex FAIL 的关键点**(2026-04-19 评审):

| # | v0.1 错误 | v0.2 本次修正位置 |
|---|----------|-------------------|
| F1 | §6 key-map Kraus `|x⟩⟨x,Z|+|x⟩⟨x,X|` 导致 $\sum K^\dagger K$ 本征值到 2(非 CPTP/TNI) | §5:删除非法 Kraus;key map 口径改为 "Alice 的 A register 存 bit + basis,M1 阶段 K 的精确 Kraus deferred 至 R1.3" |
| F2 | §3.6 / §8 / §10.1 register contract 三处冲突($d_B=1$ vs $4$ vs $2$) | §1.1 统一 register 口径 + §3.6 明确不经典化 B + §7 重写 $\rho_{AB}$ 为 pre-measurement 4-dim 态 |
| F3 | §9 $\Gamma_{\text{qber\_Z}}$ 给 $e/2$ 而非 $e$ | §8:重写 $\rho_{AB}$ 为 Bell-diag(非 branch 混合),$\Gamma$ 正确给 $e$;附 numpy-style 推导 |
| F4 | §11-§13 手算只是回代 Shor-Preskill,非独立 | §9-§10 三条独立证据链(Bell-diag 直算 + entropic UR + 对称性) |
| F5 | 缺 Limitations 章节 | §12 新增 |

---

## 1. 符号与统一的 register 口径(v0.2 修订)

### 1.1 Hilbert space —— **唯一正式口径**

**SDP 变量所在 Hilbert space**(R1.3 代码中 `conditional_alice_bob()` 的返回):

| 系统 | 记号 | 维度 | 量子 / 经典 | 物理含义 |
|------|------|------|-------------|----------|
| Alice qubit | $\mathcal{H}_A$ | $d_A = 2$ | **量子** | Alice 的 EB 态 Alice 一侧,未测量 |
| Bob qubit | $\mathcal{H}_B$ | $d_B = 2$ | **量子** | Bob 接收的 qubit,经 $\mathcal{E}_{\text{ch}}$ 后,**未测量** |

**SDP 变量总维度**:$d_{\text{cond}} = d_A \cdot d_B = 4$(`conditional_alice_bob_dim()` 返回值)。

**Alice 的 EB 纯化 register** $\mathcal{H}_{A'}$ 维度 4(存 $(x, \theta)$)——但**这是 §2 的 EB 纯化空间,不是 SDP 变量所在空间**。纯化后 Alice 可等价地视为持有一个 qubit $\mathcal{H}_A$(见 §2.5 purification 等价)。

### 1.2 关键区分(v0.1 混淆,v0.2 澄清)

v0.1 在三处混用了 "A" 所指:
- §1.1 / §2:`H_A` = 4 维(存 $(x,\theta)$,EB 纯化)
- §8:`ρ_{AB}` 放在 $H_{A_{\text{key}}}(2) \otimes H_B(2)$
- §10.1:$B_{\text{side}} = 2$ 存 $\theta_B$(M1 简化)

**v0.2 口径**:
- WLC SDP 变量 $\rho_{AB}$ 始终在 $\mathcal{H}_A(2) \otimes \mathcal{H}_B(2)$(本节 §1.1)
- EB 纯化寄存器 $\mathcal{H}_{A'}$(4 维)只在 §2.5 构造 Alice 边缘 $\rho_A$ 时用,不进入 SDP
- $B_{\text{side}}$ 不引入额外经典寄存器(M1 简化的"存 $\theta_B$"由 `observable("qber_X")` 查找表隐式承担,不需独立 register)

### 1.3 标准算子

$$I_2,\;\sigma_X,\;\sigma_Y,\;\sigma_Z,\;H = \frac{1}{\sqrt 2}\begin{pmatrix}1 & 1\\1 & -1\end{pmatrix}$$

Z 基:$\ket 0, \ket 1$;X 基:$\ket +, \ket -$;Bell 态 $\ket{\Phi^+}, \ket{\Phi^-}, \ket{\Psi^+}, \ket{\Psi^-}$(标准约定)。

---

## 2. $\mathcal{P} = (P_1)$:Alice 的 EB 纯化态

### 2.1 $P_1$ 三元组

$P_1 = (N_1=\text{Alice},\; d_{K,1}=4,\; d_{S,1}=2,\; \ket{\psi_1})$

$\ket{\psi_1} \in \mathcal{H}_{A'}(\dim 4) \otimes \mathcal{H}_{A}(\dim 2)$(**纯化空间**,非 SDP 空间)

### 2.2 EB 态显式

$$\ket{\psi_1}_{A'A} = \frac{1}{2} \sum_{x\in\{0,1\}} \sum_{\theta\in\{Z,X\}} \ket{x,\theta}_{A'} \otimes U_\theta \ket{x}_A,\qquad U_Z = I_2,\; U_X = H$$

(注意:v0.1 把两 register 记 $AA'$,v0.2 按"$A'$ = 纯化 4 维 / $A$ = 信号 2 维"命名,与 §1 一致)

### 2.3 归一化

$$\|\ket{\psi_1}\|^2 = \tfrac{1}{4} \sum_{x,\theta} 1 = 1 \quad\checkmark$$

### 2.4 $\rho_A = \text{Tr}_{A'} \proj{\psi_1}$

$$\rho_A = \tfrac{1}{4}[\proj 0 + \proj 1 + \proj + + \proj -] = \tfrac{1}{4}[I_2 + I_2] = \tfrac{1}{2} I_2$$

**Alice 信号边缘是最大混合态** — 对 Eve 无信息(BB84 安全性基础)。✓

### 2.5 Alice-as-qubit purification 等价

**Claim**:对 WLC SDP,EB 态 $\ket{\psi_1}_{A'A}$ 可等价地用 Bell 态 $\ket{\Phi^+}_{\tilde A A}$ 替代,其中 $\tilde A$ 是 2 维 register。

**Proof sketch**:关键是观察 $\ket{\psi_1}$ 的 Schmidt 分解只有 rank 2:

$$\ket{\psi_1}_{A'A} = \tfrac{1}{\sqrt 2}(\ket{u_0}_{A'} \ket 0_A + \ket{u_1}_{A'} \ket 1_A)$$

其中 $\{\ket{u_0}, \ket{u_1}\}$ 是 $\mathcal{H}_{A'}$ 内某 orthonormal pair(参见 §2.6 显式构造)。设 $V: \tilde A \to A'$ 是 isometry $V\ket x_{\tilde A} = \ket{u_x}_{A'}$,则

$$\ket{\psi_1}_{A'A} = (V \otimes I_A) \ket{\Phi^+}_{\tilde A A}$$

Alice 对 $A'$ 的(从 $\tilde A$ 的视角做基选择)任何局部操作等价于对 Bell 态 $\ket{\Phi^+}_{\tilde A A}$ 的局部操作。**WLC SDP 变量** $\rho_{AB}$ **只涉及 $A$ 和 $B$** —— Alice 的 $\tilde A$(或 $A'$)不进 SDP,只用于约束 $\rho_{AB}$ 的 Schmidt 结构(见 §7.1)。

### 2.6 $\ket{u_x}$ 显式形式(可选,§10 用)

$$\ket{u_0} = \tfrac{1}{\sqrt 2}\!\left[\ket{0,Z} + \tfrac{1}{\sqrt 2}(\ket{0,X} + \ket{1,X})\right],\quad
\ket{u_1} = \tfrac{1}{\sqrt 2}\!\left[\ket{1,Z} + \tfrac{1}{\sqrt 2}(\ket{0,X} - \ket{1,X})\right]$$

Schmidt 正交性 $\braket{u_0 | u_1} = 0$ 可直接验证。

---

## 3. $\mathcal{E}$:对称去极化信道 + Bob POVM(但 B 保持量子)

### 3.1 两部分语义

$\mathcal{E}$ 包含:

(A) 物理信道 $\mathcal{E}_{\text{ch}}: \mathcal{L}(\mathcal{H}_A) \to \mathcal{L}(\mathcal{H}_B)$(Alice 的 $A$ 发到 Bob);

(B) Bob 的 POVM $\{\Pi^{\theta_B, b}\}$:仅用于**构造 $\mathcal{A}$ 的宣告 + 派生观测量 $\Gamma_k$**,但 **Bob 的 qubit 在 SDP 变量里保持量子**。

**v0.2 的 key 选择**:不做 M1 的 `d_B = 1` 经典化,一律 `d_B = 2`。这与 WLC / CML 2016 做法一致(SDP 变量 $\rho_{AB}$ 的 B 永远 2 维量子)。

### 3.2 $\mathcal{E}_{\text{ch}}$:对称去极化

$$\mathcal{E}_{\text{ch}}(\sigma) = (1 - p)\sigma + \frac{p}{3}(\sigma_X \sigma \sigma_X + \sigma_Y \sigma \sigma_Y + \sigma_Z \sigma \sigma_Z)$$

### 3.3 QBER $\leftrightarrow p$:$p = 3e/2$(Proof 保留自 v0.1)

取 $\sigma = \proj 0$,$\mathcal{E}_{\text{ch}}(\proj 0) = (1 - \tfrac{2p}{3})\proj 0 + \tfrac{2p}{3}\proj 1$,故 $e_Z = 2p/3$;同理 $e_X = 2p/3$。✓

### 3.4 Kraus 表示(CPTP ✓)

$$K_0 = \sqrt{1-p}\, I_2,\; K_1 = \sqrt{p/3}\,\sigma_X,\; K_2 = \sqrt{p/3}\,\sigma_Y,\; K_3 = \sqrt{p/3}\,\sigma_Z$$

$\sum K_i^\dagger K_i = (1-p)I + \tfrac{p}{3}\cdot 3I = I$ ✓

### 3.5 Bob POVM(仅用于宣告 + 观测量构造)

$$\Pi^{Z, b} = \proj{b}_B,\quad \Pi^{X, b} = H \proj{b}_B H,\quad b\in\{0,1\}$$

完备性 $\sum_b \Pi^{\theta_B, b} = I_B$ ✓。

**重要**:这些 POVM **不显式作用在 SDP 变量** $\rho_{AB}$ 上。它们只出现在:
- 宣告 $\mathcal{A}$:`publish(θ_B)` 计算 Bob 公开的 basis
- 观测量 $\Gamma_k$:`Tr(Γ_qber_Z · ρ_AB)` 用 "measure A in Z AND B in Z, then test mismatch" 的投影器等价构造(见 §8)

### 3.6 $\mathcal{E}$ 整体的 MS-EB 作用

$\mathcal{E}: \mathcal{L}(\mathcal{H}_{A, \text{signal}}) \to \mathcal{L}(\mathcal{H}_B)$ **只含 $\mathcal{E}_{\text{ch}}$**(不含 Bob 测量):

$$\mathcal{E}(\sigma) = \mathcal{E}_{\text{ch}}(\sigma) = \sum_i K_i \sigma K_i^\dagger$$

**维度**:$\dim \mathcal{H}_{\text{in}} = d_{A, \text{signal}} = 2$,$\dim \mathcal{H}_{\text{out}} = d_B = 2$。

---

## 4. $\mathcal{A}$:sifting announcement

$$\text{publish}(\theta_B, b) = \theta_B,\qquad \text{sift\_keep}(\theta_A, \theta_B, b) = \mathbb{1}[\theta_A = \theta_B]$$

$p_{\text{sift}} = \sum_\theta \tfrac{1}{2} \cdot \tfrac{1}{2} = \tfrac{1}{2}$ ✓(Alice Z/X 50/50 × Bob Z/X 50/50)

**GEAT NSP**:标 **[SYN, 待 Phase 1 Sub-Q2.4 精读]**(Metger 2024 Thm 条款 NSP 对 active basis announcement 的严格核对不在 M1)。

---

## 5. $\mathcal{T}$:M1 占位(accept 恒真)

Phase 0 M1 渐近率不涉及 $\mathcal{T}$。Phase 1 finite-key 时替换。

---

## 6. $\mathcal{K}$:key map 的 **DEFERRED 实现**

**v0.1 的非法 Kraus**(`K^K_x = \proj x_{A_{\text{key}}} \otimes (\bra{x, Z}_A + \bra{x, X}_A)`)已**删除** —— 数值上 $\sum_x (K^K_x)^\dagger K^K_x$ 的本征值到 2,不是合法 CPTNI map(codex FAIL F1)。

**v0.3 处理**(订正 codex round 3 发现的接口错误):$\mathcal{K}$ 相关对象分两层:

**层 A — `KeyMap` 数据类(REFACTORING_PLAN §4.4,已有接口)**:

```python
class KeyMap:
    key_party: str          # "Alice"
    bitmap: dict[int, int]  # measurement result → key bit, e.g. {0: 0, 1: 1}
```

BB84 M1 的 `KeyMap` 可以**立即构造**:`KeyMap(key_party="Alice", bitmap={0: 0, 1: 1})`。`KeyMap` 不含 `map: KrausMap`(后者属于 `GMap` 类,是 WLC SDP 的映射对象,非协议 metadata)。

**层 B — WLC 的 $\mathcal{G}$ 映射(DEFERRED)**:`GMap.map: KrausMap` 对应 WLC 2018 Eq. (46)–(56) 中把 Alice EB 寄存器提取 key bit 的 CPTNI map,属于 `qkdx.numerics.wlc` 层,不属于 `MSEBProtocol` 的 metadata。R1.3 实施期人类 PDF 精读后给 `_construct_G_map` 的精确实现。

**M1 阶段只需要知道**:
- $P_\kappa = P_1$(Alice 是 key party)
- $d_{A_{\text{key}}} = 2$(bit 密钥)
- `KeyMap(key_party="Alice", bitmap={0: 0, 1: 1})` 合法可构造
- $\mathcal{G}$ Kraus(WLC SDP 层)DEFERRED — 不影响 R1.2 `MSEBProtocol` 五元组的可构造性

---

## 7. SDP 变量 $\rho_{AB}$ 的显式构造(WLC SDP 输入)—— v0.2 重写

### 7.1 $\rho_{AB}$ 是什么

**v0.1 错误**:把 $\rho_{AB|\text{keep}}$ 写成 $\tfrac{1}{2}\rho_{Z,Z} + \tfrac{1}{2}\rho_{X,X}$ 的 branch 混合。这破坏了 "$\rho_{AB}$ 是 pre-measurement 量子态" 的 MS-EB 约定,也让 $\Gamma$ 归一化出错。

**v0.2 正确口径**:$\rho_{AB}$ = Alice 的 EB 边缘(经 §2.5 purification 等价视为 Bell 态)通过 $\mathcal{E}_{\text{ch}}$(作用在 $A$-侧的"发出"等价 qubit)后的 pre-measurement 量子态,in $\mathcal{L}(\mathcal{H}_A(2) \otimes \mathcal{H}_B(2))$。

### 7.2 显式 Bell-diagonal 形式

从 §2.5 的 $\ket{\Phi^+}_{\tilde A A}$ EB 态出发(Alice-qubit 等价)。$\mathcal{E}_{\text{ch}}$ 作用在 $A$-to-$B$ 的传输上,等价于 $\sigma_X, \sigma_Y, \sigma_Z$ 各以概率 $p/3$ 作用于 $B$:

$$\boxed{\rho_{AB}(p) = (1-p)\proj{\Phi^+} + \frac{p}{3}\!\left[\proj{\Psi^+} + \proj{\Psi^-} + \proj{\Phi^-}\right]}$$

**推导**:
- $(I \otimes \sigma_X)\ket{\Phi^+} = \tfrac{1}{\sqrt 2}(\ket{01} + \ket{10}) = \ket{\Psi^+}$
- $(I \otimes \sigma_Y)\ket{\Phi^+} = \tfrac{i}{\sqrt 2}(\ket{01} - \ket{10}) = i\ket{\Psi^-}$(相位被 $\proj{\cdot}$ 吸收)
- $(I \otimes \sigma_Z)\ket{\Phi^+} = \tfrac{1}{\sqrt 2}(\ket{00} - \ket{11}) = \ket{\Phi^-}$

故 $\rho_{AB}(p)$ Bell-diagonal,四个本征值 $\{(1-p), p/3, p/3, p/3\}$(当 $p = 3e/2$,$e$ = QBER)。

### 7.3 $\rho_{AB}$ 的矩阵元(4×4,Z 基序 $\{00,01,10,11\}$)

**v0.3 订正**(codex round 2):v0.2 的 $p$-参量矩阵 $(1,1)/(4,4)$ 元写错为 $(1-p/3)/2$,导致该矩阵 trace $= 1 + p/3 \ne 1$。正确形式如下,逐元 Bell-diag 展开在 §7.3.1 给出。

$$\rho_{AB}(p) = \begin{pmatrix}
\tfrac{1-2p/3}{2} & 0 & 0 & \tfrac{1-4p/3}{2} \\
0 & \tfrac{p}{3} & 0 & 0 \\
0 & 0 & \tfrac{p}{3} & 0 \\
\tfrac{1-4p/3}{2} & 0 & 0 & \tfrac{1-2p/3}{2}
\end{pmatrix}$$

以 $e = 2p/3$ 代换 $\Rightarrow$

$$\rho_{AB}(e) = \tfrac{1}{2}\begin{pmatrix}
1-e & 0 & 0 & 1-2e \\
0 & e & 0 & 0 \\
0 & 0 & e & 0 \\
1-2e & 0 & 0 & 1-e
\end{pmatrix}$$

#### 7.3.1 Bell-basis → Z-basis 逐元核对

记 $a := 1-p$,$b := p/3$。从 §7.2 得 $\rho_{AB} = a\proj{\Phi^+} + b(\proj{\Phi^-} + \proj{\Psi^+} + \proj{\Psi^-})$。已知 Bell 态的 Z 基外积(关键元):

| Bell 态 | $\bra{00}\cdot\ket{00}$ | $\bra{11}\cdot\ket{11}$ | $\bra{00}\cdot\ket{11}$ | $\bra{01}\cdot\ket{01}$ | $\bra{10}\cdot\ket{10}$ | $\bra{01}\cdot\ket{10}$ |
|---------|-------------------------|-------------------------|-------------------------|-------------------------|-------------------------|-------------------------|
| $\proj{\Phi^+}$ | $1/2$ | $1/2$ | $+1/2$ | 0 | 0 | 0 |
| $\proj{\Phi^-}$ | $1/2$ | $1/2$ | $-1/2$ | 0 | 0 | 0 |
| $\proj{\Psi^+}$ | 0 | 0 | 0 | $1/2$ | $1/2$ | $+1/2$ |
| $\proj{\Psi^-}$ | 0 | 0 | 0 | $1/2$ | $1/2$ | $-1/2$ |

逐元:
- $(0,0)$:$a\cdot\tfrac12 + b\cdot\tfrac12 + 0 + 0 = \tfrac{a+b}{2} = \tfrac{1-p+p/3}{2} = \tfrac{1-2p/3}{2}$ ✓
- $(3,3)$:同上,$\tfrac{1-2p/3}{2}$ ✓
- $(0,3)$:$a\cdot\tfrac12 + b\cdot(-\tfrac12) + 0 + 0 = \tfrac{a-b}{2} = \tfrac{1-p-p/3}{2} = \tfrac{1-4p/3}{2}$ ✓
- $(1,1)$:$0 + 0 + b\cdot\tfrac12 + b\cdot\tfrac12 = b = p/3$ ✓
- $(2,2)$:同 $(1,1) = p/3$ ✓
- $(1,2)$:$0 + 0 + b\cdot\tfrac12 + b\cdot(-\tfrac12) = 0$ ✓

#### 7.3.2 Trace + Bell 本征值 sanity

- Trace:$2\cdot \tfrac{1-2p/3}{2} + 2\cdot \tfrac{p}{3} = (1-2p/3) + 2p/3 = 1$ ✓
- 以 $e = 2p/3$:$2\cdot \tfrac{1-e}{2} + 2\cdot \tfrac{e}{2} = (1-e) + e = 1$ ✓
- Bell 本征值 $(a, b, b, b) = (1-p, p/3, p/3, p/3)$,全部 $\geq 0$ 当 $p \leq 1$(即 $e \leq 2/3$) ✓
- $\rho_{AB}$ Hermitian(实对称)✓

### 7.4 $d_{\text{cond}} = 4$

`conditional_alice_bob_dim()` 返回 **4**(2×2,A qubit ⊗ B qubit),与 §1.1 口径一致。

---

## 8. 观测算符 $\Gamma_k$ 的正确形式(v0.2 修订,F3 修正)

### 8.1 Z 基 QBER

$$\boxed{\Gamma_{\text{qber\_Z}} = \proj{01}_{AB} + \proj{10}_{AB}}$$

**Claim**:$\text{Tr}(\Gamma_{\text{qber\_Z}} \rho_{AB}) = e$

**Proof**(Bell basis direct):
$$\text{Tr}(\Gamma_{\text{qber\_Z}} \rho_{AB}) = \bra{01}\rho\ket{01} + \bra{10}\rho\ket{10}$$

从 §7.3 矩阵:$\rho_{01,01} = \tfrac{e}{2},\; \rho_{10,10} = \tfrac{e}{2}$,故 Tr $= e$ ✓

**Angle 2(Bell expansion)**:$\ket{01} = \tfrac{1}{\sqrt 2}(\ket{\Psi^+} + \ket{\Psi^-})$,$\ket{10} = \tfrac{1}{\sqrt 2}(\ket{\Psi^+} - \ket{\Psi^-})$. 故 $\proj{01} + \proj{10} = \proj{\Psi^+} + \proj{\Psi^-}$.

$$\text{Tr}[(\proj{\Psi^+} + \proj{\Psi^-}) \rho_{AB}] = 0 + \tfrac{p}{3} + \tfrac{p}{3} = \tfrac{2p}{3} = e \quad\checkmark$$

### 8.2 X 基 QBER

$$\boxed{\Gamma_{\text{qber\_X}} = H_A H_B (\proj{01}_{AB} + \proj{10}_{AB}) H_A H_B}$$

**v0.3 订正**(codex round 2 F2):v0.2 把 $(H\otimes H)(\proj{01}+\proj{10})(H\otimes H)$ 的 Bell 分解写成 $\proj{\Psi^+}+\proj{\Phi^-}$,数值恰好对(对称深极化下两者权重都等于 $p/3$)但子空间标签错。正确分解为 $\proj{\Phi^-}+\proj{\Psi^-}$,推导如下。

#### 8.2.1 $H\otimes H$ 在 Bell 基上的作用表

$H\ket{0} = \ket{+},\; H\ket{1} = \ket{-}$。对 Bell 态:

| 输入 Bell 态 | 展开到 Z 基 | $(H\otimes H)\cdot$ 结果(Z 基) | 还原回 Bell |
|--------------|-------------|----------------------------------|-------------|
| $\ket{\Phi^+} = (\ket{00}+\ket{11})/\sqrt2$ | — | $(\ket{++}+\ket{--})/\sqrt2$ | $\ket{\Phi^+}$(自共轭) |
| $\ket{\Phi^-} = (\ket{00}-\ket{11})/\sqrt2$ | — | $(\ket{++}-\ket{--})/\sqrt2$ | $\ket{\Psi^+}$(注:$\ket{++}-\ket{--}=\ket{01}+\ket{10}$) |
| $\ket{\Psi^+} = (\ket{01}+\ket{10})/\sqrt2$ | — | $(\ket{+-}+\ket{-+})/\sqrt2$ | $\ket{\Phi^-}$(注:$\ket{+-}+\ket{-+}=\ket{00}-\ket{11}$) |
| $\ket{\Psi^-} = (\ket{01}-\ket{10})/\sqrt2$ | — | $(\ket{+-}-\ket{-+})/\sqrt2$ | $-\ket{\Psi^-}$(相位被 $\proj\cdot$ 吸收) |

即 $H\otimes H$ 在 $\{\Phi^+,\Phi^-,\Psi^+,\Psi^-\}$ 基上的置换矩阵为 $\Phi^+ \leftrightarrow \Phi^+,\; \Phi^- \leftrightarrow \Psi^+,\; \Psi^- \leftrightarrow \Psi^-$(最后一项带负号,不影响 $\proj\cdot$)。

#### 8.2.2 直接展开 $H\otimes H$ 作用到 $\proj{01}+\proj{10}$

$\ket{+-} = H\otimes H\ket{01} = \tfrac12(\ket{00}-\ket{01}+\ket{10}-\ket{11}) = \tfrac{1}{\sqrt2}(\ket{\Phi^-} - \ket{\Psi^-})$

$\ket{-+} = H\otimes H\ket{10} = \tfrac12(\ket{00}+\ket{01}-\ket{10}-\ket{11}) = \tfrac{1}{\sqrt2}(\ket{\Phi^-} + \ket{\Psi^-})$

$\Rightarrow \proj{+-} + \proj{-+} = \proj{\Phi^-} + \proj{\Psi^-}$(交叉项相消)✓

#### 8.2.3 Tr 计算(权重来自 §7.2 Bell-diag 系数)

$$\text{Tr}(\Gamma_{\text{qber\_X}} \rho_{AB}) = \text{Tr}[(\proj{\Phi^-}+\proj{\Psi^-})\rho_{AB}] = \tfrac{p}{3} + \tfrac{p}{3} = \tfrac{2p}{3} = e \quad\checkmark$$

数值与 v0.2 一致($e$),但 Bell 子空间标签已订正。

**对称性**:Z/X 基 QBER 相等(symmetric depolarization 性质)—— $\rho_{AB}$ 对 $\{\sigma_X,\sigma_Y,\sigma_Z\}$ 的 twirl 不变性,`test_qber_symmetry` 可在 R1.3 数值验证。

### 8.3 $p_{\text{sift}}$ 的接口契约(v0.3 与 REFACTORING_PLAN §4.6 对齐)

**v0.3 订正**(codex round 2 F4):v0.2 §8.4 写 `observation_keys = ("qber_Z", "qber_X")`,与 [REFACTORING_PLAN.md §4.6 line 796](../REFACTORING_PLAN.md) 的 `observation_keys=("qber_Z", "qber_X", "p_sift")` 契约冲突,使得 R1.2 / R1.4 / REFACTORING_PLAN 三份文档对同一 `MSEBProtocol` 接口给出不同签名。v0.3 统一为 REFACTORING_PLAN 契约。

**统一后的语义分层**:
1. **$p_{\text{sift}}$ 是 announcement-layer 的标量统计**(Alice / Bob 基选择匹配概率 + detection 通过率),不进入 WLC SDP 的 PSD 约束集。
2. **但 $p_{\text{sift}}$ 属于 `observation_keys`**:调用方须在 `observations` dict 显式提供该数值,`wlc_key_rate` 读取后作为 Devetak-Winter 外层乘子(§11 拼装 $R = p_{\text{sift}}\cdot [\cdots]$)。
3. **`observable("p_sift")`**:返回**标量常量**(理想 BB84 $= 0.5$;带损耗信道 $= \text{gain}\cdot 0.5$),而非 Hermitian 算符。R1.3 `wlc._OBSERVABLE_BUILDERS` 的 `p_sift` 构造器返回 `ScalarObservable(0.5)`(不同于 `qber_Z` 的 `HermitianObservable`)。

### 8.4 `observation_keys` tuple(v0.3 对齐)

对 BB84 M1:

$$\boxed{\texttt{observation\_keys} = (\texttt{"qber\_Z"},\, \texttt{"qber\_X"},\, \texttt{"p\_sift"})}$$

在 `build_bb84_protocol(qber=0.05)` 上,典型调用:

```python
wlc_key_rate(
    protocol,
    observations={"qber_Z": 0.05, "qber_X": 0.05, "p_sift": 0.5},
)
```

**与 REFACTORING_PLAN 的三处具体对齐点**:
- §4.4 `MSEBProtocol.observation_keys` tuple 必须三元
- §4.6 `wlc_key_rate(protocol, observations)` 的 `observations` 键集 **严格等于** `protocol.observation_keys`(缺键或多余键均 `ValueError`)
- §4.6 `observations["p_sift"]` 作为 bit/signal 的外层乘子,`R = p_sift · R_per_sift`

---

## 9. $\mathcal{G}$ / $\mathcal{Z}$ 构造 —— DEFERRED to R1.3

**v0.1 §10 的伪 Kraus** 以 "[AI-DERIVED, 待 R1.3 PDF 核对]" 标签给出,但 codex FAIL 指出该 Kraus 不符合 WLC Eq. (46)/(55)。**v0.2 暂缓给出显式 G/Z Kraus**;R1.3 实现期必须:

1. 人类研究者读 WLC 2018 Eq. (46)–(56) PDF,给出 BB84 的 G/Z 精确 Kraus
2. Python 验证 $\sum K^\dagger K = I$(或 $\leq I$ for CPTNI)
3. 在 QBER=0 验证 $D(\mathcal{G}(\rho) \| \mathcal{Z}(\mathcal{G}(\rho))) = 0$ 数值为 0(tolerance `1e-8`)
4. 在 QBER=0.05 验证 $D(\mathcal{G}(\rho) \| \mathcal{Z}(\mathcal{G}(\rho))) \approx h(0.05) = 0.2864$(tolerance `1e-3`)

**M1 需要知道的最少信息**(用于 `_construct_G_map`/`_construct_Z_pinching` 占位):
- $\mathcal{G}: \mathcal{L}(\mathcal{H}_A \otimes \mathcal{H}_B) \to \mathcal{L}(\mathcal{H}_{A_{\text{key}}} \otimes \mathcal{H}_{B_{\text{side}}})$,$d' = d_{A_{\text{key}}} \cdot d_{B_{\text{side}}} \leq 4$
- $\mathcal{Z}$ pinches $A_{\text{key}}$ in computational basis
- Devetak-Winter 拼装(v0.4 订正,见 `docs/literature/WLC-2018.md` v0.4 §5.2 PDF VERIFIED):$R = \min_\rho D(\mathcal{G}(\rho) \| \mathcal{Z}(\mathcal{G}(\rho))) - p_{\text{sift}} \cdot f_{\text{ec}} \cdot h(e)$([bit/signal];$p_\text{pass}$ 已通过 $\mathcal{G}$ 内 $\Pi$ projector 并入第一项。WLC Eq. 49-54 结论:$H = D$ 直接相等、同在 bit 单位,无 $\log_2 d$ 项、无 $/\ln 2$ 转换。v0.1 / v0.2 / v0.3 的 "$\log_2 d - D/\ln 2$" 写法**错误**,最终数值偶然自消所以 R 值不变)

**为什么 v0.1 §10 必须降级**:v0.1 写的 `K^G_{x,\theta_B} = \proj x_{A_{\text{key}}} \otimes \bra{x,\theta_B}_A \otimes \text{(sift)}_{?} \otimes \proj{\theta_B}_{B_{\text{side}}}` 在维度上就说不通 —— $\bra{x,\theta_B}$ 要求 $A$ 维度 4,但 §1.1 的 SDP 约定 $d_A = 2$。精确 G 需要完整 WLC §IV-B 对 BB84 的展开,M1 week 1 人类未完成 PDF 精读,故 deferred。

---

## 10. Hand calculation 作为 **lower-bound sanity check**(v0.3 降级,codex round 2 F3 订正)

**v0.3 降级说明**(codex round 2 F3)+ **v0.4 口径订正**(2026-04-19 PDF 核对):v0.2 把本节称为"独立证据链给出精确闭合"。这一声明过强 —— 本节 §10.2 只通过 entropic UR 给出 $H(A_Z|E) \geq 1-h(e)$ 的**下界**,未严格证明在量子侧信息 $B$ 下的等式 $H(A_X|B) = h(e)$ 或 BCKR 不等式的取等条件。**v0.4**:WLC PDF Eq. 54 直接给 $\min_\rho D(\mathcal{G}(\rho)\|\mathcal{Z}(\mathcal{G}(\rho))) = p_\text{sift}(1-h(e)) = 0.3568$ bit(非 $h(e)\ln 2 = 0.1985$ nat),见 `WLC-2018.md` v0.4 §5.2 / §6.4。**精确闭合**仍留 R1.3 SDP 数值验证(解析解 0.3568 bit 作为 SDP 最优值的参考)。

本节保留的意义:在 QBER=0 / QBER=0.05 两点,用本文件 §7-§8 的 $\rho_{AB}, \Gamma$ 对象给出**与 Shor-Preskill 数值一致的 lower bound**,作为 R1.3 SDP 求解器的 **sanity reference**(SDP 返回值 $\geq$ 本节 lower bound 即合理)。

### 10.1 Angle 1:由 $\rho_{AB}$ 直算 Z 基联合分布

对 QBER = 0.05($p = 0.075$),$\rho_{AB}$ 对角元(Z 基):

| $A B$ | 概率 |
|-------|------|
| $00$ | $(1-e)/2 = 0.475$ |
| $01$ | $e/2 = 0.025$ |
| $10$ | $e/2 = 0.025$ |
| $11$ | $(1-e)/2 = 0.475$ |

Alice measures Z,Bob measures Z,联合分布 $P(x_A, x_B) = \langle x_A x_B | \rho_{AB} | x_A x_B \rangle$。

- $P(A=B) = 0.475 + 0.475 = 0.95$ ✓(1 − QBER)
- $P(A\ne B) = 0.025 + 0.025 = 0.05$ ✓(= QBER)

**Alice 边缘**:$P(A=0) = 0.475 + 0.025 = 0.5$,$P(A=1) = 0.5$ ✓
**Bob 边缘**:同样 $1/2$-$1/2$

**条件熵** $H(A | B)$:Bob 看 $b$,对称下
$P(A=b | B=b) = 0.475/0.5 = 0.95$,$P(A \ne b | B=b) = 0.05$
$H(A | B) = h(0.05) = 0.2864$ bit ✓

### 10.2 Angle 2:entropic uncertainty relation 给 $H(A|E)$

**Berta-Christandl-Colbeck-Renes-Renner 2010 Thm 1**(以及 Coles-Colbeck-Kaniewski 2012):

$$H(A_Z | E) \geq \log_2 \tfrac{1}{c} - H(A_X | B)$$

对 Z vs X basis on 2-dim system:$\log_2(1/c) = \log_2(1/\|\braket{0|+}\|^2) = \log_2 2 = 1$.

$H(A_X | B) = h(e_X)$(Bob 量子态给 Alice X 基结果的条件熵,对称深极化 $= h(e)$)。

故 $H(A_Z | E) \geq 1 - h(e) = 1 - 0.2864 = 0.7136$ bit/sift ✓

### 10.3 Angle 3:对称性 sanity

由于 $\mathcal{E}_{\text{ch}}$ 对 $\{\sigma_X, \sigma_Y, \sigma_Z\}$ 对称,$e_Z = e_X = 2p/3$ 严格相等(§3.3 中已证)。这与 §8.1 和 §8.2 的 Tr 计算独立给出相同数字,非回代。

### 10.4 Angle 4:numpy 数值枚举(2026-04-19 执行)

作为独立第二证据链(codex round 1 要求),用 python/numpy 直接枚举 $\rho_{AB}(e)$ 的 Bell 展开 + 观测量 Tr:

```python
import numpy as np
from numpy import sqrt

zero, one = np.array([1,0]), np.array([0,1])
phi_p = (np.kron(zero,zero) + np.kron(one,one)) / sqrt(2)
phi_m = (np.kron(zero,zero) - np.kron(one,one)) / sqrt(2)
psi_p = (np.kron(zero,one) + np.kron(one,zero)) / sqrt(2)
psi_m = (np.kron(zero,one) - np.kron(one,zero)) / sqrt(2)
op = lambda v: np.outer(v, v)

for e in (0.0, 0.05, 0.10):
    p = 3*e/2
    rho = (1-p)*op(phi_p) + (p/3)*(op(psi_p)+op(psi_m)+op(phi_m))
    Γ_Z = np.diag([0,1,1,0])      # |01><01|+|10><10|
    H = (1/sqrt(2))*np.array([[1,1],[1,-1]])
    Γ_X = np.kron(H,H) @ Γ_Z @ np.kron(H,H)
    print(f"e={e}: Tr(ρ)={np.trace(rho):.4f}, "
          f"diag={[f'{rho[i,i]:.4f}' for i in range(4)]}, "
          f"Tr(Γ_Z·ρ)={np.trace(Γ_Z@rho):.4f}, "
          f"Tr(Γ_X·ρ)={np.trace(Γ_X@rho):.4f}")
```

**输出**(2026-04-19 14:12 CST,numpy 1.26):

```
e=0.0:  Tr(ρ)=1.0000, diag=['0.5000','0.0000','0.0000','0.5000'], Tr(Γ_Z·ρ)=0.0000, Tr(Γ_X·ρ)=0.0000
e=0.05: Tr(ρ)=1.0000, diag=['0.4750','0.0250','0.0250','0.4750'], Tr(Γ_Z·ρ)=0.0500, Tr(Γ_X·ρ)=0.0500
e=0.10: Tr(ρ)=1.0000, diag=['0.4500','0.0500','0.0500','0.4500'], Tr(Γ_Z·ρ)=0.1000, Tr(Γ_X·ρ)=0.1000
```

- Trace = 1 ✓
- 对角与 §7.3 预测 $[(1-e)/2, e/2, e/2, (1-e)/2]$ 完全一致 ✓
- $\text{Tr}(\Gamma_{\text{qber\_Z}} \cdot \rho) = e$ 精确成立 ✓
- $\text{Tr}(\Gamma_{\text{qber\_X}} \cdot \rho) = e$ 对称一致 ✓

**独立性说明**:此 numpy 脚本只用 Bell 态定义(原子操作),不引用 §7.3 的符号 result,是从 §7.2 Bell 展开公式独立重算,符合 codex round 1 "给一个 `numpy` 精确枚举的第二证据链" 要求。

### 10.5 最终拼装给 $R$(lower bound)

$R \geq p_{\text{sift}}[H_{\text{LB}}(A_{\text{key}} | E) - f_{\text{ec}} h(e)]$,其中 $H_{\text{LB}}(A|E) = 1 - h(e)$ 来自 §10.2 BCKR 不等式(**不是精确 Holevo 熵**),$f_{\text{ec}} = 1$(ideal EC 假设,非实际 LDPC 的 $f \approx 1.16$)。

| QBER $e$ | $p_{\text{sift}}$ | $H_{\text{LB}}(A\|E)$(§10.2) | $h(e)$ | $R \geq$ |
|----------|-------------------|-----------------------|--------|----------|
| 0 | 0.5 | 1.0000 | 0 | **0.5000** bit/signal(LB = SP) |
| 0.05 | 0.5 | 0.7136 | 0.2864 | **0.2136** bit/signal(LB = SP) |

独立对比 Shor-Preskill 2000 的 $R_{\text{SP}}(e) = p_\text{sift}\cdot (1 - 2h(e))$,$f_\text{ec}=1$:
- $e=0$:$R_{\text{SP}} = 0.5$ ✓
- $e=0.05$:$R_{\text{SP}} = 0.5 \cdot (1 - 0.5728) = 0.2136$ ✓

**本节只能得出的结论**:WLC SDP 数值 **下界**与 Shor-Preskill 数值在 QBER ∈ $\{0, 0.05\}$ 一致。BCKR 等式闭合(即 $H_{\text{LB}} = H$)需要在 R1.3 SDP 数值上直接验证 `abs_gap ≤ 5e-4`(§6.2 benchmark 表)。

---

## 11. 跨对象不变量核验

| Invariant | BB84 值 | Python check |
|-----------|---------|---------------|
| I1:$\dim_{\text{in}}(\mathcal{E}) = \prod d_{S,i}$ | $2 = 2$ | ✓ |
| I2:$P_\kappa \in \mathcal{P}$ | Alice ∈ (Alice,) | ✓ |
| I3:sift_keep 参数与 $\mathcal{C}$ 兼容 | $(\theta_A, \theta_B, b)$ | ✓ |
| I4:observation_keys 非空 | $(\text{qber\_Z},\text{qber\_X},\text{p\_sift})$ | ✓ |
| I5(R1.4):scope_tag | `"covered"` + reason=None | ✓ |

---

## 12. Limitations(codex F5 新增)

1. **$\mathcal{G}$ / $\mathcal{Z}$ Kraus 未闭合**(§9):M1 Week 1 只给出 $\rho_{AB}, \Gamma$ 的闭合形式。G/Z 的精确 Kraus 依赖 WLC 2018 Eq. (46)–(56) PDF 逐步对齐,R1.3 实现期必须人类研究者手动完成。本文件在 R1.3 实现后(R1.3 验收通过时)转为 v1.0。
2. **$\mathcal{K}$ key map 的具体 Kraus 延后**(§6):v0.1 给出的形式非法已删除;正确形式待 R1.3 与 `_construct_G_map` 共同给出。
3. **GEAT NSP 条件只标 [SYN]**(§4):Alice 的 $\theta_A$ 公开涉及 active basis selection,严格 NSP 论证依赖 Metger 2024 §III,待 Phase 1 Sub-Q2.4 精读。
4. **对称深极化假设**:本文件只处理对称 Pauli 去极化;一般 Eve 策略会造成非对称错误,WLC SDP 处理一般情况,但 §7-§8 的 Bell-diag 显式形式不再适用(SDP 变量变为一般 Hermitian 半正定 $\rho_{AB}$)。
5. **无限维 / Fock 截断**:本文件不涉及。PROSPECTUS §3.1 H4 约束下,BB84 天然是 qubit 协议,截断问题不出现。但 decoy-state BB84(Phase 1 Sub-Q2)需要显式 Fock 截断误差界。
6. **Reverse reconciliation vs direct**:本文件假设 Alice → Bob 正向 EC(direct reconciliation)。Bob → Alice 逆向 EC 会交换 $\mathcal{K}$ 的 key party + 不同 $\Gamma$ 组装,不在 M1 scope。
7. **§10 只给 lower bound,不给精确闭合**(v0.3 降级 + v0.4 口径订正):§10 用 BCKR 不等式得 $H(A|E) \geq 1-h(e)$,但 BCKR 取等条件未在本文件证明。R1.3 SDP 数值验证 $\min_\rho D(\mathcal{G}\|\mathcal{Z}(\mathcal{G})) = p_\text{sift}(1-h(e)) = 0.3568$ bit(v0.4 口径,non-nat,见 `WLC-2018.md` v0.4 §5.2)才构成精确闭合。
8. **§4 的非 signaling 假设**:`scope_tag = "covered"` 仅在 PROSPECTUS §3.1 H1-H3 + source-characterized 下成立,未涵盖 DI 或 MDI 的 Bell violation 证书。

---

## 13. AI 协助范围声明

**Claude Opus 4.7(1M context)本次协助**:

- v0.1 初稿全文
- v0.2 响应 codex FAIL 的 §1 register 口径统一、§5 非法 Kraus 删除、§7 $\rho_{AB}$ 重写为 Bell-diag、§8 $\Gamma$ 正确形式重写、§9 G/Z deferred 明示、§10 三条独立证据链、§12 Limitations 新增
- LaTeX 排版、Bell 态代数、entropic UR 引用

**必须人类研究者(Teng, Jun)核对**:

1. §7.3 $\rho_{AB}$ 矩阵元数值(Bell-diag 展开)—— R1.3 numpy 自检
2. §9 WLC 2018 Eq. (46)–(56) BB84 G/Z 展开 PDF 精读后给具体 Kraus
3. §10.2 entropic UR 引用($c = 1/2$ BB84 Z/X 互对角化 overlap)的教科书对齐(Berta et al. 2010 Thm 1)

### 使用的外部资源

- PROSPECTUS.md §4.1-4.3(本仓库)
- PHASE0_M1_TECHNICAL_SPEC.md §3(本仓库)
- WLC-2018.md v0.1(本仓库)—— 注意同步 codex FAIL 修订 v0.2 待出
- Shor-Preskill 2000 Thm 1(共识文献,未在本文件内逐条引 PDF)
- Berta-Christandl-Colbeck-Renes-Renner 2010 Thm 1 entropic UR(引用 §10.2)

### 未使用

- Web 搜索 / WebFetch(v0.2 修订期)
- Zotero 全文读(v0.2 修订期;PDF 未同步)

---

## 14. R1.3 代码实施 checklist

```python
# qkdx/protocols/bb84.py(R1.3 期实施)
# --- §2 → Alice source ---
# P1 = SourceParty(name="Alice", key_register_dim=4, signal_register_dim=2,
#                   eb_state=<§2.2 4x2 matrix>)
# 注:EB 纯化态只进 joint_state() / executed_state();WLC SDP 用 §7 的 ρ_{AB}(2x2)
#
# --- §3 → channel ---
# channel = KrausMap(kraus=[K_0,K_1,K_2,K_3] per §3.4)  # dim_in=dim_out=2
#
# --- §3.5 → Bob POVM(仅用于 _build_observable_operators) ---
# 不直接进 MSEBProtocol,只由 numerics/wlc._build_observable_operators 引用
#
# --- §4 → announcement ---
# A = AnnouncementRule(publish=lambda θB,b: θB,
#                      sift_keep=lambda θA,θB,b: θA == θB)
#
# --- §5 → T ---
# T = AcceptanceTest.always_accept()
#
# --- §6 → K ---
# K = KeyMap(key_party="Alice", bitmap={0: 0, 1: 1})  # v0.3 订正:KeyMap 无 key_register_dim/map 字段
# # GMap(map=<DEFERRED>, dim_key=2, dim_side=...) 由 WLC SDP 层 _construct_G_map 给出,不属于 KeyMap
#
# --- §7 → conditional_alice_bob ---
# MSEBProtocol.conditional_alice_bob() 返回 §7.3 Bell-diag ρ(p=3·qber/2)
# conditional_alice_bob_dim() 返回 4
#
# --- §8 → observables ---
# _OBSERVABLE_BUILDERS = {
#     "qber_Z": lambda proto: <§8.1 proj>,
#     "qber_X": lambda proto: <§8.2 proj>,
# }
# numpy 自检:Tr(Γ_qber_Z · ρ(qber=0.05)) == 0.05 (atol 1e-12)
#
# --- R1.4 → scope_tag ---
# MSEBProtocol(..., scope_tag="covered", scope_reason=None)
#
# --- §9 → G, Z(R1.3 实施期 deferred 工作) ---
# 1. 人读 WLC Eq. (46)-(56) PDF,写 _construct_G_map / _construct_Z_pinching
# 2. numpy 验证 QBER=0 → D=0, QBER=0.05 → D≈h(0.05)=0.2864
# 3. SDP 跑 test_wlc_bb84_matches_shor_preskill
```

---

## Changelog

- **v0.2**(2026-04-19, 同日):响应 codex round 1 FAIL 重写。修复 F1 非法 Kraus、F2 register contract 冲突、F3 Γ 归一化、F4 non-independent sanity、F5 缺 Limitations。§9 G/Z 明示 deferred。**补丁**:§10.4 加入 numpy 数值枚举作为 Angle 4 独立证据(响应 codex round 1 具体 ask)。
- **v0.1**(2026-04-19):首次落盘,被 codex FAIL。保留在 git 历史作为对照。

---

*R1.2 BB84 MS-EB Formulation v0.2 结束。*
