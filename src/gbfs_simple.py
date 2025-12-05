"""
=================================================================================
GBFS (Greedy Best-First Search) for Knapsack Problem - FIXED VERSION
=================================================================================
Simple greedy approach: Always select item with best value/weight ratio that fits
=================================================================================
"""

import numpy as np
from typing import Dict, List
import time


def solve_knapsack_gbfs_simple(items, weights, values, capacity):
    """
    Simple greedy approach: Select items by value/weight ratio
    This is deterministic and fast
    """
    start = time.time()
    
    weights = np.array(weights, dtype=float)
    values = np.array(values, dtype=float)
    n = len(items)
    
    # Calculate ratios
    ratios = values / weights
    
    # Sort items by ratio (descending)
    sorted_indices = np.argsort(-ratios)
    
    # Greedy selection
    selected = []
    total_weight = 0
    total_value = 0
    
    for idx in sorted_indices:
        if total_weight + weights[idx] <= capacity:
            selected.append(idx)
            total_weight += weights[idx]
            total_value += values[idx]
    
    elapsed = time.time() - start
    
    return {
        'selected_items': [items[i] for i in selected],
        'selected_indices': selected,
        'total_value': total_value,
        'total_weight': total_weight,
        'execution_time': elapsed,
        'states_explored': n
    }


# Test
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    
    from test_case_loader import TestCaseLoader
    
    loader = TestCaseLoader()
    test_case = loader.load_test_case('Size Medium 50')
    
    print("Testing Simple GBFS...")
    result = solve_knapsack_gbfs_simple(
        test_case['items'],
        test_case['weights'],
        test_case['values'],
        test_case['capacity']
    )
    
    print(f"Value: {result['total_value']:.1f}")
    print(f"Weight: {result['total_weight']:.1f} / {test_case['capacity']}")
    print(f"Time: {result['execution_time']:.4f}s")
