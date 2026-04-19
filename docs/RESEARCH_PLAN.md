# Research Plan v1.0:Phase 0–3 研究执行计划

**文档状态**:v1.0 首次落盘(2026-04-18)
**适用范围**:按 [PROSPECTUS.md](PROSPECTUS.md) v3.1 的 Sub-Q1→Sub-Q4 展开可执行研究动作
**目标读者**:主研究者 + codex 评审 + 未来 PR reviewer

> **文档在文档树中的位置**:
> - [PROSPECTUS.md](PROSPECTUS.md)(v3.1):研究地图,说 **WHY**(主问题、约束、Sub-Q 序列)
> - **本文档(RESEARCH_PLAN.md)**:研究执行计划,说 **HOW-TO-DO-RESEARCH**(文献阅读序列、证明精读任务、数值实验设计、研究 deliverable 验收标准、周度节律)
> - [REFACTORING_PLAN.md](REFACTORING_PLAN.md)(v3.1.4):实施规范,说 **HOW-TO-BUILD**(模块 API、测试、里程碑硬验收、运营控制)
>
> 三者关系:Prospectus 定方向 → 本文档把方向拆成研究动作 → Refactoring Plan 把研究动作对应的代码工程严格化。
>
> 数字冲突裁决:工期/里程碑数字以 [REFACTORING_PLAN.md §5](REFACTORING_PLAN.md) 为准(经 codex 六轮审计)。

---

## 0. TL;DR

- **Phase 0(必需 12 周,+ M4B 可选 2–3 周 → 总预算 12–16 周)**:完成 Sub-Q1(MS-EB 框架 + WLC SDP 评估工具链)+ 启动 Sub-Q2 family sheet。必需路径 M1–M3 + M4A + Phase 0 集成(§2.5),可选路径 Phase 0.5 M4B(§2.7)。实施细节见 REFACTORING_PLAN §5。
- **Phase 1(3–4 个月)**:完成 Sub-Q2 family sheets + GEAT 有限密钥层 + 启动 Sub-Q3(PLOB 精读)。
- **Phase 2(6–12 个月)**:完成 Sub-Q3 + 上界 SDP 工具链 + 启动 Sub-Q4(gap 刻画)。
- **Phase 3(12+ 个月)**:完成 Sub-Q4,给出主问题的情况 A/B/C 判定,根据结论决定后续方向。

**本文档的定位**:不重写 Prospectus 的"要做什么",也不复述 Refactoring Plan 的"怎么建代码",而是填中间层 —— **"研究动作序列怎么排、每周做什么、产出怎么验收"**。

---

## 1. 研究方法论(红线)

### 1.1 三类研究动作

本项目的研究工作全部可归为以下三类动作之一。每个动作有明确的输入、产出、验收标准。

| 动作类型 | 典型输入 | 典型产出 | 验收 |
|---------|---------|---------|------|
| **文献精读** | 一篇论文 + 相关预备文献 | `literature/<paper_tag>.md`,含概念地图、关键证明的逐步重现、与本项目的 bearing | 能在 1 小时内向另一个研究者口述论文的核心论证 |
| **数值实验** | 协议对象 + 参数扫描规格 | Jupyter notebook + 图表 + 结论 memo | 结果与文献已知值对比,误差在验收范围内;notebook 在 clean venv 中 `papermill` 一键复现 |
| **证明 / 推导** | 需要解决的命题 | `proofs/<topic>.md`,含假设、推理链、反例检查 | 关键推理步骤可独立验证;至少有一个数值 sanity check |

### 1.2 验收机制(反 AI4QKD v1 失败模式)

所有"新发现"类型的产出(改进 c、新协议、更紧上界等)必须满足:

1. **WLC SDP 核验**(下界结果):协议必须在 MS-EB 下严格书写,密钥率必须由 `qkdx.numerics.wlc.wlc_key_rate()` 给出,不使用自编公式
2. **文献交叉验证**:在已知协议上,数值结果必须与至少一篇原始文献的数值对比,误差阈值遵循 `REFACTORING_PLAN §9(4) + §11.4` 的双轨政策:
   - **MOSEK 主线**:`pytest.approx(rel=0.01, abs=5e-4)`,**不放宽**
   - **CLARABEL / SCS fallback**:`pytest.approx(rel=0.02, abs=1e-3)`,且必须在测试或 memo 中显式标注 `@pytest.mark.fallback_solver` 或文本 "(CLARABEL fallback)"
   - 其他阈值选择必须附 ADR(`docs/adr/NNNN-*.md`)

**2b. 定理拓扑适用性核对**(**v1.1 补丁 2026-04-19,应 `docs/research/RETRACTION.md` §4.2 要求**):

任何引用的上界 / 下界 / converse / achievability 定理,在 memo / 报告 / FINDINGS 中使用前,**必须**显式核对:

- **(i) 拓扑前提**:定理的原始拓扑(点对点 / 单中继 / 网络 / 多端点)与当前应用的拓扑是否一致?不一致时,**继承需要独立论证**
- **(ii) 信任假设**:定理对中间节点的信任要求(trusted / untrusted / semi-honest / adversarial)与应用情形是否一致?**不一致时不得直接引用**
- **(iii) 协议自由度**:量子存储 / 仅 LOCC / 允许跨轮等前提是否一致?
- **(iv) 定理编号 + 方程号 + 页码**:引用必须精确到论文中具体位置,不能只写论文标题

**任何上述四条之一不匹配,必须有显式的"继承 / 单调性 / 适用性 lemma",不能靠直觉或 "capacity monotonicity implicit argument"**。

违反本条的结论属于 [SYN] 或 [CONJ] 级,**不得**标 [THM] 或 [COROLLARY]。
3. **独立复现**:关键数值结果应由第二套实现独立复现(可以是:另一个求解器、手动推导子情形、第三方代码)
4. **Limitations 显式化**:任何 memo / 论文初稿都必须有 Limitations 小节,明确框架假设、数值精度、不 covered 的 cases

**红线**:违反上述任一条的结果,不得纳入 `docs/findings/` 或对外展示。

### 1.3 文献阅读深度分级

```
Level 1  概览性阅读  —— 读 abstract + intro + conclusion,理解论文在做什么,不做证明细节
Level 2  选读       —— Level 1 + 2–3 个关键章节,理解主方法,能复述 proof sketch
Level 3  精读       —— Level 2 + 全文证明每一步,写 literature/<paper_tag>.md 记录概念地图 + 关键 lemma 的逐步重现
Level 4  重推      —— Level 3 + 独立推导核心定理(至少关键 lemma),手算或数值验证一个子情形
```

Sub-Q3 的 PLOB 精读要求 Level 4;Sub-Q2 的已发表 family sheet 参考通常 Level 2-3;背景综述 Level 1 即可。

### 1.4 每周节律

- **周一**:读上周进度报告,明确本周任务(更新 `ROADMAP.md`)
- **周二-周四**:主研究动作
- **周五**:写周报(`conversations/weekly/YYYY-WNN.md`),含:完成项、阻塞、下周计划、测试状态、文献阅读进度
- **每 2 周**:跑一次 `codex exec -s read-only` 评审当周产出的新文档/新代码
- **每个 Milestone 完成**:PHASE0_REPORT.md / PHASE1_REPORT.md 的对应小节定稿,包含数值图表 + Limitations + 下阶段计划

---

## 2. Sub-Q1 研究动作分解(Phase 0,M1–M4)

**对应 Prospectus §6 Sub-Q1**:MS-EB 框架能否统一表达无中继 DV-QKD 协议?

**对应 Refactoring Plan 实施模块**:§4.1–§4.6 + §4.13 + 附录 B(WLC SDP)

### 2.1 M1(3 周):WLC SDP 在 BB84 上的最小实现

**研究动作 R1.1:Winick-Lütkenhaus-Coles 2018 Level 4 精读**(Week 1 前半)

- 输入:`Winick, Lütkenhaus, Coles (2018). Reliable numerical key rates for QKD. Quantum 2:77` + arXiv:1710.05511
- 产出:`docs/literature/WLC-2018.md`,包含:
  - §2 MS-EB 框架(与 Coles-Metodiev-Lütkenhaus 2016 的关系)
  - §3 SDP 形式:目标函数 `D(𝒢(ρ) ‖ 𝒵(𝒢(ρ)))` 的推导(从 Devetak-Winter 到 WLC)
  - §4 观测约束 Γ_k = γ_k 的构造
  - §5 primal / dual 及 gap 的 sanity check
  - §6 在 BB84 上的 benchmark 数据
- 验收:能独立写出 BB84 的 WLC SDP(变量维度、约束列表、目标函数),并用手算 QBER=0 情形的密钥率 = 1 bit/sift

**研究动作 R1.2:MS-EB 五元组在 BB84 上的书写**(Week 1 后半)

- 输入:R1.1 + Prospectus §4 MS-EB 定义
- 产出:`docs/msen/bb84-formulation.md`,包含:
  - 🗡 $\mathcal{P}$:Alice 的 EB 态 $|\psi\rangle_{AA'} = \frac{1}{2}\sum_{x,\theta}|x,\theta\rangle_A \otimes U_\theta|x\rangle_{A'}$
  - $\mathcal{E}$:量子信道 $\mathcal{E}_\text{ch}$(去极化模型) + Bob 的 POVM → classical outcome
  - $\mathcal{A}$:公开 $\theta_A, \theta_B$,`sift_keep = (θ_A == θ_B)`
  - $\mathcal{T}$:接受 QBER ≤ threshold
  - $\mathcal{K}$:Alice 的 $x \in \{0,1\}$ 作为最终密钥比特
- 验收:上述 5 个对象能被 `qkdx.protocol.base.MSEBProtocol` 构造,且 `joint_state()` / `executed_state()` / `conditional_alice_bob()` / `conditional_alice_bob_dim()` / `observable()` 均可调用

**研究动作 R1.3:WLC SDP 实现 + BB84 benchmark**(Week 2–3)

- 输入:R1.1 + R1.2 + Refactoring Plan §4.6 + 附录 B 伪代码
- 产出:
  - `qkdx/numerics/wlc.py` 通过 Refactoring Plan §4.6 的全部测试
  - `notebooks/m1_wlc_bb84.ipynb`,包含六个 QBER 点的 R(QBER) 曲线与 Shor-Preskill 解析对比图
  - `docs/findings/m1_wlc_bb84.md`,M1 验收 memo(5-8 页)
- 验收(硬):`test_wlc_bb84_matches_shor_preskill` 全部通过,MOSEK 主线 `rel=0.01, abs=5e-4` / CLARABEL fallback `rel=0.02, abs=1e-3`(§1.2);覆盖率达到 Refactoring Plan §5 M1 要求

**研究动作 R1.4:框架覆盖与 out-of-scope 标注机制**(Week 3,与 R1.3 并行)

- 动机:PROSPECTUS §6 Sub-Q1 (d) 明确要求"对框架覆盖不到的协议类型,能在 MS-EB 元数据中显式标注 out of scope"
- 输入:`MSEBProtocol` 数据类(见 Refactoring Plan §4.4)
- 产出:
  - `docs/framework_coverage.md`:covered / partial / out_of_scope 协议类型对照表,含每个 out_of_scope 协议的原因(如 "需要跨轮自适应 $\mathcal{E}$,违反 MS-EB 单一 $\mathcal{E}$ 假设")
  - `MSEBProtocol` 元数据字段扩展:`scope_tag: Literal["covered", "partial", "out_of_scope"]` + `scope_reason: str | None`(若非 covered)
  - 拒收机制:`MSEBProtocol.__post_init__` 在 `scope_tag == "out_of_scope"` 时发 `OutOfScopeWarning`,阻止自动下游 SDP 派生
- 验收(硬):
  - BB84 / 六态标注 `covered`;MDI 标注 `partial`(base-class multi-source state queries not implemented,WLC SDP via `_conditional_alice_bob` override works — see `qkdx/protocols/mdi.py` scope_reason);TF-QKD 在 M4B 完成前标注 `partial`
  - 引入一个 toy "跨轮自适应协议"单测,确认 out_of_scope 被拒收并记录原因
  - `framework_coverage.md` 对 Prospectus §4.2 的七个主流协议族每族标注至少一个代表性协议

**时间分配**:精读 3 天 + MS-EB 书写 4 天 + 实现 7 天 + R1.4 coverage 机制 2-3 天 + 数值调优 + memo 撰写 4-5 天。

### 2.2 M2(2 周):扩展到 MDI-QKD 和六态

**研究动作 R2.1:Lo-Curty-Qi 2012 + Ma-Razavi 2012 Level 3 精读**(Week 4 前半)

- 输入:MDI-QKD 原论文 + 数值基线论文
- 产出:`docs/literature/MDI-QKD.md`,含:
  - Lo-Curty-Qi 2012 的安全性证明(entanglement swapping 的 argument)
  - Ma-Razavi 2012 的诱骗态扩展 + 数值 Fig.3 的参数
- 验收:能独立写出 MDI-QKD 的 MS-EB 五元组,特别是 $\mathcal{E}$ 含 Charlie 的 Bell 测量

**研究动作 R2.2:Bruss 1998(六态)Level 2 精读**(Week 4 后半)

- 输入:`Bruss, D. (1998). Optimal eavesdropping in QKD with six states. PRL 81:3018`
- 产出:`docs/literature/six-state.md`,主要为渐近密钥率公式 $1 - h(QBER) - QBER \log_2 3$ 的推导
- 验收:能手算 QBER=0.05 的六态密钥率,与 BB84 做比较

**研究动作 R2.3:MS-EB 书写 + 数值验证**(Week 5)

- 产出:
  - `docs/msen/mdi-formulation.md` + `docs/msen/sixstate-formulation.md`
  - `qkdx/protocols/mdi.py` + `qkdx/protocols/sixstate.py` + `qkdx/analytic/six_state.py` + `qkdx/analytic/gllp.py`
  - `notebooks/m2_wlc_mdi_sixstate.ipynb` 含数值对比图
- 验收(硬):
  - 六态数值 vs 解析误差 `rel=0.01, abs=5e-4`
  - MDI 理想 vs GLLP ideal symmetric 误差 `rel=0.01, abs=5e-4`(**M2 范围**)
  - `numerics/wlc.py` 仅**加法式**修改(只新增可观测算子 builder,BB84 基线零回归)
- 延后验收(**M2 不闭合,Phase 1 Sub-Q2 / M3+ 承接**):
  - **Ma-Razavi 2012 Fig.3 对齐**:依赖 decoy + asymmetric loss,需要 Phase 1 Sub-Q2 MDI family sheet + 完整 decoy + channel loss 模型;M2 仅交付 ideal GLLP baseline,不解锁 Ma-Razavi 距离扫描对比(Agent 2 retrospective review 2026-04-19 findings)

### 2.3 M3(3 周):数值诱骗态分析

**研究动作 R3.1:诱骗态基础文献精读**(Week 6)

- 输入(按阅读顺序):
  1. `Hwang 2003` / `Wang 2005` / `Lo-Ma-Chen 2005`(诱骗态三论文之一,Level 2)
  2. `Ma-Qi-Zhao-Lo 2005`(解析基线,Level 3)
  3. `George-Lin-Lütkenhaus 2020/2021`(数值诱骗,Level 4 精读,**重点**)
- 产出:`docs/literature/decoy-state.md`,含:
  - 经典诱骗态的单光子下界公式
  - 数值诱骗态的 SDP 形式
  - 两者在 2-intensity 和 3-intensity 情形的差距
- 验收:能独立推导 2-intensity decoy 下的 $Y_1^L, e_1^U$

**研究动作 R3.2:Hu-Im-Lin-Lütkenhaus-Wolkowicz 2022 Level 4 精读**(Week 7)

- 输入:`Hu et al. 2022. Robust Interior Point Method for QKD Rate Computation. Quantum 6:792`
- 产出:`docs/literature/facial-reduction.md`,含:
  - facial reduction 的 Krantz-Wolkowicz 经典背景
  - 在 WLC SDP 中的应用位置(特别是 QBER=0 情形)
  - 算法流程(dual infeasibility detection → face projection → reduced problem)
- 验收:能在 BB84 QBER=0 的 toy case 上手动做 facial reduction,得到降秩后的 2×2 SDP

**研究动作 R3.3:数值诱骗 + facial reduction 实现**(Week 8)

- 产出:
  - `qkdx/numerics/decoy.py` + `qkdx/numerics/facial.py`
  - `notebooks/m3_decoy_distance_sweep.ipynb`,距离扫描 20–200 km
  - `docs/findings/m3_decoy.md` memo
- 验收(硬):单 decoy 数值 vs Ma 2005 解析 `rel=0.01, abs=5e-4`;两 decoy 数值 ≥ 解析 − 1e-4;距离扫描与 Lo-Ma-Chen 2005 Fig.3 视觉一致

### 2.4 M4A(2 周):对称性约化

**研究动作 R4A.1:Ferenczi-Lütkenhaus 2012 Level 3 精读**(Week 9)

- 输入:`Ferenczi, Lütkenhaus (2012). Symmetries in QKD. PRA 85:052310`
- 产出:`docs/literature/symmetry.md`,含:
  - Clifford 群平均在 BB84 的作用(dim 4 → dim 2 SDP 降维)
  - Werner state 作为 symmetry-reduced state 的 canonical 形式
- 验收:能手算 Clifford twirling 把 BB84 的 4×4 ρ 降到 2×2

**研究动作 R4A.2:symmetry/groups + twirling 实现**(Week 10)

- 产出:`qkdx/symmetry/groups.py` + `qkdx/symmetry/twirling.py`
- 验收(硬):Clifford 约化 BB84 的 SDP 变量从 4×4 降到 2×2,`rel=0.01, abs=5e-4`;六态同理

### 2.5 Phase 0 集成与复现报告(Week 11–12,**不依赖 M4B**)

**研究动作 RI.1:Phase 0 总报告**

- 产出:`docs/PHASE0_REPORT.md`(8–12 页 memo),含:
  - M1/M2/M3/M4A 每个里程碑的验收证据截图 + 数值表格(**此处不含 M4B**,见 §2.7)
  - Framework Coverage Report(Prospectus Sub-Q1 (d) 的产出,见 §2.1 R1.4)
  - 复现 Winick 2018 Fig.3 的 pipeline
  - Limitations:已识别的框架裂缝、数值不稳处、未解问题
  - Phase 0.5 M4B 启动准备清单(若决定继续做 TF-QKD) + Phase 1 启动准备清单
- 验收(硬):Refactoring Plan §5 "Phase 0 总验收"(必需范围)全部通过,独立于 M4B

### 2.7 Phase 0.5(可选):M4B TF-QKD 验收(Week 13–15,2–3 周)

> **可选性说明**:M4B 不在 Phase 0 必需关键路径(Refactoring Plan §5);如果 Phase 0 集成已通过验收,M4B 可以(a)继续进行、(b)延后启动、(c)降级为 Phase 1 首轮工作。选择基于 Phase 0 集成报告中识别的风险与资源情况。

**研究动作 R4B.1:TF-QKD 族核心文献精读**(Week 13)

- 输入(按顺序):
  1. `Lucamarini et al. 2018 Nature`(Level 3 — TF-QKD 原论文)
  2. `Ma-Zeng-Zhou 2018 PRX`(PM-QKD, Level 3)
  3. `Wang-Yu-Hu 2018 PRA`(SNS-TF,Level 2)
  4. `Zeng-Zhou-Wu-Ma 2022 Nat.Commun.`(MP-QKD,Level 2)
- 产出:`docs/literature/TF-QKD.md`,含各 TF 变体的关键差异、$\sqrt{\eta}$ 标度来源、phase reference 的工程处理
- 验收:能独立画出 TF-QKD 的 R(η) 曲线草图(log-log 斜率 = 0.5)

**研究动作 R4B.2:TF-QKD 的 MS-EB 书写 + 数值验证**(Week 14–15)

- 产出:`docs/msen/tfqkd-formulation.md` + `qkdx/protocols/tfqkd.py`
- 验收(硬):log-log 斜率 = 0.5 ± 0.05(Refactoring Plan §5 M4B)
- **风险标注**:若 TF-QKD 的 phase reference 在 MS-EB 下不自然,M4B 降级为"decoy finite-key 扩展"(Refactoring Plan §8 R3)

---

## 3. Sub-Q2 研究动作分解(Phase 0 末–Phase 1)

**对应 Prospectus §6 Sub-Q2**:已知协议族的紧密钥率下界 Pareto 前沿

### 3.1 协议族参数化(Phase 1 Week 1–3)

**研究动作 S2.1:协议族变体清单**

- 输入:Sub-Q1 已建成的 `qkdx/protocols/`(BB84, MDI, TF)
- 产出:`docs/families/` 三份 family sheet 草稿:
  - `bb84_family.md`:BB84 + 六态 + SARG04 + Efficient BB84 + 偏置基选择
  - `mdi_family.md`:基本 MDI + decoy MDI + polarization encoding + time-bin encoding
  - `tfqkd_family.md`:TF + SNS-TF + PM-QKD + MP-QKD + (decoy variants)
- 每个 family sheet 含:族成员列表、参数空间描述、MS-EB 下的参数化方式
- **验收(硬)**:每份 family sheet 必须包含:
  1. **参数边界表**:每个可调参数的 `(name, type, range, default, physical meaning)` 五元组
  2. **合法性约束**:参数组合的约束条件(如 `0 < μ_decoy < μ_signal ≤ 1`)
  3. **参数 → MS-EB 映射**:对每个变体,给出从参数到 `MSEBProtocol` 五元组各分量的显式映射函数(`build_*_protocol(...)` 签名 + docstring)
  4. 三份 family sheet 均通过**同一检查清单**`docs/families/_checklist.md`

### 3.2 Pareto 前沿数值化(Phase 1 Week 4–8)

**研究动作 S2.2:每个族内 Pareto 搜索**

- 方法:Bayesian optimization(`scikit-optimize`)或 CMA-ES(`cma` 库),**不用深度学习**(Phase 0 规则)
- 输入:WLC SDP 评估器(from Sub-Q1)
- 产出:每个族的 Pareto 前沿数据 + 最优参数 + 图表
- 验收:
  - 每个族能在参数空间扫 ≥ 1000 个点
  - Pareto 前沿的上包络点被记录在 `docs/findings/pareto_<family>.md`
  - 族间比较图(BB84 vs MDI vs TF 在 (η, R) 平面)

**研究动作 S2.3:器件不完美模型引入**

- 输入:探测器效率 $\eta_d$、dark count $p_d$、basis bias、misalignment
- 产出:`qkdx/protocols/device_imperfections.py`(轻量,只改信道 Kraus)
- 验收:在 `η_d = 0.5, p_d = 1e-6` 典型参数下,BB84 族的 Pareto 前沿对比理想场景能体现 20-50% 的退化

### 3.3 GEAT 有限密钥层(Phase 1 Week 9–14)

**研究动作 S2.4:Metger-Fawzi-Sutter-Renner 2024 Level 4 精读**

- 输入:`Metger et al. 2024. Generalised entropy accumulation. CMP 405:261`
- 产出:`docs/literature/GEAT.md`,含:
  - GEAT 定理的假设清单(NSP 条件、Markov chain)
  - 与原始 EAT(Dupuis-Fawzi-Renner 2020)的对比
  - 在 QKD 协议上的适用路径
- 验收:能独立推导一个简化 NSP 条件的验证

**研究动作 S2.5:GEAT 实现 + Kamin 2025 复现**

- 输入:`Kamin et al. 2025. Finite-Size Analysis...PRX Quantum 6:020342`
- 产出:
  - `qkdx/finite_key/` 模块
  - `notebooks/s2_kamin_reproduce.ipynb`
  - Kamin 2025 关键数值 ± 5% 复现
- 验收(硬):对 decoy-state BB84,有限密钥率(给定 n, ε_sec, ε_corr)与 Kamin 2025 Fig. 4 / Table 1 误差 < 5%

### 3.4 Sub-Q2 总结报告(Phase 1 末)

**产出**:`docs/PHASE1_REPORT.md` + 三份 family sheet 定稿 + 整合的 "DV-QKD 协议族地图"(一张 overview 图)

---

## 4. Sub-Q3 研究动作分解(Phase 1 末–Phase 2 中)

**对应 Prospectus §6 Sub-Q3**:已知上界工具在 MS-EB 框架下给出什么上界?

**注意**:本节工作量最大、时间最长(3–5 个月),是 Phase 2 主要产出。

### 4.1 PLOB 及其前传(Phase 2 Week 1–6)

**研究动作 U3.1:Takeoka-Guha-Wilde 2014 Level 3 精读**

- 输入:`Takeoka, Guha, Wilde 2014. Fundamental rate-loss tradeoff. Nat.Commun. 5:5235`
- 产出:`docs/literature/TGW-2014.md`,含 squashed entanglement 的引入
- 验收:能独立推导 TGW bound 的主要步骤

**研究动作 U3.2:Pirandola-Laurenza-Ottaviani-Banchi 2017 Level 4 精读**(重点!)

- 输入:`PLOB 2017. Fundamental limits of repeaterless quantum communications. Nat.Commun. 8:15043`
- 产出:`docs/literature/PLOB-2017.md`,**至少 20 页精读笔记**,含:
  - Teleportation simulation 的适用条件
  - Relative entropy of entanglement 的 additivity 在什么 channel 上成立
  - bosonic pure-loss 信道的 PLOB 证明逐步重现
  - 每个关键引理在 "untrusted relay" 拓扑下的 bearing(明确哪些成立,哪些不成立)
- 验收:能独立写出 PLOB bound 在纯损耗信道的 $-\log_2(1-\eta)$ 形式,并回答 "如果中间有一个 untrusted relay,这个 bound 还成立吗?"

**研究动作 U3.3:Wilde-Tomamichel-Berta 2017 Level 3 精读**

- 输入:`Wilde, Tomamichel, Berta 2017. Converse bounds for QKD. IEEE TIT 63:1792`
- 产出:`docs/literature/WTB-2017.md`,含独立于 PLOB 的 converse 推导
- 验收:能对比 PLOB vs WTB 两种证明路线在"两方 + untrusted relay"拓扑下的差异

### 4.2 网络推广与最新进展(Phase 2 Week 7–10)

**研究动作 U3.4:Pirandola 2019 网络推广 Level 3 精读**

- 输入:`Pirandola 2019. End-to-end capacities. Commun.Phys. 2:51`
- 产出:`docs/literature/Pirandola-2019.md`,识别"两方 + 单中间测量站"这个特定拓扑的上界陈述
- 验收:能对我们的拓扑写出该论文给出的 $R_{\text{UB}}(\eta)$ 表达式

**研究动作 U3.5:Das-Khatri-Wilde 2020 Level 3 精读**

- 输入:`Khatri, Wilde 2020. Principles of Quantum Communication Theory: A Modern Approach. arXiv:2011.04672`(综合 converse 框架教科书;替代此前误引 "DKW 2020 arXiv:2012.03262",该 ID 为不相关热力学论文)
- 产出:`docs/literature/DKW-2020.md`,含最新的 converse 改进
- 验收:能识别 DKW 相对 PLOB 的改进幅度及其对我们拓扑的可继承性

### 4.3 上界的 MS-EB 表述(Phase 2 Week 11–14)

**研究动作 U3.6:上界 MS-EB 重写**

- 输入:U3.1–U3.5 的所有精读笔记
- 产出:`docs/proofs/upper_bound_msen.md`,把文献中的上界翻译为:
  > 在 MS-EB 框架下,任何满足 §3.1 约束且具备 "两方 + 单 untrusted measurement relay + 纯损耗信道" 拓扑的协议 $\Pi$,必满足 $R(\Pi) \leq f(\eta)$
- 验收:$f(\eta)$ 是具体的、可数值计算的表达式,且有独立 sanity check

### 4.4 上界 SDP 的初步实现(Phase 2 Week 15–20)

**研究动作 U3.7:Relative entropy of entanglement 的 SDP**

- 数学对象:`qkdx/numerics/upper_bound.py`(新模块,Layer 5.3)
- 产出:对 toy channel(如 2-qubit 去极化信道)能计算 $R_E(\rho)$
- 验收:数值值与文献已知值对比(如 Vidal-Werner 02 的 $R_E$ 算法对比)

### 4.5 Sub-Q3 接缝报告(Phase 2 末)

**研究动作 U3.8:上界接缝报告**

- 产出:`docs/findings/upper_bound_report.md`,**30–50 页**,Prospectus Sub-Q3 验收要求
- 内容结构:
  - §1 PLOB 精读笔记(浓缩自 U3.2)
  - §2 各推广文献的 bearing 分析
  - §3 上界的 MS-EB 重写
  - §4 Layer 5.3 SDP 的实现与数值
  - §5 Limitations 与未解问题
- **验收(硬)**:
  1. **定理可追溯**:报告内每个上界结论(如 `R(Π) ≤ f(η)`)必须附原始论文的定理或方程号码(精确到 Theorem N / Eq. (M)),以及该定理的假设清单
  2. **可复现实验索引**:每个数值结果(包括 Layer 5.3 SDP 的 toy case)必须标注:
     - Notebook 路径(如 `notebooks/u3_plob_toy.ipynb`)
     - 运行命令(`papermill ...` 或等价调用)
     - 对应 `qkdx/` 代码的 git commit SHA
     - 求解器 + 版本 + seed
  3. §3 的 MS-EB 重写至少给出一条可计算的 `R_UB^current(η)` 表达式,且在 toy case 上数值非平凡

---

## 5. Sub-Q4 研究动作分解(Phase 2 下半–Phase 3)

**对应 Prospectus §6 Sub-Q4**:Gap 刻画 + 归因 A/B/C + 主问题答案

### 5.1 Gap 定量形状(Phase 2 末–Phase 3 Week 1–6)

**研究动作 G4.1:Gap 的数值计算**

- 输入:Sub-Q2 的 TF-QKD Pareto 下界 + Sub-Q3 的 $R_{\text{UB}}^{\text{current}}(\eta)$
- 产出:`notebooks/g4_gap_shape.ipynb`,给出:
  - $\text{gap}(\eta)$ 在 $\eta \in \{10^{-1}, 10^{-2}, ..., 10^{-6}\}$ 的离散值
  - 渐近行为的拟合(是 $\eta$?$\sqrt{\eta}$?常数?)
  - gap 最大处的 $\eta$ 定位
- 验收:能画出 log-log 下的 gap 形状曲线;识别 "gap 特别大"的 $\eta$ 区间

### 5.2 Gap 归因诊断(Phase 3 Week 7–14)

**研究动作 G4.2:归因三种原因的结构化诊断**

- 方法:
  - **对原因 A**(上界松):测试 PLOB/DKW 证明中"松弛处"——例如 teleportation simulation 的保守步骤、relative entropy 非 additive 时的上界放宽
  - **对原因 B**(下界松):测试 "TF-QKD 族参数空间是否已穷尽" —— 用 Sub-Q2 Pareto 扫描的残差判断
  - **对原因 C**:A 和 B 都非零
- 产出:`docs/findings/gap_analysis.md`(Prospectus Sub-Q4 验收产出)
- 验收:对三种原因给出可量化的贡献分解;对主问题答案给出情况 A/B/C 的初步判断

### 5.3 后续工作(Phase 3 后半)

根据 G4.2 的判断分叉:

**如果归因 A(上界松)**:

- 进入"改进证明"工作(纯理论)
- 产出:更紧上界的证明 memo + 可能的论文初稿
- 收敛:即使只把前因子收紧一个常数因子,也是成果

**如果归因 B(下界松)**:

- 启动 AI 搜索(此时第一次引入 AI,严格限定在 MS-EB 空间内)
- **搜索目标**由 gap 位置精确指定(例如 "在 $\eta=10^{-3}$ 处寻找密钥率 > $c\sqrt{\eta}$ 的协议")
- 产出:新协议候选 `docs/findings/new_protocols.md` + 其 MS-EB 书写 + WLC SDP 评估

**如果归因 C(上下都松)**:两条线并行

**极限情形**:如果最终 $R_{\text{UB}}^{\text{refined}} = R_{\text{LB}}^{\text{best}} = c^* \sqrt{\eta}$,则主问题答案为情况 A($\sqrt{\eta}$ 是紧上界),本项目**圆满收束**。

---

## 6. 文献阅读依赖图

### Phase 0 必读(按顺序)

```
[WLC 2018]  ────────────┐
                        ├───── M1 启动
[Shor-Preskill 2000]  ──┘

[Lo-Curty-Qi 2012]  ────┐
[Ma-Razavi 2012]  ──────┼───── M2 启动
[Bruss 1998]  ──────────┘

[Hwang 2003] ─┐
[Wang 2005] ──┤
[Lo-Ma-Chen 2005] ───────┤        ← M3 验收要求对齐其 Fig.3
[Ma-Qi-Zhao-Lo 2005] ────┼───── M3 启动
[George-Lin-Lütkenhaus 2020/2021] ──┤
[Hu et al. 2022 facial reduction] ──┘

[Ferenczi-Lütkenhaus 2012] ──── M4A 启动

[Lucamarini 2018] ──┐
[Ma-Zeng-Zhou 2018] ──┼── M4B 启动
[Wang 2018 SNS-TF] ──┤
[Zeng 2022 MP-QKD] ──┘
```

### Phase 1 必读(GEAT 栈)

```
[Renner 2005 PhD] ──(背景)── [Portmann-Renner 2022] ──(综述)──┐
[Tomamichel 2016 Smooth Entropy] ──(系统教材,smooth entropy 全景)─┤
[Dupuis-Fawzi-Renner 2020 EAT] ──────────────────────────────────┼── Sub-Q2.4/2.5
[Metger et al. 2024 GEAT] ───────────────────────────────────────┤
[Kamin et al. 2025] ─────────────────────────────────────────────┘
```

**阅读顺序提示**:Tomamichel 2016 作为 smooth entropy 的系统教材,是 EAT / GEAT 原论文的前置参考书。Level 2 选读 §4-§7(smooth min/max entropy + AEP)即可支撑 GEAT 精读。

### Phase 2 必读(上界栈)

```
[Takeoka-Guha-Wilde 2014] ──┐
[Vidal-Werner 2002 Rel. Entropy Entanglement] ──┤
[PLOB 2017] ──(重点!Level 4)──┼── Sub-Q3 上界工作
[Wilde-Tomamichel-Berta 2017] ──┤
[Pirandola 2019 网络] ──┤
[Khatri-Wilde 2020 textbook, arXiv:2011.04672] ──┘  # 替换此前误引 DKW 2020 / arXiv:2012.03262
```

---

## 7. Deliverable 模板

### 7.1 文献精读模板

`docs/literature/<paper_tag>.md` 固定结构:

```markdown
# <Paper Title> 精读(Level N)

**论文引用**:Author, Year, Journal, Volume:Page, arXiv:XXXX.YYYYY
**精读日期**:YYYY-MM-DD
**精读等级**:Level 1/2/3/4

## 1. 一句话总结

## 2. 概念地图(论文核心概念间的关系图)

## 3. 关键结果(定理/引理 + 推论)

## 4. 证明笔记(Level 3/4 必写)

### Lemma X 证明重现

## 5. 数值 / 图表理解(如有)

## 6. 与本项目的 Bearing

[特别针对 "两方 + untrusted relay + 纯损耗" 拓扑的 bearing]

## 7. Limitations / 未理解的地方

## 8. 下次读相关文献时需要带上的预备知识
```

### 7.2 Family Sheet 模板

`docs/families/<family>_family.md` 固定结构:

```markdown
# <Family Name> Family Sheet

**Family 范围**:<描述哪些协议属于这个族>
**Phase 0 覆盖协议**:<列表>
**未覆盖的族内协议**:<列表,及未覆盖原因>

## 1. MS-EB 下的族参数化

## 2. 族内 Pareto 前沿

### 2.1 数值结果(η ∈ ...,参数空间 ...)
### 2.2 Pareto 最优协议的参数值
### 2.3 对比:族内最优 vs 文献已发表最优

## 3. 有限密钥修正

## 4. 现实器件下的退化

## 5. 族内"意外发现"(如有)

## 6. Limitations
```

### 7.3 Findings Memo 模板

`docs/findings/<topic>.md` 固定结构:

```markdown
# <Finding> Memo

**日期**:YYYY-MM-DD
**研究动作**:R<N.M>(见 RESEARCH_PLAN §N)
**关联 Sub-Q**:Sub-Q<N>
**里程碑**:M<N>(如适用)

## 0. 复现元数据(必填)

- **代码版本**:git commit SHA(如 `abc1234`)
- **运行环境**:Python 3.X,CVXPY X.Y.Z,MOSEK / CLARABEL / SCS 版本
- **随机性控制**:seed = `DEFAULT_SEED`,`PYTHONHASHSEED = 20260418`
- **复现命令**:`papermill notebooks/<notebook>.ipynb out.ipynb -p ...` 或等价脚本
- **产物索引**:notebook 路径 + 图表路径 + 数据 snapshot(如 `data/m1_bb84_sweep.npz`)

## 1. 动机

## 2. 方法

## 3. 数值 / 理论结果

## 4. 与文献对比

## 5. 独立验证

## 6. Limitations(**必须写!**)

## 7. AI 协助范围(**必须写!**)

说明 Claude / 其他 LLM 在本 memo 的哪些部分参与了:讨论、初稿、代码补全、文献摘要等。未使用也要写 "无"。

## 8. 下一步
```

**对应字段也追加到 §7.1 literature 模板末尾**(复现环境 + 精读笔记对应的 commit SHA)和 §7.2 family 模板末尾(数据 snapshot 路径)。

---

## 8. 运营与节律

### 8.1 周度节律

- 周五:写 `conversations/weekly/YYYY-WNN.md` 周报
- 每双周:`codex exec -s read-only --skip-git-repo-check` 评审新增的 `docs/` 与 `qkdx/`

### 8.2 Milestone 节律

- 每 Milestone 完成即产出对应 findings memo + PHASE?_REPORT 的对应小节草稿
- Phase 0 末:PHASE0_REPORT.md 定稿(8-12 页)
- Phase 1 末:PHASE1_REPORT.md 定稿 + 三份 family sheet 定稿
- Phase 2 末:upper_bound_report.md 定稿(30-50 页)
- Phase 3 末:主问题答案 memo

### 8.3 ADR(Architecture / Assumption Decision Record)制度

任何偏离本研究计划或 PROSPECTUS.md 的决策必须写 `docs/adr/NNNN-<slug>.md`:

- 标题 + 日期 + 状态(Proposed / Accepted / Rejected / Superseded)
- 触发事件(哪条 Sub-Q 执行中发现的)
- 改变内容
- 理由(为什么要偏离)
- 后果(对其他 Sub-Q 的影响)

现已预留:
- `docs/adr/` 目录
- 首个 ADR 编号从 `0001` 开始

### 8.4 风险清单(与 REFACTORING_PLAN §8 对齐)

| # | 风险 | 本研究计划中的缓解位置 |
|---|------|--------------------|
| R1 | WLC SDP 在 QBER=0 数值不稳定 | §2.3 R3.2 提前实现 facial reduction |
| R2 | MOSEK 学术许可失败 | §1 使用 CLARABEL fallback;精度按 REFACTORING_PLAN §9.4 松一档 |
| R3 | TF-QKD 的 MS-EB 编码不自然 | §2.7 M4B(Phase 0.5)可降级为 decoy finite-key 扩展 |
| R4 | 提前引入 AI 搜索 | §1.2 红线:AI 搜索仅在 Sub-Q4 归因 B 时启动 |
| R5 | 12–16 周工期仍可能乐观 | 接受延期,**不降低验收标准** |
| R6 | CVXPY `quantum_rel_entr` 实现不全 | §2.1 R1.1 精读阶段预先验证 |
| R7 | 单人开发 | 每双周 codex 评审 + 关键 milestone 外部 reviewer 邀请 |

---

## 9. 诚信红线

本研究计划继承 PROSPECTUS.md §9 的全部诚信承诺,并加强以下具体红线(本页显式,防止后续版本漂移):

- **数值严格性**:所有密钥率数字基于 `qkdx.numerics.wlc.wlc_key_rate()` 或其严格扩展,不使用自编公式
- **定理追溯(强红线)**:**任何安全性结论或上下界陈述必须标注出处(论文 + 定理号 / 方程号 / 页码);无法追溯到具体定理的结论不得写入 `docs/findings/` 或 `PHASE?_REPORT.md`**。具体要求:
  - Shor-Preskill / Devetak-Winter 级结论引用到 Theorem 编号
  - GEAT 结论引用到 Metger et al. 2024 具体 Theorem + 适用条件(NSP / Markov chain)
  - PLOB 及其推广引用到原论文 Theorem 编号,并在 memo 中重述假设清单
- **"新发现"门槛**:任何"新发现"(改进的 c、新协议候选、更紧上界)不得在未经 §1.2 全部四条验收前对外声明
- **AI 工具使用透明度**:Claude / 其他 LLM 的使用必须在 `conversations/` 原始归档 + memo 的"AI 协助范围"(§7.3 模板)小节显式声明
- **文献引用核对**:文献引用必须手动回到 arXiv / DOI 核对,AI 建议的引用单独标注"待核对",核对后移除标注
- **违反上述任一条的 commit 拒绝合入**(即使在单人仓库也应遵守;通过 CI 检查或 pre-commit hook 强制)

---

## Changelog

- **v1.0**(2026-04-18):首次落盘。按 PROSPECTUS v3.1 的 Sub-Q1→Sub-Q4 展开成可执行的研究动作序列 + 文献阅读依赖图 + deliverable 模板 + 周度节律。

---

*文档结束*
