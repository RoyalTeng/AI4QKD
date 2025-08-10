from typing import Dict, Any, Tuple, List
from qcgf_dsl.protocol_graph import ProtocolGraph
from qcgf_dsl.node_types import NodeType
from .drl.sac_agent import SACAgent  # 或者 PPOAgent
from .ea.genetic_algorithm import GeneticAlgorithm
from .graph_encoder.gat_encoder import GATEncoder # 或者其他编码器
import copy

class HybridAgent:
    """
    混合智能体，结合了深度强化学习（DRL）和演化算法（EA）。
    """
    def __init__(self, config: Dict[str, Any]):
        """
        初始化混合智能体。

        Args:
            config (Dict[str, Any]): 包含所有子模块配置的字典。
        """
        self.config = config
        self.graph_encoder = self._init_graph_encoder()
        self.drl_agent = self._init_drl_agent()
        self.ea_agent = self._init_ea_agent()

    def _init_graph_encoder(self):
        # 根据配置初始化图编码器，如果未提供则使用合理的默认值
        encoder_config = self.config.get("graph_encoder", {})
        encoder_config.setdefault('in_channels', 16) # 假设节点特征维度为16
        encoder_config.setdefault('hidden_channels', 32)
        encoder_config.setdefault('out_channels', 64)
        return GATEncoder(**encoder_config)

    def _init_drl_agent(self):
        # 根据配置初始化DRL智能体，提供默认值
        drl_config = self.config.get("drl_agent", {})
        drl_config.setdefault('state_dim', 64) # 应与图编码器的out_channels匹配
        drl_config.setdefault('action_dim', 3) # e.g., add, remove, modify
        drl_config.setdefault('num_node_targets', 10) # 假设最大节点数为10
        drl_config.setdefault('param_dim', 5) # 假设有5个连续参数
        return SACAgent(**drl_config)

    def _init_ea_agent(self):
        # 根据配置初始化EA智能体，提供默认值
        ea_config = self.config.get("ea_agent", {})
        # EA的初始化可能更复杂，依赖于适应度函数和种群
        # 这里我们假设一个简化的初始化
        ea_config.setdefault('population_size', 50)
        ea_config.setdefault('crossover_rate', 0.8)
        ea_config.setdefault('mutation_rate', 0.1)
        # fitness_fn 和 init_population_fn 通常在更高层定义
        # 这里我们用lambda占位符，因为在当前示例中不会真正调用evolve
        ea_config.setdefault('fitness_fn', lambda x: 0.0)
        ea_config.setdefault('init_population_fn', lambda x: [])
        return GeneticAlgorithm(**ea_config)

    def save_models(self, file_path: str):
        """
        保存所有需要训练的模型的权重到指定文件。
        Args:
            file_path (str): 模型的完整保存路径，包括文件名。
        """
        # 直接调用DRL Agent自身的save方法，它知道如何保存所有组件
        self.drl_agent.save(file_path)
        print(f"模型已保存至 {file_path}")

    def load_models(self, file_path: str):
        """
        从指定文件加载所有需要训练的模型的权重。
        Args:
            file_path (str): 模型的完整加载路径，包括文件名。
        """
        try:
            # 直接调用DRL Agent自身的load方法
            self.drl_agent.load(file_path)
            print(f"模型已从 {file_path} 加载。")
        except FileNotFoundError:
            print(f"警告：在 {file_path} 未找到模型文件，将使用随机初始化的模型。")
        except Exception as e:
            print(f"加载模型时发生未知错误: {e}")

    def optimize(self, initial_protocol: ProtocolGraph) -> Tuple[ProtocolGraph, List[str]]:
        """
        执行一个简化的、基于规则的优化流程。
        真正的AI优化会使用DRL和EA，这里作为一个占位符和示例。

        Args:
            initial_protocol (ProtocolGraph): 初始的QKD协议图。

        Returns:
            Tuple[ProtocolGraph, List[str]]: 包含优化后的协议图和优化建议列表的元组。
        """
        print("--- 开始AI辅助协议优化 (简化版) ---")
        
        # 创建一个副本进行修改，以保留原始协议
        optimized_protocol = copy.deepcopy(initial_protocol)
        optimized_protocol.name = f"{initial_protocol.name}_Optimized"
        suggestions = []

        # 模拟评估初始性能 (在真实流程中，这将由外部评估器完成)
        # 这里我们假设一个初始的QBER和loss来驱动优化决策
        # 在实际的 aop 中，我们会从 simulator 获取这些值
        initial_qber = 0.05
        initial_loss = 0.3

        # 规则1: 如果QBER过高，尝试降低信道错误率
        if initial_qber > 0.03:
            for node in optimized_protocol.get_nodes_by_type(NodeType.QC):
                original_error = node.get_param('error_rate', 0.0)
                if original_error > 0.01:
                    new_error = original_error * 0.5 # 将错误率降低一半
                    node.set_param('error_rate', new_error)
                    suggestion = f"节点 '{node.node_id}': 错误率从 {original_error:.3f} 优化至 {new_error:.3f} 以降低QBER。"
                    suggestions.append(suggestion)
                    print(suggestion)

        # 规则2: 如果损耗过高，尝试降低信道损耗
        if initial_loss > 0.15:
            for node in optimized_protocol.get_nodes_by_type(NodeType.QC):
                original_loss = node.get_param('loss', 0.0)
                if original_loss > 0.1:
                    new_loss = original_loss * 0.8 # 将损耗降低20%
                    node.set_param('loss', new_loss)
                    suggestion = f"节点 '{node.node_id}': 损耗从 {original_loss:.3f} 优化至 {new_loss:.3f} 以提升增益。"
                    suggestions.append(suggestion)
                    print(suggestion)
        
        # 如果没有任何优化被触发，也给出一个说明
        if not suggestions:
            suggestions.append("未发现明确的优化点，协议已处于较好状态。")

        print("\n--- 优化完成 ---")
        return optimized_protocol, suggestions 