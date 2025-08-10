import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GATConv, global_mean_pool

class GATEncoder(nn.Module):
    """
    图注意力网络 (GAT) 编码器，用于将协议图转换为一个固定维度的嵌入向量。
    """
    def __init__(self, in_channels: int, hidden_channels: int, out_channels: int, heads: int = 4):
        """
        初始化GAT编码器。

        Args:
            in_channels (int): 输入节点特征的维度。
            hidden_channels (int): 隐藏层的维度。
            out_channels (int): 输出图嵌入的维度。
            heads (int, optional): GAT中的注意力头数。 Defaults to 4.
        """
        super(GATEncoder, self).__init__()
        self.conv1 = GATConv(in_channels, hidden_channels, heads=heads, dropout=0.6)
        # 第二层的输入维度是 heads * hidden_channels
        self.conv2 = GATConv(hidden_channels * heads, out_channels, heads=1, concat=False, dropout=0.6)

    def forward(self, data) -> torch.Tensor:
        """
        前向传播。

        Args:
            data: PyTorch Geometric 的 Data 对象，包含 x, edge_index, batch。
                  - x: 节点特征矩阵 [num_nodes, in_channels]
                  - edge_index: 图连接信息 [2, num_edges]
                  - batch: 批处理索引 [num_nodes]

        Returns:
            torch.Tensor: 图的嵌入向量 [batch_size, out_channels]。
        """
        x, edge_index, batch = data.x, data.edge_index, data.batch
        
        # 1. 第一层GAT
        x = F.dropout(x, p=0.6, training=self.training)
        x = F.elu(self.conv1(x, edge_index))
        
        # 2. 第二层GAT
        x = F.dropout(x, p=0.6, training=self.training)
        x = self.conv2(x, edge_index)
        
        # 3. 全局池化
        # 使用全局平均池化将节点嵌入聚合为单个图嵌入
        graph_embedding = global_mean_pool(x, batch)
        
        return graph_embedding 