# Sub-Q4 G4.2: Gap 归因分析 (基于 Day 4 数据)

**版本**: v0.1 [CONJ 级]  
**日期**: 2026-04-24 自主 session  
**对应**: RESEARCH_PLAN §5.2 G4.2 "归因三种原因的结构化诊断"  
**严谨性**: [CONJ]（所有上界候选仍 [CONJ]；gap 形状 [SYN]）

---

## 0. 重要免责（R0.1 红线）

本 memo 是 RESEARCH_PLAN §5.2 硬验收要求的归因分析**初稿**。FINDINGS v2 §4.2 明确要求：

> Sub-Q4 归因 α/β/γ 应在 Sub-Q3 完成之后基于**定理级上界**重新启动，不以本 interim 为预定位

当前 Sub-Q3 [CONJ] 上界候选（路径 α/β/γ 全部 OPEN）→ 归因本身也是 [CONJ]。用户升级 UB 至 [THM] 后本 memo 必须重新跑。

---

## 1. 归因三类原因定义（PROSPECTUS Sub-Q4）

| 类别 | 含义 | 诊断方法 |
|------|------|---------|
| **A** | UB 松（真紧界比本项目 UB 候选紧） | 用更紧的已知界 / 真值 proxy（如 E_R、已知 K^{↔} 真值）比较 |
| **B** | LB 松（协议 Pareto 未穷尽） | 协议变体扫描残差 / 已知解析紧界对比 |
| **C** | A + B 都非零 | A 和 B 同时诊断都有显著贡献 |

**Gap shape 观察**（`gap_shape_g4_1.md` v0.3 + 本文 §2）：
- UB cand A/B (Pirandola Type B) : TF LB = ~2000× 在工作区
- 这个 2000× 倍数**本身不区分** A/B/C —— 需要更深诊断

---

## 2. 信道级紧界数据（Day 4 建立）

### 2.1 四信道 UB-LB 紧度矩阵

| 信道 | 最紧 channel UB | 最紧 channel LB | channel UB/LB ratio | Tele-covariant? |
|------|----------------|-----------------|---------------------|----------------|
| AD γ=0.2 | **channel UB 未知** (Choi-state E_R^PPT=0.61 不是 channel UB per WTB 2017, RETRACTION §8) | Q = 0.51 (channel, degradable, Q ≤ K^{↔}) | **UNKNOWN** | **No** |
| Dephase p=0.1 | E_R^PPT = 0.53 (channel UB via tele-cov) | K^{↔} = 0.53 (PLOB Eq.39) | **1.00×** (K^{↔} 层完美) | Yes |
| Depolar p=0.1 | E_R^PPT = E_R = 0.62 (channel UB via tele-cov) | K^{↔} UNKNOWN (K^{↔} ≤ E_R) | K^{↔} ≤ E_R；gap UNKNOWN | Yes |
| Erasure p=0.1 | log_neg = 0.93 (channel UB via tele-cov) | K^{↔} = 0.90 (PLOB Eq.43) | **1.03×** (接近紧) | Yes |

**结论（信道层面）**: 对 dephasing 和 erasure（tele-covariant per PLOB Ex.3），E_R^PPT/log_neg 工具给出**接近紧** channel UB（相对已知 K^{↔} 下界）。对 depolarizing（tele-covariant），E_R^PPT = E_R 是 channel K^{↔} 的严格 UB，但 K^{↔} 真值 UNKNOWN。**对 AD**（WTB 2017 确认非 tele-covariant），Choi-state E_R^PPT **不**自动转为 channel UB —— channel K^{↔}(AD) 真值 OPEN。

### 2.2 协议层面紧度（BB84/六态等效 depolarizing）

**[单位修正 2026-04-24]**: SP 率以 **bits/信号**，BB84 p_sift=0.5，六态 p_sift=1/3（先前 per-sifted 错误，已修正）。

| Protocol@QBER | UB (E_R, /signal) | LB (SP, /signal) | UB/LB | 主导因素 |
|---------------|-------------------|------------------|--------|---------|
| 六态@12.62% (阈值) | 0.453 | ≈0 | **∞** | 阈值处 SP → 0 |
| 六态@8% | 0.598 | 0.093 | **6.4×** | 六态仍优于 BB84 但非"接近紧" |
| BB84@5% | 0.714 | 0.214 | 3.34× | ~平衡 |
| **BB84@11% (阈值)** | 0.500 | ≈ 0 | **∞** | **B 主导**（SP 公式 2h(QBER) 非紧） |

### 2.3 umr 拓扑紧度（TF/MDI, 本项目核心）

| 拓扑@loss=40dB | UB cand (Pirandola Type B) | LB (Pareto best) | UB/LB |
|---------------|---------------------------|------------------|--------|
| MDI | 0.0145 | 9.21e-6 | **~1570×** |
| TF/PM-QKD | 0.0145 | 7.67e-6 | **~1890×** |

---

## 3. 归因诊断（**结构化**）

### 3.1 A 原因（UB 松）贡献诊断

**信道层面**（§2.1）: A 原因**接近零**。E_R^PPT SDP 在 qubit 信道上**达到真 E_R**（2⊗2 PPT=SEP per Horodecki 1996）。

**umr 拓扑层面**（§2.3）: A 原因**待诊断**。当前 Pirandola N=1 仍 [CONJ for umr]，路径 α/β/γ 全部 OPEN。
- **结构 gap β.G4** (Eve model transfer): OPEN — 用户纸笔工作需要
- **结构 gap γ.B.G1** (DPI target lemma): OPEN — 同上
- **结构 gap β.G5** (adversarial comb reduction): OPEN — 同上

若以上 gap 关闭 → Pirandola UB cand 升 [THM] → A 原因可精确量化。

**A 原因当前评估**: **UNKNOWN**（pending Sub-Q3 升级）。

### 3.2 B 原因（LB 松）贡献诊断

**BB84 SP 公式 1-2h(QBER)**: **显著松**。  
依据: 在 BB84 阈值 11% 处 SP → 0 而 E_R = 0.50（信道层 UB on K^{↔}）。真 K^{↔} ∈ [0, 0.50]，BB84 Shor-Preskill 给的 LB 远未触及信道上界。  
→ **B 原因在 BB84 协议上显著**。

**六态 SP 公式**（per-signal = `six_state_rate(QBER, f_ec=1.0)` ≈ (1/3)·(1-h(QBER)-QBER·log₂3)）: **非接近紧**（per-signal 单位下 3-6×）。  
依据: 六态 E_R/SP(per-signal) ≈ 3-6× 在工作 QBER 区；先前 ≤1.8× 数据是 per-sifted 单位错误，已撤回。[CONJ]  
→ **B 原因在六态协议上中等**，优于 BB84 但仍显著。

**TF/PM-QKD Ma-Zeng-Zhou 2018 公式**: **斜率紧, prefactor 可能松**。  
依据: §2.3 UB/LB ~2000× 在 40-60 dB；斜率同 √η。  
→ **B 原因可能在 prefactor 层面**（M=相位切片数 / decoy intensity 选择等）。但 TF/PM 公式已经是 protocol-family-optimal，"B 松"来自 family 内部参数而非协议本身。

**MDI**: 类似 TF，UB/LB ~1500× 主要来自噪声参数 (e_d, p_d) 主导 cutoff。

### 3.3 综合归因

对主问题 (PROSPECTUS §1 严格 H1-H6) 的主要 gap 贡献：

| 协议 | A (UB 松) | B (LB 松) | 当前分类 | 证据 |
|------|----------|----------|---------|------|
| BB84 (QBER > 8%) | UNKNOWN | **显著** | 倾向 B 或 C | §3.2 SP→0 at 11%, E_R=0.5 |
| 六态 | UNKNOWN | 中等 (3-6× per-signal) | UNKNOWN | §2.2 修正后 per-signal UB/LB ~3-6× |
| AD 信道自身 (degradable) | **UNKNOWN** (AD 非 tele-cov; Choi-state E_R^PPT 不是 channel UB per RETRACTION §8) | ~0 (Q 是 channel LB) | channel K^{↔}(AD) OPEN; channel-level UB 工具待精读 | §2.1 per-row disclaimer |
| TF/PM-QKD umr | UNKNOWN | 斜率紧 / prefactor 可能小 | UNKNOWN | §2.3 同 √η slope, 2000× prefactor |
| MDI umr | UNKNOWN | 噪声主导 | 类似 TF | §2.3 |

### 3.4 关键 OPEN 问题（决定归因的最终 verdict）

为得到 [THM] 级的 A/B/C 归因，需以下 4 个结构 gap 关闭（R0.2 C1+C2+C3）：

1. **β.G4 Eve model transfer**: TF-QKD Pareto 是否在 umr 拓扑下实际低于 Pirandola UB？
2. **β.G5 adversarial comb reduction**: amortization 在 untrusted relay 下是否继承？
3. **γ.B.G1 DPI target lemma**: 受信道数据处理不等式是否产生更紧上界？
4. **γ.G3 ε-composable transfer**: 可组合安全框架下 gap 是否变化？

这些 gap 均需用户 paper-level work + PDF 精读 (WTB 2017, Pirandola 2019, Khatri-Wilde 2020 §19 等)，AI 已在 Day 3 Session 尝试 4 paths/gap, 全部 OPEN 并留 concrete rationale。

---

## 4. 初步情况 A/B/C 判定（[CONJ]）

基于现有数据的**倾向性**判定（不是 [THM]）:

### 4.1 主问题 (H1-H6 严格版本)

**[UNKNOWN]** — Sub-Q3 结构 gap 未关闭，不能 [THM] 级判定。

### 4.2 放宽版 $\mathcal{T}_\text{umr}^\text{bosonic-asym}$ (FINDINGS v2 §0.2)

- TF/PM-QKD 斜率 √η 与 Pirandola UB cand 同 → **情况 A**（$\sqrt{\eta}$ 是紧 scaling）**最可能** [SYN]
- Prefactor gap ~2000× 可能是 B (下界 prefactor 松) 或 A (上界 prefactor 松) 或 C
- 归因分解 prefactor 需要 Phase 3 后半的精读工作 (α/β/γ 形式化)

### 4.3 qubit 信道族（Sub-Q3 工具链部分完备）

- **Dephasing** (tele-covariant per PLOB Ex.3): E_R^PPT = K^{↔}（PLOB Eq.39 验证）→ **信道层无 A 原因** [SYN]
- **Erasure** (tele-covariant): log_neg ≈ K^{↔} (gap ≤ 0.09 bits) → **信道层 A 原因小** [SYN]
- **Depolarizing** (tele-covariant): E_R^PPT = E_R（channel UB on K^{↔}），K^{↔} UNKNOWN → **A 原因 UNKNOWN**（K^{↔} ≤ E_R but K^{↔} true value not known）
- **AD degradable (γ ≤ 1/2)** (NOT tele-covariant per WTB 2017): Q (channel, LB on K^{↔}) ∈ [0.33, 0.83]；Choi-state E_R^PPT ∈ [0.50, 0.86] 是数据 benchmark **不是 channel UB**。channel K^{↔}(AD) 真值 OPEN → **A 原因 UNKNOWN** (see RETRACTION §8)
- **AD anti-degradable (γ > 1/2)** (NOT tele-covariant): Q=0；channel K^{↔} 真值 OPEN，**A 原因 UNKNOWN**（amortized / max-Rains / squashed entanglement 等工具待精读）

---

## 5. Limitations

1. 所有 UB cand 仍 [CONJ]，归因亦 [CONJ]（§0 免责）
2. 仅基于当前项目数据 + AI 识别的结构 gap；未做独立 PDF 精读
3. Prefactor 层面的 A vs B 分解需 Phase 3 后半工作
4. 未涵盖 BB84 + decoy state, MP-QKD (out_of_scope), RRDPS (out_of_scope per earlier 讨论)

---

## 6. 下一步（用户决定）

根据 §3.4 四个结构 gap 的关闭进度，归因会明确：

**若 A 原因被确认为主**: 转向改进证明工作（纯理论）  
**若 B 原因被确认为主**: Phase 3 §5.3 启动 AI 搜索（严格限定在 MS-EB 空间内，gap 位置精确指定）  
**若 C (A+B)**: 两条线并行  

**当前最高优先级**（user action needed）:
1. β.G4 Eve model transfer 结构论证（Khatri-Wilde 2020 §19 Prop 19.2 的适用范围精读）
2. WTB 2017 converse bound 在 untrusted relay 下的继承条件
3. Pirandola 2019 Eq. 9 / Fig. 3 的拓扑适用性核对（已知 Pirandola 拓扑为 trusted-relay，umr 继承需专属 lemma）

---

## Changelog

- **v0.1** (2026-04-24): 首版，基于 Day 4 完成的 4 信道 hierarchy 数据 + E_R bug 修复后的重新评估。
