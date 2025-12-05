#!/usr/bin/env python3
"""
Quick test để verify GBFS fix
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.test_case_loader import TestCaseLoader
from src.gbfs_knapsack import solve_knapsack_gbfs
from src.bpso_knapsack import solve_knapsack_bpso
from src.dp_knapsack import solve_knapsack_dp

print("🧪 Quick Test - Verify GBFS Fix\n")

# Load test case
loader = TestCaseLoader()
test_case = loader.load_test_case('Size Medium 50')

print(f"📦 Test Case: {test_case['test_case_name']}")
print(f"   Items: {len(test_case['items'])}")
print(f"   Capacity: {test_case['capacity']}\n")

# Run DP (optimal)
print("Running DP...")
dp_result = solve_knapsack_dp(
    test_case['items'],
    test_case['weights'],
    test_case['values'],
    test_case['capacity']
)
print(f"✅ DP (Optimal): {dp_result['total_value']:.1f} ({dp_result['execution_time']:.4f}s)\n")

# Run GBFS (should be much better now)
print("Running GBFS...")
gbfs_result = solve_knapsack_gbfs(
    test_case['items'],
    test_case['weights'],
    test_case['values'],
    test_case['capacity'],
    max_states=5000
)
gbfs_pct = (gbfs_result['total_value'] / dp_result['total_value']) * 100
print(f"✅ GBFS: {gbfs_result['total_value']:.1f} ({gbfs_pct:.1f}% optimal, {gbfs_result['execution_time']:.4f}s)\n")

# Run BPSO
print("Running BPSO...")
bpso_result = solve_knapsack_bpso(
    test_case['items'],
    test_case['weights'],
    test_case['values'],
    test_case['capacity'],
    n_particles=30,
    max_iterations=100
)
bpso_pct = (bpso_result['total_value'] / dp_result['total_value']) * 100
print(f"✅ BPSO: {bpso_result['total_value']:.1f} ({bpso_pct:.1f}% optimal, {bpso_result['execution_time']:.4f}s)\n")

# Summary
print("="*70)
print("📊 SUMMARY")
print("="*70)
print(f"DP (Optimal):  {dp_result['total_value']:>10.1f}  (100.0%)")
print(f"GBFS:          {gbfs_result['total_value']:>10.1f}  ({gbfs_pct:>5.1f}%)  {'✅ GOOD!' if gbfs_pct > 50 else '❌ STILL BAD'}")
print(f"BPSO:          {bpso_result['total_value']:>10.1f}  ({bpso_pct:>5.1f}%)")
print("="*70)

if gbfs_pct > 50:
    print("\n🎉 SUCCESS! GBFS đã được sửa và hoạt động tốt!")
else:
    print("\n❌ GBFS vẫn còn vấn đề. Cần kiểm tra thêm.")
