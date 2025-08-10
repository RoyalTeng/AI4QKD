import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, global_mean_pool

class GCNEncoder(torch.nn.Module):
    """
    图卷积网络 (GCN) 编码器，作为一种简单有效的图表示学习基线模型。
    """
    def __init__(self, in_channels: int, hidden_channels: int, out_channels: int):
        """
        初始化GCN编码器。

        Args:
            in_channels (int): 输入节点特征的维度。
            hidden_channels (int): 隐藏层的维度。
            out_channels (int): 输出图嵌入的维度。
        """
        super(GCNEncoder, self).__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, hidden_channels * 2)
        self.conv3 = GCNConv(hidden_channels * 2, out_channels)

    def forward(self, data):
        """
        前向传播。

        Args:
            data: PyTorch Geometric 的 Data 对象。

        Returns:
            torch.Tensor: 图的嵌入向量。
        """
        x, edge_index, batch = data.x, data.edge_index, data.batch

        # 1. 第一层GCN + ReLU
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        
        # 2. 第二层GCN + ReLU
        x = self.conv2(x, edge_index)
        x = F.relu(x)

        # 3. 第三层GCN
        x = self.conv3(x, edge_index)
        
        # 4. 全局平均池化
        graph_embedding = global_mean_pool(x, batch)
        
        return graph_embedding 