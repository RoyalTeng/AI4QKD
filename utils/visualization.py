from typing import List, Dict, Any, Optional
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from qcgf_dsl.protocol_graph import ProtocolGraph
import numpy as np

# 我们假设 qcgf_dsl.visualizer 中有 ProtocolVisualizer
# 如果导入失败，说明需要先完成那个模块
try:
    from qcgf_dsl.visualizer import ProtocolVisualizer
except ImportError:
    print("警告: qcgf_dsl.visualizer.ProtocolVisualizer 未找到，部分可视化功能将不可用。")
    ProtocolVisualizer = None


def plot_learning_curve(rewards: List[float],
                        title: str = "DRL Learning Curve",
                        save_path: Optional[str] = None):
    """
    绘制并保存DRL智能体的学习曲线。

    Args:
        rewards (List[float]): 每一步或每个episode的奖励列表。
        title (str, optional): 图表标题. Defaults to "DRL Learning Curve".
        save_path (Optional[str], optional): 保存路径 (e.g., 'drl_curve.png'). 
                                           如果为None, 则只显示不保存. Defaults to None.
    """
    sns.set_theme(style="darkgrid")
    plt.figure(figsize=(12, 6))
    plt.plot(rewards, label="原始奖励", alpha=0.6)
    
    # 计算移动平均
    if len(rewards) >= 10:
        moving_avg = pd.Series(rewards).rolling(window=100, min_periods=1).mean()
        plt.plot(moving_avg, label="移动平均 (100 episodes)", linewidth=2)
    
    plt.title(title, fontsize=16)
    plt.xlabel("轮次 (Episode)", fontsize=12)
    plt.ylabel("奖励 (Reward)", fontsize=12)
    plt.legend()
    plt.grid(True)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()

def plot_qber_gain_evolution(history: List[Dict[str, float]],
                             title: str = "QBER and Gain Evolution",
                             save_path: Optional[str] = None):
    """
    绘制QBER和Gain随优化的演化趋势。

    Args:
        history (List[Dict[str, float]]): 历史记录，每个字典包含 'qber' 和 'gain'。
        title (str, optional): 图表标题. Defaults to "QBER and Gain Evolution".
        save_path (Optional[str], optional): 保存路径. Defaults to None.
    """
    if not history:
        print("历史记录为空，无法绘图。")
        return
        
    df = pd.DataFrame(history)
    sns.set_theme(style="whitegrid")
    
    fig, ax1 = plt.subplots(figsize=(12, 6))

    color = 'tab:red'
    ax1.set_xlabel('优化步骤 (Optimization Step)', fontsize=12)
    ax1.set_ylabel('QBER', color=color, fontsize=12)
    ax1.plot(df.get('qber'), color=color, marker='o', linestyle='--', label='QBER')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.legend(loc='upper left')

    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('增益 (Gain)', color=color, fontsize=12)
    ax2.plot(df.get('gain'), color=color, marker='x', linestyle='-', label='Gain')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.legend(loc='upper right')

    plt.title(title, fontsize=16)
    fig.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()

def visualize_protocol_graph(graph: ProtocolGraph, save_path: Optional[str] = None):
    """
    对 qcgf_dsl.visualizer 的一个简单包装，用于统一可视化接口。
    """
    if ProtocolVisualizer:
        visualizer = ProtocolVisualizer() # 假设这个类存在且可配置
        visualizer.visualize(graph) # 假设 visualize 方法会显示
    else:
        print("ProtocolVisualizer 不可用，无法绘制协议图。")

    # 注意：此处的plt.savefig可能无法捕获由visualizer.visualize创建的图，
    # 除非visualizer将其绘制在当前的matplotlib上下文中。
    # 更稳健的方法是在ProtocolVisualizer的visualize方法中直接支持save_path参数。
    # if save_path and ProtocolVisualizer:
    #     try:
    #         plt.savefig(save_path, dpi=300, bbox_inches='tight')
    #     except Exception as e:
    #         print(f"保存协议图失败: {e}")

def plot_multi_curve_comparison(data: Dict[str, Dict], 
                                title: str, 
                                xlabel: str, 
                                ylabel: str, 
                                save_path: Optional[str] = None):
    """
    绘制多条曲线进行对比。

    Args:
        data (Dict[str, Dict]): 一个字典，键是曲线的标签，值是包含 'x' 和 'y' 列表的字典。
        title (str): 图表标题。
        xlabel (str): x轴标签。
        ylabel (str): y轴标签。
        save_path (Optional[str], optional): 保存路径。
    """
    sns.set_theme(style="darkgrid")
    plt.figure(figsize=(12, 8))

    for label, curve_data in data.items():
        plt.plot(curve_data['x'], curve_data['y'], marker='o', linestyle='-', label=label)

    plt.title(title, fontsize=16)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.legend()
    plt.grid(True)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()

def plot_performance_comparison(original_metrics: Dict, 
                                optimized_metrics: Dict,
                                title: str = "优化前后性能对比",
                                save_path: Optional[str] = None):
    """
    使用条形图对比优化前后的性能指标。

    Args:
        original_metrics (Dict): 原始协议的指标字典 (qber, gain, key_rate)。
        optimized_metrics (Dict): 优化后协议的指标字典。
        title (str): 图表标题。
        save_path (Optional[str], optional): 保存路径。
    """
    labels = ['QBER', 'Gain', 'Secure Key Rate']
    original_values = [
        original_metrics.get('qber', 0),
        original_metrics.get('gain', 0),
        original_metrics.get('secure_key_rate', 0)
    ]
    optimized_values = [
        optimized_metrics.get('qber', 0),
        optimized_metrics.get('gain', 0),
        optimized_metrics.get('secure_key_rate', 0)
    ]

    x = np.arange(len(labels))
    width = 0.35

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(12, 7))
    rects1 = ax.bar(x - width/2, original_values, width, label='原始协议')
    rects2 = ax.bar(x + width/2, optimized_values, width, label='优化后协议')

    ax.set_ylabel('指标值')
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    ax.bar_label(rects1, padding=3, fmt='%.4f')
    ax.bar_label(rects2, padding=3, fmt='%.4f')

    fig.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show() 