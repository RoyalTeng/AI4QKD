import pytest
import os
import logging
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock

from utils.logger import setup_logger
from utils.metrics import compute_key_rate_metrics, track_drl_learning_curve, calculate_protocol_complexity
from utils.data_processor import normalize_results, compare_graphs
from utils.visualization import plot_learning_curve, plot_qber_gain_evolution

class TestLogger:
    def test_setup_logger(self, tmp_path):
        log_file = tmp_path / "test.log"
        logger = setup_logger(log_level="DEBUG", log_file=str(log_file))
        assert logger.level == logging.DEBUG
        assert any(isinstance(h, logging.FileHandler) for h in logger.handlers)
        
        # 测试日志写入
        test_message = "This is a test message"
        logger.info(test_message)
        
        with open(log_file, 'r') as f:
            content = f.read()
            assert test_message in content

class TestMetrics:
    def test_compute_key_rate_metrics(self):
        results = [
            {"key_rate": 0.1, "qber": 0.02},
            {"key_rate": 0.15, "qber": 0.015},
            {"key_rate": 0.12, "qber": 0.018},
        ]
        metrics = compute_key_rate_metrics(results)
        assert "average_key_rate" in metrics
        assert pytest.approx(metrics["average_key_rate"]) == np.mean([0.1, 0.15, 0.12])

    def test_track_drl_learning_curve(self):
        rewards = [1.0, 1.5, 2.0, 1.8, 2.2]
        metrics = track_drl_learning_curve(rewards)
        assert "total_reward" in metrics
        assert "moving_average_reward" in metrics
        assert len(metrics["moving_average_reward"]) == len(rewards)

    def test_calculate_protocol_complexity(self):
        # Mock a graph object
        mock_graph = MagicMock()
        mock_graph.get_node_count.return_value = 10
        mock_graph.get_edge_count.return_value = 9
        complexity = calculate_protocol_complexity(mock_graph)
        assert complexity == 19

class TestDataProcessor:
    def test_normalize_results(self):
        data = {'a': [1, 2, 3], 'b': [10, 20, 30]}
        df = pd.DataFrame(data)
        df_normalized = normalize_results(df, ['a', 'b'])
        assert df_normalized['a'].min() == 0.0
        assert df_normalized['a'].max() == 1.0
        assert df_normalized['b'].min() == 0.0
        assert df_normalized['b'].max() == 1.0
        
    def test_compare_graphs(self):
        mock_g1 = MagicMock()
        mock_g1.get_node_count.return_value = 10
        mock_g1.get_edge_count.return_value = 10
        
        mock_g2 = MagicMock()
        mock_g2.get_node_count.return_value = 8
        mock_g2.get_edge_count.return_value = 9
        
        similarity = compare_graphs(mock_g1, mock_g2)
        assert 0 <= similarity <= 1

# 可视化函数的测试通常是检查它们是否能成功运行而不报错
class TestVisualization:
    @patch('matplotlib.pyplot.show')
    def test_plot_learning_curve(self, mock_show):
        rewards = [1.0, 1.5, 2.0, 1.8, 2.2]
        plot_learning_curve(rewards)
        mock_show.assert_called_once()

    @patch('matplotlib.pyplot.show')
    def test_plot_qber_gain_evolution(self, mock_show):
        history = [
            {"qber": 0.02, "gain": 0.9},
            {"qber": 0.022, "gain": 0.88},
        ]
        plot_qber_gain_evolution(history)
        mock_show.assert_called_once()
