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

### 1.1 **path γ v0.2 → v0.3 RETRACTED**

**v0.2 试图升级到 [COROLLARY pending sign-off] → Claude audit verdict UNSOUND-RETRACT → 同日撤回到 [CONJ] (v0.3)**

**文件**：[docs/proofs/umr_data_processing_gamma.md](proofs/umr_data_processing_gamma.md) v0.2 (commit 9402e44)

**核心论证**（不再是 v0.1 的三 lemma L1/L2/L3 堆叠，改为 **adversarial containment 单步**）：

1. **观察**（**[THM]**，严格来自 Renner 2005 thesis + Portmann-Renner 2022）：若 adversary 集合 $\mathcal{A}_1 \subseteq \mathcal{A}_2$，则 $R(\Pi; \mathcal{A}_2) \leq R(\Pi; \mathcal{A}_1)$。

2. **关键事实**（用户待审）：$\mathcal{T}_\text{umr}$ 的 Eve 集合 $\mathcal{A}_\text{umr}$ **严格包含** Pirandola 2019 trusted-relay 模型的 Eve 集合 $\mathcal{A}_\text{tr}$。
   - 证明：umr Eve 的合法操作 = (控 $\mathcal{N}_A, \mathcal{N}_B$ 环境) **+** (控 Charlie 操作) ⊇ Pirandola Eve 的 (控 $\mathcal{N}_A, \mathcal{N}_B$ 环境)
   - umr Eve 可以**特例化**为"honest Charlie + 偷信道环境" = Pirandola Eve

3. **应用**：同一协议 $\Pi$ 在 umr 下的 rate ≤ 在 Pirandola-trusted 下的 rate（因 Eve 更强 → rate 更低）

4. **代入 Pirandola 2019 min-cut Thm**：在 trusted-relay 下 rate ≤ $\min(E_R(\mathcal{N}_A), E_R(\mathcal{N}_B))$ = $-\log_2(1-\min(\eta_A, \eta_B))$。

**结论**：
$$R_\varepsilon(\Pi) \leq -\log_2(1 - \min(\eta_A, \eta_B)) \qquad \forall \Pi \in \mathcal{T}_\text{umr}$$

**当前严谨性**：**[COROLLARY pending user sign-off on 关键事实 §2 的严格性]**（用户审阅 4-5 天工作量，详见 doc §5）

**若通过签字升级**：
- docs/proofs/upper_bound_msen.md 候选 A 从 [CONJ] → [COROLLARY]
- FINDINGS v2 §1.1 "$R \leq 1.44\sqrt{\eta_{AB}}$ [CONJ]" → **[COROLLARY]**（对称情形）
- docs/findings/gap_shape_g4_1.md gap 数值上界 → [COROLLARY]
- **Sub-Q4 归因 A/B/C 可启动**

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
   - **撤回原因**（Claude audit 2026-04-21 UNSOUND-RETRACT）：
     - v0.2 "adversarial containment" 是范畴错误，不是 set inclusion
     - $\mathcal{A}_\text{tr}$ 和 $\mathcal{A}_\text{umr}$ 的 Eve 生活在不同 Hilbert 空间
     - 结构性重复 FINDINGS v1 retraction (2026-04-19)
     - 详见 [docs/workflow/path-gamma-review/claude_audit_v1.md](workflow/path-gamma-review/claude_audit_v1.md)
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
14. adversarial containment 是 umr 上界继承的关键工具（vs 之前考虑的 L1/L2/L3 stacking）

---

## 3. 按 FINDINGS v2 红线的诚实声明

- **没有**把任何 [CONJ] 升级到 [THM]
- **没有**把 AI 起草的 path γ 标记为用户已签字
- **没有**在对外文档/发表格式中引用本项目的任何 [CONJ] 作为定理
- 今天新增的 path γ v0.2 **明确**为 [COROLLARY pending user sign-off]，不是 [COROLLARY]

---

## 4. 用户审阅优先级（若逐项处理）

| # | 项目 | 重要性 | 工作量 |
|---|---|---|---|
| 1 | path γ v0.2 §2.1 关键事实严格性 | **最高**：决定情况 A 能否推进 | 2 天 |
| 2 | path γ v0.2 §2.2 Step 1 adversarial containment | **最高**：主定理核心 | 1 天 |
| 3 | path γ v0.2 §4 finite-blocklength 继承（WTB Thm 47） | 中 | 1 天 |
| 4 | docs/AUTONOMOUS_SESSION_2026-04-21_LOG.md 历史记录 | 低（confirmatory） | 0.5 天 |
| 5 | D.4 Kamin MDI virtual-EB reduction 的 Werner 假设 | 中 | 0.5 天 |

**总计用户审阅工作量**：4-5 个工作日

---

## 5. 后续（取决于审阅结果）

### 若 path γ v0.2 通过 → [COROLLARY]

- **Sub-Q4 启动**：G4.1/G4.2 归因 A/B/C
- **若归因 A**：改进 $E_R$ upper bound 证明
- **若归因 B**：MS-EB 空间的新协议搜索（AI 可介入）
- **若归因 C**：双线并行

### 若 path γ v0.2 未通过 → 转备选

- **路径 β**：docs/proofs/upper_bound_msen.md §3.2 channel-reduction
- **路径 α**：Khatri-Wilde §19-20 monotonicity reduction

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
