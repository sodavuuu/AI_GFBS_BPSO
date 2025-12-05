"""
=================================================================================
MODULE: Step-by-Step Algorithm Tracker
=================================================================================
Modified algorithms that track every step for visualization
Used by GUI to show algorithm execution step by step
=================================================================================
"""

import numpy as np
from typing import Dict, List, Tuple
import copy


class StepTracker:
    """Base class to track algorithm steps"""
    
    def __init__(self):
        self.steps = []
        self.current_step = 0
    
    def add_step(self, step_data: Dict):
        """Record a step"""
        self.steps.append(copy.deepcopy(step_data))
    
    def get_step(self, index: int) -> Dict:
        """Get specific step"""
        if 0 <= index < len(self.steps):
            return self.steps[index]
        return None
    
    def get_total_steps(self) -> int:
        """Get total number of steps"""
        return len(self.steps)
    
    def reset(self):
        """Reset tracker"""
        self.steps = []
        self.current_step = 0


class GBFSStepTracker(StepTracker):
    """Track GBFS execution step by step"""
    
    def solve_with_tracking(self, items, weights, values, capacity, max_states=10000):
        """
        Run GBFS and record every step
        
        Returns:
            Dict with solution and steps
        """
        self.reset()
        
        n_items = len(items)
        weights = np.array(weights, dtype=float)
        values = np.array(values, dtype=float)
        ratios = values / weights
        
        # Initial state
        current_state = []
        current_weight = 0
        current_value = 0
        
        self.add_step({
            'type': 'start',
            'iteration': 0,
            'state': current_state.copy(),
            'weight': current_weight,
            'value': current_value,
            'capacity': capacity,
            'available_items': list(range(n_items)),
            'message': 'Khởi tạo: Túi rỗng'
        })
        
        iteration = 1
        states_explored = 0
        
        while states_explored < max_states:
            # Find available items
            remaining_capacity = capacity - current_weight
            available = [i for i in range(n_items) 
                        if i not in current_state 
                        and weights[i] <= remaining_capacity]
            
            if not available:
                # Goal state reached
                self.add_step({
                    'type': 'goal',
                    'iteration': iteration,
                    'state': current_state.copy(),
                    'weight': current_weight,
                    'value': current_value,
                    'capacity': capacity,
                    'available_items': [],
                    'message': 'Đạt trạng thái đích: Không thể thêm item'
                })
                break
            
            # Select best item by ratio (greedy)
            best_idx = max(available, key=lambda i: ratios[i])
            
            # Record before selection
            self.add_step({
                'type': 'evaluate',
                'iteration': iteration,
                'state': current_state.copy(),
                'weight': current_weight,
                'value': current_value,
                'capacity': capacity,
                'available_items': available.copy(),
                'considering': best_idx,
                'message': f'Đánh giá: Item {items[best_idx]} có ratio cao nhất ({ratios[best_idx]:.2f})'
            })
            
            # Add item
            current_state.append(best_idx)
            current_weight += weights[best_idx]
            current_value += values[best_idx]
            
            # Record after selection
            self.add_step({
                'type': 'select',
                'iteration': iteration,
                'state': current_state.copy(),
                'weight': current_weight,
                'value': current_value,
                'capacity': capacity,
                'selected': best_idx,
                'message': f'Chọn: Item {items[best_idx]} (W={weights[best_idx]:.1f}, V={values[best_idx]:.1f})'
            })
            
            iteration += 1
            states_explored += 1
        
        # Final step
        selected_items = [items[i] for i in current_state]
        
        return {
            'solution': {
                'selected_items': selected_items,
                'selected_indices': current_state,
                'total_value': current_value,
                'total_weight': current_weight,
                'capacity_used': (current_weight / capacity) * 100,
                'states_explored': states_explored
            },
            'tracker': self
        }


class BPSOStepTracker(StepTracker):
    """Track BPSO execution step by step"""
    
    def solve_with_tracking(self, items, weights, values, capacity,
                           n_particles=30, max_iterations=100,
                           w=0.7, c1=1.5, c2=1.5):
        """
        Run BPSO and record every step
        
        Returns:
            Dict with solution and steps
        """
        self.reset()
        
        n_items = len(items)
        weights = np.array(weights, dtype=float)
        values = np.array(values, dtype=float)
        
        # Initialize swarm
        positions = np.random.randint(0, 2, size=(n_particles, n_items))
        velocities = np.random.uniform(-4, 4, size=(n_particles, n_items))
        
        # Evaluate initial fitness
        fitness = np.array([self._evaluate_fitness(p, weights, values, capacity) 
                           for p in positions])
        
        # Initialize personal best
        pbest_positions = positions.copy()
        pbest_fitness = fitness.copy()
        
        # Initialize global best
        gbest_idx = np.argmax(fitness)
        gbest_position = positions[gbest_idx].copy()
        gbest_fitness = fitness[gbest_idx]
        
        # Record initialization
        self.add_step({
            'type': 'init',
            'iteration': 0,
            'positions': positions.copy(),
            'fitness': fitness.copy(),
            'gbest_position': gbest_position.copy(),
            'gbest_fitness': gbest_fitness,
            'avg_fitness': np.mean(fitness),
            'message': f'Khởi tạo {n_particles} particles. Best fitness: {gbest_fitness:.1f}'
        })
        
        # Main loop
        for iteration in range(1, max_iterations + 1):
            for i in range(n_particles):
                # Update velocity
                r1 = np.random.random(n_items)
                r2 = np.random.random(n_items)
                
                velocities[i] = (w * velocities[i] +
                               c1 * r1 * (pbest_positions[i] - positions[i]) +
                               c2 * r2 * (gbest_position - positions[i]))
                
                # Clip velocity
                velocities[i] = np.clip(velocities[i], -6, 6)
                
                # Update position using sigmoid
                sigmoid = 1 / (1 + np.exp(-velocities[i]))
                positions[i] = (np.random.random(n_items) < sigmoid).astype(int)
                
                # Evaluate fitness
                fitness[i] = self._evaluate_fitness(positions[i], weights, values, capacity)
                
                # Update personal best
                if fitness[i] > pbest_fitness[i]:
                    pbest_positions[i] = positions[i].copy()
                    pbest_fitness[i] = fitness[i]
                
                # Update global best
                if fitness[i] > gbest_fitness:
                    gbest_position = positions[i].copy()
                    gbest_fitness = fitness[i]
            
            # Record step every iteration
            self.add_step({
                'type': 'iteration',
                'iteration': iteration,
                'positions': positions.copy(),
                'fitness': fitness.copy(),
                'gbest_position': gbest_position.copy(),
                'gbest_fitness': gbest_fitness,
                'avg_fitness': np.mean(fitness),
                'best_fitness': np.max(fitness),
                'message': f'Iteration {iteration}: Best={gbest_fitness:.1f}, Avg={np.mean(fitness):.1f}'
            })
        
        # Build solution
        selected_indices = np.where(gbest_position == 1)[0].tolist()
        selected_items = [items[i] for i in selected_indices]
        total_value = np.sum(values[selected_indices])
        total_weight = np.sum(weights[selected_indices])
        
        return {
            'solution': {
                'selected_items': selected_items,
                'selected_indices': selected_indices,
                'total_value': total_value,
                'total_weight': total_weight,
                'capacity_used': (total_weight / capacity) * 100
            },
            'tracker': self
        }
    
    def _evaluate_fitness(self, position, weights, values, capacity):
        """Evaluate fitness with penalty"""
        total_value = np.sum(values * position)
        total_weight = np.sum(weights * position)
        
        if total_weight <= capacity:
            return total_value
        else:
            overflow = total_weight - capacity
            penalty = 1000 * overflow
            return total_value - penalty


class DPStepTracker(StepTracker):
    """Track DP execution step by step"""
    
    def solve_with_tracking(self, items, weights, values, capacity):
        """
        Run DP and record key steps
        
        Returns:
            Dict with solution and steps
        """
        self.reset()
        
        n_items = len(items)
        weights = np.array(weights, dtype=int)
        values = np.array(values, dtype=int)
        
        # Initialize DP table
        dp = np.zeros((n_items + 1, capacity + 1), dtype=int)
        
        self.add_step({
            'type': 'init',
            'iteration': 0,
            'message': f'Khởi tạo bảng DP: {n_items+1} x {capacity+1}'
        })
        
        # Fill DP table
        for i in range(1, n_items + 1):
            for w in range(capacity + 1):
                # Don't take item i-1
                dp[i][w] = dp[i-1][w]
                
                # Take item i-1 if possible
                if weights[i-1] <= w:
                    dp[i][w] = max(dp[i][w], 
                                  dp[i-1][w - weights[i-1]] + values[i-1])
            
            # Record progress every few items
            if i % max(1, n_items // 10) == 0:
                self.add_step({
                    'type': 'fill',
                    'iteration': i,
                    'items_processed': i,
                    'max_value': dp[i][capacity],
                    'message': f'Xử lý {i}/{n_items} items. Max value: {dp[i][capacity]}'
                })
        
        # Backtrack to find solution
        selected_indices = []
        w = capacity
        for i in range(n_items, 0, -1):
            if dp[i][w] != dp[i-1][w]:
                selected_indices.append(i-1)
                w -= weights[i-1]
        
        selected_indices.reverse()
        selected_items = [items[i] for i in selected_indices]
        total_value = dp[n_items][capacity]
        total_weight = sum(weights[i] for i in selected_indices)
        
        self.add_step({
            'type': 'backtrack',
            'iteration': n_items,
            'selected_indices': selected_indices,
            'message': f'Backtrack: Tìm được {len(selected_indices)} items'
        })
        
        return {
            'solution': {
                'selected_items': selected_items,
                'selected_indices': selected_indices,
                'total_value': int(total_value),
                'total_weight': int(total_weight),
                'capacity_used': (total_weight / capacity) * 100
            },
            'tracker': self
        }
