# Zotero Library Cross-Reference — 用户本地文献匹配本项目研究

**日期**:2026-04-19
**来源**:通过 `zotero-mcp` 访问用户本地 Zotero 库(libraryID=10024639,`~/Zotero/zotero.sqlite`)
**工具**:`mcp__zotero__zotero_search_items` + `zotero_get_item_metadata` + `zotero_get_recent`
**语义搜索(chroma_db + qwen embeddings)**:今天刚 index,未命中;改用 title / author 搜索

---

## 0. 用户身份(从库中反推)

Zotero 库里发现 **4 篇作者含 "Teng, Jun"** 的 USTC TF-QKD 实验组论文,与本仓库 `git user = royal, email aredalkkosft66@gmail.com` 对应,推断用户即 **Teng, Jun @ USTC / 郭光灿 / 韩正甫组**。已发表工作:

| # | Title | 年份 | 角色 | Item Key |
|---|-------|------|------|----------|
| 1 | Arbitrary bias control of LiNbO3 MZ intensity modulators for QKD | 2023 | 一作 | `WBGEVW43` |
| 2 | Sending-or-not-sending TF-QKD with multiphoton states | 2021 | 一作 | `YF8NTS5U` |
| 3 | Twin-field QKD with passive-decoy state | 2020 | 一作 | `86PDWT6Z` |
| 4 | Optimizing SPAD for Dynamic QKD Networks | 2020 | 二作 | `2QW7ECV5` |

**对本项目的意义**:
- 用户对 **TF-QKD / SNS / passive decoy state** 实验实现有 first-hand 深度,不是纯理论研究者
- PROSPECTUS §3.1 H3(刻画式设备信任) + S1(per-round announcement) 的物理约束,用户能从**实验端**判断合理性
- REFACTORING_PLAN §5 M4B(TF-QKD 数值验证)的 log-log 斜率 0.5 ± 0.05 验收,用户已知实验数值参考区间

---

## 1. 库中**已有的**关键理论文献(本项目可直接使用)

### 1.1 安全性与可组合性(PROSPECTUS §3.1 H5 底座)

| 文献 | 年 | Item Key | 本项目用途 |
|------|-----|----------|-----------|
| **Portmann-Renner 2022** "Security in quantum cryptography" (RMP 94:025008) | 2022 | `W7KVW7AR` | PROSPECTUS §3.1 H5 "可组合安全 Portmann-Renner 框架"直接源 |
| **Dupuis-Fawzi-Renner 2020** "Entropy Accumulation" (EAT, CMP 379:867) | 2020 | `B6YSBE3B` | GEAT 的前身,RESEARCH_PLAN Sub-Q2.4 精读必读前置 |
| **Metger-Fawzi-Sutter-Renner 2024** "Generalised Entropy Accumulation" (GEAT, CMP 405:261) | 2024 | `QGFDUPEY` | **PROSPECTUS §6 Sub-Q2.4/2.5 核心** —— finite-key 合规 QKD 证明的当前 SOTA |
| **Renner-Wolf 2023** "Quantum Advantage in Cryptography" | 2023 | `H72INRV5` | 背景综述 |

### 1.2 QKD 综述(Phase 0 Sub-Q1 文献地图前置)

| 文献 | 年 | Item Key | 本项目用途 |
|------|-----|----------|-----------|
| **Lo-Curty-Tamaki 2014** "Secure Quantum Key Distribution" (Nat. Photon.) | 2014 | `3TLTWVMR` + dup `BXWN7VS8` | PROSPECTUS §10 可补充引用;Sub-Q1 Phase 0 背景 |
| **Xu-Ma-Zhang-Lo-Pan 2020** "Secure QKD with realistic devices" (RMP 92:025002) | 2020 | `NN4WI8Z3` | RESEARCH_PLAN §6 已列,库中已有 |

### 1.3 PLOB / 容量上界

| 文献 | 年 | Item Key | 本项目用途 |
|------|-----|----------|-----------|
| **PLOB 2017** "Fundamental limits of repeaterless quantum communications" (Nat. Commun. 8:15043) | 2017 | `SELE6CYS` | **Log 02 核心依赖,已引用** —— 注意库中作者字段录入错误(只写 "Laurenza"),实际为 Pirandola-Laurenza-Ottaviani-Banchi,需要用户在 Zotero 里修正 |

**⚠️ 库中元数据修正建议**:`SELE6CYS` 的作者字段修正为完整 4 人列表。

### 1.4 TF-QKD / 可达率(Log 05 下界文献)

| 文献 | 年 | Item Key | 类型 |
|------|-----|----------|------|
| **Lucamarini-Yuan-Dynes-Shields 2018** "Overcoming rate–distance limit" (Nature 557:400) | 2018 | `QKYKWH7I` | **TF-QKD 原论文** |
| **Ma-Zeng-Zhou 2018** "Phase-Matching QKD" (PRX 8:031043) | 2018 | `VLSSID3J` + dup `AL9I5BCA` | **PM-QKD 原论文** |
| **Wang-Yu-Hu 2018** "TF-QKD with large misalignment" (PRA 98:062323) | 2018 | `E6WSHH4G` + dup `JT2LHJXY` | **SNS-TF 分支** |
| **Cui-Yin-Wang-Chen-Wang-Guo-Han 2019** "TF-QKD without Phase Postselection" | 2019 | `JJ92I596` | SNS 变体 |
| **Yu-Hu-Jiang-Xu-Wang 2019** "SNS TF-QKD in practice" | 2019 | `WGZPPVVA` | — |
| **Liu et al. 2019** "Experimental TF-QKD SNS" | 2019 | `HJYKA4XK` | 实验 |
| **Chen-Zhang-Liu-Jiang 2020** "SNS Independent Lasers 509 km" | 2020 | `78SIITYL` | 实验 |
| **Wang-Yin-He-Chen 2022** "TF-QKD over 830-km fibre" (Nat. Photon.) | 2022 | `CTC8NGY8`, `NUVTSG9X`, `6ZVSZC6Y`(多重复项)| 实验(用户所在组)|
| **Liu-Zhang-Jiang 2023** "Experimental TF-QKD 1000 km" | 2023 | `C25RXG4Y` | 实验 |
| **Zhong-Hu-Curty-Qian-Lo 2019** "Proof-of-Principle TF-type QKD" | 2019 | `D9D2MRYG` | 实验 |
| **Minder-Pittaluga 2019** "Experimental QKD beyond repeaterless" (Nat. Photon.) | 2019 | `MBCD7VCC` | **越过 PLOB 的实验** |
| **Park-Woo-Park-Kim 2022** "2×N TF-QKD network" | 2022 | `HCCCLCGD` | 网络扩展 |
| **Zeng-Zhou-Wu-Ma 2022** "Mode-pairing QKD" (Nat. Commun. 13:3903) | 2022 | `P5FK4IHP` | **MP-QKD 原论文(PROSPECTUS S1 跨轮扩展)** |

> 用户自己的 TF-QKD 工作(`YF8NTS5U`, `86PDWT6Z`)已列 §0。

### 1.5 MDI-QKD

| 文献 | 年 | Item Key | 类型 |
|------|-----|----------|------|
| **Liu-Wang-Wei-Fang 2019** "High-Rate MDI-QKD over Asymmetric Channels" | 2019 | `XQRHJ8XD` | 实验 + 非对称信道分析 |
| **Shan-Sun-Ma-Jiang-Zhou-Liang 2014** "MDI-QKD with passive decoy" | 2014 | `ZB5C7NZC` | 诱骗态 MDI |
| **Wang-Wang-Fan-Yuan-Lu-Yin-Chen-He 2022** "Afterpulse effect in MDI-QKD" | 2022 | `K9693AQY` | 实验细节 |
| **Primaatmaja-Lavie-Goh-Wang-Lim 2019** "Versatile security analysis of MDI-QKD" (PRR) | 2019 | `F5L2H5UM` | **理论分析**,含 numerical key rate 方法 |
| **Wang-Kon-Ng-Lim 2022** "Symmetric private information retrieval with MDI network" | 2022 | `XXMDDMG9` | 应用扩展 |
| **Gu-Cao-Fu-He-Yin-Chen 2022** "Experimental MDI-QKD with flawed and correlated sources" | 2022 | `E4FHSPAE` | 实验 + 源不完美分析 |

### 1.6 诱骗态 / 实现细节

| 文献 | 年 | Item Key | 本项目用途 |
|------|-----|----------|-----------|
| **Lu-Lin-Wang-Fan-Yuan-Ye-Wang-Yin 2021** "Intensity modulator for decoy-state" (npj Quantum Info) | 2021 | `QMC2N654` + webpage `7PKWS82M` | 实验 |
| **Wang-Peng-Zhang-Yang-Pan 2008** "Decoy-state with source errors" | 2008 | `UKBIFR2M` | 理论 |
| **Curty-Ma-Qi-Moroder 2010** "Passive decoy state" (两个 item key)| 2010 | `6ZT4JDYQ`, `3FP529PZ` | 理论 |
| **Roberts-Pittaluga-Minder 2018** "Patterning-effect mitigating intensity modulator" | 2018 | `NPZYSZ7R` | 实验 |
| **Mauerer-Silberhorn 2007** "QKD with passive decoy state selection" | 2007 | `SINI5A89` | 理论 |

### 1.7 DI-QKD(虽 PROSPECTUS §3.2 排除,但参考)

| 文献 | 年 | Item Key | 用途 |
|------|-----|----------|------|
| **Nadlinger et al. 2022** "Experimental QKD certified by Bell's theorem" | 2022 | `2QWXYN92` | 对比参考(用户 Renner 合作方向) |

### 1.8 其他

- **Dunjko-Briegel 2018** "Machine learning & AI in quantum domain" (`PWF7XB7R`) — Sub-Q4 若归因 β 涉及 AI 搜索时参考
- **Fan-Yuan-Teng-Wang 2020** SPAD optimization (`2QW7ECV5`) — 用户合作

---

## 2. 库中**缺失**的关键文献(建议补入)

按 PROSPECTUS / RESEARCH_PLAN 的 Phase 0–2 优先级排序:

### 2.1 高优(Sub-Q3 Phase 2 精读必读)

| 文献 | 原因 | 建议 arXiv |
|------|------|-----------|
| **Pirandola 2019** "End-to-end capacities of a quantum communication network" (Commun. Phys. 2:51) | Log 03 / 04 上界 min-cut **核心依赖**,且本项目 FINDINGS v2 的 "untrusted-relay 继承" 需精读其 Eq. (11) / (17) | [1905.12674](https://arxiv.org/abs/1905.12674) |
| **Takeoka-Guha-Wilde 2014** "Fundamental rate-loss tradeoff" (Nat. Commun. 5:5235) | 替代 converse 路线(squashed entanglement) | [arXiv:1504.06390](https://arxiv.org/abs/1504.06390) |
| **Wilde-Tomamichel-Berta 2017** "Converse bounds for private comm." (IEEE TIT 63:1792) | PLOB 独立推导路线 | [arXiv:1602.08898](https://arxiv.org/abs/1602.08898) |
| **Das-Khatri-Wilde 2020/2021** "Converse bounds for private comm. with quantum channels" | 最新 converse 综述 | [arXiv:2012.03262](https://arxiv.org/abs/2012.03262) |

### 2.2 高优(Sub-Q1 / M1 实施必读)

| 文献 | 原因 | 建议 arXiv |
|------|------|-----------|
| **Winick-Lütkenhaus-Coles 2018** "Reliable numerical key rates for QKD" (Quantum 2:77) | REFACTORING_PLAN §4.6 + 附录 B 核心实施参考(WLC SDP),PHASE0_M1_TECHNICAL_SPEC §4 第一性原理推导源 | [arXiv:1710.05511](https://arxiv.org/abs/1710.05511) |
| **Coles-Metodiev-Lütkenhaus 2016** "Numerical approach for unstructured QKD" (Nat. Commun. 7:11712) | WLC 前传 | [arXiv:1510.01294](https://arxiv.org/abs/1510.01294) |
| **Hu-Im-Lin-Lütkenhaus-Wolkowicz 2022** "Robust Interior Point Method for QKD Rate Computation" (Quantum 6:792) | REFACTORING_PLAN §4.7 facial reduction 直接依据 | [arXiv:2104.03847](https://arxiv.org/abs/2104.03847) |
| **George-Lin-Lütkenhaus 2021** "Numerical calculations of finite key rate" (PRR 3:013274) | RESEARCH_PLAN §3.3 Sub-Q2.5 复现目标 | [arXiv:2011.06530](https://arxiv.org/abs/2011.06530) |

### 2.3 中优(Sub-Q2 Phase 0-1 参考)

| 文献 | 原因 |
|------|------|
| **Lo-Curty-Qi 2012** MDI-QKD 原论文 (PRL 108:130503) | REFACTORING_PLAN §4.12 M2 目标协议 |
| **Ma-Razavi 2012** MDI-QKD alternative schemes (PRA 86:062319) | M2 数值基线 |
| **Bruss 1998** "Optimal eavesdropping six states" (PRL 81:3018) | M2 六态解析 |
| **Ferenczi-Lütkenhaus 2012** "Symmetries in QKD" (PRA 85:052310) | M4A 对称性约化 |
| **Kamin-Arqand-George-Lütkenhaus-Tan 2025** "Finite-Size Analysis" (PRX Quantum 6:020342) | RESEARCH_PLAN §3.3 Sub-Q2.5 复现目标 |

### 2.4 参考级

| 文献 | 原因 |
|------|------|
| **Tomamichel 2016** "Quantum Information Processing with Finite Resources" (Springer) | smooth entropy 系统教材,GEAT 精读前置 |
| **Fawzi-Saunderson 2023** "Optimal Self-Concordant Barriers for Quantum Relative Entropies" (SIAM J. Optim.) | `cp.quantum_rel_entr` atom 证明来源 |
| **Pirandola 2019** "Composable end-to-end security with untrusted relays" (npj Quantum Info) | 非 Gaussian 情形比对;我们 DV 版本的参照 |

---

## 3. 对项目的即时影响

### 3.1 降低 Sub-Q3 Phase 2 的起步成本

本以为 "PROSPECTUS Sub-Q3 30-50 页精读" 需要从零起步。实际上**用户库已有**:

1. **PLOB 2017 原文**(只差修正作者字段)
2. **GEAT 原文** + EAT 原文 + Portmann-Renner 综述 —— Sub-Q2.4/2.5 finite-key 层基础齐备
3. **Nadlinger 2022** DI-QKD 对比
4. **Primaatmaja 2019** MDI-QKD 的 numerical security analysis —— 这是**半个 WLC SDP 的参考**,可能作为 M1 实施的 side reference

### 3.2 FINDINGS v2 的两个关键 gap,库中可补的原文

FINDINGS v2 §1.2(C1)条件 "PLOB Thm.5 / Pirandola19 Eq.(11) 定理号精确核"—— 用户库里已有 PLOB 原文,**可以人工 PDF 精读直接确认 Thm 号**,不必外部抓取。

Pirandola 2019 网络论文**不在库中**,建议优先通过 `zotero_add_by_url` 加进去。

### 3.3 用户在 TF-QKD 实验侧的 first-hand 知识

M4B 数值 prefactor 验证时(REFACTORING_PLAN §5 "log-log 斜率 = 0.5 ± 0.05"),用户可从**自己的 SNS TF-QKD 2021 实验数据**直接提供交叉验证点,而不必纯数值 sim。这让 M4B 的 achievability 验证更稳固。

---

## 4. 建议的即时补入操作(Phase 2 启动前)

按优先级,建议用户用 `zotero_add_by_url` 或 `zotero_add_by_doi` 把 §2.1 + §2.2 的 9 篇论文加入库:

**Phase 2 Sub-Q3 上界精读(优先)**:

1. [Pirandola 2019 arXiv:1905.12674](https://arxiv.org/abs/1905.12674)
2. [Takeoka-Guha-Wilde 2014 arXiv:1504.06390](https://arxiv.org/abs/1504.06390)
3. [Wilde-Tomamichel-Berta 2017 arXiv:1602.08898](https://arxiv.org/abs/1602.08898)
4. [Das-Khatri-Wilde 2020 arXiv:2012.03262](https://arxiv.org/abs/2012.03262)

**Phase 0 M1 实施(优先)**:

5. [Winick-Lütkenhaus-Coles 2018 arXiv:1710.05511](https://arxiv.org/abs/1710.05511)
6. [Coles-Metodiev-Lütkenhaus 2016 arXiv:1510.01294](https://arxiv.org/abs/1510.01294)
7. [Hu-Im-Lin-Lütkenhaus-Wolkowicz 2022 arXiv:2104.03847](https://arxiv.org/abs/2104.03847)
8. [George-Lin-Lütkenhaus 2021 arXiv:2011.06530](https://arxiv.org/abs/2011.06530)

**M2 实施**:

9. Lo-Curty-Qi 2012 MDI-QKD(PRL 108:130503)
10. Ma-Razavi 2012 MDI alternative(PRA 86:062319)
11. Bruss 1998 六态(PRL 81:3018)

---

## 5. Zotero 库元数据修正建议

1. **`SELE6CYS`**(PLOB 2017)的作者字段补完:`Pirandola, Stefano; Laurenza, Riccardo; Ottaviani, Cosmo; Banchi, Leonardo`
2. **重复项清理**:`CTC8NGY8`/`NUVTSG9X`/`6ZVSZC6Y` 都是 Wang-Yin 2022 "TF-QKD 830-km",应去重
3. **VLSSID3J` / `AL9I5BCA`** 都是 Ma-Zeng-Zhou 2018 PM-QKD,应去重
4. **`E6WSHH4G` / `JT2LHJXY`** 都是 Wang-Yu-Hu 2018,应去重
5. **`3TLTWVMR` / `BXWN7VS8`** 都是 Lo-Curty-Tamaki 2014,应去重

可用 `zotero_find_duplicates` + `zotero_merge_duplicates` 批量处理。

---

## 6. 对 PROSPECTUS / RESEARCH_PLAN 文献清单的调整建议

PROSPECTUS §10 + RESEARCH_PLAN §6 的文献依赖图,可根据**库中已有** vs **缺失**做标注:

```
Phase 0 必读:
  [Shor-Preskill 2000]  ─ NOT IN LIBRARY
  [WLC 2018]            ─ NOT IN LIBRARY  ⚠️ Phase 0 M1 实施必读
  [Lo-Curty-Qi 2012]    ─ NOT IN LIBRARY
  [Ma-Razavi 2012]      ─ NOT IN LIBRARY
  [Bruss 1998]          ─ NOT IN LIBRARY
  [Hwang 2003]          ─ NOT IN LIBRARY
  [Wang 2005]           ─ NOT IN LIBRARY  (注:可能已有)
  [Lo-Ma-Chen 2005]     ─ NOT IN LIBRARY
  [Ma-Qi-Zhao-Lo 2005]  ─ NOT IN LIBRARY
  [George-Lin-Lütkenhaus 2020/2021] ─ NOT IN LIBRARY
  [Hu et al. 2022]      ─ NOT IN LIBRARY
  [Ferenczi-Lütkenhaus 2012] ─ NOT IN LIBRARY
  [Lucamarini 2018]     ─ ✅ QKYKWH7I
  [Ma-Zeng-Zhou 2018]   ─ ✅ VLSSID3J
  [Wang 2018 SNS-TF]    ─ ✅ E6WSHH4G
  [Zeng 2022 MP-QKD]    ─ ✅ P5FK4IHP
  [Minder 2019]         ─ ✅ MBCD7VCC

Phase 1 GEAT 栈:
  [Renner 2005 PhD]     ─ NOT IN LIBRARY
  [Portmann-Renner 2022]─ ✅ W7KVW7AR
  [Tomamichel 2016 book]─ NOT IN LIBRARY
  [Dupuis-Fawzi-Renner 2020 EAT] ─ ✅ B6YSBE3B
  [Metger et al. 2024 GEAT]      ─ ✅ QGFDUPEY
  [Kamin et al. 2025]   ─ NOT IN LIBRARY

Phase 2 上界栈:
  [Takeoka-Guha-Wilde 2014]  ─ NOT IN LIBRARY
  [PLOB 2017]                ─ ✅ SELE6CYS(作者字段需修)
  [Wilde-Tomamichel-Berta 2017] ─ NOT IN LIBRARY
  [Pirandola 2019 网络]      ─ NOT IN LIBRARY  ⚠️ FINDINGS v2 Sub-Q3 核心
  [Das-Khatri-Wilde 2020]    ─ NOT IN LIBRARY
  [Vidal-Werner 2002]        ─ NOT IN LIBRARY
```

覆盖率:**Phase 0 ~30%,Phase 1 GEAT ~60%,Phase 2 ~20%**(按必读清单)。最薄弱的是 **Phase 2 上界方向**,正是 FINDINGS v2 被撤回的地方 —— 这也是符号意义上的验证:用户库的内容分布反映了 **PROSPECTUS Sub-Q3 在现有研究中的薄弱位置**。

---

## 7. 元方法教训

本次通过 Zotero MCP 访问用户本地库,是对前几轮"AI literature synthesis 不等于 PDF 精读"教训的**补丁**:

- **AI + WebSearch**:拿到文献标题 / 摘要级信息,可能误引定理号
- **AI + Zotero MCP**:直接读取用户**已经筛选过 + 可能有 annotations** 的 PDF 全文 + 元数据,大幅降低"合成偏差"
- **最终层**:人类研究者直接精读 PDF,做 Sub-Q3 的 30-50 页报告

本 ZOTERO_REFERENCES.md 是 **AI + Zotero MCP** 层的产出,为 Sub-Q3 精读工作节约 2-4 周(跳过 "找文献 + 筛选文献" 阶段,直接进入 "读 + 重推" 阶段)。

---

## Changelog

- **v1.0**(2026-04-19):首次落盘,通过 zotero-mcp 访问用户本地库的完整盘点

---

*ZOTERO_REFERENCES 结束。下一步:补入 §4 列出的 9-11 篇缺失文献,然后按原计划继续 Phase 0 M1 准备层的用户 Q1 决策。*
