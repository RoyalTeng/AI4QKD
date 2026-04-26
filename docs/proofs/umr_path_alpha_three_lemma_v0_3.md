# Path α — Resource-Enhancement / Protocol-Class Inclusion (v0.3 — STATEMENT-STUB ONLY)

> **🟡 [USER-APPROVED PRIORITY 2026-04-25 — direction-level approval, NOT C3-passed]**
>
> **状态**：user 2026-04-25 显式 override §7.3 rollback condition；path α 作为 Phase 2 优先方向**继续**。
>
> **审计留痕（不可删除）**：
> - **Round 1 (v0.2)**: REJECTED + UNSOUND（7 traps）→ v0.2 永久 [REJECTED] banner，见 [v0.2](umr_path_alpha_three_lemma_v0_2.md)
> - **Round 2 (v0.3 本文件)**: REJECTED (diff 1 major + 1 minor) + FAIL (holistic 3 majors) → 6/7 traps 已修，剩余 5 cleanup issues 在 v0.3 内修补（见 §6.4）
> - **§7.3 rollback override (2026-04-25 同 session)**: user 原话 "如果和红线违背，那就以我的 approve 为准 ... 我已经经过反复论证了，我的 approve 没问题"
>
> **user override scope**（继承自原 §-1.4 directive boundary）：
> - ✅ approve **path α direction** 作 Phase 2 优先策略
> - ✅ approve v0.3 维持 active draft 在 repo 不撤
> - ❌ **不**等价于 dev-reviewer C3 PASS（C3 verdict 仍是 REJECTED 留痕）
> - ❌ **不**等价于 [SYN] → [COROLLARY] 升级（**R0.2 三闸门未走完**）
> - ❌ **不**得在对外论文 / 展示稿引用 v0.3 任何 lemma 表述、综合链或数值断言为定理级
>
> **R0.2 硬红线维持不变**：升级到 [COROLLARY] / [THM] 仍需 C1 ∧ C2 ∧ C3 完整流程，**user override 不替代 C3 dev-reviewer PASS**。
>
> **诚实提醒**：本 banner 是项目内**首次** user 在 spec 文档层 override Codex C3 verdict。先例风险参考 v1 retraction（user 当时也"反复论证过"）。本 override 仅适用于 cleanup-level issues + direction priority；**任何后续升级仍需重走 C3**。
>
> ---

**版本**：v0.3 [SPEC, DRAFT statement-stubs only — USER-APPROVED PRIORITY 2026-04-25, NOT C3-passed]
**日期**：2026-04-25
**前身**：
- supersedes [umr_path_alpha_three_lemma_v0_2.md](umr_path_alpha_three_lemma_v0_2.md) v0.2 [REJECTED 2026-04-25] (R0.2 红线 — 双 reviewer REJECTED + UNSOUND)
- 恢复与 [umr_path_alpha_scaffolding.md](umr_path_alpha_scaffolding.md) v0.1 (2026-04-22) **11-gap inventory** 一致
- supersedes [umr_path_delta_relaxed_trust_v0_1.md](umr_path_delta_relaxed_trust_v0_1.md) v0.1 [SUPERSEDED 2026-04-25]
**作者 / authority**：策略方向 = user directive 2026-04-25 ([PHASE_STATUS.md §4.5](../PHASE_STATUS.md))；本文件 framework = Claude (autonomous session)
**严谨性**：本文件 **[DRAFT statement-stub only]**。**不**含任何 proof / Justification sketch / 综合 closure。所有 Lemma 为**陈述目标**，所有 sub-gap **保持 [UNKNOWN]**。

---

## §-1 R0.1 / R0.2 显式状态声明（**必读 — v0.3 加固版**）

### -1.1 v0.2 [REJECTED] 教训显式承接

**第 6 次 trap memory**（2026-04-25 实例，本次 session 内）：v0.2 在 statement-only spec 文档里 smuggling closure，触发双 Codex REJECTED + UNSOUND。具体 7 条 trap 模式（v0.3 必须避免）：

| v0.2 失败模式 | v0.3 修正 |
|---|---|
| (1) Lemma A/B/C 后写 "Justification sketch" 实为 draft proof | **完全删除** Justification sketch；只留 Statement target |
| (2) §3 综合包含链写无条件 [SYN] 断言 | 改为**条件句**："If L1 ∧ L2 ∧ L3 ∧ all 11 sub-gaps were independently established, the strategy would imply ..."（明示**未独立证立**） |
| (3) §3.1 数值 "confirming" / "数值 confirm" | 改为 "**is consistent with this finite grid**"，无 scaling-tightness claim |
| (4) §6.1 "不修改 FINDINGS" 与本次 commit 修改 §4.3 矛盾 | §6.1 显式列**已修改**：FINDINGS §4.3 + PHASE_STATUS §4.5 |
| (5) 11-gap inventory 压成 4-gap 无解释 | **完整恢复** 旧 scaffolding 11-gap inventory（§3） |
| (6) Day 5-9 "[COROLLARY] 候选" 时间表 | **删除全部**短期时间表；Sub-Q3 是 3-5 月级工作（per RESEARCH_PLAN §4） |
| (7) 反转 Log 07 优先级无 user 直读依据 | 优先级反转 user 依据**显式**记入 §-1.4（user 原话），且 v0.3 不主张"比 γ 更稳"，仅记录 user 时间约束下的 hedge 选择 |

### -1.2 本文件**不**做什么

- ❌ **不**声称已严格证明 Lemma L1 / L2 / L3 中任何一条
- ❌ **不**升级任何已有 [SYN] / [CONJ] 标签到 [COROLLARY] / [THM]
- ❌ **不**声称已 close path β/γ 的 4 个 main gap
- ❌ **不**声称已 close 旧 scaffolding 的 11 个 gap 中任何一个
- ❌ **不**给 lemma "Justification sketch"、"non-proof argument"、"sketch 草图" 等任何半推半留措辞
- ❌ **不**包含任何短期时间表（"Day N" / "X 天可闭合" 等）
- ❌ **不**主张 "path α 比 path γ 更稳" 等 reviewer-flagged 措辞

### -1.3 本文件**做**什么

- ✅ **statement-only** 列出 path α 三 lemma 陈述目标（**未** prove；user-directive 仅 approve 方向，**不** approve 任何 lemma 具体表述）
- ✅ **完整恢复**旧 [umr_path_alpha_scaffolding.md](umr_path_alpha_scaffolding.md) v0.1 的 11-gap inventory
- ✅ 显式标注每个 gap 仍为 [UNKNOWN]，且其 closeable 性**未**被本文件 assess
- ✅ 复用现有 [path_alpha_v0_2_alignment.csv](../research/data/path_alpha_v0_2_alignment.csv) 数值，**仅 reframe**，不做 scaling-tightness claim
- ✅ 与 v0.2 [REJECTED] / path δ [SUPERSEDED] / 旧 scaffolding [DRAFT] 关系明示
- ✅ 提供 user directive 2026-04-25 + 优先级反转理由 verbatim 引用

### -1.4 user directive 2026-04-25 verbatim 引用（per [PHASE_STATUS.md §4.5](../PHASE_STATUS.md)）

**directive scope**：
> 反转 Log 07 的 γ-first 优先级。path α 三 lemma 路径作 Phase 2 优先策略，优先于 path γ direct converse 与 path β 紧界 converse。

**user 优先级反转理由（原话）**：
> "我手头时间紧迫，γ 估计需要更长精读周期，先看 α 能否在更短周期出 scaling-级结论。"

**directive boundary**：
- approve **方向**与**优先级**
- approve **scaling 级目标**（不追求 prefactor-紧 UB）
- **不** approve 任何具体 Lemma 表述 / closure / Justification
- **不** approve 升级路径绕过 R0.2 (C1 ∧ C2 ∧ C3)

**回滚条件**：v0.3 dev-reviewer 再 REJECTED → directive 失效，回到 Log 07 的 γ-first 顺序。

### -1.5 本文件 trap 风险预警（v0.3 加固）

memory 记录"AI draft 不得推 structural gaps"。**本文件刻意不做 closure**，但 reviewer 仍应警惕以下风险点（diff reviewer round 2 必查）：

- **L1.G1 / L2.G3 trap**: 旧 scaffolding 已识别 "$\mathcal{A}_\text{umr}$ 与 $\mathcal{A}_\text{tr}$ 在不同 Hilbert 空间" 这是 path γ v0.2 retraction 的同型陷阱
- **L2.G1 trap**: rate-direction sign check —— v1 FINDINGS retraction 是因为 trusted-relay Pirandola Eq.11 应用方向写反
- **L3.G3 trap**: 综合链最后一步 inherits Pirandola 2019 Eq.11 在 ι(Π) 拓扑下的适用性 —— 这一步本身 inherits trust assumption，**没有自动绕开 β.G4** 等价问题
- **broadcast/transcript-side-info trap (v0.2 critical)**: Charlie broadcast 算 Eve 控制还是 transcript-side-info 必须显式 specify, 不能 partial trace 默认

**所有 11 sub-gap 在 v0.3 保持 [UNKNOWN]**。**不**做 AI draft 闭合。

---

## §1 策略陈述（statement-only — for the user-directed path α workstream）

### 1.1 目标 claim（**未证立**；v0.3 patch 2026-04-26 加 Pirandola Eq. 11 specialization chain caveat）

存在一个 claim C，**若**全部 sub-gap 独立证立 **AND** Pirandola 2019 Eq. 11 specialization chain 显式 verify，**则**推得：

$$\text{C}: \quad K_{\text{umr}}(\eta_A, \eta_B) \stackrel{\text{Lemma A+B+C [SYN, conditional]}}{\leq} K_{\text{trusted-chain}}(\eta_A, \eta_B) \stackrel{\text{Eq. 11 (REE cut UB) [THM]}}{\leq} \min_C E_R(C) \stackrel{\substack{\text{Eq. (8)/(9) specialization} \\ \text{+ tele-cov + sym η split [conditional]}}}{=} -\log_2(1 - \sqrt{\eta_A \eta_B})$$

**v0.3 patch (2026-04-26) note**：v0.3 原 form 把 Pirandola 第 11 号公式 silent 等同于最右边 `-log_2(1-√η_AB)` 的 single-repeater bound。**实际**第 11 号公式是 `C(N) ≤ min_C E_R(C)` (REE 切割上界，main paper p.4)；`-log_2(1-√η_AB)` 形式来自 Eq. (8)/(9) 的 lossy chain specialization (main p.3)，需要 (i) tele-covariance（pure-loss bosonic 边）+ (ii) distillability + (iii) symmetric / equidistant η split (`η_{AB} = η_A·η_B`)。详 [RETRACTION.md §9.3](../research/RETRACTION.md#93-l3g3-gap-id-round-揭露重大-pirandola-eq-11-citationspecialization-错误)。

**sub-gap inventory updated 2026-04-26**：原 11 sub-gap inventory **已扩展为 12 sub-gap**（newly opened **L3.G2.E** 从原 L3.G3 sub-residual 4 split-out；post-split L3.G3 = 5 sub-residual）。详 [path_alpha_subgap_closure_integration_v0_3.md](path_alpha_subgap_closure_integration_v0_3.md) §1（v0.2 已 [SUPERSEDED]）+ [lemma_skeletons §6](umr_path_alpha_lemma_skeletons_v0_1.md) v0.3 corrected combined chain。

**严谨性 [UNKNOWN]**：claim C 当前**未**证立。本文件**不**主张 C 已成立、近成立、或 likely 成立。本文件**仅**作为 user-directive 下三 lemma scaffolding 的 statement-stub 记录。**post-2026-04-26 C3 R2 batch 状态**：**9 个 sub-gap C1+C3 R2 PASS**（L1.G1, L1.G2, L1.G3, **L1.G4 v0.2 redo**, L2.G2, L2.G4, L3.G1, **L3.G2 v0.5 final**, **L3.G2.E v0.3 final**）；**1 个 sub-gap C1 PASS / C3 R3 待**（L2.G1 v0.3 patched，待 C3 R3 verify）；**2 个 sub-gap OPEN per R0.1**（L2.G3 cross-space + post-split L3.G3 5 项 user-level operational-link sub-residual）。详 [integration v0.3 §1](path_alpha_subgap_closure_integration_v0_3.md) 主状态矩阵。

### 1.2 与 path β/γ/δ 的关系（v0.3 加固 framing）

| path | 状态 | 关系 |
|---|---|---|
| path α v0.3 (本文件) | [DRAFT statement-stub] / 11 gaps [UNKNOWN] | user-directive 2026-04-25 当前优先方向 |
| path α v0.2 | [REJECTED 2026-04-25] | 教训记录；**不**作为 active strategy |
| path α scaffolding v0.1 | [DRAFT, 11-gap inventory] | 本文件**继承**其 gap inventory |
| path β (β.G4 / β.G5) | OPEN | **未替代**；user-directive 暂缓但**未关闭** |
| path γ (γ.B.G1 / γ.G3) | OPEN | **未替代**；user-directive 暂缓但**未关闭** |
| path δ v0.1 | [SUPERSEDED 2026-04-25] | capacity-monotonicity 路径与 path α 同型 cross-space gap，洞察迁移到 L2.G3 |

**v0.3 不主张** "path α 比 γ 更稳" / "结构上更优" / "绕开 cross-task transfer" 等 v0.2 reviewer-flagged 措辞。**仅**记录 user 时间约束下的 hedge 选择。

### 1.3 path α 是否真"绕开" cross-task transfer：未定（v0.3 显式承认 ambiguity）

v0.2 曾主张 "path α 不需 cross-task transfer，比 path γ 安全"。**reviewer 反驳**：path α 仍在做 cross-space transfer（不同 Hilbert 空间的 Eve 集合 / protocol class 比较），见 [scaffolding L1.G1 + L2.G3](umr_path_alpha_scaffolding.md)。

**v0.3 立场**：cross-task vs cross-space transfer 究竟孰更困难，**未**有定论；user-directive 选 α 仅基于时间约束 hedge。

---

## §2 三 Lemma — Statement Target ONLY

**重申**：本节**只列 statement target**。**不含** Justification sketch / 推导 / closure。每条 Lemma 当前为 **[DRAFT stub]**，全部 sub-gap **[UNKNOWN]**。

### 2.1 Lemma L1 — Protocol Embedding

**Statement target [DRAFT stub]**：

存在一个 protocol embedding $\iota: \mathbb{P}_{\text{umr}} \to \mathbb{P}_{\text{tr}}$，使得：

- **L1.a**：$\iota$ 是良定的（well-defined）
- **L1.b**：$\iota(\Pi)$ 在 trusted-relay 协议类内合法
- **L1.c**：embedding 保持 channel use / signal accounting

**严谨性 [UNKNOWN]**：L1 statement 本身的精确表述仍依赖 4 个 [UNKNOWN] sub-gap (L1.G1 - L1.G4) 的解决。

### 2.2 Lemma L2 — Security Reduction

**Statement target [DRAFT stub]**：

在 L1 的 embedding $\iota$ 下，给定 $\varepsilon$-composable security:

- **L2.a**：rate 关系 $R_\varepsilon^{\mathcal{A}_\text{tr}}(\iota(\Pi)) \stackrel{?}{\geq} R_\varepsilon^{\mathcal{A}_\text{umr}}(\Pi)$（**方向待 L2.G1 确认，不假设**）
- **L2.b**：Eve 能力关系（在 spaces 对齐之后）

**严谨性 [UNKNOWN]**：L2 statement 涉及 4 个 [UNKNOWN] sub-gap (L2.G1 - L2.G4)。其中 L2.G3 是 path γ v0.2 retraction 的同型 trap；L2.G1 sign-direction 是 v1 FINDINGS retraction 的同型 trap。

### 2.3 Lemma L3 — Rate Definition Alignment

**Statement target [DRAFT stub]**：

$R_\varepsilon^{\mathcal{A}_\text{tr}}$ 与 $R_\varepsilon^{\mathcal{A}_\text{umr}}$ 在共享 protocol operations 与 security definition 下 operationally 对齐：

- **L3.a**：定义层 LOPC scheme + key length formula + ε-condition 同一
- **L3.b**：operational equivalence

**严谨性 [UNKNOWN]**：L3 statement 涉及 3 个 [UNKNOWN] sub-gap (L3.G1 - L3.G3)。其中 L3.G3 涉及"最后一步 inherits Pirandola 2019 Eq.11 在 $\iota(\Pi)$ 拓扑下的适用性"，**这一步本身 inherits trust assumption**，**未**自动绕开 β.G4 等价问题。

---

## §3 11-gap inventory（**annotated restoration** of [scaffolding v0.1](umr_path_alpha_scaffolding.md) §5）

**说明**（per Codex round 2 minor issue）：本节是旧 scaffolding 11-gap inventory 的 **annotated restoration** —— gap ID 与高层结构与 v0.1 一致，但本文件添加了 trap 关联标注（如 "v1 FINDINGS retraction 同型 trap" / "path γ v0.2 trap 同型"）以便 reviewer 与 user 快速 cross-reference 撤回先例。**Gap 内容 / 数目 / ID 均与 v0.1 一致；qualifiers 是 annotation 不是 substance change**。

**重申**：以下 11 gaps **全部 [UNKNOWN]**。本文件**未** close 任何一个。

| Lemma | Gap ID | 描述 | 升级所需（user / 外部依赖） |
|---|---|---|---|
| L1 | **L1.G1** | $\mathcal{A}_\text{umr}$ / $\mathcal{A}_\text{tr}$ 定义 + Hilbert 空间 alignment | user formal specification（**path γ v0.2 trap 同型**） |
| L1 | **L1.G2** | embedding $\iota$ 具体构造（tensor with dummy workspace? Symmetric unification? unspecified） | user 纸笔构造 |
| L1 | **L1.G3** | Stinespring gauge invariance | 技术 proof 或 tightness argument |
| L1 | **L1.G4** | Output state equivalence metric（distance measure 选取与证立） | 选择 + 证明合适 distance measure |
| L2 | **L2.G1** | rate-direction sign check（umr ≤ trust rate?反向?）— **v1 FINDINGS retraction 同型 trap** | user 小心算 + Pirandola Eq.11 sign convention 核对 |
| L2 | **L2.G2** | Composable ε 三分量（secret + correct + complete）transfer | Portmann-Renner 2022 适配 |
| L2 | **L2.G3** | Eve 能力包含 across spaces（v0.2 retraction trap：naive set-inclusion across different Hilbert spaces） | **必须避免** naive set-inclusion |
| L2 | **L2.G4** | Non-LOCC 联合 attack 处理（umr Eve 若可生成非 LOCC 攻击，L2.b 不成立） | Portmann-Renner semidefinite framework |
| L3 | **L3.G1** | LOPC syntax 在 trust vs umr 下 reconcile（Charlie 在两个 model 下角色不同） | 形式化 operation model |
| L3 | **L3.G2** | Key length formula + ε 跨 topology equivalence | Portmann-Renner 2022 详细适配 |
| L3 | **L3.G3** | 最后一步 inherits Pirandola 2019 Eq.11 在 $\iota(\Pi)$ 下的适用 — **inherits trust assumption** | check trust assumption 不 breach；**这一步未自动绕开 β.G4** |

**Total: 11 gaps, all [UNKNOWN]**。

### 3.1 v0.2 4-gap 与 v0.3 11-gap 的对照

**说明**（per Codex round 2 minor）：本节**仅**映射 v0.2 显式列出的 4 个 sub-gap (α.G1 / α.G2 / α.G2.E / α.G3) 到对应的 v0.3 IDs。**L1.G3 / L1.G4 在 v0.2 缺 antecedent —— 它们是从 [scaffolding v0.1](umr_path_alpha_scaffolding.md) §5 直接 restore，不在 v0.2 的 4-gap 压缩里**。这正是 v0.2 的 4-gap 压缩**不完整**的 evidence。

| v0.2 sub-gap | v0.3 归类 | 说明 |
|---|---|---|
| α.G1 (Lemma A 合法性) | → **L1.G1 + L1.G2** | 拆分到 Hilbert 对齐 + embedding 构造 |
| α.G2 (Lemma B 安全单调) | → **L2.G1 + L2.G2 + L2.G4** | 拆分到 sign + ε 三分量 + 非 LOCC |
| α.G2.E (Eve-set 兼容性) | → **L2.G3** | 旧 scaffolding 已识别为 v0.2 retraction 同型 trap |
| α.G3 (Lemma C rate 对接) | → **L3.G1 + L3.G2 + L3.G3** | 拆分到 LOPC syntax + key length + Pirandola Eq.11 适用 |
| **(无 v0.2 antecedent)** | **L1.G3 (Stinespring gauge invariance)** | v0.2 4-gap 压缩**遗漏**；v0.3 直接从 v0.1 scaffolding restore |
| **(无 v0.2 antecedent)** | **L1.G4 (Output state equivalence metric)** | v0.2 4-gap 压缩**遗漏**；v0.3 直接从 v0.1 scaffolding restore |

---

## §4 综合包含链 — **conditional 公式**（不主张 [SYN] 成立；v0.3 patch 2026-04-26 加 Pirandola Eq. 11 specialization chain caveat）

**条件句**（v0.3 加固，per Codex round 1 critical 反馈 + 2026-04-26 C3 batch finding）：

$$\text{If} \quad \bigwedge_{i \in \{1,2,3\}, j \in \text{Gaps}(L_i)} \text{L}_i.\text{G}_j \text{ AND L3.G2.E AND Eq. 11 specialization chain are independently established}$$
$$\text{then the chain would imply} \quad K_{\text{umr}} \stackrel{\text{Lemma A+B+C}}{\leq} K_{\text{trusted}} \stackrel{\text{Eq. 11 [THM]}}{\leq} \min_C E_R(C) \stackrel{\substack{\text{Eq. (8)/(9) + tele-cov} \\ \text{+ sym η split [cond.]}}}{=} -\log_2(1 - \sqrt{\eta_{AB}})$$

**关键限定**：
- 所有 12 sub-gap 当前 [UNKNOWN] / pending（**12 = 11 原 + L3.G2.E 新立项**；详 §1.1 patch + [path_alpha_subgap_closure_integration_v0_3.md](path_alpha_subgap_closure_integration_v0_3.md) §1，v0.2 已 [SUPERSEDED]）
- 综合链当前**未**成立
- 本文件**未**主张 "在某个 reasonable Eve set 下成立" / "以 high confidence 成立"
- **NEW (2026-04-26)**: Pirandola Eq. 11 specialization 到 specific η-form `-log_2(1-√η_{AB})` 是**独立 conditional step**，需 Eq. (8)/(9) lossy chain + tele-covariance（pure-loss bosonic）+ symmetric η split (`η_{AB} = η_A·η_B`)；不是 Eq. 11 直接给出（详 [RETRACTION.md §9.3](../research/RETRACTION.md#93-l3g3-gap-id-round-揭露重大-pirandola-eq-11-citationspecialization-错误)）
- 任何对外引用**禁止**援引此公式作为定理

---

## §5 数值 reframing（仅 finite grid，无 scaling-tightness claim）

### 5.1 数据来源（无新计算）

复用 [path_alpha_v0_2_alignment.csv](../research/data/path_alpha_v0_2_alignment.csv)（v0.2 生成，公式与脚本经 Codex round 1 PASS）。

### 5.2 表格（措辞加固）

| loss (dB) | $\eta_{AB}$ | $-\log_2(1-\sqrt{\eta_{AB}})$ (numerical only) | TF Pareto LB | MDI Pareto LB |
|---|---|---|---|---|
| 0 | 1.0 | $\infty$ (η=1 singular) | 8.25e-4 | 1.90e-3 |
| 10 | 1.0e-1 | 0.5484 | 2.50e-4 | 1.87e-4 |
| 20 | 1.0e-2 | 0.1520 | 7.78e-5 | 1.82e-5 |
| 30 | 1.0e-3 | 4.64e-2 | 2.44e-5 | 1.70e-6 |
| 40 | 1.0e-4 | 1.45e-2 | 7.67e-6 | 1.37e-7 |
| 50 | 1.0e-5 | 4.57e-3 | 2.37e-6 | 5.95e-9 |
| 60 | 1.0e-6 | 1.44e-3 | 6.96e-7 | 0 (cutoff) |
| 70 | 1.0e-7 | 4.56e-4 | 1.70e-7 | 0 |
| 80 | 1.0e-8 | 1.44e-4 | 9.47e-9 | 0 |

### 5.3 解读（v0.3 加固 — Codex round 1 major issue 修复）

**严格 hedge 措辞**：以下陈述**仅描述 finite-grid 数值表观**，**不**作 scaling-tightness 的研究 claim：

- 在此 finite grid 上，**numerical formula** $-\log_2(1-\sqrt{\eta_{AB}})$ 与 TF Pareto LB 的 ratio 在 10-60 dB 区间约 1900-2100×。**这是 numerical 表观，不是 scaling-tight 证立**。
- 在此 finite grid 上，MDI Pareto LB 的 ratio 在 10-50 dB 区间从约 2937× 增长到约 768593×（**v0.2 的 "~1500×" 是错误压缩，已修正**）。
- 任何**关于 √η scaling 是否紧**的判断**未**由本表给出。
- 任何**关于 prefactor gap 来源（A/B/C 因子）**的归因**未**由本表给出（per FINDINGS v2 §4.2 — Sub-Q4 归因须在 Sub-Q3 完成**之后**重启）。

### 5.4 数值脚本现状

[scripts/path_alpha_v0_2_alignment.py](../../scripts/path_alpha_v0_2_alignment.py) **保留**（脚本本身经 Codex round 1 PASS），其 docstring 已含 "no Lemma closure asserted, sub-gaps OPEN" 声明。**使用时须显式说明** v0.2 spec 文档已 [REJECTED]，v0.3 仍为 [DRAFT statement-stub]。

---

## §6 与现有文档的关系（v0.3 修正一致性）

### 6.1 累积 ledger（v0.2 立项至 v0.3 round-2-cleanup 全部修改文件）

**性质**：累积 ledger 而非单 round changeset；用于 cross-document 一致性核验。

- ✅ [docs/PHASE_STATUS.md](../PHASE_STATUS.md): §4.5 "user directive 2026-04-25" + §5 priority queue 反转 path α first
- ✅ [docs/research/FINDINGS.md](../research/FINDINGS.md): §4.3 v0.2/v0.3 retraction + user override 记录
- ✅ [docs/proofs/umr_path_alpha_three_lemma_v0_2.md](umr_path_alpha_three_lemma_v0_2.md): 顶部 [REJECTED round 1] banner
- ✅ [docs/proofs/umr_path_alpha_three_lemma_v0_3.md](umr_path_alpha_three_lemma_v0_3.md): 顶部 [USER-APPROVED PRIORITY 2026-04-25, NOT C3-passed] banner
- ✅ [docs/proofs/umr_path_delta_relaxed_trust_v0_1.md](umr_path_delta_relaxed_trust_v0_1.md): 顶部 banner 改指 v0.3 + 删 disavowed framing（round-3 cleanup）
- ✅ [docs/workflow/umr-path-alpha-three-lemma-v0-2/](../workflow/umr-path-alpha-three-lemma-v0-2/): round 1 + round 2 + round-3-cleanup 完整记录

### 6.2 不修改

- ❌ [docs/findings/upper_bound_report.md](../findings/upper_bound_report.md) v0.7（formal record）
- ❌ [docs/findings/gap_shape_g4_1.md](../findings/gap_shape_g4_1.md)（Sub-Q4 归因 record）
- ❌ [docs/proofs/umr_path_beta_*.md](../proofs/) / [umr_path_gamma_*.md](../proofs/)（β/γ 路径独立保留）
- ❌ [docs/proofs/umr_path_alpha_scaffolding.md](umr_path_alpha_scaffolding.md) v0.1（本文件继承其 11-gap inventory，但**不**修改原 scaffolding）
- ❌ [docs/proofs/umr_path_alpha_derivation.md](umr_path_alpha_derivation.md)

---

## §7 验证路径建议（C1 / C2 / C3 — 不绕过任何闸门）

### 7.1 升级 v0.3 的硬条件

任何**单**条 Lemma sub-gap 的 close 都需要 user 的 paper-level work：
- **Lemma 全部 close + 综合链成立** → 升级到 [SYN]
- **进一步**升级到 [COROLLARY] → R0.2 (C1 ∧ C2 ∧ C3) 完整流程

**C1 (independent validation)** R0.2 (a)/(b)/(c) 任一：
- (a) 跨家族 AI 双方直读 PDF（Pirandola 2019 / Khatri-Wilde §19-20 / Lucamarini 2018 / Wang 2019 / Curras-Lorenzo 2021 / Portmann-Renner 2022）
- (b) user 本人纸笔形式化
- (c) proof assistant 形式化（Coq/Lean）

**C2 (user 签字)**：user 对每个 closed sub-gap 显式签字

**C3 (dev-reviewer)**：每次 sub-gap 状态变更后重新评审

### 7.2 不做的事（Codex round 1 issue 修正）

- ❌ **不**给短期时间表（"Day N" / "X 小时" / "Y 天可闭合"）
- ❌ **不**预设 Lemma close 顺序 / 难度排序（旧 scaffolding 的 11 gap 难度互相依赖，user 决定）
- ❌ **不**主张 "20-25 小时 user 工作可关闭" 等 reviewer-flagged 时间估计
- ❌ **不**主张 "比 γ 更稳"

### 7.3 回滚条件（明示，operationalized 版本）

**注**：v0.3 round 2 已发生，user 2026-04-25 显式 override 本条 §7.3。以下为重启回滚的 specific trigger（非"同型陷阱"概括，per Codex round 2 minor 反馈）：

如果以下**任一具体事件**发生 → user-override 失效，path α retire to scaffolding-only:

- **T-7.3.1**：v0.3 在 user 直读 PDF 后发现 L1.G1 / L2.G3 与 path γ v0.2 retraction 同型 trap（"两 Eve 集合不在同 Hilbert 空间"）且 user 决定不继续
- **T-7.3.2**：v0.3 在 user 形式化时发现 L2.G1 sign-direction 与 v1 FINDINGS retraction 同型（trusted-relay Pirandola Eq.11 应用方向反）
- **T-7.3.3**：v0.3 衍生材料（v0.4 / 后续 spec / 论文草稿）在 dev-reviewer 评审中**任一 reviewer** verdict UNSOUND 且 critical issue 涉及 **lemma 内容**（非 cleanup-level）
- **T-7.3.4**：user 显式撤销 2026-04-25 override（不需理由）

**T-7.3.1 / T-7.3.2 / T-7.3.3 任一触发 → retraction 流程**：v0.3 加 [RETRACTED] banner，[FINDINGS §4.3](../research/FINDINGS.md) 改为 [RETRACTED]，path α 退出 active priority。**此 retraction 流程 not user-overridable**（per RETRACTION.md §4.1 留痕规范 + R0.1 不留痕降级）。

**T-7.3.4 触发 → simple rollback**：path α 改回 scaffolding-only / cautionary status。

---

## §8 Changelog

- **v0.3** (2026-04-25)：第二版立项。Replace v0.2 [REJECTED]。统一所有 7 条 Codex round 1 issues：恢复 11-gap inventory、移除 Justification sketch、综合链 conditional 化、数值 hedge 化 ("is consistent with this finite grid")、§6.1 一致性、移除短期时间表、user directive 优先级反转理由 verbatim 引用。**不**主张 "比 γ 更稳"。全文 [DRAFT statement-stub]，11 sub-gap [UNKNOWN]。
- **v0.2** (2026-04-25, [REJECTED 2026-04-25])：autonomous 起草，被 dev-reviewer round 1 双 Codex 撤回（diff REJECTED 1 critical + 3 major + 1 minor; holistic UNSOUND 6 维度）。
- **v0.1 scaffolding** (2026-04-22)：[umr_path_alpha_scaffolding.md](umr_path_alpha_scaffolding.md)，11-gap inventory 首版。

---

*END OF v0.3.* All 11 sub-gaps [UNKNOWN]. **No proof / closure / "更稳" claim asserted**. R0.1 不降级 / R0.2 不越权 / R0.3 [DRAFT] 级保持. user-directive 2026-04-25 仅 approve 方向不替代 R0.2 三闸门. 回滚条件见 §7.3.
