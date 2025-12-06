"""
=================================================================================
BPSO (Binary Particle Swarm Optimization) - Tối Ưu Bầy Đàn cho Bài Toán Knapsack
=================================================================================
Thuật toán metaheuristic dựa trên quần thể sử dụng trí tuệ bầy đàn
=================================================================================
"""

import numpy as np
from typing import Dict, List
import time


class KnapsackBPSO:
    """Triển khai BPSO"""
    
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
        
        # Theo dõi hội tụ
        self.best_fitness_history = []
        self.avg_fitness_history = []
        # Lịch sử particle để visualize (lấy mẫu mỗi 10 iterations)
        self.particle_history = []  # Danh sách (iteration, positions, gbest_pos)
    
    def evaluate_fitness(self, position):
        """Fitness với penalty cho trường hợp quá tải"""
        total_value = np.sum(self.values * position)
        total_weight = np.sum(self.weights * position)
        
        if total_weight <= self.capacity:
            return total_value
        else:
            overflow = total_weight - self.capacity
            return total_value - 1000 * overflow
    
    def solve(self):
        """Chạy tối ưu BPSO"""
        start = time.time()
        
        # Khởi tạo bầy đàn
        positions = np.random.randint(0, 2, (self.n_particles, self.n))
        velocities = np.random.uniform(-4, 4, (self.n_particles, self.n))
        
        # Đánh giá
        fitness = np.array([self.evaluate_fitness(p) for p in positions])
        
        # Best cá nhân
        pbest_positions = positions.copy()
        pbest_fitness = fitness.copy()
        
        # Best toàn cục
        gbest_idx = np.argmax(fitness)
        gbest_position = positions[gbest_idx].copy()
        gbest_fitness = fitness[gbest_idx]
        
        # Theo dõi hội tụ
        self.best_fitness_history = [gbest_fitness]
        self.avg_fitness_history = [np.mean(fitness)]
        
        # Lấy mẫu trạng thái ban đầu để visualize
        self.particle_history.append((0, positions.copy(), gbest_position.copy()))
        
        # Vòng lặp chính
        for iteration in range(self.max_iterations):
            for i in range(self.n_particles):
                # Cập nhật vận tốc
                r1 = np.random.random(self.n)
                r2 = np.random.random(self.n)
                velocities[i] = (self.w * velocities[i] +
                               self.c1 * r1 * (pbest_positions[i] - positions[i]) +
                               self.c2 * r2 * (gbest_position - positions[i]))
                velocities[i] = np.clip(velocities[i], -6, 6)
                
                # Cập nhật vị trí (nhị phân)
                sigmoid = 1 / (1 + np.exp(-velocities[i]))
                positions[i] = (np.random.random(self.n) < sigmoid).astype(int)
                
                # Đánh giá
                fitness[i] = self.evaluate_fitness(positions[i])
                
                # Cập nhật pbest
                if fitness[i] > pbest_fitness[i]:
                    pbest_positions[i] = positions[i].copy()
                    pbest_fitness[i] = fitness[i]
                
                # Cập nhật gbest
                if fitness[i] > gbest_fitness:
                    gbest_position = positions[i].copy()
                    gbest_fitness = fitness[i]
            
            # Theo dõi
            self.best_fitness_history.append(gbest_fitness)
            self.avg_fitness_history.append(np.mean(fitness))
            
            # Lấy mẫu vị trí particle để visualize (mỗi 10 iterations)
            if (iteration + 1) % 10 == 0 or iteration == self.max_iterations - 1:
                self.particle_history.append((iteration + 1, positions.copy(), gbest_position.copy()))
        
        elapsed = time.time() - start
        
        # Xây dựng solution
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
            'particle_history': self.particle_history  # Để visualize
        }


def solve_knapsack_bpso(items, weights, values, capacity, 
                        n_particles=30, max_iterations=100, w=0.7, c1=2.0, c2=2.0):
    """Chạy thuật toán BPSO"""
    solver = KnapsackBPSO(items, weights, values, capacity, 
                          n_particles, max_iterations, w, c1, c2)
    return solver.solve()
