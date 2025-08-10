import torch
from torch import nn
from torch_geometric.nn import TransformerConv, global_add_pool

class GraphTransformerEncoder(nn.Module):
    """
    基于Graphormer架构的简化版图Transformer编码器。
    """
    def __init__(self, in_channels, hidden_channels, out_channels, num_layers=2, heads=4):
        """
        初始化图Transformer编码器。

        Args:
            in_channels (int): 输入节点特征的维度。
            hidden_channels (int): 隐藏层的维度。
            out_channels (int): 输出图嵌入的维度。
            num_layers (int): Transformer层的数量。
            heads (int): 注意力头数。
        """
        super().__init__()
        
        # 输入维度要乘以头数，以匹配TransformerConv的内部处理
        self.node_emb = nn.Linear(in_channels, hidden_channels * heads)
        
        self.layers = nn.ModuleList()
        for _ in range(num_layers):
            # TransformerConv的输入和输出维度都是 hidden_channels * heads
            self.layers.append(
                TransformerConv(hidden_channels * heads, hidden_channels, heads=heads)
            )
            
        self.pool = global_add_pool
        self.out = nn.Linear(hidden_channels * heads, out_channels)

    def forward(self, data):
        """
        前向传播。

        Args:
            data: PyTorch Geometric 的 Data 对象。

        Returns:
            torch.Tensor: 图的嵌入向量。
        """
        x, edge_index, batch = data.x, data.edge_index, data.batch
        
        # 初始节点嵌入
        x = self.node_emb(x)
        
        # Transformer层
        for layer in self.layers:
            x = layer(x, edge_index).relu()
            
        # 全局池化
        graph_embedding = self.pool(x, batch)
        
        # 输出层
        output = self.out(graph_embedding)
        
        return output 