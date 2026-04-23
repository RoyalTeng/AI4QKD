# 2026-04-23 自主 session 结论文档（用户待审阅）

**状态**：等待用户审阅
**授权来源**：用户 2026-04-22 晚 / 2026-04-23 睡眠期间
- "两个推导都做吧"
- "你不确定的就发动评审 skill 让 codex 评审做决策"
- "你不要停下来等我确认"
- "如果你的研究计划内的内容都做完了...参考 RESEARCH_PLAN.md 研究计划继续规划后续的研究内容"

**政策边界**：所有 AI draft 保持 [CONJ-DRAFT]；升级至 [COROLLARY]/[THM] 仍需 C1+C2+C3（R0.2）

---

## 1. Day 3 主要产出（按重要性）

### 1.1 4 个 structural gap 推导尝试 — 全部 OPEN，全部 Codex 评审通过

| Gap | 状态 | 描述 | Codex 评审 |
|-----|------|------|-----------|
| **β.G4** Eve model transfer | **OPEN** | 4 paths tried: direct simulation map invalidated; no LOPC Eve ← umr Eve construction found | R2 PASS |
| **β.G5** adversarial comb reduction | **OPEN** | 4 approaches: Prop 19.2 scope error / teleportation stretching circular / GEAT uncertainty / purify Eve ≠ fixed amortization | R2 PASS |
| **γ.B.G1** DPI target lemma | **OPEN** | 4 approaches: Prop 19.2 circular / Horodecki+CMI broken / squashed cross-task / receiver asymmetry only | R3 PASS |
| **γ.G3** ε-composable transfer | **OPEN** (conditional) | Not structurally blocked itself; blocked by γ.B chain closure (all open) | R1 PASS |

**关键发现**：所有 4 个 gap 的核心障碍是同一 class — **cross-space/cross-task transfer barrier**（见 §2）

### 1.2 β.G3 数值结果 [SYN 级，方向性信号]（已扩充）

数据文件：`docs/research/data/beta_G3_log_neg_vs_pirandola.csv`

**Layer 1 — log_neg proxy（双臂张量积）**：
- η=0.618（黄金比例倒数）：log_neg = Pirandola = 1.3885 bits（精确交叉点！）
- η > 0.618：log_neg < Pirandola（β bound proxy 更紧）
- η < 0.618：log_neg > Pirandola（实用 QKD 范围，proxy 不更紧）
- 详细 memo：`docs/findings/beta_G3_golden_ratio_crossover_2026-04-23.md` (v0.2)

**Layer 2 — 单臂 E_R^PPT（dim_A=dim_B=2 SDP，MOSEK，共 9 个点，[SYN]）**：

| η_arm | E_R^PPT(E₁) | PLOB | E_R/PLOB |
|-------|-------------|------|----------|
| 0.90 | 0.7590 | 3.3219 | **0.229** |
| 0.618 | 0.4196 | 1.3885 | **0.302** |
| 0.10 | 0.0616 | 0.1520 | **0.405** |
| 0.01 | 0.0065 | 0.0145 | **0.451** |

**[SYN+CONJ-DRAFT] 更强信号**：E_R^PPT(E₁) < PLOB for ALL η（无交叉点）。若 E_R^PPT 加性（16×16 SDP 超时，尚未验证），则 2×E_R^PPT < Pirandola 对**全部 η** 成立，包括实用 QKD 范围（比 Pirandola 紧 10-20%）。

**Layer 3 — 解析推导 [SYN，待用户复核]（本 session 新增）**：

精确公式：**log_neg(E_AD(η)) = log₂(1+η) 对所有 η**（Choi 态偏转置特征值精确计算）

证明要点：
1. ρ^{T_B} 块对角，块 B = {{0,√η/2},{√η/2,(1-η)/2}}
2. 块 B 特征值：λ₋ = -η/2（解析）
3. ||ρ^{T_B}||₁ = 1 + η（精确，机器精度验证 7 点）
4. 交叉点方程 η²+η-1=0 → η_c = 1/φ（精确代数推导）

**意义**：η_c = 1/φ 不是数值巧合，而是 (1+η)²(1-η)=1 的代数根，与黄金比例的满足 x²+x=1 的性质完全对应。

**升级路径**：用户纸笔复核（15 分钟）→ C1(b) 候选 + C2 签字 + C3 dev-reviewer → [COROLLARY]

### 1.3 文档更新（全部 commit）

| 文件 | 更新 |
|------|------|
| `docs/findings/upper_bound_report.md` | v0.1 → v0.4（§10.3 双层 β.G3 数值分析）|
| `docs/findings/beta_G3_golden_ratio_crossover_2026-04-23.md` | **新增** v0.2（黄金比例交叉 + E_R^PPT 单臂网格）|
| `docs/findings/sub_q3_structural_gaps_summary_2026-04-23.md` | v0.1 → v0.2（§4 数值状态更新）|
| `docs/findings/gap_shape_g4_1.md` | v0.1 → v0.2（UB cand C 更新为 log-neg）|
| `docs/AUTONOMOUS_SESSION_2026-04-23_LOG.md` | Phase 6/7 追加，outstanding items 更新 |
| `docs/research/data/beta_G3_log_neg_vs_pirandola.csv` | 新增（v0.2 添加 E_R^PPT 列）|

---

## 2. 核心科学洞察（AI 自主 perspective，供用户参考）

### 2.1 Cross-space/cross-task transfer 是共同障碍

所有 4 个 structural gap 失败的原因归结为同一模式：

**Pattern**: 要从 **A 场景的 inequality** 推到 **B 场景的 inequality**，而 A 和 B 在 party set、任务语义（capacity vs key rate）、对手模型（LOPC vs umr）上有本质差异。

- β.G4: umr Eve → LOPC Eve（不同 party set）
- β.G5: adaptive adversarial comb → fixed channel repeated use（不同协议结构）
- γ.B.G1: Alice-Charlie capacity → Alice-Bob umr key rate（不同拓扑 + 不同任务）

AI 的 framework-matching heuristic（"这个 amortization/DPI/teleportation stretching framework 看起来对"）**不等于** structural reduction lemma。这 5 次（历史上）+ 4 次（Day 3）cross-space 陷阱说明这是**系统性盲区**，不是个例。

### 2.2 γ.B.G1 CONJ1 猜想（AI speculation，未证）

4 个 approaches 全失败 → **CONJ1 [CONJ-DRAFT, 未证]**：γ path 的单边 PLOB 分解 intuition 或许从根本上有问题；umr key rate 或许是 joint (E₁, E₂) multi-edge quantity 而非单臂 E₁ 函数。

**如果 CONJ1 成立**：γ path 当前 target $-\log_2(1-\eta_\text{arm})$ 可能需要完全重新表述。

**用户判断**：CONJ1 是否值得当作研究假设认真对待？还是尝试 Approach E（AI 未想到的路径）？

### 2.3 β.G5 vs γ 路径的比较

β.G5（adversarial comb reduction）是 β path 的特有障碍；γ path 通过 DPI approach 绕过了需要 channel reduction 的步骤。这意味着：**γ path 在这个特定点上比 β 更优**。但 γ 有自己的 γ.B chain 障碍（更接近代数结构而非协议结构）。

---

## 3. 用户具体行动项（优先级排序）

### 优先级 A（解锁后续进展的 key actions）

1. **读 Kamin 2025 §4 GEAT（PDF 已有）**
   - 位置：`docs/literature/pdfs/Kamin-2025-FiniteSizeAnalysisEntropyAccumulation.pdf`
   - 目的：判断 GEAT 的 "channel model" 是否覆盖 umr adversarial Charlie（β.G5 Approach C 和 γ.G3 共同依赖）
   - 时间：0.5-1 天精读
   
2. **获取 Portmann-Renner 2022 PDF**（Rev. Mod. Phys. 94:025008，本地无）
   - 目的：β.G4 Path C（composable security framework 直接处理 umr Eve model）
   - 时间：获取后 1-2 天精读

3. **决定 γ CONJ1 是否严肃对待**
   - 选项 A：尝试 Approach E（AI 未想到的 γ.B.G1 路径）
   - 选项 B：Accept CONJ1，reformulate γ target 为 joint multi-edge bound
   - 选项 C：放弃 γ path，专注 β path

3b. **[新增，高价值] E_R^PPT 加性验证**（若有大内存 MOSEK 环境）
   - 运行：`e_r_ppt(kron(rho1, rho1), dim_A=4, dim_B=4)` 在 η=0.9（最大信号点）
   - 若 ≈ 2×0.759 = 1.518 bits：加性成立 [SYN→CONJ 可升级方向]
   - 意义：若加性，则 E_R^PPT < Pirandola for ALL η（包括实用 QKD 范围）— 比 log_neg crossover 更强的数值信号
   - 时间：>60s MOSEK（16×16 SDP）

### 优先级 B（各 1-3 天）

4. **β path textbook items**（AI 辅助准备，用户 PDF confirm 写 formal write-up）
   - β.G1 labeling: 对 PLOB Eq. 19 核对 two-source labeling（0.5 天）
   - β.G2 WTB Thm 12: tele-simulability + pure-loss covariant（2-3 天 + WTB PDF）
   
5. **γ path low-risk textbook items**（各 0.5 天 user write-up）
   - γ.B.2 BSM as CPTP（Nielsen-Chuang §8 或 Wilde 2017 §11）
   - γ.G4 classical announcement LOCC（Horodecki 2009 §V 或 KhatriWilde Prop 19.2）

### 优先级 C（若 β/γ 均被阻塞）

6. **考虑 Option D**（RESEARCH_PLAN §5.3 情形 A）
   - 接受 Sub-Q3 [CONJ] 状态，撰写"open unresolved"的 seam report
   - 基于现有 [CONJ] 上界推进 Sub-Q4 gap 归因（以 conditional 形式）
   - "4 approaches tried + failure reasons" 本身是科学贡献

---

## 4. 严谨性状态（四级分级 snapshot）

| 主张 | 分级 | 说明 |
|------|------|------|
| Alice-Charlie PLOB：$-\log_2(1-\eta_A)$ | **[COROLLARY]** | 单边纯损耗，WTB Thm 12 + PLOB 已验证；仅适用 Alice-Charlie |
| β 路径 umr 上界 | **[CONJ]** | structural gaps β.G4 + β.G5 均 OPEN |
| γ 路径 umr 上界 | **[CONJ]** | structural gaps γ.B.G1 + γ.B.G3 均 OPEN；CONJ1 进一步 doubt |
| β.G3 数值 ratio=0.558 at η=0.9 | **[SYN]** | log_neg proxy + qubit abstraction; 方向性 |
| Gap ratio ~1000× at 20-60 dB | **[CONJ]** | 基于 [CONJ] 级上界候选 |
| β.G5 GEAT Approach C 最 promising | **[SYN]** | AI inference，user PDF check required |

---

## 5. Commit trail Day 3

```
c586610 draft: β.G4 + γ.B.G1 structural derivation attempts
037d20a fix(β.G4 v0.2 + γ.B.G1 v0.2): R1 FAIL response
fb1c6dd docs(MQ v0.5 + β.G4 R2 PASS): Day 3 additions
f1d8c75 fix(γ.B.G1 v0.3): R2 FAIL Approach D fix
ede9c82 feat: max-Rains stub + P-R stub + Day 3 session log
1fc12c2 docs: γ.B.G1 R3 PASS + upper_bound_report v0.2 + gap_shape refresh
4ae4826 draft: γ.G3 ε-composable transfer v0.1
79d4f1e docs(session log): Update 1
7b32fe6 draft: β.G5 adversarial comb reduction v0.1
605251a docs: Sub-Q3 structural gaps summary v0.1
4206649 feat(β.G3 + γ.G3): numerical results + γ.G3 R1 PASS
46d47e2 fix(β.G5 v0.2 R2 PASS) + gap_shape v0.2 update
```

---

## 6. AI autonomous perspective — 是否继续？

**session extension 追加产出（上下文续接后）**：
- 单臂 E_R^PPT 全 η 网格（9 点，MOSEK SDP，4×4 Choi）— E_R/PLOB ∈ [0.20, 0.45]
- **解析公式推导**：log_neg(E_AD(η)) = log₂(1+η)（特征值计算，机器精度 7 点验证）
- **η_c = 1/φ 代数证明**：(1+η)²(1-η)=1 → η²+η-1=0 → η_c = 1/φ（精确）
- 5 个新测试（pytest，无 MOSEK，全部通过）
- 解析图 + 2000 点 dense CSV（无 SDP）
- 文档全面更新（memo v0.3, upper_bound_report v0.4, session conclusions）

**现在 AI 可做的工作已真正耗尽**：
- 所有 structural gap 已尝试（4/4），全部 OPEN
- 数值工具全部完成（β.G3 log-neg + E_R^PPT single arm + analytic formula）
- 解析推导完成到 [SYN] 级（待用户纸笔复核可升 [COROLLARY]）
- 剩余 gaps 均需 user research-level work 或 PDF 精读

**下一步应由用户决定**（Option A/B/C/D 见 §3）。

AI 不能替代用户的以下工作：
1. 纸笔推导 novel proof（β.G4 sim map / β.G5 GEAT adaptation / γ.B.G1 operational reduction）
2. PDF 精读（Kamin 2025 GEAT scope / Portmann-Renner 2022 framework）
3. 判断 CONJ1 是否成立（γ path reformulation decision）

---

## 7. β.G3 解析结果闭环（2026-04-23 晚间追加）

**完成动作**：
1. dev-reviewer skill 双 Codex 评审：R1 FAIL → 修复 → R2 PASS
   - 修复 1: `TestLogNegAmplitudeDampingAnalytic` 移出模块级 MOSEK skip（独立 class-level `@_MOSEK_SKIP`）
   - 修复 2: 新增 3 个中间步骤测试（Choi 矩阵、PT 块、特征值集）
   - 修复 3: §2.2 明确 η=0 平凡边界解 vs η_c=1/φ 非平凡内点解
2. SymPy C1(c) 符号独立验证：全部 6 项断言 `True`
   - 特征值 [1/2, -η/2]、迹范数 η+1、因式 -η(η²+η-1)、根 (√5-1)/2
3. 用户 2026-04-23 显式 C2 签字确认数学正确性

**R0.2 三方验证状态**：
- C1(c) ✅ SymPy（`docs/workflow/beta-G3-analytic-proof-review/sympy-c1c-verification.md`）
- C2 ✅ 用户 2026-04-23 签字（commit `300945d`）
- C3 ✅ dev-reviewer R2 PASS

**分级决定**：标签保持 **[SYN]**（非 [COROLLARY]）
- 理由：当前推导是项目内独立计算，无外部 [THM] 锚点
- R0.3 中 [COROLLARY] 语义要求"从已有 [THM] 机械推导"
- 三方验证确认数学正确，但分级语义不允许自升 [COROLLARY]

**影响范围**：
- §1.2 β.G3 Layer 3 条目由 "[SYN，待用户复核]" 更新为 "[SYN，C1(c)+C2+C3 三方已确认]"
- 内部引用资格：数学正确性确认，符合 R0.3 [SYN] 级规则
- 对外引用资格：仍需外部 THM 锚点（未来文献工作）

**相关 commits**：
- `33af74d`: SymPy C1(c) 验证记录
- `300945d`: C2 用户签字

---

## Changelog

- **v0.2** (2026-04-23 evening): §7 追加 — β.G3 三方验证闭环；[SYN] 保持
- **v0.1** (2026-04-23 Day 3 session): 首稿，等待用户审阅
