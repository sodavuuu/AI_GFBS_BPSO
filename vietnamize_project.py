#!/usr/bin/env python3
"""
Script để Việt hóa toàn bộ project AI_GFBS_BPSO
"""

import re
import os
from pathlib import Path

# Mapping các cụm từ tiếng Anh sang tiếng Việt
TRANSLATIONS = {
    # General terms
    "Solution Quality": "Chất lượng giải pháp",
    "Computational Cost": "Chi phí tính toán",
    "Execution Time": "Thời gian thực thi",
    "Total Value": "Tổng giá trị",
    "Total Weight": "Tổng trọng lượng",
    "Capacity": "Sức chứa",
    "Weight": "Trọng lượng",
    "Value": "Giá trị",
    "Efficiency": "Hiệu suất",
    "Algorithm": "Thuật toán",
    "Iteration": "Vòng lặp",
    "Best Fitness": "Độ thích nghi tốt nhất",
    "Average Fitness": "Độ thích nghi trung bình",
    "Convergence": "Hội tụ",
    "Swarm Size": "Kích thước bầy đàn",
    "Number of Particles": "Số hạt",
    "Max Iterations": "Số vòng lặp tối đa",
    "Items": "Vật phẩm",
    "Selected": "Đã chọn",
    "Not Selected": "Chưa chọn",
    "Region": "Khu vực",
    "Category": "Danh mục",
    "Optimal": "Tối ưu",
    "Greedy": "Tham lam",
    
    # Plot titles
    "Impact of": "Ảnh hưởng của",
    "Comparison": "So sánh",
    "Analysis": "Phân tích",
    "vs": "vs",
    "Trade-off": "Đánh đổi",
    "Quality vs Speed": "Chất lượng vs Tốc độ",
    "Parameter": "Tham số",
    "Data Characteristics": "Đặc điểm dữ liệu",
    "Solution Map": "Bản đồ giải pháp",
    "Selection Process": "Quá trình lựa chọn",
    "Swarm Behavior": "Hành vi bầy đàn",
    "Regional Diversity": "Đa dạng khu vực",
    "Value Contribution": "Đóng góp giá trị",
    
    # Table headers
    "Metric": "Chỉ số",
    "Best": "Tốt nhất",
    "Worst": "Tệ nhất",
    "Range": "Khoảng",
    "Mean": "Trung bình",
    "Std": "Độ lệch chuẩn",
    "Time (s)": "Thời gian (s)",
    "Ranking": "Xếp hạng",
    "% of Optimal": "% Tối ưu",
    
    # Status messages
    "Running": "Đang chạy",
    "Finished": "Hoàn thành",
    "Error": "Lỗi",
    "Loading": "Đang tải",
    "Saved": "Đã lưu",
    "Failed": "Thất bại",
    
    # GUI elements
    "Click to": "Nhấp để",
    "Select": "Chọn",
    "Clear": "Xóa",
    "Export": "Xuất",
    "Run": "Chạy",
    "Visualize": "Trực quan hóa",
    "Details": "Chi tiết",
    "Summary": "Tóm tắt",
}

def vietnamize_file(filepath):
    """Việt hóa một file"""
    print(f"Processing: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Apply translations
    for eng, vie in TRANSLATIONS.items():
        # For plot labels, titles (in quotes)
        content = re.sub(rf"(['\"]){re.escape(eng)}(['\"])", rf"\1{vie}\2", content)
        # For f-strings
        content = re.sub(rf"f(['\"].*?){re.escape(eng)}(.*?['\"])", rf"f\1{vie}\2", content)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Updated")
    else:
        print(f"  - No changes")

def main():
    """Main function"""
    project_root = Path(__file__).parent
    
    # Files to process
    files_to_process = [
        "src/visualization/advanced_visualizer.py",
        "src/visualization/step_by_step_visualizer.py",
        "gui/main_gui.py",
        "experiment/chapter3/experiments.py",
    ]
    
    print("=== VIỆT HÓA PROJECT AI_GFBS_BPSO ===\n")
    
    for file_path in files_to_process:
        full_path = project_root / file_path
        if full_path.exists():
            vietnamize_file(full_path)
        else:
            print(f"File not found: {full_path}")
    
    print("\n=== HOÀN THÀNH ===")

if __name__ == "__main__":
    main()
