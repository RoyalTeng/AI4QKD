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
| **Log 04 定理 4.1 对称上界** | $O(\sqrt{\eta})$ | $1.44$ | [COROLLARY] |

### B.3 PM-QKD 的特殊性

Ma-Zeng-Zhou 2018 的 PM-QKD 是 TF-QKD 的一个**变体**,使用 **phase-matching** 而非 time-bin:

- 相位被严格随机化后公开,只保留"相位差等于 $0$ 或 $\pi$"的轮次
- 同样是 single-photon 检测 at Charlie
- Prefactor 在理论上**优于**原始 TF-QKD(因为 phase matching 避免了 phase randomization 中的信息泄露)

**[THM, MZZ18 Fig. 3]**:$R_{\text{PM}}(\eta) = c_{\text{PM}} \sqrt{\eta}$ with $c_{\text{PM}} \approx 0.2 - 0.4$(数值区间,具体取决于 decoy state 优化)。

### B.4 MP-QKD 的提升

Zeng-Zhou-Wu-Ma 2022 的 MP-QKD 是进一步改进:

- 跨轮 pairing(PROSPECTUS §3.1 S1 软约束范围):把两个时刻 click 的 signal 配对,降低 phase stability 要求
- **理论 prefactor 更高**(数值约 $0.3$+),部分源于可以用更高强度 coherent state

**[THM, ZZWM22 Fig. 4]**:$R_{\text{MP}}(\eta) \sim c_{\text{MP}} \sqrt{\eta}$ with $c_{\text{MP}} \gtrsim c_{\text{PM}}$.

### B.5 $\mathcal{T}_{\text{umr}}$ 当前最佳下界

取文献已发表的 $\mathcal{T}_{\text{umr}}$ 协议中最好的 achievable rate:

$$R_{\text{LB}}(\mathcal{T}_{\text{umr}}^{\text{sym}}; \eta) \geq c_{\text{best-pub}} \sqrt{\eta}, \quad c_{\text{best-pub}} \approx 0.3 \text{ (conservative, empirical)}$$ **[SYN,from MP-QKD 22]**

准确数字须由 Sub-Q2 的 Pareto 前沿扫描锁定(Phase 1 工作)。Phase 0 的 M4B 数值验证能给 TF-QKD 数值 prefactor 到 5% 精度。

### B.6 Scaling 层面 gap = 0

对比 Log 04 命题 4.3(上界 scaling $O(\sqrt{\eta})$)与本日志 B.2(下界 scaling $O(\sqrt{\eta})$):

$$\boxed{\text{scaling gap} = O(\sqrt{\eta}) - O(\sqrt{\eta}) = 0}$$

**即:$\mathcal{T}_{\text{umr}}$ 拓扑下,$\sqrt{\eta}$ scaling 是紧的 — 上下界同阶。**

**这是对 PROSPECTUS 主问题情况 A 的强支持**。

### B.7 可能破坏上述结论的假设

为 V1/V3 留下 checklist:

1. **pure-loss 假设的偏离**:实际信道有小量去相干/相位噪声时,PLOB/Pirandola19 上界仍然是"$E_R$ computable"类定理,but 具体 $E_R$ 可能不是 $-\log_2(1-\eta)$ —— **此时上下界的 scaling 是否还同阶?** 预期是 [SYN]-yes(噪声只是 prefactor 的下调,不改 scaling),V3 要验证。

2. **"$\mathcal{T}_{\text{umr}}$ 跨轮 pairing" 的影响**:MP-QKD 允许跨轮。是否跨轮机制能突破 $\sqrt{\eta}$ 上界?—— 我的记忆中 MP-QKD **仍然是 $\sqrt{\eta}$**(原论文明确),上界 Log 04 定理 4.1 对 multi-round 协议也成立(因为 capacity 定义本身是 $\limsup_{n \to \infty}$)。V1 要核对定理 4.1 的"每轮 vs 跨轮"鲁棒性。

3. **"有限 Fock 截断" 的影响**:$\mathcal{N}_\eta$ 的 LOCC-simulation 严格需要无穷维 Fock;有限截断可能引入小修正。数值上影响 prefactor,不影响 scaling。[SYN,Phase 0 M4B 数值验证可视)。

---

## C. 本日志的已证命题

**命题 5.1**(TF-QKD ∈ $\mathcal{T}_{\text{umr}}$)TF-QKD 及其变体(PM,SNS,MP)满足 H1-H5,属于 $\mathcal{T}_{\text{umr}}$ 拓扑。**[THM, by construction]**

**命题 5.2**(TF-QKD 可达 $\sqrt{\eta}$)TF-QKD 达到 $R_{\text{TF}}(\eta) = c_{\text{TF}} \sqrt{\eta}$,$c_{\text{TF}} > 0$. **[THM, Lucamarini18 Eq. 2-3 + Fig. 2]**

**命题 5.3**(Scaling gap 为零)$\mathcal{T}_{\text{umr}}^{\text{sym}}$ 下,上界(Log 04 Cmd 4.3)与下界(Cmd 5.2)scaling 同阶 $\sqrt{\eta}$. **[COROLLARY]**

**命题 5.4**(Prefactor 区间)$0.1 \lesssim c_{\text{pub}} \lesssim 0.4$(已发表协议),$c_{\text{upper}} = 1.4427$(定理 4.1)。**Prefactor gap $\approx 1.1 - 1.3$**. **[SYN,from published TF/PM/MP numerics]**

---

## D. 下一步依赖

Log 06:**gap 结构分析**,明确

(a) scaling gap = 0(情况 A 成立)
(b) prefactor gap 来源(是 上界松?下界优化空间?还是两端都松?)
(c) 对 PROSPECTUS Sub-Q4 的 "归因 A/B/C" 做初步映射 —— 但不得作 FINAL 结论,须经 V1-V4 验证

---

*Log 05 结束*
