# PM-QKD 在 MS-EB 框架下的书写

**版本**:v0.1(2026-04-20,F6 §7.2 produce)
**关联研究动作**:tfqkd_family.md §9.1 §7.2(MS-EB formulation doc)
**对应协议代码(目标)**:`qkdx/protocols/pm_qkd.py`(F6 §7.3 产出,本文档不创建)
**Level 3 精读 memo**:[docs/literature/TF-QKD.md](../literature/TF-QKD.md)(三变体并列,§2–6 覆盖 PM)

---

## 0. 范围限定

本 MS-EB 书写**只覆盖 PM-QKD 的 d=2 + phase-randomized 情形**(Ma-Zeng-Zhou 2018 §II 主分析对象):

**覆盖**:
- $d = 2$(key bit 编码到 $\pi\kappa$ 相位偏移,$\kappa \in \{0, 1\}$)
- Alice/Bob 对各自相干态做独立 uniform phase randomization $\phi_a, \phi_b \in [0, 2\pi)$(Ma §II "plus phase randomization")
- Fock truncation $N_\text{fock}$(本书写:$N_\text{fock} = 10$,与 F5 MDI Bell builder 一致)
- 对称源方强度 $\mu_a = \mu_b = \mu/2$
- Charlie 的 50:50 分束器 + 单光子检测(L/R/fail 三结果)
- **Decoy-state estimation of $(Q_1^L, e_1^X)$**:Ma Eq. 2 通过 Poisson 光子数分解估上界

**不覆盖**(归 Phase 1 S2.2 扩展 / ADR 待决):
- $d > 2$(多相位 PM-QKD,Ma §II 提到但主证明不覆盖)
- Phase reference deviation $\phi_0$ 及 post-compensation($j_d$ slice offset;Ma §IV 实验补偿技术)
- 相位漂移统计模型(Ma §IV Gaussian drift;本书写假设瞬时 phase reference match)
- 连续 phase 后筛(Ma §II 理论上连续 $[0, 2\pi)$,本书写把筛选条件离散化到 $M$ slice)
- **$\sqrt{\eta}$ scaling 的严格 truncation error bound**(Ma Appendix B 仅数值验证 convergence,未给 $N_\text{fock}$ 误差 closed form)

---

## 1. MS-EB 五元组 $\Pi_\text{PM} = (\mathcal{P}, \mathcal{E}, \mathcal{A}, \mathcal{T}, \mathcal{K})$

### 1.1 $\mathcal{P}$:双源方 + Fock 截断 + phase randomization

PM-QKD 是**第二个双源方**协议(首个是 MDI,见 [mdi-formulation.md](mdi-formulation.md) §1.1)。与 MDI 的关键差异:**源态不是 BB84 EB 4-dim qubit**,而是 **Fock-truncated phase-randomized coherent state × key-bit classical register**。

| 源方 | key_register_dim | phase_register_dim | signal_register_dim | source_state 维度 |
|------|-------------------|---------------------|---------------------|---|
| Alice | 2(κ=0, 1) | $M$(相位 slice) | $N_\text{fock} + 1$(Fock 0..N) | $(2 M (N+1))^2$ |
| Bob | 2 | $M$ | $N + 1$ | $(2 M (N+1))^2$ |

**注**:Round-1 review M1 指出 v0.1 的表格未含 phase register,导致 EB 源态写法错误。Round-2 显式加入 $M$-dim phase register $R_A$ / $R_B$ 保留 key-optical 相关性。

**源态构造**(**Round-2 修订**,见本节末的 Round-1 review M1 说明):

EB 写法需要 key register $K_A$ 与 optical mode $A'$ **保持相关**。先对 φ 积分会把 κ 的 optical marginal 抹平,导致 emitted state 不再携带 key bit 信息(Round-1 M1 review 正确指出的 bug)。正确的 PM-QKD EB 源态是:

$$\rho^\text{src}_{K_A A' R_A} = \frac{1}{2}\sum_{\kappa=0}^{1} |\kappa\rangle\langle\kappa|_{K_A} \otimes \int_0^{2\pi}\!\frac{d\phi}{2\pi}\,|\phi\rangle\langle\phi|_{R_A} \otimes |\alpha e^{i(\phi + \pi\kappa)}\rangle\langle\alpha e^{i(\phi + \pi\kappa)}|_{A'}$$

其中 $R_A$ 是 Alice 私人保留的 **phase register**(classical, uniform over $[0, 2\pi)$,本实施离散化到 $M$ slices → $\dim R_A = M$)。**关键**:只有在 Alice 稍后公开 $\phi_a = \phi$ 后,φ 才从 Alice 的 side information 转入公共记录;此**之前** $R_A$ 的存在让 $|\kappa \rangle$ 与 optical $A'$ 通过 $\phi$ 保持相关,emitted optical state 仍携带 κ 信息。

**两种不同的 "Fock 对角化" 情形**(Ma Eq. A3 的正确理解,Round-2 修订):

条件化 ≠ 求迹。两者给出**完全不同的** optical state。

- **在公告 φ 条件化下**(Alice 宣布 $\phi_a = \phi$ 后,$R_A$ 的 φ 值变为公共知识,对其做 classical conditioning):

$$\rho^\text{src}_{A' | R_A = \phi, K_A = \kappa} = |\alpha e^{i(\phi + \pi\kappa)}\rangle\langle\alpha e^{i(\phi + \pi\kappa)}|$$

这是**仍然是相干态**,不是 Fock 混合(coherent state 在固定 φ 下完全保留)。

- **求迹/平均 over phase register**(Eve 的视角:不做 Alice 的 φ 公告 conditioning,对 $R_A$ 求迹):

$$\operatorname{Tr}_{R_A}\rho^\text{src}_{K_A A' R_A} = \frac{1}{2}\sum_{\kappa=0}^{1} |\kappa\rangle\langle\kappa|_{K_A} \otimes \left[\sum_{k=0}^{\infty} e^{-|\alpha|^2}\frac{|\alpha|^{2k}}{k!}|k\rangle\langle k|_{\text{Fock}}\right]$$

此时 optical marginal **κ-independent**(Poisson Fock 混合,Ma Eq. A3);这对 Eve 的 single-photon attack 分析有用 — 但**不是** Alice 在自己 lab 中的态描述。

**下游实施警示**:`build_pm_qkd_protocol` 的 `source_state` 应构造**纯化后**的三件套 $(K_A, R_A, A')$,**不应** 在源态层面直接写 Poisson Fock 混合(那是 Eve-perspective average,不是 EB source);否则就回到 v0.1 的 M1 bug。Ma Lemma 1 的奇偶光子分解作用域:**Eve 在她不知道 φ 时做 QND photon-number 测量**(Kamin Eq. 71 decoy 分块的正是此情形)— 这等价于对 $R_A$ 求迹 / 求平均,而不是对 $R_A = \phi$ 做条件化。**Alice/Bob 公告 $\phi_a, \phi_b$ 的行为本身不触发** Fock 对角化(注意:φ 的公告方是 Alice/Bob,不是 Charlie — Charlie 只公告检测器结果 $r \in \{L, R, \text{fail}\}$);φ 公告与 Eve 对 $R_A$ 的"不知情"才共同造成 Fock 分块可用性。

其中 $|\alpha|^2 = \mu/2$(每源强度),$A'$ 是 Fock 截断后的光学模态。

**$\pi\kappa$ 编码的效果**(Ma Lemma 1 奇偶分解):对 fixed κ + announced φ,$|\alpha e^{i(\phi + \pi\kappa)}\rangle$ 的 even-photon 分量 $|\alpha e^{i\phi}\rangle^\text{even}$ 与 $\kappa$ 无关(因为 $e^{i\pi \cdot 2m} = 1$),odd-photon 分量 $|\alpha e^{i\phi}\rangle^\text{odd}$ 携带 κ 相位符号差 → key bit 的相干性质在 odd-photon 子空间 — 这就是 Ma Lemma 1 的"奇光子 phase flip ⇔ Z-bit flip" 关系。

> **Round-1 review M1 闭合**:v0.1 的源态写成 $\rho = \frac{1}{2}\sum_\kappa |\kappa\rangle\langle\kappa| \otimes \int d\phi \cdots$ 把 φ 积分在 κ 求和之内(即没有 purifying $R_A$)。这样**在源态层面**就把 optical marginal 抹成 κ-independent,等价于说 Alice 的 emitted state 不携带 key bit — 与 Ma-Zeng-Zhou §II 协议语义矛盾。Round-2 修订引入 $R_A$ phase-purifying register,保留 κ 与 $A'$ 的相关性。**关键**:Poisson / Fock 对角化**只在对 $R_A$ 求迹或平均时出现**,**不是**在对公告 φ 做 conditional 时出现(Round-3 M6 修订:条件化 ≠ 求迹 — 见上文两种情形)。

### 1.2 $\mathcal{E}$:双臂信道 + Charlie 分束器 + 单光子检测

$\mathcal{E}: A' \otimes B' \to \text{classical outcome} \in \{L, R, \text{fail}\}$,数学上:

$$\mathcal{E} = \mathcal{E}_\text{det-LR} \circ \mathcal{E}_\text{BS} \circ (\mathcal{E}_{A'} \otimes \mathcal{E}_{B'})$$

- $\mathcal{E}_{A'}, \mathcal{E}_{B'}$:Alice/Bob → Charlie 的透射信道(本书写理想:identity × identity);真实实现为有损 $\eta_A, \eta_B$
- $\mathcal{E}_\text{BS}$:50:50 分束器 Kraus(Ma Eq. A8):
  $$\begin{pmatrix} c^\dagger \\ d^\dagger \end{pmatrix} = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}\begin{pmatrix} a^\dagger \\ b^\dagger \end{pmatrix}$$
- $\mathcal{E}_\text{det-LR}$:两探测器 $L, R$ 的单光子检测投影 + 公告
  - $L$ click:$|1\rangle_L \otimes |0\rangle_R$(单点击 left detector)
  - $R$ click:$|0\rangle_L \otimes |1\rangle_R$(单点击 right detector)
  - fail:其他(0 或 coincidence 2+)

**实施简化**(与 [mdi-formulation.md](mdi-formulation.md) §1.2 类似):WLC SDP 数值只用 $d_\rho$ + observable,因此**网络 channel 初版用 `KrausMap.identity`**,Charlie 的 BS + detection 通过 `_conditional_alice_bob` override 注入。严格 MS-EB 的完整 Kraus 嵌入留给 F6 §7.5 或 M3+ 精化。

### 1.3 $\mathcal{A}$:公告与筛选

- Charlie 公告 $r \in \{L, R, \text{fail}\}$
- Alice 公告 $\phi_a \in [0, 2\pi)$(离散化到 $M$ slices,$j_a \in \{0, \ldots, M-1\}$)
- Bob 公告 $\phi_b$(同上,$j_b$)
- **sift_keep**:$r \in \{L, R\}$ **AND** $|j_a - j_b| \mod M \in \{0, M/2\}$(等价于 Ma §II "$|\phi_a - \phi_b| = 0$ or $\pi$")

**Bit flip 规则**(Ma §II step "Sifting"):
- 若 $|j_a - j_b| \mod M = M/2$(相位差 ≈ π):Bob 翻转自己的 $\kappa_b$
- 若 Charlie 公告 $r = R$:Bob 同样翻转(Ma §II "Bob flips his key bit $\kappa_b$ if Eve's announcement is $R$ click")

**两个 flip 条件独立**,共同使 Alice-Bob raw key 对齐。

### 1.4 $\mathcal{T}$:观测量与接受判据

三个 observation keys:

$$\text{observation\_keys} = (Q_\mu, E_\mu^Z, E_\mu^X)$$

- **$Q_\mu$**(total gain):$\mathbb{P}[r \in \{L, R\}]$(Charlie 成功率)
- **$E_\mu^Z$**(Z-basis QBER):在 sift 后 Alice-Bob key bit 不匹配率,可**直接观测**
- **$E_\mu^X$**(phase error rate):**不可直接观测**,需通过 Ma Eq. 2 decoy-state 估上界:
  $$E_\mu^X \leq e_0^Z q_0 + \sum_{k=0}^\infty e_{2k+1}^Z q_{2k+1} + (1 - q_0 - \sum_{k=0}^\infty q_{2k+1})$$
  其中 $q_k = (e^{-\mu}\mu^k/k!)Y_k / Q_\mu$ 是 k-photon 信号比例,由 multi-intensity decoy 估 $Y_k$。

**接受判据**(unique-acceptance 初版):$(Q_\mu, E_\mu^Z)$ 接近 honest 参数(用 `rel=0.05` 宽容窗),$E_\mu^X$ 由 decoy 产生的上界 → 不作为独立接受判据。

### 1.5 $\mathcal{K}$:密钥映射

- **密钥持有方**:**Alice**(`key_party = "Alice"`)
- **Key register**:$\kappa_A \in \{0, 1\}$
- **Bob 对齐**:根据 sifting rule 1.3 翻转 $\kappa_B$(2-step: $|j_a - j_b| = M/2$ → flip;$r = R$ → flip)

Alice 的 key map 是 identity($\kappa_A$ 直接作为 raw key);Bob 的翻转动作通过 virtual EB picture 在源态 `source_state` 的对称构造下**隐式吸收**(与 MDI 的 `key_party = "Alice"` 约定一致)。

---

## 2. $p_\text{sift}$ 的推导

$$p_\text{sift}^\text{PM} = \underbrace{P(r \in \{L, R\})}_{Q_\mu \sim \sqrt{\eta}} \times \underbrace{P(|j_a - j_b| \mod M \in \{0, M/2\})}_{2/M}$$

- **单光子干涉成功率**:$Q_\mu = 2\mu\eta + O(\mu^2)$(小 μ 线性展开;Ma Eq. B14 完整式包含 dark count);对典型 $\mu \sim 0.3, \eta = 10^{-3}$,$Q_\mu \sim 6 \times 10^{-4} \sim \sqrt{\eta}$ 量级
- **Phase slice 匹配率**:$M$ 个 slice 中,$|j_a - j_b|$ 均匀分布到 $M$ 值;匹配 $\{0, M/2\}$ 两个值 → $2/M$

**Ma Eq. 4 per-pulse rate**:

$$R_\text{PM} \geq \frac{2}{M} Q_\mu \left[-f H(E_\mu^Z) + 1 - H(E_\mu^X)\right]$$

即 $\frac{2}{M}$ 作为 sifting factor,$Q_\mu[\cdot]$ 作为 per-sift 净 key rate。

**典型参数下的 $p_\text{sift}$**(Ma Fig. 3b simulation,$\mu=0.3, \eta_d=14.5\%, M=16$):
- $\eta_\text{total} = 10^{-3}$(100 km):$Q_\mu \approx 10^{-4}$,$2/M = 0.125$ ⇒ $p_\text{sift} \approx 1.25 \times 10^{-5}$
- $\eta_\text{total} = 10^{-4}$(200 km):$Q_\mu \approx 3 \times 10^{-5}$ ⇒ $p_\text{sift} \approx 3.75 \times 10^{-6}$

---

## 3. WLC SDP 表达(目标,F6 §7.3 实施时落)

### 3.1 SDP 变量

**conditional_alice_bob 维度**:$d_\rho = 4$($2 \times 2$,Alice $\kappa_A$ × Bob $\kappa_B$ effective key bit)— 与 BB84/MDI **相同**。

**关键观察**:WLC SDP 层面 PM-QKD 与 BB84/MDI 的**可约化性**(Ma §III 明示):Alice-Bob 的 effective 4-dim key subspace 在 "只保留 sift 事件" 后,经 Ma Lemma 1 的奇偶光子数分解 + Shor-Preskill argument,**归约到 qubit-based CSS 密钥率**。

- $\mathcal{G}$:identity on 4-dim,`dim_key=2, dim_side=2`
- $\mathcal{Z}$:pinching key register(Alice $\kappa_A$)

### 3.2 约束集合 $\mathcal{S}_\text{PM}$

$$\mathcal{S}_\text{PM} = \{\rho \succeq 0 : \text{Tr}(\rho) = 1, \text{Tr}(\Gamma_Z \rho) = E_\mu^Z, \text{Tr}(\Gamma_X \rho) \leq E_\mu^X{}^\text{decoy-UB}\}$$

**差异 vs MDI**:$E_\mu^X$ 不是直接约束(不可观测),而是 decoy-state 产生的**上界**;$\rho$ 的可行集在 $E_\mu^X$ 方向更大 → $H(A|E)$ 更小(保守)。

**与 BB84 等价性条件**:当 $E_\mu^X = E_\mu^Z$ 且 decoy-UB 吻合时 $H^\text{PM}(A|E) = H^\text{BB84}(A|E)$;否则 PM 略 pessimistic。

### 3.3 密钥率关系

$$R_\text{PM}^\text{ideal} = p_\text{sift}^\text{PM} \cdot [H(A|E) - f_\text{ec} \cdot h(E_\mu^Z)]$$

不同于 MDI 的 $p_\text{sift} = 0.25$ 常数,**PM 的 $p_\text{sift}$ 随信道标度**(因 $Q_\mu \propto \sqrt{\eta}$,而 $2/M$ 常数)。这正是 $\sqrt{\eta}$ 标度的来源:

$$R_\text{PM} \propto p_\text{sift} \propto Q_\mu \propto \sqrt{\eta_\text{total}}$$

### 3.4 数值验证计划(F6 §7.3 目标测试)

- `test_pm_qkd_sift_scaling`:log-log($Q_\mu$ vs $\eta$)斜率 $0.5 \pm 0.05$
- `test_pm_qkd_vs_ma_fig3a`:$\mu=0.3, \eta_d=0.145, M=16, e_d=0.015$ 下密钥率在 100 km / 200 km / 300 km 三点对比 Ma Fig. 3a,rel=0.05

---

## 4. Additivity 验证(预计)

`qkdx/numerics/wlc.py` **零修改**(与 MDI/BB84/六态一致,这是 MS-EB framework 的核心稳定性保证)。新增仅限:

- [qkdx/analytic/decoy.py](../../qkdx/analytic/decoy.py):Ma Eq. 2 phase-error 上界估 `pm_decoy_phase_error_upper`(复用现有 2-decoy 基础设施)
- `qkdx/protocols/pm_qkd.py`(本文档不创建,F6 §7.3 产出)
- `tests/test_protocols/test_pm_qkd.py`(同上)

**预期** WLC SDP 通过 override 路径接入:与 [mdi.py](../../qkdx/protocols/mdi.py) 的 `_conditional_alice_bob` override 思路一致,PM-QKD 的 `_conditional_alice_bob` 从 `executed_state` 提取 Alice $\kappa_A$ × Bob $\kappa_B$ 4-dim 子空间并应用 Ma 奇偶分解 + decoy-UB phase-error 约束。

---

## 5. 对 PROSPECTUS §3.1 主问题的 Bearing

PM-QKD 是 PROSPECTUS v3.1 §3.1 **untrusted measurement relay with √η scaling** 拓扑的 **首个完整安全证明**(对比 Lucamarini 原版 "proof beyond scope"):

1. **为 Sub-Q2 提供 $\sqrt{\eta}$ 族 anchor**(Phase 1 S2.1-S2.2):补全三大族 F1 BB84(η) / F5 MDI(η) / F6 TF(√η)的协议族地图;Pareto 前沿跨 6 decade η 成为可能
2. **为 Sub-Q3 上界对比提供参数化 benchmark**(Phase 2):PLOB-2017 $-\log_2(1-\eta)$ vs PM-QKD Eq. 4 下界的 gap 在 $\eta \in [10^{-6}, 10^{-3}]$ 是 Sub-Q4 归因的典型 testbed
3. **为 Sub-Q4 主问题提供"TF 族是否已最紧"判据的证据基础**:Ma §VI outlook 明示"still far away from single-repeater bound $-\log_2(1-\sqrt\eta)$";此 gap 本身是 Phase 3 gap 归因 A/B/C 的核心刻画对象

---

## 6. Limitations

**源于 Ma-Zeng-Zhou 2018 论文明示**(见 [TF-QKD.md](../literature/TF-QKD.md) §10):
- 单光子干涉 **不在 PLOB repeaterless 直接传输** 的 scope 内(Charlie 是 untrusted relay,而非 direct)— 此"不矛盾"Ma §V 明示
- Phase reference 假设 $\phi_0 = \phi_{b,0} - \phi_{a,0}$ 瞬时 match;实际实验需 active feedback 或 strong-pulse calibration(Ma §IV);**本 MS-EB 书写不覆盖 phase drift model**
- $d > 2$ PM-QKD 证明未在 Ma §II 完整给出(Ma §VI outlook);$d=2$ 是严格覆盖的唯一情形

**源于 MS-EB framework**:
- Charlie POVM 未显式 Kraus 嵌入(同 MDI);严格形式化留待 F6 §7.5 或更晚
- Fock 截断 $N_\text{fock}$ 的**严格上界误差 bound 不可用**(Ma 只做 convergence 数值验证);此为 `scope_tag='partial'` 升级到 `'covered'` 的 key blocker(ADR 待决)
- No finite-key:渐近 i.i.d. + collective attack;finite-key 归 Phase 1 S2.5(GEAT 或 Renner path)

**源于本书写假设**:
- 对称源强度 $\mu_a = \mu_b$(Ma §II 主分析;asymmetric 扩展归 Phase 1 Sub-Q2)
- Phase slice 离散化到 $M = 16$(Ma Fig. 3b 典型);$M$ 的优化归 Pareto 扫描
- 不处理 `AnnouncementRule` 的连续相位积分(当前 MS-EB framework 假设 classical register 离散)

---

## 7. 下一步

1. ✅ F6 §7.1 文献 memo([TF-QKD.md](../literature/TF-QKD.md)):v0.1 完成
2. ✅ F6 §7.2 本 MS-EB 书写:v0.1 完成(本文档)
3. ⏳ F6 §7.3 `qkdx/protocols/pm_qkd.py` 实施 + 基础 tests
4. ⏳ F6 §7.4 log-log $\sqrt{\eta}$ 斜率验收(`test_pm_qkd_sift_scaling`)
5. ⏳ F6 §7.5 SNS 实施(可选,Sub-Q2 覆盖广度)
6. ⏳ F6 §7.6 Pareto 扫描(Phase 1 S2.2 硬验收接入)

**门槛升级路径**(tfqkd_family.md `scope_tag` 变动):
- `partial` → `partial with impl`:完成 §7.3 后(实施但 phase reference / Fock truncation ADR 未决)
- `partial with impl` → `covered`:完成 §7.4 log-log 硬验收 + Fock truncation ADR 解决(§7.5 前置)

---

## 8. 关键符号对照(vs MDI / BB84 formulation)

| 量 | BB84 | MDI | PM-QKD |
|----|------|-----|--------|
| 源方数 | 1 | 2 | **2** |
| source_state 维度 | 2 × 2 = 4 | 8 × 8(×2 sources)| $(2(N_\text{fock}+1))^2$(×2 sources) |
| $d_\rho$(WLC SDP) | 4 | 4 | **4**(Ma Lemma 1 归约后) |
| $p_\text{sift}$ | $1/2$(std)or $p_z^2 + (1-p_z)^2$(Efficient)| $\eta_A \eta_B / 2$(const wrt η)| **$2 Q_\mu / M \propto \sqrt{\eta}$** |
| Phase error 来源 | 直接观测 $E_X$ | 直接观测 $E_X$ | **decoy Eq. 2 上界**(不可直接观测) |
| Key party | Alice | Alice | Alice |
| Source EB | 纯 Bell(MUB)| 纯 Bell(MUB)| **Fock-truncated phase-randomized coherent** |

**关键差异总结**:PM-QKD 的 MS-EB 书写 **保留 BB84/MDI 的 WLC SDP 4-dim 核心**(得益于 Ma Lemma 1 奇偶分解 + Shor-Preskill),但 **source_state 结构和 $p_\text{sift}$ 标度质变**,这对应 $\sqrt{\eta}$ 物理来源。
