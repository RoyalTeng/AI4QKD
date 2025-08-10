"""
协议图可视化模块

实现了QCGF DSL协议图的可视化功能，支持多种布局和样式。
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import networkx as nx
import numpy as np
from typing import Dict, Tuple, Optional

# A dirty hack to make the test pass in a virtual environment
# 一个临时的hack，使得在虚拟环境中测试能够通过
try:
    from qcgf_dsl.protocol_graph import ProtocolGraph
    from qcgf_dsl.node_types import NodeType, Party
    from qcgf_dsl.edge_types import EdgeType
except ImportError:
    from .protocol_graph import ProtocolGraph
    from .node_types import NodeType, Party
    from .edge_types import EdgeType


class ProtocolVisualizer:
    """
    协议图可视化器
    
    提供多种可视化选项，包括节点布局、颜色方案、标签显示等。
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        初始化可视化器

        Args:
            config: 可视化配置字典
        """
        self.config = config or self._get_default_config()

    def _get_default_config(self) -> Dict:
        """获取默认配置"""
        return {
            "figsize": (16, 12),
            "node_size": 3000,
            "font_size": 9,
            "arrow_size": 20,
            "layout": "kamada_kawai",  # spring, circular, kamada_kawai, shell
            "node_colors": {
                NodeType.QSP: "#FF6B6B",
                NodeType.QC: "#4ECDC4",
                NodeType.QM: "#45B7D1",
                NodeType.CLO: "#F9A825",
                NodeType.QG: "#96CEB4",
                NodeType.QD: "#FFEAA7",
                NodeType.CS: "#DDA0DD",
                NodeType.CC: "#F7DC6F",
                NodeType.ATTACK: "#C0392B",
                NodeType.SINK: "#27AE60",
            },
            "edge_colors": {
                EdgeType.QUANTUM: "#E74C3C",
                EdgeType.CLASSICAL: "#3498DB",
                EdgeType.CONTROL: "#F39C12",
                EdgeType.DATA: "#8E44AD",
                EdgeType.FEEDBACK: "#16A085",
                EdgeType.SYNCHRONIZATION: "#7F8C8D",
            },
            "party_box_colors": {
                Party.ALICE: (1.0, 0.42, 0.42, 0.1),
                Party.BOB: (0.31, 0.8, 0.77, 0.1),
                Party.CHARLIE: (0.98, 0.66, 0.15, 0.1),
                Party.EVE: (0.75, 0.22, 0.17, 0.1),
            },
        }

    def visualize(self, graph: ProtocolGraph, ax: Optional[plt.Axes] = None) -> None:
        """
        可视化协议图

        Args:
            graph: ProtocolGraph实例
            ax: Matplotlib的Axes对象 (可选)
        """
        # 强制设置中文字体，解决大部分中文显示问题
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
        plt.rcParams['axes.unicode_minus'] = False
        
        if graph.get_node_count() == 0:
            print("Graph is empty, cannot visualize.")
            return

        # 标记是否由本函数创建图窗，以决定是否调用plt.show()
        show_after_draw = False
        if ax is None:
            _fig, ax = plt.subplots(figsize=self.config["figsize"])
            show_after_draw = True

        # 1. Calculate layout
        pos = self._get_layout(graph)

        # 2. Draw party boxes
        self._draw_party_boxes(ax, graph, pos)

        # 3. Draw edges
        self._draw_edges(ax, graph, pos)

        # 4. Draw nodes
        self._draw_nodes(ax, graph, pos)
        
        # 5. Draw labels
        self._draw_labels(ax, graph, pos)

        ax.set_title(f"Protocol Graph: {graph.name}", fontsize=16, fontweight="bold")
        ax.axis("off")
        
        # 只有当图窗是内部创建时，才自动显示
        if show_after_draw:
            plt.tight_layout()
            plt.show()

    def _get_layout(self, graph: ProtocolGraph) -> Dict:
        """计算节点布局"""
        layout_type = self.config.get("layout", "kamada_kawai")
        if layout_type == "spring":
            return nx.spring_layout(graph.graph, k=0.9, iterations=50, seed=42)
        elif layout_type == "circular":
            return nx.circular_layout(graph.graph)
        elif layout_type == "shell":
            return nx.shell_layout(graph.graph)
        else: # kamada_kawai
            return nx.kamada_kawai_layout(graph.graph)

    def _draw_party_boxes(self, ax: plt.Axes, graph: ProtocolGraph, pos: Dict) -> None:
        """绘制参与者区域背景框"""
        party_nodes = {party: [] for party in Party}
        for node_id in graph.graph.nodes():
            node = graph.get_node(node_id)
            if node and node.party:
                party_enum_member = Party(node.party) if isinstance(node.party, str) else node.party
                party_nodes[party_enum_member].append(node_id)
        
        for party, nodes in party_nodes.items():
            if not nodes:
                continue
            
            points = [pos[n] for n in nodes]
            if not points:
                continue
                
            points_arr = np.array(points)
            min_x, min_y = points_arr.min(axis=0)
            max_x, max_y = points_arr.max(axis=0)
            
            padding = 0.2
            rect = patches.Rectangle(
                (min_x - padding, min_y - padding),
                max_x - min_x + 2 * padding,
                max_y - min_y + 2 * padding,
                linewidth=1,
                edgecolor='gray',
                facecolor=self.config["party_box_colors"].get(party, (0.5, 0.5, 0.5, 0.1)),
                linestyle="--",
                label=party.value
            )
            ax.add_patch(rect)
            ax.text(max_x + padding, max_y + padding, party.value, fontsize=14, fontweight="bold", ha="right", va="top")

    def _draw_edges(self, ax: plt.Axes, graph: ProtocolGraph, pos: Dict) -> None:
        """绘制边"""
        edge_colors = [
            self.config["edge_colors"].get(data.get("edge_type"), "#333333")
            for _, _, data in graph.graph.edges(data=True)
        ]
        nx.draw_networkx_edges(
            graph.graph,
            pos,
            ax=ax,
            edge_color=edge_colors,
            width=2.0,
            alpha=0.8,
            arrows=True,
            arrowsize=self.config["arrow_size"],
            connectionstyle="arc3,rad=0.1",
        )

    def _draw_nodes(self, ax: plt.Axes, graph: ProtocolGraph, pos: Dict) -> None:
        """绘制节点"""
        node_colors = [
            self.config["node_colors"].get(graph.get_node(node_id).node_type, "#CCCCCC")
            for node_id in graph.graph.nodes()
        ]
        nx.draw_networkx_nodes(
            graph.graph,
            pos,
            ax=ax,
            node_size=self.config["node_size"],
            node_color=node_colors,
            edgecolors="black",
            linewidths=1.0,
            alpha=0.9,
        )

    def _draw_labels(self, ax: plt.Axes, graph: ProtocolGraph, pos: Dict) -> None:
        """绘制标签"""
        labels = {}
        for node_id in graph.graph.nodes():
            node = graph.get_node(node_id)
            if node:
                labels[node_id] = f"{node.node_type.value}\n({node_id})"

        nx.draw_networkx_labels(
            graph.graph,
            pos,
            labels=labels,
            ax=ax,
            font_size=self.config["font_size"],
            font_weight="bold",
            font_color="black",
        )
        
        edge_labels = {
            (u, v): d.get("edge_type").value
            for u, v, d in graph.graph.edges(data=True)
        }
        nx.draw_networkx_edge_labels(
            graph.graph,
            pos,
            edge_labels=edge_labels,
            ax=ax,
            font_size=self.config["font_size"] - 1,
            font_color="firebrick",
        )

def visualize_protocol(graph: ProtocolGraph, save_path: Optional[str] = None, config: Optional[Dict] = None, ax: Optional[plt.Axes] = None):
    """
    可视化协议图的便捷函数

    Args:
        graph (ProtocolGraph): 要可视化的ProtocolGraph实例。
        save_path (Optional[str], optional): 保存可视化结果的文件路径。如果为None，则显示图像。
        config (Optional[Dict], optional): 可视化配置字典。
        ax (Optional[plt.Axes], optional): Matplotlib的Axes对象。
    """
    visualizer = ProtocolVisualizer(config)
    
    # 如果没有提供ax，则自己创建figure和ax
    fig, current_ax = (None, ax)
    if current_ax is None:
        fig, current_ax = plt.subplots(figsize=visualizer.config.get("figsize", (16, 12)))
        
    visualizer.visualize(graph, current_ax)
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        print(f"协议图已保存至: {save_path}")
    
    # 只有当fig是内部创建时，才显示和关闭
    if fig:
        plt.show()
        plt.close(fig)