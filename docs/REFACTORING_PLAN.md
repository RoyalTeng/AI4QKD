# AI4QKD 项目重构方案(函数级详细版)

**文档状态**:v3.1.4(codex 六轮评审字面统一 + PROSPECTUS v3.1 对齐,2026-04-18)
**基准日期**:2026-04-18
**作者**:基于 2026-04-17 与 2026-04-18 代码审查 + 2026-04-18 codex 六轮评审
**目标读者**:项目负责人、实现者、codex 评审

> **与 [PROSPECTUS.md](PROSPECTUS.md) 的关系**:
> [PROSPECTUS.md](PROSPECTUS.md)(v3.1)是**研究地图**(WHY — 主问题"无中继无存储 DV-QKD 的信息论极限"、Sub-Q1→Sub-Q4 子问题序列、Gap 刻画方法);
> 本文档是**函数级实施规范**(HOW — 每个模块的 API、测试、里程碑硬验收、运营控制)。
> 两者的映射:Sub-Q1(MS-EB 框架 + 评估工具链)对应本文档 §5 的 M1-M3 + M4A/M4B,其中 M4B 可延至 Phase 0.5;Sub-Q2 的 family sheet 跨 Phase 0-1;Sub-Q3 / Sub-Q4 的上界 SDP + gap 刻画在 Phase 2–3 建设,超出 Phase 0 范围。
> 当工期/里程碑结构数字不一致时,**以本文档 §5 为准**(经 codex 六轮审计)。

> **v2 → v3 变更摘要**:根据 codex 一轮评审(`/tmp/codex_review_final.md`,702 行,9 节 18 条 Verdict),
> 修订了:§2 代码规模约束、§3 目录(移除 `gradient.py`)、§4.1/§4.4/§4.6 API 一致性(新增
> `GMap`、`conditional_alice_bob_dim()`、`observable()`)、§4.6 SDP 数值稳定性、§5 里程碑时程与阈值、
> §6 测试 fixture 与 skip guard、§7.1 迁移脚本、新增 §11 运营控制。
>
> **v3 → v3.1 变更摘要**(codex 二轮评审 `/tmp/codex_review_v3.log`,1787 行,2 🔴 Blocker + 3 ⚠️):
> - 🔴 §4.6 / 附录 B:正则化改为 `X_reg = (1-ε)X_raw + ε·tr(X_raw)·τ`(CPTNI 下 `tr(X_raw)≠1`);
>   单位口径明确为 **bit/signal**,引入 `observations["p_sift"]` 显式参数;`facial.reduce_problem`
>   的 `lift()` 被正确调用;`_construct_Z_pinching(dim_key, dim_side)` 双参数澄清张量维度契约。
> - 🔴 §7.1:脚本循环改为 `for item in *;`(`dotglob` 已覆盖 dotfile),避免双重遍历;
>   加入 `[[ -n "${BASH_VERSION:-}" ]] || exit 1` 防 zsh 误跑。
> - ⚠️ §5/§9/§4.6:阈值分主线(`rel=0.01, abs=5e-4`)与 fallback 特例(`rel=0.02, abs=1e-3`);
>   §5 工期拆成 Phase 0 必需 12 周 + M4B 可选,与 12–16 周总预算自洽。
> - ⚠️ §11.1/§11.2:`PYTHONHASHSEED` 改为启动前环境变量 + 运行时 sanity check;依赖锁定加 `uv.lock`。
>
> 各章末尾保留 "codex‑N‑M: resolved" 勾选,v3.1 追加勾选以 `(v3.1)` 标注。

---

## 0. TL;DR

**当前代码库无法通过增量修复挽救,必须整体重写。** 本方案给出函数级实现规范,使实现者无需再做架构决策,只需按签名编码 + 按测试用例验证。

- §1–§2:重构动因与项目定位(简)
- §3:仓库骨架(目录结构)
- §4:**每个模块的完整 API 规范**(类、函数、签名、docstring、不变量)— 本次新增的核心
- §5:Milestone 验收标准(与 §4 的模块一一对应)
- §6:测试用例目录(函数级对齐)
- §7–§10:旧代码处置、风险、规范、决策

**基本原则**:先把密钥率评估层做对,再谈其他一切。Phase 0 不做 AI、不做形式化验证、不做通用 DSL。

---

## 1. 为什么必须重构(摘要)

见前版 §1,此处不复述。关键数据:

| # | 缺陷 | 证据位置 |
|---|------|---------|
| 1 | 仿真器完全不读协议图 | `legacy-v1/simulator/quantum_simulator.py:29-67` |
| 2 | AI 适应度函数恒等于常数 | `legacy-v1/ai_agent/enhanced_agent.py:108` |
| 3 | `formal_verification/`、`security_evaluator/` 是空目录 | `ls` |
| 4 | "78.6% 密钥率提升"代码里找不到来源 | `grep -rn "78.6"` |
| 5 | torch/qiskit/z3 声称使用但零 import | `grep -rn "^import torch"` |

**增量修复走不通**,因为密钥率评估层需要重建(WLC SDP 框架),这要求从密度算子代数开始搭建,现仓库一行都没有。既然要重建底层,就在新仓库重建,避免被旧 API 污染。

---

## 2. 新仓库定位

**研究问题**:在由 MS-EB 五元组 `Π = (P, E, A, T, K)` 定义的数学严格协议空间内,用凸优化数值方法计算密钥率紧下界,作为后续 AI 搜索(Phase 1+)的可信评估器。

**Phase 0 做**:BB84 / 六态 / MDI / TF-QKD 解析基线 + WLC SDP 数值密钥率 + 数值诱骗态 + 对称性约化。

**Phase 0 不做**:任何 AI、任何形式化验证、finite-key 精确分析、CV-QKD、硬件集成。

**代码复杂度约束**(v3 修订,移除 LOC 硬上限):
- API 边界:公共导出符号总数 ≤ 80(由 `qkdx/__init__.py` 的 `__all__` 闸门)
- 测试/源码行数比:`tests/` 行数 ≥ `qkdx/` 行数 × 0.75
- 基准可复现:`pytest --cov=qkdx` ≥ 85%,且 `notebooks/reproduce_wlc_2018_fig3.ipynb` 在 clean venv 中 `papermill` 一键执行通过

> v2 曾设 "`qkdx/` ≤ 3000 行、`tests/` ≤ 2500 行" 硬上限,codex 评审指出该上限与 WLC + MDI + decoy + symmetry 的
> 严谨性目标冲突(§8.2),故移除 — 改由 API 边界 + 覆盖率 + 基准可复现三者约束复杂度。

**禁用依赖**:torch、stable-baselines3、qiskit、z3、coq 相关。

> **codex §8 结论**:
> - §8‑1 resolved:工期重排至 **Phase 0 = 12–16 周**(见 §5)
> - §8‑2 resolved:LOC 上限移除(本节)
> - §8‑3 resolved:`numerics/gradient.py` 从 Phase 0 目录树删除(见 §3)
> - §8‑4 resolved:M4 拆分 M4A(symmetry, BB84/6-state)与 M4B(TF-QKD)(见 §5)

---

## 3. 仓库骨架

```
qkdx/                               # 项目根
├── pyproject.toml
├── requirements.txt
├── README.md
├── .gitignore
│
├── qkdx/                           # Python 包
│   ├── __init__.py                 # 版本号 + 顶层 re-export
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── hilbert.py              # 密度算子代数
│   │   ├── operators.py            # Kraus、POVM、CPTNI
│   │   └── entropy.py              # 熵测度
│   │
│   ├── symmetry/
│   │   ├── __init__.py
│   │   ├── groups.py               # 群的有限表示
│   │   └── twirling.py             # 群平均
│   │
│   ├── protocol/
│   │   ├── __init__.py
│   │   ├── base.py                 # MSEBProtocol(dataclass)
│   │   ├── source.py               # SourceParty、PM→EB
│   │   ├── channel.py              # PublicQuantumNetwork
│   │   ├── announcement.py         # AnnouncementRule
│   │   └── key_map.py              # KeyMap
│   │
│   ├── protocols/
│   │   ├── __init__.py
│   │   ├── bb84.py
│   │   ├── sixstate.py
│   │   ├── mdi.py
│   │   └── tfqkd.py
│   │
│   ├── numerics/
│   │   ├── __init__.py
│   │   ├── wlc.py                  # 核心:WLC 2018 SDP
│   │   ├── facial.py               # facial reduction
│   │   └── decoy.py                # 数值诱骗态
│   │   # Note: gradient.py (Frank-Wolfe) deferred to Phase 1 unless a failing
│   │   #       Phase-0 benchmark + ADR requires it (codex §8-3).
│   │
│   ├── analytic/
│   │   ├── __init__.py
│   │   ├── shor_preskill.py        # 1 - 2h(e)
│   │   ├── six_state.py            # 1 - h(e) - e·log2(3)
│   │   └── gllp.py                 # 弱相干光源
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logging.py
│       └── validation.py
│
├── tests/                          # 与 qkdx/ 目录一一对齐
├── notebooks/                      # 研究 notebook(不进 CI)
├── docs/                           # 设计文档
└── archive/legacy-v1/              # 旧代码归档
```

---

## 4. 模块 API 规范(函数级)

下面每个模块给出:**公共类/函数签名 + 类型 + 行为说明 + 不变量 + 失败模式**。实现者按此 copy-paste 即可,不需要再做设计决策。

约定:
- 所有函数签名使用 PEP 604 联合类型语法(`X | Y`)
- 矩阵类型别名:`Matrix = np.ndarray`(复数矩阵,dtype=complex128),形状在 docstring 注明
- SDP 变量用 `cvxpy.Variable` 或 `cvxpy.Expression`,类型标注为 `cp.Expression`
- 所有公共函数必须带类型标注,mypy strict 通过

---

### 4.1 `qkdx/core/hilbert.py`

**职责**:密度算子代数的最小完整集。不包含任何 QKD 特定逻辑。

```python
from __future__ import annotations
import numpy as np
from numpy.typing import NDArray

Matrix = NDArray[np.complex128]           # 形状约束由 docstring 指定(v3:直接使用 np.complex128 以强化静态检查)


def ket(basis_index: int, dim: int) -> Matrix:
    """返回计算基 |i⟩,形状 (dim, 1)。

    参数:
        basis_index: 0 ≤ i < dim
        dim: 希尔伯特空间维度

    返回:
        列向量 e_i

    异常:
        ValueError: basis_index 越界
    """


def bra(basis_index: int, dim: int) -> Matrix:
    """返回计算基 ⟨i|,形状 (1, dim)。ket 的 Hermitian conjugate。"""


def proj(state: Matrix) -> Matrix:
    """投影算子 |ψ⟩⟨ψ|。

    输入:
        state: 形状 (d, 1) 的列向量,不要求归一化

    返回:
        形状 (d, d) 的 Hermitian、半正定、迹 = ‖state‖² 的矩阵

    不变量:
        output == output.conj().T(数值容差 1e-12)
    """


def tensor(*ops: Matrix) -> Matrix:
    """Kronecker 张量积,左到右。

    示例:
        tensor(sigma_x, sigma_z) 等价于 np.kron(sigma_x, sigma_z)
    """


def partial_trace(rho: Matrix, dims: tuple[int, ...], subsystems: tuple[int, ...]) -> Matrix:
    """部分迹,保留非 subsystems 中的子系统。

    参数:
        rho: 形状 (D, D),D = prod(dims)
        dims: 每个子系统的维度
        subsystems: 要 trace out 的子系统索引(从 0 开始)

    返回:
        形状 (d, d),d = prod(dims[i] for i not in subsystems)

    示例:
        # 双 qubit 系统 trace out 第二个
        rho_A = partial_trace(rho_AB, dims=(2, 2), subsystems=(1,))

    不变量:
        trace(partial_trace(rho, dims, subsystems)) == trace(rho)
    """


def partial_transpose(rho: Matrix, dims: tuple[int, ...], subsystems: tuple[int, ...]) -> Matrix:
    """部分转置,对 subsystems 中的子系统。PPT 判据用。"""


def is_hermitian(M: Matrix, atol: float = 1e-10) -> bool:
    """判断 M == M†。"""


def is_psd(M: Matrix, atol: float = 1e-10) -> bool:
    """判断 M 半正定。

    实现:
        eigvals = np.linalg.eigvalsh(M)
        return eigvals.min() >= -atol
    """


def is_density(rho: Matrix, atol: float = 1e-10) -> bool:
    """密度矩阵三性质:Hermitian + PSD + trace=1。"""


def purify(rho: Matrix) -> Matrix:
    """Schmidt 纯化:返回 |ψ⟩ ∈ H_A ⊗ H_R,使 tr_R(|ψ⟩⟨ψ|) = rho。

    形状:rho shape (d,d) → 返回 (d², 1)
    """


def fidelity(rho: Matrix, sigma: Matrix) -> float:
    """Uhlmann 保真度 F(ρ,σ) = tr(sqrt(sqrt(ρ)·σ·sqrt(ρ)))²,返回 ∈ [0,1]。"""
```

**模块常量**:
```python
# 标准 qubit 算子(注意: SIGMA_Y 对 MDI-QKD 贝尔态测量必需)
IDENTITY_2: Matrix = np.eye(2, dtype=np.complex128)
SIGMA_X: Matrix = np.array([[0, 1], [1, 0]], dtype=np.complex128)
SIGMA_Y: Matrix = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
SIGMA_Z: Matrix = np.array([[1, 0], [0, -1]], dtype=np.complex128)
HADAMARD: Matrix = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=np.complex128)

# Z 基
KET_0: Matrix = ket(0, 2)
KET_1: Matrix = ket(1, 2)
# X 基
KET_PLUS: Matrix = (KET_0 + KET_1) / np.sqrt(2)
KET_MINUS: Matrix = (KET_0 - KET_1) / np.sqrt(2)
# Bell 态
PHI_PLUS: Matrix = (tensor(KET_0, KET_0) + tensor(KET_1, KET_1)) / np.sqrt(2)
```

**不可变 ndarray 辅助**(v3 新增,用于 `frozen=True` dataclass 内保护数组字段):
```python
def _freeze_array(a: np.ndarray) -> Matrix:
    """深拷贝 + write=False,使数组内容在 frozen dataclass 内真正只读。

    不变量:
        _freeze_array(a).flags.writeable is False
        修改结果数组会抛 ValueError
    """
    b = np.array(a, copy=True, dtype=np.complex128)
    b.setflags(write=False)
    return b
```

**测试覆盖**(`tests/test_core/test_hilbert.py`):
- `test_partial_trace_preserves_trace`:随机 8×8 密度矩阵 partial_trace 后迹不变
- `test_partial_trace_bell_state_is_maximally_mixed`:tr_B(|Φ+⟩⟨Φ+|) == I/2
- `test_proj_is_hermitian_psd_rank1`:随机列向量的 proj 满足 rank=1、Hermitian、PSD
- `test_purify_then_trace_roundtrip`:purify(rho) 后 partial_trace 回来 == rho(误差 < 1e-10)
- `test_sigma_operators_anticommute`:σ_x σ_z + σ_z σ_x == 0(2x2 零矩阵)
- `test_freeze_array_blocks_writes`:`_freeze_array(np.eye(2))[0,0] = 0` 抛 ValueError

> **codex §6 结论**:
> - §6‑2 resolved:`Matrix = NDArray[np.complex128]`(移除运行时别名 `Complex`)
> - §6‑3 resolved:`_freeze_array` 辅助函数

---

### 4.2 `qkdx/core/operators.py`

**职责**:量子映射(Kraus、POVM、CPTNI)的数学抽象。

```python
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
import numpy as np
from qkdx.core.hilbert import Matrix, is_psd


@dataclass(frozen=True)
class KrausMap:
    """CPTP 或 CPTNI 映射的 Kraus 表示。

    属性:
        kraus: list of Kraus 算子 K_i,每个形状 (d_out, d_in)
        dim_in: 输入希尔伯特空间维度
        dim_out: 输出希尔伯特空间维度

    不变量(构造时校验):
        sum_i K_i† K_i ≤ I(CPTNI)
        若 strict_cptp=True 构造,则 sum_i K_i† K_i == I

    数学:
        E(ρ) = Σ_i K_i · ρ · K_i†
    """
    kraus: tuple[Matrix, ...]
    dim_in: int
    dim_out: int

    def __post_init__(self) -> None:
        """校验 CPTNI 条件;若违反抛 ValueError。"""

    def apply(self, rho: Matrix) -> Matrix:
        """施加映射到密度矩阵 ρ,返回 E(ρ)。"""

    def choi(self) -> Matrix:
        """Choi-Jamiolkowski 矩阵,形状 (dim_in·dim_out, dim_in·dim_out)。

        定义:J(E) = Σ_ij |i⟩⟨j| ⊗ E(|i⟩⟨j|)
        """

    def is_cptp(self, atol: float = 1e-10) -> bool:
        """判断是否严格 trace-preserving(而非 non-increasing)。"""

    @classmethod
    def from_unitary(cls, U: Matrix) -> "KrausMap":
        """酉演化的单 Kraus 表示:K_0 = U。"""

    @classmethod
    def identity(cls, dim: int) -> "KrausMap":
        """恒等映射。"""

    @classmethod
    def depolarizing(cls, dim: int, p: float) -> "KrausMap":
        """去极化信道 E(ρ) = (1-p)ρ + p·I/d。

        Kraus:K_0 = sqrt(1-3p/4)·I,K_{1,2,3} = sqrt(p/4)·σ_{x,y,z}(dim=2)
        """

    @classmethod
    def dephasing(cls, p: float) -> "KrausMap":
        """单 qubit 相位退相干,错误概率 p。Kraus:√(1-p)·I, √p·σ_z。"""

    def compose(self, other: "KrausMap") -> "KrausMap":
        """串联两个映射:self ∘ other。shape check。"""

    def tensor(self, other: "KrausMap") -> "KrausMap":
        """并联(张量积)两个映射。"""


@dataclass(frozen=True)
class POVM:
    """Positive Operator-Valued Measure。

    属性:
        elements: tuple of POVM elements {Π_i},每个 Hermitian PSD
        dim: 被测量系统的维度

    不变量:
        sum_i Π_i == I(dim × dim)
        每个 Π_i 半正定

    数学:
        P(outcome = i | state = ρ) = tr(Π_i · ρ)
    """
    elements: tuple[Matrix, ...]
    dim: int

    def __post_init__(self) -> None:
        """校验完备性和半正定性。"""

    def probability(self, rho: Matrix, outcome: int) -> float:
        """tr(Π_outcome · ρ)。应返回实数,虚部应 < 1e-10。"""

    def probabilities(self, rho: Matrix) -> np.ndarray:
        """所有 outcome 的概率分布,形状 (len(elements),)。"""

    @classmethod
    def computational_basis(cls, dim: int) -> "POVM":
        """计算基投影测量 {|i⟩⟨i|}。"""

    @classmethod
    def bb84_z_basis(cls) -> "POVM":
        """BB84 的 Z 基测量(qubit)。"""

    @classmethod
    def bb84_x_basis(cls) -> "POVM":
        """BB84 的 X 基测量(qubit)。"""

    @classmethod
    def bell_state_measurement(cls) -> "POVM":
        """完整贝尔态测量,4 个 outcome,dim=4。MDI-QKD 用。"""


def channel_from_choi(J: Matrix, dim_in: int, dim_out: int) -> KrausMap:
    """从 Choi 矩阵还原 Kraus 表示(通过对 J 的 SVD)。

    验证:channel_from_choi(K.choi(), d_in, d_out) 在 Choi 表示上等价于 K。
    """


def dual_map(K: KrausMap) -> KrausMap:
    """Heisenberg picture 对偶映射 E†,满足 tr(A·E(ρ)) = tr(E†(A)·ρ)。

    Kraus 形式:E†(A) = Σ_i K_i† · A · K_i
    """
```

**测试覆盖**(`tests/test_core/test_operators.py`):
- `test_krausmap_depolarizing_preserves_trace`:随机密度矩阵被去极化后迹仍为 1
- `test_krausmap_depolarizing_maximally_mixed_at_p_one`:p=1 时 E(ρ)=I/d
- `test_krausmap_compose_matches_matrix_product`:酉 K1.compose(K2) 等价于 U1·U2
- `test_povm_completeness`:所有预定义 POVM 的元素和 == I
- `test_povm_bb84_z_on_ket_plus_gives_half_half`:Π=|0⟩⟨0|,ρ=|+⟩⟨+|,p=0.5
- `test_povm_bell_measurement_on_phi_plus`:BSM 作用于 |Φ+⟩,第 0 个 outcome 概率 == 1

---

### 4.3 `qkdx/core/entropy.py`

**职责**:熵与相对熵的数值计算,WLC SDP 的目标函数来源。

```python
from __future__ import annotations
import numpy as np
from qkdx.core.hilbert import Matrix, is_density


def binary_entropy(p: float | np.ndarray) -> float | np.ndarray:
    """h(p) = -p·log2(p) - (1-p)·log2(1-p),对 p∈{0,1} 返回 0。

    向量化:接受 ndarray 返回 ndarray。
    """


def von_neumann(rho: Matrix, eps: float = 1e-12) -> float:
    """S(ρ) = -tr(ρ·log2 ρ)。

    实现:
        eigvals = np.linalg.eigvalsh(rho)
        eigvals = eigvals[eigvals > eps]
        return -np.sum(eigvals * np.log2(eigvals))

    不变量:
        0 ≤ S(ρ) ≤ log2(dim)
    """


def relative_entropy(rho: Matrix, sigma: Matrix, eps: float = 1e-12) -> float:
    """S(ρ ‖ σ) = tr(ρ·(log2 ρ - log2 σ))。

    若 supp(ρ) ⊄ supp(σ) 返回 np.inf。
    """


def conditional_entropy(rho_AB: Matrix, dim_A: int, dim_B: int) -> float:
    """S(A|B)_ρ = S(ρ_AB) - S(ρ_B)。可为负(纠缠时)。"""


def mutual_information(rho_AB: Matrix, dim_A: int, dim_B: int) -> float:
    """I(A:B)_ρ = S(A) + S(B) - S(AB)。非负。"""


def coherent_information(rho_AB: Matrix, dim_A: int, dim_B: int) -> float:
    """I_c(A⟩B)_ρ = S(B) - S(AB) = -S(A|B)。"""


def smooth_min_entropy_bound(H_vn: float, n: int, eps: float) -> float:
    """AEP 粗略估计,Phase 0 占位。Phase 1 替换为 Tomamichel 精确界。

    H_min^ε ≥ n·H_vn - O(sqrt(n·log(1/ε)))
    """
```

**测试覆盖**(`tests/test_core/test_entropy.py`):
- `test_binary_entropy_at_half_is_one`:h(0.5) == 1.0
- `test_binary_entropy_boundary`:h(0) == h(1) == 0
- `test_von_neumann_pure_state_is_zero`:任意纯态 ρ=|ψ⟩⟨ψ|,S(ρ)<1e-10
- `test_von_neumann_maximally_mixed_is_log_dim`:S(I/d) == log2(d)
- `test_relative_entropy_non_negativity`:随机 ρ,σ,S(ρ‖σ) ≥ 0
- `test_conditional_entropy_bell_is_minus_one`:S(A|B)_{|Φ+⟩⟨Φ+|} == -1

---

### 4.4 `qkdx/protocol/base.py`

**职责**:MS-EB(Multi-Source Entanglement-Based)协议的五元组数据结构。

```python
from __future__ import annotations
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
import numpy as np
import cvxpy as cp

from qkdx.core.hilbert import Matrix, _freeze_array
from qkdx.core.operators import KrausMap, POVM


@dataclass(frozen=True)
class SourceParty:
    """MS-EB 协议中的一个源方 P_i。

    属性:
        name: 如 "Alice", "Bob"
        key_register_dim: A_i 寄存器维度(经典随机性的量子化)
        signal_register_dim: A_i' 寄存器维度(要发出去的量子信号)
        eb_state: |ψ_i⟩ 的形状 (key_register_dim × signal_register_dim, 1)

    不变量:
        eb_state 归一化(‖·‖² == 1,误差 < 1e-10)
    """
    name: str
    key_register_dim: int
    signal_register_dim: int
    eb_state: Matrix

    def __post_init__(self) -> None:
        """维度与归一化校验。"""


@dataclass(frozen=True)
class PublicQuantumNetwork:
    """E:公共量子网络,CPTP 映射从 ⊗_i A_i' 到 B ⊗ ℂ[C]。

    属性:
        channel: KrausMap,输入维度 = prod(source signal dims),输出维度 = receiver_dim · classical_outcomes
        receiver_dim: Bob 接收端量子寄存器维度(可为 1 即"无量子信息转发")
        classical_outcomes: 公开声明空间 C 的大小

    不变量(仅在 PublicQuantumNetwork 自身可验证的部分):
        channel.dim_out == receiver_dim * classical_outcomes
    跨对象不变量(需要 sources)由 MSEBProtocol.__post_init__ 校验:
        channel.dim_in == prod(sources[i].signal_register_dim)

    数学:
        E: H_{A'_1} ⊗ ... ⊗ H_{A'_n} → H_B ⊗ ℂ[C]
    """
    channel: KrausMap
    receiver_dim: int
    classical_outcomes: int

    def __post_init__(self) -> None:
        """仅校验本对象可见的不变量。"""
        if self.channel.dim_out != self.receiver_dim * self.classical_outcomes:
            raise ValueError(
                f"channel.dim_out ({self.channel.dim_out}) != "
                f"receiver_dim * classical_outcomes ({self.receiver_dim * self.classical_outcomes})"
            )


@dataclass(frozen=True)
class AnnouncementRule:
    """A:公开声明函数。Phase 0 只支持 per-round announcement。

    属性:
        function: 输入 (raw_classical_info: tuple[int, ...]) → public_announcement: int
        sift_keep: 函数返回 True 表示该轮数据保留进入密钥生成,False 丢弃

    备注:
        Phase 0 不支持跨轮联合声明(如 MP-QKD)。Phase 1 再扩展。
    """
    function: Callable[[tuple[int, ...]], int]
    sift_keep: Callable[[tuple[int, ...]], bool]


@dataclass(frozen=True)
class KeyMap:
    """K:从保留下来的数据到密钥比特的映射。

    属性:
        key_party: str,哪一方的 key register 被用作最终密钥(通常 "Alice")
        bitmap: dict[int, int],key_register 的测量结果 → 最终 key bit

    Phase 0 限制:
        仅支持二进制密钥(最终 key bit ∈ {0, 1})。
        仅支持 Alice 作为 key party(MDI-QKD 中 Bob 的翻转在 announcement 里处理)。
    """
    key_party: str
    bitmap: dict[int, int]


@dataclass(frozen=True)
class MSEBProtocol:
    """MS-EB 五元组 Π = (P, E, A, T, K)。

    属性:
        name: 协议名,如 "BB84"、"MDI-QKD"
        sources: tuple of SourceParty,顺序固定为 (Alice, [Bob], [Charlie], ...)
        network: PublicQuantumNetwork
        announcement: AnnouncementRule
        key_map: KeyMap
        observation_keys: tuple of 可观测量名,如 ("qber_Z", "qber_X", "p_sift")。
            `wlc.py::_build_observable_operators` 的查表键必须是这个 tuple 的子集。
        symmetry_group: 可选,协议的对称群名(用于 SDP 约化,Phase 0 M4A 引入)

    跨对象不变量(__post_init__ 校验):
        network.channel.dim_in == prod(src.signal_register_dim for src in sources)
        key_map.key_party ∈ {src.name for src in sources}
        set(observation_keys) 与 wlc._OBSERVABLE_BUILDERS 的键交集非空

    方法:
        joint_state: 返回所有源方的联合 EB 态 ⊗_i |ψ_i⟩,形状 (prod dims × 1)
        executed_state: 返回协议执行后 A_1 ... A_n ⊗ B ⊗ C 的完整密度矩阵
        conditional_alice_bob: 筛选后的 ρ,WLC SDP 的输入
        conditional_alice_bob_dim: 上述密度矩阵的希尔伯特空间维度 d,供 wlc.py 声明 cp.Variable((d,d))
        observable: 查表返回指定观测名对应的算子 Γ_k(Hermitian,形状 d×d)
    """
    name: str
    sources: tuple[SourceParty, ...]
    network: PublicQuantumNetwork
    announcement: AnnouncementRule
    key_map: KeyMap
    observation_keys: tuple[str, ...]
    symmetry_group: str | None = None

    def __post_init__(self) -> None:
        """跨对象不变量统一在此校验(v3,从 PublicQuantumNetwork 迁入)。"""
        expected_dim_in = int(np.prod([s.signal_register_dim for s in self.sources]))
        if self.network.channel.dim_in != expected_dim_in:
            raise ValueError(
                f"network.channel.dim_in ({self.network.channel.dim_in}) != "
                f"prod(sources.signal_register_dim) ({expected_dim_in})"
            )
        party_names = {s.name for s in self.sources}
        if self.key_map.key_party not in party_names:
            raise ValueError(
                f"key_map.key_party {self.key_map.key_party!r} not in sources {party_names}"
            )
        if not self.observation_keys:
            raise ValueError("observation_keys must be non-empty")

    def joint_state(self) -> Matrix:
        """返回 ⊗_i |ψ_i⟩_{A_i A_i'} 的列向量。"""

    def executed_state(self) -> Matrix:
        """协议执行后,在 Alice 测量前的全局纯化态 ρ_{A_1...A_n B C}。"""

    def conditional_alice_bob(self) -> Matrix:
        """经过 announcement.sift_keep 筛选后的 ρ_{A_1 B | keep=True}。WLC SDP 的输入密度矩阵。"""

    def conditional_alice_bob_dim(self) -> int:
        """`conditional_alice_bob()` 返回矩阵的维度 d。

        等价于 `self.conditional_alice_bob().shape[0]`,但无需真正构造密度矩阵 —
        供 `wlc.py` 在声明 `cp.Variable((d, d), hermitian=True)` 前确定维度。
        """

    def observable(self, key: str) -> Matrix:
        """查表返回观测量 Γ_k(Hermitian,d×d,d = conditional_alice_bob_dim())。

        key ∈ self.observation_keys;未知键抛 ValueError。
        具体构造分派到 `wlc._OBSERVABLE_BUILDERS[key](self)`。
        """
```

**设计说明**:
- `MSEBProtocol` 是**纯数据类 + 只读查询方法**,不包含求解逻辑。密钥率计算在 `numerics/wlc.py` 的函数中实现。
- `AnnouncementRule` 用强类型 `Callable[[tuple[int, ...]], int/bool]`(v3,原 `callable` 失去契约)。
- `symmetry_group` 为字符串(如 `"Z2_XZ_swap"`),具体表示查 `symmetry/groups.py` 的注册表。
- 跨对象不变量**集中在 `MSEBProtocol.__post_init__`**(v3,原 `PublicQuantumNetwork` 引用 `sources` 不成立)。

**测试覆盖**(`tests/test_protocol/test_base.py`):
- `test_mseb_joint_state_norm_preserved`:`np.linalg.norm(protocol.joint_state()) == 1` (误差 1e-10)
- `test_mseb_executed_state_is_density`:`is_density(executed_state())` 返回 True
- `test_mseb_sources_tuple_immutable`:尝试修改 `sources[0].name` 抛 FrozenInstanceError
- `test_mseb_dim_mismatch_raises`:`network.channel.dim_in` 不匹配 `prod(signal_register_dim)` 抛 ValueError
- `test_mseb_unknown_observation_key_raises`:`protocol.observable("unknown_key")` 抛 ValueError
- `test_mseb_empty_observation_keys_raises`:`observation_keys=()` 抛 ValueError

> **codex §1 结论**:
> - §1‑2 resolved:`observation_keys`、`conditional_alice_bob_dim()`、`observable()` 已加入 `MSEBProtocol`
> - §1‑3 resolved:跨对象不变量从 `PublicQuantumNetwork` 迁至 `MSEBProtocol.__post_init__`
> - §1‑4 见 §4.6 `GMap`
>
> **codex §6 结论**:
> - §6‑1 resolved:`AnnouncementRule` 字段改为严格 `Callable[...]` 签名
> - §6‑4 resolved:`_build_observable_operators` 的参数/返回改为 `Sequence[str]` / `Mapping[str, Matrix]`(见 §4.6)

---

### 4.5 `qkdx/protocols/bb84.py`

**职责**:BB84 作为 MS-EB 框架的第一个具体实例。是 M1 验收的核心。

```python
from __future__ import annotations
import numpy as np
from qkdx.core.hilbert import (
    Matrix, KET_0, KET_1, KET_PLUS, KET_MINUS, tensor, proj,
    SIGMA_X, SIGMA_Z, HADAMARD
)
from qkdx.core.operators import KrausMap, POVM
from qkdx.protocol.base import (
    MSEBProtocol, SourceParty, PublicQuantumNetwork, AnnouncementRule, KeyMap
)


def bb84_alice_source() -> SourceParty:
    """Alice 的 EB 态:

        |ψ⟩_{AA'} = (1/2) · Σ_{x,θ} |x,θ⟩_A ⊗ U_θ|x⟩_{A'}

    其中:
        x ∈ {0, 1}(比特值)
        θ ∈ {Z, X}(基选择)
        U_Z = I, U_X = H

    key_register_dim = 4(x ∈ {0,1} × θ ∈ {Z,X})
    signal_register_dim = 2(qubit 发送给 Bob)
    """


def bb84_channel(qber: float) -> KrausMap:
    """简化的 qubit 量子信道模型,对应 QBER = qber 的对称去极化。

    注意:这只是 M1 的占位模型。真实信道在 M3 诱骗态以后引入。

    Kraus:
        K_0 = sqrt(1 - 3p/4) · I
        K_1 = sqrt(p/4) · σ_x
        K_2 = sqrt(p/4) · σ_y
        K_3 = sqrt(p/4) · σ_z
    其中 p = 2·qber(去极化参数与 QBER 的转换)。
    """


def bb84_network(qber: float, bob_detector_efficiency: float = 1.0) -> PublicQuantumNetwork:
    """BB84 公共网络:Alice → (信道) → Bob → 测量(基选择 θ_B ∈ {Z,X},公开)

    简化:
        Phase 0 M1 只建模完美探测器、完美光源、无暗计数。
        非理想性在 M3 引入。

    receiver_dim: 2(Bob 的量子寄存器,其实测量后立即经典化)
    classical_outcomes: 4(Bob 的 (θ_B, bit_B) 的 4 种组合)
    """


def bb84_announcement() -> AnnouncementRule:
    """筛选规则:

        function(outcomes) = (θ_A, θ_B),即公开双方基选择
        sift_keep = (θ_A == θ_B)
    """


def bb84_key_map() -> KeyMap:
    """Alice 的 x ∈ {0, 1} 就是密钥比特。"""


def build_bb84_protocol(qber: float) -> MSEBProtocol:
    """组装完整 BB84 协议。QBER 参数内嵌在信道模型里。

    构造时写入 `observation_keys=("qber_Z", "qber_X", "p_sift")`。
    BB84 完美探测器下 `p_sift = 0.5`;若 M3 引入 decoy/信道损耗,由调用方覆盖。

    示例:
        >>> protocol = build_bb84_protocol(qber=0.05)
        >>> from qkdx.numerics.wlc import wlc_key_rate
        >>> result = wlc_key_rate(
        ...     protocol,
        ...     observations={"qber_Z": 0.05, "qber_X": 0.05, "p_sift": 0.5},
        ... )
        >>> R = result.key_rate          # 单位 bit/signal
        >>> from qkdx.analytic.shor_preskill import shor_preskill_rate
        >>> R_analytic = shor_preskill_rate(0.05)   # 默认 sift_rate=0.5,单位 bit/signal
        >>> abs(R - R_analytic) < max(0.01 * R_analytic, 5e-4)   # rel=0.01, abs=5e-4
        True
    """
```

**测试覆盖**(`tests/test_protocols/test_bb84.py`):
- `test_bb84_joint_state_is_pure`:`joint_state()` 的 Schmidt rank >= 2
- `test_bb84_sift_keep_rate_is_half`:随机运行 10000 次,sift_keep 比例在 0.49–0.51
- `test_bb84_no_noise_gives_zero_qber`:qber=0 时 Alice 与 Bob 筛选后的 raw key 完全一致

---

### 4.6 `qkdx/numerics/wlc.py`(核心模块)

**职责**:实现 Winick-Lütkenhaus-Coles 2018 的 SDP 数值密钥率下界。

参考公式(WLC 2018 Eq. 8–12):

```
R ≥ inf_ρ  D( 𝒢(ρ) ‖ 𝒵(𝒢(ρ)) )
    s.t.   ⟨Γ_k⟩_ρ = γ_k     (实验观测约束)
           ρ ⪰ 0              (半正定)
           tr(ρ) = 1          (归一化)

其中:
    𝒢: A_1 A_2 → A_key ⊗ B_保留 的 CPTNI 映射(密钥映射 + Bob 测量)
    𝒵: A_key → A_key 的 pinching 信道(对密钥寄存器取对角)
    Γ_k: 可观测算子(POVM 元素的张量)
    γ_k: 对应实验测量的期望值(QBER、gain 等)
```

```python
from __future__ import annotations
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
import numpy as np
import cvxpy as cp

from qkdx.core.hilbert import Matrix
from qkdx.core.operators import KrausMap
from qkdx.protocol.base import MSEBProtocol


@dataclass(frozen=True)
class GMap:
    """v3 新增:WLC 中 𝒢 映射的封装,携带 pinching 需要的维度元数据。

    属性:
        map: CPTNI 映射(Kraus 表示)A_1 A_2 → A_key ⊗ B_side
        dim_key: A_key 寄存器维度(用于构造 pinching 信道 𝒵)
        dim_side: B_side(保留侧信息)寄存器维度
    不变量:
        map.dim_out == dim_key * dim_side
    """
    map: KrausMap
    dim_key: int
    dim_side: int

    def __post_init__(self) -> None:
        if self.map.dim_out != self.dim_key * self.dim_side:
            raise ValueError(
                f"GMap.map.dim_out ({self.map.dim_out}) != dim_key*dim_side "
                f"({self.dim_key}*{self.dim_side})"
            )


@dataclass
class WLCResult:
    """WLC SDP 求解结果。

    **单位口径(v3.1 明确)**:`key_rate` 的单位为 **bit/signal**(每一次信号发送的期望密钥比特)。
    内部计算步骤:
        1. 在 `ρ = conditional_alice_bob` 上求 H(A_key | E),单位 nat
        2. 除以 `ln 2` 得 `H_bits`,单位 bit / sift 轮
        3. 减去 `leak_ec = f_ec · h(qber_Z)`,仍 bit / sift 轮
        4. 乘以 `p_sift = observations["p_sift"]`(sift_keep 的概率,含 gain 与基匹配),得 bit / signal

    属性:
        key_rate: 密钥率下界(渐进),单位 **bit/signal**
        primal_status: cvxpy 状态字符串,接受 "optimal" 和 "optimal_inaccurate"(v3)
        h_bits_per_sift: 内部中间量,H(A_key|E)_bits(诊断用,单位 bit/sift)
        iterations: 求解器迭代次数
        duality_gap: |primal - dual|;若求解器不暴露 dual,记 NaN
        optimal_rho: 达到下界的最优 ρ(可选,用于诊断)
        solver: 实际使用的求解器名
    """
    key_rate: float
    primal_status: str
    h_bits_per_sift: float
    iterations: int
    duality_gap: float
    optimal_rho: Matrix | None = None
    solver: str = "MOSEK"


def wlc_key_rate(
    protocol: MSEBProtocol,
    observations: Mapping[str, float],
    *,
    solver: str = "MOSEK",
    epsilon_regularization: float = 1e-9,
    f_ec: float = 1.16,
    max_iters: int = 1000,
    verbose: bool = False,
) -> WLCResult:
    """WLC SDP 求解 MS-EB 协议在给定观测约束下的密钥率下界。

    参数:
        protocol: MS-EB 协议对象,必须暴露 `observation_keys`、`conditional_alice_bob_dim()`、`observable(key)`
        observations: 实验测量的期望值,键必须与 `protocol.observation_keys` 相等(v3.1:严格等于,非子集)
            **必含**键 `"p_sift"`: 每次信号发送能进入最终密钥环节的概率(= P(detection)·P(sift_keep | detection))。
            BB84 完美探测器下 `p_sift = 0.5`;带损耗时 `p_sift = gain · 0.5`。
            其他键(`qber_Z`、`qber_X` 等)与协议的 POVM 观测对应。
            示例:{"qber_Z": 0.02, "qber_X": 0.02, "p_sift": 0.5}
        solver: CVXPY 支持的 SDP 求解器,推荐 MOSEK,fallback CLARABEL/SCS
        epsilon_regularization: 通道级去极化正则化强度 ε ∈ [0,1)(v3 语义改动,见 Appendix B)
        f_ec: 纠错效率因子,用于 Devetak-Winter 公式 R = H(Key|E) − f_ec·h(qber_Z)(Brassard-Salvail 1993)
        max_iters: 求解器迭代上限
        verbose: 是否打印求解器日志

    返回:
        WLCResult(`key_rate` 单位 **bit/signal**,`h_bits_per_sift` 单位 **bit/sift**)

    异常:
        ValueError: observations 键集合不等于 protocol.observation_keys(缺键或多余键)
        cvxpy.SolverError: 求解失败(status 既非 "optimal" 也非 "optimal_inaccurate")

    实现步骤(详见 §附录 B 伪代码):
        1. 从 protocol 构造 𝒢 映射(返回 GMap,携带 dim_key/dim_side)
        2. 构造 𝒵 pinching 信道:作用空间为 A_key ⊗ B_side,pinching 只在 A_key 上,B_side 保持恒等
        3. 声明 `rho = cp.Variable((d,d), hermitian=True)`,d = protocol.conditional_alice_bob_dim()
        4. 构造约束:观测等式 + `rho >> 0` + `cp.trace(rho) == 1`
        5. 对 `X_raw = 𝒢(ρ)` 做 Hermitian 投影;通道级去极化正则化:
           `X_reg = (1-ε)·X_raw + ε·tr(X_raw)·τ`,`τ = I/d_out`
           关键:因 𝒢 为 **CPTNI**(非 CPTP),一般 `tr(X_raw) ≠ tr(ρ)=1`,必须显式用 `cp.trace(X_raw)`
        6. 目标:`min cp.quantum_rel_entr(X_reg, Y_reg)`,`Y_reg = (Z ⊗ I_side)(X_reg)`
        7. 单位换算与 Devetak-Winter 拼装:
           `H_bits = obj_value / ln 2`    # bit per sift
           `leak_ec = f_ec · h(qber_Z)`
           `R_per_sift = H_bits − leak_ec`
           `R = p_sift · R_per_sift`      # bit per signal(对外)
        8. 求解 + 包装(含 optimal_inaccurate 接受逻辑)
    """


def _build_observable_operators(
    protocol: MSEBProtocol,
    observation_keys: Sequence[str],  # v3: Sequence 而非 list
) -> Mapping[str, Matrix]:            # v3: Mapping 而非 dict
    """为每个观测名构造对应的可观测算子 Γ_k。调度到模块级注册表。

    Phase 0 支持的键(见 `_OBSERVABLE_BUILDERS`):
        "qber_Z":Z 基 QBER 对应的算子
        "qber_X":X 基 QBER 对应的算子
        "p_sift":sift 概率 P(sift_keep)(标量约束,由 announcement 统计量构造)
        "gain_Z" / "gain_X":基相关增益(M3 decoy 引入)

    扩展请向 `_OBSERVABLE_BUILDERS` 注册,无需修改本函数。
    """


# 模块级观测算子注册表(v3,§4.6 + codex §1)
_OBSERVABLE_BUILDERS: Mapping[str, Callable[[MSEBProtocol], Matrix]] = {
    # 每个 builder 接受 protocol,返回 Hermitian d×d 矩阵,d = protocol.conditional_alice_bob_dim()
}


def _construct_G_map(protocol: MSEBProtocol) -> GMap:  # v3: 返回 GMap,非 KrausMap
    """构造 WLC 公式中的 𝒢 映射,并携带 pinching 所需的维度元数据。

    𝒢 = (V_key ⊗ M_Bob) ∘ Alice_measurement

    返回:
        GMap(map=..., dim_key=..., dim_side=...)
    """


def _construct_Z_pinching(dim_key: int, dim_side: int = 1) -> KrausMap:
    """𝒵_on_XB = Z_pinching_on_Akey ⊗ I_Bside,作用在 d_key · d_side 维的 X 上(v3.1)。

    𝒵_on_XB(σ) = Σ_x (|x⟩⟨x| ⊗ I_side) · σ · (|x⟩⟨x| ⊗ I_side)

    作为 Kraus 映射:K_x = (|x⟩⟨x| ⊗ I_{d_side}),x ∈ [d_key]
    dim_in = dim_out = dim_key · dim_side

    dim_side=1 时退化为 v3 之前的纯 A_key pinching(保留默认值方便 BB84)。
    """


def _apply_cvxpy_map(K: KrausMap, X: cp.Expression) -> cp.Expression:
    """把 Kraus 映射作用在 CVXPY 表达式上:E(X) = Σ_i K_i · X · K_i†(v3 新增,codex §2-2)。

    实现:
        terms = [cp.Constant(Ki) @ X @ cp.Constant(Ki).H for Ki in K.kraus]
        return sum(terms)
    不变量:
        Ki 矩阵视为常量;X 的 Hermitian 性在调用方显式投影
        `_apply_cvxpy_map(KrausMap.identity(d), X)` 数值上等价 X(相差浮点误差)
    """
```

**关键实现细节**(CVXPY 的坑,v3 扩展):

1. **Hermitian 投影必须显式**:`cp.quantum_rel_entr(X, Y)` 对非严格 Hermitian 的线性表达式可能报 DCPError;在 `X = _apply_cvxpy_map(...)` 后插入 `X = 0.5 * (X + X.H)`。
2. **正则化不能加 εI 到两侧**(会改 trace / 引入目标偏差):用**通道级去极化**
   `X_reg = (1-ε)·X_raw + ε·tr(X_raw)·τ`,`τ = I/d_out`(见 Appendix B)。
   其中 `X_raw = 𝒢(ρ)`;因 𝒢 为 **CPTNI**,一般 `tr(X_raw) ≠ tr(ρ) = 1`,必须显式用 `cp.trace(X_raw)` 而不是 1 或 `tr(ρ)`。
3. `cp.quantum_rel_entr` 返回 **nat 基**;所有对外的密钥率必须除以 `ln 2` 转为 **bit 基**:
   `H_bits = cp.value(objective) / np.log(2.0)`。
4. CVXPY 复变量声明:`cp.Variable((d, d), hermitian=True)`,约束 `X >> 0`。
5. 观测约束必须用 `cp.real(cp.trace(Γ_k @ rho)) == γ_k`(确保 CVXPY 识别为实标量约束)。
6. MOSEK 复 SDP 求解需要 `solver=cp.MOSEK`,并显式给定 `mosek_params`(见下)—— 原 `max_iters` 直接传参不可移植。

**MOSEK 参数建议**(v3,codex §2-4):
```python
MOSEK_PARAMS = {
    "MSK_DPAR_INTPNT_CO_TOL_REL_GAP": 1e-8,
    "MSK_DPAR_INTPNT_CO_TOL_PFEAS":   1e-8,
    "MSK_DPAR_INTPNT_CO_TOL_DFEAS":   1e-8,
    "MSK_IPAR_INTPNT_MAX_ITERATIONS": 1000,
}
```

> **codex §1 结论**:
> - §1‑1 resolved:`wlc_key_rate` 签名带 `observations: Mapping[str, float]`,§4.5 示例同步
> - §1‑4 resolved:`_construct_G_map` 返回 `GMap(map, dim_key, dim_side)`
>
> **codex §2 结论**:
> - §2‑1 resolved:Hermitian 投影显式化(本节 "关键实现细节 #1" + Appendix B)
> - §2‑2 resolved:`_apply_cvxpy_map` 公开签名 + 实现(本节)
> - §2‑3 resolved **(v3.1 修订)**:通道级去极化修正为 `X_reg = (1-ε)X_raw + ε·tr(X_raw)·τ`,反映 𝒢 为 CPTNI 下 `tr(X_raw)≠tr(ρ)=1`(Appendix B)
> - §2‑4 resolved:`MOSEK_PARAMS` 明确(本节)
> - §2‑5 resolved:`key_rate_bits = prob.value / np.log(2.0)`(Appendix B)
>
> **codex v3.1 二轮结论**:
> - v3.1‑§1 resolved:`WLCResult` 新增 `h_bits_per_sift` 诊断字段;单位口径明确 **bit/signal**;`observations["p_sift"]` 显式参数
> - v3.1‑§2 resolved:`_construct_Z_pinching(dim_key, dim_side)` 双参数消除维度歧义
> - v3.1‑§3 resolved:`facial.reduce_problem` 的 `lift()` 在 Appendix B 被正确调用回注原空间

**测试覆盖**(`tests/test_numerics/test_wlc_bb84.py` — 这是 M1 验收的核心,v3 修订):

```python
import numpy as np
import pytest
from qkdx.protocols.bb84 import build_bb84_protocol
from qkdx.analytic.shor_preskill import shor_preskill_rate
from qkdx.numerics.wlc import wlc_key_rate
from qkdx.utils.solvers import has_mosek  # v3: §11.3 runtime guard

pytestmark = pytest.mark.skipif(not has_mosek(), reason="MOSEK unavailable; see docs/SOLVER_SUPPORT.md")


@pytest.fixture
def rng() -> np.random.Generator:
    """固定种子的 PRNG,保证随机测试可复现(v3)。"""
    return np.random.default_rng(20260418)


@pytest.mark.parametrize(
    "qber",
    [0.00, 0.01, 0.02, 0.05, 0.08, 0.10],
    ids=lambda x: f"qber_{x:.3f}",                       # v3: 稳定 id,避免浮点格式漂移
)
def test_wlc_bb84_matches_shor_preskill(qber: float) -> None:
    """WLC SDP 结果与 Shor-Preskill 解析值误差 rel=0.01, abs=5e-4。"""
    protocol = build_bb84_protocol(qber=qber)
    R_numerical = wlc_key_rate(
        protocol,
        observations={"qber_Z": qber, "qber_X": qber, "p_sift": 0.5},
    ).key_rate
    R_analytic = shor_preskill_rate(qber)
    assert R_numerical == pytest.approx(R_analytic, rel=0.01, abs=5e-4)


def test_wlc_bb84_above_threshold_gives_zero() -> None:
    """QBER > 11% 时密钥率应为 0(或负后被 clip 到 0)。"""
    protocol = build_bb84_protocol(qber=0.13)
    R = wlc_key_rate(
        protocol, observations={"qber_Z": 0.13, "qber_X": 0.13, "p_sift": 0.5}
    ).key_rate
    assert R <= 5e-4  # abs 容忍


@pytest.mark.slow
def test_wlc_bb84_qber_exact_zero_with_facial_reduction() -> None:
    """精确 QBER=0 会让 ρ 落入降维面,需 facial reduction 才能求解(v3,codex §7-1)。"""
    protocol = build_bb84_protocol(qber=0.0)
    result = wlc_key_rate(
        protocol, observations={"qber_Z": 0.0, "qber_X": 0.0, "p_sift": 0.5}
    )
    assert result.primal_status in {"optimal", "optimal_inaccurate"}
    assert result.key_rate == pytest.approx(1.0, rel=0.01, abs=5e-4)


def test_wlc_solver_status_is_optimal_or_inaccurate() -> None:
    """常规 QBER=0.05 的问题应能被 MOSEK 接受(接受 optimal_inaccurate,v3,codex §5-5)。"""
    protocol = build_bb84_protocol(qber=0.05)
    result = wlc_key_rate(
        protocol, observations={"qber_Z": 0.05, "qber_X": 0.05, "p_sift": 0.5}
    )
    assert result.primal_status in {"optimal", "optimal_inaccurate"}
    # duality_gap 可能为 NaN(求解器不暴露 dual),只在有限时检查
    if np.isfinite(result.duality_gap):
        assert result.duality_gap < 1e-4


def test_wlc_fallback_to_clarabel() -> None:
    """MOSEK 不可用时 fallback 到 CLARABEL 精度仍在验收范围(CLARABEL 容忍稍松)。"""
    protocol = build_bb84_protocol(qber=0.05)
    result = wlc_key_rate(
        protocol, observations={"qber_Z": 0.05, "qber_X": 0.05, "p_sift": 0.5},
        solver="CLARABEL",
    )
    R_analytic = shor_preskill_rate(0.05)
    assert result.key_rate == pytest.approx(R_analytic, rel=0.02, abs=1e-3)


def test_wlc_observable_key_missing_raises() -> None:
    """观测字典缺 protocol.observation_keys 中的键时给出清晰错误。"""
    protocol = build_bb84_protocol(qber=0.05)
    with pytest.raises(ValueError, match="missing observation: qber_X"):
        wlc_key_rate(protocol, observations={"qber_Z": 0.05, "p_sift": 0.5})


def test_wlc_observable_key_unknown_raises() -> None:
    """观测字典含 observation_keys 之外的键(可能拼写错误)抛 ValueError。"""
    protocol = build_bb84_protocol(qber=0.05)
    with pytest.raises(ValueError, match="unknown observation"):
        wlc_key_rate(
            protocol,
            observations={
                "qber_Z": 0.05, "qber_X": 0.05, "p_sift": 0.5,
                "typo_key": 0.5,
            },
        )
```

> **codex §7 结论**:
> - §7‑1 resolved:`test_wlc_bb84_qber_exact_zero_with_facial_reduction` 覆盖 QBER=0
> - §7‑2 resolved:参数化 `ids=lambda x: f"qber_{x:.3f}"`
> - §7‑3 resolved:`rng()` fixture 固定 seed
> - §7‑4 resolved:`pytestmark = pytest.mark.skipif(not has_mosek(), ...)`

---

### 4.7 `qkdx/numerics/facial.py`

**职责**:facial reduction,处理 SDP 的严格可行性失败(Hu-Li 2022)。

```python
from __future__ import annotations
from collections.abc import Callable
import numpy as np
import cvxpy as cp
from qkdx.core.hilbert import Matrix


def detect_face(
    constraints: list[cp.Constraint],
    variable: cp.Variable,
    atol: float = 1e-8,
) -> tuple[Matrix, int]:
    """侦测 ρ 必然位于的最小面(face)。

    返回:
        projector: 形状 (d, d),投影到面所在的子空间
        rank: 面的维度

    触发条件:
        当某些观测约束迫使 ρ 具有低秩结构时(如 QBER=0),CVXPY 会报告
        primal_status == "infeasible" 或 "inaccurate"。此函数检测并返回
        子空间投影,调用方用 ρ = P·ρ'·P 重新参数化,在 rank 维度上求解。

    算法(简化):
        对每个等式约束 ⟨A_k⟩_ρ = b_k,若 A_k 半正定且 b_k = 0,则
        supp(ρ) ⊂ ker(A_k)。取所有这些 ker 的交集。
    """


def reduce_problem(
    prob: cp.Problem,
    variable: cp.Variable,
) -> tuple[cp.Problem, Callable[[], Matrix]]:
    """对原问题做 facial reduction,返回 (reduced_prob, lift)(v3)。

    返回:
        reduced_prob: 降维后的等价问题,变量维度 = rank
        lift: 无参数的闭包,调用时返回原空间的 ρ(形状 d×d)。
              必须在 reduced_prob.solve() 之后调用,利用内部变量当前 .value。

    v3 修订原因:
        v2 版本 `prob.solve(); rho.value` 无法得到正确的原空间 ρ(变量映射丢失)。
        新签名把 lift 作为显式 hook,把子空间解回注到原 ρ 的形状。
    """
```

**测试覆盖**(`tests/test_numerics/test_facial.py`):
- `test_detect_face_qber_zero`:当 QBER=0 时 detect_face 返回 rank 2 而非 4 的投影器
- `test_reduce_problem_preserves_optimum`:降维前后最优值差 < 1e-10

---

### 4.8 `qkdx/numerics/decoy.py`

**职责**:数值诱骗态分析(George-Lin-Lütkenhaus 2020)。M3 交付。

```python
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import cvxpy as cp


@dataclass
class DecoyParameters:
    """诱骗态实验参数。

    属性:
        intensities: tuple[float, ...],光源强度 μ_i
        probabilities: tuple[float, ...],每个强度的发射概率
        observed_gains: dict[float, float],{μ: Q_μ}
        observed_qbers: dict[float, float],{μ: E_μ}

    不变量:
        sum(probabilities) == 1
        len(intensities) == len(probabilities) == len(observed_gains) == len(observed_qbers)
        每个 intensity ∈ (0, 1](弱相干假设)
    """
    intensities: tuple[float, ...]
    probabilities: tuple[float, ...]
    observed_gains: dict[float, float]
    observed_qbers: dict[float, float]


def single_photon_bounds(
    params: DecoyParameters,
    *,
    photon_cutoff: int = 4,
    solver: str = "MOSEK",
) -> tuple[float, float]:
    """数值估计单光子事件的增益下界 Y_1^L 和 QBER 上界 e_1^U。

    参数:
        params: 诱骗态实验数据
        photon_cutoff: Fock 空间截断,默认 4(George-Lütkenhaus 证明对较大 n 贡献可忽略)

    返回:
        (Y_1_lower_bound, e_1_upper_bound)

    数学:
        Y_n, e_n 满足:
            Q_μ = Σ_n (μ^n · e^{-μ} / n!) · Y_n
            E_μ · Q_μ = Σ_n (μ^n · e^{-μ} / n!) · Y_n · e_n
        用 SDP 求 min Y_1 和 max e_1 在这些约束下。
    """


def decoy_state_key_rate(
    params: DecoyParameters,
    *,
    f_ec: float = 1.16,  # Cascade 纠错效率因子,Brassard-Salvail 1993
) -> float:
    """基于 GLLP 公式的诱骗态 BB84 密钥率。

    R = q · { -Q_μ · f · h(E_μ) + Q_1 · [1 - h(e_1)] }

    其中 q=1/2(BB84 sift rate),Q_1 = μ·e^{-μ}·Y_1(单光子增益)。
    """
```

**测试覆盖**(`tests/test_numerics/test_decoy_bb84.py`):
- `test_decoy_one_decoy_matches_analytic`:单诱骗态 + 信号态 vs Ma-Qi-Zhao-Lo 2005 公式,误差 < 1%
- `test_decoy_two_intensities_tighter_than_analytic`:两强度 decoy 数值密钥率严格 ≥ 解析
- `test_decoy_distance_sweep`:在 {20, 50, 100, 150, 200} km 的密钥率曲线斜率在文献范围

---

### 4.9 `qkdx/analytic/shor_preskill.py`

**职责**:解析密钥率公式作为交叉验证基线。

```python
from __future__ import annotations
import numpy as np
from qkdx.core.entropy import binary_entropy


def shor_preskill_rate(qber: float, *, sift_rate: float = 0.5) -> float:
    """Shor-Preskill (2000) 渐进密钥率。

        R_∞ = sift_rate · max(0, 1 - 2·h(QBER))

    阈值:QBER = 11%,此时 R = 0。

    参数:
        qber: 量子比特错误率 ∈ [0, 0.5]
        sift_rate: 筛选保留率,BB84 = 0.5,六态 = 1/3

    返回:
        密钥率 ≥ 0
    """


def threshold_qber() -> float:
    """Shor-Preskill 阈值 QBER(BB84),由 1 - 2·h(x) = 0 解出。"""


SHOR_PRESKILL_THRESHOLD: float = 0.1100  # 更精确值见 threshold_qber()
```

---

### 4.10 `qkdx/analytic/six_state.py`

```python
import numpy as np
from qkdx.core.entropy import binary_entropy


def six_state_rate(qber: float, *, sift_rate: float = 1/3) -> float:
    """六态协议渐进密钥率(Bruss 1998):

        R_∞ = sift_rate · max(0, 1 - h(QBER) - QBER · log2(3))

    阈值:约 12.6%。
    """


SIX_STATE_THRESHOLD: float = 0.1262
```

---

### 4.11 `qkdx/analytic/gllp.py`

```python
import numpy as np
from qkdx.core.entropy import binary_entropy


def gllp_rate(
    mu: float, eta: float, e_d: float, Y_0: float,
    *, f_ec: float = 1.16,
) -> float:
    """GLLP (Gottesman-Lo-Lütkenhaus-Preskill) 密钥率。

    参数:
        mu: 信号态平均光子数
        eta: 信道 + 探测器总透过率
        e_d: 探测器误码率
        Y_0: 暗计数率
        f_ec: 纠错效率因子

    实现:
        Q_μ = Y_0 + 1 - exp(-μ·η)
        E_μ = (e_0 · Y_0 + e_d · (1 - exp(-μ·η))) / Q_μ,e_0 = 0.5
        Q_1 = μ·exp(-μ) · (Y_0 + η)
        e_1 = (e_0·Y_0 + e_d·η) / (Y_0 + η)
        R = q · { -Q_μ·f_ec·h(E_μ) + Q_1·[1 - h(e_1)] }
    """
```

---

### 4.12 `qkdx/protocols/sixstate.py`、`mdi.py`、`tfqkd.py`

结构与 `bb84.py` 平行,此处不重复列签名。关键函数名:

```python
# sixstate.py
build_sixstate_protocol(qber: float) -> MSEBProtocol

# mdi.py
build_mdi_protocol(
    qber_z: float, qber_x: float, gain: float,
    charlie_bsm_efficiency: float = 1.0,
) -> MSEBProtocol

# tfqkd.py (M4 交付)
build_tfqkd_sending_or_not_protocol(
    eta_a: float, eta_b: float, phase_ref_accuracy: float,
    coherent_amplitude: float,
) -> MSEBProtocol
```

---

### 4.13 `qkdx/symmetry/` 和 `qkdx/utils/`

(为节省篇幅,这两个模块按同样的函数级规范编写,关键函数列表:)

```python
# symmetry/groups.py
class FiniteGroup:
    name: str
    elements: tuple[Matrix, ...]
    def average(self, rho: Matrix) -> Matrix: ...

def clifford_group(dim: int) -> FiniteGroup: ...
def permutation_group(n: int) -> FiniteGroup: ...

# symmetry/twirling.py
def twirl(rho: Matrix, group: FiniteGroup) -> Matrix: ...
def symmetrize_problem(prob: cp.Problem, group: FiniteGroup) -> cp.Problem: ...

# utils/validation.py
def assert_hermitian(M: Matrix, name: str = "matrix") -> None: ...
def assert_psd(M: Matrix, name: str = "matrix") -> None: ...
def assert_density(rho: Matrix, name: str = "rho") -> None: ...

# utils/logging.py
def get_logger(name: str): ...  # structlog 封装,同时输出到文件和 console
```

---

## 5. Milestone 验收标准(与 §4 对齐)

**Phase 0 工期拆解**(v3.1,与 12–16 周口径对齐):
- **Phase 0 必需范围** = M1(3 周)+ M2(2 周)+ M3(3 周)+ M4A(2 周)+ 集成 & 复现报告(2 周)= **12 周**
- **Phase 0.5 可选范围** = M4B(2–3 周,TF-QKD),**不在 12 周必需关键路径**
- **总预算 12–16 周**:12 周完成 Phase 0,含 M4B 则上限 15 周,再加 1 周缓冲。超期不降低验收标准(§8 R5)。

| Milestone | 交付模块 | 硬验收标准 |
|-----------|---------|-----------|
| **M1**(3 周) | `core/hilbert.py`、`core/operators.py`、`core/entropy.py`、`protocol/base.py`、`protocols/bb84.py`、`analytic/shor_preskill.py`、`numerics/wlc.py`(最小版) | `test_wlc_bb84_matches_shor_preskill` 六个 qber 点全部通过(`rel=0.01, abs=5e-4`);覆盖率:core ≥ 95%、`numerics.wlc` ≥ 75%、overall ≥ 85% |
| **M2**(2 周) | `protocols/sixstate.py`、`protocols/mdi.py`、`analytic/six_state.py`、`analytic/gllp.py` | 六态数值 vs 解析误差 `rel=0.01, abs=5e-4`;MDI-QKD 数值 vs Ma-Razavi 2012 误差 `rel=0.01, abs=5e-4`;`numerics/wlc.py` 仅允许**加法式**修改(新增协议相关的可观测算子 builder),BB84 基线测试零回归 |
| **M3**(3 周) | `numerics/decoy.py`、`numerics/facial.py` | 单诱骗态数值 vs 解析误差 `rel=0.01, abs=5e-4`;两强度 decoy 数值密钥率 **≥ 解析 − 1e-4**(浮点求解器允许微量反转);距离扫描曲线与 Lo-Ma-Chen 2005 Fig.3 视觉一致 |
| **M4A**(2 周) | `symmetry/groups.py`、`symmetry/twirling.py` | Clifford 约化把 BB84 SDP 变量降到 2×2;六态同理;`rel=0.01, abs=5e-4`;**TF-QKD 不在本里程碑** |
| **M4B**(2–3 周,可延至 Phase 0.5) | `protocols/tfqkd.py` | TF-QKD 的 R(η) 在 log-log 图上斜率 = 0.5 ± 0.05;验收独立于 M4A,失败不阻塞 Phase 0 总验收 |
| **Phase 0 总验收** | 全部 | 所有 pytest 绿;`pytest --cov=qkdx` overall ≥ 85%;`docs/PHASE0_REPORT.md` 8–12 页 memo 完成;复现 Winick 2018 Fig.3;求解器遥测日志(§11.5)完整 |

> **codex §3 结论**:
> - §3‑1 resolved:数值断言统一 `rel=0.01, abs=5e-4`
> - §3‑2 resolved:M2 改为 "仅加法式修改,BB84 零回归"
> - §3‑3 resolved:M3 改为 "≥ 解析 − 1e-4"
> - §3‑4 resolved:M1 覆盖率改为 core≥95% / wlc≥75% / overall≥85%

---

## 6. 测试规范

**测试目录与源码一一对齐**:

```
tests/
├── conftest.py                        # 共享 fixtures(random_density, etc.)
├── test_core/
│   ├── test_hilbert.py                # 见 §4.1 测试列表
│   ├── test_operators.py              # 见 §4.2
│   └── test_entropy.py                # 见 §4.3
├── test_protocol/
│   ├── test_base.py                   # 见 §4.4
│   └── test_pm_to_eb_equivalence.py   # Ferenczi-Lütkenhaus 2012 数值验证
├── test_protocols/
│   ├── test_bb84.py                   # 见 §4.5
│   ├── test_sixstate.py
│   ├── test_mdi.py
│   └── test_tfqkd.py
├── test_numerics/
│   ├── test_wlc_bb84.py               # M1 核心验收,见 §4.6 完整测试代码
│   ├── test_wlc_sixstate.py
│   ├── test_wlc_mdi.py
│   ├── test_facial.py                 # 见 §4.7
│   └── test_decoy_bb84.py             # 见 §4.8
├── test_analytic/
│   └── test_shor_preskill_properties.py
└── test_integration/
    └── test_reproduce_wlc_2018_fig3.py  # Phase 0 总验收
```

**测试等级**:
- **unit**:默认,每次 commit 跑,预期 < 30 秒
- **slow**:用 `@pytest.mark.slow` 标记 SDP 耗时测试,预期 < 5 分钟,CI 跑
- **research**:用 `@pytest.mark.research` 标记需要完整距离扫描等长测试,预期 < 30 分钟,手动触发

`pyproject.toml` 配置:
```toml
[tool.pytest.ini_options]
addopts = "-ra --strict-markers"
markers = [
    "slow: SDP 单次 > 10s 的测试",
    "research: 研究级别耗时测试,手动触发",
]
```

**TDD 强制**:
- 每个 Milestone 的第一个 commit 必须只包含测试文件 + `NotImplementedError` 的函数骨架
- Reviewer 看 commit 时序,测试落后实现的 PR 驳回

---

## 7. 旧代码处置

### 7.1 操作脚本(v3,吸收 codex §4)

v3 修订点:
1. **硬前置步骤**:先把仓库 rsync 到**无空格**新路径 `$HOME/Desktop/ai4qkd/AI4QKD/`
2. 归档遍历覆盖 dotfile(`shopt -s dotglob nullglob` 让 `*` 自然匹配 dotfile;循环写 `for item in *;`,**禁止** `* .*` 以免双重遍历 —— v3.1 修订)
3. 分支切换先检测 `git rev-parse --is-inside-work-tree`,再决定 `checkout -b` 或 `git init`
4. 文件移动优先 `git mv -k -- "$item"`,失败兜底 `mv + git add -A`(保留 rename tracking)
5. 所有路径强制 `--` 双短横,避免文件名以 `-` 开头误识 flag
6. 保留 `shellcheck` 静态检查(CI 运行)

脚本位置:`scripts/migrate_legacy.sh`(不再内联在文档里执行),支持 `--dry-run` 干跑。

```bash
#!/usr/bin/env bash
# scripts/migrate_legacy.sh — pre-refactor legacy archival (v3.1)
set -Eeuo pipefail
# v3.1: 强制 bash(zsh 下 shopt/dotglob 行为不同),避免被 `zsh script.sh` 误跑
[[ -n "${BASH_VERSION:-}" ]] || { echo "This script requires bash (found: ${0##*/})"; exit 1; }
shopt -s dotglob nullglob   # 使 `*` 匹配 dotfile;未匹配时退化为空

DRY_RUN=0
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=1

OLD_ROOT="/Users/tengjun/Desktop/ai4qkd (1)/AI4QKD"
NEW_ROOT="${HOME}/Desktop/ai4qkd/AI4QKD"

run() {
  if [[ "$DRY_RUN" == "1" ]]; then
    printf 'DRY: %s\n' "$*"
  else
    "$@"
  fi
}

# ------------------------------------------------------------
# Step 0 — relocate to space-free path if needed (codex §4-4)
# ------------------------------------------------------------
if [[ "$PWD" != "$NEW_ROOT" ]]; then
  run mkdir -p "$(dirname -- "$NEW_ROOT")"
  if [[ ! -d "$NEW_ROOT" ]]; then
    run rsync -a --exclude '.git' -- "$OLD_ROOT/" "$NEW_ROOT/"
  fi
  run cd "$NEW_ROOT"
fi

# ------------------------------------------------------------
# Step 1 — insurance snapshot branch (codex §4-2)
# ------------------------------------------------------------
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  # 已是 git 仓库:把未提交变更一次性 commit,再切分支
  run git add -A
  run git commit -m "pre-refactor snapshot" --allow-empty
  run git checkout -b archive/pre-refactor-snapshot || true
else
  run git init
  run git add -A
  run git commit -m "pre-refactor snapshot" --allow-empty
  run git checkout -b archive/pre-refactor-snapshot
fi

# ------------------------------------------------------------
# Step 2 — return to main trunk
# ------------------------------------------------------------
run git checkout -B main

# ------------------------------------------------------------
# Step 3 — archive legacy tree (dotfile-inclusive, codex §4-1/4-3)
# ------------------------------------------------------------
run mkdir -p archive/legacy-v1
# v3.1:dotglob 已让 `*` 匹配 dotfile,**不能** 再写 `* .*` 否则会双重遍历
for item in *; do
  case "$item" in
    archive | docs | scripts | .git | .gitignore | .pytest_cache | \
      venv | .venv | .claude | .mypy_cache | .ruff_cache | .DS_Store) continue ;;
  esac
  if [[ "$DRY_RUN" == "1" ]]; then
    printf 'DRY: git mv -k -- %q archive/legacy-v1/\n' "$item"
  else
    git mv -k -- "$item" archive/legacy-v1/ 2>/dev/null || {
      mv -- "$item" archive/legacy-v1/
      git add -A
    }
  fi
done

# ------------------------------------------------------------
# Step 4 — archival README
# ------------------------------------------------------------
if [[ "$DRY_RUN" != "1" ]]; then
  cat > archive/legacy-v1/README_ARCHIVE.md <<'EOF'
# Legacy v1 (2025-Q1, DEPRECATED)

本目录保留 AI4QKD v1 全部代码,仅作历史记录。**不要基于此开发**。

废弃原因:
1. simulator/quantum_simulator.py:29-67 不读取协议图,对任意协议返回固定数值
2. ai_agent/enhanced_agent.py:108 的适应度函数是常数
3. formal_verification/ 与 security_evaluator/ 是空目录
4. devlog/story_update.md 中 "78.6% 提升" 数字在代码里无来源

详见项目根目录 docs/REFACTORING_PLAN.md §1.1。

新版本在项目根目录 qkdx/。
EOF
fi

echo "[ok] legacy archived to $NEW_ROOT/archive/legacy-v1/"
```

**CI 守护**:`.github/workflows/ci.yml` 里加 `- run: shellcheck scripts/*.sh`。

> **codex §4 结论**:
> - §4‑1 resolved **(v3.1 修订)**:`shopt -s dotglob` 已让 `*` 匹配 dotfile,循环改为 `for item in *;` 避免双重遍历
> - §4‑2 resolved:先 `git rev-parse --is-inside-work-tree` 再决定 init/checkout
> - §4‑3 resolved:`git mv -k --` + `mv --` 兜底保留索引
> - §4‑4 resolved:硬前置 `rsync` 到 `$HOME/Desktop/ai4qkd/AI4QKD`
> - v3.1‑§4 resolved:脚本头部加 `[[ -n "${BASH_VERSION:-}" ]] || exit 1` 防 zsh 误跑

### 7.2 可迁移内容(严格白名单)

仅以下三项可进入新仓库 `docs/references/`:

1. `legacy-v1/research_plan_tf_qkd.md` 的文献综述部分(**逐条核对引用**后)
2. `legacy-v1/requirements.txt` 中 networkx/matplotlib 版本号
3. `legacy-v1/experiment_tf_qkd.py` 中的 TF-QKD 物理参数经验范围(仅作 notebook 参数参考)

**其他一律不迁移**。尤其禁止:`protocol_description.md`、`formal_security_proof.md`、任何 `.json`、任何 PDF 报告。

---

## 8. 风险登记

| # | 风险 | 影响 | 概率 | 缓解 |
|---|------|------|------|------|
| R1 | WLC SDP 在 QBER=0 数值不稳定 | M1 延后 1 周 | 高 | §4.7 facial reduction 提前实现;测试用 qber=1e-6 |
| R2 | MOSEK 学术许可申请失败 | 精度降级到 CLARABEL | 中 | 立即申请;fallback 经验证精度仍在 0.5% 内 |
| R3 | TF-QKD 的 MS-EB 编码不自然 | M4B 失败 | 中 | 预先阅读 Ma-Zeng-Zhou 2018;备选方案:M4B 改为 decoy finite-key |
| R4 | 实现者被 AI 诱惑提前引入 DRL | 重蹈 v1 覆辙 | 中 | §2 明文禁止;pyproject.toml 依赖列表锁定;Code Review 红线 |
| R5 | 12–16 周估算仍可能乐观 | 延期 | 高 | 接受延期,**不降低验收标准** |
| R6 | CVXPY `quantum_rel_entr` 在复数上实现不全 | M1 核心受阻 | 低 | 预先在最小示例上测试;必要时自己实现(Gauss-Legendre 求积) |
| R7 | 单人开发风险 | 整体进度 | 中 | 每周一次 codex review;关键 PR 发送给有 QKD 背景的外部 reviewer |

---

## 9. 开发规范(红线)

1. **TDD 强制**:测试文件 commit 先于实现文件 commit。Reviewer 看 commit 时序。
2. **零魔法数**:密钥率公式中任何常数必须有论文引用在同行注释中。例:
   ```python
   f_ec = 1.16  # Cascade EC efficiency, Brassard-Salvail 1993, Cryptologia 13(4)
   ```
3. **CVXPY 建模两层**:
   - `build_sdp(params) -> cp.Problem`:纯构造,有单元测试验证 `.constraints` 结构
   - `solve_and_extract(prob) -> float`:调用求解器,处理异常
4. **数值验收统一**(v3.1 与 §11.4 RTOL_RATE/ABS_RATE 对齐):
   - **主线阈值(所有 MOSEK 路径的 vs-解析 测试)**:`pytest.approx(rel=0.01, abs=5e-4)`,**不放宽**
   - **fallback 特例阈值(CLARABEL/SCS 求解路径)**:`pytest.approx(rel=0.02, abs=1e-3)`,且必须在测试名/注释中显式标注 `@pytest.mark.parametrize("solver", ["CLARABEL"])` 或 `@pytest.mark.fallback_solver`
   - 任何其他阈值必须附 ADR(`docs/adr/NNNN-*.md`)
5. **不得提交二进制产物**:`.gitignore` 排除 `.pkl/.npz/.json/.pdf`。notebook `jupyter nbconvert --clear-output` 后才能 commit。
6. **Commit message 规范**:`M1:/M2:/M3:/M4:/docs:/refactor:/test:` 前缀。
7. **类型标注 strict**:`mypy --strict qkdx/` 零 error。
8. **禁止未经评审引入新依赖**:`pyproject.toml` 的 dependencies 变更走独立 PR。

---

## 10. 决策请求

文档评审通过后,请项目负责人确认:

1. **仓库位置**:继续用 `/Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/` 还是新建无空格路径?**v3 已决策**:新建 `$HOME/Desktop/ai4qkd/AI4QKD/`,`scripts/migrate_legacy.sh` 的 Step 0 会自动 rsync(§7.1)。
2. **MOSEK 许可**:是否立即启动申请?若长时间未下发,Phase 0 以 CLARABEL/SCS 作为 fallback(见 §11.3)。
3. **开工时间**:v3 修订为 **Phase 0 = 12–16 周**,M4B(TF-QKD)可延至 Phase 0.5。
4. **评审节奏**:每完成一个 Milestone 跑一次 `codex exec -s read-only` 评审(命令见 §11.5)。

---

## 11. 运营控制(v3 新增)

codex §9 识别的缺口统一在本节解决。

### 11.1 可复现性 seed 策略

```python
# qkdx/utils/repro.py
from __future__ import annotations
import os
import sys
import numpy as np

DEFAULT_SEED: int = 20260418   # 基准日期,任何 PR 不得为"求好看的结果"修改此常量

def set_repro(seed: int = DEFAULT_SEED) -> None:
    """为 NumPy 的全局与 default_rng 统一设定 seed。

    不变量:
        调用后,`np.random.default_rng(seed)` 与全局 `np.random` 的序列可复现。
        CVXPY/MOSEK 自身的随机性通过各自的 solver 参数控制(若暴露)。

    **注意**(v3.1,codex §11‑5):Python 字典/集合遍历受 `PYTHONHASHSEED` 影响,
    但此环境变量 **必须在解释器启动前** 设置,否则对当前进程无效。本函数**不会**
    试图在运行中改写它,而是做一个 sanity check,并把责任推到启动脚本/CI。
    """
    np.random.seed(seed)

    env_seed = os.environ.get("PYTHONHASHSEED")
    if env_seed != str(seed):
        # 不 raise,只发警告 — 允许本地开发忽略,但 CI 必须配置(见下)
        print(
            f"[repro] WARNING: PYTHONHASHSEED={env_seed!r}, expected {seed!r}. "
            "Set it BEFORE starting python for deterministic hash ordering.",
            file=sys.stderr,
        )
```

**CI / 本地启动脚本**(`scripts/run_tests.sh`):
```bash
#!/usr/bin/env bash
set -Eeuo pipefail
export PYTHONHASHSEED=20260418
export NUMPY_SEED=20260418
exec pytest "$@"
```

CI(`.github/workflows/ci.yml`)将 `PYTHONHASHSEED: "20260418"` 写入 `env:` 顶层,保证所有 step 生效。

测试 fixture(`tests/conftest.py`):
```python
import pytest
import numpy as np
from qkdx.utils.repro import set_repro, DEFAULT_SEED

@pytest.fixture(autouse=True)
def _seed_everything() -> None:
    set_repro(DEFAULT_SEED)

@pytest.fixture
def rng() -> np.random.Generator:
    return np.random.default_rng(DEFAULT_SEED)
```

### 11.2 依赖版本锁定 + runtime guard

**双层约束**(v3.1):`pyproject.toml` 的 `==x.y.*` 是**下限兼容声明**,真正的构建复现由 **lockfile** 强约束。

`pyproject.toml`(摘要,声明式上限):
```toml
[project]
requires-python = ">=3.11,<3.13"
dependencies = [
    "numpy==2.1.*",
    "scipy==1.14.*",
    "cvxpy==1.5.*",
    "mosek==10.2.*",          # 可选,失败时退到 CLARABEL
    "clarabel==0.9.*",
    "scs==3.2.*",
    "structlog==24.*",
]

[dependency-groups]
dev = ["pytest==8.*", "pytest-cov==5.*", "mypy==1.11.*", "ruff==0.6.*"]
```

**强约束 lockfile**:使用 [uv](https://docs.astral.sh/uv/) 生成 `uv.lock`,记录**精确到构建哈希**的版本树。
- 开发者本地:`uv sync --frozen`
- CI:`uv sync --frozen --check`(发现 lock 与 pyproject 不一致即失败)
- 任何依赖变更必须同步更新 `uv.lock` 并走独立 PR(§9.8)

为什么不用 `requirements.txt + pip freeze`:无法追踪哈希、子依赖出现新版本会静默漂移。

runtime guard(`qkdx/__init__.py`):
```python
import cvxpy as cp
if not hasattr(cp, "quantum_rel_entr"):
    raise RuntimeError(
        "CVXPY build lacks `quantum_rel_entr`. "
        "Install cvxpy>=1.5 with the exp-cone atom support."
    )
```

### 11.3 求解器支持矩阵(`docs/SOLVER_SUPPORT.md`)

| 平台 | 首选 | 次选 | 备注 |
|------|------|------|------|
| macOS arm64 | MOSEK 10.2 | CLARABEL | MOSEK 需有效学术许可,否则自动 fallback |
| macOS x86_64 | MOSEK 10.2 | CLARABEL | — |
| Linux x86_64(CI) | MOSEK 10.2 | CLARABEL / SCS | CI 必须跑,MOSEK license secret 注入 |
| Linux arm64 | CLARABEL | SCS | MOSEK arm64 Linux 不一定可用 |

`qkdx/utils/solvers.py`:
```python
from __future__ import annotations
import cvxpy as cp

def has_mosek() -> bool:
    """返回 True 当且仅当 CVXPY 能找到 MOSEK **且** license 有效。"""
    return "MOSEK" in cp.installed_solvers() and _mosek_license_ok()

def _mosek_license_ok() -> bool:
    try:
        import mosek
        mosek.Env().checkoutlicense(mosek.feature.pts)
        return True
    except Exception:
        return False
```

pytest skip 用法见 §4.6 测试开头的 `pytestmark`。

### 11.4 全局精度常量(`qkdx/utils/numerics.py`)

```python
from __future__ import annotations

# 数值属性断言(Hermitian、PSD、迹)
ATOL_HERMITIAN: float = 1e-10
ATOL_PSD: float = 1e-10
ATOL_TRACE: float = 1e-10

# 密钥率对比容忍(与解析基线)
RTOL_RATE: float = 1e-2        # 1% 相对
ABS_RATE: float = 5e-4         # 绝对兜底

# SDP 求解器容忍(MOSEK 内部参数在 §4.6 MOSEK_PARAMS)
SDP_DUALITY_GAP_MAX: float = 1e-4
SDP_STATUS_ACCEPT: frozenset[str] = frozenset({"optimal", "optimal_inaccurate"})
```

任何新断言不得再使用散落的 `1e-12 / 1e-6 / 0.01`,必须引用上述常量或 ADR 解释。

### 11.5 求解器遥测持久化

所有求解调用都经过 `qkdx/utils/logging.py::get_logger(__name__).info("wlc_solve", ...)` 结构化日志,落盘到 `logs/phase0/solver_telemetry.jsonl`(git-ignored)。

周报(`docs/PHASE0_PROGRESS.md`)的 "测试状态" 小节加入:
- 总求解次数
- `optimal` / `optimal_inaccurate` / 失败数
- 平均/p95 迭代次数
- duality_gap 分布

### 11.6 codex 二轮评审命令

```bash
codex exec -s read-only --skip-git-repo-check <<'EOF'
你是资深的密钥率数值优化评审员。请重新审阅 docs/REFACTORING_PLAN.md(v3),
特别关注:
1. §4 API 是否与 §附录 B 伪代码字面一致(wlc_key_rate 签名、GMap、conditional_alice_bob_dim)
2. §4.6 / 附录 B 的 Hermitian 投影 + 通道级正则化是否数学上无偏
3. §11.3 求解器矩阵是否覆盖开发/CI 全平台
给出 Verdict: ✅ Pass | ⚠️ Needs revision | 🔴 Blocker,每项附代码片段。
EOF
```

> **codex §9 结论**:
> - §9‑1 resolved **(v3.1 修订)**:§11.1 `set_repro` + 启动脚本设 `PYTHONHASHSEED` + 运行时 sanity check
> - §9‑2 resolved **(v3.1 修订)**:§11.2 `pyproject.toml` 声明 + `uv.lock` 强约束双层
> - §9‑3 resolved:§11.3 `docs/SOLVER_SUPPORT.md` + `has_mosek()`
> - §9‑4 resolved:§11.4 统一精度常量
> - §9‑5 resolved:§11.5 结构化遥测日志

---

## 附录 A:参考文献(最小集,BibTeX 格式放在 `docs/references/qkd_core.bib`)

- **Winick, Lütkenhaus, Coles** (2018). *Quantum* 2, 77. [arXiv:1710.05511] — **M1 核心**
- **Coles, Metger, Kaur, Berta** (2016). *Nat. Commun.* 7, 11712. — WLC 理论前传
- **George, Lin, Lütkenhaus** (2020). *Phys. Rev. Research* 3, 013274. — M3 数值诱骗
- **Ma, Qi, Zhao, Lo** (2005). *Phys. Rev. A* 72, 012326. — 解析诱骗基线
- **Ma, Razavi** (2012). *Phys. Rev. A* 86, 062319. — MDI-QKD 解析
- **Ferenczi, Lütkenhaus** (2012). *Phys. Rev. A* 85, 052310. — PM→EB 归约
- **Hu, Li** (2022). *arXiv:2208.01780*. — Facial reduction
- **Tomamichel** (2016). *Quantum Information Processing with Finite Resources*. Springer. — smooth entropy
- **Portmann, Renner** (2022). *Rev. Mod. Phys.* 94, 025008. — AC 安全框架
- **Lucamarini, Yuan, Dynes, Shields** (2018). *Nature* 557, 400. — TF-QKD 原论文
- **Ma, Zeng, Zhou** (2018). *Phys. Rev. X* 8, 031043. — Phase-matching QKD

Phase 1 追加:Dupuis-Fawzi-Renner 2020 (EAT)、Metger-Fawzi-Sutter-Renner 2024 (GEAT)、Kamin-Arqand-George-Lütkenhaus-Tan 2025。

---

## 附录 B:WLC SDP 建模伪代码(v3,吸收 codex §2 + §5)

`numerics/wlc.py` 的 `wlc_key_rate` 内部伪代码。相比 v2 的核心变更:
- 使用 `GMap`(§4.6),不再依赖不存在的 `G_map.dim_out_key`
- **通道级去极化正则化**(而非 `+εI` 两侧)
- 显式 Hermitian 投影避免 CVXPY DCPError
- 接受 `optimal_inaccurate`,移除 `max(0, prob.value)` 掩码
- 拼装 Devetak-Winter 终值 `R = p_sift · (H − f_ec·h(qber_Z))`,单位 bit/signal
- 从 nat 基转 bit 基

```python
from qkdx.numerics import facial
from qkdx.core.entropy import binary_entropy
from qkdx.utils.logging import get_logger

logger = get_logger(__name__)

def wlc_key_rate(protocol, observations, *, solver="MOSEK",
                 epsilon_regularization=1e-9, f_ec=1.16,
                 max_iters=1000, verbose=False):
    # --- 0. 观测键严格一致性(v3.1) ----------------------------
    known = set(protocol.observation_keys)
    provided = set(observations.keys())
    missing = known - provided
    if missing:
        raise ValueError(f"missing observation: {sorted(missing)[0]}")
    unknown = provided - known
    if unknown:
        raise ValueError(f"unknown observation: {sorted(unknown)}")

    # --- 1. 构造映射 ---------------------------------------------
    d_rho = protocol.conditional_alice_bob_dim()
    G = _construct_G_map(protocol)                   # GMap(map, dim_key, dim_side)
    # Z pinching 作用在 X = A_key ⊗ B_side 上:A_key 做对角化,B_side 保持恒等
    Z_on_XB = _construct_Z_pinching(G.dim_key, G.dim_side)   # v3.1:双参数

    # --- 2. 变量与基本约束 ---------------------------------------
    rho = cp.Variable((d_rho, d_rho), hermitian=True)
    constraints = [rho >> 0, cp.real(cp.trace(rho)) == 1]

    for key, expected in observations.items():
        if key == "p_sift":
            continue                                 # 标量事后量,不进 SDP
        Γ_k = protocol.observable(key)               # d_rho × d_rho Hermitian
        constraints.append(cp.real(cp.trace(cp.Constant(Γ_k) @ rho)) == float(expected))

    # --- 3. 映射 + Hermitian 投影 + 通道级去极化正则化(v3.1 修复)
    d_out = G.map.dim_out
    tau = np.eye(d_out, dtype=np.complex128) / d_out
    eps = float(epsilon_regularization)

    X_raw = _apply_cvxpy_map(G.map, rho)             # A_key ⊗ B_side
    X_raw = 0.5 * (X_raw + X_raw.H)                  # Hermitian 投影(codex §2-1)
    # 公式(codex v3.1 §2):X_reg = (1-ε)·X_raw + ε·tr(X_raw)·τ
    # 语义:𝒢 为 CPTNI,tr(X_raw) ≠ tr(ρ)=1,必须显式用 cp.trace(X_raw)
    tr_X = cp.real(cp.trace(X_raw))
    X_reg = (1 - eps) * X_raw + eps * tr_X * cp.Constant(tau)

    Y_reg = _apply_cvxpy_map(Z_on_XB, X_reg)         # pinching on A_key,I on B_side
    Y_reg = 0.5 * (Y_reg + Y_reg.H)

    # --- 4. 目标:min D(X_reg || Y_reg),单位 nat ---------------
    objective = cp.Minimize(cp.quantum_rel_entr(X_reg, Y_reg))

    # --- 5. 求解(求解器矩阵见 docs/SOLVER_SUPPORT.md) ----------
    prob = cp.Problem(objective, constraints)
    rho_value: Matrix | None = None
    try:
        if solver == "MOSEK":
            prob.solve(solver=cp.MOSEK, verbose=verbose,
                       mosek_params=MOSEK_PARAMS)    # 见 §4.6
        else:
            prob.solve(solver=solver, verbose=verbose)
        if prob.status in {"optimal", "optimal_inaccurate"}:
            rho_value = rho.value
    except cp.SolverError:
        # QBER=0 等降秩情形:facial reduction 再试一次(v3.1 正确使用 lift)
        reduced_prob, lift = facial.reduce_problem(prob, rho)
        reduced_prob.solve(solver=solver, verbose=verbose)
        prob = reduced_prob
        if prob.status in {"optimal", "optimal_inaccurate"}:
            rho_value = lift()                       # 子空间 → 原空间 ρ

    if prob.status not in {"optimal", "optimal_inaccurate"}:
        raise cp.SolverError(f"WLC solve failed: status={prob.status}")

    # --- 6. nat → bit,拼装 Devetak-Winter(bit/signal,v3.1) ---
    H_key_given_E_bits = float(prob.value) / np.log(2.0)

    qber_Z = float(observations["qber_Z"])
    p_sift = float(observations["p_sift"])           # 必须显式提供
    leak_ec = f_ec * binary_entropy(qber_Z)
    R_per_sift = H_key_given_E_bits - leak_ec
    key_rate_per_signal = p_sift * R_per_sift        # 单位 bit/signal

    # --- 7. 诊断字段 -------------------------------------------
    dual_obj = getattr(prob.solver_stats, "dual_objective", None)
    gap = float("nan") if dual_obj is None else abs(prob.value - dual_obj)

    logger.info("wlc_solve",
                protocol=protocol.name, status=prob.status,
                value_nat=prob.value, h_bits_per_sift=H_key_given_E_bits,
                r_per_sift=R_per_sift, key_rate=key_rate_per_signal,
                leak_ec=leak_ec, p_sift=p_sift,
                iters=getattr(prob.solver_stats, "num_iters", -1),
                solver=solver, eps=eps)

    return WLCResult(
        key_rate=key_rate_per_signal,                # bit/signal,不 clip(codex §5-5)
        primal_status=prob.status,
        h_bits_per_sift=H_key_given_E_bits,
        iterations=getattr(prob.solver_stats, "num_iters", -1),
        duality_gap=gap,
        optimal_rho=rho_value,
        solver=solver,
    )
```

> **codex §5 结论**:
> - §5‑1 resolved:`GMap.dim_key` 取代 `dim_out_key`,`conditional_alice_bob_dim()` 可用
> - §5‑2 resolved:`leak_ec = f_ec·h(qber_Z)`,拼装成 Devetak-Winter 终值
> - §5‑3 resolved:`facial.reduce_problem` 返回 `(reduced_prob, lift)`(见 §4.7 签名调整)
> - §5‑4 resolved:`dual_obj = getattr(solver_stats, "dual_objective", None)`,缺则 NaN
> - §5‑5 resolved:接受 `optimal_inaccurate`,移除 `max(0, ·)` 掩码

---

## 附录 C:Phase 0 进度追踪模板

`docs/PHASE0_PROGRESS.md` 每周五更新:

```markdown
## Week N (YYYY-MM-DD ~ YYYY-MM-DD)

### 完成
- [ ] 任务 1 (具体 commit hash)
- [x] 任务 2

### 阻塞
- 问题描述 + 预期解法

### 下周计划
- ...

### 测试状态
- `pytest tests/test_core/`: N passed, M failed
- `pytest tests/test_numerics/`: N passed
- Coverage: XX%
```

---

**文档结束。请 codex 重点评审:**

1. **§4 的 API 规范是否自洽**(模块间依赖方向、类型一致性、命名冲突)
2. **§4.6 WLC SDP 的实现路径是否可行**(特别是 CVXPY 的 `quantum_rel_entr` 在复数半正定变量上的实际行为)
3. **§5 的 Milestone 验收标准是否过紧或过松**
4. **§7 旧代码处置脚本是否安全**(尤其 `git mv` 的通配符展开)
5. **§附录 B 伪代码中是否有明显的数学错误**(如 `_apply_cvxpy_map` 对 hermitian 变量的处理)
6. **函数签名的 Python 类型标注是否符合 PEP 484/604 最佳实践**
7. **测试用例的 pytest 参数化是否会遇到 collection 错误**

不要仅做字面评审,请给出具体的改进建议(含 diff 或 pseudocode 如必要)。
