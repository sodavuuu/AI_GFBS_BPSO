"""
=================================================================================
BPSO (Binary Particle Swarm Optimization) for Knapsack Problem
=================================================================================
Population-based metaheuristic using swarm intelligence
=================================================================================
"""

import numpy as np
from typing import Dict, List
import time


class KnapsackBPSO:
    """BPSO implementation"""
    
    def __init__(self, items, weights, values, capacity,
                 n_particles=30, max_iterations=100, w=0.7, c1=1.5, c2=1.5):
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
        
        # Convergence tracking
        self.best_fitness_history = []
        self.avg_fitness_history = []
        # Particle history for visualization (sample every 10 iterations)
        self.particle_history = []  # List of (iteration, positions, gbest_pos)
    
    def evaluate_fitness(self, position):
        """Fitness with penalty for overweight"""
        total_value = np.sum(self.values * position)
        total_weight = np.sum(self.weights * position)
        
        if total_weight <= self.capacity:
            return total_value
        else:
            overflow = total_weight - self.capacity
            return total_value - 1000 * overflow
    
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
        return {
            'selected_items': [self.items[i] for i in selected],
            'selected_indices': selected.tolist(),
            'total_value': np.sum(self.values[selected]),
            'total_weight': np.sum(self.weights[selected]),
            'execution_time': elapsed,
            'convergence': {
                'best_fitness': self.best_fitness_history,
                'avg_fitness': self.avg_fitness_history
            },
            'particle_history': self.particle_history  # For visualization
        }


def solve_knapsack_bpso(items, weights, values, capacity, 
                        n_particles=30, max_iterations=100):
    """Run BPSO algorithm"""
    solver = KnapsackBPSO(items, weights, values, capacity, 
                          n_particles, max_iterations)
    return solver.solve()
