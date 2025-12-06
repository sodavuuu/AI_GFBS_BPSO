"""
=================================================================================
GBFS (Greedy Best-First Search) for Multi-Objective Knapsack Problem
=================================================================================
TRUE GBFS IMPLEMENTATION with:
- State tree representation
- Priority queue (heapq) for open set
- Closed set to avoid revisiting states
- State expansion and exploration
- Multi-objective fitness function (same as BPSO)
  
Fitness = alpha * f1_norm + beta * f2_norm - penalty
  f1 = Total Revenue (normalized)
  f2 = Region Coverage (normalized)
  penalty = 10.0 * overflow_ratio if exceeds capacity
  
Default: alpha=0.7, beta=0.3 (same as BPSO)
=================================================================================
"""

import numpy as np
from typing import Dict, List, Tuple
import time
import heapq


class KnapsackState:
    """Represents a state in the GBFS search tree"""
    
    def __init__(self, selected_indices, total_weight, total_value, regions_covered, next_item_idx):
        self.selected_indices = selected_indices  # List of selected item indices
        self.total_weight = total_weight
        self.total_value = total_value
        self.regions_covered = regions_covered  # Set of covered regions
        self.next_item_idx = next_item_idx  # Next item to consider expanding
        
    def __hash__(self):
        """Hash based on selected items for closed set"""
        return hash(tuple(sorted(self.selected_indices)))
    
    def __eq__(self, other):
        """Equality based on selected items"""
        return set(self.selected_indices) == set(other.selected_indices)


def solve_knapsack_gbfs(items, weights, values, capacity, regions=None, max_states=5000, 
                       alpha=0.7, beta=0.3):
    """
    TRUE Greedy Best-First Search for Multi-Objective Knapsack
    
    Args:
        items: List of item names
        weights: List of item weights (Quantity)
        values: List of item values (Total revenue)
        capacity: Knapsack capacity
        regions: List of region names for each item (for coverage bonus)
        max_states: Maximum states to explore (default 5000)
        alpha: Weight for revenue objective (default 0.7)
        beta: Weight for region coverage objective (default 0.3)
    
    Returns:
        Dict with solution details including region_coverage
    """
    start = time.time()
    
    weights = np.array(weights, dtype=float)
    values = np.array(values, dtype=float)
    n = len(items)
    
    # If no regions provided, treat as single-objective
    if regions is None:
        regions = [None] * n
    
    # Calculate normalization factors
    max_value = np.sum(values)
    unique_regions = set([r for r in regions if r is not None])
    max_regions = len(unique_regions) if len(unique_regions) > 0 else 1
    
    def evaluate_fitness(state):
        """
        Multi-Objective Fitness (same as BPSO)
        fitness = alpha * f1_norm + beta * f2_norm - penalty
        """
        # Objective 1: Total Revenue (normalized)
        f1_normalized = state.total_value / max_value if max_value > 0 else 0
        
        # Objective 2: Region Coverage (normalized)
        f2_normalized = len(state.regions_covered) / max_regions if max_regions > 0 else 0
        
        # Weighted Sum
        fitness = alpha * f1_normalized + beta * f2_normalized
        
        # Penalty for exceeding capacity
        if state.total_weight > capacity:
            overflow = state.total_weight - capacity
            penalty_ratio = overflow / capacity
            fitness -= 10.0 * penalty_ratio  # Heavy penalty
        
        return fitness
    
    # Initialize: Initial state (empty knapsack)
    initial_state = KnapsackState(
        selected_indices=[],
        total_weight=0,
        total_value=0,
        regions_covered=set(),
        next_item_idx=0
    )
    
    # Priority queue: (negative_fitness, state_id, state)
    # We use negative fitness because heapq is a min-heap
    open_set = []
    state_counter = 0
    heapq.heappush(open_set, (-evaluate_fitness(initial_state), state_counter, initial_state))
    state_counter += 1
    
    # Closed set: Track visited states to avoid revisiting
    closed_set = set()
    
    # Track best solution found
    best_state = initial_state
    best_fitness = evaluate_fitness(initial_state)
    
    states_explored = 0
    
    # GBFS main loop
    while open_set and states_explored < max_states:
        # Pop state with highest fitness (lowest negative fitness)
        neg_fitness, _, current_state = heapq.heappop(open_set)
        
        # Check if already visited
        if current_state in closed_set:
            continue
        
        closed_set.add(current_state)
        states_explored += 1
        
        # Update best solution if current is better
        current_fitness = -neg_fitness
        if current_fitness > best_fitness:
            best_fitness = current_fitness
            best_state = current_state
        
        # State expansion: Try adding each remaining item
        for item_idx in range(current_state.next_item_idx, n):
            # Skip if already selected
            if item_idx in current_state.selected_indices:
                continue
            
            # Calculate new state if we add this item
            new_weight = current_state.total_weight + weights[item_idx]
            new_value = current_state.total_value + values[item_idx]
            new_regions = current_state.regions_covered.copy()
            if regions[item_idx] is not None:
                new_regions.add(regions[item_idx])
            
            # Create new state
            new_state = KnapsackState(
                selected_indices=current_state.selected_indices + [item_idx],
                total_weight=new_weight,
                total_value=new_value,
                regions_covered=new_regions,
                next_item_idx=item_idx + 1
            )
            
            # Only add to open set if:
            # 1. Not visited before
            # 2. Doesn't exceed capacity too much (allow small violations for exploration)
            if new_state not in closed_set:
                if new_weight <= capacity * 1.2:  # Allow 20% overflow for exploration
                    new_fitness = evaluate_fitness(new_state)
                    heapq.heappush(open_set, (-new_fitness, state_counter, new_state))
                    state_counter += 1
    
    elapsed = time.time() - start
    
    # Extract final solution from best state
    return {
        'selected_items': [items[i] for i in best_state.selected_indices],
        'selected_indices': best_state.selected_indices,
        'total_value': float(best_state.total_value),
        'total_weight': float(best_state.total_weight),
        'region_coverage': len(best_state.regions_covered),
        'regions_covered': list(best_state.regions_covered),
        'execution_time': elapsed,
        'states_explored': states_explored,
        'fitness': best_fitness
    }

