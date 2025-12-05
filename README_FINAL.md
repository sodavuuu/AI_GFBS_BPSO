# 🎒 Knapsack Problem: GBFS vs BPSO vs DP

**Thesis-ready** Knapsack solver với visualization chuyên nghiệp và step-by-step algorithm tracking

## ✨ Đặc điểm nổi bật

### 📓 **Jupyter Notebooks** (theo chuẩn GA_TSP)
Tổ chức rõ ràng theo structure của GA_TSP project:
- **`notebooks/1_Parameter.ipynb`** - Section 3.1.1: Phân tích ảnh hưởng tham số
- **`notebooks/2_Algo.ipynb`** - Section 3.1.2: So sánh thuật toán chi tiết
- **`notebooks/3_Data.ipynb`** - Section 3.1.3: Ảnh hưởng đặc điểm dữ liệu
- **`notebooks/4_StepByStep.ipynb`** - ⭐ **Trực quan từng bước thuật toán**

### 🎬 **Step-by-Step Visualization**
Điểm nổi bật của project - xem thuật toán chạy **từng bước một**:
- **GBFS**: Xem cách chọn item theo ratio, tại sao chọn item đó
- **BPSO**: Xem particles di chuyển, fitness thay đổi mỗi iteration
- Interactive controls: Next ▶ / ◀ Previous / Jump to Step
- Hiển thị: selected items, capacity bar, available items, statistics

### 💻 **GUI Application** (PyQt5)
4 tabs đầy đủ:
1. **Problem Visualization** - Scatter plot items (weight vs value)
2. **BPSO Convergence** - Real-time fitness curve
3. **Algorithm Comparison** - So sánh 3 thuật toán
4. **Solution Details** - Chi tiết items được chọn

### 📊 **Experiments Framework**
Auto-generate charts + CSV cho thesis:
- Section 3.1.1: Parameter impact (GBFS max_states, BPSO n_particles/iterations)
- Section 3.1.2: Algorithm comparison (trên 13 test cases)
- Section 3.1.3: Data characteristics (size, region, category, correlation)
- Output: 300 DPI PNG + CSV data trong `results/chapter3/`

---

## 🚀 Quick Start

### Option 1: Jupyter Notebooks (Recommended!)
```bash
# Activate environment
source .venv/bin/activate

# Start Jupyter
jupyter notebook notebooks/

# Mở: 1_Parameter.ipynb để bắt đầu
```

### Option 2: GUI Application
```bash
python gui_app_enhanced.py
```

### Option 3: Run Experiments
```bash
# Chạy tất cả experiments (30 phút)
python experiment/chapter3_experiments_v2.py --experiment all

# Output: results/chapter3/*.png và *.csv
```

---

## 📁 Project Structure

```
AI_GFBS_BPSO/
├── notebooks/                         # ⭐ Jupyter Notebooks
│   ├── 1_Parameter.ipynb             # Section 3.1.1
│   ├── 2_Algo.ipynb                  # Section 3.1.2
│   ├── 3_Data.ipynb                  # Section 3.1.3
│   └── 4_StepByStep.ipynb            # Step-by-step demo
│
├── src/                               # Source code
│   ├── gbfs_knapsack.py              # GBFS algorithm
│   ├── bpso_knapsack.py              # BPSO algorithm
│   ├── dp_knapsack.py                # Dynamic Programming
│   ├── advanced_visualizer.py        # Charts (GA_TSP style)
│   ├── step_tracker.py               # ⭐ Track algorithm steps
│   ├── step_visualizer.py            # ⭐ Visualize steps
│   └── test_case_loader.py           # Load 13 test cases
│
├── experiment/
│   └── chapter3_experiments_v2.py    # Organized experiments
│
├── gui_app_enhanced.py                # GUI application
├── demo_visualizations.py             # Quick demo
│
├── data/test_cases/                   # 13 CSV test cases
│   ├── size_small_30.csv
│   ├── size_medium_50.csv            # Main test
│   ├── size_large_70.csv
│   ├── region_*.csv
│   ├── category_*.csv
│   └── data_*.csv
│
└── results/chapter3/                  # Output charts + CSV
    ├── 3_1_1_a_gbfs_params.png
    ├── 3_1_2_comparison_*.png
    └── 3_1_3_data_characteristics.png
```

---

## 🧪 Algorithms Comparison

| Algorithm | Type | Time Complexity | Optimal? | Best For |
|-----------|------|----------------|----------|----------|
| **GBFS** | Greedy Search | O(n² × max_states) | ❌ | Heuristic-friendly problems |
| **BPSO** | Metaheuristic | O(particles × iterations × n) | ❌ | Complex search spaces |
| **DP** | Exact | O(n × capacity) | ✅ | Small-medium instances |

---

## 📊 Test Cases (13 total)

### By Size
- Size Small 30 (30 items)
- **Size Medium 50** (50 items) - Main test
- Size Large 70 (70 items)

### By Region
- Region 1Regions
- Region 2Regions
- Region 3Regions

### By Category
- Category Clothing
- Category Electronics
- Category Food
- Category Furniture

### By Data Characteristics
- Data High Correlation (weight-value correlation > 0.8)
- Data Low Correlation (< 0.3)
- Data High Value (values 100-200)

---

## 📖 Documentation

- **`SECTION_3_2_GUIDE.md`** - Hướng dẫn viết section 3.2
- **`README_ENHANCED.md`** - Chi tiết features
- **`IMPLEMENTATION_SUMMARY.md`** - Technical summary
- **`LEARNING_FROM_GA_TSP_SUMMARY.md`** - Lessons learned

---

## 🎯 Key Features

### 1. Step-by-Step Algorithm Tracking
```python
from src.step_tracker import GBFSStepTracker
from src.step_visualizer import StepByStepVisualizer

tracker = GBFSStepTracker()
result = tracker.solve_with_tracking(items, weights, values, capacity)

# Visualize any step
visualizer = StepByStepVisualizer()
fig = visualizer.visualize_gbfs_step(
    tracker.get_step(5),  # Step 5
    items, weights, values
)
```

### 2. Advanced Visualization
```python
from src.advanced_visualizer import AdvancedKnapsackVisualizer

vis = AdvancedKnapsackVisualizer()
vis.plot_gbfs_parameter_impact(results_df, save_path='output.png')
vis.plot_algorithm_comparison_detailed(comparison_df, ...)
```

### 3. Organized Experiments
```python
from experiment.chapter3_experiments_v2 import *

# Run parameter analysis
experiment_3_1_1_a_gbfs_parameters()  # Auto-save PNG + CSV

# Run algorithm comparison
experiment_3_1_2_algorithm_comparison_single('Size Medium 50')

# Run all
run_all_experiments()
```

---

## 🔬 Example Results

### GBFS Parameter Impact (Section 3.1.1)
- Max states: 1000 → 10000
- Value increases ~15%
- Time increases exponentially
- Sweet spot: 5000 states

### Algorithm Comparison (Section 3.1.2)
- **DP**: Always optimal, but slowest (0.5s for 50 items)
- **GBFS**: ~5% gap, very fast (0.02s)
- **BPSO**: ~8% gap, fastest (0.01s)

### Data Characteristics (Section 3.1.3)
- **High correlation**: All algorithms perform well
- **Low correlation**: BPSO more robust
- **Large size**: DP impractical, BPSO scales best

---

## 💡 Usage Examples

### Jupyter Notebook
See `notebooks/4_StepByStep.ipynb` for interactive demo

### Python Script
```python
from src.gbfs_knapsack import solve_knapsack_gbfs
from src.test_case_loader import TestCaseLoader

loader = TestCaseLoader()
tc = loader.load_test_case('Size Medium 50')

result = solve_knapsack_gbfs(
    tc['items'], tc['weights'], tc['values'], tc['capacity'],
    max_states=5000
)

print(f"Value: {result['total_value']}")
print(f"Items: {result['selected_items']}")
```

---

## 📝 Requirements

```
Python 3.13+
PyQt5 (GUI)
matplotlib, seaborn (Visualization)
numpy, pandas (Data processing)
simpleai (GBFS implementation)
jupyter, ipywidgets (Notebooks)
```

---

## 🎓 For Thesis

1. **Run experiments**: `python experiment/chapter3_experiments_v2.py --experiment all`
2. **Get charts**: Check `results/chapter3/` for PNG files
3. **Get data**: Check CSV files for tables
4. **Write analysis**: Follow `SECTION_3_2_GUIDE.md`
5. **Take screenshots**: Run GUI and notebooks

---

## 📧 Author

Project for AI course - Knapsack Problem Analysis

