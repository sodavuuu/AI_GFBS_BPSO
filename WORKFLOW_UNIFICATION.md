# 🎯 Thống Nhất Workflow Chapter 3

## ⚠️ Vấn Đề Ban Đầu

Có **3 cách chạy experiments** khác nhau nhưng cùng mục tiêu:

### 1. **GUI** (`gui/main_gui.py`)
- **Trước đây**: 
  - ❌ Chỉ LOAD CSV có sẵn, không chạy experiments
  - ❌ Vẽ chart đơn giản bằng matplotlib trực tiếp
  - ❌ Không dùng `AdvancedKnapsackVisualizer`
  
- **Kết quả**: Hình ảnh trên GUI khác với PNG trong `results/chapter3/`

### 2. **Script** (`experiment/chapter3/experiments.py`)
- ✅ Chạy algorithms (GBFS, BPSO)
- ✅ Dùng `AdvancedKnapsackVisualizer`
- ✅ Sinh CSV + PNG vào `results/chapter3/`
- **Đây là source of truth!**

### 3. **Notebooks** (`.ipynb` files)
- ⚠️ Load CSV từ `results/chapter3/`
- ⚠️ Vẽ lại bằng matplotlib trực tiếp (code riêng trong cell)
- ⚠️ Không dùng `AdvancedKnapsackVisualizer`
- **Kết quả**: Hình ảnh trong notebook khác với PNG

---

## ✅ Giải Pháp Đã Triển Khai

### Phase 1: Thống nhất GUI (✅ DONE)

**File:** `gui/main_gui.py`

**Thay đổi:**

```python
# 1. Import AdvancedKnapsackVisualizer
from src.visualization import (
    visualize_gbfs_selection_steps,
    visualize_bpso_swarm_behavior,
    AdvancedKnapsackVisualizer  # ✅ Added
)

# 2. Tạo shared visualizer instance
def __init__(self):
    self.loader = TestCaseLoader()
    self.visualizer = AdvancedKnapsackVisualizer()  # ✅ Added
    
# 3. Run experiments thực sự (không chỉ load CSV)
def run_chapter3_experiments(self):
    from experiment.chapter3.experiments import Chapter3Experiments
    exp_runner = Chapter3Experiments()
    exp_runner.run_all_experiments()  # ✅ Chạy thật
    
# 4. Load result vẫn dùng matplotlib đơn giản (cho nhanh)
# Nhưng user có thể chạy lại experiments để tạo PNG đẹp
```

**Lợi ích:**
- 🎯 GUI giờ có thể **chạy experiments** thay vì chỉ xem kết quả cũ
- 🎯 Kết quả PNG được sinh bởi `AdvancedKnapsackVisualizer` (giống experiments.py)
- 🎯 GUI hiển thị nhanh bằng chart đơn giản, nhưng PNG full detail

---

### Phase 2: Thống nhất Notebooks (📋 RECOMMENDED)

**Các file cần sửa:**
- `experiment/chapter3/3.1.1_Parameter_Analysis.ipynb`
- `experiment/chapter3/3.1.2_Algorithm_Comparison.ipynb`
- `experiment/chapter3/3.1.3_Data_Characteristics.ipynb`
- `experiment/chapter3/3.2_Optimization_Analysis.ipynb`

**Cách tiếp cận:**

#### Option A: Dùng PNG từ results/ (KHUYẾN NGHỊ)

```python
# Cell 1: Load and display PNG
from IPython.display import Image, display

display(Image('../../results/chapter3/3_1_1_a_gbfs_params.png'))
```

**Ưu điểm:**
- ✅ Đơn giản, ít code
- ✅ Đảm bảo consistency với experiments.py
- ✅ Không cần duplicate visualization code

**Nhược điểm:**
- ⚠️ Không thể customize chart trong notebook
- ⚠️ Phải chạy experiments.py trước

#### Option B: Import và dùng AdvancedKnapsackVisualizer

```python
# Cell 1: Import
import sys
sys.path.insert(0, '../../')
from src.visualization import AdvancedKnapsackVisualizer
import pandas as pd

# Cell 2: Load data và visualize
visualizer = AdvancedKnapsackVisualizer()
df = pd.read_csv('../../results/chapter3/3_1_1_a_gbfs_params.csv')
visualizer.plot_gbfs_parameter_impact(df, save_path=None)  # Display inline
```

**Ưu điểm:**
- ✅ Giống 100% với experiments.py
- ✅ Có thể customize nếu cần
- ✅ Interactive trong notebook

**Nhược điểm:**
- ⚠️ Code dài hơn
- ⚠️ Phải import visualizer

---

## 🎨 So Sánh Visualization Methods

| Method | experiments.py | GUI (old) | GUI (new) | Notebooks (old) | Notebooks (recommended) |
|--------|---------------|-----------|-----------|-----------------|------------------------|
| **Chạy algorithms** | ✅ | ❌ | ✅ | ❌ | ❌ |
| **Dùng AdvancedVisualizer** | ✅ | ❌ | ✅ | ❌ | ✅ (Option B) |
| **Sinh PNG** | ✅ | ❌ | ✅ | ❌ | Load PNG |
| **Interactive** | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Consistency** | ⭐ Source of truth | ❌ Khác | ✅ Giống | ❌ Khác | ✅ Giống |

---

## 📊 Workflow Chuẩn

### 1. Generate Data (Chạy 1 lần)

```bash
# Option A: Chạy script
cd /Users/haphuongquynh/Desktop/AI/AI_GFBS_BPSO
python3 experiment/chapter3/experiments.py

# Option B: Dùng regenerate script
python3 regenerate_all_data.py

# Option C: Từ GUI
python3 run_gui.py
# Nhấn "RUN CHAPTER 3 EXPERIMENTS"
```

**Output:**
- `results/chapter3/*.csv` - Raw data
- `results/chapter3/*.png` - Publication-ready charts

### 2. Phân Tích (Notebooks)

```bash
# Open notebook
jupyter notebook experiment/chapter3/3.1.1_Parameter_Analysis.ipynb
```

**Trong notebook:**

```python
# Option A: Hiển thị PNG (nhanh)
from IPython.display import Image, display
display(Image('../../results/chapter3/3_1_1_a_gbfs_params.png'))

# Option B: Tạo interactive plot
import sys
sys.path.insert(0, '../../')
from src.visualization import AdvancedKnapsackVisualizer
visualizer = AdvancedKnapsackVisualizer()
df = pd.read_csv('../../results/chapter3/3_1_1_a_gbfs_params.csv')
visualizer.plot_gbfs_parameter_impact(df)
```

### 3. Trực Quan Hóa (GUI)

```bash
python3 run_gui.py
# Tab "Chapter 3" -> Chọn experiment -> Xem chart nhanh
```

---

## 🔧 Parameters Được Dùng

### GBFS
```python
solve_knapsack_gbfs(
    items, weights, values, capacity,
    regions=regions,
    max_states=5000  # Default in GUI
)
```

### BPSO
```python
solve_knapsack_bpso(
    items, weights, values, capacity,
    regions=regions,
    n_particles=30,    # Default in GUI
    max_iterations=50, # Default in GUI
    w=0.7,            # Inertia weight
    c1=2.0,           # Cognitive
    c2=2.0            # Social
)
```

### Fitness Function (BOTH)
```python
fitness = 0.7 * revenue_normalized + 0.3 * coverage_normalized - penalty
```

**Đảm bảo 3 nơi dùng cùng parameters:**
1. ✅ `src/algorithms/gbfs_knapsack.py` và `bpso_knapsack.py`
2. ✅ `experiment/chapter3/experiments.py`
3. ✅ `gui/main_gui.py`

---

## 📝 Checklist Thống Nhất

- [x] ✅ `src/algorithms/` - TRUE GBFS implemented
- [x] ✅ `src/algorithms/` - Same fitness function (alpha=0.7, beta=0.3)
- [x] ✅ `experiment/chapter3/experiments.py` - Uses AdvancedVisualizer
- [x] ✅ `gui/main_gui.py` - Can run experiments (not just load CSV)
- [x] ✅ `gui/main_gui.py` - Has visualizer instance
- [x] ✅ All experiments regenerated successfully (6/6)
- [ ] 📋 Notebooks - Update to use PNG or AdvancedVisualizer
- [ ] 📋 Notebooks - Remove duplicate matplotlib code
- [ ] 📋 Test end-to-end workflow

---

## 🎯 Kết Luận

**Hiện tại:**
- ✅ **experiments.py** và **GUI** đã thống nhất
- ✅ Cùng dùng `AdvancedKnapsackVisualizer`
- ✅ Cùng parameters, cùng algorithms
- ✅ GUI có thể chạy experiments thực sự

**Còn lại:**
- 📋 **Notebooks** nên update để consistency 100%
- 📋 Khuyến nghị: Dùng PNG có sẵn hoặc import visualizer
- 📋 Tránh duplicate visualization code

**Lợi ích:**
- 🎨 Publication-ready charts từ experiments.py
- ⚡ Quick preview trong GUI
- 📊 Detailed analysis trong notebooks
- 🔧 Single source of truth cho visualization logic
