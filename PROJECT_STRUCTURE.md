# 🎯 KNAPSACK PROJECT - STRUCTURE & FLOW

## 📋 FLOW TƯ DUY (Học từ GA_TSP)

### **Chương 3: Phân tích & Đánh giá**
```
3.1.1. Ảnh hưởng tham số    → 1. Parameter.ipynb
3.1.2. So sánh thuật toán   → 2. Algo.ipynb  
3.1.3. Ảnh hưởng dữ liệu    → 3. Data.ipynb
```

### **Chương 4: Demo & Visualization**
```
4.1. Step-by-step execution → 4. StepByStep.ipynb
4.2. Interactive GUI        → knapsack_solver_gui.py
```

---

## 📁 CẤU TRÚC FILE

### **src/** - Core Algorithms & Utilities

#### **Algorithms (3 files - theo GA_TSP pattern)**
```
src/gbfs_knapsack.py       → solve_knapsack_gbfs()
src/bpso_knapsack.py       → solve_knapsack_bpso()  
src/dp_knapsack.py         → solve_knapsack_dp()
```

#### **Data Loading**
```
src/test_case_loader.py    → TestCaseLoader class
src/data_generator.py      → Generate test cases (chạy 1 lần)
src/data_loader.py         → Legacy loader
```

#### **Visualization**
```
src/algorithm_visualizer.py    → Basic visualization
src/advanced_visualizer.py     → Advanced charts (GBFS tree, BPSO swarm, DP table)
```

#### **Step-by-Step Tracking**
```
src/step_tracker.py        → GBFSStepTracker, BPSOStepTracker, DPStepTracker
src/step_visualizer.py     → StepByStepVisualizer
```

---

### **experiment/** - Notebooks & Scripts

#### **Notebooks (4 files)**
```
1. Parameter.ipynb     → Test GBFS max_states, BPSO n_particles/iterations
2. Algo.ipynb          → Compare GBFS vs BPSO vs DP
3. Data.ipynb          → Test with different data characteristics
4. StepByStep.ipynb    → Interactive step-by-step visualization
```

#### **Scripts**
```
chapter3_experiments_v2.py → Run all Chapter 3 experiments
```

---

### **data/test_cases/** - Test Data

#### **13 CSV Files**
```
Size:
- size_small_30.csv       → 30 items
- size_medium_50.csv      → 50 items  
- size_large_70.csv       → 70 items

Regional:
- region_1regions_medium.csv
- region_2regions_medium.csv
- region_3regions_medium.csv

Category:
- category_clothing_medium.csv
- category_electronics_medium.csv
- category_food_medium.csv
- category_furniture_medium.csv

Data Characteristics:
- data_high_correlation_medium.csv
- data_high_value_medium.csv
- data_low_correlation_medium.csv
```

#### **Summary File**
```
test_cases_summary.csv     → Metadata của tất cả test cases
```

---

## 🔧 CÁCH SỬ DỤNG

### **1. Load Test Case**
```python
from src.test_case_loader import TestCaseLoader

loader = TestCaseLoader()
test_case = loader.load_test_case('Size Medium 50')

# Dict keys:
# - 'items': List[str]
# - 'weights': List[float]
# - 'values': List[float]
# - 'capacity': int
# - 'test_case_name': str  ← Chú ý: không phải 'name'!
# - 'n_items', 'total_weight', 'total_value', 'correlation', ...
```

### **2. Run Algorithms**
```python
from src.gbfs_knapsack import solve_knapsack_gbfs
from src.bpso_knapsack import solve_knapsack_bpso
from src.dp_knapsack import solve_knapsack_dp

# GBFS
result = solve_knapsack_gbfs(
    test_case['items'],
    test_case['weights'],
    test_case['values'],
    test_case['capacity'],
    max_states=5000
)

# BPSO
result = solve_knapsack_bpso(
    test_case['items'],
    test_case['weights'],
    test_case['values'],
    test_case['capacity'],
    n_particles=30,
    max_iterations=100
)

# DP
result = solve_knapsack_dp(
    test_case['items'],
    test_case['weights'],
    test_case['values'],
    test_case['capacity']
)

# Result dict keys:
# - 'selected_items': List[str]
# - 'selected_indices': List[int]
# - 'total_value': float
# - 'total_weight': float
# - 'execution_time': float
# - Extra: 'states_explored' (GBFS), 'convergence' (BPSO), 'dp_table' (DP)
```

### **3. Visualize**
```python
from src.advanced_visualizer import AdvancedKnapsackVisualizer

viz = AdvancedKnapsackVisualizer()

# GBFS tree
if 'state_tree' in result:
    viz.visualize_gbfs_tree(result['state_tree'], test_case)

# BPSO swarm
if 'particle_history' in result:
    viz.visualize_bpso_swarm(result['particle_history'], test_case)

# DP table
if 'dp_table' in result:
    viz.visualize_dp_table(result['dp_table'], test_case)
```

---

## ⚠️ NHỮNG LỖI THƯỜNG GẶP

### **1. Tên test case sai**
```python
# ❌ SAI
test_case = loader.load_test_case('Size_Medium_50')  # có dấu gạch dưới

# ✅ ĐÚNG
test_case = loader.load_test_case('Size Medium 50')  # không có dấu gạch dưới
```

### **2. Tên key trong dict**
```python
# ❌ SAI
print(test_case['name'])  # KeyError!

# ✅ ĐÚNG
print(test_case['test_case_name'])
```

### **3. Tên hàm cũ**
```python
# ❌ SAI (old names)
solve_gbfs()
solve_bpso()
solve_dp()

# ✅ ĐÚNG (new names)
solve_knapsack_gbfs()
solve_knapsack_bpso()
solve_knapsack_dp()
```

### **4. Thứ tự tham số**
```python
# ✅ ĐÚNG - Tất cả 3 thuật toán dùng cùng thứ tự
solve_knapsack_gbfs(items, weights, values, capacity, ...)
solve_knapsack_bpso(items, weights, values, capacity, ...)
solve_knapsack_dp(items, weights, values, capacity)
```

---

## 🚀 QUICK START

### **Option 1: Chạy GUI**
```bash
python3 knapsack_solver_gui.py
```

### **Option 2: Chạy Notebooks**
```bash
cd experiment/
jupyter notebook
# Mở: 1. Parameter.ipynb, 2. Algo.ipynb, 3. Data.ipynb, 4. StepByStep.ipynb
```

### **Option 3: Chạy Experiments Script**
```bash
cd experiment/
python3 chapter3_experiments_v2.py --experiment all
```

---

## 📊 OUTPUT

### **CSV Files** (in results/chapter3/)
```
3_1_1_a_gbfs_params.csv
3_1_1_b_bpso_swarm_size.csv
3_1_1_c_bpso_iterations.csv
3_1_2_comparison_*.csv
3_1_3_data_characteristics.csv
```

### **Charts** (in results/chapter3/)
```
3_1_1_a_gbfs_params.png
3_1_1_b_bpso_swarm_size.png
3_1_2_comparison_*.png
3_1_3_data_characteristics.png
```

---

## 🎓 HỌC TỪ GA_TSP

### **Những điểm giống**
✅ 1 thuật toán = 1 file riêng  
✅ Notebooks trong `experiment/`  
✅ CSV + PNG output cho mỗi experiment  
✅ Clear naming convention  
✅ Step-by-step visualization  

### **Những điểm khác**
🔸 GA_TSP: 1 algorithm → Knapsack: 3 algorithms  
🔸 GA_TSP: Population-based only → Knapsack: Heuristic + Metaheuristic + Exact  
🔸 GA_TSP: TSP data → Knapsack: Regional/Category/Size data  

---

## 🔍 CHECKLIST TRƯỚC KHI CHẠY

- [ ] Đã cài đặt dependencies: `./install_dependencies.sh`
- [ ] Test case names không có dấu `_`: `'Size Medium 50'` ✅
- [ ] Dùng `test_case['test_case_name']` không phải `['name']`
- [ ] Import đúng: `from src.gbfs_knapsack import solve_knapsack_gbfs`
- [ ] Function calls đúng: `solve_knapsack_gbfs()` không phải `solve_gbfs()`
- [ ] Tất cả notebooks trong `experiment/` không phải `notebooks/`

---

**Last Updated**: 2025-12-06  
**Status**: ✅ Ready to use
