# V1:数学逻辑自审

**日期**:2026-04-19
**对象**:FINDINGS_DRAFT + Log 01-06 的推理链
**角色**:本轮我(Claude)**刻意扮演怀疑者**,逐条核查推理 —— 尝试**反驳自己**,找出漏洞。

**规则**:发现 [BLOCKER] 级问题即停止,回 Phase R。发现 [MINOR] 问题允许记录后继续。

---

## A. 自审清单(按 FINDINGS §1 的情况 A 结论逆向追溯)

结论链:

```
情况 A 成立
  ↓
命题 6.4 (scaling 上下界同阶)
  ↓
  ├── 命题 6.1 (scaling gap = 0)
  │     ↓
  │     ├── 命题 4.3 (上界 O(√η))
  │     │     ↓
  │     │     └── 命题 4.1 (定理 4.1,min-cut + PLOB 组合)
  │     │           ↓
  │     │           ├── 命题 3.1 (Pirandola19 Thm. 2)
  │     │           ├── 命题 2.1 (PLOB17 Thm. 5)
  │     │           ├── 命题 2.3 (方向单调性 — H5 无存储)
  │     │           └── 假设 H1-H6 (拓扑 + 信道 + 信任 + 协议自由度)
  │     │
  │     └── 命题 5.3 (下界 O(√η))
  │           ↓
  │           └── 命题 5.2 (TF-QKD Lucamarini18 Eq. 2-3)
  │
  └── 命题 6.2/6.3 (情况 B/C 被排除)
        ↓
        └── 命题 4.3 (同上)
```

我按这条依赖链从叶子往根逐条检查。

---

## B. 逐条核查

### B.1 命题 2.1(PLOB 主定理)

**陈述**:$K^{\leftrightarrow}(\mathcal{N}_\eta) = -\log_2(1-\eta)$ for pure-loss bosonic.

**核查**:

- 定理号 PLOB17 Thm. 5:**记忆中的编号**,准确度约 80%([?] 标记)。V2 文献核查必办。
- 两侧等式(既是 upper 又是 achievable):**记忆中 PLOB 主结果是双侧相等**,capacity 精确等于 $-\log_2(1-\eta)$。这一点在 PLOB17 abstract 有明确陈述。
- **Achievable 方向要求量子存储**(Alice/Bob 需要 CV 量子 repeater-like 协议,非 DV-QKD 可达)。对 $\mathcal{T}_{\text{umr}}$ 而言**只使用 upper bound 方向**,与 achievability 无关,不受 DV-QKD 限制影响。

**自审结论**:**无逻辑错误**,V2 需核对定理号。

### B.2 命题 2.3(方向单调性)

**陈述**:$\mathcal{T}_{\text{umr}}$ 的 **无存储 sup $\leq$ 有存储 sup $\leq$ 允许存储的上界**.

**核查**:

- 这是 **capacity sup 的单调性** —— 更强约束导致 sup 更小或等。直接从 sup 定义:
  - $K^{\text{no-mem}} := \sup_{\Pi \in \mathcal{P}_{\text{no-mem}}} R_\Pi$
  - $K^{\text{with-mem}} := \sup_{\Pi \in \mathcal{P}_{\text{with-mem}}} R_\Pi$
  - $\mathcal{P}_{\text{no-mem}} \subset \mathcal{P}_{\text{with-mem}}$,故 $K^{\text{no-mem}} \leq K^{\text{with-mem}}$。

**自审结论**:**无逻辑错误**,这是集合论初等推论。

### B.3 命题 3.1(Pirandola19 Thm. 2)

**陈述**:LOCC-simulable 网络上 end-to-end $K^{\leftrightarrow}_{s,t} \leq \min_C \sum_{(i,j) \in C} E_R(\Phi_{\mathcal{N}_{ij}})$.

**核查**:

- 定理编号 Pirandola19 Thm. 2:**记忆中**(可能为 Thm. 3),准确度约 70%([?])。V2 必办。
- 陈述形式:**记忆中**是 min-cut of $E_R$。逻辑上 min-cut 来自 max-flow / min-cut 原理,在**经典**网络是精确,**量子**网络是 entanglement measure 的可加性(at most)。对 LOCC-simulable 信道,$E_R$ sub-additive over channels in parallel,给出 min-cut upper bound(**但不一定紧**!)。
- **潜在问题**:min-cut bound 是否**紧**?对 $\mathcal{T}_{\text{umr}}$ 线性网络,只有一条 $s$-$t$ 路径,min-cut 就是较弱的那条 edge。这时 bound 应当 tight up to constants,因为单路径网络的上界由最弱边决定。—— 但这里 "tight" 指**scaling**,不指 prefactor。本研究只要 scaling,所以 min-cut bound 足够。

**自审结论**:**scaling 层面无逻辑错误**;prefactor 层面 min-cut 可能松,但 FINDINGS 只要 scaling 结论。V2 必核。

### B.4 命题 4.1(定理 4.1,$\mathcal{T}_{\text{umr}}$ 上界)

**陈述**:$R^\infty \leq -\log_2(1 - \min(\eta_A, \eta_B))$.

**核查 Step 1-5**(Log 04 B.2):

- **Step 1**(拓扑匹配):$\mathcal{T}_{\text{umr}}$ 是 Pirandola19 网络的实例。核查:是否 Pirandola19 模型允许**经典 broadcast from 中间节点**?—— Pirandola19 允许**all nodes including intermediate share two-way LOCC**,Charlie 可以经典广播。与 $\mathcal{T}_{\text{umr}}$ 的 classical announcement 对齐。**[ok]**
- **Step 2**(应用 Thm. 2):Pirandola19 Thm. 2 把网络 capacity 上界写成 min-cut of $E_R$。**[ok]**
- **Step 3**(线性网络的 cut 结构):Alice-Charlie-Bob 是两条边一条路径,cut 集合只有 $\{C_1, C_2\}$。**[ok]**
- **Step 4**(pure-loss $E_R = -\log_2(1-\eta)$):这是 PLOB17 的计算。**[ok, 从 Step 4 B.1 继承]**
- **Step 5**(H5 无存储单调继承):见 B.2。**[ok]**

**潜在 [BLOCKER]**:

- **Q**:Pirandola19 Thm. 2 的 "LOCC-simulable" 前提在 pure-loss bosonic 下严格成立吗?—— 是,Niset-Fiurášek-Cerf 2009 给出 CV teleportation 的 LOCC-simulation 构造。**[ok]**
- **Q**:Thm. 2 的证明是否对 "internal node is untrusted / semi-honest / honest-but-curious" 敏感?—— Pirandola19 定义 internal node 可以被 Eve 控制(worst case),这是我们 $\mathcal{T}_{\text{umr}}$ 的 untrusted 场景。但若 Charlie 必须执行具体协议(如 BSM、single-photon interference),它的操作是 fixed -- 这是 "operational constraint",可能让 cardinality 比最一般 untrusted 更紧。—— 我们取的是**最一般 untrusted**(让 Charlie 最多帮 Eve),上界最松,无 [BLOCKER]。

**自审结论**:**无 [BLOCKER],逻辑通顺**。

### B.5 命题 4.3(scaling $O(\sqrt{\eta})$)

**陈述**:对称 $\eta_A = \eta_B = \sqrt{\eta_{AB}}$,$R \leq 1.44 \sqrt{\eta_{AB}}$.

**核查**:

- $-\log_2(1 - \sqrt{\eta_{AB}}) = \frac{\sqrt{\eta_{AB}}}{\ln 2} + \frac{(\sqrt{\eta_{AB}})^2}{2\ln 2} + O(\eta_{AB}^{3/2}) \approx 1.4427 \sqrt{\eta_{AB}} + O(\eta_{AB})$。—— **展开正确**。
- $1/\ln 2 = 1/(0.6931...) = 1.4427$。**数值正确**。

**自审结论**:**无错误**。

### B.6 命题 5.2(TF-QKD $\sqrt{\eta}$ 可达)

**陈述**:Lucamarini18 构造性给出 $R_{\text{TF}} \sim c_{\text{TF}} \sqrt{\eta}$,$c_{\text{TF}} > 0$.

**核查**:

- 这是**全社区共识**,Lucamarini et al. 2018 Nature 论文的核心贡献。数百篇后续论文引用、重复、扩展这个结果。
- Scaling 为 $\sqrt{\eta}$ 的**物理来源**:单光子 transmitter-to-interference-site,透过率 $\sqrt{\eta_{AB}}$(单段),单光子探测概率 $\propto \sqrt{\eta_{AB}}$。
- 具体 prefactor 依 decoy state、探测器细节,但 $c_{\text{TF}} > 0$ 是**无争议**的。

**自审结论**:**无错误**。

### B.7 命题 6.2(情况 B 排除)

**陈述**:情况 B($\alpha < 1/2$ 可达)矛盾于命题 4.3.

**核查**:

- 命题 4.3 给 $R \leq 1.44 \sqrt{\eta}$ for all $\mathcal{T}_{\text{umr}}$ 协议。
- 若情况 B 成立,存在协议使 $R \sim c \eta^\alpha$ with $\alpha < 1/2$。对 $\eta \to 0$,$\eta^\alpha = \eta^{\alpha}$ 递减**比 $\sqrt{\eta}$ 慢**(因为 $\alpha < 1/2$,$\eta^\alpha > \sqrt{\eta}$ for small $\eta$)。
- 故 $R_{\text{情况B}} \sim \eta^\alpha > \sqrt{\eta} > 1.44 \sqrt{\eta} / k$ for some $k$ large enough... 等等,这里要小心。
- 若 $R \sim c \eta^\alpha$ 且 $\alpha < 1/2$,对 $\eta$ 足够小,$c \eta^\alpha > 1.44 \sqrt{\eta}$(因为 $\eta^\alpha / \sqrt{\eta} = \eta^{\alpha - 1/2} \to \infty$)。这违反上界。

**自审结论**:**逻辑正确**,情况 B 被严格排除。

### B.8 命题 6.4(情况 A 成立)

**陈述**:PROSPECTUS §1 主问题答案为情况 A。

**核查**:

- 情况 A 定义:$\sqrt{\eta}$ scaling 紧上界。
- 证据:上界 $\sqrt{\eta}$(命题 4.3),下界同阶 $\sqrt{\eta}$(命题 5.2)。—— **"紧上界"严格讲要求 $\limsup R / \sqrt{\eta} = c^\star > 0$ for some 最优协议**。我们已证 $\limsup R / \sqrt{\eta} \geq c_{\text{TF}} > 0$(Lucamarini18)和 $\limsup R / \sqrt{\eta} \leq 1.4427$(命题 4.3)。

**潜在 [MINOR]**:严格讲,"$\sqrt{\eta}$ 紧"意味着 $\sup_{\Pi} \lim_{\eta \to 0} R_\Pi(\eta)/\sqrt{\eta} = c^\star$ 存在且有限。我们只证了它**存在于 $[c_{\text{TF}}, 1.4427]$** 的区间,**没有证明 sup 存在或精确值**。

**自审裁定**:"情况 A 成立" 的陈述对应**标度层面 $\sqrt{\eta}$ 是答案的紧标度**,不要求精确 prefactor。这是 PROSPECTUS §1 情况 A 的**原始语义**("$\sqrt{\eta}$ 标度是紧上界"),符合。

**自审结论**:**无 [BLOCKER],有 [MINOR] 语义精化建议**(在 FINDINGS 中显式说明"紧"指 scaling 层面 tight,prefactor 开放)。

### B.9 FINDINGS_DRAFT §1.1 的"答案"陈述

**陈述**:"情况 A 成立(scaling 层面,[COROLLARY] 级确定性)"

**核查**:

- "情况 A 成立"与"scaling gap = 0"等价:✓
- "[COROLLARY] 级确定性":表明不是新定理,是已发表定理的合成。符合诚信红线 ✓
- "prefactor 开放":是情况 A 内部子问题,不动摇主结论 ✓

**自审结论**:**陈述精确,分级清楚**。

---

## C. 发现清单

### C.1 [BLOCKER] 级:**0 条**

无破坏 FINDINGS 主结论的逻辑问题。

### C.2 [MINOR] 级:**2 条**

1. **命题 6.4 的"紧"语义精化**(B.8):在 FINDINGS_FINAL 中显式说明 "$\sqrt{\eta}$ 紧" 指 scaling 层面,$c^\star$ 精确值未定(Phase 2-3 任务)。

2. **定理号 [?] 待核**(B.1、B.3):PLOB17 Thm. 5、Pirandola19 Thm. 2 的编号记忆准确度 70-80%,V2 必做原文核对。

### C.3 [SUGGESTION] 级:**1 条**

1. **扩展 Log 04 定理 4.1 的形式化**:加一条"假设 H5 的无存储继承"作为 Step 0,显式标出 PROSPECTUS §3.1 H2 的精确映射。(本轮不必回 Phase R,FINDINGS_FINAL 直接提。)

---

## D. V1 结论

**Verdict**: **PASS**(条件:V2 文献交叉核查解决 B.1/B.3 的定理编号)

主结论 "情况 A 成立"的**数学逻辑链**经自审无 [BLOCKER]。V1 完成,可进入 V2。

---

*V1 结束*
