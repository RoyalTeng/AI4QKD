# SymPy C1(c) 验证记录 — log_neg(E_AD(η)) = log₂(1+η)

**日期**: 2026-04-23  
**验证类型**: R0.2 C1(c) — 非 AI 工具（SymPy 符号计算系统）独立复现  
**工具**: SymPy 1.x（确定性代数系统，非 AI 推理）  
**验证目标**: `docs/findings/beta_G3_golden_ratio_crossover_2026-04-23.md §2` 全部 5 推导步骤  

---

## 验证状态

**C1(c): ✅ VERIFIED** — 所有 6 项断言符号验证通过  
**C3: ✅ PASS** — dev-reviewer Round 2 PASS（workflow-log.md）  
**C2: ⏳ 待用户签字**  

---

## 验证脚本输出（逐行）

```
=== SymPy C1(c) 符号验证：log_neg(E_AD(η)) = log₂(1+η) ===

步骤1: Choi 态矩阵（基 |00⟩,|01⟩,|10⟩,|11⟩）
Matrix([
[1/2,   0,       0,   sqrt(eta)/2],
[  0,   0,       0,             0],
[  0,   0, 1/2 - eta/2,          0],
[sqrt(eta)/2, 0, 0,         eta/2]])
✓ rho[0,0] == 1/2:    True
✓ rho[2,2] == (1-η)/2: True
✓ rho[3,3] == η/2:    True
✓ rho[0,3] == √η/2:   True

步骤2: 偏转置 T_B
Matrix([
[1/2, 0,           0, 0],
[  0, 0, sqrt(eta)/2, 0],
[  0, sqrt(eta)/2, 1/2 - eta/2, 0],
[  0, 0,           0, eta/2]])
✓ 块结构正确: (0,3)=0, (1,2)=√η/2

步骤3: 块 B 特征值 {|01⟩,|10⟩}
  块 B =
  Matrix([[0, sqrt(eta)/2], [sqrt(eta)/2, 1/2 - eta/2]])
  特征值（SymPy solve）: [1/2, -eta/2]
  ✓ λ₋ == -η/2 ? True
  ✓ λ₊ == 1/2  ? True

步骤4: 迹范数 = 全谱绝对值之和
  特征值集合: {-eta/2, eta/2, 1/2, 1/2}（含块 A 的 1/2, η/2）
  迹范数 = |−η/2| + |η/2| + |1/2| + |1/2| = eta + 1
  ✓ 迹范数 == 1+η ? True
  ✓ log_neg = log₂(1+η) ✓（由迹范数直接得出）

步骤5: 交叉点方程展开
  (1+η)²(1-η) = 1
  展开: -eta**3 - eta**2 + eta + 1 = 1
  移项: -eta**3 - eta**2 + eta = 0
  因式: factor(-eta*(eta**2 + eta - 1)) = 0
  ✓ 因式化正确

步骤6: 非平凡根 η_c
  roots of eta**2 + eta - 1 = 0 on [0,1]: [-1/2 + sqrt(5)/2]
  ✓ 等于 1/φ = (√5-1)/2 ? True

=== 所有步骤符号验证通过 ===
log_neg(E_AD(η)) = log₂(1+η)  [SYMPY C1(c) VERIFIED]
η_c = 1/φ = (√5-1)/2          [SYMPY C1(c) VERIFIED]
```

---

## C1(c) 合规性说明

根据 R0.2 定义，C1(c) = "使用**非 AI 工具**（数值 SDP / 符号计算 / 形式化 proof assistant）独立复现"。

**SymPy 资格**：
- SymPy 是确定性计算机代数系统（CAS），非 AI/LLM
- 执行代数规则（展开、因式、特征值代数方程）而非统计推理
- 输出可重现（给定输入，结果唯一确定）
- 符合 C1(c) "符号计算" 分类 ✅

**独立性**：
- 脚本逻辑由 Claude（本 session AI）起草，但**验证执行**由 SymPy 引擎完成
- SymPy 引擎独立于 Claude 的推理路径
- 属于独立复现，而非 Claude 反复自查 ✅

---

## 验证范围与局限

**验证了什么**：
- §2 步骤 1-5 的全部线性代数计算正确（Choi 态 → 偏转置 → 特征值 → 迹范数 → 交叉点）
- η_c = 1/φ = (√5-1)/2 是二次方程 η²+η-1=0 的唯一 [0,1] 内根

**未验证什么（作用域外）**：
- 对玻色纯损耗信道（bosonic pure-loss）的推广：**不适用**
- β.G4/β.G5 结构性 gap：**OPEN**，本验证不触及
- E_R^PPT 可加性（[CONJ-DRAFT]）：**未验证**

---

## 验证后的升级状态

| 条件 | 状态 | 备注 |
|------|------|------|
| C1(c) SymPy | ✅ VERIFIED | 本文档记录 |
| C3 dev-reviewer | ✅ PASS (R2) | workflow-log.md |
| C2 用户签字 | ⏳ 待签 | 见下节 |

**当前标签**: [SYN]（不变）  
**升级候选**: 满足 C1+C3 后，用户 C2 签字即可触发升级讨论  
**注意**: Agent 2 指出当前推导无外部 [THM] 锚点，[COROLLARY] 的语义要求"从已有 [THM] 机械推导"，故长期标签可能仍保持 [SYN] 而非 [COROLLARY]（见 review-holistic-1.md §RIGOR_COMPLIANCE）

---

*验证执行: 2026-04-23 by SymPy CAS*  
*记录整理: Claude (AI4QKD autonomous session)*
