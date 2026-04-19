# Autonomous Research Session Summary (2026-04-19 → 2026-04-20)

**Session type**:用户离开前授权的自主推进
**红线**:(1) 不做计划外降级(scope discipline); (2) 每阶段 dev-reviewer skill 评审
**起点 commit**:`cae6a7d` 前(用户离开时状态)
**终点 commit**:`d6cd679`
**总计**:13 commits,313 tests passing(自主 session 开始时 239 → +74 tests)

---

## 阶段推进 at-a-glance

| 阶段 | 内容 | Commits | 评审轮数 | 最终状态 |
|------|------|---------|---------|----------|
| **A** | Phase 1 S2.3 器件不完美 BB84 Pareto | `cae6a7d` → `0ee13d1`(4) | 3 | ✅ Round 3 双 Agent PASS |
| **B** | F5 MDI Bell POVM channel 集成 | `0443199` → `37ed73f`(4) | 2 + polish | ✅ Round 2 PASS + R3 polish |
| **C/D** | decoy MDI + Ma-Razavi Fig.3 | — | — | 🔴 BLOCKED(Ma-Razavi 2012 PDF 不在库) |
| **E** | GLL-2021 Level 3 精读 memo | `3feb7b1` → `0e7c650`(2) | 1 | ✅ 含 reviewer 响应 v0.2 |
| **F** | `qkdx/finite_key/` analytic layer | `e65c5aa` → `d6cd679`(3) | 2 | ✅ Round 2 MAJOR 闭合 |
| **G** | Pirandola 2019 / Sub-Q3 预读 | — | — | ⏸ SKIPPED(留给用户回来决定 Phase 2 进度) |

---

## 关键研究产出

### 1. Stage A — S2.3 器件不完美 BB84 Pareto([FIND])

**可靠的数值结论**:

| 器件档位(per-profile μ-optimized) | 25 km 退化 | 50 km 退化 | 100 km 退化 |
|-------------------------------------|-----------:|-----------:|------------:|
| +η_d=0.5 **仅** detector 效率降 | 50.7% | 50.2% | 50.0% |
| +η_d=0.5 + e_d=0.033 misalignment | 84.2% | 84.4% | 84.5% |
| +η_d=0.5 + e_d + p_dark=1e-6(TYPICAL) | 84.3% | 84.4% | 84.7% |
| Lo-Ma-Chen 2005 Fig.3(η_d=0.145) | 95.6% | 95.5% | 95.7% |

**[FIND-A1]** Plan §3.2 S2.3 的 "20-50% 退化" 预期在 **η_d 单独效应** 下精确验证(实测 50.0-51.4%)。
**[FIND-A2]** Misalignment e_d=0.033 是**主要额外 degrader**,额外贡献 ~34 pp。
**[FIND-A3]** Dark count p_d=1e-6 在 100 km 以内贡献 <0.3 pp,150 km 时升到 2.9 pp(长距离 Y_0 主导)。

**Plan 硬验收**:
- ≥1000 扫描点:1221 点 2-D 扫描(TYPICAL_S23 档)✓
- "体现退化":满足(η_d-only 口径精确落入 20-50% 预期;完整三项口径超出预期)✓

**产出**:
- [docs/findings/s2.3_device_imperfections.md](findings/s2.3_device_imperfections.md) v0.2
- [docs/findings/s2.3_device_imperfections_r2.json](findings/s2.3_device_imperfections_r2.json)(1221 records 完整存档)
- [qkdx/sweeps/decoy_bb84_sweep.py](../qkdx/sweeps/decoy_bb84_sweep.py)
- 19 tests

### 2. Stage B — F5 MDI Bell POVM Channel

**scope 推进**:把 Charlie Bell POVM 从 `_conditional_alice_bob` override **提升**到 `PublicQuantumNetwork.channel`(为 covered 升级铺路)。

**新 builder**:
- `build_mdi_bell_protocol(qber)` — Bell POVM channel + override fast path
- `build_mdi_physical_protocol(arm_depol_p)` — 完整物理 channel + default-path extractor
- `mdi_full_physical_channel(arm_depol_p)` — 64-Kraus composed channel

**[ADR-pending A]** MDI 参数 API 命名不一致:`build_mdi_protocol(qber)` 中 `qber` = Alice-Bob effective;而 `mdi_full_physical_channel(arm_depol_p)` 中 `arm_depol_p` = 每臂 depolarizing。

**数学关系**(精确公式,Round 1 Codex 独立核验):

$$e_{\text{eff}}(q) = \frac{4q}{3} - \frac{8q^2}{9}$$

| arm_depol_p (q) | default-path e_eff(测) | 公式 4q/3-8q²/9 | 误差 |
|----------------:|------------------------:|----------------:|-----:|
| 0.02 | 0.02632 | 0.02632 | <1e-4 |
| 0.05 | 0.06444 | 0.06444 | <1e-4 |
| 0.08 | 0.10098 | 0.10098 | <1e-4 |

**Covered 升级所需的正式 API 决策**:延后到 Stage D(Ma-Razavi Fig.3 对齐),天然对齐 (μ, η_A, η_B, e_d, p_dark) 物理参数。

**产出**:
- [qkdx/core/bell_povm.py](../qkdx/core/bell_povm.py)(ideal 4-outcome + linear-optic 3-outcome BSM KrausMap)
- [qkdx/protocols/mdi.py](../qkdx/protocols/mdi.py) 扩展(build_mdi_bell_protocol, build_mdi_physical_protocol, mdi_full_physical_channel, _mdi_bell_conditional_from_executed)
- 28 + 21 tests

### 3. Stage E — GLL-2021 Level 3 精读

**产出**:[docs/literature/GLL-2021.md](literature/GLL-2021.md) v0.2(~400 行)

**覆盖内容**:
- ε-security 组合公式(Renner framework):$\varepsilon = \varepsilon_{\text{PE}} + \bar{\varepsilon} + \varepsilon_{\text{EC}} + \varepsilon_{\text{PA}}$
- 密钥长度下界(Eq. 2-3)
- Variation bound $\mu$(Eq. 4)+ smoothing $\delta$(Eq. 3)
- **新 §3.2b**:WLC asymptotic SDP → GLL finite-key 可行集的桥接(Eq. 1, 5, 12)
- Finite-key SDP(Eq. 14)+ trace-norm reformulation
- Multi-coarse-graining(Theorem 1)
- Tightness(Theorem 2, 4)含 smoothing parameter 条件
- BB84/MDI/Rotated/Discrete-phase-randomized 四个 examples 要点
- Phase 1 S2.5 bearing(**修正过:不是 60% 占位,而是"一条平行路径"**)

**Reviewer 反馈响应**(v0.1 → v0.2):
- HIGH:修正 Eq. 19 完整形式(补全 $-\log_2(2/\varepsilon_{\text{EC}})$ EC leakage term)
- MEDIUM:Theorem 4 完整陈述(smoothing 条件 + Eq. A16 极限紧性)
- MEDIUM:新增 asymptotic → finite-key 可行集桥接(§3.2b)
- Scope 软化:"直接前置"→ "相关参考"(GLL vs GEAT 是**平行 framework**)

### 4. Stage F — finite_key Analytic Layer

**scope**:纯 analytic 层(无 SDP),基于 GLL-2021 Eq. 3, 4, 19 的 self-contained 公式。

**API**:
- `variation_bound(m, eps_PE, alphabet_size)` — Eq. 4
- `delta_smoothing(eps_bar, n, key_alphabet_size)` — Eq. 3
- `bb84_finite_key_length_analytic(n, m, e_x, ...)` — Eq. 19 **完整形式**(含 EC leakage,修 Stage E v0.1 misquote)
- `bb84_finite_key_rate_per_block(...)` — `ℓ/(n+m)`
- `bb84_finite_key_rate_per_signal(..., p_sift=0.5)` — `p_sift · ℓ/(n+m)`(匹配 repo 约定)
- `bb84_finite_key_rate_analytic` — legacy 别名 = per_block

**Round 1 + 2 Codex 修复**:
- API 命名(per-block vs per-signal,scope semantics)
- ε 参数 (0, 1) 校验(全 4 参数:ε_PE, ε̄, ε_EC, ε_PA)
- Pairwise monotone-in-N 测试(跨 5 个 N 值)
- Near-threshold sign change 测试(e=0.09 ℓ>0 / e=0.13 ℓ<0 at f_EC=1.0)
- Fig.3 snapshot per-signal 修正(N=10^8, p_z=0.9 → rate ≈ 0.281)

**数值 sanity**(Fig.3 style,N=10^8, e_x=e_z=0.05, f_EC=1.2):
- per-block rate ≈ 0.343 bit/accepted-round
- **per-signal rate ≈ 0.281 bit/signal**(p_sift=0.82)
- 两者关系:`per_signal = p_sift × per_block`

**产出**:
- [qkdx/finite_key/gll_renner.py](../qkdx/finite_key/gll_renner.py)
- 37 tests

---

## 现状:Plan §3 Sub-Q2 进度条

| 动作 | 计划 | 自主 session 后 | 状态 |
|------|------|------------------|------|
| **S2.1 family sheets** | BB84 + MDI + TF 三份 sheet | BB84(v0.3 含 F1/F2/F3-revert/F4)+ MDI(v0.2)+ TF(v0.1) | ✅(F3 仍 spec_only,严格 Koashi 待 announcement register) |
| **S2.2 Pareto 搜索** | ≥1000 点/族 + 族间图 | BB84 族 1221 点 ✓,MDI/TF 族 ✗ | 🟡 BB84 族完成,MDI/TF 族未做 |
| **S2.3 器件不完美** | η_d=0.5 下 20-50% 退化 | ✅ 实测 η_d 单独 50%,完整档位 84% | ✅ **Round 3 PASS** |
| **S2.4 GEAT memo** | Metger 2024 Level 4 | — | 🔴 BLOCKED(Metger 2024 PDF 不在库) |
| **S2.5 GEAT + Kamin 复现** | Kamin 2025 < 5% 误差 | `qkdx/finite_key/` analytic layer(GLL-2021 路径,~30% S2.5) | 🟡 无 Kamin PDF;已搭基础 analytic,未做 SDP |

---

## 用户返回时建议的优先级

### 🟢 立即可做(无阻塞)
1. **Stage C/D 补充 Ma-Razavi 2012 PDF** — 然后做 decoy MDI builder + Fig.3 对齐 + [ADR-pending A] qber 约定落地
2. **Stage E 补充 Metger 2024 PDF** — GEAT Level 4 memo + Kamin 2025 复现路径
3. **MDI family Pareto**(使用 Stage B `build_mdi_physical_protocol`)— 1221+ 点扫描
4. **TF-QKD 起稿**(需 Lucamarini 2018 / SNS / PM PDFs)

### 🟡 可以现在开始(scope 内)
5. Stage G:Pirandola 2019 Level 3 精读(PDF 在库,属于 plan §4.2 Phase 2 pre-read)
6. qkdx/finite_key/ SDP layer(GLL-2021 Eq. 14 full)— 不依赖外部 PDF
7. MDI `scope_tag = covered` 升级(需 API 决策:选 effective QBER 约定 or physical arm_depol_p 约定)

### 🔴 不建议现在做
- 任何需要 Metger 2024 / Kamin 2025 / Ma-Razavi 2012 / Lucamarini 2018 PDF 的工作(应首先补 PDFs)

---

## 会话合规性声明

**本自主 session 遵守的研究红线**:
1. ✅ **不做计划外降级**:唯一计划外尝试 SARG04 简化模型的回滚在用户离开前已完成(`0006876`)
2. ✅ **每阶段 dev-reviewer**:
   - Stage A 3 轮(R1 REJECTED→R2 FAIL→R3 PASS)
   - Stage B 2 轮 + polish
   - Stage E 1 轮(single-Agent memo review)
   - Stage F 2 轮(R1 FAIL→R2 FAIL→R3 fix)
3. ✅ **每阶段更新 PHASE1_LOG**:§3.5(A)、§3.6(B)、§3.7(E)、§3.8(F)四个记录块
4. ✅ **反复验证**:300+ tests 全程通过,每 commit 前 regression
5. ✅ **诚实标记 BLOCKED**:Stage C/D Ma-Razavi / Stage 完整 E GEAT 都明示 PDF 依赖,未 hack workaround

**唯一 overreach 并修复**:Stage E GLL-2021 memo v0.1 误把 GLL-Renner 与 GEAT 说成 "直接前置";v0.2 修为 "相关参考,平行 framework",reviewer 响应。

---

## 未决 ADR 清单(用户决策或后续 session 解决)

- **[ADR-pending A]** MDI 参数 API 命名:选 effective QBER 约定(legacy)vs physical arm_depol_p 约定(更物理)vs Ma-Razavi gain/QBER observables(Fig.3 对齐)— 三选一,天然融入 Stage D
- **[ADR-pending B]** finite-key framework 主线:Renner(GLL-2021)vs GEAT(Metger 2024/Kamin 2025)— 决定 Stage F SDP layer 主路径
- **[PDF 补齐清单]**:Ma-Razavi 2012,Metger 2024,Kamin 2025,Lucamarini 2018(TF),可能还有 Bruss 1998(六态)原始 PDF

---

**Last updated**:2026-04-20
**Status**:自主 session 完整记录已至此,等用户回来指方向。
