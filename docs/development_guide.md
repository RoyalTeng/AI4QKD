# 开发指南

> 本文档为参与AI4QKD项目协作的开发者提供开发规范、流程与建议，旨在提高协作效率与代码质量。

---

## 一、目录结构与开发规范

### 1. 目录结构说明

本项目的目录结构遵循模块化原则，核心模块均有独立的目录。在开发前，请务必熟悉 `README.md` 中定义的完整目录结构。

- **`config/`**：存放全局配置、协议模板、AI智能体超参数。
- **`qcgf_dsl/`**：协议图的DSL定义、解析、编译与可视化。
- **`simulator/`**：量子物理过程仿真器，包含信道、噪声、测量等模型。
- **`security_evaluator/`**：安全评估模块，负责计算密钥率、熵等指标。
- **`ai_agent/`**：AI智能体，包含DRL、EA等优化算法。
- **`formal_verification/`**：形式化验证模块，用于协议的理论安全性证明。
- **`tests/`**：单元测试与集成测试，所有核心功能都应有对应测试。
- **`docs/`**：项目文档，包括架构、API、用户指南与本开发指南。
- **`devlog/`**：开发日志，用于记录日常开发与决策。

### 2. 代码规范

- **格式化**：统一使用 `black` 进行代码格式化。
- **检查**：使用 `flake8` 进行代码风格检查，`mypy` 进行类型检查。
- **命名**：类名使用 `CamelCase`，函数与变量使用 `snake_case`。
- **注释**：所有公开的类、方法、函数都应有标准的Docstring（Google风格），说明其功能、参数、返回值。

---

## 二、如何新增模块

### 1. 新增一个QKD协议

所有QKD协议都以 `ProtocolGraph` 的形式存在。要新增一个协议：

1. **在 `config/qkd_protocols.py` 中定义**：
   - 创建一个新函数，如 `create_e91_protocol()`。
   - 在函数内部，实例化一个 `ProtocolGraph` 对象。
   - 调用 `add_node()` 和 `add_edge()` 方法构建协议图的拓扑结构。
   - 返回 `ProtocolGraph` 实例。
2. **在 `examples/` 中创建示例**：
   - 新建一个 `e91_example.py` 文件。
   - 从 `config.qkd_protocols` 导入你的协议创建函数。
   - 编写调用仿真、评估流程的代码，并打印结果。

### 2. 新增一个AI优化策略

1. **选择算法类型**：确定是基于DRL还是EA。
2. **创建算法文件**：
   - 如果是DRL，在 `ai_agent/drl/` 下新建文件，如 `a2c_agent.py`。
   - 如果是EA，在 `ai_agent/ea/` 下新建文件，如 `cma_es_algorithm.py`。
3. **实现核心类**：
   - 定义一个Agent或Algorithm类，包含初始化、训练/演化、选择动作/生成新一代等核心方法。
4. **集成到 `HybridAgent`**：
   - 在 `ai_agent/hybrid_agent.py` 中导入你的新策略。
   - 在 `HybridAgent` 的初始化或配置中，添加调用新策略的逻辑分支。

---

## 三、测试与TDD原则

### 1. 编写测试（pytest）

- 所有测试文件都放在 `tests/` 目录下，并以 `test_` 开头。
- 每个模块都应有对应的测试文件，如 `simulator/` -> `tests/test_simulator.py`。
- 测试函数也以 `test_` 开头，函数名应清晰描述测试场景。
- 使用 `pytest.fixture` 来创建可复用的测试对象（如 `ProtocolGraph` 实例）。
- 大量使用 `assert` 来验证函数返回值、对象状态是否符合预期。

```python
# tests/test_qcgf_dsl.py 示例
import pytest
from qcgf_dsl.protocol_graph import ProtocolGraph

@pytest.fixture
def basic_bb84_graph():
    """返回一个基础的BB84协议图 fixture"""
    graph = ProtocolGraph(name="TestBB84")
    graph.add_node(node_type="QSP", ...)
    graph.add_node(node_type="QC", ...)
    graph.add_edge(...)
    return graph

def test_add_node(basic_bb84_graph):
    """测试节点添加功能"""
    initial_count = basic_bb84_graph.get_node_count()
    basic_bb84_graph.add_node(node_type="QM", ...)
    assert basic_bb84_graph.get_node_count() == initial_count + 1
```

### 2. 测试驱动开发（TDD）重构

对于 `simulator` 等复杂模块，我们严格遵循TDD原则：

1. **先写测试**：在修改或新增任何逻辑前，先在 `tests/` 中编写一个或多个会失败的测试用例。
2. **再写实现**：回到模块代码中，编写最少的代码让测试用例通过。
3. **后重构**：在测试通过后，重构代码以提高可读性、性能，并确保所有测试仍然通过。

**示例：重构 `channel_model.py`**
- **步骤1**：在 `tests/test_simulator.py` 中添加 `test_channel_with_polarization_noise()`，断言加入噪声后量子态的变化。此测试初始会失败。
- **步骤2**：在 `channel_model.py` 中实现噪声施加逻辑，直到测试通过。
- **步骤3**：优化噪声计算代码，并再次运行所有测试，确保无功能退化。

---

## 四、开发建议与规则约束

### 1. `.cursor-rules.json` 使用说明

本项目配置了 `.cursor-rules.json`，为AI辅助编程提供上下文和规则约束，以保证生成代码的风格统一和质量。

- **触发条件（when/trigger）**：定义了在编辑特定文件或模块时触发的规则。例如，编辑 `simulator/` 目录下的文件会触发"仿真器模块"规则。
- **指令（instructions）**：是一系列对AI的提示，指导其如何生成代码。例如，要求其"推荐使用 Qiskit Aer"、"补全物理公式注释"等。

**如何使用与维护？**
- **自动触发**：当你在匹配的文件中请求AI生成或修改代码时，这些规则会自动生效。
- **新增规则**：如果你发现某个模块的开发有固定的模式，可以向该文件添加新的规则，以提高AI的辅助效率。例如，为 `formal_verification/` 模块添加Z3求解器的使用建议。

### 2. 文档与日志维护

- **API文档**：修改或新增任何公开接口后，请同步更新 `docs/api_reference.md`。
- **架构文档**：若有重大模块重构或新增，请更新 `docs/architecture.md`。
- **开发日志**：每次完成一个有意义的开发任务后，请在 `devlog/` 目录下以日期（如 `YYYY-MM-DD.md`）为文件名创建日志文件，简要记录：
  - 本次更新的主要内容（如：新增了XXX功能，修复了XXX bug）。
  - 设计决策的简要理由。
  -遇到的问题与解决方案。

此举有助于团队成员了解项目进展和历史决策，方便追踪与回顾。 