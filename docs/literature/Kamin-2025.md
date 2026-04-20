# Kamin-Arqand-George-Lütkenhaus-Tan 2025 精读(Level 3–4)

**论文引用**:
- Kamin, L., Arqand, A., George, I., Lütkenhaus, N., Tan, E. Y.-Z. (2025). *Finite-size analysis of prepare-and-measure and decoy-state QKD via entropy accumulation.* arXiv:2406.10198v3 [quant-ph] (15 Sep 2025).
- 本 memo 基于 PDF (968 KB, 40 pp.)
- **注**:RESEARCH_PLAN §3.3 S2.5 原引作 "Kamin et al. 2025. PRX Quantum 6:020342";arXiv 版本 v3 为本 memo 依据
- 重要前置:
  - [MFS+22/MR23] Metger-Fawzi-Sutter-Renner 2022 = GEAT 主文(本仓库 `docs/literature/GEAT-2024.md`)
  - [GLH+22] George-Lin-Lütkenhaus-van-Himbeeck 2022 = 前期 EAT QKD 分析(GLL-2021 扩展)
  - [LLR+21] Liu et al. 2021 = 改进 GEAT 第二阶项的另一版本(Supplement Theorem 2)
  - [WLC18] Winick-Lütkenhaus-Coles 2018 = 渐近数值 QKD SDP
  - [DF19] Dupuis-Fawzi 2019 = EAT with improved second-order term
  - [WL22, NUL23, KL24, KTL25] = decoy-state 分析的前置(被本文统一成单步 SDP)

**精读日期**:2026-04-19 / 2026-04-20(Phase 1 S2.5 准备层)
**精读等级**:**Level 3–4**
- §1 Introduction:完整精读(定位贡献 + 与前置的比较)
- §2 Notation:浏览
- §3 Protocol description (Protocol 1):完整精读
- §4 Improved EA analysis for PM protocols:完整精读(GEAT channel 定义 + Theorem 1 + 密钥长度 Theorem 3)
- §5 Key rate computation techniques:**完整精读**(Theorem 4 SDP + completeness LP + security parameter optimization)
- §6 Qubit BB84 with loss:完整精读(Fig. 1, 2)
- §7 Decoy-state with improved analysis:Level 3 精读(Theorem 6 + Fig. 3, 4);Appendix B/C 浏览
- §8 Conclusion + Theorem 5(coherent attack 扩展):完整精读

**范围说明**:
- 本 memo **覆盖**:Kamin 2025 的 GEAT 框架密钥长度公式(Eq. 16)+ Choi-state 单步 SDP(Eq. 79–80)+ 数值结果(Fig. 1, 3)+ 与前置方法的理论对比(Remark 3)+ coherent attack 可靠性(Theorem 5)
- 本 memo **不覆盖**:Appendix A 的 Theorem 4 完整证明(Legendre-Fenchel 对偶),Appendix B 的 squashing-based flag-state 扩展,Appendix C 的 Rényi-von Neumann 转换细节

---

## 1. 一句话总结

**Kamin 2025 给出了 prepare-and-measure QKD(含 decoy-state)的完整 GEAT 有限密钥安全证明 + 数值化实施路线**:通过把 [GLH+22] 的 EAT 分析改造为 GEAT(消除 Markov 条件 → 消除 test-round 通告的负向惩罚),加入 [LLR+21] 改进的 second-order 项,并把 decoy-state 的两步法(先算光子数 yield 上/下界,再对 single-photon 熵做 SDP)**合并为单步 Choi-state 凸优化**,实施于 BB84 qubit-with-loss + decoy-state BB84 两个例子,涵盖从 Rényi 散度到 Frank-Wolfe 实施的完整工具链。**硬验收**:BB84 qubit-with-loss(Fig. 1)+ decoy-state BB84(Fig. 3, 4)。

> **命名说明(Round 2 修订)**:Kamin 2025 用 "PM-QKD" 作为 *prepare-and-measure QKD* 的英文缩写,本项目在 F6 TF-QKD family 中用 "PM-QKD" 指 *phase-matching QKD*(Ma-Zeng-Zhou 2018)。**两者含义完全不同**。本 memo 之后统一改用 "**prepare-and-measure QKD**" 或 "**PM(准备-测量)**" 全称以避免与 F6 的 PM = phase-matching 混淆;引用 Kamin §/Table/Eq. 原文时按原文保留 "PM-QKD"。

---

## 2. 概念地图

```
            ┌─────────────────────────────────────────────────────────┐
            │    GEAT [MFS+22/MR23] (已见 docs/literature/GEAT-2024.md) │
            │    H_min^ε(A^n|E_n)|_Ω ≥ nh + n·T_α(f) - ...            │
            └─────────────────────────────────────────────────────────┘
                                      │
                ┌─────────────────────┼─────────────────────┐
                ▼                                           ▼
   ┌─────────────────────────┐              ┌─────────────────────────┐
   │ [GLH+22] EAT QKD 分析    │              │ [LLR+21] 改进 GEAT      │
   │ Markov 条件 → test-round │              │ second-order 项        │
   │ 通告导致 subtractive 惩罚 │              │ (本文采用此版本)        │
   │ (本文用 GEAT 避免)       │              │                         │
   └─────────────────────────┘              └─────────────────────────┘
                                      │
                                      ▼
            ┌─────────────────────────────────────────────────────────┐
            │    Kamin 2025 主贡献                                     │
            │    1. prepare-and-measure QKD 的 Choi-state 参数化         │
            │       (Eq. 30-31)                                        │
            │    2. 密钥长度 Theorem 3 (Eq. 16):                        │
            │       l ≤ nh + nT_α(f) - n((α-1)/(2-α))²K(α)            │
            │           - λ_EC - ⌈log(1/ε_EV)⌉ - (α/(α-1))log(1/ε_PA) │
            │           + 2                                            │
            │    3. Theorem 4 最优 min-tradeoff SDP(Eq. 49-51)         │
            │    4. Decoy-state 单步 convex optimization(Eq. 79-80)   │
            └─────────────────────────────────────────────────────────┘
                                      │
                ┌─────────────────────┼─────────────────────┐
                ▼                                           ▼
   ┌─────────────────────────┐              ┌─────────────────────────┐
   │ Fig. 1/2: qubit BB84    │              │ Fig. 3/4: decoy BB84    │
   │ p_hon^depol = 0.01      │              │ μ_sig=0.9, μ_2=2e-2,    │
   │ n ∈ {10^6, 10^8, 10^10, │              │ μ_3=1e-3, N_ph=10       │
   │       10^12}            │              │ θ_misalign=sin^-1(0.1)  │
   │ 25 dB @ n=10^10         │              │ 25 dB @ n=10^12         │
   └─────────────────────────┘              └─────────────────────────┘
```

---

## 3. 协议与符号(§2–3 精要)

### 3.1 通用 prepare-and-measure QKD 协议(Kamin Protocol 1,§3)

每轮:
1. **State preparation + transmission**:Alice 以概率 γ 选 test round(发 test-round 状态),否则选 generation round。她记录基底 + 信号态到 $X_i$,公共通告 $C_i^A$。
2. **Measurement**:Bob 用 POVM $\{M_k^B\}$ 测量,记录 $Y_i$,公共通告 $C_i^B$。
3. **Public announcement**:Alice/Bob 宣告 $C_i^A C_i^B$,联合计算 $C_i$(test round 时 $C_i$ 取 test 结果;generation round 时 $C_i = \perp$)。
4. **Sifting + key map**:Alice 基于 $X_i$ 和 $I_i = (C_i^A, C_i^B, \cdots)$ 做 sifting + key map,产出 $S_i$。

**Acceptance test**:对 $C_1^n$ 的频率分布 $\mathbf{F}^\text{obs}$,接受当且仅当 $\mathbf{F}^\text{obs} \in S_\text{acc}$。

**EC + EV + PA**:Alice 发送 $\lambda_\text{EC}$ 比特做纠错;Bob 验证 $\lceil \log(1/\varepsilon_\text{EV}) \rceil$ 比特哈希;最后用 2-universal 哈希把 $S_1^n$ 压缩为长度 $\ell$ 的最终密钥。

### 3.2 Composable 安全定义(§4, Def. 9)

- $\varepsilon^\text{secret}$-secret(Eq. 13):$\frac{1}{2}\Pr[\Omega_\text{acc}] \| \rho_{K_AE|\Omega_\text{acc}} - \mathbb{1}_{K_A}/|\mathcal{K}_A| \otimes \rho_{E|\Omega_\text{acc}} \|_1 \leq \varepsilon^\text{secret}$
- $\varepsilon^\text{correct}$-correct(Eq. 14):$\Pr[K_A \neq K_B \wedge \text{accept}] \leq \varepsilon^\text{correct}$
- $\varepsilon^\text{com}$-complete(Eq. 15):$\Pr[\text{abort}] \leq \varepsilon^\text{com}$(诚实行为下)
- $\varepsilon^\text{secure} = \varepsilon^\text{secret} + \varepsilon^\text{correct}$

---

## 4. 核心结果

### 4.1 GEAT channel 条件 + rate function(§4, Def. 6-8)

GEAT channel 序列 $\{\mathcal{M}_i\}_i$ 满足:
- **统计可重建**(Eq. 7):$\exists \mathcal{P}_{A^nE_n \to C^n A^n E_n}, \{\mathcal{N}_i\}$ 使得 $\mathcal{M}_n \circ \cdots \circ \mathcal{M}_1 = \mathcal{P} \circ \mathcal{N}_n \circ \cdots \circ \mathcal{N}_1$(投影形式)
- **Non-signalling**(同 Metger 2024):$\exists \mathcal{R}_i$ 使得 $\operatorname{Tr}_{A_iR_iC_i} \circ \mathcal{M}_i = \mathcal{R}_i \circ \operatorname{Tr}_{R_{i-1}}$

**Rate function**(Def. 7):$\text{rate}(\mathbf{p}) \leq \inf_\nu H(A_i|E_i R)_\nu$,其中 $\Sigma_i(\mathbf{p})$ 是 $\mathcal{M}_i$ 输出中 $C_i$ 边际为 $\mathbf{p}$ 的状态集。

**Min-tradeoff function**(Def. 8):$f(\mathbf{p}) = \mathbf{f} \cdot \mathbf{p} + k_f$ 是 affine rate function。

### 4.2 Theorem 1(GEAT with LLR+21 improvement, Eq. 10)

对 $\alpha \in (1, 3/2)$, $\varepsilon \in (0,1)$:

$$H_\alpha^\uparrow(A^n|E_n)_{\mathcal{M}_n\circ\cdots\circ\mathcal{M}_1(\rho)|\Omega} \geq nh + nT_\alpha(f) - \frac{\alpha}{\alpha-1}\log\frac{1}{\Pr[\Omega]} - n\left(\frac{\alpha-1}{2-\alpha}\right)^2 K(\alpha)$$

其中:
- $T_\alpha(f) := \inf_{\mathbf{p} \in \mathcal{Q}} \left(\text{rate}(\mathbf{p}) - f(\mathbf{p}) - \frac{\alpha-1}{2-\alpha}\cdot\frac{\ln 2}{2}V(\mathbf{p}, f)\right)$(Eq. 11)
- $V(\mathbf{p}, f) = (\log(1+2d_A^\kappa) + \sqrt{2+\text{Var}(\mathbf{p}, f)})^2$,$\kappa = 1$(经典 $A_i$)或 $2$(量子)
- $K(\alpha)$:与 Metger 2024 Cor 4.6 相同的复合项(含 max/min 差、维度、ln³ 项)
- $h = \min_{c^n \in \Omega} f(\text{freq}(c^n))$

### 4.3 Theorem 3(密钥长度, Eq. 16)

对 $\alpha \in (1, 3/2)$, $\varepsilon_\text{PA}, \varepsilon_\text{EV} \in (0, 1]$,Protocol 1 是 $\varepsilon_\text{PA}$-secret 且 $\varepsilon_\text{EV}$-correct,只要:

$$\boxed{\ell \leq nh + nT_\alpha(f) - n\left(\frac{\alpha-1}{2-\alpha}\right)^2 K(\alpha) - \lambda_\text{EC} - \left\lceil \log\frac{1}{\varepsilon_\text{EV}} \right\rceil - \frac{\alpha}{\alpha-1}\log\frac{1}{\varepsilon_\text{PA}} + 2}$$

**关键**:采用 Rényi privacy amplification [Dup23] 替代传统 smoothing 的优势 — 只出现单个 $\varepsilon_\text{PA}$ 项,结构上比 [GLH+22] 更简洁。

### 4.4 Completeness(§4.2, Eq. 22-25)

$\varepsilon^\text{com} = \varepsilon^\text{com}_\text{AT} + \varepsilon^\text{com}_\text{EV}$,其中 $\varepsilon^\text{com}_\text{AT}$(acceptance test)通过 binomial 尾概率 LP 控制(Eq. 25);$\varepsilon^\text{com}_\text{EV}$ 来自 EC 失败。**本文选 $\varepsilon^\text{com} = 10^{-3}$**。

**接受集形状**(Eq. 23):$S_\text{acc} = \{\mathbf{p}^\text{acc} \mid \forall c, p_c^\text{hon} - t_c^\text{low} \leq p_c^\text{acc} \leq p_c^\text{hon} + t_c^\text{upp}\}$ — "entrywise" 容忍区间。Unique-acceptance 是特例($t = 0$)。

### 4.5 Completeness penalty(§5.1, Eq. 40)

$h = \min_{c^n \in \Omega} f(\text{freq}(c^n)) = f(\mathbf{p}^\text{hon}) - \Delta_\text{com}$

其中 $\Delta_\text{com} := \sup_{\mathbf{p}^\text{acc} \in S_\text{acc}} -\mathbf{f} \cdot (\mathbf{p}^\text{acc} - \mathbf{p}^\text{hon})$ — LP 可解。

---

## 5. 数值实施技巧(§5,本文核心技术)

### 5.1 Rate function via Choi state(§4.3, Eq. 30-31)

把 Eve 的 channel $\mathcal{E}: A' \to B$ 参数化为 Choi state $J$:
- Test round:$\rho_J^t = \operatorname{Tr}_{A'}[(\mathbb{1}_A \otimes J)(|\xi^t\rangle\langle\xi^t|^{T_{A'}} \otimes \mathbb{1}_B)]$
- Generation round:$\rho_J^g$ 类似,用 $|\xi^g\rangle$

**Rate function 重写**(Eq. 30):
$$\text{rate}(\mathbf{p}) = \inf_J W(\rho_J^g) \quad \text{s.t.} \quad \gamma \Phi[\rho_J^t] = \mathbf{p}_{\backslash \perp}$$

$W(\rho) = D(\mathcal{G}(\rho) \| \mathcal{Z}(\mathcal{G}(\rho)))$ 是 WLC-2018 形式的相对熵。此参数化 → **凸优化**(Frank-Wolfe 可解)。

### 5.2 Crossover min-tradeoff function(§4.3, Eq. 33-35)

Infrequent-sampling channels(test prob γ 小) → 先对 test round 构造 crossover rate function:
$$r_\text{cross}(\mathbf{q}) = \inf_J W(\rho_J^g) \quad \text{s.t.} \quad \Phi[\rho_J^t] = \mathbf{q}$$

Crossover min-tradeoff $g$(affine 下界)通过 [DF19] 方法转换为 min-tradeoff $f$:
$$f(\delta_c) = \frac{1}{\gamma}g(\delta_c) + \left(1 - \frac{1}{\gamma}\right)\text{Max}(g), \quad f(\delta_\perp) = \text{Max}(g)$$

即 $\mathbf{f} = \frac{1}{\gamma}(\mathbf{g}, \text{Max}(\mathbf{g}))$(Eq. 37)。

### 5.3 Theorem 4(最优 min-tradeoff 的 SDP 构造, Eq. 49-51)

**关键定理**:最优 crossover min-tradeoff $\mathbf{g}^*$ 就是以下凸优化的 **dual variable**:

$$r_\text{best} = \sup_g (g(\mathbf{q}^\text{hon}) - \hat{T}(\mathbf{g}))$$

其中 $\hat{T}(\mathbf{g}) = \varphi_0 (\max(\mathbf{g}) - \min(\mathbf{g}))^2 + \varphi_1 (\max(\mathbf{g}) - \min(\mathbf{g}))$(Eq. 44)是 $T_\alpha$ 的 loose substitute。

通过 Legendre-Fenchel 对偶(Appendix A),等价于求解:

$$r_\text{SDP} = \inf_{J, \boldsymbol{\lambda}, \boldsymbol{\tau}} L(\rho_J^g, \boldsymbol{\tau}) \quad \text{s.t.} \quad \mathbf{q}^\text{hon} - \boldsymbol{\Phi}[\rho_J^t] - \boldsymbol{\lambda} = 0, \quad -\boldsymbol{\tau} \leq \boldsymbol{\lambda} \leq \boldsymbol{\tau}$$

最优 $\mathbf{g}^*$ 是上面 $\mathbf{q}^\text{hon} - \boldsymbol{\Phi}[\rho_J^t] - \boldsymbol{\lambda} = 0$ 约束的 **Lagrange 对偶乘子**。

**实用**:每次 Frank-Wolfe 迭代解一个 SDP,其 dual 自然给出当前最优 $\mathbf{g}$;算法终止时的 $\mathbf{g}^*$ 即最优 min-tradeoff。

### 5.4 Completeness-penalty LP(§5.2.2, Eq. 54-55)

对形如 Eq. 23 的 $S_\text{acc}$,$\Delta_\text{com}$ 简化为带约束的线性规划。本文给出 greedy 算法(Eq. 55 下段),比通用 LP 求解器更快,并与 CVX 结果一致验证。

### 5.5 Security parameter optimization(§5.2.3, Eq. 57)

最小化 $f_\alpha(\varepsilon^\text{secure}, \varepsilon_\text{PA}) = \frac{\alpha}{\alpha-1}\log(1/\varepsilon_\text{PA}) + \log(2/(\varepsilon^\text{secure}-\varepsilon_\text{PA}))$,得到最优:

$$\varepsilon_\text{PA} = \frac{\alpha}{2\alpha-1}\varepsilon^\text{secure}, \quad \varepsilon_\text{EV} = \frac{\alpha-1}{2\alpha-1}\varepsilon^\text{secure}$$

### 5.6 整体流程(§5.2.3 末段)

```
for each (γ, α) on grid:
    for each (t^low, t^upp):
        g = SDP_dual_variable(γ, α, t, t')   # §5.2.1 via Frank-Wolfe
        ℓ = key_length_formula(Eq.42/82, γ, α, t, t', g)  # with Δ_com
    maximize over (t^low, t^upp)              # completeness LP
maximize over (γ, α)                          # grid search
```

---

## 6. Qubit BB84 with loss(§6,Fig. 1/2 复现目标)

### 6.1 Protocol 模型(§6, Eq. 58)

- **Source**:perfect qubit source
- **Channel**:$\mathcal{E}_\text{depol}[\rho] = (1-p^\text{depol}_\text{hon})\rho + p^\text{depol}_\text{hon}\mathbb{1}/2$ + loss (probability $1 - 10^{-\zeta_\text{hon}/10\,\text{dB}}$ qubit 丢失)
- **Test**:$|+\rangle, |-\rangle$(X-basis)
- **Generation**:$|0\rangle, |1\rangle$(Z-basis)
- **Sifting**:generation round × Bob in Z × detection

### 6.2 G-map / Z-map(§6, Eq. 63-64)

- $K_Z$ Kraus(单个):
$$K_Z = \left[\binom{1}{0}_S \otimes \begin{pmatrix}1&0\\0&0\end{pmatrix}_A + \binom{0}{1}_S \otimes \begin{pmatrix}0&0\\0&1\end{pmatrix}_A\right] \otimes \binom{1}{0}_B \otimes \mathbb{1}_I$$
- $\mathcal{Z}$ Kraus:$Z_1 = \binom{1}{0} \otimes \mathbb{1}$, $Z_2 = \binom{0}{1} \otimes \mathbb{1}$

$W(\rho_J^g) = (1-\gamma)^2 D(\mathcal{G}(\rho_J^g) \| \mathcal{Z}\circ\mathcal{G}(\rho_J^g))$ 是 WLC 形式。

### 6.3 数值结果(Fig. 1)

| $n$ | cutoff loss (GEAT) | cutoff loss (IID [KTL25]) |
|-----|--------------------|---------------------------|
| $10^6$ | ≈ 15 dB | ≈ 15 dB |
| $10^8$ | ≈ 20 dB | ≈ 25 dB |
| $10^{10}$ | ≈ 25 dB | ≈ 35 dB |
| $10^{12}$ | ≈ 26 dB | ≈ 36 dB |

**观察**:
- 低损耗下 GEAT ≈ IID(对 coherent attack 无明显惩罚)
- 高损耗下 GEAT 下降更快(对 coherent attack 的保守性显现)
- $n = 10^{12}$ 下 0 dB 密钥率 ≈ 0.9(接近 asymptotic)

**Fig. 2 (unique vs realistic acceptance)**:realistic 损失很小(~5 dB cutoff 左右);**EUR (complementarity-based) 略好**,说明对 qubit BB84 EUR 方法竞争力强。

---

## 7. Decoy-state BB84(§7,Fig. 3/4)

### 7.1 Protocol 扩展(§7.1)

- WCP 源,intensities $\{\mu_\text{sig}, \mu_2, \mu_3\}$
- 偏振编码 $\{\rho_H, \rho_V, \rho_D, \rho_A\}$
- Test round:X 基,随机 intensity $\mu_i \in \{\mu_\text{sig}, \mu_2, \mu_3\}$;Generation round:Z 基,$\mu_\text{sig}$
- Active BB84 detection + [BML08, GBN+14] post-processing
- Misalignment model from [WL22]:$\theta_\text{hon}^\text{misalign}$

### 7.2 块对角 Choi state 分解(§7.2, Eq. 71-78)

- Eve 做 QND 光子数测量 ⇒ Choi state $J = \bigoplus_n J_n$
- n-photon yields:$Y_n^{ab} = \boldsymbol{\Phi}_{ab}[\rho_{J_n}^{t,\mu}]$(与 intensity μ 无关,因为 Eve 对 n 选择 attack,独立 μ)
- 引入光子数 cut-off $N_\text{ph}$ 处理无穷和

### 7.3 单步 SDP(Theorem 4 decoy 版, Eq. 80)

$$r_\text{best} = \inf_{J_1, \mathbf{Y}_0, \cdots, \mathbf{Y}_{N_\text{ph}}, \boldsymbol{\delta}^\mu, \boldsymbol{\tau}^\mu} p(1) W(\rho_{J_1}^g) + s(\cdot)$$

s.t. (Eq. 80 约束组):
- $-\boldsymbol{\tau}^\mu \leq \mathbf{q}^\mu - p(\mu|t)(\sum_{n \leq N_\text{ph}} p_\mu(n)\mathbf{Y}_n + \boldsymbol{\delta}^\mu) \leq \boldsymbol{\tau}^\mu$
- $0 \leq \boldsymbol{\delta}^\mu \leq 1 - p_\text{tot}(\mu)$
- $p(\mu|t)\mathbf{Y}_1 = p(\mu|t)\boldsymbol{\Phi}[\rho_{J_1}^{t,\mu}]$
- $\sum_b Y_n^{ab} = p(a|t, n)$

**Remark 3**:此单步 convex optimization 在数学上严格优于 [WL22, NUL23, KL24, KTL25] 的两步法(在渐近/IID 场景),因为它不允许"Eve 同时对所有 yields 取 worst case"的非物理可行点。

### 7.4 数值结果(Fig. 3/4)

**参数**:$\mu_\text{sig} = 0.9$, $\mu_2 = 2 \times 10^{-2}$, $\mu_3 = 10^{-3}$, $\theta^\text{misalign} = \sin^{-1}(0.1)$, $N_\text{ph} = 10$, $\varepsilon^\text{secure} = 10^{-8}$, $\varepsilon^\text{com} = 10^{-3}$.

| $n$ | cutoff loss (GEAT) | cutoff loss (IID) |
|-----|--------------------|--------------------|
| $10^7$ | ≈ 5 dB | ≈ 10 dB |
| $10^8$ | ≈ 10 dB | ≈ 15 dB |
| $10^{10}$ | ≈ 20 dB | ≈ 30 dB |
| $10^{12}$ | ≈ 25 dB | ≈ 38 dB |

**Fig. 4 (unique vs realistic acceptance, decoy)**:realistic 惩罚比 qubit case 大得多,尤其高损耗区 → **实际协议需要可忍受的 acceptance set**。

**Fig. 4 下 (GEAT vs EUR)**:**低损耗 GEAT 好,高损耗 EUR 好**;说明对 decoy-state 两种方法各有优势。

---

## 8. Coherent attack 扩展(§8, Theorem 5)

原 [MR23] 要求"Eve 每轮只与单个信号交互"。[FKR+25, AT25] 证明此条件可移除 — 即 **本文的 GEAT 密钥率对任意 coherent attack(Eve 可同时持有所有信号)仍然成立**。

**Theorem 5**(本文 Eq. 85):对任意 source-replaced state $\mathcal{M}^{\otimes n}(\rho_{A_1^n B_1^n E})$,GEAT 界 Eq. 10 同样成立,无需 single-signal 交互限制。

**Remark**:[FKR+25, AT25] 还给出基于 Rényi 熵的 sharper bounds,未来工作可合并。

---

## 9. 与本项目的 Bearing

### 9.1 与 RESEARCH_PLAN §3.3 S2.5 的对齐

| Plan 要求 | 本文覆盖 | 备注 |
|----------|---------|------|
| 对 decoy-state BB84 finite-key rate 误差 < 5% | ✓ Fig. 3 提供 benchmark | Fig. 4 上图 realistic acceptance 是实用验收目标 |
| `qkdx/finite_key/` 模块 | 本文 §5 提供实施蓝图 | Choi-state SDP + FW + Theorem 4 dual |
| `notebooks/s2_kamin_reproduce.ipynb` | 待实施 | Fig. 1 qubit BB84 可作为简化起点 |
| Kamin 2025 Table 1 对比 | **注意**:Kamin 2025 的 Table 1 是符号表(notation, p.5),**不是** RESEARCH_PLAN §3.3 S2.5 隐指的 benchmark 表 | Plan 引用错位;本 memo 把 **Fig. 3**(decoy 有限密钥数值)作为 decoy 硬验收的实用 target |

### 9.2 实施路径建议(三阶段)

**Stage 1(1 周,低风险):qubit BB84 (Fig. 1) asymptotic sanity**
- 复现 $n = 10^{12}$ 下 0–5 dB 密钥率(应 ≈ asymptotic Devetak-Winter,即 $(1-\gamma)^2(1-2h(e))$ at low loss)
- **不需要 SDP**;只需 analytic entropy 形式 + optimized γ, α grid search
- 验收:0 dB @ $p^\text{depol} = 0.01$ asymptotic rate $\approx 0.91 \cdot (1-\gamma)^2$ matches plot

**Stage 2(3–4 周,中风险):qubit BB84 (Fig. 1) full GEAT**
- 实施 Theorem 3 密钥长度公式(Eq. 16)
- 实施 Frank-Wolfe + SDP(CVXPY + MOSEK)求 min-tradeoff $\mathbf{g}$
- 实施 Theorem 4 dual extraction
- 验收:Fig. 1 四条 $n$ 曲线对 loss 关键点 < 5% 误差

**Stage 3(6–8 周,高风险):decoy-state BB84 (Fig. 3, 4)**
- 扩展单步 convex optimization(Eq. 80):photon-number 块对角 + yield 约束
- Cut-off $N_\text{ph} = 10$ ⇒ 11 个 yield 向量 + $\boldsymbol{\delta}^\mu$
- 验收:Fig. 3 四条 $n$ 曲线 < 5% 误差

### 9.3 ADR-B 决策落实

**推荐**:Phase 1 S2.5 采用 **Stage 1 + Stage 2 缩减版** 作为**硬验收 proxy**;Stage 3 decoy 留到 Phase 2 Sub-Q3 与上界对比时合并实施(因为 Sub-Q3 PLOB 对比也需要 decoy finite-key rate)。

**理由**:
- Stage 1/2 验证 GEAT 工具链核心(Theorem 3 + Choi SDP + Theorem 4 dual)
- Stage 3 引入 decoy 特有的 photon-number 块对角,复杂度 + 时间成本显著更高
- RESEARCH_PLAN §3.3 S2.5 验收"BB84"未明确 qubit vs decoy — qubit Fig. 1 亦可作为有效硬验收,decoy 作 stretch goal
- 与 GLL-2021 analytic 对接:Stage 1 的 asymptotic 极限应 ≈ GLL-2021 BB84 公式,形成 cross-validation anchor

---

## 10. Limitations(论文明示 + 项目视角)

### 论文明示(§8 Conclusion + Fig. 2/4 lower panels)

- **对 complementarity-based 技术(EUR)的比较未完整**:§1 "We emphasize that the scope of our above claims is restricted to the specifically mentioned works ... claims do not encompass complementarity-based proof techniques"。Fig. 2/4 下图对 qubit BB84 EUR 更好;decoy 下 EUR 在高损耗好。
- **Photon cut-off $N_\text{ph}$ 引入松弛**:Eq. 78 的 $\boldsymbol{\delta}^\mu$ 是上界,非物理 Choi state;原则上 $N_\text{ph} \to \infty$ 恢复严格,但数值成本高
- **Fig. 4 realistic acceptance 的 cutoff 损失**:比 unique acceptance 差很多,实际实现需要"adaptive key rate formulations"(如 [TTL24, HB25])
- **Passive detection setup 需要 flag-state squasher**(Appendix B Theorem 6),本文只做 active detection

### 项目视角

- **MATLAB/CVX+MOSEK 实施**:本文代码仓库为 MATLAB,移植到 Python(CVXPY)有工作量
- **Frank-Wolfe improved variant [LJ15]**:论文用了改进的 FW(避免 zigzagging),实施时需注意这个 detail
- **Asymptotic limit 验证**:论文未明确给出 Stage 1 asymptotic expected value,需自己推导 $(1-\gamma)^2 (1 - h(p^\text{depol}/2) - h(p^\text{depol}/2))$ 作为 anchor
- **γ, α optimization grid**:论文"optimized for each data point"但未公开具体值 ⇒ 复现时需要 grid search
- **[LLR+21] Supplement Theorem 2 细节**:本文只引用,未完整复述 → 若对 $K(\alpha)$ 系数存疑需查原文

---

## 11. 下一级 Level 4 升级需求(若后续回来精读)

- **Appendix A 完整**:Legendre-Fenchel 对偶推导(Eq. 46 $\hat{T}^*(\boldsymbol{\lambda}) = s(\|\boldsymbol{\lambda}\|_1 / 2)$ 证明)+ Theorem 4 完整证明 + Eq. 95-96 sign convention
- **Appendix B**:Flag-state squasher + Theorem 6 for passive detection — 若 decoy-state 实施中用 passive detection(常见实验设定)必读
- **Appendix C**:Rényi-von Neumann 转换 + [FKR+25, AT25] 的 sharper bounds 合并技术
- **[DF19] Lemma V.5**:$\hat{T}(\mathbf{g})$ 推导的关键引理
- **[LLR+21] Supplement Theorem 2**:改进 $K(\alpha)$ second-order 项的完整证明

---

## 12. 与 GEAT-2024 (Metger) 精读 memo 的关系

两份 memo **互补**:
- `GEAT-2024.md`:GEAT 定理本体(Thm 4.1/4.3, Cor 4.6, Lemma 4.7)的数学层 + E91 概念示例
- `Kamin-2025.md`(本文):GEAT 应用到 prepare-and-measure QKD + decoy-state + **数值实施完整 pipeline**

Kamin 2025 **依赖** Metger 2024 的 Thm 4.3 / Cor 4.6,并添加 [LLR+21] 改进 second-order;阅读顺序 GEAT-2024 → Kamin-2025 是合理的。

---

## 13. 变更日志

- **v0.1** (2026-04-20):首稿 Level 3–4 精读。基于 PDF 全文 §1-§8 精读(§5, §6 完整;§7 Level 3;§4.3 complete);Appendices 浏览。配合 Phase 1 S2.5 实施路径决策 + ADR-B 落实。
