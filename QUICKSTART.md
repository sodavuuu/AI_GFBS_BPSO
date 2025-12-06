# 🚀 Quick Start Guide

## ⚡ TL;DR - Chạy Ngay

```bash
# Chạy GUI
python3 main.py

# Chạy experiments
python3 main.py --experiments

# Regenerate data
python3 main.py --regenerate
```

---

## 📁 Cấu Trúc Project

```
AI_GFBS_BPSO/
│
├── main.py                    # 🎯 CHẠY FILE NÀY
│
├── src/                       # Core algorithms
│   ├── algorithms/            # GBFS, BPSO
│   ├── utils/                 # Data loader
│   └── visualization/         # Charts
│
├── gui/                       # Giao diện
│   └── main_gui.py
│
├── experiment/chapter3/       # Phân tích
│   ├── experiments.py
│   └── *.ipynb               # Notebooks
│
├── data/test_cases/           # 13 test cases
└── results/chapter3/          # Kết quả
```

---

## 🎯 3 Cách Sử Dụng

### 1. GUI (Giao Diện)
```bash
python3 main.py
```
- Load test cases
- Chạy GBFS/BPSO
- Visualize kết quả
- Export CSV

### 2. Experiments (Phân Tích)
```bash
python3 main.py --experiments
```
Menu:
1. GBFS Parameters
2. BPSO Swarm Size
3. BPSO Iterations
4-6. Algorithm Comparison
7. **Run ALL**

### 3. Notebooks (Chi Tiết)
```bash
cd experiment/chapter3
jupyter notebook
```
- 3.1.1 - Parameter Analysis
- 3.1.2 - Algorithm Comparison
- 3.1.3 - Data Characteristics

---

## 🧠 Algorithms

**GBFS:**
- Deterministic (kết quả ổn định)
- Fast (< 50ms)
- Config: `max_states=5000`

**BPSO:**
- Global search (escape local optima)
- Stochastic (variance cao)
- Config: `n_particles=30, max_iterations=50`

**Fitness Function (BOTH):**
```python
fitness = 0.7 * revenue + 0.3 * coverage - penalty
```

---

## 📊 Kết Quả

Tất cả kết quả trong: `results/chapter3/`

**CSV Files:**
- `3_1_1_a_gbfs_params.csv`
- `3_1_1_b_bpso_swarm_size.csv`
- `3_1_1_c_bpso_iterations.csv`
- `3_1_2_comparison_*.csv`
- `3_1_3_data_characteristics.csv`

**PNG Files:**
- Tương ứng với mỗi CSV
- Publication-ready charts

---

## 🔧 Troubleshooting

**GUI không chạy?**
```bash
pip install PyQt5
```

**Import error?**
```bash
pip install -r requirements.txt
```

**Thiếu data?**
```bash
python3 main.py --regenerate
```

---

## 📖 Documentation

- **README.md** - Hướng dẫn chi tiết
- **WORKFLOW_UNIFICATION.md** - Kiến trúc
- **CLEANUP_SUMMARY.md** - Tổng kết cleanup

---

## 💡 Tips

1. **Chạy GUI** trước để làm quen
2. **Run experiments** để generate data
3. **Open notebooks** để phân tích chi tiết

**Workflow:**
```
main.py --regenerate → main.py --gui → Notebooks
```

---

**Made with ❤️ for Multi-Objective Optimization**
