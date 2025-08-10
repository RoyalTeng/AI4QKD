import pytest
import os
from qcgf_dsl.protocol_graph import ProtocolGraph
from qcgf_dsl.node_types import NodeType, Party
from qcgf_dsl.edge_types import EdgeType
from qcgf_dsl.parser import QCGFParser, QCGFSerializer


@pytest.fixture
def empty_graph():
    """一个空的协议图 fixture"""
    return ProtocolGraph(name="TestEmpty")


@pytest.fixture
def sample_graph():
    """一个包含基本节点的协议图 fixture"""
    graph = ProtocolGraph(name="TestSample")
    graph.add_node(node_type=NodeType.QSP, node_id="qsp1", party=Party.ALICE, params={"state": "|0>"})
    graph.add_node(node_type=NodeType.QC, node_id="qc1", params={"loss": 0.2})
    graph.add_node(node_type=NodeType.QM, node_id="qm1", party=Party.BOB, params={"basis": "Z"})
    graph.add_edge("qsp1", "qc1", edge_type=EdgeType.QUANTUM)
    graph.add_edge("qc1", "qm1", edge_type=EdgeType.QUANTUM)
    return graph


class TestProtocolGraph:
    """测试 ProtocolGraph 类的功能"""

    def test_graph_creation(self, empty_graph):
        assert empty_graph.name == "TestEmpty"
        assert empty_graph.get_node_count() == 0
        assert empty_graph.get_edge_count() == 0

    def test_add_node(self, empty_graph):
        node_id = empty_graph.add_node(node_type=NodeType.QSP, party=Party.ALICE, params={"state": "|+>"})
        assert empty_graph.get_node_count() == 1
        assert empty_graph.has_node(node_id)
        node = empty_graph.get_node(node_id)
        assert node is not None
        assert node.node_type == NodeType.QSP
        assert node.party == Party.ALICE
        assert node.get_param("state") == "|+>"

    def test_add_existing_node_raises_error(self, sample_graph):
        with pytest.raises(ValueError, match="already exists"):
            sample_graph.add_node(node_type=NodeType.QSP, node_id="qsp1")

    def test_remove_node(self, sample_graph):
        assert sample_graph.get_node_count() == 3
        assert sample_graph.has_node("qc1")
        sample_graph.remove_node("qc1")
        assert not sample_graph.has_node("qc1")
        assert sample_graph.get_node_count() == 2
        # Edges connected to the node should also be removed
        assert sample_graph.get_edge_count() == 0

    def test_add_edge(self, sample_graph):
        sample_graph.add_node(node_type=NodeType.CLO, node_id="clo1", party=Party.BOB)
        sample_graph.add_edge("qm1", "clo1", edge_type=EdgeType.CLASSICAL)
        assert sample_graph.has_edge("qm1", "clo1")
        edge_data = sample_graph.graph.get_edge_data("qm1", "clo1")
        assert edge_data["edge_type"] == EdgeType.CLASSICAL

    def test_add_edge_cycle_raises_error(self, sample_graph):
        # Create a cycle
        sample_graph.add_node(node_type=NodeType.CLO, node_id="clo1")
        sample_graph.add_edge("qm1", "clo1")
        with pytest.raises(ValueError, match="would create a cycle"):
            sample_graph.add_edge("clo1", "qsp1")

    def test_get_statistics(self, sample_graph):
        stats = sample_graph.get_statistics()
        assert stats["node_count"] == 3
        assert stats["edge_count"] == 2
        assert stats["is_dag"] is True
        assert stats["node_stats"][NodeType.QSP.value] == 1
        assert stats["party_stats"][Party.ALICE.value] == 1


class TestParserSerializer:
    """测试 DSL 解析器和序列化器"""

    @pytest.fixture
    def dsl_text(self):
        """一个DSL文本 fixture"""
        return """
        # BB84 Protocol Example
        QSP qsp_alice: party=ALICE, state="random"
        QC channel1: loss=0.5, distance=10.0
        QM qm_bob: party=BOB, basis="random"
        CC channel2: bandwidth=1e9

        qsp_alice -> channel1 [QUANTUM]
        channel1 -> qm_bob [QUANTUM]
        """

    def test_parser(self, dsl_text):
        parser = QCGFParser()
        graph = parser.parse(dsl_text)

        assert graph.get_node_count() == 4
        assert graph.get_edge_count() == 2
        
        alice_node = graph.get_node("qsp_alice")
        assert alice_node.party == Party.ALICE
        assert alice_node.get_param("state") == "random"

        channel_edge = graph.graph.get_edge_data("channel1", "qm_bob")
        assert channel_edge["edge_type"] == EdgeType.QUANTUM

    def test_serializer(self, sample_graph):
        serializer = QCGFSerializer()
        dsl_text = serializer.serialize(sample_graph)

        # Split the line to avoid order-dependent failures
        qsp_line = [line for line in dsl_text.split('\n') if 'QSP qsp1' in line][0]
        assert 'party="Alice"' in qsp_line
        assert 'state="|0>"' in qsp_line
        
        qc_line = [line for line in dsl_text.split('\n') if 'QC qc1' in line][0]
        assert 'loss=0.2' in qc_line
        assert 'qsp1 -> qc1 [quantum]' in dsl_text

    def test_parse_serialize_identity(self, dsl_text):
        """测试解析后再序列化是否能得到相似的结果"""
        parser = QCGFParser()
        graph = parser.parse(dsl_text)

        serializer = QCGFSerializer()
        serialized_text = serializer.serialize(graph)
        
        # Re-parse and check for major properties
        new_graph = parser.parse(serialized_text)
        assert new_graph.get_node_count() == graph.get_node_count()
        assert new_graph.get_edge_count() == graph.get_edge_count()
        assert new_graph.get_node("qsp_alice").party == Party.ALICE


class TestSerialization:
    """测试图的 to_dict 和 from_dict 功能"""

    def test_to_from_dict_identity(self, sample_graph):
        graph_dict = sample_graph.to_dict()

        assert graph_dict["name"] == "TestSample"
        assert len(graph_dict["nodes"]) == 3
        assert len(graph_dict["edges"]) == 2

        new_graph = ProtocolGraph.from_dict(graph_dict)

        assert new_graph.name == sample_graph.name
        assert new_graph.get_node_count() == sample_graph.get_node_count()
        assert new_graph.get_edge_count() == sample_graph.get_edge_count()
        
        original_node = sample_graph.get_node("qsp1")
        new_node = new_graph.get_node("qsp1")
        assert original_node.to_dict() == new_node.to_dict()

    def test_save_load_file(self, sample_graph, tmp_path):
        """测试保存到文件和从文件加载"""
        filepath = os.path.join(tmp_path, "test_graph.json")
        sample_graph.save_to_file(filepath)
        assert os.path.exists(filepath)

        loaded_graph = ProtocolGraph.load_from_file(filepath)
        assert loaded_graph.get_node_count() == sample_graph.get_node_count()
        assert loaded_graph.get_node("qm1").party == Party.BOB 