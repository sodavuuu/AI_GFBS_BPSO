# 🎒 Bài Toán Cái Túi - So Sánh Thuật Toán GBFS, BPSO và DP

## 📋 Mục đích

Ứng dụng desktop giúp **học tập và so sánh** các thuật toán giải bài toán 0/1 Knapsack:

- **GBFS** (Greedy Best First Search) - Thuật toán tham lam với SimpleAI
- **BPSO** (Binary Particle Swarm Optimization) - Thuật toán đàn hạt
- **DP** (Dynamic Programming) - Thuật toán quy hoạch động (tối ưu 100%)

### 🎯 Mục tiêu học tập

1. **Hiểu cách hoạt động** của từng thuật toán qua giải thích chi tiết và minh họa
2. **So sánh hiệu suất** về giá trị, tốc độ, và độ chính xác
3. **Thử nghiệm** với các loại dataset khác nhau để thấy điểm mạnh/yếu
4. **Phân tích tự động** - Hệ thống giải thích kết quả và đưa ra khuyến nghị

---

## 🚀 Hướng dẫn Cài đặt

### Bước 1: Chuẩn bị môi trường

Yêu cầu: **Python 3.8+**

Tạo virtual environment (khuyến nghị):
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### Bước 2: Cài đặt thư viện

```bash
pip install -r requirements.txt
```

Hoặc cài thủ công:
```bash
pip install simpleai>=0.8.3 numpy>=1.24.0 PyQt5>=5.15.0 matplotlib>=3.7.0
```

### Bước 3: Chạy chương trình

```bash
python gui_app.py
```

Giao diện PyQt5 sẽ mở ra với 3 panel chính.

---

## 📖 Cách sử dụng Chương trình

### Giao diện 3 panel

```
┌─────────────┬───────────────────┬──────────────────┐
│             │                   │                  │
│   PANEL 1   │     PANEL 2       │    PANEL 3       │
│  Điều khiển │   Kết quả & Đồ thị│  Phân tích       │
│             │                   │                  │
└─────────────┴───────────────────┴──────────────────┘
```

### **Panel 1 (Trái) - Điều khiển**

1. **Tạo Dataset:**
   - Chọn loại: Random, High Correlation, Outlier, Similar Ratio
   - Điều chỉnh số items (10-30)
   - Điều chỉnh capacity (100-500)
   - Click "Tạo Bộ Dữ Liệu"

2. **Cấu hình Thuật toán:**
   - GBFS: Giới hạn states (tránh bùng nổ)
   - BPSO: Số particles (20-50), Iterations (50-200)

3. **Chạy:**
   - Click "Chạy Tất Cả Thuật Toán" (khuyến nghị)
   - Hoặc chạy từng thuật toán riêng

4. **Giải thích Thuật toán:**
   - Chọn GBFS/BPSO/DP từ dropdown
   - Đọc cách hoạt động, ví dụ, ưu/nhược điểm

### **Panel 2 (Giữa) - Kết quả**

1. **Bảng So sánh:**
   - Rows: Giá trị, Trọng lượng, % Capacity, Số items, Thời gian, Gap vs Optimal
   - Columns: GBFS, BPSO, DP
   - **Màu xanh** = Tốt nhất/Optimal
   - **Màu đỏ** = Kém nhất/Không khả thi

2. **4 Biểu đồ:**
   - **Trên trái:** So sánh giá trị đạt được
   - **Trên phải:** Quá trình hội tụ BPSO (với baseline GBFS & Optimal)
   - **Dưới trái:** Thời gian thực thi (ms)
   - **Dưới phải:** Gap so với optimal (%)

3. **Minh họa Quá trình:**
   - GBFS: Từng bước chọn item theo ratio
   - BPSO: Key iterations với best/avg fitness
   - DP: Backtracking từ bảng quy hoạch động

### **Panel 3 (Phải) - Phân tích Tự động**

1. **Phân tích Kết quả:**
   - Ranking theo giá trị (best → worst)
   - Ranking theo tốc độ (fastest → slowest)
   - Đánh giá sử dụng capacity

2. **Giải thích & Khuyến nghị:**
   - Phân tích dựa trên loại dataset
   - Giải thích tại sao thuật toán X tốt/kém
   - Khuyến nghị thuật toán phù hợp cho từng tình huống

3. **Vật phẩm được chọn:**
   - Danh sách items của từng thuật toán
   - So sánh sự khác biệt trong lựa chọn

---

## 🎓 Cách hiểu Chương trình

### 1. **Hiểu bài toán 0/1 Knapsack**

**Đề bài:** Có N items, mỗi item có:
- `weight` (trọng lượng)
- `value` (giá trị)

Túi có sức chứa `capacity`. Chọn items sao cho:
- Tổng weight ≤ capacity
- Tổng value **tối đa**

**Ví dụ:**
```
Items: A(w=10,v=60), B(w=20,v=100), C(w=30,v=120)
Capacity: 50

Giải pháp tối ưu: Chọn A + B → value = 160, weight = 30
```

### 2. **Hiểu 3 thuật toán**

#### **GBFS - Greedy Best First Search**

**Ý tưởng:** Luôn chọn item "hứa hẹn" nhất (theo heuristic)

**Cách hoạt động:**
```python
1. Bắt đầu: Túi rỗng
2. Tính heuristic cho mỗi item còn lại
   h(item) = Fractional Bound (ước lượng tiềm năng)
3. Chọn item có h() cao nhất → Thêm vào túi
4. Lặp lại cho đến khi không thêm được nữa
```

**Khi nào dùng:**
- ✅ Dataset nhỏ (<20 items), random
- ✅ Cần kết quả nhanh (vài milliseconds)
- ❌ Dataset phức tạp (high correlation, outliers)

#### **BPSO - Binary Particle Swarm Optimization**

**Ý tưởng:** Mô phỏng đàn chim tìm thức ăn

**Cách hoạt động:**
```python
1. Khởi tạo đàn hạt (mỗi hạt = 1 solution ngẫu nhiên)
2. Mỗi iteration:
   - Đánh giá fitness từng hạt
   - Cập nhật pbest (best cá nhân)
   - Cập nhật gbest (best toàn đàn)
   - Các hạt "bay" về phía gbest
3. Sau N iterations → gbest là solution
```

**Khi nào dùng:**
- ✅ Dataset lớn (>20 items), phức tạp
- ✅ Cần chất lượng cao (gần optimal)
- ❌ Thời gian thực thi không quan trọng

#### **DP - Dynamic Programming**

**Ý tưởng:** Tính toán mọi khả năng, chọn tối ưu

**Cách hoạt động:**
```python
1. Tạo bảng DP[i][w] (i items, capacity w)
2. DP[i][w] = max(
     DP[i-1][w],              # Không chọn item i
     DP[i-1][w-wi] + vi       # Chọn item i
   )
3. Backtrack để tìm items được chọn
```

**Khi nào dùng:**
- ✅ Cần 100% optimal
- ✅ Capacity nhỏ (<1000)
- ❌ Dataset rất lớn (chậm, tốn RAM)

### 3. **Hiểu các loại Dataset**

Chương trình cung cấp 4 test cases:

| Dataset          | Đặc điểm                              | GBFS     | BPSO     | DP      |
|------------------|---------------------------------------|----------|----------|---------|
| **Random**       | Items ngẫu nhiên, cân bằng            | ✅ Tốt   | ✅ Tốt   | ✅ Tốt  |
| **High Correlation** | value ≈ 2×weight                   | ❌ Yếu   | ✅ Mạnh  | ✅ Tốt  |
| **Outlier**      | Có items nặng = 60% capacity          | ⚠️ Bẫy   | ✅ Tránh | ✅ Tốt  |
| **Similar Ratio** | Tất cả items có v/w ≈ 2.0            | ⚠️ Khó   | ✅ Tốt   | ✅ Tốt  |

**Khuyến nghị học tập:**
1. Chạy **Random** trước → Thấy GBFS nhanh & tốt
2. Chạy **High Correlation** → Thấy GBFS thua BPSO rõ rệt
3. Chạy **Outlier** → Thấy GBFS có thể bị bẫy
4. Chạy **Similar Ratio** → Thấy BPSO explore tốt hơn

### 4. **Hiểu Kết quả**

#### **Metrics quan trọng:**

- **Total Value:** Giá trị đạt được (càng cao càng tốt)
- **Gap với Optimal:** % chênh lệch so với DP (càng thấp càng tốt)
  - Gap < 1% → Excellent
  - Gap 1-5% → Good
  - Gap > 10% → Poor
- **Execution Time:** Thời gian chạy
  - GBFS: ~1-10ms (nhanh nhất)
  - BPSO: ~50-500ms (chậm hơn)
  - DP: ~10-100ms (phụ thuộc capacity)
- **Capacity Usage:** % sử dụng túi
  - ≥95% → Excellent (tận dụng tốt)
  - 85-95% → Good
  - <80% → Poor (lãng phí không gian)

#### **Phân tích Gap:**

Nếu GBFS gap cao:
→ Dataset khó, cần dùng BPSO hoặc DP

Nếu BPSO gap cao:
→ Tăng particles/iterations hoặc dùng DP

### 5. **Hiểu Code Structure**

```
gui_app.py          # Giao diện PyQt5 (main file)
├── create_left_panel()    # Controls & Algorithm explanation
├── create_middle_panel()  # Results table & Charts
├── create_right_panel()   # Auto analysis & Recommendations
├── run_algorithm()        # Execute GBFS/BPSO/DP
└── plot_bpso_convergence()# Draw 4 charts

algorithms.py       # Core algorithms
├── GBFS_Solver    # SimpleAI SearchProblem + heuristic
├── BPSO_Solver    # PSO với binary encoding
├── DP_Solver      # Quy hoạch động
└── generate_dataset()  # 4 test cases
```

**Điểm mấu chốt:**

1. **GBFS_Solver** kế thừa `SearchProblem` của SimpleAI:
   - `heuristic()`: Fractional Bound (âm để SimpleAI ưu tiên)
   - `actions()`: Items có thể thêm (sorted by ratio)
   - `max_states`: Limit để tránh bùng nổ

2. **BPSO_Solver** track `history`:
   - Mỗi iteration lưu gbest_fitness, avg_fitness
   - Dùng để vẽ convergence curve

3. **GUI** tự động phân tích:
   - `update_analysis()`: Ranking theo value/speed
   - `update_explanation()`: Smart recommendations dựa dataset type

---

## 📁 Cấu trúc Project

```
AICK/
├── gui_app.py          # Main PyQt5 application
├── algorithms.py       # GBFS, BPSO, DP implementations
├── requirements.txt    # Dependencies
├── README.md          # Documentation (file này)
└── ai.py              # (Old file - not used)
```

---

## 🔧 Tùy chỉnh nâng cao

### Điều chỉnh GBFS max_states

Nếu GBFS crash với dataset lớn, giảm max_states:
```python
# Trong GUI: Spinbox "Giới Hạn States" (default 10000)
# Hoặc trong code:
solver = GBFS_Solver(problem, max_states=5000)
```

### Điều chỉnh BPSO parameters

```python
# Trong GUI: Spinboxes
# Hoặc trong code:
solver = BPSO_Solver(
    problem,
    n_particles=50,      # Nhiều hơn → chậm nhưng tốt hơn
    max_iterations=200,  # Nhiều hơn → hội tụ tốt hơn
    w=0.7,               # Inertia weight
    c1=1.5,              # Cognitive (học từ bản thân)
    c2=1.5               # Social (học từ đàn)
)
```

---

## 📊 Tips học tập

### Thực hành theo thứ tự:

1. **Làm quen:**
   - Tạo dataset Random (10 items, capacity 100)
   - Chạy tất cả → Xem GBFS thắng

2. **Thử thách GBFS:**
   - Tạo High Correlation (20 items, capacity 300)
   - Chạy → Xem GBFS thua BPSO

3. **Phân tích convergence:**
   - Quan sát đồ thị Hội tụ BPSO
   - Thấy BPSO vượt GBFS sau ~20-30 iterations

4. **Thử nghiệm parameters:**
   - Giảm BPSO iterations xuống 20 → Gap tăng
   - Tăng lên 200 → Gap giảm (nhưng chậm)

5. **So sánh với Optimal:**
   - DP luôn cho gap = 0%
   - Nhưng chậm với capacity lớn (>500)

---

## 🎯 Kết luận

Sau khi học xong chương trình này, bạn sẽ:

✅ Hiểu bản chất bài toán 0/1 Knapsack  
✅ Biết khi nào dùng GBFS (nhanh), BPSO (chất lượng), DP (tối ưu)  
✅ Phân tích được trade-off giữa tốc độ và chất lượng  
✅ Đọc được convergence curve và phân tích gap  
✅ Áp dụng cho các bài toán tối ưu khác  

---

## 📚 Tham khảo

- **SimpleAI Library:** https://github.com/simpleai-team/simpleai
- **BPSO Paper:** Kennedy & Eberhart (1997) - "A discrete binary version of the particle swarm algorithm"
- **Knapsack Problem:** https://en.wikipedia.org/wiki/Knapsack_problem

---

**Chúc bạn học tốt! 🎓📚**
