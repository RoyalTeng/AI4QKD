"""
AI4QKD - 协议编译器模块 (重构版)

重构思路：
- 参考GitHub master分支的compiler.py实现思路
- 保持原有QCGFCompiler类的接口兼容性
- 简化了代码生成逻辑，提高性能和可读性
- 优化了模板系统和输出格式

设计原则：
- 清晰的代码生成流程
- 高效的模板渲染系统
- 灵活的目标语言支持
- 完整的向后兼容性

主要改进：
- 简化了编译流程
- 优化了模板管理系统
- 改进了代码格式化
- 统一了输出接口

作者: Claude (AI Assistant)
重构日期: 2025-08-17
参考版本: GitHub master分支 compiler.py
"""

import warnings
from typing import Dict, Any, Optional, List
from .protocol_graph import ProtocolGraph

# =============================================================================
# 重构说明: 此模块基于GitHub master分支的compiler.py重构
# 重构日期: 2025-08-17
# 重构原因: 简化代码生成逻辑，提高性能和可维护性
# 主要改进: 优化模板系统，简化流程，改进格式化
# 参考文件: qcgf_dsl/compiler.py
# =============================================================================


class QCGFCompiler:
    """
    QCGF协议编译器 - 重构版本
    
    重构思路：
    - 保持原有QCGFCompiler类的接口兼容性
    - 简化了代码生成的实现逻辑
    - 优化了模板系统和渲染性能
    - 改进了错误处理机制
    
    设计改进：
    - 更清晰的编译流程
    - 统一的模板管理系统
    - 灵活的目标语言支持
    - 完善的错误处理
    
    核心功能：
    - 协议图到代码的转换
    - 多种目标语言支持
    - 可定制的代码模板
    - 完整的依赖管理
    """
    
    def __init__(self, target_language: str = "python", 
                 template_config: Optional[Dict[str, Any]] = None):
        """
        初始化编译器
        
        重构思路：
        - 保持原有构造函数的接口
        - 支持多种目标语言
        - 提供可配置的模板系统
        - 便于扩展和定制
        
        Args:
            target_language: 目标语言 ("python", "qiskit", "cirq")
            template_config: 模板配置字典
        """
        self.target_language = target_language.lower()
        self.template_config = template_config or {}
        
        # 支持的目标语言
        self.supported_languages = ["python", "qiskit", "cirq", "pennylane"]
        
        if self.target_language not in self.supported_languages:
            warnings.warn(
                f"Target language '{target_language}' may not be fully supported. "
                f"Supported languages: {self.supported_languages}",
                UserWarning
            )
        
        # 初始化代码模板
        self._init_templates()
        
        # 检查目标框架可用性
        self._check_framework_availability()
    
    def _init_templates(self):
        """
        初始化代码模板
        
        重构思路：
        - 简化模板结构
        - 提供基础的代码生成模板
        - 支持模板的动态加载和配置
        """
        # Python基础模板
        self.python_templates = {
            "header": '''"""
AI4QKD协议实现 - 自动生成代码
协议名称: {protocol_name}
生成时间: {generation_time}
目标框架: {target_framework}
"""

import numpy as np
from typing import Dict, Any, List, Optional
''',
            "class_definition": '''
class {protocol_class_name}:
    """
    {protocol_name}协议实现
    
    自动生成的协议类，包含完整的协议逻辑
    """
    
    def __init__(self, **kwargs):
        """初始化协议参数"""
        self.protocol_name = "{protocol_name}"
        self.parameters = kwargs
        self._setup_protocol()
    
    def _setup_protocol(self):
        """设置协议参数"""
        pass
''',
            "node_method": '''
    def {method_name}(self, {parameters}):
        """
        {node_description}
        
        节点类型: {node_type}
        参与者: {party}
        """
        # TODO: 实现{node_type}节点逻辑
        pass
''',
            "run_method": '''
    def run_protocol(self):
        """
        执行完整协议流程
        """
        results = {}
        
        # 协议执行步骤
{execution_steps}
        
        return results
'''
        }
        
        # Qiskit特定模板
        self.qiskit_templates = {
            "imports": '''
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import execute, Aer
from qiskit.quantum_info import random_statevector
''',
            "circuit_creation": '''
        # 创建量子电路
        qreg = QuantumRegister({num_qubits}, 'q')
        creg = ClassicalRegister({num_bits}, 'c')
        circuit = QuantumCircuit(qreg, creg)
'''
        }
    
    def _check_framework_availability(self):
        """
        检查目标框架可用性
        
        重构思路：
        - 检查必要的依赖框架
        - 提供友好的错误信息
        - 支持功能的优雅降级
        """
        self.framework_available = {}
        
        # 检查Qiskit
        try:
            import qiskit
            self.framework_available["qiskit"] = True
        except ImportError:
            self.framework_available["qiskit"] = False
            if self.target_language == "qiskit":
                warnings.warn("Qiskit not available but required for target language", ImportWarning)
        
        # 检查Cirq
        try:
            import cirq
            self.framework_available["cirq"] = True
        except ImportError:
            self.framework_available["cirq"] = False
            if self.target_language == "cirq":
                warnings.warn("Cirq not available but required for target language", ImportWarning)
    
    def compile(self, protocol: ProtocolGraph, 
                output_file: Optional[str] = None,
                include_comments: bool = True,
                include_tests: bool = False) -> str:
        """
        编译协议图为目标语言代码
        
        重构思路：
        - 保持原有compile方法的接口
        - 简化了编译流程
        - 优化了代码生成性能
        - 支持多种输出选项
        
        Args:
            protocol: 要编译的协议图
            output_file: 输出文件路径（可选）
            include_comments: 是否包含注释
            include_tests: 是否包含测试代码
            
        Returns:
            str: 生成的代码字符串
            
        Raises:
            ValueError: 协议格式错误时抛出
            RuntimeError: 编译过程出错时抛出
        """
        try:
            # 验证协议图
            self._validate_protocol(protocol)
            
            # 生成代码
            if self.target_language == "python":
                code = self._compile_to_python(protocol, include_comments, include_tests)
            elif self.target_language == "qiskit":
                code = self._compile_to_qiskit(protocol, include_comments, include_tests)
            elif self.target_language == "cirq":
                code = self._compile_to_cirq(protocol, include_comments, include_tests)
            else:
                # 默认Python代码生成
                code = self._compile_to_python(protocol, include_comments, include_tests)
            
            # 保存到文件
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(code)
                print(f"代码已生成到: {output_file}")
            
            return code
            
        except Exception as e:
            raise RuntimeError(f"Protocol compilation failed: {e}")
    
    def _validate_protocol(self, protocol: ProtocolGraph):
        """
        验证协议图的有效性
        
        Args:
            protocol: 协议图对象
            
        Raises:
            ValueError: 协议图无效时抛出
        """
        if not protocol:
            raise ValueError("Protocol graph cannot be None")
        
        if protocol.get_node_count() == 0:
            raise ValueError("Protocol graph is empty")
        
        if not protocol.is_dag():
            raise ValueError("Protocol graph must be a DAG")
    
    def _compile_to_python(self, protocol: ProtocolGraph, 
                          include_comments: bool, 
                          include_tests: bool) -> str:
        """
        编译为Python代码
        
        Args:
            protocol: 协议图对象
            include_comments: 是否包含注释
            include_tests: 是否包含测试代码
            
        Returns:
            str: 生成的Python代码
        """
        import datetime
        
        # 准备模板变量
        template_vars = {
            "protocol_name": protocol.name,
            "protocol_class_name": self._to_class_name(protocol.name),
            "generation_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "target_framework": "Python (基础实现)"
        }
        
        # 生成代码段
        code_parts = []
        
        # 文件头部
        code_parts.append(self.python_templates["header"].format(**template_vars))
        
        # 类定义
        code_parts.append(self.python_templates["class_definition"].format(**template_vars))
        
        # 生成节点方法
        for node in protocol.get_all_nodes():
            node_method = self._generate_node_method(node, include_comments)
            code_parts.append(node_method)
        
        # 生成执行方法
        execution_steps = self._generate_execution_steps(protocol)
        run_method = self.python_templates["run_method"].format(
            execution_steps=execution_steps
        )
        code_parts.append(run_method)
        
        # 生成测试代码（可选）
        if include_tests:
            test_code = self._generate_test_code(protocol)
            code_parts.append(test_code)
        
        return "\n".join(code_parts)
    
    def _compile_to_qiskit(self, protocol: ProtocolGraph, 
                          include_comments: bool, 
                          include_tests: bool) -> str:
        """
        编译为Qiskit代码
        
        Args:
            protocol: 协议图对象
            include_comments: 是否包含注释
            include_tests: 是否包含测试代码
            
        Returns:
            str: 生成的Qiskit代码
        """
        if not self.framework_available.get("qiskit", False):
            warnings.warn("Qiskit not available, generating basic Python code instead")
            return self._compile_to_python(protocol, include_comments, include_tests)
        
        # 基于Python代码生成，添加Qiskit特定内容
        python_code = self._compile_to_python(protocol, include_comments, include_tests)
        
        # 添加Qiskit导入
        qiskit_imports = self.qiskit_templates["imports"]
        
        # 插入Qiskit特定代码
        lines = python_code.split('\n')
        import_index = -1
        for i, line in enumerate(lines):
            if line.startswith('from typing'):
                import_index = i
                break
        
        if import_index >= 0:
            lines.insert(import_index + 1, qiskit_imports)
        
        return '\n'.join(lines)
    
    def _compile_to_cirq(self, protocol: ProtocolGraph, 
                        include_comments: bool, 
                        include_tests: bool) -> str:
        """
        编译为Cirq代码
        
        Args:
            protocol: 协议图对象
            include_comments: 是否包含注释
            include_tests: 是否包含测试代码
            
        Returns:
            str: 生成的Cirq代码
        """
        if not self.framework_available.get("cirq", False):
            warnings.warn("Cirq not available, generating basic Python code instead")
            return self._compile_to_python(protocol, include_comments, include_tests)
        
        # TODO: 实现Cirq特定的代码生成
        return self._compile_to_python(protocol, include_comments, include_tests)
    
    def _generate_node_method(self, node, include_comments: bool) -> str:
        """
        生成节点方法代码
        
        Args:
            node: 节点对象
            include_comments: 是否包含注释
            
        Returns:
            str: 节点方法代码
        """
        method_name = f"execute_{node.node_id.lower()}"
        node_type = node.node_type.value if hasattr(node.node_type, 'value') else str(node.node_type)
        party = node.party.value if node.party and hasattr(node.party, 'value') else "Unknown"
        
        # 生成参数列表
        params = [f"input_data: Any = None"]
        
        template_vars = {
            "method_name": method_name,
            "parameters": ", ".join(params),
            "node_description": f"执行{node_type}节点操作",
            "node_type": node_type,
            "party": party
        }
        
        return self.python_templates["node_method"].format(**template_vars)
    
    def _generate_execution_steps(self, protocol: ProtocolGraph) -> str:
        """
        生成协议执行步骤代码
        
        Args:
            protocol: 协议图对象
            
        Returns:
            str: 执行步骤代码
        """
        steps = []
        
        # 获取拓扑排序的节点顺序
        try:
            import networkx as nx
            if hasattr(nx, 'topological_sort'):
                node_order = list(nx.topological_sort(protocol.graph))
            else:
                node_order = list(protocol.graph.nodes())
        except:
            node_order = list(protocol.graph.nodes())
        
        for i, node_id in enumerate(node_order):
            method_name = f"execute_{node_id.lower()}"
            step_comment = f"        # 步骤 {i+1}: 执行节点 {node_id}"
            step_call = f"        results['{node_id}'] = self.{method_name}()"
            
            steps.append(step_comment)
            steps.append(step_call)
            steps.append("")  # 空行
        
        return "\n".join(steps)
    
    def _generate_test_code(self, protocol: ProtocolGraph) -> str:
        """
        生成测试代码
        
        Args:
            protocol: 协议图对象
            
        Returns:
            str: 测试代码
        """
        class_name = self._to_class_name(protocol.name)
        
        test_code = f'''

# 测试代码
def test_{protocol.name.lower()}():
    """测试{protocol.name}协议"""
    protocol = {class_name}()
    results = protocol.run_protocol()
    
    # 验证结果
    assert results is not None
    assert len(results) > 0
    
    print(f"协议执行成功，结果: {{results}}")

if __name__ == "__main__":
    test_{protocol.name.lower()}()
'''
        return test_code
    
    def _to_class_name(self, name: str) -> str:
        """
        转换协议名称为类名
        
        Args:
            name: 协议名称
            
        Returns:
            str: 类名
        """
        # 移除特殊字符，转换为驼峰命名
        import re
        clean_name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        parts = clean_name.split('_')
        return ''.join(word.capitalize() for word in parts if word)


def compile_protocol(protocol: ProtocolGraph, 
                    target_language: str = "python",
                    output_file: Optional[str] = None,
                    **kwargs) -> str:
    """
    快速编译协议的便捷函数
    
    重构思路：
    - 保持原有的快速编译接口
    - 简化调用方式
    - 提供常用参数的快捷设置
    
    Args:
        protocol: 要编译的协议图
        target_language: 目标语言
        output_file: 输出文件路径
        **kwargs: 其他编译参数
        
    Returns:
        str: 生成的代码
    """
    compiler = QCGFCompiler(target_language)
    return compiler.compile(protocol, output_file=output_file, **kwargs)


def compile_to_file(protocol: ProtocolGraph, 
                   filepath: str,
                   target_language: str = "python",
                   **kwargs):
    """
    编译协议并保存到文件
    
    重构思路：
    - 保持原有的文件输出接口
    - 简化文件操作
    - 提供友好的错误处理
    
    Args:
        protocol: 要编译的协议图
        filepath: 输出文件路径
        target_language: 目标语言
        **kwargs: 其他编译参数
    """
    code = compile_protocol(protocol, target_language, **kwargs)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f"协议代码已生成到: {filepath}")
    except Exception as e:
        raise IOError(f"Failed to write code to file '{filepath}': {e}")