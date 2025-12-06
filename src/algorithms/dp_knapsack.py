"""
=================================================================================
DP (Dynamic Programming) - Quy Hoạch Động cho Bài Toán Knapsack
=================================================================================
Thuật toán chính xác đảm bảo tìm được lời giải tối ưu
=================================================================================
"""

import numpy as np
from typing import Dict, List
import time


def solve_knapsack_dp(items, weights, values, capacity):
    """Giải pháp DP chính xác"""
    start = time.time()
    
    n = len(items)
    weights_arr = np.array(weights, dtype=int)
    values_arr = np.array(values, dtype=int)
    
    # Bảng DP
    dp = np.zeros((n + 1, capacity + 1), dtype=int)
    
    # Điền bảng
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i-1][w]
            if weights_arr[i-1] <= w:
                dp[i][w] = max(dp[i][w], 
                             dp[i-1][w - weights_arr[i-1]] + values_arr[i-1])
    
    # Truy ngược
    selected = []
    backtrack_path = []  # Để visualize
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected.append(i-1)
            backtrack_path.append((i, w, i-1))  # (hàng, cột, item_được_chọn)
            w -= weights_arr[i-1]
        else:
            backtrack_path.append((i, w, -1))  # (hàng, cột, không_chọn)
    
    selected.reverse()
    elapsed = time.time() - start
    
    return {
        'selected_items': [items[i] for i in selected],
        'selected_indices': selected,
        'total_value': int(dp[n][capacity]),
        'total_weight': int(sum(weights_arr[i] for i in selected)),
        'execution_time': elapsed,
        'dp_table': dp,  # Để visualize
        'backtrack_path': backtrack_path  # Để visualize
    }
