# BB84 Family Sheet

**Family tag**: `F1/F2/F3/F4` (per [framework_coverage.md §3.1](../framework_coverage.md))
**Version**: v0.1
**Last updated**: 2026-04-19
**Checklist pass**: see §8 self-check

---

## 0. Scope

### 0.1 包含的变体(In-scope)

| 变体 | 标签 | 代码 | 状态 |
|------|------|------|------|
| **BB84** | F1 | [`build_bb84_protocol`](../../qkdx/protocols/bb84.py) | `covered` — Phase 0 M1 闭合 |
| **Six-state** | F2 | [`build_sixstate_protocol`](../../qkdx/protocols/sixstate.py) | `covered` — Phase 0 M2 闭合 |
| **SARG04** | F3 | [`build_sarg04_protocol`](../../qkdx/protocols/sarg04.py) | **`partial`** — Phase 1 S2.1 实施完成(简化 Werner 模型;详见 §0.4) |
| **Efficient BB84**(Lo-Chau-Ardehali 偏置基) | F4 | [`build_efficient_bb84_protocol`](../../qkdx/protocols/efficient_bb84.py) | `covered` — Phase 1 S2.1 Week 1-3 已实施(commit 本轮) |

### 0.2 不包含的变体(Out-of-scope)

- **Decoy-state BB84**:归入 `decoy` 横切族(见 [qkdx/numerics/decoy.py](../../qkdx/numerics/decoy.py)),可与任何离散 BB84 变体组合
- **Device-independent BB84**:违反 MS-EB "单一固定 $\mathcal{E}$" 假设(见 [framework_coverage.md §2.2](../framework_coverage.md#22-out-of-scope-判据))
- **连续变量 BB84**(CV-BB84 Grosshans-Grangier):违反"离散有限维 $\mathcal{P}$"假设

### 0.4 F3 SARG04 `partial` 简化模型说明

SARG04 的 Alice 宣告非正交态对(4 对),Bob 做 USD (unambiguous state discrimination)筛选。本实施把宣告语义**折叠**进:
- `p_sift(e) = 1/4 + e/2`(从枚举 4 状态 × 2 宣告 × 2 Bob 基 × 2 结果推导)
- 筛后错误率 `q(e) = e / (1 + 2e)`
- Conditional state:`diag((1-q)/2, q/2, q/2, (1-q)/2)` Werner 形式

**简化代价**:阈值 $e \leq 14.1\%$(本模型) vs Koashi 2005 严格阈值 $\sim 9.68\%$。升级到 `covered` 需把宣告对作为 classical register 显式编入 $\mathcal{A}$(Phase 1 Sub-Q2 延后工作)。详见 [qkdx/protocols/sarg04.py](../../qkdx/protocols/sarg04.py) scope_reason。

### 0.3 共同 MS-EB 结构

本族所有变体共享:
- **$\mathcal{P}$**:Alice 单一 SourceParty(F5 MDI 才有 Bob 第二源)
- **$\mathcal{E}$**:对称去极化信道 $K_0=\sqrt{1-3p/4}I, K_{1,2,3}=\sqrt{p/4}\sigma_{x,y,z}$
- **$\mathcal{A}$**:基匹配 sifting (`outcomes[0] == outcomes[1]`)
- **$\mathcal{T}$**:$\Gamma_{Z}, \Gamma_{X}$(F2 加 $\Gamma_Y$,F3 形状不同),+ `p_sift` 标量
- **$\mathcal{K}$**:Alice 持 key,bitmap 由 key_register 索引取 mod 2

---

## 1. 参数边界表

### 1.1 BB84(F1)

| name | type | range | default | physical meaning | validated? |
|------|------|-------|---------|------------------|-----------|
| `qber` | `float` | `[0.0, 1.0]` | — | 对称去极化 QBER(Z = X 基一致) | ✓ `build_bb84_protocol` line 137 |

### 1.2 Six-state(F2)

| name | type | range | default | physical meaning | validated? |
|------|------|-------|---------|------------------|-----------|
| `qber` | `float` | `[0.0, 2/3]` | — | 对称去极化 QBER(Z = X = Y 基);上限 2/3 = 完全去极化 | ✓ `build_sixstate_protocol` line 140 |

### 1.3 SARG04(F3,简化 Werner 模型,partial)

| name | type | range | default | physical meaning | validated? |
|------|------|-------|---------|------------------|-----------|
| `qber` | `float` | `[0.0, 1.0]`(阈值检查 via WLC 输出) | — | 信道 QBER;简化模型阈值 $\lesssim 14.1\%$(Koashi 2005 严格阈值 9.68%,见 §0.4) | ✓ `build_sarg04_protocol` line 100 |

### 1.4 Efficient BB84(F4)

| name | type | range | default | physical meaning | validated? |
|------|------|-------|---------|------------------|-----------|
| `qber` | `float` | `[0.0, 1.0]` | — | 同 BB84 | ✓ `build_efficient_bb84_protocol` line 92 |
| `p_Z` | `float` | `(0.5, 1.0)` **strict** | `0.9` | Z 基概率(效率 BB84 偏置 Z);$p_X = 1 - p_Z$ | ✓ `build_efficient_bb84_protocol` line 94 |

---

## 2. 合法性约束

| 约束表达式 | 适用变体 | 错误类型 | 位置 | 反例(回归锚点) |
|---|---|---|---|---|
| `0.0 <= qber <= 1.0` | F1 | `ValueError("QBER must be in [0, 1], got <x>")` | `build_bb84_protocol` | `qber=-0.01`, `qber=1.1`, `qber=np.nan` |
| `0.0 <= qber <= 2/3` | F2 | `ValueError("QBER must be in [0, 2/3] for six-state, got <x>")` | `build_sixstate_protocol` | `qber=0.7`, `qber=-0.01` |
| `0.0 <= qber <= 1.0` | F3(构造不阻断) | `ValueError("QBER must be in [0, 1]")` | `build_sarg04_protocol` line 100 | `qber=-0.01, qber=1.1`(阈值本身 via WLC 输出 ≤ 0 判定) |
| `0.5 < p_Z < 1.0` strict | F4 | `ValueError("p_Z must be in (0.5, 1.0) strictly, got <x>")` | `build_efficient_bb84_protocol` | `p_Z=0.0`, `p_Z=0.3`, `p_Z=0.5`, `p_Z=1.0`, `p_Z=1.5` |

**已有测试覆盖**:

- F1: [`tests/test_protocols/test_bb84.py`](../../tests/test_protocols/test_bb84.py)
- F2: [`tests/test_protocols/test_sixstate.py`](../../tests/test_protocols/test_sixstate.py)
- F3: [`tests/test_protocols/test_sarg04.py`](../../tests/test_protocols/test_sarg04.py)(24 tests,含 q(e)/p_sift(e) 公式 + WLC 阈值行为 + Werner 公式对照)
- F4: [`tests/test_protocols/test_efficient_bb84.py`](../../tests/test_protocols/test_efficient_bb84.py)(27 tests,含 parametric QBER × p_Z 扫描 + input validation + source purity)

---

## 3. 参数 → MS-EB 映射

### 3.1 BB84(F1)

- **$\mathcal{P}$**:`bb84_alice_source(qber)` 构造 8-dim EB 态 $|\psi\rangle_{AA'}$(4-dim 基+值寄存器 × 2-dim 信号),线路见 [bb84.py:32-45](../../qkdx/protocols/bb84.py#L32-L45)
- **$\mathcal{E}$**:`bb84_channel(qber)` 返回 4 个 Kraus 算子的对称去极化 $K_0,K_1,K_2,K_3$([bb84.py:55-77](../../qkdx/protocols/bb84.py#L55-L77))
- **$\mathcal{A}$**:`sift_keep = lambda o: o[0] == o[1]`(Alice 基 = Bob 基)
- **$\mathcal{T}$**:`observation_keys = ("qber_Z", "qber_X", "p_sift")`;$\Gamma_Z = \mathrm{diag}(0,1,1,0)$,$\Gamma_X = (H\otimes H)\Gamma_Z(H\otimes H)^\dagger$
- **$\mathcal{K}$**:`KeyMap(key_party="Alice", bitmap={0:0, 1:1, 2:0, 3:1})`(基索引整除 2 取 mod 2)

**conditional_alice_bob override**:返回 4-dim 解析 Werner 状态 $\rho = \mathrm{diag}((1-e)/2, e/2, e/2, (1-e)/2)$,绕过 `executed_state` + `_sift_projector` 计算路径(精度 + 速度)

### 3.2 Six-state(F2)

与 BB84 的差异:
- **$\mathcal{P}$**:`key_register_dim = 6`(3 基 × 2 值),`source_state` 是 12-dim EB 态
- **$\mathcal{E}$**:**同** BB84(同一去极化信道)
- **$\mathcal{A}$**:同 BB84 `outcomes[0] == outcomes[1]`(基匹配,现在是 3-way)
- **$\mathcal{T}$**:`observation_keys` 增 `"qber_Y"`;$\Gamma_Y = (U_Y \otimes U_Y^*) \Gamma_Z (U_Y \otimes U_Y^*)^\dagger$(Y-基上 Bob 共轭处理,见 [sixstate.py:91-110](../../qkdx/protocols/sixstate.py#L91-L110) docstring)
- **$\mathcal{K}$**:`bitmap = {0:0, 1:1, 2:0, 3:1, 4:0, 5:1}`

**conditional_alice_bob override**:**复用** BB84 的 4-dim Werner 态(对称去极化信道下 Z-sifted 态形式相同,仅 SDP 约束集增 $\Gamma_Y$)

### 3.3 SARG04(F3,简化 Werner 模型)

- **$\mathcal{P}$**:复用 BB84 的 8-dim 纯 EB 态(4-dim key × 2-dim signal);**全 SARG04 需要把宣告对作为额外 classical register**,简化模型省略
- **$\mathcal{E}$**:同 BB84 去极化信道
- **$\mathcal{A}$**:**简化**为基匹配(BB84-style);**真实 SARG04** 的 USD 筛选 + Alice 宣告对被折叠进下面的 p_sift 标量 + conditional state
- **$\mathcal{T}$**:复用 BB84 的 $\Gamma_Z, \Gamma_X$;`p_sift` scaled 到 $1/4 + e/2$
- **$\mathcal{K}$**:`bitmap = {0:0, 1:1, 2:0, 3:1}` — SARG04 "sign" convention($|0\rangle, |+\rangle \to$ bit 0;$|1\rangle, |-\rangle \to$ bit 1)
- **conditional_alice_bob override**:Werner 态 $\mathrm{diag}((1-q)/2, q/2, q/2, (1-q)/2)$,$q(e) = e/(1+2e)$
- **推导**:见 [qkdx/protocols/sarg04.py](../../qkdx/protocols/sarg04.py) docstring,基于枚举 4 状态 × 2 宣告对 × 2 Bob 基 × 2 Bob 结果,应用 USD 筛选条件

### 3.4 Efficient BB84(F4)

- **$\mathcal{P}$**:**偏置权重**纯 EB 态,8-dim 列向量幅值 $\sqrt{p_Z/2}$(Z 分量)+ $\sqrt{(1-p_Z)/4}$(X 分量),确保基匹配 $P(Z)=p_Z$、$P(X)=1-p_Z$;见 [efficient_bb84.py:32-55](../../qkdx/protocols/efficient_bb84.py#L32-L55)
- **$\mathcal{E}$**:同 BB84(`bb84_channel(qber)` 对称去极化)
- **$\mathcal{A}$**:基匹配 `outcomes[0] == outcomes[1]`,但先验概率偏置,导致 $p_{\text{sift}} = p_Z^2 + (1-p_Z)^2$
- **$\mathcal{T}$**:复用 BB84 的 $\Gamma_Z, \Gamma_X$;`p_sift` observable 缩放为 $p_{\text{sift}} \cdot I/4$
- **$\mathcal{K}$**:同 BB84 `bitmap = {0:0, 1:1, 2:0, 3:1}`
- **conditional_alice_bob override**:**复用** BB84 的 Werner 形式 $\rho = \mathrm{diag}((1-e)/2, e/2, e/2, (1-e)/2)$;**bias 在条件化(Z-sifting)时被吸收,不影响条件分布**
- **Key rate**:$R = p_{\text{sift}} \cdot (1 - h(e) - f_{\text{ec}} \cdot h(e))$,$p_Z \to 1$ 时 $p_{\text{sift}} \to 1$ 达 BB84 两倍

---

## 4. `build_*_protocol(...)` 签名规范

### 4.1 F1 / F2(已实施)

```python
def build_bb84_protocol(qber: float) -> MSEBProtocol:
    """Construct the BB84 MS-EB protocol object for a given QBER.

    Args:
        qber: Symmetric depolarising QBER, in [0, 1].

    Returns:
        MSEBProtocol with scope_tag='covered' (inherited default);
        conditional_alice_bob_dim() = 4;
        observation_keys = ("qber_Z", "qber_X", "p_sift").

    Raises:
        ValueError: if qber not in [0, 1].

    References:
        Winick-Lütkenhaus-Coles 2018 §5;
        Coles-Metodiev-Lütkenhaus 2016 §3.
    """

def build_sixstate_protocol(qber: float) -> MSEBProtocol:
    """Same as BB84, but with a Y-basis observable Γ_Y added.

    Args:
        qber: Symmetric depolarising QBER, in [0, 2/3].

    Returns:
        MSEBProtocol with scope_tag='covered';
        observation_keys = ("qber_Z", "qber_X", "qber_Y", "p_sift").

    Raises:
        ValueError: if qber not in [0, 2/3].

    References:
        Bruss 1998, PRL 81:3018;
        Lo 2001, QIC 1:81.
    """
```

### 4.2 F4(已实施)

```python
def build_efficient_bb84_protocol(qber: float, p_Z: float = 0.9) -> MSEBProtocol:
    """Construct the Efficient BB84 (F4) MS-EB protocol.

    Args:
        qber: Symmetric depolarising QBER (Z = X basis), in [0, 1].
        p_Z: Z-basis selection probability, must be in (0.5, 1.0) strictly.
             Default 0.9 (typical efficient BB84 bias).

    Returns:
        MSEBProtocol with scope_tag='covered';
        p_sift = p_Z^2 + (1-p_Z)^2;
        observation_keys = ("qber_Z", "qber_X", "p_sift").

    Raises:
        ValueError: qber not in [0, 1], or p_Z not in (0.5, 1.0).

    References:
        Lo-Chau-Ardehali 2005, J. Cryptology 18:133.
    """
```

### 4.3 F3(已实施,simplified partial)

```python
def build_sarg04_protocol(qber: float) -> MSEBProtocol:
    """Construct the SARG04 (F3) MS-EB protocol (simplified, partial scope).

    Args:
        qber: Symmetric depolarising channel QBER (Z = X), in [0, 1].

    Returns:
        MSEBProtocol with scope_tag='partial':
            - conditional_alice_bob_dim() = 4
            - Conditional state Werner(q) with q = e/(1+2e)
            - p_sift = 1/4 + e/2
            - Simplified threshold ~14.1% (Koashi 2005 exact ~9.68%)

    Raises:
        ValueError: if qber not in [0, 1].

    References:
        Scarani-Acín-Ribordy-Gisin 2004, PRL 92:057901;
        Koashi 2005, quant-ph/0507154;
        Fung-Tamaki-Lo 2006, PRA 73:012337.
    """
```

---

## 5. 数值验证锚点

### 5.1 已有(F1, F2)

| 变体 | 测试文件 | 对照文献 | 阈值 | 状态 |
|------|----------|----------|------|------|
| F1 BB84 | `test_wlc_bb84.py::test_wlc_bb84_matches_shor_preskill` | Shor-Preskill 2000 | MOSEK `rel=0.01, abs=5e-4`;CLARABEL `rel=0.02, abs=1e-3` | ✅ 6 QBER 点 parametric |
| F1 BB84 | `test_wlc_bb84.py::test_wlc_bb84_above_threshold_gives_zero` | QBER > 11% → R ≈ 0 | abs=5e-4 | ✅ |
| F1 BB84 | `test_wlc_bb84.py::test_wlc_regularization_uses_convex_combination` | 正则化 convex-combo 回归 | — | ✅(MOSEK) |
| F2 Six-state | `test_sixstate.py::test_wlc_sixstate_matches_analytic` | Lo 2001 + Scarani 2009 | 同上 | ✅ |

### 5.2 F4 已补(commit 本轮)

| 测试 | 对照 | 阈值 | 状态 |
|------|------|------|------|
| `test_wlc_efficient_bb84_matches_analytic` | $R = p_{\text{sift}} \cdot (1-h-f_{\text{ec}}h)$;5 (QBER,p_Z) 点 | MOSEK `5e-4`;CLARABEL `1e-3` | ✅ |
| `test_efficient_bb84_beats_bb84_at_p_Z_09` | ratio $\approx p_{\text{sift}}/0.5 = 1.64$ | `rel=0.02` | ✅ |
| `test_source_state_basis_weights` | 基边缘 $P(Z)=p_Z, P(X)=1-p_Z$(4 个 p_Z 点) | `1e-10` | ✅ |
| `test_source_state_is_pure_normalized` | trace=1, rank=1(4 个 p_Z 点) | `1e-10` | ✅ |

### 5.3 F3 已补(commit 本轮,简化模型)

| 测试 | 对照 | 阈值 | 状态 |
|------|------|------|------|
| `test_sarg04_sifted_qber_formula` | $q(e) = e/(1+2e)$(4 点) | `1e-12` | ✅ |
| `test_sarg04_p_sift_formula` | $p_s(e) = 1/4 + e/2$(4 点) | `1e-12` | ✅ |
| `test_wlc_sarg04_gives_positive_rate_below_threshold` | WLC R > 0 @ qber ∈ {0, 0.02, 0.05, 0.08} | — | ✅ |
| `test_wlc_sarg04_above_simplified_threshold_gives_zero` | qber=0.16 → R ≤ 5e-4 | — | ✅ |
| `test_wlc_sarg04_matches_werner_formula` | WLC vs $p_s \cdot (1 - 2h(q))$ | `rel=0.02, abs=1e-3` | ✅ |
| `test_source_state_is_pure_normalized` | rank-1 + trace-1(5 QBER 点) | `1e-10` | ✅ |

### 5.4 待补(F3 完整版)

- F3 Koashi 2005 完整验证:需要宣告对显式 register + USD 筛选(Phase 1 Sub-Q2 延后)

---

## 6. Bearing 与参考资料

### 6.1 主文献

- **F1 BB84**:Bennett-Brassard 1984, IEEE Conf. on Comp., Syst. and Signal Proc.;Shor-Preskill 2000, PRL 85:441
- **F2 Six-state**:Bruss 1998, PRL 81:3018;Lo 2001, QIC 1:81
- **F3 SARG04**:Scarani-Acín-Ribordy-Gisin 2004, PRL 92:057901;Koashi 2005, quant-ph/0507154
- **F4 Efficient BB84**:Lo-Chau-Ardehali 2005, J. Cryptol. 18:133

### 6.2 Phase 0 工具依赖

- [qkdx/numerics/wlc.py](../../qkdx/numerics/wlc.py):WLC SDP 评估器
- [qkdx/analytic/shor_preskill.py](../../qkdx/analytic/shor_preskill.py):BB84 解析基线
- [qkdx/analytic/six_state.py](../../qkdx/analytic/six_state.py):six-state 解析基线
- [qkdx/protocol/base.py](../../qkdx/protocol/base.py):MS-EB 五元组数据类(含 scope 机制)

### 6.3 Sub-Q3 上界预期 bearing

- BB84 族在 Phase 2 Sub-Q3 中受 **PLOB 单一信道上界** $R \leq -\log_2(1-\eta)$ 约束(纯损耗极限)
- Six-state vs BB84 的**下界 gap** 来自 Eve 多一维 POVM 约束 → Phase 2 Sub-Q4 gap 分析起点

---

## 7. Pareto 搜索预留(Phase 1 S2.2 Week 4-8)

待 S2.2 启动后填充:

- **F1 BB84 Pareto 轴**:`(QBER, R)` 单点评估,Pareto 前沿退化为阈值函数
- **F4 Efficient BB84 Pareto 轴**:$(p_Z, \text{QBER}) \to R \cdot p_{\text{sift}}(p_Z)$,BO 在 $p_Z \in (0.5, 1.0)$ 搜索最优 bias

---

## 8. Self-check(按 `_checklist.md`)

| 章节 | 项 | F1 | F2 | F3 | F4 |
|------|------|----|----|----|----|
| §0 基本元信息 | 标题/scope/out-of-scope/代码引用 | ✓ | ✓ | ✓(partial 说明 §0.4) | ✓ |
| §1 参数边界表 | 完整/类型/range/default | ✓ | ✓ | ✓ | ✓ |
| §2 合法性约束 | 表达式/错误类型/位置/反例 | ✓ | ✓ | ✓ | ✓ |
| §3 MS-EB 映射 | 五分量显式映射 | ✓ | ✓ | ✓(简化模型) | ✓ |
| §4 签名规范 | 签名 + docstring + scope_tag | ✓ | ✓ | ✓(partial) | ✓ |
| §5 数值锚点 | 回归测试 + 阈值 | ✓ | ✓ | ✓(24 tests, 简化 Werner) | ✓(27 tests) |
| §6 Bearing | 文献 + 模块 + Sub-Q3 | ✓ | ✓ | ✓ | ✓ |

**通过门槛**:F1, F2, F3, F4 全部项 ✓(F3 为 `partial` 简化模型,完整 Koashi 2005 验证延后);本 sheet v0.3:F3 SARG04 从 spec_only 升级到 partial。

---

## 9. 变更日志

- **v0.1** (2026-04-19):初稿。F1/F2 对齐 Phase 0 已实施代码;F3/F4 作为 Phase 1 S2.1 Week 1-3 spec_only 占位。
- **v0.2** (2026-04-19):F4 Efficient BB84 实施完成(commit 本轮)。`qkdx/protocols/efficient_bb84.py` + `tests/test_protocols/test_efficient_bb84.py`(27 tests),scope_tag 从 spec_only → covered。
- **v0.3** (2026-04-19):F3 SARG04 简化 Werner 模型实施(commit 本轮)。`qkdx/protocols/sarg04.py` + `tests/test_protocols/test_sarg04.py`(24 tests),scope_tag 从 spec_only → **partial**。阈值 14.1%(简化模型) vs Koashi 2005 严格 9.68%,完整 SARG04 的宣告 register 延后到 Phase 1 Sub-Q2 升级。
