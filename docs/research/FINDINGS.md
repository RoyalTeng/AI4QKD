# INTERIM VERDICT — 放宽 bosonic-asymptotic 设定下的 scaling 判断

**文档状态**:修订版 v2 ·**scoped interim verdict** ·替代已撤回的 v1(over-claimed)
**日期**:2026-04-19
**作者**:Claude Opus 4.7,literature-informed synthesis(**仍需项目负责人签字才能作正式依据**)
**前身**:v1(commit `df92de9`)以"覆盖 PROSPECTUS §1 主问题"的方式过度宣称,经 commit `2644317` + [RETRACTION.md](RETRACTION.md) 撤回
**当前定位**:Sub-Q3 / Sub-Q4 的**研究起点(interim research judgment)**,**不是** PROSPECTUS v3.1 §1 主问题的最终答案

---

## 0. 重要范围界定(强约束)

本文件 **明确不是** PROSPECTUS v3.1 §1 主问题的答案。它是**一个放宽版本**的 scaling verdict,相对原始 PROSPECTUS 的硬约束有以下差距:

### 0.1 实际工作覆盖的假设 vs PROSPECTUS §3.1 硬约束

| PROSPECTUS §3.1 硬约束 | 本 interim 实际覆盖 | 差距说明 |
|----------------------|--------------------|----------|
| **H1** 无量子中继($\|\mathcal{P}\| \in \{1,2\}$) | ✓ 满足 | — |
| **H2** 无量子存储(源方制备后不做延迟操作) | ✓ 满足 | — |
| **H3** 刻画式设备信任(Level 1-3,排除 DI) | ✓ 满足(Charlie untrusted measurement) | — |
| **H4** 有限维(含 Fock 截断 $N_{\text{cut}} < \infty$) | ✗ **未覆盖** | PLOB / Pirandola19 上界用 bosonic(无穷维 Fock),finite-cutoff 对 scaling 的影响只停在 [SYN] 级(Log 05 B.7.3) |
| **H5** 可组合安全性(Portmann-Renner AC 框架) | ✗ **未覆盖** | 本研究是 asymptotic collective attack + de Finetti 化简,**没有处理 composable finite-key**。Kamin 2025 / Metger 2024 GEAT 适用是 Phase 1 Sub-Q2.4/2.5 工作 |
| **H6** 离散变量(密钥信息编码在离散寄存器) | ✗ **部分覆盖** | TF-QKD / PM-QKD / MP-QKD 使用 coherent states(bosonic),严格意义下不是 "pure DV"。下界引用这些协议作 achievability,属于 coherent-state/bosonic achievability,不是 "真 single-photon DV" achievability |

### 0.2 本 interim verdict 的**精确范围**

本文件的 scaling verdict 只在以下**放宽版 $\mathcal{T}_{\text{umr}}^{\text{bosonic-asym}}$** 上成立:

- 两方 Alice + Bob,一个 untrusted measurement relay Charlie(H1/H3 满足)
- 两段 **pure-loss bosonic channel**,透过率 $\eta_A, \eta_B$(**H4 放宽**:允许无穷维 Fock)
- **asymptotic rate + collective attack**(**H5 放宽**:不做 finite-key 可组合处理)
- Alice 和 Bob 的制备 **允许 coherent states**(**H6 放宽**:不是严格 single-photon DV)
- Alice/Bob 无量子存储(H2 满足)

**原始 PROSPECTUS 主问题(H1-H6 全部)仍然开放**,归 Sub-Q3 Phase 2 + Sub-Q4 严肃处理。

---

## 1. 核心 Interim Verdict

### 1.1 Scaling 判断

在 §0.2 的放宽版 $\mathcal{T}_{\text{umr}}^{\text{bosonic-asym}}$ 拓扑下,**最可能**的紧 scaling 为 $\sqrt{\eta_{AB}}$:

- **可达性下界(构造性,[THM])**:在 **严格 $\mathcal{T}_{\text{umr}}$**(per-round announcement)下,TF-QKD + PM-QKD 达 $R \geq c_{\text{strict}} \sqrt{\eta_{AB}}$,$c_{\text{strict}} \approx 0.2$(Lucamarini 2018 + Ma-Zeng-Zhou 2018)。在 **扩展 $\mathcal{T}_{\text{umr}}^+$**(允许跨轮 pairing,PROSPECTUS §3.1 S1 软约束外)下,MP-QKD 达 $c_{\text{ext}} \approx 0.3$(Zeng-Zhou-Wu-Ma 2022)。见 [Log 05 §B.4-B.5](05_achievable_rates_tfqkd.md) 口径澄清,[VERIFIED] 于 [EVIDENCE_APPENDIX.md](EVIDENCE_APPENDIX.md) §A
- **上界(尚待严格证成)**:$R \leq -\log_2(1 - \min(\eta_A, \eta_B))$,对称 $\approx 1.44 \sqrt{\eta_{AB}}$
  - **来源**:Pirandola 2019 network min-cut,Eq. (11)(single-path)/ Eq. (17)(multi-path)
  - **适用性间隙(严重)**:Pirandola 2019 严格 converse 针对 trusted / fully-cooperative relay nodes;**untrusted measurement relay 的 converse 继承依赖 "capacity monotonicity" 直觉**,本 interim 中**未升级到定理级继承 lemma**
  - 因此本上界分级为 **[SYN + CONJ]**,不是 [COROLLARY],更不是 [THM]

### 1.2 可信度评级

| 命题 | 分级 | 理由 |
|------|------|------|
| TF-QKD 族可达 $\sqrt{\eta_{AB}}$(in bosonic-asymptotic) | **[THM]** | Lucamarini 18 + 多篇复现,[VERIFIED] |
| $\sqrt{\eta_{AB}}$ 是最可能的紧 scaling | **[SYN]** | 文献共识("single-repeater bound"术语);无反例 |
| $R \leq 1.44 \sqrt{\eta_{AB}}$ 严格上界 | **[CONJ]** | Pirandola19 在 untrusted-relay 下的严格继承 **open**,capacity monotonicity 需 Sub-Q3 定理级工作 |
| 情况 A 在 PROSPECTUS 原始(H1-H6)意义下成立 | **[UNKNOWN]** | 本研究未处理 H4/H5/H6 的回归;**撤回覆盖宣称** |

**情况 B / C 的排除也退至 [SYN] 级**(而非原 FINDINGS 的 [COROLLARY]):

- **情况 B(按 PROSPECTUS 字面 $\alpha \in (1/2, 1)$,即 rate 小于 $\sqrt{\eta}$)**:由 TF-QKD achievability [THM] 直接排除(这部分论证保持有效)
- **情况 B(物理直觉 $\alpha < 1/2$,rate 大于 $\sqrt{\eta}$)**:依赖于 §1.1 的上界,**属 [CONJ] 级排除**
- **情况 C**:同情况 B 的 [CONJ] 级排除
- **情况 A**:**最可能成立**,但仅在 §0.2 放宽版本下,且上界为 [CONJ]

### 1.3 结论一句话

在 bosonic-asymptotic 的放宽版 $\mathcal{T}_{\text{umr}}$ 下,**$\sqrt{\eta_{AB}}$ 是**最可能的紧 scaling**(情况 A 方向);严格 converse 需要 Sub-Q3 精读工作把 untrusted-relay 适用性升级到 [THM] 级**。PROSPECTUS 原始 H1-H6 版本仍然开放。

---

## 2. 证据链(更严格重新梳理)

### 2.1 [THM] 级 — 已核实

| 命题 | 引用 | 核查位置 |
|------|------|----------|
| PLOB pure-loss $E_R = -\log_2(1-\eta)$ | Pirandola-Laurenza-Ottaviani-Banchi 2017, Nat. Commun. 8:15043 | [EVIDENCE_APPENDIX.md](EVIDENCE_APPENDIX.md) §A.1 — **公式 [VERIFIED]**,定理号 **未直接核正文** |
| TF-QKD $\sqrt{\eta}$ achievable | Lucamarini et al. 2018, Nature 557:400 | [EVIDENCE_APPENDIX.md](EVIDENCE_APPENDIX.md) §A.4 — **[VERIFIED]** via multiple secondary sources |
| Pure-loss LOCC-simulation | Niset-Fiurášek-Cerf 2009 + PLOB17 Eq. (4) | [EVIDENCE_APPENDIX.md](EVIDENCE_APPENDIX.md) §A.3 — 教科书共识 |

### 2.2 [SYN + CONJ] 级 — 未升级到定理

| 命题 | 分级 | 依赖的 gap |
|------|------|----------|
| Pirandola 2019 网络 min-cut bound | [THM for trusted relay] + [CONJ for untrusted] | **untrusted-case 继承**没写成定理级 lemma(见 §1.1 关键 gap) |
| "Scaling gap = 0" | [SYN] | 依赖于放宽版 $\mathcal{T}_{\text{umr}}^{\text{bosonic-asym}}$ 上界 [CONJ] |
| 情况 A 成立(放宽版) | [SYN] | 同上 |
| 情况 A 在原始 PROSPECTUS(H1-H6)下成立 | [UNKNOWN] | H4/H5/H6 未处理 |

### 2.3 证据审计

所有外部文献引用的 URL、抓取日期、引用片段全部归档在 [EVIDENCE_APPENDIX.md](EVIDENCE_APPENDIX.md),供独立复核。

---

## 3. 撤回 v1 的关键错误清单(警示)

见 [RETRACTION.md](RETRACTION.md)。本文件 v2 对 v1 错误的修正映射:

| v1 错误 | v2 对应修正 |
|---------|------------|
| [COROLLARY] 级分级伪装 | §1.2 降为 [SYN] / [CONJ] / [UNKNOWN] 四级混合 |
| 形式上像 PLOB 误用(-log₂(1-√η_AB)) | §1.1 明确为 "Pirandola19 min-cut 应用到 segment 层面",**不是** PLOB 直接应用;严格继承 gap 显式 |
| 越权覆盖 PROSPECTUS §3.1 H4/H5/H6 | §0.1 显式表,承认三条硬约束未覆盖 |
| "已关闭 Sub-Q3" | §0.2 + §4 明确主问题仍开放,本文是 Sub-Q3 **起点** |
| Phase V 审计过信 | §5 对 V1-V4 的有效性做重新评估 |

---

## 4. 对 Sub-Q3 / Sub-Q4 的研究建议

### 4.1 Sub-Q3 的 Phase 2 精读重点(按本 interim 暴露的 gap)

1. **untrusted-relay 的 converse 定理化**(**优先级最高**):
   - 目标:把 capacity monotonicity 从 trusted 到 untrusted 的继承升级到定理级
   - 文献起点:Pirandola 2019 Eq. (11) + 其证明细节;DKW 2020 converse bound;是否有文献已经处理 untrusted-measurement relay?
   - 产出:**Lemma**:untrusted relay 协议类族 ⊆ trusted relay 协议类族,故 sup 单调 ≤。或给出**直接**的 untrusted-relay converse 证明。
2. **bosonic → DV 的降级分析**:
   - Fock 截断 $N_{\text{cut}}$ 如何影响上界?finite-dim + DV 载体下的 $\mathcal{T}_{\text{umr}}$ 上界是否仍 $\sqrt{\eta}$?
   - 文献起点:George-Lin-Lütkenhaus 2020 数值诱饵 + Hu-Im-Lin-Lütkenhaus-Wolkowicz 2022 facial reduction
3. **composable finite-key**:
   - Metger 2024 GEAT 在 $\mathcal{T}_{\text{umr}}$ 的 NSP 兼容性 + finite-key scaling 是否仍 $\sqrt{\eta}$?
   - 文献起点:Kamin et al. 2025 为 decoy BB84 已做(non-$\mathcal{T}_{\text{umr}}$),需扩到 TF-QKD family

### 4.2 Sub-Q4 的 gap 归因重新定位

本 interim 撤回"γ 预判"(两端都松)。Sub-Q4 的归因 α/β/γ 应在 Sub-Q3 完成**之后**基于定理级上界重新启动,**不以本 interim 为预定位**。

---

## 5. 对 Phase V 审计流程本身的反省

### 5.1 V1-V4 未抓住的盲点

- **V1 逻辑自审**:检查符号 / 推理步 / 假设遗漏;**未检查"定理的原始拓扑是否匹配应用"**
- **V2 文献交叉**:WebSearch 核公式,未深究 untrusted-vs-trusted 区分;未核正文定理编号
- **V3 反例搜索**:搜超越 $\sqrt{\eta}$ 的协议(下界方向);**未反向搜 "untrusted-measurement upper bound" 专论**
- **V4 codex 独立评审**:codex 共享 Claude 的训练偏差,没独立提出拓扑适用性质疑

### 5.2 方法论补丁

已写入 [RESEARCH_PLAN.md §1.2 补丁 2b](../RESEARCH_PLAN.md)(四条硬要求:拓扑 / 信任 / 协议自由度 / 精确编号)。

**额外**:

- AI 结论性文档必须经**项目负责人显式 review + sign-off** 才能 commit 为"最终"状态(避免本 v1 自动 commit 的失误)
- 多 AI cross-audit 不构成"独立验证"(RETRACTION.md §4.3)

---

## 6. 授信边界再声明

本 interim verdict v2:

- **尚未经项目负责人正式签字**,**不得**作为正式对外依据
- 作为 Sub-Q3 的**内部研究起点**,建议与 RESEARCH_PLAN §2.1 R1.1(WLC 2018 精读)Phase 2 工作同步启动
- 本文件的任何 [SYN] / [CONJ] 命题**不得**在对外论文 / 展示 / 对其他研究组陈述 中被升级引用

---

## Changelog

- **v2**(2026-04-19):本版。替代 v1(over-claimed + retracted)。严格 scope 到 bosonic-asymptotic 放宽版;所有分级降档到 [SYN]/[CONJ]/[UNKNOWN];明确保留 PROSPECTUS 主问题开放;添加 EVIDENCE_APPENDIX.md 可审计证据。
- **v1**(2026-04-19):原 FINDINGS,因过度宣称被撤回(详见 [RETRACTION.md](RETRACTION.md),commit `2644317`)。

---

*INTERIM VERDICT v2 结束。PROSPECTUS 主问题仍开放。*
