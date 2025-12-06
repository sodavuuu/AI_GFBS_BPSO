# 🎒 Knapsack Solver - Multi-Objective Optimization

**Version 2.0** | **GBFS + BPSO + DP** | **Unified GUI** | **Chapter 3 Analysis**

A comprehensive implementation of three algorithms for solving the Multi-Objective 0/1 Knapsack Problem with interactive GUI and experimental analysis.

---

## 📋 Problem Definition

**Multi-Objective 0/1 Knapsack**:
- **Objective 1**: Maximize total value (revenue)
- **Objective 2**: Maximize regional diversity
- **Constraint**: Total weight ≤ Capacity

### 🎯 Algorithms

1. **GBFS** (Greedy Best-First Search)
   - Fast heuristic approach
   - Selects items by value/weight ratio
   - O(n log n) complexity

2. **BPSO** (Binary Particle Swarm Optimization)
   - Metaheuristic search algorithm
   - Population-based optimization
   - Good balance between exploration and exploitation

3. **DP** (Dynamic Programming)
   - Optimal solution guaranteed
   - Classical approach
   - O(n × capacity) complexity

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/sodavuuu/AI_GFBS_BPSO.git
cd AI_GFBS_BPSO

# Install dependencies
pip install -r requirements.txt
```

### Run GUI

```bash
python3 run_gui.py
```

### Run Experiments

```bash
# Chapter 3 experiments
cd experiment/chapter3
python3 experiments.py
```

---

## 📁 Project Structure

```
AI_GFBS_BPSO/
├── gui/                    # GUI Application
│   ├── __init__.py
│   └── main_gui.py        # Unified GUI (7 tabs)
│
├── src/                    # Source Code
│   ├── algorithms/        # Algorithm Implementations
│   │   ├── gbfs_knapsack.py
│   │   ├── bpso_knapsack.py
│   │   └── dp_knapsack.py
│   ├── utils/             # Utilities
│   │   └── test_case_loader.py
│   └── visualization/     # Visualization
│       ├── step_by_step_visualizer.py
│       └── advanced_visualizer.py
│
├── data/                   # Test Data
│   └── test_cases/        # 13 CSV test cases
│
├── experiment/            # Experiments
│   ├── chapter3/          # Chapter 3 Analysis
│   │   ├── experiments.py
│   │   └── *.ipynb       # Jupyter notebooks
│   └── chapter4/          # Chapter 4 (Future)
│
├── results/               # Experiment Results
│   └── chapter3/          # CSV result files
│
├── run_gui.py             # GUI Launcher
└── requirements.txt       # Dependencies
```

---

## 🖥️ GUI Features

### 7 Interactive Tabs:

1. **Problem Tab**
   - Interactive item selection
   - Click items to manually select/deselect
   - Visual representation of items (weight vs value)

2. **GBFS Flow Tab**
   - Selection order visualization
   - Arrows showing greedy path
   - Ratio ranking

3. **BPSO Swarm Tab**
   - Convergence plot
   - Swarm diversity
   - Solution space with connections

4. **Comparison Tab**
   - Algorithm performance comparison
   - Value and time charts
   - Bar graphs

5. **Regional Tab**
   - Regional distribution analysis
   - Diversity scores (Shannon entropy)
   - Items colored by region

6. **Details Tab**
   - Selected items table
   - Item properties
   - Algorithm used

7. **Chapter 3 Tab**
   - Load experiment results from CSV
   - 5 experiment types:
     - 3.1.1.a: GBFS Parameters
     - 3.1.1.b: BPSO Swarm Size
     - 3.1.1.c: BPSO Iterations
     - 3.1.2: Algorithm Comparison
     - 3.1.3: Data Characteristics

---

## 📊 Test Cases

**13 test cases** with different characteristics:

### By Size:
- **Small**: 30 items, capacity 101
- **Medium**: 50 items, capacity 178
- **Large**: 70 items, capacity varies

### By Category:
- Clothing Medium (70 items, 4 regions)
- Electronics Medium (70 items, 4 regions)
- Food Medium (70 items, 4 regions)
- Furniture Medium (70 items, 4 regions)

### By Correlation:
- Low Correlation (70 items)
- High Correlation (70 items)

### By Value:
- High Value Medium (70 items)

### By Regions:
- 1 Region (70 items)
- 2 Regions (70 items)
- 3 Regions (70 items)

---

## 🧪 Chapter 3 Experiments

### 3.1.1 Parameter Impact

**a) GBFS: max_states parameter**
- Tests: 1000, 2000, 3000, 5000, 10000
- Measures: value, time, efficiency

**b) BPSO: swarm_size**
- Tests: 10, 20, 30, 50, 100
- Measures: value, time

**c) BPSO: iterations**
- Tests: 20, 30, 50, 70, 100
- Measures: value, time, convergence

### 3.1.2 Algorithm Comparison

- Compare GBFS, BPSO, DP across all 13 test cases
- Metrics: value, time, % of optimal

### 3.1.3 Data Characteristics

- Analyze performance on different data types
- Correlation, value, regions impact
- Solution quality comparison

**Results Location**: `results/chapter3/*.csv`

---

## 💻 Usage Examples

### GUI Usage

1. **Launch GUI**:
   ```bash
   python3 run_gui.py
   ```

2. **Select Test Case**: Use dropdown menu

3. **Adjust Parameters**:
   - GBFS: Max States (default 5000)
   - BPSO: Particles (30), Iterations (50), Inertia (0.7)

4. **Run Algorithms**: Click "RUN ALL ALGORITHMS"

5. **View Results**: Switch between tabs to see visualizations

### Programmatic Usage

```python
from src.algorithms import solve_knapsack_gbfs, solve_knapsack_bpso, solve_knapsack_dp

# Prepare data
items = ['Item1', 'Item2', 'Item3']
weights = [10, 20, 30]
values = [60, 100, 120]
capacity = 50

# Run GBFS
result_gbfs = solve_knapsack_gbfs(items, weights, values, capacity)

# Run BPSO
result_bpso = solve_knapsack_bpso(items, weights, values, capacity,
                                   n_particles=30, max_iterations=50)

# Run DP
result_dp = solve_knapsack_dp(items, weights, values, capacity)

# Results contain
print(result_gbfs['selected_items'])  # List of selected items
print(result_gbfs['total_value'])     # Total value
print(result_gbfs['total_weight'])    # Total weight
print(result_gbfs['execution_time'])  # Time in seconds
```

---

## 🔧 Development

### Requirements

- Python 3.8+
- PyQt5 5.15+
- NumPy 1.23+
- Pandas 2.0+
- Matplotlib 3.7+
- Seaborn 0.13+

### Code Style

- PEP 8 compliant
- Type hints where applicable
- Docstrings for all functions
- Modular structure

---

## 📚 Documentation

- **README.md** (this file): Project overview
- **USAGE.md**: Detailed usage guide
- **experiment/chapter3/README.md**: Experiment documentation
- **SECTION_3_2_GUIDE.md**: Section 3.2 guide

---

## 🎓 Academic Context

This project implements:
- **Chapter 3**: Analysis and Evaluation
  - Parameter tuning
  - Algorithm comparison
  - Data characteristics analysis
  
- **Future Chapter 4**: Advanced topics

---

## 📄 License

MIT License

Copyright (c) 2025 Ha Phuong Quynh

---

## 👥 Author

**Ha Phuong Quynh** (@sodavuuu)
- GitHub: [sodavuuu](https://github.com/sodavuuu)
- Repository: [AI_GFBS_BPSO](https://github.com/sodavuuu/AI_GFBS_BPSO)

---

## 🙏 Acknowledgments

- Inspired by GA_TSP project structure
- PyQt5 for GUI framework
- Matplotlib/Seaborn for visualizations
- NumPy/Pandas for data processing

---

## 📝 Changelog

### Version 2.0 (Current)
- ✅ Unified GUI with 7 tabs
- ✅ Refactored src/ into modules
- ✅ Organized experiments by chapter
- ✅ Chapter 3 experiments implemented
- ✅ Comprehensive documentation

### Version 1.0
- Initial implementation
- Separate GUI files
- Basic algorithms
