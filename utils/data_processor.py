from typing import Dict, Any, List
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from qcgf_dsl.protocol_graph import ProtocolGraph

def normalize_results(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    对指定的列进行Min-Max规范化。

    Args:
        df (pd.DataFrame): 包含数据的DataFrame。
        columns (List[str]): 需要规范化的列名列表。

    Returns:
        pd.DataFrame: 包含规范化后数据的新DataFrame。
    """
    scaler = MinMaxScaler()
    df_normalized = df.copy()
    df_normalized[columns] = scaler.fit_transform(df[columns])
    return df_normalized

def graph_to_dict(graph: ProtocolGraph) -> Dict[str, Any]:
    """
    将ProtocolGraph对象序列化为字典。
    (这通常在ProtocolGraph类中实现，这里只是一个包装或示例)

    Args:
        graph (ProtocolGraph): 协议图对象。

    Returns:
        Dict[str, Any]: 图的字典表示。
    """
    return graph.to_dict()

def dict_to_graph(graph_dict: Dict[str, Any]) -> ProtocolGraph:
    """
    从字典反序列化为ProtocolGraph对象。
    (这通常在ProtocolGraph类中实现，这里只是一个包装或示例)

    Args:
        graph_dict (Dict[str, Any]): 图的字典表示。

    Returns:
        ProtocolGraph: 协议图对象。
    """
    return ProtocolGraph.from_dict(graph_dict)

def compare_graphs(g1: ProtocolGraph, g2: ProtocolGraph) -> float:
    """
    比较两个协议图的结构相似性（一个简单的示例）。
    使用图编辑距离。

    Args:
        g1 (ProtocolGraph): 第一个图。
        g2 (ProtocolGraph): 第二个图。

    Returns:
        float: 相似度得分 (0到1之间，1表示完全相同)。
    """
    # networkx有近似图编辑距离的函数，但可能需要额外安装
    # import networkx as nx
    # ged = nx.graph_edit_distance(g1.graph, g2.graph)
    # 这是一个简化的替代方案：比较节点和边的数量
    
    nodes1 = g1.get_node_count()
    edges1 = g1.get_edge_count()
    nodes2 = g2.get_node_count()
    edges2 = g2.get_edge_count()
    
    node_similarity = 1 - abs(nodes1 - nodes2) / max(nodes1, nodes2, 1)
    edge_similarity = 1 - abs(edges1 - edges2) / max(edges1, edges2, 1)
    
    return (node_similarity + edge_similarity) / 2 