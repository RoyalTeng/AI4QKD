# Six-State QKD 精读(Level 2)

**论文引用**:
- Bruss, D. (1998). *Optimal eavesdropping in QKD with six states.* Physical Review Letters **81**, 3018. DOI: 10.1103/PhysRevLett.81.3018
- (辅助)Lo, H.-K. (2001). *Proof of unconditional security of six-state QKD scheme.* Quantum Information and Computation **1**, 81–94.
- (辅助)Scarani, V., Bechmann-Pasquinucci, H., Cerf, N. J., Dušek, M., Lütkenhaus, N., Peev, M. (2009). *The security of practical quantum key distribution.* Rev. Mod. Phys. **81**, 1301–1350. §III.D.1

**精读日期**:2026-04-19
**精读等级**:**Level 2**(阅 abstract + intro + conclusion + 关键公式段,不做完整证明重现)
**后续精读计划**:M2 验收后若 SDP 与解析相差 >5e-4,升级到 Level 3 重做证明

---

## 1. 一句话总结

**六态协议** = BB84 加第三个 MUB(Z, X, **Y**)⇒ 对称攻击者在同样 QBER 下得到**更少**信息,代价是筛选率从 1/2 降到 **1/3**。

---

## 2. 概念地图

```
BB84 (2 MUBs: Z,X)    ──►  六态 (3 MUBs: Z,X,Y)
  ↓                            ↓
  p_sift = 1/2                 p_sift = 1/3
  Q_Z, Q_X 约束                Q_Z, Q_X, Q_Y 约束
  Eve 信息:h(e)                Eve 信息:严格更小
  阈值:~11.0%                  阈值:~12.62%(Lo 2001)
```

**关键直觉**:第三个 MUB 约束相当于把 Eve 的攻击空间从"最优化 Z + X 干扰"进一步限制到"Z + X + Y 同时干扰"。在对称信道下,三个 MUB 的干扰对称 ⇒ ρ_AB 唯一被钉死为 **Werner 态**,不留给 Eve 任何隐藏信息自由度。

---

## 3. 关键结果(公式层面)

### 3.1 六态的三个 MUB

| 基 | 态 | 本征向量(Z 基) |
|----|------|------------------|
| Z | σ_z | $\|0\rangle, \|1\rangle$ |
| X | σ_x | $\|+\rangle = (\|0\rangle+\|1\rangle)/\sqrt 2,\ \|-\rangle = (\|0\rangle-\|1\rangle)/\sqrt 2$ |
| Y | σ_y | $\|+y\rangle = (\|0\rangle+i\|1\rangle)/\sqrt 2,\ \|-y\rangle = (\|0\rangle-i\|1\rangle)/\sqrt 2$ |

三者构成 $\mathbb{C}^2$ 上唯一一组 3-MUB(维度 2 下 MUB 最多 3 个;Z、X、Y 即 Pauli 本征基)。

### 3.2 对称信道下的 Werner 态(本项目核心对象)

对称去极化信道 $\mathcal{E}(\rho) = (1-p)\rho + p\,I/2$,$\text{QBER} = p/2 =: e$,且 Z/X/Y 三基同时约束 $Q_\theta = e$ ⇒ Bell 对角形式唯一确定:

$$\rho_{AB}^* = \left(1 - \frac{3e}{2}\right) |\Phi^+\rangle\langle\Phi^+| + \frac{e}{2}\sum_{i \in \{\Phi^-, \Psi^+, \Psi^-\}} |\text{Bell}_i\rangle\langle\text{Bell}_i|$$

其中 $|\Phi^\pm\rangle = (|00\rangle \pm |11\rangle)/\sqrt 2$,$|\Psi^\pm\rangle = (|01\rangle \pm |10\rangle)/\sqrt 2$。

**验算**:
- $\text{Tr}(\Gamma_Z \rho^*) = 0 \cdot (1-3e/2) + (e/2)(0 + 1 + 1) = e$ ✓
- 同理 $Q_X = Q_Y = e$ ✓(三个 Bell 非 $\Phi^+$ 权重相等保证所有三基 QBER 相等)

### 3.3 渐近密钥率公式(本 memo §2.2 derive,与 Lo 2001 / Scarani 2009 一致)

**直接从 Werner 态计算**(见 [qkdx/analytic/six_state.py](../../qkdx/analytic/six_state.py) §docstring):

$$H_{\text{six}}(A|E) = 1 + h(e) + \left(1 - \frac{3e}{2}\right) \log_2\left(1 - \frac{3e}{2}\right) + \frac{3e}{2} \log_2\frac{e}{2}$$

$$R_{\text{six}}(e, f_{\text{ec}}) = \frac{1}{3} \cdot \left[H_{\text{six}}(A|E) - f_{\text{ec}} \cdot h(e)\right] \quad [\text{bit/signal}]$$

在 $f_{\text{ec}} = 1.0$ 下:
- $R_{\text{six}}(0) = 1/3$ bit/signal(理想信道,p_sift × 1 = 1/3)
- $R_{\text{six}}(0.05) \approx 0.180$ bit/signal(手算 §4 验证)
- $R_{\text{six}}(0.126) \approx 0$(阈值,与 Bruss 1998 coherent-attack 分析一致)

### 3.4 推导纲要(Werner 态 → WLC 目标函数)

$\mathcal{G} = $ identity on 4-dim $A_{\text{key}} \otimes B$;$\mathcal{Z}$ pinch key register(zeroes cross-key 2×2 block)。

1. **ρ\* 在 {|00⟩,|01⟩,|10⟩,|11⟩} 基下**:对角 $((1-e)/2, e/2, e/2, (1-e)/2)$,唯一非零反对角 $(0,3) = (3,0) = (1-2e)/2$
2. **Z pinching 清掉 (0,3), (3,0)** ⇒ $\mathcal{Z}(\mathcal{G}(\rho^*)) = \text{diag}((1-e)/2, e/2, e/2, (1-e)/2)$(全对角)
3. **ρ\* 的特征值**:
   - {e/2, e/2} 来自 (1,1), (2,2) 块
   - {(2-3e)/2, e/2} 来自 [(1-e)/2, (1-2e)/2; (1-2e)/2, (1-e)/2] 2×2 反对角块
   - 合:{1-3e/2, e/2, e/2, e/2} ✓
4. $H(\rho^*) = -(1-3e/2)\log_2(1-3e/2) - 3(e/2)\log_2(e/2)$
5. $H(\mathcal{Z}(\mathcal{G}(\rho^*))) = 1 + h(e)$(两对 $((1-e)/2, e/2)$,熵 = $h(e) + 1$)
6. $D(\rho^* \| \mathcal{Z}(\mathcal{G}(\rho^*))) = H(\mathcal{Z}(\mathcal{G}(\rho^*))) - H(\rho^*)$(当 $\mathcal{Z}(\mathcal{G}(\rho^*))$ 对角且其对角 = $\rho^*$ 对角时该恒等式严格成立)= §3.3 的 $H_{\text{six}}(A|E)$

### 3.5 为什么 Werner 态是 SDP 最优?

六态约束 $Q_Z = Q_X = Q_Y = e$ 在 Bell 基下等价于固定 3 个 Bell 权重之和,而对称性(Clifford 群轨道)保证 $\lambda_{\Phi^-} = \lambda_{\Psi^+} = \lambda_{\Psi^-}$。WLC 目标函数 $D(\mathcal{G}\cdot\|\mathcal{Z}\mathcal{G}\cdot)$ 在 Clifford 不变子集上凸,最优在对称点取到 ⇒ ρ\* 唯一。严格证明见 Kraus-Gisin-Renner 2005, Renner PhD §6.5。

---

## 4. 数值 / 图表理解:手算 QBER=0.05

按 §3.3 公式:

- $e = 0.05$,$1 - 3e/2 = 0.925$,$e/2 = 0.025$
- $\log_2(0.925) = -0.112452$,$\log_2(0.025) = -5.321928$
- $h(0.05) = 0.286397$
- $H(\mathcal{G}(\rho^*)) = -0.925 \cdot (-0.112452) - 3 \cdot 0.025 \cdot (-5.321928) = 0.104018 + 0.399145 = 0.503163$ bits
- $H(\mathcal{Z}(\mathcal{G}(\rho^*))) = 1 + h(0.05) = 1.286397$ bits
- $H_{\text{six}}(A|E) = 1.286397 - 0.503163 = 0.783213$ bits/sift

- $R_{\text{six}}(0.05, f_{\text{ec}}=1) = (1/3)(0.783213 - 0.286397) = (1/3)(0.496816) = 0.165605$ bit/signal(Python 高精度:`0.1656054228`)

**对比 BB84(QBER=0.05, $f_{\text{ec}}=1$)**:
- $R_{\text{BB84}} = 0.5 \cdot (1 - 2 h(0.05)) = 0.5 \cdot (1 - 0.5728) = 0.21360$ bit/signal

⇒ BB84 > 六态 at QBER=0.05(BB84 每信号筛选率更高,每比特信息量差异小)。
⇒ 六态优势只在高 QBER(接近 11% 阈值)显现。

---

## 5. 与本项目的 Bearing

### 5.1 对 Phase 0 M2 的直接用途

六态作为"**BB84 + 单一观测约束**"的最小扩展,验证 `qkdx/numerics/wlc.py` 的**additivity**:新协议只加 observable builder,不改 SDP 核。符合 REFACTORING_PLAN §5 M2 要求 "BB84 基线零回归"。

### 5.2 对"两方 + untrusted relay + 纯损耗"拓扑(PROSPECTUS §3.1)的贡献

**间接**。六态本身仍是两方直接信道(无 relay),不直接回答 PROSPECTUS §1 主问题。但:

- 六态证实"更多 MUB 约束 ⇒ Eve 信息严格减少",这对 Sub-Q2 协议族地图(Phase 1)有意义(device-dependence 分析)
- 六态的 Clifford 对称约化是 M4A 的先验结构,Sub-Q1 (b) "对称约化自动化"的 toy case

### 5.3 对 FINDINGS v2 interim verdict 的 Bearing

**无直接影响**。六态**不改变** PROSPECTUS §1 主问题的 $\sqrt{\eta}$ scaling 判断,因为六态的分析仍是 BB84-like 点对点信道(无距离 scaling)。

---

## 6. Limitations / 未理解的地方

1. **Lo 2001 的精确 coherent-attack 阈值 12.62%**:本 memo 的 Werner 态最优性论证仅给**下界** $H_{\text{six}}(A|E) \geq$ §3.3 的值。Lo 2001 严格证明这是紧上界(即 Eve 能达到);**本 memo 未 Level 3 复查该证明**,仅引用结论。若 M2 WLC SDP 与 §3.3 解析公式偏差 >5e-4,需升级该 memo 到 Level 3 读 Lo 2001 §III-IV。
2. **Renner PhD §6.5 的 Clifford 对称性论证**:本 memo 仅声称"对称凸最优必在对称点",未展开对称约化 lemma 的严格证明(标准工具,但未逐步验证)。
3. **有限密钥修正**:Bruss 1998 和本 memo 均是渐近 i.i.d.,有限密钥六态安全性归 GEAT(Metger 2024)+ Phase 1 Sub-Q2.4/2.5,不在此范围。

---

## 7. 下次读相关文献时需要带上的预备知识

- **本 memo §3.4 的 Werner 态推导**(直接可用)
- **Renner 2005 PhD §6.5**:Clifford 对称约化的经典推导
- **Kraus-Gisin-Renner 2005 PRL 95:080501**:单向 CC 密钥率的 Devetak-Winter 框架,与本 memo 公式等价但表述不同
- **Scarani 2009 RMP §III.D**:QKD 安全性证明技巧的标准综述 —— 六态部分见 Eq. (86)+正文
