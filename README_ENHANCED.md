# 🎯 Multi-Objective Knapsack Solver - Inspired by GA_TSP

Giải quyết bài toán **0/1 Knapsack** với 2 mục tiêu:
- **f₁**: Maximize revenue (total value)
- **f₂**: Maximize regional diversity

So sánh 3 thuật toán: **GBFS**, **BPSO**, **DP**

---

## 🚀 Quick Start

### 1. Cài Đặt

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies (if needed)
pip install -r requirements.txt
```

### 2. Chạy GUI

#### GUI Cơ Bản (Version 2)
```bash
python gui_app_v2.py
```
- Simple 2-panel layout
- Basic convergence plots
- Algorithm comparison

#### GUI Nâng Cao (Enhanced - Recommended)
```bash
python gui_app_enhanced.py
```
- 4 tabs: Problem Visualization, Convergence, Comparison, Details
- Advanced charts học từ GA_TSP
- Real-time parameter tuning
- Problem-specific visualization

### 3. Chạy Experiments (Cho Chương 3)

```bash
# Chạy tất cả experiments
python experiment/chapter3_experiments_v2.py --experiment all

# Hoặc chạy từng phần
python experiment/chapter3_experiments_v2.py --experiment 3.1.1a  # GBFS parameters
python experiment/chapter3_experiments_v2.py --experiment 3.1.1b  # BPSO swarm size
python experiment/chapter3_experiments_v2.py --experiment 3.1.2   # Algorithm comparison
python experiment/chapter3_experiments_v2.py --experiment 3.1.3   # Data characteristics
```

**Kết quả:**
- CSV files: `results/chapter3/*.csv`
- PNG charts: `results/chapter3/*.png`

---

## 📂 Project Structure

```
AI_GFBS_BPSO/
├── src/
│   ├── gbfs_knapsack.py              # GBFS algorithm
│   ├── bpso_knapsack.py              # BPSO algorithm
│   ├── dp_knapsack.py                # Dynamic Programming
│   ├── test_case_loader.py           # Load 13 test cases
│   ├── visualizer.py                 # Basic visualizations
│   └── advanced_visualizer.py        # Advanced charts (GA_TSP style) ⭐NEW
│
├── data/test_cases/
│   ├── size_small_30.csv             # 30 items
│   ├── size_medium_50.csv            # 50 items (MAIN TEST)
│   ├── size_large_70.csv             # 70 items
│   ├── region_1regions_medium.csv    # Single region
│   ├── region_3regions_medium.csv    # Multi-region
│   ├── data_low_correlation_medium.csv
│   ├── data_high_correlation_medium.csv
│   └── ... (13 test cases total)
│
├── experiment/
│   ├── chapter3_experiments.py       # Original experiments
│   └── chapter3_experiments_v2.py    # Organized by 3.1.1, 3.1.2, 3.1.3 ⭐NEW
│
├── results/chapter3/                 # Experiment outputs ⭐NEW
│   ├── 3_1_1_a_gbfs_params.csv/.png
│   ├── 3_1_1_b_bpso_swarm_size.csv/.png
│   ├── 3_1_2_comparison_*.csv/.png
│   └── 3_1_3_data_characteristics.csv/.png
│
├── gui_app.py                        # Original GUI (1295 lines)
├── gui_app_v2.py                     # Simplified GUI (600 lines)
├── gui_app_enhanced.py               # Advanced GUI (650 lines) ⭐NEW
│
└── SECTION_3_2_GUIDE.md              # Guide for writing thesis section 3.2 ⭐NEW
```

---

## 🎓 Test Cases (13 Total)

### SIZE Tests (3)
- `Size Small 30` - 30 items
- `Size Medium 50` - 50 items ⭐ **Main Test Case**
- `Size Large 70` - 70 items

### REGIONAL Tests (3)
- `Region 1Regions Medium` - Items from 1 region
- `Region 2Regions Medium` - Items from 2 regions
- `Region 3Regions Medium` - Items from 3 regions

### CATEGORY Tests (4)
- `Category Clothing Medium`
- `Category Electronics Medium`
- `Category Food Medium`
- `Category Furniture Medium`

### DATA CHARACTERISTIC Tests (3)
- `Data Low Correlation Medium` - Weight & Value uncorrelated
- `Data High Correlation Medium` - Weight ≈ Value (hard case)
- `Data High Value Medium` - Large value spread

---

## 🔬 Algorithms

### 1. GBFS (Greedy Best-First Search)
**Idea:** Select items with highest value/weight ratio

**Parameters:**
- `max_states`: Depth limit (default: 5000)

**Pros:**
- Very fast (0.001-0.01s)
- Good for real-time

**Cons:**
- Local optima (~85% optimal)
- No backtracking

### 2. BPSO (Binary Particle Swarm Optimization)
**Idea:** Swarm intelligence with social learning

**Parameters:**
- `n_particles`: Swarm size (default: 30)
- `max_iterations`: Number of iterations (default: 50)
- `w`: Inertia weight (default: 0.7)
- `c1`: Cognitive coefficient (default: 1.5)
- `c2`: Social coefficient (default: 1.5)

**Pros:**
- Balance quality/speed (~92% optimal)
- Avoid local optima
- Track convergence

**Cons:**
- Slower than GBFS (0.5-2s)
- Stochastic (need multiple runs)

### 3. DP (Dynamic Programming)
**Idea:** Optimal solution by exhaustive search

**Parameters:** None (deterministic)

**Pros:**
- 100% optimal
- Guaranteed solution

**Cons:**
- Slow (1-10s for 50-70 items)
- Not scalable (O(nC))

---

## 📊 Learning from GA_TSP

### What We Learned

#### 1. Visualization Style
- **GA_TSP:** Cities on map, route visualization, convergence plots
- **Knapsack:** Items scatter (weight vs value), capacity pie chart, regional distribution

#### 2. Experiment Organization
**GA_TSP Structure:**
```
3.1.1. Parameter Analysis (Population, Mutation, Generations)
3.1.2. Algorithm Comparison (Mutations, Crossovers, Selections)
3.1.3. Data Variants (Different city sets)
```

**Knapsack Adaptation:**
```
3.1.1. Parameter Analysis
   a. GBFS - Max States
   b. BPSO - Swarm Size
   c. BPSO - Iterations
   d. BPSO - Inertia Weight

3.1.2. Algorithm Comparison
   - GBFS vs BPSO vs DP
   - Quality vs Speed trade-off
   - Convergence analysis

3.1.3. Data Characteristics
   - Correlation impact
   - Value spread effects
   - Regional diversity
```

#### 3. Chart Types

| GA_TSP Chart | Knapsack Equivalent |
|--------------|---------------------|
| Population Size vs Fitness | Max States / Swarm Size vs Value |
| Convergence over Generations | Convergence over Iterations |
| Route on Map | Items Selection Map |
| Distance Optimization | Capacity Utilization |
| City Distribution | Regional Diversity |

---

## 📈 Key Features (New)

### Advanced Visualizer (`src/advanced_visualizer.py`)

```python
from src.advanced_visualizer import AdvancedKnapsackVisualizer

visualizer = AdvancedKnapsackVisualizer()

# 1. Parameter Impact (như GA_TSP analyze population size)
visualizer.plot_gbfs_parameter_impact(results_df)
visualizer.plot_bpso_parameter_impact(results_df, 'n_particles')

# 2. Algorithm Comparison (như GA_TSP compare mutations)
visualizer.plot_algorithm_comparison_detailed(gbfs, bpso, dp)

# 3. Data Characteristics (như GA_TSP test different cities)
visualizer.plot_data_characteristics_impact(results_dict)

# 4. Solution Map (thay map của TSP)
visualizer.plot_knapsack_solution_map(solution, items_df)
```

### Chapter 3 Experiments (`experiment/chapter3_experiments_v2.py`)

```python
from experiment.chapter3_experiments_v2 import Chapter3Experiments

exp = Chapter3Experiments()

# Run specific experiments
exp.experiment_3_1_1_a_gbfs_parameters()      # GBFS max_states analysis
exp.experiment_3_1_1_b_bpso_swarm_size()      # BPSO particles impact
exp.experiment_3_1_2_algorithm_comparison_single()  # Detailed comparison
exp.experiment_3_1_3_data_characteristics()   # Data impact

# Or run all
exp.run_all_experiments()
```

### Enhanced GUI (`gui_app_enhanced.py`)

**4 Tabs:**
1. **Problem Visualization** - Item distribution, như map của GA_TSP
2. **BPSO Convergence** - Real-time fitness tracking
3. **Algorithm Comparison** - Side-by-side comparison
4. **Solution Details** - Results table

**Features:**
- Problem definition display
- Test case info preview
- Advanced parameter controls
- Real-time visualization
- Export-ready charts

---

## 🎯 Usage for Thesis Section 3.2

### Step 1: Run Experiments

```bash
python experiment/chapter3_experiments_v2.py --experiment all
```

This generates:
- `results/chapter3/*.csv` - Data tables
- `results/chapter3/*.png` - Charts ready for report

### Step 2: Analyze Results

See `SECTION_3_2_GUIDE.md` for detailed guide:
- How to interpret each chart
- What to write for each subsection
- Comparison with GA_TSP
- Tips for report writing

### Step 3: Insert Charts

Charts are organized by section:
```
3.1.1.a → 3_1_1_a_gbfs_params.png
3.1.1.b → 3_1_1_b_bpso_swarm_size.png
3.1.1.c → 3_1_1_c_bpso_iterations.png
3.1.1.d → 3_1_1_d_bpso_w.png
3.1.2   → 3_1_2_comparison_*.png
3.1.3   → 3_1_3_data_characteristics.png
```

---

## 📝 Documentation

### Main Files
- `README.md` - This file
- `SECTION_3_2_GUIDE.md` - Detailed guide for writing thesis section 3.2
- `GUI_REDESIGN_SUMMARY.md` - GUI design principles
- `QUICKSTART.md` - Basic usage guide

### Key Concepts

**Multi-Objective Fitness:**
```
Fitness = 0.7 × (normalized_value) + 0.3 × (regional_diversity)

where:
- normalized_value = total_value / max_possible_value
- regional_diversity = unique_regions / total_regions
```

**Test Case Naming:**
- Use SPACES not underscores: `"Size Medium 50"` not `"Size_Medium_50"`
- Loaded via: `loader.load_test_case("Size Medium 50")`

---

## 🔧 Troubleshooting

### GUI không hiển thị charts?
- Đảm bảo đã install matplotlib: `pip install matplotlib seaborn`
- Check virtual environment: `which python` should show `.venv/bin/python`

### Experiments chạy chậm?
- Giảm số runs: `range(5)` → `range(3)` trong experiments
- Giảm BPSO parameters: `n_particles=30`, `max_iterations=50`

### Test case not found?
- Check tên test case: Phải có SPACES: `"Size Medium 50"`
- Verify CSV exists: `ls data/test_cases/`

---

## 🎉 Improvements from GA_TSP Learning

### Before (gui_app.py)
- ❌ 1295 lines, complex 3-panel layout
- ❌ Basic convergence plots only
- ❌ No parameter impact visualization
- ❌ No organized experiments

### After (gui_app_enhanced.py + advanced_visualizer.py)
- ✅ 650 lines GUI + 900 lines visualizer
- ✅ 4-tab layout with problem visualization
- ✅ Parameter impact charts (like GA_TSP)
- ✅ Algorithm comparison (like GA_TSP)
- ✅ Data characteristics analysis (like GA_TSP)
- ✅ Experiments organized by thesis sections
- ✅ Auto-generate PNG + CSV for report

### Key Takeaways
1. **Layout**: 25% controls, 75% visualization (GA_TSP: 30/70)
2. **Charts**: Multi-plot figures with annotations
3. **Experiments**: Systematic parameter sweep
4. **Comparison**: Side-by-side algorithm analysis
5. **Problem viz**: Adapt TSP map → Knapsack item map

---

## 📧 Next Steps

1. ✅ **Run experiments:** `python experiment/chapter3_experiments_v2.py --experiment all`
2. ✅ **Review charts:** Check `results/chapter3/*.png`
3. ✅ **Write analysis:** Follow `SECTION_3_2_GUIDE.md`
4. ⏳ **Screenshot GUI:** For problem introduction
5. ⏳ **Create tables:** Summarize CSV results

---

## 🙏 Credits

**Inspired by:**
- GA_TSP project (Parameter analysis, Convergence plots, Map visualization)
- Research papers (Kennedy & Eberhart 1997, Martello & Toth 1990, Pisinger 2005)

**Technologies:**
- Python 3.11
- PyQt5 (GUI)
- Matplotlib, Seaborn (Visualization)
- NumPy, Pandas (Data processing)

---

**Author:** Ha Phuong Quynh  
**Date:** December 2024  
**Project:** Multi-Objective Knapsack Solver (GBFS vs BPSO vs DP)
