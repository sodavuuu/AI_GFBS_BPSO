# 📚 EXPERIMENT NOTEBOOKS - HƯỚNG DẪN SỬ DỤNG

## 🎯 Tổng quan

Tất cả experiments đã được cập nhật theo style GA_TSP với:
- ✅ Load kết quả từ CSV (đã generate bởi `chapter3_experiments_v2.py`)
- ✅ Visualizations chuyên nghiệp với `AdvancedKnapsackVisualizer`
- ✅ Phân tích chi tiết và insights
- ✅ Summary tables và rankings

---

## 📂 Cấu trúc Notebooks

### ✅ **1. Parameter.ipynb** (ĐÃ SỬA)
**Section 3.1.1: Phân tích tham số**

- **GBFS Parameters**: max_states impact
  - 4 subplots: Value, Time, Efficiency, Summary
  - CSV: `3_1_1_a_gbfs_params.csv`
  
- **BPSO Parameters**: 
  - Swarm size (n_particles): Convergence comparison, quality analysis
  - Max iterations: Impact on solution quality
  - CSV: `3_1_1_b_bpso_swarm_size.csv`, `3_1_1_c_bpso_iterations.csv`

**Visualizations:**
- Multi-line convergence plots
- Error bars và annotations
- Best value markers
- Professional styling

---

### ✅ **2_Algo_FIXED.ipynb** (MỚI TẠO)
**Section 3.1.2: So sánh thuật toán**

- Load từ CSV: `3_1_2_comparison_Size_Medium_50.csv`
- Visualizations:
  - Solution quality comparison (bar chart)
  - Computational cost (log scale)
  - Efficiency analysis (value/time)
  - Quality vs Speed trade-off (scatter)
  - Ranking table với emojis 🥇🥈🥉

**Methods sử dụng:**
```python
visualizer.plot_algorithm_comparison(df_comparison)
```

**Insights included:**
- Statistical analysis per algorithm
- Performance degradation từ optimal
- Recommendations based on scenarios

---

### ✅ **3_Data_FIXED.ipynb** (MỚI TẠO)
**Section 3.1.3: Ảnh hưởng đặc điểm dữ liệu**

- Load từ CSV: `3_1_3_data_characteristics.csv`
- Test characteristics:
  - Low/High correlation
  - High value distribution
  - Regional diversity

**Visualizations:**
- Solution quality by characteristic (grouped bars)
- Computational cost impact (log scale)
- Performance degradation analysis
- Summary table với % optimal

**Methods sử dụng:**
```python
visualizer.plot_data_characteristics_impact(df_data)
```

**Insights included:**
- Algorithm sensitivity analysis
- Data characteristic rankings
- Practical implications

---

### ❌ **4. StepByStep.ipynb** (CHƯA SỬA)
**Section 3.2: Visualization từng bước**

- Sẽ cần update để show step-by-step process
- Sử dụng `step_by_step_visualizer.py`

---

## 🚀 Cách chạy

### Bước 1: Generate results (nếu chưa có)
```bash
cd experiment
python chapter3_experiments_v2.py
```

### Bước 2: Run notebooks
```bash
jupyter notebook
```

Chạy theo thứ tự:
1. `1. Parameter.ipynb` ✅
2. `2_Algo_FIXED.ipynb` ✅ (thay thế `2. Algo.ipynb`)
3. `3_Data_FIXED.ipynb` ✅ (thay thế `3. Data.ipynb`)
4. `4. StepByStep.ipynb` ⚠️ (cần update)

---

## 📊 CSV Results Location

Tất cả kết quả trong `results/chapter3/`:

```
results/chapter3/
├── 3_1_1_a_gbfs_params.csv           # GBFS parameter analysis
├── 3_1_1_b_bpso_swarm_size.csv       # BPSO swarm size impact
├── 3_1_1_c_bpso_iterations.csv       # BPSO iterations impact
├── 3_1_2_comparison_Size_Medium_50.csv  # Algorithm comparison
└── 3_1_3_data_characteristics.csv    # Data characteristics impact
```

---

## 🎨 AdvancedKnapsackVisualizer Methods

### Có sẵn và đã test:
1. ✅ `plot_gbfs_parameter_impact(df)`
2. ✅ `plot_bpso_parameter_impact(df, param_name)`
3. ✅ `plot_algorithm_comparison(df)` **(MỚI THÊM)**
4. ✅ `plot_data_characteristics_impact(df)` **(MỚI THÊM)**
5. ✅ `plot_knapsack_solution_map(solution, items_df)`

### Usage example:
```python
from src.advanced_visualizer import AdvancedKnapsackVisualizer

visualizer = AdvancedKnapsackVisualizer()

# Load CSV
df = pd.read_csv('results/chapter3/3_1_2_comparison.csv')

# Create visualization
fig = visualizer.plot_algorithm_comparison(
    df, 
    title="Algorithm Comparison",
    save_path='output.png'
)
plt.show()
```

---

## ✨ Style Guidelines (GA_TSP inspired)

### Colors:
- GBFS: Blue `#3498db`
- BPSO: Red `#e74c3c`
- DP: Green `#2ecc71`

### Visualizations checklist:
- ✅ Error bars cho stochastic algorithms
- ✅ Annotations với arrows
- ✅ Grid alpha=0.3
- ✅ Bold labels và titles
- ✅ Legend với frameon=True, shadow=True
- ✅ Summary tables styled
- ✅ Save at 300 DPI

---

## 🔄 Migration from Old Notebooks

### ❌ **2. Algo.ipynb** (OLD)
- Có errors
- Chạy trực tiếp algorithms (slow)
- Không có professional visualizations

### ✅ **2_Algo_FIXED.ipynb** (NEW)
- Load từ CSV (fast)
- Professional visualizations
- Detailed insights và analysis

**→ SỬ DỤNG FILE MỚI!**

---

## 📝 TODO

- [ ] Update `4. StepByStep.ipynb` với step visualizations
- [ ] Thêm convergence animations (optional)
- [ ] Tạo master notebook combine tất cả sections
- [ ] Generate PDF report từ notebooks

---

## 🎓 For Academic Report

**Recommended structure:**

1. **Section 3.1.1**: Parameter Analysis
   - Use: `1. Parameter.ipynb`
   - Figures: GBFS params, BPSO swarm size, BPSO iterations

2. **Section 3.1.2**: Algorithm Comparison
   - Use: `2_Algo_FIXED.ipynb`
   - Figures: Comparison charts, trade-off analysis

3. **Section 3.1.3**: Data Characteristics
   - Use: `3_Data_FIXED.ipynb`
   - Figures: Characteristic impact, sensitivity analysis

4. **Section 3.2**: Step-by-Step Visualization
   - Use: `4. StepByStep.ipynb` (needs update)
   - Figures: Algorithm execution visualization

---

## 💡 Tips

1. **Always load from CSV** - Nhanh hơn và consistent
2. **Use visualizer methods** - Đã optimize cho GA_TSP style
3. **Include insights** - Markdown cells với phân tích chi tiết
4. **Save high-res** - 300 DPI cho publication
5. **Version control** - Commit notebooks sau khi run xong

---

## 📞 Support

Nếu có lỗi:
1. Check CSV files tồn tại trong `results/chapter3/`
2. Run `chapter3_experiments_v2.py` để generate results
3. Verify column names match expectations
4. Check `AdvancedKnapsackVisualizer` methods

---

**🎉 READY TO USE! Tất cả notebooks đã được chuẩn hóa theo GA_TSP style.**
