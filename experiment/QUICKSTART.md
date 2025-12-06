# 🚀 QUICK START GUIDE - EXPERIMENT NOTEBOOKS

## ⚠️ Lỗi thường gặp và cách fix

### Lỗi 1: `ModuleNotFoundError: No module named 'numpy'`

**Nguyên nhân:** Chưa cài đặt dependencies

**Fix:**
```bash
# Về thư mục gốc project
cd /Users/haphuongquynh/Desktop/AI/AI_GFBS_BPSO

# Cài đặt dependencies
pip3 install -r requirements.txt
```

---

### Lỗi 2: `FileNotFoundError: test_cases_summary.csv not found`

**Nguyên nhân:** Chưa generate test cases

**Fix:**
```bash
# Generate test cases
python3 src/data_generator.py
```

---

### Lỗi 3: `NameError: name 'test_case' is not defined`

**Nguyên nhân:** Chạy cells không theo thứ tự hoặc cell setup bị lỗi

**Fix:** 
- Restart kernel: `Kernel > Restart & Clear Output`
- Chạy lại từ đầu: `Cell > Run All`

---

## ✅ CÁCH CHẠY ĐÚNG

### Bước 1: Setup môi trường
```bash
cd /Users/haphuongquynh/Desktop/AI/AI_GFBS_BPSO

# Install packages
pip3 install numpy pandas matplotlib seaborn jupyter scikit-learn

# Generate test data
python3 src/data_generator.py

# Generate experiment results
cd experiment
python3 chapter3_experiments_v2.py
```

### Bước 2: Start Jupyter
```bash
cd experiment
jupyter notebook
```

### Bước 3: Chạy notebooks theo thứ tự

**Option A: Chạy từ scratch (chậm, ~10-15 phút)**
- Open `1. Parameter.ipynb`
- `Kernel > Restart & Run All`
- Chờ tất cả cells chạy xong
- Results sẽ được save vào `results/chapter3/`

**Option B: Load từ CSV (NHANH, ~1 giây) ✅ RECOMMENDED**
- Open `2_Algo_FIXED.ipynb`
- `Kernel > Restart & Run All`
- Chỉ load và visualize, không chạy algorithms

---

## 📂 Notebooks nào nên dùng?

| Notebook | Nên dùng? | Lý do |
|----------|-----------|-------|
| `1. Parameter.ipynb` | ⚠️ CẦN FIX | Có lỗi, cần chạy từ scratch |
| `2. Algo.ipynb` | ❌ KHÔNG | Cũ, có lỗi |
| `2_Algo_FIXED.ipynb` | ✅ DÙNG | Load CSV, nhanh, đẹp |
| `3. Data.ipynb` | ❌ KHÔNG | Cũ, có lỗi |
| `3_Data_FIXED.ipynb` | ✅ DÙNG | Load CSV, nhanh, đẹp |
| `4. StepByStep.ipynb` | ⚠️ | Cần update |

---

## 🔧 Fix Notebook `1. Parameter.ipynb`

Notebook này cần chạy experiments từ đầu. Nếu gặp lỗi:

### Fix 1: Import errors
Đảm bảo cell setup chạy thành công:
```python
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, Markdown, HTML

from src.gbfs_knapsack import solve_knapsack_gbfs
from src.bpso_knapsack import solve_knapsack_bpso
from src.dp_knapsack import solve_knapsack_dp
from src.test_case_loader import TestCaseLoader
from src.advanced_visualizer import AdvancedKnapsackVisualizer
```

### Fix 2: Test case loader
Đảm bảo đã generate test cases:
```bash
python3 src/data_generator.py
```

### Fix 3: NameError
Chạy lại từ đầu:
- `Kernel > Restart & Clear Output`
- `Cell > Run All`

---

## 🎯 RECOMMENDED WORKFLOW

### Cho Academic Report (NHANH):

1. **Generate results một lần:**
```bash
cd experiment
python3 chapter3_experiments_v2.py
# Chờ ~5 phút, tạo tất cả CSV files
```

2. **Dùng notebooks FIXED:**
   - `2_Algo_FIXED.ipynb` - Algorithm comparison
   - `3_Data_FIXED.ipynb` - Data characteristics
   
3. **Export figures:**
   - Figures tự động save vào `results/chapter3/`
   - Format: PNG, 300 DPI
   - Ready cho báo cáo

### Cho Deep Analysis:

1. **Chạy `1. Parameter.ipynb`**
   - Takes ~10-15 minutes
   - Generates parameter analysis với nhiều runs
   - Interactive exploration

2. **Modify parameters:**
   - Thay đổi `max_states_values`, `swarm_sizes`, `max_iterations_list`
   - Re-run để test configurations khác

---

## 📊 Expected Results Location

Sau khi chạy xong:
```
results/chapter3/
├── 3_1_1_a_gbfs_params.csv              ✅ From notebook 1
├── 3_1_1_a_gbfs_params.png              ✅ Visualization
├── 3_1_1_b_bpso_swarm_size.csv         ✅ From notebook 1
├── 3_1_1_b_bpso_swarm_size.png         ✅ Visualization
├── 3_1_1_c_bpso_iterations.csv         ✅ From notebook 1
├── 3_1_2_comparison_Size_Medium_50.csv ✅ From chapter3_experiments_v2.py
├── 3_1_2_comparison_visualization.png  ✅ From notebook 2_FIXED
├── 3_1_3_data_characteristics.csv      ✅ From chapter3_experiments_v2.py
└── 3_1_3_data_visualization.png        ✅ From notebook 3_FIXED
```

---

## 💡 Tips

1. **Luôn restart kernel** trước khi chạy notebook lần đầu
2. **Chạy Cell > Run All** thay vì chạy từng cell
3. **Đợi cell chạy xong** trước khi chạy cell tiếp theo
4. **Check console output** để thấy progress
5. **Dùng notebooks _FIXED** để tiết kiệm thời gian

---

## 🆘 Still Having Issues?

### Check list:
- [ ] Installed all dependencies (`pip3 install -r requirements.txt`)
- [ ] Generated test cases (`python3 src/data_generator.py`)
- [ ] Generated experiment results (`python3 chapter3_experiments_v2.py`)
- [ ] Using correct notebook (`2_Algo_FIXED.ipynb`, not `2. Algo.ipynb`)
- [ ] Restarted kernel before running
- [ ] Current directory is `experiment/`

### Nếu vẫn lỗi:
```bash
# Clean và start lại
cd /Users/haphuongquynh/Desktop/AI/AI_GFBS_BPSO

# Remove cache
rm -rf **/__pycache__
rm -rf **/.ipynb_checkpoints

# Reinstall
pip3 install --upgrade -r requirements.txt

# Regenerate everything
python3 src/data_generator.py
cd experiment
python3 chapter3_experiments_v2.py

# Now try notebooks
jupyter notebook
```

---

## 🎉 Success Criteria

Khi chạy thành công, bạn sẽ thấy:

1. **Console output:**
```
✅ Loaded 13 test cases
🔬 Running GBFS Parameter Experiments...
Testing max_states = 1000...
  ✓ Value: 114375.0 ± 0.0
  ✓ Time: 0.0015s
...
✅ Visualization saved to: results/chapter3/...
```

2. **Figures hiển thị** trong notebook
3. **CSV files** được tạo trong `results/chapter3/`
4. **PNG files** cho từng visualization

---

**🚀 BẮT ĐẦU TỪ ĐÂY: Chạy `python3 chapter3_experiments_v2.py` rồi dùng notebooks _FIXED!**
