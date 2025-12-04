"""
=================================================================================
KNAPSACK SOLVER - GUI APPLICATION (PyQt5)
=================================================================================
Ứng dụng desktop để visualize và so sánh các thuật toán giải 0/1 Knapsack:
- GBFS (Greedy Best First Search)
- BPSO (Binary Particle Swarm Optimization)
- DP (Dynamic Programming - Optimal)

Tính năng:
1. Chọn loại dataset (4 tình huống test)
2. Tùy chỉnh parameters cho từng thuật toán
3. Chạy từng thuật toán hoặc tất cả
4. Hiển thị kết quả với color coding
5. So sánh gap với optimal
6. Visualize convergence curve (BPSO)
7. Export kết quả
=================================================================================
"""
import sys
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Import algorithms
from algorithms import (
    Item, KnapsackProblem, 
    GBFS_Solver, BPSO_Solver, DP_Solver,
    generate_dataset
)


# =================================================================================
# CLASS: MatplotlibCanvas - Widget để vẽ chart
# =================================================================================
class MatplotlibCanvas(FigureCanvas):
    """Canvas để nhúng matplotlib vào PyQt5"""
    
    def __init__(self, parent=None, width=10, height=8, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(fig)
        self.setParent(parent)
        # Không tạo axes trước, sẽ dùng gridspec trong plot function


# =================================================================================
# CLASS: KnapsackSolverGUI - Cửa sổ chính
# =================================================================================
class KnapsackSolverGUI(QMainWindow):
    """
    Ứng dụng GUI chính cho Knapsack Solver
    """
    
    def __init__(self):
        super().__init__()
        
        # Data
        self.problem = None
        self.results = {}  # Lưu kết quả từng thuật toán
        
        # Real-world scenarios data
        self.scenarios_data = self.init_scenarios()
        
        # UI Setup
        self.init_ui()
        
        # Show initial explanation
        self.show_algorithm_explanation()
    
    def init_scenarios(self):
        """Định nghĩa các tình huống thực tế - 2 GBFS thắng, 2 BPSO thắng"""
        return {
            # ===== TÌNH HUỐNG 1: GBFS THẮNG =====
            # Fractional knapsack với nhiều items - greedy optimal nhưng search space = 2^15
            0: {
                'name': 'Du Lịch Cuối Tuần - Đà Lạt 2 Ngày',
                'context': 'Ba lô 50kg, chọn đồ theo độ ưu tiên rõ ràng, nhiều lựa chọn',
                'capacity': 50,
                'winner': 'GBFS',
                'reason': 'Fractional knapsack với 15 items: Greedy picks top 5 items = optimal. BPSO search space 2^15=32768, với 20 iterations khó converge',
                'items': [
                    # Top 5 items = exactly 50kg, perfect greedy solution (value=400)
                    ('Thuốc khẩn cấp', 10, 100, 'Ratio=10.0, must-have'),
                    ('Sạc dự phòng', 10, 90, 'Ratio=9.0, essential'),
                    ('Áo khoác ấm', 10, 80, 'Ratio=8.0, Đà Lạt cold'),
                    ('Giày trekking', 10, 70, 'Ratio=7.0, walking'),
                    ('Đèn pin', 10, 60, 'Ratio=6.0, safety'),
                    # Decoy items - worse ratios
                    ('Dao đa năng', 11, 55, 'Ratio=5.0'),
                    ('Nước suối 2L', 12, 48, 'Ratio=4.0'),
                    ('Snack', 13, 39, 'Ratio=3.0'),
                    ('Khăn tắm', 14, 28, 'Ratio=2.0'),
                    ('Áo mưa', 15, 15, 'Ratio=1.0'),
                    ('Dù', 16, 16, 'Ratio=1.0'),
                    ('Chăn', 17, 17, 'Ratio=1.0'),
                    ('Gối', 18, 18, 'Ratio=1.0'),
                    ('Tất dự phòng', 19, 19, 'Ratio=1.0'),
                    ('Bao nylon', 20, 20, 'Ratio=1.0'),
                ]
            },
            
            # ===== TÌNH HUỐNG 2: BPSO THẮNG =====
            # 0/1 knapsack: greedy fails, need combination exploration
            1: {
                'name': 'Cướp Kho Báu Bảo Tàng',
                'context': 'Túi 20kg, đồ quý giá trị phức tạp',
                'capacity': 20,
                'winner': 'BPSO',
                'reason': 'Greedy trap: highest ratio item leads to suboptimal, need exploration',
                'items': [
                    # Classic greedy trap
                    ('Kim cương nhỏ', 1, 11, 'Ratio=11.0, greedy picks this'),  # Trap!
                    ('Vàng A', 10, 100, 'Ratio=10.0'),  # Should pick this
                    ('Vàng B', 10, 100, 'Ratio=10.0'),  # Should pick this
                    # Greedy: picks item 0 first (ratio=11), then 1+2 don't fit (need 20kg)
                    # Optimal: picks items 1+2 (value=200 vs 11)
                ]
            },
            
            # ===== TÌNH HUỐNG 3: GBFS THẮNG =====
            # Simple fractional với nhiều items
            2: {
                'name': 'Mua Sắm Flash Sale - Săn Deal Hot',
                'context': 'Budget 200k, nhiều món giảm giá, chọn deals tốt nhất',
                'capacity': 200,
                'winner': 'GBFS',
                'reason': 'Clear discount ranking với 12 items: Top 4 deals = optimal. BPSO search space 2^12=4096',
                'items': [
                    # Top 4 items = 200k exactly (value=400)
                    ('Áo khoác -70%', 50, 125, 'Ratio=2.5, best deal'),
                    ('Giày -60%', 50, 110, 'Ratio=2.2, great'),
                    ('Balo -50%', 50, 100, 'Ratio=2.0, good'),
                    ('Đồng hồ -40%', 50, 65, 'Ratio=1.3, ok'),
                    # Worse deals
                    ('Túi xách -30%', 40, 48, 'Ratio=1.2'),
                    ('Ví -20%', 35, 38, 'Ratio=1.09'),
                    ('Thắt lưng -15%', 30, 31, 'Ratio=1.03'),
                    ('Mũ -10%', 25, 25, 'Ratio=1.0'),
                    ('Găng tay -5%', 20, 19, 'Ratio=0.95'),
                    ('Tất -5%', 15, 14, 'Ratio=0.93'),
                    ('Khăn -3%', 10, 9, 'Ratio=0.9'),
                    ('Sticker -1%', 5, 4, 'Ratio=0.8'),
                ]
            },
            
            # ===== TÌNH HUỐNG 4: BPSO THẮNG =====
            # Complex combination problem
            3: {
                'name': 'Chuyển Nhà - Xe Tải Nhỏ',
                'context': 'Xe 50kg, nhiều đồ giá trị gần nhau',
                'capacity': 50,
                'winner': 'BPSO',
                'reason': 'Many items with similar ratios, many local optima, exploration wins',
                'items': [
                    # Many similar items - combination matters
                    ('Tủ lạnh', 20, 42, 'Ratio=2.1'),
                    ('TV', 15, 31, 'Ratio=2.07'),
                    ('Giường', 18, 38, 'Ratio=2.11'),
                    ('Bàn', 12, 25, 'Ratio=2.08'),
                    ('Ghế A', 8, 17, 'Ratio=2.12'),
                    ('Ghế B', 7, 15, 'Ratio=2.14'),
                    ('Kệ', 10, 21, 'Ratio=2.10'),
                    ('Tủ', 14, 29, 'Ratio=2.07'),
                    ('Quạt', 6, 13, 'Ratio=2.17'),
                    ('Đèn', 5, 11, 'Ratio=2.20'),
                ]
            }
        }
    
    def generate_real_scenario(self, scenario_idx):
        """Tạo problem từ tình huống thực tế"""
        scenario = self.scenarios_data[scenario_idx]
        
        items = []
        for i, (name, weight, value, desc) in enumerate(scenario['items']):
            # Keep original weights and values (no scaling needed)
            w = int(weight)
            v = int(value)
            
            item = Item(name, w, v)
            item.description = desc  # Add description attribute
            items.append(item)
        
        capacity = int(scenario['capacity'])
        
        from algorithms import KnapsackProblem
        problem = KnapsackProblem(items, capacity)
        problem.scenario_name = scenario['name']
        problem.scenario_context = scenario['context']
        problem.expected_winner = scenario['winner']
        problem.winner_reason = scenario['reason']
        
        return problem
    
    # =========================================================================
    # PHẦN 1: KHỞI TẠO GIAO DIỆN
    # =========================================================================
    def init_ui(self):
        """Khởi tạo giao diện"""
        self.setWindowTitle('Bài Toán Cái Túi - So Sánh GBFS, BPSO và DP')
        self.setGeometry(100, 100, 1600, 900)
        
        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Main layout: Horizontal (Left + Middle + Right)
        main_layout = QHBoxLayout(main_widget)
        
        # Left panel: Controls
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)
        
        # Middle panel: Results
        middle_panel = self.create_middle_panel()
        main_layout.addWidget(middle_panel, 2)
        
        # Right panel: Analysis & Explanation
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 1)
    
    def create_left_panel(self):
        """Tạo panel bên trái (controls)"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # ===== SECTION 0: Cách Hoạt Động =====
        how_group = QGroupBox("Cách Hoạt Động Thuật Toán")
        how_layout = QVBoxLayout()
        
        self.algo_explain_combo = QComboBox()
        self.algo_explain_combo.addItems(['GBFS', 'BPSO', 'DP'])
        self.algo_explain_combo.currentIndexChanged.connect(self.show_algorithm_explanation)
        how_layout.addWidget(self.algo_explain_combo)
        
        self.algo_explain_text = QTextEdit()
        self.algo_explain_text.setReadOnly(True)
        self.algo_explain_text.setMaximumHeight(200)
        how_layout.addWidget(self.algo_explain_text)
        
        how_group.setLayout(how_layout)
        layout.addWidget(how_group)
        
        # ===== SECTION 1: Dataset Configuration =====
        dataset_group = QGroupBox("Cấu Hình Bộ Dữ Liệu")
        dataset_layout = QVBoxLayout()
        
        # Mode selection: Real-world or Abstract
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Chế Độ:"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(['Tình Huống Thực Tế', 'Dataset Trừu Tượng'])
        self.mode_combo.currentIndexChanged.connect(self.on_mode_changed)
        mode_layout.addWidget(self.mode_combo)
        dataset_layout.addLayout(mode_layout)
        
        # Real-world scenario selector (initially visible)
        self.scenario_layout = QHBoxLayout()
        self.scenario_layout.addWidget(QLabel("Tình Huống:"))
        self.scenario_combo = QComboBox()
        self.scenario_combo.addItems([
            '🎒 Du Lịch Cuối Tuần (GBFS Thắng)',
            '💰 Cướp Kho Báu (BPSO Thắng)',
            '🛒 Mua Sắm Flash Sale (GBFS Thắng)',
            '📦 Chuyển Nhà Tiết Kiệm (BPSO Thắng)'
        ])
        self.scenario_combo.currentIndexChanged.connect(self.on_scenario_changed)
        self.scenario_layout.addWidget(self.scenario_combo)
        dataset_layout.addLayout(self.scenario_layout)
        
        # Abstract dataset type selector (initially hidden)
        self.abstract_layout = QHBoxLayout()
        self.abstract_label = QLabel("Loại Dữ Liệu:")
        self.abstract_layout.addWidget(self.abstract_label)
        self.dataset_combo = QComboBox()
        self.dataset_combo.addItems([
            'Random (Cân bằng)',
            'High Correlation (Khó cho GBFS)',
            'Outlier (Có bẫy)',
            'Similar Ratio (Tie-breaking)'
        ])
        self.abstract_layout.addWidget(self.dataset_combo)
        dataset_layout.addLayout(self.abstract_layout)
        
        # Hide abstract by default
        self.abstract_label.setVisible(False)
        self.dataset_combo.setVisible(False)
        
        # Number of items
        items_layout = QHBoxLayout()
        items_layout.addWidget(QLabel("Số Vật Phẩm:"))
        self.items_spin = QSpinBox()
        self.items_spin.setRange(5, 30)
        self.items_spin.setValue(15)
        items_layout.addWidget(self.items_spin)
        dataset_layout.addLayout(items_layout)
        
        # Capacity
        capacity_layout = QHBoxLayout()
        capacity_layout.addWidget(QLabel("Sức Chứa Túi:"))
        self.capacity_spin = QSpinBox()
        self.capacity_spin.setRange(50, 1000)
        self.capacity_spin.setValue(200)
        capacity_layout.addWidget(self.capacity_spin)
        dataset_layout.addLayout(capacity_layout)
        
        # Generate button
        self.gen_btn = QPushButton("Tạo Bộ Dữ Liệu")
        self.gen_btn.clicked.connect(self.generate_dataset_click)
        dataset_layout.addWidget(self.gen_btn)
        
        dataset_group.setLayout(dataset_layout)
        layout.addWidget(dataset_group)
        
        # ===== SECTION 2: Algorithm Parameters =====
        algo_group = QGroupBox("Tham Số Thuật Toán")
        algo_layout = QVBoxLayout()
        
        # GBFS parameters
        algo_layout.addWidget(QLabel("<b>Tham Số GBFS:</b>"))
        
        max_states_layout = QHBoxLayout()
        max_states_layout.addWidget(QLabel("Giới Hạn States:"))
        self.max_states_spin = QSpinBox()
        self.max_states_spin.setRange(1000, 50000)
        self.max_states_spin.setValue(10000)
        self.max_states_spin.setSingleStep(1000)
        max_states_layout.addWidget(self.max_states_spin)
        algo_layout.addLayout(max_states_layout)
        
        algo_layout.addWidget(QLabel("─" * 30))
        
        # BPSO parameters
        algo_layout.addWidget(QLabel("<b>Tham Số BPSO:</b>"))
        
        particles_layout = QHBoxLayout()
        particles_layout.addWidget(QLabel("Số Hạt (Particles):"))
        self.particles_spin = QSpinBox()
        self.particles_spin.setRange(10, 100)
        self.particles_spin.setValue(20)
        particles_layout.addWidget(self.particles_spin)
        algo_layout.addLayout(particles_layout)
        
        iterations_layout = QHBoxLayout()
        iterations_layout.addWidget(QLabel("Số Vòng Lặp:"))
        self.iterations_spin = QSpinBox()
        self.iterations_spin.setRange(10, 200)
        self.iterations_spin.setValue(10)
        iterations_layout.addWidget(self.iterations_spin)
        algo_layout.addLayout(iterations_layout)
        
        algo_group.setLayout(algo_layout)
        layout.addWidget(algo_group)
        
        # ===== SECTION 3: Run Algorithms =====
        run_group = QGroupBox("Chạy Thuật Toán")
        run_layout = QVBoxLayout()
        
        self.gbfs_btn = QPushButton("Chỉ Chạy GBFS")
        self.gbfs_btn.clicked.connect(lambda: self.run_algorithm('gbfs'))
        self.gbfs_btn.setEnabled(False)
        run_layout.addWidget(self.gbfs_btn)
        
        self.bpso_btn = QPushButton("Chỉ Chạy BPSO")
        self.bpso_btn.clicked.connect(lambda: self.run_algorithm('bpso'))
        self.bpso_btn.setEnabled(False)
        run_layout.addWidget(self.bpso_btn)
        
        self.dp_btn = QPushButton("Chỉ Chạy DP (Tối Ưu)")
        self.dp_btn.clicked.connect(lambda: self.run_algorithm('dp'))
        self.dp_btn.setEnabled(False)
        run_layout.addWidget(self.dp_btn)
        
        run_layout.addWidget(QLabel("─" * 30))
        
        self.run_all_btn = QPushButton("Chạy Tất Cả Thuật Toán")
        self.run_all_btn.clicked.connect(self.run_all_algorithms)
        self.run_all_btn.setEnabled(False)
        self.run_all_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        run_layout.addWidget(self.run_all_btn)
        
        run_group.setLayout(run_layout)
        layout.addWidget(run_group)
        
        # ===== SECTION 4: Dataset Info =====
        info_group = QGroupBox("Thông Tin Dữ Liệu")
        info_layout = QVBoxLayout()
        
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setMaximumHeight(150)
        self.info_text.setPlainText("Chưa tạo bộ dữ liệu.\nNhấn 'Tạo Bộ Dữ Liệu' để bắt đầu.")
        info_layout.addWidget(self.info_text)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Spacer
        layout.addStretch()
        
        return panel
    
    def create_middle_panel(self):
        """Tạo panel giữa (results)"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # ===== SECTION 1: Results Table =====
        results_group = QGroupBox("So Sánh Kết Quả")
        results_layout = QVBoxLayout()
        
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels([
            'Chỉ Số', 'GBFS', 'BPSO', 'DP (Tối Ưu)'
        ])
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.setAlternatingRowColors(True)
        
        results_layout.addWidget(self.results_table)
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)
        
        # ===== SECTION 2: Visualization =====
        viz_group = QGroupBox("Biểu Đồ So Sánh & Phân Tích")
        viz_layout = QVBoxLayout()
        
        self.canvas = MatplotlibCanvas(self, width=10, height=8, dpi=100)
        viz_layout.addWidget(self.canvas)
        
        viz_group.setLayout(viz_layout)
        layout.addWidget(viz_group)
        
        # ===== SECTION 2.5: Process Visualization =====
        process_group = QGroupBox("Minh Họa Quá Trình Giải")
        process_layout = QVBoxLayout()
        
        self.process_text = QTextEdit()
        self.process_text.setReadOnly(True)
        self.process_text.setMaximumHeight(200)
        self.process_text.setPlainText("Chạy thuật toán để xem quá trình giải từng bước...")
        process_layout.addWidget(self.process_text)
        
        process_group.setLayout(process_layout)
        layout.addWidget(process_group)
        
        return panel
    
    def create_right_panel(self):
        """Tạo panel bên phải (phân tích & giải thích)"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # ===== SECTION 1: Phân Tích Tự Động =====
        analysis_group = QGroupBox("Phân Tích Kết Quả")
        analysis_layout = QVBoxLayout()
        
        self.analysis_text = QTextEdit()
        self.analysis_text.setReadOnly(True)
        self.analysis_text.setMinimumHeight(250)
        self.analysis_text.setPlainText("Chạy thuật toán để xem phân tích tự động...")
        analysis_layout.addWidget(self.analysis_text)
        
        analysis_group.setLayout(analysis_layout)
        layout.addWidget(analysis_group)
        
        # ===== SECTION 2: Giải Thích Chi Tiết =====
        explain_group = QGroupBox("Giải Thích & Khuyến Nghị")
        explain_layout = QVBoxLayout()
        
        self.explain_text = QTextEdit()
        self.explain_text.setReadOnly(True)
        self.explain_text.setMinimumHeight(250)
        self.explain_text.setHtml("""
<b>Hướng dẫn sử dụng:</b><br>
<br>
1. <b>Tạo Dataset:</b> Chọn loại và tạo dữ liệu<br>
2. <b>Chạy Thuật Toán:</b> Click "Chạy Tất Cả"<br>
3. <b>Xem Phân Tích:</b> Hệ thống tự động giải thích<br>
<br>
<b>Các loại dataset:</b><br>
• <b>Random:</b> GBFS thường thắng (nhanh & chính xác)<br>
• <b>High Correlation:</b> GBFS yếu, BPSO mạnh<br>
• <b>Outlier:</b> Test khả năng tránh bẫy<br>
• <b>Similar Ratio:</b> Test tie-breaking<br>
        """)
        explain_layout.addWidget(self.explain_text)
        
        explain_group.setLayout(explain_layout)
        layout.addWidget(explain_group)
        
        # ===== SECTION 3: Selected Items =====
        items_group = QGroupBox("Vật Phẩm Được Chọn")
        items_layout = QVBoxLayout()
        
        self.items_text = QTextEdit()
        self.items_text.setReadOnly(True)
        self.items_text.setMaximumHeight(200)
        items_layout.addWidget(self.items_text)
        
        items_group.setLayout(items_layout)
        layout.addWidget(items_group)
        
        return panel
    
    def show_algorithm_explanation(self):
        """Hiển thị giải thích thuật toán"""
        algo = self.algo_explain_combo.currentText()
        
        explanations = {
            'GBFS': """
<b>GBFS - Greedy Best First Search (Tìm Kiếm Tham Lam)</b><br>
<br>
<b>Ý tưởng:</b> Luôn chọn item "hứa hẹn" nhất<br>
<br>
<b>Các bước:</b><br>
1. Bắt đầu với túi rỗng<br>
2. Tính heuristic cho mỗi item:<br>
   h(item) = Fractional Bound (giá trị tối đa có thể)<br>
3. Chọn item có h() cao nhất<br>
4. Lặp lại cho đến khi đầy<br>
<br>
<b>Ví dụ:</b><br>
Items: A(w=10,v=60), B(w=20,v=100), C(w=30,v=120)<br>
Capacity: 50, Ratio: A=6.0, B=5.0, C=4.0<br>
→ Chọn A → Chọn B → Dừng<br>
→ Kết quả: [A,B], value=160<br>
<br>
<b>Ưu điểm:</b> Nhanh (milliseconds)<br>
<b>Nhược điểm:</b> Có thể sai với dataset phức tạp
            """,
            'BPSO': """
<b>BPSO - Binary Particle Swarm Optimization (Đàn Hạt)</b><br>
<br>
<b>Ý tưởng:</b> Mô phỏng đàn chim tìm thức ăn<br>
<br>
<b>Các bước:</b><br>
1. Khởi tạo 20 hạt (solutions ngẫu nhiên)<br>
   Mỗi hạt = [1,0,1,0,...] (1=chọn, 0=không)<br>
<br>
2. Mỗi vòng lặp:<br>
   • Đánh giá fitness mỗi hạt<br>
   • Cập nhật pbest (best cá nhân)<br>
   • Cập nhật gbest (best toàn đàn)<br>
   • Các hạt "bay" về phía gbest<br>
<br>
3. Sau 50 vòng → gbest là solution<br>
<br>
<b>Ví dụ:</b><br>
Iter 0: Hạt ngẫu nhiên → gbest=[1,1,0], value=160<br>
Iter 25: Hội tụ → gbest=[1,0,1], value=180<br>
Iter 50: Stable → Kết quả=[1,0,1]<br>
<br>
<b>Ưu điểm:</b> Tránh bẫy, tìm được solution tốt<br>
<b>Nhược điểm:</b> Chậm hơn GBFS
            """,
            'DP': """
<b>DP - Dynamic Programming (Quy Hoạch Động)</b><br>
<br>
<b>Ý tưởng:</b> Tính tất cả khả năng, chọn tối ưu<br>
<br>
<b>Các bước:</b><br>
1. Tạo bảng DP[i][w]:<br>
   DP[i][w] = Giá trị tối đa với i items, capacity w<br>
<br>
2. Công thức:<br>
   DP[i][w] = max(<br>
     DP[i-1][w],         // Không chọn item i<br>
     DP[i-1][w-wi] + vi  // Chọn item i<br>
   )<br>
<br>
3. Backtrack để tìm items được chọn<br>
<br>
<b>Ví dụ:</b><br>
Items: A(w=10,v=60), B(w=20,v=100), Cap=30<br>
Bảng: DP[0][30]=0 → DP[1][30]=60 → DP[2][30]=160<br>
Backtrack → Chọn [A,B]<br>
<br>
<b>Ưu điểm:</b> 100% optimal, chắc chắn<br>
<b>Nhược điểm:</b> Chậm với dataset lớn
            """
        }
        
        self.algo_explain_text.setHtml(explanations[algo])
    
    # =========================================================================
    # PHẦN 2: XỬ LÝ SỰ KIỆN
    # =========================================================================
    def on_mode_changed(self):
        """Xử lý khi đổi chế độ Real-world/Abstract"""
        is_real = self.mode_combo.currentIndex() == 0
        
        # Show/hide appropriate controls
        for i in range(self.scenario_layout.count()):
            widget = self.scenario_layout.itemAt(i).widget()
            if widget:
                widget.setVisible(is_real)
        
        self.abstract_label.setVisible(not is_real)
        self.dataset_combo.setVisible(not is_real)
        
        # Update items/capacity controls
        if is_real:
            # Fixed by scenario
            self.items_spin.setEnabled(False)
            self.capacity_spin.setEnabled(False)
            self.on_scenario_changed()
        else:
            # User configurable
            self.items_spin.setEnabled(True)
            self.capacity_spin.setEnabled(True)
    
    def on_scenario_changed(self):
        """Cập nhật parameters khi đổi tình huống"""
        scenarios = {
            0: {'items': 15, 'capacity': 50},    # Du lịch - fractional với nhiều items
            1: {'items': 3, 'capacity': 20},     # Cướp - greedy trap
            2: {'items': 12, 'capacity': 200},   # Flash sale - nhiều deals
            3: {'items': 10, 'capacity': 50}     # Chuyển nhà - complex
        }
        
        idx = self.scenario_combo.currentIndex()
        config = scenarios[idx]
        
        self.items_spin.setValue(config['items'])
        self.capacity_spin.setValue(config['capacity'])
    
    def generate_dataset_click(self):
        """Xử lý khi click Generate Dataset"""
        is_real = self.mode_combo.currentIndex() == 0
        
        try:
            if is_real:
                # Generate real-world scenario
                scenario_idx = self.scenario_combo.currentIndex()
                self.problem = self.generate_real_scenario(scenario_idx)
            else:
                # Generate abstract dataset
                dataset_types = {
                    0: 'random',
                    1: 'high_correlation',
                    2: 'outlier',
                    3: 'similar_ratio'
                }
                dataset_type = dataset_types[self.dataset_combo.currentIndex()]
                n_items = self.items_spin.value()
                capacity = self.capacity_spin.value()
                
                self.problem = generate_dataset(
                    n_items=n_items,
                    max_value=100,
                    max_weight=50,
                    capacity=capacity,
                    seed=42,
                    dataset_type=dataset_type
                )
                
            # Hiển thị info
            self.display_dataset_info()
            
            # Enable buttons
            self.gbfs_btn.setEnabled(True)
            self.bpso_btn.setEnabled(True)
            self.dp_btn.setEnabled(True)
            self.run_all_btn.setEnabled(True)
            
            # Clear previous results
            self.results = {}
            self.results_table.setRowCount(0)
            self.items_text.clear()
            self.analysis_text.clear()
            
            # Success message
            if is_real:
                msg = f"Tình huống: {self.problem.scenario_name}\n"
                msg += f"{self.problem.scenario_context}\n"
                msg += f"{self.problem.n_items} vật phẩm, giới hạn = {self.problem.capacity}"
            else:
                msg = f"Tạo dữ liệu thành công!\n{self.problem.n_items} vật phẩm, sức chứa = {self.problem.capacity}"
            
            QMessageBox.information(self, "Thành Công", msg)
        
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tạo dữ liệu:\n{str(e)}")
    
    def display_dataset_info(self):
        """Hiển thị thông tin dataset"""
        values = np.array([item.value for item in self.problem.items])
        weights = np.array([item.weight for item in self.problem.items])
        ratios = np.array([item.ratio for item in self.problem.items])
        
        # Check if real-world scenario
        is_scenario = hasattr(self.problem, 'scenario_name')
        
        if is_scenario:
            info = f"""
<b>TÌNH HUỐNG:</b><br>
<h3 style='color: #2196F3;'>{self.problem.scenario_name}</h3>
<p style='background: #f0f0f0; padding: 8px; border-radius: 4px;'>
<i>{self.problem.scenario_context}</i>
</p>
<br>
<b>Danh Sách Vật Phẩm:</b><br>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━<br>
"""
            for i, item in enumerate(self.problem.items, 1):
                desc = getattr(item, 'description', '')
                info += f"{i}. <b>{item.name}</b><br>"
                info += f"   Nặng: {item.weight}, Giá trị: {item.value}, Ratio: {item.ratio:.2f}<br>"
                if desc:
                    info += f"   <i style='color: #666;'>{desc}</i><br>"
                info += "<br>"
            
            info += f"<br><b>Giới hạn:</b> {self.problem.capacity}<br>"
        else:
            # Abstract dataset
            info = f"""
<b>Thông Tin Bộ Dữ Liệu:</b><br>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━<br>
Số Vật Phẩm: {self.problem.n_items}<br>
Sức Chứa Túi: {self.problem.capacity}<br>
<br>
<b>Thống Kê:</b><br>
• Giá Trị: min={values.min()}, max={values.max()}, tb={values.mean():.1f}<br>
• Trọng Lượng: min={weights.min()}, max={weights.max()}, tb={weights.mean():.1f}<br>
• Tỷ Lệ (v/w): tb={ratios.mean():.2f}, độ lệch chuẩn={ratios.std():.2f}<br>
<br>
<b>Top 3 vật phẩm (theo tỷ lệ):</b><br>
"""
            # Sort by ratio
            items_sorted = sorted(self.problem.items, key=lambda x: x.ratio, reverse=True)
            for i, item in enumerate(items_sorted[:3]):
                info += f"{i+1}. {item.name}: w={item.weight}, v={item.value}, r={item.ratio:.2f}<br>"
        
        self.info_text.setHtml(info)
    
    def run_algorithm(self, algo_name):
        """Chạy một thuật toán"""
        if not self.problem:
            QMessageBox.warning(self, "Cảnh Báo", "Vui lòng tạo dữ liệu trước!")
            return
        
        try:
            # Progress dialog
            progress = QProgressDialog(f"Đang chạy {algo_name.upper()}...", None, 0, 0, self)
            progress.setWindowModality(Qt.WindowModal)
            progress.show()
            QApplication.processEvents()
            
            # Đo thời gian
            import time
            start_time = time.time()
            
            # Run algorithm
            if algo_name == 'gbfs':
                # Sử dụng max_states từ UI
                max_states = self.max_states_spin.value()
                solver = GBFS_Solver(self.problem, max_states=max_states)
                result = solver.solve()
            elif algo_name == 'bpso':
                solver = BPSO_Solver(
                    self.problem,
                    n_particles=self.particles_spin.value(),
                    max_iterations=self.iterations_spin.value()
                )
                result = solver.solve(verbose=False)
            elif algo_name == 'dp':
                if self.problem.n_items > 25:
                    QMessageBox.warning(self, "Cảnh Báo", 
                                      "Dữ liệu quá lớn cho DP (>25 vật phẩm).\nCó thể mất nhiều thời gian...")
                solver = DP_Solver(self.problem)
                result = solver.solve()
            
            # Lưu thời gian chạy
            elapsed_time = time.time() - start_time
            result['execution_time'] = elapsed_time
            
            # Save result
            self.results[algo_name] = result
            
            # Update display
            self.update_results_display()
            
            progress.close()
            
            QMessageBox.information(self, "Thành Công", 
                                  f"{algo_name.upper()} hoàn thành!\nGiá trị = {result['total_value']}")
        
        except Exception as e:
            progress.close()
            QMessageBox.critical(self, "Lỗi", f"Không thể chạy {algo_name.upper()}:\n{str(e)}")
    
    def run_all_algorithms(self):
        """Chạy tất cả thuật toán"""
        if not self.problem:
            QMessageBox.warning(self, "Cảnh Báo", "Vui lòng tạo dữ liệu trước!")
            return
        
        # Check DP
        if self.problem.n_items > 25:
            reply = QMessageBox.question(
                self, 'Dữ Liệu Lớn',
                'Dữ liệu có > 25 vật phẩm. DP có thể chậm.\nVẫn chạy?',
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
        
        try:
            progress = QProgressDialog("Đang chạy tất cả thuật toán...", None, 0, 3, self)
            progress.setWindowModality(Qt.WindowModal)
            
            # GBFS
            progress.setValue(0)
            progress.setLabelText("Đang chạy GBFS...")
            QApplication.processEvents()
            self.run_algorithm('gbfs')
            
            # BPSO
            progress.setValue(1)
            progress.setLabelText("Đang chạy BPSO...")
            QApplication.processEvents()
            self.run_algorithm('bpso')
            
            # DP
            progress.setValue(2)
            progress.setLabelText("Đang chạy DP...")
            QApplication.processEvents()
            self.run_algorithm('dp')
            
            progress.setValue(3)
            progress.close()
            
            # Plot convergence
            self.plot_bpso_convergence()
            
            QMessageBox.information(self, "Thành Công", "Tất cả thuật toán đã hoàn thành!")
        
        except Exception as e:
            progress.close()
            QMessageBox.critical(self, "Lỗi", f"Không thể chạy thuật toán:\n{str(e)}")
    
    # =========================================================================
    # PHẦN 3: HIỂN THỊ KẾT QUẢ
    # =========================================================================
    def update_results_display(self):
        """Cập nhật bảng kết quả"""
        # Metrics
        metrics = [
            'Tổng Giá Trị',
            'Tổng Trọng Lượng',
            'Tỷ Lệ Sử Dụng (%)',
            'Số Vật Phẩm Chọn',
            'Khả Thi',
            'Trạng Thái/Vòng Lặp',
            'Thời Gian (giây)',
            'So Với Optimal (%)'
        ]
        
        self.results_table.setRowCount(len(metrics))
        self.results_table.setVerticalHeaderLabels(metrics)
        
        # Find optimal value (from DP if available)
        optimal_value = None
        if 'dp' in self.results:
            optimal_value = self.results['dp']['total_value']
        
        # Fill data
        algos = ['gbfs', 'bpso', 'dp']
        algo_names = ['GBFS', 'BPSO', 'DP']
        
        for col, (algo, name) in enumerate(zip(algos, algo_names), start=1):
            if algo in self.results:
                r = self.results[algo]
                
                # Value
                item = QTableWidgetItem(str(r['total_value']))
                if optimal_value and r['total_value'] == optimal_value:
                    item.setBackground(QColor(144, 238, 144))  # Light green
                self.results_table.setItem(0, col, item)
                
                # Weight
                self.results_table.setItem(1, col, 
                    QTableWidgetItem(f"{r['total_weight']}/{self.problem.capacity}"))
                
                # Capacity usage
                usage = r['total_weight'] / self.problem.capacity * 100
                usage_item = QTableWidgetItem(f"{usage:.1f}%")
                if usage >= 95:
                    usage_item.setBackground(QColor(144, 238, 144))  # Light green
                elif usage < 80:
                    usage_item.setBackground(QColor(255, 182, 193))  # Light red
                self.results_table.setItem(2, col, usage_item)
                
                # Items selected
                self.results_table.setItem(3, col, QTableWidgetItem(str(r['n_items_selected'])))
                
                # Feasible
                feasible_text = "✓" if r['is_feasible'] else "✗"
                feasible_item = QTableWidgetItem(feasible_text)
                if r['is_feasible']:
                    feasible_item.setBackground(QColor(144, 238, 144))
                else:
                    feasible_item.setBackground(QColor(255, 182, 193))
                self.results_table.setItem(4, col, feasible_item)
                
                # States/Iterations
                if algo == 'gbfs':
                    self.results_table.setItem(5, col, 
                        QTableWidgetItem(f"{r['states_explored']} trạng thái"))
                elif algo == 'bpso':
                    self.results_table.setItem(5, col, 
                        QTableWidgetItem(f"{r['iterations']} vòng lặp"))
                else:
                    self.results_table.setItem(5, col, QTableWidgetItem("N/A"))
                
                # Execution Time
                if 'execution_time' in r:
                    time_str = f"{r['execution_time']:.4f}s"
                    if r['execution_time'] < 0.001:
                        time_str = f"{r['execution_time']*1000:.2f}ms"
                    time_item = QTableWidgetItem(time_str)
                    # Highlight fastest
                    if r['execution_time'] == min(res.get('execution_time', float('inf')) 
                                                  for res in self.results.values()):
                        time_item.setBackground(QColor(144, 238, 144))
                    self.results_table.setItem(6, col, time_item)
                else:
                    self.results_table.setItem(6, col, QTableWidgetItem("N/A"))
                
                # Comparison with optimal
                if optimal_value and optimal_value > 0:
                    gap = (r['total_value'] / optimal_value) * 100
                    gap_item = QTableWidgetItem(f"{gap:.2f}%")
                    if gap >= 99:
                        gap_item.setBackground(QColor(144, 238, 144))
                    elif gap < 90:
                        gap_item.setBackground(QColor(255, 182, 193))
                    self.results_table.setItem(7, col, gap_item)
                else:
                    self.results_table.setItem(7, col, QTableWidgetItem("N/A"))
        
        # Update selected items
        self.update_selected_items_display()
        
        # Update analysis and explanation
        self.update_analysis()
        
        # Update process visualization
        self.update_process_visualization()
    
    def update_process_visualization(self):
        """Minh họa quá trình giải từng bước"""
        if not self.results:
            return
        
        process = "<b>QUÁ TRÌNH GIẢI:</b><br>"
        process += "━" * 50 + "<br><br>"
        
        # GBFS process
        if 'gbfs' in self.results:
            r = self.results['gbfs']
            process += "<b>GBFS - Các bước chọn item:</b><br>"
            process += f"• Bắt đầu: Túi rỗng, capacity còn lại = {self.problem.capacity}<br>"
            
            # Sort items by ratio
            items_sorted = sorted(self.problem.items, key=lambda x: x.ratio, reverse=True)
            selected_names = [item.name for item in r['selected_items']]
            
            current_weight = 0
            step = 1
            for item in items_sorted:
                if item.name in selected_names:
                    current_weight += item.weight
                    remaining = self.problem.capacity - current_weight
                    process += f"• Bước {step}: Chọn {item.name} (ratio={item.ratio:.2f}) "
                    process += f"→ weight={current_weight}/{self.problem.capacity}, "
                    process += f"value={r['total_value']}, còn lại={remaining}<br>"
                    step += 1
            
            process += f"• Kết quả: {r['n_items_selected']} items, value={r['total_value']}<br>"
            process += f"• States explored: {r['states_explored']}<br><br>"
        
        # BPSO process
        if 'bpso' in self.results:
            r = self.results['bpso']
            process += "<b>BPSO - Quá trình hội tụ:</b><br>"
            
            if 'history' in r and len(r['history']) > 0:
                history = r['history']
                
                # Show key iterations
                key_iters = [0, len(history)//4, len(history)//2, len(history)-1]
                for idx in key_iters:
                    if idx < len(history):
                        h = history[idx]
                        process += f"• Iteration {h['iteration']}: "
                        process += f"Best={h['gbest_fitness']:.0f}, "
                        process += f"Avg={h['avg_fitness']:.0f}<br>"
                
                # Convergence info
                final_best = history[-1]['gbest_fitness']
                initial_best = history[0]['gbest_fitness']
                improvement = final_best - initial_best
                
                process += f"<br>• Cải thiện: {initial_best:.0f} → {final_best:.0f} "
                process += f"(+{improvement:.0f})<br>"
                process += f"• Kết quả cuối: {r['n_items_selected']} items, value={r['total_value']}<br><br>"
        
        # DP process
        if 'dp' in self.results:
            r = self.results['dp']
            process += "<b>DP - Bảng quy hoạch động:</b><br>"
            process += f"• Kích thước bảng: {self.problem.n_items} items × {self.problem.capacity} capacity<br>"
            process += f"• Tổng cells tính toán: {self.problem.n_items * self.problem.capacity:,}<br>"
            process += f"• Giá trị tối ưu: DP[{self.problem.n_items}][{self.problem.capacity}] = {r['total_value']}<br>"
            
            # Backtrack info
            process += f"<br>• Backtrack từ cell cuối:<br>"
            for i, item in enumerate(r['selected_items'][:5], 1):  # Show first 5
                process += f"  {i}. Chọn {item.name} (w={item.weight}, v={item.value})<br>"
            
            if len(r['selected_items']) > 5:
                process += f"  ... và {len(r['selected_items'])-5} items khác<br>"
            
            process += f"<br>• Kết quả: {r['n_items_selected']} items, value={r['total_value']} (OPTIMAL)<br>"
        
        self.process_text.setHtml(process)
    
    def update_analysis(self):
        """Phân tích tự động kết quả"""
        if not self.results:
            return
        
        # Lấy thông tin dataset
        dataset_type = self.dataset_combo.currentText().split(' ')[0]
        n_items = self.problem.n_items
        capacity = self.problem.capacity
        
        # Phân tích
        analysis = f"""
<b>PHÂN TÍCH KẾT QUẢ:</b><br>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━<br>
<b>Dataset:</b> {dataset_type}, {n_items} items, capacity={capacity}<br>
<br>
"""
        
        # So sánh giá trị
        values = {algo: self.results[algo]['total_value'] for algo in self.results}
        max_value = max(values.values())
        
        analysis += "<b>RANKING THEO GIÁ TRỊ:</b><br>"
        sorted_algos = sorted(values.items(), key=lambda x: x[1], reverse=True)
        for i, (algo, val) in enumerate(sorted_algos, 1):
            name = {'gbfs': 'GBFS', 'bpso': 'BPSO', 'dp': 'DP'}[algo]
            gap = (val / max_value * 100) if max_value > 0 else 0
            
            if i == 1:
                analysis += f"  1. {name}: {val} (100%)<br>"
            elif i == 2:
                analysis += f"  2. {name}: {val} ({gap:.1f}%)<br>"
            else:
                analysis += f"  3. {name}: {val} ({gap:.1f}%)<br>"
        
        analysis += "<br>"
        
        # So sánh thời gian
        if all('execution_time' in self.results[algo] for algo in self.results):
            times = {algo: self.results[algo]['execution_time'] for algo in self.results}
            sorted_times = sorted(times.items(), key=lambda x: x[1])
            
            analysis += "<b>RANKING THEO TỐC ĐỘ:</b><br>"
            for i, (algo, time) in enumerate(sorted_times, 1):
                name = {'gbfs': 'GBFS', 'bpso': 'BPSO', 'dp': 'DP'}[algo]
                time_str = f"{time*1000:.2f}ms" if time < 0.01 else f"{time:.3f}s"
                
                if i == 1:
                    analysis += f"  1. {name}: {time_str}<br>"
                elif i == 2:
                    speedup = sorted_times[0][1] / time
                    analysis += f"  2. {name}: {time_str} (chậm hơn {speedup:.1f}x)<br>"
                else:
                    speedup = sorted_times[0][1] / time
                    analysis += f"  3. {name}: {time_str} (chậm hơn {speedup:.1f}x)<br>"
            
            analysis += "<br>"
        
        # So sánh capacity usage
        analysis += "<b>SỬ DỤNG CAPACITY:</b><br>"
        for algo in ['gbfs', 'bpso', 'dp']:
            if algo in self.results:
                r = self.results[algo]
                usage = r['total_weight'] / capacity * 100
                name = {'gbfs': 'GBFS', 'bpso': 'BPSO', 'dp': 'DP'}[algo]
                
                if usage >= 95:
                    prefix = "OK"
                elif usage >= 85:
                    prefix = "!"
                else:
                    prefix = "X"
                
                analysis += f"  [{prefix}] {name}: {usage:.1f}% ({r['total_weight']}/{capacity})<br>"
        
        self.analysis_text.setHtml(analysis)
        
        # Cập nhật giải thích
        self.update_explanation()
    
    def update_explanation(self):
        """Giải thích chi tiết và khuyến nghị"""
        if not self.results:
            return
        
        # Check if real-world scenario
        is_scenario = hasattr(self.problem, 'scenario_name')
        
        explanation = "<b>GIẢI THÍCH & KHUYẾN NGHỊ:</b><br>"
        explanation += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━<br><br>"
        
        if is_scenario:
            # Real-world scenario analysis
            scenario_name = self.problem.scenario_name
            expected_winner = self.problem.expected_winner
            winner_reason = self.problem.winner_reason
            
            explanation += f"<b style='color: #2196F3;'>{scenario_name}</b><br><br>"
            
            # Dataset characteristics
            explanation += "<b>ĐẶC ĐIỂM BỘ DATASET:</b><br>"
            explanation += f"<p style='background: #f0f0f0; padding: 8px; border-radius: 4px;'>"
            explanation += f"{winner_reason}"
            explanation += "</p><br>"
            
            # Compare GBFS vs BPSO
            if 'gbfs' in self.results and 'bpso' in self.results:
                gbfs = self.results['gbfs']
                bpso = self.results['bpso']
                
                explanation += "<b>KẾT QUẢ THỰC TẾ:</b><br><br>"
                
                # Determine actual winner
                actual_winner = None
                if bpso['total_value'] > gbfs['total_value']:
                    actual_winner = 'BPSO'
                    winner_color = '#EA4335'
                    loser_color = '#999'
                elif gbfs['total_value'] > bpso['total_value']:
                    actual_winner = 'GBFS'
                    winner_color = '#4285F4'
                    loser_color = '#999'
                else:
                    actual_winner = 'HÒA'
                    winner_color = '#34A853'
                    loser_color = '#34A853'
                
                # Display results with winner highlighting
                gbfs_color = winner_color if actual_winner == 'GBFS' else loser_color
                bpso_color = winner_color if actual_winner == 'BPSO' else loser_color
                
                explanation += f"<table border='1' cellpadding='8' style='border-collapse: collapse; width: 100%;'>"
                explanation += f"<tr style='background: #f5f5f5;'>"
                explanation += f"<th>Thuật toán</th><th>Giá trị</th><th>Số lượng</th><th>Thời gian</th></tr>"
                
                explanation += f"<tr style='color: {gbfs_color};'>"
                explanation += f"<td><b>GBFS</b></td>"
                explanation += f"<td><b>{gbfs['total_value']}</b></td>"
                explanation += f"<td>{gbfs['n_items_selected']} items</td>"
                explanation += f"<td>{gbfs.get('execution_time', 0)*1000:.1f}ms</td></tr>"
                
                explanation += f"<tr style='color: {bpso_color};'>"
                explanation += f"<td><b>BPSO</b></td>"
                explanation += f"<td><b>{bpso['total_value']}</b></td>"
                explanation += f"<td>{bpso['n_items_selected']} items</td>"
                explanation += f"<td>{bpso.get('execution_time', 0)*1000:.1f}ms</td></tr>"
                explanation += "</table><br>"
                
                # Winner announcement
                if actual_winner == 'BPSO':
                    diff = bpso['total_value'] - gbfs['total_value']
                    pct = (diff / gbfs['total_value'] * 100) if gbfs['total_value'] > 0 else 0
                    explanation += f"<h3 style='color: {winner_color};'>🏆 BPSO THẮNG (+{diff} điểm, +{pct:.1f}%)</h3>"
                elif actual_winner == 'GBFS':
                    diff = gbfs['total_value'] - bpso['total_value']
                    pct = (diff / bpso['total_value'] * 100) if bpso['total_value'] > 0 else 0
                    explanation += f"<h3 style='color: {winner_color};'>🏆 GBFS THẮNG (+{diff} điểm, +{pct:.1f}%)</h3>"
                else:
                    explanation += f"<h3 style='color: {winner_color};'>🤝 HÒA (cùng {gbfs['total_value']} điểm)</h3>"
                
                # Explanation of WHY this algorithm won
                explanation += "<br><b>TẠI SAO THẮNG?</b><br>"
                explanation += "<p style='background: #fff3cd; padding: 10px; border-radius: 4px; border-left: 4px solid #ffc107;'>"
                
                if expected_winner == 'GBFS' and actual_winner == 'GBFS':
                    explanation += "<b>✓ Đúng như dự đoán - GBFS thắng vì:</b><br>"
                    explanation += "• Dataset có <b>ratio rõ ràng</b>, items khác biệt về value/weight<br>"
                    explanation += "• Greedy chọn theo ratio cao → thấp, không bị nhầm lẫn<br>"
                    explanation += "• Ít items, không gian tìm kiếm nhỏ → greedy đủ tốt<br>"
                    explanation += f"• <b>Nhanh hơn BPSO</b> {(bpso.get('execution_time', 0) / gbfs.get('execution_time', 0.001)):.1f}x lần"
                    
                elif expected_winner == 'BPSO' and actual_winner == 'BPSO':
                    explanation += "<b>✓ Đúng như dự đoán - BPSO thắng vì:</b><br>"
                    explanation += "• Dataset có <b>ratio tương tự nhau</b>, items khó phân biệt<br>"
                    explanation += "• GBFS bối rối khi nhiều items có ratio gần nhau<br>"
                    explanation += "• Có outliers (items nặng) làm GBFS sa bẫy<br>"
                    explanation += "• BPSO explore nhiều tổ hợp → tìm được solution tốt hơn"
                    
                elif actual_winner != expected_winner and actual_winner != 'HÒA':
                    explanation += f"<b>⚠ Bất ngờ! {actual_winner} thắng thay vì {expected_winner}:</b><br>"
                    explanation += "• Có thể do parameters BPSO (particles, iterations) chưa tối ưu<br>"
                    explanation += "• Hoặc GBFS may mắn với random seed<br>"
                    explanation += "• Dataset thực tế có thể phức tạp hơn dự đoán"
                else:
                    explanation += "<b>🤝 Hòa - Cả 2 thuật toán đều tốt với dataset này</b>"
                
                explanation += "</p>"
                
                # Show selected items comparison
                explanation += "<br><b>ITEMS ĐÃ CHỌN:</b><br>"
                explanation += f"<b>GBFS:</b> "
                gbfs_names = [item.name for item in gbfs['selected_items'][:5]]
                explanation += ", ".join(gbfs_names)
                if gbfs['n_items_selected'] > 5:
                    explanation += f" ... (+{gbfs['n_items_selected']-5})"
                explanation += "<br>"
                
                explanation += f"<b>BPSO:</b> "
                bpso_names = [item.name for item in bpso['selected_items'][:5]]
                explanation += ", ".join(bpso_names)
                if bpso['n_items_selected'] > 5:
                    explanation += f" ... (+{bpso['n_items_selected']-5})"
                explanation += "<br>"
            
            # Optimal comparison
            if 'dp' in self.results:
                dp = self.results['dp']
                explanation += f"<br><b>GIẢI PHÁP TỐI ƯU (DP): {dp['total_value']} điểm ⭐</b><br>"
                
                if 'gbfs' in self.results:
                    gbfs_gap = ((dp['total_value'] - self.results['gbfs']['total_value']) / dp['total_value'] * 100) if dp['total_value'] > 0 else 0
                    explanation += f"• GBFS gap: {gbfs_gap:.2f}%<br>"
                
                if 'bpso' in self.results:
                    bpso_gap = ((dp['total_value'] - self.results['bpso']['total_value']) / dp['total_value'] * 100) if dp['total_value'] > 0 else 0
                    explanation += f"• BPSO gap: {bpso_gap:.2f}%<br>"
        
        else:
            # Abstract dataset analysis (existing code)
            dataset_type = self.dataset_combo.currentText().split(' ')[0]
            
            # Phân tích theo dataset type
            if dataset_type == "Random":
                explanation += "<b>Tình huống: Random (Cân bằng)</b><br>"
                explanation += "Đây là dataset ngẫu nhiên, items có value/weight phân tán tốt.<br><br>"
                
                if 'gbfs' in self.results and 'dp' in self.results:
                    gbfs_val = self.results['gbfs']['total_value']
                    dp_val = self.results['dp']['total_value']
                    gap = abs(gbfs_val - dp_val) / dp_val * 100 if dp_val > 0 else 0
                    
                    if gap < 5:
                        explanation += "[OK] <b>GBFS hoạt động TỐT:</b><br>"
                        explanation += f"  • Đạt gần optimal (gap chỉ {gap:.1f}%)<br>"
                        explanation += "  • Nhanh hơn BPSO rất nhiều<br>"
                        explanation += "  • Phù hợp cho dataset loại này<br><br>"
                        explanation += "<b>Khuyến nghị:</b> Dùng GBFS cho dataset random nhỏ/vừa<br>"
                    else:
                        explanation += "[!] <b>GBFS chưa tối ưu:</b><br>"
                        explanation += f"  • Gap với optimal: {gap:.1f}%<br>"
                        explanation += "  • Có thể do max_states quá thấp<br><br>"
                        explanation += "<b>Khuyến nghị:</b> Tăng max_states hoặc dùng BPSO<br>"
            
            elif dataset_type == "High":
                explanation += "<b>Tình huống: High Correlation</b><br>"
                explanation += "Items có value/weight tương quan cao → Ratio giống nhau.<br><br>"
                
                if 'gbfs' in self.results and 'bpso' in self.results:
                    gbfs_usage = self.results['gbfs']['total_weight'] / self.problem.capacity * 100
                    bpso_usage = self.results['bpso']['total_weight'] / self.problem.capacity * 100
                    
                    if gbfs_usage < 85:
                        explanation += "[X] <b>GBFS YẾU KÉM:</b><br>"
                        explanation += f"  • Chỉ dùng {gbfs_usage:.1f}% capacity<br>"
                        explanation += "  • Không biết ưu tiên item nào khi ratio giống nhau<br>"
                        explanation += "  • Để lại nhiều 'khe trống' lãng phí<br><br>"
                    else:
                        explanation += "[!] <b>GBFS khá tốt (bất ngờ):</b><br>"
                        explanation += f"  • Đạt {gbfs_usage:.1f}% capacity<br><br>"
                    
                    if bpso_usage > gbfs_usage + 5:
                        explanation += "[OK] <b>BPSO VƯỢT TRỘI:</b><br>"
                        explanation += f"  • Đạt {bpso_usage:.1f}% capacity<br>"
                        explanation += f"  • Tốt hơn GBFS {bpso_usage - gbfs_usage:.1f}%<br>"
                        explanation += "  • Khám phá nhiều tổ hợp tốt hơn<br><br>"
                        explanation += "<b>Khuyến nghị:</b> Dùng BPSO cho dataset có correlation cao<br>"
            
            elif dataset_type == "Outlier":
                explanation += "<b>Tình huống: Outlier (Có bẫy)</b><br>"
                explanation += "Có items nặng (60% capacity) nhưng value cao → Bẫy cho greedy.<br><br>"
                
                if 'gbfs' in self.results and 'bpso' in self.results:
                    gbfs_val = self.results['gbfs']['total_value']
                    bpso_val = self.results['bpso']['total_value']
                    
                    if bpso_val > gbfs_val * 1.1:
                        explanation += "[X] <b>GBFS SA BẪY:</b><br>"
                        explanation += f"  • GBFS: {gbfs_val}<br>"
                        explanation += f"  • BPSO: {bpso_val} (cao hơn {(bpso_val/gbfs_val-1)*100:.1f}%)<br>"
                        explanation += "  • GBFS chọn outlier nặng → hết chỗ<br>"
                        explanation += "  • BPSO tránh được bẫy<br><br>"
                        explanation += "<b>Khuyến nghị:</b> Dùng BPSO hoặc DP cho dataset có outliers<br>"
                    else:
                        explanation += "[OK] <b>GBFS tránh bẫy tốt:</b><br>"
                        explanation += "  • Không bị đánh lừa bởi outlier<br><br>"
            
                explanation += "<b>Tình huống: Similar Ratio</b><br>"
                explanation += "Tất cả items có ratio gần nhau → Test tie-breaking.<br><br>"
                
                if 'gbfs' in self.results and 'bpso' in self.results:
                    gbfs_val = self.results['gbfs']['total_value']
                    bpso_val = self.results['bpso']['total_value']
                    
                    explanation += "<b>SO SÁNH TIE-BREAKING:</b><br>"
                    explanation += f"  • GBFS: {gbfs_val}<br>"
                    explanation += f"  • BPSO: {bpso_val}<br>"
                    
                    if bpso_val > gbfs_val:
                        explanation += "  • BPSO tốt hơn nhờ khám phá nhiều tổ hợp<br><br>"
                    else:
                        explanation += "  • GBFS cũng đủ tốt với dataset này<br><br>"
        
        # Kết luận chung
        explanation += "<br><b>TÓM TẮT:</b><br>"
        explanation += "<table border='1' cellpadding='5' style='border-collapse: collapse;'>"
        explanation += "<tr><th>Thuật Toán</th><th>Khi Nào Dùng</th></tr>"
        explanation += "<tr><td><b>GBFS</b></td><td>Dataset nhỏ, random, cần tốc độ</td></tr>"
        explanation += "<tr><td><b>BPSO</b></td><td>Dataset lớn/phức tạp, cần chất lượng</td></tr>"
        explanation += "<tr><td><b>DP</b></td><td>Cần 100% optimal, dataset vừa</td></tr>"
        explanation += "</table>"
        
        self.explain_text.setHtml(explanation)
    
    def update_selected_items_display(self):
        """Hiển thị items được chọn"""
        text = "<b>So Sánh Vật Phẩm Được Chọn:</b><br>"
        text += "━" * 50 + "<br><br>"
        
        algos = [('gbfs', 'GBFS'), ('bpso', 'BPSO'), ('dp', 'DP (Tối Ưu)')]
        
        for algo, name in algos:
            if algo in self.results:
                r = self.results[algo]
                text += f"<b>{name}:</b><br>"
                text += f"Giá trị = {r['total_value']}, Trọng lượng = {r['total_weight']}<br>"
                text += "Vật phẩm: "
                items_str = ", ".join([item.name for item in r['selected_items']])
                text += items_str + "<br><br>"
        
        self.items_text.setHtml(text)
    
    def plot_bpso_convergence(self):
        """Vẽ các biểu đồ so sánh GBFS, BPSO và DP"""
        if not self.results:
            return
        
        # Clear toàn bộ figure
        self.canvas.figure.clear()
        
        # Tạo 2x2 subplots với spacing lớn hơn
        gs = self.canvas.figure.add_gridspec(2, 2, hspace=0.4, wspace=0.35,
                                            left=0.08, right=0.95, top=0.95, bottom=0.08)
        
        # ===== SUBPLOT 1: So sánh Value =====
        ax1 = self.canvas.figure.add_subplot(gs[0, 0])
        
        algos = []
        values = []
        colors_bar = []
        
        if 'gbfs' in self.results:
            algos.append('GBFS')
            values.append(self.results['gbfs']['total_value'])
            colors_bar.append('#4285F4')
        
        if 'bpso' in self.results:
            algos.append('BPSO')
            values.append(self.results['bpso']['total_value'])
            colors_bar.append('#EA4335')
        
        if 'dp' in self.results:
            algos.append('DP')
            values.append(self.results['dp']['total_value'])
            colors_bar.append('#34A853')
        
        x_pos = np.arange(len(algos))
        bars = ax1.bar(x_pos, values, color=colors_bar, alpha=0.8, width=0.6)
        
        ax1.set_ylabel('Giá Trị', fontweight='bold', fontsize=10)
        ax1.set_title('So Sánh Giá Trị', fontweight='bold', fontsize=11)
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(algos, fontsize=9)
        ax1.grid(alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar, val in zip(bars, values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(val)}',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # ===== SUBPLOT 2: BPSO Convergence =====
        ax2 = self.canvas.figure.add_subplot(gs[0, 1])
        
        if 'bpso' in self.results and 'history' in self.results['bpso']:
            history = self.results['bpso']['history']
            iterations = [h['iteration'] for h in history]
            gbest_fitness = [h['gbest_fitness'] for h in history]
            avg_fitness = [h['avg_fitness'] for h in history]
            
            ax2.plot(iterations, gbest_fitness, 'b-', linewidth=2, label='Best')
            ax2.plot(iterations, avg_fitness, color='skyblue', linestyle='--', 
                    linewidth=1.5, label='Avg', alpha=0.7)
            
            # GBFS value as horizontal line
            if 'gbfs' in self.results:
                gbfs_val = self.results['gbfs']['total_value']
                ax2.axhline(gbfs_val, color='#4285F4', linestyle='-.', 
                          linewidth=2, label='GBFS', alpha=0.8)
            
            # Optimal line
            if 'dp' in self.results:
                optimal = self.results['dp']['total_value']
                ax2.axhline(optimal, color='#34A853', linestyle=':', 
                          linewidth=2.5, label='Optimal', alpha=0.8)
            
            ax2.set_xlabel('Iteration', fontweight='bold', fontsize=10)
            ax2.set_ylabel('Fitness', fontweight='bold', fontsize=10)
            ax2.set_title('Hội Tụ BPSO', fontweight='bold', fontsize=11)
            ax2.legend(loc='lower right', fontsize=8, framealpha=0.9)
            ax2.grid(alpha=0.3)
            ax2.tick_params(labelsize=8)
        
        # ===== SUBPLOT 3: Execution Time =====
        ax3 = self.canvas.figure.add_subplot(gs[1, 0])
        
        algos_time = []
        times_ms = []
        colors_time = []
        
        for algo, name, color in [('gbfs', 'GBFS', '#4285F4'), 
                                   ('bpso', 'BPSO', '#EA4335'), 
                                   ('dp', 'DP', '#34A853')]:
            if algo in self.results and 'execution_time' in self.results[algo]:
                algos_time.append(name)
                times_ms.append(self.results[algo]['execution_time'] * 1000)
                colors_time.append(color)
        
        if algos_time:
            x_pos = np.arange(len(algos_time))
            bars_time = ax3.bar(x_pos, times_ms, color=colors_time, alpha=0.8, width=0.6)
            
            ax3.set_ylabel('Thời Gian (ms)', fontweight='bold', fontsize=10)
            ax3.set_title('Tốc Độ Thực Thi', fontweight='bold', fontsize=11)
            ax3.set_xticks(x_pos)
            ax3.set_xticklabels(algos_time, fontsize=9)
            ax3.grid(alpha=0.3, axis='y')
            
            # Add time labels
            for bar, time_val in zip(bars_time, times_ms):
                height = bar.get_height()
                if time_val < 1:
                    label_text = f'{time_val:.2f}'
                else:
                    label_text = f'{time_val:.1f}'
                ax3.text(bar.get_x() + bar.get_width()/2., height,
                        label_text,
                        ha='center', va='bottom', fontsize=8, fontweight='bold')
        
        # ===== SUBPLOT 4: Gap Analysis =====
        ax4 = self.canvas.figure.add_subplot(gs[1, 1])
        
        if 'dp' in self.results:
            optimal_val = self.results['dp']['total_value']
            
            algos_gap = []
            gaps = []
            colors_gap = []
            
            for algo, name, color in [('gbfs', 'GBFS', '#4285F4'), 
                                       ('bpso', 'BPSO', '#EA4335')]:
                if algo in self.results:
                    algos_gap.append(name)
                    val = self.results[algo]['total_value']
                    gap = ((optimal_val - val) / optimal_val * 100) if optimal_val > 0 else 0
                    gaps.append(gap)
                    colors_gap.append(color)
            
            if algos_gap:
                x_pos = np.arange(len(algos_gap))
                bars_gap = ax4.bar(x_pos, gaps, color=colors_gap, alpha=0.8, width=0.6)
                
                ax4.set_ylabel('Gap (%)', fontweight='bold', fontsize=10)
                ax4.set_title('Độ Lệch So Optimal', fontweight='bold', fontsize=11)
                ax4.set_xticks(x_pos)
                ax4.set_xticklabels(algos_gap, fontsize=9)
                ax4.grid(alpha=0.3, axis='y')
                ax4.axhline(0, color='green', linestyle='-', linewidth=1.5, alpha=0.5)
                
                # Add gap labels
                for bar, gap in zip(bars_gap, gaps):
                    height = bar.get_height()
                    ax4.text(bar.get_x() + bar.get_width()/2., height,
                            f'{gap:.2f}%',
                            ha='center', va='bottom', fontsize=8, fontweight='bold')
        
        self.canvas.draw()


# =================================================================================
# MAIN: Chạy ứng dụng
# =================================================================================
def main():
    """Khởi động ứng dụng GUI"""
    app = QApplication(sys.argv)
    
    # Set style
    app.setStyle('Fusion')
    
    # Main window
    window = KnapsackSolverGUI()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
