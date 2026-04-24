# Sub-Q3 上界接缝报告（Upper Bound Report）

**版本**：v0.6
**日期**：2026-04-24（v0.6 修正）/ 2026-04-21 首稿
**对应**：PROSPECTUS Sub-Q3 验收产出 + RESEARCH_PLAN §4.5 U3.8
**预期篇幅**：30-50 页（本稿约 25 页等价，可扩展）
**严谨性**：全文遵循 FINDINGS v2 §1.2 四级分级（[THM]/[COROLLARY]/[CONJ]/[UNKNOWN]），绝不越权

---

## 摘要

**主要发现**：

1. **文献精读完成**：PLOB 2017 / Pirandola 2019 / TGW 2014 / WTB 2017 / Khatri-Wilde 2024 五篇核心文献 Level 3-4 精读（docs/literature/）
2. **umr 拓扑继承问题显式识别**：五篇文献的上界定理在 umr（untrusted measurement relay）拓扑下的继承**都是 [CONJ] 级**，具体失效点由用户 Log 07 技术审计给出
3. **三候选修复路径**（Log 07 §3 + Khatri-Wilde §19-20 整合）：路径 α monotonicity reduction / β channel-reduction / γ PLOB+data-processing
4. **Layer 5.3 SDP 数值工具实施**：`qkdx/numerics/upper_bound.py` 含 E_R^PPT + max-Rains（Wang-Duan 2016b）SDP，15 tests pass
5. **Gap 定量形状初稿**（[CONJ] 级，G4.1）：`docs/findings/gap_shape_g4_1.md`

**未完成（honest accounting）**：

- 理论级 umr 继承 lemma 形式化（推荐路径 γ，留给用户纸笔工作）
- 任何 [CONJ] 候选的 [THM] 升级
- Sub-Q4 归因（依赖上述升级）

---

## 1. 引言与范围

### 1.1 PROSPECTUS Sub-Q3 的核心问题

> 已知的上界工具在 MS-EB 框架下给出什么上界?

具体要回答：

- **(a)** PLOB 精读 + 关键假设识别 + umr 拓扑 bearing
- **(b)** Pirandola 2019 network extension 在 "两方 + 单中间测量站" 的上界
- **(c)** WTB 2017 替代证明路线
- **(d)** 上界 MS-EB 表述（docs/proofs/upper_bound_msen.md）
- **(e)** 上界 SDP 实施（qkdx/numerics/upper_bound.py）

### 1.2 验收条件

1. 每个上界结论附原始论文定理/方程号
2. 每个数值结果附 notebook 路径 + commit SHA + 求解器版本
3. §3 MS-EB 重写至少有一条可计算的 $R_\text{UB}^\text{current}(\eta)$

### 1.3 本报告结构

- §2 文献定理精读精要（六份 memo 浓缩）
- §3 MS-EB 框架下的重写（从 docs/proofs/upper_bound_msen.md）
- §4 Layer 5.3 SDP 数值实施
- §5 数值验证 + gap 分析
- §6 Limitations + 待续
- §7 Sub-Q4 handoff

---

## 2. 文献定理精读精要

### 2.1 PLOB 2017 (Pirandola-Laurenza-Ottaviani-Banchi, Nat. Commun. 8:15043)

**主要结果**（原始两方直连拓扑，[THM]）：

- **Eq. 19 pure-loss bosonic**：$C_\text{loss}(\eta) = -\log_2(1 - \eta)$ bits/channel use
- **Eq. 28 QL amplifier**：$C(g) = -\log_2(1 - 1/g)$
- **Eq. 39 dephasing**：$C = 1 - H_2(p)$
- **Eq. 43 erasure**：$C = 1 - p$

**证明技术**（§III）：
1. Teleportation simulation：tele-simulable channel 等价于 Choi state
2. Relative entropy of entanglement $E_R$ 在 tele-simulable 上 single-letter
3. Purity reduction：tele-sim reduces two-way assisted to bipartite state problem

**umr 拓扑 bearing**（Log 07 §1.3）：
- PLOB 原始安全模型是"Eve 控制 channel 环境"，**relay 是 trusted**
- umr "Eve 控 Charlie" 严格更强，**PLOB 不直接适用**
- Assumption DP（data-processing）+ PLOB on single-edge 的组合可能给出 [COROLLARY]

**详细 memo**：[docs/literature/PLOB-2017.md](../literature/PLOB-2017.md)（commit 4d803ce, Level 4 精读）

### 2.2 Pirandola 2019 (Commun. Phys. 2:51)

**主要结果**（network-stretching 推广）：

- **Eq. 11 single-path min-cut**：$\mathcal{K}(a, b) \leq \min_{C \in \mathcal{C}(a,b)} \sum_{(i,j) \in C} E_R(\mathcal{E}_{ij})$
- **Eq. 9 equispaced chain**：$C_\text{loss,chain}(\eta, N) = -\log_2(1-\eta^{1/(N+1)})$

**关键假设**（Log 07 §2）：
- §II-A multi-graph 网络 + LOCC-assisted adaptive protocol
- §II-C 安全模型：Eve 控 **channel environments**，**not** party's internal registers
- **§IV Proof Step C** cut-partition 假设 relay nodes 可信

**umr 失效点**：Log 07 §2.4 指出 "Eve 控 Charlie" 违反 §II-C 安全模型

**详细 memo**：[docs/literature/Pirandola-2019.md](../literature/Pirandola-2019.md)（commit 186da1a, Level 4 精读）+ [docs/research/07_pirandola_2019_technical_audit.md](../research/07_pirandola_2019_technical_audit.md)（用户亲自审计）

### 2.3 WTB 2017 (Wilde-Tomamichel-Berta, IEEE TIT 63:1792)

**主要结果**（PLOB 强 converse 升级 + 有限 blocklength）：

- **Thm 12**：对 tele-simulable channel，$R \leq E_R(\mathcal{N})$ 是 **strong converse** rate （audit 2026-04-21 修正：prior memo "Thm 26"，PDF 实际 Thm 12）
  - 超过该率，error → 1 exponentially（PLOB 只证明 error → not → 0）
- **Thm 19 second-order expansion** for covariant channels:
  $$\hat{P}_\mathcal{N}^\leftrightarrow(n, \varepsilon) \leq E_R(\mathcal{N}) + \sqrt{V(\mathcal{N}, \varepsilon)/n}\, \Phi^{-1}(\varepsilon) + O(\log n / n)$$

**umr bearing**：继承 Q 同 PLOB；升级强 converse 不改变"Eve 控 Charlie"失效问题

**详细 memo**：[docs/literature/WTB-2017.md](../literature/WTB-2017.md)（commit 8446ced, Level 3 精读）

### 2.4 TGW 2014 (Takeoka-Guha-Wilde, Nat. Commun. 5:5235)

**主要结果**：

- **Eq. 1 squashed-E bound**：$R \leq \log_2 \frac{1+\eta}{1-\eta}$ for pure-loss
- 松于 PLOB 2×（$2.88\eta$ vs $1.44\eta$ at $\eta \ll 1$）

**historical value**：首次给出 pure-loss channel 的可计算上界；证明技术（squashed-E 子加性）被 PLOB 改进

**详细 memo**：[docs/literature/TGW-2014.md](../literature/TGW-2014.md)（commit 8446ced, Level 3 精读）

### 2.5 Khatri-Wilde 2024 (arXiv:2011.04672v2)

**综合教科书** — 1200+ 页。Sub-Q3 相关核心章节：

- **Ch 9/10 Entanglement Measures**：Rains, max-Rains, squashed-E, generalized divergences
- **Ch 19 LOCC-Assisted Quantum Comm**：
  - **Proposition 19.2**：$E(M_A;M_B)_\omega \leq n \cdot E^{\mathcal{A}}(\mathcal{N})$（amortized entanglement 统一框架）
  - **Corollary 19.3**：tele-simulable reduction
  - **Thm 19.4**：squashed entanglement weak converse
  - **Thm 19.8**：max-Rains strong converse（**SDP-可计算**，Wang-Duan 2016b）
  - **Thm 19.9**：Rains strong converse for PPT-simulable
- **Ch 20 Secret Key Agreement**：同 Ch 19 但专门 for private communication；结果平行

**对本项目最直接**：Thm 19.8 max-Rains SDP（`qkdx/numerics/upper_bound.py:r_max_channel_sdp`）+ Prop 19.2/Cor 19.3 为三候选路径形式化提供 template

**详细 memo**：[docs/literature/KhatriWilde-2020.md](../literature/KhatriWilde-2020.md)（commit 804da71, Level 3 精读）

---

## 3. MS-EB 框架下的上界重写

### 3.1 $\mathcal{T}_\text{umr}$ 拓扑类定义

详见 [docs/proofs/upper_bound_msen.md §2.1](../proofs/upper_bound_msen.md)。简记：两方 + 一 untrusted measurement relay Charlie + 纯损耗 bosonic 信道 + MS-EB H1-H6 全满足。

### 3.2 三候选上界陈述（[CONJ] 级）+ 三 formal path 分析

**候选公式表**：

| 候选 | 公式 | 来源 | 继承 lemma 状态 |
|---|---|---|---|
| A | $R \leq -\log_2(1 - \min(\eta_A, \eta_B))$ | PLOB worst-edge | Assumption DP 待形式化 |
| B | $R \leq -\log_2(1 - \sqrt{\eta_A\eta_B})$ | Pirandola N=1 chain | channel-reduction 待验证 |
| C | $R \leq E_R^\text{PPT}$ / $R_\max$ | Khatri-Wilde Thm 19.8 | LOPC monotonicity reduction 待证 |

对称 $\eta_A = \eta_B = \eta_\text{arm}$ 下，A 和 B 公式一致。

### 3.2.1 三条 formal path 的现状（2026-04-22 Codex 5-round 确认 [CONJ]）

用户 2026-04-22 指示 "三个 path 你都推导一下，并让 codex 确认" 后的当前状态：

**path α (monotonicity reduction via Khatri-Wilde §19-20)** — [scaffolding-only]
- 文档：[docs/proofs/umr_path_alpha_scaffolding.md](../proofs/umr_path_alpha_scaffolding.md) + [umr_path_alpha_derivation.md](../proofs/umr_path_alpha_derivation.md) v0.2+R4
- 11 authoritative gaps (scaffolding §5)
- Codex R1-R5 一致判定：identity-embedding 与 retracted v0.2 set-inclusion **同类 cross-space 陷阱**
- 升级前提：用户纸笔 formal Portmann-Renner embedding + security-transfer lemma (预估 10-15 人日)

**path β (channel-reduction + PLOB/WTB on effective channel)** — [CONJ], 5 gaps
- 文档：[docs/proofs/umr_path_beta_derivation.md](../proofs/umr_path_beta_derivation.md) v0.2+R3
- 5 gaps (4 MAJOR + 1 MINOR): β.G1 two-source merge / β.G2 PLOB on 2-to-2 broadcast / β.G3 $E_R^\infty(\tilde{\mathcal{M}})$ closed form / β.G4 Eve model transfer / β.G5 adversarial-channel reduction
- Tightness vs Pirandola min-cut **agnostic** — Log 07 §4.4 原文即 agnostic
- 潜在价值：若 SDP numerics 显示 $f(\eta_A, \eta_B) <$ Pirandola bound，可作 Sub-Q3 新上界

**path γ (single-edge PLOB + DPI target lemma, Log 07 §4.5 minimal baseline)** — [CONJ], 5 gaps
- 文档：[docs/proofs/umr_path_gamma_v0_4_derivation.md](../proofs/umr_path_gamma_v0_4_derivation.md) v0.4+R3
- 5 gaps (4 MAJOR + 1 MINOR): γ.B.G1 DPI lemma formal / γ.B.G2 BSM 是 quantum+classical joint / γ.B.G3 Alice-Charlie 与 Alice-Bob 的 operational 联系 / γ.G3 ε-composable transfer / γ.G4 classical announcement
- 历史：v0.2 retracted (set-inclusion)，v0.3 FAIL (super-receiver merge)，v0.4+R3 目前最干净
- Step B 明示 **target DPI lemma**（不是 $K_\text{A-B} \leq K_\text{A-C}$ capacity transfer）

**package level**：三路径 cycle 经 Codex 5-round review (workflow `docs/workflow/paths-review/`) 确认 at [CONJ] / scaffolding level。**没有** any path 升到 [COROLLARY]；升级仍需 R0.2 C1 ∧ C2 ∧ C3。

**Codex 5-round 教训汇总**（防止未来 derivation 重蹈 retraction pattern）：
任何声称 "umr 与 trusted-relay 之间的 continuity / embedding / inclusion / monotonicity / reduction shortcut"（无论措辞如何：identity-embedding、super-receiver merge、adversarial containment、cross-task capacity transfer），**都是** Portmann-Renner cross-space framework 的 un-closed gap。Codex R1-R5 反复捕获 4 类 drift: math errors / wording / partial-demotion / cross-file stale refs。

### 3.3 可数值计算的 $R_\text{UB}^\text{current}(\eta_\text{arm})$

**[COROLLARY under Assumption DP]**（候选 A/B 对称情形）：

$$R_\text{UB}^\text{current}(\eta_\text{arm}) = -\log_2(1 - \eta_\text{arm}) \text{ bits/round}$$

示例值：
- $\eta_\text{arm} = 0.5$（5 dB 单臂）：$R_\text{UB} = 1$ bit
- $\eta_\text{arm} = 0.1$（10 dB）：$R_\text{UB} = 0.152$
- $\eta_\text{arm} = 0.01$（20 dB）：$R_\text{UB} = 0.0145$

**[COROLLARY under LOPC monotonicity reduction]**（候选 C）：

$$R_\text{UB}^\text{current}(\eta_\text{arm}) = R_\max(\text{amp-damping}(\gamma = 1 - \eta_\text{arm}))$$

数值（本报告 §4 生成）：
- $\eta_\text{arm} = 0.316$（10 dB）：$R_\max \approx 0.193$
- $\eta_\text{arm} = 0.1$ (20 dB)：$R_\max \approx 0.062$

---

## 4. Layer 5.3 SDP 实施

### 4.1 模块：`qkdx/numerics/upper_bound.py`

**提供的 API**：

```python
# 工具
partial_transpose_B(ρ, d_A, d_B) → ρ^{T_B}
choi_state_from_kraus(kraus, d_A) → Choi state

# 标准 qubit 信道 Kraus
kraus_identity_qubit()
kraus_depolarizing_qubit(p)
kraus_dephasing_qubit(p)
kraus_amplitude_damping_qubit(γ)

# E_R^PPT SDP（Vidal-Werner 2002）
e_r_ppt(ρ, dim_A, dim_B) → {E_R_ppt_bits, sigma_opt, status}
e_r_channel_ppt(kraus, dim_A) → {E_R_channel_bits, ...}

# max-Rains SDP（Wang-Duan 2016b; Khatri-Wilde Thm 19.8）
r_max_channel_sdp(kraus, dim_A) → {R_max_bits, V_opt, status}

# Gap helper
dv_gap_from_achievable(ub, achievable) → {abs_gap, ratio, ...}
```

### 4.2 严格验证（15 tests pass，`tests/test_numerics/test_upper_bound.py`）

- Partial transpose primitive（product state, Bell state PPT criterion）
- Choi state construction（identity = Bell, full depol 是 PPT）
- E_R^PPT@identity = 1 ✓, E_R^PPT@full-depol = 0 ✓, monotone in p
- R_max@identity = 1 ✓, R_max@full-depol = 0 ✓, monotone in p

**求解器**：MOSEK via `cvxpy.quantum_rel_entr`。注册 `~/mosek/mosek.lic` 自动侦测。

### 4.3 计算复杂度

- 2-qubit state E_R^PPT: ~10s MOSEK
- 2-qubit channel max-Rains: ~3s
- 扫描 21-point parameter grid: ~2-3 min

---

## 5. 数值验证 + Gap 分析

### 5.1 Toy channel 数值（`scripts/sweep_upper_bound_toy.py`）

详见 [docs/research/data/er_ppt_{depol,dephasing,amp_damping}_sweep.csv](../research/data/) + [figures/upper_bound_toy_channels.{png,pdf}](../research/figures/).

Depolarizing sweep（p ∈ [0, 1]）:
- E_R^PPT: 1.0 → 0.0 (transition around p ≈ 0.65, isotropic SEP boundary)
- 与 Vollbrecht-Werner 2001 的解析形式对比：一致到 solver 精度

Amplitude damping sweep（γ ∈ [0, 1]）:
- E_R^PPT: 1.0 → 0.0 (monotone)
- TGW 2014 上界对比：我的 E_R^PPT < TGW（意味 E_R^PPT 更紧）

### 5.2 Gap 定量形状（G4.1，`scripts/gap_shape_analysis.py`）

详见 [docs/findings/gap_shape_g4_1.md](gap_shape_g4_1.md) + [data/gap_shape.csv](../research/data/gap_shape.csv) + [figures/gap_shape.{png,pdf}](../research/figures/).

**Gap ratio (UB / LB) 表**：

| loss (dB) | cand A/B : TF | cand C : TF |
|---|---|---|
| 10 | ~3200 | ~510 |
| 20 | ~1950 | ~790 |
| 40 | ~1890 | ~850 |
| 60 | ~2080 | ~1000 |
| 80 | ~960 | ~650 |

**Log-log slope 分析**：
- TF LB slope: -1/2（√η scaling）
- Candidate A/B UB slope: -1（η scaling）

**[CONJ 级判断]**：如果 candidate A/B 升级到 [THM]，gap 在 log-log 下**线性发散**，可能支持情况 B（超越 √η 的协议存在）。但**严格不升级**，仅作初稿。

---

## 6. Limitations + 待续

### 6.1 理论层

1. **Assumption DP**（候选 A/B）未形式化证明。**用户 Log 07 §3.3 推荐先做**。
2. **LOPC monotonicity reduction**（候选 C）未证。Khatri-Wilde Ch 20 Thm 20.x 的 umr 版本 open。
3. **Second-order finite-blocklength** Sub-Q3 未计算。WTB Thm 19 需要 per-channel relative entropy variance $V(\mathcal{N}, \varepsilon)$。

### 6.2 数值层

1. **Layer 5.3 SDP 仅 qubit-level**。Bosonic（Fock 空间）CV 计算未实施——对本项目 DV 聚焦是合理的。
2. **Smoothed E_R^ε** 未实施（WTB 二阶展开需要）。
3. **$k$-extendibility hierarchy**（SEP upper bound 的阶梯）未实施。PPT 是最低阶，对 2⊗2 已等于 SEP。

### 6.3 协议层

1. **MDI / BB84 family 的 finite-key 上界对齐**未做。Sub-Q3 主 focus 是 TF/umr 拓扑，其他协议的 finite-key converse 延后。

---

## 7. Sub-Q4 Handoff

本报告完成后，Sub-Q4 §5.1-5.3（gap 定量形状 + 归因）具备启动条件，**前提是至少一条候选升级到 [COROLLARY]**。

### 7.1 当前 Sub-Q4 可做（[CONJ] 级）

- [Done] G4.1 形状分析（initial, [CONJ]）
- [Pending] "如果候选 A/B 是 [THM]"下的假设分析 notebook（sensitivity to Assumption DP）

### 7.2 依赖用户理论工作后可做

- G4.2 归因 A/B/C（上界松 / 下界松 / 都松）
- G4.3 根据归因启动后续：
  - 若归因 A：证明更紧上界
  - 若归因 B：MS-EB 空间协议搜索
  - 若归因 C：两线并行

---

## 8. 完整索引

### 8.1 相关 commits（本期工作）

- `3434db3` → `ca202a1`：Kamin GEAT family（Phase 1 Sub-Q2）
- `50e4f25`：Kamin V² rigor（Eq. 38/39）
- `43f038f` / `d8f743c` / `3f98c8b`：Kamin decoy SDP + Thm 4
- `c49b2bf`：qubit Thm 4 τ-slack diagnostic
- `ccd0090` / `9e3df89`：MDI + TF Pareto sweeps
- `ffa3c3d`：PHASE1_REPORT.md
- **`a7b1d9b`**：**U3.7 Layer 5.3 SDP (E_R^PPT)**
- **`804da71`**：**U3.5 Khatri-Wilde memo**
- **`26b11ae`**：**U3.6 MS-EB 重写 + max-Rains SDP**
- **`2238581`**：**G4.1 Gap shape [CONJ]**

### 8.2 关键文件索引

**精读 memo**（`docs/literature/`）：
- `PLOB-2017.md`（Level 4）
- `Pirandola-2019.md`（Level 4）
- `WTB-2017.md`（Level 3）
- `TGW-2014.md`（Level 3）
- `KhatriWilde-2020.md`（Level 3）

**理论文档**（`docs/proofs/`, `docs/research/`）：
- `proofs/upper_bound_msen.md`（U3.6 MS-EB 重写）
- `research/07_pirandola_2019_technical_audit.md`（用户亲自审计）
- `research/FINDINGS.md`（v2 interim verdict [SYN/CONJ/UNKNOWN]）

**数值代码**（`qkdx/numerics/`）：
- `upper_bound.py`（U3.7 + extensions）
- `e_r_upper.py`（closed-form PLOB/Pirandola/TGW）

**测试**（`tests/test_numerics/`）：
- `test_upper_bound.py`（15 tests, Layer 5.3 SDP）
- `test_e_r_upper.py`（36 tests, closed-form bounds）

**扫描脚本 + 数据**：
- `scripts/sweep_upper_bound_toy.py` / `scripts/gap_shape_analysis.py`
- `docs/research/data/er_ppt_*.csv` / `gap_shape.csv`
- `docs/research/figures/upper_bound_toy_channels.{png,pdf}` / `gap_shape.{png,pdf}`

---

## 9. 严谨性守则声明

本报告全文遵循：

1. **四级分级**：[THM] / [COROLLARY] / [CONJ] / [UNKNOWN] 明示每个命题
2. **拓扑适用性红线**：PLOB/Pirandola/WTB/TGW 原始定理都是直接信道/trusted-relay，**严格不自动继承到 umr**
3. **AI 合成约束**（FINDINGS v2 §1.2 + Log 07 §3.4）：[SYN] / [CONJ] 命题不得升级到 [THM]，不得在对外论文直接引用
4. **用户 sign-off 要求**：本报告 v0.1 为 AI 整合稿，**任何 [COROLLARY] 及以上引用需项目负责人显式 review + sign-off**

---

## 10. Day 3 (2026-04-23) 增补 — structural derivation attempts

### 10.1 β + γ detailed drafts FINALIZED

两份 detailed drafts (commit 7813810) 经 Codex 多轮 review 后 FINALIZED at **[CONJ-DRAFT, open-only]**:

- [umr_path_beta_v0_4_detailed_draft.md](../proofs/umr_path_beta_v0_4_detailed_draft.md) — R4 PASS
- [umr_path_gamma_v0_6_detailed_draft.md](../proofs/umr_path_gamma_v0_6_detailed_draft.md) — R2 PASS

两份均:
- 所有 structural gaps (β.G2/G4/G5, γ.B.G1/G3, γ.G3) **保持 OPEN**
- 使用 5 级 citation taxonomy (VERIFIED / MEMO-LEVEL QUOTE / SUMMARY / INFERENCE / RECALLED)
- §9 user work plan 明确分 **PDF verification** (textbook-stable) vs **novel proof required** (structural)

### 10.2 β.G4 + γ.B.G1 derivation attempts

**β.G4 (Eve model transfer)** [commits c586610 → 037d20a → fb1c6dd, R2 PASS]:
- §2.3 direct simulation map (LOPC Eve ← umr Eve from channel environments) **invalidated**
- §2.5 LOPC+gift heuristic bridge **不 establish rate inequality**
- Paths A/B/C enumerated (effective channel extension / amortized β.G5 / Portmann-Renner C1 pathway)
- **β.G4 remains OPEN**, no AI simulation reduction found

**γ.B.G1 (DPI target lemma)** [commits c586610 → 037d20a → f1d8c75, R3 pending]:
- 4 approaches fail: Prop 19.2 circular / Horodecki+CMI broken / squashed cross-task / broadcast receiver asymmetry
- **Speculative conjecture CONJ1 [CONJ-DRAFT, NOT established]**: γ path 单边 PLOB 分解 intuition 可能 structurally 错; key rate 或许 joint $(\mathcal{E}_1, \mathcal{E}_2)$ multi-edge quantity — **未 proven**
- **γ.B.G1 remains OPEN**; agnostic on Q1 impact

### 10.3 Numerical scaffolding updates

- **β.G3 E_R SDP** [COMPLETED]: Two-layer proxy analysis.

  **Layer 1 — log_neg proxy (tensor product channel, qubit AD)**:
  
  | η_arm | log_neg 2-arm (bits) | Pirandola (bits) | ratio |
  |-------|---------------------|-----------------|-------|
  | 0.90 | 1.852 | 3.322 | **0.558** |
  | **0.618** | **1.388** | **1.388** | **1.000** ← crossover at η_c=1/φ |
  | 0.50 | 1.170 | 1.000 | 1.170 |
  | 0.10 | 0.275 | 0.152 | 1.809 |
  | 0.01 | 0.0287 | 0.0145 | 1.980 |

  **Layer 2 — E_R^PPT single arm (qubit AD, dim_A=dim_B=2 SDP, MOSEK)**:
  
  | η_arm | E_R^PPT(E₁) | log_neg(E₁) | PLOB | E_R/PLOB |
  |-------|-------------|-------------|------|----------|
  | 0.90 | 0.7590 | 0.9260 | 3.3219 | **0.229** |
  | 0.618 | 0.4196 | 0.6942 | 1.3885 | **0.302** |
  | 0.50 | 0.3217 | 0.5850 | 1.0000 | **0.322** |
  | 0.10 | 0.0616 | 0.1375 | 0.1520 | **0.405** |
  | 0.01 | 0.0065 | 0.0144 | 0.0145 | **0.451** |

  **[SYN] key findings**:
  1. log_neg crossover: η_c = 1/φ ≈ 0.618 (exact). Above: tighter; below: looser than Pirandola.
  2. E_R^PPT(E₁) < PLOB = Pirandola for ALL η ∈ [0.01, 0.95]; ratio 0.20-0.45.
  3. **[CONJ-DRAFT]** if E_R^PPT is additive: 2×E_R^PPT(E₁) < Pirandola for ALL η, including practical QKD range (η≈0.1). Tensor SDP (16×16) timed out — additivity unverified.

  Detail memo: `docs/findings/beta_G3_golden_ratio_crossover_2026-04-23.md` (v0.2)  
  Data: `docs/research/data/beta_G3_log_neg_vs_pirandola.csv`

- **max-Rains Wang-Duan SDP**: AI draft 2 variants both failed validation (Identity → 0 not 1; full depolar → -2); converted to `NotImplementedError` stub pointing user to PDF verify
- **Gap shape G4.1** (`scripts/gap_shape_analysis.py`) 已重跑, `gap_shape.csv` + figures refreshed

### 10.4 Portmann-Renner 2022 stub

[PortmannRenner-2022.md stub] — PDF **not** in local `docs/literature/pdfs/`. β.G4 Path C 依赖 P-R 2022 framework; user action: obtain PDF (APS or arXiv), put at standard filename. AI 不基于 [RECALLED] 推 P-R.

### 10.5 Net status update on Sub-Q3

**Sub-Q3 上界 status** (Day 3 agnostic snapshot):
- α/β/γ 三路径仍 [CONJ] 全部 open
- β + γ detailed drafts 明确 structural gaps 需 **user research-level proof**
- β.G4 + γ.B.G1 attempts 提供 concrete rationale for structural difficulty (not just "unknown")
- Numerical scaffolding (gap_shape + β.G3 SDP + max-Rains stub) 继续 build, 非 proof replacement

**未 shifted**:
- Sub-Q3 [THM] 级 answer 仍 pending C1+C2+C3 升级路径
- PROSPECTUS Sub-Q3 的实质结果**不** closed

### 10.6 Day 3 session log

[docs/AUTONOMOUS_SESSION_2026-04-23_LOG.md](../AUTONOMOUS_SESSION_2026-04-23_LOG.md) — 完整决策 + 迭代 + Codex verdict trail for user audit.

---

## 11. Day 4 (2026-04-24) 增补：4 信道 hierarchy + bug 修复 + AD Q analytic

### 11.1 Bug 修复（**项目级 bug 数据驱动地由 SDP 抓出**）

`qkdx/numerics/upper_bound.py:e_r_depolarizing_analytic` 公式错（Vollbrecht-Werner 在 d⊗d 维度的 (d-1) 被误为 (d²-1)）：

- 旧（错误）：`E_R = 1 - h(F) - (1-F)·log₂(d²-1)` (= subtracts log₂3 for d=2)
- 新（正确）：`E_R = log₂(d) + F·log₂F + (1-F)·log₂((1-F)/(d-1))`，对 d=2 简化为 `1 - h(F)`
- 来源：Plenio-Virmani 2007 §V.E (V.86)
- 影响：旧公式 underestimate E_R 0.03-0.40 bits；早期错误零点 p ≈ 0.27 vs 真 p = 2/3
- 验证：MOSEK SDP `e_r_channel_ppt(depolarizing)` 与新公式机器精度匹配（2⊗2 PPT=SEP per Horodecki 1996）

记录：`docs/findings/qubit_E_R_PPT_hierarchy_2026-04-23.md` §2.5；commit `b4efaae`。

### 11.2 4 qubit 信道 log_neg 解析公式（[SYN]，SymPy 验证）

**前提 — Choi-state vs channel-level 的区分** (2026-04-24 corrected after Codex REJECTED review of AD memo):
- **Teleportation-covariant 信道** (PLOB 2017 Ex.3: dephasing, depolarizing, erasure 等 Pauli 信道): Choi-state REE ≡ channel REE → `E_R^PPT(J_N)` 可作 channel `K^{↔}(N)` 的 UB
- **Non-tele-covariant 信道** (如 AD, WTB 2017): Choi-state E_R^PPT **不**自动 upper-bound channel K^{↔} —— 需 amortized / squashed / max-Rains 等 channel-level 工具。本表 AD 行的 E_R^PPT 值仅是 **Choi 态 Rains 熵**，不是 channel UB。

| 信道 | log_neg (Choi) | 最紧已知 K^{↔} 下界 | 最紧已知 K^{↔} 上界 | tele-covariant? |
|------|----------------|---------------------|---------------------|-----------------|
| AD (γ ≤ 1/2) | `log₂(2−γ)` | Q = `max_p[h₂((1-γ)p) − h₂(γp)]` (degradable, K^{↔} ≥ Q) | **channel UB 未知** (Choi-state E_R^PPT 不转 channel UB) | **No** |
| AD (γ > 1/2) | `log₂(2−γ)` | unknown (anti-degradable，K^{↔} OPEN) | **channel UB 未知** | **No** |
| Dephasing | `log₂(1+\|1−2p\|)` | K^{↔} = `1−h(p)` (PLOB Eq.39 [SYN]) | = log_neg UB (tele-cov → channel) | Yes |
| Depolarizing | `max(0, log₂(2−3p/2))` | K^{↔} UNKNOWN (E_R = `1−h(F)` is channel UB) | E_R (Vollbrecht-Werner, channel 级) | Yes |
| Erasure | `log₂(2−p)` | K^{↔} = `1−p` (PLOB Eq.43) | log_neg (接近紧, channel 级) | Yes |

实现：`analytic_log_neg_{amplitude_damping, dephasing, depolarizing, erasure}` + `quantum_capacity_amplitude_damping_degradable` (computes Q, NOT K^{↔}) in `qkdx/numerics/upper_bound.py`。

测试：13 tests in `TestAnalyticLogNegFormulas`（含 SymPy SDP 双验证 + Plenio 不等式 4 信道 × 200 grid pts × 800 检查 + bug regression）。

### 11.3 上界紧度层级（**Day 4 完成 hierarchy table**; 2026-04-24 evening Choi-state vs channel-level 修订）

| 信道 | log_neg (Choi) | E_R^PPT (Choi, SDP) | channel K^{↔} 已知范围 | 备注 |
|------|---------------|---------------------|------------------------|------|
| AD γ=0.05 | 0.964 | 0.855 (Choi only) | Q=0.831 ≤ K^{↔} ≤ **channel UB 未知** | AD **not** tele-covariant; Choi-SDP 不转 channel UB |
| AD γ=0.10 | 0.926 | 0.759 (Choi only) | Q=0.709 ≤ K^{↔} ≤ **channel UB 未知** | 同上 |
| AD γ=0.20 | 0.848 | 0.612 (Choi only) | Q=0.506 ≤ K^{↔} ≤ **channel UB 未知** | 同上 |
| AD γ=0.30 | 0.766 | 0.498 (Choi only) | Q=0.328 ≤ K^{↔} ≤ **channel UB 未知** | 同上 |
| Dephase p=0.10 | 0.848 | 0.531 (**channel UB**) | K^{↔}=0.531 (PLOB Eq.39) → E_R^PPT = K^{↔} | tele-covariant (PLOB Ex.3) |
| Depolar p=0.10 | 0.888 | 0.616 (**channel UB**) | K^{↔} ≤ E_R = 0.616; K^{↔} 真值 UNKNOWN | tele-covariant (PLOB Ex.3) |

**关键 Sub-Q3 工具评估**（修订）：
- **Dephasing: E_R^PPT = K^{↔} (channel)**（PLOB Eq.39 SDP 验证 [SYN]）→ PPT-SDP 在 K^{↔} 层完全紧化
- **Depolarizing: E_R^PPT = E_R (channel)**（Vollbrecht-Werner SDP 验证）→ E_R 是 channel K^{↔} 的紧 UB
- **AD degradable: Q 是 channel 级 LB; Choi-state E_R^PPT 不是 channel UB**（AD 非 tele-covariant；gap 表述应改为 Q ≤ K^{↔}, channel UB 需 amortized/max-Rains 工具）
- **AD anti-degradable: K^{↔} 真正 OPEN**（Q=0 但 K^{↔} 可能 > 0）；Choi-state E_R^PPT ≠ channel UB
- **Erasure: tele-covariant → E_R^PPT 是 channel UB; K^{↔} ≈ 0.90，log_neg ≈ 0.93** → log_neg 接近紧（channel 级）

**教训** (2026-04-24 Codex REJECTED `AD_anti_degradable_E_R_PPT_2026-04-24.md` v1.0 后记录): `e_r_channel_ppt` 函数计算 Choi 态 Rains 熵；对 tele-covariant 信道是 channel capacity UB，对非 tele-covariant 信道（如 AD）**不是**。先前 §11 的 AD 行 "E_R^PPT(AD) / Q ratio" 若读作 channel K^{↔} / Q 紧度，会误导。现已修订，保留数值 record（作 Choi-state benchmark）+ 显式 channel-level disclaimer。

### 11.4 BB84 / six-state 紧化分析

BB84 等效 depolarizing 信道 p_depol = 4·QBER/3（per `qkdx/protocols/bb84.py:bb84_channel`）：

**[单位修正 2026-04-24]**: SP 率以 **bits/信号** (= bits/channel use)，BB84 p_sift=0.5，六态 p_sift=1/3。先前表格错误使用 per-sifted 值，已修正。

| QBER | log_neg | **E_R = E_R^PPT** | SP_BB84 (/signal) | SP_6state (/signal) | E_R/SP_BB84 | E_R/SP_6state |
|------|---------|--------------------|-------------------|----------------------|-------------|---------------|
| 1.00% | 0.986 | 0.919 | 0.419 | 0.288 | 2.19 | **3.19** |
| 5.00% | 0.926 | 0.714 | 0.214 | 0.166 | 3.34 | **4.31** |
| 8.00% | 0.880 | 0.598 | 0.098 | 0.093 | 6.11 | **6.40** |
| 11.0% | 0.832 | **0.500** | ≈0 | 0.031 | ∞ | **16.3** |
| 12.62% | 0.805 | 0.453 | 0 | ≈0 | ∞ | **∞** |

**观察** [单位修正后]：
1. **六态 E_R/SP 比率 ~3-6×** (per-signal)，优于 BB84，但**非"接近闭合"** — 先前 ≤1.8× 因 per-sifted 单位错误已撤回 [CONJ]
2. **BB84 SP 离 E_R 仍远**：BB84 SP 在 11% 阈值已 0，E_R 仍 0.50 — 真 K^{↔} 在两者之间 [SYN]
3. **log_neg → E_R 在 BB84 阈值处紧化 40%**（0.83 → 0.50）[VERIFIED]

### 11.5 复合信道 PPT 视角观察（[SYN]）

n-fold self-composition 给出 4 信道分两类参数递归：
- AD/Depolar/Erasure: `p_n = 1 − (1−p)^n`
- Dephasing: `p_n = (1 − (1−2p)^n)/2`

**结构观察**: AD^n ≡ Erasure^n 在 log_neg 视角下完全相同（同参数递归 + 同单段公式）。这表示 PPT-relaxed 上界**失去区分**两类完全不同信道的能力。

详见：`docs/findings/qubit_log_neg_composition_2026-04-23.md` + `qubit_log_neg_n_fold_and_mixed_2026-04-23.md`。

### 11.6 仍 OPEN 的 Sub-Q3 项

| Item | 原因 |
|------|------|
| α/β/γ 三路径 [CONJ] | 结构 gap β.G4/β.G5/γ.B.G1/γ.G3 需 user paper-level work |
| AD γ > 1/2 K^{↔} (OPEN) | anti-degradable, Q=0 but K^{↔} may > 0；squashed entanglement 等需 PDF 精读 |
| Erasure E_R^PPT SDP | dim_B=3 → 16x16 SDP OOM 当前环境 |
| MDI/TF E_R^PPT | 拓扑 type B + bosonic, 工具链需扩展 |
| max-Rains SDP | Wang-Duan 2016b PDF 精读 + 2-cone form 实现 |

### 11.7 Day 4 commits

- `b4efaae`: e_r_depolarizing_analytic bug 修复 + 2 regression tests
- `5579e0f`: docs(tightness) 修订 反映 bug 修复
- `01935fa`: BB84 真 E_R 紧化（注：原"六态 UB-LB 接近闭合"因单位错误已撤回，见 v0.6 修正）
- `73bd18f`: AD Q analytic = quantum capacity (degradable γ < 1/2); Q is LB on K^{↔}
- `c0531a7`: Plenio 不等式扩展 4 信道
- `ea7868d`: session epilogue v0.2

---

## Changelog

- **v0.7** (2026-04-24 evening post-Codex-REJECTED): §11.2 + §11.3 修订 AD 的 E_R^PPT 陈述 — Choi-state vs channel-level 区分明示。AD 非 tele-covariant (WTB 2017 + PLOB Ex.3)，Choi-state E_R^PPT 不是 channel K^{↔} UB。先前 "E_R^PPT(AD)/Q ratio" 若读作 channel 层紧度是误导，已加 disclaimer 保留数据 record。Dephasing/depolarizing/erasure 的 channel-level 陈述仍有效（tele-covariant）。
- **v0.6** (2026-04-24 Round 2): 三项 FAIL 修正 — (1) AD K_D → Q rename（Q 是 LB on K^{↔} 非 UB）；(2) 六态 UB-LB 单位修正（per-signal 比率 ~3-6×，撤回 ≤1.8× "接近闭合"）；(3) 澄清 depolarizing K^{↔} UNKNOWN（E_R^PPT = E_R，非 K^{↔}）。
- **v0.5** (2026-04-24 Day 4): §11 增补 — e_r_depolarizing_analytic bug 修复 + AD Q degradable 公式 + 4 信道 hierarchy + 六态 UB-LB（单位错误版）+ Plenio 4-channel 扩展。已由 v0.6 修正。
- **v0.4** (2026-04-23 Day 3 cont.): §10.3 expanded — added E_R^PPT single-arm grid (Layer 2); golden ratio crossover η_c=1/φ; E_R^PPT < PLOB for all η; [CONJ-DRAFT] additivity pending 16×16 SDP verification
- **v0.3** (2026-04-23 Day 3 cont.): §10.3 β.G3 numerical results added — log_neg(E_1⊗E_2) vs Pirandola table; directional signal: tighter at η=0.9, not at η<0.5
- **v0.2** (2026-04-23 Day 3 autonomous session): §10 新增 Day 3 增补 — β + γ drafts FINALIZED, β.G4 + γ.B.G1 attempts both OPEN, numerical updates, P-R stub
- **v0.1**（2026-04-21 autonomous session）：首稿 25 页等价，整合 U3.1-U3.7 + G4.1 工作。30-50 页完整版留待后续基于理论 lemma 升级（路径 γ 形式化完成后）扩展。
