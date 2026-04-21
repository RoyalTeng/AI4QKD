# Khatri-Wilde 2020/2024 — *Principles of Quantum Communication Theory: A Modern Approach*

**Reference**: arXiv:2011.04672v2 (11 Feb 2024), 1200+ 页教科书
**PDF**：[docs/literature/pdfs/KhatriWilde-2020-PrinciplesQuantumComm.pdf](pdfs/KhatriWilde-2020-PrinciplesQuantumComm.pdf)
**Level**：3 精读（章节范围 Ch 9-10 Entanglement Measures + Ch 15-16 Secret-Key / Private Communication + Ch 19-20 LOCC-Assisted 上界）
**关联 Phase 2 动作**：U3.5（RESEARCH_PLAN §4.2）
**更新日期**：2026-04-21 自主 session

---

## 0. 读这本书的范围

Khatri-Wilde 是 1200+ 页的完整综合教科书。本 memo 聚焦 Sub-Q3 相关的四大区域：

| 范围 | 页码 | Sub-Q3 bearing |
|---|---|---|
| **Ch 9 纠缠度量**（Rains, Squashed, Gen. Divergence） | 503-580 | E_R / R / E_sq 定义与性质 |
| **Ch 10 量子信道纠缠度量** | 581-626 | amortized entanglement, Max-Rains, Max-E_R |
| **Ch 15 Secret Key Distillation** | 938-1017 | bipartite private-state framework |
| **Ch 16 Private Communication** | 1018-1066 | E_R 强 converse for private capacity |
| **Ch 19 LOCC-Assisted Quantum Comm.** | 1145-1162 | **Proposition 19.2 核心定理** |
| **Ch 20 Secret Key Agreement** | 1163-1193 | Sub-Q3 最关键章节 |

其他章节（经典通信 Ch 11-12, 纠缠蒸馏 Ch 13, 量子通信 Ch 14, 反馈辅助 Ch 17-18）未深读。

---

## 1. 一句话总结

Khatri-Wilde 的核心贡献是把 PLOB / Pirandola / TGW / WTB 等文献的**各式上界**（E_R, Rains 信息, max-Rains, squashed entanglement, generalized divergences）整合到一个 **amortized entanglement 框架**下，并对 **teleportation-simulable channels** 给出 n-shot non-asymptotic 强 converse 界（Thm 19.4, 19.8, 19.9, 20.x）。对本项目 Sub-Q3 最直接的是 **Proposition 19.2 + Corollary 19.3**：对任意"熵测度单调非增 + 分离态为零"的 E，n-shot LOCC-assisted 通信的输出纠缠不超过 n·E^A(N)（amortized），对 tele-simulable channel 退化为 n·E(R;B')_θ。

---

## 2. Ch 19 LOCC-Assisted Quantum Communication — 核心定理

### 2.1 Proposition 19.2（amortized entanglement general bound）

**陈述**：对任意量子信道 N_{A→B}，任意 n ∈ ℕ，任意 (n, M, ε) LOCC-assisted 量子通信协议，其最终态 ω_{M_A M_B} 满足

> $$E(M_A; M_B)_\omega \leq n \cdot E^{\mathcal{A}}(\mathcal{N})$$

其中 E 是任意"LOCC-单调 + 分离态零"的纠缠度量，E^A(N) 是信道 N 的 **amortized 纠缠度量**。

**Proof idea**：链式不等式（19.1.20 → 19.1.24）。归纳地把 ω^{(n)} 的 entanglement 回溯到 ρ^{(1)}（分离态 → E=0），每一步 LOCC-单调缩，总累积 ≤ n·E^A(N)。

**Sub-Q3 bearing**：这是所有后续定理（squashed, Rains, max-Rains）的**共同骨架**。把一个具体 E 插入，就得到该 E 对应的 n-shot converse。

### 2.2 Corollary 19.3（tele-simulable reduction）

**陈述**：若 E_S 是 subadditive + separable-zero 纠缠度量，且 N 是 tele-simulable channel（resource state θ_{RB'}），则

> $$E_S(M_A; M_B)_\omega \leq n \cdot E_S(R; B')_\theta$$

**Sub-Q3 bearing**：PLOB 和 Pirandola 2019 的上界都可以通过 Corollary 19.3 + 具体选择 E_S = E_R 或 R (Rains) 或 E_sq 得到。对 pure-loss bosonic channel：
- E_R(θ_{loss}) = -log₂(1-η) → PLOB Eq. 19
- R(θ_{loss}) = 同上（对 pure-loss tight）

### 2.3 Thm 19.4（squashed entanglement weak converse）

**陈述**：对任意信道 N，任意 (n, M, ε) LOCC-assisted 量子通信：

> $$\log_2 M \leq \frac{1}{1 - \sqrt{\varepsilon}} \left[n \cdot E_{\mathrm{sq}}(\mathcal{N}) + g_2(\sqrt{\varepsilon})\right]$$

其中 g_2(x) = (1+x)·log₂(1+x) - x·log₂(x)（二元熵修正）。

**特点**：
- **Weak converse only**：ε → 0 时 tight
- **不 SDP-可计算**（E_sq 无已知有限维 SDP）
- 对 amplitude damping 给出 TGW 2014 bound 的 non-asymptotic 版本

### 2.4 Thm 19.8（max-Rains strong converse）

**陈述**：

> $$\log_2 M \leq n \cdot R_{\max}(\mathcal{N}) + \log_2\left(\frac{1}{1-\varepsilon}\right)$$

**特点**：
- **Strong converse**（ε → 1 也成立 asymptotically sharp）
- **SDP-可计算**（max-Rains = max-Rényi of Rains is SDP via Wang-Duan 2016b）
- Berta-Wilde 2018 原创

**Sub-Q3 对接点**：`qkdx/numerics/upper_bound.py` 下一步可扩展为 max-Rains SDP（Wang-Duan 2016b formulation），与当前的 E_R^PPT 互补。

### 2.5 Thm 19.9（Rains strong converse for PPT-simulable）

**陈述**：若 N 是 PPT-simulable with resource θ，则对所有 α > 1：

> $$\log_2 M \leq n \cdot \tilde{R}_\alpha(S; B')_\theta + \frac{\alpha}{\alpha - 1} \log_2\frac{1}{1 - \varepsilon}$$

> $$\log_2 M \leq \frac{1}{1-\varepsilon}[n \cdot R(S; B')_\theta + h_2(\varepsilon)]$$

**Sub-Q3 bearing**：对 PPT-simulable channel（包括所有 covariant 信道，如 Pauli / depolarizing），给出最紧的 strong converse。这是 PLOB 框架的自然推广。

---

## 3. Ch 20 Secret Key Agreement — Sub-Q3 最核心章节

### 3.1 协议定义（Sec 20.1）

n-shot secret-key-agreement protocol 通过量子信道 N 分发 ε-secure 密钥位 log_2 K。两个等价表达：
- **LOPC-assisted private communication**（Alice 发经典密钥位，受 LOPC 保护）
- **LOCC-assisted private-state distillation**（Alice-Bob 蒸馏 bipartite private state）

**PROSPECTUS Sub-Q3 bearing**：我们的 umr 拓扑可以**嵌入** LOPC-assisted private communication 框架（Eve 控 Charlie 等价于 Charlie 只能做 LOPC），但需要形式化证成（见 FINDINGS v2 §1.1 + Log 07 路径 α/β/γ）。

### 3.2 Thm 20.3 Squashed entanglement key-agreement 上界

> $$\log_2 K \leq \frac{1}{1 - \sqrt{\varepsilon}}[n \cdot E_{\mathrm{sq}}(\mathcal{N}) + g_2(\sqrt{\varepsilon})]$$

（书中编号 Thm 20.5 或类似；具体编号需核正文）

**关键**：E_sq(N) 是 **key-agreement capacity 的 weak-converse 上界**，与 Sec 19.3 的 Q^↔ ≤ E_sq(N) 同根源。

### 3.3 Thm 20.4 相对熵纠缠 key-agreement 上界（Sec 20.4）

> $$\log_2 K \leq n \cdot D(\mathcal{N}) + \text{(小常数项)}$$

其中 D(N) 是 **信道 Rains 信息 R(N) 或 E_R(N)**（具体型式依 PPT-simulable vs. tele-simulable 而异）。这是 **PLOB / WTB / Pirandola 的统一陈述**。

---

## 4. 与现有 memo 的对接

### 4.1 相比 PLOB / Pirandola / WTB / TGW 的增量

| 相对 | Khatri-Wilde 补上了什么 |
|---|---|
| **PLOB 2017** | non-asymptotic n-shot 版本 + 一般信道（非仅 pure-loss） |
| **Pirandola 2019** | 显式 amortized 框架下的陈述 |
| **WTB 2017** | 统一了 Rains / max-Rains / 各类 Rényi 的强 converse 家族 |
| **TGW 2014** | squashed entanglement 上界的 non-asymptotic 版本 + g_2 小常数 |

### 4.2 与 umr（untrusted measurement relay）拓扑的 bearing

**关键适用性问题**（延续 Log 07 审计）：

1. **Ch 20 的安全模型**：私有通信 capacity 定义是 Alice-Bob 对 Eve（信道环境）安全。Khatri-Wilde 标准 LOPC 模型中，**relay node 是可信 party**（可做 LOCC）。
2. **umr 额外要求**：Eve 控制 Charlie（中间测量站）。这**不是** Khatri-Wilde 原始模型覆盖的情景。
3. **修复路径**（Log 07 §3）：
   - 路径 α：把 umr Charlie 建模为 Eve 可控 LOCC sub-channel → 归约到 Khatri-Wilde 模型
   - 路径 β：把 umr 整体视为 effective A→B channel → 直接套用 Ch 19.3 / Ch 20 PLOB-style 上界
   - 路径 γ：只用 single edge PLOB + data-processing inequality（Khatri-Wilde Prop 19.2 特例）→ 最小可信 baseline

**推荐**：**路径 γ** 最符合 Khatri-Wilde 框架，因为它就是 **Prop 19.2 + Cor 19.3** 对 pure-loss edge 的直接应用，+ 一个"Eve's manipulation of Charlie's quantum state is a (deterministic) map that can only decrease Alice-Bob correlation"的 data-processing argument。

---

## 5. Layer 5.3 SDP 扩展路线

当前 `qkdx/numerics/upper_bound.py` 只实现 E_R^PPT（PPT-relaxed relative entropy of entanglement）。Khatri-Wilde Ch 9-10 / Ch 19 给出两条扩展路线：

### 5.1 max-Rains R_max(N)（Thm 19.8 需要）

Wang-Duan 2016b 的 SDP 形式：

$$R_{\max}(\mathcal{N}) = \log_2 \min \left\{\|T_{R'B} + T_{R'B}'\|_\infty : T_{R'B} \geq 0, T_{R'B} \geq \rho_{RB}^{\mathcal{N}}\right\}$$

其中 ρ^N 是 Choi state。可以直接写成 SDP，MOSEK 求解 → 给出 strong converse upper bound。

**优势**：SDP-computable（vs E_sq 不可计算）， strong converse（vs E_R^PPT 只是 weak converse 的一种变体）。

### 5.2 generalized Rains divergence（Sec 9.3）

Rains divergence R(ρ||σ) 和 E_R 很接近，但用 PPT 约束优化而非 SEP。我已经实现的 E_R^PPT 其实就是 generalized Rains divergence 的一个特例（当 α → 1）。可以扩展到 α-Rényi 族：R̃_α, R̂_α（hockey-stick）等。

### 5.3 E_sq squashed entanglement（Thm 19.4 需要）

不 SDP-可计算（需在所有 "squashing" 扩展上求 inf）。但存在 Li-Winter 2014 的 pass-through bounds 和 Takeoka-Guha-Wilde 2014 的具体 squashing choice。对 Sub-Q3 可以用 TGW 2014 的选择作为**上界的上界**，在不可 PPT-simulable 的 channel 上仍有效。

---

## 6. 对本项目的具体 actionable items

### 6.1 立即可做（数值）

1. **扩展 `qkdx/numerics/upper_bound.py` 添加 `r_max_channel_sdp(kraus_ops, dim_A)`**：Wang-Duan 2016b SDP 形式的 max-Rains 信道信息。对 toy channels (depolarizing, dephasing, amp damping) 数值验证，对 PPT-simulable channel 比较 E_R^PPT vs R_max。
2. **在 `e_r_channel_ppt` 测试里添加 Khatri-Wilde 定理 validation**：对 generalized amplitude damping，E_R ≤ R_max 要验证。
3. **对 Sub-Q4 gap 分析**：gap(η) = R_max^PPT(N_η) − R_Kamin_achievable(N_η) 给出更紧的 gap 形状。

### 6.2 理论 / memo（留给用户）

1. **路径 γ 形式化**（Log 07 §3 + Khatri-Wilde Prop 19.2 + Cor 19.3）：写成一条 3-4 页的 lemma memo，放入 `docs/proofs/umr_data_processing.md`。
2. **Ch 20 "Secret Key Agreement" 的重新陈述**：在 `docs/proofs/upper_bound_msen.md` 中把 Khatri-Wilde Thm 20.x 翻译成 MS-EB 框架下"对 umr 拓扑任意 Π 满足 R(Π) ≤ f(η)"的形式。

---

## 7. Limitations

1. **本 memo 没读 Ch 11-18**：经典通信容量、反馈辅助等与 Sub-Q3 间接相关，但非本期核心。
2. **未自己验证所有引理证明**：Level 3 精读，部分证明仅 take-it-for-granted。如果 Sub-Q4 归因依赖某具体 lemma（如 amortization collapse Thm 10.x），需回头做 Level 4。
3. **[IN PROGRESS] 标记**：书中 Ch 1 Introduction + Ch 19.4 Examples 都标记 [IN PROGRESS]，意味着 v2 2024-02 版某些 specific channel examples 尚未完全写出。已知引理的陈述本身稳定，但 specific numerical illustrations 可能不完整。

---

## 8. 与本项目 Phase 2 的连接

本 memo 完成后：

1. ✅ U3.5（Khatri-Wilde Level 3 精读 memo）
2. ⏳ U3.6 上界 MS-EB 重写：基于本 memo + Log 07 + PLOB/Pirandola/WTB/TGW memos 整合
3. ⏳ U3.7 Layer 5.3 SDP 扩展：添加 max-Rains SDP
4. ⏳ U3.8 upper_bound_report.md：30-50 页综合接缝报告

---

## Changelog

- **v0.1**（2026-04-21 autonomous session）：首版 Level 3 精读 memo，聚焦 Ch 19-20（LOCC-assisted / Secret Key Agreement）+ 与项目 Sub-Q3 / Log 07 的适用性分析。
