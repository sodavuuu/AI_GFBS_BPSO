"""
=================================================================================
BPSO (Binary Particle Swarm Optimization) for Multi-Objective Knapsack
=================================================================================
Population-based metaheuristic using swarm intelligence

MULTI-OBJECTIVE FITNESS (Weighted Sum Method):
  fitness = alpha * f1_normalized + (1-alpha) * f2_normalized - penalty
  
  f1 = Total Revenue (maximize)
  f2 = Region Coverage (maximize, 0-4 regions)
  alpha = 0.7 (revenue weight)
  penalty = 10.0 * overflow_ratio if over capacity
=================================================================================
"""

import numpy as np
from typing import Dict, List
import time


class KnapsackBPSO:
    """BPSO implementation with Multi-Objective fitness"""
    
    def __init__(self, items, weights, values, capacity, regions=None,
                 n_particles=30, max_iterations=100, w=0.7, c1=2.0, c2=2.0,
                 alpha=0.7):
        self.items = items
        self.weights = np.array(weights, dtype=float)
        self.values = np.array(values, dtype=float)
        self.capacity = capacity
        self.n = len(items)
        self.n_particles = n_particles
        self.max_iterations = max_iterations
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.alpha = alpha  # Weight for revenue objective
        
        # Region data for coverage objective
        if regions is None:
            self.regions = [None] * self.n
            self.max_regions = 1  # No region data
        else:
            self.regions = regions
            self.max_regions = len(set([r for r in regions if r is not None]))
        
        # Normalization bounds (updated during optimization)
        self.max_value = np.sum(self.values)  # Theoretical max revenue
        
        # Convergence tracking
        self.best_fitness_history = []
        self.avg_fitness_history = []
        # Particle history for visualization (sample every 10 iterations)
        self.particle_history = []  # List of (iteration, positions, gbest_pos)
    
    def evaluate_fitness(self, position):
        """
        Multi-Objective Fitness with Weighted Sum Method
        
        fitness = alpha * f1_norm + (1-alpha) * f2_norm - penalty
        
        f1 = Total Revenue (normalized to 0-1)
        f2 = Region Coverage (normalized to 0-1, max=4 regions)
        penalty = 10.0 * overflow_ratio if exceeds capacity
        """
        # Objective 1: Total Revenue
        total_value = np.sum(self.values * position)
        f1_normalized = total_value / self.max_value if self.max_value > 0 else 0
        
        # Objective 2: Region Coverage (number of unique regions)
        selected_indices = np.where(position == 1)[0]
        if len(selected_indices) > 0 and self.regions[0] is not None:
            selected_regions = set([self.regions[i] for i in selected_indices])
            region_coverage = len(selected_regions)
        else:
            region_coverage = 0
        f2_normalized = region_coverage / self.max_regions if self.max_regions > 0 else 0
        
        # Weighted Sum
        fitness = self.alpha * f1_normalized + (1 - self.alpha) * f2_normalized
        
        # Penalty for exceeding capacity
        total_weight = np.sum(self.weights * position)
        if total_weight > self.capacity:
            overflow = total_weight - self.capacity
            penalty_ratio = overflow / self.capacity
            fitness -= 10.0 * penalty_ratio  # Heavy penalty (beta=10.0)
        
        return fitness
    
    def solve(self):
        """Run BPSO optimization"""
        start = time.time()
        
        # Initialize swarm
        positions = np.random.randint(0, 2, (self.n_particles, self.n))
        velocities = np.random.uniform(-4, 4, (self.n_particles, self.n))
        
        # Evaluate
        fitness = np.array([self.evaluate_fitness(p) for p in positions])
        
        # Personal best
        pbest_positions = positions.copy()
        pbest_fitness = fitness.copy()
        
        # Global best
        gbest_idx = np.argmax(fitness)
        gbest_position = positions[gbest_idx].copy()
        gbest_fitness = fitness[gbest_idx]
        
        # Track convergence
        self.best_fitness_history = [gbest_fitness]
        self.avg_fitness_history = [np.mean(fitness)]
        
        # Sample initial state for visualization
        self.particle_history.append((0, positions.copy(), gbest_position.copy()))
        
        # Main loop
        for iteration in range(self.max_iterations):
            for i in range(self.n_particles):
                # Update velocity
                r1 = np.random.random(self.n)
                r2 = np.random.random(self.n)
                velocities[i] = (self.w * velocities[i] +
                               self.c1 * r1 * (pbest_positions[i] - positions[i]) +
                               self.c2 * r2 * (gbest_position - positions[i]))
                velocities[i] = np.clip(velocities[i], -6, 6)
                
                # Update position (binary)
                sigmoid = 1 / (1 + np.exp(-velocities[i]))
                positions[i] = (np.random.random(self.n) < sigmoid).astype(int)
                
                # Evaluate
                fitness[i] = self.evaluate_fitness(positions[i])
                
                # Update pbest
                if fitness[i] > pbest_fitness[i]:
                    pbest_positions[i] = positions[i].copy()
                    pbest_fitness[i] = fitness[i]
                
                # Update gbest
                if fitness[i] > gbest_fitness:
                    gbest_position = positions[i].copy()
                    gbest_fitness = fitness[i]
            
            # Track
            self.best_fitness_history.append(gbest_fitness)
            self.avg_fitness_history.append(np.mean(fitness))
            
            # Sample particle positions for visualization (every 10 iterations)
            if (iteration + 1) % 10 == 0 or iteration == self.max_iterations - 1:
                self.particle_history.append((iteration + 1, positions.copy(), gbest_position.copy()))
        
        elapsed = time.time() - start
        
        # Build solution
        selected = np.where(gbest_position == 1)[0]
        
        # Calculate region coverage
        if self.regions[0] is not None:
            selected_regions = set([self.regions[i] for i in selected])
            region_coverage = len(selected_regions)
            regions_covered = list(selected_regions)
        else:
            region_coverage = 0
            regions_covered = []
        
        return {
            'selected_items': [self.items[i] for i in selected],
            'selected_indices': selected.tolist(),
            'total_value': np.sum(self.values[selected]),
            'total_weight': np.sum(self.weights[selected]),
            'region_coverage': region_coverage,
            'regions_covered': regions_covered,
            'execution_time': elapsed,
            'convergence': {
                'best_fitness': self.best_fitness_history,
                'avg_fitness': self.avg_fitness_history
            },
            'particle_history': self.particle_history  # For visualization
        }


def solve_knapsack_bpso(items, weights, values, capacity, regions=None,
                        n_particles=30, max_iterations=100, w=0.7, c1=2.0, c2=2.0,
                        alpha=0.7):
    """
    Run BPSO algorithm with Multi-Objective fitness
    
    Args:
        regions: List of region names for each item (for coverage objective)
        alpha: Weight for revenue objective (default 0.7)
    """
    solver = KnapsackBPSO(items, weights, values, capacity, regions,
                          n_particles, max_iterations, w, c1, c2, alpha)
    return solver.solve()
