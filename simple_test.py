#!/usr/bin/env python3
"""
Simple test for quantum memory removal verification
"""

def test_quantum_memory_removal():
    """Test quantum memory type removal"""
    print("Verifying quantum memory removal...")
    
    try:
        from qcgf_dsl.node_types import (
            NodeType, NodeSubType, get_node_template, 
            get_supported_subtypes, QC_SUBTYPE_TEMPLATES
        )
        
        # 1. Check QC supported subtypes
        qc_subtypes = get_supported_subtypes(NodeType.QC)
        qc_subtype_names = [st.value for st in qc_subtypes]
        print(f"QC subtypes: {qc_subtype_names}")
        
        if 'QuantumMemory' in qc_subtype_names:
            print("[FAIL] QuantumMemory still found in subtypes")
            return False
        else:
            print("[PASS] QuantumMemory removed from subtypes")
        
        # 2. Test FIBER works
        fiber_template = get_node_template(NodeType.QC, NodeSubType.FIBER)
        print(f"FIBER params: {list(fiber_template.keys())}")
        print("[PASS] FIBER subtype works")
        
        # 3. Test FREE_SPACE works
        freespace_template = get_node_template(NodeType.QC, NodeSubType.FREE_SPACE)
        print(f"FREE_SPACE params: {list(freespace_template.keys())}")
        print("[PASS] FREE_SPACE subtype works")
        
        print("Quantum memory removal verification SUCCESS!")
        return True
        
    except Exception as e:
        print(f"[FAIL] Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_quantum_memory_removal()
    exit(0 if success else 1)