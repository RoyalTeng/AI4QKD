# RETRACTION — FINDINGS.md 正式撤回

**日期**:2026-04-19
**撤回者**:项目负责人(用户)经过对 FINDINGS.md 内容的独立审查后决定
**撤回文件**:[FINDINGS.md](FINDINGS.md) v1.0(commit `df92de9`)
**撤回触发**:用户 2026-04-19 审查意见(见本仓库 conversation log / issue tracker)

---

## 0. 撤回强声明

**[RETRACTED] `FINDINGS.md` 在本文件发布之后不得作为 PROSPECTUS v3.1 Sub-Q1 / §1 主问题的答案被引用**。保留原文件是为审计历史完整,不是为继续使用。

**[RESTORED] PROSPECTUS v3.1 §1 主问题的 A / B / C 判定重新回到"开放研究问题"状态**,按原计划由 Sub-Q3 Phase 2 精读 + Sub-Q4 gap 归因来严肃处理。

本 RETRACTION 所依据的用户审查意见被认定为**比 FINDINGS 文件内容更具权威性**(PROSPECTUS §9 诚信红线:项目负责人对所有 AI 协作产物拥有否决权)。

---

## 1. FINDINGS 的**实质性问题**清单

### 1.1 **Pirandola 2019 对 untrusted relay 适用性的论证缺失**[严重]

- FINDINGS 定理 4.1 的上界 $R \leq -\log_2(1 - \min(\eta_A, \eta_B))$,其来源是 Pirandola 2019 网络 min-cut 结果
- **但 Pirandola 2019 的严格 converse 证明假设 internal nodes 可以做 LOCC-simulable 的一般操作**,即最强意义下 "trusted-in-the-sense-of-protocol-cooperation" 的 relay
- **untrusted measurement relay(Charlie 被 Eve 控制)不直接落在 Pirandola 2019 定理覆盖范围内**
- FINDINGS 从 "trusted case 上界" 继承到 "untrusted case 上界" 靠的是 **capacity monotonicity argument**(untrusted 协议集 $\subseteq$ trusted 协议集,故 sup 单调),但:
  - 这个论证**没被 FINDINGS 正文明确写出**,只出现在 Log 02 B.5 + V1 审核的旁白中
  - 这个论证**可能不是文献定理级**,而更像"物理直觉可接受的推理链",适用于 [SYN] 级非 [COROLLARY] 级
  - 其严格形式化可能需要处理一些精细点(如 untrusted Charlie 的 classical announcement 是否可以帮 Alice-Bob 做出 trusted 情形下不可行的事)

**致命后果**:FINDINGS [COROLLARY] 级的分级,是在**把未经文献定理级支持的推理链伪装成定理推论**。这恰好是 PROSPECTUS §9 诚信红线要防的。

### 1.2 **形式表述让上界**读起来像**PLOB 误用**[严重 — 表述层]

- FINDINGS §1.1 公式 $R \leq -\log_2(1 - \sqrt{\eta_{AB}})$
- **PLOB 主定理的 $\eta$ 是 Alice-Bob 端到端透过率**,不是分段
- 上述公式 **字面上像** "把 PLOB 的 $\eta$ 替换成 $\sqrt{\eta_{AB}}$",这是**明显的拓扑误用** ——  同样的公式在 3-节点 TF-QKD 拓扑下有另外的合法推导路径(min-cut),但 FINDINGS **没在正文做出该区分**
- 读者(包括人类 reviewer + 未来的我)读这句会把它当作 PLOB 误用 → **与 AI4QKD v1 的"自编公式"错误模式同构**

### 1.3 **文献共识 $\neq$ 定理**[中等]

- "TF-QKD 社区普遍认为 $\sqrt{\eta}$ 是 single-repeater bound" 是文献**共识术语**,但:
  - 在 literature 里,**TF-QKD 的 $\sqrt{\eta}$ 一般被描述为 achievability / lower bound**,不是来自严格 converse 证明的 upper bound
  - "surpassing PLOB bound" 的陈述反复出现,意指超越 **$\eta$ 线性界**(点对点),不意指 $\sqrt{\eta}$ 本身是 converse 得到的严格 upper bound
- FINDINGS 把这个文献共识等同于"定理级 upper bound 已证",**越界半档** —— 应该是 [SYN] 级,不能是 [COROLLARY] 级

### 1.4 **四轮 Phase V 审计未能抓住这一物理问题**[元问题]

- V1 逻辑自审:检查符号 / 循环 / 假设遗漏,**未质疑 Pirandola19 适用性**
- V2 文献交叉:WebSearch 核对公式,**未深究 untrusted vs trusted 的适用区分**
- V3 反例搜索:搜索超 $\sqrt{\eta}$ scaling 的协议,**未反向搜索 untrusted-case upper bound 的专门文献**
- V4 codex 独立评审:**codex 也没质疑 untrusted relay 适用性** —— codex 和 Claude 可能共享相似的训练数据偏差

**失败模式**:**多层 AI 审计在"文档一致性 / 引用格式 / 逻辑闭合"层检查,但没有一个真正独立地**从物理定理内容出发**质疑拓扑适用性**。

这与 **AI4QKD v1 的失败模式同构**:v1 用漂亮的软件外壳(RL + 仿真器)掩盖评估层不严格;这份 FINDINGS 用漂亮的流程外壳(Phase R + Phase V)掩盖对**关键物理定理适用性的真实核对缺失**。

### 1.5 **越权"关闭"了 PROSPECTUS Sub-Q3 工作**[方法论]

- PROSPECTUS v3.1 §6 Sub-Q3 明确是 **30-50 页 PLOB 精读 + 应用到我们的拓扑** 的工作,归 Phase 2(6-12 个月)
- FINDINGS 在一天内用 literature synthesis 宣称"scaling 层面已解决,情况 A",这**等同于把 Sub-Q3 的结论在没做 Sub-Q3 的工作的情况下"提前公布"**
- 即便**偶然猜对了**(scaling 真的是 $\sqrt{\eta}$),这个越权关闭也**破坏了 PROSPECTUS §6 的研究节律与 §9 的诚信承诺**

---

## 2. **可能仍然是对的**的部分

做负面清单的同时,也记录下什么**仍然可能站得住**,供 Sub-Q3 未来参考:

### 2.1 Scaling 预判

**[CONJ,非 [SYN]]**:$\sqrt{\eta_{AB}}$ 是 $\mathcal{T}_{\text{umr}}$ 对称拓扑下的**最可能的紧 scaling**。

**理由**:

- TF-QKD / PM-QKD / MP-QKD 族 achievability 为 $\sqrt{\eta}$ [THM]
- 所有 2018-2025 文献中没有 $\mathcal{T}_{\text{umr}}$ 协议 beat $\sqrt{\eta}$ 的报道 [SYN]
- Pirandola 2019 trusted-case min-cut 给 $\sqrt{\eta}$ [THM],untrusted 情形按 capacity monotonicity 直觉 $\leq \sqrt{\eta}$ [CONJ,无严格定理]

**关键警示**:这不是**证明**情况 A 成立。这是"最可能的情况 A",但 B / C 在严格意义下**没被排除**,PROSPECTUS 主问题**仍然开放**。

### 2.2 Case B 的排除(由下界侧)

**[THM 级]**:若 PROSPECTUS 情况 B 严格按字面解读($\alpha \in (1/2, 1)$,即 rate $\lesssim \eta^\alpha < \sqrt{\eta}$),则与 TF-QKD 已达 $\sqrt{\eta}$ 矛盾。这个推理只依赖 Lucamarini 2018 achievability [VERIFIED],无 converse 上界依赖,**保持有效**。

情况 B 在这种读法下**确实被排除**。但如果 PROSPECTUS 作者的意图是"$\alpha < 1/2$"(即更优 scaling),那排除需要上界工作,**不能靠当前 FINDINGS**。

### 2.3 Log 01-05 的文献地图部分

Logs 01-05 的**文献地图 + 引用清单**仍有 Phase 2 Sub-Q3 工作的起点价值 —— 它们列清了需要精读的论文、定理、可能的推理路径。这部分不撤回,但**不能代替 Sub-Q3 的实际精读报告**。

---

## 3. **状态复位清单**

### 3.1 文件状态

| 文件 | 原状态 | 新状态 |
|------|--------|--------|
| [FINDINGS.md](FINDINGS.md) | 最终答案 | **[RETRACTED]** — 加顶部警告,保留原文供审计 |
| [FINDINGS_DRAFT.md](FINDINGS_DRAFT.md) | Phase R 初稿 | **[RETRACTED]** — 同上 |
| [V1_logical_selfaudit.md](V1_logical_selfaudit.md) | PASS | **[FAILED in retrospect]** — 未抓住物理拓扑误用 |
| [V2_literature_crosscheck.md](V2_literature_crosscheck.md) | PASS | **[INSUFFICIENT]** — 仅核了公式,未核定理适用性 |
| [V3_counterexample_hunt.md](V3_counterexample_hunt.md) | PASS | **[UNDIRECTED]** — 反例搜的是下界方向,未反向搜 upper-bound 文献 |
| [V4_codex_independent.md](V4_codex_independent.md) | NEEDS_REVISION → 修订后 PASS | **[INSUFFICIENT]** — codex 未独立质疑物理拓扑,与 Claude 同偏差 |
| Logs 01-05(文献地图)| Phase R 研究日志 | **[PARTIAL VALUE]** — 保留作 Sub-Q3 起点,**不作 Sub-Q1 答案** |
| Log 06(Gap 结构分析)| Phase R | **[RETRACTED on conclusion]** — 结论"scaling gap = 0,情况 A"撤回,中间观察可部分保留 |

### 3.2 主问题状态

| PROSPECTUS 问题 | 撤回前状态 | 撤回后状态 |
|-----------------|-----------|-----------|
| §1 主问题 A / B / C | "情况 A 成立(条件化 COROLLARY)" | **"开放研究问题,归 Sub-Q3 Phase 2"** |
| Sub-Q3 上界工作 | "被 FINDINGS 预先部分回答" | **"完整开放,未开始"** |
| Sub-Q4 gap 归因 | "γ(两端都松)的预判" | **"撤回,Sub-Q4 启动需在 Sub-Q3 完成后"** |

### 3.3 对 PHASE0_M1 的影响

- **M1-M4 验收计划不变** — 数值验证 TF-QKD 的 $\sqrt{\eta}$ scaling 仍然有价值(achievability 侧),不受 FINDINGS 撤回影响
- **REFACTORING_PLAN §5 M4B 的"log-log 斜率 = 0.5 ± 0.05"** 仍是合法验收标准(TF-QKD 的 achievability)
- **但不得基于 FINDINGS §5 的"即时行动建议"做任何调整** —— 那几条建议(Sub-Q3 工作重心预定位、Sub-Q4 归因预设 γ)都是基于已撤回的结论

---

## 4. **用户审查意见的元教训**

### 4.1 AI 协作产物的授信边界

PROSPECTUS §9 写的"AI 工具的角色是'信息整理者 + 结构化讨论伙伴',不是权威来源"**在本案例中未被严格执行**。FINDINGS.md 被 Claude 自动落盘并 commit 时,没有经过项目负责人的审阅签字。

**修订后的授信规则**(写入后续 RESEARCH_PLAN / 下一个 ADR):

1. 任何 AI 产出的**结论性文档**(FINDINGS / 最终报告 / 答案声明)**必须**经过项目负责人显式 review + ok 后才能 commit 为"最终"状态
2. AI 产出的**过程性文档**(logs / drafts / 引用合成)可以自动 commit,但文件头必须显式标 `[AI-DRAFT, NOT HUMAN-REVIEWED]`
3. AI 产出的**多层审计流程**(Phase V 类)**不计入** "独立验证" —— 除非每一层审计包含**来自不同训练偏差源的独立人类或工具**
4. Commit message 必须显式说明"是否经过人类审阅",不允许 Co-Authored-By 单独作为"signed off"的替代

### 4.2 文献适用性核对的刚性要求

任何引用的上界 / 下界 / converse / achievability 定理,必须显式核对:

1. 定理的**拓扑前提**是否匹配当前应用
2. 定理的**信任假设**是否匹配(trusted / untrusted / semi-honest 区分)
3. 定理的**协议自由度前提**是否匹配(有 / 无量子存储、是 / 否 LOCC 限制)
4. **以上任何一条不匹配,必须有定理级的"继承"或"单调性"论证,不能靠直觉**

这条规则将被加入 [RESEARCH_PLAN §1.2 验收机制](RESEARCH_PLAN.md#12-验收机制反-ai4qkd-v1-失败模式) 作为补丁。

### 4.3 "多 AI cross-audit 不等于独立验证"

Claude + codex + 其他 LLM 即便独立部署,**仍可能共享训练语料偏差**。尤其对 QKD 这种**有共识术语(如 "single-repeater bound")但 converse 证明细节分散**的领域,所有 AI 容易**默认 scaling 共识等于定理成立**。

真正独立的验证渠道:

- **人类 QKD 专家审阅**(最权威)
- **直接 PDF 阅读 + 重推关键定理**(Sub-Q3 Phase 2 要做的工作)
- **针对关键定理的反向 specialist 论文搜索**(搜 "upper bound untrusted relay" 而非 "TF-QKD sqrt eta")

---

## 5. **给后续工作的承诺**

- 按 PROSPECTUS §6 原计划,Sub-Q3 Phase 2 **从零起步**,不以 FINDINGS 的结论为起点
- Sub-Q3 精读必须**实际阅读 Pirandola 2017 + Pirandola 2019 的 PDF**,核对定理编号 + $\eta$ 定义 + 拓扑前提,不能靠综述二手引用
- 在 Sub-Q3 完成之前,**不得**在任何论文 / 报告 / 对外展示中**陈述 "PROSPECTUS 主问题情况 A 已被确定"** 或等价表述
- 若 Sub-Q3 完成后确实得出"情况 A"结论,那份报告(而非本 FINDINGS)是合法来源

---

## 6. 本 RETRACTION 的自我检查

- [x] 明确标出被撤回文件
- [x] 列出撤回理由(不只是一条,而是 5 条 + 元问题)
- [x] 区分"已撤回"与"部分仍可用"的内容
- [x] 状态复位到 PROSPECTUS Sub-Q3 启动前的位置
- [x] 不试图保全 FINDINGS 的任何"关键结论"作为"scaling 预判仍可能对"以外的陈述
- [x] 记录方法论教训,作为 RESEARCH_PLAN §1 的补丁
- [x] 给后续工作明确承诺

---

## Changelog

- **v1.0**(2026-04-19):首次落盘。作为 [FINDINGS.md](FINDINGS.md) v1.0 的正式撤回声明。

---

*RETRACTION 结束。FINDINGS 状态:已撤回。Sub-Q3 状态:开放,未开始。*
