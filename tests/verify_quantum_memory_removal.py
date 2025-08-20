#!/usr/bin/env python3
"""
验证量子存储器类型移除脚本

测试目标：
- 确认QUANTUM_MEMORY子类型已从枚举中移除
- 确认QC_SUBTYPE_TEMPLATES不再包含量子存储器模板
- 确认get_supported_subtypes(NodeType.QC)不返回QUANTUM_MEMORY
- 确认现有的FIBER和FREE_SPACE子类型仍然正常工作

作者: Claude (AI Assistant)
日期: 2025-08-19
"""

def test_quantum_memory_removal():
    """测试量子存储器类型移除"""
    print("🔍 验证量子存储器类型移除...")
    
    try:
        # 导入必要模块
        from qcgf_dsl.node_types import (
            NodeType, NodeSubType, get_node_template, 
            get_supported_subtypes, QC_SUBTYPE_TEMPLATES
        )
        
        # 1. 检查枚举中是否还存在QUANTUM_MEMORY
        print("1. 检查NodeSubType枚举...")
        try:
            quantum_memory = NodeSubType.QUANTUM_MEMORY
            print("   ❌ QUANTUM_MEMORY仍然存在于NodeSubType枚举中")
            return False
        except AttributeError:
            print("   ✅ QUANTUM_MEMORY已从NodeSubType枚举中移除")
        
        # 2. 检查QC_SUBTYPE_TEMPLATES
        print("2. 检查QC_SUBTYPE_TEMPLATES...")
        quantum_memory_in_templates = any(
            str(key).find('QUANTUM_MEMORY') != -1 
            for key in QC_SUBTYPE_TEMPLATES.keys()
        )
        if quantum_memory_in_templates:
            print("   ❌ QC_SUBTYPE_TEMPLATES中仍然包含QUANTUM_MEMORY")
            return False
        else:
            print("   ✅ QC_SUBTYPE_TEMPLATES中已移除QUANTUM_MEMORY")
        
        # 3. 检查get_supported_subtypes
        print("3. 检查get_supported_subtypes(NodeType.QC)...")
        qc_subtypes = get_supported_subtypes(NodeType.QC)
        qc_subtype_names = [st.value for st in qc_subtypes]
        print(f"   QC支持的子类型: {qc_subtype_names}")
        
        if 'QuantumMemory' in qc_subtype_names:
            print("   ❌ get_supported_subtypes仍然返回QuantumMemory")
            return False
        else:
            print("   ✅ get_supported_subtypes不再返回QuantumMemory")
        
        # 4. 确认FIBER和FREE_SPACE仍然工作
        print("4. 检查剩余子类型是否正常工作...")
        
        # 测试FIBER
        try:
            fiber_template = get_node_template(NodeType.QC, NodeSubType.FIBER)
            expected_fiber_params = ['subtype', 'length', 'loss_per_km', 'dispersion_parameter']
            for param in expected_fiber_params:
                if param not in fiber_template:
                    print(f"   ❌ FIBER模板缺少参数: {param}")
                    return False
            print("   ✅ FIBER子类型工作正常")
        except Exception as e:
            print(f"   ❌ FIBER子类型测试失败: {e}")
            return False
        
        # 测试FREE_SPACE
        try:
            freespace_template = get_node_template(NodeType.QC, NodeSubType.FREE_SPACE)
            expected_freespace_params = ['subtype', 'distance', 'atmospheric_transmission', 'turbulence_parameter']
            for param in expected_freespace_params:
                if param not in freespace_template:
                    print(f"   ❌ FREE_SPACE模板缺少参数: {param}")
                    return False
            print("   ✅ FREE_SPACE子类型工作正常")
        except Exception as e:
            print(f"   ❌ FREE_SPACE子类型测试失败: {e}")
            return False
        
        # 5. 确认尝试使用QUANTUM_MEMORY会失败
        print("5. 检查使用QUANTUM_MEMORY是否正确失败...")
        try:
            # 这应该抛出异常，因为QUANTUM_MEMORY已被移除
            memory_template = get_node_template(NodeType.QC, "QuantumMemory")  
            print("   ❌ 使用QUANTUM_MEMORY应该失败但却成功了")
            return False
        except:
            print("   ✅ 使用QUANTUM_MEMORY正确地失败了")
        
        print("\n🎉 量子存储器类型移除验证完全成功！")
        return True
        
    except Exception as e:
        print(f"❌ 验证过程出错: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🚀 AI4QKD 量子存储器类型移除验证")
    print("目标：确保点对点DV-QKD不包含量子存储器类型")
    print("=" * 60)
    
    if test_quantum_memory_removal():
        print("\n✅ 验证成功: 量子存储器类型已完全移除")
        print("🎯 代码已符合点对点离散变量量子密钥分发协议设计要求")
        return True
    else:
        print("\n❌ 验证失败: 仍存在量子存储器相关代码")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)