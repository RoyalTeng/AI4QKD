# 六态 QKD 在 MS-EB 框架下的书写

**版本**:v0.1(2026-04-19,M2 R2.3 produce)
**关联研究动作**:R2.2(Level 2 精读)+ R2.3(实现)
**对应协议代码**:[qkdx/protocols/sixstate.py](../../qkdx/protocols/sixstate.py)
**Level 2 精读 memo**:[docs/literature/six-state.md](../literature/six-state.md)

---

## 0. 动机

R2.3 要求:扩展 [qkdx/protocols/bb84.py](../../qkdx/protocols/bb84.py) 实现 **最小增量**的新协议,验证 WLC SDP (`qkdx/numerics/wlc.py`) 的 **additivity** —— 新协议只加 observable builder,不改 SDP 核,BB84 基线零回归。

六态是理想的验证协议,因为:

1. 与 BB84 共享 **同一个** d=4 SDP 空间($A_{\text{key}} \otimes B$)
2. 与 BB84 共享 **同一个** 去极化信道(对称模型)
3. 只增加一个观测约束 $\Gamma_Y$ 到 SDP

---

## 1. MS-EB 五元组 $\Pi_{\text{six}} = (\mathcal{P}, \mathcal{E}, \mathcal{A}, \mathcal{T}, \mathcal{K})$

### 1.1 $\mathcal{P}$:源方(Alice)

- **寄存器维度**:
  - Key 寄存器 $A$:$\dim A = 6$(3 基 × 2 值)
  - Signal 寄存器 $A'$:$\dim A' = 2$
- **源态**:
$$|\psi\rangle_{AA'} = \frac{1}{\sqrt 6}\sum_{\theta \in \{Z, X, Y\}}\sum_{x \in \{0,1\}} |\theta, x\rangle_A \otimes U_\theta |x\rangle_{A'}$$
- **基索引约定**:
  | $A$ 寄存器标签 | 索引 | 含义 |
  |---------------|------|------|
  | $\|Z,0\rangle$ | 0 | 选 Z 基,比特 0 |
  | $\|Z,1\rangle$ | 1 | 选 Z 基,比特 1 |
  | $\|X,0\rangle$ | 2 | 选 X 基,比特 0 |
  | $\|X,1\rangle$ | 3 | 选 X 基,比特 1 |
  | $\|Y,0\rangle$ | 4 | 选 Y 基,比特 0 |
  | $\|Y,1\rangle$ | 5 | 选 Y 基,比特 1 |
- **基旋转矩阵**:
  - $U_Z = I$
  - $U_X = H$(Hadamard)
  - $U_Y = \frac{1}{\sqrt 2}\begin{pmatrix} 1 & 1 \\ i & -i \end{pmatrix}$,满足 $U_Y\|0\rangle = \|{+y}\rangle$,$U_Y\|1\rangle = \|{-y}\rangle$

### 1.2 $\mathcal{E}$:量子信道

**与 BB84 完全相同**的对称去极化信道(`bb84_channel(qber)` 直接复用):
$$\mathcal{E}(\rho) = (1-p)\rho + p\cdot \frac{I_2}{2}, \quad p = 4e/3$$
Kraus 算子:$K_0 = \sqrt{1 - 3p/4}\,I$,$K_1 = \sqrt{p/4}\,\sigma_x$,$K_2 = \sqrt{p/4}\,\sigma_y$,$K_3 = \sqrt{p/4}\,\sigma_z$。

此信道对三基对称 ⇒ $Q_Z = Q_X = Q_Y = p/2 = e$。

### 1.3 $\mathcal{A}$:公告与筛选

- **公告**:$\theta_A, \theta_B \in \{Z, X, Y\}$
- **筛选判据**:`sift_keep = (θ_A == θ_B)`
- **筛选概率**:$p_{\text{sift}} = P(\theta_A = \theta_B) = 3 \cdot (1/3)(1/3) = 1/3$(均匀独立选基)

### 1.4 $\mathcal{T}$:接受判据

观测集合:**四**个 observation keys(BB84 加一):
$$\text{observation\_keys} = (\text{qber\_Z}, \text{qber\_X}, \text{qber\_Y}, \text{p\_sift})$$

### 1.5 $\mathcal{K}$:密钥映射

Alice 从 $A$ 寄存器对应比特值:`bitmap = {0:0, 1:1, 2:0, 3:1, 4:0, 5:1}`(每基的"0"标签 → 密钥 0,"1"标签 → 密钥 1)。

---

## 2. Observable $\Gamma_Y$ 的推导(关键技术点)

### 2.1 BB84 的 $\Gamma_Z$ 与 $\Gamma_X$

BB84 [CML 2016 Eq. 25-26]:
$$\Gamma_Z = |01\rangle\langle 01| + |10\rangle\langle 10| = \text{diag}(0,1,1,0)$$
$$\Gamma_X = (H \otimes H)\Gamma_Z(H \otimes H)^\dagger$$

注意 $H$ 是**实矩阵** ⇒ $H^* = H$ ⇒ Bob 与 Alice 使用相同旋转时无复共轭问题。

### 2.2 $\Gamma_Y$ 为什么需要 Bob 侧复共轭

**关键物理事实**:Bell 态 $|\Phi^+\rangle$ 在 Y 基下表现为 **反关联**:

$$|\Phi^+\rangle = \frac{1}{\sqrt 2}(|00\rangle + |11\rangle) = \frac{1}{\sqrt 2}(|+y, -y\rangle + |-y, +y\rangle)$$

验证:$|0\rangle = (|+y\rangle + |-y\rangle)/\sqrt 2$,$|1\rangle = -i(|+y\rangle - |-y\rangle)/\sqrt 2$,代入展开可得上式。

**结果**:若 Alice 和 Bob 同时在 $|\Phi^+\rangle$ 上测量 Y 基,他们的 Y 值**永远相反**,即 $Q_Y(|\Phi^+\rangle) = 1$,不是 0。

### 2.3 正确的 $\Gamma_Y$ 构造

为使 $\text{Tr}(\Gamma_Y \cdot \rho_{\text{Werner}}) = e$(标准 QBER 约定),Bob 侧的基旋转需取复共轭:

$$\boxed{\Gamma_Y = (U_Y \otimes U_Y^*) \Gamma_Z (U_Y \otimes U_Y^*)^\dagger}$$

其中 $U_Y^* = \frac{1}{\sqrt 2}\begin{pmatrix} 1 & 1 \\ -i & i \end{pmatrix}$。

**物理解释**:Bob 的 Y 测量结果需要做一次比特翻转后才能和 Alice 对齐。$(U_Y \otimes U_Y^*)$ 已吸收此翻转,使得 $\Gamma_Y$ 对应 "Alice Y 值 ≠ Bob Y 值(post-alignment)"。Z、X 基无此问题,因为 $U_Z, U_X$ 是实矩阵。

### 2.4 数值验证

对 Werner 态 $\rho_W = (1-3e/2)|\Phi^+\rangle\langle\Phi^+| + (e/2)\sum_{\text{other}} |\text{Bell}_i\rangle\langle\text{Bell}_i|$:

| e | $\text{Tr}(\Gamma_Z \rho_W)$ | $\text{Tr}(\Gamma_X \rho_W)$ | $\text{Tr}(\Gamma_Y \rho_W)$ |
|---|---|---|---|
| 0.01 | 0.01 ✓ | 0.01 ✓ | 0.01 ✓ |
| 0.05 | 0.05 ✓ | 0.05 ✓ | 0.05 ✓ |
| 0.10 | 0.10 ✓ | 0.10 ✓ | 0.10 ✓ |

(测试:[tests/test_protocols/test_sixstate.py](../../tests/test_protocols/test_sixstate.py)`::test_gamma_Y_agrees_with_werner_state` + `::test_gamma_Z_X_agree_with_werner_state`)

---

## 3. WLC SDP 表达

### 3.1 SDP 变量维度

- $d_\rho = \dim(\text{conditional\_alice\_bob}) = 4$(**与 BB84 相同**)
- $\mathcal{G}$:identity on 4-dim(`dim_key=2, dim_side=2`,由 `_construct_G_map` 根据 `bitmap.values()` 自动推断)
- $\mathcal{Z}$:pinching key register($K_0 = |0\rangle\langle 0|_{\text{key}} \otimes I_2$,$K_1 = |1\rangle\langle 1|_{\text{key}} \otimes I_2$)

### 3.2 约束集合 $\mathcal{S}_6$

$$\mathcal{S}_6 = \{\rho \succeq 0 : \text{Tr}(\rho) = 1, \text{Tr}(\Gamma_Z \rho) = e, \text{Tr}(\Gamma_X \rho) = e, \text{Tr}(\Gamma_Y \rho) = e\}$$

相对 BB84 的 $\mathcal{S}_{\text{BB84}}$(只含 $Z, X$ 约束),$\mathcal{S}_6 \subsetneq \mathcal{S}_{\text{BB84}}$ ⇒
$$\min_{\mathcal{S}_6} D(\mathcal{G}(\rho)\|\mathcal{Z}(\mathcal{G}(\rho))) \geq \min_{\mathcal{S}_{\text{BB84}}} D(\cdot)$$

⇒ 六态 per-sift 密钥率 ≥ BB84 per-sift 密钥率(数值测试 `test_wlc_sixstate_above_bb84_per_sift` 验证)。

### 3.3 最优态

对称性强制最优态在 Bell 对角 Werner 态处取到:
$$\rho_6^* = (1 - 3e/2)|\Phi^+\rangle\langle\Phi^+| + \frac{e}{2}\sum_{i \in \{\Phi^-, \Psi^+, \Psi^-\}} |\text{Bell}_i\rangle\langle\text{Bell}_i|$$

详见 [six-state.md §3.5](../literature/six-state.md)。

---

## 4. 数值实验结果(R2.3 硬验收)

### 4.1 WLC SDP vs. 解析公式(CLARABEL fallback)

5 个 QBER 点,`f_ec = 1.0`,全部满足 `abs=1e-3` fallback 阈值:

| QBER | WLC (bit/signal) | 解析 (bit/signal) | \|WLC − 解析\| |
|------|------------------|------------------|----------------|
| 0.01 | 参见 [m2_wlc_mdi_sixstate.ipynb](../../notebooks/m2_wlc_mdi_sixstate.ipynb) | — | < 1e-3 |
| 0.02 | … | … | < 1e-3 |
| 0.05 | ~0.1656 | 0.1656 | < 1e-3 |
| 0.08 | … | … | < 1e-3 |
| 0.10 | … | … | < 1e-3 |

完整 QBER 扫描 + 图表参见 [notebooks/m2_wlc_mdi_sixstate.ipynb](../../notebooks/m2_wlc_mdi_sixstate.ipynb)。

### 4.2 BB84 基线零回归

所有 BB84 测试在增加六态后仍全部通过(21 passed + 9 MOSEK-skip,与 M1 完全一致)。

---

## 5. Additivity 验证

`qkdx/numerics/wlc.py` **零修改**。新增仅限:

- [qkdx/protocols/sixstate.py](../../qkdx/protocols/sixstate.py)(新文件,复用 `bb84_channel` + `_bb84_conditional_state` + `_gamma_qber_Z` + `_gamma_qber_X`)
- [qkdx/analytic/six_state.py](../../qkdx/analytic/six_state.py)(新文件)

符合 REFACTORING_PLAN §5 M2 硬要求:"`numerics/wlc.py` 仅加法式修改"。

---

## 6. Limitations

1. **对称信道假设**:本书写只处理 $Q_Z = Q_X = Q_Y$。非对称情况 M3 + M4A 工作。
2. **假设 Alice 基选择均匀 1/3 每基**:实际实验中常用 biased basis(主基 Z + 辅助基 X/Y),本书写不覆盖 bias,归 Phase 1 Sub-Q2 family sheet。
3. **未覆盖 advantage distillation**:Bruss 1998 + Chau 2002 讨论的 6-state 二路后处理可将阈值推到 ~27.6%,本书写只做单向后处理(渐近 Devetak-Winter),与 RESEARCH_PLAN §2.2 范围一致。
