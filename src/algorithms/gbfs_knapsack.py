"""
=================================================================================
GBFS (Greedy Best-First Search) - Tìm Kiếm Tham Lam cho Bài Toán Knapsack
=================================================================================
Sử dụng heuristic fractional knapsack (tham lam theo tỷ lệ giá trị/trọng lượng)
=================================================================================
"""

import numpy as np
from typing import Dict, List
import time


def solve_knapsack_gbfs(items, weights, values, capacity, max_states=5000):
    """
    Thuật toán tham lam: Chọn vật phẩm theo tỷ lệ giá trị/trọng lượng
    Lưu ý: Tham số max_states được giữ để tương thích interface nhưng không sử dụng
    """
    start = time.time()
    
    weights = np.array(weights, dtype=float)
    values = np.array(values, dtype=float)
    n = len(items)
    
    # Tính tỷ lệ giá trị/trọng lượng
    ratios = values / weights
    
    # Sắp xếp các vật phẩm theo tỷ lệ (giảm dần)
    sorted_indices = np.argsort(-ratios)
    
    # Chọn tham lam
    selected = []
    total_weight = 0
    total_value = 0
    
    for idx in sorted_indices:
        if total_weight + weights[idx] <= capacity:
            selected.append(int(idx))
            total_weight += weights[idx]
            total_value += values[idx]
    
    elapsed = time.time() - start
    
    return {
        'selected_items': [items[i] for i in selected],
        'selected_indices': selected,
        'total_value': float(total_value),
        'total_weight': float(total_weight),
        'execution_time': elapsed,
        'states_explored': n
    }
    
    if result is None:
        return {'selected_items': [], 'total_value': 0, 'total_weight': 0, 
                'execution_time': elapsed, 'states_explored': problem.states_explored}
    
    selected_indices = list(result.state)
    return {
        'selected_items': [items[i] for i in selected_indices],
        'selected_indices': selected_indices,
        'total_value': sum(values[i] for i in selected_indices),
        'total_weight': sum(weights[i] for i in selected_indices),
        'execution_time': elapsed,
        'states_explored': problem.states_explored,
        'state_tree': problem.state_tree  # For visualization
    }
