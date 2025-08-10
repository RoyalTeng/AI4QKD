import pytest
import torch
import numpy as np
from torch_geometric.data import Data
from ai_agent.drl import PolicyNetwork, ValueNetwork, QNetwork, SACAgent, PPOAgent, ReplayBuffer
from ai_agent.ea import GeneticAlgorithm, EvolutionStrategy, Population
from ai_agent.graph_encoder import GATEncoder, GraphTransformerEncoder, GCNEncoder
from ai_agent.hybrid_agent import HybridAgent

# --- Fixtures ---
@pytest.fixture
def state_embedding():
    return torch.randn(1, 128) # (batch_size, feature_dim)

@pytest.fixture
def graph_data():
    return Data(
        x=torch.randn(5, 16), # 5 nodes, 16 features
        edge_index=torch.tensor([[0, 1, 2, 3], [1, 2, 3, 4]]),
        batch=torch.zeros(5, dtype=torch.long)
    )

# --- DRL Submodule Tests ---
class TestDRL:
    def test_policy_network(self, state_embedding):
        net = PolicyNetwork(input_dim=128, num_actions=4, num_node_targets=10, param_dim=2)
        action_probs, target_probs, param_mean, param_std = net(state_embedding)
        assert action_probs.shape == (1, 4)
        assert target_probs.shape == (1, 10)
        assert param_mean.shape == (1, 2)

    def test_value_network(self, state_embedding):
        net = ValueNetwork(input_dim=128)
        value = net(state_embedding)
        assert value.shape == (1, 1)

    def test_q_network(self, state_embedding):
        action = torch.randn(1, 6) # action_dim=6
        net = QNetwork(input_dim=128, action_dim=6)
        q_value = net(state_embedding, action)
        assert q_value.shape == (1, 1)

    def test_sac_agent_init(self):
        agent = SACAgent(state_dim=128, action_dim=4, num_node_targets=10, param_dim=2)
        assert agent is not None

    def test_ppo_agent_init(self):
        agent = PPOAgent(state_dim=128, action_dim=4, num_node_targets=10, param_dim=2)
        assert agent is not None

# --- EA Submodule Tests ---
class TestEA:
    def test_genetic_algorithm_init(self):
        ga = GeneticAlgorithm(
            population_size=10,
            crossover_rate=0.8,
            mutation_rate=0.1,
            fitness_fn=lambda x: 1.0,
            init_population_fn=lambda size: [None] * size
        )
        assert ga is not None

    def test_evolution_strategy_init(self):
        es = EvolutionStrategy(
            mean_vector=np.random.randn(10),
            stdev_vector=np.ones(10),
            population_size=20,
            learning_rate=0.01,
            fitness_fn=lambda x: -np.sum(x**2)
        )
        assert es is not None

# --- Graph Encoder Submodule Tests ---
class TestGraphEncoders:
    def test_gat_encoder(self, graph_data):
        encoder = GATEncoder(in_channels=16, hidden_channels=32, out_channels=64)
        embedding = encoder(graph_data)
        assert embedding.shape == (1, 64)

    def test_gcn_encoder(self, graph_data):
        encoder = GCNEncoder(in_channels=16, hidden_channels=32, out_channels=64)
        embedding = encoder(graph_data)
        assert embedding.shape == (1, 64)

    def test_graph_transformer_encoder(self, graph_data):
        encoder = GraphTransformerEncoder(in_channels=16, hidden_channels=32, out_channels=64)
        embedding = encoder(graph_data)
        assert embedding.shape == (1, 64)

# --- Hybrid Agent Test ---
def test_hybrid_agent_init_placeholder():
    # A dummy config for initialization test
    config = {
        "graph_encoder": {"in_channels": 16, "hidden_channels": 32, "out_channels": 128},
        "drl_agent": {"state_dim": 128, "action_dim": 4, "num_node_targets": 10, "param_dim": 2},
        "ea_agent": {
            "population_size": 10,
            "crossover_rate": 0.8,
            "mutation_rate": 0.1,
            "fitness_fn": lambda x: 1.0,
            "init_population_fn": lambda size: [None] * size
        }
    }
    # 直接断言初始化成功
    agent = HybridAgent(config)
    assert agent is not None 