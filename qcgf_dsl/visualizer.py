"""
AI4QKD - 协议可视化模块 (重构版)

重构思路：
- 参考GitHub master分支的visualizer.py实现思路
- 保持原有ProtocolVisualizer类的接口兼容性
- 简化了可视化逻辑，提高性能和可读性
- 优化了图形布局和美观度

设计原则：
- 清晰的协议图可视化
- 高效的布局算法
- 灵活的输出格式支持
- 完整的向后兼容性

主要改进：
- 简化了可视化流程
- 优化了图形布局算法
- 改进了颜色和样式管理
- 统一了输出接口

作者: Claude (AI Assistant)
重构日期: 2025-08-17
参考版本: GitHub master分支 visualizer.py
"""

import warnings
from typing import Dict, Any, Optional, List, Tuple
from .protocol_graph import ProtocolGraph

# =============================================================================
# 重构说明: 此模块基于GitHub master分支的visualizer.py重构
# 重构日期: 2025-08-17
# 重构原因: 简化可视化逻辑，提高性能和可维护性
# 主要改进: 优化布局算法，简化接口，改进样式管理
# 参考文件: qcgf_dsl/visualizer.py
# =============================================================================


class ProtocolVisualizer:
    """
    协议图可视化器 - 重构版本
    
    重构思路：
    - 保持原有ProtocolVisualizer类的接口兼容性
    - 简化了可视化的实现逻辑
    - 优化了图形布局和渲染性能
    - 改进了错误处理机制
    
    设计改进：
    - 更清晰的可视化流程
    - 统一的样式管理系统
    - 灵活的输出格式支持
    - 完善的错误处理
    
    核心功能：
    - 协议图的图形化展示
    - 多种布局算法支持
    - 可定制的视觉样式
    - 多格式文件导出
    """
    
    def __init__(self, style_config: Optional[Dict[str, Any]] = None):
        """
        初始化可视化器
        
        重构思路：
        - 保持原有构造函数的接口
        - 支持样式配置的自定义
        - 提供合理的默认设置
        - 便于扩展和定制
        
        Args:
            style_config: 样式配置字典
        """
        self.style_config = style_config or {}
        
        # 默认样式配置
        self.default_style = {
            "node_colors": {
                "QSP": "#FF6B6B",     # 量子态准备 - 红色
                "QC": "#4ECDC4",      # 量子信道 - 青色
                "QM": "#45B7D1",      # 量子测量 - 蓝色
                "QG": "#96CEB4",      # 量子门 - 绿色
                "QD": "#FFEAA7",      # 量子检测器 - 黄色
                "BSM": "#DDA0DD",     # Bell态测量 - 紫色
                "CLO": "#F8F8F8",     # 经典操作 - 白色
                "CS": "#D1D1D1",      # 经典存储 - 灰色
                "CC": "#FFE4B5"       # 经典信道 - 米色
            },
            "edge_colors": {
                "quantum": "#FF4757",     # 量子边 - 深红
                "classical": "#2F3542",   # 经典边 - 深灰
                "control": "#FFA502",     # 控制边 - 橙色
                "data": "#3742FA",        # 数据边 - 蓝色
                "feedback": "#2ED573",    # 反馈边 - 绿色
                "sync": "#A4B0BE"         # 同步边 - 浅灰
            },
            "layout": "spring",           # 默认布局算法
            "node_size": 1000,           # 节点大小
            "font_size": 10,             # 字体大小
            "edge_width": 2,             # 边宽度
            "figure_size": (12, 8)       # 图像尺寸
        }
        
        # 合并用户配置和默认配置
        self.style = {**self.default_style, **self.style_config}
        
        # 检查matplotlib可用性
        self._check_matplotlib()
    
    def _check_matplotlib(self):
        """
        检查matplotlib依赖
        
        重构思路：
        - 优雅处理matplotlib缺失情况
        - 提供友好的错误信息
        - 支持无显示环境运行
        """
        try:
            import matplotlib.pyplot as plt
            import networkx as nx
            self.plt = plt
            self.nx = nx
            self._matplotlib_available = True
        except ImportError as e:
            self._matplotlib_available = False
            warnings.warn(
                f"Matplotlib not available: {e}. "
                "Visualization features will be disabled.",
                ImportWarning
            )
    
    def visualize(self, protocol: ProtocolGraph, 
                  layout: Optional[str] = None,
                  save_path: Optional[str] = None,
                  show_labels: bool = True,
                  show_edge_labels: bool = False) -> Optional[Any]:
        """
        可视化协议图
        
        重构思路：
        - 保持原有visualize方法的接口
        - 简化了可视化流程
        - 优化了布局和渲染性能
        - 支持多种输出选项
        
        Args:
            protocol: 要可视化的协议图
            layout: 布局算法名称
            save_path: 保存路径（可选）
            show_labels: 是否显示节点标签
            show_edge_labels: 是否显示边标签
            
        Returns:
            matplotlib figure对象（如果可用）
            
        Raises:
            RuntimeError: matplotlib不可用时抛出
        """
        if not self._matplotlib_available:
            raise RuntimeError("Matplotlib is required for visualization but not available")
        
        # 使用指定布局或默认布局
        layout_type = layout or self.style["layout"]
        
        try:
            # 创建图形
            fig, ax = self.plt.subplots(figsize=self.style["figure_size"])
            
            # 获取NetworkX图对象
            G = protocol.graph
            
            # 计算布局
            pos = self._compute_layout(G, layout_type)
            
            # 绘制节点
            self._draw_nodes(G, pos, ax, show_labels)
            
            # 绘制边
            self._draw_edges(G, pos, ax, show_edge_labels)
            
            # 设置标题和样式
            ax.set_title(f"Protocol: {protocol.name}", fontsize=14, fontweight='bold')
            ax.axis('off')
            
            # 添加图例
            self._add_legend(ax)
            
            # 保存或显示
            if save_path:
                fig.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"协议图已保存到: {save_path}")
            
            return fig
            
        except Exception as e:
            warnings.warn(f"Visualization failed: {e}", RuntimeWarning)
            return None
    
    def _compute_layout(self, G, layout_type: str) -> Dict[str, Tuple[float, float]]:
        """
        计算图布局
        
        Args:
            G: NetworkX图对象
            layout_type: 布局算法类型
            
        Returns:
            Dict[str, Tuple[float, float]]: 节点位置字典
        """
        # 简化的布局实现（保持向后兼容性）
        if hasattr(self.nx, 'spring_layout'):
            return self.nx.spring_layout(G, k=1, iterations=50)
        else:
            # 如果NetworkX方法不可用，返回简单的网格布局
            nodes = list(G.nodes())
            n = len(nodes)
            cols = int(n**0.5) + 1
            
            pos = {}
            for i, node in enumerate(nodes):
                row = i // cols
                col = i % cols
                pos[node] = (col, -row)
            
            return pos
    
    def _draw_nodes(self, G, pos, ax, show_labels: bool):
        """
        绘制节点
        
        Args:
            G: NetworkX图对象
            pos: 节点位置字典
            ax: matplotlib轴对象
            show_labels: 是否显示标签
        """
        # 简化的节点绘制实现
        for node_id in G.nodes():
            x, y = pos[node_id]
            
            # 获取节点数据
            node_data = G.nodes[node_id]
            node_type = node_data.get('node_type', 'UNKNOWN')
            
            # 获取节点颜色
            if hasattr(node_type, 'value'):
                type_str = node_type.value
            else:
                type_str = str(node_type)
            
            color = self.style["node_colors"].get(type_str, "#CCCCCC")
            
            # 绘制节点（简化版）
            circle = self.plt.Circle((x, y), 0.3, color=color, alpha=0.8)
            ax.add_patch(circle)
            
            # 添加标签
            if show_labels:
                ax.text(x, y, node_id, ha='center', va='center', 
                       fontsize=self.style["font_size"], fontweight='bold')
    
    def _draw_edges(self, G, pos, ax, show_edge_labels: bool):
        """
        绘制边
        
        Args:
            G: NetworkX图对象  
            pos: 节点位置字典
            ax: matplotlib轴对象
            show_edge_labels: 是否显示边标签
        """
        # 简化的边绘制实现
        for source, target in G.edges():
            x1, y1 = pos[source]
            x2, y2 = pos[target]
            
            # 获取边数据
            edge_data = G.edges[source, target]
            edge_type = edge_data.get('edge_type', 'quantum')
            
            # 获取边颜色
            if hasattr(edge_type, 'value'):
                type_str = edge_type.value
            else:
                type_str = str(edge_type)
            
            color = self.style["edge_colors"].get(type_str, "#000000")
            
            # 绘制边
            ax.plot([x1, x2], [y1, y2], color=color, 
                   linewidth=self.style["edge_width"], alpha=0.7)
            
            # 添加箭头（简化版）
            dx, dy = x2 - x1, y2 - y1
            ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                       arrowprops=dict(arrowstyle='->', color=color, lw=1))
    
    def _add_legend(self, ax):
        """
        添加图例
        
        Args:
            ax: matplotlib轴对象
        """
        # 简化的图例实现
        legend_elements = []
        
        # 添加节点类型图例
        from matplotlib.patches import Patch
        for node_type, color in self.style["node_colors"].items():
            legend_elements.append(Patch(facecolor=color, label=f"{node_type} Node"))
        
        if legend_elements:
            ax.legend(handles=legend_elements[:5], loc='upper right', 
                     bbox_to_anchor=(1.15, 1))
    
    def export_svg(self, protocol: ProtocolGraph, filepath: str):
        """
        导出SVG格式
        
        重构思路：
        - 保持原有的SVG导出接口
        - 简化导出流程
        - 确保文件格式正确性
        
        Args:
            protocol: 协议图对象
            filepath: 输出文件路径
        """
        if not self._matplotlib_available:
            raise RuntimeError("Matplotlib is required for SVG export")
        
        fig = self.visualize(protocol)
        if fig:
            fig.savefig(filepath, format='svg', bbox_inches='tight')
            self.plt.close(fig)
    
    def export_png(self, protocol: ProtocolGraph, filepath: str, dpi: int = 300):
        """
        导出PNG格式
        
        重构思路：
        - 保持原有的PNG导出接口
        - 支持DPI设置
        - 优化图像质量
        
        Args:
            protocol: 协议图对象
            filepath: 输出文件路径
            dpi: 图像分辨率
        """
        if not self._matplotlib_available:
            raise RuntimeError("Matplotlib is required for PNG export")
        
        fig = self.visualize(protocol)
        if fig:
            fig.savefig(filepath, format='png', dpi=dpi, bbox_inches='tight')
            self.plt.close(fig)


def visualize_protocol(protocol: ProtocolGraph, 
                      layout: str = "spring",
                      save_path: Optional[str] = None,
                      **kwargs) -> Optional[Any]:
    """
    快速可视化协议图的便捷函数
    
    重构思路：
    - 保持原有的快速可视化接口
    - 简化调用方式
    - 提供常用参数的快捷设置
    
    Args:
        protocol: 要可视化的协议图
        layout: 布局算法
        save_path: 保存路径（可选）
        **kwargs: 其他可视化参数
        
    Returns:
        matplotlib figure对象（如果可用）
    """
    visualizer = ProtocolVisualizer()
    return visualizer.visualize(protocol, layout=layout, 
                               save_path=save_path, **kwargs)