# Log 06:Gap 结构分析 — scaling 级 vs prefactor 级

**日期**:2026-04-19
**子任务**:把 Log 04(上界)与 Log 05(下界)并列,分析 gap 的定量形状,为 PROSPECTUS Sub-Q4 的归因 A/B/C 做初步映射。

---

## A. 子问题

PROSPECTUS Sub-Q4 (b) 给出三种 gap 归因:

- **原因 α**:上界松(证明技术保守)
- **原因 β**:下界松(已知协议族不够好)
- **原因 γ**:两端都松

(PROSPECTUS 中的归因字母是 A/B/C,但与主问题的情况 A/B/C 同名,为避免混淆,本日志用 α/β/γ 表示归因)

本日志对 $\mathcal{T}_{\text{umr}}^{\text{sym}}$(对称拓扑)做 gap 诊断。

---

## B. 工作草稿

### B.1 上下界并列

$$\text{LB}(\eta) = c_{\text{best-pub}} \sqrt{\eta} \approx 0.3 \sqrt{\eta}$$

$$\text{UB}(\eta) = 1.4427 \sqrt{\eta} + O(\eta)$$

Gap:

$$\text{gap}(\eta) = \text{UB}(\eta) - \text{LB}(\eta) \approx (1.4427 - 0.3) \sqrt{\eta} \approx 1.14 \sqrt{\eta}$$

### B.2 Scaling 分析

gap 的 **scaling** 是 $\sqrt{\eta}$,**与 UB 同阶**(因为两者都是 $\sqrt{\eta}$)。

**关键结论**:

$$\lim_{\eta \to 0} \frac{\text{gap}(\eta)}{\text{UB}(\eta)} = \frac{1.4427 - 0.3}{1.4427} \approx 0.79$$

gap 占 UB 的大约 80%。非零但**不发散**(非 $\eta^\alpha, \alpha < 1/2$)。

### B.3 PROSPECTUS 主问题的对照

回到 PROSPECTUS §1 的三种情况:

- **情况 A**($\sqrt{\eta}$ 紧上界):$\exists\, c^* > 0$ such that $R \leq c^* \sqrt{\eta}$ 且**存在协议达到** $R \geq c^* \sqrt{\eta}$(渐近)
- **情况 B**($\eta^\alpha$,$1/2 < \alpha < 1$):$\exists\, R \sim \eta^\alpha$ 协议
- **情况 C**:上界 $\eta^\alpha$ 但不可达

**分析**:

由 Log 04 命题 4.3,$R \leq 1.4427 \sqrt{\eta}$(scaling $\sqrt{\eta}$,任何 $\mathcal{T}_{\text{umr}}$ 协议都受约束)。

**这直接排除情况 B**:情况 B 要求 scaling $\eta^\alpha$, $\alpha < 1/2$,但我们已有 $\sqrt{\eta}$ scaling 的硬上界(定理 4.1,$[COROLLARY]$ from PLOB + Pirandola19)。$\alpha < 1/2$ 等价于 $\eta^\alpha > \sqrt{\eta}$ for small $\eta$,这违反定理 4.1。

**更进一步排除情况 C**:情况 C 要求"上界 $\eta^\alpha$,$\alpha < 1/2$",同样被定理 4.1 排除。

**只剩情况 A**:$\sqrt{\eta}$ 是紧上界,且 TF-QKD 族达到这个 scaling(Log 05 命题 5.3)。

### B.4 Gap 归因(α / β / γ)

Gap 归因于:

- **原因 α(上界松)**:$1.4427$ 这个 prefactor 是**点对点 bosonic pure-loss PLOB 的 single-edge**约束。对 $\mathcal{T}_{\text{umr}}$ 的特殊结构(Charlie 不可信但参与),可能有**更紧的 prefactor**(比如考虑 Charlie 必须 broadcast classical announcement,这会降低 $E_R$ 的有效值?)。但这需要针对 $\mathcal{T}_{\text{umr}}$ 的 **topology-specific converse**,文献中未见严格到比 $1.4427$ 更紧的结果。**[SYN + CONJ]**
- **原因 β(下界松)**:TF/PM/MP 的 $c \sim 0.3$ 远未饱和 $1.4427$。可能有**更好的 $\mathcal{T}_{\text{umr}}$ 协议**(新的信号格式、新的 sifting 规则、新的 post-processing)达到更高 prefactor。但**不能超过 $1.4427$**(定理 4.1)。提升 $c$ 的空间确实存在。**[SYN]**
- **原因 γ(两端都松)**:最可能的情形 —— 上界技术保守(α),下界协议未最优化(β),两者共同构成 gap 约 80% 的大小。**[SYN]**

**初步归因**:**γ 最可能**。α 可能贡献 0.3-0.5 prefactor units,β 可能贡献 0.5-0.8 prefactor units(视提升后的 TF-QKD 变体)。

### B.5 Scaling 结论 vs Prefactor 开放问题的分离

**Scaling 层面,情况 A 成立,证据:[THM] 级**

- 上界 $\sqrt{\eta}$:定理 4.1,[COROLLARY] of PLOB + Pirandola19
- 下界 $\sqrt{\eta}$:TF-QKD,[THM] of Lucamarini18

Scaling gap = $0$,情况 B/C 被 [THM] 级排除。

**Prefactor 层面,开放(情况 A 内的子问题)**

- 最好已知 $c^\star \in [c_{\text{best-pub}}, 1.4427]$,具体位置未定
- PROSPECTUS Sub-Q4 (b) 归因 α/β/γ 初步落在 γ(两端可改进)
- 缩小 prefactor gap 是剩余研究的内容(Phase 2 + Phase 3)

### B.6 可能的 "Case A wrinkles"(Case A 内的细分)

情况 A 成立后,仍有值得 Phase 2/3 细究的开放点:

**A1**(对称 prefactor)对 $\eta_A = \eta_B$,$c^\star = ?$

**A2**(不对称情形)$\eta_A \neq \eta_B$ 时,上界 $-\log_2(1 - \min(\eta_A, \eta_B))$,可达 prefactor 如何取决于 $\eta_A/\eta_B$?(TF-QKD 原论文一般只处理对称)

**A3**(noisy channel)非 pure-loss(有去相干、相位噪声、基错配)时,上下界都会变。scaling 期望仍 $\sqrt{\eta}$,prefactor 都会下调。

**A4**(finite key)finite-key 修正后的 scaling 是否仍为 $\sqrt{\eta}$?Kamin 2025 给部分答案(对 decoy-state BB84);对 TF-QKD 的 finite-key 分析尚在发展。

**A5**(非 IID)de Finetti 化简是否对 $\mathcal{T}_{\text{umr}}$ 总是成立?MS-EB 的 GEAT 兼容性(Metger 2024)应适用。

这些都是 Phase 2 / Phase 3 的工作,不改变 scaling 结论。

### B.7 一个易错点:Case B 和 Case C 的边界

情况 B 需要**同时**:

(i) 上界 $\eta^\alpha$,$\alpha < 1/2$(scaling 更好)
(ii) 协议**可达**

情况 C 需要(i)但不(ii)。

由定理 4.1,(i) 被**排除**(上界 scaling 已 $\sqrt{\eta}$,任何更紧的上界也必然 $\leq \sqrt{\eta}$ 即 $\alpha \geq 1/2$)。

**但要小心**:若我们把 "$\alpha$" 做更精细的 interpretation(比如 $\alpha = 1/2 - \epsilon$ 表示 $\sqrt{\eta}$ 乘多项对数,即 $\sqrt{\eta} \cdot \text{poly}(\log \eta^{-1})$?)这种 **logarithmic improvement** 严格讲不属于情况 B(定义里说 $\eta^\alpha$ 的幂律改进),但文献里常被讨论。定理 4.1 的 $-\log_2(1 - \sqrt{\eta})$ 展开为 $\frac{\sqrt{\eta}}{\ln 2} + \frac{\eta}{2\ln 2} + O(\eta^{3/2})$,主项 $\sqrt{\eta}$ —— 无 $\log$ 改进空间。所以情况 B 严格按 PROSPECTUS 定义被排除。**[THM]**

---

## C. 本日志的已证命题

**命题 6.1**(Scaling gap = 0)$\mathcal{T}_{\text{umr}}^{\text{sym}}$ 的上下界在 $\eta \to 0$ 渐近 scaling 同阶 $\sqrt{\eta}$. **[THM,Log 04 Cmd 4.3 + Log 05 Cmd 5.3]**

**命题 6.2**(情况 B 被排除)PROSPECTUS §1 情况 B(存在 $\eta^\alpha$,$1/2 < \alpha < 1$ 可达)与定理 4.1 矛盾,**不成立**。**[COROLLARY of 4.1]**

**命题 6.3**(情况 C 被排除)情况 C(上界 $\eta^\alpha$, $\alpha < 1/2$,不可达)同样与定理 4.1 矛盾,**不成立**。**[COROLLARY of 4.1]**

**命题 6.4**(情况 A 成立)PROSPECTUS §1 主问题答案为**情况 A**:$\sqrt{\eta}$ 是紧上界,TF-QKD 族达到这个 scaling. **[COROLLARY of 4.1 + 5.3]**

**命题 6.5**(Prefactor gap 开放)情况 A 内部 prefactor gap $\approx 1.1$(从 $c_{\text{pub}} \approx 0.3$ 到 $c_{\text{upper}} = 1.4427$)。缩窄方向的归因初步判断为**γ(两端都松)**,具体收窄工作属于 Phase 2-3 研究范围,未在本日志证成。**[SYN]**

**命题 6.6**(开放 wrinkles)情况 A 成立后,仍有 A1-A5 五类精细问题(non-IID / finite-key / asymmetric / noisy / prefactor optimization)作为 Phase 2/3 研究内容。**[元命题]**

---

## D. 下一步依赖

**Phase R 的最后一步:FINDINGS_DRAFT**

Log 06 已把主问题答案推到 **情况 A,[COROLLARY] 级确定性**。FINDINGS_DRAFT 将

(a) 正式声明主问题答案
(b) 分级展示支持证据链
(c) 列 Phase 2-3 开放工作项(A1-A5)
(d) 诚信红线:这是 [SYN] 级整合,不是新定理

**但**:FINDINGS_DRAFT **不可作为最终答案**,必须经 V1-V4 验证循环。

---

*Log 06 结束,Phase R 论证部分完成。下一阶段:FINDINGS_DRAFT + Phase V 验证循环。*
