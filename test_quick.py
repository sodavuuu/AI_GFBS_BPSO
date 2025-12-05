#!/usr/bin/env python3
"""
=================================================================================
QUICK TEST - Verify all components work
=================================================================================
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

print("="*70)
print("🧪 KNAPSACK PROJECT - QUICK TEST")
print("="*70)

# Test 1: Import all modules
print("\n[1/5] Testing imports...")
try:
    from src.test_case_loader import TestCaseLoader
    from src.gbfs_knapsack import solve_knapsack_gbfs
    from src.bpso_knapsack import solve_knapsack_bpso
    from src.dp_knapsack import solve_knapsack_dp
    from src.algorithm_visualizer import AlgorithmVisualizer
    from src.advanced_visualizer import AdvancedKnapsackVisualizer
    print("   ✅ All imports successful")
except Exception as e:
    print(f"   ❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Load test cases
print("\n[2/5] Testing test case loader...")
try:
    loader = TestCaseLoader()
    test_cases = loader.list_test_cases()
    print(f"   ✅ Loaded {len(test_cases)} test cases")
    
    # Verify key test cases exist
    required = ['Size Small 30', 'Size Medium 50', 'Size Large 70']
    for name in required:
        tc = loader.load_test_case(name)
        assert tc['test_case_name'] == name, f"Name mismatch: {tc['test_case_name']} != {name}"
        print(f"   ✅ {name}: {tc['n_items']} items, capacity={tc['capacity']}")
except Exception as e:
    print(f"   ❌ Test case loading failed: {e}")
    sys.exit(1)

# Test 3: Run GBFS
print("\n[3/5] Testing GBFS algorithm...")
try:
    tc = loader.load_test_case('Size Medium 50')
    result = solve_knapsack_gbfs(
        tc['items'], tc['weights'], tc['values'], tc['capacity'],
        max_states=1000
    )
    assert 'total_value' in result, "Missing total_value"
    assert 'execution_time' in result, "Missing execution_time"
    assert 'states_explored' in result, "Missing states_explored"
    print(f"   ✅ GBFS: Value={result['total_value']:.1f}, Time={result['execution_time']:.4f}s")
except Exception as e:
    print(f"   ❌ GBFS failed: {e}")
    sys.exit(1)

# Test 4: Run BPSO
print("\n[4/5] Testing BPSO algorithm...")
try:
    result = solve_knapsack_bpso(
        tc['items'], tc['weights'], tc['values'], tc['capacity'],
        n_particles=20, max_iterations=30
    )
    assert 'total_value' in result, "Missing total_value"
    assert 'execution_time' in result, "Missing execution_time"
    assert 'convergence' in result, "Missing convergence"
    print(f"   ✅ BPSO: Value={result['total_value']:.1f}, Time={result['execution_time']:.4f}s")
except Exception as e:
    print(f"   ❌ BPSO failed: {e}")
    sys.exit(1)

# Test 5: Run DP
print("\n[5/5] Testing DP algorithm...")
try:
    result = solve_knapsack_dp(
        tc['items'], tc['weights'], tc['values'], tc['capacity']
    )
    assert 'total_value' in result, "Missing total_value"
    assert 'execution_time' in result, "Missing execution_time"
    assert 'dp_table' in result, "Missing dp_table"
    print(f"   ✅ DP: Value={result['total_value']:.1f}, Time={result['execution_time']:.4f}s (OPTIMAL)")
except Exception as e:
    print(f"   ❌ DP failed: {e}")
    sys.exit(1)

# Summary
print("\n" + "="*70)
print("✅ ALL TESTS PASSED!")
print("="*70)
print("\n📝 Next steps:")
print("   1. Run GUI:        python3 knapsack_solver_gui.py")
print("   2. Run notebooks:  cd experiment/ && jupyter notebook")
print("   3. Run experiments: cd experiment/ && python3 chapter3_experiments_v2.py")
print()
