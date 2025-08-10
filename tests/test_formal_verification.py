import pytest
from qcgf_dsl import ProtocolGraph, NodeType, EdgeType
from formal_verification import (
    ProtocolVerifier,
    SecurityProof,
    ModelChecker,
    TheoremProver,
)
from z3 import unsat, sat

@pytest.fixture
def valid_dag_graph():
    """一个有效的、有向无环的协议图。"""
    g = ProtocolGraph("ValidDAG")
    g.add_node(node_type=NodeType.QSP, node_id="qsp1")
    g.add_node(node_type=NodeType.QC, node_id="qc1")
    g.add_node(node_type=NodeType.QM, node_id="qm1")
    g.add_edge("qsp1", "qc1", EdgeType.QUANTUM)
    g.add_edge("qc1", "qm1", EdgeType.QUANTUM)
    return g

@pytest.fixture
def cyclic_graph():
    """一个包含环路的协议图。"""
    g = ProtocolGraph("Cyclic")
    g.add_node(node_type=NodeType.QSP, node_id="qsp1")
    g.add_node(node_type=NodeType.QC, node_id="qc1")
    g.add_edge("qsp1", "qc1", EdgeType.QUANTUM)
    # This creates a cycle
    g.graph.add_edge("qc1", "qsp1") 
    return g

class TestProtocolVerifier:
    def test_verify_valid_graph(self, valid_dag_graph):
        verifier = ProtocolVerifier()
        report = verifier.verify(valid_dag_graph)
        assert report.is_valid is True
        assert len(report.errors) == 0

    def test_verify_cyclic_graph(self, cyclic_graph):
        verifier = ProtocolVerifier()
        report = verifier.verify(cyclic_graph)
        assert report.is_valid is False
        assert "协议图包含环路" in report.errors[0]

class TestSecurityProof:
    def test_generate_proof(self, valid_dag_graph):
        prover = SecurityProof()
        proof_text = prover.generate(valid_dag_graph, qber=0.02, gain=0.9)
        assert isinstance(proof_text, str)
        assert r"\section*{QKD Protocol Security Proof}" in proof_text
        assert "QBER = 0.0200" in proof_text

class TestModelChecker:
    def test_to_kripke_structure(self, valid_dag_graph):
        checker = ModelChecker()
        kripke = checker.to_kripke_structure(valid_dag_graph)
        assert "states" in kripke
        assert "initial_states" in kripke
        assert "transitions" in kripke
        assert len(kripke["states"]) == 3
        assert kripke["initial_states"] == ["qsp1"]

    def test_run_model_check_stub(self, valid_dag_graph):
        checker = ModelChecker()
        # 测试存根，预期返回True
        result = checker.run_model_check("AG(qsp1 -> AF(qm1))", valid_dag_graph)
        assert result is True

class TestTheoremProver:
    def test_prove_no_cloning(self):
        prover = TheoremProver()
        # 预期结果是unsat，因为假设通用克隆存在会导致矛盾
        result = prover.prove_no_cloning()
        assert result == unsat

    def test_prove_distinguishability(self):
        prover = TheoremProver()
        # 非正交态(False) -> 不可区分(unsat)
        result_non_orthogonal = prover.prove_distinguishability(are_orthogonal=False)
        assert result_non_orthogonal == unsat
        
        # 正交态(True) -> 可以区分(sat)
        result_orthogonal = prover.prove_distinguishability(are_orthogonal=True)
        assert result_orthogonal == sat
