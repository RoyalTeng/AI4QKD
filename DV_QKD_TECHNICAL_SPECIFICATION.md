# AI4QKD 离散变量QKD技术规范

**版本**: 1.0  
**日期**: 2025-08-19  
**状态**: 正式发布  
**适用版本**: AI4QKD v2.0.1+

## 📋 文档概述

本文档定义了AI4QKD项目的技术边界和规范，确保项目100%专注于离散变量量子密钥分发（DV-QKD）技术，明确区分并排除连续变量QKD（CV-QKD）相关技术。

## 🎯 技术定位声明

### 核心定位
AI4QKD项目是一个**纯粹的离散变量量子密钥分发（DV-QKD）**研究和开发平台，专注于基于离散量子态的密钥分发协议设计、优化和分析。

### 技术边界
- ✅ **支持**: 所有基于离散量子态的QKD协议和技术
- ❌ **不支持**: 任何连续变量QKD技术和相关概念
- ⚠️ **严格限制**: 禁止引入任何CV-QKD相关参数、算法或概念

## 🔬 DV-QKD技术框架

### 量子态规范

#### 允许的量子态类型
```python
# ✅ 离散量子态 - 严格限定使用
DISCRETE_QUANTUM_STATES = {
    # 计算基态
    "|0⟩": np.array([1, 0]),
    "|1⟩": np.array([0, 1]),
    
    # 叠加态
    "|+⟩": np.array([1, 1]) / np.sqrt(2),
    "|-⟩": np.array([1, -1]) / np.sqrt(2),
    
    # 偏振态
    "|H⟩": np.array([1, 0]),  # 水平偏振
    "|V⟩": np.array([0, 1]),  # 垂直偏振
    "|D⟩": np.array([1, 1]) / np.sqrt(2),  # 对角偏振
    "|A⟩": np.array([1, -1]) / np.sqrt(2), # 反对角偏振
    "|L⟩": np.array([1, 1j]) / np.sqrt(2), # 左圆偏振
    "|R⟩": np.array([1, -1j]) / np.sqrt(2), # 右圆偏振
}
```

#### 禁止的量子态类型
```python
# ❌ 连续变量态 - 严格禁止使用
FORBIDDEN_QUANTUM_STATES = {
    # 相干态
    "coherent_state": "α|α⟩",
    
    # 压缩态  
    "squeezed_state": "S(ξ)|0⟩",
    
    # 热态
    "thermal_state": "混合态 ρ_th",
    
    # 猫态（宏观叠加态）
    "cat_state": "(|α⟩ + |-α⟩)/√2",
}
```

### 编码方式规范

#### DV-QKD编码方式
```python
ENCODING_SCHEMES = {
    "polarization": {
        "type": "偏振编码",
        "bases": ["H/V", "D/A", "L/R"],
        "description": "利用光子偏振态编码信息"
    },
    
    "phase": {
        "type": "相位编码", 
        "bases": ["0/π", "π/2/3π/2"],
        "description": "利用光子相位编码信息"
    },
    
    "time_bin": {
        "type": "时分编码",
        "bases": ["early/late"],
        "description": "利用光子到达时间编码信息"
    },
    
    "frequency": {
        "type": "频率编码",
        "bases": ["ω1/ω2"],
        "description": "利用光子频率编码信息"
    }
}

# ❌ 禁止的编码方式
FORBIDDEN_ENCODINGS = {
    "quadrature_amplitude": "正交振幅调制",
    "gaussian_modulation": "高斯调制",
    "heterodyne_encoding": "外差编码",
    "homodyne_encoding": "零差编码"
}
```

### 测量技术规范

#### DV-QKD测量方式
```python
MEASUREMENT_TECHNIQUES = {
    "single_photon_detection": {
        "detectors": ["APD", "SPAD", "SNS"],
        "principle": "光子计数检测",
        "output": "点击/无点击",
        "threshold": "单光子级别"
    },
    
    "interferometric_detection": {
        "setup": ["Mach-Zehnder", "Michelson"],
        "principle": "干涉测量",
        "output": "探测器点击模式",
        "basis_choice": "主动/被动基选择"
    },
    
    "polarization_analysis": {
        "components": ["PBS", "HWP", "QWP"],
        "principle": "偏振态投影测量",
        "output": "偏振检测结果",
        "basis": "直线/圆偏振基"
    }
}

# ❌ 禁止的测量技术
FORBIDDEN_MEASUREMENTS = {
    "homodyne_detection": "零差检测",
    "heterodyne_detection": "外差检测", 
    "quadrature_measurement": "正交分量测量",
    "threshold_detection": "阈值判决检测"
}
```

## 📊 参数规范体系

### 节点参数分类

#### QSP (量子态准备) 参数
```python
QSP_PARAMETERS = {
    # ✅ 允许的参数
    "state": ["H", "V", "D", "A", "L", "R", "|0⟩", "|1⟩", "|+⟩", "|-⟩"],
    "fidelity": {"type": float, "range": [0.0, 1.0]},
    "preparation_time": {"type": float, "range": [1e-12, 1e-6]},
    "intensity": {"type": float, "range": [0.0, 1.0]},
    "extinction_ratio": {"type": float, "range": [0.0, 1.0]},
    
    # ❌ 禁止的参数
    "discrimination_threshold": "连续变量判决阈值",
    "coherent_amplitude": "相干态振幅",
    "displacement_parameter": "位移参数"
}
```

#### QM (量子测量) 参数
```python
QM_PARAMETERS = {
    # ✅ 允许的参数
    "basis": ["Z", "X", "computational", "hadamard", "circular"],
    "efficiency": {"type": float, "range": [0.0, 1.0]},
    "dark_count_rate": {"type": float, "range": [0.0, 1e-3]},
    "gate_time": {"type": float, "range": [1e-12, 1e-6]},
    "dead_time": {"type": float, "range": [1e-9, 1e-6]},
    "timing_jitter": {"type": float, "range": [0.0, 1e-9]},
    
    # ❌ 禁止的参数  
    "variance": "测量方差",
    "quadrature_phase": "正交相位",
    "homodyne_angle": "零差测量角度"
}
```

#### QC (量子信道) 参数
```python
QC_PARAMETERS = {
    # ✅ 允许的参数
    "loss": {"type": float, "range": [0.0, 1.0]},
    "distance": {"type": float, "range": [0.0, 1000.0]},  # km
    "transmission": {"type": float, "range": [0.0, 1.0]},
    "depolarization_rate": {"type": float, "range": [0.0, 0.5]},
    "background_noise": {"type": float, "range": [0.0, 0.1]},
    "channel_efficiency": {"type": float, "range": [0.0, 1.0]},
    
    # 子类型特定参数
    "FIBER": {
        "attenuation": {"type": float, "range": [0.0, 1.0]},
        "dispersion": {"type": float, "range": [0.0, 100.0]},
        "bend_loss": {"type": float, "range": [0.0, 0.1]}
    },
    
    "FREE_SPACE": {
        "atmospheric_loss": {"type": float, "range": [0.0, 0.9]},
        "turbulence_strength": {"type": float, "range": [0.0, 1.0]},
        "weather_factor": {"type": float, "range": [0.0, 1.0]}
    }
}
```

### 全局参数验证规则

#### 参数命名规范
```python
NAMING_CONVENTIONS = {
    # ✅ 推荐的命名模式
    "recommended_patterns": [
        r"^(efficiency|fidelity|loss|transmission)$",
        r"^(state|basis|polarization)$", 
        r"^.*_(rate|time|ratio|factor)$",
        r"^(dark|background)_.*$"
    ],
    
    # ❌ 禁止的命名模式
    "forbidden_patterns": [
        r".*discrimination.*",
        r".*threshold.*",
        r".*coherent.*",
        r".*squeezed.*",
        r".*quadrature.*",
        r".*homodyne.*",
        r".*heterodyne.*",
        r".*gaussian.*",
        r".*variance.*",
        r".*displacement.*"
    ]
}
```

#### 参数值验证
```python
def validate_parameter(param_name: str, value: Any, node_type: NodeType) -> bool:
    """
    DV-QKD参数验证函数
    
    验证规则：
    1. 参数名称不包含CV-QKD关键词
    2. 参数值在DV-QKD物理约束范围内
    3. 参数类型符合DV-QKD要求
    """
    # 检查禁用参数
    forbidden_keywords = [
        "discrimination", "threshold", "coherent", "squeezed",
        "quadrature", "homodyne", "heterodyne", "gaussian",
        "displacement", "thermal"
    ]
    
    for keyword in forbidden_keywords:
        if keyword in param_name.lower():
            raise ValueError(f"禁止使用CV-QKD参数: {param_name}")
    
    # 物理约束验证
    if param_name in ["efficiency", "fidelity", "transmission"]:
        if not (0.0 <= value <= 1.0):
            raise ValueError(f"参数 {param_name} 必须在 [0.0, 1.0] 范围内")
    
    return True
```

## 🚫 明确禁止列表

### 禁止的参数类型
```python
FORBIDDEN_PARAMETERS = {
    # 连续变量特有参数
    "discrimination_threshold": {
        "reason": "连续变量判决阈值，DV-QKD不需要",
        "removed_version": "v2.0.1",
        "replacement": "使用探测器点击模式"
    },
    
    "variance": {
        "reason": "高斯调制方差，属于CV-QKD",
        "alternative": "使用离散态参数"
    },
    
    "quadrature_phase": {
        "reason": "正交相位参数，CV-QKD概念",
        "alternative": "使用偏振或相位编码"
    },
    
    "coherent_amplitude": {
        "reason": "相干态振幅，属于连续变量", 
        "alternative": "使用离散态保真度"
    },
    
    "squeezed_parameter": {
        "reason": "压缩参数，CV-QKD技术",
        "alternative": "使用标准离散量子态"
    },
    
    "homodyne_angle": {
        "reason": "零差测量角度，CV-QKD测量",
        "alternative": "使用偏振测量基"
    },
    
    "heterodyne_phase": {
        "reason": "外差测量相位，CV-QKD技术",
        "alternative": "使用时间或频率基"
    },
    
    "displacement_parameter": {
        "reason": "位移算符参数，连续变量操作",
        "alternative": "使用量子门操作"
    },
    
    "thermal_photon_number": {
        "reason": "热光子数，连续变量噪声",
        "alternative": "使用暗计数率"
    }
}
```

### 禁止的算法概念
```python
FORBIDDEN_ALGORITHMS = {
    "gaussian_modulation": "高斯调制算法",
    "quadrature_demodulation": "正交解调算法", 
    "homodyne_reconstruction": "零差重构算法",
    "continuous_error_correction": "连续变量纠错",
    "thermal_noise_modeling": "热噪声建模"
}
```

### 禁止的数学表示
```python
FORBIDDEN_MATH_NOTATION = {
    "∫": "连续积分（应使用离散求和 Σ）",
    "∂/∂x": "连续偏导（应使用离散差分）",
    "Gaussian(μ,σ²)": "高斯分布（应使用泊松或二项分布）",
    "⟨x̂⟩": "位置算符期望（应使用Pauli算符）",
    "⟨p̂⟩": "动量算符期望（应使用离散可观测量）"
}
```

## 📏 性能指标规范

### DV-QKD性能指标
```python
PERFORMANCE_METRICS = {
    "key_rate": {
        "unit": "bits/pulse",
        "typical_range": [1e-6, 1e-3],
        "formula": "R = I(A:B) - I(A:E)"
    },
    
    "qber": {
        "unit": "percentage",
        "acceptable_range": [0.0, 0.11],
        "description": "量子误码率"
    },
    
    "detection_efficiency": {
        "unit": "percentage", 
        "typical_range": [0.1, 0.95],
        "description": "单光子探测效率"
    },
    
    "dark_count_rate": {
        "unit": "counts/second",
        "typical_range": [1e-6, 1e-3],
        "description": "暗计数率"
    },
    
    "repetition_rate": {
        "unit": "Hz",
        "typical_range": [1e6, 1e9], 
        "description": "脉冲重复频率"
    }
}

# ❌ 禁止的性能指标
FORBIDDEN_METRICS = {
    "squeezing_level": "压缩程度（dB）",
    "displacement_amplitude": "位移振幅",
    "quadrature_variance": "正交分量方差",
    "thermal_photon_number": "平均热光子数"
}
```

## 🧪 验证和测试规范

### 参数合规性测试
```python
def test_parameter_compliance():
    """测试参数合规性"""
    
    # 测试允许的参数
    valid_params = {
        "state": "|0⟩",
        "fidelity": 0.99,
        "efficiency": 0.8,
        "dark_count_rate": 1e-6
    }
    
    for param, value in valid_params.items():
        assert validate_parameter(param, value, NodeType.QSP)
    
    # 测试禁止的参数
    invalid_params = {
        "discrimination_threshold": 0.5,
        "coherent_amplitude": 2.0,
        "quadrature_phase": np.pi/4
    }
    
    for param, value in invalid_params.items():
        with pytest.raises(ValueError):
            validate_parameter(param, value, NodeType.QSP)
```

### 量子态验证测试
```python
def test_quantum_state_compliance():
    """测试量子态合规性"""
    
    # 允许的离散量子态
    valid_states = ["|0⟩", "|1⟩", "|+⟩", "|-⟩", "H", "V", "D", "A"]
    for state in valid_states:
        assert is_discrete_quantum_state(state)
    
    # 禁止的连续变量态
    invalid_states = ["coherent", "squeezed", "thermal", "cat"]
    for state in invalid_states:
        assert not is_discrete_quantum_state(state)
```

### 代码审查检查列表
```python
CODE_REVIEW_CHECKLIST = {
    "parameter_names": [
        "检查是否包含CV-QKD关键词",
        "验证参数命名符合DV-QKD规范",
        "确认参数物理意义正确"
    ],
    
    "quantum_states": [
        "验证只使用离散量子态",
        "检查态向量定义正确性", 
        "确认基底选择合理性"
    ],
    
    "algorithms": [
        "验证算法基于离散操作",
        "检查测量过程使用光子探测",
        "确认不包含连续变量概念"
    ],
    
    "documentation": [
        "检查注释避免CV-QKD术语",
        "验证文档描述准确性",
        "确认示例代码合规性"
    ]
}
```

## 📖 合规性指导

### 开发者指导原则

1. **严格遵守**: 所有代码必须符合DV-QKD技术规范
2. **主动验证**: 使用自动化工具检查参数合规性  
3. **持续学习**: 深入理解DV-QKD技术原理
4. **及时更新**: 关注规范更新和技术发展

### 审查流程

1. **自动检查**: 使用参数验证工具进行初步检查
2. **代码审查**: 人工审查代码的技术一致性
3. **测试验证**: 运行合规性测试套件
4. **文档检查**: 确保文档描述准确无误

### 违规处理

1. **轻微违规**: 提醒并要求修改
2. **严重违规**: 拒绝代码合并，要求重新设计
3. **持续违规**: 提供培训和技术指导

## 🔄 规范更新机制

### 版本控制
- **主版本**: 重大技术方向调整
- **次版本**: 新增参数类型或规范  
- **修订版本**: 细节完善和错误修正

### 更新流程
1. 技术委员会讨论
2. 社区征求意见
3. 正式发布更新
4. 文档同步更新

### 历史记录
- **v1.0** (2025-08-19): 初始版本，建立基本规范

---

## 📞 技术支持

### 联系方式
- **技术问题**: GitHub Issues
- **规范咨询**: 技术委员会邮箱
- **培训需求**: 开发者社区

### 参考资源
- **DV-QKD基础**: 相关学术论文和教材
- **代码示例**: examples/目录下的标准实现
- **测试用例**: tests/目录下的合规性测试

---

**📝 声明**: 本技术规范是AI4QKD项目的正式技术文档，所有贡献者和用户必须严格遵守。规范的目的是确保项目技术方向的一致性和专业性，推动离散变量QKD技术的发展和应用。

**🔄 最后更新**: 2025年8月19日  
**📋 下次审查**: 2025年11月19日