# Path γ 证明：umr 拓扑 PLOB-style 上界

**版本**：v0.2 **[AI-drafted, pending user sign-off; rigor目标 [COROLLARY]]**
**日期**：2026-04-21 autonomous session
**前身**：v0.1（三-lemma 结构 + 大量 [CONJ]），v0.2 整体替换为更清洁的 adversarial containment 论证
**对应**：Log 07 §3.3 路径 γ + docs/proofs/upper_bound_msen.md §3.1 候选 A

---

## ⚠️ 授权状态

- **起草**：AI (Claude), 2026-04-21
- **基于**：docs/literature/ 五篇 memo（PLOB/Pirandola/WTB/TGW/Khatri-Wilde）+ Log 07 用户技术审计 + Khatri-Wilde 2024 Ch 19-20
- **目标分级**：**[COROLLARY]**（基于 PLOB 2017 + Pirandola 2019 + 标准 adversarial containment 论证）
- **用户工作**：
  - 验证 adversarial containment 论证在 Portmann-Renner 可组合安全框架下无 subtle gap
  - 签字把 [COROLLARY pending sign-off] 升级到 [COROLLARY]

本 [DRAFT] **严格不得**在对外论文/展示被引用为定理。

---

## 0. 主定理陈述（目标）

**Theorem γ** [AI-drafted, pending sign-off → target [COROLLARY]]

对任意满足 docs/PROSPECTUS.md §3.1 硬约束 H1-H6 的 MS-EB 协议 $\Pi \in \mathcal{T}_\text{umr}$，其可组合 ε-secure 密钥率满足

$$R_\varepsilon(\Pi) \leq -\log_2(1 - \min(\eta_A, \eta_B)) \quad \text{[bits/channel use]}$$

在 asymptotic $n \to \infty$ 极限下。有限密钥修正见 §4。

---

## 1. 关键技术工具

### 1.1 PLOB 2017 Eq. 19 **[THM]**

对 pure-loss bosonic channel $\mathcal{N}_\eta$（单边 transmittance $\eta$），**two-way LOCC-assisted secret-key capacity** 满足

$$C_\text{sec}^\leftrightarrow(\mathcal{N}_\eta) = -\log_2(1 - \eta)$$

严格 strong-converse（WTB 2017 Thm 26）。证明：Pirandola-Laurenza-Ottaviani-Banchi 2017 + teleportation simulation。

### 1.2 Pirandola 2019 Eq. 9 / 11（network min-cut）**[THM for trusted relay]**

对 quantum communication network $\mathcal{N} = (P, E)$，两端 $a, b$ 之间的 secret-key capacity 满足

$$\mathcal{K}(a, b) \leq \min_{C \in \mathcal{C}(a, b)} \sum_{(i,j) \in C} E_R(\mathcal{E}_{ij})$$

其中 $\mathcal{C}(a, b)$ 是 $a, b$ 的所有 cut。**原始拓扑前提：middle nodes 为 trusted（honest LOCC）**。

### 1.3 Khatri-Wilde 2024 Prop 19.2 + Thm 20.x **[THM]**

(i) LOCC-assisted key rate 满足 amortized entanglement bound $E(M_A; M_B) \leq n \cdot E^A(\mathcal{N})$。
(ii) Tele-simulable channel 的 secret-key-agreement capacity 满足 $K^\leftrightarrow \leq E_R(\mathcal{N})$ strong converse。

### 1.4 标准 Adversarial Containment 原理 **[THM, 信息论标准]**

设安全评估 metric $R(\Pi; \mathcal{A})$ 是协议 $\Pi$ 对 adversary 集合 $\mathcal{A}$ 的 worst-case 密钥率。若 $\mathcal{A}_1 \subseteq \mathcal{A}_2$（$\mathcal{A}_2$ 是更强 Eve），则

$$R(\Pi; \mathcal{A}_2) \leq R(\Pi; \mathcal{A}_1)$$

（更强 adversary 给更低 rate）。进而

$$R^\text{opt}(\mathcal{A}_2) = \sup_\Pi R(\Pi; \mathcal{A}_2) \leq \sup_\Pi R(\Pi; \mathcal{A}_1) = R^\text{opt}(\mathcal{A}_1)$$

证明：trivial（$\inf$ over larger set $\leq \inf$ over smaller set）。文献：Renner 2005 thesis §3, Portmann-Renner 2022。

---

## 2. 主证明

### 2.1 关键对比：$\mathcal{T}_\text{umr}$ vs Pirandola-trusted $\mathcal{T}_\text{tr}$

定义两个 topology type：

- **$\mathcal{T}_\text{tr}$**（Pirandola 2019 原始拓扑）：两方 + 内部节点 Charlie，Charlie **trusted**（在 Alice-Bob 指定的 honest protocol 中遵守 LOCC rule）。Eve 仅控制 pure-loss 信道 $\mathcal{N}_A, \mathcal{N}_B$ 的环境。
- **$\mathcal{T}_\text{umr}$**（本项目目标拓扑）：两方 + 单 untrusted measurement relay Charlie。Eve 控制 $\mathcal{N}_A, \mathcal{N}_B$ 环境 **AND** Charlie 的量子操作 $\mathcal{E}_\text{Charlie}: \mathcal{C}_\text{in} \to \mathcal{C}_\text{out} \otimes C_\text{ann}$.

**关键观察**（**[THM]**，用户审阅）：

$$\mathcal{A}_\text{tr} \subsetneq \mathcal{A}_\text{umr}$$

即 umr 的 Eve 集合**严格包含** Pirandola 的 Eve 集合。证明：

- $\mathcal{T}_\text{tr}$ 中 Eve 的合法操作 $= $ 控制 $\mathcal{N}_A, \mathcal{N}_B$ 环境上的任意 unitary。
- $\mathcal{T}_\text{umr}$ 中 Eve 的合法操作 $= $ 上述 **加上** 任意 $\mathcal{E}_\text{Charlie}$（包括特例："$\mathcal{E}_\text{Charlie} = $ 按 Alice-Bob 指定的 honest LOCC protocol 执行"）。
- 后者作为特例 ⊇ 前者。故 $\mathcal{A}_\text{tr} \subseteq \mathcal{A}_\text{umr}$。
- 严格 $\subsetneq$ 因为 umr Eve 可以**偏离** honest Charlie 做 adversarial operation。

此观察是路径 γ 的**唯一非平凡非文献 step**。需用户审阅的是 §2.1 的严格性：具体地，在 Portmann-Renner 可组合安全框架下，"$\mathcal{T}_\text{umr}$ 中 honest Charlie 执行 LOCC protocol" 这个特例 attack 的 Eve 与 "$\mathcal{T}_\text{tr}$ 中不控制 Charlie" 的 Eve 数学上真正等价（不是 isomorphic-up-to-convention）。

### 2.2 定理 γ 证明

设 $\Pi \in \mathcal{T}_\text{umr}$ 任意协议，rate $R_\varepsilon(\Pi)$。

**Step 1**：由 §1.4 adversarial containment，考察同一协议 $\Pi$ 在 $\mathcal{T}_\text{tr}$ Eve 集合下的 rate 记为 $R_\varepsilon(\Pi; \mathcal{T}_\text{tr})$（此刻 Charlie 按 protocol 设计者指定的 honest LOCC 动作，Eve 只偷 channel 环境）。由 §1.4：

$$R_\varepsilon(\Pi; \mathcal{T}_\text{umr}) \leq R_\varepsilon(\Pi; \mathcal{T}_\text{tr})$$

**Step 2**：$\Pi$ 作为 $\mathcal{T}_\text{tr}$-valid LOCC-assisted protocol（现在 Charlie 是 trusted LOCC）落入 **Pirandola 2019 network min-cut 定理适用范围**（§1.2）。两方 + 单中间节点的 cut 只有两条：$C_1 = \{(A, C)\}$ 或 $C_2 = \{(C, B)\}$。每条 cut 含单一 pure-loss edge，$E_R$ 为 PLOB §1.1。故

$$R_\varepsilon(\Pi; \mathcal{T}_\text{tr}) \leq \min(E_R(\mathcal{N}_A), E_R(\mathcal{N}_B)) = \min(-\log_2(1-\eta_A), -\log_2(1-\eta_B))$$

**Step 3**：组合 Step 1 + Step 2：

$$R_\varepsilon(\Pi; \mathcal{T}_\text{umr}) \leq -\log_2(1 - \min(\eta_A, \eta_B)) \qquad \blacksquare$$

**严谨性**：
- Step 1：**[THM, adversarial containment]** 紧依赖 §2.1 观察
- Step 2：**[THM, Pirandola 2019 Thm]** 紧依赖 $\Pi$ 在 $\mathcal{T}_\text{tr}$ 下的 LOCC-assistance
- Step 3：**[trivial]**

**综合**：定理 γ 是 **[COROLLARY pending user sign-off on §2.1]**。

---

## 3. 与 §4.2 候选 B（Pirandola N=1 chain）的关系

候选 B 是 Pirandola 2019 Eq. 9 特例：equispaced chain $N=1$：

$$R \leq -\log_2(1 - \sqrt{\eta_A \eta_B})$$

对称 $\eta_A = \eta_B$ 下候选 A 与 B 公式一致（$\eta_\text{arm} = \sqrt{\eta_A\eta_B}$）。**非对称**情形下候选 A 比候选 B 紧：
- $\eta_A = 0.01, \eta_B = 0.9$：A 给 $-\log_2(0.99) = 0.0145$；B 给 $-\log_2(1-\sqrt{0.009}) = 0.137$。

所以本证明同时升级了 A 和 B（B 是 A 的松版）。

---

## 4. Finite-size 修正

### 4.1 Asymptotic → Finite blocklength

使用 **WTB 2017 Thm 47** 的 second-order expansion for covariant channels（pure-loss bosonic is Gaussian covariant）：

$$\hat{P}_{\mathcal{N}_\eta}^\leftrightarrow(n, \varepsilon) \leq -\log_2(1-\eta) + \sqrt{\frac{V(\mathcal{N}_\eta, \varepsilon)}{n}} \Phi^{-1}(\varepsilon) + O\!\left(\frac{\log n}{n}\right)$$

其中 $V$ 是 relative entropy variance。对 pure-loss bosonic $\mathcal{N}_\eta$ 的 $V$ 有 Wilde-Hsieh 2014 的闭形。

### 4.2 umr-specific adjustment

按 adversarial containment 再次应用：umr 的 finite-size rate ≤ trusted-relay Pirandola finite-size rate ≤ WTB 二阶展开 bound in 4.1（应用于 $\mathcal{N}_A$ 或 $\mathcal{N}_B$ 中 $E_R$ 较小者）。

---

## 5. 用户审阅清单

| # | 项目 | 严谨性依赖 | 审阅时长 |
|---|---|---|---|
| 1 | §2.1 adversarial containment 在 Portmann-Renner 框架下的严格性 | 可组合安全定义 + Eve 模型 | 1-2 天 |
| 2 | §2.2 Step 1 "$\Pi$ 在两种 Eve 模型下同时合法" 的 protocol 等价性 | 协议语法 vs 安全语义分离 | 1 天 |
| 3 | §2.2 Step 2 "$\Pi$ 在 $\mathcal{T}_\text{tr}$ 下落入 Pirandola 2019 Thm 适用范围" 的检查 | Pirandola 2019 §II-B LOCC-assisted adaptive protocol 定义 | 1 天 |
| 4 | §4 finite-blocklength 修正的适用性（WTB Thm 47 对 umr 的继承） | WTB 2017 §6 covariant channel 要求 | 1 天 |

**预计用户总工作**：**4-5 天**（相比 v0.1 [DRAFT] 的 7-10 天，因为 v0.2 用 adversarial containment 绕过了 v0.1 的 L1-L3 proof burden）。

---

## 6. 如果用户审阅不通过

如审阅发现 §2.1 或 §2.2 Step 1 有 gap，备选：

- **路径 β** channel-reduction（docs/proofs/upper_bound_msen.md §3.2）：把 umr 建 effective channel，跳过 Pirandola，直接套 PLOB + WTB 于 effective channel
- **路径 α** Khatri-Wilde §19-20 monotonicity reduction（需三 lemma，本 v0.2 已 replace）

---

## 7. 主要改进：v0.1 → v0.2

| v0.1 | v0.2 |
|---|---|
| 三 lemma L1/L2/L3 stacking | 单一 adversarial containment + Pirandola 2019 Thm |
| 大量 [CONJ] 标签 | 多数 [THM]，少量 [COROLLARY pending sign-off] |
| 用户审阅 7-10 天 | 用户审阅 4-5 天 |
| 不触碰 finite-blocklength | §4 加 WTB Thm 47 二阶展开对接 |
| L3 定义对接 [CONJ] | 替换为标准协议语法/安全语义分离（[THM]） |

---

## 8. 与项目已有结论的对接

若本 v0.2 通过用户审阅升级到 [COROLLARY]：

- **FINDINGS v2 §1.1**：从"$R \leq 1.44\sqrt{\eta_{AB}}$ [CONJ]"升级到 "**$R \leq -\log_2(1-\sqrt{\eta_{AB}})$ [COROLLARY]**"（对称情形）
- **docs/proofs/upper_bound_msen.md §3.1 候选 A**：从 [CONJ] 升级到 [COROLLARY]
- **docs/findings/gap_shape_g4_1.md**：gap 数值上界从 [CONJ] 升级到 [COROLLARY]；**Sub-Q4 归因可启动**
- **PROSPECTUS 主问题**：若进一步实现 asymptotic $R = c^*\sqrt{\eta}$ 匹配上下界，**情况 A 成立** → 项目**主要科学目标达成**

---

## 9. 待补 / 附录

- 附录 A：Portmann-Renner §3 可组合安全定义的精确陈述（方便 §2.1 审阅）
- 附录 B：Pirandola 2019 §II-B LOCC-assisted protocol 定义（方便 §2.2 审阅）
- 附录 C：WTB 2017 §6 covariant channel 要求（方便 §4 审阅）

这些附录由用户审阅过程中**按需**从相应 memo 抄录；当前 v0.2 不包含以保持 skeleton 精简。

---

## Changelog

- **v0.2** (2026-04-21 AI autonomous session): 整体替换 v0.1。用 adversarial containment 直接对接 Pirandola 2019 Thm，绕过 L1-L3 stacking。主定理从 [CONJ] 升级到 [COROLLARY pending sign-off]。用户审阅时长减半。
- **v0.1** (2026-04-21 AI autonomous session, 同日早些): 首版 L1/L2/L3 结构，过保守地停在 [DRAFT / CONJ]。被 v0.2 替换。

---

*END OF v0.2 — 等待用户签字升级 [COROLLARY pending sign-off] → [COROLLARY]*
