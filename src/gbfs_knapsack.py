"""
=================================================================================
GBFS (Greedy Best-First Search) for Knapsack Problem
=================================================================================
Uses fractional knapsack heuristic (greedy by value/weight ratio)
=================================================================================
"""

import numpy as np
from typing import Dict, List
import time


def solve_knapsack_gbfs(items, weights, values, capacity, max_states=5000):
    """
    Greedy algorithm: Select items by value/weight ratio
    Note: max_states parameter kept for interface compatibility but not used
    """
    start = time.time()
    
    weights = np.array(weights, dtype=float)
    values = np.array(values, dtype=float)
    n = len(items)
    
    # Calculate value/weight ratios
    ratios = values / weights
    
    # Sort items by ratio (descending)
    sorted_indices = np.argsort(-ratios)
    
    # Greedy selection
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
