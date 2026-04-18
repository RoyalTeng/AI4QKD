# Phase 0 M1 Technical Specification v0.1

**文档状态**:v0.1 首次落盘(2026-04-19)
**关联文档**:
- [PROSPECTUS.md](PROSPECTUS.md) v3.1 §4.1 引用本文件的 §2(MS-EB 完整技术定义)
- [RESEARCH_PLAN.md](RESEARCH_PLAN.md) v1.0 §2.1–§2.5 引用本文件的 §7(M1–M4 验收流程)
- [REFACTORING_PLAN.md](REFACTORING_PLAN.md) v3.1.4 §4.1–§4.6 + 附录 B 是本文件数学定义的 Python 实现
**目标读者**:M1–M4 实施者 + codex 评审 + 未来外部审稿人

> **本文件在文档栈中的位置**:
> - PROSPECTUS = 研究地图(WHY)
> - RESEARCH_PLAN = 研究执行计划(HOW-to-do-research)
> - **本文件 = 技术规格(HOW-to-formalize-the-math)**:给出 MS-EB 框架的**数学严格**定义 + BB84 完整 worked example + WLC SDP 的**第一性原理推导** + M1–M4 的验收协议(可被第三方执行 + 校验)
> - REFACTORING_PLAN = 实施规范(HOW-to-build:Python API、测试、运营)

---

## 0. TL;DR

本文件是 M1 实施的**数学铭牌**。所有 M1 代码(`qkdx/core/`, `qkdx/protocol/base.py`, `qkdx/protocols/bb84.py`, `qkdx/numerics/wlc.py`)必须能被本文件的定义**形式化验证** —— 即:给一个第三方(人或 AI)这份文件 + 代码,他们能独立判定代码是否正确实现了本文件所规定的数学对象。

**验收边界**:M1 代码通过 `pytest tests/test_numerics/test_wlc_bb84.py`(见 REFACTORING_PLAN §4.6 完整测试)+ 本文件 §7 的验收协议。

---

## 1. 符号约定

| 记号 | 含义 | 形式 |
|------|------|------|
| $\mathcal{H}, \mathcal{H}_A, \mathcal{H}_B$ | Hilbert 空间;下标标注系统 | 有限维复向量空间 |
| $\dim \mathcal{H}_X$ | 系统 $X$ 的 Hilbert 空间维度 | 正整数 |
| $\mathcal{L}(\mathcal{H})$ | $\mathcal{H}$ 上的线性算子空间 | 约定为 $\mathcal{H} \to \mathcal{H}$ |
| $\mathcal{D}(\mathcal{H})$ | 密度算子集合 | $\{\rho \in \mathcal{L}(\mathcal{H}): \rho = \rho^\dagger, \rho \succeq 0, \tr\rho = 1\}$ |
| $\ket{i}, \bra{j}$ | 计算基 ket / bra | 列向量 / 行向量 |
| $\ket{\psi}_{AB}$ | $\mathcal{H}_A \otimes \mathcal{H}_B$ 上的纯态 | 单位向量 |
| $\mathcal{E}: \mathcal{L}(\mathcal{H}_\text{in}) \to \mathcal{L}(\mathcal{H}_\text{out})$ | 量子映射 | 线性,CP;TP(Trace Preserving)或 TNI(Trace Non-Increasing) |
| $\{K_i\}$ | $\mathcal{E}$ 的 Kraus 表示 | $\mathcal{E}(\rho) = \sum_i K_i \rho K_i^\dagger$ |
| CPTP | 完全正 + 迹保持 | $\sum_i K_i^\dagger K_i = I$ |
| CPTNI | 完全正 + 迹不增 | $\sum_i K_i^\dagger K_i \preceq I$ |
| $\tr_X$ | 对子系统 $X$ 求偏迹 | — |
| $S(\rho)$ | von Neumann 熵(bit 基) | $-\tr(\rho \log_2 \rho)$ |
| $h(x)$ | 二元熵 | $-x\log_2 x - (1-x)\log_2(1-x)$,$x \in [0,1]$ |
| $D(\rho \| \sigma)$ | 相对熵(bit 基) | $\tr\rho(\log_2\rho - \log_2\sigma)$ 若 $\supp\rho \subset \supp\sigma$,否则 $+\infty$ |
| $\ln, \log_2$ | 自然对数 / 2-对数 | 默认熵的单位为 bit,即 $\log_2$ |

**基对流约定**:所有密钥率数字以 **bit/signal** 为最终单位(见 REFACTORING_PLAN.md §4.6 `WLCResult.key_rate`)。CVXPY 的 `quantum_rel_entr` 返回 nat 基,代码中需除以 $\ln 2$ 换算。

---

## 2. MS-EB 框架的形式化定义

本节是 PROSPECTUS §4.1 引用的"完整技术定义"。

### 2.1 五元组定义

**定义 2.1(MS-EB 协议)**:一个 MS-EB 协议是五元组

$$\Pi = (\mathcal{P}, \mathcal{E}, \mathcal{A}, \mathcal{T}, \mathcal{K})$$

其中各分量定义如下。

#### 2.1.1 $\mathcal{P}$:源方集合

$\mathcal{P} = (P_1, P_2, \ldots, P_n)$ 是一个有序源方列表。每个 $P_i$ 是三元组

$$P_i = (N_i, d_{K,i}, d_{S,i}, \ket{\psi_i}_{A_i A_i'})$$

- $N_i \in \{\text{"Alice"}, \text{"Bob"}, \text{"Charlie"}, \ldots\}$:源方名称
- $d_{K,i} \in \mathbb{Z}_+$:$P_i$ 的**密钥寄存器** $A_i$ 的 Hilbert 空间维度
- $d_{S,i} \in \mathbb{Z}_+$:$P_i$ 的**信号寄存器** $A_i'$ 的 Hilbert 空间维度
- $\ket{\psi_i}_{A_i A_i'} \in \mathcal{H}_{A_i} \otimes \mathcal{H}_{A_i'}$:$P_i$ 制备的 EB 纯态,满足 $\|\ket{\psi_i}\|^2 = 1$

**语义**:$P_i$ 本地持有 $A_i$(密钥寄存器,是其经典随机选择的量子化),通过 $\mathcal{E}$ 向公共网络发送 $A_i'$(信号寄存器)。

#### 2.1.2 $\mathcal{E}$:公共量子网络

$\mathcal{E}$ 是一个 **CPTP**(严格 trace-preserving)映射

$$\mathcal{E}: \mathcal{L}\!\left(\bigotimes_{i=1}^n \mathcal{H}_{A_i'}\right) \longrightarrow \mathcal{L}(\mathcal{H}_B) \otimes \mathbb{C}[\mathcal{C}]$$

其中:

- $\mathcal{H}_B$:接收方(Bob)的量子寄存器,维度 $d_B$
- $\mathcal{C}$:公开声明空间,有限集合,维度 $|\mathcal{C}|$
- $\mathbb{C}[\mathcal{C}]$:以 $\mathcal{C}$ 为计算基的经典寄存器

**维度一致性**(不变量 I1):
$$\dim \mathcal{H}_\text{in}(\mathcal{E}) = \prod_{i=1}^n d_{S,i}, \quad \dim \mathcal{H}_\text{out}(\mathcal{E}) = d_B \cdot |\mathcal{C}|$$

**语义**:$\mathcal{E}$ 把所有源方的信号寄存器同时作为输入,输出 Bob 的量子寄存器 $B$ 和一个公开的 classical outcome $c \in \mathcal{C}$(通常是探测器点击模式)。

**untrusted measurement relay 拓扑的特化**:当 $d_B = 1$ 时(即 Bob 的量子输出被完全测量化),$\mathcal{E}$ 退化为"纯经典输出"的网络(如 MDI-QKD 的 Charlie),PROSPECTUS §1 主问题正是对此拓扑。

#### 2.1.3 $\mathcal{A}$:宣告规则

$\mathcal{A}$ 是一对函数 $(\text{publish}, \text{sift\_keep})$:

$$\text{publish}: \mathcal{C} \to \mathcal{D}, \qquad \text{sift\_keep}: \mathcal{C} \to \{\text{True}, \text{False}\}$$

其中 $\mathcal{D}$ 是公开宣告空间(可与 $\mathcal{C}$ 不同,如投影掉 Bob 的 bit 只公开基)。

**GEAT non-signalling 兼容性(NSP 条件,硬约束)**:存在某个固定 Markov chain $M_i \to A_i K_i A_\text{pub}$(Metger et al. 2024 Thm. 2.1 的形式),使得每轮的公开信息 $A_\text{pub} = \text{publish}(c)$ 关于 Eve 的信息是可控的。**Phase 0 只要求 per-round $\mathcal{A}$,不考虑跨轮**。

#### 2.1.4 $\mathcal{T}$:接受性测试

$\mathcal{T}$ 是一个布尔谓词

$$\mathcal{T}: (\text{accumulated statistics}) \to \{\text{accept}, \text{abort}\}$$

在 Phase 0 M1 只用作占位符(总是 accept),M1 的密钥率为渐近率,不涉及 $\mathcal{T}$ 的具体实现。

#### 2.1.5 $\mathcal{K}$:密钥映射

$\mathcal{K}$ 是一个 CPTP 映射

$$\mathcal{K}: \mathcal{L}(\mathcal{H}_{A_\kappa}) \to \mathcal{L}(\mathcal{H}_{A_\text{key}})$$

其中 $P_\kappa \in \mathcal{P}$ 是 **密钥方**(通常是 Alice),$A_\text{key}$ 是最终密钥寄存器。

**Phase 0 限制**:

- $A_\text{key}$ 为经典 bit,即 $\dim \mathcal{H}_{A_\text{key}} = 2$
- $\mathcal{K}$ 是沿 $A_\kappa$ 某组正交基的投影测量 + 经典 bitmap,即 $\mathcal{K}(\rho) = \sum_x b(x) \cdot \proj{x}\rho\proj{x}$,其中 $b: \{\text{outcomes}\} \to \{0,1\}$

#### 2.1.6 跨对象不变量(在 `MSEBProtocol.__post_init__` 中校验)

**I1**(见 §2.1.2):$\dim \mathcal{H}_\text{in}(\mathcal{E}.channel) = \prod_i d_{S,i}$

**I2**:$P_\kappa \in \mathcal{P}$(密钥方必须在源方列表中)

**I3**:$\text{sift\_keep}$ 的定义域与 $\mathcal{E}$ 的 classical outcomes 兼容

**I4**(v3.1 Sub-Q1(d)):每个协议对象必须带 `scope_tag ∈ {covered, partial, out_of_scope}` 与 `scope_reason`,out-of-scope 类型阻止下游 SDP 派生

### 2.2 协议执行语义

**定义 2.2(联合态)**:

$$\ket{\psi_\Pi}_{A_1 A_1' A_2 A_2' \cdots A_n A_n'} \coloneqq \bigotimes_{i=1}^n \ket{\psi_i}_{A_i A_i'}$$

**定义 2.3(执行后态)**:对 $\mathcal{E}$ 作用在所有信号寄存器后,

$$\rho^{\text{exec}}_\Pi \coloneqq (\mathbb{I}_{A_1 \cdots A_n} \otimes \mathcal{E}) \left[ \proj{\psi_\Pi}_{A_1 A_1' \cdots A_n A_n'} \right]$$

这是 $\mathcal{H}_{A_1} \otimes \cdots \otimes \mathcal{H}_{A_n} \otimes \mathcal{H}_B \otimes \mathbb{C}[\mathcal{C}]$ 上的密度算子。

**定义 2.4(sifted 条件态)**:给定宣告规则 $\mathcal{A}$,定义

$$\rho^{\text{sift}}_\Pi \coloneqq \frac{1}{p_\text{sift}} \sum_{c \in \mathcal{C}:\, \text{sift\_keep}(c) = \text{True}} \tr_{\mathcal{H}_B \otimes \mathbb{C}[\mathcal{C}]}\!\left[ (I \otimes \proj{c}) \rho^{\text{exec}}_\Pi (I \otimes \proj{c}) \right] \otimes \proj{c}_{A_\text{pub}}$$

其中 $p_\text{sift} = \sum_{c: \text{keep}=\text{True}} \tr[(I \otimes \proj{c}) \rho^{\text{exec}}]$ 是 sift 概率(Phase 0 M1 对 BB84 理想 = 0.5)。

该态是下游 WLC SDP 的输入,记为

$$\rho_{AB \mid \text{keep}} \coloneqq \tr_{A_\text{pub}} \rho^{\text{sift}}_\Pi$$

当没有歧义时,直接称作"conditional Alice-Bob state"。$\rho_{AB \mid \text{keep}}$ 的 Hilbert 空间维度记作 $d_\text{cond}$,**REFACTORING_PLAN §4.4 的 `MSEBProtocol.conditional_alice_bob_dim()` 必须返回此值**。

### 2.3 "out-of-scope" 协议的形式化识别

**命题 2.5**(框架覆盖裂缝)一个协议 $\Pi'$ 落在 MS-EB 覆盖**外**(`scope_tag = out_of_scope`)当且仅当满足以下至少一条:

(a) 源方的信号寄存器 $A_i'$ 在多轮间被保留(违反 PROSPECTUS §3.1 H2 无量子存储)

(b) $\mathcal{E}$ 在协议执行过程中**依赖先前轮次的公开声明而改变**(如跨轮自适应重定义 channel)

(c) $\mathcal{A}$ 需要跨轮联合声明(如 MP-QKD 的 pairing;Phase 0 降级处理,Phase 1 扩展)

(d) 需要 Bell 违反作为安全性来源(DI-QKD;违反 PROSPECTUS §3.1 H3)

对应 RESEARCH_PLAN §2.1 R1.4 的拒收机制在 `MSEBProtocol.__post_init__` 对这些情形显式 raise `OutOfScopeError` 或发 `OutOfScopeWarning`。

---

## 3. BB84 的 MS-EB 完整 worked example

本节是 §2 定义的具体化。M1 代码(`qkdx/protocols/bb84.py`)必须能复现本节所有数学对象。

### 3.1 $\mathcal{P}$:单源方 Alice

$\mathcal{P} = (P_1)$,$P_1 = (\text{"Alice"}, d_K = 4, d_S = 2, \ket{\psi_1})$:

- 密钥寄存器 $A_1$ 维度 $d_K = 4$,基为 $\{\ket{x, \theta}: x \in \{0,1\}, \theta \in \{Z, X\}\}$
- 信号寄存器 $A_1'$ 维度 $d_S = 2$(qubit)
- EB 纯态:

$$\ket{\psi_1}_{A_1 A_1'} = \frac{1}{2} \sum_{x \in \{0,1\}} \sum_{\theta \in \{Z,X\}} \ket{x, \theta}_{A_1} \otimes U_\theta \ket{x}_{A_1'}$$

其中 $U_Z = I$,$U_X = H$(Hadamard)。

**归一化校验**:$\|\ket{\psi_1}\|^2 = \frac{1}{4} \sum_{x,\theta} 1 = 1$ ✓

### 3.2 $\mathcal{E}$:量子信道 + Bob 测量

$\mathcal{E} = \mathcal{E}_\text{ch} \circ \mathcal{M}_\text{Bob}$,分两步:

#### 3.2.1 $\mathcal{E}_\text{ch}$:对称去极化信道(M1 占位模型)

$$\mathcal{E}_\text{ch}(\sigma) = (1 - p)\sigma + \frac{p}{3}(X\sigma X + Y\sigma Y + Z\sigma Z)$$

QBER 与 $p$ 的转换:对 $\sigma = \proj{0}$,测量在计算基上得到 $\ket{1}$ 的概率为 $\frac{2p}{3}$;定义 QBER $e = \frac{2p}{3}$,故 $p = \frac{3e}{2}$。

**Kraus 形式**:

$$K_0 = \sqrt{1 - p}\, I, \qquad K_1 = \sqrt{p/3}\, X, \qquad K_2 = \sqrt{p/3}\, Y, \qquad K_3 = \sqrt{p/3}\, Z$$

**CPTP 校验**:$\sum_i K_i^\dagger K_i = (1-p)I + \frac{p}{3}(X^2 + Y^2 + Z^2) = (1-p)I + pI = I$ ✓

#### 3.2.2 $\mathcal{M}_\text{Bob}$:Bob 的随机基选择测量

Bob 先均匀随机选择 $\theta_B \in \{Z, X\}$,在 $\theta_B$ 基上测量,得到 bit $b \in \{0,1\}$。

形式化为 POVM $\{\Pi^{\theta_B, b}\}$,共 4 个 outcome,

$$\Pi^{Z,0} = \frac{1}{2}\proj{0}, \quad \Pi^{Z,1} = \frac{1}{2}\proj{1}, \quad \Pi^{X,0} = \frac{1}{2}\proj{+}, \quad \Pi^{X,1} = \frac{1}{2}\proj{-}$$

每个因子 $\frac{1}{2}$ 来自 Bob 随机选择 $\theta_B$ 的概率。**POVM 完备性**:$\sum_{\theta_B, b} \Pi^{\theta_B, b} = \frac{1}{2}(I + I) = I$ ✓

经过 $\mathcal{M}_\text{Bob}$ 后,Bob 的量子寄存器被测量坍缩;$d_B = 1$(纯经典输出);$|\mathcal{C}| = 4$(四个 $(\theta_B, b)$ 组合)。

### 3.3 $\mathcal{A}$:sifting

$$\text{publish}(\theta_B, b) = \theta_B \quad (\text{公开 Bob 的基选择,Alice 同时公开 } \theta_A)$$

$$\text{sift\_keep}(\theta_A, \theta_B, b) = [\theta_A = \theta_B]$$

理想 BB84 下,$p_\text{sift} = \Pr[\theta_A = \theta_B] = 1/2$。

### 3.4 $\mathcal{T}$:M1 占位

$\mathcal{T}$ 总是返回 accept(M1 渐近率不涉及 $\mathcal{T}$)。

### 3.5 $\mathcal{K}$:Alice 的 bit 作为密钥

$P_\kappa = P_1$(Alice),$\mathcal{K}$ 对 $A_\text{key}$ 寄存器的"bit 子系统"取对角:

$$\mathcal{K}(\rho_{A_\text{key}}) = \sum_{x \in \{0,1\}} \proj{x} \rho_{A_\text{key}} \proj{x}$$

其中 $\ket{x}$ 是 bit 寄存器的计算基。

### 3.6 跨对象不变量校验

- **I1**:$\dim \mathcal{H}_\text{in}(\mathcal{E}) = d_S = 2$,且 $\prod_i d_{S,i} = 2$ ✓
- **I2**:$P_\kappa = \text{Alice} \in \mathcal{P}$ ✓
- **I3**:$\text{sift\_keep}$ 接受 $(\theta_A, \theta_B, b)$,与 $\mathcal{C} = \{(\theta_B, b)\}$ 兼容(Alice 的 $\theta_A$ 由 Alice 本地知道)
- **I4**:`scope_tag = covered`

### 3.7 $\rho_{AB \mid \text{keep}}$ 的显式形式

应用 §2.2 的执行语义,对 QBER = $e$ 的理想 BB84:

$$\rho_{AB \mid \text{keep}} = \frac{1}{2}\sum_{\theta \in \{Z, X\}} \sum_{x \in \{0,1\}} \proj{x, \theta}_{A_\text{key}} \otimes \mathcal{E}_\text{ch}(U_\theta \proj{x} U_\theta^\dagger)_{B}$$

$d_\text{cond} = 4 \cdot 2 = 8$(Alice key register 4 维 × Bob 残余 qubit 2 维)。

**Alice-Bob 两基的 QBER 可观测量**(Γ 算子):

$$\Gamma_\text{qber\_Z} = \frac{1}{2} \sum_{x} \proj{x, Z}_{A_\text{key}} \otimes \proj{1-x}_B$$

$$\Gamma_\text{qber\_X} = \frac{1}{2} \sum_{x} \proj{x, X}_{A_\text{key}} \otimes H\proj{1-x}H_B$$

(系数 $\frac{1}{2}$ 是 Alice 基选择概率;Bob 基已由 sifting 锁定为同基)

**观测约束**:$\tr(\Gamma_\text{qber\_Z} \cdot \rho_{AB \mid \text{keep}}) = e$,$\tr(\Gamma_\text{qber\_X} \cdot \rho_{AB \mid \text{keep}}) = e$(对称去极化下两基 QBER 相等)。

---

## 4. WLC SDP 的第一性原理推导

本节给出 REFACTORING_PLAN.md §4.6 + 附录 B 的数学来源。引用 Winick-Lütkenhaus-Coles 2018(以下简称 WLC18)的 Eq. 编号。

### 4.1 Devetak-Winter 公式与 WLC 化简

**Devetak-Winter 公式**(Devetak-Winter 2005 Thm. 1):对集体攻击的渐近密钥率下界

$$R_\infty \geq p_\text{sift} \cdot \left[ H(A_\text{key} \mid E) - f_\text{ec} \cdot H(A_\text{key} \mid B)_{\text{keep}} \right]$$

其中 $E$ 是 Eve 的窃听系统,$H(A_\text{key} \mid E)$ 是 Alice key 对 Eve 的条件熵(越大越安全),$H(A_\text{key} \mid B)$ 是 Alice-Bob 的经典条件熵(反映 EC 代价,$f_\text{ec} \geq 1$ 是 Cascade 效率因子)。

**对 BB84**:$H(A_\text{key} \mid B)_\text{keep} = h(e)$(QBER = $e$)。

### 4.2 WLC 的关键化简

WLC18 §3 指出,对于 Purified(EB)协议,$H(A_\text{key} \mid E) = H(A_\text{key})_{\mathcal{G}(\rho)} - H(A_\text{key})_{\mathcal{Z}(\mathcal{G}(\rho))}$ 可以进一步化简为相对熵的差:

$$H(A_\text{key} \mid E)_{\rho_{AB|\text{keep}}} = \min_{\rho \in S} D\big( \mathcal{G}(\rho) \,\big\|\, \mathcal{Z}(\mathcal{G}(\rho)) \big) \tag{WLC18 Eq. 8}$$

其中:

- $S = \{\rho \in \mathcal{D}(\mathcal{H}_{AB}) : \tr(\Gamma_k \rho) = \gamma_k,\; \forall k\}$ 是满足实验观测约束的可行密度算子集合
- $\mathcal{G}: \mathcal{L}(\mathcal{H}_{AB}) \to \mathcal{L}(\mathcal{H}_{A_\text{key}} \otimes \mathcal{H}_{B_\text{side}})$ 是**密钥提取 + Bob 测量**的 CPTNI 映射(非 trace-preserving,因为可以丢掉部分 outcome)
- $\mathcal{Z}: \mathcal{L}(\mathcal{H}_{A_\text{key}}) \to \mathcal{L}(\mathcal{H}_{A_\text{key}})$ 是 pinching 信道 $\mathcal{Z}(\sigma) = \sum_x \proj{x} \sigma \proj{x}$,在 $\mathcal{H}_{A_\text{key}} \otimes \mathcal{H}_{B_\text{side}}$ 上自然延拓为 $\mathcal{Z} \otimes \mathbb{I}_{B_\text{side}}$

### 4.3 从连续优化到 SDP

$D(\rho \| \sigma)$ 是联合凸的(Lindblad 定理),$S$ 是关于 $\rho$ 仿射,故 (WLC18 Eq. 8) 是凸优化问题。在 CVXPY 的实现中,$D(\cdot \| \cdot)$ 以 `cp.quantum_rel_entr` 提供,其为 SDP-representable(Fawzi-Saunderson 2023)。

**完整 SDP**:

$$\begin{aligned}
\min_{\rho}\quad &D\big(\mathcal{G}(\rho) \,\big\|\, (\mathcal{Z} \otimes \mathbb{I}_{B_\text{side}})(\mathcal{G}(\rho))\big) \\
\text{s.t.}\quad &\rho \in \mathcal{L}(\mathcal{H}_{AB}),\quad \rho = \rho^\dagger,\quad \rho \succeq 0 \\
&\tr(\rho) = 1 \\
&\tr(\Gamma_k \rho) = \gamma_k,\quad k \in \{\text{观测名}\}
\end{aligned}$$

**Devetak-Winter 拼装**:最终密钥率(bit/signal)为

$$R = p_\text{sift} \cdot \left[ \text{SDP}^\star / \ln 2 - f_\text{ec} \cdot h(e_Z) \right]$$

其中 $\text{SDP}^\star$ 是 SDP 目标最优值(CVXPY 返回 nat 基,除以 $\ln 2$ 换 bit),$e_Z$ 是 Z 基 QBER。

### 4.4 数值稳定性修订(对应 REFACTORING_PLAN §4.6 关键细节)

**问题**:直接写 `cp.quantum_rel_entr(G(ρ), Z(G(ρ)))`,当 $\mathcal{G}(\rho)$ 退化(低秩)时会抛 DCPError。

**修订 1(Hermitian 投影)**:显式对齐 Hermitian 性:

$$X_\text{raw} \leftarrow \frac{1}{2}(X_\text{raw} + X_\text{raw}^\dagger), \qquad X_\text{raw} = \mathcal{G}(\rho)$$

**修订 2(通道级去极化正则化)**:加入 $\varepsilon \in (0, 1)$ 的正则化:

$$X_\text{reg} = (1-\varepsilon) X_\text{raw} + \varepsilon \cdot \tr(X_\text{raw}) \cdot \frac{I}{d_\text{out}}$$

**关键**:$\mathcal{G}$ 为 **CPTNI**,一般 $\tr(X_\text{raw}) \neq \tr(\rho) = 1$;必须显式用 `cp.trace(X_raw)`,不可替换为常数 1(见 REFACTORING_PLAN §4.6 关键实现细节 #2)。

**修订 3(单位换算)**:`cp.quantum_rel_entr` 返回 nat 基,对外密钥率必须除以 $\ln 2$。

### 4.5 与 Shor-Preskill 解析的对应

**Shor-Preskill 2000**:对 BB84,$R_{SP}(e) = p_\text{sift} \cdot \max(0, 1 - 2h(e))$,$p_\text{sift} = 1/2$。

**一致性要求**(M1 硬验收):

$$\left| R_{\text{WLC-SDP}}(e) - R_{SP}(e) \right| \leq \max(0.01 \cdot R_{SP}(e),\; 5 \times 10^{-4}), \qquad \forall e \in \{0, 0.01, 0.02, 0.05, 0.08, 0.10\}$$

(MOSEK 主线阈值,CLARABEL fallback 松一档至 $\text{rel}=0.02, \text{abs}=10^{-3}$;见 RESEARCH_PLAN §1.2)

---

## 5. facial reduction:QBER = 0 情形的处理

### 5.1 现象

当 $e = 0$ 时,$\rho_{AB \mid \text{keep}}$ 被观测约束强制为特定投影面(Alice 的 key 与 Bob 的测量结果完全相关),即 $\supp(\rho) \subsetneq \mathcal{H}_{AB}$。此时 SDP 在原始变量空间中 strictly primal infeasible,MOSEK 与 CLARABEL 都会报 `infeasible` 或 `inaccurate`。

### 5.2 Hu-Im-Lin-Lütkenhaus-Wolkowicz 2022 的 facial reduction 修订

**Hu et al. 2022 Algorithm 1**:
1. 检测 dual infeasibility,识别 $\rho$ 必然位于的最小面 $F$
2. 构造从 $F$ 到原空间的 lift 算子 $L: F \to \mathcal{H}_{AB}$
3. 在 $F$ 上重新参数化求解

**本项目的接口**(REFACTORING_PLAN §4.7):

```python
def reduce_problem(
    prob: cp.Problem,
    variable: cp.Variable,
) -> tuple[cp.Problem, Callable[[], Matrix]]:
    """返回 (reduced_prob, lift)。
    lift(): 在 reduced_prob.solve() 之后调用,返回原空间 ρ 的 .value。"""
```

### 5.3 M3 硬验收

`test_wlc_bb84_qber_exact_zero_with_facial_reduction`(REFACTORING_PLAN §4.6 测试)要求:对精确 QBER=0,`primal_status ∈ {optimal, optimal_inaccurate}` 且 $R = 1.0 \pm 5 \times 10^{-4}$(bit/sift)再 乘 $p_\text{sift} = 0.5$ 即 bit/signal。

---

## 6. 六态、MDI-QKD、TF-QKD 的 MS-EB 书写大纲(M2–M4)

本节仅列出 $(\mathcal{P}, \mathcal{E}, \mathcal{A}, \mathcal{T}, \mathcal{K})$ 的核心差异,完整书写见 M2/M3/M4 的 `docs/msen/*.md`。

### 6.1 六态(M2)

- $\mathcal{P}$ 与 BB84 相同,但密钥寄存器 $d_K = 6$(3 基 × 2 bit),基集合 $\{Z, X, Y\}$
- $\mathcal{E}_\text{ch}$ 相同
- $\mathcal{A}$ 匹配基,$p_\text{sift} = 1/3$
- $\mathcal{K}$ 同 BB84
- 解析基线:$R_\text{six-state}(e) = p_\text{sift} \cdot (1 - h(e) - e \log_2 3)$

### 6.2 MDI-QKD(M2)

- $\mathcal{P} = (P_1, P_2)$ 两源方(Alice, Bob),各自独立 BB84 源
- $\mathcal{E}$ 包含:两端信道 $\mathcal{E}_\text{ch,A} \otimes \mathcal{E}_\text{ch,B}$ + Charlie 的 Bell-state 测量 POVM $\{\Pi^{\text{BSM}}_i\}_{i=1}^4$(或 $\{\Pi^{\text{BSM}}_i\}_{i=1}^2$ 的 partial BSM)
- $d_B = 1$(Charlie 纯经典输出);$|\mathcal{C}| = 4 \times 4 = 16$(Alice 基 + Bob 基 + BSM 结果)
- $\mathcal{A}$:Alice 与 Bob 公开基,Charlie 公开 BSM outcome,`sift_keep = [基匹配 AND BSM 成功]`
- $\mathcal{K}$:Alice 或 Bob 根据 Charlie 宣告做翻转,最终密钥比特取自 Alice

### 6.3 TF-QKD(M4B)

- $\mathcal{P} = (P_1, P_2)$ 两源方,但 $A_i'$ 为光模式(有限 Fock 截断 $N_\text{cut}$),$d_{S,i} = N_\text{cut} + 1$
- $\mathcal{E}$ 包含:两端信道 + Charlie 的**单光子干涉**(mode matching + single-click detection)
- 难点(PROSPECTUS §4.3 已识别裂缝):分布式相位参考在 MS-EB 下是否**自然表达**,Phase 0.5 研究的第一工作
- 若不自然 → 降级到 decoy finite-key 扩展(REFACTORING_PLAN §8 R3)

---

## 7. M1–M4 验收协议(第三方可执行)

### 7.1 M1 验收流程(逐步)

第三方(人或 codex)执行以下命令:

```bash
# Step 0: 环境
cd $REPO_ROOT
uv sync --frozen                # 用 uv.lock 精确复现
export PYTHONHASHSEED=20260418  # 见 REFACTORING_PLAN §11.1

# Step 1: 单元测试
pytest tests/test_core/ -v                        # §4.1-§4.3 基础模块
pytest tests/test_protocol/test_base.py -v        # §4.4 MSEBProtocol 不变量
pytest tests/test_protocols/test_bb84.py -v       # §4.5 BB84 MS-EB 构造
pytest tests/test_numerics/test_wlc_bb84.py -v    # §4.6 WLC SDP 核心测试(6 qber 点)

# Step 2: 覆盖率
pytest --cov=qkdx --cov-report=term-missing \
    --cov-config=.coveragerc
# 验收:core ≥ 95%, numerics.wlc ≥ 75%, overall ≥ 85%

# Step 3: notebook 复现
papermill notebooks/m1_wlc_bb84.ipynb /tmp/m1_out.ipynb
# 验收:完成且无异常;生成 notebooks/figures/m1_bb84_vs_shor_preskill.png

# Step 4: out-of-scope 拒收(R1.4)
python -c "from qkdx.protocol.base import MSEBProtocol; \
    from tests.fixtures.out_of_scope_toy import build_toy_out_of_scope; \
    try: build_toy_out_of_scope(); print('FAIL: should raise'); \
    except Exception as e: print(f'OK: {e}')"
# 验收:打印 OK + OutOfScopeError 的 reason 字段非空
```

### 7.2 M1 硬验收清单(M1 memo `docs/findings/m1_wlc_bb84.md` 必填)

- [ ] `test_wlc_bb84_matches_shor_preskill` 6 个 qber 点全部通过,MOSEK 主线 `rel=0.01, abs=5e-4`
- [ ] `test_wlc_bb84_above_threshold_gives_zero` 通过(QBER=0.13 → $R \leq 5 \times 10^{-4}$)
- [ ] `test_wlc_bb84_qber_exact_zero_with_facial_reduction` 通过(QBER=0 → $R \approx 1$,facial reduction 被触发)
- [ ] `test_wlc_observable_key_missing_raises` + `test_wlc_observable_key_unknown_raises` 通过
- [ ] `test_wlc_fallback_to_clarabel` 通过(CLARABEL fallback 阈值 `rel=0.02, abs=1e-3`)
- [ ] 覆盖率:core ≥ 95%, `numerics.wlc` ≥ 75%, overall ≥ 85%
- [ ] notebook `m1_wlc_bb84.ipynb` 一键 papermill 重跑;复现图 `figures/m1_bb84_vs_shor_preskill.png`
- [ ] `framework_coverage.md` 草稿(R1.4 产出)含 BB84 标注 `covered`
- [ ] memo 含 §0 复现元数据 + §6 Limitations + §7 AI 协助范围(RESEARCH_PLAN §7.3 模板)

### 7.3 M2–M4 验收协议的对应扩展

- **M2**:加 `tests/test_protocols/test_sixstate.py`, `test_mdi.py` + `analytic/gllp.py` 单测;六态 / MDI 各一份 msen 文档;BB84 基线测试零回归
- **M3**:加 `tests/test_numerics/test_facial.py`, `test_decoy_bb84.py`;距离扫描图 20-200 km
- **M4A**:加 `tests/test_symmetry/` 全套;Clifford 约化 BB84 的 SDP 维度 4→2 数值一致性
- **M4B**(Phase 0.5,可选):加 `tests/test_protocols/test_tfqkd.py`;log-log 斜率 = 0.5 ± 0.05

详细 M2–M4 验收见 REFACTORING_PLAN §5 的 Milestone 表格,本文件不重复。

---

## 8. 验证:本文件与代码的一致性检查

本文件的**数学定义**必须被代码**忠实实现**。一致性通过以下机制保证:

### 8.1 docstring 引用本文件的 §

所有 `qkdx/` 公共 API 的 docstring 必须在 See Also / Notes 小节引用本文件的定义编号,如:

```python
def conditional_alice_bob(self) -> Matrix:
    """Return the sifted conditional density operator ρ_{AB | keep}.

    See Also
    --------
    docs/PHASE0_M1_TECHNICAL_SPEC.md §2.2, Definition 2.4
    """
```

### 8.2 定理号的 commit message 交叉引用

涉及本文件命题的代码改动,commit message 必须显式引用:"Implements TECH_SPEC §N.M Def/Thm/Eq X.Y"。

### 8.3 codex 协议一致性评审

每个 Milestone 完成后,跑一次 codex review,输入 `docs/PHASE0_M1_TECHNICAL_SPEC.md + qkdx/<milestone>/*.py`,要求输出 ✅ 或具体 diff。

---

## 9. 变更控制

本文件是 M1–M4 实施的**规格**。变更规则:

1. **定义变更**:任何 §1–§6 的定义变更必须同步到代码 + 测试,不允许先改代码再补文件
2. **验收变更**:任何 §7 的验收条件变更必须先得到 RESEARCH_PLAN 的同步更新;严格 non-regression
3. **ADR**:任何背离本文件的实现决策必须写 `docs/adr/NNNN-*.md` 并在 memo 中显式声明

---

## Changelog

- **v0.1**(2026-04-19):首次落盘。包含 MS-EB 五元组的形式化定义(§2)、BB84 worked example(§3)、WLC SDP 第一性原理推导(§4)、facial reduction 数学处理(§5)、M2-M4 大纲(§6)、第三方可执行的 M1-M4 验收协议(§7)、代码-规格一致性机制(§8)。

---

*文档结束*
