# Log 02:PLOB 2017 定理结构剖析

**日期**:2026-04-19
**子任务**:把 PLOB(Pirandola-Laurenza-Ottaviani-Banchi 2017,Nat. Commun. 8:15043)的主定理精确陈述,识别它的适用边界,为 Log 03-04 的网络版本推广铺路。

---

## A. 子问题

PLOB 给出了点对点 pure-loss 信道的 secret-key capacity 紧上界。本日志要回答:

1. 定理的**精确陈述**是什么?(包括 $\lim$ vs $\limsup$、私钥 vs 共享秘密等版本)
2. 定理的**关键假设**是什么?(点对点、pure-loss、LOCC)
3. 定理的**证明骨架**是什么?(以便判断哪些步骤在 $\mathcal{T}_{\text{umr}}$ 拓扑下还成立)
4. 这个定理对 $\mathcal{T}_{\text{umr}}$ 的直接 bearing?

---

## B. 工作草稿

### B.1 capacity 的精确定义

QKD 语境下的 "secret-key capacity" 有多个层级,容易混淆。按 PLOB17 + 后续文献的约定:

**定义 2.1**(两点 secret-key capacity,$K^{\leftrightarrow}$)给定一个量子信道 $\mathcal{N}: \mathcal{L}(\mathcal{H}_A) \to \mathcal{L}(\mathcal{H}_B)$,Alice 和 Bob 通过使用 $n$ 次 $\mathcal{N}$ 与任意 two-way LOCC(经典双向通信)生成长度为 $\ell$ 的密钥 $S$,满足:
- 安全性:存在与 Eve 几乎无关的理想密钥 $\tilde S$,$\| \rho_{SE}^{\text{prot}} - \tilde\rho_{SE} \|_1 \leq \varepsilon$
- 可靠性:Alice 与 Bob 的 key 除 $\varepsilon$ 误差外一致

$K^{\leftrightarrow}(\mathcal{N}) = \sup_{\text{protocols}} \limsup_{n \to \infty} \ell/n$。**[定义级]**

本定义中:

- Alice、Bob 共享 **unlimited classical two-way channel**(LOCC,标准假设)
- Eve 可以对 $\mathcal{N}$ 的环境做**任意 collective / coherent 攻击**
- 没有预共享秘密、没有量子存储于 Alice 和 Bob 的 required assumption —— 但 "no restriction on protocol" 允许 Alice/Bob 拥有本地量子存储(这个自由度在我们的 PROSPECTUS §3.1 H2 下**被去除**,后面要处理)

### B.2 PLOB Main Theorem

**定理 2.2**(PLOB 紧界)对 pure-loss bosonic channel $\mathcal{N}_\eta$(透过率 $\eta$),

$$K^{\leftrightarrow}(\mathcal{N}_\eta) = -\log_2(1 - \eta)$$ **[THM, PLOB17 Thm. 5 (numbered as Main Result)]**

等价表达:

$$K^{\leftrightarrow}(\mathcal{N}_\eta) = \log_2\frac{1}{1 - \eta}$$

渐近小 $\eta$ 展开:$-\log_2(1-\eta) = \frac{\eta}{\ln 2} + O(\eta^2) \approx 1.4427\, \eta + O(\eta^2)$.

**注释**:

- 这是**两侧相等**的结果:PLOB 既是 upper bound(converse)也是 achievable(direct)。
- Achievable 部分(lower bound $\geq -\log_2(1-\eta)$)由**reverse coherent information**类协议达到(可参考 García-Patrón-Cerf 2009 + Pirandola-Mancini-Braunstein-Vitali 2008 式结构),需要 continuous-variable 协议 + 量子存储 —— 对 DV-QKD **通常不可达**,但这不影响 upper bound 的适用性。
- **DV-QKD 单光子协议(BB84)只能达到 $R = O(\eta)$**,小 $\eta$ 时 PLOB 界给出的常数 $1.4427$ 比 BB84 的典型 prefactor(约 $0.5 \cdot \frac{1}{2}$ 对称基)大,说明 PLOB 对 DV-QKD 并非紧 —— 但 PLOB 是**任何允许协议**的上界,所以它仍然是**刚性约束**。

### B.3 证明骨架(用于后续推广)

PLOB 的证明核心是三步:

**Step 1**(LOCC-simulability of pure-loss channel)Pure-loss bosonic channel 满足 "teleportation simulation" 条件:

$$\mathcal{N}_\eta(\rho) = \mathcal{L}_{\text{BK}}(\rho \otimes \Phi_\eta)$$

其中 $\Phi_\eta$ 是 $\mathcal{N}_\eta$ 的 Choi 态,$\mathcal{L}_{\text{BK}}$ 是 Braunstein-Kimble teleportation(连续变量 LOCC)。**[THM, PLOB17 Eq. (4), originated in BDSW96 framework]**

**Step 2**(capacity bound by entanglement measure)对任何 LOCC-simulable channel,

$$K^{\leftrightarrow}(\mathcal{N}) \leq E_R(\Phi_\mathcal{N})$$

其中 $E_R$ 是 **relative entropy of entanglement** of Choi state。**[THM, PLOB17 Thm. 4]**

关键观察:$E_R$ 是 **entanglement monotone under LOCC**,而 LOCC-simulation 把信道使用转化为 LOCC on Choi state,故 $E_R$ 直接限 key rate。

**Step 3**(compute $E_R(\Phi_{\eta})$ for pure-loss)对 pure-loss 的 Choi 态,$E_R = -\log_2(1-\eta)$(解析可算)。

**综合**:$K^{\leftrightarrow}(\mathcal{N}_\eta) \leq -\log_2(1-\eta)$(converse),配合 achievable 等式成立。

### B.4 关键假设的地图

PLOB Main Theorem 成立的前提:

| 假设 | 角色 | 在 $\mathcal{T}_{\text{umr}}$ 下是否成立 |
|------|------|-----------------------------------|
| A1. 点对点单信道 $\mathcal{N}$ | 定义 $K^{\leftrightarrow}$ 的对象 | **不直接成立**:$\mathcal{T}_{\text{umr}}$ 有两段信道 + Charlie |
| A2. Two-way LOCC 自由 | 协议自由度 | 成立(PROSPECTUS 允许 classical channel) |
| A3. LOCC-simulation $\mathcal{N} = \mathcal{L}(\cdot \otimes \Phi)$ | Step 1 的核心 | **Charlie 的 POVM 不是 LOCC**,但 Alice-Charlie 和 Charlie-Bob 各自的信道是 |
| A4. Alice/Bob 可用 **量子存储** | 协议自由度(通常 capacity 定义允许) | **PROSPECTUS §3.1 H2 禁止**,所以即便 PLOB 类上界成立,其 achievability 对我们不重要 |
| A5. IID 集体攻击(或经 de Finetti 化简为 IID) | PLOB 证明风格 | 成立(标准假设) |

**结论**:PLOB 不能**直接**应用于 $\mathcal{T}_{\text{umr}}$,因为拓扑不同。但其**证明方法**(Step 1-3)的关键砌块(LOCC-simulation + $E_R$-monotone)可以迁移到**网络版本**,这是 Pirandola 2019 的工作,Log 03 要处理。

### B.5 为什么 A4 "no-memory" 不改变上界

PROSPECTUS 限制 Alice/Bob 无量子存储(仅 per-round),但 PLOB 是 **upper bound**(converse 方向),它对协议的限制越多,上界只能**更紧或同样**,不会更松。

直觉:去掉自由度(存储)只会让可达率**变低**。既然 PLOB 给的上界在"有存储" capacity 定义下成立,**在"无存储"限制下的 sup 也 ≤ PLOB 值**(因为 "无存储可达" ⊂ "有存储可达")。

**所以**:若某个 $C^{\text{umr}}(\eta_A, \eta_B)$ 是 $\mathcal{T}_{\text{umr}}$ 的上界,它也是**同一拓扑但允许存储**下的上界(**更强**);若是同一拓扑但允许存储下的上界,它也是**无存储**下的上界(**更弱**)。

方向:**无存储下的 sup ≤ 有存储下的 sup ≤ 同一拓扑允许存储的上界**。

这意味着:我们可以从"允许存储版本"得到的上界,**直接继承**到 PROSPECTUS 的无存储限制,而不需要额外修证明。

---

## C. 本日志的已证命题

**命题 2.1**(PLOB 主定理)对 pure-loss channel $\mathcal{N}_\eta$,$K^{\leftrightarrow}(\mathcal{N}_\eta) = -\log_2(1-\eta) \approx 1.44 \eta$.  **[THM, PLOB17 Thm. 5]**

**命题 2.2**(PLOB 证明骨架)可由三步骤(LOCC-simulation + $E_R$ bound + $E_R$ computation)独立验证;关键技术 "LOCC-simulation"可扩到多段 LOCC-simulable 信道复合。**[THM, PLOB17 §II]**

**命题 2.3**(方向单调性)对 $\mathcal{T}_{\text{umr}}$,无存储限制下的 $R$ 上界 $\leq$ 有存储限制下的上界。  **[COROLLARY from capacity sup 定义]**

**命题 2.4**(PLOB 不直接适用 $\mathcal{T}_{\text{umr}}$)PLOB Main Theorem 的"点对点单信道"前提与 $\mathcal{T}_{\text{umr}}$ 的"两段 + Charlie"拓扑不同,不可字面引用;需要网络版本(Log 03)。  **[COROLLARY,by definition of $\mathcal{T}_{\text{umr}}$]**

---

## D. 下一步依赖

Log 03:把 Pirandola 2019 "end-to-end capacity of a quantum network" 的结果精确陈述 —— 它用 **min-cut** 把网络 capacity 约化为 single-edge PLOB 的 min。

Log 03 核心问题:
- Pirandola 2019 定理 2 / 3 的精确陈述(network $E_R$ upper bound)
- "untrusted relay" 拓扑是否属于该定理覆盖范围
- 如果是:上界就是 $\min\!\big(C_{\text{PLOB}}(\eta_A), C_{\text{PLOB}}(\eta_B)\big)$

---

*Log 02 结束*
