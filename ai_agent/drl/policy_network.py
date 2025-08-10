import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple

class PolicyNetwork(nn.Module):
    """
    策略网络，将图嵌入向量映射到具体的协议修改动作。
    """
    def __init__(self, input_dim: int, num_actions: int, num_node_targets: int, param_dim: int):
        """
        初始化策略网络。

        Args:
            input_dim (int): 输入的图嵌入向量维度。
            num_actions (int): 离散动作类型的数量 (e.g., add_node, remove_node)。
            num_node_targets (int): 可能的目标节点数量（用于选择节点）。
            param_dim (int): 连续参数的维度。
        """
        super(PolicyNetwork, self).__init__()
        
        # 共享层
        self.fc1 = nn.Linear(input_dim, 256)
        self.fc2 = nn.Linear(256, 128)

        # 动作类型头 (离散)
        self.action_head = nn.Linear(128, num_actions)

        # 目标节点头 (离散)
        self.target_node_head = nn.Linear(128, num_node_targets)

        # 参数头 (连续)
        self.param_head_mean = nn.Linear(128, param_dim)
        self.param_head_std = nn.Linear(128, param_dim)

    def forward(self, state_embedding: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        前向传播。

        Args:
            state_embedding (torch.Tensor): 从图编码器得到的图嵌入状态。

        Returns:
            Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
            - action_probs: 动作类型选择的概率分布。
            - target_node_probs: 目标节点选择的概率分布。
            - param_mean: 连续参数的正态分布均值。
            - param_std: 连续参数的正态分布标准差。
        """
        x = F.relu(self.fc1(state_embedding))
        x = F.relu(self.fc2(x))

        # 计算各个头的输出
        action_logits = self.action_head(x)
        action_probs = F.softmax(action_logits, dim=-1)

        target_node_logits = self.target_node_head(x)
        target_node_probs = F.softmax(target_node_logits, dim=-1)

        param_mean = torch.tanh(self.param_head_mean(x)) # 将均值限制在[-1, 1]
        param_std = F.softplus(self.param_head_std(x))   # 保证标准差为正

        return action_probs, target_node_probs, param_mean, param_std

    def select_action(self, state_embedding: torch.Tensor):
        """
        根据当前状态选择一个动作。
        这里我们从多头输出的分布中采样。
        """
        action_probs, target_node_probs, param_mean, param_std = self.forward(state_embedding)
        
        # 创建多类别分布并采样
        action_dist = torch.distributions.Categorical(action_probs)
        action_type = action_dist.sample()
        
        target_node_dist = torch.distributions.Categorical(target_node_probs)
        target_node = target_node_dist.sample()

        # 创建正态分布并采样
        param_dist = torch.distributions.Normal(param_mean, param_std)
        params = param_dist.sample()
        
        return action_type, target_node, params 