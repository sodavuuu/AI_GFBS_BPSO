"""
Binary Particle Swarm Optimization cho 0/1 Knapsack
Không dùng SimpleAI (vì PSO không phải search algorithm)
"""
import numpy as np
from typing import List, Tuple


class BPSOSolver:
    """
    Binary PSO cho 0/1 Knapsack
    Kennedy & Eberhart (1997)
    """
    
    def __init__(self, items: List[Tuple[str, int, int]], capacity: int,
                 n_particles: int = 30, max_iterations: int = 100,
                 w: float = 0.7, c1: float = 1.5, c2: float = 1.5, v_max: float = 6.0):
        self.items = items
        self.capacity = capacity
        self.n_items = len(items)
        
        self.n_particles = n_particles
        self.max_iterations = max_iterations
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.v_max = v_max
        
        # Extract weights and values
        self.weights = np.array([item[1] for item in items])
        self.values = np.array([item[2] for item in items])
    
    def evaluate(self, position: np.ndarray) -> float:
        """Tính fitness (value nếu feasible, penalty nếu không)"""
        total_value = np.sum(self.values * position)
        total_weight = np.sum(self.weights * position)
        
        if total_weight <= self.capacity:
            return total_value
        else:
            overflow = total_weight - self.capacity
            return total_value - 1000 * overflow
    
    def solve(self, verbose: bool = True):
        """Chạy BPSO"""
        # Initialize swarm
        positions = np.random.randint(0, 2, (self.n_particles, self.n_items))
        velocities = np.random.uniform(-4, 4, (self.n_particles, self.n_items))
        
        # Personal best
        pbest_positions = positions.copy()
        pbest_fitness = np.array([self.evaluate(p) for p in positions])
        
        # Global best
        gbest_idx = np.argmax(pbest_fitness)
        gbest_position = pbest_positions[gbest_idx].copy()
        gbest_fitness = pbest_fitness[gbest_idx]
        
        # History
        history = []
        
        if verbose:
            print(f"\n{'='*70}")
            print("BPSO SOLVER")
            print(f"{'='*70}")
            print(f"Particles: {self.n_particles}, Iterations: {self.max_iterations}")
            print(f"w={self.w}, c1={self.c1}, c2={self.c2}, v_max={self.v_max}\n")
        
        for iteration in range(self.max_iterations):
            for i in range(self.n_particles):
                # Update velocity
                r1 = np.random.random(self.n_items)
                r2 = np.random.random(self.n_items)
                
                velocities[i] = (self.w * velocities[i] +
                               self.c1 * r1 * (pbest_positions[i] - positions[i]) +
                               self.c2 * r2 * (gbest_position - positions[i]))
                
                # Clamp velocity
                velocities[i] = np.clip(velocities[i], -self.v_max, self.v_max)
                
                # Update position (sigmoid)
                sigmoid = 1.0 / (1.0 + np.exp(-velocities[i]))
                positions[i] = (np.random.random(self.n_items) < sigmoid).astype(int)
                
                # Evaluate
                fitness = self.evaluate(positions[i])
                
                # Update personal best
                if fitness > pbest_fitness[i]:
                    pbest_positions[i] = positions[i].copy()
                    pbest_fitness[i] = fitness
                
                # Update global best
                if fitness > gbest_fitness:
                    gbest_position = positions[i].copy()
                    gbest_fitness = fitness
            
            # Log
            avg_fitness = np.mean(pbest_fitness)
            history.append({
                'iteration': iteration,
                'gbest_fitness': gbest_fitness,
                'avg_fitness': avg_fitness
            })
            
            if verbose and iteration % 10 == 0:
                print(f"Iter {iteration:3d}: Best={gbest_fitness:.0f}, Avg={avg_fitness:.0f}")
        
        # Final result
        total_weight = int(np.sum(self.weights * gbest_position))
        total_value = int(np.sum(self.values * gbest_position))
        is_feasible = total_weight <= self.capacity
        
        selected_items = [self.items[i][0] for i in range(self.n_items) if gbest_position[i] == 1]
        
        result = {
            'position': gbest_position,
            'fitness': gbest_fitness,
            'total_value': total_value,
            'total_weight': total_weight,
            'is_feasible': is_feasible,
            'items': selected_items,
            'n_items_selected': int(np.sum(gbest_position)),
            'iterations': self.max_iterations,
            'history': history
        }
        
        if verbose:
            print(f"\n{'='*70}")
            print("KẾT QUẢ BPSO")
            print(f"{'='*70}")
            print(f"Best fitness: {gbest_fitness:.0f}")
            print(f"Total value: {total_value}")
            print(f"Total weight: {total_weight}/{self.capacity}")
            print(f"Feasible: {is_feasible}")
            print(f"Items selected: {len(selected_items)}")
            print(f"{'='*70}\n")
        
        return result
