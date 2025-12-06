# 🎒 Multi-Objective Knapsack Solver

> Giải quyết bài toán Knapsack đa mục tiêu với GBFS (Greedy Best-First Search) và BPSO (Binary Particle Swarm Optimization)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Mục Lục

- [Giới Thiệu](#-giới-thiệu)
- [Cài Đặt](#-cài-đặt)
- [Sử Dụng](#-sử-dụng)
- [Cấu Trúc Dự Án](#-cấu-trúc-dự-án)
- [Thuật Toán](#-thuật-toán)
- [Experiments Chapter 3](#-experiments-chapter-3)

---

## 🎯 Giới Thiệu

**Bài toán:** Multi-Objective 0/1 Knapsack Problem

**Mục tiêu:**
1. **Maximize Revenue** - Tối đa hóa tổng giá trị
2. **Maximize Regional Coverage** - Tối đa hóa đa dạng vùng miền

**Thuật toán:**
- **GBFS** - Greedy Best-First Search (Deterministic, Fast)
- **BPSO** - Binary Particle Swarm Optimization (Stochastic, Global Search)

**Fitness Function (Unified):**
```python
fitness = 0.7 * revenue_normalized + 0.3 * coverage_normalized - penalty
```

---

## 🚀 Cài Đặt

```bash
# 1. Clone repository
git clone https://github.com/sodavuuu/AI_GFBS_BPSO.git
cd AI_GFBS_BPSO

# 2. Cài đặt dependencies
pip install -r requirements.txt
```

**Requirements:** Python 3.8+, PyQt5, matplotlib, pandas, numpy

---

## 💻 Sử Dụng

### 🎯 ENTRY POINT DUY NHẤT: `main.py`

```bash
# Chạy GUI (default)
python3 main.py

# Chạy experiments
python3 main.py --experiments

# Regenerate data
python3 main.py --regenerate
```

### 🖥️ GUI Mode

```bash
python3 main.py --gui
```

**Chức năng:**
- Load test cases (13 bộ test)
- Chạy GBFS/BPSO với parameters tùy chỉnh
- Visualize real-time
- So sánh algorithms
- Chạy Chapter 3 Experiments

### 📊 Experiments Mode

```bash
python3 main.py --experiments
```

**Menu:**
1. GBFS Parameter Analysis
2. BPSO Swarm Size Analysis
3. BPSO Iterations Analysis
4. Algorithm Comparison (Single)
5. Algorithm Comparison (All 13 cases)
6. Data Characteristics Analysis
7. **Run ALL**

**Output:** `results/chapter3/*.csv`, `*.png`

---

## 📁 Cấu Trúc Dự Án

```
AI_GFBS_BPSO/
│
├── main.py                      # 🎯 ENTRY POINT DUY NHẤT
│
├── src/                         # Core algorithms
│   ├── algorithms/
│   │   ├── gbfs_knapsack.py    # TRUE GBFS
│   │   └── bpso_knapsack.py    # Binary PSO
│   ├── utils/
│   │   └── test_case_loader.py
│   └── visualization/
│       └── advanced_visualizer.py  # Shared visualizer
│
├── gui/
│   └── main_gui.py             # PyQt5 interface
│
├── experiment/chapter3/
│   ├── experiments.py          # Experiment runner
│   ├── 3.1.1_Parameter_Analysis.ipynb
│   ├── 3.1.2_Algorithm_Comparison.ipynb
│   ├── 3.1.3_Data_Characteristics.ipynb
│   └── 3.2_Optimization_Analysis.ipynb
│
├── data/test_cases/            # 13 CSV test files
├── results/chapter3/           # Experiment outputs
├── README.md
├── WORKFLOW_UNIFICATION.md     # Architecture notes
└── requirements.txt
```

---

## 🧠 Thuật Toán

### GBFS (Greedy Best-First Search)

✅ Deterministic (std ≈ 0)  
✅ Fast (< 50ms)  
⚠️ Local optima  

```python
from src.algorithms import solve_knapsack_gbfs
result = solve_knapsack_gbfs(items, weights, values, capacity, max_states=5000)
```

### BPSO (Binary Particle Swarm Optimization)

✅ Global search  
⚠️ Stochastic (variance > 0)  
⚠️ Slower  

```python
from src.algorithms import solve_knapsack_bpso
result = solve_knapsack_bpso(items, weights, values, capacity, n_particles=30, max_iterations=50)
```

---

## 🔬 Experiments Chapter 3

### 3.1.1. Parameter Analysis
- **GBFS:** Max states (converges at 7000)
- **BPSO:** Swarm size (best: 70-100), Iterations (improves with more)

### 3.1.2. Algorithm Comparison
- **Single case:** GBFS deterministic, BPSO variance
- **All 13 cases:** GBFS wins 8/13, BPSO wins 5/13

### 3.1.3. Data Characteristics
- Low/high correlation, value spread, regional diversity
- GBFS stable, BPSO sensitive to structure

**Files:** `results/chapter3/*.csv`, `*.png`

---

## 📊 Notebooks

```bash
cd experiment/chapter3
jupyter notebook
```

**Notebooks sử dụng `AdvancedKnapsackVisualizer`** để đảm bảo consistency với experiments.py và GUI.

---

## 🎓 Khuyến Nghị

**Dùng GBFS khi:**
- Cần deterministic
- Cần fast
- Medium complexity

**Dùng BPSO khi:**
- Escape local optima
- Complex constraints
- Chấp nhận variance

---

## 📖 Documentation

- **README.md** - Usage guide (file này)
- **WORKFLOW_UNIFICATION.md** - Architecture & workflow

---

## 👥 Contributors

**Hà Phương Quỳnh**  
Repository: [sodavuuu/AI_GFBS_BPSO](https://github.com/sodavuuu/AI_GFBS_BPSO)

---

**Made with ❤️ for Multi-Objective Optimization Research**
