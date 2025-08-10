"""
DSL编译器模块

实现了QCGF DSL的编译功能，将协议图转换为可执行的仿真代码。
"""

import ast
from typing import Dict, List, Any, Optional, Tuple
from .protocol_graph import ProtocolGraph, Node
from .node_types import NodeType, Party
from .edge_types import EdgeType


class QCGFCompiler:
    """
    QCGF DSL编译器
    
    将ProtocolGraph对象编译为可执行的Python代码。
    """
    
    def __init__(self):
        """初始化编译器"""
        self.template_imports = [
            "import numpy as np",
            "import qiskit as qk",
            "from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister",
            "from qiskit.providers.aer import QasmSimulator",
            "from qiskit.quantum_info import Operator",
            "import networkx as nx",
            "from typing import Dict, List, Any, Optional"
        ]
        
        self.node_templates = {
            NodeType.QSP: self._compile_qsp_node,
            NodeType.QC: self._compile_qc_node,
            NodeType.QM: self._compile_qm_node,
            NodeType.QG: self._compile_qg_node,
            NodeType.QD: self._compile_qd_node,
            NodeType.CLO: self._compile_clo_node,
            NodeType.CS: self._compile_cs_node,
            NodeType.CC: self._compile_cc_node,
            NodeType.ATTACK: self._compile_attack_node,
            NodeType.SINK: self._compile_sink_node
        }
    
    def compile_protocol(self, protocol_graph: ProtocolGraph, 
                        target_language: str = "python") -> str:
        """
        编译协议图为可执行代码
        
        Args:
            protocol_graph: ProtocolGraph对象
            target_language: 目标语言（目前只支持python）
            
        Returns:
            编译后的代码字符串
        """
        if target_language.lower() != "python":
            raise ValueError(f"Unsupported target language: {target_language}")
        
        # 生成代码
        code_lines = []
        
        # 添加导入语句
        code_lines.extend(self.template_imports)
        code_lines.append("")
        
        # 添加类定义
        code_lines.append("class CompiledProtocol:")
        code_lines.append("    \"\"\"编译后的协议类\"\"\"")
        code_lines.append("")
        
        # 添加初始化方法
        code_lines.extend(self._compile_init_method(protocol_graph))
        code_lines.append("")
        
        # 添加节点方法
        code_lines.extend(self._compile_node_methods(protocol_graph))
        code_lines.append("")
        
        # 添加执行方法
        code_lines.extend(self._compile_execute_method(protocol_graph))
        code_lines.append("")
        
        # 添加主函数
        code_lines.extend(self._compile_main_function(protocol_graph))
        
        return '\n'.join(code_lines)
    
    def _compile_init_method(self, protocol_graph: ProtocolGraph) -> List[str]:
        """
        编译初始化方法
        
        Args:
            protocol_graph: ProtocolGraph对象
            
        Returns:
            初始化方法代码行列表
        """
        lines = [
            "    def __init__(self):",
            "        \"\"\"初始化协议\"\"\"",
            "        self.results = {}",
            "        self.quantum_circuit = None",
            "        self.classical_data = {}",
            "        self.simulation_results = {}"
        ]
        
        # 添加节点属性
        for node in protocol_graph.graph.nodes.values():
            node_data = protocol_graph.get_node(node)
            if node_data:
                lines.append(f"        self.{node_data.node_id} = None")
        
        lines.append("")
        return lines
    
    def _compile_node_methods(self, protocol_graph: ProtocolGraph) -> List[str]:
        """
        编译节点方法
        
        Args:
            protocol_graph: ProtocolGraph对象
            
        Returns:
            节点方法代码行列表
        """
        lines = []
        
        # 按拓扑顺序处理节点
        try:
            node_order = protocol_graph.get_topological_order()
        except:
            # 如果无法获取拓扑顺序，使用任意顺序
            node_order = list(protocol_graph.graph.nodes.keys())
        
        for node_id in node_order:
            node_data = protocol_graph.get_node(node_id)
            if node_data:
                method_lines = self.node_templates[node_data.node_type](node_data)
                lines.extend(method_lines)
                lines.append("")
        
        return lines
    
    def _compile_qsp_node(self, node: Node) -> List[str]:
        """
        编译量子态准备节点
        
        Args:
            node: 节点对象
            
        Returns:
            编译后的代码行列表
        """
        state = node.get_param("state", "|0⟩")
        fidelity = node.get_param("fidelity", 0.99)
        
        lines = [
            f"    def {node.node_id}(self):",
            f"        \"\"\"量子态准备: {state}\"\"\"",
            f"        # 创建量子寄存器",
            f"        qr = QuantumRegister(1, '{node.node_id}')",
            f"        cr = ClassicalRegister(1, '{node.node_id}_meas')",
            f"        qc = QuantumCircuit(qr, cr)",
            f"",
            f"        # 准备量子态",
        ]
        
        if state == "|0⟩":
            lines.append("        # |0⟩态是默认态，无需操作")
        elif state == "|1⟩":
            lines.append("        qc.x(qr[0])  # 应用X门得到|1⟩")
        elif state == "|+⟩":
            lines.append("        qc.h(qr[0])  # 应用H门得到|+⟩")
        elif state == "|-⟩":
            lines.append("        qc.x(qr[0])")
            lines.append("        qc.h(qr[0])  # 应用XH门得到|-⟩")
        else:
            lines.append(f"        # 自定义态: {state}")
            lines.append("        # 需要根据具体态实现相应的门序列")
        
        lines.extend([
            f"",
            f"        self.{node.node_id} = qc",
            f"        return qc"
        ])
        
        return lines
    
    def _compile_qc_node(self, node: Node) -> List[str]:
        """
        编译量子信道节点
        
        Args:
            node: 节点对象
            
        Returns:
            编译后的代码行列表
        """
        loss = node.get_param("loss", 0.1)
        noise = node.get_param("noise", 0.01)
        distance = node.get_param("distance", 50.0)
        
        lines = [
            f"    def {node.node_id}(self, input_circuit):",
            f"        \"\"\"量子信道: 损耗={loss}, 噪声={noise}, 距离={distance}km\"\"\"",
            f"        # 创建噪声模型",
            f"        from qiskit.providers.aer.noise import NoiseModel",
            f"        from qiskit.providers.aer.noise.errors import depolarizing_error",
            f"",
            f"        noise_model = NoiseModel()",
            f"        # 添加去极化噪声",
            f"        error = depolarizing_error({noise}, 1)",
            f"        noise_model.add_all_qubit_quantum_error(error, ['u1', 'u2', 'u3'])",
            f"",
            f"        # 应用损耗（简化模型）",
            f"        transmission_probability = 1 - {loss}",
            f"",
            f"        # 返回带噪声的电路",
            f"        self.{node.node_id} = input_circuit",
            f"        return input_circuit, noise_model, transmission_probability"
        ]
        
        return lines
    
    def _compile_qm_node(self, node: Node) -> List[str]:
        """
        编译量子测量节点
        
        Args:
            node: 节点对象
            
        Returns:
            编译后的代码行列表
        """
        basis = node.get_param("basis", "computational")
        efficiency = node.get_param("efficiency", 0.8)
        
        lines = [
            f"    def {node.node_id}(self, input_circuit):",
            f"        \"\"\"量子测量: 基={basis}, 效率={efficiency}\"\"\"",
            f"        # 复制输入电路",
            f"        measured_circuit = input_circuit.copy()",
            f"",
            f"        # 根据测量基选择测量方式",
        ]
        
        if basis == "computational":
            lines.extend([
                "        # 计算基测量",
                "        measured_circuit.measure_all()"
            ])
        elif basis == "bell":
            lines.extend([
                "        # Bell基测量",
                "        measured_circuit.h(0)",
                "        measured_circuit.cx(0, 1)",
                "        measured_circuit.measure_all()"
            ])
        else:
            lines.extend([
                f"        # 自定义基测量: {basis}",
                "        # 需要根据具体基实现相应的门序列",
                "        measured_circuit.measure_all()"
            ])
        
        lines.extend([
            f"",
            f"        self.{node.node_id} = measured_circuit",
            f"        return measured_circuit"
        ])
        
        return lines
    
    def _compile_qg_node(self, node: Node) -> List[str]:
        """
        编译量子门节点
        
        Args:
            node: 节点对象
            
        Returns:
            编译后的代码行列表
        """
        gate_type = node.get_param("gate_type", "H")
        fidelity = node.get_param("fidelity", 0.99)
        
        lines = [
            f"    def {node.node_id}(self, input_circuit, qubit_index=0):",
            f"        \"\"\"量子门: {gate_type}, 保真度={fidelity}\"\"\"",
            f"        # 复制输入电路",
            f"        gated_circuit = input_circuit.copy()",
            f"",
            f"        # 应用量子门",
        ]
        
        gate_operations = {
            "H": "gated_circuit.h(qubit_index)",
            "X": "gated_circuit.x(qubit_index)",
            "Y": "gated_circuit.y(qubit_index)",
            "Z": "gated_circuit.z(qubit_index)",
            "S": "gated_circuit.s(qubit_index)",
            "T": "gated_circuit.t(qubit_index)",
            "CNOT": "gated_circuit.cx(qubit_index, qubit_index + 1)",
            "SWAP": "gated_circuit.swap(qubit_index, qubit_index + 1)"
        }
        
        if gate_type in gate_operations:
            lines.append(f"        {gate_operations[gate_type]}")
        else:
            lines.extend([
                f"        # 自定义门: {gate_type}",
                "        # 需要根据具体门类型实现相应的操作"
            ])
        
        lines.extend([
            f"",
            f"        self.{node.node_id} = gated_circuit",
            f"        return gated_circuit"
        ])
        
        return lines
    
    def _compile_qd_node(self, node: Node) -> List[str]:
        """
        编译量子检测器节点
        
        Args:
            node: 节点对象
            
        Returns:
            编译后的代码行列表
        """
        detector_type = node.get_param("detector_type", "SPAD")
        efficiency = node.get_param("efficiency", 0.8)
        dark_count_rate = node.get_param("dark_count_rate", 1e-6)
        
        lines = [
            f"    def {node.node_id}(self, measurement_result):",
            f"        \"\"\"量子检测器: {detector_type}, 效率={efficiency}\"\"\"",
            f"        # 模拟检测器响应",
            f"        import random",
            f"",
            f"        # 应用检测效率",
            f"        if random.random() > {efficiency}:",
            f"            return None  # 检测失败",
            f"",
            f"        # 模拟暗计数",
            f"        if random.random() < {dark_count_rate}:",
            f"            return random.choice([0, 1])  # 随机暗计数",
            f"",
            f"        # 返回实际测量结果",
            f"        self.{node.node_id} = measurement_result",
            f"        return measurement_result"
        ]
        
        return lines
    
    def _compile_clo_node(self, node: Node) -> List[str]:
        """
        编译经典逻辑操作节点
        
        Args:
            node: 节点对象
            
        Returns:
            编译后的代码行列表
        """
        operation = node.get_param("operation", "XOR")
        
        lines = [
            f"    def {node.node_id}(self, *inputs):",
            f"        \"\"\"经典逻辑操作: {operation}\"\"\"",
            f"        # 执行逻辑操作",
        ]
        
        if operation == "XOR":
            lines.extend([
                "        result = 0",
                "        for input_val in inputs:",
                "            result ^= input_val",
                "        return result"
            ])
        elif operation == "AND":
            lines.extend([
                "        result = 1",
                "        for input_val in inputs:",
                "            result &= input_val",
                "        return result"
            ])
        elif operation == "OR":
            lines.extend([
                "        result = 0",
                "        for input_val in inputs:",
                "            result |= input_val",
                "        return result"
            ])
        else:
            lines.extend([
                f"        # 自定义操作: {operation}",
                "        # 需要根据具体操作实现相应的逻辑",
                "        return inputs[0] if inputs else 0"
            ])
        
        lines.extend([
            f"",
            f"        self.{node.node_id} = result",
            f"        return result"
        ])
        
        return lines
    
    def _compile_cs_node(self, node: Node) -> List[str]:
        """
        编译经典存储节点
        
        Args:
            node: 节点对象
            
        Returns:
            编译后的代码行列表
        """
        storage_type = node.get_param("storage_type", "memory")
        capacity = node.get_param("capacity", 1000)
        
        lines = [
            f"    def {node.node_id}(self, data):",
            f"        \"\"\"经典存储: {storage_type}, 容量={capacity}\"\"\"",
            f"        # 存储数据",
            f"        if not hasattr(self, '_{node.node_id}_storage'):",
            f"            self._{node.node_id}_storage = []",
            f"",
            f"        # 检查容量",
            f"        if len(self._{node.node_id}_storage) >= {capacity}:",
            f"            # 移除最旧的数据",
            f"            self._{node.node_id}_storage.pop(0)",
            f"",
            f"        # 添加新数据",
            f"        self._{node.node_id}_storage.append(data)",
            f"        self.{node.node_id} = data",
            f"        return data"
        ]
        
        return lines
    
    def _compile_cc_node(self, node: Node) -> List[str]:
        """
        编译经典信道节点
        
        Args:
            node: 节点对象
            
        Returns:
            编译后的代码行列表
        """
        bandwidth = node.get_param("bandwidth", 1e9)
        latency = node.get_param("latency", 1e-6)
        error_rate = node.get_param("error_rate", 1e-9)
        
        lines = [
            f"    def {node.node_id}(self, data):",
            f"        \"\"\"经典信道: 带宽={bandwidth}, 延迟={latency}\"\"\"",
            f"        import random",
            f"        import time",
            f"",
            f"        # 模拟传输延迟",
            f"        time.sleep({latency})",
            f"",
            f"        # 模拟传输错误",
            f"        if random.random() < {error_rate}:",
            f"            # 传输错误，返回None",
            f"            return None",
            f"",
            f"        # 成功传输",
            f"        self.{node.node_id} = data",
            f"        return data"
        ]
        
        return lines
    
    def _compile_attack_node(self, node: Node) -> List[str]:
        """
        编译攻击节点
        
        Args:
            node: 节点对象
            
        Returns:
            编译后的代码行列表
        """
        attack_type = node.get_param("attack_type", "intercept_resend")
        intercept_probability = node.get_param("intercept_probability", 0.5)
        
        lines = [
            f"    def {node.node_id}(self, quantum_data):",
            f"        \"\"\"攻击节点: {attack_type}, 截获概率={intercept_probability}\"\"\"",
            f"        import random",
            f"",
            f"        # 模拟攻击",
            f"        if random.random() < {intercept_probability}:",
            f"            # 成功截获",
            f"            if '{attack_type}' == 'intercept_resend':",
            f"                # 截获重发攻击",
            f"                # 随机测量并重发",
            f"                measured_basis = random.choice(['computational', 'hadamard'])",
            f"                # 这里简化处理，实际需要根据测量基进行测量",
            f"                return quantum_data  # 简化：直接返回原数据",
            f"            else:",
            f"                # 其他攻击类型",
            f"                return quantum_data",
            f"        else:",
            f"            # 攻击失败，数据正常传输",
            f"            return quantum_data"
        ]
        
        return lines
    
    def _compile_sink_node(self, node: Node) -> List[str]:
        """
        编译汇聚节点
        
        Args:
            node: 节点对象
            
        Returns:
            编译后的代码行列表
        """
        sink_type = node.get_param("sink_type", "key_generation")
        
        lines = [
            f"    def {node.node_id}(self, *inputs):",
            f"        \"\"\"汇聚节点: {sink_type}\"\"\"",
            f"        # 处理输入数据",
            f"        if '{sink_type}' == 'key_generation':",
            f"            # 密钥生成",
            f"            key_data = list(inputs)",
            f"            # 这里可以添加密钥后处理步骤",
            f"            final_key = ''.join(map(str, key_data))",
            f"            self.{node.node_id} = final_key",
            f"            return final_key",
            f"        else:",
            f"            # 其他汇聚类型",
            f"            result = list(inputs)",
            f"            self.{node.node_id} = result",
            f"            return result"
        ]
        
        return lines
    
    def _compile_execute_method(self, protocol_graph: ProtocolGraph) -> List[str]:
        """
        编译执行方法
        
        Args:
            protocol_graph: ProtocolGraph对象
            
        Returns:
            执行方法代码行列表
        """
        lines = [
            "    def execute(self):",
            "        \"\"\"执行协议\"\"\"",
            "        print(f\"执行协议: {protocol_graph.name}\")",
            "        ",
            "        # 按拓扑顺序执行节点",
        ]
        
        try:
            node_order = protocol_graph.get_topological_order()
        except:
            node_order = list(protocol_graph.graph.nodes.keys())
        
        for node_id in node_order:
            node_data = protocol_graph.get_node(node_id)
            if node_data:
                lines.append(f"        # 执行节点: {node_id}")
                lines.append(f"        self.{node_id}()")
                lines.append("")
        
        lines.extend([
            "        print(\"协议执行完成\")",
            "        return self.results"
        ])
        
        return lines
    
    def _compile_main_function(self, protocol_graph: ProtocolGraph) -> List[str]:
        """
        编译主函数
        
        Args:
            protocol_graph: ProtocolGraph对象
            
        Returns:
            主函数代码行列表
        """
        lines = [
            "",
            "def main():",
            "    \"\"\"主函数\"\"\"",
            f"    protocol = CompiledProtocol()",
            "    results = protocol.execute()",
            "    print(f\"执行结果: {results}\")",
            "    return results",
            "",
            "",
            "if __name__ == \"__main__\":",
            "    main()"
        ]
        
        return lines


# 便捷函数
def compile_protocol(protocol_graph: ProtocolGraph, target_language: str = "python") -> str:
    """
    编译协议图的便捷函数
    
    Args:
        protocol_graph: ProtocolGraph对象
        target_language: 目标语言
        
    Returns:
        编译后的代码字符串
    """
    compiler = QCGFCompiler()
    return compiler.compile_protocol(protocol_graph, target_language)


def compile_to_file(protocol_graph: ProtocolGraph, filename: str, 
                   target_language: str = "python"):
    """
    编译协议图到文件的便捷函数
    
    Args:
        protocol_graph: ProtocolGraph对象
        filename: 输出文件路径
        target_language: 目标语言
    """
    code = compile_protocol(protocol_graph, target_language)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(code) 