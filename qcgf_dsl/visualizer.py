"""
协议可视化工具
"""

try:
    import matplotlib.pyplot as plt
    import networkx as nx
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


def visualize_protocol(protocol, save_path=None):
    """
    可视化协议图
    
    Args:
        protocol: ProtocolGraph对象
        save_path: 保存路径（可选）
    """
    if not HAS_MATPLOTLIB:
        print("⚠️  需要matplotlib进行可视化")
        print("安装: pip install matplotlib")
        return
    
    try:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # 左侧：文本信息
        stats = protocol.get_statistics()
        text = f"协议: {stats['name']}\n"
        text += f"节点数: {stats['node_count']}\n"
        text += f"边数: {stats['edge_count']}\n\n"
        text += "节点统计:\n"
        for node_type, count in stats['node_stats'].items():
            text += f"  {node_type}: {count}\n"
        
        ax1.text(0.1, 0.9, text, transform=ax1.transAxes,
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        ax1.set_title("协议信息")
        ax1.axis('off')
        
        # 右侧：图形
        G = protocol.graph
        
        if G.number_of_nodes() > 0:
            # 创建位置
            pos = nx.spring_layout(G, seed=42)
            
            # 节点颜色
            node_colors = []
            for node_id in G.nodes():
                node = G.nodes[node_id]['node']
                if hasattr(node, 'party') and node.party:
                    if node.party.value == 'alice':
                        node_colors.append('lightblue')
                    elif node.party.value == 'bob':
                        node_colors.append('lightgreen')
                    else:
                        node_colors.append('lightgray')
                else:
                    node_colors.append('white')
            
            # 绘制节点
            nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                                  node_size=500, ax=ax2)
            
            # 边颜色
            edge_colors = []
            for source_id, target_id in G.edges():
                edge = G.edges[source_id, target_id]['edge']
                if edge.edge_type == 'quantum':
                    edge_colors.append('blue')
                else:
                    edge_colors.append('red')
            
            # 绘制边
            nx.draw_networkx_edges(G, pos, edge_color=edge_colors, 
                                  width=2, ax=ax2)
            
            # 标签
            labels = {}
            for node_id in G.nodes():
                node = G.nodes[node_id]['node']
                labels[node_id] = f"{node.node_type.value[:10]}\n{node_id}"
            
            nx.draw_networkx_labels(G, pos, labels, font_size=8, ax=ax2)
        
        ax2.set_title("协议图结构")
        ax2.axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"可视化已保存到: {save_path}")
        
        plt.show()
        
    except Exception as e:
        print(f"可视化失败: {e}")


def print_protocol_info(protocol):
    """打印协议信息"""
    stats = protocol.get_statistics()
    
    print("\n" + "=" * 60)
    print(f"协议: {stats['name']}")
    print("=" * 60)
    
    print(f"节点数: {stats['node_count']}")
    print(f"边数: {stats['edge_count']}")
    
    print("\n节点统计:")
    for node_type, count in stats['node_stats'].items():
        print(f"  {node_type}: {count}")
    
    if 'party_stats' in stats and stats['party_stats']:
        print("\n参与者统计:")
        for party, count in stats['party_stats'].items():
            print(f"  {party}: {count}")
    
    print("\n节点详情:")
    for node_id in protocol.graph.nodes():
        node = protocol.graph.nodes[node_id]['node']
        party_info = f" ({node.party.value})" if node.party else ""
        print(f"  {node_id}: {node.node_type.value}{party_info}")
        if node.params:
            print(f"    参数: {node.params}")