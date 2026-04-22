# Q1 Decision Record: β 主攻 + γ safety net

**版本**：v1.0
**日期**：2026-04-22 Day 2 late evening
**决策者**：用户
**决策依据**：[q1_path_choice_decision_analysis_2026-04-22.md §4.2](q1_path_choice_decision_analysis_2026-04-22.md)

---

## 0. 用户决策

> "我选择 beta，第二个方案" (2026-04-22)

即 [q1_path_choice_decision_analysis §4.2](q1_path_choice_decision_analysis_2026-04-22.md)：

> **若用户目标 = 潜在最高学术价值 → 选 β, 但备份 γ**
> - β 主攻 (7-10 人日)
> - γ 并行作 fallback (5-7 人日)
> - 若 β 给更紧 bound → 新定理；若 β = Pirandola 等价 → γ 兜底

---

## 1. 授权范围

**用户 C1(b) scope** (用户纸笔):
- **Primary: β formal derivation** — close β.G1-G5
- **Secondary: γ v0.4+R3 formal derivation** (safety net) — close γ.B.G1-G3 + γ.G3 + γ.G4

**AI autonomous scope** (本次 session 继续工作):
- ✓ 深化 β scaffolding (explicit sub-gaps + literature pointers + numerical roadmap)
- ✓ 深化 γ scaffolding (same depth)
- ✓ β.G3 数值 SDP 实证 ("β bound 方向是否更紧"): 实施 $E_R^\infty(\tilde{\mathcal{M}})$ SDP for toy parameters 比较 with Pirandola min-cut
- ✗ 不替代用户 C1(b) 纸笔工作
- ✗ 不 upgrade [CONJ] → [COROLLARY] (需 C1 ∧ C2 ∧ C3)

---

## 2. α 路径状态 post-decision

**α path**: **dormant** — 根据用户决定，α 不启动 formal 工作。保留 [scaffolding-only](../proofs/umr_path_alpha_derivation.md) + [scaffolding](../proofs/umr_path_alpha_scaffolding.md) 作为 cautionary record 用于未来任何"要不要做 α"的评估。

---

## 3. Execution order (user-decided)

**Phase 1** (用户): Read β scaffolding + γ safety-net scaffolding (0.5-1 天)
**Phase 2a** (用户): β formal derivation + gap closure (7-10 人日)
**Phase 2b** (用户, 可并行): γ safety-net formal (5-7 人日)
**Phase 3** (协作): dev-reviewer + C2 签字 → 若 β 成功 = 新 theorem; 若 β = γ-equivalent, γ 兜底 → Sub-Q4 G4.2 启动

---

## 4. 后续 AI autonomous 工作 (本 session 继续)

按决策触发，AI 立即开始:

1. **β scaffolding v0.3**: 深化 β.G1-G5，加 literature reference stack, 加 numerical sub-plan
2. **γ v0.4+R3 safety-net scaffolding**: 深化 γ.B.G1-G3 + γ.G3 + γ.G4, 加 DPI formal 陈述 pointer
3. **β.G3 数值探索**: 实施 E_R^∞(M_tilde) SDP for toy (η_A, η_B), 比较 Pirandola min-cut (给用户 early signal 关于 β 方向)
4. 更新 main_question_interim_status + upper_bound_report §3.2.1 反映用户决策

---

## 5. 严谨性

- 本 decision record 仅 **process-level decision** (用户选路径, 非 rigor upgrade)
- α 不启动 formal 工作; β+γ 启动 formal work
- AI 继续 autonomous scaffolding + numerical work **保持** [CONJ] / [SYN-data]
- R0.2 C1∧C2∧C3 invariant 不变: 任何 [COROLLARY] 升级仍需完整 C1+C2+C3
