# 🎒 Knapsack Problem Solver

**3 Algorithms**: GBFS + BPSO + DP | **13 Test Cases** | **Interactive GUI** | **Step-by-Step Visualization**

---

## 🚀 Quick Start

```bash
# 1. Install
./install_dependencies.sh

# 2. Test
python3 test_quick.py

# 3. Run GUI
python3 knapsack_solver_gui.py

# 4. Run notebooks
cd experiment/ && jupyter notebook

# 5. Run experiments
cd experiment/ && python3 chapter3_experiments_v2.py --experiment all
```

---

## 🔧 3 Algorithms

| Algorithm | Type | Speed | Quality | Use Case |
|-----------|------|-------|---------|----------|
| **GBFS** | Heuristic | ⚡⚡⚡ | 🎯🎯 | Quick good solution |
| **BPSO** | Metaheuristic | ⚡⚡ | 🎯🎯🎯 | Explore solution space |
| **DP** | Exact | ⚡ | 🎯🎯🎯🎯 | Optimal solution |

---

## 📊 13 Test Cases

- **Size**: Small (30) / Medium (50) / Large (70)
- **Region**: 1/2/3 regions
- **Category**: Clothing / Electronics / Food / Furniture
- **Characteristics**: High Correlation / High Value / Low Correlation

---

## 💻 Usage

```python
from src.test_case_loader import TestCaseLoader
from src.gbfs_knapsack import solve_knapsack_gbfs

loader = TestCaseLoader()
tc = loader.load_test_case('Size Medium 50')

result = solve_knapsack_gbfs(tc['items'], tc['weights'], tc['values'], tc['capacity'])
print(f"Value: {result['total_value']}")
```

---

## �� Structure

```
src/            → gbfs_knapsack.py, bpso_knapsack.py, dp_knapsack.py
experiment/     → 1. Parameter.ipynb, 2. Algo.ipynb, 3. Data.ipynb, 4. StepByStep.ipynb
data/test_cases/→ 13 CSV files
results/        → CSV + PNG outputs
```

📘 **Full docs**: PROJECT_STRUCTURE.md

---

## ⚠️ Common Issues

```python
# ❌ WRONG
loader.load_test_case('Size_Medium_50')  # underscore
print(tc['name'])  # wrong key

# ✅ CORRECT  
loader.load_test_case('Size Medium 50')  # space
print(tc['test_case_name'])  # correct key
```

---

**Status**: ✅ Ready | **Updated**: 2025-12-06
