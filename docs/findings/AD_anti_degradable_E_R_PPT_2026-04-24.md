# AD anti-degradable (γ > 1/2): E_R^PPT 作为 K^{↔} 的非平凡 UB

**日期**: 2026-04-24（Day 4 末 autonomous session）
**严谨性**: [SYN]（基于 Day 4 已修复 `e_r_channel_ppt` MOSEK SDP + Plenio-Virmani UB 继承）
**Scope**: qubit amplitude-damping 信道 γ ∈ (1/2, 1); 不涉及协议层或 umr 拓扑

---

## 0. 动机

Day 4 新加 `quantum_capacity_amplitude_damping_degradable(γ)` 给出 γ ≤ 1/2 的 AD 信道 Q（Caruso-Giovannetti-Holevo 2014 degradable single-letter）。γ > 1/2 进入 **anti-degradable** 区，Q = 0（Eve 获得 Bob 状态副本故 one-shot quantum capacity 为 0）。但 K^{↔}（两向辅助密钥蒸馏率）并**不**自动等于 0 —— 两向 LOCC 允许 Alice/Bob 用 Eve 无法完全模拟的交互协议。

**问题**: 对 γ > 1/2 的 AD 信道，K^{↔} 真值开放；有无可计算的 UB/LB？

---

## 1. 观察

Day 4 已有 MOSEK SDP 计算 `docs/research/data/qubit_E_R_PPT_SDP_all_4.csv`:

| γ | E_R^PPT (SDP, bits) | log_neg (analytic, bits) | Q (LB, 若 γ < 1/2) | Status |
|---|---|---|---|---|
| 0.05 | 0.8552 | 0.9635 | 0.8311 | degradable |
| 0.10 | 0.7590 | 0.9260 | 0.7094 | degradable |
| 0.20 | 0.6125 | 0.8481 | 0.5062 | degradable |
| 0.30 | 0.4984 | 0.7655 | 0.3280 | degradable |
| **0.50** | **0.3217** | 0.5850 | 0 (boundary) | **border** |
| **0.70** | **0.1830** | 0.3785 | **Q = 0** | anti-degradable |
| **0.90** | **0.0616** | 0.1375 | **Q = 0** | anti-degradable |

（Q 列通过 `quantum_capacity_amplitude_damping_degradable` 实时计算；其余来自 `qubit_E_R_PPT_SDP_all_4.csv` + `analytic_log_neg_amplitude_damping`。）

**关键结果**:

- **E_R^PPT(γ=0.7) = 0.183 bits**：非平凡 UB 上限，即使 Q = 0
- **E_R^PPT(γ=0.9) = 0.062 bits**：近归零但仍非零
- **log_neg 与 E_R^PPT 比率**（γ > 1/2 区）：0.585/0.322 ≈ 1.82, 0.379/0.183 ≈ 2.07, 0.138/0.062 ≈ 2.24 — log_neg 持续 ~2× 更松

---

## 2. 为什么 E_R^PPT > 0 有意义

**Horodecki 1996 2⊗2 PPT = SEP**（qubit Choi 状态 4×4）：对 qubit amplitude-damping 信道，E_R^PPT(ρ_Choi) = E_R(ρ_Choi)（真 Rains bound 等于 PPT-relaxed 值）。

**Rains 1999 + Christandl-Winter 2004** 级联结果:
- E_R 是 `D^{↔}_d`（两向辅助 distillable entanglement）的 UB
- 因 K^{↔} ≤ D^{↔}_d（蒸馏密钥不比蒸馏 ebit 多），故 **K^{↔}(AD γ) ≤ E_R^PPT(AD γ)**

所以对 γ = 0.7 的 AD 信道：

```
K^{↔}(AD, γ=0.7) ∈ [0, 0.183]   （严格 UB 来自 E_R^PPT）
Q(AD, γ=0.7)     = 0             （anti-degradable）
```

这个 0.183 是**目前可得的最紧 UB**，且由 SDP 数值严格。

---

## 3. [CONJ] 级观察：K^{↔}(AD γ>1/2) 是否 = 0？

**一种直觉**：anti-degradable 信道 Eve 有 Bob 副本，直接 distill 是 0。但两向 LOCC 允许 advantage distillation（Maurer 1993）+ 噪声正项化（Chitambar et al. 2016）。

**反例直觉**（未证）:
- AD γ=0.6 (仅略 > 0.5): 离 degradable 边界极近，K^{↔} 预计 > 0 via small perturbation arg
- AD γ→1 (全损耗): 物理上 K^{↔} → 0 因为 Bob 永远获得 |0>

**文献检查**（初步，仅 Pirandola 2019 / PLOB 2017 扫描）:
- PLOB 2017 §VII: 给出 **bosonic** amplitude-damping（pure-loss）的 K^{↔} = -log₂(1-η) 封闭式
- **qubit AD channel 的 two-way K^{↔} 在 γ > 1/2 未见解析式**
- Khatri-Wilde 2020 §19 可能涉及；待精读

**暂记 [UNKNOWN]** + E_R^PPT UB 可作数值挡路板。

---

## 4. 对 Sub-Q3 / Sub-Q4 的启示

### 4.1 Sub-Q3 上界工具链

- **E_R^PPT SDP 延伸到 γ > 1/2 区**: 即使 Q 工具在该区失效，SDP 仍给可计算 UB → 7 个数据点可直接加入 `upper_bound_report §11`
- **log_neg 在 γ > 1/2 仍 ~2× 松于 E_R^PPT**: log_neg 对 anti-degradable 区价值有限
- **protocol-specific LB** (e.g., 某 prepare-and-measure 协议 on AD γ=0.7) 可与 E_R^PPT UB 对比 → 量化 B (LB 松) 原因

### 4.2 Sub-Q4 gap 归因

若今后能对某 umr 协议（如一般 PM-QKD）做有效 qubit AD 信道建模:
- UB = E_R^PPT(γ_eff) 可作 A (UB 紧度) 的 proxy
- LB = 协议 Pareto 数值扫描
- gap 分解的信道层诊断框架扩展一条新 column

---

## 5. 提议的下一步（不在本 memo 完成）

- [ ] 计算 AD γ = 0.55, 0.6, 0.8 的 E_R^PPT SDP（补细化）
- [ ] 搜索 Khatri-Wilde 2020 §19 是否给出 AD γ > 1/2 的 K^{↔} 解析 UB
- [ ] 对某 PM-QKD 协议 + AD channel（γ=0.7）做 LB 数值扫描，与 E_R^PPT=0.183 对比
- [ ] 探索 squashed entanglement 是否对 AD γ > 1/2 给出比 E_R^PPT 更紧的 UB（文献: Takeoka-Guha-Wilde 2014）

---

## 6. 严谨性边界

- **[SYN]**：数据来自已验证 SDP 基础设施 + Rains/Plenio-Virmani UB 继承
- **不构成** [COROLLARY]：缺 C2 用户签字 + C1 (a)/(b)/(c)（文献重读或跨家族 PDF 直读）未启动
- **不升级到** [THM]：需 R0.2 三方验证链完整 + 文献 THM anchor（目前缺）

---

## 7. 相关产物

- 数据: `docs/research/data/qubit_E_R_PPT_SDP_all_4.csv` (Day 4 e054a1e)
- 脚本: `scripts/qubit_E_R_PPT_SDP_all_4_channels.py`
- 前置 memo: `docs/findings/qubit_E_R_PPT_hierarchy_2026-04-23.md`（AD 部分）
- 前置 memo: `docs/findings/upper_bound_report.md §11.3`（4 信道 hierarchy table）

---

## Changelog

- **v1.0** (2026-04-24): 首版。观察 E_R^PPT 在 γ > 1/2 非平凡 + K^{↔}(AD γ>1/2) OPEN 陈述 + 下一步建议。
