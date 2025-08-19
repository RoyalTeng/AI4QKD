"""
AI4QKD - 协议图核心模块 (重构版)

重构思路：
- 参考GitHub master分支的protocol_graph.py实现思路
- 保持原有ProtocolGraph和Node类的接口兼容性
- 简化了图管理逻辑，提高性能和可维护性
- 优化了节点和边的创建、删除、查找机制

设计原则：
- 清晰的图数据结构管理
- 高效的节点和边操作
- 严格的DAG约束验证
- 完整的序列化支持

主要改进：
- 简化了节点管理的内部逻辑
- 优化了图操作的性能
- 改进了统计信息的计算
- 统一了错误处理机制

作者: Claude (AI Assistant)
重构日期: 2025-08-17
参考版本: GitHub master分支 protocol_graph.py
"""

import networkx as nx
import json
import uuid
from typing import Dict, List, Any, Optional, Tuple, Union
from .node_types import NodeType, Party, get_node_template, validate_node_params
from .edge_types import EdgeType, Edge

# =============================================================================
# 重构说明: 此模块基于GitHub master分支的protocol_graph.py重构
# 重构日期: 2025-08-17
# 重构原因: 简化图管理逻辑，提高性能和可维护性
# 主要改进: 优化节点操作，改进边管理，简化统计计算
# 参考文件: qcgf_dsl/protocol_graph.py
# =============================================================================


class Node:
    """
    协议节点类 - 重构版本
    
    重构思路：
    - 保持原有Node类的接口兼容性
    - 简化了节点的创建和参数管理
    - 优化了参数验证和更新机制
    - 改进了序列化和反序列化功能
    
    设计改进：
    - 更清晰的构造函数设计
    - 统一的参数管理接口
    - 简化的类型检查方法
    - 完善的字符串表示
    
    核心功能：
    - 节点的创建和参数管理
    - 节点类型和参与者的验证
    - 节点对象的序列化
    """
    
    def __init__(self,
                 node_id: str,
                 node_type: NodeType,
                 params: Optional[Dict[str, Any]] = None,
                 party: Optional[Party] = None,
                 position: Optional[Tuple[float, float]] = None,
                 metadata: Optional[Dict[str, Any]] = None):
        """
        初始化节点
        
        重构思路：
        - 保持原有构造函数的接口
        - 简化了参数处理逻辑
        - 优化了默认参数的设置
        - 改进了验证机制
        
        参数：
            node_id: 节点唯一标识符
            node_type: 节点类型
            params: 节点参数字典
            party: 参与者
            position: 节点位置坐标 (x, y)
            metadata: 额外元数据
            
        异常：
            ValueError: 参数无效时抛出
        """
        self.node_id = node_id
        self.node_type = node_type
        self.params = params if params is not None else {}
        self.party = party
        self.position = position or (0.0, 0.0)
        self.metadata = metadata or {}
        
        # 设置默认参数
        self._set_default_params()
        
        # 验证参数
        if not validate_node_params(node_type, self.params):
            raise ValueError(f"节点类型 {node_type} 的参数无效: {self.params}")
    
    def _set_default_params(self):
        """
        设置默认参数
        
        重构思路：
        - 基于模板系统设置默认值
        - 避免覆盖用户提供的参数
        - 自动推断参与者信息
        """
        template = get_node_template(self.node_type)
        for key, value in template.items():
            if key not in self.params:
                self.params[key] = value
        
        # 从参数中推断参与者（如果未明确指定）
        if self.party is None and "party" in self.params:
            if isinstance(self.params["party"], Party):
                self.party = self.params["party"]
            elif isinstance(self.params["party"], str):
                try:
                    self.party = Party(self.params["party"])
                except ValueError:
                    self.party = Party.UNKNOWN
    
    def update_params(self, new_params: Dict[str, Any]):
        """
        更新节点参数
        
        重构思路：
        - 保持原有的参数更新接口
        - 确保更新后参数的有效性
        - 提供清晰的错误信息
        
        参数：
            new_params: 新的参数字典
            
        异常：
            ValueError: 参数无效时抛出
        """
        # 备份原参数
        old_params = self.params.copy()
        
        # 更新参数
        self.params.update(new_params)
        
        # 验证更新后的参数
        if not validate_node_params(self.node_type, self.params):
            # 恢复原参数
            self.params = old_params
            raise ValueError(f"节点类型 {self.node_type} 的参数无效: {new_params}")
        
        # 更新参与者信息（如果参数中包含）
        if "party" in new_params:
            if isinstance(new_params["party"], Party):
                self.party = new_params["party"]
            elif isinstance(new_params["party"], str):
                try:
                    self.party = Party(new_params["party"])
                except ValueError:
                    self.party = Party.UNKNOWN
    
    def get_param(self, key: str, default: Any = None) -> Any:
        """
        获取指定参数值
        
        重构思路：
        - 保持原有的参数获取接口
        - 支持默认值机制
        - 简化参数访问逻辑
        
        参数：
            key: 参数名
            default: 默认值
            
        返回值：
            Any: 参数值
        """
        return self.params.get(key, default)
    
    def set_param(self, key: str, value: Any):
        """
        设置单个参数值
        
        重构思路：
        - 提供便捷的单参数设置接口
        - 确保设置后参数的有效性
        - 简化参数修改操作
        
        参数：
            key: 参数名
            value: 参数值
            
        异常：
            ValueError: 参数无效时抛出
        """
        # 备份原值
        old_value = self.params.get(key)
        
        # 设置新值
        self.params[key] = value
        
        # 验证参数
        if not validate_node_params(self.node_type, self.params):
            # 恢复原值
            if old_value is not None:
                self.params[key] = old_value
            else:
                self.params.pop(key, None)
            raise ValueError(f"节点类型 {self.node_type} 的参数无效: {key}={value}")
        
        # 特殊处理参与者参数
        if key == "party":
            if isinstance(value, Party):
                self.party = value
            elif isinstance(value, str):
                try:
                    self.party = Party(value)
                except ValueError:
                    self.party = Party.UNKNOWN
    
    def is_quantum_node(self) -> bool:
        """
        判断是否为量子节点
        
        重构思路：
        - 保持原有的类型判断接口
        - 使用类方法简化判断逻辑
        
        返回值：
            bool: 是否为量子节点
        """
        return NodeType.is_quantum_type(self.node_type)
    
    def is_classical_node(self) -> bool:
        """
        判断是否为经典节点
        
        重构思路：
        - 保持原有的类型判断接口
        - 与量子节点判断保持一致
        
        返回值：
            bool: 是否为经典节点
        """
        return NodeType.is_classical_type(self.node_type)
    
    def get_description(self) -> str:
        """
        获取节点的描述信息
        
        重构思路：
        - 新增节点描述的便捷方法
        - 结合类型和参与者信息
        - 便于调试和文档生成
        
        返回值：
            str: 节点描述
        """
        type_desc = self.node_type.get_description()
        party_desc = f" ({self.party.value})" if self.party and self.party != Party.UNKNOWN else ""
        return f"{type_desc}{party_desc}"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将节点转换为可序列化的字典
        
        重构思路：
        - 保持原有的序列化接口
        - 正确处理枚举类型的序列化
        - 确保所有属性的正确序列化
        
        返回值：
            Dict[str, Any]: 节点的字典表示
        """
        # 处理参数中的枚举类型
        serializable_params = {}
        for key, value in self.params.items():
            if hasattr(value, 'value'):  # 枚举类型
                serializable_params[key] = value.value
            else:
                serializable_params[key] = value
        
        return {
            "node_id": self.node_id,
            "node_type": self.node_type.value,
            "params": serializable_params,
            "party": self.party.value if self.party else None,
            "position": self.position,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Node':
        """
        从字典创建节点
        
        重构思路：
        - 保持原有的反序列化接口
        - 正确处理枚举类型的反序列化
        - 确保创建对象的有效性
        
        参数：
            data: 节点数据字典
            
        返回值：
            Node: 节点实例
            
        异常：
            ValueError: 数据格式错误时抛出
        """
        # 处理枚举类型的反序列化
        params = data.get("params", {}).copy()
        if "party" in params and isinstance(params["party"], str):
            try:
                params["party"] = Party(params["party"])
            except ValueError:
                params["party"] = Party.UNKNOWN
        
        party = None
        if data.get("party"):
            try:
                party = Party(data["party"])
            except ValueError:
                party = Party.UNKNOWN
        
        return cls(
            node_id=data["node_id"],
            node_type=NodeType(data["node_type"]),
            params=params,
            party=party,
            position=data.get("position", (0.0, 0.0)),
            metadata=data.get("metadata", {})
        )
    
    def __str__(self) -> str:
        """
        字符串表示
        
        重构思路：
        - 保持原有的字符串表示格式
        - 提供更多有用信息
        - 便于调试和日志记录
        
        返回值：
            str: 节点的字符串表示
        """
        party_str = f", {self.party.value}" if self.party != Party.UNKNOWN else ""
        return f"Node({self.node_id}, {self.node_type.value}{party_str})"
    
    def __repr__(self) -> str:
        """
        详细字符串表示
        
        返回值：
            str: 节点的详细字符串表示
        """
        return f"Node(id={self.node_id}, type={self.node_type.value}, party={self.party.value if self.party else 'None'}, params={len(self.params)} items)"
    
    def __eq__(self, other) -> bool:
        """
        节点的相等性比较
        
        参数：
            other: 另一个节点对象
            
        返回值：
            bool: 是否相等
        """
        if not isinstance(other, Node):
            return False
        
        return self.node_id == other.node_id
    
    def __hash__(self) -> int:
        """
        节点的哈希值计算
        
        返回值：
            int: 哈希值
        """
        return hash(self.node_id)


class ProtocolGraph:
    """
    协议图类 - 重构版本
    
    重构思路：
    - 保持原有ProtocolGraph类的接口兼容性
    - 简化了图管理逻辑，提高性能
    - 优化了节点和边的操作机制
    - 改进了统计信息和序列化功能
    
    设计改进：
    - 使用NetworkX作为底层图存储
    - 统一的节点和边管理接口
    - 高效的DAG验证机制
    - 完善的统计信息计算
    
    核心功能：
    - 协议图的创建和管理
    - 节点和边的增删改查
    - DAG约束的验证
    - 协议图的序列化
    """
    
    def __init__(self, name: str = "QKD_Protocol"):
        """
        初始化协议图
        
        重构思路：
        - 保持原有构造函数的接口
        - 简化了图的初始化逻辑
        - 优化了统计信息的管理
        
        参数：
            name: 协议图名称
        """
        self.name = name
        self.graph = nx.DiGraph()
        self.node_counter = 0  # 全局节点计数器
        
        # 节点和参与者统计缓存
        self._node_stats = {}
        self._party_stats = {}
        self._stats_dirty = True  # 标记统计信息是否需要更新
    
    def add_node(self,
                 node_type: NodeType,
                 params: Optional[Dict[str, Any]] = None,
                 party: Optional[Party] = None,
                 position: Optional[Tuple[float, float]] = None,
                 node_id: Optional[str] = None) -> str:
        """
        添加节点到协议图
        
        重构思路：
        - 保持原有add_node方法的接口
        - 简化了节点创建逻辑
        - 优化了ID生成机制
        - 改进了重复检查和验证
        
        参数：
            node_type: 节点类型
            params: 节点参数
            party: 参与者
            position: 节点位置
            node_id: 节点ID（可选，自动生成）
            
        返回值：
            str: 节点ID
            
        异常：
            ValueError: 节点ID已存在或参数无效
        """
        # 生成唯一节点ID
        if node_id is None:
            node_id = self._generate_node_id(node_type)
        
        # 检查节点ID是否已存在
        if self.has_node(node_id):
            raise ValueError(f"节点ID '{node_id}' 已存在")
        
        # 创建节点对象
        try:
            node = Node(
                node_id=node_id,
                node_type=node_type,
                params=params,
                party=party,
                position=position
            )
        except ValueError as e:
            raise ValueError(f"创建节点 '{node_id}' 失败: {e}")
        
        # 添加到图中
        self.graph.add_node(node_id, node=node)
        
        # 标记统计信息需要更新
        self._stats_dirty = True
        
        return node_id
    
    def _generate_node_id(self, node_type: NodeType) -> str:
        """
        生成唯一的节点ID
        
        重构思路：
        - 基于节点类型和计数器生成ID
        - 确保ID的唯一性和可读性
        - 支持调试和可视化
        
        参数：
            node_type: 节点类型
            
        返回值：
            str: 唯一的节点ID
        """
        base_id = f"{node_type.value.lower()}_{self.node_counter}"
        self.node_counter += 1
        
        # 确保ID唯一性（理论上不会重复，但保险起见）
        while self.has_node(base_id):
            base_id = f"{node_type.value.lower()}_{self.node_counter}"
            self.node_counter += 1
        
        return base_id
    
    def remove_node(self, node_id: str) -> bool:
        """
        从协议图中删除节点
        
        重构思路：
        - 保持原有remove_node方法的接口
        - 自动删除相关的边
        - 更新统计信息
        
        参数：
            node_id: 节点ID
            
        返回值：
            bool: 是否成功删除
        """
        if not self.has_node(node_id):
            return False
        
        # 删除节点（NetworkX会自动删除相关边）
        self.graph.remove_node(node_id)
        
        # 标记统计信息需要更新
        self._stats_dirty = True
        
        return True
    
    def add_edge(self,
                 source_id: str,
                 target_id: str,
                 edge_type: EdgeType = EdgeType.QF,
                 params: Optional[Dict[str, Any]] = None) -> bool:
        """
        添加边到协议图
        
        重构思路：
        - 保持原有add_edge方法的接口
        - 简化了边创建逻辑
        - 强化了DAG约束检查
        - 优化了参数验证
        
        参数：
            source_id: 源节点ID
            target_id: 目标节点ID
            edge_type: 边类型
            params: 边参数
            
        返回值：
            bool: 是否成功添加
            
        异常：
            ValueError: 创建环路或参数无效时抛出
        """
        # 检查节点是否存在
        if not self.has_node(source_id):
            raise ValueError(f"源节点 '{source_id}' 不存在")
        if not self.has_node(target_id):
            raise ValueError(f"目标节点 '{target_id}' 不存在")
        
        # 检查是否会形成环路
        if self._would_create_cycle(source_id, target_id):
            raise ValueError(f"添加边 {source_id} -> {target_id} 会形成环路")
        
        # 创建边对象
        try:
            edge = Edge(
                source_id=source_id,
                target_id=target_id,
                edge_type=edge_type,
                params=params
            )
        except ValueError as e:
            raise ValueError(f"创建边 {source_id} -> {target_id} 失败: {e}")
        
        # 添加边到图中
        self.graph.add_edge(source_id, target_id, edge=edge, edge_type=edge_type, params=params or {})
        
        return True
    
    def remove_edge(self, source_id: str, target_id: str) -> bool:
        """
        删除边
        
        重构思路：
        - 保持原有remove_edge方法的接口
        - 简化删除逻辑
        
        参数：
            source_id: 源节点ID
            target_id: 目标节点ID
            
        返回值：
            bool: 是否成功删除
        """
        if self.graph.has_edge(source_id, target_id):
            self.graph.remove_edge(source_id, target_id)
            return True
        return False
    
    def get_node(self, node_id: str) -> Optional[Node]:
        """
        获取节点
        
        重构思路：
        - 保持原有get_node方法的接口
        - 简化节点访问逻辑
        
        参数：
            node_id: 节点ID
            
        返回值：
            Optional[Node]: 节点实例或None
        """
        if self.has_node(node_id):
            return self.graph.nodes[node_id]["node"]
        return None
    
    def get_all_nodes(self) -> List[Node]:
        """
        获取所有节点
        
        重构思路：
        - 新增获取所有节点的便捷方法
        - 便于遍历和批量操作
        
        返回值：
            List[Node]: 所有节点的列表
        """
        return [node_data["node"] for node_id, node_data in self.graph.nodes(data=True)]
    
    def get_nodes_by_type(self, node_type: NodeType) -> List[Node]:
        """
        根据类型获取节点列表
        
        重构思路：
        - 保持原有get_nodes_by_type方法的接口
        - 优化查找性能
        
        参数：
            node_type: 节点类型
            
        返回值：
            List[Node]: 指定类型的节点列表
        """
        nodes = []
        for node_id, node_data in self.graph.nodes(data=True):
            node = node_data["node"]
            if node.node_type == node_type:
                nodes.append(node)
        return nodes
    
    def get_nodes_by_party(self, party: Party) -> List[Node]:
        """
        根据参与者获取节点列表
        
        重构思路：
        - 保持原有get_nodes_by_party方法的接口
        - 简化查找逻辑
        
        参数：
            party: 参与者
            
        返回值：
            List[Node]: 指定参与者的节点列表
        """
        nodes = []
        for node_id, node_data in self.graph.nodes(data=True):
            node = node_data["node"]
            if node.party == party:
                nodes.append(node)
        return nodes
    
    def get_neighbors(self, node_id: str, direction: str = "both") -> List[str]:
        """
        获取邻居节点
        
        重构思路：
        - 保持原有get_neighbors方法的接口
        - 支持不同方向的邻居查找
        
        参数：
            node_id: 节点ID
            direction: 方向 ("in", "out", "both")
            
        返回值：
            List[str]: 邻居节点ID列表
        """
        if not self.has_node(node_id):
            return []
        
        if direction == "in":
            return list(self.graph.predecessors(node_id))
        elif direction == "out":
            return list(self.graph.successors(node_id))
        else:  # both
            predecessors = set(self.graph.predecessors(node_id))
            successors = set(self.graph.successors(node_id))
            return list(predecessors | successors)
    
    def get_edges(self, node_id: str = None) -> List[Tuple[str, str, Dict]]:
        """
        获取边列表
        
        重构思路：
        - 保持原有get_edges方法的接口
        - 支持获取特定节点的边
        
        参数：
            node_id: 节点ID（可选）
            
        返回值：
            List[Tuple[str, str, Dict]]: 边列表
        """
        if node_id:
            edges = []
            # 获取入边
            for pred in self.graph.predecessors(node_id):
                edge_data = self.graph.edges[pred, node_id]
                edges.append((pred, node_id, edge_data))
            # 获取出边
            for succ in self.graph.successors(node_id):
                edge_data = self.graph.edges[node_id, succ]
                edges.append((node_id, succ, edge_data))
            return edges
        else:
            return list(self.graph.edges(data=True))
    
    def get_edge_data(self, source_id: str, target_id: str) -> Optional[Dict[str, Any]]:
        """
        获取边的数据
        
        重构思路：
        - 新增获取边数据的便捷方法
        - 便于边属性的访问
        
        参数：
            source_id: 源节点ID
            target_id: 目标节点ID
            
        返回值：
            Optional[Dict[str, Any]]: 边数据或None
        """
        if self.has_edge(source_id, target_id):
            return self.graph.edges[source_id, target_id]
        return None
    
    def has_node(self, node_id: str) -> bool:
        """
        检查节点是否存在
        
        重构思路：
        - 保持原有has_node方法的接口
        
        参数：
            node_id: 节点ID
            
        返回值：
            bool: 节点是否存在
        """
        return self.graph.has_node(node_id)
    
    def has_edge(self, source_id: str, target_id: str) -> bool:
        """
        检查边是否存在
        
        重构思路：
        - 保持原有has_edge方法的接口
        
        参数：
            source_id: 源节点ID
            target_id: 目标节点ID
            
        返回值：
            bool: 边是否存在
        """
        return self.graph.has_edge(source_id, target_id)
    
    def get_node_count(self) -> int:
        """
        获取节点数量
        
        重构思路：
        - 保持原有get_node_count方法的接口
        
        返回值：
            int: 节点数量
        """
        return self.graph.number_of_nodes()
    
    def get_edge_count(self) -> int:
        """
        获取边数量
        
        重构思路：
        - 保持原有get_edge_count方法的接口
        
        返回值：
            int: 边数量
        """
        return self.graph.number_of_edges()
    
    def is_dag(self) -> bool:
        """
        检查是否为有向无环图
        
        重构思路：
        - 保持原有is_dag方法的接口
        - 使用NetworkX的高效实现
        
        返回值：
            bool: 是否为DAG
        """
        return nx.is_directed_acyclic_graph(self.graph)
    
    def get_topological_order(self) -> List[str]:
        """
        获取图的拓扑排序
        
        重构思路：
        - 保持原有get_topological_order方法的接口
        - 使用NetworkX的高效算法
        
        返回值：
            List[str]: 拓扑排序的节点ID列表
            
        异常：
            ValueError: 图不是DAG时抛出
        """
        if not self.is_dag():
            raise ValueError("图不是有向无环图（DAG），无法进行拓扑排序")
        return list(nx.topological_sort(self.graph))
    
    def find_first_node_by_type(self, node_type: NodeType) -> Optional[Node]:
        """
        按拓扑顺序查找第一个指定类型的节点
        
        重构思路：
        - 保持原有find_first_node_by_type方法的接口
        - 结合拓扑排序和类型查找
        
        参数：
            node_type: 节点类型
            
        返回值：
            Optional[Node]: 找到的节点或None
        """
        try:
            for node_id in self.get_topological_order():
                node = self.get_node(node_id)
                if node and node.node_type == node_type:
                    return node
        except ValueError:
            # 如果不是DAG，则按任意顺序查找
            for node in self.get_all_nodes():
                if node.node_type == node_type:
                    return node
        return None
    
    def _would_create_cycle(self, source_id: str, target_id: str) -> bool:
        """
        检查添加边是否会形成环路
        
        重构思路：
        - 保持原有的环路检查逻辑
        - 使用NetworkX的高效实现
        
        参数：
            source_id: 源节点ID
            target_id: 目标节点ID
            
        返回值：
            bool: 是否会形成环路
        """
        # 创建临时图进行测试
        temp_graph = self.graph.copy()
        temp_graph.add_edge(source_id, target_id)
        return not nx.is_directed_acyclic_graph(temp_graph)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取协议图统计信息
        
        重构思路：
        - 保持原有get_statistics方法的接口
        - 使用缓存机制提高性能
        - 扩展统计信息的内容
        
        返回值：
            Dict[str, Any]: 统计信息字典
        """
        # 如果统计信息需要更新，重新计算
        if self._stats_dirty:
            self._update_statistics()
        
        return {
            "name": self.name,
            "node_count": self.get_node_count(),
            "edge_count": self.get_edge_count(),
            "is_dag": self.is_dag(),
            "node_stats": self._node_stats.copy(),
            "party_stats": self._party_stats.copy(),
            "edge_types": self._get_edge_type_stats(),
            "density": self._calculate_graph_density(),
            "avg_degree": self._calculate_average_degree()
        }
    
    def _update_statistics(self):
        """
        更新统计信息缓存
        
        重构思路：
        - 分离统计计算逻辑
        - 避免重复计算
        - 提高查询性能
        """
        # 重置统计信息
        self._node_stats = {}
        self._party_stats = {}
        
        # 统计节点类型和参与者
        for node in self.get_all_nodes():
            # 节点类型统计
            node_type_key = node.node_type.value
            self._node_stats[node_type_key] = self._node_stats.get(node_type_key, 0) + 1
            
            # 参与者统计
            if node.party:
                party_key = node.party.value
                self._party_stats[party_key] = self._party_stats.get(party_key, 0) + 1
        
        # 标记统计信息已更新
        self._stats_dirty = False
    
    def _get_edge_type_stats(self) -> Dict[str, int]:
        """
        获取边类型统计
        
        返回值：
            Dict[str, int]: 边类型统计字典
        """
        edge_stats = {}
        for _, _, edge_data in self.graph.edges(data=True):
            edge_type = edge_data.get("edge_type", EdgeType.QF)
            if hasattr(edge_type, 'value'):
                edge_type_key = edge_type.value
            else:
                edge_type_key = str(edge_type)
            edge_stats[edge_type_key] = edge_stats.get(edge_type_key, 0) + 1
        return edge_stats
    
    def _calculate_graph_density(self) -> float:
        """
        计算图的密度
        
        返回值：
            float: 图的密度（0-1之间）
        """
        node_count = self.get_node_count()
        if node_count <= 1:
            return 0.0
        
        max_edges = node_count * (node_count - 1)  # 有向图的最大边数
        actual_edges = self.get_edge_count()
        return actual_edges / max_edges if max_edges > 0 else 0.0
    
    def _calculate_average_degree(self) -> float:
        """
        计算平均度数
        
        返回值：
            float: 平均度数
        """
        node_count = self.get_node_count()
        if node_count == 0:
            return 0.0
        
        total_degree = sum(self.graph.degree(node) for node in self.graph.nodes())
        return total_degree / node_count
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将协议图转换为字典表示
        
        重构思路：
        - 保持原有to_dict方法的接口
        - 确保所有数据的正确序列化
        - 支持完整的往返转换
        
        返回值：
            Dict[str, Any]: 协议图字典表示
        """
        # 序列化节点
        nodes = {}
        for node_id, node_data in self.graph.nodes(data=True):
            nodes[node_id] = node_data["node"].to_dict()
        
        # 序列化边
        edges = []
        for source, target, edge_data in self.graph.edges(data=True):
            edge_dict = {
                "source": source,
                "target": target,
                "edge_type": edge_data.get("edge_type", EdgeType.QF).value,
                "params": edge_data.get("params", {})
            }
            edges.append(edge_dict)
        
        return {
            "name": self.name,
            "nodes": nodes,
            "edges": edges,
            "metadata": {
                "node_counter": self.node_counter,
                "version": "2.0.0"  # 重构版本标识
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProtocolGraph':
        """
        从字典创建协议图
        
        重构思路：
        - 保持原有from_dict方法的接口
        - 正确处理所有数据的反序列化
        - 确保对象创建的有效性
        
        参数：
            data: 协议图数据字典
            
        返回值：
            ProtocolGraph: 协议图实例
            
        异常：
            ValueError: 数据格式错误时抛出
        """
        graph = cls(data.get("name", "QKD_Protocol"))
        
        # 恢复节点
        for node_id, node_data in data["nodes"].items():
            try:
                node = Node.from_dict(node_data)
                graph.graph.add_node(node_id, node=node)
            except Exception as e:
                raise ValueError(f"恢复节点 '{node_id}' 失败: {e}")
        
        # 恢复边
        for edge_data in data["edges"]:
            try:
                source = edge_data["source"]
                target = edge_data["target"]
                edge_type = EdgeType(edge_data["edge_type"])
                params = edge_data.get("params", {})
                
                # 创建边对象
                edge = Edge(source, target, edge_type, params)
                graph.graph.add_edge(source, target, edge=edge, edge_type=edge_type, params=params)
                
            except Exception as e:
                raise ValueError(f"恢复边 {edge_data.get('source', '?')} -> {edge_data.get('target', '?')} 失败: {e}")
        
        # 恢复元数据
        metadata = data.get("metadata", {})
        graph.node_counter = metadata.get("node_counter", 0)
        
        # 标记统计信息需要更新
        graph._stats_dirty = True
        
        return graph
    
    def save_to_file(self, filename: str):
        """
        保存协议图到文件
        
        重构思路：
        - 保持原有save_to_file方法的接口
        - 使用UTF-8编码确保中文支持
        - 格式化JSON输出便于阅读
        
        参数：
            filename: 文件名
            
        异常：
            IOError: 文件写入错误时抛出
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise IOError(f"Failed to save protocol graph to '{filename}': {e}")
    
    @classmethod
    def load_from_file(cls, filename: str) -> 'ProtocolGraph':
        """
        从文件加载协议图
        
        重构思路：
        - 保持原有load_from_file方法的接口
        - 使用UTF-8编码确保中文支持
        - 提供清晰的错误信息
        
        参数：
            filename: 文件名
            
        返回值：
            ProtocolGraph: 协议图实例
            
        异常：
            IOError: 文件读取错误时抛出
            ValueError: 文件格式错误时抛出
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return cls.from_dict(data)
        except FileNotFoundError:
            raise IOError(f"Protocol graph file '{filename}' not found")
        except json.JSONDecodeError as e:
            raise ValueError(f"文件 '{filename}' 的JSON格式无效: {e}")
        except Exception as e:
            raise IOError(f"Failed to load protocol graph from '{filename}': {e}")
    
    def clone(self) -> 'ProtocolGraph':
        """
        克隆协议图
        
        重构思路：
        - 新增协议图克隆的便捷方法
        - 通过序列化/反序列化实现深拷贝
        - 便于协议变体的创建
        
        返回值：
            ProtocolGraph: 克隆的协议图
        """
        return self.from_dict(self.to_dict())
    
    def merge(self, other: 'ProtocolGraph', prefix: str = "merged") -> 'ProtocolGraph':
        """
        合并两个协议图
        
        重构思路：
        - 新增协议图合并功能
        - 自动处理节点ID冲突
        - 支持复合协议的构建
        
        参数：
            other: 要合并的协议图
            prefix: 节点ID前缀（避免冲突）
            
        返回值：
            ProtocolGraph: 合并后的协议图
        """
        merged = self.clone()
        merged.name = f"{self.name}_merged_with_{other.name}"
        
        # 节点ID映射（处理冲突）
        id_mapping = {}
        
        # 添加其他图的节点
        for node in other.get_all_nodes():
            original_id = node.node_id
            new_id = f"{prefix}_{original_id}"
            
            # 确保新ID唯一
            counter = 0
            while merged.has_node(new_id):
                new_id = f"{prefix}_{original_id}_{counter}"
                counter += 1
            
            id_mapping[original_id] = new_id
            
            # 添加节点
            merged.add_node(
                node_type=node.node_type,
                params=node.params.copy(),
                party=node.party,
                position=node.position,
                node_id=new_id
            )
        
        # 添加其他图的边
        for source, target, edge_data in other.get_edges():
            new_source = id_mapping[source]
            new_target = id_mapping[target]
            edge_type = edge_data.get("edge_type", EdgeType.QF)
            params = edge_data.get("params", {})
            
            merged.add_edge(new_source, new_target, edge_type, params)
        
        return merged
    
    def __str__(self) -> str:
        """
        字符串表示
        
        重构思路：
        - 保持原有字符串表示格式
        - 提供有用的统计信息
        
        返回值：
            str: 协议图的字符串表示
        """
        stats = self.get_statistics()
        return f"ProtocolGraph({self.name}, nodes={stats['node_count']}, edges={stats['edge_count']}, DAG={stats['is_dag']})"
    
    def __repr__(self) -> str:
        """
        详细字符串表示
        
        返回值：
            str: 协议图的详细字符串表示
        """
        stats = self.get_statistics()
        return f"ProtocolGraph(name='{self.name}', nodes={stats['node_count']}, edges={stats['edge_count']}, types={list(stats['node_stats'].keys())})"