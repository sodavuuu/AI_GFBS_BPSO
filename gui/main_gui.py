"""
=================================================================================
KNAPSACK SOLVER - UNIFIED GUI (Version 2.0)
=================================================================================
Combines best features from both previous GUIs:
1. Interactive item selection (click to select)
2. Algorithm visualization (show selection process)
3. Chapter 3 experiments integration
4. Clean layout inspired by GA_TSP
=================================================================================
Problem: Multi-Objective 0/1 Knapsack
- Objective 1: Maximize total value
- Objective 2: Maximize regional diversity
- Constraint: Total weight ≤ Capacity

Algorithms:
- GBFS (Greedy Best-First Search): Fast heuristic
- BPSO (Binary Particle Swarm Optimization): Metaheuristic
- DP (Dynamic Programming): Optimal solution
=================================================================================
"""

import sys
import numpy as np
import pandas as pd
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QSpinBox, QDoubleSpinBox,
    QGroupBox, QTabWidget, QTableWidget, QTableWidgetItem,
    QProgressBar, QTextEdit, QMessageBox, QSplitter, QFrame
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import seaborn as sns

# Import algorithms and visualizers
from src.utils import TestCaseLoader
from src.algorithms import solve_knapsack_gbfs, solve_knapsack_bpso, solve_knapsack_dp
from src.visualization import (
    visualize_gbfs_selection_steps,
    visualize_bpso_swarm_behavior
)


# =============================================================================
# WORKER THREAD FOR ALGORITHMS
# =============================================================================

class AlgorithmWorker(QThread):
    """Worker thread to run algorithms without blocking GUI"""
    finished = pyqtSignal(dict)
    progress = pyqtSignal(str)
    
    def __init__(self, algorithm, items, capacity, params):
        super().__init__()
        self.algorithm = algorithm
        self.items = items
        self.capacity = capacity
        self.params = params
    
    def run(self):
        """Run algorithm in background"""
        try:
            self.progress.emit(f"Đang chạy {self.algorithm}...")
            
            # Extract item names, weights, values
            item_names = [item['name'] for item in self.items]
            weights = [item['weight'] for item in self.items]
            values = [item['value'] for item in self.items]
            
            if self.algorithm == "GBFS":
                result = solve_knapsack_gbfs(
                    item_names, weights, values, self.capacity,
                    max_states=self.params.get('max_states', 5000)
                )
            elif self.algorithm == "BPSO":
                result = solve_knapsack_bpso(
                    item_names, weights, values, self.capacity,
                    n_particles=self.params.get('n_particles', 30),
                    max_iterations=self.params.get('max_iterations', 50),
                    w=self.params.get('w', 0.7),
                    c1=self.params.get('c1', 2.0),
                    c2=self.params.get('c2', 2.0)
                )
            elif self.algorithm == "DP":
                result = solve_knapsack_dp(item_names, weights, values, self.capacity)
            else:
                raise ValueError(f"Unknown algorithm: {self.algorithm}")
            
            result['algorithm'] = self.algorithm
            self.finished.emit(result)
            
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            self.progress.emit(f"Lỗi: {str(e)}")
            self.finished.emit({'error': str(e), 'traceback': error_detail})


# =============================================================================
# INTERACTIVE CANVAS (Click to select items)
# =============================================================================

# =============================================================================
# MAIN GUI CLASS
# =============================================================================

class KnapsackSolverGUI(QMainWindow):
    """
    Unified Knapsack Solver GUI
    
    Layout:
    - Left (25%): Control Panel
    - Right (75%): Visualization Tabs
    """
    
    def __init__(self):
        super().__init__()
        
        # Data
        self.loader = TestCaseLoader()
        self.current_test_case = None
        self.test_data_df = None
        self.results = {}  # {algorithm: result_dict}
        self.workers = []  # Active worker threads
        
        # UI Setup
        self.init_ui()
        self.load_first_test_case()
    
    # =========================================================================
    # UI INITIALIZATION
    # =========================================================================
    
    def init_ui(self):
        """Initialize main UI"""
        self.setWindowTitle('Knapsack Solver - Multi-Objective Optimization (GBFS | BPSO | DP)')
        self.setGeometry(50, 50, 1600, 900)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Use QSplitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel (Control)
        left_panel = self.create_control_panel()
        left_panel.setMaximumWidth(400)
        splitter.addWidget(left_panel)
        
        # Right panel (Visualization)
        right_panel = self.create_visualization_panel()
        splitter.addWidget(right_panel)
        
        # Set initial sizes (25% - 75%)
        splitter.setSizes([400, 1200])
        
        # Main layout
        layout = QHBoxLayout(main_widget)
        layout.addWidget(splitter)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Status bar
        self.statusBar().showMessage('Ready')
    
    def create_control_panel(self):
        """Create left control panel"""
        panel = QWidget()
        panel.setStyleSheet("""
            QWidget {
                background-color: #f5f6fa;
                font-family: 'Segoe UI', Arial;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dcdde1;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QPushButton {
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # === HEADER ===
        header = QLabel("KNAPSACK SOLVER")
        header.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            background-color: #ecf0f1;
            padding: 12px;
            border-radius: 5px;
        """)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        subtitle = QLabel("Multi-Objective 0/1 Knapsack\n"
                         "f1: Doanh thu  |  f2: Đa dạng Khu vực")
        subtitle.setStyleSheet("font-size: 10px; color: #7f8c8d; padding: 3px;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        # === PROBLEM DEFINITION ===
        problem_group = QGroupBox("Định nghĩa Bài toán")
        problem_layout = QVBoxLayout()
        
        self.problem_info = QTextEdit()
        self.problem_info.setReadOnly(True)
        self.problem_info.setMaximumHeight(120)
        self.problem_info.setStyleSheet("""
            background-color: white;
            border: 1px solid #bdc3c7;
            border-radius: 3px;
            padding: 5px;
            font-size: 9px;
        """)
        problem_layout.addWidget(self.problem_info)
        
        problem_group.setLayout(problem_layout)
        layout.addWidget(problem_group)
        
        # === TEST CASE SELECTION ===
        testcase_group = QGroupBox("Chọn Trường hợp Kiểm thử")
        testcase_layout = QVBoxLayout()
        
        testcase_layout.addWidget(QLabel("Chọn Trường hợp Kiểm thử:"))
        self.testcase_combo = QComboBox()
        test_cases = self.loader.list_test_cases()
        self.testcase_combo.addItems(test_cases)
        self.testcase_combo.currentTextChanged.connect(self.on_testcase_changed)
        testcase_layout.addWidget(self.testcase_combo)
        
        self.testcase_info = QLabel()
        self.testcase_info.setStyleSheet("""
            background-color: #e8f5e9;
            padding: 8px;
            border-radius: 3px;
            font-size: 9px;
        """)
        self.testcase_info.setWordWrap(True)
        testcase_layout.addWidget(self.testcase_info)
        
        testcase_group.setLayout(testcase_layout)
        layout.addWidget(testcase_group)
        
        # === ALGORITHM PARAMETERS ===
        params_group = QGroupBox("Tham số Thuật toán")
        params_layout = QVBoxLayout()
        
        # GBFS
        params_layout.addWidget(QLabel("GBFS:"))
        gbfs_layout = QHBoxLayout()
        gbfs_layout.addWidget(QLabel("Trạng thái tối đa:"))
        self.gbfs_max_states = QSpinBox()
        self.gbfs_max_states.setRange(1000, 20000)
        self.gbfs_max_states.setValue(5000)
        self.gbfs_max_states.setSingleStep(1000)
        gbfs_layout.addWidget(self.gbfs_max_states)
        params_layout.addLayout(gbfs_layout)
        
        # BPSO
        params_layout.addWidget(QLabel("BPSO:"))
        
        bpso_particles_layout = QHBoxLayout()
        bpso_particles_layout.addWidget(QLabel("Số hạt:"))
        self.bpso_particles = QSpinBox()
        self.bpso_particles.setRange(10, 100)
        self.bpso_particles.setValue(30)
        bpso_particles_layout.addWidget(self.bpso_particles)
        params_layout.addLayout(bpso_particles_layout)
        
        bpso_iter_layout = QHBoxLayout()
        bpso_iter_layout.addWidget(QLabel("Số vòng lặp:"))
        self.bpso_iterations = QSpinBox()
        self.bpso_iterations.setRange(10, 200)
        self.bpso_iterations.setValue(50)
        bpso_iter_layout.addWidget(self.bpso_iterations)
        params_layout.addLayout(bpso_iter_layout)
        
        bpso_w_layout = QHBoxLayout()
        bpso_w_layout.addWidget(QLabel("Quán tính (w):"))
        self.bpso_w = QDoubleSpinBox()
        self.bpso_w.setRange(0.1, 1.0)
        self.bpso_w.setValue(0.7)
        self.bpso_w.setSingleStep(0.1)
        bpso_w_layout.addWidget(self.bpso_w)
        params_layout.addLayout(bpso_w_layout)
        
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)
        
        # === ACTION BUTTONS ===
        buttons_group = QGroupBox("Hành động")
        buttons_layout = QVBoxLayout()
        
        self.run_all_btn = QPushButton("CHẠY TẤT CẢ THUẬT TOÁN")
        self.run_all_btn.setStyleSheet("""
            background-color: #27ae60;
            color: white;
            font-size: 12px;
            padding: 10px;
        """)
        self.run_all_btn.clicked.connect(self.run_all_algorithms)
        buttons_layout.addWidget(self.run_all_btn)
        
        self.run_chapter3_btn = QPushButton("CHẠY THÍ NGHIỆM CHƯƠNG 3")
        self.run_chapter3_btn.setStyleSheet("""
            background-color: #e67e22;
            color: white;
            font-size: 11px;
        """)
        self.run_chapter3_btn.clicked.connect(self.run_chapter3_experiments)
        buttons_layout.addWidget(self.run_chapter3_btn)
        
        self.export_btn = QPushButton("XUẤT KẾT QUẢ")
        self.export_btn.setStyleSheet("""
            background-color: #3498db;
            color: white;
            font-size: 11px;
        """)
        self.export_btn.clicked.connect(self.export_results)
        buttons_layout.addWidget(self.export_btn)
        
        buttons_group.setLayout(buttons_layout)
        layout.addWidget(buttons_group)
        
        # === PROGRESS ===
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Stretch to push everything up
        layout.addStretch()
        
        return panel
    
    def create_visualization_panel(self):
        """Create right visualization panel with tabs"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Create tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #bdc3c7;
                background-color: white;
            }
            QTabBar::tab {
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        
        # Tab 0: Problem Statement
        self.tab_problem_statement = self.create_problem_statement_tab()
        self.tabs.addTab(self.tab_problem_statement, "Bài toán")
        
        # Tab 1: GBFS Algorithm Flow
        self.tab_gbfs = self.create_gbfs_tab()
        self.tabs.addTab(self.tab_gbfs, "Luồng GBFS")
        
        # Tab 3: BPSO Algorithm
        self.tab_bpso = self.create_bpso_tab()
        self.tabs.addTab(self.tab_bpso, "Bầy đàn BPSO")
        
        # Tab 4: Algorithm Comparison
        self.tab_comparison = self.create_comparison_tab()
        self.tabs.addTab(self.tab_comparison, "So sánh")
        
        # Tab 5: Regional Analysis
        self.tab_regional = self.create_regional_tab()
        self.tabs.addTab(self.tab_regional, "Khu vực")
        
        # Tab 6: Solution Details
        self.tab_solution = self.create_solution_tab()
        self.tabs.addTab(self.tab_solution, "Chi tiết")
        
        # Tab 7: Chapter 3 Results
        self.tab_chapter3 = self.create_chapter3_tab()
        self.tabs.addTab(self.tab_chapter3, "Chương 3")
        
        layout.addWidget(self.tabs)
        
        return panel
    
    # =========================================================================
    # TAB CREATION
    # =========================================================================
    
    def create_problem_statement_tab(self):
        """Tab 0: Detailed problem statement and objectives"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Create scrollable area for long content
        from PyQt5.QtWidgets import QScrollArea
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: white; }")
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(15)
        
        # === TITLE ===
        title = QLabel("BÀI TOÁN TỐI ƯU HÓA ĐA MỤC TIÊU")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #2c3e50;
            padding: 20px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                       stop:0 #3498db, stop:1 #2980b9);
            color: white;
            border-radius: 8px;
        """)
        title.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(title)
        
        # === PROBLEM DESCRIPTION ===
        problem_section = QLabel("""
<div style='background-color: #ecf0f1; padding: 20px; border-radius: 5px; border-left: 5px solid #3498db;'>
<h2 style='color: #2c3e50; margin-top: 0; font-size: 20px;'>Bài toán Cái túi 0/1 Đa mục tiêu (Multi-Objective 0/1 Knapsack)</h2>

<h3 style='color: #34495e; font-size: 17px;'>Bối cảnh thực tế:</h3>
<p style='font-size: 15px; line-height: 1.8;'>
Một công ty logistics cần lựa chọn hàng hóa để vận chuyển trong một chuyến xe với <b>sức chứa giới hạn</b>. 
Mỗi vật phẩm có <b>trọng lượng</b>, <b>giá trị thương mại</b>, và thuộc về một <b>khu vực địa lý</b> cụ thể.
</p>

<h3 style='color: #34495e; font-size: 17px;'>Dữ liệu đầu vào:</h3>
<ul style='font-size: 15px; line-height: 1.8;'>
<li><b>N vật phẩm</b> (items): Mỗi vật phẩm có:</li>
<ul>
    <li>Trọng lượng (weight): w<sub>i</sub></li>
    <li>Giá trị (value): v<sub>i</sub></li>
    <li>Khu vực (region): r<sub>i</sub> ∈ {1, 2, 3}</li>
    <li>Loại hàng (category): Điện tử, Quần áo, Thực phẩm, Nội thất</li>
</ul>
<li><b>Sức chứa xe tải</b> (capacity): W</li>
</ul>
</div>
        """)
        problem_section.setWordWrap(True)
        problem_section.setTextFormat(Qt.RichText)
        content_layout.addWidget(problem_section)
        
        # === OBJECTIVES ===
        objectives_section = QLabel("""
<div style='background-color: #e8f5e9; padding: 20px; border-radius: 5px; border-left: 5px solid #27ae60;'>
<h2 style='color: #27ae60; margin-top: 0; font-size: 20px;'>MỤC TIÊU TỐI ƯU HÓA (Đồng thời 2 mục tiêu)</h2>

<h3 style='color: #229954; font-size: 17px;'>Mục tiêu 1: Tối đa hóa Tổng giá trị (Maximize Revenue)</h3>
<p style='font-size: 15px; line-height: 1.8; padding-left: 20px;'>
<b>Công thức:</b> f₁(x) = Σ(v<sub>i</sub> × x<sub>i</sub>) → MAX<br>
<b>Ý nghĩa:</b> Tăng doanh thu bằng cách chọn những vật phẩm có giá trị cao<br>
<b>Trọng số:</b> 70% (ưu tiên chính)
</p>

<h3 style='color: #229954; font-size: 17px;'>Mục tiêu 2: Tối đa hóa Đa dạng Khu vực (Maximize Regional Diversity)</h3>
<p style='font-size: 15px; line-height: 1.8; padding-left: 20px;'>
<b>Công thức:</b> f₂(x) = Số khu vực khác nhau được chọn → MAX<br>
<b>Ý nghĩa:</b> Phân phối đều hàng hóa từ nhiều khu vực, giảm rủi ro tập trung<br>
<b>Trọng số:</b> 30% (mục tiêu phụ)<br>
<b>Lợi ích:</b> Cân bằng nguồn hàng, tăng khả năng phục hồi chuỗi cung ứng
</p>

<h3 style='color: #c0392b; font-size: 17px;'>Ràng buộc:</h3>
<p style='font-size: 15px; line-height: 1.8; padding-left: 20px;'>
<b>Công thức:</b> Σ(w<sub>i</sub> × x<sub>i</sub>) ≤ W<br>
<b>Ý nghĩa:</b> Tổng trọng lượng không vượt quá sức chứa xe<br>
<b>Biến quyết định:</b> x<sub>i</sub> ∈ {0, 1} (chọn hoặc không chọn)
</p>
</div>
        """)
        objectives_section.setWordWrap(True)
        objectives_section.setTextFormat(Qt.RichText)
        content_layout.addWidget(objectives_section)
        
        # === ALGORITHMS ===
        algorithms_section = QLabel("""
<div style='background-color: #fff3e0; padding: 20px; border-radius: 5px; border-left: 5px solid #e67e22;'>
<h2 style='color: #d35400; margin-top: 0; font-size: 20px;'>CÁC THUẬT TOÁN GIẢI QUYẾT</h2>

<h3 style='color: #d35400; font-size: 17px;'>1. GBFS - Greedy Best-First Search (Tham lam Ưu tiên Tốt nhất)</h3>
<ul style='font-size: 15px; line-height: 1.8;'>
<li><b>Ý tưởng:</b> Sắp xếp vật phẩm theo tỷ lệ giá trị/trọng lượng giảm dần, chọn lần lượt</li>
<li><b>Độ phức tạp:</b> O(n log n)</li>
<li><b>Ưu điểm:</b> Nhanh, đơn giản, hiệu quả với dữ liệu có tỷ lệ rõ ràng</li>
<li><b>Nhược điểm:</b> Không đảm bảo tối ưu toàn cục, có thể bỏ sót tổ hợp tốt hơn</li>
<li><b>Khi nào dùng:</b> Cần kết quả nhanh, dữ liệu lớn, chấp nhận sai số 5-15%</li>
</ul>

<h3 style='color: #d35400; font-size: 17px;'>2. BPSO - Binary Particle Swarm Optimization (Tối ưu Bầy đàn Nhị phân)</h3>
<ul style='font-size: 15px; line-height: 1.8;'>
<li><b>Ý tưởng:</b> Mô phỏng bầy đàn (30 hạt) tìm kiếm song song, học từ kinh nghiệm cá nhân và tập thể</li>
<li><b>Độ phức tạp:</b> O(particles × iterations × n) ~ O(1500n)</li>
<li><b>Ưu điểm:</b> Cân bằng khám phá/khai thác, tránh tối ưu cục bộ, xử lý tốt đa mục tiêu</li>
<li><b>Nhược điểm:</b> Chậm hơn GBFS, cần điều chỉnh tham số (w, c1, c2)</li>
<li><b>Khi nào dùng:</b> Cần chất lượng cao, dữ liệu phức tạp, có thời gian tính toán</li>
</ul>

<h3 style='color: #d35400; font-size: 17px;'>3. DP - Dynamic Programming (Quy hoạch Động)</h3>
<ul style='font-size: 15px; line-height: 1.8;'>
<li><b>Ý tưởng:</b> Tính toán tất cả trạng thái con, xây dựng bảng dp[n][W]</li>
<li><b>Độ phức tạp:</b> O(n × W)</li>
<li><b>Ưu điểm:</b> Đảm bảo tối ưu tuyệt đối cho mục tiêu đơn (giá trị)</li>
<li><b>Nhược điểm:</b> Chỉ tối ưu f₁, bỏ qua f₂ (regional diversity), chậm với W lớn</li>
<li><b>Khi nào dùng:</b> Bài toán nhỏ (n < 100, W < 10000), cần nghiệm chuẩn để so sánh</li>
</ul>
</div>
        """)
        algorithms_section.setWordWrap(True)
        algorithms_section.setTextFormat(Qt.RichText)
        content_layout.addWidget(algorithms_section)
        
        # === RESEARCH OBJECTIVES ===
        research_section = QLabel("""
<div style='background-color: #f3e5f5; padding: 20px; border-radius: 5px; border-left: 5px solid #8e44ad;'>
<h2 style='color: #8e44ad; margin-top: 0; font-size: 20px;'>MỤC ĐÍCH NGHIÊN CỨU (Chương 3)</h2>

<h3 style='color: #7d3c98; font-size: 17px;'>Phân tích So sánh:</h3>
<ul style='font-size: 15px; line-height: 1.8;'>
<li><b>Chất lượng nghiệm:</b> So sánh giá trị đạt được (f₁, f₂) của từng thuật toán</li>
<li><b>Thời gian thực thi:</b> Đo tốc độ GBFS vs BPSO vs DP</li>
<li><b>Độ ổn định:</b> Phân tích độ lệch chuẩn qua nhiều lần chạy (BPSO)</li>
<li><b>Khả năng mở rộng:</b> Kiểm tra hiệu suất với n = {30, 50, 100, 200}</li>
</ul>

<h3 style='color: #7d3c98; font-size: 17px;'>Điều chỉnh Tham số:</h3>
<ul style='font-size: 15px; line-height: 1.8;'>
<li><b>BPSO:</b> Tìm bộ tham số tối ưu (w, c₁, c₂, particles, iterations)</li>
<li><b>GBFS:</b> Thử nghiệm các chiến lược sắp xếp khác nhau</li>
<li><b>Trade-off:</b> Phân tích đánh đổi giữa thời gian và chất lượng</li>
</ul>

<h3 style='color: #7d3c98; font-size: 17px;'>Đặc điểm Dữ liệu:</h3>
<ul style='font-size: 15px; line-height: 1.8;'>
<li><b>Phân phối giá trị:</b> Ảnh hưởng của dữ liệu uniform vs skewed</li>
<li><b>Tương quan w-v:</b> Hiệu quả khi weight và value có/không tương quan</li>
<li><b>Khu vực:</b> Tác động của số lượng regions đến regional diversity</li>
</ul>

<h3 style='color: #7d3c98; font-size: 17px;'>Kết luận Kỳ vọng:</h3>
<ul style='font-size: 15px; line-height: 1.8;'>
<li>Xác định thuật toán phù hợp với từng kịch bản thực tế</li>
<li>Đưa ra khuyến nghị cài đặt tham số tối ưu</li>
<li>Chứng minh giá trị của multi-objective optimization trong logistics</li>
</ul>
</div>
        """)
        research_section.setWordWrap(True)
        research_section.setTextFormat(Qt.RichText)
        content_layout.addWidget(research_section)
        
        # Add stretch at the end
        content_layout.addStretch()
        
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        
        return tab
    
    def create_gbfs_tab(self):
        """Tab 2: GBFS algorithm flow"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Explanation section
        explanation = QLabel("""
<div style='background-color: #e8f5e9; padding: 15px; border-radius: 5px; border-left: 4px solid #27ae60;'>
<h3 style='color: #27ae60; margin-top: 0; font-size: 16px;'>Giải thích các biểu đồ GBFS (Tham lam Ưu tiên Tốt nhất):</h3>
<ul style='font-size: 14px; line-height: 1.8;'>
<li><b>Biểu đồ 1 - Thứ tự lựa chọn:</b> Hiển thị thứ tự vật phẩm được chọn (số càng nhỏ = chọn càng sớm). Mũi tên nối các điểm theo trình tự chọn. <i>Xanh = đã chọn, Xám = bỏ qua.</i></li>
<li><b>Biểu đồ 2 - Giá trị từng vật phẩm:</b> Đồ thị đường thể hiện giá trị của từng vật phẩm được chọn theo thứ tự. <i>Cao = vật phẩm giá trị lớn.</i></li>
<li><b>Biểu đồ 3 - Trọng lượng tích lũy:</b> Đường xanh tăng dần cho thấy trọng lượng cộng dồn. Đường đỏ là giới hạn sức chứa. <i>Diện tích xanh = trọng lượng đã dùng.</i></li>
<li><b>Biểu đồ 4 - Top 20 vật phẩm theo tỷ lệ:</b> Xếp hạng vật phẩm theo tỷ lệ giá trị/trọng lượng. <i>Xanh = được chọn, Xám = không được chọn (do hết sức chứa).</i></li>
</ul>
</div>
        """)
        explanation.setWordWrap(True)
        explanation.setTextFormat(Qt.RichText)
        layout.addWidget(explanation)
        
        self.gbfs_fig = Figure(figsize=(12, 9), facecolor='white')
        self.gbfs_canvas = FigureCanvas(self.gbfs_fig)
        self.gbfs_canvas.fig = self.gbfs_fig  # Add fig attribute
        layout.addWidget(self.gbfs_canvas)
        
        return tab
    
    def create_bpso_tab(self):
        """Tab 3: BPSO swarm behavior"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Explanation section
        explanation = QLabel("""
<div style='background-color: #e3f2fd; padding: 15px; border-radius: 5px; border-left: 4px solid #2196f3;'>
<h3 style='color: #1976d2; margin-top: 0; font-size: 16px;'>Giải thích các biểu đồ BPSO (Tối ưu Bầy đàn):</h3>
<ul style='font-size: 14px; line-height: 1.8;'>
<li><b>Biểu đồ 1 - Hội tụ BPSO:</b> Đường xanh (Độ thích nghi tốt nhất) tăng dần → thuật toán đang tìm được nghiệm tốt hơn. Đường đỏ (Độ thích nghi trung bình) dao động nhiều → bầy đàn đang khám phá. <i>Số cuối cùng = giá trị tốt nhất đạt được.</i></li>
<li><b>Biểu đồ 2 - Đa dạng Bầy đàn:</b> Biểu đồ tím cho thấy mức độ khác biệt giữa các hạt. <i>Cao = đang khám phá rộng, Thấp = đang hội tụ về nghiệm.</i></li>
<li><b>Biểu đồ 3 - Không gian Giải pháp:</b> Mỗi điểm xanh = 1 giải pháp tìm được bởi bầy đàn. Sao đỏ = giải pháp tốt nhất toàn cục. <i>Điểm càng phải trên = giá trị càng cao.</i></li>
</ul>
<p style='font-size: 13px; color: #555; margin-top: 10px;'><i>💡 Lưu ý: BPSO chạy ngẫu nhiên nên mỗi lần kết quả có thể khác nhau một chút.</i></p>
</div>
        """)
        explanation.setWordWrap(True)
        explanation.setTextFormat(Qt.RichText)
        layout.addWidget(explanation)
        
        self.bpso_fig = Figure(figsize=(12, 9), facecolor='white')
        self.bpso_canvas = FigureCanvas(self.bpso_fig)
        self.bpso_canvas.fig = self.bpso_fig  # Add fig attribute
        layout.addWidget(self.bpso_canvas)
        
        return tab
    
    def create_comparison_tab(self):
        """Tab 5: Algorithm comparison"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        info = QLabel("GBFS vs BPSO vs DP - So sánh Hiệu suất")
        info.setStyleSheet("background-color: #fff3e0; padding: 8px;")
        layout.addWidget(info)
        
        self.comparison_fig = Figure(figsize=(12, 9), facecolor='white')
        self.comparison_canvas = FigureCanvas(self.comparison_fig)
        self.comparison_canvas.fig = self.comparison_fig  # Add fig attribute
        layout.addWidget(self.comparison_canvas)
        
        return tab
    
    def create_regional_tab(self):
        """Tab 6: Regional diversity analysis"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        info = QLabel("Regional Diversity Analysis")
        info.setStyleSheet("background-color: #f3e5f5; padding: 8px;")
        layout.addWidget(info)
        
        self.regional_fig = Figure(figsize=(12, 9), facecolor='white')
        self.regional_canvas = FigureCanvas(self.regional_fig)
        self.regional_canvas.fig = self.regional_fig  # Add fig attribute
        layout.addWidget(self.regional_canvas)
        
        return tab
    
    def create_solution_tab(self):
        """Tab 7: Solution details table"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        info = QLabel("Detailed Solution - Selected Items")
        info.setStyleSheet("background-color: #e0f2f1; padding: 8px;")
        layout.addWidget(info)
        
        self.solution_table = QTableWidget()
        self.solution_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #bdc3c7;
                font-size: 10px;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 5px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.solution_table)
        
        return tab
    
    def create_chapter3_tab(self):
        """Tab 8: Chapter 3 experiment results"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        info = QLabel("Chapter 3: Experimental Analysis Results")
        info.setStyleSheet("background-color: #ede7f6; padding: 8px;")
        layout.addWidget(info)
        
        self.chapter3_fig = Figure(figsize=(12, 9), facecolor='white')
        self.chapter3_canvas = FigureCanvas(self.chapter3_fig)
        self.chapter3_canvas.fig = self.chapter3_fig  # Add fig attribute
        layout.addWidget(self.chapter3_canvas)
        
        # Experiment selection
        exp_layout = QHBoxLayout()
        exp_layout.addWidget(QLabel("Select Experiment:"))
        
        self.exp_combo = QComboBox()
        self.exp_combo.addItems([
            "3.1.1.a - GBFS Parameters",
            "3.1.1.b - BPSO Swarm Size",
            "3.1.1.c - BPSO Iterations",
            "3.1.2 - Algorithm Comparison",
            "3.1.3 - Data Characteristics"
        ])
        self.exp_combo.currentTextChanged.connect(self.load_experiment_result)
        exp_layout.addWidget(self.exp_combo)
        exp_layout.addStretch()
        
        layout.addLayout(exp_layout)
        
        return tab
    
    # =========================================================================
    # EVENT HANDLERS
    # =========================================================================
    
    def load_first_test_case(self):
        """Load first test case on startup"""
        if self.testcase_combo.count() > 0:
            first_test = self.testcase_combo.itemText(0)
            self.on_testcase_changed(first_test)
    
    def on_testcase_changed(self, test_name):
        """Handle test case selection change"""
        try:
            # Load test case
            self.current_test_case = self.loader.load_test_case(test_name)
            
            # Get test case info
            info = self.loader.get_test_case_info(test_name)
            
            # Load data as DataFrame
            filepath = self.loader.test_cases_dir / info['File']
            self.test_data_df = pd.read_csv(filepath)
            
            # Rename columns for compatibility
            if 'Quantity' in self.test_data_df.columns:
                self.test_data_df['weight'] = self.test_data_df['Quantity']
            if 'Total' in self.test_data_df.columns:
                self.test_data_df['value'] = self.test_data_df['Total']
            
            # Add region if not exists
            if 'region' not in self.test_data_df.columns:
                # Extract region from Region column or default to 1
                if 'Khu vực' in self.test_data_df.columns:
                    # Map region names to numbers
                    region_map = {}
                    for i, r in enumerate(self.test_data_df['Khu vực'].unique()):
                        region_map[r] = i + 1
                    self.test_data_df['region'] = self.test_data_df['Khu vực'].map(region_map)
                else:
                    self.test_data_df['region'] = 1
            
            # Update problem info
            self.update_problem_info(test_name, info)
            
            # Update test case info
            self.update_testcase_info(info)
            
            # Clear previous results
            self.results = {}
            
            self.statusBar().showMessage(f'Đã tải: {test_name}')
            
        except Exception as e:
            import traceback
            error_msg = f"Thất bại to load test case:\n{str(e)}\n\n{traceback.format_exc()}"
            QMessageBox.warning(self, "Lỗi", error_msg)
            print(error_msg)
    
    def update_problem_info(self, test_name, info):
        """Update problem definition text"""
        text = f"""<b>0/1 Knapsack Problem</b><br>
<b>Input:</b> n items (weight, value, region)<br>
<b>Constraint:</b> Total weight <= Capacity<br>
<b>Objective 1:</b> Maximize Sum value<br>
<b>Objective 2:</b> Maximize regional diversity<br>
<br>
<b>Current Test:</b> {test_name}<br>
<b>Items:</b> {info['N_Items']}<br>
<b>Capacity:</b> {info['Capacity']}<br>
<b>Regions:</b> {info['N_Regions']}
"""
        self.problem_info.setHtml(text)
    
    def update_testcase_info(self, info):
        """Update test case info label"""
        text = f"""Vật phẩm: {info['N_Items']} | Sức chứa: {info['Capacity']} | Khu vực: {info['N_Regions']} | Tổng giá trị: {int(info['Total_Value'])}"""
        self.testcase_info.setText(text)
    
    def run_all_algorithms(self):
        """Run all three algorithms"""
        if self.current_test_case is None:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn trường hợp kiểm thử trước!")
            return
        
        # Disable button and show progress
        self.run_all_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        
        # Clear previous results
        self.results = {}
        
        # Get parameters
        params = {
            'gbfs': {
                'max_states': self.gbfs_max_states.value(),
                'heuristic': 'value_weight_ratio'
            },
            'bpso': {
                'n_particles': self.bpso_particles.value(),
                'max_iterations': self.bpso_iterations.value(),
                'w': self.bpso_w.value(),
                'c1': 2.0,
                'c2': 2.0
            },
            'dp': {}
        }
        
        # Prepare items in correct format for algorithms
        items_for_algo = []
        for idx, row in self.test_data_df.iterrows():
            items_for_algo.append({
                'name': f'Item_{idx}',
                'weight': row['weight'],
                'value': row['value']
            })
        
        # Run algorithms sequentially
        algorithms = ['GBFS', 'BPSO', 'DP']
        
        try:
            for algo in algorithms:
                self.statusBar().showMessage(f'Đang chạy {algo}...')
                QApplication.processEvents()  # Update UI
                
                worker = AlgorithmWorker(
                    algo,
                    items_for_algo,
                    self.current_test_case['capacity'],
                    params[algo.lower()]
                )
                worker.finished.connect(self.on_algorithm_finished)
                worker.progress.connect(self.on_algorithm_progress)
                worker.start()
                
                # Wait for worker to finish (or use signals)
                worker.wait()
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Thuật toán execution failed:\n{str(e)}")
            self.run_all_btn.setEnabled(True)
            self.progress_bar.setVisible(False)
    def on_algorithm_progress(self, message):
        """Handle algorithm progress update"""
        self.statusBar().showMessage(message)
    
    def on_algorithm_finished(self, result):
        """Handle algorithm completion"""
        if 'error' in result:
            QMessageBox.critical(self, "Lỗi", f"Thuật toán failed:\n{result['error']}")
            return
        
        algo = result['algorithm']
        self.results[algo] = result
        
        self.statusBar().showMessage(f'{algo} completed: Giá trị={result.get("total_value", 0)}')
        
        # If all algorithms done
        if len(self.results) == 3:
            self.run_all_btn.setEnabled(True)
            self.progress_bar.setVisible(False)
            
            # Update visualizations
            self.update_all_visualizations()
            
            QMessageBox.information(self, "Success", 
                                  "All algorithms completed successfully!")
    
    def update_all_visualizations(self):
        """Update all visualization tabs after algorithms run"""
        try:
            # Update each tab
            self.visualize_gbfs_flow()
            self.visualize_bpso_behavior()
            self.visualize_comparison()
            self.visualize_regional()
            self.populate_solution_table()
            
        except Exception as e:
            print(f"Lỗi updating visualizations: {e}")
    
    def visualize_gbfs_flow(self):
        """Visualize GBFS selection process"""
        if 'GBFS' not in self.results:
            return
        
        try:
            visualize_gbfs_selection_steps(
                self.gbfs_canvas,
                self.results['GBFS'],
                self.test_data_df,
                self.current_test_case
            )
        except Exception as e:
            print(f"Lỗi visualizing GBFS: {e}")
            import traceback
            traceback.print_exc()
    
    def visualize_bpso_behavior(self):
        """Visualize BPSO swarm and convergence"""
        if 'BPSO' not in self.results:
            return
        
        try:
            visualize_bpso_swarm_behavior(
                self.bpso_canvas,
                self.results['BPSO'],
                self.test_data_df
            )
        except Exception as e:
            print(f"Lỗi visualizing BPSO: {e}")
            import traceback
            traceback.print_exc()
    
    def visualize_comparison(self):
        """Compare all three algorithms"""
        if len(self.results) < 3:
            return
        
        try:
            fig = self.comparison_canvas.fig
            fig.clear()
            
            # Create comparison plot
            algorithms = ['GBFS', 'BPSO', 'DP']
            values = [self.results[a]['total_value'] for a in algorithms]
            times = [self.results[a]['execution_time'] for a in algorithms]
            
            # Two subplots
            ax1 = fig.add_subplot(121)
            colors = ['#27ae60', '#3498db', '#e74c3c']
            ax1.bar(algorithms, values, color=colors, alpha=0.7)
            ax1.set_ylabel('Tổng giá trị')
            ax1.set_title('Chất lượng giải pháp')
            ax1.grid(True, alpha=0.3)
            
            ax2 = fig.add_subplot(122)
            ax2.bar(algorithms, times, color=colors, alpha=0.7)
            ax2.set_ylabel('Time (seconds)')
            ax2.set_title('Thời gian thực thi')
            ax2.grid(True, alpha=0.3)
            
            fig.tight_layout()
            self.comparison_canvas.draw()
            
        except Exception as e:
            print(f"Lỗi visualizing comparison: {e}")
    
    def visualize_regional(self):
        """Visualize regional diversity"""
        if len(self.results) == 0:
            return
        
        try:
            fig = self.regional_canvas.fig
            fig.clear()
            
            # Check if test data has region information
            if self.test_data_df is None or 'region' not in self.test_data_df.columns:
                ax = fig.add_subplot(111)
                ax.text(0.5, 0.5, 'No regional data available\nfor current test case',
                       ha='center', va='center', fontsize=14)
                self.regional_canvas.draw()
                return
            
            # Create 2x2 layout for regional analysis
            ax1 = fig.add_subplot(2, 2, 1)
            ax2 = fig.add_subplot(2, 2, 2)
            ax3 = fig.add_subplot(2, 2, 3)
            ax4 = fig.add_subplot(2, 2, 4)
            
            colors_algo = {'GBFS': '#27ae60', 'BPSO': '#3498db', 'DP': '#e74c3c'}
            
            # Plot 1: Regional distribution for each algorithm
            for algo, result in self.results.items():
                selected_indices = result['selected_indices']
                selected_regions = self.test_data_df.iloc[selected_indices]['region'].values
                
                region_counts = {}
                for r in selected_regions:
                    region_counts[r] = region_counts.get(r, 0) + 1
                
                regions = sorted(region_counts.keys())
                counts = [region_counts.get(r, 0) for r in regions]
                
                ax1.bar([f'R{r}' for r in regions], counts, alpha=0.6, label=algo, 
                       color=colors_algo.get(algo, 'gray'))
            
            ax1.set_xlabel('Khu vực', fontsize=10, fontweight='bold')
            ax1.set_ylabel('Number of Items', fontsize=10, fontweight='bold')
            ax1.set_title('Regional Distribution Comparison', fontsize=11, fontweight='bold')
            ax1.legend(fontsize=9)
            ax1.grid(True, alpha=0.3, axis='y')
            
            # Plot 2: Regional diversity score (Shannon entropy)
            diversity_scores = {}
            for algo, result in self.results.items():
                selected_indices = result['selected_indices']
                selected_regions = self.test_data_df.iloc[selected_indices]['region'].values
                
                # Calculate Shannon entropy
                from collections import Counter
                region_counts = Counter(selected_regions)
                total = len(selected_regions)
                entropy = 0
                for count in region_counts.values():
                    if count > 0:
                        p = count / total
                        entropy -= p * np.log2(p)
                
                diversity_scores[algo] = entropy
            
            algos = list(diversity_scores.keys())
            scores = list(diversity_scores.values())
            colors = [colors_algo.get(a, 'gray') for a in algos]
            
            ax2.bar(algos, scores, color=colors, alpha=0.7)
            ax2.set_ylabel('Shannon Entropy', fontsize=10, fontweight='bold')
            ax2.set_title('Regional Diversity Score', fontsize=11, fontweight='bold')
            ax2.grid(True, alpha=0.3, axis='y')
            
            # Add score labels
            for i, (algo, score) in enumerate(zip(algos, scores)):
                ax2.text(i, score, f'{score:.2f}', ha='center', va='bottom', fontweight='bold')
            
            # Plot 3: Items colored by region (all items)
            regions_all = self.test_data_df['region'].unique()
            cmap = plt.cm.get_cmap('tab10', len(regions_all))
            
            for i, region in enumerate(sorted(regions_all)):
                region_items = self.test_data_df[self.test_data_df['region'] == region]
                ax3.scatter(region_items['weight'], region_items['value'],
                           s=60, alpha=0.5, c=[cmap(i)], label=f'Khu vực {region}',
                           edgecolors='black', linewidth=0.5)
            
            ax3.set_xlabel('Trọng lượng', fontsize=10, fontweight='bold')
            ax3.set_ylabel('Giá trị', fontsize=10, fontweight='bold')
            ax3.set_title('All Items by Region', fontsize=11, fontweight='bold')
            ax3.legend(fontsize=8, loc='best', ncol=2)
            ax3.grid(True, alpha=0.3)
            
            # Plot 4: Selected items by best algorithm (colored by region)
            best_algo = max(self.results, key=lambda a: self.results[a]['total_value'])
            result = self.results[best_algo]
            selected_indices = result['selected_indices']
            
            # Show all items in gray
            ax4.scatter(self.test_data_df['weight'], self.test_data_df['value'],
                       s=50, alpha=0.2, c='gray', edgecolors='black', linewidth=0.5)
            
            # Show selected items colored by region
            selected_items = self.test_data_df.iloc[selected_indices]
            for i, region in enumerate(sorted(regions_all)):
                region_selected = selected_items[selected_items['region'] == region]
                if len(region_selected) > 0:
                    ax4.scatter(region_selected['weight'], region_selected['value'],
                               s=120, alpha=0.8, c=[cmap(i)], label=f'Khu vực {region}',
                               edgecolors='black', linewidth=2)
            
            ax4.set_xlabel('Trọng lượng', fontsize=10, fontweight='bold')
            ax4.set_ylabel('Giá trị', fontsize=10, fontweight='bold')
            ax4.set_title(f'{best_algo} Chọnion by Khu vực', fontsize=11, fontweight='bold')
            ax4.legend(fontsize=8, loc='best', ncol=2)
            ax4.grid(True, alpha=0.3)
            
            fig.tight_layout()
            self.regional_canvas.draw()
            
        except Exception as e:
            print(f"Lỗi visualizing regional: {e}")
            import traceback
            traceback.print_exc()
    
    def populate_solution_table(self):
        """Populate solution details table"""
        if len(self.results) == 0:
            return
        
        try:
            # Use best result (highest value)
            best_algo = max(self.results, key=lambda a: self.results[a]['total_value'])
            result = self.results[best_algo]
            
            selected_items = result['selected_items']
            
            # Setup table
            self.solution_table.setRowCount(len(selected_items))
            self.solution_table.setColumnCount(6)
            self.solution_table.setHorizontalHeaderLabels([
                'Item ID', 'Trọng lượng', 'Giá trị', 'Khu vực', 'Ratio', 'Thuật toán'
            ])
            
            # Populate rows
            for i, item_name in enumerate(selected_items):
                # Get item index
                idx = int(item_name.split('_')[1])
                row = self.test_data_df.iloc[idx]
                
                self.solution_table.setItem(i, 0, QTableWidgetItem(item_name))
                self.solution_table.setItem(i, 1, QTableWidgetItem(str(row['weight'])))
                self.solution_table.setItem(i, 2, QTableWidgetItem(str(row['value'])))
                self.solution_table.setItem(i, 3, QTableWidgetItem(str(row.get('region', 'N/A'))))
                
                ratio = row['value'] / row['weight'] if row['weight'] > 0 else 0
                self.solution_table.setItem(i, 4, QTableWidgetItem(f"{ratio:.2f}"))
                self.solution_table.setItem(i, 5, QTableWidgetItem(best_algo))
            
            self.solution_table.resizeColumnsToContents()
            
        except Exception as e:
            print(f"Lỗi populating table: {e}")
    
    def run_chapter3_experiments(self):
        """Run Chapter 3 experiments"""
        QMessageBox.information(self, "Chapter 3 Experiments",
                               "This will run all experiments for Chapter 3.\n"
                               "It may take several minutes.\n\n"
                               "Results will be saved in results/chapter3/")
        
        # TODO: Implement experiment runner
        # For now, just load existing results
        self.load_experiment_result(self.exp_combo.currentText())
    
    def load_experiment_result(self, exp_name):
        """Load and display experiment result from CSV files"""
        try:
            fig = self.chapter3_canvas.fig
            fig.clear()
            
            results_dir = Path(__file__).parent.parent / 'results' / 'chapter3'
            
            # Map experiment names to CSV files
            exp_files = {
                "3.1.1.a - GBFS Parameters": "3_1_1_a_gbfs_params.csv",
                "3.1.1.b - BPSO Swarm Size": "3_1_1_b_bpso_swarm_size.csv",
                "3.1.1.c - BPSO Iterations": "3_1_1_c_bpso_iterations.csv",
                "3.1.2 - Algorithm Comparison": "3_1_2_comparison_all_testcases.csv",
                "3.1.3 - Data Characteristics": "3_1_3_data_characteristics.csv"
            }
            
            if exp_name not in exp_files:
                ax = fig.add_subplot(111)
                ax.text(0.5, 0.5, f'Unknown experiment: {exp_name}',
                       ha='center', va='center', fontsize=14)
                self.chapter3_canvas.draw()
                return
            
            csv_file = results_dir / exp_files[exp_name]
            
            if not csv_file.exists():
                ax = fig.add_subplot(111)
                ax.text(0.5, 0.5, f'File not found:\n{csv_file.name}\\n\\nPlease run experiments first',
                       ha='center', va='center', fontsize=12, color='red')
                self.chapter3_canvas.draw()
                return
            
            # Load and visualize data
            df = pd.read_csv(csv_file)
            
            if "3.1.1.a" in exp_name:
                # GBFS Parameters: max_states vs performance
                ax = fig.add_subplot(111)
                ax.plot(df['max_states'], df['value'], 'bo-', linewidth=2, markersize=8, label='Giá trị')
                ax.set_xlabel('Max States', fontsize=12, fontweight='bold')
                ax.set_ylabel('Giá trị', fontsize=12, fontweight='bold', color='blue')
                ax.tick_params(axis='y', labelcolor='blue')
                ax.set_title('GBFS: Impact of Max States Parameter', fontsize=14, fontweight='bold')
                ax.grid(True, alpha=0.3)
                
                # Secondary y-axis for time
                ax2 = ax.twinx()
                ax2.plot(df['max_states'], df['time'], 'r^--', linewidth=2, markersize=8, label='Thời gian (s)')
                ax2.set_ylabel('Thời gian (s)', fontsize=12, fontweight='bold', color='red')
                ax2.tick_params(axis='y', labelcolor='red')
                
            elif "3.1.1.b" in exp_name:
                # BPSO Swarm Size
                ax = fig.add_subplot(111)
                ax.plot(df['param_value'], df['value'], 'go-', linewidth=2, markersize=8, label='Giá trị')
                ax.set_xlabel('Swarm Size (particles)', fontsize=12, fontweight='bold')
                ax.set_ylabel('Giá trị', fontsize=12, fontweight='bold', color='green')
                ax.tick_params(axis='y', labelcolor='green')
                ax.set_title('BPSO: Impact of Swarm Size', fontsize=14, fontweight='bold')
                ax.grid(True, alpha=0.3)
                
                # Secondary y-axis for time
                ax2 = ax.twinx()
                ax2.plot(df['param_value'], df['time'], 'r^--', linewidth=2, markersize=8, label='Thời gian (s)')
                ax2.set_ylabel('Thời gian (s)', fontsize=12, fontweight='bold', color='red')
                ax2.tick_params(axis='y', labelcolor='red')
                
            elif "3.1.1.c" in exp_name:
                # BPSO Iterations
                ax = fig.add_subplot(111)
                ax.plot(df['param_value'], df['value'], 'mo-', linewidth=2, markersize=8, label='Giá trị')
                ax.set_xlabel('Iterations', fontsize=12, fontweight='bold')
                ax.set_ylabel('Giá trị', fontsize=12, fontweight='bold', color='purple')
                ax.tick_params(axis='y', labelcolor='purple')
                ax.set_title('BPSO: Impact of Iteration Count', fontsize=14, fontweight='bold')
                ax.grid(True, alpha=0.3)
                
                # Secondary y-axis for time
                ax2 = ax.twinx()
                ax2.plot(df['param_value'], df['time'], 'r^--', linewidth=2, markersize=8, label='Thời gian (s)')
                ax2.set_ylabel('Thời gian (s)', fontsize=12, fontweight='bold', color='red')
                ax2.tick_params(axis='y', labelcolor='red')
                
            elif "3.1.2" in exp_name:
                # Algorithm Comparison
                ax1 = fig.add_subplot(121)
                
                # Calculate average across all test cases
                avg_gbfs = df['gbfs_value'].mean()
                avg_bpso = df['bpso_value'].mean()
                avg_dp = df['dp_value'].mean()
                
                algorithms = ['GBFS', 'BPSO', 'DP']
                values = [avg_gbfs, avg_bpso, avg_dp]
                colors = ['#27ae60', '#3498db', '#e74c3c']
                
                ax1.bar(algorithms, values, color=colors, alpha=0.7)
                ax1.set_ylabel('Average Value', fontsize=11, fontweight='bold')
                ax1.set_title('Solution Quality (All Test Cases)', fontsize=12, fontweight='bold')
                ax1.grid(True, alpha=0.3, axis='y')
                
                # Add value labels on bars
                for i, (algo, val) in enumerate(zip(algorithms, values)):
                    ax1.text(i, val, f'{val:.0f}', ha='center', va='bottom', fontweight='bold')
                
                ax2 = fig.add_subplot(122)
                
                avg_gbfs_time = df['gbfs_time'].mean()
                avg_bpso_time = df['bpso_time'].mean()
                avg_dp_time = df['dp_time'].mean()
                
                times = [avg_gbfs_time, avg_bpso_time, avg_dp_time]
                
                ax2.bar(algorithms, times, color=colors, alpha=0.7)
                ax2.set_ylabel('Average Time (s)', fontsize=11, fontweight='bold')
                ax2.set_title('Execution Time (All Test Cases)', fontsize=12, fontweight='bold')
                ax2.grid(True, alpha=0.3, axis='y')
                
                # Add time labels
                for i, (algo, t) in enumerate(zip(algorithms, times)):
                    ax2.text(i, t, f'{t:.4f}s', ha='center', va='bottom', fontweight='bold', fontsize=9)
                
            elif "3.1.3" in exp_name:
                # Data Characteristics - Compare performance across different data types
                ax1 = fig.add_subplot(121)
                ax2 = fig.add_subplot(122)
                
                # Plot 1: Solution Quality (% of optimal)
                characteristics = df['characteristic'].values
                gbfs_pct = df['gbfs_pct_optimal'].values
                bpso_pct = df['bpso_pct_optimal'].values
                
                x = range(len(characteristics))
                width = 0.35
                
                ax1.bar([i - width/2 for i in x], gbfs_pct, width, label='GBFS', color='#27ae60', alpha=0.7)
                ax1.bar([i + width/2 for i in x], bpso_pct, width, label='BPSO', color='#3498db', alpha=0.7)
                
                ax1.set_xlabel('Data Characteristic', fontsize=11, fontweight='bold')
                ax1.set_ylabel('% Tối ưu', fontsize=11, fontweight='bold')
                ax1.set_title('Solution Quality by Data Type', fontsize=12, fontweight='bold')
                ax1.set_xticks(x)
                ax1.set_xticklabels([c.replace('_', ' ').title() for c in characteristics], 
                                   rotation=45, ha='right', fontsize=9)
                ax1.legend(fontsize=10)
                ax1.grid(True, alpha=0.3, axis='y')
                ax1.set_ylim([0, 105])
                
                # Add value labels
                for i, (g, b) in enumerate(zip(gbfs_pct, bpso_pct)):
                    ax1.text(i - width/2, g + 1, f'{g:.1f}%', ha='center', va='bottom', fontsize=8)
                    ax1.text(i + width/2, b + 1, f'{b:.1f}%', ha='center', va='bottom', fontsize=8)
                
                # Plot 2: Execution Time
                gbfs_time = df['gbfs_time'].values * 1000  # Convert to ms
                bpso_time = df['bpso_time'].values * 1000
                dp_time = df['dp_time'].values * 1000
                
                ax2.bar([i - width for i in x], gbfs_time, width, label='GBFS', color='#27ae60', alpha=0.7)
                ax2.bar(x, bpso_time, width, label='BPSO', color='#3498db', alpha=0.7)
                ax2.bar([i + width for i in x], dp_time, width, label='DP', color='#e74c3c', alpha=0.7)
                
                ax2.set_xlabel('Data Characteristic', fontsize=11, fontweight='bold')
                ax2.set_ylabel('Time (ms)', fontsize=11, fontweight='bold')
                ax2.set_title('Execution Time by Data Type', fontsize=12, fontweight='bold')
                ax2.set_xticks(x)
                ax2.set_xticklabels([c.replace('_', ' ').title() for c in characteristics], 
                                   rotation=45, ha='right', fontsize=9)
                ax2.legend(fontsize=10)
                ax2.grid(True, alpha=0.3, axis='y')
            
            fig.tight_layout()
            self.chapter3_canvas.draw()
            
        except Exception as e:
            import traceback
            print(f"Lỗi loading experiment: {e}")
            traceback.print_exc()
            
            fig = self.chapter3_canvas.fig
            fig.clear()
            ax = fig.add_subplot(111)
            ax.text(0.5, 0.5, f'Lỗi loading experiment:\\n{str(e)}',
                   ha='center', va='center', fontsize=12, color='red')
            self.chapter3_canvas.draw()
    
    def export_results(self):
        """Export results to CSV"""
        if len(self.results) == 0:
            QMessageBox.warning(self, "Cảnh báo", "Không có kết quả để xuất!")
            return
        
        try:
            # Create results DataFrame
            data = []
            for algo, result in self.results.items():
                data.append({
                    'Thuật toán': algo,
                    'Tổng giá trị': result['total_value'],
                    'Tổng trọng lượng': result['total_weight'],
                    'Items Selected': len(result['selected_items']),
                    'Thời gian thực thi': result['execution_time']
                })
            
            df = pd.DataFrame(data)
            
            # Save to CSV
            output_path = Path('results') / 'latest_results.csv'
            output_path.parent.mkdir(exist_ok=True)
            df.to_csv(output_path, index=False)
            
            QMessageBox.information(self, "Success", 
                                   f"Results exported to:\n{output_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Xuất failed:\n{str(e)}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Set default font (use system font instead of Segoe UI)
    font = QFont('Arial', 10)
    # Set default font (use system font instead of Segoe UI)
    font = QFont('Arial', 10)
    app.setFont(font)
    
    # Create and show GUI
    gui = KnapsackSolverGUI()
    gui.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
