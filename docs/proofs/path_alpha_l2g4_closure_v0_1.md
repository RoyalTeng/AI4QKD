# Path α Lemma B sub-gap L2.G4 — Closure Candidate v0.1

**Sub-gap**：L2.G4 — non-LOCC joint attack (Eve 不限于 LOCC 的最一般攻击) covered by Cui 2019 collective + asymptotic coherent extension

**版本**：v0.1
**日期**：2026-04-26
**C1 path used**：**C1(a)** 跨家族 AI 直读 Cui 2019 Eq. (1) + Section III
**严谨性 banner**：[COROLLARY] — C1(a) ✅ / C2 ✅ (2026-05-01 user batch sign-off) / C3 ✅

---

## §-1 R0.2 升级闸门状态

| 闸门 | 状态 |
|---|---|
| **C1(a)** 跨家族 AI 直读 Cui 2019 PDF | ✅ **PASS** at Codex round 2 |
| **C1(c)** non-AI 数值 | 不适用 |
| **C1** aggregate | ✅ **PASS** via C1(a) |
| **C2** 用户审签 | ⏳ 待 |
| **C3** dev-reviewer 双 Codex 评审 | ⏳ 待 batch |

---

## §1 Sub-gap statement

### 1.1 Lemma L2.G4 statement

**Lemma L2.G4 (asymptotic-coherent attack covered by Cui 2019)**：

设 $\Pi$ 是 Cui 2019 simplified TFQKD 协议（per [docs/proofs/umr_path_alpha_lemma_skeletons_v0_1.md](umr_path_alpha_lemma_skeletons_v0_1.md) §1）。则 Π 的安全性分析 Cui 2019 已 cover 以下 Eve 攻击范围：

- (a) **任意 most general collective attack**：per Cui Eq. (1)，Eve 选 arbitrary unitary $\hat{U}$ + measurement on classical message register；Eve ancilla space 任意 dim
- (b) **asymptotic coherent attack**：per Cui Section III page 3 文本，"results in Refs. [25] and [26]"（即 Renner de Finetti + postselection technique）guarantee security against coherent attacks **asymptotically**

**严格 scope of L2.G4 closure**：本 lemma 仅 confirm (a) + (b) 是 Cui 2019 已建立的 conclusion；**不**推 finite-key coherent attack security（属 GEAT / Kamin 2025 / Metger 2024 framework 工作，**显式标注 out-of-scope**）。

### 1.2 Lemma 在 path α Lemma B 中的位置

Path α Lemma B 主张 Π 安全性向 ι(Π) 的继承。Π 自身的安全性来源是 Cui 2019 Section III + Appendix A 的 Devetak-Winter rate analysis + de Finetti 推 coherent。L2.G4 是这一来源的 textual confirmation —— path α Lemma B 不需自己 reprove Π 的 security，only invoke Cui 2019 conclusion。

### 1.3 严格 scope

- ✅ 本 lemma 是 **Cui 2019 conclusion textual confirmation**
- ❌ 本 lemma **不**主张 finite-key coherent attack security（out-of-scope per path α v0.3 §6 strict-scope statement "asymptotic（finite-key 不在 scope）"）
- ❌ 本 lemma **不**主张 Π_tr 继承 Π 的 security（依赖 L2.G3 / L1.G2 [UNKNOWN]）

---

## §2 引文（Citation accuracy 核对，pending Codex C1(a) round）

### 2.1 Cui 2019 Eq. (1) — most general collective attack

**Cui-Yin-Wang-Chen-Wang-Guo-Han 2019**, *Phys Rev Applied* 11:034053 (待 Codex 直读 confirm verbatim)：

PDF p.2 Section III "MAIN RESULTS OF SECURITY PROOF" 段：

> "Eve's most general collective attack to the above simplified TFQKD protocol can be defined as an arbitrary measurement after an arbitrary unitary operation operating on the whole system with her pre-prepared ancilla [4,5]. Under photon-number representation, this collective attack is given by..."

直接给 collective attack 的最一般 form Eq. (1)。

### 2.2 Cui 2019 Section III page 3 — asymptotic coherent extension

PDF p.3 Section III 段尾 (待 Codex 直读 confirm verbatim)：

> "results in Refs. [25] and [26]. Hence, our proof can guarantee security against the coherent attacks asymptotically. It also ends our security proof rigorously."

**含义**：Cui 用 quantum de Finetti（Ref. [25] = Caves-Fuchs-Schack 2002）+ postselection technique（Ref. [26] = Christandl-Koenig-Renner 2009）把 collective attack security extend 到 asymptotic coherent attack。**注意**：仅 asymptotic regime（n → ∞），finite-key 需 finite-key technique（Kamin 2025 / Metger 2024 GEAT）—— **不在本 lemma scope**。

### 2.3 与 path α Lemma A/B 的关系

L2.G4 仅 confirm Π 自身已对 (a) collective + (b) asymptotic coherent 安全。**不**直接推 Π_tr 继承（那是 path α Lemma B 主结论，依赖 L2.G3 / L1.G2 [UNKNOWN]）。L2.G4 的作用是提供 **Π 的 security 来源 textual citation**，使 Lemma B 可以 invoke "Π is ε-secure" 而**不需要** path α 内重做 Π 的 security 分析。

---

## §3 数学陈述 / 推导

L2.G4 是**纯 citation closure**，无独立数学推导。Cui 2019 Section III + Appendix A 给完整 security proof against (a) + (b)；本 closure 仅 verify 这一文本 fact。

---

## §4 待启动的 C1(a) Codex round

让 Codex 直读 [Cui 2019 PDF](../literature/pdfs/Cui%20等%20-%202019%20-%20Twin-Field%20Quantum%20Key%20Distribution%20without%20Phase%20.pdf) Section III + Eq. (1) verify：

1. PDF p.2 Eq. (1) 给 collective attack form
2. PDF p.3 Section III 段尾 "Hence, our proof can guarantee security against the coherent attacks asymptotically" 文本存在
3. Cui Ref. [25] = Caves-Fuchs-Schack 2002 quantum de Finetti；Ref. [26] = Christandl-Koenig-Renner 2009 postselection
4. **CRITICAL**: Cui Section III + Appendix A 仅推 asymptotic coherent，未推 finite-key（path α v0.3 §6 strict scope 已 explicit 排除 finite-key）
5. Lemma scope clean：不 smuggle finite-key claim, 不 smuggle Π_tr inheritance

**预期 verdict**：PASS（pure citation confirmation）

---

## §5 Changelog

- **v0.1** (2026-04-26)：首版 closure candidate。基于 Cui 2019 Eq. (1) + Section III page 3 asymptotic coherent extension via Refs. [25] [26]。L2.G4 是 pure citation closure；finite-key 显式 out-of-scope。C1(a) Codex round 待启动。C1(c) 不适用。C2 / C3 待。
- **v0.2** (2026-04-26 same-day)：Codex round 1 verdict = FAIL only on Ref. [25] mis-attributed (Renner 2008 → Caves-Fuchs-Schack 2002 quantum de Finetti)。其余 4 项 PASS。仅修 §2.2 + §4 引文 attribution。
- **v0.2 final** (2026-04-26 same-day)：**C1(a) Codex round 2 verdict = PASS**。Refs [25][26] attribution 已 verified accurate。**L2.G4 C1 aggregate PASS via C1(a)**。C2 / C3 待。
