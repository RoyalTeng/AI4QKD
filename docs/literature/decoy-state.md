# Decoy-State QKD 精读(Level 2-3 混合)

**论文引用**(按阅读顺序):
1. Hwang, W.-Y. (2003). *Quantum key distribution with high loss: toward global secure communication.* PRL 91:057901. arXiv:quant-ph/0211153 —— 诱骗态概念原提出
2. Wang, X.-B. (2005). *Beating the photon-number-splitting attack in practical QKD.* PRL 94:230503. arXiv:quant-ph/0410075 —— 实用方案之一
3. Lo, H.-K., Ma, X., Chen, K. (2005). *Decoy state quantum key distribution.* PRL 94:230504. arXiv:quant-ph/0411004 —— 单光子 bound 理论框架
4. **Ma, X., Qi, B., Zhao, Y., Lo, H.-K. (2005). *Practical decoy state for quantum key distribution.* PRA 72:012326. arXiv:quant-ph/0503005** —— **核心参考**,1-decoy 和 2-decoy 解析公式
5. Ma, X., Razavi, M. (2012). *Alternative schemes for measurement-device-independent quantum key distribution.* PRA 86:062319 —— MDI decoy 扩展(M2 延后项)
6. George, I., Lin, J., Lütkenhaus, N. (2020). *Numerical calculations of the finite key rate for general quantum key distribution protocols.* PRR 3:013274. arXiv:2004.11865 —— 数值方法完整版(**Level 4 留待 M3 结尾升级**)
7. (辅助)Scarani 2009 RMP §IV.C

**精读日期**:2026-04-19
**精读等级**:**Level 2-3 混合**
- Level 3:Ma-Qi-Zhao-Lo 2005 §IV 的 1-decoy + 2-decoy 解析公式 + 信道模型
- Level 2:George-Lin-Lütkenhaus 2020/2021 数值方法(**本 memo 不深读;Level 4 升级留 M3 验收后**)

---

## 1. 一句话总结

Alice 用多个强度(μ、ν₁、ν₂…)的弱相干态,Eve 无法区分"哪个是信号哪个是诱骗" ⇒ Alice 能从观察到的各强度 gain $Q_μ$ 和 QBER $E_μ$ **解析反推**单光子部分的 yield $Y_1$ 和 QBER $e_1$,从而套用 GLLP 单光子密钥率公式。

---

## 2. 概念地图

```
 Alice (WCP 源)        Bob (探测器)
 ────────────          ────────────
 μ: signal            ┌─► detector click
 ν₁: decoy 1  ━━━━▶ 损耗 + 暗计数 + 对齐
 ν₂: decoy 2          └─► no-click
 0: vacuum (可选)

                     测量得:{Q_μ, Q_{ν₁}, Q_{ν₂}, Q_0}, {E_μ, E_{ν₁}, ...}

                    ┌──────────────────────────────────┐
                    │  解析:反推 Y_1^L, e_1^U        │
                    │  (1-decoy 或 2-decoy 公式)     │
                    └──────────────────────────────────┘
                                      │
                                      ▼
                    GLLP 单光子渐近率:R = q {Q_1^L [1 - H(e_1^U)] - Q_μ f H(E_μ)}
```

---

## 3. 关键结果(解析公式,**Level 3**)

### 3.1 Gain 和 QBER 的 Poisson 展开

Alice 发送强度 μ 的 WCP(相干态 |α⟩,$|α|^2 = μ$),光子数分布 $p(n;μ) = μ^n e^{-μ}/n!$。Bob 的观测:

$$Q_μ = \sum_{n=0}^\infty p(n;μ) \cdot Y_n$$
$$E_μ Q_μ = \sum_{n=0}^\infty p(n;μ) \cdot Y_n \cdot e_n$$

其中 $Y_n$ 是 n-光子态的 yield(detect 概率给定 n 光子输入),$e_n$ 是 n-光子态的 QBER。

**关键点**:Eve 的 PNS 攻击只能影响 $Y_n, e_n$(与 n 相关),但**不能**与 Alice 的 intensity μ 相关(因 Eve 看不到 μ)。Alice 用多个 μ 值 ⇒ 通过线性/凸组合解出 $Y_n, e_n$。

### 3.2 标准信道模型([Ma-Qi-Zhao-Lo 2005 §III](../../docs/literature/decoy-state.md))

- **线路损耗**:$\eta_l(L) = 10^{-αL/10}$,$α = 0.2$ dB/km @ 1550 nm
- **探测效率**:$\eta_d$(典型 0.14 - 0.5)
- **总透过率**:$\eta = \eta_d \eta_l$
- **暗计数率**:$p_{dc}$ per pulse(典型 $10^{-6}$ to $10^{-5}$)
- **对齐误差**:$e_d$(典型 0.01 - 0.03)

**n-光子 yield**([Ma 2005 Eq. 16](../../docs/literature/decoy-state.md)):
$$Y_n = 1 - (1-Y_0)(1-\eta)^n, \quad Y_0 \approx 2 p_{dc}$$

**n-光子 QBER**(Ma 2005 Eq. 17):
$$e_n = \frac{e_0 Y_0 + e_d \cdot (1 - (1-\eta)^n)}{Y_n}, \quad e_0 = 1/2$$

### 3.3 1-Decoy(weak + vacuum,Ma-Qi-Zhao-Lo 2005 Eq. 34-35)

Alice 用 signal μ + vacuum 0 两个强度。

- **$Y_0^L$** 来自真空 pulse:$Q_0 = Y_0$(直接测量)
- **$Y_1^L$** 来自 Hockey-stick lemma:
$$Y_1^{L,\text{vac}}(μ) = \frac{μ}{e^{-μ}(μ - ν)} \cdot (Q_ν e^ν - Q_μ e^μ \cdot (ν/μ)^2 - (1 - ν²/μ²) Y_0) \quad (ν=0)$$
$$Y_1^L = \frac{1}{μ^2 / (1-e^{-μ} - μ e^{-μ})} \cdot [Q_μ e^μ - Y_0]  \quad \text{(Eq. 34 }\nu_1=0\text{)}$$

实际 1-decoy weak + vacuum 的**较紧 bound**:
$$Y_1^L \geq \frac{μ}{μν - ν²}\left[Q_ν e^ν - Q_μ e^μ \frac{ν^2}{μ²} - \frac{μ^2-ν^2}{μ^2} Y_0\right]$$

- **$e_1^U$**:
$$e_1^U \leq \frac{E_ν Q_ν e^ν - e_0 Y_0}{Y_1^L \cdot ν}$$

### 3.4 2-Decoy(μ + ν₁ + ν₂,Ma 2005 Eq. 36-37)

Alice 用 signal μ + 两个非零 decoy ν₁, ν₂(ν₁ > ν₂,典型 ν₁ = 0.1μ, ν₂ = 0):

$$Y_1^L = \frac{μ}{μν_1 - μν_2 - ν_1^2 + ν_2^2}\left[Q_{ν_1}e^{ν_1} - Q_{ν_2}e^{ν_2} - \frac{ν_1^2 - ν_2^2}{μ^2}(Q_μ e^μ - Y_0)\right]$$

$$e_1^U = \frac{E_{ν_1} Q_{ν_1} e^{ν_1} - E_{ν_2} Q_{ν_2} e^{ν_2}}{(ν_1 - ν_2) Y_1^L}$$

**实际简化**:若 ν₂ = 0(vacuum decoy): $Y_0 = Q_0$(直接测),上式退化为 1-decoy(weak+vacuum)形式。

### 3.5 Infinite-Decoy 极限(Lo-Ma-Chen 2005)

理论上 Alice 用无穷多个 decoy 强度 → Y_1 和 e_1 **精确**可解:
$$Y_1 = \lim_{ν→0} \frac{Q_ν e^ν - Q_0}{ν}$$
$$e_1 Y_1 = \lim_{ν→0} \frac{E_ν Q_ν e^ν - e_0 Y_0}{ν}$$

这是 M3 数值验证的最终理论上限,任何有限 decoy 方案必须满足 $Y_1^{(\text{finite})} \leq Y_1^{\text{infinite}}$。

### 3.6 GLLP 渐近密钥率(整合 Ma 2005 Eq. 2)

$$R = q \cdot \{-Q_μ f(E_μ) H(E_μ) + Q_1^L [1 - H(e_1^U)]\}$$

其中:
- $q = 1/2$(BB84 基筛选因子)
- $f(E_μ)$:EC efficiency(典型 1.16 Cascade)
- $Q_1^L = μ e^{-μ} Y_1^L$:Alice 发的 μ-pulse 里单光子事件概率 × $Y_1^L$
- $H$:二元熵

**渐近最优 μ**:一般 μ ≈ 0.3 - 0.8(取决于 η,由微分 $dR/dμ = 0$ 解出)。

---

## 4. 数值 / 图表理解

### 4.1 Lo-Ma-Chen 2005 Fig.3(**M3 硬验收目标**)

描绘 $R$ vs 距离 $L$(km),典型参数:
- $\eta_d = 0.145$
- $p_{dc} = 8.5 \times 10^{-7}$
- $e_d = 0.033$
- $α = 0.21$ dB/km
- $f_{ec} = 1.22$

曲线特征:
- 近距离($L < 100$ km):$R \sim 10^{-3}$ bit/pulse
- 远距离($L > 150$ km):$R \sim 10^{-5}$ 到 $10^{-7}$
- **极限距离**:$R \to 0$ 在 $L \sim 180$ km(2-decoy)

### 4.2 Ma-Razavi 2012 Fig.3(M2 延后项,**M3 本阶段补**)

MDI-QKD decoy 扩展。曲线与 Lo-Ma-Chen 2005 Fig.3 类似但标度不同($R \sim \eta$ 而非 $R \sim \sqrt{\eta}$)。

---

## 5. 与本项目的 Bearing

### 5.1 对 Phase 0 M3 的直接用途

- 实现 `qkdx/analytic/decoy.py`:1-decoy + 2-decoy 的 $Y_1^L, e_1^U$ 公式
- 实现 `qkdx/analytic/channel.py`:Lo-Ma-Chen 信道模型
- 实现 `qkdx/numerics/decoy.py`:将 $\{Y_1^L, e_1^U\}$ 接入 WLC SDP(作为单光子部分的 $\Gamma_Z = e_1^U$ 约束)
- 距离扫描 notebook

### 5.2 对 PROSPECTUS §1 主问题的贡献

**间接**。decoy 是**实用工具**,把 coherent-state 源在安全模型下降级到"有效单光子源"。它**不改变** PROSPECTUS H4 硬约束(仍需 Fock 截断),也**不影响** $\sqrt{\eta}$ scaling 判断。

### 5.3 对 FINDINGS v2 的 Bearing

**无直接影响**。decoy 是 BB84 + MDI + TF-QKD 的通用工具,在 achievability 分析中提供"有效单光子"的等价。

---

## 6. Limitations / 未理解的地方

1. **George-Lin-Lütkenhaus 2020/2021 Level 4**:本 memo 只引用,未深读数值方法细节。若 M3 WLC SDP-decoy 整合与 Ma 2005 解析差异 >1e-3,需升级到 Level 4。
2. **$Y_1^L$ bound 的紧性**:1-decoy 比 2-decoy 宽松,2-decoy 比 infinite-decoy 宽松。具体宽松程度依 $(μ, ν_1, ν_2)$ 选择,M3 实施时需参数扫描。
3. **暗计数假设**:Ma 2005 模型假设 dark count per pulse 独立。现实中 after-pulse effect、dead time 等影响未纳入,归 Phase 1 Sub-Q2 器件不完美讨论。
4. **finite-key 效应**:本 memo 只讨论渐近。finite-key decoy 需 Chernoff bound + Lin-Lütkenhaus 2020(George-Lin-Lütkenhaus 2020 同族),归 Phase 1 Sub-Q2.4/2.5。

---

## 7. 下次读相关文献时需要带上的预备知识

- **本 memo §3 的解析公式**
- **Ma-Qi-Zhao-Lo 2005 §IV**(若发现 1-decoy bound 不够紧)
- **Lin-Lütkenhaus 2020(arXiv:1905.10896)**:finite-key 数值方法,Phase 1 S2.5 必读
- **Hu-Im-Lin-Lütkenhaus-Wolkowicz 2022**:facial reduction,M3 R3.2 单独精读

---

## 8. M3 实施分步(精确到模块)

| 步骤 | 模块/文件 | 参考公式 | 测试阈值 |
|------|-----------|----------|----------|
| 1 | `qkdx/analytic/channel.py` | Ma 2005 Eq. 15-17 | $Q_μ$、$E_μ$ 与 BB84 M1 数据一致 |
| 2 | `qkdx/analytic/decoy.py`(1-decoy)| Ma 2005 Eq. 34-35 | 在 toy 参数下 $Y_1^L \leq Y_1^{\text{exact}}$ |
| 3 | `qkdx/analytic/decoy.py`(2-decoy)| Ma 2005 Eq. 36-37 | 2-decoy $Y_1^L \geq$ 1-decoy $Y_1^L$ |
| 4 | `qkdx/numerics/decoy.py` | GLLP + WLC 整合 | WLC(Q_1^L, e_1^U) 匹配 GLLP 渐近 |
| 5 | distance sweep notebook | Lo-Ma-Chen 2005 Fig.3 | 视觉一致 + 阈距离 ±5 km |
