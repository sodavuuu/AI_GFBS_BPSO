"""
Knapsack Problem sử dụng SimpleAI
Dựa trên ai.py đã có
"""
from simpleai.search import SearchProblem, greedy, astar, breadth_first, depth_first
import numpy as np
from typing import List, Tuple


class KnapsackGBFS(SearchProblem):
    """
    0/1 Knapsack Problem sử dụng GBFS của SimpleAI
    
    State: tuple các index của items đã chọn
    Example: (0, 2, 5) = đã chọn items 0, 2, 5
    """
    
    def __init__(self, items: List[Tuple[str, int, int]], capacity: int):
        """
        Args:
            items: List of (name, weight, value)
            capacity: Max weight capacity
        """
        self.items = items
        self.capacity = capacity
        self.n_items = len(items)
        
        # Thống kê
        self.states_explored = 0
        self.max_depth = 0
        
        # Initial state: empty knapsack
        super().__init__(initial_state=tuple())
    
    def actions(self, state):
        """
        Trả về list các items có thể thêm vào
        
        Điều kiện:
        - Item chưa được chọn
        - Thêm vào không vượt capacity
        """
        current_weight = sum(self.items[i][1] for i in state)
        possible_actions = []
        
        for i in range(self.n_items):
            if i not in state:
                item_weight = self.items[i][1]
                if current_weight + item_weight <= self.capacity:
                    possible_actions.append(i)
        
        return possible_actions
    
    def result(self, state, action):
        """
        State mới sau khi chọn item có index = action
        """
        self.states_explored += 1
        new_state = tuple(sorted(state + (action,)))
        self.max_depth = max(self.max_depth, len(new_state))
        return new_state
    
    def is_goal(self, state):
        """
        Goal: Không thể thêm item nào nữa
        """
        return len(self.actions(state)) == 0
    
    def heuristic(self, state):
        """
        Heuristic: Fractional Knapsack Bound
        
        Ước lượng giá trị tối đa có thể đạt được từ state này:
        1. Tính value hiện tại
        2. Tính remaining capacity
        3. Sắp xếp items chưa chọn theo v/w giảm dần
        4. Thêm items theo thứ tự (fractional nếu cần)
        
        SimpleAI: heuristic càng NHỎ càng ưu tiên
        → Return -bound (âm của upper bound)
        """
        current_value = sum(self.items[i][2] for i in state)
        current_weight = sum(self.items[i][1] for i in state)
        remaining_capacity = self.capacity - current_weight
        
        # Items chưa chọn với ratio v/w
        remaining_items = []
        for i in range(self.n_items):
            if i not in state:
                name, weight, value = self.items[i]
                ratio = value / weight if weight > 0 else 0
                remaining_items.append((i, weight, value, ratio))
        
        # Sắp xếp theo ratio giảm dần
        remaining_items.sort(key=lambda x: x[3], reverse=True)
        
        # Fractional knapsack để ước lượng
        fractional_value = current_value
        for i, weight, value, ratio in remaining_items:
            if remaining_capacity >= weight:
                fractional_value += value
                remaining_capacity -= weight
            else:
                # Lấy phần fractional
                fractional_value += ratio * remaining_capacity
                break
        
        # Return âm để SimpleAI ưu tiên giá trị cao
        return -fractional_value
    
    def value(self, state):
        """Cost function (không dùng cho GBFS nhưng cần cho A*)"""
        return -sum(self.items[i][2] for i in state)
    
    def get_solution_info(self, state):
        """Lấy thông tin về solution"""
        total_value = sum(self.items[i][2] for i in state)
        total_weight = sum(self.items[i][1] for i in state)
        items_selected = [self.items[i][0] for i in state]
        
        return {
            'state': state,
            'items': items_selected,
            'total_value': total_value,
            'total_weight': total_weight,
            'capacity': self.capacity,
            'n_items_selected': len(state),
            'states_explored': self.states_explored,
            'max_depth': self.max_depth
        }


def generate_dataset(n_items: int, max_value: int, max_weight: int, 
                     capacity: int, seed: int = 42,
                     dataset_type: str = 'random') -> List[Tuple[str, int, int]]:
    """
    Sinh dataset cho Knapsack
    
    Args:
        n_items: Số lượng items
        max_value: Giá trị tối đa
        max_weight: Trọng lượng tối đa
        capacity: Sức chứa túi
        seed: Random seed
        dataset_type: 'random', 'high_correlation', 'outlier', 'similar_ratio'
    
    Returns:
        List of (name, weight, value)
    """
    np.random.seed(seed)
    
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
        
        n_outliers = min(3, n_items // 10)
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
    
    items = [(f"Item_{i}", int(weights[i]), int(values[i])) 
             for i in range(n_items)]
    
    return items


def analyze_dataset(items: List[Tuple[str, int, int]], capacity: int):
    """Phân tích dataset"""
    print("\n" + "="*70)
    print("PHÂN TÍCH DATASET")
    print("="*70)
    
    values = np.array([item[2] for item in items])
    weights = np.array([item[1] for item in items])
    ratios = values / weights
    
    print(f"\nSố items: {len(items)}")
    print(f"Capacity: {capacity}")
    print(f"\nValue:  min={values.min()}, max={values.max()}, avg={values.mean():.1f}")
    print(f"Weight: min={weights.min()}, max={weights.max()}, avg={weights.mean():.1f}")
    print(f"Ratio (v/w): min={ratios.min():.2f}, max={ratios.max():.2f}, avg={ratios.mean():.2f}")
    print(f"Ratio std: {ratios.std():.2f} (CV: {ratios.std()/ratios.mean():.1%})")
    
    corr = np.corrcoef(values, weights)[0, 1]
    print(f"\nCorrelation (v-w): {corr:.3f}")
    
    # Top 5 items
    print("\nTop 5 items (by v/w ratio):")
    items_with_ratio = [(items[i][0], items[i][1], items[i][2], ratios[i]) 
                        for i in range(len(items))]
    items_with_ratio.sort(key=lambda x: x[3], reverse=True)
    
    for i, (name, weight, value, ratio) in enumerate(items_with_ratio[:5]):
        print(f"  {i+1}. {name}: w={weight}, v={value}, ratio={ratio:.2f}")
    
    print("\n" + "="*70)


def solve_optimal_dp(items: List[Tuple[str, int, int]], capacity: int) -> Tuple[int, List[int]]:
    """
    Giải optimal bằng Dynamic Programming
    
    Returns:
        (optimal_value, selected_indices)
    """
    n = len(items)
    
    # DP table
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    # Fill DP table
    for i in range(1, n + 1):
        name, weight, value = items[i - 1]
        for w in range(capacity + 1):
            # Không chọn item i
            dp[i][w] = dp[i - 1][w]
            
            # Chọn item i nếu có thể
            if weight <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - weight] + value)
    
    # Backtrack để tìm items
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(i - 1)
            w -= items[i - 1][1]
    
    selected.reverse()
    optimal_value = dp[n][capacity]
    
    return optimal_value, selected
