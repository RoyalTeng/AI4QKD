import torch
import torch.nn as nn
import torch.nn.functional as F

class ValueNetwork(nn.Module):
    """
    价值网络 (Critic)，用于估计状态的价值 (V-value)。
    """
    def __init__(self, input_dim: int):
        """
        初始化价值网络。

        Args:
            input_dim (int): 输入的图嵌入向量维度。
        """
        super(ValueNetwork, self).__init__()
        self.fc1 = nn.Linear(input_dim, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 1)

    def forward(self, state_embedding: torch.Tensor) -> torch.Tensor:
        """
        前向传播，计算状态价值。

        Args:
            state_embedding (torch.Tensor): 图嵌入状态。

        Returns:
            torch.Tensor: 预测的状态价值 (V-value)。
        """
        x = F.relu(self.fc1(state_embedding))
        x = F.relu(self.fc2(x))
        state_value = self.fc3(x)
        return state_value

class QNetwork(nn.Module):
    """
    Q值网络 (Critic)，用于估计在特定状态下执行特定动作的价值 (Q-value)。
    """
    def __init__(self, input_dim: int, action_dim: int):
        """
        初始化Q值网络。

        Args:
            input_dim (int): 输入的图嵌入向量维度。
            action_dim (int): 动作向量的维度。
                             对于复合动作空间，这需要将所有动作部分拼接起来。
        """
        super(QNetwork, self).__init__()
        
        # 将状态和动作拼接后输入
        self.fc1 = nn.Linear(input_dim + action_dim, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 1)

    def forward(self, state_embedding: torch.Tensor, action: torch.Tensor) -> torch.Tensor:
        """
        前向传播，计算Q值。

        Args:
            state_embedding (torch.Tensor): 图嵌入状态。
            action (torch.Tensor): 动作向量。

        Returns:
            torch.Tensor: 预测的Q值。
        """
        # 将状态和动作向量在特征维度上拼接
        x = torch.cat([state_embedding, action], dim=1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        q_value = self.fc3(x)
        return q_value 