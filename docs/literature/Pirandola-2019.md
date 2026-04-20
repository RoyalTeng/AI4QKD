# Pirandola 2019 End-to-End Capacities 精读(Level 4)

**论文引用**:
- Pirandola, S. (2019). *End-to-end capacities of a quantum communication network.*
  Communications Physics **2**:51.  arXiv:1905.12674v1(29 May 2019).
- 本 memo 基于 PDF(`docs/literature/pdfs/Pirandola-2019-EndToEndCapacities.pdf`, 1.0 MB, 8 pp.)
- **主要前置**:
  - [PLOB17] Pirandola-Laurenza-Ottaviani-Banchi 2017 **基础**(已精读:`docs/literature/PLOB-2017.md`)
  - [PLOB17 SI] Supplementary Note 3(3 种等价证明)
  - [Ref 16] Pirandola "Bounds for private communication"(Theorem 2 chain-form)

**精读日期**:2026-04-20(Phase 2 Sub-Q3 前置 — TF-QKD 拓扑的正确上界)
**精读等级**:**Level 4**
- §Abstract + Introduction:完整
- §Results(§Ultimate limits of repeater chains / §Lossy chains / §Networks single-path / §Networks multi-path / §Formulas for distillable chains and networks):完整
- §Discussion:完整
- §Methods(General weak converse / Network simulation):完整
- Supplementary Notes 1-6:浏览(未重推所有证明细节)

**范围说明**:
- 覆盖:Pirandola 2019 所有核心结果(repeater chain, network cuts, distillable channels 闭式)
- 不覆盖:SI Note 2-3(truncation tools / weak converse 3 种证明),SI Note 5-6(multi-path max-flow 完整推导)— 需要 Level 5 时补

---

## 1. 一句话总结

**Pirandola 2019 把 PLOB 的 point-to-point REE 上界推广到 arbitrary quantum networks with N 个 repeaters**,使用 "network teleportation stretching + entanglement cut" 技术,对 distillable channels 给出 single-letter 闭合公式;对本项目最重要的结果是**单 repeater lossy chain 的 two-way 容量 $\mathcal{C} = -\log_2(1 - \sqrt{\eta})$(Eq. 9 at N=1)— 这正是 TF-QKD / PM-QKD 拓扑的正确上界**(区别于 PLOB direct-link $-\log_2(1-\eta)$);Ma §VI 指的 "still far from single-repeater bound" 就是它。

---

## 2. 概念地图

```
              ┌─────────────────────────────────────────────────────┐
              │    PLOB 2017 (point-to-point)                       │
              │    C(E) ≤ E_R(ρ_E)  via teleportation stretching    │
              │    lossy channel: C(η) = -log_2(1 - η)              │
              └─────────────────────────────────────────────────────┘
                                   │
                                   │ extend via network stretching
                                   ▼
              ┌─────────────────────────────────────────────────────┐
              │    Repeater chain {E_i}_{i=0..N}                    │
              │    Alice — r_1 — r_2 — ... — r_N — Bob              │
              │    entanglement cut "i" disconnects E_i              │
              │    C({E_i}) ≤ min_i E_R(σ_i)      (Eq. 1)            │
              │    For distillable: C({E_i}) = min_i E_R(ρ_{E_i})   │
              └─────────────────────────────────────────────────────┘
                                   │
                                   │ Lossy chain specialization
                                   ▼
              ┌─────────────────────────────────────────────────────┐
              │    C_loss(η, N) = -log_2(1 - η^{1/(N+1)})           │
              │                                          (Eq. 9)    │
              │                                                     │
              │    N = 0 (no repeater)  → PLOB: -log_2(1 - η)       │
              │    N = 1 (single relay) → -log_2(1 - √η)            │
              │                           ⇔ TF-QKD / PM-QKD benchmark│
              │    N → ∞                → ∞/no loss                 │
              └─────────────────────────────────────────────────────┘
                                   │
                                   │ further extend to networks
                                   ▼
              ┌─────────────────────────────────────────────────────┐
              │    Quantum network N = (P, E) undirected graph      │
              │    Entanglement cut C → cut-set C̃ ⊆ E               │
              │                                                     │
              │    Single-path (sequential, one route ω at a time): │
              │      C(N) ≤ min_C max_{(x,y)∈C̃} E_R(σ_xy) = min_C E_R(C)│
              │    Multi-path (flooding, all edges simultaneously): │
              │      C^m(N) ≤ min_C Σ_{(x,y)∈C̃} E_R(σ_xy)           │
              │                                                     │
              │    For distillable networks: upper = lower          │
              │      Single-path: C(N) = -log_2(1 - η_N)            │
              │                   (η_N = widest path transmissivity)│
              │      Multi-path: C^m(N) = -log_2 L_N                │
              │                  (L_N = max cut loss)               │
              └─────────────────────────────────────────────────────┘
```

---

## 3. 主要结果

### 3.1 Repeater chain 容量(Eq. 1 one-shot + Eq. 4-7 tightened)

**设定**:Alice $= \mathbf{r}_0$,$\mathbf{r}_1, \ldots, \mathbf{r}_N$ 为 repeaters,Bob $= \mathbf{r}_{N+1}$;共 $N+1$ 个 channel $\mathcal{E}_i: \mathbf{r}_i \to \mathbf{r}_{i+1}$ for $i = 0, \ldots, N$.

**General weak converse(Eq. 1)**:对任意 entanglement cut $i$(断开 $\mathcal{E}_i$ 的 edge),
$$\mathcal{C}(\{\mathcal{E}_i\}) \leq E_R(\sigma_i)$$
其中 $\sigma_i$ 是 $\mathcal{E}_i$ 的 resource state(任何 σ-stretchable 的 σ)。

**关键 single-letter reduction(Eq. 4)**:通过 minimize over cuts,
$$\mathcal{C}(\{\mathcal{E}_i\}) \leq \min_i E_R(\sigma_i)$$

**Teleportation-covariant chains(Eq. 5)**:$\sigma_i = \rho_{\mathcal{E}_i}$(Choi matrix),
$$\mathcal{C}(\{\mathcal{E}_i\}) \leq \min_i E_R(\rho_{\mathcal{E}_i})$$

**Distillable chains(Eq. 7)**:exact capacity
$$\mathcal{C}(\{\mathcal{E}_i\}) = \min_i \mathcal{C}(\mathcal{E}_i) = \min_i E_R(\rho_{\mathcal{E}_i})$$

**物理意义**:**最弱 link 决定整个链的容量**(weakest-link 原理)。与经典网络信道容量直觉一致,但这里是量子版本。

### 3.2 Lossy repeater chain(Eq. 8-9 — **本项目核心结果**)

**等距 $N+1$ 链**($N$ 个 equispaced repeaters,每段 transmissivity $\eta_\text{link} = \eta^{1/(N+1)}$):

$$\boxed{\mathcal{C}_\text{loss}(\eta, N) = -\log_2(1 - \eta^{1/(N+1)})}$$

**特例**:
- **$N = 0$ (no repeater)**:$\mathcal{C}_\text{loss}(\eta, 0) = -\log_2(1 - \eta)$ ← PLOB 直接重现
- **$N = 1$ (single repeater)**:$\mathcal{C}_\text{loss}(\eta, 1) = -\log_2(1 - \sqrt{\eta})$ ← **TF-QKD / PM-QKD 的正确上界**
- **$N = 10$**:$-\log_2(1 - \eta^{1/11})$ ≈ 2× 跟 $N=1$ 比不多收益(Fig. 2 "(10)" 曲线)
- **$N = 100$**:$-\log_2(1 - \eta^{1/101})$ 已经很接近 no-loss(Fig. 2 "(100)")

**高损耗 $\eta \ll 1$ 近似**:
$$\mathcal{C}_\text{loss}(\eta, N) \approx \frac{\eta^{1/(N+1)}}{\ln 2}$$

**对 $N = 1$**:$\mathcal{C}_\text{loss} \approx \sqrt{\eta}/\ln 2 \approx 1.44\sqrt{\eta}$ — **这就是 Ma-Zeng-Zhou §VI outlook 所说的 "single-repeater bound,$-\log_2(1-\sqrt{\eta})$"**.

**"3 dB rule"**(§Lossy chains 末段):If we want to guarantee ≥ 1 target bit/chain use, we can tolerate at most 3 dB of loss in each individual link.

### 3.3 量子网络单路径容量(Eq. 10-14)

**网络结构**:undirected graph $\mathcal{N} = (P, E)$,每条边 $(\mathbf{x}, \mathbf{y}) \in E$ 带信道 $\mathcal{E}_{\mathbf{x}\mathbf{y}}$.

**Entanglement cut $C$ of $P$**:将 $P$ 分成两组 $(\mathbf{A}, \mathbf{B})$,$\mathbf{a} \in \mathbf{A}, \mathbf{b} \in \mathbf{B}$.$\tilde{C}$ = cut-set = 横跨 cut 的 edges.

**Single-edge flow of REE across cut $C$**(Eq. 10):
$$E_R(C) := \max_{(\mathbf{x}, \mathbf{y}) \in \tilde{C}} E_R(\sigma_{\mathbf{xy}})$$

**Single-path upper bound(Eq. 11)**:
$$\mathcal{C}(\mathcal{N}) \leq \min_C E_R(C)$$

**Distillable networks(Eq. 12-14)**:
$$\mathcal{C}(\mathcal{N}) = \max_\omega \mathcal{C}(\omega) = \min_C \mathcal{C}(C) = \min_C E_R(C)$$

**算法**:找 optimal route $\omega_*$ = **widest path problem**,Dijkstra-modified 算法 $O(|E| \log_2 |P|)$ 时间。

**Lossy network specialization(Eq. 15)**:
$$\mathcal{C}(\mathcal{N}_\text{loss}) = -\log_2(1 - \eta_\mathcal{N})$$
其中 $\eta_\mathcal{N} = \max_\omega \eta_\omega$ 是**最佳路由 total transmissivity**(经 widest path 算法求得)。

### 3.4 量子网络多路径容量(Eq. 16-21)

**Multi-path routing (flooding)**:同时 use 所有 edges 一次,多点通信 + 网络 LOCC.

**Multi-edge flow of REE across cut $C$**(Eq. 16):
$$E_R^m(C) := \sum_{(\mathbf{x}, \mathbf{y}) \in \tilde{C}} E_R(\sigma_{\mathbf{xy}})$$
注意 **sum**,不是 max.

**Multi-path upper bound(Eq. 17)**:
$$\mathcal{C}^m(\mathcal{N}) \leq \min_C E_R^m(C)$$

**Distillable multi-path(Eq. 19)**:
$$\mathcal{C}^m(\mathcal{N}) = \min_C \mathcal{C}^m(C) = \min_C E_R^m(C)$$

**算法**:**max-flow min-cut 问题**,Orlin 算法 $O(|P| \cdot |E|)$ 时间.

**Lossy multi-path(Eq. 20)**:
$$\mathcal{C}^m(\mathcal{N}_\text{loss}) = -\log_2 L_\mathcal{N}$$
其中 $L_\mathcal{N} = \max_C \prod_{(x,y) \in \tilde{C}} (1 - \eta_{xy})$ = max cut total loss.

**Diamond network example(Eq. 21)**:对四点菱形 $\mathcal{N}^\diamond_\text{loss}$ with 每 edge transmissivity $\eta$,
$$\mathcal{C}^m(\mathcal{N}^\diamond_\text{loss}) = 2 \mathcal{C}(\mathcal{N}^\diamond_\text{loss}) = -2\log_2(1 - \eta)$$
parallel = 2× sequential(因为 cut-set 有 2 条 edge 可并发)。

### 3.5 Distillable channels 完整公式表(Table I)

| 信道 | Chain $\mathcal{C}(\{\mathcal{E}_i\})$ | Network single-path $\mathcal{C}(\mathcal{N})$ | Network multi-path $\mathcal{C}^m(\mathcal{N})$ |
|------|---------------------------------------|------------------------------------------------|----------------------------------------------|
| Lossy (η) | $-\log_2(1 - \min_i \eta_i)$ | $-\log_2(1 - \eta_\mathcal{N})$ | $-\log_2 L_\mathcal{N}$ |
| QL amplifier (g) | $-\log_2[1 - (\max_i g_i)^{-1}]$ | $-\log_2(1 - g_\mathcal{N}^{-1})$ | $-\log_2 G_\mathcal{N}$ |
| Dephasing (p) | $1 - H_2(\max_i p_i)$ | $1 - H_2(p_\mathcal{N})$ | $\min_C \sum_{(x,y) \in \tilde{C}} [1 - H_2(p_{xy})]$ |
| Erasure (p) | $1 - \max_i p_i$ | $1 - p_\mathcal{N}$ | $\min_C \sum_{(x,y) \in \tilde{C}} (1 - p_{xy})$ |

其中(Eq. 26-30):
- $\eta_\mathcal{N} = \min_\omega \min_{i \in \omega} \eta_i^\omega$(widest path transmissivity)
- $g_\mathcal{N} = \min_\omega \max_{i \in \omega} g_i^\omega$
- $p_\mathcal{N}$ 类似
- $L_\mathcal{N} = \max_C \prod_{\tilde{C}}(1 - \eta_{xy})$
- $G_\mathcal{N} = \max_C \prod_{\tilde{C}}(1 - g_{xy}^{-1})$

---

## 4. 技术路径(§Methods)

### 4.1 General weak converse(§Methods)

证明 strategy(Eq. 35-41):
1. 任何 protocol $\mathcal{P}$ 输出 $\rho_{\mathbf{ab}}^n$ ε-close 到 target state $\phi^n$,$\phi^n$ 有 $n R_n^\varepsilon$ secret bits
2. 取 entanglement measure $E_M$:满足 (i) $E_M(\phi^n) \geq n R_n^\varepsilon$(normalization);(ii) continuity $|E_M(\rho) - E_M(\sigma)| \leq g(\varepsilon) \log d + h(\varepsilon)$;(iii) LOCC monotonicity;(iv) sub-additivity $E_M(\rho^{\otimes n}) \leq n E_M(\rho)$
3. REE 和 Squashed Entanglement 都满足以上
4. 推出 $R_n^\varepsilon \leq E_M(\rho_{\mathbf{ab}}^n)/n + \text{corrections} \to E_M(\rho_{\mathbf{ab}}^n)/n$ 取极限
5. 取 sup over protocols:$E_M^\star(\mathcal{N}) := \sup_\mathcal{P} \lim_n E_M(\rho_{\mathbf{ab}}^n)/n$(Eq. 41)

### 4.2 Network simulation(§Methods)

- 每个 edge $\mathcal{E}_{\mathbf{xy}}$ 用 resource state $\sigma_{\mathbf{xy}}$ simulate: $\mathcal{E}_{\mathbf{xy}}(\rho) = \mathcal{T}_{\mathbf{xy}}(\rho \otimes \sigma_{\mathbf{xy}})$
- 对 tele-covariant 信道:$\sigma_{\mathbf{xy}} = \rho_{\mathcal{E}_{\mathbf{xy}}}$(Choi matrix)
- Bosonic:asymptotic $\sigma_{\mathbf{xy}}^\mu$,$\mu \to \infty$
- Energy-constrained diamond distance(Eq. 42):$\|\mathcal{E}_{\mathbf{xy}} - \mathcal{E}_{\mathbf{xy}}^\mu\|_{\diamond \bar{N}} \to 0$

### 4.3 Cut-minimization for upper bound

对 network $\mathcal{N}$ 的任意 entanglement cut $C$:
1. Stretching: $\rho_{\mathbf{ab}}^n = \bar{\Lambda}_C(\sigma_C^{\otimes n})$,其中 $\sigma_C$ 是 cut-set 上 edges 的 joint resource state
2. REE 的 LOCC monotonicity + sub-additivity:
   $$E_R(\rho_{\mathbf{ab}}^n)/n \leq E_R(\sigma_C)$$
3. Single-path (one edge used at a time per cut):$E_R(\sigma_C) = \max_{\tilde{C}} E_R(\sigma_{\mathbf{xy}})$
4. Multi-path (all edges used at once):$E_R(\sigma_C) = \sum_{\tilde{C}} E_R(\sigma_{\mathbf{xy}})$
5. Min over cuts → Eq. 11 / Eq. 17

### 4.4 Lower bound via classical algorithms

- **Single-path**:widest path problem — 找 route $\omega_*$ maximizing $\mathcal{C}(\omega_*) = \min_i \mathcal{C}(\mathcal{E}_i^{\omega_*})$;Dijkstra-modified
- **Multi-path**:max-flow min-cut — 找 flow saturating all cuts;Orlin 算法
- 对 distillable network,lower bound = upper bound ⇒ exact capacity

---

## 5. 对本项目的 Bearing — Sub-Q3 核心

### 5.1 TF-QKD / PM-QKD 拓扑的正确上界(**关键修正**)

根据本 memo 分析,PLOB 2017 的 $-\log_2(1-\eta)$ 对 **TF 族不直接适用**(点对点,无中间节点),正确的上界来自 Pirandola 2019 Eq. 9 at $N = 1$:

$$\boxed{\mathcal{C}_\text{loss}(\eta, N=1) = -\log_2(1 - \sqrt{\eta})}$$

其中 $\eta = \eta_{AB}$ 是 Alice-Bob 总 transmittance。

**数值对比**($\eta = 10^{-2}$ @ 100 km):
- PLOB direct:$-\log_2(1 - 10^{-2}) \approx 0.0145$ bit/use
- Single-repeater (N=1):$-\log_2(1 - 0.1) \approx 0.152$ bit/use(10× 更宽松)
- PM-QKD 实测 (Ma Fig. 3a):$\sim 10^{-3}$ bit/use(150× 低于 single-repeater bound)

**Sub-Q3 gap 量化**(Ma §VI 所说 "still far away"):
- 在 100-200 km 距离:PM-QKD vs $-\log_2(1-\sqrt\eta)$ gap ~100-200×(orders)
- 在 300+ km:gap 收敛(两者都 ~10⁻⁶ 量级)

### 5.2 Charlie = untrusted repeater(topology 关键注解)

Pirandola 2019 §Discussion 明示:
> "These upper bounds are very general and also apply to chains and networks with untrusted nodes (i.e., run by an eavesdropper)"

所以 **$-\log_2(1-\sqrt{\eta})$ 对 TF-QKD(Charlie untrusted)仍然成立** — untrusted relay 只能让 rate 更差,不能超过 trusted-repeater 上界。

**逻辑**:PM-QKD / TF-QKD 属于 N=1 repeater chain with **untrusted** relay 场景。Pirandola 2019 给出的 $-\log_2(1-\sqrt\eta)$ 是**ultimate**(允许 trusted repeater + 任意 LOCC)bound。TF-QKD 不能做更好 — gap 表明 TF 协议本身有优化空间,或者 untrusted-relay 带来真实的 fundamental penalty(后者是 Sub-Q4 归因 A 的重要判据)。

### 5.3 Sub-Q3 拓扑适用性 lemma(§4.3 硬要求)

**本 memo 的核心结论**:
1. BB84 decoy / MDI direct-link:上界 $-\log_2(1-\eta)$(PLOB)
2. TF-QKD / PM-QKD relay topology(N=1):上界 $-\log_2(1-\sqrt\eta)$(Pirandola Eq. 9 at N=1)
3. 两者用法取决于协议的 **MS-EB formulation 中的 $\mathcal{E}$ 结构**:
   - $\mathcal{E}$ 是 Alice→Bob 单信道 → PLOB
   - $\mathcal{E}$ 分解为 Alice→Charlie 和 Bob→Charlie 两段 → Pirandola N=1
4. **拓扑适用性 lemma 形式化**(留 Sub-Q3 §4.3 实施):映射 MS-EB $\mathcal{E}$ 的 structural type 到 Pirandola 2019 的 network class(chain / single-path network / multi-path)

### 5.4 Sub-Q4 gap 归因指导

以 Pirandola 2019 上界为基准,Sub-Q4 A/B/C 归因变得清晰:

- **A (上界松)**:对 distillable channels (lossy / amplifier / dephasing / erasure),Pirandola 上界 = 下界 exact;故在这些信道上 A 归因**可排除**。对 bosonic thermal-loss 和 amplitude damping 仍有 gap(前者 Eq. 23 Eq. 25 gap,后者需要 squashed bound)。
- **B (下界松)**:PM-QKD 下界距 Pirandola 上界 ~100×(低损耗)— 需要 μ 优化 + 更紧的 E^X UB + 更好的协议(如 SNS 降低 misalignment penalty)
- **C (拓扑约束)**:N=1 vs N=10 在 Pirandola Fig. 2 差别巨大;相对无 repeater(N=0),N=1 (TF-QKD) 已经是 √η 等级的 "免费" 收益。TF-QKD 是当前现实可行最佳 topology。

### 5.5 对 Phase 2 的实施建议

1. **优先验证**(Week 1):数值计算 $-\log_2(1-\sqrt\eta)$ vs Ma Fig. 3a PM-QKD rate @ L=100 / 200 / 300 / 400 km,建 Pareto gap 表
2. **拓扑适用性 lemma**(Week 2):MS-EB formulation → Pirandola network class 的 mapping;记录在 `docs/msen/topology_applicability.md`
3. **Sub-Q3 §4.3 memo**(Week 3):结合 PLOB + Pirandola 2019 给出 direct-link vs relay 上界的 full 数值对照,作为 Sub-Q4 gap 起点
4. **上界 SDP 工具链**(§4.4,可选):实现 $E_R$ 数值计算(REE optimization over separable states)— 只在 distillable class 之外(non-lossy Gaussian)才必需

---

## 6. Limitations(论文明示 + 本 memo 视角)

### 论文明示

- **Distillable 限制**:网络容量闭式要求所有 edge channel 都是 distillable(lossy / amplifier / dephasing / erasure)。Non-Gaussian non-Pauli 网络仍有 gap
- **Network model**:undirected + sequential / flooding routing;不涵盖 adaptive quantum routing(wrt protocol feedback)
- **Asymptotic**:Bosonic networks 的 teleportation stretching 仍是 $\mu \to \infty$ 极限
- **Multi-point communications**:Sec. 多路径限制为 single-sender-multiple-receiver(flooding),不含 multi-sender 扩展

### 本 memo 读者(本项目)

- **TF-QKD Charlie 的"untrusted-relay" 语义**:Pirandola 框架下是 "eavesdropper-run node",但 TF-QKD 协议本身(Ma-Zeng-Zhou)假设 Charlie 的公告对 security 不必 honest;两者 coincident 但推理路径不完全相同。**Sub-Q3 需要验证语义映射精确性**
- **Pirandola Fig. 2**:repeater chain N=1/2/10/100 的 rate curves vs PLOB;图示直观,但具体 curves 的 tightness(实际实验 vs bound)未在本 memo 数值化
- **具体 e2e capacity formulas 用于 MS-EB**:表 I 的 $\eta_\mathcal{N}$ 等是 network-level 量,需要 MS-EB Sub-Q1 protocol formulation 中的 $\mathcal{E}$ structure 映射才能正确 compute(Sub-Q3 实施步骤)

---

## 7. 下一级 Level 5 升级需求

- **SI Note 2-3**:Truncation tools for asymptotic states + 3 种等价证明 of Theorem 1
- **SI Note 5**:完整 multi-path max-flow min-cut 推导
- **SI Note 6**:Related literature + follow-up works
- **具体 Gaussian thermal-loss chain 上界 Eq. 23-25 在 chain 形式下的扩展**
- **具体 amplitude damping 的 CV↔DV decomposition 推导**(Eq. 47-49 in PLOB → chain version)

---

## 8. 对本项目下阶段直接 bearing

### Phase 2 Sub-Q3 立即行动

1. ✅ **PLOB-2017.md + Pirandola-2019.md 双 memo 配对** — 两篇都 Level 4 覆盖(本 memo 是第二篇)
2. 🔲 **拓扑适用性 lemma 形式化** — 基于本 §5.3 论证,写 `docs/msen/topology_applicability.md`(~2 天)
3. 🔲 **TF-QKD vs Pirandola N=1 gap 数值表** — 扩展 PM-QKD Ma Fig.3a 对比到 single-repeater bound 对照(~1 天)
4. 🔲 **Squashed entanglement 补读**(TGW 2014 + WTB 2017)— amplitude damping / non-lossy Gaussian 的 tighter bound

### Sub-Q4 gap 归因准备

- Pirandola bound + PM-QKD 实测 gap = Sub-Q4 A/B/C 分配的数据源
- 需要 Phase 2 §4.4 的 E_R 数值工具链(可选 SDP)来算 non-distillable 信道的 gap

---

## 9. 变更日志

- **v0.1** (2026-04-20):首稿 Level 4 精读。基于 PDF 8 页主文完整 + §Methods 浏览;SI Notes 未覆盖。作为 PLOB-2017.md 的 relay-topology 补件,配合 Phase 2 Sub-Q3 §4.3 拓扑适用性 lemma 攻坚。核心发现:**TF-QKD / PM-QKD 的正确上界是 Pirandola Eq. 9 at N=1**,即 $-\log_2(1 - \sqrt\eta)$,区别于 PLOB point-to-point $-\log_2(1-\eta)$。
