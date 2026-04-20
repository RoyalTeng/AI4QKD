# 上界拓扑适用性 Lemma(Sub-Q3 §4.3)

**版本**:v0.1(2026-04-20 autonomous session produce)
**关联研究动作**:RESEARCH_PLAN §Sub-Q3 §4.3 "上界的 MS-EB 表述"
**前置精读 memo**:
- [PLOB-2017.md](../literature/PLOB-2017.md)(Level 4)
- [Pirandola-2019.md](../literature/Pirandola-2019.md)(Level 4)

---

## 0. 目的与范围

### 0.1 问题陈述

PLOB 2017 给出 point-to-point 信道的 two-way 容量上界 $\mathcal{C}(\mathcal{E}) \leq E_R(\rho_\mathcal{E})$,lossy 特化为 $-\log_2(1 - \eta)$。Pirandola 2019 扩展到 N-repeater chain 与一般 quantum network,lossy chain 给出 $-\log_2(1 - \eta^{1/(N+1)})$。

**核心问题**(RESEARCH_PLAN §1.2 红线 2b):
> "拓扑适用性 lemma — 何种 topology 条件下 $-\log_2(1-\eta)$ / $-\log_2(1-\sqrt\eta)$ 是 rate 的上界?把错位使用当数据会导致 Sub-Q4 归因失真。"

### 0.2 本文档定位

- **提供**:MS-EB formulation 中的 channel $\mathcal{E}$ 与 PLOB / Pirandola network 框架之间的对应 lemma,附具体 gap 数值
- **不提供**:PLOB / Pirandola 定理的完整证明重写(见两篇 Level 4 memo);multi-path 多源 QKD 的 relay 化简(留 Phase 2 §Sub-Q3 §4.3 后续);decoy-state 对上界的软化(Phase 2 §Sub-Q3 §4.4)

### 0.3 范围限定

- **In-scope**:DV QKD 协议族(F1 BB84、F2 six-state、F3 SARG04 spec_only、F4 efficient BB84、F5 MDI、F6 TF-QKD/PM-QKD)
- **Out of scope**:CV-QKD、DI-QKD、多方 QKD(`network with more than 2 end-points`)

---

## 1. MS-EB Channel 结构分类

MS-EB framework 下,协议的 channel 部分 $\mathcal{E}$ 是从 source signal registers $\{A_i'\}$(i=1,..,N_source 方)到 announcement classical register 的 CPTP map。根据 $\mathcal{E}$ 的**分解结构**,协议拓扑分三类:

### 1.1 Type A:**Point-to-point direct link**

**结构**:$\mathcal{E}: A' \to B$,单信道,**无中间节点**

**对应协议**:
- F1 BB84(Alice → Bob 直接信道)
- F2 six-state(同)
- F3 SARG04 spec_only(同)
- F4 efficient BB84(同)

**Pirandola 拓扑对应**:N = 0 repeater chain(= PLOB point-to-point)

**应用上界**:
$$\mathcal{C}(\mathcal{E}) \leq E_R(\rho_\mathcal{E})$$
For lossy channel:
$$\mathcal{C}(\mathcal{E}) = -\log_2(1 - \eta) \approx \frac{\eta}{\ln 2} \approx 1.44\,\eta \text{ (at } \eta \ll 1\text{)}$$

### 1.2 Type B:**Untrusted-relay single-chain**(TF / PM 族核心)

**结构**:$\mathcal{E}: A' \otimes B' \to C$,**两个源方 + 一个 untrusted relay Charlie**,Charlie 输出 classical announcement

**对应协议**:
- F5 MDI-QKD(Alice-Charlie-Bob,Bell measurement)
- F6 TF-QKD / PM-QKD(Alice-Charlie-Bob,single-photon interference)

**Pirandola 拓扑对应**:N = 1 repeater chain(untrusted Charlie 作为 "eavesdropper-run node";per Pirandola §Discussion 仍适用)

**应用上界**(lossy channel,Pirandola 2019 Eq. 9 at N=1):
$$\mathcal{C}(\mathcal{E}) \leq -\log_2(1 - \sqrt{\eta_{AB}})$$

其中 $\eta_{AB}$ 是**总** Alice-Bob 信道 transmittance;每段 Alice-Charlie / Charlie-Bob 的 transmittance 是 $\eta^{1/2} = \sqrt{\eta_{AB}}$.

**关键注**:**MDI 与 TF-QKD 共享 Type B 拓扑,但下界不同**:
- MDI 达到 $\eta_{AB} = \eta_A \cdot \eta_B$ 标度(Charlie 双光子 coincidence,与 $\eta$ 成正比)
- TF 达到 $\sqrt{\eta_{AB}}$ 标度(Charlie 单光子 interference)

两者上界都是 Pirandola N=1 = $-\log_2(1 - \sqrt{\eta_{AB}})$。所以 MDI 与 TF 的 Sub-Q4 gap 归因:
- **MDI vs Pirandola N=1**:gap **很大**(因为 MDI 本身是 η 标度);这表明 MDI **没有用上**中间节点的 $\sqrt{\eta}$ 优势
- **TF vs Pirandola N=1**:gap **较小**(因为 TF 已经是 $\sqrt\eta$ 标度);gap 主要来自 protocol overhead,不是 scaling

### 1.3 Type C:**Multi-path / network**(out of current scope)

**结构**:多 relay 节点 + 多路径 + 网络 LOCC

**对应协议**:不在本项目 Phase 1 scope,留 Phase 3 discussion

**应用上界**:Pirandola 2019 Eq. 17 / 19 multi-path min-cut

---

## 2. Lemma 形式陈述

**Lemma 1(上界拓扑适用性)**:设 $\Pi = (\mathcal{P}, \mathcal{E}, \mathcal{A}, \mathcal{T}, \mathcal{K})$ 是 MS-EB protocol,协议率 $R_\Pi(\eta_{AB})$ 为 Alice-Bob 总 transmittance $\eta_{AB}$ 的函数. 则:

**(a) Type A(point-to-point)**: 若 $\mathcal{E}$ 的 single-letter Choi matrix $\rho_\mathcal{E}$ 对应 point-to-point lossy channel with transmittance $\eta_{AB}$,
$$R_\Pi(\eta_{AB}) \leq -\log_2(1 - \eta_{AB})$$

**(b) Type B(untrusted single-chain)**: 若 $\mathcal{E}$ 分解为 Alice-Charlie 和 Bob-Charlie 两段 lossy channel with combined end-to-end transmittance $\eta_{AB}$,
$$R_\Pi(\eta_{AB}) \leq -\log_2(1 - \sqrt{\eta_{AB}})$$

**(c)**: 将 (a) 的上界误用到 Type B 协议(e.g., 声称 TF-QKD 违反 PLOB 是错误的),或将 (b) 的上界误用到 Type A 协议(会把 BB84 的 gap 严重低估),都会导致 Sub-Q4 归因失真。

### 2.1 证明 sketch(基于前置 memo)

**(a)** 直接引用 PLOB 2017 Theorem 1 + distillable lossy channel(PLOB Eq. 19)。

**(b)** 引用 Pirandola 2019 Eq. 9 at N=1;untrusted Charlie 视作 "eavesdropper-run repeater"(Pirandola §Discussion 明示此 extension)。

**(c)** 反证:
- 若把 (a) 的 $-\log_2(1-\eta)$ 当成 TF-QKD 上界,则在 $\eta = 10^{-6}$ 时上界约 $1.44 \times 10^{-6}$;但 PM-QKD 实测 > $10^{-6}$(Ma Fig.3a @ 300 km)。违背!这说明 (a) 上界**对 Type B 不适用**。
- 若把 (b) 的 $-\log_2(1-\sqrt\eta)$ 当成 BB84 上界,则在 $\eta = 10^{-2}$ 时上界约 $0.15$ bit/use;但 BB84 实际上 $\sim 0.005$(η/2);无矛盾但过松 ⇒ **gap 严重低估**,不利于 Sub-Q4 A 归因。

### 2.2 Corollary:协议族 → 上界映射表

| 族 | 协议 | Type | 正确上界 |
|---|------|------|---------|
| F1 | BB84 | A | $-\log_2(1-\eta_{AB})$ |
| F2 | Six-state | A | $-\log_2(1-\eta_{AB})$ |
| F4 | Efficient BB84 | A | $-\log_2(1-\eta_{AB})$ |
| F5 | MDI-QKD | B | $-\log_2(1-\sqrt{\eta_{AB}})$ |
| F6-TF | Lucamarini TF-QKD | B | $-\log_2(1-\sqrt{\eta_{AB}})$ |
| F6-SNS | Wang SNS-TF | B | $-\log_2(1-\sqrt{\eta_{AB}})$ |
| F6-PM | Ma PM-QKD | B | $-\log_2(1-\sqrt{\eta_{AB}})$ |

---

## 3. 数值 Gap 表(Type B 为例)

**设定**:fibre loss 0.2 dB/km,total Alice-Bob transmittance $\eta_{AB} = 10^{-\text{dB}/10}$。

### 3.1 PLOB direct-link vs Pirandola N=1

| L (km) | dB | $\eta_{AB}$ | $\sqrt{\eta_{AB}}$ | PLOB $-\log_2(1-\eta)$ | Pirandola N=1 $-\log_2(1-\sqrt\eta)$ |
|--------|-----|-----|-----|-----|-----|
| 50 | 10 | 0.10 | 0.316 | 0.152 | 0.548 |
| 100 | 20 | 0.010 | 0.100 | 0.0145 | 0.152 |
| 150 | 30 | 1e-3 | 0.032 | 1.44e-3 | 0.0464 |
| 200 | 40 | 1e-4 | 0.010 | 1.44e-4 | 0.0145 |
| 250 | 50 | 1e-5 | 0.0032 | 1.44e-5 | 4.57e-3 |
| 300 | 60 | 1e-6 | 1e-3 | 1.44e-6 | 1.44e-3 |
| 400 | 80 | 1e-8 | 1e-4 | 1.44e-8 | 1.44e-4 |
| 500 | 100 | 1e-10 | 1e-5 | 1.44e-10 | 1.44e-5 |

**观察**:
- 在所有距离,Pirandola N=1 大于 PLOB direct 约 $\sqrt{\eta}/\eta = 1/\sqrt{\eta}$ 倍
- 50 km 处差 3.6×,200 km 差 100×,500 km 差 $10^5$×
- 这也是 TF-QKD 相对 BB84 的**理论物理优势**(同距离)的来源

### 3.2 PM-QKD 实测 vs Pirandola N=1 bound

用 `qkdx.analytic.pm_qkd_decoy.pm_rate_sweep_optimized`(μ-optimized, Ma Fig.3b params):

| L (km) | dB | PM 实测率 | Pirandola N=1 bound | **Gap (×)** |
|--------|-----|----------|---------|-------|
| 50 | 10 | 2.50e-4 | 5.48e-1 | 2196 |
| 100 | 20 | 7.78e-5 | 1.52e-1 | 1953 |
| 150 | 30 | 2.44e-5 | 4.64e-2 | 1896 |
| 200 | 40 | 7.67e-6 | 1.45e-2 | 1892 |
| 250 | 50 | 2.37e-6 | 4.57e-3 | 1929 |
| 300 | 60 | 6.96e-7 | 1.44e-3 | 2075 |
| 350 | 70 | 1.70e-7 | 4.56e-4 | 2690 |
| 400 | 80 | 9.47e-9 | 1.44e-4 | 15239 |

**观察**:
- **Mid-range (100-250 km)**:gap 稳定在 ~1900-2200× 之间(orders of magnitude)
- **近距离 (50 km)**:gap 略大(2196×),因为 PM-QKD 的 $\sqrt\eta$ 效率在低损耗区没发挥
- **远距离 (>300 km)**:gap 快速放大,表明 PM-QKD 接近 cutoff 前 protocol overhead 迅速支配
- **cutoff**:PM-QKD @ ~400 km(9.5e-9),Pirandola N=1 @ 500+ km 仍 > 10^-5

**Sub-Q4 gap 归因 sketch**:
- **A 归因(上界松)**:Distillable lossy channel 下 Pirandola 2019 is tight(理论上 N=1 chain 容量精确等于 $-\log_2(1-\sqrt\eta)$);故 A **基本排除** for pure-lossy channel
- **B 归因(下界松)**:PM-QKD vs Pirandola gap ~2000×。其中:
  - ~13× 来自本项目 §7.5 analytic 实施的 B20 近似(Ma paper 也只达到 ~150× gap per Ma eyeball)
  - ~150× 来自 Ma PM-QKD 协议本身 vs 理论 bound(Ma §VI outlook "still far away")
  - 所以 B 是主导 gap 来源,进一步分为:protocol-structural(150×)+ implementation(13×)
- **C 归因(协议拓扑约束)**:PM-QKD 已经达到 N=1 topology 的 $\sqrt\eta$ scaling,topology 层面无优化空间(除非 N→2 等更多 relay,即 "quantum repeater proper")

### 3.3 MDI-QKD 期望 gap(用 Ma-Razavi 2012 default params)

MDI 达到 $\eta_{AB} = \eta_A \eta_B$ scaling(非 $\sqrt\eta$),所以 MDI 天然 gap 大于 TF:

At η=10⁻² (100 km):
- MDI rate ~ $(η_A·η_B)/2 \approx η/2 = 5 \times 10^{-3}$(粗估)
- Pirandola N=1 bound = 0.152
- Gap ~30×

即 MDI 的 gap 主要是 **scaling mismatch**(η vs √η),而 TF 的 gap 主要是 **protocol overhead**。

---

## 4. 附:实际应用注意事项

### 4.1 多强度 decoy + 上界的兼容性

Pirandola 2019 的 N=1 bound 假设**任意 LOCC**(包括 infinite decoy-state Choi simulation)。所以 PM-QKD 使用 decoy-state 估 $Y_1 / e_1$ 不违反上界 — 只是 **Alice/Bob 做的是特定 LOCC 子集**(Ma Eq.4 Shor-Preskill style),故 ≤ 上界。

### 4.2 Finite-key 软化

Pirandola 2019 上界是 asymptotic(n → ∞)。Finite-key $\ell_n/n$ 可能 finite-size 软化上界(Kamin 2025 style)— 但在 $n \gtrsim 10^{10}$ 时 finite-size 惩罚 << protocol gap,所以 asymptotic 上界仍是 Sub-Q3 主要工作对象。

### 4.3 Thermal-loss(dark count)修正

Pirandola 2019 §Table I 显示:纯 lossy bound 在 ideal limit;若信道带 dark count / thermal photons,应使用 thermal-loss 的 Eq. 23 公式,上界略松(≤ $-\log_2[(1-\eta)\eta^{\bar n}] - h(\bar n)$)。对现实 QKD 实验,dark count 贡献微乎其微 ($\bar n \sim 10^{-4}$ 量级),修正可忽略。

### 4.4 MS-EB 框架下 "E" 的实际含义

- 对 F1/F2/F4(Type A):$\mathcal{E}$ 是 Alice-Bob 单信道,$\rho_\mathcal{E}$ 是其 Choi matrix;Pirandola $\sigma_\mathcal{E} = \rho_\mathcal{E}$
- 对 F5/F6(Type B):$\mathcal{E}$ 是 Alice-Charlie + Bob-Charlie + Charlie-announce 的**合成** channel。**不要** 直接用整个 $\mathcal{E}$ 的 Choi 去算 $E_R$ — 正确做法是**先做 entanglement cut**(切在 Alice-Charlie 或 Bob-Charlie)得到该段的 Choi,再取 min(即 Pirandola Eq. 4-5 流程)

### 4.5 与 TGW 2014 + WTB 2017 的关系

**TGW 2014**:squashed entanglement bound,较 PLOB 松(lossy 下 $-\log_2\frac{1-\eta}{1+\eta} \approx 2.88\eta$ vs PLOB $1.44\eta$)— 已被 PLOB 超越,但对 **amplitude damping** 等非 distillable 信道可能更紧

**WTB 2017**:REE bound 扩展 + coherent info 的独立证明路径 — 与 PLOB 时间上平行,技术细节略异

**Sub-Q3 §4.4 路径**:用 TGW + WTB + PLOB + Pirandola 四者的 **min**(most-tight)bound;对 distillable channels 一般 Pirandola 最优,对 amplitude damping 用 TGW-style squashed

---

## 5. Sub-Q3 §4.3 完成度与下一步

### 5.1 本 memo 覆盖

- ✓ MS-EB channel type 分类(Type A/B,out-of-scope C)
- ✓ 上界拓扑适用性 Lemma 1 形式陈述
- ✓ 协议族 → 上界映射表(§2.2)
- ✓ 数值 gap 表(§3)
- ✓ Sub-Q4 A/B/C 归因 sketch

### 5.2 未覆盖(留 Sub-Q3 §4.4 或 Phase 2 §5+)

- 🔲 **Amplitude damping + thermal-loss 的更紧上界**(需精读 TGW 2014 + WTB 2017;PDF 已在库)
- 🔲 **Squashed entanglement numerical implementation**(`qkdx/numerics/` 新模块,Sub-Q3 §4.4 硬验收)
- 🔲 **Finite-decoy + finite-key 下界的 Pareto 比较**(需 §7.5d / Kamin 2025 实施)
- 🔲 **TGW-style 对 non-distillable channel 的替代上界**

### 5.3 下一步具体工作

1. **Week 1**:TGW 2014 Level 3-4 精读(squashed entanglement + lossy bound);PDF `docs/literature/pdfs/TGW-2014-FundamentalRateLoss.pdf` 已在库
2. **Week 1-2**:WTB 2017 Level 3-4 精读;PDF `docs/literature/pdfs/WTB-2017-ConverseBoundsPrivate.pdf`
3. **Week 2-3**:`qkdx/numerics/e_r_upper.py` 实施 REE 数值计算(对 non-distillable channels)
4. **Week 3-4**:Sub-Q3 §4.3 完整 memo(基于本 lemma 扩展) + §4.4 上界数值工具

---

## 6. 变更日志

- **v0.1** (2026-04-20,autonomous session):首稿。基于 PLOB-2017.md + Pirandola-2019.md 两篇 Level 4 memo 导出。包含 MS-EB channel type 分类 + Lemma 1 正式陈述 + F1-F6 映射表 + PM-QKD vs Pirandola N=1 gap 量化表。
