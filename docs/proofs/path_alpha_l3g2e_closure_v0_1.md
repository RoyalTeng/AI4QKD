# Path α Lemma C sub-gap L3.G2.E — Closure Candidate v0.1

**Sub-gap**：L3.G2.E — Channel-use counting normalization alignment（信道使用次数计数对齐）

> Cui 2019 Eq. (3) 给的密钥率 $R = Q_\mu[1 - fh(e_\mu, 1-e_\mu) - I^u_{AE}]$ 是 **per-trial**（每次试验）；Pirandola 2019 chain protocol 的 secret-key rate 是 **per-network-use**（每次网络使用）。L3.G2.E close 的是这两个分母的 alignment。

**版本**：v0.1
**日期**：2026-04-26
**前身 / 立项依据**：[c3-dev-reviewer-batch-holistic-1.md](../workflow/umr-path-alpha-three-lemma-v0-2/c3-dev-reviewer-batch-holistic-1.md) §1 + [RETRACTION.md §9.4](../research/RETRACTION.md#94-holistic-fail--lemma-c-countingnormalization-residual) — holistic reviewer Round 1 揭露 L3.G2 closure（在 user Option B 下 close Devetak-Winter ↔ ε-private state bridge）**未** 吸收 lemma_skeletons §157 原 statement target C 中"channel use 计数对齐"的部分；该部分 split 为新 sub-gap L3.G2.E

**C1 path used**：**C1(a)** 跨家族 AI 直读 Cui 2019 Section III + Pirandola 2019 SI Note 1/2
**严谨性 banner**：[SYN candidate-for-COROLLARY-pending-C1(a) Codex citation verify ∧ C2 user signature]

---

## §-1 R0.2 升级闸门状态

| 闸门 | 状态 |
|---|---|
| **C1(a)** 跨家族 AI 直读 Cui 2019 + Pirandola 2019 PDFs | ✅ **PASS at Codex round 3**（R1 FAIL 3 issues → v0.2 patch；R2 FAIL only on D propagation → v0.3 patch；R3 PASS）|
| **C1(c)** non-AI 数值 | 不适用（结构性 / 计数对齐 lemma，无数值 question）|
| **C1** aggregate | ✅ **PASS** via C1(a) |
| **C2** 用户审签 | ⏳ 待 |
| **C3** dev-reviewer 双 Codex 评审 | ⏳ 待 batch（与 L1.G4 v0.2 + L3.G2 v0.5 一起 R2 batch）|

---

## §1 Sub-gap statement

### 1.1 立项背景

[lemma_skeletons §157](umr_path_alpha_lemma_skeletons_v0_1.md) 原 Lemma C statement target 写：

> 在 channel use 计数对齐 + 同 ε-secure criterion 下，$R_{Cui}(\Pi) \leq R_{Pirandola}(\Pi_{tr})$

L3.G2 closure（v0.3 final，[path_alpha_l3g2_closure_v0_1.md](path_alpha_l3g2_closure_v0_1.md)）在 user Option B（implicit Devetak-Winter bridge）下 close 了**后者** —— Cui per-trial Devetak-Winter rate 与 Portmann-Renner ε-close-to-private-state criterion 之间的 standard QC IT bridge。

**未 close 部分**：**前者 channel-use counting 对齐** —— Cui per-trial accounting 与 Pirandola per-network-use accounting 之间的 normalization 是否 well-defined 等同。

C3 dev-reviewer Round 1 holistic 评审揭露这一 hidden residual；本 closure 立项为 **L3.G2.E**（Lemma C 第 2 号 sub-gap 的 Extension），独立于 L3.G2 走 C1+C2+C3 验证。

### 1.2 Lemma L3.G2.E statement

**Lemma L3.G2.E (Channel-use counting normalization alignment)**：

设：
- $\Pi$ = Cui 2019 simplified TFQKD protocol（path α 的 anchor 协议）
- $R_{Cui}(\Pi)$ = Cui 2019 Eq. (3) 给的 **per-trial** secret key rate（即 1 trial → 1 unit of $R_{Cui}$）
- $\iota(\Pi) = \Pi_{tr}$ = ι 嵌入后的 trusted-relay 协议（Pirandola SI Note 1 chain protocol class 成员）
- $R_{Pirandola}(\Pi_{tr})$ = Pirandola 2019 chain protocol 框架下 $\Pi_{tr}$ 的 **per-network-use** secret-key rate

**Lemma**：在自然 identification "1 Cui trial = 1 Pirandola N=1 chain end-to-end network use" 下，

$$R_{Cui}(\Pi) \;\text{(per Cui trial)} \;\equiv\; R_{Pirandola}(\Pi_{tr}) \;\text{(per Pirandola network use)}$$

即两者的分母（counting unit）well-defined 等同，比较 $R_{Cui}(\Pi) \leq R_{Pirandola}(\Pi_{tr})$ 的 inequality 在 unit-level 一致。

### 1.3 严格 scope

- ✅ 本 lemma 仅 close **counting unit** 等同性（每个 Cui 试验对应一个 Pirandola 网络使用）
- ❌ 本 lemma **不**主张 $R_{Cui}(\Pi) \leq R_{Pirandola}(\Pi_{tr})$ 这一 inequality 本身（依赖 Lemma C 整体）
- ❌ 本 lemma **不**主张 ε-criterion 等同性（依赖 L3.G2 user Option B）
- ❌ 本 lemma **不**主张 LOPC syntax compatibility（依赖 L3.G1，已 PASS）
- ❌ 本 lemma **不**主张 Pirandola Eq. 11 specialization 到 $-\log_2(1-\sqrt{\eta_{AB}})$（依赖 post-split L3.G3 剩余 5 个 sub-residual；原 L3.G3 第 4 项已 split out 为本 L3.G2.E，详 §2.4）
- ❌ 本 lemma **不**主张 Π / Π_tr 任一具体安全性 conclusion（依赖 Lemma A + B）

---

## §2 引文（Citation accuracy 核对，pending Codex C1(a) round）

### 2.1 Cui 2019 — per-trial accounting

**Cui-Yin-Wang-Chen-Wang-Guo-Han 2019**, *Phys Rev Applied* 11:034053（[PDF](../literature/pdfs/Cui%20等%20-%202019%20-%20Twin-Field%20Quantum%20Key%20Distribution%20without%20Phase%20.pdf)，per L2.G4 + L3.G2 round verify PASS for verbatim Section III + Eq. (1)/(3)）：

#### 2.1.a Cui Eq. (3) verbatim — per-trial 标注

per [c1a-l3g2-citation-verify-round2.md](../workflow/umr-path-alpha-three-lemma-v0-2/c1a-l3g2-citation-verify-round2.md) Codex direct PDF read confirmed verbatim：

> "According to Devetak-Winter's bound [24], the secret key rate **per trial in a code mode** is then given by $R = Q_\mu [1 - fh(e_\mu, 1-e_\mu) - I^u_{AE}]$"

**关键 verbatim**："**per trial in a code mode**" —— Cui 显式 stating R 的分母是 trial。

#### 2.1.b Cui Step 2 + Step 3 — 1 trial 的物理操作（v0.2 修正：分别 verbatim，不 stitch）

per Section II Step 2.a + Step 3（PDF p.2，[c1a-l3g2e-citation-verify.md](../workflow/umr-path-alpha-three-lemma-v0-2/c1a-l3g2e-citation-verify.md) §A Codex direct PDF read confirmed）：

**Step 2.a verbatim**：

> "If code mode is selected, Alice (Bob) ... sends ..."

**Step 3 verbatim**：

> "For each trial, the middle receiver Eve must publicly announce a successful message $|1\rangle_M$ or a failure message $|0\rangle_M$ to Alice and Bob. ..."

**v0.1 → v0.2 fix**：v0.1 误把 Step 2.a 与 Step 3 两句话 stitch 成一句假 verbatim "For each trial, ... Alice (Bob) sends ..."（[Codex round 1 finding](../workflow/umr-path-alpha-three-lemma-v0-2/c1a-l3g2e-citation-verify.md) §A）。v0.2 拆开两句各自原话 verbatim。

**inference**（不再标 verbatim）：综合 Step 2.a "If code mode is selected, Alice (Bob) ... sends ..." + Step 3 "For each trial, the middle receiver Eve must publicly announce ..."，每次 Cui trial 物理上消耗 1 次 Alice→Charlie 传输 + 1 次 Bob→Charlie 传输 + Charlie 接收处理 + announcement 经典广播。

### 2.2 Pirandola 2019 SI Note 1/2 — per-network-use accounting

**Pirandola-Laurenza-Ottaviani-Banchi 2019**, *Nat Commun* 10:1006（[PDF](../literature/pdfs/Pirandola-2019-EndToEndCapacities.pdf)）：

#### 2.2.a SI Note 1 page 15 chain protocol class

per [L1.G1 closure](path_alpha_l1g1_closure_v0_1.md) §2.2 Codex round 2 verify PASS verbatim：

> "The most general distribution protocol over the chain is based on adaptive LOs and unlimited two-way CC involving all the points in the chain"

#### 2.2.b SI Note 2 — memoryless edge channel

per [L1.G2 closure](path_alpha_l1g2_closure_v0_1.md) §2.2 + [c1a-l1g2-citation-verify.md](../workflow/umr-path-alpha-three-lemma-v0-2/c1a-l1g2-citation-verify.md) item 2 (b) Codex direct PDF read：

> SI Note 2 "memoryless quantum channels" —— edges connect points by memoryless channels；每次"network use"消耗一次每条 edge use 的 budget

#### 2.2.c Pirandola n-channel-use rate accounting（Methods + SI Note 1）

per Methods Eq. (35)-(41) + SI Note 1 Eq. (91)-(92)（[L3.G2 closure](path_alpha_l3g2_closure_v0_1.md) v0.3 final + [c1a-l3g3-gap-identification-round1.md](../workflow/umr-path-alpha-three-lemma-v0-2/c1a-l3g3-gap-identification-round1.md) §B item "asymptotic regime" Codex direct read）：

> "Capacities are weak-converse asymptotic limits n→∞, ε→0"

Pirandola 框架下 secret-key rate 的分母是 **n channel uses for an end-to-end network use**；具体到 N=1 chain (A-Charlie-B)，1 个 end-to-end network use 消耗 1 次 A-Charlie edge use + 1 次 Charlie-B edge use（per SI Note 1 Eq. 91-92 + Note 2 memoryless edge model）。

### 2.3 Identification: 1 Cui trial = 1 Pirandola N=1 chain end-to-end use（v0.2 修正：边使用是 denominator unit；本地操作 + 经典通信是 admissible structure 但非 denominator metering）

**v0.1 → v0.2 fix**：v0.1 §2.3 表把 4 项资源消耗都标"1 次"作 counting unit。但 [Codex round 1 §C](../workflow/umr-path-alpha-three-lemma-v0-2/c1a-l3g2e-citation-verify.md) 直读 Pirandola PDF 揭露：Pirandola 框架里 secret-key rate 的**分母**只算 **edge use**（per "all the channels are used exactly once" main p.2 + SI Note 1 "bits per chain use"），**不**单独 metering "1 local op" 或 "1 CC use"。后两项是 admissible structural ingredients 但不算 counting unit。v0.2 修正为：

**对照**（v0.2 修正后）：

| 资源消耗 | Cui 1 trial | Pirandola N=1 chain 1 end-to-end use | 是 denominator unit？ |
|---|---|---|---|
| Alice→Charlie transmission（A-C edge use） | ✅ 1 次 | ✅ 1 次 | ✅ **是**（Pirandola 主分母）|
| Bob→Charlie transmission（B-C edge use） | ✅ 1 次 | ✅ 1 次 | ✅ **是**（Pirandola 主分母）|
| Charlie measurement + announcement step | ✅ 1 次（Cui Step 3）| ✅ 内部 LOCC 步骤（per Pirandola SI Note 1 "adaptive LOs"）| ⚠️ **不**算独立 denominator unit（admissible structure but not metered）|
| classical announcement broadcast | ✅ 1 次（Cui Step 3）| ✅ 内部 two-way CC 步骤 | ⚠️ **不**算独立 denominator unit（unlimited two-way CC, not metered）|

**v0.2 修正后的等同性**（仅就 denominator unit 而言）：

- **Pirandola 框架的 N=1 chain "1 end-to-end use" denominator** = 1 次 A-C edge use + 1 次 B-C edge use（per Pirandola main p.2 verbatim "all the channels are used exactly once" + SI Note 1 "bits per chain use"）
- **Cui 框架的 "1 trial" denominator** = 1 次 A→Charlie 传输 + 1 次 B→Charlie 传输（per Cui Step 2.a "Alice (Bob) ... sends ..."）
- 两者**主 denominator unit（edge use 数）一致**：1 次 trial = 2 次 edge uses = 1 次 Pirandola N=1 chain end-to-end use

**counting unit alignment**：

$$\frac{R_{Cui}(\Pi)}{1 \text{ Cui trial} = 2 \text{ edge uses}} \;\stackrel{\text{trial-to-network-use 等同}}{\equiv}\; \frac{R_{Pirandola}(\Pi_{tr})}{1 \text{ Pirandola N=1 network use} = 2 \text{ edge uses}}$$

即两者在 per-edge-use 意义下分母 well-defined 等同（local op + CC 是两侧均允许的 admissible structure，对 denominator metering 无独立贡献）。

### 2.4 与 L3.G3 sub-residual 4 的关系（v0.2 修正：L3.G2.E **就是** L3.G3 sub-residual 4 的 split-out，不是 precondition）

**v0.1 → v0.2 fix**：v0.1 §2.4 把 L3.G2.E 描述成 L3.G3 sub-residual 4 的"前置"（precondition），但 [Codex round 1 §D](../workflow/umr-path-alpha-three-lemma-v0-2/c1a-l3g2e-citation-verify.md) 揭露这是 misclassification：[L3.G3 gap-id round](../workflow/umr-path-alpha-three-lemma-v0-2/c1a-l3g3-gap-identification-round1.md) §D 第 4 项的原话是 "Channel-use accounting gap: an explicit argument is still needed that one Cui trial is one Pirandola chain use / single-path network use ... about operational counting only"，**就是** L3.G2.E 处理的同一个问题。v0.2 修正定位。

**v0.2 修正后的边界**：

- **L3.G2.E**（本 lemma）= **L3.G3 第 4 项 sub-residual 的 split-out**：从 L3.G3 inventory 中拆出 "channel-use accounting" 这一项，独立立项作 Lemma C 的 sub-gap (L3.G2.E)
- **拆分理由**：
  - L3.G3 其余 5 项（citation specialization / parameter id / symmetry / protocol-model / edge-model）涉及 Pirandola Eq. 11 specialization 到 `-log_2(1-√η_{AB})` 的具体过程，**深度结构性 / operational-link**（per memory feedback `feedback_ai_draft_structural_gaps`，AI 不得 close）
  - L3.G3 第 4 项（counting alignment）相对**独立**：是 abstract resource counting 论证，不依赖 specific η-form specialization；**AI 可 draft closure**（不属于 cross-task / cross-space / operational-link 范畴）
  - 拆分后：L3.G2.E 走 AI closure 路径；L3.G3 减员到 5 项 sub-residual，全部维持 user-level OPEN

**post-split inventory** of L3.G3：

L3.G3 拆分后剩余 5 项 sub-residual（v0.1 列的第 4 项已 split out 为 L3.G2.E）：
1. ~~Citation gap~~（保留为 L3.G3 第 1 项）
2. ~~Parameter-identification gap~~（保留为 L3.G3 第 2 项）
3. ~~Symmetry / equidistance gap~~（保留为 L3.G3 第 3 项）
4. ~~Channel-use accounting gap~~ → **split out 为 L3.G2.E**
5. ~~Protocol-model gap~~（重新编号为 L3.G3 第 4 项）
6. ~~Edge-model gap~~（重新编号为 L3.G3 第 5 项）

post-split L3.G3 = 5 项 sub-residual，全部 user-level OPEN（AI 不 draft closure）。

**逻辑关系**：

- L3.G2.E close 后，Cui R 与 Pirandola R 比较 well-defined（即 Lemma C inequality target 有意义）
- post-split L3.G3 (5 项) close 后，才能从 Pirandola R 的 generic form 推到 specific `-log_2(1-√η_{AB})` 形式

两者顺序：L3.G2.E（counting）→ post-split L3.G3 第 1 项（generic UB → specific η-form 的 specialization chain），L3.G2.E 是 prerequisite step in this chain，但**不**等同 L3.G3 整体；L3.G2.E 自身**就是**原 L3.G3 sub-residual 4。

---

## §3 数学陈述 / 推导

### §3.1 Cui per-trial accounting（per §2.1 verbatim）

由 Cui Eq. (3) verbatim "secret key rate **per trial** in a code mode"，$R_{Cui}(\Pi)$ 的 denominator 是 1 trial。1 trial 物理上是 1 个 A→Charlie + 1 个 B→Charlie 传输 + Charlie announcement（Cui Step 2-3）。

### §3.2 Pirandola per-network-use accounting（per §2.2 verbatim）

由 Pirandola Methods + SI Note 1 verbatim "n→∞ asymptotic limit" 配 SI Note 1 chain protocol class definition，$R_{Pirandola}(\Pi_{tr})$ 的 denominator 是 1 end-to-end network use。N=1 chain (A-Charlie-B) 的 1 end-to-end use 物理上是 1 个 A→Charlie edge use + 1 个 Charlie→B edge use（or 反向）+ Charlie local op + two-way CC。

### §3.3 Identification 推论

由 §3.1 + §3.2 + §2.3 表的 4 项 resource consumption 一一对应：

$$\boxed{1 \text{ Cui trial} \;\equiv\; 1 \text{ Pirandola N=1 chain end-to-end use}}$$

在此 identification 下，rate inequality $R_{Cui}(\Pi) \leq R_{Pirandola}(\Pi_{tr})$ 的两侧 denominator 等同，比较 well-defined。

### §3.4 严格 scope reaffirm

本 §3 仅 verify counting unit 等同性。**不**主张：

- inequality $R_{Cui}(\Pi) \leq R_{Pirandola}(\Pi_{tr})$ 本身成立（那是 Lemma C 整体在所有 sub-gap close 后的 conclusion）
- ε criterion 等同（L3.G2 user Option B）
- specific η-form specialization（post-split L3.G3 剩余 5 项，特别是 citation gap + parameter-id + symmetry；本 L3.G2.E 即从原 L3.G3 第 4 项 channel-use accounting split out）

---

## §4 待启动的 C1(a) Codex round

让 Codex 直读：

1. Cui 2019 PDF Section III page 2 Eq. (3) verbatim，**特别 verify "per trial in a code mode" 字样**
2. Cui 2019 PDF Section II Step 2-3 page 2 verbatim "For each trial, Alice (Bob) sends..."
3. Pirandola 2019 PDF SI Note 1 page 15 chain protocol class + SI Note 2 memoryless channel
4. Pirandola 2019 PDF Methods + SI Note 1 Eq. (91)-(92) "n channel uses asymptotic limit"
5. **CRITICAL Codex check**：
   - §2.3 表的 4 项 resource consumption 一一对应是否 valid（不 smuggle 额外 step）
   - §2.4 L3.G2.E 与 L3.G3 sub-residual 4 的边界划分是否清晰（不 smuggle L3.G3 closure）
   - §1.3 严格 scope 5 项 disclaim 是否 throughout §3 honored
   - **scope cleanliness**：本 closure 仅 close counting unit alignment，不 smuggle Lemma A / Lemma B / L3.G1 / L3.G2 / L3.G3 任何 closure

**预期 verdict**：PASS（counting unit alignment 是 abstract resource counting 论证；citation 全部已在前几轮 PASS 引用过，本 closure 仅做 specific identification 步骤）

---

## §5 Changelog

- **v0.1** (2026-04-26)：首版立项 closure。基于 [holistic R1 finding](../workflow/umr-path-alpha-three-lemma-v0-2/c3-dev-reviewer-batch-holistic-1.md) §1 + [RETRACTION.md §9.4](../research/RETRACTION.md#94-holistic-fail--lemma-c-countingnormalization-residual)。L3.G2.E 立项作 Lemma C 第 2 号 sub-gap 的 Extension。C1(a) Codex round 待启动。C1(c) 不适用。C2 / C3 R2 待。
- **v0.2** (2026-04-26 same-day, C1(a) round 1 patch)：**C1(a) Codex round 1 verdict = FAIL** ([review](../workflow/umr-path-alpha-three-lemma-v0-2/c1a-l3g2e-citation-verify.md))，三处具体问题：(A) §2.1.b Cui Step 2-3 引文是 stitched 假 verbatim，非 PDF 原话；(C) §2.3 表后两行（local op + CC）不是 Pirandola denominator metering unit 而仅是 admissible structure；(D) §2.4 把 L3.G2.E 错描述成 L3.G3 sub-residual 4 的 precondition，实际**就是** sub-residual 4 的 split-out。修复策略：(A) §2.1.b 拆 Step 2.a + Step 3 各自原话 verbatim，注明 inference 部分非 verbatim；(C) §2.3 表加"是 denominator unit？"列，前两行 ✅ 后两行 ⚠️ admissible-but-not-metered，主 alignment 改为 per-edge-use；(D) §2.4 改为"L3.G2.E **就是** L3.G3 sub-residual 4 split-out"，post-split L3.G3 减到 5 项 sub-residual。
- **v0.3** (2026-04-26 same-day, C1(a) round 2 propagation patch)：**C1(a) Codex round 2 verdict = FAIL only on D propagation** ([review](../workflow/umr-path-alpha-three-lemma-v0-2/c1a-l3g2e-citation-verify-round2.md))。A + C 已 PASS；D 修了 §2.4 但**未** propagate 到 §1.3 line 64 + §3.4 line 205 的 stale references "L3.G3 6 个 sub-residual" + "L3.G3 sub-residual 4"。修：§1.3 改"post-split L3.G3 剩余 5 个 sub-residual"，§3.4 改"post-split L3.G3 剩余 5 项..."。
- **v0.3 final** (2026-04-26 same-day)：**C1(a) Codex round 3 verdict = PASS** ([review](../workflow/umr-path-alpha-three-lemma-v0-2/c1a-l3g2e-citation-verify-round3.md))。Stale references 已 propagate；§2.4 split-out framing 维持；无 scope drift。**L3.G2.E C1 aggregate PASS via C1(a)**。C2 / C3 R2（与 L1.G4 v0.2 + L3.G2 v0.5 一起 batch）待。
