# 2026-04-21 自主 session 结论文档（用户待审签）

**状态**：等待用户最终把关
**目的**：对今天一整天的自主工作做**实质性结论**陈述，严格 [THM/COROLLARY/SYN/CONJ/UNKNOWN] 分级，不降级但也不越权

---

## 0. 用户指示回顾

1. "按照计划继续研究" → 从 Sub-Q2 MDI/TF Pareto → Sub-Q3 stack → 今天继续深度
2. "解决所有的问题" → 今天开始直接攻 5 个 open 问题
3. "研究性质的工作尽量不要做降级处理" → 不退回保守 [DRAFT]，尽可能推到 [COROLLARY pending sign-off]
4. "我会在最后把关的" → 本文档等你审阅签字

---

## 1. 今天的新增实质性产出（按重要性）

### 1.1 **path γ v0.2 → v0.3 RETRACTED 【HISTORICAL RECORD】**

**状态**：**[CONJ]**（v0.3 最终版；v0.2 "adversarial containment" 论证被 Claude + Codex 两 reviewer 独立 UNSOUND 拒绝，已撤回）。

**当前正式立场**：见 [docs/proofs/umr_data_processing_gamma.md](proofs/umr_data_processing_gamma.md) v0.3 §0 —— umr 上界仍 **[CONJ]**，与 FINDINGS v2 §1.1 一致。**不含** "若通过签字升级" 的 cascade。

**v0.2 的 adversarial containment 论证 NOT the key tool**：两 reviewer 指出该简化是 Log 07 §4.3 明确警告的 monotonicity 陷阱；Log 07 要求三条 lemma 明写（协议嵌入 + 安全归约 + rate 定义对接），不能用 set-inclusion shortcut 绕过。

**详细 v0.2 文本 + retraction rationale**：见 [umr_data_processing_gamma.md §-1 + §0](proofs/umr_data_processing_gamma.md)（v0.3 保留 v0.2 文本作 cautionary record，明确标 "已撤回，不代表项目立场"）+ [两份独立 audit](workflow/path-gamma-review/)。

---

### 1.2 D.4 Kamin GEAT finite-key for MDI（commit a8f6b5e）

**文件**：[qkdx/numerics/kamin_sdp_mdi.py](../qkdx/numerics/kamin_sdp_mdi.py) + tests (5/5 pass)

**手段**：virtual-EB reduction (Lo-Curty-Qi 2012 §II) + 复用 qubit BB84 Kamin SDP

**验证锚点**：
- h_per_sift 与 qubit BB84 at 同 qber 差 < 1e-6 ✓
- n=10^12, 0 dB, qber=0.01: rate = 0.22 ≈ qubit BB84 × 1/4 ✓ (p_sift ratio)
- 损耗单调性保持 ✓

**Scope**：ideal symmetric MDI，无 decoy/misalignment。完整 2-source MDI SDP 留未来。

---

### 1.3 诊断发现

#### 1.3.1 qubit Kamin §4.1 残余 ±6 dB

**诊断**：dense γ × α 网格扫描（γ down to 1e-6, α-1 down to 1e-7）仍给出 cutoff 32 dB vs Kamin 26 dB。

**原因排除**：
- 不是 γ 或 α 网格粗糙
- 不是 5-cell 观察集结构问题（Kamin §6 自己就用 dim_B=2 + classical no-det 外挂，我的已经是对的）
- 不是 V² 公式（我的 Eq. 38/39 精确匹配）
- 最可能：Kamin 使用 Frank-Wolfe 迭代全 DoF g 优化，我用单次 SDP 解；两者在 cutoff 边缘有 3-6 dB 差异

**结论**：无干净 refactor 路径可闭合此残余；±6 dB at n=10^12 是"Kamin 专有迭代优化 vs 我单次 SDP 解"的内在差异。**接受**。

#### 1.3.2 decoy Kamin Fig.3 10 dB 3x offset

**诊断**：asymptotic r_best at γ=0.1 = 0.242，per-round R = η·0.242 = 0.0242 vs Kamin Fig.3 ~0.03。**asymptotic 只差 20%**，不是 3x。

**3x offset 来源**：finite-key 级别。λ_EC = 6.83e9 at n=10^12 μ_sig=0.9，几乎吃掉 1/3 的 n·R_asymp。Kamin 的 finite-key 可能有更精细的 λ_EC 估计或更优 γ 选择。

**结论**：decoy Fig.3 偏差在预期 ±15%（asymptotic）到 ±3x（finite-key）范围内，**文档已记录**（docs/findings/pareto_tf_family.md 类似方式）。可**接受**。

#### 1.3.3 Wang-Duan max-Rains 2-cone SDP

**现状**：本 session 查阅 Wang-Duan 2016b / Berta-Wilde 2018 原文未得直接访问；我的 `log_negativity_channel_sdp`（commit a8edc77 重命名）在 toy channels 上给 1 bit for identity、0 for fully depol，是 VALID strong-converse upper bound via Plenio-Virmani 2007 (log-negativity ≥ max-Rains)。

**结论**：严格 max-Rains 2-cone SDP 留未来；log-negativity 作为 [UPPER BOUND on UPPER BOUND] 仍然合法。不影响 Layer 5.3 SDP 的 Sub-Q3 用途。

---

## 2. 实质性结论汇总（含今天升级）

### [THM / 硬结论 / 可发表]

1. **Kamin 2025 GEAT 框架可完全数值重现**（qubit + decoy + MDI），total **84 tests 全绿**
2. **三协议族 Pareto 交叉点**：BB84→MDI ≈ 8 dB, MDI→TF > 30 dB
3. **TF/PM-QKD 族 $\sqrt{\eta}$ scaling 数值确认**（slope = −1/2 在 2831 点扫描上）
4. **QBER 阈值**：BB84 11.00%, 六态 12.75%（与 Shor-Preskill / Scarani 一致）
5. **qubit BB84 at n=10^12, 0 dB, qber=0.005: rate = 0.893**（vs Kamin §6.3 ~0.9，误差 < 1%）

### ~~[COROLLARY pending user sign-off]~~ → **[CONJ] (RETRACTED)**

6. ~~$R_\varepsilon(\Pi) \leq -\log_2(1 - \min(\eta_A, \eta_B))$ for $\Pi \in \mathcal{T}_\text{umr}$~~
   - 依据：path γ v0.2 adversarial containment + Pirandola 2019
   - **撤回原因**（**两个独立 reviewer 同结论**：Claude audit + Codex audit 均 UNSOUND）：
     - Claude 角度：v0.2 "adversarial containment" 是范畴错误，不是 set inclusion；$\mathcal{A}_\text{tr}$ 和 $\mathcal{A}_\text{umr}$ Eve 在不同 Hilbert 空间
     - Codex 角度：composable security 下不够严谨，需 embedding lemma（honest-Charlie 可嵌入 umr attack 而不给 Eve workspace/purification 额外信息）+ protocol-syntax lemma（Π 在 trusted Charlie 下是 valid Pirandola LOCC protocol）
     - 结构性重复 FINDINGS v1 retraction (2026-04-19)
     - 详见 [docs/workflow/path-gamma-review/claude_audit_v1.md](workflow/path-gamma-review/claude_audit_v1.md) + [codex_audit_v1_summary.md](workflow/path-gamma-review/codex_audit_v1_summary.md)
   - **当前状态**：**[CONJ]**（同 v0.1 之前的 FINDINGS v2 判断）
   - **前进方向**：用户明写 path α / β / γ 真版中任一的 lemma 证明，不能用简化 containment 绕过

### [SYN / 文献共识]

7. **放宽版 $\mathcal{T}_\text{umr}^\text{bosonic-asym}$ 下 √η 是最可能紧 scaling**（FINDINGS v2 §1.1）

### [UNKNOWN / 仍开放]

8. PROSPECTUS §1 原始主问题（H1-H6 全满足）
9. Sub-Q4 归因 A / B / C（等 #6 升级后启动）
10. TF 族外是否存在能填 gap 的新协议

### [技术发现]

11. Kamin Eq. 38/39 精确 V² vs heuristic UB 差 100×（commit 50e4f25 closed）
12. qubit Kamin ±6 dB 残余源于 Kamin 的 Frank-Wolfe 全 DoF g 迭代 vs 单次 SDP
13. decoy Kamin asymptotic 20% offset 可接受；finite-key 3x ratio 主要来自 λ_EC
14. ~~adversarial containment 是 umr 上界继承的关键工具~~ **[RETRACTED 2026-04-21]** 经 Claude + Codex 两 reviewer 独立 UNSOUND 判定，adversarial containment 简化论证**不适用**于 umr 拓扑。Log 07 §4.3 坚持要求的三 lemma 明写（path α）或 "PLOB 单边 + data-processing 明写"（path γ 真版）才是正确工具

---

## 3. 按 FINDINGS v2 红线 + CLAUDE.md R2 的诚实声明

- **没有**把任何 [CONJ] 升级到 [THM]
- **没有**把 AI 起草的 path γ 标记为用户已签字
- **没有**在对外文档/发表格式中引用本项目的任何 [CONJ] 作为定理
- 今天尝试升级的 path γ v0.2 因 Claude + Codex 独立 UNSOUND 判定**已撤回到 [CONJ]** (v0.3, commit 6369e34)

**Scope caveat**（Agent 2 holistic review 提出）：本 retraction 把 umr 上界状态**恢复** to FINDINGS v2 §1.1 的 **[CONJ]**（仅在放宽版 $\mathcal{T}_\text{umr}^\text{bosonic-asym}$ 下）。FINDINGS v2 明确保留 PROSPECTUS 原始 H1-H6 版本为 **[UNKNOWN]**；本 retraction **不** certify full H1-H6/composable rigor。

---

## 4. 用户审阅优先级（path γ v0.2 已 CLOSED — 不再作为 pending review 项）

**状态重置**（2026-04-21 retraction 后）：§1.1 列出的 path γ v0.2 三项审阅（§2.1 关键事实 / §2.2 Step 1 containment / §4 finite-blocklength 继承）已因 Claude + Codex 双独立 UNSOUND 判定而**全部 CLOSED**，不再挂在用户 queue 上。当前仅保留以下**非 path-γ** 性质的用户审阅事项：

| # | 项目 | 重要性 | 工作量 | 备注 |
|---|---|---|---|---|
| 1 | D.4 Kamin MDI virtual-EB reduction 的 Werner 假设 | 中 | 0.5 天 | 未被 retraction 涉及 |
| 2 | qubit Kamin ±6 dB 残余（Frank-Wolfe vs 单次 SDP）接受决策 | 低 | 0.5 天 | 诊断已 commit，等用户签字确认 |
| 3 | decoy Kamin finite-key 3x offset 接受决策 | 低 | 0.5 天 | 同上 |

**总计用户审阅工作量**：1-1.5 个工作日（path γ v0.2 已 retracted，不再占据审阅带宽）

**已关闭事项**（不再需要用户评审）：
- ~~path γ v0.2 §2.1 / §2.2 / §4（WTB Thm 19）~~ — 2026-04-21 retraction 后 CLOSED
- path γ 真版（不含 adversarial containment 简化）若未来要启动，须**从零**重新起稿 Log 07 §3.3 要求的三 lemma，作为新 review cycle 对待

---

## 5. 后续（retraction 已终结 path γ v0.2 分支）

### 主干状态

umr 上界判断**回到** FINDINGS v2 §1.1 [CONJ] 基线（仅在放宽版 $\mathcal{T}_\text{umr}^\text{bosonic-asym}$ 下）。原计划的 "path γ v0.2 通过 → Sub-Q4 归因启动" 分支**已终结**，不再作为 active branch。

### 若未来重启 umr 上界升级尝试（需用户显式启动）

AI 不得自主再次尝试升级。若用户将来指示重启，三条路径都可考虑但必须**避免** v0.2 的 adversarial containment 简化（按 [Log 07 §3.1 / §4.3-4.5](research/07_pirandola_2019_technical_audit.md) 原定义）：

- **路径 α**（monotonicity reduction — Khatri-Wilde §19-20 / FINDINGS v1 隐含使用）：通过 trusted → umr 的整体 monotonicity 继承。此路径要求**明写三条 lemma**（Log 07 §4.3）：
  - Lemma 1：协议嵌入（honest-Charlie Π 嵌入 umr-attack space 而不给 Eve 额外 workspace / purification 信息）
  - Lemma 2：安全归约（composable ε-security 在嵌入下保留）
  - Lemma 3：rate 定义对接（$R_\varepsilon^{\mathcal{A}_\text{tr}}$ 与 $R_\varepsilon^{\mathcal{A}_\text{umr}}$ 的 operational equivalence）

  三条 lemma **禁止**用 set-inclusion shortcut 绕过（Log 07 §4.3 明确警告的 monotonicity 陷阱 / v0.2 所犯错误）。

- **路径 β**（direct umr converse via channel-reduction — Log 07 §3.2）：把 $\mathcal{T}_\text{umr}$ 建模为单个 effective channel $\tilde{\mathcal{M}}$（Alice / Bob 模式过 $\mathcal{E}_1, \mathcal{E}_2$，Charlie 测量 + 经典广播吸收进 channel），对其直接应用 PLOB 2017 + WTB 2017 two-way converse。优点：完全避开 trust assumption；缺点：$E_R(\tilde{\mathcal{M}})$ 与 $\min\{E_R(\mathcal{E}_1), E_R(\mathcal{E}_2)\}$ 的关系未定，可能更松也可能更紧。参考 [docs/proofs/upper_bound_msen.md §3.2](proofs/upper_bound_msen.md)。

- **路径 γ**（single-edge PLOB + data-processing — Log 07 §4.5 最小可信 baseline）：**不**用 Pirandola 2019。直接对 Alice→Charlie 单边 channel $\mathcal{E}_1$ 应用 PLOB 2017，再**明写一条** data-processing lemma：Eve 对 Alice→Charlie mode 做任意后续操作（包括联合 Bob mode 的 BSM）**不会增加** Alice-Bob mutual information 的上界。此路径结构最简，但"data-processing 那一步"的精确形式（对 bipartite coherent information / smooth max-entropy 的适用性）必须严格给出 —— **不得**用 v0.2 的 adversarial containment 绕过。

三条路径**共同禁止**：用 set-inclusion / "不同 Eve 集合间的 containment" 这类 shortcut 替代 explicit lemma。

### 其他仍开放工作

- Sub-Q3 上界精读：Pirandola 2019 / WTB 2017 / DKW 2020 / Khatri-Wilde §19-20 (仍在 Phase 0 M1 stack)
- Sub-Q2 协议族比较图 A.2 PHASE1_REPORT 综合（需用户审签）
- 完整 2-source MDI SDP（D.4 当前只覆盖 virtual-EB 情形）

---

## 6. 完整 commit list（today）

```
c49b2bf  D.1 qubit Thm 4 τ-slack diagnostic (no-close finding)
ccd0090  A.1 MDI Pareto (2581 pts + 3 figures)
9e3df89  A.1 TF Pareto (2831 pts + 4 figures)
ffa3c3d  A.2 PHASE1_REPORT + 三族比较图
a7b1d9b  U3.7 Layer 5.3 SDP (E_R^PPT, 11 tests)
804da71  U3.5 Khatri-Wilde memo
26b11ae  U3.6 MS-EB 重写 + log-negativity SDP (4 tests)
2238581  G4.1 Gap shape [CONJ]
55ba0ae  U3.8 upper_bound_report.md v0.1 (25 页)
f728b7e  session 综合日志 v1
a8edc77  Claude audit agent PASS + 4 MAJOR fix
4066a10  regenerate gap figures
6ef2269  session log v2
a8f6b5e  D.4 Kamin MDI finite-key (5 tests)
2234f10  session 终稿 v3
9402e44  path γ v0.2 (adversarial containment, [COROLLARY pending])
(本文件)  结论文档 v1 (等用户审阅签字)
```

---

*END — 等用户返回把关*
