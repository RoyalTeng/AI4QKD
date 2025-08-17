"""
AI4QKD - DSL解析器模块 (重构版)

重构思路：
- 参考GitHub master分支的parser.py实现思路
- 保持原有QCGFParser和QCGFSerializer类的接口兼容性
- 简化了DSL语法解析逻辑，提高解析性能
- 优化了序列化格式，增强可读性

设计原则：
- 清晰的DSL语法定义
- 高效的解析算法
- 完整的错误处理
- 优雅的序列化格式

主要改进：
- 简化了正则表达式的复杂度
- 优化了参数解析的性能
- 改进了错误信息的质量
- 统一了文件操作接口

作者: Claude (AI Assistant)
重构日期: 2025-08-17
参考版本: GitHub master分支 parser.py
"""

import re
import os
from typing import Dict, List, Any, Optional, Union, Tuple
from enum import Enum

from .protocol_graph import ProtocolGraph, Node
from .node_types import NodeType, Party
from .edge_types import EdgeType

# =============================================================================
# 重构说明: 此模块基于GitHub master分支的parser.py重构
# 重构日期: 2025-08-17
# 重构原因: 简化DSL解析逻辑，提高性能和可维护性
# 主要改进: 优化正则表达式，改进错误处理，简化序列化格式
# 参考文件: qcgf_dsl/parser.py
# =============================================================================


class QCGFParser:
    """
    QCGF DSL解析器 - 重构版本
    
    重构思路：
    - 保持原有QCGFParser类的接口兼容性
    - 简化了DSL语法的解析逻辑
    - 优化了正则表达式的性能
    - 改进了错误处理和报告机制
    
    设计改进：
    - 更清晰的语法规则定义
    - 高效的参数解析算法
    - 完善的错误定位和报告
    - 灵活的语法扩展支持
    
    DSL语法格式：
    - 节点定义: NodeType node_id: param1=value1, param2=value2
    - 边定义: source_id -> target_id [edge_type]: param1=value1
    - 注释: # 这是注释
    - 空行: 自动忽略
    """
    
    def __init__(self):
        """
        初始化解析器
        
        重构思路：
        - 简化了正则表达式的复杂度
        - 优化了匹配模式的性能
        - 提供更清晰的语法规则
        """
        # 节点定义的正则表达式
        # 格式: NodeType node_id: param1=value1, param2=value2
        self.node_regex = re.compile(
            r"^(?P<type>[A-Z_]+)\s+(?P<id>\w+)\s*(?::\s*(?P<params>.+))?$",
            re.IGNORECASE
        )
        
        # 边定义的正则表达式
        # 格式: source_id -> target_id [edge_type]: param1=value1
        self.edge_regex = re.compile(
            r"^(?P<source>\w+)\s*->\s*(?P<target>\w+)\s*\[(?P<type>\w+)\]\s*(?::\s*(?P<params>.+))?$",
            re.IGNORECASE
        )
        
        # 参数解析的正则表达式
        # 支持: key=value, key="value", key='value'
        self.param_regex = re.compile(
            r'(\w+)\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^,\s]+))',
            re.IGNORECASE
        )
        
        # 行号计数器（用于错误报告）
        self._current_line = 0
    
    def parse(self, text: str) -> ProtocolGraph:
        """
        解析协议文本
        
        重构思路：
        - 保持原有parse方法的接口
        - 简化了解析主循环逻辑
        - 改进了错误处理和报告
        - 优化了解析性能
        
        Args:
            text: 包含协议描述的DSL文本
            
        Returns:
            ProtocolGraph: 解析后的协议图
            
        Raises:
            ValueError: DSL语法错误时抛出
        """
        # 重置行号计数器
        self._current_line = 0
        
        # 创建协议图
        protocol = ProtocolGraph("Parsed_Protocol")
        
        # 预处理文本行
        lines = self._preprocess_lines(text)
        
        # 第一遍：解析节点定义
        self._parse_nodes(lines, protocol)
        
        # 第二遍：解析边定义
        self._parse_edges(lines, protocol)
        
        # 验证解析结果
        self._validate_protocol(protocol)
        
        return protocol
    
    def _preprocess_lines(self, text: str) -> List[Tuple[int, str]]:
        """
        预处理文本行
        
        重构思路：
        - 分离预处理逻辑，提高代码可读性
        - 统一处理注释、空行、行号
        - 便于错误定位和报告
        
        Args:
            text: 原始DSL文本
            
        Returns:
            List[Tuple[int, str]]: (行号, 有效行内容) 的列表
        """
        valid_lines = []
        
        for line_num, line in enumerate(text.splitlines(), 1):
            # 去除首尾空白
            line = line.strip()
            
            # 跳过空行和注释行
            if not line or line.startswith('#'):
                continue
            
            # 移除行尾注释
            comment_pos = line.find('#')
            if comment_pos >= 0:
                line = line[:comment_pos].strip()
            
            # 跳过处理后的空行
            if not line:
                continue
            
            valid_lines.append((line_num, line))
        
        return valid_lines
    
    def _parse_nodes(self, lines: List[Tuple[int, str]], protocol: ProtocolGraph):
        """
        解析节点定义
        
        重构思路：
        - 分离节点解析逻辑
        - 提供详细的错误定位
        - 支持灵活的参数格式
        
        Args:
            lines: 预处理后的文本行
            protocol: 协议图对象
            
        Raises:
            ValueError: 节点定义语法错误时抛出
        """
        for line_num, line in lines:
            self._current_line = line_num
            
            node_match = self.node_regex.match(line)
            if node_match:
                try:
                    self._parse_single_node(node_match, protocol)
                except Exception as e:
                    raise ValueError(f"Line {line_num}: Failed to parse node - {e}")
    
    def _parse_single_node(self, match: re.Match, protocol: ProtocolGraph):
        """
        解析单个节点定义
        
        Args:
            match: 正则匹配结果
            protocol: 协议图对象
        """
        # 提取匹配的组
        node_type_str = match.group("type")
        node_id = match.group("id")
        params_str = match.group("params")
        
        # 解析节点类型
        try:
            node_type = NodeType(node_type_str.upper())
        except ValueError:
            raise ValueError(f"Unknown node type: {node_type_str}")
        
        # 解析参数
        params = self._parse_params(params_str) if params_str else {}
        
        # 提取参与者信息
        party = None
        if "party" in params:
            party_str = params["party"]
            if isinstance(party_str, str):
                try:
                    party = Party(party_str)
                except ValueError:
                    raise ValueError(f"Unknown party: {party_str}")
        
        # 添加节点到协议图
        protocol.add_node(
            node_type=node_type,
            params=params,
            party=party,
            node_id=node_id
        )
    
    def _parse_edges(self, lines: List[Tuple[int, str]], protocol: ProtocolGraph):
        """
        解析边定义
        
        重构思路：
        - 分离边解析逻辑
        - 验证节点存在性
        - 支持边参数定义
        
        Args:
            lines: 预处理后的文本行
            protocol: 协议图对象
            
        Raises:
            ValueError: 边定义语法错误时抛出
        """
        for line_num, line in lines:
            self._current_line = line_num
            
            edge_match = self.edge_regex.match(line)
            if edge_match:
                try:
                    self._parse_single_edge(edge_match, protocol)
                except Exception as e:
                    raise ValueError(f"Line {line_num}: Failed to parse edge - {e}")
    
    def _parse_single_edge(self, match: re.Match, protocol: ProtocolGraph):
        """
        解析单个边定义
        
        Args:
            match: 正则匹配结果
            protocol: 协议图对象
        """
        # 提取匹配的组
        source_id = match.group("source")
        target_id = match.group("target")
        edge_type_str = match.group("type")
        params_str = match.group("params")
        
        # 验证节点存在
        if not protocol.has_node(source_id):
            raise ValueError(f"Source node '{source_id}' not found")
        if not protocol.has_node(target_id):
            raise ValueError(f"Target node '{target_id}' not found")
        
        # 解析边类型
        try:
            edge_type = EdgeType(edge_type_str.lower())
        except ValueError:
            raise ValueError(f"Unknown edge type: {edge_type_str}")
        
        # 解析参数
        params = self._parse_params(params_str) if params_str else {}
        
        # 添加边到协议图
        protocol.add_edge(
            source_id=source_id,
            target_id=target_id,
            edge_type=edge_type,
            params=params
        )
    
    def _parse_params(self, params_str: str) -> Dict[str, Any]:
        """
        解析参数字符串
        
        重构思路：
        - 保持原有参数解析的兼容性
        - 支持多种参数值格式
        - 自动类型转换和验证
        - 改进错误处理
        
        Args:
            params_str: 参数字符串
            
        Returns:
            Dict[str, Any]: 解析后的参数字典
            
        Raises:
            ValueError: 参数格式错误时抛出
        """
        if not params_str:
            return {}
        
        params = {}
        
        # 使用正则表达式查找所有参数
        for match in self.param_regex.finditer(params_str):
            key = match.group(1)
            
            # 提取参数值（支持引号包围的值）
            value = match.group(2) or match.group(3) or match.group(4)
            
            if value is None:
                continue
            
            # 尝试自动类型转换
            try:
                params[key] = self._convert_param_value(value)
            except Exception as e:
                raise ValueError(f"Invalid parameter {key}={value}: {e}")
        
        return params
    
    def _convert_param_value(self, value: str) -> Any:
        """
        转换参数值的类型
        
        重构思路：
        - 自动识别和转换常见类型
        - 支持布尔值、数值、字符串
        - 提供合理的默认转换逻辑
        
        Args:
            value: 字符串格式的参数值
            
        Returns:
            Any: 转换后的参数值
        """
        # 去除首尾空白
        value = value.strip()
        
        # 布尔值转换
        if value.lower() in ('true', 'yes', '1', 'on'):
            return True
        elif value.lower() in ('false', 'no', '0', 'off'):
            return False
        
        # 数值转换
        try:
            # 尝试整数转换
            if '.' not in value and 'e' not in value.lower():
                return int(value)
            # 尝试浮点数转换
            else:
                return float(value)
        except ValueError:
            pass
        
        # 特殊值处理
        if value.lower() in ('null', 'none'):
            return None
        
        # 默认返回字符串
        return value
    
    def _validate_protocol(self, protocol: ProtocolGraph):
        """
        验证解析后的协议图
        
        重构思路：
        - 分离验证逻辑，提高代码清晰度
        - 检查协议图的基本完整性
        - 提供有用的验证信息
        
        Args:
            protocol: 协议图对象
            
        Raises:
            ValueError: 协议图不完整或无效时抛出
        """
        # 检查协议图是否为空
        if protocol.get_node_count() == 0:
            raise ValueError("Protocol graph is empty - no nodes defined")
        
        # 检查是否为DAG
        if not protocol.is_dag():
            raise ValueError("Protocol graph contains cycles - not a valid DAG")
        
        # 检查是否有孤立节点（可选警告）
        isolated_nodes = []
        for node in protocol.get_all_nodes():
            neighbors = protocol.get_neighbors(node.node_id)
            if not neighbors:
                isolated_nodes.append(node.node_id)
        
        if isolated_nodes:
            print(f"Warning: Found isolated nodes: {isolated_nodes}")
    
    def parse_from_file(self, filepath: str) -> ProtocolGraph:
        """
        从文件解析协议
        
        重构思路：
        - 保持原有parse_from_file方法的接口
        - 使用UTF-8编码确保中文支持
        - 提供详细的文件错误信息
        
        Args:
            filepath: 文件路径
            
        Returns:
            ProtocolGraph: 解析后的协议图
            
        Raises:
            IOError: 文件读取错误时抛出
            ValueError: 文件格式错误时抛出
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # 解析文本内容
            protocol = self.parse(text)
            
            # 设置协议名称为文件名（去除扩展名）
            filename = os.path.basename(filepath)
            protocol_name = os.path.splitext(filename)[0]
            protocol.name = protocol_name
            
            return protocol
            
        except FileNotFoundError:
            raise IOError(f"Protocol file '{filepath}' not found")
        except UnicodeDecodeError as e:
            raise IOError(f"Failed to decode file '{filepath}': {e}")
        except Exception as e:
            if isinstance(e, ValueError):
                raise ValueError(f"Error parsing file '{filepath}': {e}")
            else:
                raise IOError(f"Failed to read file '{filepath}': {e}")


class QCGFSerializer:
    """
    QCGF DSL序列化器 - 重构版本
    
    重构思路：
    - 保持原有QCGFSerializer类的接口兼容性
    - 优化了序列化格式的可读性
    - 改进了参数格式化逻辑
    - 支持美观的DSL输出
    
    设计改进：
    - 更清晰的DSL文本布局
    - 统一的参数格式化规则
    - 完善的注释和文档
    - 支持自定义格式选项
    
    序列化格式：
    - 协议头部注释
    - 节点定义区块
    - 边定义区块
    - 统计信息注释
    """
    
    def __init__(self, format_options: Optional[Dict[str, Any]] = None):
        """
        初始化序列化器
        
        重构思路：
        - 支持格式化选项的自定义
        - 提供合理的默认格式设置
        - 便于扩展和定制
        
        Args:
            format_options: 格式化选项字典
        """
        self.format_options = format_options or {}
        
        # 默认格式化选项
        self.default_options = {
            "include_header": True,        # 包含协议头部信息
            "include_statistics": True,    # 包含统计信息
            "sort_nodes": True,           # 对节点排序
            "sort_edges": True,           # 对边排序
            "indent_params": True,        # 参数缩进对齐
            "group_by_type": False,       # 按类型分组节点
            "add_descriptions": True      # 添加类型描述注释
        }
        
        # 合并用户选项和默认选项
        self.options = {**self.default_options, **self.format_options}
    
    def serialize(self, protocol: ProtocolGraph) -> str:
        """
        序列化协议图为DSL文本
        
        重构思路：
        - 保持原有serialize方法的接口
        - 优化了序列化格式的布局
        - 改进了可读性和结构化
        - 支持多种格式化选项
        
        Args:
            protocol: ProtocolGraph实例
            
        Returns:
            str: 协议的DSL文本表示
        """
        lines = []
        
        # 添加协议头部信息
        if self.options["include_header"]:
            lines.extend(self._generate_header(protocol))
            lines.append("")  # 空行分隔
        
        # 添加节点定义区块
        lines.extend(self._serialize_nodes(protocol))
        lines.append("")  # 空行分隔
        
        # 添加边定义区块
        lines.extend(self._serialize_edges(protocol))
        
        # 添加统计信息
        if self.options["include_statistics"]:
            lines.append("")  # 空行分隔
            lines.extend(self._generate_statistics(protocol))
        
        return '\n'.join(lines)
    
    def _generate_header(self, protocol: ProtocolGraph) -> List[str]:
        """
        生成协议头部信息
        
        重构思路：
        - 提供协议的基本信息
        - 包含生成时间和版本
        - 便于文档和追踪
        
        Args:
            protocol: 协议图对象
            
        Returns:
            List[str]: 头部信息行列表
        """
        import datetime
        
        lines = [
            f"# Protocol: {protocol.name}",
            f"# Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"# AI4QKD DSL v2.0 (Refactored)",
            "#"
        ]
        
        # 添加协议基本统计
        stats = protocol.get_statistics()
        lines.extend([
            f"# Nodes: {stats['node_count']} | Edges: {stats['edge_count']} | DAG: {stats['is_dag']}",
            f"# Node types: {', '.join(stats['node_stats'].keys())}",
            f"# Parties: {', '.join(stats['party_stats'].keys()) if stats['party_stats'] else 'None'}"
        ])
        
        return lines
    
    def _serialize_nodes(self, protocol: ProtocolGraph) -> List[str]:
        """
        序列化节点定义
        
        重构思路：
        - 支持多种节点排序方式
        - 优化参数格式化
        - 添加类型描述注释
        
        Args:
            protocol: 协议图对象
            
        Returns:
            List[str]: 节点定义行列表
        """
        lines = ["# Node Definitions"]
        
        # 获取所有节点
        nodes = protocol.get_all_nodes()
        
        # 对节点排序
        if self.options["sort_nodes"]:
            nodes.sort(key=lambda n: (n.node_type.value, n.node_id))
        
        # 按类型分组（可选）
        if self.options["group_by_type"]:
            return self._serialize_nodes_by_type(protocol, nodes)
        
        # 序列化每个节点
        for node in nodes:
            # 添加类型描述注释（可选）
            if self.options["add_descriptions"]:
                lines.append(f"# {node.get_description()}")
            
            # 生成节点定义行
            node_line = self._format_node_line(node)
            lines.append(node_line)
        
        return lines
    
    def _serialize_nodes_by_type(self, protocol: ProtocolGraph, nodes: List[Node]) -> List[str]:
        """
        按类型分组序列化节点
        
        Args:
            protocol: 协议图对象
            nodes: 节点列表
            
        Returns:
            List[str]: 分组后的节点定义行列表
        """
        lines = ["# Node Definitions (Grouped by Type)"]
        
        # 按节点类型分组
        type_groups = {}
        for node in nodes:
            node_type = node.node_type
            if node_type not in type_groups:
                type_groups[node_type] = []
            type_groups[node_type].append(node)
        
        # 按类型名称排序
        sorted_types = sorted(type_groups.keys(), key=lambda t: t.value)
        
        # 为每个类型生成定义
        for node_type in sorted_types:
            type_nodes = type_groups[node_type]
            
            # 添加类型组标题
            lines.append("")
            lines.append(f"# {node_type.value} Nodes - {node_type.get_description()}")
            
            # 对组内节点排序
            type_nodes.sort(key=lambda n: n.node_id)
            
            # 序列化组内节点
            for node in type_nodes:
                node_line = self._format_node_line(node)
                lines.append(node_line)
        
        return lines
    
    def _format_node_line(self, node: Node) -> str:
        """
        格式化单个节点定义行
        
        重构思路：
        - 统一的节点格式化规则
        - 优化参数对齐和可读性
        - 处理特殊字符和引号
        
        Args:
            node: 节点对象
            
        Returns:
            str: 格式化的节点定义行
        """
        # 基本格式: NodeType node_id
        line_parts = [node.node_type.value, node.node_id]
        
        # 获取需要序列化的参数
        params_to_serialize = self._get_serializable_params(node)
        
        # 格式化参数
        if params_to_serialize:
            param_str = self._format_params(params_to_serialize)
            line_parts.append(f": {param_str}")
        
        return " ".join(line_parts)
    
    def _get_serializable_params(self, node: Node) -> Dict[str, Any]:
        """
        获取需要序列化的参数
        
        重构思路：
        - 过滤默认参数，减少冗余
        - 确保重要参数的完整性
        - 处理枚举类型的序列化
        
        Args:
            node: 节点对象
            
        Returns:
            Dict[str, Any]: 需要序列化的参数
        """
        # 获取节点的默认模板
        from .node_types import get_node_template
        template = get_node_template(node.node_type)
        
        # 只序列化与默认值不同的参数
        serializable_params = {}
        
        for key, value in node.params.items():
            # 跳过与默认值相同的参数
            if key in template and template[key] == value:
                continue
            
            serializable_params[key] = value
        
        # 始终包含重要参数
        important_params = ["party", "state", "basis", "operation"]
        for param in important_params:
            if param in node.params:
                serializable_params[param] = node.params[param]
        
        # 确保party参数的正确性
        if node.party and node.party != Party.UNKNOWN:
            serializable_params["party"] = node.party.value
        
        return serializable_params
    
    def _serialize_edges(self, protocol: ProtocolGraph) -> List[str]:
        """
        序列化边定义
        
        重构思路：
        - 支持边的排序和分组
        - 优化边参数的格式化
        - 提供清晰的边类型标识
        
        Args:
            protocol: 协议图对象
            
        Returns:
            List[str]: 边定义行列表
        """
        lines = ["# Edge Definitions"]
        
        # 获取所有边
        edges = protocol.get_edges()
        
        # 对边排序
        if self.options["sort_edges"]:
            edges.sort(key=lambda e: (e[0], e[1]))  # 按源节点和目标节点排序
        
        # 序列化每条边
        for source, target, edge_data in edges:
            edge_line = self._format_edge_line(source, target, edge_data)
            lines.append(edge_line)
        
        return lines
    
    def _format_edge_line(self, source: str, target: str, edge_data: Dict[str, Any]) -> str:
        """
        格式化单个边定义行
        
        重构思路：
        - 统一的边格式化规则
        - 清晰的边类型标识
        - 合理的参数格式化
        
        Args:
            source: 源节点ID
            target: 目标节点ID
            edge_data: 边数据字典
            
        Returns:
            str: 格式化的边定义行
        """
        # 获取边类型
        edge_type = edge_data.get("edge_type", EdgeType.QUANTUM)
        if hasattr(edge_type, 'value'):
            edge_type_str = edge_type.value
        else:
            edge_type_str = str(edge_type)
        
        # 基本格式: source -> target [edge_type]
        line_parts = [source, "->", target, f"[{edge_type_str}]"]
        
        # 获取需要序列化的边参数
        params = edge_data.get("params", {})
        if params:
            param_str = self._format_params(params)
            line_parts.append(f": {param_str}")
        
        return " ".join(line_parts)
    
    def _format_params(self, params: Dict[str, Any]) -> str:
        """
        格式化参数字典为字符串
        
        重构思路：
        - 保持原有参数格式化的兼容性
        - 优化参数值的引号处理
        - 支持多种数据类型的格式化
        - 提供美观的排列方式
        
        Args:
            params: 参数字典
            
        Returns:
            str: 格式化的参数字符串
        """
        if not params:
            return ""
        
        param_parts = []
        
        # 对参数键排序，确保输出的一致性
        sorted_keys = sorted(params.keys())
        
        for key in sorted_keys:
            value = params[key]
            formatted_value = self._format_param_value(value)
            param_parts.append(f"{key}={formatted_value}")
        
        # 使用逗号和空格连接参数
        return ", ".join(param_parts)
    
    def _format_param_value(self, value: Any) -> str:
        """
        格式化单个参数值
        
        重构思路：
        - 处理各种数据类型的格式化
        - 智能添加引号
        - 处理枚举类型
        - 保持数值精度
        
        Args:
            value: 参数值
            
        Returns:
            str: 格式化的参数值字符串
        """
        # 处理None值
        if value is None:
            return "null"
        
        # 处理枚举类型
        if hasattr(value, 'value'):
            return f'"{value.value}"'
        
        # 处理布尔值
        if isinstance(value, bool):
            return "true" if value else "false"
        
        # 处理数值类型
        if isinstance(value, (int, float)):
            # 对于浮点数，保持合理的精度
            if isinstance(value, float):
                if value == float('inf'):
                    return "inf"
                elif value == float('-inf'):
                    return "-inf"
                else:
                    # 保留最多6位小数，去除尾随零
                    return f"{value:.6g}"
            else:
                return str(value)
        
        # 处理字符串类型
        if isinstance(value, str):
            # 如果字符串包含特殊字符或空格，使用引号
            if any(char in value for char in [' ', ',', '=', '"', "'", '#']):
                # 使用双引号，转义内部的双引号
                escaped_value = value.replace('"', '\\"')
                return f'"{escaped_value}"'
            else:
                return value
        
        # 处理其他类型，转换为字符串
        return f'"{str(value)}"'
    
    def _generate_statistics(self, protocol: ProtocolGraph) -> List[str]:
        """
        生成协议统计信息
        
        重构思路：
        - 提供有用的协议统计
        - 便于协议分析和调试
        - 格式化统计信息的展示
        
        Args:
            protocol: 协议图对象
            
        Returns:
            List[str]: 统计信息行列表
        """
        lines = ["# Protocol Statistics"]
        
        stats = protocol.get_statistics()
        
        # 基本统计
        lines.extend([
            f"# Total nodes: {stats['node_count']}",
            f"# Total edges: {stats['edge_count']}",
            f"# Is DAG: {stats['is_dag']}",
            f"# Graph density: {stats.get('density', 0):.3f}",
            f"# Average degree: {stats.get('avg_degree', 0):.2f}"
        ])
        
        # 节点类型统计
        if stats['node_stats']:
            lines.append("#")
            lines.append("# Node type distribution:")
            for node_type, count in stats['node_stats'].items():
                lines.append(f"#   {node_type}: {count}")
        
        # 参与者统计
        if stats['party_stats']:
            lines.append("#")
            lines.append("# Party distribution:")
            for party, count in stats['party_stats'].items():
                lines.append(f"#   {party}: {count}")
        
        # 边类型统计
        if stats.get('edge_types'):
            lines.append("#")
            lines.append("# Edge type distribution:")
            for edge_type, count in stats['edge_types'].items():
                lines.append(f"#   {edge_type}: {count}")
        
        return lines
    
    def serialize_to_file(self, protocol: ProtocolGraph, filepath: str):
        """
        序列化协议图到文件
        
        重构思路：
        - 保持原有serialize_to_file方法的接口
        - 使用UTF-8编码确保中文支持
        - 提供详细的文件错误信息
        
        Args:
            protocol: ProtocolGraph实例
            filepath: 输出文件路径
            
        Raises:
            IOError: 文件写入错误时抛出
        """
        try:
            # 序列化为DSL文本
            dsl_text = self.serialize(protocol)
            
            # 写入文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(dsl_text)
                
        except Exception as e:
            raise IOError(f"Failed to serialize protocol to '{filepath}': {e}")
    
    def set_format_option(self, key: str, value: Any):
        """
        设置格式化选项
        
        重构思路：
        - 提供动态修改格式化选项的接口
        - 便于定制序列化输出
        
        Args:
            key: 选项键
            value: 选项值
        """
        self.options[key] = value
    
    def get_format_options(self) -> Dict[str, Any]:
        """
        获取当前格式化选项
        
        Returns:
            Dict[str, Any]: 当前格式化选项
        """
        return self.options.copy()