# V4:codex 独立评审

**日期**:2026-04-19
**评审者**:codex(gpt-5.3-codex, xhigh reasoning, read-only sandbox)
**被评审对象**:FINDINGS_DRAFT + Log 01-06 + V1-V3
**角色**:codex 作为独立对抗者,专门找反驳点

---

## A. codex 的 Verdict

**NEEDS_REVISION** —— 主结论(情况 A)**立场仍然支持**,但有 7 条 findings 需修订。

codex 独立立场:

> "仍是 A,但把确定性下调半档。当前材料支持 '√η 是该拓扑最可能的紧 scaling',我不支持 B/C。"

---

## B. codex 的 7 条 findings

### finding 1 [严重]:情况 B/C 的 α 定义前后冲突

**问题**:PROSPECTUS §1 情况 B 写 "$1/2 < \alpha < 1$"(L40),但研究日志(Log 06,FINDINGS_DRAFT)按 "$\alpha < 1/2$ (更好 scaling)" 推理。字面与 PROSPECTUS 不一致。

**codex 分析**:若沿用 PROSPECTUS 字面 $\alpha \in (1/2, 1)$,排除情况 B 应由"TF 已给 $\Omega(\sqrt{\eta})$"来做(**下界推动**,不是上界)。

**我的分析**(补充):PROSPECTUS §1 情况 B 的字面定义与 TF-QKD 已实现 $\sqrt{\eta}$ 可达在**物理上内部矛盾**,因为 $\eta^\alpha$ with $\alpha > 1/2$ 对 $\eta < 1$ 等价 $< \sqrt{\eta}$,但 TF-QKD 已达 $\sqrt{\eta}$ 则"可达"不可能小于 $\sqrt{\eta}$。

**两种读法**:

- **读法 A(PROSPECTUS 字面,$\alpha \in (1/2, 1)$)**:情况 B 陈述 "$\eta^\alpha$ 上界**可达**,$1/2 < \alpha < 1$"。由 TF-QKD $\sqrt{\eta}$ 已可达,实际可达 $\geq \sqrt{\eta}$,与 "$\eta^\alpha$ 可达 ($\alpha > 1/2$,小于 $\sqrt{\eta}$)"矛盾。**由下界排除**。
- **读法 B(物理直觉,$\alpha \in (0, 1/2)$)**:情况 B 陈述"比 $\sqrt{\eta}$ 更好 scaling 可达"。由定理 4.1 上界 $\sqrt{\eta}$ 排除。**由上界排除**。

无论哪种读法,**情况 B 被排除**,FINDINGS 主结论(情况 A)不变。

**修正**:FINDINGS 显式处理 PROSPECTUS 的 $\alpha$ 约定歧义,两种读法下均给出情况 B 排除的论证。

### finding 2 [严重]:Pirandola 2019 公式写型

**问题**:Log 03 把 single-path min-cut 写成 **sum over cut**。codex 指出,Pirandola 2019 主文的 Eq. (11) 是 **max over cut**(single-path),而 Eq. (17) 是 **sum over cut**(multi-path)。另外定理号 "Thm. 2 / Thm. 3" 不是 2019 论文的稳妥引用方式,应该用方程号。

**我的重新推理**:

对 **single-path $s$-$t$ network**,min-cut 在经典 max-flow 意义下仅 1 条边(任何 cut 都"切掉至少一条 source-target 唯一路径")。若 cut 集合是 $\{e^*\}$(仅一条边)— 那 "sum over $\{e^*\}$" = "max over $\{e^*\}$" = $E_R(\Phi_{e^*})$。

对 **linear single-path 三节点**(Alice - Charlie - Bob):合法 $s$-$t$ cut 是 $\{e_1\}$ 或 $\{e_2\}$,两者都是 single-edge cut。min over cuts:取较小 $E_R$。

所以**对 linear single-path $\mathcal{T}_{\text{umr}}$**,codex 的 "max over cut edges" 与我之前的 "sum over cut edges" 给**相同数值**(因为 cut 只含一条边)。

但**公式表达上,codex 是对的**:一般性陈述应该用 Eq. (11) 的 min over cuts, max (或具体 single-edge) E_R。我的 "sum" 写法只在 linear single-path 情形是对的,不够一般。

**修正**:Log 03 改为"对 single-path network,min-cut 是 min over cuts 的 edge $E_R$(不是 sum)";linear 三节点情形的结果保持。引用改为 "Pirandola19 Eq. (11) for single-path / Eq. (17) for multi-path"。

### finding 3 [中等]:PLOB 对 DV-QKD achievability 不紧

**问题**:PLOB 的 converse 是硬上界,但其 achievability 要求 CV + 量子存储(非 DV)。用 PLOB 做 $\mathcal{T}_{\text{umr}}$ 上界合法,但**对 DV 协议类的 prefactor 判断偏松** —— 实际 DV 协议可能远不能达到 $1.44 \sqrt{\eta}$。

**我的分析**:这不改变 scaling,只影响 prefactor 的解释。FINDINGS §4.1 A1 已标注 prefactor gap 是开放的,但需要显式说明"**prefactor gap 的存在部分源于 PLOB 的 achievability 用 CV+memory 协议,不适用 DV**"。

**修正**:FINDINGS §4.1 补说明。

### finding 4 [中等]:集合包含关系显式

**问题**:Pirandola 2019 网络 bound 对更一般的协议成立;$\mathcal{T}_{\text{umr}}$ 是其子集。

**我的分析**:本来就如此 — 定理 4.1 隐含了"Allowed($\mathcal{T}_{\text{umr}}$) ⊂ Allowed(Pirandola-network)",所以上界可直接继承(单调性)。codex 要求显式写出。

**修正**:Log 04 + FINDINGS 补一句 "Allowed($\mathcal{T}_{\text{umr}}$) ⊂ Allowed(Pirandola-network),故上界继承"。

### finding 5 [中等]:scaling gap = 0 的附加条件

**问题**:scaling gap = 0 的成立条件应显式为 "**asymptotic + pure-loss + 单中继**";finite-key / non-IID / noisy channel 作为外推风险单列。

**我的分析**:本来 FINDINGS §4 的开放点 A3-A5 已覆盖,但主结论陈述需要把附加条件写进。

**修正**:FINDINGS §1 主结论陈述加附加条件括号。

### finding 6 [中等]:定理号可信度

**codex 独立建议**:

1. PLOB 2017:**最可能 Thm. 5(主结果)**。**[LIKELY VERIFIED]**
2. Pirandola 2019 min-cut:**更稳妥用 Eq. (11) / (17)**,不建议硬写 Thm 号。
3. "Thm. 2" 更像 2018 channel-simulation 的编号,不是 2019 网络主文。

**修正**:FINDINGS + Log 03 + Log 04 统一为:

- PLOB17 **Thm. 5(主结果)** `[LIKELY]`
- Pirandola19 **Eq. (11) single-path + Eq. (17) multi-path** `[VERIFIED by codex memory]`

### finding 7 [结论]:确定性下调半档

**codex 建议**:把"[COROLLARY] 级确定性"改成"**条件化 COROLLARY(待定义统一 + 编号核定)**"。

**我的分析**:合理。FINDINGS_DRAFT 的 [COROLLARY] 级是基于"PROSPECTUS 定义清晰 + 定理号准确"两个前提。finding 1 揭示 PROSPECTUS 有约定歧义,finding 6 揭示定理号非 100% 确定。故条件化处理更诚实。

**修正**:FINDINGS 的主结论置于 **条件化 COROLLARY** 级,明确两个前提。

---

## C. V4 需要做的修订清单

| # | 位置 | 修改内容 |
|---|------|----------|
| 1 | FINDINGS | 显式处理 PROSPECTUS $\alpha$ 约定歧义,两种读法下均给情况 B/C 排除 |
| 2 | Log 03 | 公式改为 min over cuts,single/multi-path 区分 |
| 3 | FINDINGS §4.1 | prefactor gap 解释:PLOB achievability 用 CV+memory,不适用 DV |
| 4 | Log 04 + FINDINGS | 补 "Allowed($\mathcal{T}_{\text{umr}}$) ⊂ Allowed(Pirandola-network)" 显式继承 |
| 5 | FINDINGS §1 | 主结论加附加条件 "asymptotic + pure-loss + 单中继" |
| 6 | 全部文件 | 定理号改为:PLOB17 Thm. 5 [LIKELY] / Pirandola19 Eq. (11)/(17) |
| 7 | FINDINGS §1 | 确定性级别改 **条件化 COROLLARY** |

---

## D. V4 结论

**Verdict**: **NEEDS_REVISION**(可修复,非 BLOCKER)

主结论 **情况 A 成立**:codex 独立立场也确认。没有 [BLOCKER] 级反驳。修订后可进 FINDINGS_FINAL。

---

*V4 结束,进入 FINDINGS_FINAL。*
