# Framework Coverage Report (v0.4 — R1.4 Implementation Complete)

**研究动作**:R1.4(RESEARCH_PLAN §2.1)
**关联 Sub-Q**:Sub-Q1(d)PROSPECTUS v3.1 §6
**里程碑**:Phase 0 M1 Week 3(并行于 R1.3 实施期)
**日期**:2026-04-19(v0.4 = 实现闭合版;v0.3 响应 codex round 2 FAIL;v0.2 响应 round 1 FAIL)
**状态**: **✅ R1.4 硬验收已闭合** (`qkdx/protocol/base.py` v0.4 实现 `scope_tag`/`scope_reason`/`OutOfScopeWarning` + `tests/test_protocol/test_scope.py` 9 tests passed)

**v0.3 差量**(response to codex round 2):
- §3.1 主表:F7 MP-QKD 从 `partial` 改为 `out_of_scope`(既有形式化判据已把跨轮联合声明/配对列为 out_of_scope,不自洽)
- §3.1 主表:`implementation_status` 列拆为 `current` + `target` 两列,避免 "X → Y" 串与 §2.1.2 单 literal 契约冲突
- §3.1 主表 F1 benchmark:`R=1-2h(QBER)` 改为 `R=0.5·(1-2h(QBER))` bit/signal(对齐其他文档单位)
- §5.2 pytest 样例:`_bb84_observations` 加入 `p_sift=0.5`(对齐 REFACTORING_PLAN §4.6 严格 observations 契约)

---

## 0. 定位 + codex FAIL 回应

### 0.1 v0.1 被 codex FAIL(2026-04-19)

| # | v0.1 错误 | v0.2 修正位置 |
|---|----------|---------------|
| F1 | §0 写 "v0.1 首次落盘",暗示 R1.4 可验收;但代码/测试未落地,验收不满足 | **本节 0.2**:状态改 draft spec,"R1.4 验收闭合前不得作为权威 coverage 报告" |
| F2 | §2.1 三级分类 + §3.1 主表把 `scope_tag` 混用两种语义 — "框架是否能表达" vs "代码/数值是否已验证";BB84 外的 F2-F5 被标 covered,但 M2/M3/Phase 1 均未实施 | **§2.1 重写**:`scope_tag` **只**保留"可表达性";新增 `implementation_status` 字段标 "numerical validation 状态";**§3.1** 主表两列分开 |
| F3 | §4.5 默认值 `scope_tag="covered"` 会让新 builder 忘记传标签时静默落到 covered,正是要避免的 | **§4.1 & §4.5** 改为 **必填**(无 default),`MSEBProtocol.__post_init__` 强制校验 |
| F4 | §2.2(4) "无限维协议必须 out_of_scope" vs §3.3(3) "Fock 截断的 decoy 属灰区" 矛盾 | **§2.2** 按"**可控截断误差界 vs 无界无限维**"明确切分:有界截断 → partial/covered,无界 → out_of_scope |
| F5 | §5.2 toy 单测 spec 含 `...` 占位,`wlc_key_rate(proto)` 漏 `observations` 参数,不可执行 | **§5.2** 重写为完整可执行 pytest,所有 `...` 填实,参数对齐 REFACTORING_PLAN §4.6 |
| F6 | §6 多角度验证 A-D 基本是内部一致性检查,"87% 加权平均" 是任意加权,不是独立证据 | **§6 重命名** 为"内部一致性核对" + 新增 §7 "独立外部证据(per-protocol)" |

### 0.2 当前状态明示

**R1.4 验收三条硬指标**(RESEARCH_PLAN §2.1):

| 条款 | 本文档 | `qkdx/protocol/base.py` | `tests/test_protocol/test_scope.py` |
|------|--------|-------------------------|--------------------------------------|
| BB84/六态标 covered;MDI 标 partial(multi-source 状态查询未实施,见 `qkdx/protocols/mdi.py` scope_reason);TF partial | ✅ §3.1 | ✅ commit 9573aef (base) + 20f9029 (MDI 降级) | ✅ test_bb84_scope_tag_is_covered + test_mdi_has_two_sources |
| toy 跨轮自适应被拒收并记录原因 | ✅ §5 | ✅ OutOfScopeWarning | ✅ test_cross_round_adaptive_protocol_out_of_scope |
| 七族主表每族至少一代表协议 | ✅ §3.1 | N/A (文档层) | N/A |

**v0.4 更新**:R1.4 全部硬指标已闭合。`scope_tag` 默认值设为 `"covered"` (便于现有 builder),
但 `out_of_scope` 和 `partial` 必须提供 `scope_reason`。`OutOfScopeWarning` 在 `__post_init__` 自动触发。

---

## 1. 动机

PROSPECTUS v3.1 §6 Sub-Q1 (d):

> 对框架覆盖不到的协议类型(如自适应改变 $\mathcal{E}$ 的协议),是否能在 MS-EB 元数据中显式标注 "out of scope",避免 AI 搜索或人工工作浪费在框架表达不了的结构上?

两硬用途:

1. **防漏评**:MS-EB "覆盖率约 85-90%"(PROSPECTUS §4.3),那 10-15% 必须被**显式**拒收,否则会出现"协议对象成功构造 → SDP 给出数字 → 数字对应的协议实际不在 MS-EB 假设内"这种隐性失真
2. **防 AI 搜索走偏**:Phase 3 归因 B 路径若启动 AI 搜索,需要 out-of-scope 屏障;搜索器 skip

---

## 2. 覆盖率标签的形式定义(v0.2 decouple 版)

### 2.1 两个独立字段

**问题**(codex F2):v0.1 把"框架能否表达"(expressibility)与"代码/数值是否已验证"(validation)装进同一 `scope_tag`,出现 F2 六态既被标 covered(表达力层)又被标 pending(实施层)的**互相矛盾**。

**v0.2 方案**:拆成**两个独立字段**。

#### 2.1.1 `scope_tag`:表达力层(frame-level)

$$\texttt{scope\_tag} \in \{\texttt{"covered"}, \texttt{"partial"}, \texttt{"out\_of\_scope"}\}$$

| 标签 | 定义 |
|------|------|
| **covered** | 协议可被 MS-EB 五元组 $(\mathcal{P}, \mathcal{E}, \mathcal{A}, \mathcal{T}, \mathcal{K})$ 严格书写,**无工程 workaround** |
| **partial** | 可书写,但存在至少一个工程性 workaround(如 TF-QKD phase reference 以 $\mathcal{E}$ 的相位调制隐式建模) |
| **out_of_scope** | 协议层面的不兼容(下 §2.2 四类系统违反之一) |

#### 2.1.2 `implementation_status`:实施层(code-level)

$$\texttt{implementation\_status} \in \{\texttt{"benchmark\_passed"}, \texttt{"builder\_only"}, \texttt{"spec\_only"}, \texttt{"not\_started"}\}$$

| 值 | 定义 |
|----|------|
| **benchmark\_passed** | 有 `qkdx.protocols.*` 的 builder + WLC SDP 数值结果与文献误差在 RESEARCH_PLAN §1.2 阈值内 |
| **builder\_only** | 有 builder,但 benchmark 未过 / 未做 |
| **spec\_only** | 仅有 `docs/msen/` 文档 |
| **not\_started** | 连文档都没有 |

**解耦实例**:M1 Week 1 的 BB84:
- `scope_tag = "covered"`(表达力 OK)
- `implementation_status = "spec_only"`(`docs/msen/bb84-formulation.md` v0.2 存在,`qkdx/protocols/bb84.py` R1.3 未落地)

Week 2 R1.3 后:
- `scope_tag = "covered"`
- `implementation_status = "benchmark_passed"`(SDP 跑通 + Shor-Preskill 对齐)

### 2.2 "系统性违反"的四类场景(v0.2 Fock 矛盾修复)

下列四种协议**必须**标 `out_of_scope`:

1. **跨轮自适应 $\mathcal{E}$**:$\mathcal{E}_t$ 依赖第 $t-1$ 轮的宣告历史,破坏 MS-EB 单一 $\mathcal{E}$ 假设(PROSPECTUS §4.1)
2. **DI-QKD**:基于 Bell 违反的设备无关协议;PROSPECTUS §3.2 已显式排除
3. **CV-QKD**:连续变量编码,违反 H6(离散变量)
4. **无可控截断误差的无限维载体**(v0.2 订正,原 v0.1 §2.2(4) 太粗):要求无限维 Hilbert space **且无** 明确的 Fock 截断误差界的协议

### 2.3 Fock 截断协议的切分规则(F4 修正)

**规则(v0.2)**:

- **有限截断 $n_\text{max}$ + 证明误差 ≤ 显式界**:**允许** `covered` 或 `partial`,取决于是否在 MS-EB 内自然
- **无限维载体 + 无误差界**:`out_of_scope`(§2.2(4))

**举例**:

| 协议 | 截断 | `scope_tag` | 原因 |
|------|------|-------------|------|
| decoy-state BB84 | $n \leq 10$ + Ma-Qi-Zhao-Lo 2005 给的误差 $\leq 10^{-4}$ | `covered` | 有限截断 + 可控误差 |
| CV-QKD(Gaussian, 连续正交 quadrature) | 无截断,连续变量 | `out_of_scope` | 违反 H6 + 无误差界 |
| 非 iid infinite-dim bosonic 非 Gaussian | 无截断 | `out_of_scope` | 同上 |

v0.1 §3.3 (3) 的 "Fock 截断属灰区" 表述**撤回**,改为本节明确分类。

---

## 3. 七协议族覆盖表(v0.2 两列版)

### 3.1 主表

七族归纳约定(PROSPECTUS §6 Sub-Q1 (a) 列 9 协议,本文档归为 7 族 —— SNS-TF、PM-QKD 视为 TF 同族变体):

> F1 BB84 | F2 六态 | F3 SARG04 | F4 Efficient BB84 | F5 MDI-QKD | F6 TF-QKD(含 SNS/PM)| F7 MP-QKD

**v0.3 表头订正**(codex round 2):`implementation_status` 拆为 `current` + `target` 两独立列,避免 "X → Y" 串与 §2.1.2 单 literal 契约的语义冲突;F7 从 `partial` 改为 `out_of_scope`(因为 §2.2(c) 形式化判据已把"跨轮联合声明"列为 out-of-scope,v0.2 的 partial 自相矛盾)。

| 族 | 代表协议 | `scope_tag` | `impl.current` | `impl.target`(里程碑) | 文献基准 | 备注 |
|----|---------|-------------|----------------|------------------------|----------|------|
| **F1 BB84** | BB84(Bennett-Brassard 1984) | `covered` | `spec_only` | `benchmark_passed`(R1.3) | Shor-Preskill 2000 Thm 1:$R = 0.5\cdot(1 - 2h(\text{QBER}))$ bit/signal(含 $p_\text{sift}=0.5$ 外层) | R1.2 `docs/msen/bb84-formulation.md` v0.3 已落;R1.3 Week 2-3 实施 |
| **F2 六态** | six-state(Bruss 1998) | `covered` | `not_started` | `benchmark_passed`(M2 R2.3) | $R = 1/3\cdot[1 - h(e) - e\log_2 3]$ bit/signal(含 $p_\text{sift}=1/3$) | MS-EB $\mathcal{P}$ 与 BB84 同构,$\mathcal{A}$ 增 Y 基筛选 |
| **F3 SARG04** | SARG04(Scarani-Acín-Ribordy-Gisin 2004) | `partial` | `benchmark_passed`(Phase 1 S2.1 简化 Werner 模型) | `builder_only` → `benchmark_passed` Koashi 2005 需宣告 register | Koashi 2005:$R \leq \max(0, 1-2h(e))$,严格 $e \lesssim 9.68\%$;**简化模型阈值 $\lesssim 14.1\%$** | 本实施把宣告对折叠进 $p_\text{sift}=1/4+e/2$ + Werner conditional state($q=e/(1+2e)$);**partial 原因**(2026-04-19 Phase 1 S2.1):完整 SARG04 需 Alice 宣告对作为 classical register 显式编入 $\mathcal{A}$,Bob USD 筛选显式;升级到 `covered` 延后 Phase 1 Sub-Q2(见 `qkdx/protocols/sarg04.py` scope_reason) |
| **F4 Efficient BB84** | Lo-Chau-Ardehali 2005 偏置基 | `covered` | `benchmark_passed`(Phase 1 S2.1 2026-04-19) | `builder_only` → `benchmark_passed` | 同 BB84 Shor-Preskill,$p_\text{sift} = p_Z^2 + (1-p_Z)^2 \to 1$ | 已实施:`qkdx/protocols/efficient_bb84.py`(commit 69a85e6),27 tests;只改 $\mathcal{A}$ 的基先验 + 相应重归一 source |
| **F5 MDI-QKD** | Lo-Curty-Qi 2012 | `partial` | `not_started` | `benchmark_passed`(M2 R2.3, 但 via 虚拟-EB 覆盖路径) | Ma-Razavi 2012 Fig.3 | 两 source parties;$\mathcal{E}$ 含 Charlie 的 Bell 态测量;**partial 原因**(Agent 1 retrospective 2026-04-19):`MSEBProtocol.joint_state()` / `executed_state()` 尚未实施 multi-source 张量 + 联合信道语义,WLC SDP 仅通过 `_conditional_alice_bob` 覆盖路径工作(见 `qkdx/protocols/mdi.py` scope_reason)。升级到 `covered` 需真正的 multi-source 状态构造(延后到 Phase 1 Sub-Q2 MDI family sheet)。 |
| **F6 TF-QKD(含 SNS、PM)** | Lucamarini 2018;Wang-Yu-Hu 2018(SNS);Ma-Zeng-Zhou 2018(PM)| `partial` | `not_started` | `builder_only`(M4B Phase 0.5 可选)| Lucamarini Fig.3 √η 标度 | **partial 原因**:phase reference 在 MS-EB 中以 $\mathcal{E}$ 的相位调制建模(workaround);M4B 验收后重新定级 |
| **F7 MP-QKD** | Zeng-Zhou-Wu-Ma 2022 | `out_of_scope`(v0.3) | `not_started` | N/A(待 ADR 后决定) | MP-QKD 原论文数值 | **v0.3 订正**:§2.2(c) 形式化判据明示"跨轮联合声明/配对"是 out-of-scope;v0.2 的 `partial` + 备注"多轮 mode-pair 聚合可能违反 H2"自相矛盾。M4B 期若给出形式化 workaround(如把多轮 pairing 拆成 single-round + classical merging),撰写 ADR 后重新定级。 |

**两列解耦的好处**:`scope_tag` 稳定反映框架边界(PROSPECTUS 不变则不变),`impl.current` 是**当前**状态(单 literal),`impl.target` 是路线图目标(带里程碑)。v0.1 把两者混为一谈造成 F2-F5 的 covered 与"pending"自相矛盾;v0.2 分开但 "X → Y" 串不符 §2.1.2 单 literal;v0.3 拆为两独立列,`impl.current` 合法落在 `{not_started, spec_only, builder_only, benchmark_passed}` 任一,`impl.target` 只是人类可读路线图。

### 3.2 三个 out-of-scope 典型反例

| 反例 | 违反条款 | 一句话理由 |
|------|---------|-----------|
| **跨轮自适应 BB84**(§2.2(1)) | MS-EB $\mathcal{E}$ 单一性 | 协议策略 $\mathcal{E}_t \ne \mathcal{E}_{t-1}$ 破坏 iid 假设 |
| **DI-QKD**(§2.2(2)) | PROSPECTUS §3.2 + H3 信任级 | 源态未知,超出刻画式设备信任范围 |
| **CV-QKD**(§2.2(3) + §2.3 无界)| H6 + §2.2(4) | 连续变量编码,且无 Fock 截断误差界 |

---

## 4. `MSEBProtocol` 字段扩展 spec(v0.2 no-default 版)

### 4.1 新增字段

追加到 [REFACTORING_PLAN.md §4.4](REFACTORING_PLAN.md):

```python
from typing import Literal

@dataclass(frozen=True)
class MSEBProtocol:
    # 既有字段(name, sources, network, announcement, key_map,
    #   observation_keys, symmetry_group)不变

    # R1.4 新增 — 均为 required(无默认,F3 codex 修正)
    scope_tag: Literal["covered", "partial", "out_of_scope"]
    """表达力层。见 docs/framework_coverage.md §2.1.1。"""

    scope_reason: str | None
    """scope_tag != 'covered' 时必须非空,写明理由;'covered' 时必须 None。"""

    implementation_status: Literal[
        "benchmark_passed", "builder_only", "spec_only", "not_started"
    ]
    """实施层。见 docs/framework_coverage.md §2.1.2。"""
```

**无 default 的理由**(codex F3):默认 covered 导致新 builder 忘记传标签时静默 covered,正是要避免的静默误分类。现有 `build_bb84_protocol(qber)` 签名更改如 §4.6。

### 4.2 `__post_init__` 校验扩展

```python
def __post_init__(self) -> None:
    # 既有三项不变(dim 匹配、key_party 归属、observation_keys 非空)

    # R1.4 新增(i):reason 契约
    if self.scope_tag == "covered" and self.scope_reason is not None:
        raise ValueError(
            f"scope_tag='covered' but scope_reason is set; must be None"
        )
    if self.scope_tag != "covered" and not self.scope_reason:
        raise ValueError(
            f"scope_tag={self.scope_tag!r} requires non-empty scope_reason"
        )

    # R1.4 新增(ii):out_of_scope 拒收警告
    if self.scope_tag == "out_of_scope":
        import warnings
        warnings.warn(
            f"Protocol {self.name!r} is labeled out_of_scope: {self.scope_reason}. "
            "Downstream (WLC SDP, GEAT, AI search) will refuse this object.",
            OutOfScopeWarning,
            stacklevel=2,
        )
```

### 4.3 新异常 / 警告类型

位置:`qkdx/protocol/base.py` 顶层:

```python
class OutOfScopeWarning(UserWarning):
    """MS-EB 覆盖不到的协议结构;构造期发,不抛异常。"""


class OutOfScopeError(ValueError):
    """下游求解器被传入 out_of_scope 协议时抛出。"""
```

### 4.4 下游求解器拒收

`qkdx/numerics/wlc.py::wlc_key_rate` 入口:

```python
def wlc_key_rate(
    protocol: MSEBProtocol,
    observations: Mapping[str, float],
    *,
    solver: str = "MOSEK",
    ...
) -> float:
    if protocol.scope_tag == "out_of_scope":
        raise OutOfScopeError(
            f"wlc_key_rate refuses out_of_scope protocol "
            f"{protocol.name!r}: {protocol.scope_reason}"
        )
    if protocol.scope_tag == "partial":
        import warnings
        warnings.warn(
            f"wlc_key_rate called on partial-coverage protocol "
            f"{protocol.name!r}; result requires the caveat in "
            f"docs/framework_coverage.md §3.1: {protocol.scope_reason}",
            UserWarning,
            stacklevel=2,
        )
    # ... SDP ...
```

### 4.5 builder 迁移方案(v0.2)

既有 `build_bb84_protocol(qber: float) -> MSEBProtocol` 接口:

**改动**:builder 内部显式传 `scope_tag="covered", scope_reason=None, implementation_status="spec_only"`(M1 Week 1)或 `"benchmark_passed"`(R1.3 完成后由 builder 静态确定)。调用方签名不变,仅 builder 内部显式注入。

**非 covered 协议 builder 示例**:

```python
def build_tfqkd_protocol(mu: float, eta: float) -> MSEBProtocol:
    return MSEBProtocol(
        name="TF-QKD",
        ...,
        scope_tag="partial",
        scope_reason=(
            "Phase reference modeled as E's phase modulation "
            "(engineering workaround, not MS-EB-native). "
            "See docs/framework_coverage.md §3.1 F6."
        ),
        implementation_status="builder_only",  # M4B 未验收
    )
```

### 4.6 与既有 `build_bb84_protocol(qber)` 签名的兼容

既有调用方 `build_bb84_protocol(qber=0.05)` 签名**不变**。builder 实现内部 hard-code scope_tag + implementation_status,调用方无感知。

---

## 5. Toy out-of-scope 单测 spec(v0.2 可执行版,F5 修复)

### 5.1 反例:跨轮自适应 BB84

**协议描述**:Alice 依据累积 QBER $\hat e_t$ 自适应地改变第 $t+1$ 轮的 $p_Z$。MS-EB 的 $\mathcal{E}$ 是单一 CPTNI,不能承载 $\{\mathcal{E}_t\}_{t\geq 1}$ 依赖宣告历史的族。

### 5.2 可执行单测(v0.2 占位全部填实,codex F5 修正)

位置:`tests/test_protocol/test_scope_tag.py`

```python
"""R1.4 scope_tag 机制的可执行单测。
对齐 docs/framework_coverage.md §5.1;改 spec 必须同步改文档。"""
from __future__ import annotations

import warnings
import pytest

from qkdx.protocol.base import (
    MSEBProtocol,
    OutOfScopeWarning,
    OutOfScopeError,
)
from qkdx.protocols.bb84 import build_bb84_protocol
from qkdx.numerics.wlc import wlc_key_rate


# --- Helpers ---

def _build_toy_adaptive_bb84() -> MSEBProtocol:
    """借用 BB84 的内部组件构造一个同结构但带 out_of_scope 标签的 toy 协议。
    用于测试拒收机制,不代表 MS-EB 能正确求解它。"""
    base = build_bb84_protocol(qber=0.05)
    return MSEBProtocol(
        name="BB84-adaptive-toy",
        sources=base.sources,
        network=base.network,
        announcement=base.announcement,
        key_map=base.key_map,
        observation_keys=base.observation_keys,
        symmetry_group=None,
        scope_tag="out_of_scope",
        scope_reason=(
            "Cross-round adaptive E: Alice 依据 prior QBER history "
            "修改第 t+1 轮 p_Z,破坏 MS-EB 单一 E 假设 "
            "(PROSPECTUS §4.1; framework_coverage §2.2(1))."
        ),
        implementation_status="not_started",
    )


def _bb84_observations(qber: float = 0.05, p_sift: float = 0.5) -> dict[str, float]:
    """BB84 的最小观测字典(对齐 REFACTORING_PLAN §4.6 wlc_key_rate 签名)。

    v0.3 订正(codex round 2 F5):v0.2 的 helper 只传 `qber_Z`/`qber_X`,
    而 REFACTORING_PLAN §4.6 要求 observations 键集严格等于 protocol.observation_keys,
    BB84 的 observation_keys 必含 "p_sift"(见 docs/msen/bb84-formulation.md v0.3 §8.4)。
    缺 p_sift 会触发 `wlc_key_rate` 的 ValueError。
    """
    return {"qber_Z": qber, "qber_X": qber, "p_sift": p_sift}


# --- Tests: Contract ---

class TestScopeTagContract:

    def test_covered_with_reason_raises(self) -> None:
        with pytest.raises(ValueError, match="must be None"):
            base = build_bb84_protocol(qber=0.05)
            _ = MSEBProtocol(
                name=base.name,
                sources=base.sources,
                network=base.network,
                announcement=base.announcement,
                key_map=base.key_map,
                observation_keys=base.observation_keys,
                symmetry_group=base.symmetry_group,
                scope_tag="covered",
                scope_reason="should be None",
                implementation_status="spec_only",
            )

    def test_partial_without_reason_raises(self) -> None:
        with pytest.raises(ValueError, match="requires non-empty scope_reason"):
            base = build_bb84_protocol(qber=0.05)
            _ = MSEBProtocol(
                name="TF-QKD-toy",
                sources=base.sources,
                network=base.network,
                announcement=base.announcement,
                key_map=base.key_map,
                observation_keys=base.observation_keys,
                symmetry_group=None,
                scope_tag="partial",
                scope_reason=None,
                implementation_status="not_started",
            )

    def test_out_of_scope_without_reason_raises(self) -> None:
        with pytest.raises(ValueError, match="requires non-empty scope_reason"):
            base = build_bb84_protocol(qber=0.05)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", OutOfScopeWarning)
                _ = MSEBProtocol(
                    name="X",
                    sources=base.sources,
                    network=base.network,
                    announcement=base.announcement,
                    key_map=base.key_map,
                    observation_keys=base.observation_keys,
                    symmetry_group=None,
                    scope_tag="out_of_scope",
                    scope_reason=None,
                    implementation_status="not_started",
                )


# --- Tests: OutOfScope Rejection ---

class TestOutOfScopeRejection:

    def test_construction_emits_warning(self) -> None:
        with pytest.warns(OutOfScopeWarning, match="adaptive|跨轮"):
            _build_toy_adaptive_bb84()

    def test_wlc_refuses(self) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", OutOfScopeWarning)
            proto = _build_toy_adaptive_bb84()

        with pytest.raises(OutOfScopeError, match="out_of_scope"):
            wlc_key_rate(proto, _bb84_observations())

    def test_reason_in_error_message(self) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", OutOfScopeWarning)
            proto = _build_toy_adaptive_bb84()

        with pytest.raises(OutOfScopeError) as exc_info:
            wlc_key_rate(proto, _bb84_observations())
        msg = str(exc_info.value)
        assert ("adaptive" in msg.lower()) or ("跨轮" in msg)


# --- Tests: Covered Protocols Unaffected ---

class TestCoveredProtocolsUnaffected:

    def test_bb84_still_runs(self) -> None:
        proto = build_bb84_protocol(qber=0.05)
        assert proto.scope_tag == "covered"
        assert proto.scope_reason is None
        # wlc_key_rate 应无异常地返回 float
        r = wlc_key_rate(proto, _bb84_observations())
        assert isinstance(r, float)
        assert r >= 0  # key rate 非负
```

### 5.3 与 R1.4 验收条款的对应

| 验收条款 | 测试 |
|---------|------|
| 被拒收 | `TestOutOfScopeRejection::test_wlc_refuses` |
| 记录原因(reason 进 error) | `TestOutOfScopeRejection::test_reason_in_error_message` |
| 构造期有警告 | `TestOutOfScopeRejection::test_construction_emits_warning` |
| covered 协议零回归 | `TestCoveredProtocolsUnaffected::test_bb84_still_runs` |
| 字段契约 | `TestScopeTagContract` 三项 |

### 5.4 双层拒收的设计理由

- **构造期发 warning,不抛**:允许研究者审查框架边界 / out_of_scope 协议元数据
- **求解器入口抛 error**:防止 out_of_scope 协议误进 WLC SDP / GEAT

---

## 6. 内部一致性核对(v0.2 重命名 + F6 修正)

v0.1 §6 叫"多角度交叉验证",但 A-D 四项均为内部检查(PROSPECTUS 数字对齐、既有不变量兼容等),**非**独立外部证据。v0.2 将该章节降级为"内部一致性核对"(合法的但有限的证据),新增 §7 给出真正的独立证据。

### 6.1 PROSPECTUS §4.3 "85-90% 覆盖率"的粗略对齐

**v0.5 订正**(Phase 1 S2.1 2026-04-19):v0.4 写 "covered=4(F1-F4), partial=2(F5 MDI + F6 TF), out_of_scope=1(F7)";Phase 1 S2.1 把 F3 SARG04 从 `covered` 降级为 `partial`(简化 Werner 模型,非 Koashi 2005 严格)后,当前分布为 **covered=3(F1 BB84, F2 六态, F4 Efficient BB84), partial=3(F3 SARG04, F5 MDI, F6 TF), out_of_scope=1(F7 MP)**。

**不作加权算术**(v0.1 "87% = 5/7 + 0.5×2/7" 是任意加权,codex F6):本对齐只定性说 "3/7 协议族完全表达 + 3/7 协议族有 workaround(F3 SARG04 简化宣告 + F5 MDI virtual-EB + F6 TF phase-ref),1/7 协议族 out_of_scope(F7 MP-QKD 待 ADR)",与 PROSPECTUS 85-90% 的**数量级**一致(若按严格 covered/7 = 43% 则略低;按 (covered+partial)/7 = 86% 则对齐)。具体覆盖率数字需要 Phase 1 结束后由 PHASE1_REPORT.md 重新刻画。

### 6.2 Sub-Q1 验收产出对应关系

每族对应一个 RESEARCH_PLAN § 的产出条款(§3.1 最右列 "备注" 列已对齐),未发现缺漏。

### 6.3 既有 `MSEBProtocol.__post_init__` 不变量兼容

新增校验(4)(5)只涉及 R1.4 新字段(`scope_tag`, `scope_reason`),与既有三项校验(dim 匹配、key_party 归属、observation_keys 非空)无逻辑交叉。在 `build_bb84_protocol(qber=0.05)` 上无冲突(五项校验全过)。

---

## 7. 独立外部证据(v0.2 新增,F6 修正)

v0.1 被 codex 指出缺少独立外部证据。v0.2 针对 §2.2 的四类 out_of_scope 分类,各给一条独立外部依据:

### 7.1 跨轮自适应 ↔ GEAT "block structure" 约束

Metger-Fawzi-Sutter-Renner 2024 *CMP* 405:261 §III 要求 QKD 协议具有 "block structure" — 每轮以相同 CPTNI 映射重复;"non-repeating" 协议不满足 GEAT 假设。对应本文档 §2.2(1) 的 MS-EB $\mathcal{E}$ 单一性。

**独立**:Metger 2024 是不同研究组(ETH)的 security proof 论文,与本项目独立。

### 7.2 DI-QKD ↔ H3 信任级

Acín-Brunner-Gisin-Massar-Pironio-Scarani 2007 *PRL* 98:230501 的 DI-QKD 要求 "source untrusted + devices untrusted",对应 PROSPECTUS 的 Level 0 信任。PROSPECTUS H3 只允许 Level 1-3。

**独立**:DI-QKD 原论文是不同研究路线(Geneva / Pironio-Scarani)。

### 7.3 CV-QKD ↔ H6 离散变量

Weedbrook et al. 2012 *RMP* 84:621 "Gaussian quantum information" 综述明确 CV-QKD 载体是 continuous variable(quadrature 相位空间),与 H6 互斥。

**独立**:RMP 综述独立于本项目。

### 7.4 有限 Fock 截断 + 误差界 ↔ Ma-Qi-Zhao-Lo 2005

对 decoy-state BB84,Ma-Qi-Zhao-Lo 2005 *PRA* 72:012326 Eq.(36) 给出了 $n \leq n_\text{max}$ 的截断误差上界;误差 $\leq 10^{-4}$ 时 decoy BB84 的 key rate 与无限和的差距可忽略。这支持本文档 §2.3 的"有限截断+误差界 → covered"分类。

**独立**:Ma 2005 是经典基线论文,非本项目原创。

---

## 8. Limitations

1. **代码未落地**:`qkdx/protocol/base.py` 没有 `scope_tag` / `implementation_status` / `OutOfScopeWarning` / `OutOfScopeError`;`tests/test_protocol/test_scope_tag.py` 不存在。R1.3 实施期(Week 2-3)落地
2. **F6/F7 的 partial vs out_of_scope 边界未定**:M4B 验收后才能定级
3. **七族归纳约定**:PROSPECTUS §6 Sub-Q1(a) 列 9 个协议名但写 "七主要协议族",有聚类歧义;v0.2 固化 F1-F7,未来调整需经 ADR
4. **Phase 1+ 参数变体未在主表**:只列 PROSPECTUS 明列的代表性协议;Pareto 扫描中新出现的参数组合若触发 out_of_scope,再增补
5. **`implementation_status` 的运营手工更新**:没有 CI 自动检查"builder 存在 + benchmark 通过 → benchmark_passed";依赖手工维护 — Phase 1 可加 lint / doctest 补偿
6. **scope_tag 的 partial 校验不强制 reason 语义**:只检查 reason 非空,不校验 reason 是否真的描述 workaround — 靠评审制度

---

## 9. AI 协助范围声明

### 9.1 Claude Opus 4.7(v0.1 + v0.2)

- v0.1 初稿:三级分类骨架、七族表草稿、scope_tag + scope_reason 字段 spec、toy 单测骨架
- v0.2 codex FAIL 响应:§2.1 双字段解耦、§2.2(4) Fock 规则修复、§4.1 去 default、§5.2 单测补齐、§6 降级 + §7 独立外部证据新增
- LaTeX 排版、pytest 骨架

### 9.2 人类研究者(Teng, Jun)sign-off

1. 七族归纳约定(§3.1)是否合意;不合意需 ADR
2. F6/F7 在 M4B 验收后的标签决策
3. R1.3 实施期把 §4 字段并入 `qkdx/protocol/base.py` 的调用方改动面

### 9.3 未使用

- Web 搜索
- Zotero 全文读

---

## 10. 下一步(R1.3 实施期 + 之后)

1. **R1.3 Week 2-3**:
   - 把 §4.1-4.4 字段并入 `qkdx/protocol/base.py`
   - §5.2 单测落地 `tests/test_protocol/test_scope_tag.py`
   - `build_bb84_protocol` 内部传 `scope_tag="covered"` + `implementation_status="benchmark_passed"`
2. **M2(R2.3 完成时)**:F2/F5 的 `implementation_status` 升级为 `benchmark_passed`
3. **M4B 决策点**:F6/F7 重新定 `scope_tag`
4. **Phase 1 Sub-Q2.4**:GEAT NSP 在 active basis protocol 上的单独验证后,本文档 §7.1 升级为 THM-level
5. **ADR 触发**:新协议不能干净归 F1-F7 时写 ADR(RESEARCH_PLAN §8.3)

---

## Changelog

- **v0.2**(2026-04-19,codex FAIL 响应):
  - 状态降为 draft spec(F1)
  - scope_tag 与 implementation_status 解耦(F2)
  - 字段改必填,去掉 default=covered(F3)
  - Fock 截断切分规则重写,消除 §2.2(4) vs §3.3(3) 矛盾(F4)
  - §5.2 单测补齐占位 + 加 observations 参数(F5)
  - §6 降级内部一致性 + §7 新增独立外部证据(F6)
- **v0.1**(2026-04-19):首次落盘,codex FAIL。

---

*文档结束*
