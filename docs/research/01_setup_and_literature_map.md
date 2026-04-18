# Log 01:设置与文献地图

**日期**:2026-04-19
**子任务**:在开始数学推导之前,精确定位我们的拓扑在文献中的位置,列出可用上下界工具。

---

## A. 本日志的子问题

PROSPECTUS §1 的主问题不是抽象的 QKD 容量问题,而是非常具体的**拓扑约束**。我先精确陈述:

**研究对象拓扑**(以下称 $\mathcal{T}_{\text{umr}}$,Untrusted Measurement Relay 的缩写):

- 两个终端节点 Alice、Bob,各持本地经典+量子寄存器(**无量子存储**:发射后本地信号寄存器不再保留,PROSPECTUS §3.1 H2)
- 一个**中间节点** Charlie(测量站),位置可在 Alice 与 Bob 之间任意(工程上常在中点)
- Charlie 只做**测量**,不做纠缠生成、不做纠缠交换(禁止纠缠态共享,PROSPECTUS §3.1 H1)
- Alice ↔ Charlie 的量子信道是**纯损耗玻色信道**,透过率 $\eta_A$
- Bob ↔ Charlie 的量子信道是**纯损耗玻色信道**,透过率 $\eta_B$
- 端到端透过率(若直接通信)$\eta_{AB} = \eta_A \cdot \eta_B$(乘性损耗)
- Charlie **不可信**:可以被 Eve 控制或替换;Alice/Bob 只信任 Charlie 的**经典宣告统计**是可以被他们验证的(via 诱饵态或双方 POVM 统计),但**不信任**Charlie 的量子操作
- 载体:**离散变量**(光子偏振 / 时间箱 / 相位),离散基选择

**研究问题**:$\mathcal{T}_{\text{umr}}$ 拓扑下,渐近 secret-key rate $R^\infty(\eta_A, \eta_B)$ 的紧上界 $C(\eta_A, \eta_B)$ 是什么标度?

对称情形 $\eta_A = \eta_B = \sqrt{\eta_{AB}}$(Charlie 置于中点),问题变为 $C(\eta_{AB})$ 的标度。

---

## B. 工作草稿 / 思考过程

### B.1 为什么这个拓扑重要

在 QKD 文献中,点对点 Alice-Bob 直接通信有 **PLOB 界**(Pirandola 2017):

$$R \leq C_{\text{PLOB}}(\eta) = -\log_2(1 - \eta) \approx 1.4427\,\eta \quad (\eta \to 0)$$ **[THM, PLOB17 Thm. 5]**

这是**对任何点对点协议的 secret-key capacity 紧上界**。BB84 族(单光子 prepare-measure)和 MDI-QKD(两光子 Bell measurement)都在这个界以下,且两者都只能达到 $O(\eta)$ 或 $O(\eta^2)$(MDI 因为需要双光子 coincidence)。

TF-QKD 2018(Lucamarini et al.)的突破性在于:通过 Charlie 处的**单光子干涉**,实现了

$$R_{\text{TF}} \sim O(\sqrt{\eta})$$ **[THM, Lucamarini18 Eq. 2-3]**

这比 PLOB 界在 $\eta \to 0$ 时**大得多**(因为 $\sqrt{\eta} \gg \eta$ 对 $\eta < 1$)。

**关键问题**:如何可能? 答案是:**TF-QKD 不是点对点协议**。它用了 untrusted measurement relay。PLOB 界不约束它。

### B.2 这个"悖论"的解决

TF-QKD **不违反** PLOB,因为 PLOB 针对的是 Alice → (单一信道 $\eta_{AB}$) → Bob。TF-QKD 的两段信道 $\eta_A, \eta_B$ **每段** 都受 PLOB 约束:

$$R \leq \min\!\big( C_{\text{PLOB}}(\eta_A),\, C_{\text{PLOB}}(\eta_B) \big)$$ **[SYN,来自 min-cut 论证]**

对 $\eta_A = \eta_B = \sqrt{\eta_{AB}}$,有 $C_{\text{PLOB}}(\sqrt{\eta_{AB}}) \approx 1.44\sqrt{\eta_{AB}}$,确实给出 $O(\sqrt{\eta})$ 的量级上界。

**这就是我们要的上界的第一形**。下面要严谨化。

### B.3 拓扑中的关键区分

在 $\mathcal{T}_{\text{umr}}$ 下,Charlie 的**"untrusted measurement only"**身份让这个拓扑不同于:

1. **Trusted relay**(信任中继):Charlie 可以做 key 的生成/存储/转发。此时 Alice-Charlie 和 Charlie-Bob 各自独立做 QKD,端到端 key 通过 Charlie 本地转发。Capacity 可以用两段 PLOB capacity 的直接组合(Pirandola 2019 网络 capacity 理论)。
2. **Quantum repeater**(量子中继):Charlie 有量子存储 + 纠缠交换,能把 PLOB 的 $\eta$ 依赖退化为更弱的依赖(如 $\eta$ vs $\log(\eta)$)。**违反 PROSPECTUS §3.1 H2**,不在本研究范围。
3. **Measurement-device-independent (MDI)**:Charlie 做 Bell 态测量,rate $\sim O(\eta^2)$(因为两光子 coincidence)。MDI 是 $\mathcal{T}_{\text{umr}}$ 的一个特例(离散变量 + 贝尔态测量)。
4. **Twin-Field (TF)-QKD**:Charlie 做单光子干涉测量(single-click),rate $\sim O(\sqrt{\eta})$。也是 $\mathcal{T}_{\text{umr}}$ 的特例。
5. **Mode-Pairing (MP)-QKD**:Charlie 做单光子测量 + 跨轮 pairing,rate $\sim O(\sqrt{\eta})$。**注意**:MP-QKD 严格讲要求跨轮 announcement,PROSPECTUS §3.1 S1 的软约束允许 Phase 0 覆盖。

TF-QKD 在 $\mathcal{T}_{\text{umr}}$ 中是**已知最好**的构造性下界。问题:还能更好吗?

### B.4 两个方向的"更好"

"更好"有两种可能:

**(i) 改进 scaling**:存在协议使 $R \sim \eta^\alpha$,$\alpha < 1/2$?

**(ii) 改进 prefactor**:在 $R = c \cdot \sqrt{\eta}$ 这个 scaling 下,找到 $c > c_{\text{TF}}$?

**关键观察**:这两者分别对应 PROSPECTUS 的情况 B 和情况 A 内的 "prefactor gap"。情况 C(有上界但不可达)对应"紧 scaling 上界 $> c \sqrt{\eta}$ 但没有协议能到"。

### B.5 从文献记忆推断的初步判断

**我从训练语料中的记忆**(须在后续 Log 中验证):

- **PLOB 点对点在 $\mathcal{T}_{\text{umr}}$ 对两段分别应用是合法的**(min-cut 原理;Pirandola 2019 应有明确陈述)。
- **squashed entanglement 上界** $E_{\text{sq}}$(TGW14)给出的上界在 $\mathcal{T}_{\text{umr}}$ 下比 PLOB 严格(更小),也给 $O(\sqrt{\eta})$ scaling。
- **TF-QKD 的 $\sqrt{\eta}$ 是"重复器式"结构的 fundamental limit**。Pirandola 等多个作者的综述讨论 "repeater-less bound" 时经常说:无存储无中继,$\sqrt{\eta}$ 是**repeaterless** 极限(在单中继的含义下,单中继的最优 scaling)。

**初步判断**:情况 A **很可能**成立(scaling 上 $\sqrt{\eta}$ 紧);真正开放的是 prefactor 与 specific-topology 的紧度。

但这是 [SYN] 级判断,不是 [THM]。下面日志要把它推到 [THM] 级或明确承认只能到 [SYN] 级。

### B.6 本研究必须克服的三个技术难点

1. **untrusted 拓扑的 converse 证明的精确形式**:PLOB 是点对点,Pirandola 2019 的网络版本要精确引用。
2. **定义 "secret-key capacity" 的不同版本**:Private capacity $P$、Two-way assisted capacity $K^{\leftrightarrow}$、LOCC-assisted distillation,不同文献不同约定,不能乱引。
3. **$\sqrt{\eta}$ scaling 的"tight"究竟什么意思**:是对任意允许的操作集合吗(包括跨轮 memory)?还是只对 per-round + no-memory? PROSPECTUS §3.1 H2 限定了后者。

---

## C. 本日志的已证命题

**命题 1.1**(拓扑定义)$\mathcal{T}_{\text{umr}}$ 是由 §A 的硬约束列表精确定义的协议类族。**[定义性命题,非定理]**

**命题 1.2**(TF-QKD 属于 $\mathcal{T}_{\text{umr}}$)$\mathcal{T}_{\text{umr}}$ 包含 TF-QKD、SNS-TF-QKD、PM-QKD 作为具体协议实例。**[THM, by construction, Lucamarini18 + MZZ18]**

**命题 1.3**(MDI-QKD 属于 $\mathcal{T}_{\text{umr}}$)$\mathcal{T}_{\text{umr}}$ 包含所有 MDI-QKD 变体。**[THM, by construction]**

**命题 1.4**(点对点 BB84 **不属于** $\mathcal{T}_{\text{umr}}$)BB84 prepare-measure 是无中继 1-终端信道,不是 $\mathcal{T}_{\text{umr}}$。它是**更强**的参考(point-to-point),PLOB 直接约束它,且 BB84 实际只能 $O(\eta)$。

**命题 1.5**(MP-QKD 近似属于 $\mathcal{T}_{\text{umr}}$)MP-QKD 要求跨轮 announcement(PROSPECTUS §3.1 软约束 S1)。Phase 0 覆盖需要"per-round + pairing 封装"处理;这是 PROSPECTUS §4.3 已标注的裂缝,不影响本研究主问题的 scaling 判断。

---

## D. 下一步依赖

本日志确立了"我们要证明什么":$\mathcal{T}_{\text{umr}}$ 下 scaling $\sqrt{\eta}$ 的紧上界(情况 A 成立)。

**Log 02** 任务:精确陈述 PLOB Thm 5,识别其点对点假设,为 Log 03-04 的网络版本铺路。

**Log 03** 任务:陈述 Pirandola 2019 的网络 capacity(或等价的 min-cut 推论),直接应用到 $\mathcal{T}_{\text{umr}}$。

**Log 04** 任务:把 $\mathcal{T}_{\text{umr}}$ 的上界精确写成 $C_{\mathcal{T}_{\text{umr}}}(\eta_A, \eta_B)$。

**Log 05** 任务:TF-QKD 可达率的精确 prefactor(最好带诱饵态、有限探测器)。

**Log 06** 任务:scaling gap(预期:零)+ prefactor gap 定量化。

**FINDINGS** 任务:定结论。

---

*Log 01 结束*
