# AI4QKD 开发指南

## 🎯 开发指南概述

本指南面向希望参与AI4QKD项目开发的贡献者，包括核心开发者、研究人员和社区贡献者。

**⚠️ 重要提醒**: 项目当前处于**完全重构阶段** (`clean-start-v3` 分支)，原有复杂代码已清空，只保留核心 `qcgf_dsl` 模块。参与开发前请先阅读 [CLAUDE.md](../CLAUDE.md) 了解重构指导原则。

## 📋 开发环境

### 系统要求

#### 硬件要求
- **CPU**: 4核以上，推荐8核
- **内存**: 最少8GB，推荐16GB+
- **存储**: 至少10GB可用空间
- **网络**: 稳定的互联网连接

#### 软件要求
- **操作系统**: 
  - Windows 10+ (推荐WSL2)
  - macOS 10.15+
  - Linux (Ubuntu 18.04+, CentOS 7+)
- **Python**: 3.8-3.11 (推荐3.9)
- **Git**: 2.20+
- **Conda**: Anaconda 或 Miniconda

### 开发环境配置

#### 1. 克隆项目
```bash
# Fork项目到您的GitHub账户
# 然后克隆您的fork
git clone https://github.com/您的用户名/AI4QKD.git
cd AI4QKD

# 添加上游仓库
git remote add upstream https://github.com/RoyalTeng/AI4QKD.git

# 验证远程仓库
git remote -v
```

#### 2. 环境设置
```bash
# 方式1：使用预配置环境（推荐）
conda activate ai4qkd_env

# 方式2：创建新环境
conda create -n ai4qkd_dev python=3.9
conda activate ai4qkd_dev

# 安装基础依赖
pip install -r requirements.txt

# 安装开发依赖
pip install pytest black flake8 mypy coverage pre-commit
```

#### 3. 验证环境
```bash
# 运行测试
python -m pytest tests/ -v

# 运行快速验证
python test_refactor.py

# 检查代码质量
black --check qcgf_dsl/
flake8 qcgf_dsl/
mypy qcgf_dsl/
```

## 🏗️ 项目架构

### 当前架构 (v2.0.0) - clean-start-v3 分支

```
AI4QKD/
├── qcgf_dsl/                    # 核心DSL模块
│   ├── __init__.py              # 模块入口和便捷函数
│   ├── protocol_graph.py        # 协议图核心类
│   ├── node_types.py            # 节点类型定义
│   ├── edge_types.py            # 边类型定义
│   ├── parser.py                # DSL解析器
│   ├── compiler.py              # DSL编译器
│   └── visualizer.py            # 可视化工具
├── tests/                       # 测试模块
│   ├── conftest.py              # pytest配置
│   ├── test_qcgf_dsl_refactor.py # 主要测试文件
│   └── integration/             # 集成测试（计划中）
├── docs/                        # 文档目录
│   ├── API_REFERENCE.md         # API参考文档
│   ├── USER_GUIDE.md           # 用户指南
│   └── DEVELOPMENT_GUIDE.md    # 本文档
├── examples/                    # 示例代码（计划中）
├── 参考文献/                     # 理论参考文献
├── 研究方案/                     # 研究设计文档
├── CLAUDE.md                   # Claude开发指导
├── README.md                   # 项目说明
├── CONTRIBUTING.md             # 贡献指南
├── CHANGELOG.md               # 版本变更日志
└── requirements.txt           # 依赖声明
```

### 计划架构 (v3.0.0)

```
AI4QKD/
├── core/                       # 核心模块
│   ├── protocol/               # 协议表示
│   ├── simulator/              # 量子仿真
│   ├── ai_designer/            # AI驱动优化
│   └── evaluator/              # 安全评估
├── interfaces/                 # 接口层
│   ├── cli/                    # 命令行界面
│   ├── web/                    # Web界面
│   └── api/                    # REST API
├── utils/                      # 工具函数
├── config/                     # 配置管理
├── tests/                      # 测试体系
├── examples/                   # 示例代码
└── docs/                       # 完整文档
```

## 🔄 重构指导原则

### 基本原则

#### 1. 技术方向一致性原则 (NEW! 2025-08-19)
- **DV-QKD专注**: 项目专注于点对点离散变量量子密钥分发协议
- **参数纯净性**: 严格禁止引入连续变量QKD(CV-QKD)相关参数
- **架构清洁**: 保持技术架构的专业性和一致性
- **概念分离**: 避免DV-QKD和CV-QKD概念混淆

#### 2. 基于参考的重构
- **必须参考**: GitHub master分支的原有实现
- **保持思路**: 维持设计思路的连续性
- **优化实现**: 在原有基础上改进性能和可维护性
- **记录过程**: 详细记录重构思路和改进点

#### 2. 重构工作流
所有重构工作必须遵循5步流程：

```
🧠 探索与规划 → 🧪 测试先行 → 💻 编码实现 → 🔄 多轮迭代 → ✅ 提交与反馈
```

### DV-QKD技术规范 (NEW! 2025-08-19)

#### 禁止的CV-QKD参数

**⚠️ 严格禁止**: 开发者必须严格避免引入以下连续变量QKD相关参数：

```python
# ❌ 禁止的参数类型
discrimination_threshold = 0.5  # 连续变量判决阈值
variance = 0.1                  # 高斯调制方差  
quadrature_phase = 0.0         # 正交相位参数
coherent_amplitude = 1.0       # 相干态振幅
squeezed_parameter = 0.2       # 压缩参数
homodyne_angle = np.pi/4       # 零差测量角度
displacement_parameter = 2.0    # 位移参数
squeezing_angle = 0.0          # 压缩角
quadrature_variance = 0.25     # 正交分量方差
thermal_photon_number = 0.1    # 热光子数
heterodyne_phase = np.pi/3     # 外差测量相位
```

**⚠️ 违规检测**: 代码审查时必须检查以下关键词：
- `discrimination`、`threshold`、`coherent`、`squeezed`
- `quadrature`、`homodyne`、`heterodyne`、`gaussian`
- `variance`（除非明确用于其他统计目的）
- `displacement`、`squeezing`、`thermal`

#### 允许的DV-QKD参数
以下参数符合离散变量QKD要求，可以在代码中使用：

```python
# ✅ 允许的参数
# 偏振相关
polarization_state = "H"       # 水平偏振态
polarization_angle = 0.0       # 偏振角度
extinction_ratio = 0.99        # 消光比

# 测量相关
basis = "Z"                    # 测量基（Z基或X基）
detector_efficiency = 0.8     # 探测器效率
dark_count_rate = 1e-6         # 暗计数率
gate_time = 1e-9              # 门时间

# 量子门相关
gate_type = "CNOT"            # 量子门类型
gate_fidelity = 0.99          # 量子门保真度
rotation_angle = np.pi/2      # 旋转角度（用于量子门）

# 物理信道相关
transmission_loss = 0.2        # 传输损耗
background_noise = 0.01       # 背景噪声
channel_length = 10.0         # 信道长度(km)
```

#### 量子态定义规范
DV-QKD中的量子态必须是离散的：

```python
# ✅ 正确的量子态定义
quantum_states = {
    "0": np.array([1, 0]),     # |0⟩态
    "1": np.array([0, 1]),     # |1⟩态
    "+": np.array([1, 1])/np.sqrt(2),  # |+⟩态
    "-": np.array([1, -1])/np.sqrt(2), # |-⟩态
}

# ❌ 避免的连续态定义
coherent_state = np.exp(-alpha**2/2) * np.array([...])  # 相干态
squeezed_state = ...                                    # 压缩态
```

#### 测量方式规范
DV-QKD使用光子探测器进行测量：

```python
# ✅ 正确的测量方式
def photon_detection_measurement(quantum_state, basis="Z"):
    """光子探测器测量"""
    if basis == "Z":
        # Z基测量：直接测量|0⟩和|1⟩
        prob_0 = abs(quantum_state[0])**2
        return 0 if np.random.random() < prob_0 else 1
    elif basis == "X":
        # X基测量：测量|+⟩和|-⟩
        plus_state = np.array([1, 1])/np.sqrt(2)
        minus_state = np.array([1, -1])/np.sqrt(2)
        prob_plus = abs(np.dot(quantum_state, plus_state))**2
        return 0 if np.random.random() < prob_plus else 1

# ❌ 避免的连续测量方式
def homodyne_detection(quantum_state, local_oscillator_phase):
    """避免：零差测量（连续变量测量方式）"""
    pass
```

### 代码注释要求

#### 文件头部注释
```python
"""
AI4QKD - [模块名称] (重构版)

重构思路：
- 参考GitHub master分支的[具体文件]实现思路
- 简化了[具体简化点]，提升了[具体改进]
- 保持了[具体保持的设计思路]

设计原则：
- [设计原则1]
- [设计原则2]
- [设计原则3]

主要改进：
- [改进点1]
- [改进点2]
- [改进点3]

作者: [您的姓名]
重构日期: [日期]
参考版本: GitHub master分支
"""
```

#### 重构函数注释
```python
# ============================================================================
# 重构说明: 此函数基于GitHub master分支的[原函数名]重构
# 重构日期: [日期]
# 重构原因: [具体原因]
# 主要改进: [改进点]
# 参考文件: [GitHub上的原文件路径]
# ============================================================================

def refactored_function(self, param1, param2):
    """
    重构后的函数实现
    
    重构思路：
    - 参考原有[原函数名]的实现逻辑
    - 简化了[具体简化点]
    - 优化了[具体优化点]
    - 改进了[具体改进点]
    
    与原有实现的差异：
    - [差异点1]
    - [差异点2]
    - [差异点3]
    
    参数：
        param1: 参数1说明
        param2: 参数2说明
        
    返回值：
        返回值说明
        
    异常：
        异常说明
    """
    pass
```

## 🧪 测试驱动开发

### TDD流程

#### 红-绿-重构循环
1. **红(Red)**: 写一个失败的测试
2. **绿(Green)**: 写最少的代码使测试通过
3. **重构(Refactor)**: 改进代码质量，保持测试通过

#### 测试层次
```
🔺 单元测试 (Unit Tests)
├── 函数级测试
├── 类方法测试
└── 模块接口测试

🔺 集成测试 (Integration Tests)
├── 模块间交互测试
├── 文件I/O测试
└── 外部依赖测试

🔺 端到端测试 (E2E Tests)
├── 完整用例测试
├── 性能测试
└── 用户场景测试
```

### 测试规范

#### 测试文件命名
```
tests/
├── test_[模块名].py           # 单元测试
├── test_[模块名]_integration.py # 集成测试
├── test_[模块名]_performance.py # 性能测试
└── fixtures/                  # 测试数据
    ├── protocols/             # 测试协议
    └── data/                  # 测试数据集
```

#### 测试类结构
```python
class Test[ModuleName]Refactor:
    """[模块名称]重构测试用例 - 基于原有接口"""
    
    def setup_method(self):
        """每个测试方法前的设置"""
        pass
    
    def teardown_method(self):
        """每个测试方法后的清理"""
        pass
    
    def test_[功能名]_basic(self):
        """测试[功能名]的基本功能"""
        pass
    
    def test_[功能名]_edge_cases(self):
        """测试[功能名]的边界情况"""
        pass
    
    def test_[功能名]_error_handling(self):
        """测试[功能名]的错误处理"""
        pass
    
    def test_[功能名]_compatibility(self):
        """测试[功能名]的向后兼容性"""
        pass
```

#### 测试示例
```python
import pytest
from qcgf_dsl import *

class TestProtocolGraphRefactor:
    """ProtocolGraph重构测试用例"""
    
    def setup_method(self):
        self.protocol = ProtocolGraph("测试协议")
    
    def test_add_node_basic_functionality(self):
        """测试添加节点的基本功能"""
        # Arrange
        node_type = NodeType.QSP
        party = Party.ALICE
        
        # Act
        node_id = self.protocol.add_node(node_type, party=party)
        
        # Assert
        assert node_id is not None
        assert self.protocol.has_node(node_id)
        
        node = self.protocol.get_node(node_id)
        assert node.node_type == node_type
        assert node.party == party
    
    def test_add_node_parameter_validation(self):
        """测试节点参数验证"""
        # 测试无效效率值
        with pytest.raises(ValueError, match="效率"):
            self.protocol.add_node(
                NodeType.QM,
                params={"efficiency": 1.5}
            )
        
        # 测试有效参数
        node_id = self.protocol.add_node(
            NodeType.QM,
            params={"efficiency": 0.8}
        )
        assert node_id is not None
    
    @pytest.mark.performance
    def test_large_scale_node_addition(self):
        """测试大规模节点添加性能"""
        import time
        
        start_time = time.time()
        for i in range(1000):
            self.protocol.add_node(NodeType.QSP)
        end_time = time.time()
        
        # 性能要求：1000个节点添加应在1秒内完成
        assert end_time - start_time < 1.0
        assert self.protocol.get_node_count() == 1000
```

### 运行测试

#### 基本测试命令
```bash
# 运行所有测试
python -m pytest tests/ -v

# 运行特定测试文件
python -m pytest tests/test_qcgf_dsl_refactor.py -v

# 运行特定测试方法
python -m pytest tests/test_qcgf_dsl_refactor.py::TestProtocolGraphRefactor::test_add_node_basic -v

# 运行带标记的测试
python -m pytest tests/ -m performance -v

# 并行运行测试
python -m pytest tests/ -n auto
```

#### 测试覆盖率
```bash
# 生成覆盖率报告
python -m pytest tests/ --cov=qcgf_dsl --cov-report=html --cov-report=term

# 查看详细覆盖率
python -m pytest tests/ --cov=qcgf_dsl --cov-report=term-missing

# 覆盖率要求
# 单元测试覆盖率 > 90%
# 关键路径覆盖率 = 100%
```

## 🔧 代码质量

### 代码规范

#### Python代码风格
- **PEP 8**: 遵循Python官方风格指南
- **类型注解**: 所有公共接口必须有类型注解
- **文档字符串**: 所有公共函数和类必须有docstring
- **命名规范**: 使用描述性的变量和函数名

#### 代码格式化
```bash
# 使用Black格式化代码
black qcgf_dsl/ tests/

# 检查格式
black --check qcgf_dsl/ tests/

# 使用isort整理导入
isort qcgf_dsl/ tests/
```

#### 代码检查
```bash
# 使用flake8检查代码风格
flake8 qcgf_dsl/ tests/

# 使用mypy检查类型
mypy qcgf_dsl/

# 使用pylint进行深度检查
pylint qcgf_dsl/
```

### 性能要求

#### 性能基准
```python
# 协议创建性能
create_bb84_protocol()  # < 10ms

# 节点添加性能
protocol.add_node()     # < 1ms per node

# 大型协议处理
1000个节点的协议       # < 1s创建时间
                      # < 100MB内存使用
```

#### 性能测试
```python
import time
import psutil
import memory_profiler

@pytest.mark.performance
def test_protocol_creation_performance():
    """测试协议创建性能"""
    iterations = 100
    
    start_time = time.time()
    for _ in range(iterations):
        protocol = create_bb84_protocol()
    end_time = time.time()
    
    avg_time = (end_time - start_time) / iterations
    assert avg_time < 0.01  # 每次创建 < 10ms

@memory_profiler.profile
def test_memory_usage():
    """测试内存使用"""
    protocols = []
    for i in range(100):
        protocol = create_bb84_protocol()
        protocols.append(protocol)
    
    process = psutil.Process()
    memory_mb = process.memory_info().rss / 1024 / 1024
    assert memory_mb < 100  # 内存使用 < 100MB
```

## 🚀 开发工作流

### Git工作流

#### 分支策略
```
main/master              # 稳定版本，生产就绪
├── clean-start-v3       # 重构主分支，当前开发
├── feature/新功能名      # 功能开发分支
├── fix/bug描述          # bug修复分支
├── refactor/模块名      # 重构分支
└── docs/文档类型        # 文档更新分支
```

#### 标准工作流程
```bash
# 1. 更新本地主分支
git checkout clean-start-v3
git pull upstream clean-start-v3

# 2. 创建功能分支
git checkout -b feature/protocol-validation

# 3. 开发和提交
git add .
git commit -m "feat(qcgf_dsl): 添加协议验证功能

- 实现协议DAG验证
- 添加循环检测
- 包含完整测试用例
- 更新API文档

🤖 Generated with [Claude Code](https://claude.ai/code)
Co-Authored-By: Claude <noreply@anthropic.com>"

# 4. 推送分支
git push origin feature/protocol-validation

# 5. 创建Pull Request
# 在GitHub上创建PR，等待代码审查

# 6. 合并后清理
git checkout clean-start-v3
git pull upstream clean-start-v3
git branch -d feature/protocol-validation
```

### 提交信息规范

#### 提交类型
```
feat:     新功能
fix:      bug修复
docs:     文档更新
style:    代码格式修改（不影响功能）
refactor: 代码重构
perf:     性能优化
test:     测试相关
build:    构建系统或依赖修改
ci:       CI配置修改
chore:    其他不修改src或test的修改
revert:   撤销之前的提交
```

#### 提交信息格式
```
类型(作用域): 简短描述

详细描述（可选）
- 列出主要变更
- 说明变更原因
- 描述影响范围

相关Issue: #123, #456

🤖 Generated with [Claude Code](https://claude.ai/code)
Co-Authored-By: Claude <noreply@anthropic.com>
```

## 📦 模块开发

### 新模块开发流程

#### 1. 探索与规划阶段
```markdown
## 🧠 探索与规划

### GitHub代码分析
- 分析原有模块的架构设计
- 识别核心功能和接口
- 理解实现思路和算法

### 重构目标
- 明确需要改进的方面
- 确定保持的设计思路
- 制定优化策略

### 技术方案
- 选择技术栈和依赖
- 设计API接口
- 规划实现步骤

### 风险评估
- 识别技术风险
- 评估兼容性影响
- 制定风险缓解措施
```

#### 2. 测试先行阶段
```python
# 创建测试文件 tests/test_new_module.py
class TestNewModuleRefactor:
    """新模块重构测试用例"""
    
    def test_basic_functionality(self):
        """测试基本功能 - 基于原有接口"""
        # 测试原有接口的兼容性
        pass
    
    def test_improved_features(self):
        """测试改进功能 - 重构优化"""
        # 测试新的优化功能
        pass
    
    def test_performance(self):
        """测试性能改进"""
        # 验证性能提升
        pass
```

#### 3. 编码实现阶段
```python
# 创建模块文件 qcgf_dsl/new_module.py
"""
AI4QKD - 新模块 (重构版)

重构思路：
- 参考GitHub master分支的[原模块]实现思路
- 简化了[具体改进点]
- 优化了[性能方面]
"""

class NewModule:
    """新模块类 - 基于原有设计重构"""
    
    def __init__(self):
        """初始化新模块"""
        pass
    
    def core_method(self):
        """核心方法 - 参考原有实现，优化性能"""
        pass
```

#### 4. 迭代重构阶段
- 代码审查和反馈
- 性能优化
- 接口完善
- 文档更新

#### 5. 提交与集成阶段
- 测试验证
- 文档完善
- 版本更新
- 发布准备

### 模块设计模式

#### 单一职责原则
```python
# 好的设计 - 单一职责
class ProtocolValidator:
    """专门负责协议验证"""
    
    def validate_dag_structure(self, protocol):
        """验证DAG结构"""
        pass
    
    def validate_physical_constraints(self, protocol):
        """验证物理约束"""
        pass

# 避免的设计 - 职责过多
class ProtocolManager:
    """避免：职责过多的设计"""
    
    def create_protocol(self):
        pass
    
    def validate_protocol(self):
        pass
    
    def simulate_protocol(self):
        pass
    
    def optimize_protocol(self):
        pass
```

#### 接口隔离原则
```python
# 好的设计 - 接口隔离
class ProtocolReader:
    """只读接口"""
    
    def get_node_count(self):
        pass
    
    def get_statistics(self):
        pass

class ProtocolWriter:
    """写入接口"""
    
    def add_node(self):
        pass
    
    def add_edge(self):
        pass

# 具体类实现多个接口
class ProtocolGraph(ProtocolReader, ProtocolWriter):
    pass
```

## 🔍 调试和分析

### 调试技巧

#### 日志记录
```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def debug_protocol_creation(protocol):
    """调试协议创建过程"""
    logger.debug(f"创建协议: {protocol.name}")
    logger.debug(f"节点数: {protocol.get_node_count()}")
    logger.debug(f"边数: {protocol.get_edge_count()}")
    
    for node in protocol.get_all_nodes():
        logger.debug(f"节点 {node.node_id}: {node.node_type.value}")
```

#### 性能分析
```python
import cProfile
import pstats

def profile_function():
    """性能分析装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            pr = cProfile.Profile()
            pr.enable()
            result = func(*args, **kwargs)
            pr.disable()
            
            stats = pstats.Stats(pr)
            stats.sort_stats('cumulative')
            stats.print_stats(10)  # 显示前10个最慢的函数
            
            return result
        return wrapper
    return decorator

@profile_function()
def create_large_protocol():
    protocol = ProtocolGraph("大型协议")
    for i in range(1000):
        protocol.add_node(NodeType.QSP)
    return protocol
```

#### 内存分析
```python
import memory_profiler
import tracemalloc

@memory_profiler.profile
def analyze_memory_usage():
    """分析内存使用"""
    protocols = []
    for i in range(100):
        protocol = create_bb84_protocol()
        protocols.append(protocol)
    return protocols

def trace_memory_allocations():
    """跟踪内存分配"""
    tracemalloc.start()
    
    # 执行代码
    protocol = create_bb84_protocol()
    
    # 获取内存快照
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')
    
    print("内存使用前10位:")
    for stat in top_stats[:10]:
        print(stat)
```

### 问题诊断

#### 常见问题排查
```python
def diagnose_protocol_issues(protocol):
    """诊断协议问题"""
    issues = []
    
    # 检查DAG结构
    if not protocol.is_dag():
        issues.append("协议图包含环路")
    
    # 检查节点参数
    for node in protocol.get_all_nodes():
        if node.node_type == NodeType.QM:
            efficiency = node.get_param('efficiency', 0)
            if efficiency > 1.0:
                issues.append(f"节点 {node.node_id} 效率超过1.0: {efficiency}")
    
    # 检查连通性
    if protocol.get_node_count() > 1 and protocol.get_edge_count() == 0:
        issues.append("协议图缺少边连接")
    
    return issues
```

## 📚 文档维护

### 文档类型

#### API文档
- 自动生成：使用docstring生成API文档
- 手动维护：复杂接口的详细说明
- 示例代码：每个API都包含使用示例

#### 用户文档
- 快速开始：新用户的入门指南
- 详细教程：深入的功能说明
- 最佳实践：推荐的使用方法

#### 开发文档
- 架构设计：系统架构和设计决策
- 开发流程：开发和贡献指南
- 故障排除：常见问题和解决方案

### 文档更新流程

#### 同步更新原则
- 代码变更时必须同步更新文档
- API修改必须更新API文档
- 新功能必须包含使用示例
- bug修复必须更新故障排除文档

#### 文档审查
- 技术准确性：确保文档与代码一致
- 可读性：文档易于理解
- 完整性：覆盖所有重要功能
- 时效性：保持文档最新

## 🚀 发布流程

### 版本管理

#### 语义化版本控制
```
主版本.次版本.修订版本 (例如: 2.1.3)

主版本: 不兼容的API修改
次版本: 向后兼容的功能新增
修订版本: 向后兼容的问题修正
```

#### 发布准备
```bash
# 1. 更新版本号
# 修改 qcgf_dsl/__init__.py 中的 __version__

# 2. 更新CHANGELOG
# 在 CHANGELOG.md 中添加新版本的变更记录

# 3. 运行完整测试
python -m pytest tests/ -v
python test_refactor.py

# 4. 生成文档
# 更新API文档和用户指南

# 5. 创建发布标签
git tag -a v2.1.0 -m "Release version 2.1.0"
git push upstream v2.1.0
```

### 持续集成

#### GitHub Actions配置
```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ clean-start-v3 ]
  pull_request:
    branches: [ clean-start-v3 ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest black flake8
    
    - name: Run tests
      run: python -m pytest tests/ -v
    
    - name: Check code style
      run: |
        black --check qcgf_dsl/
        flake8 qcgf_dsl/
```

## 🤝 团队协作

### 代码审查

#### 审查清单
- [ ] 功能实现正确
- [ ] 包含重构思路注释
- [ ] 测试覆盖充分
- [ ] 文档更新同步
- [ ] 代码风格规范
- [ ] 性能要求满足
- [ ] 向后兼容性保持
- [ ] **DV-QKD技术方向一致性** (NEW! 2025-08-19)
  - [ ] 无连续变量QKD相关参数（如discrimination_threshold）
  - [ ] 量子态定义符合离散变量QKD要求
  - [ ] 测量方式使用光子探测器模式
  - [ ] 参数范围符合DV-QKD物理约束
  - [ ] 变量命名遵循DV-QKD术语规范
  - [ ] 代码注释避免CV-QKD概念引用
  - [ ] 算法实现基于离散量子态操作
  - [ ] 性能指标符合DV-QKD评估标准

#### 审查流程
1. **提交PR**: 创建详细的Pull Request
2. **自动检查**: CI/CD自动运行测试
3. **人工审查**: 团队成员进行代码审查
4. **修改完善**: 根据反馈修改代码
5. **批准合并**: 审查通过后合并代码

### 沟通渠道

#### 开发讨论
- **GitHub Discussions**: 技术讨论和问题
- **GitHub Issues**: bug报告和功能请求
- **邮件列表**: 重要决策和公告

#### 会议安排
- **每周同步**: 团队进度同步
- **月度评审**: 项目里程碑评审
- **季度规划**: 版本规划和路线图

## 🎓 学习资源

### 必读材料
1. **量子密码学基础**: Gisin等(2002)的经典论文
2. **AI-量子应用**: Dunjko & Briegel(2018)的综述
3. **图论基础**: NetworkX官方文档
4. **Python最佳实践**: PEP 8和相关文档

### 推荐工具
- **IDE**: PyCharm Professional 或 VS Code
- **Git GUI**: SourceTree 或 GitKraken
- **API测试**: Postman 或 Insomnia
- **性能分析**: py-spy, memory_profiler

### 在线资源
- **项目文档**: https://ai4qkd.readthedocs.io
- **API参考**: https://api.ai4qkd.org
- **讨论社区**: https://github.com/RoyalTeng/AI4QKD/discussions

---

**🚀 欢迎加入AI4QKD开发团队！让我们一起构建量子密码学和人工智能的未来！**