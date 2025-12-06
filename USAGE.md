# 📖 Usage Guide

Comprehensive guide for using the Knapsack Solver GUI and running experiments.

---

## 🖥️ GUI Usage

### Starting the Application

```bash
python3 run_gui.py
```

### Interface Overview

The GUI is divided into two panels:

**Left Panel (25%)**:
- Problem Definition
- Test Case Selection
- Algorithm Parameters
- Action Buttons

**Right Panel (75%)**:
- 7 Visualization Tabs

---

## 📋 Step-by-Step Guide

### 1. Select Test Case

1. Use the **"Select Test Case"** dropdown
2. Choose from 13 available test cases
3. Problem info updates automatically
4. Items are displayed in the Problem tab

**Test Case Info Shows**:
- Number of items
- Capacity
- Number of regions
- Total value

### 2. Adjust Algorithm Parameters

#### GBFS Parameters
- **Max States**: Number of states to explore (1000-10000)
  - Higher = more thorough search
  - Default: 5000

#### BPSO Parameters
- **Particles**: Swarm size (10-100)
  - Higher = more exploration
  - Default: 30

- **Iterations**: Number of iterations (20-100)
  - Higher = better convergence
  - Default: 50

- **Inertia (w)**: Balance exploration/exploitation (0.4-0.9)
  - Lower = more exploitation
  - Higher = more exploration
  - Default: 0.7

### 3. Run Algorithms

Click **"RUN ALL ALGORITHMS"** button

- Progress bar appears
- Status bar shows current algorithm
- All 3 algorithms run sequentially
- Results populate automatically

**Note**: Algorithms run in order:
1. GBFS (fastest)
2. BPSO (moderate)
3. DP (slowest for large problems)

### 4. View Results

Switch between tabs to see different visualizations:

#### Tab 1: Problem
- **Interactive scatter plot** (Weight vs Value)
- **Click items** to select/deselect manually
- Green = selected, Gray = not selected
- Use "Clear Selection" to reset

#### Tab 2: GBFS Flow
- **4 plots**:
  1. Selection order with arrows
  2. Value of each selected item
  3. Cumulative weight vs capacity
  4. Top 20 items by ratio

#### Tab 3: BPSO Swarm
- **3 plots**:
  1. Convergence (Best vs Avg fitness)
  2. Swarm diversity over iterations
  3. Solution space with selected items

#### Tab 4: Comparison
- **2 plots**:
  1. Solution quality (total value)
  2. Execution time
- Compares all 3 algorithms

#### Tab 5: Regional
- **4 plots**:
  1. Regional distribution comparison
  2. Diversity scores (Shannon entropy)
  3. All items colored by region
  4. Selected items by best algorithm

**Note**: Only shows if test case has regional data

#### Tab 6: Details
- **Table showing**:
  - Item ID
  - Weight
  - Value
  - Region
  - Value/Weight ratio
  - Algorithm that selected it

#### Tab 7: Chapter 3
- **Dropdown**: Select experiment type
- **5 experiments**:
  - 3.1.1.a: GBFS Parameters
  - 3.1.1.b: BPSO Swarm Size
  - 3.1.1.c: BPSO Iterations
  - 3.1.2: Algorithm Comparison
  - 3.1.3: Data Characteristics

**Note**: Requires CSV files in `results/chapter3/`

---

## 🧪 Running Experiments

### Chapter 3 Experiments

```bash
cd experiment/chapter3
python3 experiments.py
```

### What It Does

1. **Loads test cases** from `data/test_cases/`
2. **Runs experiments**:
   - 3.1.1.a: GBFS with different max_states
   - 3.1.1.b: BPSO with different swarm sizes
   - 3.1.1.c: BPSO with different iterations
   - 3.1.2: Compare algorithms on all test cases
   - 3.1.3: Analyze data characteristics
3. **Saves results** to `results/chapter3/*.csv`
4. **Generates visualizations** (optional)

### Experiment Options

Edit `experiments.py` to customize:

```python
# Parameter ranges
MAX_STATES_VALUES = [1000, 2000, 3000, 5000, 10000]
SWARM_SIZES = [10, 20, 30, 50, 100]
ITERATIONS = [20, 30, 50, 70, 100]

# Test runs per configuration
N_RUNS = 10  # Run each config 10 times for statistical validity
```

### Expected Runtime

- **3.1.1.a** (GBFS params): ~2-3 minutes
- **3.1.1.b** (BPSO swarm): ~5-10 minutes
- **3.1.1.c** (BPSO iterations): ~10-15 minutes
- **3.1.2** (Comparison): ~15-20 minutes
- **3.1.3** (Data chars): ~10-15 minutes

**Total**: ~45-60 minutes for all experiments

---

## 💻 Programmatic Usage

### Basic Example

```python
from src.algorithms import solve_knapsack_gbfs, solve_knapsack_bpso, solve_knapsack_dp

# Define problem
items = ['Laptop', 'Phone', 'Tablet', 'Camera', 'Headphones']
weights = [15, 8, 10, 12, 5]
values = [2000, 1500, 1000, 800, 300]
capacity = 25

# Solve with GBFS
result = solve_knapsack_gbfs(items, weights, values, capacity)

print(f"Selected: {result['selected_items']}")
print(f"Total Value: {result['total_value']}")
print(f"Total Weight: {result['total_weight']}")
print(f"Time: {result['execution_time']:.4f}s")
```

### Advanced Example with All Algorithms

```python
from src.algorithms import solve_knapsack_gbfs, solve_knapsack_bpso, solve_knapsack_dp
import time

# Problem setup
items = [f'Item_{i}' for i in range(50)]
weights = [random.randint(5, 30) for _ in range(50)]
values = [random.randint(50, 500) for _ in range(50)]
capacity = 250

# Run all algorithms
algorithms = {
    'GBFS': lambda: solve_knapsack_gbfs(items, weights, values, capacity, max_states=5000),
    'BPSO': lambda: solve_knapsack_bpso(items, weights, values, capacity, 
                                        n_particles=30, max_iterations=50, w=0.7),
    'DP': lambda: solve_knapsack_dp(items, weights, values, capacity)
}

results = {}
for name, algo in algorithms.items():
    start = time.time()
    result = algo()
    result['execution_time'] = time.time() - start
    results[name] = result
    
    print(f"{name}:")
    print(f"  Value: {result['total_value']}")
    print(f"  Weight: {result['total_weight']}/{capacity}")
    print(f"  Items: {len(result['selected_items'])}")
    print(f"  Time: {result['execution_time']:.4f}s")
    print()

# Find best solution
best_algo = max(results, key=lambda x: results[x]['total_value'])
print(f"Best: {best_algo} with value {results[best_algo]['total_value']}")
```

### Loading Test Cases

```python
from src.utils import TestCaseLoader

# Initialize loader
loader = TestCaseLoader()

# List all test cases
test_cases = loader.list_test_cases()
print(f"Available: {len(test_cases)} test cases")

# Load specific test case
test_case = loader.load_test_case("Size Small 30")

# Access data
items = test_case['items']
weights = test_case['weights']
values = test_case['values']
capacity = test_case['capacity']
metadata = test_case['metadata']

print(f"Loaded: {metadata['name']}")
print(f"Items: {len(items)}")
print(f"Capacity: {capacity}")
```

---

## 🎨 Customizing Visualizations

### Matplotlib Style

The GUI uses Matplotlib for all plots. You can customize:

```python
# In gui/main_gui.py
import matplotlib.pyplot as plt

# Change style
plt.style.use('seaborn')  # or 'ggplot', 'bmh', etc.

# Adjust figure DPI
self.gbfs_fig = Figure(figsize=(12, 9), dpi=150)  # Higher DPI
```

### Colors

Algorithm colors are defined in visualization functions:

```python
colors = {
    'GBFS': '#27ae60',  # Green
    'BPSO': '#3498db',  # Blue
    'DP': '#e74c3c'     # Red
}
```

---

## ⚙️ Configuration

### Test Case Directory

Default: `data/test_cases/`

To change:

```python
# In src/utils/test_case_loader.py
self.test_cases_dir = Path('your/custom/path')
```

### Results Directory

Default: `results/chapter3/`

To change experiment output:

```python
# In experiment/chapter3/experiments.py
RESULTS_DIR = Path('your/custom/path')
```

---

## 🐛 Troubleshooting

### GUI Won't Start

**Issue**: `ModuleNotFoundError`

**Solution**:
```bash
pip install -r requirements.txt
```

### Font Warning

**Issue**: "Missing font family 'Segoe UI'"

**Solution**: Already using Arial. Ignore warning or install Segoe UI font.

### No Results in Chapter 3 Tab

**Issue**: "File not found"

**Solution**:
```bash
cd experiment/chapter3
python3 experiments.py
```

### Slow Performance

**Issue**: GUI laggy with large test cases

**Solutions**:
- Reduce max_states for GBFS
- Reduce particles/iterations for BPSO
- Use smaller test cases
- Close other applications

---

## 📊 Understanding Results

### Solution Quality

**% of Optimal**: How close to DP solution
- 100% = Optimal
- 90-99% = Very good
- 80-89% = Good
- <80% = May need parameter tuning

### Execution Time

Typical times (Size Medium 50):
- GBFS: 0.00001 - 0.0001 seconds
- BPSO: 0.01 - 0.02 seconds
- DP: 0.009 - 0.01 seconds

### Convergence

BPSO convergence plot shows:
- **Rapid initial drop**: Good exploration
- **Gradual improvement**: Good exploitation
- **Plateau**: Convergence achieved

**Diversity plot**:
- **High initial diversity**: Good exploration
- **Decreasing diversity**: Moving toward solution
- **Low final diversity**: Swarm converged

---

## 💡 Tips & Best Practices

### For Best Results

1. **Start with defaults**: Test with default parameters first
2. **Run multiple times**: Especially for BPSO (stochastic)
3. **Compare on same test case**: Fair comparison
4. **Check % optimal**: Validate solution quality
5. **Consider trade-offs**: Speed vs quality

### Parameter Tuning

**GBFS max_states**:
- Start: 5000
- Increase if: Need better solution
- Decrease if: Too slow

**BPSO particles**:
- Start: 30
- Increase if: Stuck in local optima
- Decrease if: Too slow

**BPSO iterations**:
- Start: 50
- Increase if: Not converged
- Decrease if: Already converged early

**BPSO inertia (w)**:
- 0.9: More exploration (early phase)
- 0.7: Balanced (default)
- 0.4: More exploitation (fine-tuning)

### Interpreting Regional Analysis

**Shannon Entropy**:
- High (>1.5): Very diverse
- Medium (1.0-1.5): Moderate diversity
- Low (<1.0): Concentrated in few regions

**Good regional diversity**: 
- Select items from multiple regions
- Balance value and diversity

---

## 📚 Further Reading

- **README.md**: Project overview
- **experiment/chapter3/README.md**: Experiment details
- **SECTION_3_2_GUIDE.md**: Section 3.2 guide
- Source code documentation: Inline comments and docstrings

---

## ❓ FAQ

**Q: Which algorithm should I use?**

A: Depends on your needs:
- **Speed priority**: GBFS
- **Quality priority**: DP (for small-medium problems)
- **Large problems**: BPSO or GBFS
- **Research/Analysis**: All three for comparison

**Q: How to add new test cases?**

A: Add CSV file to `data/test_cases/` with columns:
- Name, Quantity (weight), Total (value), Region (optional)

**Q: Can I use with real data?**

A: Yes! Format your data as CSV with required columns.

**Q: How to export results?**

A: Click "EXPORT RESULTS" button in GUI or access `results/` directory.

**Q: Can I modify algorithms?**

A: Yes! Edit files in `src/algorithms/`. Follow existing function signatures.

---

## 🔗 Resources

- **GitHub**: https://github.com/sodavuuu/AI_GFBS_BPSO
- **Issues**: Report bugs or request features
- **Documentation**: Check README.md and source code

---

**Last Updated**: December 2025
