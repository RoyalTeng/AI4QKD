"""
AI4QKD - qcgf_dsl模块重构测试框架

重构思路：
- 参考GitHub master分支的tests/test_qcgf_dsl.py实现思路
- 保持原有接口的向后兼容性测试
- 新增简化后的功能优化测试
- 基于原有测试用例设计，确保不遗漏关键功能

设计原则：
- 测试驱动开发（TDD）：先写测试再实现
- 接口兼容性：确保重构后API与原版兼容
- 功能完整性：覆盖所有核心功能的测试
- 简化验证：测试简化后的实现是否正确工作

主要改进：
- 更清晰的测试用例组织结构
- 更全面的边界条件测试
- 更简洁的测试数据准备
- 更直观的断言验证

作者: Claude (AI Assistant)
重构日期: 2025-08-17
参考版本: GitHub master分支 tests/test_qcgf_dsl.py
"""

import pytest
import tempfile
import os
from typing import Dict, Any


# =============================================================================
# 重构说明: 此测试文件基于GitHub master分支的test_qcgf_dsl.py重构
# 重构日期: 2025-08-17
# 重构原因: 简化测试结构，提高测试覆盖率和可读性
# 主要改进: 更好的测试组织，更全面的边界测试，更清晰的断言
# 参考文件: tests/test_qcgf_dsl.py
# =============================================================================


class TestProtocolGraphRefactor:
    """
    协议图重构测试用例 - 基于原有ProtocolGraph接口
    
    重构思路：
    - 参考原有ProtocolGraph类的测试用例设计
    - 保持add_node, add_edge, remove_node等核心接口
    - 简化了测试数据的准备和验证逻辑
    - 新增了更多边界条件和异常处理测试
    
    设计改进：
    - 使用更清晰的fixture设计
    - 统一的节点/边测试模式
    - 更全面的统计信息验证
    
    核心测试范围：
    - 协议图的创建和基本属性
    - 节点的添加、删除、查找
    - 边的添加、删除、验证
    - DAG约束和拓扑排序
    - 统计信息和序列化
    """
    
    @pytest.fixture
    def empty_protocol(self):
        """
        空协议图fixture - 参考原有empty_graph
        
        重构思路：
        - 保持原有的空图创建接口
        - 简化了初始化参数
        """
        # TODO: 实现ProtocolGraph类后启用
        # from qcgf_dsl import ProtocolGraph
        # return ProtocolGraph("TestProtocol")
        return None
    
    @pytest.fixture  
    def sample_bb84_protocol(self):
        """
        BB84协议样例fixture - 基于原有sample_graph优化
        
        重构思路：
        - 参考原有的BB84测试协议结构
        - 使用标准的QSP->QC->QM流程
        - 简化了节点参数设置
        - 保持了原有的Alice-Bob通信模式
        """
        # TODO: 实现相关类后启用
        # from qcgf_dsl import ProtocolGraph, NodeType, Party, EdgeType
        # 
        # protocol = ProtocolGraph("BB84_Sample")
        # 
        # # Alice方：量子态准备
        # alice_qsp = protocol.add_node(
        #     node_type=NodeType.QSP,
        #     party=Party.ALICE, 
        #     params={"state": "|0⟩", "fidelity": 0.99}
        # )
        # 
        # # 量子信道：Alice到Bob
        # quantum_channel = protocol.add_node(
        #     node_type=NodeType.QC,
        #     params={"loss": 0.1, "noise": 0.01, "distance": 50.0}
        # )
        # 
        # # Bob方：量子测量
        # bob_qm = protocol.add_node(
        #     node_type=NodeType.QM,
        #     party=Party.BOB,
        #     params={"basis": "computational", "efficiency": 0.8}
        # )
        # 
        # # 连接节点：构建BB84通信流程
        # protocol.add_edge(alice_qsp, quantum_channel, EdgeType.QUANTUM)
        # protocol.add_edge(quantum_channel, bob_qm, EdgeType.QUANTUM)
        # 
        # return protocol
        return None
    
    def test_protocol_creation_compatibility(self, empty_protocol):
        """
        测试协议创建的向后兼容性 - 基于原有test_graph_creation
        
        重构思路：
        - 保持原有的协议创建接口
        - 验证基本属性设置是否正确
        - 确保初始状态符合预期
        """
        if empty_protocol is None:
            pytest.skip("ProtocolGraph类尚未实现")
            
        # 验证协议基本属性
        assert empty_protocol.name == "TestProtocol"
        assert empty_protocol.get_node_count() == 0
        assert empty_protocol.get_edge_count() == 0
        assert empty_protocol.is_dag() is True  # 空图是DAG
    
    def test_add_node_interface_compatibility(self, empty_protocol):
        """
        测试添加节点接口的向后兼容性 - 基于原有test_add_node
        
        重构思路：
        - 保持原有add_node方法的参数接口
        - 验证节点创建后的属性设置
        - 确保参数验证机制正常工作
        """
        if empty_protocol is None:
            pytest.skip("ProtocolGraph类尚未实现")
            
        # TODO: 实现NodeType和Party枚举后启用
        # from qcgf_dsl import NodeType, Party
        # 
        # # 添加量子态准备节点
        # node_id = empty_protocol.add_node(
        #     node_type=NodeType.QSP,
        #     party=Party.ALICE,
        #     params={"state": "|+⟩", "fidelity": 0.95}
        # )
        # 
        # # 验证节点添加结果
        # assert empty_protocol.get_node_count() == 1
        # assert empty_protocol.has_node(node_id)
        # 
        # # 验证节点属性
        # node = empty_protocol.get_node(node_id)
        # assert node is not None
        # assert node.node_type == NodeType.QSP
        # assert node.party == Party.ALICE
        # assert node.get_param("state") == "|+⟩"
        # assert node.get_param("fidelity") == 0.95
    
    def test_add_edge_with_validation(self, sample_bb84_protocol):
        """
        测试边添加和验证功能 - 基于原有test_add_edge
        
        重构思路：
        - 保持原有add_edge方法接口
        - 增强了边类型验证
        - 简化了测试数据结构
        """
        if sample_bb84_protocol is None:
            pytest.skip("测试协议尚未实现")
            
        # TODO: 实现相关类后启用
        # from qcgf_dsl import NodeType, Party, EdgeType
        # 
        # # 添加经典处理节点
        # classical_node = sample_bb84_protocol.add_node(
        #     node_type=NodeType.CLO,
        #     party=Party.BOB,
        #     params={"operation": "key_extraction"}
        # )
        # 
        # # 获取现有的Bob测量节点
        # bob_nodes = sample_bb84_protocol.get_nodes_by_party(Party.BOB)
        # bob_qm = [n for n in bob_nodes if n.node_type == NodeType.QM][0]
        # 
        # # 添加经典边：测量结果到经典处理
        # success = sample_bb84_protocol.add_edge(
        #     bob_qm.node_id, 
        #     classical_node, 
        #     EdgeType.CLASSICAL
        # )
        # 
        # # 验证边添加结果
        # assert success is True
        # assert sample_bb84_protocol.has_edge(bob_qm.node_id, classical_node)
        # 
        # # 验证边属性
        # edge_data = sample_bb84_protocol.get_edge_data(bob_qm.node_id, classical_node)
        # assert edge_data["edge_type"] == EdgeType.CLASSICAL
    
    def test_dag_constraint_enforcement(self, sample_bb84_protocol):
        """
        测试DAG约束强制执行 - 基于原有test_add_edge_cycle_raises_error
        
        重构思路：
        - 保持原有的环路检测逻辑
        - 简化了环路创建的测试场景
        - 增强了错误信息验证
        """
        if sample_bb84_protocol is None:
            pytest.skip("测试协议尚未实现")
            
        # TODO: 实现相关类后启用
        # from qcgf_dsl import NodeType, EdgeType
        # 
        # # 获取协议中的节点
        # nodes = list(sample_bb84_protocol.get_all_nodes())
        # first_node = nodes[0].node_id
        # last_node = nodes[-1].node_id
        # 
        # # 尝试创建环路：从最后一个节点回到第一个节点
        # with pytest.raises(ValueError, match="would create a cycle"):
        #     sample_bb84_protocol.add_edge(last_node, first_node, EdgeType.CLASSICAL)
        # 
        # # 验证图仍然是DAG
        # assert sample_bb84_protocol.is_dag() is True
    
    def test_protocol_statistics_accuracy(self, sample_bb84_protocol):
        """
        测试协议统计信息准确性 - 基于原有test_get_statistics
        
        重构思路：
        - 保持原有的统计信息接口
        - 增加了更详细的统计验证
        - 简化了统计数据的断言逻辑
        """
        if sample_bb84_protocol is None:
            pytest.skip("测试协议尚未实现")
            
        # TODO: 实现相关类后启用
        # from qcgf_dsl import NodeType, Party
        # 
        # stats = sample_bb84_protocol.get_statistics()
        # 
        # # 验证基本统计
        # assert stats["node_count"] == 3  # QSP + QC + QM
        # assert stats["edge_count"] == 2  # QSP->QC + QC->QM  
        # assert stats["is_dag"] is True
        # 
        # # 验证节点类型统计
        # assert stats["node_stats"]["QSP"] == 1
        # assert stats["node_stats"]["QC"] == 1
        # assert stats["node_stats"]["QM"] == 1
        # 
        # # 验证参与者统计
        # assert stats["party_stats"]["Alice"] == 1
        # assert stats["party_stats"]["Bob"] == 1
        # 
        # # 验证边类型统计
        # assert stats["edge_types"]["quantum"] == 2
    
    def test_node_removal_cascade(self, sample_bb84_protocol):
        """
        测试节点删除的级联效应 - 基于原有test_remove_node优化
        
        重构思路：
        - 保持原有remove_node方法接口
        - 验证删除节点时相关边的自动清理
        - 简化了删除后状态的验证逻辑
        """
        if sample_bb84_protocol is None:
            pytest.skip("测试协议尚未实现")
            
        # TODO: 实现相关类后启用
        # from qcgf_dsl import NodeType
        # 
        # # 记录删除前状态
        # initial_nodes = sample_bb84_protocol.get_node_count()
        # initial_edges = sample_bb84_protocol.get_edge_count()
        # 
        # # 获取中间的量子信道节点
        # qc_nodes = sample_bb84_protocol.get_nodes_by_type(NodeType.QC)
        # qc_node_id = qc_nodes[0].node_id
        # 
        # # 删除量子信道节点
        # success = sample_bb84_protocol.remove_node(qc_node_id)
        # assert success is True
        # 
        # # 验证删除结果
        # assert not sample_bb84_protocol.has_node(qc_node_id)
        # assert sample_bb84_protocol.get_node_count() == initial_nodes - 1
        # 
        # # 验证相关边被自动删除（量子信道连接了2条边）
        # assert sample_bb84_protocol.get_edge_count() == 0
        # 
        # # 验证图仍然是有效的DAG
        # assert sample_bb84_protocol.is_dag() is True


class TestNodeTypesRefactor:
    """
    节点类型重构测试用例 - 基于原有节点类型系统
    
    重构思路：
    - 参考原有NodeType和Party枚举设计
    - 保持节点类型的分类逻辑（量子vs经典）
    - 简化了参数模板和验证机制
    - 新增了理想化模式的测试支持
    
    设计改进：
    - 更清晰的枚举测试结构
    - 统一的参数验证测试模式
    - 理想化vs现实模式的对比测试
    """
    
    def test_node_type_classification(self):
        """
        测试节点类型分类功能 - 基于原有分类逻辑
        
        重构思路：
        - 保持原有的量子/经典节点分类方法
        - 验证所有节点类型的正确分类
        - 简化了分类测试的逻辑结构
        """
        # TODO: 实现NodeType枚举后启用
        # from qcgf_dsl import NodeType
        # 
        # # 测试量子节点类型
        # quantum_types = [NodeType.QSP, NodeType.QC, NodeType.QM, NodeType.QG, NodeType.QD]
        # for node_type in quantum_types:
        #     assert NodeType.is_quantum_type(node_type)
        #     assert not NodeType.is_classical_type(node_type)
        # 
        # # 测试经典节点类型  
        # classical_types = [NodeType.CLO, NodeType.CS, NodeType.CC]
        # for node_type in classical_types:
        #     assert NodeType.is_classical_type(node_type)
        #     assert not NodeType.is_quantum_type(node_type)
    
    def test_parameter_template_system(self):
        """
        测试参数模板系统 - 基于原有模板机制
        
        重构思路：
        - 保持原有get_node_template函数接口
        - 验证每种节点类型的默认参数
        - 简化了模板验证的断言逻辑
        """
        # TODO: 实现参数模板系统后启用
        # from qcgf_dsl import NodeType, get_node_template
        # 
        # # 测试QSP节点模板
        # qsp_template = get_node_template(NodeType.QSP)
        # assert "state" in qsp_template
        # assert "fidelity" in qsp_template
        # assert "party" in qsp_template
        # assert qsp_template["fidelity"] == 0.99
        # 
        # # 测试QC节点模板
        # qc_template = get_node_template(NodeType.QC)
        # assert "loss" in qc_template
        # assert "noise" in qc_template
        # assert "distance" in qc_template
        # assert 0 <= qc_template["loss"] <= 1
        # 
        # # 测试QM节点模板
        # qm_template = get_node_template(NodeType.QM)
        # assert "basis" in qm_template
        # assert "efficiency" in qm_template
        # assert "party" in qm_template
        # assert 0 <= qm_template["efficiency"] <= 1
    
    def test_parameter_validation_system(self):
        """
        测试参数验证系统 - 基于原有验证逻辑
        
        重构思路：
        - 保持原有validate_node_params函数接口
        - 验证参数的范围和类型检查
        - 简化了验证测试的用例设计
        """
        # TODO: 实现参数验证系统后启用
        # from qcgf_dsl import NodeType, validate_node_params
        # 
        # # 测试有效参数验证
        # valid_qsp_params = {"state": "|0⟩", "fidelity": 0.95, "party": "Alice"}
        # assert validate_node_params(NodeType.QSP, valid_qsp_params)
        # 
        # # 测试无效参数验证 - 缺少必需参数
        # invalid_qsp_params = {"fidelity": 0.95}  # 缺少state
        # assert not validate_node_params(NodeType.QSP, invalid_qsp_params)
        # 
        # # 测试无效参数验证 - 参数值超出范围
        # invalid_qc_params = {"loss": 1.5, "noise": 0.01}  # loss > 1
        # assert not validate_node_params(NodeType.QC, invalid_qc_params)
        # 
        # # 测试无效参数验证 - 效率参数超出范围
        # invalid_qm_params = {"basis": "Z", "efficiency": 1.2}  # efficiency > 1
        # assert not validate_node_params(NodeType.QM, invalid_qm_params)
    
    def test_idealized_mode_support(self):
        """
        测试理想化模式支持 - 新增功能测试
        
        重构思路：
        - 基于原有的理想化模式设计
        - 测试模式切换对参数模板的影响
        - 验证理想化参数的正确性
        """
        # TODO: 实现理想化模式后启用
        # from qcgf_dsl import (
        #     set_idealized_mode, 
        #     is_idealized_mode,
        #     get_node_template,
        #     NodeType
        # )
        # 
        # # 测试理想化模式切换
        # set_idealized_mode(True)
        # assert is_idealized_mode() is True
        # 
        # # 获取理想化模式下的模板
        # ideal_qm_template = get_node_template(NodeType.QM)
        # assert ideal_qm_template["efficiency"] == 1.0  # 理想检测效率
        # 
        # ideal_qc_template = get_node_template(NodeType.QC)
        # assert ideal_qc_template["loss"] == 0.0  # 理想信道无损耗
        # assert ideal_qc_template["noise"] == 0.0  # 理想信道无噪声
        # 
        # # 恢复现实模式
        # set_idealized_mode(False)
        # assert is_idealized_mode() is False
        # 
        # # 验证现实模式参数
        # real_qm_template = get_node_template(NodeType.QM)
        # assert real_qm_template["efficiency"] < 1.0  # 现实检测效率


class TestDSLParsingRefactor:
    """
    DSL解析重构测试用例 - 基于原有解析器设计
    
    重构思路：
    - 参考原有QCGFParser和QCGFSerializer类设计
    - 保持DSL文本格式的向后兼容性
    - 简化了解析和序列化的测试逻辑
    - 新增了更多错误处理测试
    
    设计改进：
    - 更清晰的DSL文本样例
    - 统一的解析测试模式
    - 更全面的序列化往返测试
    """
    
    @pytest.fixture
    def bb84_dsl_text(self):
        """
        BB84协议DSL文本fixture - 基于原有dsl_text
        
        重构思路：
        - 参考原有的DSL语法格式
        - 使用标准的BB84协议结构
        - 简化了参数设置，突出核心逻辑
        """
        return """
        # BB84协议示例 - 重构版本
        # Alice方：量子态准备
        QSP qsp_alice: party="Alice", state="|0⟩", fidelity=0.99
        
        # 量子信道：Alice到Bob
        QC quantum_channel: loss=0.1, noise=0.01, distance=50.0
        
        # Bob方：量子测量
        QM qm_bob: party="Bob", basis="computational", efficiency=0.8
        
        # 经典信道：基比较
        CC classical_channel: bandwidth=1e9, latency=1e-6
        
        # 连接关系：构建协议流程
        qsp_alice -> quantum_channel [quantum]
        quantum_channel -> qm_bob [quantum]
        qm_bob -> classical_channel [classical]: data_type="measurement_results"
        """
    
    def test_dsl_parsing_compatibility(self, bb84_dsl_text):
        """
        测试DSL解析的向后兼容性 - 基于原有test_parser
        
        重构思路：
        - 保持原有QCGFParser类的接口
        - 验证解析后的协议图结构
        - 简化了解析结果的验证逻辑
        """
        # TODO: 实现DSL解析器后启用
        # from qcgf_dsl import QCGFParser, NodeType, Party, EdgeType
        # 
        # parser = QCGFParser()
        # protocol = parser.parse(bb84_dsl_text)
        # 
        # # 验证解析结果的基本结构
        # assert protocol.get_node_count() == 4
        # assert protocol.get_edge_count() == 3
        # assert protocol.is_dag() is True
        # 
        # # 验证Alice节点解析
        # alice_nodes = protocol.get_nodes_by_party(Party.ALICE)
        # assert len(alice_nodes) == 1
        # assert alice_nodes[0].node_type == NodeType.QSP
        # assert alice_nodes[0].get_param("state") == "|0⟩"
        # 
        # # 验证Bob节点解析
        # bob_nodes = protocol.get_nodes_by_party(Party.BOB)
        # assert len(bob_nodes) == 1
        # assert bob_nodes[0].node_type == NodeType.QM
        # assert bob_nodes[0].get_param("basis") == "computational"
        # 
        # # 验证边解析
        # edges = protocol.get_edges()
        # quantum_edges = [e for e in edges if e[2]["edge_type"] == EdgeType.QUANTUM]
        # classical_edges = [e for e in edges if e[2]["edge_type"] == EdgeType.CLASSICAL]
        # assert len(quantum_edges) == 2
        # assert len(classical_edges) == 1
    
    def test_dsl_serialization_roundtrip(self, sample_bb84_protocol):
        """
        测试DSL序列化往返一致性 - 基于原有序列化测试
        
        重构思路：
        - 保持原有QCGFSerializer类的接口
        - 验证序列化后的DSL文本格式
        - 确保往返序列化的一致性
        """
        if sample_bb84_protocol is None:
            pytest.skip("测试协议尚未实现")
            
        # TODO: 实现DSL序列化器后启用
        # from qcgf_dsl import QCGFSerializer, QCGFParser
        # 
        # # 序列化协议图为DSL文本
        # serializer = QCGFSerializer()
        # dsl_text = serializer.serialize(sample_bb84_protocol)
        # 
        # # 验证DSL文本包含预期内容
        # assert "QSP" in dsl_text
        # assert "QC" in dsl_text
        # assert "QM" in dsl_text
        # assert "Alice" in dsl_text
        # assert "Bob" in dsl_text
        # assert "[quantum]" in dsl_text
        # 
        # # 重新解析DSL文本
        # parser = QCGFParser()
        # reparsed_protocol = parser.parse(dsl_text)
        # 
        # # 验证往返一致性
        # assert reparsed_protocol.get_node_count() == sample_bb84_protocol.get_node_count()
        # assert reparsed_protocol.get_edge_count() == sample_bb84_protocol.get_edge_count()
        # assert reparsed_protocol.is_dag() == sample_bb84_protocol.is_dag()
    
    def test_dsl_file_operations(self, sample_bb84_protocol):
        """
        测试DSL文件操作 - 基于原有文件I/O测试
        
        重构思路：
        - 保持原有的文件读写接口
        - 使用临时文件避免测试污染
        - 简化了文件操作的测试逻辑
        """
        if sample_bb84_protocol is None:
            pytest.skip("测试协议尚未实现")
            
        # TODO: 实现文件操作后启用
        # from qcgf_dsl import QCGFSerializer, QCGFParser
        # 
        # with tempfile.NamedTemporaryFile(mode='w', suffix='.qcgf', delete=False) as f:
        #     temp_filename = f.name
        # 
        # try:
        #     # 保存协议图到文件
        #     serializer = QCGFSerializer()
        #     serializer.serialize_to_file(sample_bb84_protocol, temp_filename)
        #     
        #     # 验证文件存在
        #     assert os.path.exists(temp_filename)
        #     
        #     # 从文件加载协议图
        #     parser = QCGFParser()
        #     loaded_protocol = parser.parse_from_file(temp_filename)
        #     
        #     # 验证加载结果
        #     assert loaded_protocol.get_node_count() == sample_bb84_protocol.get_node_count()
        #     assert loaded_protocol.get_edge_count() == sample_bb84_protocol.get_edge_count()
        #     assert loaded_protocol.is_dag() == sample_bb84_protocol.is_dag()
        #     
        # finally:
        #     # 清理临时文件
        #     if os.path.exists(temp_filename):
        #         os.unlink(temp_filename)
    
    def test_dsl_error_handling(self):
        """
        测试DSL错误处理 - 新增错误处理测试
        
        重构思路：
        - 基于原有的错误处理逻辑
        - 测试各种无效DSL输入的处理
        - 验证错误信息的准确性
        """
        # TODO: 实现DSL解析器后启用
        # from qcgf_dsl import QCGFParser
        # 
        # parser = QCGFParser()
        # 
        # # 测试无效节点语法
        # invalid_node_dsl = "INVALID_NODE_TYPE node1: param=value"
        # with pytest.raises(ValueError, match="Invalid DSL syntax"):
        #     parser.parse(invalid_node_dsl)
        # 
        # # 测试无效边语法
        # invalid_edge_dsl = """
        # QSP node1: state="|0⟩"
        # QM node2: basis="Z"
        # node1 -> node2 [INVALID_EDGE_TYPE]
        # """
        # with pytest.raises(ValueError):
        #     parser.parse(invalid_edge_dsl)
        # 
        # # 测试无效参数语法
        # invalid_param_dsl = "QSP node1: invalid_param_syntax"
        # with pytest.raises(ValueError):
        #     parser.parse(invalid_param_dsl)


class TestVisualizationRefactor:
    """
    可视化重构测试用例 - 基于原有可视化功能
    
    重构思路：
    - 参考原有ProtocolVisualizer类设计
    - 保持可视化接口的向后兼容性
    - 简化了可视化配置和测试逻辑
    - 新增了无显示环境的测试支持
    
    设计改进：
    - 更清晰的可视化配置测试
    - 统一的图像生成测试模式
    - 更全面的布局和样式测试
    """
    
    def test_visualization_interface_compatibility(self, sample_bb84_protocol):
        """
        测试可视化接口的向后兼容性 - 基于原有可视化接口
        
        重构思路：
        - 保持原有ProtocolVisualizer类的接口
        - 验证可视化配置的正确性
        - 支持无显示环境的测试
        """
        if sample_bb84_protocol is None:
            pytest.skip("测试协议尚未实现")
            
        # TODO: 实现可视化器后启用
        # from qcgf_dsl import ProtocolVisualizer
        # import matplotlib
        # matplotlib.use('Agg')  # 无显示环境
        # 
        # # 创建可视化器
        # visualizer = ProtocolVisualizer()
        # 
        # # 验证默认配置
        # assert "figsize" in visualizer.config
        # assert "node_size" in visualizer.config
        # assert "node_colors" in visualizer.config
        # assert "edge_colors" in visualizer.config
        # 
        # # 测试可视化方法不抛出异常
        # try:
        #     import matplotlib.pyplot as plt
        #     fig, ax = plt.subplots()
        #     visualizer.visualize(sample_bb84_protocol, ax=ax)
        #     plt.close(fig)
        # except Exception as e:
        #     pytest.fail(f"Visualization failed: {e}")
    
    def test_visualization_file_export(self, sample_bb84_protocol):
        """
        测试可视化文件导出 - 基于原有文件保存功能
        
        重构思路：
        - 保持原有的文件保存接口
        - 使用临时文件避免测试污染
        - 验证导出文件的正确性
        """
        if sample_bb84_protocol is None:
            pytest.skip("测试协议尚未实现")
            
        # TODO: 实现可视化文件导出后启用
        # from qcgf_dsl import visualize_protocol
        # import matplotlib
        # matplotlib.use('Agg')  # 无显示环境
        # 
        # with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        #     temp_filename = f.name
        # 
        # try:
        #     # 导出协议图
        #     visualize_protocol(
        #         sample_bb84_protocol, 
        #         save_path=temp_filename
        #     )
        #     
        #     # 验证文件存在
        #     assert os.path.exists(temp_filename)
        #     
        #     # 验证文件大小（确保有内容）
        #     assert os.path.getsize(temp_filename) > 0
        #     
        # finally:
        #     # 清理临时文件
        #     if os.path.exists(temp_filename):
        #         os.unlink(temp_filename)


class TestCodeGenerationRefactor:
    """
    代码生成重构测试用例 - 基于原有编译器功能
    
    重构思路：
    - 参考原有QCGFCompiler类设计
    - 保持代码生成接口的向后兼容性
    - 简化了代码生成的测试逻辑
    - 新增了生成代码的语法验证
    
    设计改进：
    - 更清晰的代码生成测试结构
    - 统一的语法验证测试模式
    - 更全面的编译目标测试
    """
    
    def test_python_code_generation(self, sample_bb84_protocol):
        """
        测试Python代码生成 - 基于原有编译功能
        
        重构思路：
        - 保持原有QCGFCompiler类的接口
        - 验证生成代码的语法正确性
        - 确保生成的代码包含预期结构
        """
        if sample_bb84_protocol is None:
            pytest.skip("测试协议尚未实现")
            
        # TODO: 实现代码编译器后启用
        # from qcgf_dsl import QCGFCompiler
        # import ast
        # 
        # compiler = QCGFCompiler()
        # 
        # # 编译协议为Python代码
        # python_code = compiler.compile_protocol(
        #     sample_bb84_protocol, 
        #     target_language="python"
        # )
        # 
        # # 验证生成的代码不为空
        # assert len(python_code) > 0
        # assert "class CompiledProtocol" in python_code
        # assert "def execute(self)" in python_code
        # 
        # # 验证Python语法正确性
        # try:
        #     ast.parse(python_code)
        # except SyntaxError as e:
        #     pytest.fail(f"Generated code has syntax error: {e}")
        # 
        # # 验证包含预期的导入和方法
        # assert "import qiskit" in python_code
        # assert "QuantumCircuit" in python_code
        # assert "def __init__(self)" in python_code
    
    def test_code_generation_file_output(self, sample_bb84_protocol):
        """
        测试代码生成文件输出 - 基于原有文件输出功能
        
        重构思路：
        - 保持原有的文件输出接口
        - 使用临时文件避免测试污染
        - 验证输出文件的正确性
        """
        if sample_bb84_protocol is None:
            pytest.skip("测试协议尚未实现")
            
        # TODO: 实现代码文件输出后启用
        # from qcgf_dsl import compile_to_file
        # import ast
        # 
        # with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        #     temp_filename = f.name
        # 
        # try:
        #     # 编译协议到文件
        #     compile_to_file(
        #         sample_bb84_protocol,
        #         temp_filename,
        #         target_language="python"
        #     )
        #     
        #     # 验证文件存在
        #     assert os.path.exists(temp_filename)
        #     
        #     # 读取并验证文件内容
        #     with open(temp_filename, 'r', encoding='utf-8') as f:
        #         file_content = f.read()
        #     
        #     # 验证内容不为空且语法正确
        #     assert len(file_content) > 0
        #     ast.parse(file_content)  # 验证语法
        #     
        # finally:
        #     # 清理临时文件
        #     if os.path.exists(temp_filename):
        #         os.unlink(temp_filename)


# =============================================================================
# 集成测试：端到端功能验证
# =============================================================================

class TestIntegrationRefactor:
    """
    集成测试重构用例 - 端到端功能验证
    
    重构思路：
    - 基于原有的集成测试逻辑
    - 验证各模块间的协同工作
    - 简化了集成测试的场景设计
    - 新增了性能基准测试
    
    设计改进：
    - 更清晰的端到端测试流程
    - 统一的集成验证模式
    - 更全面的兼容性测试
    """
    
    def test_full_workflow_integration(self):
        """
        测试完整工作流程集成 - DSL解析->可视化->代码生成
        
        重构思路：
        - 基于原有的完整工作流程
        - 验证从DSL到代码的完整转换
        - 确保各模块间的数据一致性
        """
        # TODO: 实现完整模块后启用
        # from qcgf_dsl import (
        #     QCGFParser, ProtocolVisualizer, 
        #     QCGFCompiler, QCGFSerializer
        # )
        # import matplotlib
        # matplotlib.use('Agg')
        # 
        # # 定义完整的BB84协议DSL
        # bb84_dsl = """
        # # 完整BB84协议
        # QSP alice_prep: party="Alice", state="random_bb84"
        # QC quantum_channel: loss=0.1, distance=50
        # QM bob_measure: party="Bob", basis="random_bb84"
        # CLO key_extraction: party="Bob", operation="sifting"
        # 
        # alice_prep -> quantum_channel [quantum]
        # quantum_channel -> bob_measure [quantum]  
        # bob_measure -> key_extraction [classical]
        # """
        # 
        # # 1. 解析DSL为协议图
        # parser = QCGFParser()
        # protocol = parser.parse(bb84_dsl)
        # 
        # # 2. 序列化验证往返一致性
        # serializer = QCGFSerializer()
        # reserialized_dsl = serializer.serialize(protocol)
        # 
        # # 3. 可视化协议图
        # visualizer = ProtocolVisualizer()
        # # 验证可视化不抛出异常
        # 
        # # 4. 编译为可执行代码
        # compiler = QCGFCompiler()
        # python_code = compiler.compile_protocol(protocol)
        # 
        # # 验证整个流程的一致性
        # assert protocol.get_node_count() == 4
        # assert protocol.is_dag() is True
        # assert len(python_code) > 1000  # 确保生成了完整代码
        # assert "BB84" in reserialized_dsl or "bb84" in reserialized_dsl.lower()
    
    def test_performance_benchmarks(self):
        """
        测试性能基准 - 新增性能测试
        
        重构思路：
        - 基于重构目标的性能改进要求
        - 测试关键操作的执行时间
        - 建立性能回归测试基准
        """
        # TODO: 实现性能基准测试后启用
        # import time
        # from qcgf_dsl import ProtocolGraph, NodeType, Party
        # 
        # # 测试大规模协议图创建性能
        # start_time = time.time()
        # 
        # large_protocol = ProtocolGraph("LargeProtocol")
        # 
        # # 创建100个节点的协议图
        # for i in range(100):
        #     large_protocol.add_node(
        #         node_type=NodeType.QSP if i % 2 == 0 else NodeType.QM,
        #         party=Party.ALICE if i % 2 == 0 else Party.BOB,
        #         params={"index": i}
        #     )
        # 
        # creation_time = time.time() - start_time
        # 
        # # 验证性能目标：100个节点创建应在1秒内完成
        # assert creation_time < 1.0
        # assert large_protocol.get_node_count() == 100
        # assert large_protocol.is_dag() is True


if __name__ == "__main__":
    """
    测试运行入口
    
    重构思路：
    - 保持标准的pytest运行方式
    - 支持详细的测试输出
    - 便于开发过程中的快速测试
    """
    pytest.main([__file__, "-v", "--tb=short"])