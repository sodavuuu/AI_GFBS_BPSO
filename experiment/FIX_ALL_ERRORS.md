# 🎯 FIX TẤT CẢ LỖI NOTEBOOKS - HƯỚNG DẪN NHANH

## ⚡ Solution 1: Chạy Script Tự Động (KHUYẾN NGHỊ)

```bash
# Về thư mục project
cd /Users/haphuongquynh/Desktop/AI/AI_GFBS_BPSO

# Cho phép chạy script
chmod +x setup_experiments.sh

# Chạy auto setup
./setup_experiments.sh
```

Script sẽ tự động:
1. ✅ Check Python installation
2. ✅ Install dependencies
3. ✅ Generate test cases
4. ✅ Generate experiment results
5. ✅ Verify everything

**Sau khi chạy xong:**
```bash
cd experiment
jupyter notebook
```

Mở notebooks `2_Algo_FIXED.ipynb` và `3_Data_FIXED.ipynb` → Chạy ngay!

---

## 🔧 Solution 2: Fix Thủ Công (Nếu script không chạy)

### Bước 1: Install Dependencies
```bash
cd /Users/haphuongquynh/Desktop/AI/AI_GFBS_BPSO
pip3 install numpy pandas matplotlib seaborn jupyter scikit-learn
```

### Bước 2: Generate Test Data
```bash
python3 src/data_generator.py
```

Kết quả: File `data/test_cases/test_cases_summary.csv` được tạo

### Bước 3: Generate Experiment Results
```bash
cd experiment
python3 chapter3_experiments_v2.py
```

Kết quả: CSV files trong `results/chapter3/`

### Bước 4: Start Jupyter
```bash
jupyter notebook
```

### Bước 5: Dùng Notebooks FIXED
- ✅ Open `2_Algo_FIXED.ipynb`
- ✅ `Kernel > Restart & Run All`
- ✅ Open `3_Data_FIXED.ipynb`
- ✅ `Kernel > Restart & Run All`

---

## 📋 Checklist - Đảm bảo không lỗi

### Before Running Notebooks:

- [ ] Python 3 installed (`python3 --version`)
- [ ] Dependencies installed (`pip3 list | grep numpy`)
- [ ] Test cases generated (`ls data/test_cases/*.csv`)
- [ ] Experiment results generated (`ls results/chapter3/*.csv`)
- [ ] Current directory is `experiment/`
- [ ] Using correct notebooks (`*_FIXED.ipynb`)

### Common Issues:

| Lỗi | Fix |
|-----|-----|
| `ModuleNotFoundError: No module named 'numpy'` | `pip3 install numpy pandas matplotlib seaborn` |
| `FileNotFoundError: test_cases_summary.csv` | `python3 src/data_generator.py` |
| `NameError: name 'test_case' is not defined` | Restart kernel & Run All |
| Notebook chạy lâu | Dùng `*_FIXED.ipynb` thay vì chạy từ scratch |

---

## 🎨 Which Notebooks to Use?

### ✅ RECOMMENDED (Load CSV - Fast):

1. **`2_Algo_FIXED.ipynb`**
   - Loads: `3_1_2_comparison_Size_Medium_50.csv`
   - Time: ~5 seconds
   - Output: Beautiful comparison charts

2. **`3_Data_FIXED.ipynb`**
   - Loads: `3_1_3_data_characteristics.csv`
   - Time: ~5 seconds
   - Output: Data characteristics analysis

### ⚠️ NEEDS SETUP (Run Experiments - Slow):

3. **`1. Parameter.ipynb`**
   - Runs: GBFS & BPSO experiments
   - Time: ~10-15 minutes
   - Output: Parameter analysis with many runs
   - **Requires:** All dependencies + test cases

### ❌ OLD (Don't Use):

- `2. Algo.ipynb` → Has errors, use `2_Algo_FIXED.ipynb`
- `3. Data.ipynb` → Has errors, use `3_Data_FIXED.ipynb`

---

## 📊 Expected File Structure After Setup

```
AI_GFBS_BPSO/
├── data/
│   └── test_cases/
│       ├── test_cases_summary.csv        ✅ Must exist
│       ├── Size_Small_30.csv            ✅ Must exist
│       ├── Size_Medium_50.csv           ✅ Must exist
│       └── ... (13 CSV files total)
│
├── results/
│   └── chapter3/
│       ├── 3_1_2_comparison_Size_Medium_50.csv  ✅ Must exist
│       ├── 3_1_3_data_characteristics.csv       ✅ Must exist
│       └── *.png (visualizations)
│
└── experiment/
    ├── 2_Algo_FIXED.ipynb               ✅ Use this
    ├── 3_Data_FIXED.ipynb               ✅ Use this
    ├── 1. Parameter.ipynb               ⚠️ Needs setup
    └── setup_experiments.sh             🔧 Auto setup
```

---

## 🚀 Quick Start (1 Phút)

```bash
# 1. Go to project
cd /Users/haphuongquynh/Desktop/AI/AI_GFBS_BPSO

# 2. Run auto setup
chmod +x setup_experiments.sh && ./setup_experiments.sh

# 3. Start Jupyter
cd experiment && jupyter notebook

# 4. Open 2_Algo_FIXED.ipynb → Run All
# 5. Open 3_Data_FIXED.ipynb → Run All
```

**Done! 🎉**

---

## 💡 Pro Tips

### For Academic Report:
1. Generate all results once: `./setup_experiments.sh`
2. Use `*_FIXED.ipynb` notebooks for fast visualization
3. Export figures from `results/chapter3/*.png`
4. Copy figures into LaTeX/Word document

### For Exploration:
1. Modify `1. Parameter.ipynb` to test different parameters
2. Change `max_states_values`, `swarm_sizes`, etc.
3. Re-run to see impact

### For Presentation:
1. All figures are 300 DPI, publication-ready
2. Styled like GA_TSP (professional)
3. Can be used directly in slides

---

## 🆘 Still Having Issues?

### Check Python Environment:
```bash
python3 --version        # Should be 3.8+
pip3 list | grep numpy   # Should show numpy version
```

### Clean Install:
```bash
cd /Users/haphuongquynh/Desktop/AI/AI_GFBS_BPSO

# Remove caches
rm -rf **/__pycache__
rm -rf **/.ipynb_checkpoints

# Reinstall
pip3 install --force-reinstall numpy pandas matplotlib seaborn

# Regenerate data
python3 src/data_generator.py
cd experiment
python3 chapter3_experiments_v2.py
```

### Verify Setup:
```bash
# Should show 13+ files
ls -l data/test_cases/*.csv | wc -l

# Should show 5+ files
ls -l results/chapter3/*.csv | wc -l

# Should show notebook files
ls -l experiment/*.ipynb
```

---

## ✅ Success Indicators

Khi setup thành công, bạn sẽ thấy:

1. **No errors** khi import trong notebook
2. **CSV files** tồn tại trong `results/chapter3/`
3. **Visualizations** hiển thị đẹp trong notebook
4. **Execution time** < 10 giây cho notebooks FIXED

---

**🎯 BOTTOM LINE: Chạy `./setup_experiments.sh` và dùng `*_FIXED.ipynb` notebooks!**
