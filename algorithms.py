"""
=================================================================================
MODULE: Knapsack Algorithms
=================================================================================
Chứa các thuật toán giải bài toán 0/1 Knapsack:
1. GBFS - Greedy Best First Search (SimpleAI)
2. BPSO - Binary Particle Swarm Optimization
3. DP - Dynamic Programming (Optimal Solution)

Mỗi thuật toán được tách riêng, dễ hiểu, có comment đầy đủ
=================================================================================
"""
import numpy as np
from typing import List, Tuple, Dict
from simpleai.search import SearchProblem, greedy


# =================================================================================
# CLASS: Item - Đại diện cho một vật phẩm
# =================================================================================
class Item:
    """
    Một item trong bài toán Knapsack
    
    Attributes:
        name (str): Tên item
        weight (int): Trọng lượng
        value (int): Giá trị
        ratio (float): Tỷ lệ value/weight
    """
    def __init__(self, name: str, weight: int, value: int):
        self.name = name
        self.weight = weight
        self.value = value
        self.ratio = value / weight if weight > 0 else 0
    
    def __repr__(self):
        return f"{self.name}(w={self.weight}, v={self.value}, r={self.ratio:.2f})"


# =================================================================================
# CLASS: KnapsackProblem - Định nghĩa bài toán
# =================================================================================
class KnapsackProblem:
    """
    Bài toán 0/1 Knapsack
    
    Attributes:
        items (List[Item]): Danh sách các items
        capacity (int): Sức chứa túi
        n_items (int): Số lượng items
    """
    def __init__(self, items: List[Item], capacity: int):
        self.items = items
        self.capacity = capacity
        self.n_items = len(items)
    
    def evaluate_solution(self, solution: np.ndarray) -> Tuple[int, int, bool]:
        """
        Đánh giá một solution (binary vector)
        
        Args:
            solution: Binary array [0,1,0,1,...] cho biết item nào được chọn
        
        Returns:
            (total_value, total_weight, is_feasible)
        """
        total_value = sum(self.items[i].value * solution[i] for i in range(self.n_items))
        total_weight = sum(self.items[i].weight * solution[i] for i in range(self.n_items))
        is_feasible = total_weight <= self.capacity
        
        return total_value, total_weight, is_feasible


# =================================================================================
# THUẬT TOÁN 1: GBFS - Greedy Best First Search (SimpleAI)
# =================================================================================
class GBFS_Solver(SearchProblem):
    """
    Giải Knapsack bằng GBFS sử dụng thư viện SimpleAI
    
    Thuật toán:
    1. Bắt đầu với túi rỗng
    2. Mỗi bước, chọn item có heuristic value cao nhất
    3. Heuristic = Fractional Knapsack Bound (ước lượng tiềm năng)
    4. Dừng khi không thể thêm item nào
    
    Ưu điểm: Nhanh, dễ hiểu
    Nhược điểm: Có thể bị local optimum
    """
    
    def __init__(self, problem: KnapsackProblem, max_states: int = 10000):
        """
        Khởi tạo GBFS solver
        
        Args:
            problem: KnapsackProblem instance
            max_states: Giới hạn số states explore (tránh bùng nổ)
        """
        self.problem = problem
        self.items = problem.items
        self.capacity = problem.capacity
        self.n_items = problem.n_items
        self.max_states = max_states
        
        # Logging
        self.states_explored = 0
        self.search_path = []  # Lưu đường đi của thuật toán
        
        # Initial state: empty knapsack (tuple rỗng)
        super().__init__(initial_state=tuple())
    
    def actions(self, state):
        """
        Trả về các actions có thể thực hiện từ state hiện tại
        
        Action = index của item có thể thêm vào
        
        Điều kiện:
        - Item chưa được chọn
        - Thêm vào không vượt capacity
        
        Cải tiến: Sắp xếp theo ratio để greedy chọn tốt hơn
        """
        current_weight = sum(self.items[i].weight for i in state)
        possible_actions = []
        
        for i in range(self.n_items):
            if i not in state:  # Chưa chọn
                if current_weight + self.items[i].weight <= self.capacity:  # Còn chỗ
                    possible_actions.append(i)
        
        # Sắp xếp theo ratio giảm dần để ưu tiên items tốt
        possible_actions.sort(key=lambda i: self.items[i].ratio, reverse=True)
        
        return possible_actions
    
    def result(self, state, action):
        """
        Tạo state mới sau khi thực hiện action
        
        Args:
            state: State hiện tại (tuple các index)
            action: Index của item cần thêm
        
        Returns:
            State mới (tuple đã sorted)
        """
        self.states_explored += 1
        
        # Kiểm tra giới hạn states
        if self.states_explored > self.max_states:
            # Dừng search sớm - trả về state hiện tại
            # SimpleAI sẽ coi đây như một dead-end
            return state
        
        new_state = tuple(sorted(state + (action,)))
        return new_state
    
    def is_goal(self, state):
        """
        Kiểm tra state có phải goal không
        
        Goal: Không thể thêm item nào nữa
        """
        return len(self.actions(state)) == 0
    
    def heuristic(self, state):
        """
        Hàm heuristic: Ước lượng giá trị tối đa có thể đạt từ state này
        
        Sử dụng Fractional Knapsack Bound:
        1. Tính value hiện tại
        2. Sắp xếp items chưa chọn theo ratio giảm dần
        3. Thêm items theo thứ tự (cho phép fractional)
        
        SimpleAI: heuristic càng NHỎ càng ưu tiên
        → Return -bound (âm của upper bound)
        """
        # Value và weight hiện tại
        current_value = sum(self.items[i].value for i in state)
        current_weight = sum(self.items[i].weight for i in state)
        remaining_capacity = self.capacity - current_weight
        
        # Items chưa chọn với ratio
        remaining_items = []
        for i in range(self.n_items):
            if i not in state:
                item = self.items[i]
                remaining_items.append((i, item.weight, item.value, item.ratio))
        
        # Sort theo ratio giảm dần (tham lam)
        remaining_items.sort(key=lambda x: x[3], reverse=True)
        
        # Fractional knapsack để ước lượng
        fractional_value = current_value
        for i, weight, value, ratio in remaining_items:
            if remaining_capacity >= weight:
                # Thêm toàn bộ item
                fractional_value += value
                remaining_capacity -= weight
            else:
                # Thêm phần fractional
                fractional_value += ratio * remaining_capacity
                break
        
        # Return âm để SimpleAI ưu tiên giá trị cao
        return -fractional_value
    
    def solve(self) -> Dict:
        """
        Giải bài toán bằng GBFS
        
        Returns:
            Dict chứa kết quả và thông tin
        """
        # Reset
        self.states_explored = 0
        self.search_path = []
        
        try:
            # Chạy GBFS
            result = greedy(self, graph_search=True)
            
            # Lấy solution
            solution_indices = list(result.state)
        except Exception as e:
            # Nếu search bị timeout hoặc lỗi, dùng greedy đơn giản
            print(f"GBFS search failed: {e}, using simple greedy fallback")
            solution_indices = self._simple_greedy_fallback()
        
        solution_binary = np.zeros(self.n_items, dtype=int)
        solution_binary[solution_indices] = 1
        
        # Đánh giá
        total_value, total_weight, is_feasible = self.problem.evaluate_solution(solution_binary)
        
        # Items được chọn
        selected_items = [self.items[i] for i in solution_indices]
        
        return {
            'algorithm': 'GBFS',
            'solution': solution_binary,
            'selected_indices': solution_indices,
            'selected_items': selected_items,
            'total_value': total_value,
            'total_weight': total_weight,
            'is_feasible': is_feasible,
            'states_explored': self.states_explored,
            'n_items_selected': len(solution_indices)
        }
    
    def _simple_greedy_fallback(self):
        """
        Greedy đơn giản khi GBFS search thất bại
        Chọn items theo ratio giảm dần
        """
        # Sort by ratio
        sorted_indices = sorted(range(self.n_items), 
                              key=lambda i: self.items[i].ratio, 
                              reverse=True)
        
        selected = []
        current_weight = 0
        
        for i in sorted_indices:
            if current_weight + self.items[i].weight <= self.capacity:
                selected.append(i)
                current_weight += self.items[i].weight
        
        return selected


# =================================================================================
# THUẬT TOÁN 2: BPSO - Binary Particle Swarm Optimization
# =================================================================================
class BPSO_Solver:
    """
    Giải Knapsack bằng Binary PSO
    
    Thuật toán (Kennedy & Eberhart 1997):
    1. Khởi tạo swarm (đàn particles)
    2. Mỗi iteration:
       - Update velocity dựa trên pbest và gbest
       - Update position (binary) dùng sigmoid
       - Update pbest và gbest
    3. Trả về gbest
    
    Ưu điểm: Explore rộng, ít bị trap
    Nhược điểm: Chậm hơn GBFS, có thể mất diversity
    """
    
    def __init__(self, problem: KnapsackProblem,
                 n_particles: int = 30, max_iterations: int = 100,
                 w: float = 0.7, c1: float = 1.5, c2: float = 1.5, 
                 v_max: float = 6.0):
        """
        Khởi tạo BPSO solver
        
        Args:
            problem: KnapsackProblem instance
            n_particles: Số lượng particles
            max_iterations: Số iterations tối đa
            w: Inertia weight (quán tính)
            c1: Cognitive parameter (học từ bản thân)
            c2: Social parameter (học từ đàn)
            v_max: Velocity tối đa
        """
        self.problem = problem
        self.items = problem.items
        self.capacity = problem.capacity
        self.n_items = problem.n_items
        
        # PSO parameters
        self.n_particles = n_particles
        self.max_iterations = max_iterations
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.v_max = v_max
        
        # Extract data
        self.weights = np.array([item.weight for item in self.items])
        self.values = np.array([item.value for item in self.items])
        
        # History
        self.history = []
    
    def evaluate_fitness(self, position: np.ndarray) -> float:
        """
        Tính fitness của một position
        
        Fitness = value nếu feasible
                = value - penalty nếu infeasible
        
        Args:
            position: Binary array [0,1,0,1,...]
        
        Returns:
            Fitness value
        """
        total_value = np.sum(self.values * position)
        total_weight = np.sum(self.weights * position)
        
        if total_weight <= self.capacity:
            return total_value
        else:
            # Penalty cho infeasible solution
            overflow = total_weight - self.capacity
            return total_value - 1000 * overflow
    
    def solve(self, verbose: bool = False) -> Dict:
        """
        Giải bài toán bằng BPSO
        
        Args:
            verbose: In log ra màn hình
        
        Returns:
            Dict chứa kết quả
        """
        # ===== KHỞI TẠO SWARM =====
        # Positions: Binary matrix (n_particles × n_items)
        positions = np.random.randint(0, 2, (self.n_particles, self.n_items))
        
        # Velocities: Continuous matrix (n_particles × n_items)
        velocities = np.random.uniform(-4, 4, (self.n_particles, self.n_items))
        
        # Personal best positions và fitness
        pbest_positions = positions.copy()
        pbest_fitness = np.array([self.evaluate_fitness(p) for p in positions])
        
        # Global best
        gbest_idx = np.argmax(pbest_fitness)
        gbest_position = pbest_positions[gbest_idx].copy()
        gbest_fitness = pbest_fitness[gbest_idx]
        
        # History
        self.history = []
        
        # ===== MAIN LOOP =====
        for iteration in range(self.max_iterations):
            for i in range(self.n_particles):
                # --- Update Velocity ---
                # Công thức: v = w*v + c1*r1*(pbest-x) + c2*r2*(gbest-x)
                r1 = np.random.random(self.n_items)
                r2 = np.random.random(self.n_items)
                
                velocities[i] = (
                    self.w * velocities[i] +
                    self.c1 * r1 * (pbest_positions[i] - positions[i]) +
                    self.c2 * r2 * (gbest_position - positions[i])
                )
                
                # Clamp velocity
                velocities[i] = np.clip(velocities[i], -self.v_max, self.v_max)
                
                # --- Update Position (Binary) ---
                # Sigmoid: P(bit=1) = 1 / (1 + exp(-v))
                sigmoid = 1.0 / (1.0 + np.exp(-velocities[i]))
                positions[i] = (np.random.random(self.n_items) < sigmoid).astype(int)
                
                # --- Evaluate ---
                fitness = self.evaluate_fitness(positions[i])
                
                # --- Update Personal Best ---
                if fitness > pbest_fitness[i]:
                    pbest_positions[i] = positions[i].copy()
                    pbest_fitness[i] = fitness
                
                # --- Update Global Best ---
                if fitness > gbest_fitness:
                    gbest_position = positions[i].copy()
                    gbest_fitness = fitness
            
            # Log history
            avg_fitness = np.mean(pbest_fitness)
            self.history.append({
                'iteration': iteration,
                'gbest_fitness': gbest_fitness,
                'avg_fitness': avg_fitness
            })
            
            # Verbose
            if verbose and iteration % 10 == 0:
                print(f"Iter {iteration:3d}: Best={gbest_fitness:.0f}, Avg={avg_fitness:.0f}")
        
        # ===== TRÍCH XUẤT KẾT QUẢ =====
        total_weight = int(np.sum(self.weights * gbest_position))
        total_value = int(np.sum(self.values * gbest_position))
        is_feasible = total_weight <= self.capacity
        
        selected_indices = [i for i in range(self.n_items) if gbest_position[i] == 1]
        selected_items = [self.items[i] for i in selected_indices]
        
        return {
            'algorithm': 'BPSO',
            'solution': gbest_position,
            'selected_indices': selected_indices,
            'selected_items': selected_items,
            'total_value': total_value,
            'total_weight': total_weight,
            'is_feasible': is_feasible,
            'iterations': self.max_iterations,
            'n_items_selected': len(selected_indices),
            'history': self.history
        }


# =================================================================================
# THUẬT TOÁN 3: DP - Dynamic Programming (Optimal)
# =================================================================================
class DP_Solver:
    """
    Giải Knapsack bằng Dynamic Programming
    
    Thuật toán:
    1. Tạo bảng DP[i][w]: value tối đa với i items đầu và capacity w
    2. DP[i][w] = max(
            DP[i-1][w],                          # Không chọn item i
            DP[i-1][w-weight[i]] + value[i]      # Chọn item i
        )
    3. Backtrack để tìm items được chọn
    
    Ưu điểm: Tìm được optimal solution
    Nhược điểm: Chậm với dataset lớn, cần nhiều memory
    """
    
    def __init__(self, problem: KnapsackProblem):
        """
        Khởi tạo DP solver
        
        Args:
            problem: KnapsackProblem instance
        """
        self.problem = problem
        self.items = problem.items
        self.capacity = problem.capacity
        self.n_items = problem.n_items
    
    def solve(self) -> Dict:
        """
        Giải bài toán bằng DP
        
        Returns:
            Dict chứa optimal solution
        """
        n = self.n_items
        W = self.capacity
        
        # ===== TẠO BẢNG DP =====
        # dp[i][w] = value tối đa với i items đầu tiên và capacity w
        dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]
        
        # ===== FILL BẢNG DP =====
        for i in range(1, n + 1):
            item = self.items[i - 1]
            for w in range(W + 1):
                # Không chọn item i
                dp[i][w] = dp[i - 1][w]
                
                # Chọn item i (nếu có thể)
                if item.weight <= w:
                    dp[i][w] = max(dp[i][w], 
                                  dp[i - 1][w - item.weight] + item.value)
        
        # ===== BACKTRACK ĐỂ TÌM ITEMS =====
        selected_indices = []
        w = W
        for i in range(n, 0, -1):
            # Nếu dp[i][w] != dp[i-1][w] → item i được chọn
            if dp[i][w] != dp[i - 1][w]:
                selected_indices.append(i - 1)
                w -= self.items[i - 1].weight
        
        selected_indices.reverse()
        
        # ===== TRÍCH XUẤT KẾT QUẢ =====
        optimal_value = dp[n][W]
        
        solution_binary = np.zeros(n, dtype=int)
        solution_binary[selected_indices] = 1
        
        total_value, total_weight, is_feasible = self.problem.evaluate_solution(solution_binary)
        
        selected_items = [self.items[i] for i in selected_indices]
        
        return {
            'algorithm': 'DP (Optimal)',
            'solution': solution_binary,
            'selected_indices': selected_indices,
            'selected_items': selected_items,
            'total_value': total_value,
            'total_weight': total_weight,
            'is_feasible': is_feasible,
            'n_items_selected': len(selected_indices)
        }


# =================================================================================
# HÀM TIỆN ÍCH: Sinh dataset
# =================================================================================
def generate_dataset(n_items: int, max_value: int, max_weight: int, 
                     capacity: int, seed: int = 42,
                     dataset_type: str = 'random') -> KnapsackProblem:
    """
    Sinh dataset cho bài toán Knapsack
    
    Args:
        n_items: Số lượng items
        max_value: Giá trị tối đa của item
        max_weight: Trọng lượng tối đa của item
        capacity: Sức chứa túi
        seed: Random seed
        dataset_type: Loại dataset
            - 'random': Ngẫu nhiên cân bằng
            - 'high_correlation': value-weight tương quan cao
            - 'outlier': Có items nặng gần capacity
            - 'similar_ratio': v/w ratio gần nhau
    
    Returns:
        KnapsackProblem instance
    """
    np.random.seed(seed)
    
    # Sinh values và weights theo loại dataset
    if dataset_type == 'random':
        values = np.random.randint(10, max_value + 1, n_items)
        weights = np.random.randint(5, max_weight + 1, n_items)
    
    elif dataset_type == 'high_correlation':
        weights = np.random.randint(5, max_weight + 1, n_items)
        values = (weights * 2 + np.random.randint(-10, 11, n_items)).astype(int)
        values = np.clip(values, 10, max_value)
    
    elif dataset_type == 'outlier':
        values = np.random.randint(10, max_value + 1, n_items)
        weights = np.random.randint(5, max_weight + 1, n_items)
        
        # Tạo outliers
        n_outliers = min(2, n_items // 10)
        outlier_indices = np.random.choice(n_items, n_outliers, replace=False)
        for idx in outlier_indices:
            weights[idx] = int(capacity * 0.6)
            values[idx] = max_value * 2
    
    elif dataset_type == 'similar_ratio':
        base_ratio = 2.0
        weights = np.random.randint(5, max_weight + 1, n_items)
        values = (weights * base_ratio + np.random.randint(-5, 6, n_items)).astype(int)
        values = np.clip(values, 10, max_value)
    
    else:
        values = np.random.randint(10, max_value + 1, n_items)
        weights = np.random.randint(5, max_weight + 1, n_items)
    
    # Tạo items
    items = [Item(f"Item_{i}", int(weights[i]), int(values[i])) 
             for i in range(n_items)]
    
    return KnapsackProblem(items, capacity)
