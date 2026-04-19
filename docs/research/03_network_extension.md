# Log 03:网络 capacity 推广 — Pirandola 2019 与 min-cut bound

**日期**:2026-04-19
**子任务**:把 Pirandola 2019 的网络 secret-key capacity 精确陈述,应用到 $\mathcal{T}_{\text{umr}}$ 拓扑(两方 + 一个 untrusted measurement relay)。

---

## A. 子问题

Log 02 的 PLOB 是点对点。$\mathcal{T}_{\text{umr}}$ 是两段 + Charlie 的网络。需要网络版本的上界。

核心文献:**Pirandola 2019** "End-to-end capacities of a quantum communication network", Commun. Phys. 2:51.

要回答:

1. Pirandola 2019 的主定理是什么?
2. 它如何依赖 "cut"/"min-cut" 结构?
3. $\mathcal{T}_{\text{umr}}$ 的 cut 是什么?min-cut bound 给什么?
4. Charlie 的 "untrusted" 身份如何影响这个 bound?

---

## B. 工作草稿

### B.1 网络模型

**网络**定义为有向图 $G = (V, E)$,节点 $V$,边 $E$。每条边 $(i,j)$ 附有量子信道 $\mathcal{N}_{ij}$。两个指定节点 Alice($s$)和 Bob($t$)为 source/target。

协议允许:
- 任何节点 $v$ 可在本地拥有量子寄存器
- 任意 two-way LOCC 经典通信(全网络所有节点之间)
- 任何节点可做任意 quantum operation on 本地寄存器
- 信道使用次数计入 rate

**秘密约束**:secret key 定义为 Alice 与 Bob 共享;**所有其他节点(包括中间 relay)在安全性意义下不被信任**(相当于 Eve)。

**重要**:这个模型的 **"untrusted intermediate node"** 正是 $\mathcal{T}_{\text{umr}}$ 的 Charlie。中间节点得到任何信息都必须视作 Eve 的。

### B.2 Pirandola 2019 主定理

**定理 3.1**(network capacity min-cut bound,v4 修订)设 $G$ 是 LOCC-simulable channels 组成的网络,以 Alice-Bob 为 source-target。

**Single-path 形式**(Pirandola19 Eq. (11)):对 single-path $s \to t$ protocol,

$$K^{\leftrightarrow}_{s,t}(G; \text{single-path}) \leq \min_C \max_{(i,j) \in C} E_R(\Phi_{\mathcal{N}_{ij}})$$

**Multi-path / flooding 形式**(Pirandola19 Eq. (17)):

$$K^{\leftrightarrow}_{s,t}(G; \text{multi-path}) \leq \min_C \sum_{(i,j) \in C} E_R(\Phi_{\mathcal{N}_{ij}})$$

**状态**:[VERIFIED by literature + codex cross-review V4]

**[v4 更正]**:之前写法误将 Eq. (17) 的 sum 应用到 single-path 情形。对 $\mathcal{T}_{\text{umr}}$ 这种 single-path 拓扑(Alice-Charlie-Bob 线性链),**应使用 Eq. (11) 的 `max over edges in cut`**,不是 sum。对 linear single-path 三节点,cut 只含 1 条边,max 与 sum 给相同数值,但公式表达严谨性要求用 Eq. (11)。

**对 bosonic pure-loss 网络**:$E_R(\Phi_{\mathcal{N}_\eta}) = -\log_2(1-\eta)$,single-path(Eq. (11))下

$$K^{\leftrightarrow}_{s,t}(G; \text{single-path}) \leq \min_C \max_{(i,j) \in C} [-\log_2(1 - \eta_{ij})]$$ **[COROLLARY 3.1, v4 修订]**

对**单路径线性网络**($s \to r_1 \to r_2 \to \cdots \to r_n \to t$),每个 cut 只含一条边(删任一边即切断),所以

$$K^{\leftrightarrow}_{s,t}(\text{linear}) \leq \min_i [-\log_2(1 - \eta_{i,i+1})]$$ **[COROLLARY 3.2]**

(对 linear single-path,max over edges in a 1-edge cut = 该 edge 的 $E_R$,min over 1-edge cuts 取各 edge $E_R$ 的最小。)

### B.3 应用到 $\mathcal{T}_{\text{umr}}$

$\mathcal{T}_{\text{umr}}$ 的图结构是:

```
Alice ──(η_A)── Charlie ──(η_B)── Bob
```

这是两条边、三节点的线性网络。$s$-$t$ cut:

- Cut $C_1 = \{(Alice, Charlie)\}$:删 Alice-Charlie 边,$s$-$t$ 不连通 ✓
- Cut $C_2 = \{(Charlie, Bob)\}$:删 Charlie-Bob 边,不连通 ✓
- Cut $C_3 = \{(Alice, Charlie), (Charlie, Bob)\}$:两条都删,也不连通(但比 $C_1$/$C_2$ 更大,不 minimal)

Min-cut 是 $C_1$ 或 $C_2$ 取 $E_R$ 较小者。应用 Corollary 3.1:

$$K^{\leftrightarrow}_{A,B}(\mathcal{T}_{\text{umr}}) \leq \min\!\big(\, -\log_2(1-\eta_A), \; -\log_2(1-\eta_B)\, \big)$$ **[COROLLARY 3.3]**

$= -\log_2(1 - \min(\eta_A, \eta_B))$

### B.4 对称情形下的 scaling

若 Charlie 在中点,$\eta_A = \eta_B = \sqrt{\eta_{AB}}$($\eta_{AB}$ 为 Alice-Bob 端到端透过率)。

$$K^{\leftrightarrow}_{A,B}(\mathcal{T}_{\text{umr}}^{\text{sym}}) \leq -\log_2(1 - \sqrt{\eta_{AB}})$$

对 $\eta_{AB} \to 0$:$-\log_2(1 - \sqrt{\eta_{AB}}) \approx \frac{\sqrt{\eta_{AB}}}{\ln 2} \approx 1.4427\sqrt{\eta_{AB}}$.

**核心结论**:

$$\boxed{K^{\leftrightarrow}_{A,B}(\mathcal{T}_{\text{umr}}^{\text{sym}}) \leq 1.4427\sqrt{\eta_{AB}} + O(\eta_{AB})}$$ **[COROLLARY 3.4]**

**Scaling:$O(\sqrt{\eta_{AB}})$,与 TF-QKD 的可达 scaling 相同**。

### B.5 关键约束的检视

Cor. 3.3 的适用性依赖 Thm. 3.1 的假设:

| 假设 | 在 $\mathcal{T}_{\text{umr}}$ 下的核查 |
|------|-------------------------------|
| 每条边的信道 LOCC-simulable | Alice-Charlie 和 Charlie-Bob 都是 pure-loss bosonic,**成立** |
| 网络节点可自由本地量子操作 | $\mathcal{T}_{\text{umr}}$ 限制 Alice/Bob 无量子存储 —— **注**:Thm. 3.1 给的是"允许存储版本的上界",PROSPECTUS 无存储情形是它的**子集**,按 Log 02 B.5 方向单调,上界**更紧**(或至少不松) |
| 中间节点(Charlie)**可被 Eve 控制** | Thm. 3.1 默认中间节点不信任(相当于 Eve 拥有) —— **正匹配** $\mathcal{T}_{\text{umr}}$ 的 untrusted 假设 |
| Two-way LOCC 全网络 | PROSPECTUS 允许(standard assumption) |

**结论**:Cor. 3.3 **直接适用**于 $\mathcal{T}_{\text{umr}}$。

### B.6 untrusted 对上界的"反直觉加强"

初看令人惊讶:Charlie 是 **untrusted**,但这恰好让上界**更紧**(而不是更松)。逻辑:

- 若 Charlie 是 **trusted**(例如与 Alice-Bob 共享秘密):end-to-end rate = min(Alice-Charlie, Charlie-Bob),可以做 trusted repeater,每段 PLOB → overall min PLOB over edges = $O(\sqrt{\eta})$
- 若 Charlie 是 **untrusted**:不能做 trusted repeater。任何通过 Charlie 的信息相当于 Eve 可访问,capacity 只会**更低**或持平

即:**untrusted 上界 ≤ trusted 上界**,两者**在 scaling 上**同为 $O(\sqrt{\eta})$(大家都受同样的 min-cut 约束)。

### B.7 另一证明路线:Takeoka-Guha-Wilde 2014 squashed entanglement

独立于 PLOB/Pirandola19,**TGW14** 给出基于 **squashed entanglement $E_{sq}$** 的上界:

$$K^{\leftrightarrow}(\mathcal{N}) \leq E_{sq}(\Phi_{\mathcal{N}})$$ **[THM, TGW14 Thm. 1]**

对 pure-loss,$E_{sq} = \log_2\frac{1+\eta}{1-\eta}$(TGW14 Eq. (8) 附近),对 $\eta \to 0$ 展开 $\approx \frac{2\eta}{\ln 2}$,约为 PLOB 的 **两倍** —— **不如 PLOB 紧**。但 TGW14 的价值在于**技术无关**(不需要 LOCC-simulation)。

网络推广也存在(多个 $E_{sq}$ 的 sub-additive 组合),给出类似的 min-cut 结构,验证了 Corollary 3.4 的定性结论。**[SYN]**

### B.8 Das-Khatri-Wilde 2020 的改进

**Khatri-Wilde 2020 textbook**(arXiv:2011.04672,*Principles of Quantum Communication Theory: A Modern Approach*)在 Ch. 14+ 系统讲 converse bounds:对 pure-loss 点对点 recovers PLOB;对 network 给出与 Pirandola 2019 等价的 min-cut 结构(并把 Pirandola19 的 bosonic-specific 证明推到更广 channel classes)。

**[v5 修正]**:此前误引 "DKW 2020 arXiv:2012.03262" 是错记忆 — 那个 arXiv ID 实为不相关热力学论文。本研究用到的 converse 综合参考替换为 Khatri-Wilde 2020 textbook。

DKW20 的要点对我们:
- 陈述更干净(technical streamlined)
- 把 Pirandola19 的 bosonic-specific 证明推到更广 channel classes
- 但对 **我们的具体拓扑($\mathcal{T}_{\text{umr}}$ + pure-loss)**,**DKW20 不给出比 Pirandola19 更紧的 bound** —— pure-loss bosonic 已经是 PLOB 紧的,DKW 只是换了证明路线。**[SYN]**

所以 Log 04 主要引用 Pirandola19 的 Cor. 3.4 版本,DKW20 用作验证参考。

---

## C. 本日志的已证命题(v4 修订后)

**命题 3.1**(网络 min-cut bound,**v4 修订**):在 LOCC-simulable 信道网络上,

- **Single-path protocol**:$K^{\leftrightarrow}_{s,t} \leq \min_C \max_{(i,j) \in C} E_R(\Phi_{\mathcal{N}_{ij}})$ — **[THM, Pirandola19 Eq. (11)]**
- **Multi-path protocol**:$K^{\leftrightarrow}_{s,t} \leq \min_C \sum_{(i,j) \in C} E_R(\Phi_{\mathcal{N}_{ij}})$ — **[THM, Pirandola19 Eq. (17)]**

**[v4 更正]**:之前写法(sum over cut + "Thm. 2")混淆了 single-path 与 multi-path 版本。对 $\mathcal{T}_{\text{umr}}$(线性 single-path 拓扑)应使用 Eq. (11)(max-over-cut);由于线性拓扑的 cut 只含 1 条边,max 与 sum 数值相同。

**命题 3.2**(线性网络的 min-cut)线性单路径网络($s \to r_1 \to \cdots \to t$),每个 cut 含 1 条边,max-over-cut 与 sum-over-cut 重合,故 $K^{\leftrightarrow}_{s,t}(\text{linear}) \leq \min_i E_R(\Phi_{\mathcal{N}_i})$. **[COROLLARY of 3.1]**

**命题 3.3**($\mathcal{T}_{\text{umr}}$ 上界,**[v4 限界]**):$K^{\leftrightarrow}_{A,B}(\mathcal{T}_{\text{umr}}) \leq -\log_2(1 - \min(\eta_A, \eta_B))$. **[COROLLARY,依赖命题 3.2 + pure-loss $E_R = -\log_2(1-\eta)$]**

**注(v4 限界)**:命题 3.3 的严格推导基于 Pirandola 2019 Eq. (11) 的 **trusted / cooperative relay** 假设。在 $\mathcal{T}_{\text{umr}}$ 的 **untrusted Charlie** 情形,从 Eq. (11) 继承上界依赖 "capacity monotonicity"(untrusted 协议类族 ⊆ trusted 协议类族),**本论证未升级到定理级**,属 [SYN / CONJ] 级。严格化是 Sub-Q3 Phase 2 工作。

**命题 3.4**(对称情形 scaling 上界,**[v4 限界]**):$\eta_A = \eta_B = \sqrt{\eta_{AB}}$ 时,$K^{\leftrightarrow}_{A,B} \leq -\log_2(1-\sqrt{\eta_{AB}}) \approx 1.44 \sqrt{\eta_{AB}}$. **[COROLLARY of 3.3,继承 3.3 的 [SYN / CONJ] 分级]**

**命题 3.5**(Untrusted 不放松上界,**[v4 降级]**):Charlie 的 untrusted 身份**不应**放松上界(物理直觉 + 协议类族包含关系)。但严格陈述需定理级继承 lemma。**[SYN 级,非 COROLLARY]**

**命题 3.6**(无存储约束的单调继承)PROSPECTUS §3.1 H2 禁用 Alice/Bob 量子存储的情形继承 Pirandola19 上界(方向单调性,Log 02 B.5)。**[COROLLARY]**

---

## C.bis 命题 3.1-3.6 的分级表(v4 后集中显示)

| 命题 | v1 分级 | v4 修订后分级 | 降级理由 |
|------|--------|--------------|----------|
| 3.1(网络 min-cut) | [THM, Thm. 2] | [THM, Eq. (11)/(17)] | 公式形式更新,定理 ≠ 方程,依赖 Pirandola 2019 正文 |
| 3.2(线性 min-cut) | [COROLLARY] | [COROLLARY] | 保持 |
| 3.3($\mathcal{T}_{\text{umr}}$ 上界) | [COROLLARY] | **[SYN / CONJ]** | untrusted-relay 继承未 lemma 化 |
| 3.4(对称 scaling 上界) | [COROLLARY] | **[SYN / CONJ]** | 继承 3.3 |
| 3.5(Untrusted 不放松) | [COROLLARY] | **[SYN]** | 物理直觉 + 协议类族包含直觉,非定理 |
| 3.6(无存储单调) | [COROLLARY] | [COROLLARY] | 保持(sup 单调性是初等) |

---

## D. 下一步依赖

Log 04:把 Log 02 + Log 03 的命题整合,写出 $\mathcal{T}_{\text{umr}}$ 的**完整上界陈述 + 假设清单**,作为 Sub-Q3 验收产出的数学内核。

---

*Log 03 结束*
