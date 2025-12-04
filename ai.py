from simpleai.search import SearchProblem, greedy


class SimpleKnapsackAI(SearchProblem):
    def __init__(self, items, capacity):
        """
        items: list of (name, weight, value)
        capacity: max capacity
        """
        self.items = items
        self.capacity = capacity

        # initial state: empty tuple
        super().__init__(initial_state=tuple())

    # --------------------------------------------
    # 1. Actions: trả về list item index có thể thêm
    # --------------------------------------------
    def actions(self, state):
        current_weight = sum(self.items[i][1] for i in state)
        possible = []

        for i in range(len(self.items)):
            if i not in state:
                if current_weight + self.items[i][1] <= self.capacity:
                    possible.append(i)

        return possible

    # --------------------------------------------
    # 2. Result: state mới sau khi chọn item index=action
    # --------------------------------------------
    def result(self, state, action):
        new_state = tuple(sorted(state + (action,)))
        return new_state

    # --------------------------------------------
    # 3. is_goal: không còn item nào thêm được
    # --------------------------------------------
    def is_goal(self, state):
        current_weight = sum(self.items[i][1] for i in state)

        for i in range(len(self.items)):
            if i not in state and current_weight + self.items[i][1] <= self.capacity:
                return False
        return True

    # --------------------------------------------
    # 4. Heuristic đơn giản: v/w của item có thể chọn tiếp
    #    Lấy giá trị MAX v/w trong các item chưa chọn.
    #    GBFS sẽ chọn state dẫn đến item tiếp theo tốt nhất.
    # --------------------------------------------
    def heuristic(self, state):
        best_ratio = 0

        for i in range(len(self.items)):
            if i not in state:
                value = self.items[i][2]
                weight = self.items[i][1]
                ratio = value / weight
                best_ratio = max(best_ratio, ratio)

        # simpleai: heuristic càng nhỏ càng ưu tiên
        return -best_ratio


# ------------------------------------------------------
# CHẠY THUẬT TOÁN
# ------------------------------------------------------
if __name__ == "__main__":
    items = [
        ("A", 5, 10),
        ("B", 4, 6),
        ("C", 3, 5),
        ("D", 2, 4),
        ("E", 6, 13),
    ]

    capacity = 10

    problem = SimpleKnapsackAI(items, capacity)

    result = greedy(problem, graph_search=True)

    print("\n=== RESULT ===")
    print("Selected items:", result.state)
    total_value = sum(items[i][2] for i in result.state)
    total_weight = sum(items[i][1] for i in result.state)
    print("Total value:", total_value)
    print("Total weight:", total_weight)

   