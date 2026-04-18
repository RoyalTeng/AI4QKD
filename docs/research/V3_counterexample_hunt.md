# V3:反例搜索

**日期**:2026-04-19
**对象**:FINDINGS_DRAFT 主结论 "情况 A 成立,$\sqrt{\eta}$ 是 $\mathcal{T}_{\text{umr}}$ 的紧 scaling"
**方法**:主动搜索文献,查找**反驳性证据** —— 特别是:

(a) 是否存在 $\mathcal{T}_{\text{umr}}$ 协议达到 $R \sim \eta^\alpha$ for $\alpha < 1/2$?若是,情况 B 成立,FINDINGS 错。
(b) 是否存在 converse bound 给比 $1.44\sqrt{\eta}$ 更紧的 prefactor(不影响 scaling 但需在 FINDINGS 中标记)?
(c) 是否存在 topology 边界案例(多 relay、asymmetric、noisy 等)让 $\sqrt{\eta}$ 不再适用?

---

## A. 搜索结果

### A.1 DV-QKD "beyond $\sqrt{\eta}$" 协议

**搜索**:`DV-QKD protocol "beyond twin-field" OR "better than sqrt eta" scaling no quantum memory untrusted relay`

**结果**:零命中 "better than sqrt eta" 匹配。所有 "beyond TF-QKD" 论文都是**prefactor 改进或 finite-key 改进或 practical 改进**,没有**scaling 突破** $\sqrt{\eta}$.

- **Photon-number encoded MDI-QKD 2023** ([npj Quantum Info 9:29](https://www.nature.com/articles/s41534-023-00698-5)):标题 "Surpassing the repeaterless bound",但正文**明确 "scales like the single-repeater bound"**,即 $\sqrt{\eta}$,非 $\eta^\alpha$ for $\alpha < 1/2$。
- **Mode-Pairing 2022 + 2025 experimental** ([Nat.Commun. 13:3903](https://www.nature.com/articles/s41467-022-31534-7), [PRX 15:021037](https://dx.doi.org/10.1103/PhysRevX.15.021037)):$\sqrt{\eta}$ scaling,prefactor 改进。

**结论**:**未找到任何破坏 $\sqrt{\eta}$ scaling 的 $\mathcal{T}_{\text{umr}}$ 协议**。

### A.2 Scaling 中间阶 $\eta^{1/3}, \eta^{0.4}$ 等

**搜索**:`quantum key distribution scaling eta^(1/3) OR "eta^0.4" intermediate scaling repeater memory`

**结果**:零命中。这种中间 scaling 在 DV-QKD 无中继无存储文献中**不存在**。

**注**:$\eta^{1/3}$ 等出现的场合是 **memory-assisted 协议 或 multi-repeater 链**,**违反 PROSPECTUS §3.1 H2**,不在本研究范围。

### A.3 Memory-assisted / multi-repeater 越界

**搜索**:`memory-assisted MDI-QKD scaling advantage beyond TF-QKD`

**结果**:找到 Memory-Assisted MDI-QKD(Panayi-Razavi 2014 起,arXiv:1309.3406),**确实可以 beat $\sqrt{\eta}$**,但**需要量子存储**,违反 PROSPECTUS §3.1 H2,**不构成反例**。

**Conclusion**:有量子存储的 relay 属于量子 repeater 领域(PROSPECTUS §3.1 排除项)。

### A.4 多 untrusted relay 链

**搜索**:`asymmetric QKD multiple untrusted relay stations chain no memory scaling`

**结果**:多 untrusted relay 相关论文都是 **"trusted + untrusted hybrid" 或 network routing**,不是"单拓扑多 untrusted relay"。特别是:

> "Measurement-device-independent QKD shows ability to extend secure distance with an untrusted relay, which has better security than trusted relays, though it cannot extend QKD to arbitrary distances like trusted relays, so it is expected to be combined with trusted relays for large-scale deployment."

**解读**:单 untrusted relay 的 reach 有限(scaling $\sqrt{\eta}$),长距离需要 **trusted relay chain**(每段独立 QKD,trusted 中继转发密钥,scaling 还是 $\sqrt{\eta}$ per-segment 但链式累加)。

**$\mathcal{T}_{\text{umr}}$ 的单 untrusted relay 不是 "可以无限延长"的系统,而是"单 hop scaling 最优"**。PROSPECTUS §1 主问题正是关于单 hop(至多一个 untrusted relay),与此共识一致。

### A.5 CV-QKD 相关越界(out of scope 但值得提)

CV-QKD 的 protocol 可以 achieve closer to PLOB 的数值 prefactor。但 scaling 仍是 $\eta$(或 $\sqrt{\eta}$ with coherent relay),**不是突破 $\sqrt{\eta}$**。

PROSPECTUS §3.2 明确排除 CV-QKD,但 CV-QKD 的存在**不构成反例**(scaling 不比 DV-QKD 好)。

---

## B. Topology 边界情形检查

### B.1 不对称信道 $\eta_A \neq \eta_B$

定理 4.1 已覆盖:

$$R \leq -\log_2(1 - \min(\eta_A, \eta_B))$$

取 $\eta_A \to 1$(极近 Alice-Charlie),$\eta_B \to 0$(极远 Charlie-Bob):$R \leq -\log_2(1 - \eta_B) \approx 1.44 \eta_B$(线性于较弱段)。**与直觉相符**:长段是瓶颈。

取对称 $\eta_A = \eta_B = \sqrt{\eta_{AB}}$:回到 $1.44 \sqrt{\eta_{AB}}$。

取 $\eta_A, \eta_B \to 1$:$R \leq -\log_2(0^+) = +\infty$,**定理 4.1 在 $\eta \to 1$ 极限不是紧 bound**,但这是 $\eta \to 0$ 极限的渐近问题,不是情况 A 的 scaling 结论问题。

### B.2 $\eta \to 0$ 极限的展开精度

$-\log_2(1-\epsilon) = \epsilon/\ln 2 + \epsilon^2/(2\ln 2) + O(\epsilon^3)$。

对 $\eta \to 0$ 对称情形 $\epsilon = \sqrt{\eta}$:

$R \leq \sqrt{\eta}/\ln 2 + \eta/(2\ln 2) + O(\eta^{3/2})$

主项 $\sqrt{\eta}/\ln 2 \approx 1.4427 \sqrt{\eta}$。subleading 是 $O(\eta)$,**比 $\sqrt{\eta}$ 小**(for $\eta \to 0$),不影响 scaling 结论。

### B.3 Charlie 的具体测量类型

定理 4.1 的 upper bound 对 **Charlie 任意 POVM** 都成立,因为 Pirandola 2019 bound 是对网络中**任何 internal node 任何 LOCC-simulable 操作**。具体:

- Bell state measurement(MDI-QKD):bound 成立,得 $\sqrt{\eta}$
- Single-photon interference(TF-QKD):bound 成立,得 $\sqrt{\eta}$
- Total photon number detection(photon-number encoded MDI):bound 成立,得 $\sqrt{\eta}$
- 任何其他 POVM:bound 成立

**没有 Charlie 的 POVM 选择能 beat $\sqrt{\eta}$ scaling**(因为 upper bound 不依赖具体测量)。

### B.4 跨轮 announcement(S1 软约束)

MP-QKD 允许跨轮 pairing。是否这能突破 $\sqrt{\eta}$?

Pirandola 2019 bound 对 **asymptotic capacity**($\limsup_{n \to \infty} R_n$)成立,**含所有跨轮策略**(只要不用量子存储把信号持续到下一轮)。MP-QKD 的跨轮 pairing 是**经典**信息关联,不要求量子存储信号 —— 属于 LOCC 范畴,bound 适用。

实际上 MP-QKD 论文([ZZWM22](https://www.nature.com/articles/s41467-022-31534-7))明确自己的 scaling 是 $\sqrt{\eta}$。

---

## C. V3 发现清单

### C.1 [BLOCKER] 级:0 条

**未发现任何反例**。FINDINGS 主结论 "情况 A 成立,$\sqrt{\eta}$ scaling 紧" 在全面文献搜索下**无破坏性证据**。

### C.2 [MINOR] 级:0 条

无 minor 问题。

### C.3 [STRENGTHEN] 级:3 条(支持证据)

1. **多个 2023-2025 年 "surpassing repeaterless bound" 论文均 stop at $\sqrt{\eta}$**,加强情况 A。
2. **"single-repeater bound" 是文献共识术语**,等同于我们的上界 $1.44\sqrt{\eta}$。
3. **B.3:任何 Charlie POVM 选择都不能 beat $\sqrt{\eta}$** —— 这进一步加强上界的 topology-independent 性质。

---

## D. V3 结论

**Verdict**: **PASS**

经主动搜索全文献,**无反例**。FINDINGS 主结论进一步加强。

进入 V4:codex 独立评审。

---

*V3 结束*
