# HƯỚNG DẪN VIỆT HÓA HOÀN CHỈNH PROJECT AI_GFBS_BPSO

## Tổng quan
Project đã được Việt hóa một phần. Dưới đây là tổng kết và hướng dẫn để hoàn thiện.

## ✅ ĐÃ HOÀN THÀNH

### 1. `src/visualization/advanced_visualizer.py`
- ✅ Việt hóa `plot_gbfs_parameter_impact()`:
  - Labels: "Số trạng thái tối đa", "Tổng giá trị", "Thời gian thực thi"
  - Titles: "Ảnh hưởng Max States đến chất lượng giải pháp"
  - Table headers: "Chỉ số", "Tốt nhất", "Tệ nhất"
  
- ✅ Việt hóa `plot_bpso_parameter_impact()`:
  - Labels: "Kích thước bầy đàn", "Vòng lặp", "Độ thích nghi"
  - Titles: "So sánh hội tụ", "Phân tích tốc độ hội tụ"
  
- ✅ Việt hóa `plot_algorithm_comparison_detailed()`:
  - Labels: "So sánh chất lượng giải pháp", "Chi phí tính toán", "Hiệu suất"
  - Table: "Thuật toán", "Giá trị", "% Tối ưu", "Xếp hạng"
  - Baselines: "GBFS (Tham lam)", "DP (Tối ưu)"

### 2. `src/visualization/step_by_step_visualizer.py`
- ✅ Việt hóa `visualize_gbfs_selection_steps()`:
  - "Chưa chọn", "Thứ tự lựa chọn", "Trọng lượng tích lũy vs Sức chứa"
  - "Top 20 vật phẩm theo tỷ lệ"
  
- ✅ Việt hóa `visualize_bpso_swarm_behavior()`:
  - "Hội tụ của BPSO", "Đa dạng bầy đàn (Khám phá)"
  - "Không gian giải pháp của BPSO", "Tốt nhất toàn cục"

## 🔄 CẦN HOÀN THIỆN

### 3. `gui/main_gui.py` (Chưa hoàn thành)
Việt hóa cần thiết:

```python
# Window title
self.setWindowTitle('Giải bài toán Knapsack - Tối ưu đa mục tiêu (GBFS | BPSO | DP)')

# Group headers
"Problem Definition" → "Định nghĩa bài toán"
"Test Case Selection" → "Chọn bộ test"
"Algorithm Parameters" → "Tham số thuật toán"
"Actions" → "Thao tác"

# Buttons
"RUN ALL ALGORITHMS" → "CHẠY TẤT CẢ THUẬT TOÁN"
"RUN CHAPTER 3 EXPERIMENTS" → "CHẠY THỰC NGHIỆM CHƯƠNG 3"
"EXPORT RESULTS" → "XUẤT KẾT QUẢ"
"Clear Selection" → "Xóa lựa chọn"
"Visualize Problem" → "Trực quan hóa bài toán"

# Tab names
"Problem" → "Bài toán"
"GBFS Flow" → "Quy trình GBFS"
"BPSO Swarm" → "Bầy đàn BPSO"
"Comparison" → "So sánh"
"Regional" → "Khu vực"
"Details" → "Chi tiết"
"Chapter 3" → "Chương 3"

# Info labels
"Click on items to manually select/deselect" → "Nhấp vào vật phẩm để chọn/bỏ chọn thủ công"
"GBFS Selection Process: Greedy selection by value/weight ratio" → 
  "Quá trình lựa chọn GBFS: Tham lam theo tỷ lệ giá trị/trọng lượng"
"BPSO Convergence & Swarm Behavior" → "Hội tụ & Hành vi bầy đàn BPSO"
"GBFS vs BPSO vs DP - Performance Comparison" → "So sánh hiệu năng: GBFS vs BPSO vs DP"
"Regional Diversity Analysis" → "Phân tích đa dạng khu vực"
"Detailed Solution - Selected Items" → "Giải pháp chi tiết - Vật phẩm đã chọn"
"Chapter 3: Experimental Analysis Results" → "Chương 3: Kết quả phân tích thực nghiệm"

# Status messages
"Ready" → "Sẵn sàng"
"Running" → "Đang chạy"
"Finished" → "Hoàn thành"
"Failed to load test case" → "Không tải được bộ test"
"Selected Item" → "Đã chọn vật phẩm"
"Deselected Item" → "Đã bỏ chọn vật phẩm"
"Loaded:" → "Đã tải:"
```

### 4. `experiment/chapter3/experiments.py` (Chưa hoàn thành)
Việt hóa print statements:

```python
# Section headers
"GBFS PARAMETER ANALYSIS - Max States Impact" →
  "PHÂN TÍCH THAM SỐ GBFS - Ảnh hưởng Max States"

"BPSO PARAMETER ANALYSIS - Swarm Size Impact" →
  "PHÂN TÍCH THAM SỐ BPSO - Ảnh hưởng kích thước bầy đàn"

# Progress messages
"Test Case:" → "Bộ test:"
"Items:" → "Số vật phẩm:"
"Capacity:" → "Sức chứa:"
"Testing max_states =" → "Đang test max_states ="
"Testing n_particles =" → "Đang test n_particles ="
"Run" → "Lần chạy"
"Value=" → "Giá trị="
"Time=" → "Thời gian="
"Mean Value:" → "Giá trị trung bình:"
"Mean Time:" → "Thời gian trung bình:"
"Saved CSV:" → "Đã lưu CSV:"
"Saved Chart:" → "Đã lưu biểu đồ:"
```

### 5. Jupyter Notebooks (5 files - Chưa hoàn thành)
Các notebooks cần Việt hóa:

#### 5.1. `1. Parameter.ipynb`
- Markdown cells: Việt hóa tiêu đề sections, mô tả
- Print statements: Việt hóa output messages
- Nhận xét phân tích: Đã được Việt hóa trước đó

#### 5.2. `2. Algo.ipynb`
- Tiêu đề: "3.1.2 ALGORITHM COMPARISON" → "3.1.2 SO SÁNH THUẬT TOÁN"
- Sections: "Single Test Case Analysis" → "Phân tích một bộ test"
- Labels plots: Việt hóa tất cả labels, legends, titles

#### 5.3. `3. Data.ipynb`
- Tiêu đề: "3.1.3 DATA CHARACTERISTICS ANALYSIS" → "3.1.3 PHÂN TÍCH ĐẶC ĐIỂM DỮ LIỆU"
- Sections: "Correlation Impact" → "Ảnh hưởng của tương quan"

#### 5.4. `4. Optimization.ipynb`
- Tiêu đề: "3.1.4 OPTIMIZATION & BEST PRACTICES" → "3.1.4 TỐI ƯU HÓA & THỰC HÀNH TỐT NHẤT"
- Decision tree labels: Việt hóa tất cả nodes

#### 5.5. `5. EnhancedAlgorithm.ipynb`
- Tiêu đề: "3.1.5 ENHANCED ALGORITHMS & HYBRID APPROACHES" →
  "3.1.5 THUẬT TOÁN CẢI TIẾN & PHƯƠNG PHÁP KẾT HỢP"
- Sections: "Hybrid GBFS + Local Search" → "GBFS kết hợp với tìm kiếm cục bộ"

## 📝 QUY TẮC VIỆT HÓA

### GIỮ NGUYÊN (Không dịch):
1. **Tên thuật toán**: GBFS, BPSO, DP, GA_TSP
2. **Tham số toán học**: w, c₁, c₂, n, capacity
3. **Thuật ngữ kỹ thuật đặc trưng**:
   - Knapsack (giữ nguyên hoặc "bài toán Knapsack")
   - Fitness (đôi khi dùng "độ thích nghi")
   - Swarm (đôi khi dùng "bầy đàn")
4. **Tên biến trong code**: selected_indices, total_value, etc.
5. **Định dạng file**: .csv, .ipynb, .py

### DỊCH SANG TIẾNG VIỆT:
1. **Labels trục đồ thị**: Weight → Trọng lượng, Value → Giá trị
2. **Tiêu đề plots**: "Solution Quality" → "Chất lượng giải pháp"
3. **Mô tả phân tích**: Dịch toàn bộ nhận xét, kết luận
4. **Messages GUI**: Dịch tất cả thông báo, nút bấm
5. **Table headers**: "Algorithm" → "Thuật toán", "Ranking" → "Xếp hạng"
6. **Nhận xét trong notebook**: Dịch markdown cells

### CÁCH DỊCH ƯU TIÊN:
- "Best" → "Tốt nhất" (không dùng "Cao nhất")
- "Optimal" → "Tối ưu" 
- "Execution Time" → "Thời gian thực thi"
- "Selected" → "Đã chọn"
- "Iteration" → "Vòng lặp"
- "Convergence" → "Hội tụ"
- "Analysis" → "Phân tích"
- "Comparison" → "So sánh"

## 🛠️ CÔNG CỤ HỖ TRỢ

### Script tự động (đã tạo):
`vietnamize_project.py` - Dùng để Việt hóa hàng loạt

### Manual check cần thiết:
1. Kiểm tra context để đảm bảo dịch đúng nghĩa
2. Đảm bảo format string không bị lỗi
3. Test hiển thị tiếng Việt có dấu trong plots
4. Kiểm tra độ dài text không bị tràn khung

## 📊 TIẾN ĐỘ

- [x] advanced_visualizer.py (70% - các hàm chính)
- [x] step_by_step_visualizer.py (100%)
- [ ] main_gui.py (0% - cần làm tiếp)
- [ ] experiments.py (0%)
- [ ] 1. Parameter.ipynb (50% - chỉ nhận xét)
- [ ] 2. Algo.ipynb (0%)
- [ ] 3. Data.ipynb (0%)
- [ ] 4. Optimization.ipynb (0%)
- [ ] 5. EnhancedAlgorithm.ipynb (0%)

## 🎯 ƯU TIÊN TIẾP THEO

1. **main_gui.py** - Quan trọng nhất vì người dùng tương tác trực tiếp
2. **5 notebooks** - Nội dung chính của chương 3
3. **experiments.py** - Print output khi chạy thực nghiệm
4. **Hoàn thiện advanced_visualizer.py** - Các hàm còn lại

## ✅ KIỂM TRA SAU VIỆT HÓA

```bash
# Test GUI
python run_gui.py

# Check hiển thị tiếng Việt
# - Tất cả labels, buttons có hiển thị đúng dấu?
# - Plot titles không bị cắt?
# - Table headers align đúng?

# Test notebooks
jupyter notebook experiment/chapter3/1.\ Parameter.ipynb

# Check markdown cells
# - Heading formats đúng?
# - Math equations không bị ảnh hưởng?
# - Code cells vẫn chạy được?
```

## 📚 THAM KHẢO

- Đã Việt hóa: `step_by_step_visualizer.py` - tham khảo cách dịch
- Font hỗ trợ tiếng Việt trong matplotlib: 'Segoe UI', 'Arial', 'DejaVu Sans'
- Encoding: Luôn dùng UTF-8

---
**Lưu ý**: Sau khi Việt hóa, nên test kỹ để đảm bảo:
1. Không có lỗi syntax
2. Hiển thị tiếng Việt có dấu đúng
3. Layout plots không bị lỗi do text dài hơn
4. Tất cả chức năng hoạt động bình thường
