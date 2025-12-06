"""
=================================================================================
DP (Dynamic Programming) for Knapsack Problem
=================================================================================
Exact algorithm guaranteed to find optimal solution
=================================================================================
"""

import numpy as np
from typing import Dict, List
import time


def solve_knapsack_dp(items, weights, values, capacity):
    """Exact DP solution"""
    start = time.time()
    
    n = len(items)
    weights_arr = np.array(weights, dtype=int)
    values_arr = np.array(values, dtype=int)
    
    # DP table
    dp = np.zeros((n + 1, capacity + 1), dtype=int)
    
    # Fill table
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i-1][w]
            if weights_arr[i-1] <= w:
                dp[i][w] = max(dp[i][w], 
                             dp[i-1][w - weights_arr[i-1]] + values_arr[i-1])
    
    # Backtrack
    selected = []
    backtrack_path = []  # For visualization
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected.append(i-1)
            backtrack_path.append((i, w, i-1))  # (row, col, item_taken)
            w -= weights_arr[i-1]
        else:
            backtrack_path.append((i, w, -1))  # (row, col, no_item)
    
    selected.reverse()
    elapsed = time.time() - start
    
    return {
        'selected_items': [items[i] for i in selected],
        'selected_indices': selected,
        'total_value': int(dp[n][capacity]),
        'total_weight': int(sum(weights_arr[i] for i in selected)),
        'execution_time': elapsed,
        'dp_table': dp,  # For visualization
        'backtrack_path': backtrack_path  # For visualization
    }
