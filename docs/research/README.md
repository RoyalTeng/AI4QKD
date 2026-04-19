# Research Journal — PROSPECTUS 主问题攻坚

**启动日期**:2026-04-19
**任务**:依据 [PROSPECTUS.md](../PROSPECTUS.md) v3.1 §1,对无中继无存储 DV-QKD + 至多一个 untrusted measurement relay 拓扑的信息论极限,给出**情况 A / B / C** 判定。

---

## 0. 本轮工作的**认识论边界**(硬声明)

在任何具体研究开始前,必须诚实说明本次工作的性质与限制:

### 0.1 本次工作的定性

**本轮是"literature-informed analysis",不是"新的定理证明"。**

本轮研究者(Claude Opus 4.7)是 AI 模型,工作方式是:
- 从训练语料中合成已有文献的共识
- 按已发表的定理做逻辑推演
- 写出结构化的推理链

**不是**:
- 生成新的数学定理
- 替代 PROSPECTUS §6 Sub-Q3 要求的"30-50 页 PLOB 精读接缝报告"(那是人类研究者的多月工作)
- 替代 Sub-Q4 要求的完整 gap 归因 SDP 数值

### 0.2 输出标注协议

每个命题按以下四级标注可信度:

| 标记 | 含义 | 依据 |
|------|------|------|
| **[THM]** | 已证明定理 | 引用具体论文 + 定理号 |
| **[COROLLARY]** | 从 [THM] 推出的推论 | 给出推导步骤 |
| **[SYN]** | 文献合成 | 多个独立来源的共识,但我未亲自核对原文 |
| **[CONJ]** | 基于模式推测 | 符合场域直觉但无严格来源 |

**任何 [SYN] 和 [CONJ] 的命题在 FINDINGS 中不能作为"答案",只能作为"最有可能的情况"**。

### 0.3 可核查性

所有引用的文献、定理编号、公式在本研究日志中必须可被人类研究者独立核查。**无法独立核查的命题一律标 [CONJ]**。

---

## 1. 日志索引

工作分两个阶段:**Phase R 研究** → **Phase V 验证**。只有 Phase V 全部通过,FINDINGS 才被视为可读结论。

### Phase R:研究(Research)

| # | 文件 | 主题 | 状态 |
|---|------|------|------|
| 01 | [01_setup_and_literature_map.md](01_setup_and_literature_map.md) | 设置与文献地图 | ✅ AI 合成 |
| 02 | [02_plob_dissection.md](02_plob_dissection.md) | PLOB 2017 定理结构剖析 | ✅ AI 合成 |
| 03 | [03_network_extension.md](03_network_extension.md) | Pirandola 2019 网络推广 + DKW 2020 | ⚠️ AI 合成,核心论述被 Log 07 取代 |
| 04 | [04_upper_bound_for_untrusted_relay.md](04_upper_bound_for_untrusted_relay.md) | untrusted measurement relay 拓扑的上界 | ⚠️ AI 合成,适用性诊断被 Log 07 取代 |
| 05 | [05_achievable_rates_tfqkd.md](05_achievable_rates_tfqkd.md) | TF-QKD / MP-QKD 可达率(下界端) | ✅ AI 合成,v5 修订 |
| 06 | [06_gap_structure.md](06_gap_structure.md) | Gap 结构分析(scaling vs prefactor) | ⚠️ AI 合成,结论依赖被 Log 07 取代的 Log 04 |
| **07** | **[07_pirandola_2019_technical_audit.md](07_pirandola_2019_technical_audit.md)** | **Pirandola 2019 §II+§IV 逐步核查 + 修复路径 α/β/γ** | **✅ 人类精读(项目负责人),[THM-LEVEL AUDIT]** |
| DRAFT | [FINDINGS_DRAFT.md](FINDINGS_DRAFT.md) | 结论初稿 | ❌ 撤回 |

### Phase V:反复验证(Verification Loop)

四轮独立验证:

| V# | 文件 | 验证视角 | Verdict |
|----|------|---------|---------|
| V1 | [V1_logical_selfaudit.md](V1_logical_selfaudit.md) | 数学逻辑自审(逐条核推理链) | **PASS**(0 BLOCKER + 2 MINOR) |
| V2 | [V2_literature_crosscheck.md](V2_literature_crosscheck.md) | 文献交叉核查(WebSearch + WebFetch 独立多源) | **PASS** + 发现 "single-repeater bound" 术语加强 |
| V3 | [V3_counterexample_hunt.md](V3_counterexample_hunt.md) | 反例搜索(主动搜文献找越界协议) | **PASS** + 多篇 2023-2025 年论文确认 stop-at-√η |
| V4 | [V4_codex_independent.md](V4_codex_independent.md) | codex 独立评审(对抗立场 + 反驳尝试) | **NEEDS_REVISION**(7 findings,主结论保,细节修)→ 已应用修订 |

**最终结论(原)**:

| F | 文件 | 主题 | 当前状态 |
|---|------|------|----------|
| FINDINGS | [FINDINGS.md](FINDINGS.md) | 原宣称"情况 A 成立" | **❌ [RETRACTED 2026-04-19]** |
| FINDINGS_DRAFT | [FINDINGS_DRAFT.md](FINDINGS_DRAFT.md) | Phase R 初稿 | **❌ [RETRACTED 2026-04-19]** |
| **RETRACTION** | **[RETRACTION.md](RETRACTION.md)** | **撤回声明 + 方法论教训** | **✅ 当前权威文件** |

---

## 🛑 当前状态(2026-04-19 撤回后 + Log 07 技术审计后)

- **PROSPECTUS v3.1 §1 主问题**:**仍然开放**,归 Sub-Q3 Phase 2 + Sub-Q4
- **Sub-Q3 上界工作**:**技术起点已由 Log 07 建立**(项目负责人人类精读),失效诊断(Step C)+ 三条修复路径(α 单调归约 / β 直接 channel converse / γ 最小 PLOB + data-processing baseline)已写清。Sub-Q3 接下来的工作是**把路径 γ 形式化**或按 α/β 推进。
- **Sub-Q4 gap 归因**:**撤回预判**,等 Sub-Q3 的 Step C 替换论证完成后启动

**撤回原因摘要**(完整见 [RETRACTION.md](RETRACTION.md)):

1. Pirandola 2019 对 untrusted relay 适用性论证缺失(靠未显式写出的 capacity monotonicity 直觉)
2. 公式表述读起来像 PLOB 误用(形式同构 "PLOB 的 η 替换为 √η_AB")
3. 文献共识 ≠ 定理级 converse 证明
4. Phase V 四轮审计未抓住物理拓扑误用 —— 与 AI4QKD v1 失败模式同构
5. 越权"关闭"PROSPECTUS Sub-Q3 原本要做的 30-50 页精读工作

**Logs 01-05 文献地图部分**仍保留作 Sub-Q3 起点价值,但**不作 Sub-Q1 答案**。

---

## 2. 研究问题重述(自 PROSPECTUS §1)

**核心问题**:在无量子中继($|\mathcal{P}| \in \{1,2\}$,不含纠缠交换或纠缠生成中间节点)、无量子存储(源方制备后不做本地延迟操作)、使用离散变量载体的约束下,两方之间通过**至多一个 untrusted measurement relay** 建立共享密钥的**信息论极限**是什么?

三种结构性可能:

- **情况 A**:$R \leq C_A(\eta)$ 其中 $C_A(\eta) \sim \sqrt{\eta}$ 是紧上界。TF-QKD 族达到根本极限。
- **情况 B**:$R \leq C_B(\eta)$ 其中 $C_B(\eta) \sim \eta^\alpha$,$1/2 < \alpha < 1$,且可达。新协议空间存在。
- **情况 C**:$C_B(\eta)$ 这样的标度上界存在但不可达。数学上有空间但物理实现不了。

**本研究日志的**任务:给出上述三者中最可能的答案,并分离其**确定性等级**(定理证明 / 文献合成 / 合理猜测)。

---

## 3. 使用的文献清单(**v5 修正 web-access 口径**)

**原 README 自相矛盾声明修正**:原文本称"本次工作没有 Web 访问",但 V2 实际使用了 WebSearch + WebFetch 工具(见 [V2_literature_crosscheck.md](V2_literature_crosscheck.md))。**正确的描述为**:

- **Phase R 写作(Log 01-06)**:仅使用训练语料中的已知内容,不做 web 访问
- **Phase V 验证(V1-V4)**:
  - V1(逻辑自审)无 web 访问
  - **V2(文献交叉核查)使用 WebSearch + WebFetch** 独立核查外部定理
  - V3(反例搜索)使用 WebSearch
  - V4(codex 独立评审)通过 `codex exec` 子进程调用 OpenAI codex,与 Claude 共享训练偏差(见 RETRACTION §4.3)

**所有 web 访问的证据(URL / 抓取日期 / 引用片段)归档在 [EVIDENCE_APPENDIX.md](EVIDENCE_APPENDIX.md)**,供独立复核。

引用时标注 [VERIFIED](web 独立核查通过)、[RECALLED](记忆中存在但未核)、[SYN](文献共识合成)。

**Phase 0-2 核心文献(按引用密度排)**:

| 引用键 | 作者-年 | 出处 | 本研究用途 |
|--------|---------|------|-----------|
| PLOB17 | Pirandola-Laurenza-Ottaviani-Banchi 2017 | Nat. Commun. 8:15043 | 点对点 secret-key capacity 紧上界 |
| Pirandola19 | Pirandola 2019 | Commun. Phys. 2:51 | 网络拓扑的端到端 capacity |
| TGW14 | Takeoka-Guha-Wilde 2014 | Nat. Commun. 5:5235 | 基于 squashed entanglement 的上界 |
| WTB17 | Wilde-Tomamichel-Berta 2017 | IEEE TIT 63:1792 | converse bound 独立推导 |
| DKW20 | Das-Khatri-Wilde 2020 | arXiv:2012.03262 | 最新 converse bound |
| Lucamarini18 | Lucamarini-Yuan-Dynes-Shields 2018 | Nature 557:400 | TF-QKD 原论文,$\sqrt{\eta}$ 可达 |
| MZZ18 | Ma-Zeng-Zhou 2018 | PRX 8:031043 | PM-QKD |
| ZZWM22 | Zeng-Zhou-Wu-Ma 2022 | Nat. Commun. 13:3903 | MP-QKD |
| WLC18 | Winick-Lütkenhaus-Coles 2018 | Quantum 2:77 | 密钥率 SDP 下界 |
| KhatriWilde24 | Khatri-Wilde 2024 | 综述书 *Principles of Quantum Communication Theory* | 系统整理 capacity 结果 |

**次要参考**:Bennett-Brassard 84 (BB84)、Lo-Curty-Qi 2012 (MDI-QKD)、Ferenczi-Lütkenhaus 2012 (对称性)、Portmann-Renner 2022 (可组合安全综述)。

---

## 4. 方法学大纲

每个研究日志按以下结构:

```
§A 本日志的子问题 + 为何必须处理
§B 工作草稿(思考过程,允许重复推敲)
§C 已证命题(附定理可信度标记)
§D 下一步依赖
```

最终 FINDINGS 按以下结构:

```
§1 主问题答案(带确定性分级)
§2 支持证据链(从 Log 01-06 汇总)
§3 未决的开放问题(接给 PROSPECTUS Sub-Q3 / Sub-Q4 的人类研究)
§4 给 PHASE0_M1 的即时行动建议
```

---

## 5. 诚信附注

- 任何引用的定理编号、方程号、常数,若我记忆不清,标 `[?]` 并在 FINDINGS 中提示需要人工核对
- 所有 [CONJ] 级别的推测在 FINDINGS 不纳入"答案",仅作"方向暗示"
- 如果最终答案不是 A/B/C 中任何一个(例如"证据不足以判定"),FINDINGS 会明确说明

---

*README 结束,进入 Log 01。*
