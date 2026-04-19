# Protocol Family Sheet — 验收检查清单

**Scope**: `docs/families/bb84_family.md`, `mdi_family.md`, `tfqkd_family.md` (RESEARCH_PLAN §3.1 S2.1)
**验收口径**: 每份 family sheet 必须逐项通过本清单,缺一不可通过
**Last updated**: 2026-04-19

---

## 0. 基本元信息

- [ ] **文档标题** 明确标注协议族名称 + 版本号 + 最后更新日期
- [ ] **Scope 声明** 列出本族包含的变体(如 "BB84 + six-state + SARG04 + Efficient BB84")
- [ ] **Out-of-scope 声明** 列出**不**包含的变体及其原因(引到 `framework_coverage.md` 或 `RESEARCH_PLAN.md`)
- [ ] **对应代码模块** 显式引用 `qkdx/protocols/<family>.py` 及其 `build_*_protocol(...)` 构造函数列表

## 1. 参数边界表(硬验收项 1)

每个族成员必须提供 **参数边界表**,每行一个可调参数,列:

| 列名 | 必填 | 说明 |
|------|------|------|
| `name` | ✓ | 参数在 `build_*_protocol` 签名中的形参名 |
| `type` | ✓ | `float` / `int` / `str` / `tuple[...]` 等具体 Python 类型 |
| `range` | ✓ | 合法值区间,如 `[0, 0.5]` 或 `{"Z", "X", "Y"}` |
| `default` | ✓ | 默认值(若 `build_*_protocol` 签名提供默认) |
| `physical meaning` | ✓ | 对应的物理量(QBER / loss / intensity 等) |
| `validated?` | ✓ | 是否已在 `__post_init__` 或 `build_*_protocol` 入口校验(✓/✗) |

- [ ] **表格完整**:所有 `build_*_protocol` 形参都在表中出现,无遗漏
- [ ] **范围可验证**:`range` 列可直接转为 `if not (... <= x <= ...)` 校验代码
- [ ] **默认值与代码一致**:表中 `default` == `build_*_protocol` 签名默认值

## 2. 合法性约束(硬验收项 2)

参数组合的约束条件,表达为 predicate 列表:

- [ ] **每个约束** 有:`约束表达式`(数学形式)+ `违反时的错误类型`(`ValueError` / `NotImplementedError` 等)+ `在代码中的位置`
- [ ] **约束可测试**:`tests/test_protocols/test_<family>.py` 中有至少一个测试对每个约束断言 `raises(ValueError)` 或等价
- [ ] **典型反例**:列出至少 3 个违反约束的参数组合供回归测试锚定

典型示例(decoy BB84):

| 约束表达式 | 错误类型 | 位置 | 反例 |
|---|---|---|---|
| `0 < μ_decoy < μ_signal` | `ValueError` | `build_decoy_bb84_protocol` 入口 | `μ_decoy=0.5, μ_signal=0.5` (等) |

## 3. 参数 → MS-EB 映射(硬验收项 3)

对每个变体,给出从参数元组 $(\theta_1, \theta_2, \ldots)$ 到 `MSEBProtocol` 五元组 $(\mathcal{P}, \mathcal{E}, \mathcal{A}, \mathcal{T}, \mathcal{K})$ 各分量的显式映射:

- [ ] **$\mathcal{P}$ (sources)**:每个 `SourceParty` 的 `source_state` 如何由参数构造(含 `key_register_dim` × `signal_register_dim`)
- [ ] **$\mathcal{E}$ (network)**:`channel.kraus` 由哪些参数决定;若为 noisy channel,Kraus 表达式显式给出
- [ ] **$\mathcal{A}$ (announcement)**:`sift_keep` 的逻辑(基匹配 / 强度分箱 / Bell 测量结果等)
- [ ] **$\mathcal{T}$ (tomography / observables)**:`observation_keys` 列表 + 每个 $\Gamma_k$ 的矩阵形式
- [ ] **$\mathcal{K}$ (key_map)**:`bitmap` 的定义 + key_party 归属

**建议格式**: 用 LaTeX block + Python 伪代码双栏展示,便于交叉验证。

## 4. `build_*_protocol(...)` 签名规范(硬验收项 3 续)

- [ ] **函数签名** 用代码块展示(含类型注解 + 默认值)
- [ ] **docstring** 覆盖:Args / Returns / Raises / References(引用原论文)
- [ ] **返回的 `MSEBProtocol.scope_tag`** 明确标注(covered / partial / out_of_scope + scope_reason)
- [ ] **`_observable_builders` 注册** 若使用覆盖机制(如 MDI `_conditional_alice_bob`),需在 docstring 中声明并引用 [base.py](../../qkdx/protocol/base.py) 对应字段

## 5. 数值验证锚点(硬验收项 4 — 独立于以上,但 `_checklist.md` 强制)

- [ ] **族内至少一个变体** 有 WLC SDP 数值 vs 文献解析的回归测试 (`tests/test_protocols/test_<family>.py`)
- [ ] **验收阈值** 遵循 REFACTORING_PLAN §9(4) + §11.4:MOSEK `rel=0.01, abs=5e-4`;CLARABEL fallback `rel=0.02, abs=1e-3`
- [ ] **pinned 数值** 至少一个测试 pin 到 7 位数字的精确值(防止数值悄悄漂移)

## 6. Bearing / 参考资料

- [ ] **主文献列表** 每个变体至少一篇原始论文 + 对应 `docs/literature/<tag>.md`(如存在)
- [ ] **Phase 0 工具依赖** 声明本 sheet 依赖哪些 `qkdx/` 模块(`numerics/wlc.py` / `analytic/*.py` / ...)
- [ ] **Phase 2 上界回放** 标注本族在 Sub-Q3 上界分析中的预期 bearing(如 "BB84 族受 PLOB 单一信道上界约束")

---

## 7. 审阅流程

1. **Self-check**: 作者按本清单逐项打勾,任一项未勾选不得提交
2. **TDD 规范**(CLAUDE.md):任何新 `build_*_protocol` 必须先有测试再有实现
3. **Codex dual-review**(按需): 对大变更(如 MDI multi-source 实现)走 `/dev-reviewer` skill 双 Agent 评审

## 8. 模板 / 范例

新建 family sheet 时,推荐先从 `bb84_family.md` 复制结构(它是最简族 + 最成熟实现),再按具体族差异替换内容。
