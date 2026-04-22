# Q1 Path α/β/γ Decision Analysis — 用户决策辅助文档

**版本**：v0.1
**日期**：2026-04-22 Day 2 late evening (autonomous analysis)
**类型**：**decision-support document**, **非 rigor claim**
**目的**：为用户选哪条 path 做 formal 工作提供系统化对比 + 推荐

---

## 0. 分析 scope

本文件聚焦 **user decision Q1**（见 [main_question_interim_status_2026-04-22.md](main_question_interim_status_2026-04-22.md) §7 upgrade path）：选择 **path α (monotonicity reduction)** / **β (channel-reduction)** / **γ (single-edge PLOB + DPI)** 中**哪一条**做用户纸笔 formal 工作 (C1(b))。

**前提**：用户已决定走 formal 工作（**而非** 放弃该 subgoal）。**本分析不 re-litigate 是否应启动 formal 工作**；只对比三选项。

---

## 1. 核心对比表

| 维度 | α (monotonicity) | β (channel-reduction) | γ v0.4+R3 (single-edge PLOB + DPI) |
|---|---|---|---|
| **Log 07 定位** | §4.3 "正确路径,但需要写出来" | §4.4 "可能给出更紧的 bound" | §4.5 "最小可信的 baseline" |
| **Core tool** | Khatri-Wilde §19-20 monotonicity | Effective channel $\tilde{\mathcal{M}}$ + PLOB/WTB | PLOB on $\mathcal{E}_1$ alone + data-processing inequality |
| **Primary literature** | Khatri-Wilde 2020/2024 (Ch 19-20) | PLOB 2017 + WTB 2017 | PLOB 2017 + QI textbook DPI |
| **Target bound 形式** | $R \leq -\log_2(1 - \min(\eta_A, \eta_B))$ | $R \leq f(\eta_A, \eta_B)$, $f$ unknown but computable via SDP | $R \leq -\log_2(1 - \min(\eta_A, \eta_B))$ |
| **Scaling** | $\sqrt{\eta_{AB}}$ (same as Pirandola 2019) | **unknown**: 可能更紧、comparable、或更松 | $\sqrt{\eta_{AB}}$ (same) |
| **Gaps 数量** | 11 (scaffolding authoritative) | 5 (β.G1-G5) | 5 (γ.B.G1-G3 + γ.G3 + γ.G4) |
| **估计人日** | **10-15** | **7-10** | **5-7** (最短) |
| **Codex history (本项目)** | R1-R5 反复 flag identity-embedding = v0.2 陷阱 | R1-R5 逐步收敛; tightness 方向 agnostic | v0.2 retracted, v0.3 retracted, v0.4+R3 收敛但仍 [CONJ] |
| **Retraction risk at start** | **HIGH** — 11 gaps + 2 属于 "cross-space" 类 | MEDIUM — β.G5 adversarial reduction 有前车之鉴 | MEDIUM — 3 次迭代史; v0.4 最干净 but Step B 仍开 |
| **Research output novelty** | **Low** (bound 与 Pirandola 2019 等价, 只是严格推导) | **HIGH** (若成功, 是 **新** bound, 可能 Sub-Q4 attribution-relevant) | Low (bound 与 PLOB single-edge 等价, "最小可信") |
| **Unblocks Sub-Q4 G4.2?** | ✓ (升到 [COROLLARY]) | ✓ (升到 [COROLLARY]) + **potentially 更精确的 attribution** | ✓ (升到 [COROLLARY]) |
| **Dependency pre-reqs** | Khatri-Wilde Prop 19.2 proof (textbook) + Portmann-Renner framework | PLOB 2017 + WTB 2017 + SDP theory | PLOB 2017 + Nielsen-Chuang DPI (standard) |

---

## 2. 各维度深度分析

### 2.1 数学难度 & 陷阱历史

**α**:
- 11 gaps 涉及 3 大类 Lemma (L1 Protocol embedding, L2 Security reduction, L3 Rate definition alignment)
- L2.G3 "Eve spaces across topology" 是 **v0.2 + v0.3 retraction 同类陷阱**
- 陷阱形式：把 trusted/umr Eve powers 做 cross-space comparison without formal embedding
- **需要 Portmann-Renner composable framework** — 这个 framework 对多数研究者都是 ~1-2 周学习 + ~1 周适配

**β**:
- β.G5 (adversarial-channel reduction) 是 Codex R1 补的 gap — **新发现**
- 数学工具更具体 (PLOB + WTB + SDP), 已有 literature
- 核心难点: two-source merge (β.G1, MINOR) + PLOB apply to 2-to-2 broadcast channel (β.G2, MAJOR) + $E_R^\infty$ SDP 数值 (β.G3, MAJOR)
- **不依赖** Portmann-Renner framework
- 风险: SDP 若给不出 closed form，只有 numerical bound (值得做 but 不够"漂亮")

**γ v0.4+R3**:
- Step B 降级 为 target DPI lemma (不是 capacity transfer)
- γ.B.G1 DPI 的 rigorous formulation 是**关键** — Log 07 §4.5 原文 intuition 是 "Eve 对 Charlie mode 做任意后续 operations 不增 Alice-Bob correlation"
- γ.B.G2 Charlie BSM 是 joint quantum + classical operation — 需 careful handle
- γ.B.G3 Alice-Charlie point-to-point bound 与 Alice-Bob key rate 之间的 operational link
- **结构最简**, 但 γ.B.G1-G3 是**新 gap** (v0.4+R3 加)
- 风险: v0.2 + v0.3 已 failed；v0.4 是第三次尝试

### 2.2 Research output value

**α**:
- 给 $-\log_2(1-\sqrt{\eta_{AB}})$ scaling — 已在 Pirandola 2019 trusted-relay setting 存在
- **对学术界新颖度低** — 主要是 "把 trusted 推广到 untrusted 的严格继承"
- 论文 angle: "First rigorous untrusted-relay converse via Khatri-Wilde amortized entanglement"

**β**:
- $f(\eta_A, \eta_B)$ 未知 — 可能 **严格紧于** Pirandola min-cut
- 若成功, 是**新 bound** — Log 07 §4.4 推测 "umr 约束 Charlie 为 measure-only 可能降 Eve 提取" 
- **论文 angle 最强**: "Tighter converse for untrusted measurement relay via channel reduction"
- **Sub-Q4 attribution bearing**: 若 β 给 **更紧** bound, gap 缩小, 可 refine attribution (part of α 还是 β 还是 γ?)

**γ**:
- 与 PLOB single-edge 等价 — **最小 novelty**
- 论文 angle: "Minimal converse proof for untrusted relay via data-processing"
- **价值**: baseline 性质 — 即使 β 失败, γ 也能兜底给合理上界

### 2.3 项目完成度 vs 学术研究深度

用户项目目标 (PROSPECTUS §1 + RESEARCH_PLAN): **主问题 + 4 Sub-Q "明确结论"**。

**最快到 "明确结论"**:
- **γ 最短** (5-7 人日) → 解锁 Sub-Q4 G4.2 attribution 启动
- α, β 需要更久

**学术深度最高**:
- **β** (if succeeds): new tight bound, novel result
- α, γ: re-derivation of known scaling with different rigor framework

### 2.4 Codex guardrail view

三 path 经 5 轮 Codex review:
- α: Codex 一致判定 "identity-embedding = v0.2 class"，反复 flag。**最高 retraction risk**
- β: Codex 关切集中在 β.G5 adversarial reduction + tightness overclaim — 都是 **localized** issues
- γ v0.4+R3: v0.2 + v0.3 已过滤掉 2 种陷阱变种, v0.4 "最干净 at iteration cost"

Codex 反复 review 的**信号**: path α 的陷阱更深、更广、更难 avoid。

---

## 3. 决策矩阵

| 决策目标 | 最优 path | 原因 |
|---|---|---|
| **最短时间 close Sub-Q3** | **γ** (5-7 人日) | Log 07 §4.5 "最小可信" + 最少 gap + 结构最简 |
| **最高学术 novelty** | **β** | potential 新 tight bound, Log 07 §4.4 推测更紧 |
| **最低 retraction risk** | **γ v0.4+R3** | v0.4 已过滤掉 v0.2 + v0.3 两种陷阱; β.G5 is known gap |
| **解锁 Sub-Q4 G4.2 最好** | **β** (若更紧) 或 **γ** (若 β 不更紧) | β 紧化可能 refine attribution; γ 兜底 |
| **最易 collaborate** | **β** | SDP + numeric 工具可验证; 用户 paper + AI numeric 分工自然 |
| **最容易避免重复 v1/v0.2 陷阱** | **γ v0.4+R3** (iteration 已过滤) | α 最危险 (11 gaps with 2 CRITICAL); β.G5 单一 |

---

## 4. 具体推荐

### 4.1 若用户目标 = 尽快 close Sub-Q3 → **选 γ v0.4+R3**

- 5-7 人日
- Log 07 §4.5 用户自己原推荐 baseline
- v0.4+R3 已过滤 2 陷阱变种 (v0.2 + v0.3)
- 风险主要是 γ.B.G1-G3 三 gap, 但都 localized
- Output: $\sqrt{\eta_{AB}}$ 紧 scaling [COROLLARY] after C1∧C2∧C3

### 4.2 若用户目标 = 潜在最高学术价值 → **选 β, 但备份 γ**

- 7-10 人日
- **唯一** potential 给 **新** tight bound 的 path
- Log 07 §4.4 推测更紧 (agnostic per Codex)
- 并行做 γ 作为 fallback (若 β 数值显示 not tighter than Pirandola, 保 γ 仍给 baseline)
- Output: **potentially 新定理** + Sub-Q4 refined attribution

### 4.3 若用户想要完整 rigorous coverage → **γ 先做, 然后 β, 然后 α**

- 按风险从低到高顺序
- γ 作 baseline (5-7 人日)
- 之后 β 尝试紧化 (7-10 人日)
- α 只做 if 研究扩展需要 (10-15 人日, 风险最高)

### 4.4 **不**推荐 α 作为首选

- 11 gaps 最多, 含 2 CRITICAL 级 (retraction-pattern-class)
- Codex 5 轮反复 flag identity-embedding 是 v0.2 同类
- 工期最长 (10-15 人日)
- Output novelty 最低 (与 Pirandola 2019 等价 bound)
- **除非**: 用户已有 Khatri-Wilde §19-20 + Portmann-Renner 熟练程度, 并愿接受 framework cost

---

## 5. 决策建议汇总

**默认推荐**: **γ v0.4+R3** (最短, 最低 retraction risk, Log 07 原推荐 baseline)

**若有学术 paper target**: **β 作主攻, γ 作 safety net**

**若时间充裕 + 想做多种 bound 对比**: γ → β → α 顺序

**不推荐 α as 首选**: retraction risk + 长工期 + 低 novelty

---

## 6. User action to execute (选定后)

无论选 α/β/γ，用户需做:

**Phase 1 — Scope definition** (0.5 天):
- 阅读对应 scaffolding / derivation doc
- 确认 target statement + gaps list
- 确定 scope (bosonic-asym / DV strict / finite-key / etc.)

**Phase 2 — Formal derivation** (5-15 人日 per path):
- 按 gaps 逐一 close
- 每 close 一个 gap 留 note (用户纸笔或 digital)
- 关键 lemma 用**跨家族 AI (Claude + GPT + Gemini 独立复核)** 或 **非 AI 工具 (Mathematica symbolic)** 验证 → 满足 R0.2 C1(b) + C1(c)

**Phase 3 — Integration** (1-2 天):
- 起草 `docs/proofs/umr_path_<X>_formal_vN.md`
- dev-reviewer double Codex review → C3
- 用户审签 → C2
- 触发 Sub-Q4 G4.2 启动

---

## 7. 严谨性

- 本文件 **decision-support analysis, not rigor upgrade**
- 推荐基于 Codex 5-round review 历史 + Log 07 原审计 + 项目效率 trade-off
- **不**预判用户 paper target 或个人偏好
- 实际选择 **由用户决定**

---

## Changelog

- **v0.1** (2026-04-22 Day 2 late evening autonomous): Q1 decision-support analysis; 推荐 γ (default), β (paper angle), 不推荐 α 首选
