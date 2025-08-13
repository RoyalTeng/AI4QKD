# CLAUDE.md

此文件为Claude Code (claude.ai/code) 在此代码库中工作时提供指导。

## 项目概述

AI4QKD是一个使用人工智能自动设计和优化量子密钥分发（QKD）协议的研究系统。该系统结合了量子计算仿真、密码学安全分析和机器学习技术，以发现具有更好性能的新颖QKD协议。

## 开发命令

### 环境设置
```bash
# 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装依赖包
pip install -r requirements.txt

# 以开发模式安装
pip install -e .
```

### 测试
```bash
# 运行所有测试
pytest tests/

# 运行带覆盖率的测试
pytest --cov=. tests/

# 运行特定测试模块
pytest tests/test_simulator.py
pytest tests/test_security_evaluator.py
pytest tests/test_ai_agent.py

# 运行单个测试
pytest tests/test_simulator.py::test_bb84_simulation
```

### 代码质量
```bash
# 格式化代码
black .

# 代码检查
flake8 .

# 类型检查
mypy .
```

### 运行系统
```bash
# 主训练程序
python main.py

# 使用自定义运行ID
python main.py --run_id my_experiment

# 从之前的运行中恢复
python main.py --resume_id previous_run_id

# 从特定回合恢复
python main.py --resume_id previous_run_id --episode 50

# 运行示例
python examples/bb84_example.py
python examples/example_security_evaluator.py
```

## 架构概览

系统采用5层模块化架构：

### 1. AI智能体层 (`ai_agent/`)
- **目的**：深度强化学习和演化算法优化
- **关键组件**：
  - `hybrid_agent.py`：结合DRL和EA的主要AI智能体
  - `drl/`：深度强化学习智能体（PPO、SAC）
  - `ea/`：演化算法（遗传算法、演化策略）
  - `graph_encoder/`：用于协议表示的图神经网络
  - `environment.py`：协议设计的强化学习环境

### 2. 协议表示层 (`qcgf_dsl/`)
- **目的**：将QKD协议表示为图的领域特定语言
- **关键组件**：
  - `protocol_graph.py`：核心协议图数据结构
  - `node_types.py`：量子/经典节点类型定义（QSP、QC、QM、CLO）
  - `edge_types.py`：连接类型定义
  - `parser.py`：协议描述的DSL解析器
  - `visualizer.py`：协议可视化工具

### 3. 量子仿真层 (`simulator/`)
- **目的**：量子协议的物理层仿真
- **关键组件**：
  - `quantum_simulator.py`：主仿真框架
  - `real_quantum_simulator.py`：高保真物理仿真器
  - `channel_model.py`：量子信道建模
  - `noise_model.py`：噪声和退相干模型
  - `measurement.py`：量子测量仿真
  - `qiskit_interface.py`：与Qiskit的集成

### 4. 安全评估层 (`security_evaluator/`)
- **目的**：信息论安全评估
- **关键组件**：
  - `key_rate_calculator.py`：安全密钥率计算
  - `entropy_estimator.py`：量子熵估计
  - `finite_key_analysis.py`：有限密钥制度安全分析
  - `ac_framework.py`：抽象密码学框架
  - `composable_security.py`：可组合安全分析

### 5. 形式化验证层 (`formal_verification/`)
- **目的**：安全属性的数学证明和验证
- **关键组件**：
  - `protocol_verifier.py`：协议正确性验证
  - `security_proof.py`：自动化安全证明
  - `model_checker.py`：协议属性的模型检查

## 关键开发原则

### 测试驱动开发（TDD）
- **关键**：所有`simulator/`模块的更改必须遵循TDD - 先写测试再实现
- 递增式构建测试：单光子 → 单信道 → 单测量 → 完整协议
- 绝不在没有完整测试覆盖的情况下提交`simulate_protocol_graph`

### 节点类型和协议结构
- **标准节点类型**：QSP（量子态准备）、QC（量子信道）、QM（量子测量）、CLO（经典操作）
- **命名约定**：节点ID应反映其类型（如`qsp_1`、`qc_alice_bob`）
- **方归属**：每个节点都应有`party`属性（Alice、Bob、Eve）

### 安全分析焦点
- **有限密钥分析**：始终使用有限密钥安全分析而非渐近极限
- **可组合安全**：实现可组合安全框架以获得现实密钥率
- **熵计算**：使用平滑最小熵H_min^ε(X|E)进行安全证明

## 配置管理

### 主要配置
- **全局设置**：`config/settings.py` - 系统参数和超参数
- **协议定义**：`config/qkd_protocols.py` - 预定义协议配置
- **AI智能体配置**：`config/ai_agent_config.py` - AI特定设置

### 训练配置
- **超参数**：NUM_EPISODES、MAX_STEPS_PER_EPISODE、学习率
- **日志记录**：带有动作日志、训练指标的综合日志系统
- **检查点**：按回合间隔自动保存模型

## 重要数据结构

### 协议图格式
```python
protocol_graph = {
    "nodes": [
        {
            "id": "qsp_1",
            "type": "QSP",
            "params": {"state": "|0⟩", "party": "Alice"},
            "position": (x, y)
        }
    ],
    "edges": [
        {
            "source": "qsp_1",
            "target": "qc_1",
            "type": "quantum"
        }
    ]
}
```

### 动作空间
- **add_node**：添加新的协议节点
- **remove_node**：删除现有节点
- **add_edge**：连接节点
- **modify_params**：修改节点参数

## 依赖库

### 核心库
- **量子计算**：qiskit、qutip、cirq
- **机器学习**：torch、torch-geometric、transformers、stable-baselines3
- **科学计算**：numpy、scipy、pandas
- **密码学**：cryptography、pycryptodome
- **验证**：z3-solver、sympy

### 开发工具
- **测试**：pytest、pytest-cov、pytest-mock
- **质量**：black、flake8、mypy
- **文档**：sphinx、jupyter

## 输出结构

### 训练结果
- **日志**：`logs/ai_training/[run_id]/` - 详细训练日志
- **结果**：`results/[run_id]/` - 模型检查点和性能数据
- **回合**：`results/[run_id]/episodes/` - 每回合保存
- **最佳模型**：`results/[run_id]/best/` - 最佳性能模型

### 示例使用
`examples/`目录包含BB84、MDI-QKD和自定义协议的完整使用示例。

## 模块间依赖关系

系统需要层间仔细协调：
1. **AI智能体**通过**QCGF DSL**生成协议图
2. **仿真器**执行协议以生成测量统计
3. **安全评估器**使用有限密钥分析计算密钥率
4. **形式化验证**数学证明安全属性
5. **训练日志器**捕获所有结果用于分析和恢复

## 开发工作流程

1. **设置**：安装依赖并激活虚拟环境
2. **测试**：在进行更改前始终运行`pytest tests/`
3. **开发**：遵循TDD原则，特别是对于仿真器模块
4. **验证**：使用`black`、`flake8`和`mypy`进行代码质量检查
5. **测试示例**：用`python examples/bb84_example.py`验证更改
6. **文档**：在`devlog/`中更新重要更改的开发日志

## 开发规则总结

### 必须遵循的命令规范

#### 环境命令
```bash
# Windows环境设置
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

#### 测试命令（强制要求）
```bash
# 所有变更前必须运行
pytest tests/
pytest --cov=. tests/
pytest tests/test_simulator.py    # 仿真器模块专用
```

#### 代码质量命令（提交前必须）
```bash
black .      # 代码格式化
flake8 .     # 代码检查
mypy .       # 类型检查
```

#### 验证命令
```bash
python examples/bb84_example.py  # 验证更改有效性
```

### 严格执行的开发原则

#### 1. TDD强制要求
- **仿真器模块（simulator/）**：所有更改必须先写测试再实现
- **测试构建顺序**：单光子 → 单信道 → 单测量 → 完整协议
- **绝对禁止**：在没有完整测试覆盖下提交`simulate_protocol_graph`

#### 2. 节点类型规范（不可违反）
- **标准类型**：QSP、QC、QM、CLO（量子态准备、信道、测量、经典操作）
- **命名规则**：节点ID必须反映类型（`qsp_1`、`qc_alice_bob`）
- **归属规则**：每个节点必须有`party`属性（Alice、Bob、Eve）

#### 3. 安全分析要求（关键规范）
- **强制使用**：有限密钥安全分析（非渐近极限）
- **框架要求**：可组合安全框架实现
- **计算规则**：使用平滑最小熵H_min^ε(X|E)

#### 4. 架构依赖顺序（不可颠倒）
1. AI智能体层 → QCGF DSL  
2. QCGF DSL → 仿真器
3. 仿真器 → 安全评估器
4. 安全评估器 → 形式化验证

### 代码质量要求
- **提交前检查**：必须通过black、flake8、mypy
- **测试覆盖率**：仿真器模块要求100%覆盖
- **示例验证**：所有更改必须通过`python examples/bb84_example.py`验证

### 项目特殊要求
- **协议图格式**：必须符合指定的数据结构规范
- **安全计算**：禁用渐近分析，仅使用现实有限密钥方法
- **模块协调**：层间接口严格按照依赖关系设计