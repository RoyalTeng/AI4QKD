"""
AI4QKD - 测试配置文件

重构思路：
- 参考GitHub master分支的测试配置思路
- 提供全局测试fixture和配置
- 支持理想化模式和现实模式切换测试
- 简化测试环境的设置和清理

设计原则：
- 统一的测试环境配置
- 可重用的测试数据fixture
- 清晰的测试模式管理
- 完善的测试清理机制

主要改进：
- 更简洁的fixture设计
- 更好的测试隔离
- 更全面的配置管理
- 更直观的模式切换

作者: Claude (AI Assistant)
重构日期: 2025-08-17
参考版本: GitHub master分支测试配置
"""

import pytest
import os
import tempfile
import shutil
from typing import Generator, Dict, Any


# =============================================================================
# 重构说明: 此配置文件基于GitHub master分支的测试框架重构
# 重构日期: 2025-08-17
# 重构原因: 简化测试配置，提高测试可维护性
# 主要改进: 统一fixture管理，简化模式切换，改进环境隔离
# 参考文件: 原有测试文件中的fixture和配置模式
# =============================================================================


@pytest.fixture(scope="session")
def test_environment():
    """
    测试环境session级fixture
    
    重构思路：
    - 提供整个测试会话的全局配置
    - 设置测试专用的临时目录
    - 配置无显示环境（支持CI/CD）
    - 确保测试环境的隔离性
    """
    # 设置matplotlib为非交互式后端（支持无显示环境）
    try:
        import matplotlib
        matplotlib.use('Agg')
    except ImportError:
        pass  # matplotlib未安装时跳过
    
    # 创建测试专用临时目录
    test_temp_dir = tempfile.mkdtemp(prefix="ai4qkd_test_")
    
    # 测试环境配置
    env_config = {
        "temp_dir": test_temp_dir,
        "test_mode": True,
        "verbose": False
    }
    
    yield env_config
    
    # 清理测试环境
    if os.path.exists(test_temp_dir):
        shutil.rmtree(test_temp_dir, ignore_errors=True)


@pytest.fixture
def idealized_mode_context():
    """
    理想化模式上下文fixture
    
    重构思路：
    - 基于原有的理想化模式设计
    - 提供模式切换的上下文管理
    - 确保测试后模式状态恢复
    - 支持临时模式切换测试
    """
    # TODO: 实现理想化模式后启用
    # from qcgf_dsl import is_idealized_mode, set_idealized_mode
    # 
    # # 保存当前模式状态
    # original_mode = is_idealized_mode()
    # 
    # def switch_mode(idealized: bool):
    #     """切换测试模式"""
    #     set_idealized_mode(idealized)
    #     return idealized
    # 
    # yield switch_mode
    # 
    # # 恢复原始模式状态
    # set_idealized_mode(original_mode)
    
    # 临时返回一个占位函数
    def placeholder_switch(idealized: bool):
        return idealized
    yield placeholder_switch


@pytest.fixture
def temp_file_manager(test_environment):
    """
    临时文件管理fixture
    
    重构思路：
    - 提供统一的临时文件管理
    - 自动清理测试文件
    - 支持多种文件类型
    - 确保测试间的文件隔离
    """
    temp_files = []
    temp_dir = test_environment["temp_dir"]
    
    def create_temp_file(suffix=".tmp", content=None):
        """创建临时文件"""
        fd, filepath = tempfile.mkstemp(suffix=suffix, dir=temp_dir)
        temp_files.append(filepath)
        
        if content:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            os.close(fd)
        
        return filepath
    
    yield create_temp_file
    
    # 清理所有临时文件
    for filepath in temp_files:
        if os.path.exists(filepath):
            os.unlink(filepath)


@pytest.fixture
def sample_protocol_data():
    """
    样例协议数据fixture
    
    重构思路：
    - 基于原有的测试协议数据结构
    - 提供标准化的测试数据
    - 支持不同协议类型的测试
    - 简化测试数据的创建
    """
    # BB84协议的标准测试数据
    bb84_data = {
        "name": "BB84_Test",
        "nodes": {
            "alice_qsp": {
                "type": "QSP",
                "party": "Alice",
                "params": {
                    "state": "|0⟩",
                    "fidelity": 0.99,
                    "preparation_time": 1e-9
                }
            },
            "quantum_channel": {
                "type": "QC", 
                "party": None,
                "params": {
                    "loss": 0.1,
                    "noise": 0.01,
                    "distance": 50.0
                }
            },
            "bob_qm": {
                "type": "QM",
                "party": "Bob",
                "params": {
                    "basis": "computational",
                    "efficiency": 0.8,
                    "dark_count_rate": 1e-6
                }
            }
        },
        "edges": [
            {
                "source": "alice_qsp",
                "target": "quantum_channel",
                "type": "quantum",
                "params": {}
            },
            {
                "source": "quantum_channel", 
                "target": "bob_qm",
                "type": "quantum",
                "params": {}
            }
        ]
    }
    
    # MDI-QKD协议的测试数据
    mdi_qkd_data = {
        "name": "MDI_QKD_Test",
        "nodes": {
            "alice_qsp": {
                "type": "QSP",
                "party": "Alice", 
                "params": {"state": "|+⟩", "fidelity": 0.95}
            },
            "bob_qsp": {
                "type": "QSP",
                "party": "Bob",
                "params": {"state": "|+⟩", "fidelity": 0.95}
            },
            "charlie_bsm": {
                "type": "BSM",
                "party": "Charlie",
                "params": {"efficiency": 0.5}
            }
        },
        "edges": [
            {
                "source": "alice_qsp",
                "target": "charlie_bsm", 
                "type": "quantum",
                "params": {}
            },
            {
                "source": "bob_qsp",
                "target": "charlie_bsm",
                "type": "quantum", 
                "params": {}
            }
        ]
    }
    
    return {
        "bb84": bb84_data,
        "mdi_qkd": mdi_qkd_data
    }


@pytest.fixture
def sample_bb84_protocol():
    """
    创建标准BB84协议的测试固件
    
    重构思路：
    - 使用重构后的qcgf_dsl模块创建BB84协议
    - 提供完整的ProtocolGraph对象用于测试
    - 支持各种测试场景的需求
    """
    from qcgf_dsl import create_bb84_protocol
    return create_bb84_protocol()


@pytest.fixture
def sample_dsl_texts():
    """
    样例DSL文本fixture
    
    重构思路：
    - 基于原有的DSL文本格式
    - 提供多种协议的DSL样例
    - 支持解析器测试用例
    - 包含正确和错误的DSL样例
    """
    # 正确的BB84协议DSL
    valid_bb84_dsl = """
    # BB84协议标准实现
    QSP alice_state: party="Alice", state="|0⟩", fidelity=0.99
    QC quantum_link: loss=0.1, noise=0.01, distance=50.0
    QM bob_detector: party="Bob", basis="computational", efficiency=0.8
    
    # 协议连接
    alice_state -> quantum_link [quantum]
    quantum_link -> bob_detector [quantum]
    """
    
    # 包含错误的DSL（用于错误处理测试）
    invalid_dsl_samples = {
        "invalid_node_type": "UNKNOWN_TYPE node1: param=value",
        "invalid_edge_type": """
        QSP node1: state="|0⟩"
        QM node2: basis="Z"
        node1 -> node2 [INVALID_EDGE]
        """,
        "missing_required_param": "QSP node1: fidelity=0.99",  # 缺少state参数
        "invalid_syntax": "QSP node1 invalid syntax here"
    }
    
    # 复杂协议DSL（用于性能测试）
    complex_protocol_dsl = """
    # 复杂多节点协议
    QSP alice_prep1: party="Alice", state="|0⟩"
    QSP alice_prep2: party="Alice", state="|1⟩"
    QG alice_gate: gate_type="H", fidelity=0.99
    QC channel1: loss=0.05, distance=25.0
    QC channel2: loss=0.05, distance=25.0
    QM bob_measure1: party="Bob", basis="X", efficiency=0.9
    QM bob_measure2: party="Bob", basis="Z", efficiency=0.9
    CLO processing: party="Bob", operation="correlation_analysis"
    
    # 复杂连接结构
    alice_prep1 -> alice_gate [quantum]
    alice_prep2 -> channel2 [quantum]
    alice_gate -> channel1 [quantum]
    channel1 -> bob_measure1 [quantum]
    channel2 -> bob_measure2 [quantum]
    bob_measure1 -> processing [classical]
    bob_measure2 -> processing [classical]
    """
    
    return {
        "valid_bb84": valid_bb84_dsl,
        "invalid_samples": invalid_dsl_samples,
        "complex_protocol": complex_protocol_dsl
    }


@pytest.fixture(params=["realistic", "idealized"])
def test_mode(request, idealized_mode_context):
    """
    参数化测试模式fixture
    
    重构思路：
    - 支持同一测试在不同模式下运行
    - 自动切换理想化/现实模式
    - 确保测试覆盖两种模式
    - 简化模式相关测试的编写
    """
    mode = request.param
    is_idealized = (mode == "idealized")
    
    # 切换到对应模式
    idealized_mode_context(is_idealized)
    
    return {
        "mode": mode,
        "is_idealized": is_idealized
    }


@pytest.fixture
def performance_monitor():
    """
    性能监控fixture
    
    重构思路：
    - 提供统一的性能测试工具
    - 支持执行时间和内存使用监控
    - 建立性能基准和回归检测
    - 简化性能测试的实现
    """
    import time
    import psutil
    import os
    
    class PerformanceMonitor:
        def __init__(self):
            self.start_time = None
            self.start_memory = None
            self.process = psutil.Process(os.getpid())
        
        def start(self):
            """开始监控"""
            self.start_time = time.time()
            self.start_memory = self.process.memory_info().rss
        
        def stop(self):
            """停止监控并返回结果"""
            end_time = time.time()
            end_memory = self.process.memory_info().rss
            
            return {
                "execution_time": end_time - self.start_time if self.start_time else 0,
                "memory_delta": end_memory - self.start_memory if self.start_memory else 0,
                "peak_memory": self.process.memory_info().rss
            }
        
        def assert_performance(self, max_time=None, max_memory_mb=None):
            """断言性能要求"""
            results = self.stop()
            
            if max_time and results["execution_time"] > max_time:
                pytest.fail(f"执行时间 {results['execution_time']:.3f}s 超过限制 {max_time}s")
            
            if max_memory_mb:
                memory_mb = results["memory_delta"] / (1024 * 1024)
                if memory_mb > max_memory_mb:
                    pytest.fail(f"内存使用 {memory_mb:.1f}MB 超过限制 {max_memory_mb}MB")
            
            return results
    
    return PerformanceMonitor()


# 测试标记定义
def pytest_configure(config):
    """
    pytest配置
    
    重构思路：
    - 定义统一的测试标记
    - 配置测试分类和过滤
    - 支持不同级别的测试运行
    """
    # 注册自定义测试标记
    config.addinivalue_line("markers", "unit: 单元测试标记")
    config.addinivalue_line("markers", "integration: 集成测试标记") 
    config.addinivalue_line("markers", "performance: 性能测试标记")
    config.addinivalue_line("markers", "compatibility: 兼容性测试标记")
    config.addinivalue_line("markers", "slow: 慢速测试标记")
    config.addinivalue_line("markers", "requires_qiskit: 需要Qiskit的测试")
    config.addinivalue_line("markers", "requires_display: 需要显示设备的测试")


def pytest_collection_modifyitems(config, items):
    """
    修改测试收集
    
    重构思路：
    - 自动为测试添加适当标记
    - 支持条件跳过测试
    - 优化测试运行顺序
    """
    # 为需要外部依赖的测试添加标记
    for item in items:
        # 检查是否需要Qiskit
        if "qiskit" in item.name.lower() or "quantum_circuit" in item.name.lower():
            item.add_marker(pytest.mark.requires_qiskit)
        
        # 检查是否需要显示设备
        if "visualization" in item.name.lower() or "plot" in item.name.lower():
            item.add_marker(pytest.mark.requires_display)
        
        # 标记性能测试
        if "performance" in item.name.lower() or "benchmark" in item.name.lower():
            item.add_marker(pytest.mark.performance)
            item.add_marker(pytest.mark.slow)


# 跳过条件定义
def pytest_runtest_setup(item):
    """
    测试运行前的设置检查
    
    重构思路：
    - 检查测试运行的前置条件
    - 自动跳过不满足条件的测试
    - 提供清晰的跳过原因
    """
    # 检查Qiskit依赖
    if item.get_closest_marker("requires_qiskit"):
        try:
            import qiskit
        except ImportError:
            pytest.skip("Qiskit is required but not installed")
    
    # 检查显示环境
    if item.get_closest_marker("requires_display"):
        if os.environ.get("CI") or not os.environ.get("DISPLAY"):
            pytest.skip("Display environment required but not available")