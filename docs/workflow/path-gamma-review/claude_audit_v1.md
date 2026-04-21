# Claude-native audit of path γ v0.2

**日期**：2026-04-21
**评审对象**：[docs/proofs/umr_data_processing_gamma.md](../../proofs/umr_data_processing_gamma.md) v0.2
**Codex 状态**：exec 完成但输出 dump Khatri-Wilde textbook 而非 focused verdict；Claude audit 作为主 verdict
**评审 verdict**：**UNSOUND-RETRACT**

---

## CRITICAL（撤销 [COROLLARY] 主张）

1. **§2.1 "Eve 包含" 是范畴错误，不是集合包含**
   
   Proof 声称 $\mathcal{A}_\text{tr} \subsetneq \mathcal{A}_\text{umr}$，但两者生活在**不同 Hilbert 空间 / 不同安全博弈**：
   - Pirandola 2019 §II-C (per Log 07 §1.3)：Eve 系统 $E$ = **channel 环境的 purification only**；Charlie 寄存器**不**在 $E$
   - umr：Charlie 量子寄存器**在** $E$
   
   不能写 $\mathcal{A}_\text{tr} \subseteq \mathcal{A}_\text{umr}$ 因为 ambient universe 不同。"Eve 选择在 Charlie 处 honest 操作" 是 umr 模型中的 strategy over Charlie 寄存器；Pirandola $\mathcal{T}_\text{tr}$ 中 Eve **根本没有** Charlie 寄存器。这两个不可 by set inclusion 比较。

2. **§2.2 Step 1 对 "同一协议 $\Pi$" 玩语义游戏**
   
   Portmann-Renner 协议 $=$ 所有 honest parties 操作的 tuple，Charlie honest 时 Charlie 算 honest party。
   - $\mathcal{T}_\text{tr}$ 中 $\Pi$ **包含** Charlie 的 LOCC box 作为 honest-party spec
   - $\mathcal{T}_\text{umr}$ 中 $\Pi$ **只** spec Alice 和 Bob；Charlie box 被 adversarial channel 替代
   
   Step 1 (A_tr 评估) 和 Step 2 (A_umr 评估) 中的 $\Pi$ **honest parties 数量和 identity 不同**，不是 "同一协议"。§1.4 的 "trivial $\inf$-over-larger-set" **不适用**。

3. **Structurally isomorphic to retracted FINDINGS v1 error**
   
   Log 07 §4.3 已识别 "path α monotonicity 需三条 lemma 明写"（协议嵌入 + 安全归约 + rate 定义对接）。v0.2 把三条 lemma **合并到一个未审查的 "containment" 句子**。RETRACTION §1.1 明示**禁止**此 pattern：把未经文献定理级支持的推理链伪装成定理推论。v0.2 **重复** FINDINGS retraction 失败模式。

---

## MAJOR（sign-off 前必须处理）

4. **§1.4 containment 方向正确**（larger Eve → lower rate），回答用户 Q1。问题**不在** §1.4 本身，**而在** §2.1 错误识别 "larger" 在两个不等价安全博弈间的含义。

5. **非对称 $\min(\eta_A, \eta_B)$ 主张**即使在 trusted 情形也不从 Pirandola 2019 简单推出。§2.2 Step 2 invoke min-cut 给 $\min(E_R(\mathcal{N}_A), E_R(\mathcal{N}_B))$，这对**对称**单中继 chain 正确；Log 07 §2.2 Step C 显示 Pirandola cut 论证要求 intra-cut 节点与该侧 endpoint 协作。引用卫生要求明说是 "trusted $N=1$ chain 的 min-cut"，不是 generic 定理。

6. **§3 数值 "A tighter than B" 误导**
   
   $-\log_2(0.99)=0.0145$ at $\eta_A=0.01$ 算术正确，但 $-\log_2(1-\sqrt{\eta_A\eta_B})$ 作为 B 是否在非对称情形下也是上界——**不是显然**。Pirandola N=1 equispaced 公式针对**对称** chain，非对称继承本身是 [CONJ] 级动作。**不应**在未独立推导 B 的情况下用 B 作 comparison baseline。

7. **§4 finite-blocklength chaining 双 conjectural**
   
   §4.2 再次 apply "adversarial containment" 继承 WTB Thm 47：
   - (i) §2.1 containment unsound → §4 继承 unsound
   - (ii) WTB Thm 47 covariance 要求**信道**，不是网络；重用需 Pirandola stretching，在 umr 下按 Log 07 §3 Step C 失败

---

## MINOR

- §1.3 "Khatri-Wilde 2024 Prop 19.2 + Thm 20.x" 留 literal "x"。填或标 [RECALLED]
- §1.2 Pirandola "Eq. 9 / 11" 模糊；Log 07 标为 [RECALLED]，v0.2 未继承该 uncertainty 标记
- §1.1 PLOB strong converse attribution "WTB 2017 Thm 26" 标准，但应注 WTB formulation 是 general-attack strong converse；$-\log_2(1-\eta)$ primary 来源是 PLOB paper 本身
- §0 states "asymptotic $n\to\infty$" 但 §4 promises finite-size；pick a lane 或明层
- Changelog 宣称 "审阅时长减半" (4-5 days vs 7-10) 是 illusory：v0.2 把 L1-L3 proof burden 埋到一个未审的 containment claim 中。Burden 没缩小，只是被藏起来

---

## VERDICT

**UNSOUND-RETRACT**

§2.1 adversarial containment 论证是 Log 07 §3.1 / §4.3 识别的同一个 [SYN/CONJ] monotonicity move，需要三条明写 lemma（protocol embedding + security reduction + rate-definition matching）。v0.2 **没给出** 这些 lemma；而是 assert set inclusion between Eve 模型 living in different Hilbert spaces 和 different security games——这**不是** well-formed 的 set-theoretic relation。

Pirandola 2019 §II-C 安全定义**明确排除** Eve-controlling-Charlie (Log 07 §1.3)，所以 invoke Pirandola min-cut against umr Eve 正是**触发** FINDINGS retraction on 2026-04-19 的 scope violation。升级 [CONJ] → [COROLLARY] on this basis 是 **结构性重复** retracted overclaim.

**推荐行动**：revert 主定理到 **[CONJ]**。若用户想追 [COROLLARY]，正确路径是 Log 07 **path γ** (§4.5) 的**原始** 公式：PLOB on $\mathcal{N}_A$ 单边 + **明写** data-processing lemma（Charlie 操作 adversarial 与否，不能增加 Alice-Bob mutual information 超过 weaker arm PLOB）。此路径**不需要** Pirandola 2019，sidestep trust-assumption quagmire。

Path-α 三 lemma 也 work，但必须**明写**，不是 assert。

---

## 关联文件（审查时 cross-reference）

- [docs/proofs/umr_data_processing_gamma.md](../../proofs/umr_data_processing_gamma.md) v0.2: unsound as drafted
- [docs/research/07_pirandola_2019_technical_audit.md](../../research/07_pirandola_2019_technical_audit.md) §1.3, §3.1, §4.3, §4.5: authoritative diagnosis v0.2 覆盖 without 回应
- [docs/research/RETRACTION.md](../../research/RETRACTION.md) §1.1, §4.2: precedent + anti-repeat rules v0.2 违反
