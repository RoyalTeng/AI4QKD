# TF-QKD 族三变体精读(Level 3)

**目标**:为 F6 TF-QKD family sheet([tfqkd_family.md](../families/tfqkd_family.md))upgrade 路径 §9.1 提供文献基础 — 三份原始论文并列精读,给出 MS-EB 映射可行性评估 + 密钥率公式 + 数值 benchmark。

## 论文引用

1. **TF-QKD (原版)**:Lucamarini, M., Yuan, Z. L., Dynes, J. F., Shields, A. J. (2018). *Overcoming the rate-distance limit of quantum key distribution without quantum repeaters.* Nature **557**:400–403. arXiv:1811.06826.
2. **SNS-TF-QKD**:Wang, X.-B., Yu, Z.-W., Hu, X.-L. (2018). *Sending or not sending: Twin-field quantum key distribution with large misalignment error.* PRA **98**:062323. arXiv:1805.09222v9.
3. **PM-QKD**:Ma, X., Zeng, P., Zhou, H. (2018). *Phase-Matching Quantum Key Distribution.* PRX **8**:031043. arXiv:1805.05538v3.

**精读日期**:2026-04-20(Phase 1 F6 TF-QKD 协议族覆盖准备)
**精读等级**:**Level 3**
- 各篇主文:完整精读(协议 + 密钥率公式 + 数值 benchmark)
- 安全证明细节:Level 2(Ma-Zeng-Zhou Appendix A / Wang-Yu-Hu §V 虚拟协议浏览)

**范围说明**:
- 本 memo **覆盖**:三变体的共同骨架 + 各自的关键区别 + 密钥率公式 + 数值参数 + MS-EB 适用性初判
- 本 memo **不覆盖**:Wang-Yu-Hu §VI 完整 tagged-model 证明;Ma-Zeng-Zhou Appendix B 完整仿真公式推导;phase-locking 实验细节(Lucamarini SI)

---

## 1. 一句话总结

**三变体共享"两方 + Charlie 相干干涉 + 单光子检测"拓扑**,密钥率均 $\propto \sqrt{\eta}$ 击穿 PLOB 直接传输极限;三者在 **phase reference / 后筛策略 / 安全证明** 的路线各异,其中 **SNS 用 "发或不发" 回避信号后筛让 traditional decoy-state 直接适用**,**PM 用 optical-mode EDP 给出完整安全证明**,Lucamarini 原版主要贡献是物理方案提出。

---

## 2. 共同骨架(三变体 MS-EB 可抽象层)

```
             Alice                Charlie(Eve 可控)                  Bob
       ┌─────────────┐        ┌────────────────────┐           ┌─────────────┐
       │ 激光源 |√μ⟩  │        │ 分束器 (50:50)     │           │ 激光源 |√μ⟩ │
       │ 随机相位 φ_a │──────→ │ + 干涉测量         │  ←──────  │ 随机相位 φ_b│
       │ 编码 κ_a     │        │ + 单光子检测 D_L/D_R │           │ 编码 κ_b    │
       └─────────────┘        └────────────────────┘           └─────────────┘
                                        │
                                        ▼
                          Charlie 公开检测器点击结果
                          (L / R / fail)
                                        │
                                        ▼
                    Alice/Bob 公开随机相位 φ_a, φ_b
                                        │
                                        ▼
             ┌──────────────────────────────────────────┐
             │  变体区别所在(下表):                   │
             │  - 信号窗口是否做 phase post-selection?  │
             │  - decoy 方法能否直接用?                 │
             │  - 安全证明的路径?                       │
             └──────────────────────────────────────────┘
```

**核心物理机制**:
- Alice/Bob 独立制备**相干态**,经信道传输到 Charlie → 在 Charlie 处做**单光子干涉**(而非 MDI 的 coincidence)→ 单光子事件率 $\propto \eta_\text{total} = \eta_A \cdot \eta_B$ 的**平方根** $\sqrt{\eta_\text{total}}$
- **拓扑相同于 MDI**(Alice/Bob/Charlie 三方,Charlie 可 malicious),但 **TF 对单光子检测的依赖**使 $R \propto \sqrt{\eta}$ 而非 MDI 的 $R \propto \eta$
- **关键假设**:Alice/Bob 的激光源 **phase-locked** 或 phase reference 可通过强脉冲互校准(可实现)

---

## 3. 三变体对比

| 维度 | TF-QKD(Lucamarini) | SNS-TF-QKD(Wang) | PM-QKD(Ma) |
|------|---------------------|-------------------|-------------|
| **信号源** | 相干态 + 随机相位 + κ bit 编码到相位 | 信号窗口:以 ε 概率发 \|√μ'⟩,以 1-ε 发真空 | 相干态 + 随机相位 φ + κ bit 编码到 κπ 相位偏移 |
| **Decoy 源** | 相干态 \|√μ⟩ with random phase ρ | 独立 decoy 窗口,多强度 μ_i | 独立 decoy 窗口,多强度 μ_i |
| **Phase slicing 后筛** | **必需**:M 个 phase slice(典型 M=16),筛选 \|ρ_a−ρ_b\| 落同 slice | **不做信号筛**(Z-windows 无 post-selection);X-windows 用 \|cos(δ_a−δ_b)\| 判据 | 连续 φ 后筛 \|φ_a−φ_b\| = 0 or π(等效 M→∞)|
| **Decoy-state 有效性** | 传统 decoy **不直接适用**(phase 后筛引入额外非经典信息) | **直接适用**(Z 基无筛 → 信号是 classical mixture of Fock states)| **适用** + Ma optical-mode 证明直接用 |
| **安全证明状态** | Lucamarini 承认 "unconditional security beyond scope" | 完整 tagged-model 证明(§V 虚拟协议 + reduction) | 完整 optical-mode EDP 证明(Appendix A) |
| **Misalignment 容忍** | ~几个 % | **35%–45%**(关键优势) | ~1.5% 实际,可容 ~10% |
| **sifting 因子** | 1/M ≈ 6.25%(M=16) | 2ε(1-ε) ≈ 几个 % | 2/M ≈ 12.5%(M=16) |

**结论**(MS-EB 映射难度):
- **PM-QKD 最友好**:Ma 的 optical-mode 证明使用 Fock-truncation + parity measurement 直接,和 WLC numerical 工具链接口清晰(Ma Lemma 1 偶奇光子数分开分析)
- **SNS 次友好**:Decoy 直接用,"发或不发" 等效 coherent state + vacuum 的二元选择 → `source_state` 是 density matrix superposition
- **Lucamarini** 最不友好:无完整安全证明,phase slicing 后筛需 post-selection `AnnouncementRule`(F3 SARG04 遗留的基础设施缺口类似)

---

## 4. 密钥率公式

### 4.1 Lucamarini 2018(Eq. 2–3)

原版 decoy-state QKD-style 形式:

$$R_\text{QKD}(\mu, L) = \left.Q_1\right|_{\mu, L}\left[1 - h\left(\bar{e}_1\big|_{\mu, L}\right)\right] - f Q_{\mu, L} h(E_{\mu, L})$$

其中 $Q_1 = p_{1|\mu} y_1$ single-photon gain,$\bar{e}_1$ phase error upper bound(decoy 估)。**TF-QKD** 额外有 phase-slice 筛因子:

$$R_\text{TF-QKD}(\mu, L) = \frac{d}{M}\left.\left[R_\text{QKD}(\mu, L/2)\right]\right|_{\oplus E_M}$$

其中 $E_M = 1/2 - \sin(2\pi/M)/(4\pi/M)$ 是 phase slice 引入的 intrinsic QBER。$L/2$ 体现 "each user effectively travels L/2" 的 √η 优势来源。

### 4.2 Wang-Yu-Hu 2018(Eq. 3–4)

SNS 信号窗口 Z-basis 无筛,直接用 Shor-Preskill:

$$N_f = n_1 [1 - H(e_1^{ph})] - n_t f H(E^Z)$$

Per-time-window rate(Eq. 4):

$$R = 2\epsilon(1-\epsilon) \mu' e^{-\mu'} s_1 [1 - H(e_1^{ph})] - S_Z f H(E^Z)$$

其中 $s_1$ 是 $\mathcal{X}_1$-windows 的单光子 yield,$e_1^{ph}$ 是 Z1-bits 的 phase-flip rate(由 X-window 数据通过 Eq. 2 估计):

$$e_1^{\mathcal{X}_1} = \frac{S_\mu E_\mu^X - e^{-2\mu} s_0 / 2}{2 \mu e^{-2\mu} s_1}$$

### 4.3 Ma-Zeng-Zhou 2018(Eq. 4)

PM-QKD Shor-Preskill 形式:

$$R_\text{PM} \geq \frac{2}{M} Q_\mu \left[-f H(E_\mu^Z) + 1 - H(E_\mu^X)\right]$$

其中 $E_\mu^X$ 上界由 Eq. 2 通过 decoy-state 给出(单光子 phase error ≈ bit error of odd-photon-number states,per Ma Lemma 1)。

**相同结构性**:三式都是 "**single-photon contribution 给 privacy term** $[1 - H(e_1^X)]$ + **总 gain 给 leak_EC term** $-f Q h(E^Z)$";decoy-state 估 $(Q_1, e_1^X)$ 是核心数值任务。

---

## 5. 数值 benchmark(三变体 Fig. 复现 target)

| 变体 | 参数 | Fig. | 典型距离 | 密钥率 |
|------|------|------|----------|--------|
| Lucamarini | $p_d=10$ Hz, $\eta_d=30\%$, $e_\text{opt}=1\%$, $f=1.15$, M=16 | Fig. 1a(thick line) | 500 km | ~10² bit/s(~10⁻⁸ bit/pulse at 1 GHz clock) |
| SNS-Wang | $p_d=10^{-11}$, $\eta_d=80\%$, $f_\text{EC}=1.1$, 理想解析 | Fig. 1 | 700 km @ $e_a=15\%$;500 km @ $e_a=35\%$ | $10^{-7}$ at 500 km @ $e_a=35\%$ |
| PM-Ma | $p_d=8\times10^{-8}$, $\eta_d=14.5\%$, $f=1.15$, $M=16$, $e_d=1.5\%$ | Fig. 3a | 418 km(cutoff $10^{-8}$) | 超过 PLOB 线性 bound at $l > 250$ km |

**统一标度**:三者均展示 $R \propto \sqrt{\eta}$,log-log 斜率 $0.5$(vs BB84/MDI 的 1)。

**F6 tfqkd_family.md §5.2 硬验收对齐**:
- TF(Lucamarini):log-log 斜率 $0.5 \pm 0.05$
- SNS:密钥率误差 rel=0.05(vs Fig. 1 曲线)
- PM:密钥率误差 rel=0.05(vs Table II / Fig. 3)

---

## 6. MS-EB 映射可行性初判

### 6.1 PM-QKD(**推荐首先实施**)

- **$\mathcal{P}$**:双 `SourceParty`,`source_state` 为 Fock 截断后的 coherent state + phase-randomization(Ma Eq. A3 Poisson 分布 + 奇偶子空间分解 Ma Eq. A4)
- **$\mathcal{E}$**:BS 干涉 + 单光子检测 → 3-outcome classical register({L, R, fail})
- **$\mathcal{A}$**:`sift_keep` = (L or R) ∧ ($|\phi_a - \phi_b| \in \{0, \pi\}$);Bob 在 $|\phi_a - \phi_b| = \pi$ 时 flip bit(classical post-processing)
- **$\mathcal{T}$**:$Q_\mu, E_\mu^Z$ 直接观测;$E_\mu^X$ 通过 decoy-state(多强度) estimate via Ma Eq. 2
- **$\mathcal{K}$**:Alice 持 key,Bob 对齐后持同步 key

**实施路径**:Phase 0 已有 `qkdx/numerics/wlc.py` + `qkdx/analytic/decoy.py`;PM-QKD 增量是 **`qkdx/protocols/pm_qkd.py`**,共享 MDI-QKD 的双源 + Charlie 框架([qkdx/protocols/mdi.py](../../qkdx/protocols/mdi.py))。`scope_tag='partial'` 转 `'covered'` 的门槛:Fock 截断合法化 + Ma Lemma 1 奇偶分解写入 `build_pm_qkd_protocol`。

### 6.2 SNS-TF-QKD(次优先)

- **$\mathcal{P}$**:`source_state` = $\epsilon |\sqrt{\mu'} e^{i\delta}\rangle\langle \sqrt{\mu'} e^{i\delta}| + (1-\epsilon) |0\rangle\langle 0|$ — 需要 density matrix 混合(非 pure MUB)
- **其余**:同 PM
- **特殊点**:信号窗口无 post-selection → `sift_keep` 只看 Charlie 声明 ∈ {L, R},无相位判据 → 最简

**门槛**:`source_state` 不再是 single MUB state;需要 MS-EB framework 支持 source 层 classical register(发/不发的经典决策)。Phase 1 S2.1 MDI multi-source 的基础设施已覆盖此情形([qkdx/protocols/mdi.py](../../qkdx/protocols/mdi.py) `build_mdi_bell_protocol`)。

### 6.3 Lucamarini 原版(**降级为 `spec_only`,不推荐实施**)

- **$\mathcal{A}$**:需要 phase slice post-selection($|\rho_a - \rho_b|$ 落同 M-slice 内)→ 需要 `AnnouncementRule` 支持 classical register post-selection 谓词
- **安全证明**:Lucamarini 自己承认未完成;后续文献(Ma 2018 / Curty-Azuma-Lo 2019)补全
- **建议**:F6 主实施走 PM-QKD 或 SNS,Lucamarini 原版在文档中作为历史参考,不单独实施

---

## 7. F6 实施路径建议(Phase 1 S2.1-S2.2 节律)

| 子阶段 | 产出 | 难度 | Plan 对齐 |
|--------|------|------|-----------|
| 7.1 文献 memo | **本 memo** | 已完成 | S2.1 R1.1 |
| 7.2 MS-EB formulation doc | `docs/msen/pm_qkd_formulation.md` | 低 | S2.1 R1.2 |
| 7.3 PM-QKD 实施 | `qkdx/protocols/pm_qkd.py` + tests | 中(~1 周) | S2.1 R1.3 |
| 7.4 log-log 斜率验收 | `test_pm_qkd_sqrt_eta_scaling` | 低 | tfqkd_family.md §5.2 |
| 7.5 SNS 实施(可选) | `qkdx/protocols/sns_tfqkd.py` + tests | 中(~1 周) | Sub-Q2 覆盖广度 |
| 7.6 Pareto 扫描 | `qkdx/sweeps/tfqkd_family_sweep.py` | 低 | S2.2 硬验收 |

**S2.1 R1.3 验收**(family sheet `scope_tag='covered'`):
- PM-QKD log-log 斜率 $0.5 \pm 0.05$ in range $\eta \in [10^{-3}, 10^{-5}]$
- 至少 1 个文献 anchor(Ma Fig. 3a)匹配在 cutoff 距离附近

**MS-EB 映射未解决点**(留作 ADR):
- PM-QKD 的 Fock 截断 $N_\text{fock}$ 选择(Ma 用 implicit 无限;我们需要 $N \leq 10-20$)→ 引入 truncation error,量化影响
- SNS 的"发或不发"在 `SourceParty` 层如何表达(二元 classical register 是否破坏 MS-EB H2 单一 $\mathcal{E}$?)— 需要 Phase 0 multi-source 基础设施验证

---

## 8. 对 Phase 1 / Phase 2 的 Bearing

### 8.1 Phase 1 Sub-Q2 bearing

- 完成 F6 后,Sub-Q2 三大协议族(F1 BB84 / F5 MDI / F6 TF)**全覆盖**;Pareto 比较图可横跨 $\eta \in [10^{-6}, 1]$
- $\sqrt{\eta}$ vs $\eta$ 的物理本质是 **中间节点的单光子 vs 双光子相干**,在 Sub-Q2 Pareto sheet 中作为"协议族层面最优选择"轴

### 8.2 Phase 2 Sub-Q3 bearing

- **TF 族 vs PLOB/Pirandola 上界**:TF 是首个 $\sqrt{\eta}$ 协议族;Sub-Q3 上界对比图的核心对象
- 已有上界文献(本仓库 [docs/literature/pdfs/](pdfs/)):PLOB-2017 / TGW-2014 / WTB-2017 / Pirandola-2019 / DKW-2020 全在库
- **gap 刻画**:TF 下界 $\sim \sqrt{\eta}$ vs 上界 $-\log_2(1-\eta) \approx \eta/\ln 2$ 在 $\eta \ll 1$ 下 ⇒ TF 接近但未达上界 — Sub-Q4 归因 A/B/C 的典型 testbed(Ma §VI outlook 明示)

### 8.3 Sub-Q4 主问题 bearing

TF 族是 [PROSPECTUS.md](../PROSPECTUS.md) 主问题攻坚的**最大权重** testbed(Sub-Q3 + Sub-Q4 均以 TF 为主对象)。本 memo 完成 + PM-QKD 实施后,主问题的"下界层"工具链完整。

---

## 9. 三篇论文的关键符号对照表

| 概念 | Lucamarini | Wang-Yu-Hu | Ma-Zeng-Zhou |
|------|------------|------------|--------------|
| 信号强度 | $\mu$ (combined $\mu_a + \mu_b$) | $\mu'$(signal),$\mu_k$(decoy) | $\mu_a = \mu_b = \mu_i / 2$ |
| 随机相位 | $\rho_a, \rho_b$ 全局 + $\gamma_a, \gamma_b$ 编码 | $\delta_A, \delta_B$ 随机 + $\gamma_A, \gamma_B$ 参考 | $\phi_a, \phi_b$ 随机 + $\pi\kappa_{a,b}$ 编码 |
| Phase slice 数 | $M$ | 不做(有 $\lambda$ judgement) | $M$ |
| 信号 QBER | $E_{\mu, L}$(overall) | $E^Z$(Z-basis) | $E_\mu^Z$ |
| Phase error | $\bar{e}_1$(single-photon) | $e_1^{ph}$ | $E_\mu^X$ |
| Sifting factor | $d/M$ | $2\epsilon(1-\epsilon)$(×$\mu' e^{-\mu'}$) | $2/M$ |

---

## 10. Limitations 与未解决点

### 作者明示

- **Lucamarini 2018**:§3(结尾)明确 "a rigorous proof of unconditional security is beyond the scope of the current paper"
- **Wang-Yu-Hu 2018**:§V 虚拟协议 + Reduction 论证展示 "信号后筛取消 + tagged-model" 路径对 SNS-TF 的安全性；本 memo v0.1 曾附加"coherent attack 需要进一步论证"的限定,**Round-2 修订撤回** — 该限定在原文中没有直接支撑,属 memo 作者越权 paraphrase。Wang 原文仅指出 "traditional decoy-state method does not apply to the original TF-QKD protocol" 的论证焦点,我 memo 中的进一步 coherent-attack 限制是 不当推断,应以 Wang 原文论述为准
- **Ma-Zeng-Zhou 2018 §VI**:"our bound Eq. (4) is still far away from this bound [single-repeater $-\log_2(1-\sqrt\eta)$]";参数空间优化(如 biased phase randomization)未完成

### 本 memo 读者视角

- **Phase reference 实验难度**:三方案均需 phase-locked 激光或强脉冲互校准(Lucamarini SI 详述);我们的 MS-EB 模型如何表达此 phase reference **可能需要 ADR**(tfqkd_family.md §9.4 已列预案)
- **Fock 截断 error bound**:Ma-Zeng-Zhou 的 $N \to \infty$ 证明在 truncation 下的严格误差未给出;WLC numerical 在 $N = 10$ 的数值是否严格 lower bound 需额外论证(Ma Appendix B 仿真仅验证 convergence)
- **与 Kamin 2025 GEAT 的兼容性**:Kamin §7 分析 decoy-state BB84 用 Choi-state 块对角;TF-QKD 的 optical-mode 结构是否需要扩展 Kamin 框架待评估(Kamin 论文明确只做 BB84-class 协议,未涉及 TF)

---

## 11. 下一级 Level 4 升级需求(若后续回来精读)

- **Ma-Zeng-Zhou Appendix A.4**:optical-mode EDP 证明细节(Protocol I 的 $|\Psi_0^{(k)}\rangle$ 推导)
- **Ma-Zeng-Zhou Appendix A.5**:$E_\mu^X$ 的 decoy-state 上界推导(奇偶光子数 phase error 关系 Lemma 1 的完整证明)
- **Wang-Yu-Hu §V Theorem + Reduction 2**:完整 tagged-model 证明 + $X_0/X_1$-window 扩展
- **Lucamarini 2018 SI**:phase-locking 技术 + Eq. 4 相位漂移模型完整导出

---

## 12. 变更日志

- **v0.1** (2026-04-20):首稿 Level 3 并列精读。基于三篇 PDF 主文完整阅读 + Appendix 浏览。配合 Phase 1 F6 tfqkd_family.md v0.1 → v0.2 的 TF/SNS/PM 实施准备层。
