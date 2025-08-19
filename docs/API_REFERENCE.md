# qcgf_dsl 模块 API 参考文档

## 概述

qcgf_dsl（Quantum-Classical Graph Flow Domain Specific Language）是AI4QKD项目的核心模块，提供量子密钥分发协议的图形化表示和操作接口。

## 快速开始

```python
from qcgf_dsl import *

# 创建BB84协议
bb84 = create_bb84_protocol()

# 添加自定义节点
node_id = bb84.add_node(NodeType.QSP, party=Party.ALICE, 
                        params={"state": "|+⟩", "fidelity": 0.99})

# 保存协议
save_protocol_to_file(bb84, "my_bb84.json")
```

## 核心类

### ProtocolGraph

QKD协议的图形表示类，支持节点和边的管理。

```python
class ProtocolGraph:
    def __init__(self, name: str = "QKD_Protocol")
```

#### 方法

##### add_node()
```python
def add_node(self,
             node_type: NodeType,
             params: Optional[Dict[str, Any]] = None,
             party: Optional[Party] = None,
             position: Optional[Tuple[float, float]] = None,
             node_id: Optional[str] = None) -> str
```

向协议图添加节点。

**参数：**
- `node_type`: 节点类型（如 `NodeType.QSP`, `NodeType.QM`）
- `params`: 节点参数字典
- `party`: 参与者（`Party.ALICE`, `Party.BOB`, `Party.CHARLIE`）
- `position`: 节点在可视化中的位置 (x, y)
- `node_id`: 自定义节点ID（可选）

**返回值：**
- `str`: 生成的节点ID

**示例：**
```python
# 添加Alice的量子态准备节点
alice_qsp = protocol.add_node(
    NodeType.QSP,
    party=Party.ALICE,
    params={"state": "|0⟩", "fidelity": 0.99}
)

# 添加量子信道
qc = protocol.add_node(
    NodeType.QC,
    params={"loss": 0.1, "distance": 50.0}
)
```

##### add_edge()
```python
def add_edge(self,
             source_id: str,
             target_id: str,
             edge_type: EdgeType = EdgeType.QUANTUM,
             params: Optional[Dict[str, Any]] = None) -> bool
```

添加边连接两个节点。

**参数：**
- `source_id`: 源节点ID
- `target_id`: 目标节点ID
- `edge_type`: 边类型（`EdgeType.QUANTUM`, `EdgeType.CLASSICAL`）
- `params`: 边参数字典

**返回值：**
- `bool`: 是否成功添加

**示例：**
```python
# 连接Alice的量子态准备节点到量子信道
protocol.add_edge(alice_qsp, quantum_channel, EdgeType.QUANTUM)

# 添加经典通信
protocol.add_edge(alice_node, bob_node, EdgeType.CLASSICAL,
                  params={"bandwidth": 1e9, "latency": 1e-6})
```

##### get_node()
```python
def get_node(self, node_id: str) -> Optional[Node]
```

获取指定ID的节点。

##### get_nodes_by_type()
```python
def get_nodes_by_type(self, node_type: NodeType) -> List[Node]
```

获取指定类型的所有节点。

##### get_nodes_by_party()
```python
def get_nodes_by_party(self, party: Party) -> List[Node]
```

获取指定参与者的所有节点。

##### get_statistics()
```python
def get_statistics(self) -> Dict[str, Any]
```

获取协议图的统计信息。

**返回值：**
```python
{
    "name": "协议名称",
    "node_count": 节点数量,
    "edge_count": 边数量,
    "is_dag": 是否为有向无环图,
    "node_stats": {"QSP": 2, "QM": 1, ...},
    "party_stats": {"Alice": 3, "Bob": 2, ...},
    "edge_types": {"quantum": 2, "classical": 1},
    "density": 图密度,
    "avg_degree": 平均度数
}
```

##### save_to_file() / load_from_file()
```python
def save_to_file(self, filename: str)

@classmethod
def load_from_file(cls, filename: str) -> 'ProtocolGraph'
```

协议图的文件保存和加载。

### Node

协议图中的节点类。

```python
class Node:
    def __init__(self,
                 node_id: str,
                 node_type: NodeType,
                 params: Optional[Dict[str, Any]] = None,
                 party: Optional[Party] = None,
                 position: Optional[Tuple[float, float]] = None,
                 metadata: Optional[Dict[str, Any]] = None)
```

#### 方法

##### update_params()
```python
def update_params(self, new_params: Dict[str, Any])
```

更新节点参数。

##### get_param() / set_param()
```python
def get_param(self, key: str, default: Any = None) -> Any
def set_param(self, key: str, value: Any)
```

获取/设置单个参数。

##### is_quantum_node() / is_classical_node()
```python
def is_quantum_node(self) -> bool
def is_classical_node(self) -> bool
```

判断节点类型。

## 枚举类型

### NodeType

节点类型定义。

```python
class NodeType(Enum):
    QSP = "QSP"      # 量子态准备
    QC = "QC"        # 量子信道
    QM = "QM"        # 量子测量
    QG = "QG"        # 量子门
    QD = "QD"        # 量子检测器
    BSM = "BSM"      # 贝尔态测量
    CLO = "CLO"      # 经典逻辑操作
    CS = "CS"        # 经典存储
    CC = "CC"        # 经典信道
    ATTACK = "ATTACK"  # 攻击节点
    SINK = "SINK"      # 汇聚节点
```

#### QC节点子类型说明

QC（量子信道）节点支持以下子类型：

- **FIBER**: 光纤量子信道
  - 适用于光纤传输的量子通信
  - 支持参数：`loss`、`distance`、`dispersion` 等
  
- **FREE_SPACE**: 自由空间量子信道  
  - 适用于自由空间传输的量子通信
  - 支持参数：`loss`、`distance`、`atmospheric_effects` 等

**注意**: 
- v2.0.1版本已移除 `QUANTUM_MEMORY` 子类型
- 移除原因：点对点DV-QKD协议专业化，不需要量子存储器功能
- 现有使用 `FIBER` 和 `FREE_SPACE` 子类型的代码无影响

#### 方法

##### get_quantum_types() / get_classical_types()
```python
@classmethod
def get_quantum_types(cls) -> List['NodeType']

@classmethod
def get_classical_types(cls) -> List['NodeType']
```

获取量子/经典节点类型列表。

##### is_quantum_type() / is_classical_type()
```python
@classmethod
def is_quantum_type(cls, node_type: 'NodeType') -> bool

@classmethod
def is_classical_type(cls, node_type: 'NodeType') -> bool
```

判断节点类型分类。

##### get_description()
```python
def get_description(self) -> str
```

获取节点类型的中文描述。

### Party

协议参与者定义。

```python
class Party(Enum):
    ALICE = "Alice"     # 发送方
    BOB = "Bob"         # 接收方
    EVE = "Eve"         # 窃听者
    CHARLIE = "Charlie" # 第三方
    UNKNOWN = "Unknown" # 未知
```

### EdgeType

边类型定义。

```python
class EdgeType(Enum):
    QUANTUM = "quantum"           # 量子信道
    CLASSICAL = "classical"       # 经典信道
    CONTROL = "control"           # 控制信号
    DATA = "data"                # 数据传输
    FEEDBACK = "feedback"        # 反馈信号
    SYNCHRONIZATION = "sync"     # 同步信号
```

### EdgeDirection

边方向定义。

```python
class EdgeDirection(Enum):
    FORWARD = "forward"          # 前向
    BACKWARD = "backward"        # 后向
    BIDIRECTIONAL = "bidirectional"  # 双向
```

## 模板和验证

### 节点模板

```python
def get_node_template(node_type: NodeType) -> Dict[str, Any]
```

获取节点类型的默认参数模板。

**示例：**
```python
# 获取QSP节点模板
template = get_node_template(NodeType.QSP)
# 返回: {"state": "|0⟩", "fidelity": 0.99, "preparation_time": 1e-9, ...}
```

### 参数验证

```python
def validate_node_params(node_type: NodeType, params: Dict[str, Any]) -> bool
def validate_edge_params(edge_type: EdgeType, params: Dict[str, Any]) -> bool
```

验证节点/边参数的有效性。

## 理想化模式

### 模式控制

```python
def set_idealized_mode(enabled: bool = True)
def is_idealized_mode() -> bool
def setup_idealized_research_mode()
def setup_realistic_deployment_mode()
```

控制理想化/现实模式。

**示例：**
```python
# 切换到理想化模式（用于研究）
set_idealized_mode(True)

# 获取理想化参数模板
template = get_node_template(NodeType.QM)
# 在理想化模式下：efficiency=1.0, dark_count_rate=0.0

# 切换回现实模式
set_idealized_mode(False)
```

### 参数对比

```python
def compare_mode_parameters(node_type: NodeType) -> Dict[str, Any]
```

比较理想化和现实模式的参数差异。

## 便捷功能

### 协议创建

```python
def create_bb84_protocol() -> ProtocolGraph
def create_mdi_qkd_protocol() -> ProtocolGraph
```

快速创建标准协议。

### 文件操作

```python
def save_protocol_to_file(protocol: ProtocolGraph, filepath: str, format_type: str = "json")
def load_protocol_from_file(filepath: str) -> ProtocolGraph
def parse_protocol_from_string(dsl_text: str) -> ProtocolGraph
```

协议的保存、加载和解析。

## DSL解析和序列化

### QCGFParser

```python
class QCGFParser:
    def parse(self, dsl_text: str) -> ProtocolGraph
    def parse_from_file(self, filepath: str) -> ProtocolGraph
```

DSL文本解析器。

### QCGFSerializer

```python
class QCGFSerializer:
    def serialize(self, protocol: ProtocolGraph) -> str
    def serialize_to_file(self, protocol: ProtocolGraph, filepath: str)
```

协议序列化器。

## 可视化

### ProtocolVisualizer

```python
class ProtocolVisualizer:
    def visualize(self, protocol: ProtocolGraph, **kwargs)
    def save_visualization(self, protocol: ProtocolGraph, filepath: str)
```

协议图可视化。

### 便捷函数

```python
def visualize_protocol(protocol: ProtocolGraph, **kwargs)
```

快速可视化协议图。

## 代码生成

### QCGFCompiler

```python
class QCGFCompiler:
    def compile(self, protocol: ProtocolGraph, target: str = "qiskit") -> str
```

将协议编译为量子电路代码。

### 便捷函数

```python
def compile_protocol(protocol: ProtocolGraph, target: str = "qiskit") -> str
def compile_to_file(protocol: ProtocolGraph, filepath: str, target: str = "qiskit")
```

## 错误处理

### 常见异常

- `ValueError`: 参数无效或类型错误
- `IOError`: 文件读写错误
- `QCGFValidationError`: 协议验证失败（如果实现）
- `QCGFParsingError`: DSL解析错误（如果实现）

### 调试技巧

```python
# 检查协议图有效性
if not protocol.is_dag():
    print("警告：协议图包含环路")

# 获取详细统计信息
stats = protocol.get_statistics()
print(f"节点数：{stats['node_count']}")
print(f"边数：{stats['edge_count']}")

# 检查节点参数
for node in protocol.get_all_nodes():
    print(f"节点 {node.node_id}: {node.get_description()}")
```

## 最佳实践

### 1. 协议设计

```python
# 好的做法：逐步构建协议
protocol = ProtocolGraph("My_Protocol")

# 先添加节点
alice_qsp = protocol.add_node(NodeType.QSP, party=Party.ALICE)
bob_qm = protocol.add_node(NodeType.QM, party=Party.BOB)

# 再添加连接
protocol.add_edge(alice_qsp, bob_qm, EdgeType.QUANTUM)

# 验证协议
assert protocol.is_dag(), "协议图必须是DAG"
```

### 2. 参数管理

```python
# 使用模板作为起点
template = get_node_template(NodeType.QSP)
custom_params = template.copy()
custom_params.update({"fidelity": 0.995})

node_id = protocol.add_node(NodeType.QSP, params=custom_params)
```

### 3. 错误处理

```python
try:
    protocol.add_node(NodeType.QSP, params={"invalid_param": "value"})
except ValueError as e:
    print(f"参数错误：{e}")
```

### 4. 性能优化

```python
# 批量操作时禁用统计更新
protocol._stats_dirty = False
for i in range(1000):
    protocol.add_node(NodeType.QSP)
protocol._stats_dirty = True  # 手动标记需要更新
```

## 版本兼容性

- **当前版本**: 2.0.0 (重构版本)
- **Python要求**: 3.8+
- **依赖**: NetworkX, NumPy, Matplotlib (可选)

## 更多资源

- [用户指南](USER_GUIDE.md)
- [开发指南](DEVELOPMENT_GUIDE.md)
- [示例代码](../examples/)
- [测试用例](../tests/)