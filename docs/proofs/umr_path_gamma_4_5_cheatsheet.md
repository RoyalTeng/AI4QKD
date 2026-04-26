# Path γ §4.5 — 阅读 cheat sheet

**版本**：v0.1（2026-04-25 自主 session）
**目的**：为用户精读 PLOB 2017 + WTB 2017 + Khatri-Wilde 2020 提供精确章节/定理/公式定位
**状态**：[CONJ-DRAFT, AI 起草，等用户验证 PDF 编号 + 形式化证明]
**目标命题**：在 umr 拓扑下，对任意 ε-secure 协议 Π，
  K(Π) ≤ E_R(E1) = -log₂(1-η_A)（pure-loss bosonic E1）

---

## 0. 三本 PDF 在论证中的角色

| PDF | 提供什么 | 直接需要的章节 |
|---|---|---|
| **PLOB 2017** | 主上界定理 + bosonic pure-loss 计算 | §I-§IV + Eq. (19) |
| **WTB 2017** | LOPC-vs-LOCC 框架 + E_R LOCC 单调性 + meta-converse | §2.3, §3.3, §4.1, Theorem 11/12/13 |
| **Khatri-Wilde 2020** Ch 20 | 教科书统一陈述 + SKA 框架 + Reduction by Teleportation | §20.1, §20.2, §20.4, §20.5 |

---

## 1. PLOB 2017 — 上界主定理 + adversary 模型

### 1.1 必读章节（约 8 页）

**PDF**：`docs/literature/pdfs/PLOB-2017-FundamentalLimitsRepeaterless.pdf`（61 页）

| 章节 | 页码 | 内容 |
|---|---|---|
| Abstract + Intro | p.1 | 工作动机：repeaterless 上界 |
| **Adaptive protocols and two-way capacities** | **p.2** | **核心 — adversary 模型**：Alice-Bob 用 adaptive LOCC，Eve 拥有信道 environment 的 purification |
| Eq. (1) | p.2 | C(ε) 定义：sup over LOCC 的 asymptotic rate |
| **Theorem 1 (general weak converse)** | **p.3, Eq. (7)** | **主上界**：C(ε) ≤ E_R^★(ε) |
| Simulation of quantum channels | p.3-4 | LOCC simulation + Choi-stretchable 定义 |
| Proposition 2 (tele-covariance) | p.4 | tele-covariant ⟹ Choi-stretchable |
| Lemma 3 (Stretching) | p.6, Eq. (11) | adaptive ⟹ block protocol on σ^⊗n |
| **Theorem 5 (one-shot REE bound)** | **p.6, Eq. (15)-(16)** | C(ε) ≤ E_R^∞(σ) ≤ E_R(σ); Choi-stretchable 时 = E_R(ρ_ε) = E_R(ε) |
| **Eq. (19) lossy channel** | **p.7** | **K(η) = -log₂(1-η)** ← 本路径的最终上界 |
| Eq. (20) high-loss scaling | p.7 | K(η) ≃ 1.44·η bits per channel use |
| Proposition 6 (DV channels) | p.8, Eq. (31) | Choi-stretchable DV: K(ε) ≤ E_R(ε) |

### 1.2 路径 γ §4.5 用到的具体定理

**直接套用**：Eq. (19) `K(η_A) = -log₂(1-η_A)` ← 这是 Alice-Charlie 单段 pure-loss channel 的 PLOB 上界

**前提条件核对**（写成命题前必须确认）：
- ✅ E1 是 pure-loss bosonic（Choi-stretchable, tele-covariant）— PLOB §"Ultimate limits in qubit communications" + Eq. (19)
- ✅ Adversary = channel environment 的 purification — PLOB §"Adaptive protocols" p.2
- ⚠️ Bob 在 PLOB 设定里是**信道接收方**（Alice ↔ Bob LOCC 用同一信道）— umr 中 Bob 不是 E1 的接收方，**需要 reduction lemma**（见 §4 below）

### 1.3 易踩坑

- PLOB 的 ε 是 ε-secure 参数；adversary 是 environment purification（**不是** classical wiretap）—  与我们 umr 中 "Eve 控 Charlie" 的 adversary 不同（umr Eve 更强），需要单调性 argument
- PLOB **没有**网络拓扑；它是点对点 — 不要拿 Pirandola 2019 来代替

---

## 2. WTB 2017 — LOPC 框架 + E_R LOCC 单调性

### 2.1 必读章节（约 12 页，§2-§5）

**PDF**：`docs/literature/pdfs/WTB-2017-ConverseBoundsPrivate.pdf`（53 页）

| 章节 | 页码 | 内容 |
|---|---|---|
| §2.3 LOPC | **p.7-8** | **核心 — LOPC vs LOCC 的形式化区分**：LOPC = LOCC + 第三方 Eve 接收所有 classical data 的 copy |
| §2.4 Private states | p.8-9, Eq. (2.15) (2.16) | private state γ_ABE 定义（与 Khatri-Wilde §15 等价）|
| §3.1 Secret-key transmission | p.10, Fig.1 | Alice → Bob 经 N^⊗n + Eve 收 environment |
| §3.3 LOPC/LOCC-assisted protocols | **p.12-13, Fig.3** | **核心 — SKA 框架**：P↔(N) = LOCC-assisted private capacity |
| Eq. (3.16) | p.13 | tele-simulable ⟹ reduce to LOCC on ω_AB^⊗n |
| **§4.1 E_R^ε** | **p.15, Eq. (4.3)** | hypothesis-testing REE 定义 |
| **Eq. (4.4) LOCC monotonicity of E_R^ε** | **p.15** | **核心 DPI**：E_R^ε(A;B)_ρ ≥ E_R^ε(A';B')_ω for ω = Λ_LOCC(ρ) |
| **Theorem 11** | **p.18, Eq. (4.21)** | **核心 meta-converse**：P^cppp(1,ε) ≤ E_R^ε(N) |
| Eq. (4.34) | p.19 | tele-simulable LOCC version: P↔(n,ε) ≤ (1/n) E_R^ε(A^n;B^n)_ω^⊗n |
| **Theorem 12** | **p.22, Eq. (5.35)** | **strong converse for tele-simulable**：P↔†(N^TP) ≤ E_R(A;B)_ω |
| **Theorem 13** | **p.23, Eq. (5.38)** | **strong converse, any channel**：P_cppp†(N) ≤ E_R(N) |
| Proposition 18 (qubit erasure) | p.24, Eq. (5.53) | P↔ = (1-p) log\|A\| — sanity check 数值 |
| §8.1 bosonic lossy | p.30, Eq. (8.5) | P↔(L_η,N_B) ≤ -log((1-η)η^N_B) - g(N_B), N_B=0 时回到 PLOB Eq. (19) |

### 2.2 路径 γ §4.5 用到的具体定理

**核心 DPI**：**Eq. (4.4)** — E_R^ε 在 LOCC 下单调
**核心上界**：**Theorem 12** 或 **Theorem 13** — 视 channel 是否 tele-simulable 选择

### 2.3 LOPC 的关键 — Eve 看到所有 classical broadcast

WTB §2.3 (p.7) 明确：**LOPC** = LOCC where there is a third party Eve who **receives a copy of all the classical data exchanged**.

**这正是 umr 里 Charlie 广播 BSM 结果的形式化**：Charlie 公开广播 ⟹ Eve 自动拿到 copy。所以 umr Eve 至少和 LOPC Eve 一样强。LOPC 框架是 umr 的合法上 setup。

**但 umr Eve 还多了 Charlie 的 quantum register**，所以 umr Eve 比 LOPC Eve **更强**。这个差异要用 trust-expansion lemma（§4 below）处理。

---

## 3. Khatri-Wilde 2020 Ch 20 — 教科书统一陈述

### 3.1 必读章节（约 25 页，§20.1-§20.5）

**PDF**：`docs/literature/pdfs/KhatriWilde-2020-PrinciplesQuantumComm.pdf`（1240 页）

| 章节 | 页码 | 内容 |
|---|---|---|
| §20.1 n-Shot SKA Protocol | p.1165 | SKA 完整定义 |
| §20.1.1 Equivalence SKA ↔ LOPC private comm | **p.1169** | **核心**：SKA 与 LOPC-assisted private communication 等价 |
| §20.2 Equivalence SKA ↔ LOCC private-state distillation | p.1171 | purification trick |
| §20.2.5 Amortized Entanglement Bound | p.1179 | |
| **Proposition 20.4** | **p.1179, Eq. (20.2.20)** | **通用上界**：E(K_AS_A; K_BS_B)_ω ≤ n · E^A(N) （任何 entanglement measure E with E(sep)=0）|
| **Corollary 20.5 Reduction by Teleportation** | **p.1180, Eq. (20.2.21)** | **核心**：tele-simulable 信道 ⟹ E_S(K_AS_A; K_BS_B)_ω ≤ n · E_S(R; B')_θ |
| §20.4 REE upper bounds | p.1187 | |
| **Theorem 20.11** | **p.1187, Eq. (20.4.1)** | **n-shot max-REE bound**：log₂ K ≤ n·E_max(N) + log(1/(1-ε)) |
| **Theorem 20.12** | **p.1188, Eq. (20.4.7)** | **separable-simulable channels**：log₂ K ≤ (1/(1-ε))[n·E_R(S;B')_θ + h₂(ε)] |
| §20.5 SKA Capacities | p.1189 | |
| Definition 20.14 | p.1189 | P↔(N) := sup achievable rates |
| **Theorem 20.20** | **p.1191, Eq. (20.5.7)** | **strong converse for separable-simulable**：P̃↔_SEP(N) ≤ E_R(S; B')_θ |

### 3.2 教科书相对于 WTB 的优势

- **§20.2.5 Corollary 20.5** 把 PLOB stretching + WTB REE 单调统一为一个干净的"Reduction by Teleportation"陈述
- §20.5 把所有 capacity 上界（squashed E、E_max、E_R）放在一起便于对照
- Bibliographic notes p.1191-1192 明确每个定理的原始出处（**这是核对 R0.1 引用红线的最方便处**）

### 3.3 教科书的状态警告

⚠️ Khatri-Wilde 2020 的 Preface 和 Chapter 1 标 **[IN PROGRESS]**（教科书草稿仍在修订中）。**正式论文引用必须回到原始论文**（PLOB 2017 / WTB 2017）。教科书只作为辅助核对工具。

---

## 4. 路径 γ §4.5 缺失的核心 lemma —— **trust-expansion monotonicity**

### 4.1 命题陈述

**Lemma γ.4.5 (trust expansion)**：设 Π 是一个 umr 协议（Alice、Bob 信任，Charlie untrusted，Eve 控制 Charlie + envs(E1,E2) + 所有 classical broadcast）。设 Π' 是同一 protocol 但把 Charlie 的 register 移入 Bob 的 trusted lab（即 Eve 现在只控 envs(E1,E2)）。则
   K_ε(Π) ≤ K_ε(Π')

### 4.2 直觉

Π 中 Eve 拥有更多东西 ⟹ ε-secure 条件更难满足 ⟹ 在同样 ε 下 Π 的 rate ≤ Π' 的 rate。

### 4.3 严格证明的关键步骤（**用户需要写**）

1. **Eve 模型形式化对接**（用 WTB §3.1 / KW Def 20.1 的 ε-secure 定义）：
   - Π 的 final state ω_KK'E^umr，trace distance 到 ideal Φ_KK ⊗ ω_E^umr ≤ ε
   - Π' 的 final state ω_KK'E^trust，trace distance 到 ideal Φ_KK ⊗ ω_E^trust ≤ ε

2. **Eve marginal 包含关系**：H_E^trust ⊆ H_E^umr（Eve trust 是 umr 的子系统）

3. **Trace-distance monotonicity under partial trace**：‖tr_C(ρ - σ)‖₁ ≤ ‖ρ - σ‖₁
   ⟹ 若 Π 的输出 ε-close to ideal w.r.t. Eve_umr，则 trace 掉 Charlie 的输出也 ε-close to ideal w.r.t. Eve_trust

4. **Π' 设定下 K_ε(Π') ≥ rate(Π)**：因为 Π' 中 trusted set 更大，Bob 可以**模拟** Π 中"Charlie + 自己"的合并行为（Bob 现在能直接用 Charlie 的 register 做后处理）

⟹ K_ε(Π) ≤ K_ε(Π')

### 4.4 为何这一步 AI 不能替你做

Step 3 的 trace-distance + ε-参数对接看似 trivial，但：
- ε-secure 定义里 **ω_E** 不是固定的，是协议输出的；trust 改变后输出变了
- Bob 在 Π' 中"模拟" Charlie 的能力依赖于他能**拷贝**所有经典 broadcast — 经典广播本来就公开，可以；但 Charlie 的 quantum register 在 Π 中 Bob 拿不到，Π' 中拿到，**这一步增加了 Bob 的能力**，所以 K_ε(Π') ≥ K_ε(Π) 成立

每一步都需要**对照 KW Def 20.1 + WTB §3 的精确定义形式化**，不能靠直觉滑过。

---

## 5. 完整论证骨架

```
[Step 1] umr 协议 Π，K_ε(Π) = R
   ↓ 应用 Lemma γ.4.5 (trust expansion)
[Step 2] K_ε(Π') ≥ R  where Π' has Charlie trusted

   ↓ 在 Π' 中，E2 + Charlie 现在是 Bob 内部资源
   ↓ Π' 是 Alice → B-tot 的 SKA over single channel E1
   ↓ B-tot 内部有任意 local resource（包括 internal noisy channel E2）

[Step 3] 应用 PLOB Theorem 1 / WTB Theorem 12 / KW Theorem 20.20
   on E1 (Alice → B-tot) as a single point-to-point SKA setup

[Step 4] K_ε(Π') ≤ E_R(E1) = -log₂(1-η_A)  [pure-loss bosonic, PLOB Eq. 19]

[结论] R ≤ -log₂(1-η_A)
```

---

## 6. 待用户填写的事项清单（精度核对）

### 6.1 核对 PDF 编号（防止 [RECALLED] 漂移）

- [ ] PLOB 2017 Theorem 1 / Theorem 5 / Eq. (19) — 页码 + 编号是否与 cheat sheet §1 一致
- [ ] WTB 2017 Theorem 11 / Theorem 12 / Theorem 13 / Eq. (4.4) — 页码 + 编号是否一致
- [ ] Khatri-Wilde 2020 Theorem 20.20 / Proposition 20.4 / Corollary 20.5 — 页码 + 编号是否一致

### 6.2 形式化 Lemma γ.4.5

- [ ] Step 3（trace-distance monotonicity）的精确 ε 计算
- [ ] Step 4（Π' 中 Bob 模拟 Π 的 Bob+Charlie）的协议构造细节
- [ ] 与 WTB §3 / KW §20.1 的 ε-secure 定义一致性

### 6.3 选择 Theorem 12 还是 Theorem 13

- **Theorem 12**：tele-simulable channels — pure-loss bosonic 是 tele-covariant ⟹ tele-simulable，**适用** ✅
- **Theorem 13**：any channel — 适用但 bound 不如 Theorem 12 紧
- **建议用 Theorem 12**（KW Theorem 20.20 是教科书版本）

### 6.4 R0.2 升级路径

满足 C1 (a/b/c) ∧ C2 ∧ C3 后可升 [THM]：
- **C1 (a)** 跨家族 PDF 直读：用户 + 一位人类同行（或 GPT-5 reading PDF directly），双方独立写出 Lemma γ.4.5 证明
- **C1 (b)** 用户纸笔复核 — 推荐
- **C1 (c)** SymPy 形式化（trace-distance + ε 算术）— 可补充
- **C2** 用户对升级 [THM] 签字
- **C3** 我跑 dev-reviewer 双 Codex 评审 cheat sheet → Lemma γ.4.5 → 主命题

---

## 7. 与 path α / β 的关系

| 路径 | 上界 | 假设强度 | 工作量 |
|---|---|---|---|
| **α** (monotonicity to Pirandola 2019) | min(E_R(E1), E_R(E2)) | 需要 Pirandola network theorem 的 trust-expansion + 三 lemma | 中 |
| **β** (effective channel + WTB direct) | 数值 SDP（潜在更紧）| 需要 Charlie BSM 形式化为 effective channel | 大（β.G4/β.G5 受阻）|
| **γ §4.5** (single-channel PLOB on E1) | E_R(E1) = -log₂(1-η_A) | 仅需 trust-expansion + 单点 PLOB | **小**（仅一个 lemma + 直接套定理）|

**γ §4.5 的劣势**：在对称 η_A=η_B=√η_AB 下，给出的 bound 是 -log(1-√η_AB)，**与 α 给出的 Pirandola min-cut bound 在数值上相同**。但**论证路径短得多**，不依赖 Pirandola 2019 的网络 stretching。

---

## 8. AI 已确认 / 用户验证（per R0.1 留痕）

**AI confirmed via direct PDF reading (2026-04-25 session)**：
- ✅ PLOB Eq. (19) `K(η) = -log₂(1-η)` for lossy channel — `PLOB-2017` p.7
- ✅ WTB Theorem 11/12/13 + Eq. (4.4) LOCC monotonicity — `WTB-2017` p.15-23
- ✅ Khatri-Wilde Theorem 20.20 / Proposition 20.4 / Corollary 20.5 — `KhatriWilde-2020` p.1180-1191
- ✅ WTB §2.3 LOPC framework with Eve 收 classical broadcast copies — `WTB-2017` p.7-8

**仍需用户验证**：
- ⏳ Lemma γ.4.5 形式化（**Step 1-4 精确写出**）
- ⏳ ε-参数对接（umr-Eve 与 trust-Eve 的 ε 是否相同）
- ⏳ 升级到 [THM] 的 R0.2 C1+C2+C3 闸门

---

## Changelog

- **v0.1** (2026-04-25): 首版。基于 AI 直读 PLOB / WTB / KW Ch20 的精确章节定位，给出 path γ §4.5 的论证骨架 + 用户待办清单。**所有理论陈述保持 [CONJ-DRAFT]，待用户 PDF 复核 + 形式化 + R0.2 升级**。
