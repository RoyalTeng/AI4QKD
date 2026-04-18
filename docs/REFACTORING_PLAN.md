# AI4QKD 项目重构方案(函数级详细版)

**文档状态**:草案 v2(函数级详细化)
**基准日期**:2026-04-18
**作者**:基于 2026-04-17 与 2026-04-18 两轮代码审查
**目标读者**:项目负责人、实现者、codex 评审

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

**代码规模目标**:`qkdx/` 源代码 ≤ 3000 行,`tests/` ≤ 2500 行,测试/源码行数比 ≥ 0.75。

**禁用依赖**:torch、stable-baselines3、qiskit、z3、coq 相关。

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
│   │   ├── decoy.py                # 数值诱骗态
│   │   └── gradient.py             # Frank-Wolfe 求解器
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

Complex = np.complex128
Matrix = NDArray[Complex]                 # 形状约束由 docstring 指定


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
# 标准 qubit 算子
IDENTITY_2 = np.eye(2, dtype=Complex)
SIGMA_X: Matrix = np.array([[0, 1], [1, 0]], dtype=Complex)
SIGMA_Y: Matrix = np.array([[0, -1j], [1j, 0]], dtype=Complex)
SIGMA_Z: Matrix = np.array([[1, 0], [0, -1]], dtype=Complex)
HADAMARD: Matrix = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=Complex)

# Z 基
KET_0: Matrix = ket(0, 2)
KET_1: Matrix = ket(1, 2)
# X 基
KET_PLUS: Matrix = (KET_0 + KET_1) / np.sqrt(2)
KET_MINUS: Matrix = (KET_0 - KET_1) / np.sqrt(2)
# Bell 态
PHI_PLUS: Matrix = (tensor(KET_0, KET_0) + tensor(KET_1, KET_1)) / np.sqrt(2)
```

**测试覆盖**(`tests/test_core/test_hilbert.py`):
- `test_partial_trace_preserves_trace`:随机 8×8 密度矩阵 partial_trace 后迹不变
- `test_partial_trace_bell_state_is_maximally_mixed`:tr_B(|Φ+⟩⟨Φ+|) == I/2
- `test_proj_is_hermitian_psd_rank1`:随机列向量的 proj 满足 rank=1、Hermitian、PSD
- `test_purify_then_trace_roundtrip`:purify(rho) 后 partial_trace 回来 == rho(误差 < 1e-10)
- `test_sigma_operators_anticommute`:σ_x σ_z + σ_z σ_x == 0(2x2 零矩阵)

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
from dataclasses import dataclass, field
from typing import Protocol as _TypingProtocol
import cvxpy as cp

from qkdx.core.hilbert import Matrix
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

    不变量:
        channel.dim_in == prod(sources[i].signal_register_dim)
        channel.dim_out == receiver_dim * classical_outcomes

    数学:
        E: H_{A'_1} ⊗ ... ⊗ H_{A'_n} → H_B ⊗ ℂ[C]
    """
    channel: KrausMap
    receiver_dim: int
    classical_outcomes: int


@dataclass(frozen=True)
class AnnouncementRule:
    """A:公开声明函数。Phase 0 只支持 per-round announcement。

    属性:
        function: 输入 (raw_classical_info: tuple[int, ...]) → public_announcement: int
        sift_keep: 函数返回 True 表示该轮数据保留进入密钥生成,False 丢弃

    备注:
        Phase 0 不支持跨轮联合声明(如 MP-QKD)。Phase 1 再扩展。
    """
    function: callable
    sift_keep: callable


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
        symmetry_group: 可选,协议的对称群名(用于 SDP 约化,Phase 0 M4 引入)

    不变量:
        announcement.function 的输入维度匹配 network 的 classical_outcomes
        key_map.key_party in {src.name for src in sources}

    方法:
        joint_state: 返回所有源方的联合 EB 态 ⊗_i |ψ_i⟩,形状 (prod dims × 1)
        executed_state: 返回协议执行后 A_1 ... A_n ⊗ B ⊗ C 的完整密度矩阵
    """
    name: str
    sources: tuple[SourceParty, ...]
    network: PublicQuantumNetwork
    announcement: AnnouncementRule
    key_map: KeyMap
    symmetry_group: str | None = None

    def joint_state(self) -> Matrix:
        """返回 ⊗_i |ψ_i⟩_{A_i A_i'} 的列向量。"""

    def executed_state(self) -> Matrix:
        """协议执行后,在 Alice 测量前的全局纯化态 ρ_{A_1...A_n B C}。

        步骤:
            1. 从 joint_state 出发
            2. 对每个源方的 A_i' 应用 network.channel
            3. 结果的形状:(prod key_dims · receiver_dim · classical_outcomes, ...)
        """

    def conditional_alice_bob(self) -> Matrix:
        """经过 announcement.sift_keep 筛选后的 ρ_{A_1 B | keep=True}。
        这是 WLC SDP 的输入。
        """
```

**设计说明**:
- `MSEBProtocol` 是**纯数据类**,不包含密钥率计算逻辑。密钥率计算在 `numerics/wlc.py` 中以函数形式实现,接受 `MSEBProtocol` 作为输入。
- `AnnouncementRule` 用 `callable` 而非子类,降低认知负担。
- `symmetry_group` 为字符串(如 `"Z2_XZ_swap"`),具体表示查 `symmetry/groups.py` 的注册表。

**测试覆盖**(`tests/test_protocol/test_base.py`):
- `test_mseb_joint_state_norm_preserved`:`np.linalg.norm(protocol.joint_state()) == 1` (误差 1e-10)
- `test_mseb_executed_state_is_density`:`is_density(executed_state())` 返回 True
- `test_mseb_sources_tuple_immutable`:尝试修改 `sources[0].name` 抛 FrozenInstanceError

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

    示例:
        >>> protocol = build_bb84_protocol(qber=0.05)
        >>> from qkdx.numerics.wlc import wlc_key_rate
        >>> R = wlc_key_rate(protocol)
        >>> from qkdx.analytic.shor_preskill import shor_preskill_rate
        >>> R_analytic = shor_preskill_rate(0.05)
        >>> abs(R - R_analytic) / R_analytic < 0.01  # < 1% 相对误差
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
from dataclasses import dataclass
import numpy as np
import cvxpy as cp

from qkdx.core.hilbert import Matrix
from qkdx.core.operators import KrausMap
from qkdx.protocol.base import MSEBProtocol


@dataclass
class WLCResult:
    """WLC SDP 求解结果。

    属性:
        key_rate: 密钥率下界(渐进)
        primal_status: cvxpy 状态字符串,"optimal" 等
        iterations: 求解器迭代次数
        duality_gap: |primal - dual|,用于诊断
        optimal_rho: 达到下界的最优 ρ(可选,用于诊断)
    """
    key_rate: float
    primal_status: str
    iterations: int
    duality_gap: float
    optimal_rho: Matrix | None = None


def wlc_key_rate(
    protocol: MSEBProtocol,
    observations: dict[str, float],
    *,
    solver: str = "MOSEK",
    epsilon_regularization: float = 1e-10,
    max_iters: int = 1000,
    verbose: bool = False,
) -> WLCResult:
    """WLC SDP 求解 MS-EB 协议在给定观测约束下的密钥率下界。

    参数:
        protocol: MS-EB 协议对象
        observations: 实验测量的期望值,键必须对应 protocol 已声明的可观测量
            示例:{"qber_Z": 0.02, "qber_X": 0.02, "gain": 0.72}
        solver: CVXPY 支持的 SDP 求解器,推荐 MOSEK,fallback CLARABEL
        epsilon_regularization: ρ → ρ + ε·I 的正则化,避免 matrix log 奇异
        max_iters: 求解器迭代上限
        verbose: 是否打印求解器日志

    返回:
        WLCResult

    异常:
        ValueError: observations 缺键或协议定义不兼容
        cvxpy.SolverError: 求解失败(primal_status != "optimal")

    实现步骤(详见 §附录 B 伪代码):
        1. 从 protocol 构造 𝒢 映射(作为 CVXPY 可处理的线性算子)
        2. 从 protocol 构造 𝒵 pinching 信道
        3. 声明变量 ρ,形状 = protocol 的 conditional_alice_bob 的维度
        4. 构造约束:观测等式 + 半正定 + 迹 1
        5. 目标函数:D(𝒢(ρ) ‖ 𝒵(𝒢(ρ))),用 CVXPY 的 cp.quantum_rel_entr
        6. 最小化,返回结果
    """


def _build_observable_operators(
    protocol: MSEBProtocol,
    observation_keys: list[str],
) -> dict[str, Matrix]:
    """为每个观测名构造对应的可观测算子 Γ_k。

    Phase 0 支持的键:
        "qber_Z":Z 基 QBER 对应的算子
        "qber_X":X 基 QBER 对应的算子
        "gain":总增益算子
        "gain_Z":Z 基增益
        "gain_X":X 基增益

    扩展需修改此函数。
    """


def _construct_G_map(protocol: MSEBProtocol) -> KrausMap:
    """构造 WLC 公式中的 𝒢 映射。

    𝒢 = (V_key ⊗ M_Bob) ∘ Alice_measurement

    其中:
        Alice_measurement:把 A_A' 的 Alice 基与密钥寄存器分开
        M_Bob:Bob 的 POVM 对应的 Naimark 拓展(如果需要保留 Bob 的侧信息)
        V_key:把 Alice 的密钥比特抽取到独立寄存器 A_key
    """


def _construct_Z_pinching(dim_key: int) -> KrausMap:
    """𝒵 是对密钥寄存器的 pinching(computational basis 对角化)。

    𝒵(σ) = Σ_x |x⟩⟨x| · σ · |x⟩⟨x|

    作为 Kraus 映射:K_x = |x⟩⟨x|(dim=dim_key 个 Kraus)
    """
```

**关键实现细节**(CVXPY 的坑):

1. `cp.quantum_rel_entr(P, Q)` 对 `Q` 秩不满会抛错,必须先做 `Q = Q + ε·I`。
2. CVXPY 不直接支持"复数厄米半正定变量",需要 `X = cp.Variable((d, d), hermitian=True)` 并配合 `X >> 0`。
3. 张量积约束必须展开为标量方程,用 `cp.trace(Γ_k @ ρ) == γ_k`。
4. MOSEK 求解复 SDP 时必须指定 `solver=cp.MOSEK, verbose=verbose`,否则默认 CLARABEL。

**测试覆盖**(`tests/test_numerics/test_wlc_bb84.py` — 这是 M1 验收的核心):

```python
import pytest
import numpy as np
from qkdx.protocols.bb84 import build_bb84_protocol
from qkdx.analytic.shor_preskill import shor_preskill_rate
from qkdx.numerics.wlc import wlc_key_rate


@pytest.mark.parametrize("qber", [0.00, 0.01, 0.02, 0.05, 0.08, 0.10])
def test_wlc_bb84_matches_shor_preskill(qber: float) -> None:
    """WLC SDP 结果与 Shor-Preskill 解析值误差 < 1%。"""
    protocol = build_bb84_protocol(qber=qber)
    R_numerical = wlc_key_rate(
        protocol,
        observations={"qber_Z": qber, "qber_X": qber, "gain": 1.0},
    ).key_rate
    R_analytic = shor_preskill_rate(qber)
    assert R_numerical == pytest.approx(R_analytic, rel=0.01)


def test_wlc_bb84_above_threshold_gives_zero() -> None:
    """QBER > 11% 时密钥率应为 0(或负后被 clip)。"""
    protocol = build_bb84_protocol(qber=0.13)
    R = wlc_key_rate(protocol, observations={"qber_Z": 0.13, "qber_X": 0.13, "gain": 1.0}).key_rate
    assert R <= 1e-6


def test_wlc_bb84_qber_zero_gives_unity() -> None:
    """无噪声时 R == 1。"""
    protocol = build_bb84_protocol(qber=1e-6)
    R = wlc_key_rate(protocol, observations={"qber_Z": 1e-6, "qber_X": 1e-6, "gain": 1.0}).key_rate
    assert R == pytest.approx(1.0, abs=0.01)


def test_wlc_solver_status_is_optimal() -> None:
    """常规 QBER=0.05 的问题应能被求解器接受。"""
    protocol = build_bb84_protocol(qber=0.05)
    result = wlc_key_rate(protocol, observations={"qber_Z": 0.05, "qber_X": 0.05, "gain": 1.0})
    assert result.primal_status == "optimal"
    assert result.duality_gap < 1e-4


def test_wlc_fallback_to_clarabel() -> None:
    """MOSEK 不可用时 fallback 到 CLARABEL 精度仍在验收范围。"""
    protocol = build_bb84_protocol(qber=0.05)
    result = wlc_key_rate(
        protocol, observations={"qber_Z": 0.05, "qber_X": 0.05, "gain": 1.0},
        solver="CLARABEL",
    )
    R_analytic = shor_preskill_rate(0.05)
    assert result.key_rate == pytest.approx(R_analytic, rel=0.02)  # CLARABEL 稍松


def test_wlc_observable_key_missing_raises() -> None:
    """观测字典缺键时给出清晰错误。"""
    protocol = build_bb84_protocol(qber=0.05)
    with pytest.raises(ValueError, match="missing observation: qber_X"):
        wlc_key_rate(protocol, observations={"qber_Z": 0.05, "gain": 1.0})
```

---

### 4.7 `qkdx/numerics/facial.py`

**职责**:facial reduction,处理 SDP 的严格可行性失败(Hu-Li 2022)。

```python
from __future__ import annotations
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
) -> cp.Problem:
    """对原问题做 facial reduction,返回降维后的等价问题。"""
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

| Milestone | 交付模块 | 硬验收标准 |
|-----------|---------|-----------|
| **M1**(2 周) | `core/hilbert.py`、`core/operators.py`、`core/entropy.py`、`protocol/base.py`、`protocols/bb84.py`、`analytic/shor_preskill.py`、`numerics/wlc.py`(最小版) | `test_wlc_bb84_matches_shor_preskill` 六个 qber 点全部通过(rel=0.01);`pytest --cov=qkdx.core --cov=qkdx.numerics.wlc` ≥ 90% |
| **M2**(1.5 周) | `protocols/sixstate.py`、`protocols/mdi.py`、`analytic/six_state.py`、`analytic/gllp.py` | 六态数值 vs 解析误差 < 1%;MDI-QKD 数值 vs Ma-Razavi 2012 误差 < 1%;`numerics/wlc.py` 未修改 |
| **M3**(2 周) | `numerics/decoy.py`、`numerics/facial.py` | 单诱骗态数值 vs 解析误差 < 1%;两强度 decoy 数值严格优于解析;距离扫描曲线与 Lo-Ma-Chen 2005 Fig.3 视觉一致 |
| **M4**(1.5 周) | `symmetry/groups.py`、`symmetry/twirling.py`、`protocols/tfqkd.py` | Clifford 约化把 BB84 SDP 变量降到 2×2,结果误差 < 1%;TF-QKD 的 R(η) 在 log-log 图上斜率 = 0.5 ± 0.05 |
| **Phase 0 总验收** | 全部 | 所有 pytest 绿;`pytest --cov=qkdx` ≥ 80%;`docs/PHASE0_REPORT.md` 8–12 页 memo 完成;复现 Winick 2018 Fig.3 |

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

### 7.1 操作脚本

```bash
cd "/Users/tengjun/Desktop/ai4qkd (1)/AI4QKD"

# 1. 保险快照
git checkout -b archive/pre-refactor-snapshot 2>/dev/null || { git init && git add -A && git commit -m "pre-refactor snapshot" --allow-empty; }

# 2. 切回主干
git checkout -B main

# 3. 归档
mkdir -p archive/legacy-v1
for item in *; do
  case "$item" in
    archive|docs|.git|.gitignore|.pytest_cache|venv) ;;
    *) git mv "$item" archive/legacy-v1/ 2>/dev/null || mv "$item" archive/legacy-v1/ ;;
  esac
done

# 4. 归档 README
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
```

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
| R3 | TF-QKD 的 MS-EB 编码不自然 | M4 失败 | 中 | 预先阅读 Ma-Zeng-Zhou 2018;备选方案:M4 改为 decoy finite-key |
| R4 | 实现者被 AI 诱惑提前引入 DRL | 重蹈 v1 覆辙 | 中 | §2 明文禁止;pyproject.toml 依赖列表锁定;Code Review 红线 |
| R5 | 6-8 周估算乐观 | 延期 | 高 | 接受延期,**不降低验收标准** |
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
4. **数值验收统一**:所有"vs 解析"测试用 `pytest.approx(rel=0.01)`,不放宽。
5. **不得提交二进制产物**:`.gitignore` 排除 `.pkl/.npz/.json/.pdf`。notebook `jupyter nbconvert --clear-output` 后才能 commit。
6. **Commit message 规范**:`M1:/M2:/M3:/M4:/docs:/refactor:/test:` 前缀。
7. **类型标注 strict**:`mypy --strict qkdx/` 零 error。
8. **禁止未经评审引入新依赖**:`pyproject.toml` 的 dependencies 变更走独立 PR。

---

## 10. 决策请求

文档评审通过后,请项目负责人确认:

1. **仓库位置**:继续用 `/Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/` 还是新建无空格路径?**推荐后者**,路径空格会在 shell 脚本和 Python 包导入里持续制造问题。
2. **MOSEK 许可**:是否立即启动申请?
3. **开工时间**:6–8 周工时是否可用?
4. **评审节奏**:是否每完成一个 Milestone 就跑一次 `codex review`?

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

## 附录 B:WLC SDP 建模伪代码

`numerics/wlc.py` 的 `wlc_key_rate` 函数内部伪代码,供实现参考:

```
function wlc_key_rate(protocol, observations):
    # 1. 从 protocol 构造相关算子
    rho_AB_input_dim = protocol.conditional_alice_bob_dim()
    G_map = _construct_G_map(protocol)                         # KrausMap A_1 A_2 → A_key B'
    Z_pinching = _construct_Z_pinching(G_map.dim_out_key)      # pinching on A_key

    # 2. 声明 CVXPY 变量
    rho = cp.Variable((rho_AB_input_dim, rho_AB_input_dim), hermitian=True)

    # 3. 构造约束
    constraints = [rho >> 0, cp.trace(rho) == 1]

    observable_ops = _build_observable_operators(protocol, list(observations.keys()))
    for key, expected_value in observations.items():
        Γ_k = observable_ops[key]
        constraints.append(cp.real(cp.trace(Γ_k @ rho)) == expected_value)

    # 4. 构造目标函数 D(𝒢(ρ) ‖ 𝒵(𝒢(ρ)))
    G_rho = _apply_cvxpy_map(G_map, rho)                       # 线性算子作用
    Z_G_rho = _apply_cvxpy_map(Z_pinching, G_rho)              # pinching 后

    # 正则化避免秩亏导致 log 奇异
    G_rho_reg = G_rho + epsilon_regularization * cp.Constant(np.eye(G_map.dim_out))
    Z_G_rho_reg = Z_G_rho + epsilon_regularization * cp.Constant(np.eye(G_map.dim_out))

    objective = cp.Minimize(cp.quantum_rel_entr(G_rho_reg, Z_G_rho_reg))

    # 5. 求解
    prob = cp.Problem(objective, constraints)
    prob.solve(solver=solver, max_iters=max_iters, verbose=verbose)

    # 6. 包装结果
    if prob.status != "optimal":
        # 尝试 facial reduction
        reduced = facial.reduce_problem(prob, rho)
        if reduced is not None:
            prob = reduced
            prob.solve(solver=solver, max_iters=max_iters)

    return WLCResult(
        key_rate=max(0.0, prob.value),
        primal_status=prob.status,
        iterations=prob.solver_stats.num_iters,
        duality_gap=abs(prob.value - prob.solver_stats.extra_stats.get("dual_obj", prob.value)),
        optimal_rho=rho.value if prob.status == "optimal" else None,
    )
```

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
