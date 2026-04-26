## STRATEGY_FIT
- **部分对齐，但当前文本已越过“策略说明”边界。** 作为 Log 07 已列出的 path α 选项，它和 Sub-Q3/Sub-Q4 的研究方向是对齐的；但当前稿把完整链条直接写成 `[SYN]` 断言，而不是条件化 scaffolding：[α v0.2 §1.3](
</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/proofs/umr_path_alpha_three_lemma_v0_2.md:85>)、[§3](
</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/proofs/umr_path_alpha_three_lemma_v0_2.md:222>)。
- **与 FINDINGS v2 §0.2 的 bosonic-asymptotic 放宽范围只算“隐含一致”，不算“明确一致”。** FINDINGS v2 明确说当前 scaling verdict 只在放宽版 bosonic-asym 范围内成立，[FINDINGS v2 §0.2](
</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/research/FINDINGS.md:26>)；α v0.2 没把 H4/H5/H6 的放宽重新钉牢，只是默认继承。
- **不符合 RESEARCH_PLAN 的 Phase 2 边界。** RESEARCH_PLAN 把 Sub-Q3 定位为 3–5 个月、Level 3-4 精读、30–50 页接缝报告的大工作，[RESEARCH_PLAN §4](
</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/RESEARCH_PLAN.md:316>)；α v0.2 的 “Day 5-9 → v0.3 → 候选 [COROLLARY]” 明显过快，[α v0.2 §5.2-§5.3](
</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/proofs/umr_path_alpha_three_lemma_v0_2.md:314>)。
- **已提前做了 Sub-Q4 gap 归因。** `[SYN-α-1/2/3]` 直接把 TF gap 归因为 prefactor、把 MDI gap 归因为 scaling mismatch，这与 FINDINGS v2 “Sub-Q4 归因应在 Sub-Q3 完成后重启” 冲突，[FINDINGS v2 §4.2](
</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/research/07_pirandola_2019_technical_audit.md:135>)、[α v0.2 §3.1](
</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/proofs/umr_path_alpha_three_lemma_v0_2.md:261>)。

## RETRACTION_RISK_VS_PRIOR_PRECEDENTS
- **对比 retracted γ v0.2：是同型风险，只是包装更整洁。** γ v0.2 的问题是把三条 lemma 合成一个 containment shortcut；α v0.2 虽然把三条 lemma 拆开了，但仍在 `[α v0.2 §3]` 写出无条件 combined chain。repo 里旧 α 文档已把这类 embedding / inclusion / monotonicity shortcut 明确列为同类 cross-space trap，[旧 α 记录 §4](
</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/proofs/umr_path_alpha_derivation.md:91>)。
- **对比 retracted γ v0.6：没有直接重犯 cross-task transfer，但仍在做 cross-space transfer。** 它没有把 Alice-Charlie task 转成 Alice-Bob task，这点比 γ v0.6 好；但 `Π -> Π_tr`、`E_tr = Tr_{Charlie+broadcast} E_umr`、`R_umr ≤ R_tr` 仍然是跨安全博弈/跨空间的 transfer，不是纯文献核对。
- **对比 retracted FINDINGS v1：`[SYN-α-1/2/3]` 有明确 over-claim。** 数值图只能支持“若 α 链成立，则与现有 LB 的相对位置如此”；不能支持“confirm TF 同 scaling / MDI scaling mismatch / prefactor-only gap”这类归因性句子。
- **对比 AD channel-vs-state 撤回：有同类“跨层级静默升级”。** AD 先把 state-level 数值偷换成 channel-level claim；这里则把 protocol-class framing、security-game monotonicity、capacity inequality 连成一个结果。层级不同，但 silent-upgrade 机制同类。
- **对比第 5 次 trap memory：未满足“gaps must remain OPEN”的实质要求。** 名义上 OPEN，实质上却给出完整链条、`confirm` 语句、3-4 天 closure 计划，这正是 memory 禁止的模式。

## R0_2_VALIDATION_CHAIN
- **C1 与 C3 在文字上区分清楚了。** `[α v0.2 §5.1]` 把 C1/C2/C3 分开写，这点是合规的。
- **但 α.G1/G2/G2.E/G3 并没有做到“只保持 OPEN，不做隐式闭合”。** 真正的问题不在表格里，而在 `[α v0.2 §1.3]`、`§3`、`§3.1` 已把链条和结论写成成立中的 `[SYN]`。
- **§-1.5 的 trap warning 不够。** 它提醒了 G1/G2/G3 的“显然化”风险，但漏掉了旧 α scaffolding 认定的核心难点：cross-space protocol embedding、security-game alignment、LOPC syntax reconciliation、rate-definition reconciliation 其实是结构 gap，不是 1 行 textbook lemma，[旧 α scaffolding §2-§5](
</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/proofs/umr_path_alpha_scaffolding.md:60>)。
- **因此 validation chain 的最大问题不是 C1/C3 混淆，而是前置对象本身已被写得过强。** 在这种状态下谈 C1/C2/C3，会把“需重写的问题陈述”伪装成“待验证的候选结论”。

## PATH_RELATIONSHIPS
- **“α 是 complement，不是 replacement”在口头上写对了。** `[α v0.2 §-1.3]`、`§6.3` 明确说不替代 β/γ，只做 scaling-level looser UB。
- **但文本行为上又把 α 推成了主路径。** 它不仅 supersede 了 δ，还把 α 说成“比继续尝试 γ 更稳”，这与 Log 07 的权威建议“先试 γ baseline，失败再回 α/β”相冲突，[Log 07 §4.5/结论](
</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/research/07_pirandola_2019_technical_audit.md:162>)、[α v0.2 §5.4](
</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/proofs/umr_path_alpha_three_lemma_v0_2.md:335>)。
- **δ 的 supersession 记录方式本身是干净的。** 保留历史、迁移洞察，这点没问题。
- **不干净的是 supersession 的理由。** “path α 不比较 Eve，只比较 protocol class，从而真正绕开 β.G4”说得太满，因为 Lemma B 仍在比较 Eve access / side information；按旧 α scaffolding，这恰恰还是 cross-space gap 的一部分。

## ALIGNMENT_WITH_LOG_07
- **优点：它承认 α 不是关闭 β.G4/β.G5 的紧界路径，只是 scaling-level bypass。** 这点与 Log 07 大方向一致。
- **缺点：它没有保留 Log 07 的优先级判断。** Log 07 当前权威建议是 γ 先、α/β 后；α v0.2 反而把 α 提成“先闭合目标”，没有新的用户直读依据支撑这种优先级反转。
- **更重要的缺点：它低估了 Log 07 对 α 自身 gap 的重量级。** Log 07 只说“这三条 lemma 要写出来”；后续旧 α scaffolding 已把这件事展开成 11 个 `[UNKNOWN]` gap，而 α v0.2 退回成 4 个 checklist，和现有 repo 记忆不一致。
- **所以结论是：它承认“不是替代 β/γ”，但没有充分承认“自己的三 lemma 也还远没到可收口状态”。**

## COMPLETENESS
- **paper checklist 的方向基本对。** Pirandola 2019、Lucamarini 2018、Wang 2019、Curras-Lorenzo 2021、Lo-Curty-Qi 2012、Portmann-Renner、Renner/Tomamichel 都是应读材料。
- **但 checklist 不完整。** 按旧 α scaffolding，最关键的不是再多读几篇 protocol paper，而是明确 cross-space embedding、security definition transfer、LOPC syntax reconciliation 这些 novel-proof 任务；当前 checklist 把它们压缩成“PDF 核查 + 1 行 formalization”，不真实。
- **时间估计明显失真。** α v0.2 估 20–25 小时 / 3–4 天，[α v0.2 §4](
</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/proofs/umr_path_alpha_three_lemma_v0_2.md:281>)；旧 α scaffolding 估 10–15 人日，[旧 α scaffolding §7](
</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/proofs/umr_path_alpha_scaffolding.md:144>)。当前估时更像“citation check”，不像“closing structural gap”。
- **Day 5-9 计划与 R0.2 timing 不一致。** C1(b) 人类纸笔、C2 明确签字、C3 dev-reviewer、以及可能的 FAIL/REJECTED 迭代，都不可能被稳妥压进这个节奏里。

## RECOMMENDATIONS
- **先撤回当前 α v0.2 作为 active strategy text，改成 scaffolding-only / cautionary v0.3。** 核心动作是删掉无条件 combined chain、删掉 `[SYN-α-1/2/3]` 的 `confirm` 话术、删掉 Day 5-9 的 `[COROLLARY]` 候选时间表。
- **恢复与旧 α scaffolding 的一致性。** 要么回到 11-gap inventory，要么显式说明为什么 11 gaps 可严格压缩为 4 gaps，并逐条回应 [旧 α 记录](
</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/proofs/umr_path_alpha_derivation.md:95>) 与 [旧 α scaffolding](
</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/proofs/umr_path_alpha_scaffolding.md:116>)。
- **把所有结果句改成条件句。** 例如把 `K_umr ≤ ...`、`[SYN-α-1/2/3] confirm` 改为 “contingent on α.G1/G2/G2.E/G3 all being independently established, the resulting strategy would imply …”.
- **明确重钉 scope。** 在文件首页重述“仅限 FINDINGS v2 §0.2 的 bosonic-asymptotic relaxed scope；不回答 PROSPECTUS H1-H6 主问题”。
- **把 path α 定位改回“候选补充路径”，不要重写 Log 07 的优先级。** 若想改成 α-first，必须有新的用户直读理由，而不是 AI 自评“更稳”。

应先修订，不应以当前版本进入 user review。

VERDICT: UNSOUND