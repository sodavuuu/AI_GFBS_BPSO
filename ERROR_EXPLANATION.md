# 🔧 GIẢI THÍCH LỖI VÀ CÁCH SỬA

## ❌ **Lỗi gặp phải:**

```
ValueError: operands could not be broadcast together with shapes (5,) (50,)
```

---

## 🔍 **Nguyên nhân:**

### **KHÔNG phải trùng lặp file!**

Vấn đề là **sự khác biệt về interface** giữa code cũ và mới:

### **Code cũ (Notebooks):**
```python
# Notebooks đang dùng interface CŨ
solve_knapsack_bpso(
    test_case['values'],      # ❌ values đầu tiên
    test_case['weights'],     # ❌ weights thứ hai
    test_case['capacity'],    # ❌ Thiếu items!
    n_particles=30
)
```

### **Code mới (Source files):**
```python
# Source code đã CẬP NHẬT interface
def solve_knapsack_bpso(items, weights, values, capacity, ...):
    #                   ^^^^^ THÊM items ở đầu!
```

### **Tại sao lại có lỗi shapes (5,) vs (50,)?**

Khi notebooks truyền:
- `test_case['values']` (50 elements) → được nhận như **items**
- `test_case['weights']` (50 elements) → được nhận như **weights**  
- `test_case['capacity']` (số nguyên 178) → được nhận như **values**

→ Khi thuật toán tạo `items`:
```python
items = [f"Item_{i+1}" for i in range(len(values))]
# len(values) = capacity = 178... NHƯNG chỉ lấy 5 phần tử đầu!
```

---

## ✅ **Cách sửa:**

### **1. File `chapter3_experiments_v2.py`** 
✅ **ĐÃ ĐÚNG** - Đang truyền: `(items, weights, values, capacity)`

### **2. Notebooks**
❌ **CẦN SỬA** - Đổi từ `(values, weights, capacity)` sang `(items, weights, values, capacity)`

---

## 📝 **Đã sửa trong các notebooks:**

### ✅ `1. Parameter.ipynb`
- Cell test swarm size: Thêm `test_case['items']` ở đầu
- Cell test iterations: Thêm `test_case['items']` ở đầu

### ✅ `2. Algo.ipynb`  
- Đã có `items` trong tất cả các calls

### ✅ `3. Data.ipynb`
- Đã có `items` trong tất cả các calls

### ✅ `4. StepByStep.ipynb`
- Đã có `items` trong step tracking

---

## 🎯 **Tại sao chapter3_experiments_v2.py chạy được một phần?**

Vì nó đang dùng **interface đúng** từ đầu!

Nhưng có lỗi khác:
1. **Lỗi shapes ở lần chạy thứ 2**: Có thể do random seed hoặc state không reset
2. **Lỗi `w` parameter**: Function không hỗ trợ tham số `w` (inertia weight)

---

## 🔨 **Hành động cần làm:**

### **Bước 1: Kiểm tra lại source code**

Đảm bảo `solve_knapsack_bpso` trong `src/bpso_knapsack.py` có signature:

```python
def solve_knapsack_bpso(items, weights, values, capacity, 
                        n_particles=30, max_iterations=100):
    # ✅ Đúng thứ tự: items, weights, values, capacity
```

### **Bước 2: Chạy lại notebooks**

Bây giờ các notebooks đã được sửa, hãy chạy từng cell để kiểm tra:

```bash
jupyter notebook
# Mở 1. Parameter.ipynb và chạy từng cell
```

### **Bước 3: Xử lý lỗi trong chapter3_experiments_v2.py**

Có 2 vấn đề cần sửa:

#### **a) Lỗi shapes ở run thứ 2**
Có thể do test case loader trả về data khác nhau. Cần kiểm tra xem có random sampling không.

#### **b) Lỗi parameter `w`**
Function không nhận `w` parameter. Cần:
- Hoặc bỏ experiment test inertia weight
- Hoặc thêm `w` vào function signature

---

## 💡 **Tóm tắt:**

| Vấn đề | Nguyên nhân | Giải pháp |
|--------|-------------|-----------|
| **Shapes mismatch** | Notebooks dùng interface cũ | ✅ Đã sửa: thêm `items` parameter |
| **chapter3 lỗi run 2** | Có thể do random/state | 🔍 Cần điều tra thêm |
| **Lỗi parameter `w`** | Function không hỗ trợ | 🔧 Cần update function hoặc bỏ experiment |

---

## 🎉 **Kết luận:**

- ✅ **Notebooks đã được sửa** - Giờ khớp với source code
- ✅ **Không có trùng lặp file** - Chỉ là khác interface
- 🔍 **Chapter3 script** - Cần xử lý thêm 2 lỗi còn lại

**Hãy chạy lại notebooks để kiểm tra!**
