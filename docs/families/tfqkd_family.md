# TF-QKD Family Sheet

**Family tag**: `F6` (per [framework_coverage.md §3.1](../framework_coverage.md))
**Version**: v0.1
**Last updated**: 2026-04-19
**Checklist pass**: see §8 self-check
**Scope status**: `partial` — phase reference 的 MS-EB 表达是 workaround(见 [framework_coverage.md §3.1 F6](../framework_coverage.md)),M4B(Phase 0.5 可选)完成后重新定级;**本 sheet 为 Phase 1 S2.1 起稿,spec_only 层面先落**

---

## 0. Scope

### 0.1 包含的变体(In-scope)

| 变体 | 代码 | 状态 |
|------|------|------|
| **TF-QKD**(Lucamarini 2018 原版,phase-encoding) | 未实施 | `spec_only` — 本 sheet 起稿 |
| **SNS-TF-QKD**(Wang-Yu-Hu 2018 "sending-or-not-sending") | 未实施 | `spec_only` |
| **PM-QKD**(Ma-Zeng-Zhou 2018 "phase-matching") | 未实施 | `spec_only` |
| **MP-QKD**(Zeng-Zhou-Wu-Ma 2022 mode-pairing) | 未实施 | **`out_of_scope`**(v0.3 订正,跨轮联合声明违反 MS-EB 单一 $\mathcal{E}$;[framework_coverage.md §3.1 F7](../framework_coverage.md))— **本 sheet 列为对比参考** |
| **Decoy TF / SNS / PM 变体** | 未实施 | `spec_only` — 与主变体同构 |

### 0.2 不包含的变体(Out-of-scope)

- **CV-TF-QKD**:违反离散 $\mathcal{P}$
- **MP-QKD 的 multi-round pairing**:跨轮联合声明 → 违反 MS-EB H2 假设(单轮 $\mathcal{E}$);**需要 ADR**(v0.3 订正)才能重新定级
- **Twin-field DI-QKD**:违反"Eve 全权控 $\mathcal{E}$ + 固定测量"

### 0.3 共同 MS-EB 结构

TF 族的核心困难是 **phase reference 的表达**:
- 经典 phase reference(如本地振荡器)在 MS-EB 下表达为 $\mathcal{E}$ 的相位调制项(workaround)— 这是 F6 `partial` 的 scope_reason
- 两方 + 单中间 Charlie 与 MDI **拓扑相同**,但 TF 依赖光场 phase 相干 ⇒ Charlie 的 $\mathcal{E}$ 复杂度高于 MDI

**共同骨架**:
- **$\mathcal{P}$**:两 SourceParty(Alice + Bob),但 `source_state` 需编码 phase(非简单 MUB)
- **$\mathcal{E}$**:Charlie 的单光子干涉测量 + 相位声明;带 phase reference 时含本振注入
- **$\mathcal{A}$**:基匹配 + Charlie 干涉结果 + phase 后筛
- **$\mathcal{T}$**:至少 2 组 gain/QBER 观测量,各 μ 下
- **$\mathcal{K}$**:Alice/Bob 各持 key(取决于具体变体)

### 0.4 关键理论差异(触发 partial 的根源)

| 变体 | phase reference 形式 | MS-EB 下的表达 | 困难 |
|------|---------------------|----------------|------|
| **TF**(Lucamarini) | 本振光场 | $\mathcal{E}$ 含 phase 调制 Kraus | phase 抖动对 $\mathcal{E}$ 的破坏需额外 post-selection |
| **SNS** | "发或不发"决策 | $\mathcal{P}$ 含空真空态 superposition | source_state 引入 coherent state(需 Fock 截断) |
| **PM** | 相位匹配后筛 | $\mathcal{A}$ 在 Charlie 声明后做 phase-matching post-selection | 筛选条件跨 round(如果按 round 对齐则 OK) |
| **MP** | 多轮 mode-pairing | **违反 MS-EB 单一 $\mathcal{E}$ 假设** | **`out_of_scope`** |

---

## 1. 参数边界表

### 1.1 TF-QKD(主变体,拟实施)

| name | type | range | default | physical meaning |
|------|------|-------|---------|------------------|
| `mu` | `float` | `(0.0, 1.0]` | `0.1` | coherent state 平均光子数(TF 典型 μ ~ 0.1) |
| `eta_ch` | `float` | `(0.0, 1.0]` | — | 单臂信道透射率(√η_total) |
| `phase_noise_sigma` | `float` | `[0.0, π]` | `0.1` | phase reference 抖动方差(rad) |
| `p_dark` | `float` | `[0.0, 1.0)` | `1e-6` | 探测器暗计数 |
| `efficiency_d` | `float` | `(0.0, 1.0]` | `0.5` | 探测器效率 η_d |

### 1.2 SNS-TF-QKD(拟实施)

额外参数(在 TF 基础上):

| name | type | range | default | physical meaning |
|------|------|-------|---------|------------------|
| `p_send` | `float` | `(0.0, 1.0)` | `0.25` | "发送 signal"概率 |
| `mu_signal` | `float` | `(0.0, 1.0]` | `0.4` | signal 强度 |
| `mu_decoy` | `float` | `(0.0, mu_signal)` | `0.1` | decoy 强度 |

### 1.3 PM-QKD(拟实施)

| name | type | range | default | physical meaning |
|------|------|-------|---------|------------------|
| `D_phase` | `int` | `{4, 8, 16}` | `16` | phase 离散化分片数 |
| `mu` | `float` | `(0.0, 1.0]` | `0.3` | coherent state 强度 |

### 1.4 MP-QKD(**out_of_scope** — 仅文档)

无参数表,作为对比参考:违反 MS-EB 单一 $\mathcal{E}$ 假设。

---

## 2. 合法性约束

| 约束表达式 | 适用变体 | 错误类型 | 位置 | 反例 |
|---|---|---|---|---|
| `0 < mu <= 1` | TF/PM | `ValueError` | `build_tfqkd_protocol`(pending) | `mu=0.0`, `mu=1.1` |
| `0 < eta_ch <= 1` | all TF | `ValueError` | 同上 | `eta_ch=0.0`, `eta_ch=1.5` |
| `0 <= phase_noise_sigma <= π` | TF | `ValueError` | 同上 | `phase_noise_sigma=-0.1`, `phase_noise_sigma=4.0` |
| `0 < p_send < 1` | SNS | `ValueError` | `build_sns_tfqkd_protocol`(pending) | `p_send=0.0`, `p_send=1.0` |
| `0 < mu_decoy < mu_signal` | SNS | `ValueError` | 同上 | `mu_decoy=0.5, mu_signal=0.4` |
| `D_phase in {4, 8, 16}` | PM | `ValueError` | `build_pm_qkd_protocol`(pending) | `D_phase=3`, `D_phase=32` |

---

## 3. 参数 → MS-EB 映射

### 3.1 TF-QKD(草稿,Phase 0.5 M4B 落地路径)

- **$\mathcal{P}$**:两个 `SourceParty`,`source_state` 为 coherent state 在 Fock 截断(截断阶 `N_fock = 10`)后的混合态;每个 source 含 `key_register_dim = 2`(bit choice),`signal_register_dim = N_fock`
- **$\mathcal{E}$**:Charlie 的单光子干涉测量 $\mathcal{E}_{\text{int}}$:$A'\otimes B' \to \{D_0, D_1, \text{fail}\}$(两个探测器 + 失败)+ phase reference 相位调制 Kraus $U_\phi = e^{i\phi n}$,以 $\mathcal{N}(0, \sigma^2)$ 分布平均
- **$\mathcal{A}$**:sift_keep = Charlie 声明 ∈ {D_0, D_1} 且 Alice-Bob phase 差匹配(post-selection)
- **$\mathcal{T}$**:gain $Q_\mu$ + QBER $E_\mu$;观测量 $\Gamma$ 投影到 "D_0 vs D_1" 的错误子空间
- **$\mathcal{K}$**:Alice 持 key,Bob flip bit 若 Charlie 声明 D_1

**log-log 斜率验收**:TF 理论预期 $R \propto \sqrt{\eta}$(PLOB 标度 √η),对应 log-log 斜率 = 0.5;Refactoring Plan §5 M4B 硬验收 `斜率 = 0.5 ± 0.05`

### 3.2 SNS-TF-QKD

- **$\mathcal{P}$**:`source_state` = $p_{\text{send}} |\mu_s\rangle\langle\mu_s| + (1-p_{\text{send}}) |0\rangle\langle 0|$(发或不发 coherent state 混合)
- 其余同 TF

### 3.3 PM-QKD

- **$\mathcal{P}$**:`key_register_dim = D_phase`(D 个离散相位);`source_state` 为 $\sum_k |k\rangle\langle k| \otimes |\alpha e^{i\phi_k}\rangle\langle\alpha e^{i\phi_k}|$
- **$\mathcal{A}$**:phase matching post-selection(Alice-Bob phase difference mod D)

---

## 4. `build_*_protocol(...)` 目标签名

```python
def build_tfqkd_protocol(
    mu: float = 0.1,
    eta_ch: float = 0.5,
    phase_noise_sigma: float = 0.1,
    p_dark: float = 1e-6,
    efficiency_d: float = 0.5,
    N_fock: int = 10,
) -> MSEBProtocol:
    """TF-QKD (Lucamarini 2018) MS-EB protocol.

    Returns:
        MSEBProtocol with scope_tag='partial' (phase reference via
        channel phase modulation is a workaround; M4B re-evaluate).

    References:
        Lucamarini et al. 2018, Nature 557:400.
    """

def build_sns_tfqkd_protocol(
    p_send: float = 0.25,
    mu_signal: float = 0.4,
    mu_decoy: float = 0.1,
    eta_ch: float = 0.5,
    **kwargs,
) -> MSEBProtocol: ...

def build_pm_qkd_protocol(
    mu: float = 0.3, D_phase: int = 16, eta_ch: float = 0.5, **kwargs,
) -> MSEBProtocol: ...
```

**注**:上述签名在 Phase 0.5 M4B 实施时可能调整;**本 sheet 作为 spec_only 起稿,签名稳定性不做硬承诺**。

---

## 5. 数值验证锚点

### 5.1 已有

无(F6 Phase 0 未实施)

### 5.2 待补(Phase 0.5 M4B — 可选 / Phase 1 S2.2)

| 变体 | 对照 | 阈值 | Phase | 状态 |
|------|------|------|-------|------|
| TF | Lucamarini 2018 Fig.3 | log-log 斜率 `0.5 ± 0.05` | M4B 硬验收 | 待实施 |
| SNS | Wang-Yu-Hu 2018 Fig.3 | 密钥率误差 `rel=0.05` | S2.2 | 待实施 |
| **PM** | **Ma-Zeng-Zhou 2018 Fig.3a / Eq.4** | **log-log 斜率 `0.5 ± 0.05`** | **F6 §7.3 (2026-04-20)** | **✓ commit `pending`** |

**F6 §7.3 第一遍实施**(`qkdx/analytic/pm_qkd.py`, 2026-04-20):
- Ma Eq. 4 + Eq. 2 decoy phase-error UB(honest-behaviour first-pass)
- 实测 log-log 斜率 **0.52**(target 0.5 ± 0.05 ✓)
- 绝对密钥率比 Ma Fig.3a 低 1-2 个数量级(per-distance μ 未优化 + phase-error UB 未接入完整 decoy 反演,§7.5+ 补)
- 20 tests 全过;tfqkd_family §5.2 PM 硬验收**斜率形状通过**,绝对值匹配归 §7.5

---

## 6. Bearing 与参考资料

### 6.1 主文献

- **TF**:Lucamarini et al. 2018, Nature 557:400 — 原 TF-QKD
- **SNS**:Wang-Yu-Hu 2018, PRA 98:062323
- **PM**:Ma-Zeng-Zhou 2018, PRX 8:031043
- **MP**(out_of_scope):Zeng-Zhou-Wu-Ma 2022, Nat.Commun. 13:4470
- [docs/literature/TF-QKD.md](../literature/TF-QKD.md)(待建立)

### 6.2 Phase 0 工具依赖

- 暂无直接依赖(F6 未实施);未来将依赖 `qkdx/numerics/wlc.py` + Fock 截断工具
- **新建预期模块**:`qkdx/protocols/tfqkd.py`(Phase 0.5 M4B)

### 6.3 Sub-Q3 上界预期 bearing

- **TF 家族最重要**:$\sqrt{\eta}$ 标度的物理来源是"两方 + 单 untrusted relay + 光场 phase 相干"拓扑
- **Sub-Q3 主目标**:Pirandola 2019 end-to-end capacity 在该拓扑给出 $R_{\text{UB}}(\eta)$,TF 下界(WLC) vs 该上界的 gap 就是 Sub-Q4 核心刻画对象
- **主问题 relevance**:TF 族在 [docs/PROSPECTUS.md](../PROSPECTUS.md) 攻坚问题中占最大权重(主问题 Sub-Q3 + Sub-Q4 均以 TF 为典型 testbed)

---

## 7. Pareto 搜索预留(Phase 1 S2.2)

- **Pareto 轴**:TF $(\mu, \text{phase\_noise}, \text{distance}) \to R_{\text{key}}$
- **TF vs BB84 vs MDI 对比**:同 η_total 下 TF $\propto \sqrt{\eta}$ 应显著优于 MDI/BB84 $\propto \eta$(Phase 1 S2.2 overview 图的核心卖点)

---

## 8. Self-check(按 `_checklist.md`)

| 章节 | 项 | TF | SNS | PM | MP(out) |
|------|------|----|-----|-----|--------|
| §0 基本元信息 | 标题/scope/代码引用 | ✓ | ✓ | ✓ | ✓(out 标注) |
| §1 参数边界表 | 完整/类型/range/default | ✓(目标) | ✓(目标) | ✓(目标) | N/A |
| §2 合法性约束 | 表达式/错误类型/位置/反例 | ✓(目标) | ✓(目标) | ✓(目标) | N/A |
| §3 MS-EB 映射 | 五分量显式映射 | ✓(草稿) | ✓(草稿) | ✓(草稿) | N/A |
| §4 签名规范 | 签名 + docstring + scope_tag | ✓(目标) | ✓(目标) | ✓(目标) | N/A |
| §5 数值锚点 | 回归测试 + 阈值 | ✗ (M4B 承接) | ✗ (S2.2) | ✗ (S2.2) | N/A |
| §6 Bearing | 文献 + 模块 + Sub-Q3 | ✓(最重要) | ✓ | ✓ | ✓ |

**通过门槛**:本 sheet v0.1 **定位为 spec_only 起稿**;全部实施 "✗" 是 M4B/S2.2 预期产出。v0.2 在 M4B 完成 TF 实施后升级。

---

## 9. 升级路径

### 9.1 近期(Phase 0.5 M4B — 可选 2-3 周)

1. `docs/literature/TF-QKD.md` Level 3 精读(Lucamarini 2018 + SNS + PM + MP)
2. `docs/msen/tfqkd-formulation.md` MS-EB 书写
3. `qkdx/protocols/tfqkd.py` 实施(至少 TF 主变体 + SNS)
4. log-log 斜率 0.5 硬验收

### 9.2 中期(Phase 1 S2.1-S2.2)

5. SNS / PM 完整实施
6. Pareto 搜索(TF vs MDI vs BB84 overview)

### 9.3 远期(Phase 2 Sub-Q3 / Sub-Q4)

7. TF vs Pirandola 2019 上界 gap 刻画
8. 是否 TF 已实现 $\sqrt{\eta}$ 标度下的"最紧" / 还是存在可改进空间

### 9.4 降级预案

**Refactoring Plan §8 R3**:若 TF-QKD 的 phase reference 在 MS-EB 下不自然,M4B 降级为"decoy finite-key 扩展",本 sheet 同步 `out_of_scope` + scope_reason 指向 phase-reference limitation

---

## 10. 变更日志

- **v0.1** (2026-04-19):初稿 / spec_only。本 sheet 的 TF/SNS/PM 变体均未实施,作为 Phase 0.5 M4B + Phase 1 S2.1-S2.2 的 spec 起稿;MP 明确 `out_of_scope`
