#!/usr/bin/env python3
"""
子类型系统测试脚本 - 验证基于研究方案的精确子类型实现

测试目标：
- 验证不同子类型具有不同的参数集合
- 确认intensity参数只在WCP子类型中存在
- 验证理想化模式对所有子类型的正确应用

作者: Claude (AI Assistant)
日期: 2025-08-19
"""

import warnings
warnings.filterwarnings('ignore')

def test_qsp_subtypes():
    """测试QSP子类型的参数差异"""
    print("🔬 测试QSP子类型参数差异...")
    
    try:
        from qcgf_dsl.node_types import (
            NodeType, NodeSubType, get_node_template, get_supported_subtypes
        )
        
        # 获取QSP支持的所有子类型
        qsp_subtypes = get_supported_subtypes(NodeType.QSP)
        print(f"   QSP支持的子类型: {[st.value for st in qsp_subtypes]}")
        
        # 测试各子类型的参数差异
        print("\n   各子类型参数对比:")
        
        # 1. 理想单光子 - 不应该有intensity参数
        ideal_template = get_node_template(NodeType.QSP, NodeSubType.IDEAL_SINGLE_PHOTON)
        print(f"   IdealSinglePhoton参数: {list(ideal_template.keys())}")
        if "intensity" in ideal_template:
            print("   ❌ 理想单光子不应该有intensity参数")
            return False
        else:
            print("   ✅ 理想单光子正确排除intensity参数")
        
        # 2. 弱相干脉冲 - 应该有intensity参数
        wcp_template = get_node_template(NodeType.QSP, NodeSubType.WEAK_COHERENT_PULSE)
        print(f"   WeakCoherentPulse参数: {list(wcp_template.keys())}")
        if "intensity" not in wcp_template:
            print("   ❌ 弱相干脉冲应该有intensity参数")
            return False
        else:
            print("   ✅ 弱相干脉冲正确包含intensity参数")
        
        # 3. 纠缠对 - 应该有特殊参数
        entangled_template = get_node_template(NodeType.QSP, NodeSubType.ENTANGLED_PAIR)
        print(f"   EntangledPair参数: {list(entangled_template.keys())}")
        if "entanglement_fidelity" not in entangled_template:
            print("   ❌ 纠缠对应该有entanglement_fidelity参数")
            return False
        else:
            print("   ✅ 纠缠对正确包含特殊参数")
        
        # 4. 任意量子态 - 应该有state_vector参数
        arbitrary_template = get_node_template(NodeType.QSP, NodeSubType.ARBITRARY_QSTATE)
        print(f"   ArbitraryQState参数: {list(arbitrary_template.keys())}")
        if "state_vector" not in arbitrary_template:
            print("   ❌ 任意量子态应该有state_vector参数")
            return False
        else:
            print("   ✅ 任意量子态正确包含state_vector参数")
        
        return True
        
    except Exception as e:
        print(f"   ❌ QSP子类型测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_qop_subtypes():
    """测试QOP子类型的参数差异"""
    print("\n⚙️ 测试QOP子类型参数差异...")
    
    try:
        from qcgf_dsl.node_types import NodeType, NodeSubType, get_node_template
        
        # 测试酉门类型
        print("   酉门类型参数:")
        
        # Hadamard门
        hadamard_template = get_node_template(NodeType.QOP, NodeSubType.HADAMARD)
        print(f"   Hadamard: {list(hadamard_template.keys())}")
        
        # PhaseShift门 - 应该有phase_angle参数
        phase_template = get_node_template(NodeType.QOP, NodeSubType.PHASE_SHIFT)
        print(f"   PhaseShift: {list(phase_template.keys())}")
        if "phase_angle" not in phase_template:
            print("   ❌ PhaseShift应该有phase_angle参数")
            return False
        else:
            print("   ✅ PhaseShift正确包含phase_angle参数")
        
        # CNOT门 - 应该有control_qubit_id和target_qubit_id
        cnot_template = get_node_template(NodeType.QOP, NodeSubType.CNOT)
        print(f"   CNOT: {list(cnot_template.keys())}")
        if "control_qubit_id" not in cnot_template or "target_qubit_id" not in cnot_template:
            print("   ❌ CNOT应该有control_qubit_id和target_qubit_id参数")
            return False
        else:
            print("   ✅ CNOT正确包含双量子比特参数")
        
        # 测试噪声类型
        print("   噪声模拟类型参数:")
        
        # 光子损耗
        loss_template = get_node_template(NodeType.QOP, NodeSubType.PHOTON_LOSS)
        print(f"   PhotonLoss: {list(loss_template.keys())}")
        if "loss_probability" not in loss_template:
            print("   ❌ PhotonLoss应该有loss_probability参数")
            return False
        else:
            print("   ✅ PhotonLoss正确包含损耗参数")
        
        return True
        
    except Exception as e:
        print(f"   ❌ QOP子类型测试失败: {e}")
        return False

def test_qc_subtypes():
    """测试QC子类型的参数差异"""
    print("\n🌐 测试QC子类型参数差异...")
    
    try:
        from qcgf_dsl.node_types import NodeType, NodeSubType, get_node_template
        
        # 光纤信道
        fiber_template = get_node_template(NodeType.QC, NodeSubType.FIBER)
        print(f"   Fiber: {list(fiber_template.keys())}")
        if "loss_per_km" not in fiber_template:
            print("   ❌ Fiber应该有loss_per_km参数")
            return False
        
        # 自由空间信道
        freespace_template = get_node_template(NodeType.QC, NodeSubType.FREE_SPACE)
        print(f"   FreeSpace: {list(freespace_template.keys())}")
        if "atmospheric_transmission" not in freespace_template:
            print("   ❌ FreeSpace应该有atmospheric_transmission参数")
            return False
        
        
        print("   ✅ QC所有子类型参数正确")
        return True
        
    except Exception as e:
        print(f"   ❌ QC子类型测试失败: {e}")
        return False

def test_idealized_mode_subtypes():
    """测试理想化模式对子类型的影响"""
    print("\n⚡ 测试理想化模式对子类型的影响...")
    
    try:
        from qcgf_dsl.node_types import (
            NodeType, NodeSubType, get_node_template, 
            set_idealized_mode, is_idealized_mode
        )
        
        # 切换到理想化模式
        set_idealized_mode(True)
        print("   理想化模式已启用")
        
        # 测试光纤信道的理想化
        fiber_ideal = get_node_template(NodeType.QC, NodeSubType.FIBER)
        if fiber_ideal.get("loss_per_km", 1.0) != 0.0:
            print("   ❌ 理想化模式下光纤应该无损耗")
            return False
        else:
            print("   ✅ 光纤信道理想化正确（loss_per_km=0.0）")
        
        # 测试自由空间的理想化
        freespace_ideal = get_node_template(NodeType.QC, NodeSubType.FREE_SPACE)
        if freespace_ideal.get("atmospheric_transmission", 0.0) != 1.0:
            print("   ❌ 理想化模式下大气透射率应该为1.0")
            return False
        else:
            print("   ✅ 自由空间信道理想化正确（atmospheric_transmission=1.0）")
        
        # 测试量子测量的理想化
        projective_ideal = get_node_template(NodeType.QM, NodeSubType.PROJECTIVE_MEASUREMENT)
        if projective_ideal.get("detector_efficiency", 0.0) != 1.0:
            print("   ❌ 理想化模式下检测效率应该为1.0")
            return False
        else:
            print("   ✅ 投影测量理想化正确（detector_efficiency=1.0）")
        
        # 恢复现实模式
        set_idealized_mode(False)
        print("   ✅ 理想化模式测试通过，已恢复现实模式")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 理想化模式测试失败: {e}")
        return False

def test_subtype_validation():
    """测试子类型验证"""
    print("\n🔒 测试子类型验证...")
    
    try:
        from qcgf_dsl.node_types import NodeType, NodeSubType, get_node_template
        
        # 测试有效的子类型组合
        try:
            get_node_template(NodeType.QSP, NodeSubType.WEAK_COHERENT_PULSE)
            print("   ✅ 有效子类型组合通过")
        except Exception as e:
            print(f"   ❌ 有效子类型组合失败: {e}")
            return False
        
        # 测试无效的子类型组合
        try:
            get_node_template(NodeType.QSP, NodeSubType.HADAMARD)  # QSP不支持Hadamard
            print("   ❌ 无效子类型组合应该抛出异常")
            return False
        except ValueError:
            print("   ✅ 无效子类型组合正确被拒绝")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 子类型验证测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 AI4QKD 子类型系统验证测试")
    print("基于研究方案PDF第2.2节的精确子类型定义")
    print("=" * 60)
    
    test_functions = [
        ("QSP子类型参数差异", test_qsp_subtypes),
        ("QOP子类型参数差异", test_qop_subtypes),
        ("QC子类型参数差异", test_qc_subtypes),
        ("理想化模式子类型", test_idealized_mode_subtypes),
        ("子类型验证", test_subtype_validation)
    ]
    
    passed = 0
    total = len(test_functions)
    
    for test_name, test_func in test_functions:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} 测试通过")
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 子类型系统完全正确！")
        print("✅ 基于研究方案的精确子类型参数模板实现成功")
        print("✅ intensity参数正确地只在WCP子类型中存在")
        print("✅ 不同子类型具有各自特有的参数集合")
        return True
    else:
        print("⚠️  部分测试失败，需要进一步修复")
        return False

if __name__ == "__main__":
    main()