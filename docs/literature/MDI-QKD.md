# MDI-QKD 精读(Level 2-3 混合)

**论文引用**:
- Lo, H.-K., Curty, M., Qi, B. (2012). *Measurement-Device-Independent Quantum Key Distribution.* Physical Review Letters **108**, 130503. arXiv:1109.1473
- Ma, X., Razavi, M. (2012). *Alternative schemes for measurement-device-independent quantum key distribution.* Physical Review A **86**, 062319. arXiv:1204.4856
- (辅助)Scarani et al. 2009 RMP §II.C(untrusted measurement),Gottesman-Lo-Lütkenhaus-Preskill 2004(GLLP 单光子 bound)

**精读日期**:2026-04-19
**精读等级**:**Level 2-3 混合**
- Level 3:MS-EB formulation + 安全性归约(§1-§3)
- Level 2:Ma-Razavi 2012 数值细节(Fig.3 decoy-state 曲线留到 M3 精读)

**范围限定(scope)**:
- 本 memo **覆盖**:MDI-QKD 的 **信源等价(EB)** 归约、MS-EB 框架下的五元组书写、理想对称损耗下的渐近密钥率
- 本 memo **不覆盖**:decoy-state 分析(Ma-Razavi 2012 Fig.3 core 对象)⇒ **归 M3 R3.1** 精读
- 对 M2 的影响:MDI 在 M2 只做**理想情形**验收(零损耗/对称去极化,单光子源),Ma-Razavi Fig.3 的距离扫描复现**延后到 M3**

---

## 1. 一句话总结

MDI-QKD 把**测量设备移出安全模型**:Alice/Bob 只做制备,Charlie 做 Bell 测量但**完全不可信**,安全性只依赖 Alice/Bob 源的量子性 + 诱骗态分析(实际实现)或单光子假设(理论)。

---

## 2. 概念地图

```
                ┌────────────────────────────────────────────┐
                │          2-Photon Entanglement Swap       │
                │  (virtual EB picture for security proof)  │
                └────────────────────────────────────────────┘
                              ▲
 Alice 制备 ρ_A (4 BB84 态)   │         Bob 制备 ρ_B (4 BB84 态)
                ▼             │             ▼
 Alice ──── channel η_A ────▶ Charlie ◀── channel η_B ──── Bob
                              │
                              ▼ Bell 测量(untrusted),公告结果 r ∈ {Ψ+, Ψ-, ⊥}
                              ▼
              Alice/Bob 根据 r + 基匹配 → raw key
```

- **Charlie 是 adversary 的一部分**,只 public classical announcement 被使用
- **安全性核心**:Alice/Bob 送入 channel 的 qubit **没有** 经过任何 Eve-controlled measurement 之前 的泄露 —— Charlie 即使是 Eve,也只能看 Alice/Bob 送出的态,不比原始 BB84 + 长 channel 更糟

---

## 3. MS-EB 归约(Level 3)

### 3.1 Virtual EB 图像(Lo-Curty-Qi 2012 §II)

**实际协议(Prepare-and-Measure)**:Alice 扔硬币选基 + 比特 → 准备 BB84 qubit → 送 Charlie。

**虚拟 EB 等价**:Alice 持有 Bell pair $|\Phi^+\rangle_{AA'}$,Bob 持有 $|\Phi^+\rangle_{BB'}$,把 $A', B'$ 送到 Charlie;Charlie 在 $A'B'$ 上做 Bell measurement,公告结果 $r$。

等价性源于:$(M_A \otimes I) |\Phi^+\rangle_{AA'} = |x\rangle_A \otimes |x\rangle_{A'}$(若 Alice 在 $A$ 上 Z 基测 = 获得 $x$)。这就是 remote state preparation。

### 3.2 Charlie 成功 Bell 测量的效果

$|\Phi^+\rangle_{AA'} \otimes |\Phi^+\rangle_{BB'}$ 分解后包含 $|\Psi^+\rangle_{A'B'} \otimes \dots$ 等项。Charlie 在 $A'B'$ 上测得 $|\Psi^+\rangle$ ⇒ 塌缩后 $(AB)$ 的态是某个纠缠态,具体依赖 Bell 选择。

具体:对于 Charlie 测到 $|\Psi^-\rangle$ 的情形($\Psi^-$ 是最易产生的 Bell 态,因为 HOM 干涉),塌缩后的 $(AB)$ 态是 $|\Psi^-\rangle_{AB}$(单重态) —— Alice 与 Bob 在同基下 **反关联**(类似 Ekert91)。因此**双方一方需取非运算**后得到 correlated raw key。

### 3.3 MS-EB 五元组 $\Pi_{\text{MDI}} = (\mathcal{P}, \mathcal{E}, \mathcal{A}, \mathcal{T}, \mathcal{K})$

#### 3.3.1 $\mathcal{P}$:两个源方(Alice + Bob)

MDI-QKD 是**本项目第一个多源方协议**(与 BB84/六态的单源不同)。

| 源 | key_register_dim | signal_register_dim | 源态 |
|----|------------------|----------------------|------|
| Alice | 4(Z/X × 2)| 2 | $\|\psi\rangle_{AA'} = $ BB84 EB(见 [bb84.py](../../qkdx/protocols/bb84.py) §bb84_alice_source)|
| Bob | 4 | 2 | 同 Alice(镜像) |

#### 3.3.2 $\mathcal{E}$:信道 + Charlie

$\mathcal{E}: A' \otimes B' \to \text{classical outcome } r$,由三步合成:

1. **Alice→Charlie 信道**:$\eta_A$ 透过率(M2 理想情形:$\eta_A = 1$)
2. **Bob→Charlie 信道**:$\eta_B$ 透过率
3. **Charlie Bell 测量**:POVM $\{P_{\Psi^-}, P_{\Psi^+}, P_{\perp}\}$

**简化记号**:若 $\eta_A = \eta_B = 1$(无损),$\mathcal{E}$ 是 $(A' \otimes B') \to (\text{classical } r)$ 的**测量-公告信道**。在 MS-EB 框架里,classical 输出可以 embed 到 d=3 或 d=2 的量子寄存器(只保留 $r \in \{\Psi^-, \Psi^+\}$,舍弃 $\perp$)。

#### 3.3.3 $\mathcal{A}$:公告与筛选

双源方:$\text{outcomes} = (\theta_A, \theta_B)$,基 $\in \{Z, X\}$(M2 理想 MDI 不含 Y 基)。

筛选判据:
- $\theta_A = \theta_B$(基匹配)AND
- Charlie 公告 $r \neq \perp$(Bell 测量成功)

$p_{\text{sift}}^{\text{ideal}} = \underbrace{1/2}_{\text{basis match}} \times \underbrace{1/2}_{\text{Charlie 成功率(理想 linear-optic)}} = 1/4$

#### 3.3.4 $\mathcal{T}$:接受判据

观测集合:
$$\text{observation\_keys} = (\text{qber\_Z}, \text{qber\_X}, \text{p\_sift})$$

注意:MDI **不使用 Y 基**(Lo-Curty-Qi 原论文),所以 observable 数量与 BB84 一致。但 $\Gamma$ 的构造涉及 Alice-Bob 双方 + Charlie 公告,不再是单方 MS-EB 的 4×4 矩阵 —— 详见 §3.4。

#### 3.3.5 $\mathcal{K}$:密钥映射

- Alice 的 $x \in \{0,1\}$ 作为 raw key
- Bob 接收 Charlie 公告后,根据 $r$ 决定是否 flip 自己的比特(如 $r = \Psi^-$ 需 flip;$r = \Psi^+$ 不 flip)
- 最终 Alice-Bob key 比特匹配

### 3.4 理想 MDI 的渐近密钥率公式(Level 3 证明)

对**对称理想 MDI**(无损,对称去极化 channel leg,单光子源):

设 $e_Z, e_X$ 分别为 Alice-Bob raw key bit 在 Z 基、X 基下的失配率。由 GLLP 单光子 bound:

$$R_{\text{MDI}}^{\text{ideal}} = p_{\text{sift}} \cdot [1 - H(e_Z) - H(e_X)]$$

其中 $p_{\text{sift}} = 1/4$(M2 理想情形),$H(\cdot) = h(\cdot) = -x \log_2 x - (1-x)\log_2(1-x)$ 是二元熵。

**对称情形** $e_Z = e_X = e$:
$$R_{\text{MDI}}^{\text{symmetric}} = \frac{1}{4} \cdot (1 - 2h(e))$$

与 BB84 比较:$R_{\text{BB84}} = \frac{1}{2}(1 - 2h(e))$ ⇒ **MDI = BB84 / 2**(理想情形,对称 QBER,无损)。

**为什么是 /2 而不是不一致?** 因为 MDI 的 Bell 测量成功率 1/2 × 基匹配率 1/2 = 1/4,比 BB84 的 1/2 少一个因子 2。

---

## 4. 数值 / 图表理解

### 4.1 理想情形一致性检查

在 $\eta_A = \eta_B = 1$,Z-X 对称去极化,$e = 0.05$:
- $R_{\text{MDI}}^{\text{ideal}}(0.05) = 0.25 \cdot (1 - 2 \cdot 0.28640) = 0.25 \cdot 0.42720 = 0.10680$ bit/signal
- $R_{\text{BB84}}(0.05) = 0.21360$ bit/signal(M1 实测值)
- 比例 $R_{\text{MDI}} / R_{\text{BB84}} = 0.5$ ✓

### 4.2 Ma-Razavi 2012 Fig.3(距离扫描,decoy-state,**M2 不核实**)

Fig.3 描绘 $R$ vs 距离(km),含 decoy-state 分析 + 探测效率 + 暗计数 + 对齐误差。**本 M2 不复现**;延后到 M3 `notebooks/m3_decoy_distance_sweep.ipynb`,配合 decoy-state 实现。

---

## 5. 与本项目的 Bearing

### 5.1 对 Phase 0 M2 的直接用途

MDI-QKD 是本项目**首个**:
- **多源方**协议 —— 验证 `MSEBProtocol.sources` tuple 长度 > 1 的支持
- **含不可信中间节点**协议 —— 验证 $\mathcal{E}$ 不止是两方 channel,还含 Charlie 的 untrusted measurement

### 5.2 对 PROSPECTUS §3.1 主问题的贡献(**关键!**)

MDI-QKD 是 PROSPECTUS v3.1 §3.1 **H3(刻画式设备信任)下 untrusted measurement relay** 拓扑的**最早、最清晰实例**。六态 + BB84 只是"两方点对点"拓扑,不涉及 PROSPECTUS 主问题的 Charlie relay 元素。

**这意味着**:MDI-QKD 的代码对象(`build_mdi_protocol` + WLC SDP 评估)是 Sub-Q3(上界工作,Phase 2)直接使用的基础。Sub-Q3 上界 SDP 需要在 MDI 的拓扑上做,而不是 BB84。

### 5.3 对 FINDINGS v2 的 Bearing

FINDINGS v2(interim verdict)的 **[CONJ] 级上界 $R \leq 1.44\sqrt{\eta_{AB}}$** 是针对 untrusted measurement relay 拓扑。MDI-QKD 的 achievability 部分 **不涉及** $\sqrt{\eta}$ scaling(MDI 标度 $\eta = \eta_A \eta_B$,不是 $\sqrt{\eta}$)—— TF-QKD / PM-QKD 才是 $\sqrt{\eta}$ 的 achievability 来源(M4B 工作)。

---

## 6. Limitations / 未理解的地方

1. **MDI 在有限 dim 下的信源描述**:MS-EB 书写假设 Alice/Bob 各持 BB84 EB Bell pair,但真实实验使用 coherent state + decoy。coherent state 在 MS-EB 下需 Fock truncation,留 M3 处理。
2. **Charlie 的 POVM 的 MS-EB 内嵌**:在 MS-EB 的 5 元组里,$\mathcal{E}$ 严格说是 CPTP map。把 Charlie 的 Bell 测量 + 公告 embed 成一个 quantum-classical channel 需要显式 POVM → Kraus。M2 实现简化为:Charlie 直接"塌缩"成 Bell state,之后做 sifting,这**不完全忠实**于原始协议(但与 virtual EB picture 等价)。
3. **非对称信道 $\eta_A \neq \eta_B$**:M2 只做对称情形。非对称 MDI 是 Phase 1 Sub-Q2 family sheet 话题。

---

## 7. 下次读相关文献时需要带上的预备知识

- **本 memo §3.1-§3.3 的 virtual EB 归约**
- **Lo-Preskill 2007**:"Security of QKD using weak coherent states"(coherent state 在 MS-EB 下的处理,为 M3 coherent state MDI 做准备)
- **Ma-Qi-Zhao-Lo 2005**:decoy-state 解析公式,M3 R3.1 必读
- **Coles-Metodiev-Lütkenhaus 2016 §V.B**:WLC SDP 在 MDI-QKD 上的应用示例(已在 [CML-2016.md](CML-2016.md) Level 3 覆盖)

---

## 8. 下一步(M2 收尾)

1. 实现 `qkdx/analytic/gllp.py`:通用 GLLP/single-photon 渐近密钥率公式(供 MDI 和未来诱骗 MDI 共用)
2. 实现 `qkdx/protocols/mdi.py`:理想 MDI MS-EB 协议
3. WLC SDP 验证:`R_MDI^{WLC}(e=0.05)` vs $0.25 \cdot (1 - 2h(e))$,fallback 阈值 `abs=1e-3`
4. M2 收尾 notebook + memo
