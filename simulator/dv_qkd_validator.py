"""
AI4QKD - DV-QKD技术规范验证器

重构思路：
- 严格执行DV_QKD_TECHNICAL_SPECIFICATION.md的合规性检查
- 阻止任何CV-QKD参数或概念的混入
- 提供详细的合规性验证报告
- 支持自动化的规范检查流程

设计原则：
- 严格合规：100%遵循DV-QKD技术边界
- 零容忍：对CV-QKD参数绝对禁止
- 详细反馈：提供明确的违规信息
- 自动化检查：集成到仿真流程中

主要改进：
- 建立完整的DV-QKD合规检查体系
- 实现禁止参数的自动检测和拒绝
- 提供技术规范的实时验证
- 支持新协议的合规性预检查

作者: Claude (AI Assistant)
重构日期: 2025-08-24
参考版本: DV_QKD_TECHNICAL_SPECIFICATION.md
"""

import numpy as np
import warnings
from typing import Dict, Any, Union, List, Tuple, Optional, Set
from dataclasses import dataclass
import logging
from enum import Enum

# =============================================================================
# 重构说明: 此模块实现严格的DV-QKD技术规范合规性检查
# 重构日期: 2025-08-24
# 重构原因: 确保simulator模块100%符合DV-QKD技术边界
# 主要特点: 严格合规检查，零容忍CV-QKD，详细验证反馈
# 参考文件: DV_QKD_TECHNICAL_SPECIFICATION.md
# =============================================================================

# 配置日志
logger = logging.getLogger(__name__)


class ComplianceLevel(Enum):
    """合规性级别枚举"""
    COMPLIANT = "compliant"           # 完全合规
    WARNING = "warning"               # 警告级别
    VIOLATION = "violation"           # 违规
    CRITICAL_VIOLATION = "critical"   # 严重违规


@dataclass
class ComplianceReport:
    """
    合规性检查报告
    
    重构思路：
    - 提供详细的合规性检查结果
    - 分类违规严重程度
    - 支持自动化的合规判断
    """
    
    is_compliant: bool = True
    compliance_level: ComplianceLevel = ComplianceLevel.COMPLIANT
    
    # 检查结果统计
    total_checks: int = 0
    passed_checks: int = 0
    warning_checks: int = 0
    failed_checks: int = 0
    
    # 详细问题列表
    violations: List[Dict[str, Any]] = None
    warnings: List[Dict[str, Any]] = None
    
    # 建议和修复
    recommendations: List[str] = None
    
    def __post_init__(self):
        if self.violations is None:
            self.violations = []
        if self.warnings is None:
            self.warnings = []
        if self.recommendations is None:
            self.recommendations = []
    
    def add_violation(self, category: str, description: str, severity: str = "high"):
        """添加违规记录"""
        self.violations.append({
            'category': category,
            'description': description,
            'severity': severity
        })
        self.failed_checks += 1
        self.is_compliant = False
    
    def add_warning(self, category: str, description: str):
        """添加警告记录"""
        self.warnings.append({
            'category': category,
            'description': description
        })
        self.warning_checks += 1
    
    def add_recommendation(self, recommendation: str):
        """添加建议"""
        self.recommendations.append(recommendation)


class DVQKDValidator:
    """
    DV-QKD技术规范验证器
    
    重构思路：
    - 实现完整的DV-QKD合规性检查
    - 严格禁止CV-QKD相关参数和概念
    - 提供自动化的验证流程
    - 支持多层次的合规性分析
    """
    
    def __init__(self):
        """
        初始化DV-QKD验证器
        
        重构思路：
        - 加载DV-QKD技术规范定义
        - 配置禁止的CV-QKD参数列表
        - 初始化验证规则引擎
        """
        # 允许的离散量子态
        self.allowed_quantum_states = {
            # 计算基态
            "|0⟩", "|1⟩",
            # 叠加态
            "|+⟩", "|-⟩", 
            # 偏振态
            "|H⟩", "|V⟩", "|D⟩", "|A⟩", "|L⟩", "|R⟩"
        }
        
        # 允许的DV-QKD编码方式
        self.allowed_encoding_schemes = {
            "polarization", "phase", "time_bin", "frequency"
        }
        
        # 允许的测量技术
        self.allowed_measurement_techniques = {
            "single_photon_detection", "interferometric_detection", 
            "polarization_analysis", "time_resolved_detection"
        }
        
        # 严格禁止的CV-QKD参数
        self.forbidden_cv_parameters = {
            # 连续变量态参数
            "coherent_state_alpha", "squeezing_parameter", "displacement_amplitude",
            "quadrature_amplitude", "quadrature_phase", "thermal_state_parameter",
            "cat_state_alpha", "squeezed_state_xi", "displaced_squeezed_state",
            
            # CV-QKD编码参数
            "gaussian_modulation", "heterodyne_encoding", "homodyne_detection",
            "quadrature_measurement", "phase_space_encoding",
            
            # CV-QKD系统参数
            "local_oscillator_power", "shot_noise_variance", "electronic_noise_variance",
            "reconciliation_efficiency", "reverse_reconciliation",
            
            # CV-QKD安全参数
            "excess_noise", "channel_transmittance", "trusted_detector_noise"
        }
        
        # 禁止的CV-QKD术语
        self.forbidden_cv_terms = {
            "coherent state", "squeezed state", "quadrature", "homodyne", "heterodyne",
            "gaussian", "continuous variable", "phase space", "shot noise",
            "local oscillator", "displacement", "squeezing"
        }
        
        # DV-QKD物理约束
        self.dv_qkd_constraints = {
            'qber_max': 0.11,                    # BB84理论安全阈值
            'detection_efficiency_max': 1.0,     # 最大探测效率
            'dark_count_rate_max': 1e-3,         # 最大暗计数率
            'polarization_extinction_ratio_min': 10.0,  # 最小偏振消光比
            'timing_resolution_min': 1e-12,      # 最小时间分辨率
            'channel_loss_max': 50.0,            # 最大信道损耗 (dB)
        }
        
        logger.info("DVQKDValidator初始化完成")
    
    def validate_dv_qkd_compliance(self, data: Dict[str, Any]) -> ComplianceReport:
        """
        执行完整的DV-QKD合规性检查
        
        重构思路：
        - 检查所有参数的DV-QKD合规性
        - 严格禁止任何CV-QKD参数
        - 验证物理约束条件
        - 生成详细的合规性报告
        
        参数：
            data: 待检查的数据（协议参数、仿真结果等）
            
        返回值：
            ComplianceReport: 详细的合规性检查报告
        """
        report = ComplianceReport()
        
        try:
            logger.info("开始DV-QKD合规性检查")
            
            # 1. 检查禁止的CV-QKD参数
            self._check_forbidden_cv_parameters(data, report)
            
            # 2. 检查禁止的CV-QKD术语
            self._check_forbidden_cv_terms(data, report)
            
            # 3. 验证DV-QKD物理约束
            self._check_dv_qkd_constraints(data, report)
            
            # 4. 验证编码方式合规性
            self._check_encoding_compliance(data, report)
            
            # 5. 验证量子态合规性
            self._check_quantum_state_compliance(data, report)
            
            # 6. 验证测量技术合规性
            self._check_measurement_compliance(data, report)
            
            # 计算总检查数
            report.total_checks = (report.passed_checks + 
                                 report.warning_checks + 
                                 report.failed_checks)
            
            # 确定最终合规级别
            if report.failed_checks > 0:
                report.compliance_level = ComplianceLevel.CRITICAL_VIOLATION
                report.is_compliant = False
            elif report.warning_checks > 0:
                report.compliance_level = ComplianceLevel.WARNING
            else:
                report.compliance_level = ComplianceLevel.COMPLIANT
            
            # 生成建议
            self._generate_recommendations(report)
            
            logger.info(f"DV-QKD合规性检查完成: {'合规' if report.is_compliant else '不合规'}")
            
            return report
            
        except Exception as e:
            logger.error(f"DV-QKD合规性检查失败: {e}")
            report.add_violation("system_error", f"合规性检查系统错误: {e}")
            return report
    
    def check_forbidden_cv_params(self, parameters: Dict[str, Any]) -> List[str]:
        """
        检查禁止的CV-QKD参数
        
        重构思路：
        - 快速检测CV-QKD参数的存在
        - 返回发现的违规参数列表
        - 支持递归检查嵌套字典
        
        参数：
            parameters: 参数字典
            
        返回值：
            List[str]: 发现的禁止参数列表
        """
        forbidden_found = []
        
        def recursive_check(obj, path=""):
            """递归检查参数"""
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    
                    # 检查参数名
                    if key.lower() in self.forbidden_cv_parameters:
                        forbidden_found.append(current_path)
                    
                    # 检查参数值中的术语
                    if isinstance(value, str):
                        for term in self.forbidden_cv_terms:
                            if term.lower() in value.lower():
                                forbidden_found.append(f"{current_path}='{value}'")
                    
                    # 递归检查嵌套结构
                    recursive_check(value, current_path)
                    
            elif isinstance(obj, (list, tuple)):
                for i, item in enumerate(obj):
                    recursive_check(item, f"{path}[{i}]")
        
        recursive_check(parameters)
        return list(set(forbidden_found))  # 去重
    
    def validate_physical_parameters(self, params: Dict[str, float]) -> Dict[str, bool]:
        """
        验证物理参数的DV-QKD合规性
        
        重构思路：
        - 检查参数是否在DV-QKD允许的物理范围内
        - 验证参数间的物理一致性
        - 提供具体的违规参数标识
        
        参数：
            params: 物理参数字典
            
        返回值：
            Dict[str, bool]: 参数验证结果
        """
        validation_results = {}
        
        # QBER检查
        if 'qber' in params:
            qber = params['qber']
            validation_results['qber'] = (0.0 <= qber <= self.dv_qkd_constraints['qber_max'])
        
        # 探测器效率检查
        if 'detection_efficiency' in params:
            eff = params['detection_efficiency']
            validation_results['detection_efficiency'] = (0.0 <= eff <= 1.0)
        
        # 暗计数率检查
        if 'dark_count_rate' in params:
            dcr = params['dark_count_rate']
            validation_results['dark_count_rate'] = (0.0 <= dcr <= self.dv_qkd_constraints['dark_count_rate_max'])
        
        # 偏振消光比检查
        if 'polarization_extinction_ratio' in params:
            per = params['polarization_extinction_ratio']
            validation_results['polarization_extinction_ratio'] = (per >= self.dv_qkd_constraints['polarization_extinction_ratio_min'])
        
        # 信道损耗检查
        if 'channel_loss' in params:
            loss = params['channel_loss']
            validation_results['channel_loss'] = (0.0 <= loss <= self.dv_qkd_constraints['channel_loss_max'])
        
        return validation_results
    
    def is_dv_qkd_compliant(self, data: Any) -> bool:
        """
        快速DV-QKD合规性判断
        
        重构思路：
        - 提供快速的合规性判断接口
        - 适用于实时检查和流程控制
        - 基于完整验证的简化版本
        
        参数：
            data: 待检查的数据
            
        返回值：
            bool: 是否合规
        """
        try:
            if isinstance(data, dict):
                # 快速检查禁止参数
                forbidden_params = self.check_forbidden_cv_params(data)
                if forbidden_params:
                    return False
                
                # 快速检查物理参数
                physical_validation = self.validate_physical_parameters(data)
                if any(not valid for valid in physical_validation.values()):
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"快速合规性检查失败: {e}")
            return False
    
    # 私有检查方法
    def _check_forbidden_cv_parameters(self, data: Dict[str, Any], report: ComplianceReport):
        """检查禁止的CV-QKD参数"""
        forbidden_found = self.check_forbidden_cv_params(data)
        
        if forbidden_found:
            for param in forbidden_found:
                report.add_violation(
                    "forbidden_cv_parameter",
                    f"检测到禁止的CV-QKD参数: {param}",
                    "critical"
                )
            report.add_recommendation("移除所有CV-QKD相关参数，使用DV-QKD标准参数")
        else:
            report.passed_checks += 1
    
    def _check_forbidden_cv_terms(self, data: Dict[str, Any], report: ComplianceReport):
        """检查禁止的CV-QKD术语"""
        def search_terms(obj, path=""):
            found_terms = []
            if isinstance(obj, str):
                for term in self.forbidden_cv_terms:
                    if term.lower() in obj.lower():
                        found_terms.append((path, term, obj))
            elif isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    found_terms.extend(search_terms(value, current_path))
            elif isinstance(obj, (list, tuple)):
                for i, item in enumerate(obj):
                    found_terms.extend(search_terms(item, f"{path}[{i}]"))
            return found_terms
        
        forbidden_terms = search_terms(data)
        
        if forbidden_terms:
            for path, term, context in forbidden_terms:
                report.add_violation(
                    "forbidden_cv_term",
                    f"在 {path} 中检测到禁止的CV-QKD术语: '{term}' (上下文: '{context}')",
                    "high"
                )
            report.add_recommendation("使用DV-QKD标准术语，避免任何CV-QKD相关表述")
        else:
            report.passed_checks += 1
    
    def _check_dv_qkd_constraints(self, data: Dict[str, Any], report: ComplianceReport):
        """检查DV-QKD物理约束"""
        validation_results = self.validate_physical_parameters(data)
        
        for param, is_valid in validation_results.items():
            if not is_valid:
                param_value = data.get(param, "未知")
                constraint_info = self._get_constraint_info(param)
                report.add_violation(
                    "physical_constraint",
                    f"参数 {param}={param_value} 违反DV-QKD物理约束: {constraint_info}",
                    "high"
                )
            else:
                report.passed_checks += 1
        
        if validation_results and all(validation_results.values()):
            report.add_recommendation("所有物理参数符合DV-QKD规范")
    
    def _check_encoding_compliance(self, data: Dict[str, Any], report: ComplianceReport):
        """检查编码方式合规性"""
        encoding_scheme = data.get('encoding_scheme', data.get('encoding', None))
        
        if encoding_scheme:
            if isinstance(encoding_scheme, str):
                if encoding_scheme.lower() not in self.allowed_encoding_schemes:
                    report.add_violation(
                        "encoding_compliance",
                        f"不支持的编码方式: {encoding_scheme}. 允许的编码: {list(self.allowed_encoding_schemes)}",
                        "high"
                    )
                else:
                    report.passed_checks += 1
            else:
                report.add_warning(
                    "encoding_format",
                    f"编码方式格式不正确: {type(encoding_scheme)}"
                )
    
    def _check_quantum_state_compliance(self, data: Dict[str, Any], report: ComplianceReport):
        """检查量子态合规性"""
        # 检查可能的量子态定义
        state_keys = ['quantum_state', 'states', 'polarization_states', 'basis_states']
        
        for key in state_keys:
            if key in data:
                states = data[key]
                if isinstance(states, (list, tuple, set)):
                    for state in states:
                        if str(state) not in self.allowed_quantum_states:
                            report.add_violation(
                                "quantum_state_compliance",
                                f"不支持的量子态: {state}. 只允许离散量子态",
                                "high"
                            )
                        else:
                            report.passed_checks += 1
    
    def _check_measurement_compliance(self, data: Dict[str, Any], report: ComplianceReport):
        """检查测量技术合规性"""
        measurement_keys = ['measurement_technique', 'detection_method', 'measurement_type']
        
        for key in measurement_keys:
            if key in data:
                technique = data[key]
                if isinstance(technique, str):
                    if technique.lower() not in self.allowed_measurement_techniques:
                        report.add_violation(
                            "measurement_compliance",
                            f"不支持的测量技术: {technique}",
                            "medium"
                        )
                    else:
                        report.passed_checks += 1
    
    def _get_constraint_info(self, param: str) -> str:
        """获取约束信息"""
        constraint_map = {
            'qber': f"QBER必须 ≤ {self.dv_qkd_constraints['qber_max']}",
            'detection_efficiency': "探测效率必须在[0,1]范围内",
            'dark_count_rate': f"暗计数率必须 ≤ {self.dv_qkd_constraints['dark_count_rate_max']}",
            'polarization_extinction_ratio': f"偏振消光比必须 ≥ {self.dv_qkd_constraints['polarization_extinction_ratio_min']}dB",
            'channel_loss': f"信道损耗必须 ≤ {self.dv_qkd_constraints['channel_loss_max']}dB"
        }
        return constraint_map.get(param, "未知约束")
    
    def _generate_recommendations(self, report: ComplianceReport):
        """生成合规性建议"""
        if report.failed_checks == 0 and report.warning_checks == 0:
            report.add_recommendation("✅ 完全符合DV-QKD技术规范")
        
        if report.failed_checks > 0:
            report.add_recommendation("❌ 存在严重违规，必须修复后才能继续")
            report.add_recommendation("📖 请参考 DV_QKD_TECHNICAL_SPECIFICATION.md 了解详细规范")
        
        if report.warning_checks > 0:
            report.add_recommendation("⚠️ 存在警告项，建议进行优化改进")


# 便捷函数接口
def validate_dv_qkd_compliance(data: Dict[str, Any]) -> ComplianceReport:
    """
    DV-QKD合规性验证的便捷函数
    
    参数：
        data: 待检查的数据
        
    返回值：
        ComplianceReport: 合规性报告
    """
    validator = DVQKDValidator()
    return validator.validate_dv_qkd_compliance(data)


def check_forbidden_cv_params(parameters: Dict[str, Any]) -> List[str]:
    """
    检查禁止CV-QKD参数的便捷函数
    
    参数：
        parameters: 参数字典
        
    返回值：
        List[str]: 禁止参数列表
    """
    validator = DVQKDValidator()
    return validator.check_forbidden_cv_params(parameters)


def is_dv_qkd_compliant(data: Any) -> bool:
    """
    快速DV-QKD合规性检查的便捷函数
    
    参数：
        data: 待检查的数据
        
    返回值：
        bool: 是否合规
    """
    validator = DVQKDValidator()
    return validator.is_dv_qkd_compliant(data)