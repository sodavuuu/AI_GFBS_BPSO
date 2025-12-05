# 🐛 LỖI GBFS - PHÂN TÍCH CHI TIẾT

## ❌ **Vấn đề chính:**

GBFS hiện tại chỉ đạt **7-25% optimal** thay vì gần 100%.

---

## 🔍 **Nguyên nhân:**

### **1. Heuristic function sai hướng**

```python
def heuristic(self, state):
    """Fractional knapsack upper bound"""
    current_weight = sum(self.weights[i] for i in state)
    current_value = sum(self.values[i] for i in state)
    remaining = self.capacity - current_weight
    
    # Tính upper bound...
    return current_value  # ❌ Trả về giá trị DƯƠNG
```

**Vấn đề:**
- `simpleai.greedy()` tìm kiếm theo hướng **MINIMIZE** heuristic
- Nhưng chúng ta cần **MAXIMIZE** giá trị
- → GBFS đang chọn states có giá trị **THẤP** thay vì **CAO**!

**Giải pháp:**
```python
return -current_value  # ✅ Đổi dấu để minimize = maximize
```

---

### **2. Max_states không hoạt động đúng**

```python
def is_goal(self, state):
    """Check if no more items can fit"""
    if self.states_explored >= self.max_states:
        return True  # ❌ Dừng sớm khi đạt max_states
    self.states_explored += 1
    return len(self.actions(state)) == 0
```

**Vấn đề:**
- Khi đạt max_states, algorithm **dừng ngay lập tức**
- Có thể dừng ở state chưa tốt
- Giải thích tại sao max_states=10000 cho kết quả tệ hơn 5000

**Giải pháp:**
- Chỉ dừng khi không có actions (capacity đầy)
- Dùng max_states như giới hạn exploration, không phải goal

---

## 🔧 **CÁC LỖI CẦN SỬA**

### **Lỗi 1: Heuristic sai dấu** (CRITICAL ⚠️)

**File:** `src/gbfs_knapsack.py`

**Dòng 73:** 
```python
return current_value  # ❌ SAI
```

**Sửa thành:**
```python
return -current_value  # ✅ ĐÚNG (negative for maximization)
```

---

### **Lỗi 2: is_goal logic sai** (IMPORTANT ⚠️)

**File:** `src/gbfs_knapsack.py`

**Dòng 50-54:**
```python
def is_goal(self, state):
    if self.states_explored >= self.max_states:
        return True  # ❌ Dừng sớm
    self.states_explored += 1
    return len(self.actions(state)) == 0
```

**Sửa thành:**
```python
def is_goal(self, state):
    self.states_explored += 1
    # Chỉ goal khi không còn items nào fit
    return len(self.actions(state)) == 0
```

Và thêm check max_states trong actions hoặc result.

---

### **Lỗi 3: Không track best solution**

Hiện tại GBFS chỉ trả về state cuối cùng, không track state tốt nhất gặp được.

**Giải pháp:**
```python
def __init__(self, ...):
    ...
    self.best_state = tuple()
    self.best_value = 0

def result(self, state, action):
    new_state = tuple(sorted(state + (action,)))
    
    # Track best solution
    new_value = sum(self.values[i] for i in new_state)
    if new_value > self.best_value:
        self.best_value = new_value
        self.best_state = new_state
    
    return new_state
```

---

## 📊 **Tác động của bugs:**

### **Bug 1: Heuristic sai dấu**
- **Hiện tượng:** GBFS chọn items có giá trị THẤP
- **Kết quả:** Chỉ đạt 7-25% optimal
- **Mức độ:** 🔴 CRITICAL

### **Bug 2: Max_states dừng sớm**
- **Hiện tượng:** max_states lớn → kết quả tệ
- **Kết quả:** 10000 states cho 92,989 thay vì 114,374
- **Mức độ:** 🟡 IMPORTANT

### **Bug 3: Không track best**
- **Hiện tượng:** Có thể bỏ lỡ solution tốt
- **Kết quả:** Không ổn định
- **Mức độ:** 🟢 NICE TO HAVE

---

## ✅ **Hành động:**

1. **Sửa heuristic function** (return -current_value)
2. **Sửa is_goal logic** (bỏ check max_states)
3. **Thêm best solution tracking**
4. **Test lại toàn bộ experiments**

**Dự đoán sau khi sửa:**
- GBFS sẽ đạt **70-90%** optimal (gần BPSO)
- Max_states lớn hơn → kết quả tốt hơn
- Ổn định và deterministic

---

## 🎯 **Kết luận:**

**Root cause:** Heuristic function sai dấu → GBFS minimize thay vì maximize

**Fix:** Đổi `return current_value` thành `return -current_value`

**Expected result:** GBFS sẽ hoạt động tốt hơn rất nhiều (từ 7% → 70-90%)
