# Log 05:TF-QKD / MP-QKD 可达速率(下界端)

**日期**:2026-04-19
**子任务**:给出 $\mathcal{T}_{\text{umr}}$ 拓扑下**已构造性达到的**密钥率,锁定 scaling 与 prefactor。

---

## A. 子问题

要与 Log 04 的上界 $1.44\sqrt{\eta}$ 配对,需要**存在协议**$\Pi$ 使得 $R_\Pi(\eta) \geq c \cdot \sqrt{\eta}$,$c > 0$。

三个候选:

1. TF-QKD(Lucamarini et al. 2018,Nature 557:400)
2. PM-QKD(Ma-Zeng-Zhou 2018,PRX 8:031043)
3. MP-QKD(Zeng-Zhou-Wu-Ma 2022,Nat. Commun. 13:3903)

要回答:

1. 这三个协议是否都属于 $\mathcal{T}_{\text{umr}}$(H1-H5 兼容)?
2. 每个的可达 $R(\eta)$ 的 scaling 与 prefactor?
3. 哪个的 prefactor 最高?这是 gap 的下界端。

---

## B. 工作草稿

### B.1 TF-QKD 协议框架

**原始 Lucamarini 2018**:
- Alice 和 Bob 各自准备 coherent state $\ket{\alpha}e^{i\phi_A}$ 和 $\ket{\alpha}e^{i\phi_B}$(相同振幅,不同相位)
- 信号寄存器是 phase-randomized coherent state 的强度部分
- Charlie 处做 **single-photon interference** 测量:两束光经 beam splitter 合束,两个探测器各自 click
- 当**恰一个**探测器 click 时,Alice-Bob 可以推断 $\phi_A - \phi_B$ 的奇偶性(大致)
- 相位匹配后公开 basis(即相位集合),sift 得密钥

**属于 $\mathcal{T}_{\text{umr}}$ 吗**:

- H1 ✓:Alice - Charlie - Bob 三节点线性网络
- H2 ✓:Charlie 只做 POVM(测量 + 经典宣告),无纠缠生成交换
- H3 ✓:Charlie untrusted(TF-QKD 安全证明不假设 Charlie 诚实,基于 decoy state 的 statistical test 判断)
- H4 ✓:Alice/Bob 本地量子操作(phase randomization + encoding)+ 经典通信
- H5 ✓(Phase 0 语义):per-round 发射 + 本地处理,不保留信号

**结论**:TF-QKD ∈ $\mathcal{T}_{\text{umr}}$。**[THM, Lucamarini18 + by 定义]**

### B.2 TF-QKD 的 $\sqrt{\eta}$ scaling

**核心机制**(Lucamarini18 Eq. 2-3):

原始 TF-QKD 渐近密钥率(理想探测器、单 decoy 状态优化)有

$$R_{\text{TF}}(\eta) \approx \frac{1}{2}\sqrt{\eta} \cdot \nu \cdot [1 - 2h(e_{\phi})] \cdot e^{-\mu}$$

其中:
- $\sqrt{\eta}$ 来自 **单光子探测概率 $\propto \sqrt{\eta}$**(只需一个光子存活,走过一段长度 $L/2$,$\eta = \eta_0^{L/2}$,单光子透过率为 $\sqrt{\eta_{\text{end-to-end}}}$)—— 这是 TF 对 BB84 $\eta$ 和 MDI $\eta^2$ 的突破
- $1/2$ 来自基矢选择(Z/X 对称 BB84 风格筛选)
- $\nu$ 来自 phase matching 成功率因子(依赖具体协议版本)
- $1 - 2h(e_\phi)$ 是 Shor-Preskill 型 privacy amplification 项
- $e^{-\mu}$ 是 coherent state 的单光子概率(需要数值优化 $\mu$)

**核心 scaling**:$R_{\text{TF}}(\eta) = c_{\text{TF}} \sqrt{\eta}$ with $c_{\text{TF}}$ 在 $10^{-2}$ 到 $10^{-1}$ 之间(依 $\mu$、$e_\phi$ 等)。**[THM, Lucamarini18 Fig. 2]**

精确 prefactor(BB84-like post-processing + no noise + infinite key length):

Consider $\mu^\star$ 最优化后,典型数值(from Lucamarini 18 Fig. 2 + 后续 Wang 2018 SNS-TF 变体):

$$c_{\text{TF}}^{\text{opt}} \approx 0.1 \text{ to } 0.3 \quad \text{(in units of bits per signal, } \sqrt{\eta} \text{ coefficient)}$$ **[SYN,综合多个 TF-QKD 论文的数值图]**

数值对比:

| 协议 | scaling | prefactor | 来源 |
|------|---------|-----------|------|
| BB84(单光子 prepare-measure)| $O(\eta)$ | $\sim 0.5$ | Shor-Preskill,$p_{\text{sift}} = 1/2$,$1-2h(e)$ |
| MDI-QKD(Bell 测量) | $O(\eta^2)$ | $\sim 0.1$ | Lo-Curty-Qi 2012 |
| **TF-QKD**(single-photon 干涉) | $O(\sqrt{\eta})$ | $\sim 0.1-0.3$ | Lucamarini 18 |
| **SNS-TF-QKD**(Sending-or-not-sending) | $O(\sqrt{\eta})$ | $\sim 0.2$ | Wang 18 |
| **PM-QKD**(phase-matching) | $O(\sqrt{\eta})$ | $\sim 0.2-0.3$ | Ma-Zeng-Zhou 18 |
| **MP-QKD**(mode-pairing) | $O(\sqrt{\eta})$ | $\sim 0.3+$ | Zeng-Zhou-Wu-Ma 22 |
| PLOB 点对点上界 | $O(\eta)$ | $1.44$ | PLOB17 |
| **Log 04 对称上界**(放宽版 bosonic-asymptotic) | $O(\sqrt{\eta})$ | $1.44$ | **[SYN / CONJ]** — untrusted-relay 继承未 lemma 化 |

### B.3 PM-QKD 的特殊性

Ma-Zeng-Zhou 2018 的 PM-QKD 是 TF-QKD 的一个**变体**,使用 **phase-matching** 而非 time-bin:

- 相位被严格随机化后公开,只保留"相位差等于 $0$ 或 $\pi$"的轮次
- 同样是 single-photon 检测 at Charlie
- Prefactor 在理论上**优于**原始 TF-QKD(因为 phase matching 避免了 phase randomization 中的信息泄露)

**[THM, MZZ18 Fig. 3]**:$R_{\text{PM}}(\eta) = c_{\text{PM}} \sqrt{\eta}$ with $c_{\text{PM}} \approx 0.2 - 0.4$(数值区间,具体取决于 decoy state 优化)。

### B.4 MP-QKD 的提升(**v5 口径澄清**)

Zeng-Zhou-Wu-Ma 2022 的 MP-QKD:

- 跨轮 pairing:把两个时刻 click 的 signal 配对,降低 phase stability 要求
- **注意**(v5 澄清,修 Log 01 与 Log 05 不一致):MP-QKD 的跨轮 announcement **严格意义下违反** PROSPECTUS §3.1 S1(per-round announcement 软约束)。Log 01 把 MP-QKD 标为**"近似属于 $\mathcal{T}_{\text{umr}}$"**(§A.5 / Prop 1.5),本日志前版本误把它直接纳入 $\mathcal{T}_{\text{umr}}$,**此处更正**。
- 因此 MP-QKD 的 prefactor **不**作为 $\mathcal{T}_{\text{umr}}$ **严格类内** 最佳 published 下界

**[THM, ZZWM22 Fig. 4]**(独立性陈述):$R_{\text{MP}}(\eta) \sim c_{\text{MP}} \sqrt{\eta}$ with $c_{\text{MP}} \gtrsim c_{\text{PM}}$(but MP-QKD ∈ 扩展 $\mathcal{T}_{\text{umr}}^+$(允许跨轮),not strict $\mathcal{T}_{\text{umr}}$)

### B.5 $\mathcal{T}_{\text{umr}}$ 当前最佳下界(**v5 口径修正**)

区分**严格 $\mathcal{T}_{\text{umr}}$**(per-round only,符合 PROSPECTUS S1)与**扩展 $\mathcal{T}_{\text{umr}}^+$**(允许跨轮 pairing,MP-QKD 归此类):

**严格 $\mathcal{T}_{\text{umr}}$ 已发表最佳下界**(TF-QKD + PM-QKD 族,不含 MP-QKD):

$$R_{\text{LB}}(\mathcal{T}_{\text{umr}}^{\text{strict-sym}}; \eta) \geq c_{\text{best-strict}} \sqrt{\eta}, \quad c_{\text{best-strict}} \approx 0.2 \text{(from PM-QKD / SNS-TF)}$$

**扩展 $\mathcal{T}_{\text{umr}}^+$ 已发表最佳下界**(含 MP-QKD):

$$R_{\text{LB}}(\mathcal{T}_{\text{umr}}^{+\text{-sym}}; \eta) \geq c_{\text{best-ext}} \sqrt{\eta}, \quad c_{\text{best-ext}} \approx 0.3 \text{(from MP-QKD)}$$

两个区间 **[SYN,from multiple TF/PM/MP publications]**。

准确数字须由 Sub-Q2 的 Pareto 前沿扫描锁定(Phase 1 工作)。Phase 0 M4B 数值验证 TF-QKD prefactor。**注:所有后续 FINDINGS / 报告引用应明示使用哪个 $\mathcal{T}_{\text{umr}}$ 版本**。

### B.6 Scaling 层面 gap = 0(**v5 限界**)

对比 Log 04 命题 4.3(上界 scaling $O(\sqrt{\eta})$,**[SYN / CONJ]** 级,依赖未 lemma 化的 untrusted-relay 继承)与本日志 B.2(下界 scaling $O(\sqrt{\eta})$,**[THM]** 级):

$$\text{scaling gap} = O(\sqrt{\eta}) - O(\sqrt{\eta}) = 0 \quad \text{(at [SYN] level,放宽 bosonic-asymptotic 下)}$$

**重要限界**(vs v1):
- 本结论**只在放宽版 $\mathcal{T}_{\text{umr}}^{\text{bosonic-asym}}$ 下**([FINDINGS.md v2 §0](FINDINGS.md) 范围),**不**覆盖 PROSPECTUS §3.1 H4(finite-dim) / H5(composable) / H6(DV 严格意义)
- 继承 Log 04 上界 [SYN/CONJ] 分级,**非** [COROLLARY]
- 对 PROSPECTUS 主问题"情况 A 成立"是 **[SYN] 级支持**,不是 [THM] 级证成

### B.7 可能破坏上述结论的假设

为 V1/V3 留下 checklist:

1. **pure-loss 假设的偏离**:实际信道有小量去相干/相位噪声时,PLOB/Pirandola19 上界仍然是"$E_R$ computable"类定理,but 具体 $E_R$ 可能不是 $-\log_2(1-\eta)$ —— **此时上下界的 scaling 是否还同阶?** 预期是 [SYN]-yes(噪声只是 prefactor 的下调,不改 scaling),V3 要验证。

2. **"$\mathcal{T}_{\text{umr}}$ 跨轮 pairing" 的影响**:MP-QKD 允许跨轮。是否跨轮机制能突破 $\sqrt{\eta}$ 上界?—— 我的记忆中 MP-QKD **仍然是 $\sqrt{\eta}$**(原论文明确),上界 Log 04 定理 4.1 对 multi-round 协议也成立(因为 capacity 定义本身是 $\limsup_{n \to \infty}$)。V1 要核对定理 4.1 的"每轮 vs 跨轮"鲁棒性。

3. **"有限 Fock 截断" 的影响**:$\mathcal{N}_\eta$ 的 LOCC-simulation 严格需要无穷维 Fock;有限截断可能引入小修正。数值上影响 prefactor,不影响 scaling。[SYN,Phase 0 M4B 数值验证可视)。

---

## C. 本日志的已证命题(**v5 修订**)

**命题 5.1**(TF-QKD / PM-QKD / SNS-TF ∈ 严格 $\mathcal{T}_{\text{umr}}$;MP-QKD ∈ 扩展 $\mathcal{T}_{\text{umr}}^+$)

- **严格 $\mathcal{T}_{\text{umr}}$**(per-round announcement,符合 PROSPECTUS §3.1 S1):TF-QKD, PM-QKD, SNS-TF-QKD。**[THM, by construction]**
- **扩展 $\mathcal{T}_{\text{umr}}^+$**(允许跨轮 pairing,**超出 S1 软约束范围**):MP-QKD 归此类;Log 01 §A.5 标为"近似属于 $\mathcal{T}_{\text{umr}}$"。**[THM, by construction]**
- v1 把 MP-QKD 并入严格 $\mathcal{T}_{\text{umr}}$ 是错误,本版本更正。

**命题 5.2**(TF 族可达 $\sqrt{\eta}$)TF-QKD 达 $R_{\text{TF}}(\eta) = c_{\text{TF}} \sqrt{\eta}$,$c_{\text{TF}} > 0$. **[THM, Lucamarini18 Eq. 2-3 + Fig. 2]**

**命题 5.3**(放宽 bosonic-asym 下 scaling gap 消失,**[SYN]**)在 $\mathcal{T}_{\text{umr}}^{\text{bosonic-asym}}$(FINDINGS v2 §0.2 定义)下,上界(Log 04 Cmd 4.1,**[SYN / CONJ]**)与下界(本日志 Cmd 5.2,**[THM]**)scaling 同阶 $\sqrt{\eta}$。

**重要限界**(vs v1):
- 本命题分级为 **[SYN]**,非 [COROLLARY](v1 过分)
- 只在放宽 bosonic-asymptotic 子问题下有效,**不**覆盖 PROSPECTUS §3.1 原始 H4/H5/H6
- 严格化依赖 Sub-Q3 Phase 2 把 Log 04 Cmd 4.1 的 untrusted-relay 继承升到 [THM] 级

**命题 5.4**(Prefactor 区间,**按严格 / 扩展 $\mathcal{T}_{\text{umr}}$ 分开**,**[SYN]**)

- 严格 $\mathcal{T}_{\text{umr}}$(不含 MP-QKD):$c_{\text{strict}} \approx 0.2$(PM-QKD / SNS-TF)
- 扩展 $\mathcal{T}_{\text{umr}}^+$(含 MP-QKD):$c_{\text{ext}} \approx 0.3$
- 上界端:$c_{\text{upper}} = 1.4427$(Log 04 Cmd 4.2,[SYN / CONJ])
- **Prefactor gap**:严格 $\approx 1.2$,扩展 $\approx 1.1$(**未严格化,Phase 2 Pareto 工作**)
- v1 的"0.1-0.4 混合区间"是错用,此处更正按类别分开

**[元元命题]**:Log 05 整体得出的"scaling gap = 0"结论分级为 **[SYN]**(而非 [COROLLARY]),只在放宽 bosonic-asymptotic 子问题有效。

---

## D. 下一步依赖

Log 06:**gap 结构分析**,明确

(a) scaling gap = 0(情况 A 成立)
(b) prefactor gap 来源(是 上界松?下界优化空间?还是两端都松?)
(c) 对 PROSPECTUS Sub-Q4 的 "归因 A/B/C" 做初步映射 —— 但不得作 FINAL 结论,须经 V1-V4 验证

---

*Log 05 结束*
