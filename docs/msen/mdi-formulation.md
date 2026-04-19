# MDI-QKD 在 MS-EB 框架下的书写

**版本**:v0.1(2026-04-19,M2 R2.3 produce)
**关联研究动作**:R2.1(Level 2-3 精读)+ R2.3(实现)
**对应协议代码**:[qkdx/protocols/mdi.py](../../qkdx/protocols/mdi.py)
**Level 2-3 精读 memo**:[docs/literature/MDI-QKD.md](../literature/MDI-QKD.md)

---

## 0. 范围限定

本 MS-EB 书写**只覆盖 MDI-QKD 的理想情形**:
- $\eta_A = \eta_B = 1$(无损)
- 单光子源(无 decoy)
- 对称去极化等效信道 ⇒ Alice-Bob effective $Q_Z = Q_X = e$
- 忽略暗计数和对齐误差

**不覆盖**:
- Decoy-state 分析(归 M3 R3.1)
- Coherent-state 源 + Fock 截断(归 M3 R3.3)
- 非对称 $\eta_A \neq \eta_B$(归 Phase 1 Sub-Q2 family sheet)
- 器件不完美(暗计数、探测效率、对齐)(归 Phase 1 S2.3)

---

## 1. MS-EB 五元组 $\Pi_{\text{MDI}} = (\mathcal{P}, \mathcal{E}, \mathcal{A}, \mathcal{T}, \mathcal{K})$

### 1.1 $\mathcal{P}$:双源方

MDI-QKD 是本项目**首个双源方**协议,`sources` tuple 长度 = 2。

| 源方 | key_register_dim | signal_register_dim | source_state 维度 |
|------|-------------------|---------------------|------|
| Alice | 4(Z/X × 2) | 2 | 8 × 8 |
| Bob | 4 | 2 | 8 × 8 |

两源的源态**完全相同**(BB84-style EB),详见 [bb84.py](../../qkdx/protocols/bb84.py)`::bb84_alice_source`。这对应 Lo-Curty-Qi 2012 §II 的 virtual EB picture。

### 1.2 $\mathcal{E}$:Charlie 信道

$\mathcal{E}: A' \otimes B' \to \text{classical outcome}$,数学上是:
$$\mathcal{E} = \mathcal{E}_{\text{Charlie-BSM}} \circ (\mathcal{E}_{A'} \otimes \mathcal{E}_{B'})$$

其中 $\mathcal{E}_{A'}, \mathcal{E}_{B'}$ 是 Alice→Charlie、Bob→Charlie 的量子信道(M2 理想:identity),$\mathcal{E}_{\text{Charlie-BSM}}$ 是 Charlie 的 Bell 测量 + 公告。

**M2 实现简化**:使用 `KrausMap.identity(4)` 作为 network channel,**Charlie 的 BSM + 条件化**通过 `_conditional_alice_bob` override 注入。这对 WLC SDP 数值等价(SDP 只用 $d_\rho$ + observable,不直接用 network channel)。

严格 MS-EB 下 Charlie 的 BSM 需表达为 POVM → Kraus 嵌入,留 M3 精化。

### 1.3 $\mathcal{A}$:公告与筛选

- Alice 公告基 $\theta_A \in \{Z, X\}$
- Bob 公告基 $\theta_B \in \{Z, X\}$
- Charlie 公告 Bell 测量结果 $r \in \{\Psi^+, \Psi^-, \text{fail}\}$
- **sift_keep**:`θ_A == θ_B` AND `r ≠ fail`

### 1.4 $\mathcal{T}$:接受判据

$$\text{observation\_keys} = (\text{qber\_Z}, \text{qber\_X}, \text{p\_sift})$$

观测 $\Gamma_Z, \Gamma_X$ 与 BB84 **完全相同**(4×4 Hermitian on $A_{\text{key}} \otimes B_{\text{effective-bit}}$);差异只在 $p_{\text{sift}}$。

### 1.5 $\mathcal{K}$:密钥映射

- 密钥持有方:**Alice**(`key_party = "Alice"`)
- 密钥映射:$\text{bitmap} = \{0 \mapsto 0, 1 \mapsto 1, 2 \mapsto 0, 3 \mapsto 1\}$(与 BB84 一致)
- Bob 根据 Charlie 公告 $r$ 决定是否翻转自己的比特,使 raw key 与 Alice 匹配 —— 此翻转**不显式建模**,通过 virtual EB picture 吸收

---

## 2. $p_{\text{sift}}$ 的推导

$$p_{\text{sift}}^{\text{ideal}} = \underbrace{P(\theta_A = \theta_B)}_{1/2} \times \underbrace{P(r \neq \text{fail} \mid \text{same basis})}_{1/2}$$

- **基匹配 1/2**:Alice、Bob 独立均匀选 Z/X
- **Charlie 成功率 1/2**:理想 linear-optic Bell-state measurement 只能区分 $|\Psi^+\rangle, |\Psi^-\rangle$(2/4),舍弃 $|\Phi^\pm\rangle$(详见 Calsamiglia-Lütkenhaus 2001)

⇒ $p_{\text{sift}} = 0.25$。

**推广**:引入损耗 $\eta_A, \eta_B < 1$ 后 $p_{\text{sift}} \sim \eta_A \eta_B / 2$,即 MDI-QKD 的标度 $\eta$(不是 $\sqrt{\eta}$)。这是 PROSPECTUS §3.1 Sub-Q4 gap 分析的关键 —— MDI ∈ PLOB 可达性内。

---

## 3. WLC SDP 表达

### 3.1 SDP 变量

- $d_\rho = \dim(\text{conditional\_alice\_bob}) = 4$(**与 BB84 相同**)
- $\mathcal{G}$:identity on 4-dim,`dim_key=2, dim_side=2`
- $\mathcal{Z}$:pinching key register(同 BB84)

### 3.2 约束集合 $\mathcal{S}_{\text{MDI}}$

$$\mathcal{S}_{\text{MDI}} = \{\rho \succeq 0 : \text{Tr}(\rho) = 1, \text{Tr}(\Gamma_Z \rho) = e, \text{Tr}(\Gamma_X \rho) = e\}$$

**$\mathcal{S}_{\text{MDI}} = \mathcal{S}_{\text{BB84}}$**(同一个 4×4 约束集合) ⇒ MIN 完全相等。

**结论**:$H^{\text{MDI}}(A|E) = H^{\text{BB84}}(A|E)$,MDI 和 BB84 的 per-sift 渐近密钥率**完全相等**。

### 3.3 密钥率关系

$$R_{\text{MDI}}^{\text{ideal}} = p_{\text{sift}}^{\text{MDI}} \cdot [H(A|E) - f_{\text{ec}} \cdot h(e)] = 0.25 \cdot \text{(BB84 per-sift)}$$
$$R_{\text{BB84}} = 0.5 \cdot \text{(BB84 per-sift)}$$
$$\boxed{R_{\text{MDI}}^{\text{ideal}} = R_{\text{BB84}} / 2}$$

### 3.4 数值验证

[tests/test_protocols/test_mdi.py](../../tests/test_protocols/test_mdi.py)::`test_wlc_mdi_is_bb84_halved` 数值验证 $R_{\text{MDI}} = R_{\text{BB84}} / 2$ 在 QBER=0.05 下。

---

## 4. Additivity 验证

`qkdx/numerics/wlc.py` **零修改**(与六态实现一致)。新增仅限:

- [qkdx/analytic/gllp.py](../../qkdx/analytic/gllp.py)
- [qkdx/protocols/mdi.py](../../qkdx/protocols/mdi.py)
- 测试:[tests/test_analytic/test_gllp.py](../../tests/test_analytic/test_gllp.py) + [tests/test_protocols/test_mdi.py](../../tests/test_protocols/test_mdi.py)

---

## 5. 对 PROSPECTUS §3.1 主问题的 Bearing

MDI-QKD 是 PROSPECTUS v3.1 §3.1 **untrusted measurement relay** 拓扑的**最早、最清晰实例**。其 MS-EB 书写 **不会** 直接解决 PROSPECTUS §1 主问题,但:

1. **为 Sub-Q3(Phase 2)上界工作奠定基础**:Pirandola 2019 Eq. (11)/(17) 在 untrusted-relay 拓扑下的继承 lemma,需要在 MDI 的 MS-EB 书写上验证(而不是 BB84 的点对点)
2. **为 Sub-Q2 family sheet(Phase 1)提供参数化锚点**:mdi_family.md 的起点
3. **不提供 $\sqrt{\eta}$ achievability**:MDI 标度 $\eta = \eta_A \eta_B$,$\sqrt{\eta}$ 可达性归 TF-QKD(M4B)

---

## 6. Limitations

见 [MDI-QKD.md](../literature/MDI-QKD.md) §6 + 本文 §0。核心:

- **理想 channel 假设**:真实 MDI 实验 coherent state + decoy,当前实现无法复现 Ma-Razavi 2012 Fig.3
- **Charlie POVM 未显式建模**:严格 MS-EB 需要把 Charlie BSM 写成 quantum-classical channel Kraus,当前绕过
- **无 finite-key**:渐近 i.i.d. + collective attack,finite-key 归 Phase 1 GEAT

---

## 7. 下一步

1. ✅ M2 MDI 理想情形 WLC SDP 验收(本文档覆盖)
2. ⏳ M2 收尾 notebook + memo(下一 commit)
3. ⏳ M3 decoy-state 扩展:R_MDI(distance) 与 Ma-Razavi 2012 Fig.3 对比
4. ⏳ M3 Charlie POVM 严格 Kraus 嵌入(精化 `mdi_charlie_network`)
