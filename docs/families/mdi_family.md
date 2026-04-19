# MDI-QKD Family Sheet

**Family tag**: `F5` (per [framework_coverage.md §3.1](../framework_coverage.md))
**Version**: v0.1
**Last updated**: 2026-04-19
**Checklist pass**: see §8 self-check
**Scope status**: `partial` — 详见 §0.4

---

## 0. Scope

### 0.1 包含的变体(In-scope)

| 变体 | 代码 | 状态 |
|------|------|------|
| **Ideal symmetric MDI-QKD**(无损、单光子、对称 QBER) | [`build_mdi_protocol`](../../qkdx/protocols/mdi.py) | `partial` — Phase 0 M2 闭合(via virtual-EB) |
| **Decoy MDI-QKD** | 未实施 | `spec_only` — Phase 1 S2.1 Week 1-3 起稿 |
| **Polarization encoding MDI** | 未实施 | `spec_only` — 对 `conditional_alice_bob` 无实质影响(编码仅改 Kraus) |
| **Time-bin encoding MDI** | 未实施 | `spec_only` — 同上,差异在 source state 构造 |
| **Asymmetric-loss MDI**(η_A ≠ η_B) | 未实施 | `spec_only` — Phase 1 S2.2 Pareto 需要 |

### 0.2 不包含的变体(Out-of-scope)

- **MDI-CV-QKD**:违反离散有限维 $\mathcal{P}$(与 CV-BB84 同理)
- **Measurement-device-independent QDS**(数字签名变体):属于 QDS 而非 QKD 主线
- **Post-MDI loopholes**(如 side-channel 攻击建模):违反 MS-EB "Eve 控 $\mathcal{E}$" 的全权假设

### 0.3 共同 MS-EB 结构

- **$\mathcal{P}$**:**两个** SourceParty(Alice + Bob),各自 4-dim key × 2-dim signal
- **$\mathcal{E}$**:Charlie 的 Bell 测量 + 公开声明(virtual-EB picture 简化为恒等 + 声明为独立 $\mathcal{A}$)
- **$\mathcal{A}$**:Alice-Bob 基匹配 **与** Charlie 成功(本实施把 Charlie 成功概率吸收进 $p_{\text{sift}}$,见 §0.4)
- **$\mathcal{T}$**:$\Gamma_Z, \Gamma_X$ 对应 Alice-Bob effective QBER
- **$\mathcal{K}$**:Alice 持 key(Bob 在 sifting 后做 bit flip 对齐,等效表达由 bitmap 吸收)

### 0.4 `partial` 的原因(关键)

(Agent 1 retrospective review 2026-04-19,commit `20f9029`)

- **symptom**:`MSEBProtocol.joint_state()` / `executed_state()` 对 `len(sources) > 1` 的 MDI 直接 raise `MultiSourceNotImplementedError`
- **workaround**:`build_mdi_protocol` 注册 `_conditional_alice_bob` override,返回与 BB84 同形的 4×4 Werner 状态,**绕过** base-class 状态构造;WLC SDP 仅消费 override + `_cond_dim`,不访问 `joint_state`
- **数值正确性**:理想对称情况下 WLC vs GLLP ideal symmetric 误差 `8.33e-08`,优于 MOSEK 阈值(见 [tests/test_protocols/test_mdi.py](../../tests/test_protocols/test_mdi.py))
- **升级路径**(Phase 1 S2.1 目标):
  1. 在 [qkdx/protocol/base.py](../../qkdx/protocol/base.py) 实施真正的 multi-source `executed_state`:对每个 source 的 `source_state` 做 tensor product,对组合 `(dim_A_signal × dim_B_signal)` → 应用 `network.channel`(Charlie 的 Bell-POVM Kraus)
  2. 把 `_mdi_sift_keep` 升级为 3-tuple(Alice 基,Bob 基,Charlie 声明)
  3. 将 `scope_tag` 从 `partial` → `covered`,同步 [framework_coverage.md](../framework_coverage.md) + [docs/PHASE0_REPORT.md](../PHASE0_REPORT.md)

---

## 1. 参数边界表

### 1.1 Ideal symmetric MDI(已实施)

| name | type | range | default | physical meaning | validated? |
|------|------|-------|---------|------------------|-----------|
| `qber` | `float` | `[0.0, 1.0]` | — | Alice-Bob effective QBER(对称 Z=X 基) | ✓ `build_mdi_protocol` line 116 |
| `p_sift` | `float` | `(0.0, 1.0]` | `0.25` | 筛选概率 = 1/2 基匹配 × 1/2 理想 Bell 成功率 | ✓ `build_mdi_protocol` line 118 |

### 1.2 Decoy MDI(拟实施)

| name | type | range | default | physical meaning | validated? |
|------|------|-------|---------|------------------|-----------|
| `mu_signal` | `float` | `(0.0, 1.0]` | `0.5` | 信号态强度(平均光子数) | ✗ 待实施 |
| `mu_decoy` | `float` | `(0.0, mu_signal)` | `0.1` | 诱骗态强度 | ✗ 待实施 |
| `mu_vacuum` | `float` | `[0.0, mu_decoy)` | `0.0` | 真空态强度 | ✗ 待实施 |
| `eta_A` | `float` | `(0.0, 1.0]` | `1.0` | Alice 端信道透射率 | ✗ 待实施 |
| `eta_B` | `float` | `(0.0, 1.0]` | `1.0` | Bob 端信道透射率 | ✗ 待实施 |
| `p_dark` | `float` | `[0.0, 1.0)` | `1e-6` | 探测器暗计数率 | ✗ 待实施 |

### 1.3 Polarization encoding MDI(拟实施)

同 ideal symmetric,加:

| name | type | range | default | physical meaning |
|------|------|-------|---------|------------------|
| `misalignment_angle` | `float` | `[0.0, π/4]` | `0.0` | 偏振基不对齐角度 |

### 1.4 Time-bin encoding MDI(拟实施)

| name | type | range | default | physical meaning |
|------|------|-------|---------|------------------|
| `delta_phi` | `float` | `[0.0, π]` | `0.0` | 时间-bin 相位参考偏差 |

---

## 2. 合法性约束

| 约束表达式 | 适用变体 | 错误类型 | 位置 | 反例 |
|---|---|---|---|---|
| `0.0 <= qber <= 1.0` | Ideal | `ValueError` | `build_mdi_protocol` line 116 | `qber=-0.01`, `qber=1.1` |
| `0.0 < p_sift <= 1.0` | Ideal | `ValueError` | `build_mdi_protocol` line 118 | `p_sift=0.0`, `p_sift=1.5` |
| `0 < mu_decoy < mu_signal <= 1` | Decoy | `ValueError` | `build_decoy_mdi_protocol`(pending) | `mu_decoy=0.5, mu_signal=0.5` |
| `0 <= mu_vacuum < mu_decoy` | Decoy | `ValueError` | `build_decoy_mdi_protocol`(pending) | `mu_vacuum=0.2, mu_decoy=0.1` |
| `0 < eta_A, eta_B <= 1` | Decoy/Asymmetric | `ValueError` | `build_asymmetric_mdi_protocol`(pending) | `eta_A=0.0`, `eta_B=1.5` |

**已有测试覆盖**:

- Ideal: [`tests/test_protocols/test_mdi.py`](../../tests/test_protocols/test_mdi.py)
  - `test_invalid_qber` / `test_invalid_p_sift`
  - `test_mdi_joint_state_raises_multi_source` / `test_mdi_executed_state_raises_multi_source`(`partial` 门禁)
  - `test_mdi_sift_keep_*`(sift 规则 3 case)
- Decoy / asymmetric: 待 TDD

---

## 3. 参数 → MS-EB 映射

### 3.1 Ideal symmetric MDI(已实施,virtual-EB 简化路径)

- **$\mathcal{P}$**:两个 `SourceParty`,均复用 `bb84_alice_source(qber)` 构造(4-dim key × 2-dim signal,4-dim EB 态)
  - Alice: `name="Alice"`
  - Bob: `name="Bob"`
- **$\mathcal{E}$**:`KrausMap.identity(4)` on 4-dim($A'\otimes B'$ 组合空间)— **Charlie 的 Bell 测量 + 声明被吸收进 `_conditional_alice_bob` override,不显式走 channel**
- **$\mathcal{A}$**:`_mdi_sift_keep(outcomes) = (outcomes[0] == outcomes[1])` — **仅**检查 Alice-Bob 基匹配;**Charlie 声明成功概率 0.5 被吸收进外部 `p_sift=0.25`**(见 [mdi.py:82-102](../../qkdx/protocols/mdi.py#L82-L102) docstring)
- **$\mathcal{T}$**:`observation_keys = ("qber_Z", "qber_X", "p_sift")`;复用 BB84 的 $\Gamma_Z, \Gamma_X$
- **$\mathcal{K}$**:`KeyMap(key_party="Alice", bitmap={0:0,1:1,2:0,3:1})`;等效表达下 Bob 的 bit flip 吸收进 EB 对态约定

**conditional_alice_bob override**:返回 BB84 形式 $\rho = \mathrm{diag}((1-e)/2, e/2, e/2, (1-e)/2)$,per Lo-Curty-Qi 2012 §II virtual-EB picture

### 3.2 Decoy MDI(拟实施)

- **$\mathcal{P}$**:同 ideal,但 `source_state` 需引入 Fock 截断后的强度 μ 加权叠加
- **$\mathcal{E}$**:Charlie Bell POVM + 探测器暗计数(dark count 通过 Kraus 扩展表达)
- **$\mathcal{A}$**:3-tuple(Alice 基,Bob 基,Charlie 声明 ∈ {Φ+, Ψ-, fail}),筛选条件 `basis match AND Charlie in {Φ+, Ψ-}`
- **$\mathcal{T}$**:增 `gain_Q_μ`(各强度 μ 的 gain 量)+ `qber_μ`
- **$\mathcal{K}$**:同 ideal

### 3.3 升级 ideal partial → covered 的设计要点(Phase 1 S2.1 目标)

```python
# qkdx/protocol/base.py 升级草稿:
def executed_state(self) -> Matrix:
    """Multi-source tensor + joint-channel state."""
    # 1. Tensor product each source's EB state
    rho_joint_AA_prime = reduce(tensor_product,
                                 (s.source_state for s in self.sources))
    # 2. Apply network channel to combined signal registers
    d_signals = prod(s.signal_register_dim for s in self.sources)
    # ... (I_A1..n ⊗ E) ρ_joint (I_A1..n ⊗ E^†)
    # 3. Result: rho_{A1..An, B}, dim = (prod key_dims) × network.dim_out
```

**关键测试**:新 multi-source `executed_state` 应用于 ideal MDI,与当前 `_conditional_alice_bob` override 给出的 4×4 约化态经 `p_sift=0.25` 归一化后**数值一致**(误差 < 1e-10)。

---

## 4. `build_*_protocol(...)` 签名规范

### 4.1 已实施

```python
def build_mdi_protocol(qber: float, p_sift: float = 0.25) -> MSEBProtocol:
    """Ideal symmetric MDI-QKD MS-EB protocol.

    Args:
        qber: Alice-Bob effective QBER in Z and X bases (symmetric).
        p_sift: Sifting probability. Default 0.25 (1/2 basis match ×
                1/2 Charlie Bell success).

    Returns:
        MSEBProtocol with scope_tag='partial' (multi-source state queries
        not implemented); WLC SDP works via _conditional_alice_bob override.

    Raises:
        ValueError: qber out of [0, 1] or p_sift out of (0, 1].

    References:
        Lo-Curty-Qi 2012, PRL 108:130503;
        Ma-Razavi 2012, PRA 86:062319.
    """
```

### 4.2 拟实施目标签名

```python
def build_decoy_mdi_protocol(
    mu_signal: float = 0.5,
    mu_decoy: float = 0.1,
    mu_vacuum: float = 0.0,
    eta_A: float = 1.0,
    eta_B: float = 1.0,
    p_dark: float = 1e-6,
) -> MSEBProtocol:
    """Decoy MDI-QKD (Ma-Razavi 2012 full model)."""

def build_asymmetric_mdi_protocol(
    qber: float, eta_A: float, eta_B: float, p_sift: float | None = None,
) -> MSEBProtocol:
    """Asymmetric-loss MDI-QKD for Pareto sweep S2.2."""

def build_polarization_mdi_protocol(
    qber: float, misalignment_angle: float = 0.0, p_sift: float = 0.25,
) -> MSEBProtocol:
    """Polarization-encoded MDI (differs in SourceParty.source_state)."""
```

---

## 5. 数值验证锚点

### 5.1 已有

| 测试 | 对照 | 阈值 | 结果 |
|------|------|------|------|
| `test_wlc_mdi_matches_analytic` | GLLP ideal symmetric | MOSEK `5e-4`;CLARABEL `1e-3` | **8.33e-08** ✅ |
| `test_wlc_mdi_is_bb84_halved` | BB84 rate × 0.5(p_sift 比 0.25/0.5) | 同上 | 精确 0.5000 ✅ |
| `test_mdi_zero_qber` | R = 0.25 | 同上 | ✅ |

### 5.2 待补(Phase 1 S2.1-S2.2)

- **Ma-Razavi 2012 Fig.3 对齐**(Phase 0 M2 延后项,Round 4 review commit `21f226d`):需要 decoy + asymmetric loss → 在 `build_decoy_mdi_protocol` + `build_asymmetric_mdi_protocol` 实施后承接
- Polarization misalignment 回归:与 Ma-Razavi Fig.2 对齐 5%

---

## 6. Bearing 与参考资料

### 6.1 主文献

- **Lo-Curty-Qi 2012**, PRL 108:130503 (arXiv:1109.1473) — 原 MDI 提案
- **Ma-Razavi 2012**, PRA 86:062319 (arXiv:1204.4856) — 数值基线 + Fig.3
- **Rubenok et al. 2013**, PRL 111:130501 — 首次实验
- [docs/literature/MDI-QKD.md](../literature/MDI-QKD.md)(Level 2-3 memo)
- [docs/msen/mdi-formulation.md](../msen/mdi-formulation.md)

### 6.2 Phase 0 工具依赖

- `qkdx/protocols/bb84.py`(复用 source + observables)
- `qkdx/analytic/gllp.py`(GLLP + `mdi_ideal_symmetric_rate`)
- `qkdx/numerics/wlc.py`

### 6.3 Sub-Q3 上界预期 bearing

- MDI 作为"两方 + untrusted relay"拓扑,是 **PLOB 推广上界**(Pirandola 2019 end-to-end capacity)最直接的 testbed
- Sub-Q4 gap 分析:MDI-QKD 下界(WLC) vs Pirandola 2019 上界,gap 可能来自 relay 非信任假设在 LOCC 上的松紧度

---

## 7. Pareto 搜索预留(Phase 1 S2.2)

- **Pareto 轴**:`(eta_A, eta_B, mu_signal, mu_decoy) → (gain_Q, R_key)`
- **Ma-Razavi Fig.3 对齐**:在 eta_A = eta_B 对称情形下扫 `total_distance ∈ [0, 200] km`,对比 Fig.3 的密钥率 vs 距离曲线(硬阈值 `rel=0.05`)

---

## 8. Self-check(按 `_checklist.md`)

| 章节 | 项 | Ideal | Decoy | Asymmetric | Polarization | Time-bin |
|------|------|-------|-------|------------|--------------|----------|
| §0 基本元信息 | 标题/scope/代码引用 | ✓ | ✓(pending 标注) | ✓ | ✓ | ✓ |
| §1 参数边界表 | 完整/类型/range/default | ✓ | ✓ | ✓ | ✓ | ✓ |
| §2 合法性约束 | 表达式/错误类型/位置/反例 | ✓ | ✓(pending) | ✓(pending) | ✓(pending) | ✓(pending) |
| §3 MS-EB 映射 | 五分量显式映射 | ✓(含 virtual-EB 简化说明) | ✓(草稿) | 待补 | 待补 | 待补 |
| §4 签名规范 | 签名 + docstring + scope_tag | ✓ | ✓(目标) | ✓(目标) | ✓(目标) | 待补 |
| §5 数值锚点 | 回归测试 + 阈值 | ✓(8.33e-08) | ✗ | ✗ | ✗ | ✗ |
| §6 Bearing | 文献 + 模块 + Sub-Q3 | ✓ | ✓ | ✓ | ✓ | ✓ |

**通过门槛**:Ideal 项全部 ✓(含 `partial` scope 说明);其他变体的 "✗" 是 Phase 1 S2.1-S2.2 预期产出。

---

## 9. 升级路径

### 9.1 近期(Phase 1 S2.1 Week 1-3)

1. 实施 `MSEBProtocol.executed_state` 的 multi-source 版本
2. 升级 `_mdi_sift_keep` 为 3-tuple 形式
3. 将 `build_mdi_protocol` 的 `scope_tag` 从 `partial` → `covered`
4. 同步 [framework_coverage.md](../framework_coverage.md) §3.1 F5 + §6.1 计数 + [PHASE0_REPORT.md](../PHASE0_REPORT.md) §2 + §4.1

### 9.2 中期(Phase 1 S2.1 Week 2-3 + S2.2 Week 4-8)

5. 实施 `build_decoy_mdi_protocol`(TDD:先写 Ma-Razavi Fig.3 回归)
6. 实施 `build_asymmetric_mdi_protocol`(Pareto 需要)
7. 启动 S2.2 MDI Pareto 扫描

### 9.3 远期(Phase 2)

8. MDI 作为 Sub-Q3 上界 testbed:对比 PLOB / Pirandola 2019 end-to-end capacity

---

## 10. 变更日志

- **v0.1** (2026-04-19):初稿。Ideal symmetric 对齐 Phase 0 M2 已实施代码(含 `partial` scope 说明);decoy/asymmetric/encoding 作为 Phase 1 S2.1 占位。
