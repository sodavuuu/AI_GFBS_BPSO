"""
=================================================================================
ENHANCED KNAPSACK GUI - Learning from GA_TSP
=================================================================================
Improvements:
1. Problem visualization (like GA_TSP map)
2. Real-time algorithm behavior display
3. Advanced charts for section 3.2
4. Better test case selection with preview
=================================================================================
"""
import sys
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import seaborn as sns

# Import algorithms and visualizers
from src.test_case_loader import TestCaseLoader
from src.gbfs_knapsack import solve_knapsack_gbfs
from src.bpso_knapsack import solve_knapsack_bpso
from src.dp_knapsack import solve_knapsack_dp
from src.advanced_visualizer import AdvancedKnapsackVisualizer
from src.algorithm_flowchart import draw_gbfs_flowchart, draw_bpso_flowchart


class MatplotlibCanvas(FigureCanvas):
    """Canvas for matplotlib plots"""
    def __init__(self, parent=None, width=12, height=10, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='white')
        super().__init__(self.fig)
        self.setParent(parent)


class KnapsackGUIEnhanced(QMainWindow):
    """
    Enhanced Knapsack GUI - Learning from GA_TSP
    """
    def __init__(self):
        super().__init__()
        
        # Data
        self.loader = TestCaseLoader()
        self.visualizer = AdvancedKnapsackVisualizer()
        self.current_test_case = None
        self.current_test_data = None  # DataFrame with item details
        self.results = {}
        
        # UI
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle('Knapsack Solver - Advanced Analysis (GA_TSP Style)')
        self.setGeometry(50, 50, 1800, 1000)
        
        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        
        # Left panel (25%)
        left_panel = self.create_control_panel()
        main_layout.addWidget(left_panel, 25)
        
        # Right panel (75%)
        right_panel = self.create_visualization_panel()
        main_layout.addWidget(right_panel, 75)
    
    def create_control_panel(self):
        """Create left control panel"""
        panel = QWidget()
        panel.setMaximumWidth(450)
        panel.setStyleSheet("background-color: #f8f9fa;")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # ===== HEADER =====
        title = QLabel("KNAPSACK SOLVER")
        title.setStyleSheet("""
            font-size: 20px; 
            font-weight: bold; 
            color: #2c3e50;
            padding: 10px;
            background-color: #ecf0f1;
            border-radius: 5px;
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Multi-Objective Optimization\nf₁: Revenue | f₂: Regional Diversity")
        subtitle.setStyleSheet("font-size: 11px; color: #7f8c8d; padding: 5px;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addWidget(self._separator())
        
        # ===== PROBLEM DEFINITION =====
        problem_group = QGroupBox("Problem Definition")
        problem_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        problem_layout = QVBoxLayout()
        
        problem_text = QLabel(
            "<b>0/1 Knapsack Problem:</b><br>"
            "• <b>Input:</b> n items (weight, value, region)<br>"
            "• <b>Constraint:</b> Total weight ≤ Capacity<br>"
            "• <b>Objective 1:</b> Maximize total value<br>"
            "• <b>Objective 2:</b> Maximize regional diversity<br>"
            "• <b>Fitness:</b> 0.7×f₁ + 0.3×f₂"
        )
        problem_text.setStyleSheet("font-size: 10px; padding: 5px; line-height: 1.4;")
        problem_text.setWordWrap(True)
        problem_layout.addWidget(problem_text)
        
        problem_group.setLayout(problem_layout)
        layout.addWidget(problem_group)
        
        # ===== TEST CASE SELECTION =====
        test_group = QGroupBox("Test Case Selection")
        test_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
        """)
        test_layout = QVBoxLayout()
        
        # Test case dropdown
        test_label = QLabel("Select Test Case:")
        test_label.setStyleSheet("font-weight: bold; font-size: 11px;")
        test_layout.addWidget(test_label)
        
        self.test_combo = QComboBox()
        self.test_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                font-size: 11px;
                border: 1px solid #bdc3c7;
                border-radius: 3px;
            }
        """)
        
        # Populate with grouped test cases
        test_cases = self.loader.list_test_cases()
        
        # Group by type
        size_cases = [t for t in test_cases if t.startswith('Size')]
        region_cases = [t for t in test_cases if t.startswith('Region')]
        category_cases = [t for t in test_cases if t.startswith('Category')]
        data_cases = [t for t in test_cases if t.startswith('Data')]
        
        self.test_combo.addItem("--- SIZE TESTS ---")
        for tc in size_cases:
            self.test_combo.addItem(tc)
        
        self.test_combo.addItem("--- REGIONAL TESTS ---")
        for tc in region_cases:
            self.test_combo.addItem(tc)
        
        self.test_combo.addItem("--- CATEGORY TESTS ---")
        for tc in category_cases:
            self.test_combo.addItem(tc)
        
        self.test_combo.addItem("--- DATA CHARACTERISTIC TESTS ---")
        for tc in data_cases:
            self.test_combo.addItem(tc)
        
        # Set default
        if len(size_cases) > 0:
            self.test_combo.setCurrentText(size_cases[1] if len(size_cases) > 1 else size_cases[0])
        
        self.test_combo.currentTextChanged.connect(self.on_test_case_changed)
        test_layout.addWidget(self.test_combo)
        
        # Test case info display
        self.test_info_label = QLabel("Select a test case to see details")
        self.test_info_label.setStyleSheet("""
            background-color: #ecf0f1; 
            padding: 10px; 
            border-radius: 5px;
            font-size: 10px;
        """)
        self.test_info_label.setWordWrap(True)
        test_layout.addWidget(self.test_info_label)
        
        test_group.setLayout(test_layout)
        layout.addWidget(test_group)
        
        # ===== ALGORITHM PARAMETERS =====
        params_group = QGroupBox("Algorithm Parameters")
        params_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e74c3c;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
        """)
        params_layout = QVBoxLayout()
        
        # GBFS params
        gbfs_label = QLabel("<b>GBFS:</b>")
        gbfs_label.setStyleSheet("font-size: 11px;")
        params_layout.addWidget(gbfs_label)
        
        gbfs_inner = QHBoxLayout()
        gbfs_inner.addWidget(QLabel("Max States:"))
        self.gbfs_max_states = QSpinBox()
        self.gbfs_max_states.setRange(1000, 20000)
        self.gbfs_max_states.setValue(5000)
        self.gbfs_max_states.setSingleStep(1000)
        gbfs_inner.addWidget(self.gbfs_max_states)
        params_layout.addLayout(gbfs_inner)
        
        params_layout.addWidget(self._separator())
        
        # BPSO params
        bpso_label = QLabel("<b>BPSO:</b>")
        bpso_label.setStyleSheet("font-size: 11px;")
        params_layout.addWidget(bpso_label)
        
        bpso_particles = QHBoxLayout()
        bpso_particles.addWidget(QLabel("Particles:"))
        self.bpso_particles = QSpinBox()
        self.bpso_particles.setRange(10, 100)
        self.bpso_particles.setValue(30)
        self.bpso_particles.setSingleStep(10)
        bpso_particles.addWidget(self.bpso_particles)
        params_layout.addLayout(bpso_particles)
        
        bpso_iters = QHBoxLayout()
        bpso_iters.addWidget(QLabel("Iterations:"))
        self.bpso_iterations = QSpinBox()
        self.bpso_iterations.setRange(20, 200)
        self.bpso_iterations.setValue(50)
        self.bpso_iterations.setSingleStep(10)
        bpso_iters.addWidget(self.bpso_iterations)
        params_layout.addLayout(bpso_iters)
        
        bpso_w = QHBoxLayout()
        bpso_w.addWidget(QLabel("Inertia (w):"))
        self.bpso_w = QDoubleSpinBox()
        self.bpso_w.setRange(0.1, 1.0)
        self.bpso_w.setValue(0.7)
        self.bpso_w.setSingleStep(0.1)
        bpso_w.addWidget(self.bpso_w)
        params_layout.addLayout(bpso_w)
        
        bpso_c1 = QHBoxLayout()
        bpso_c1.addWidget(QLabel("Cognitive (c₁):"))
        self.bpso_c1 = QDoubleSpinBox()
        self.bpso_c1.setRange(0.0, 4.0)
        self.bpso_c1.setValue(2.0)
        self.bpso_c1.setSingleStep(0.5)
        bpso_c1.addWidget(self.bpso_c1)
        params_layout.addLayout(bpso_c1)
        
        bpso_c2 = QHBoxLayout()
        bpso_c2.addWidget(QLabel("Social (c₂):"))
        self.bpso_c2 = QDoubleSpinBox()
        self.bpso_c2.setRange(0.0, 4.0)
        self.bpso_c2.setValue(2.0)
        self.bpso_c2.setSingleStep(0.5)
        bpso_c2.addWidget(self.bpso_c2)
        params_layout.addLayout(bpso_c2)
        
        params_layout.addWidget(self._separator())
        
        # Heuristic Type
        heur_label = QLabel("<b>GBFS Heuristic:</b>")
        heur_label.setStyleSheet("font-size: 11px;")
        params_layout.addWidget(heur_label)
        
        self.heuristic_combo = QComboBox()
        self.heuristic_combo.addItems(["Value/Weight Ratio", "Pure Value", "Pure Weight"])
        self.heuristic_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                font-size: 10px;
                border: 1px solid #bdc3c7;
                border-radius: 3px;
            }
        """)
        params_layout.addWidget(self.heuristic_combo)
        
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)
        
        # ===== RUN BUTTONS =====
        self.run_btn = QPushButton("RUN ALL ALGORITHMS")
        self.run_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 15px;
                border-radius: 5px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        self.run_btn.clicked.connect(self.run_all_algorithms)
        layout.addWidget(self.run_btn)
        
        # Chapter 3 Experiments button
        self.exp_btn = QPushButton("RUN CHAPTER 3 EXPERIMENTS")
        self.exp_btn.setStyleSheet("""
            QPushButton {
                background-color: #e67e22;
                color: white;
                font-size: 12px;
                font-weight: bold;
                padding: 12px;
                border-radius: 5px;
                margin-top: 5px;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
            QPushButton:pressed {
                background-color: #ba4a00;
            }
        """)
        self.exp_btn.clicked.connect(self.run_chapter3_experiments)
        layout.addWidget(self.exp_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #3498db;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        layout.addStretch()
        
        return panel
    
    def create_visualization_panel(self):
        """Create right visualization panel with tabs"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
            }
            QTabBar::tab {
                background: #ecf0f1;
                border: 1px solid #bdc3c7;
                padding: 10px 20px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: #3498db;
                color: white;
            }
        """)
        
        # Tab 1: Problem Visualization (like GA_TSP map)
        self.tab_problem = QWidget()
        self.tab_problem_layout = QVBoxLayout(self.tab_problem)
        self.canvas_problem = MatplotlibCanvas(width=14, height=10)
        self.tab_problem_layout.addWidget(self.canvas_problem)
        self.tabs.addTab(self.tab_problem, "Problem Visualization")
        
        # Tab 2: BPSO Convergence
        self.tab_convergence = QWidget()
        self.tab_convergence_layout = QVBoxLayout(self.tab_convergence)
        self.canvas_convergence = MatplotlibCanvas(width=14, height=10)
        self.tab_convergence_layout.addWidget(self.canvas_convergence)
        self.tabs.addTab(self.tab_convergence, "BPSO Convergence")
        
        # Tab 3: Algorithm Comparison
        self.tab_comparison = QWidget()
        self.tab_comparison_layout = QVBoxLayout(self.tab_comparison)
        self.canvas_comparison = MatplotlibCanvas(width=14, height=10)
        self.tab_comparison_layout.addWidget(self.canvas_comparison)
        self.tabs.addTab(self.tab_comparison, "Algorithm Comparison")
        
        # Tab 4: GBFS State Tree
        self.tab_gbfs_tree = QWidget()
        self.tab_gbfs_tree_layout = QVBoxLayout(self.tab_gbfs_tree)
        self.canvas_gbfs_tree = MatplotlibCanvas(width=14, height=10)
        self.tab_gbfs_tree_layout.addWidget(self.canvas_gbfs_tree)
        self.tabs.addTab(self.tab_gbfs_tree, "GBFS Algorithm Flow")
        
        # Tab 5: BPSO Swarm
        self.tab_bpso_swarm = QWidget()
        self.tab_bpso_swarm_layout = QVBoxLayout(self.tab_bpso_swarm)
        self.canvas_bpso_swarm = MatplotlibCanvas(width=14, height=10)
        self.tab_bpso_swarm_layout.addWidget(self.canvas_bpso_swarm)
        self.tabs.addTab(self.tab_bpso_swarm, "BPSO Algorithm Flow")
        
        # Tab 6: Regional Distribution
        self.tab_regional = QWidget()
        self.tab_regional_layout = QVBoxLayout(self.tab_regional)
        self.canvas_regional = MatplotlibCanvas(width=14, height=10)
        self.tab_regional_layout.addWidget(self.canvas_regional)
        self.tabs.addTab(self.tab_regional, "Regional Analysis")
        
        # Tab 7: Selected Items Detail
        self.tab_items = QWidget()
        self.tab_items_layout = QVBoxLayout(self.tab_items)
        self.items_table = QTableWidget()
        self.items_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #bdc3c7;
                gridline-color: #ecf0f1;
                font-size: 10px;
            }
            QHeaderView::section {
                background-color: #16a085;
                color: white;
                padding: 8px;
                font-weight: bold;
            }
        """)
        self.tab_items_layout.addWidget(self.items_table)
        self.tabs.addTab(self.tab_items, "Selected Items")
        
        # Tab 8: Solution Details
        self.tab_solution = QWidget()
        self.tab_solution_layout = QVBoxLayout(self.tab_solution)
        
        # Solution table
        self.solution_table = QTableWidget()
        self.solution_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #bdc3c7;
                gridline-color: #ecf0f1;
                font-size: 10px;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 8px;
                font-weight: bold;
            }
        """)
        self.tab_solution_layout.addWidget(self.solution_table)
        
        self.tabs.addTab(self.tab_solution, "Solution Details")
        
        # Tab 9: Chapter 3 Experiments Results
        self.tab_experiments = QWidget()
        self.tab_experiments_layout = QVBoxLayout(self.tab_experiments)
        
        # Experiments info and load button
        exp_header = QHBoxLayout()
        exp_info = QLabel("Chapter 3 Experiment Results (CSV Data)")
        exp_info.setStyleSheet("font-weight: bold; font-size: 12px;")
        exp_header.addWidget(exp_info)
        
        self.load_csv_btn = QPushButton("Load Results from CSV")
        self.load_csv_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 15px;
                border-radius: 3px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.load_csv_btn.clicked.connect(self.load_experiment_results)
        exp_header.addWidget(self.load_csv_btn)
        exp_header.addStretch()
        
        self.tab_experiments_layout.addLayout(exp_header)
        
        # Experiments canvas
        self.canvas_experiments = MatplotlibCanvas(width=14, height=10)
        self.tab_experiments_layout.addWidget(self.canvas_experiments)
        
        self.tabs.addTab(self.tab_experiments, "Chapter 3 Experiments")
        
        layout.addWidget(self.tabs)
        
        return panel
    
    def _separator(self):
        """Create horizontal separator"""
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #bdc3c7;")
        return line
    
    def on_test_case_changed(self, test_name):
        """Handle test case selection change"""
        if test_name.startswith("---"):
            return
        
        try:
            self.current_test_case = self.loader.load_test_case(test_name)
            
            # Update info label
            info_text = (
                f"<b>{test_name}</b><br>"
                f"Items: {self.current_test_case['n_items']}<br>"
                f"Capacity: {self.current_test_case['capacity']:.0f}<br>"
                f"Total Weight: {self.current_test_case['total_weight']:.0f}<br>"
                f"Total Value: {self.current_test_case['total_value']:.0f}<br>"
                f"Regions: {self.current_test_case['n_regions']}<br>"
                f"Correlation (w,v): {self.current_test_case['correlation']:.3f}"
            )
            self.test_info_label.setText(info_text)
            
            # Load full item data for visualization
            self.load_test_data(test_name)
            
            # Visualize problem (like GA_TSP map)
            self.visualize_problem()
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load test case: {str(e)}")
    
    def load_test_data(self, test_name):
        """Load full item data including regions/categories"""
        try:
            info = self.loader.get_test_case_info(test_name)
            filepath = self.loader.test_cases_dir / info['File']
            
            # Load CSV with all columns
            df = pd.read_csv(filepath)
            df['name'] = [f"Item_{i+1}" for i in range(len(df))]
            df['weight'] = df['Quantity']
            df['value'] = df['Total']
            
            # Rename columns if needed
            if 'Segment' in df.columns:
                df['region'] = df['Segment']
            
            self.current_test_data = df
            
        except Exception as e:
            print(f"Warning: Could not load detailed test data: {e}")
            self.current_test_data = None
    
    def visualize_problem(self):
        """Visualize problem characteristics (like GA_TSP map)"""
        if self.current_test_case is None:
            return
        
        try:
            fig = self.canvas_problem.fig
            fig.clear()
            
            # Create dummy solution for initial visualization
            dummy_solution = {
                'selected_items': [],
                'total_value': 0,
                'total_weight': 0,
                'capacity': self.current_test_case['capacity']
            }
            
            # If we have detailed data, create better visualization
            if self.current_test_data is not None:
                self.visualizer.plot_knapsack_solution_map(
                    dummy_solution, 
                    self.current_test_data, 
                    save_path=None
                )
                
                # Copy to our canvas
                new_fig = plt.gcf()
                self.canvas_problem.fig = new_fig
                self.canvas_problem.draw()
            else:
                # Simple visualization
                ax = fig.add_subplot(111)
                ax.text(0.5, 0.5, 
                       f"Test Case: {self.current_test_case['test_case_name']}\n\n"
                       f"Items: {self.current_test_case['n_items']}\n"
                       f"Capacity: {self.current_test_case['capacity']:.0f}\n"
                       f"Total Value Available: {self.current_test_case['total_value']:.0f}\n\n"
                       "Click RUN to see solution visualization",
                       ha='center', va='center', fontsize=14)
                ax.axis('off')
                self.canvas_problem.draw()
                
        except Exception as e:
            print(f"Error visualizing problem: {e}")
    
    def run_all_algorithms(self):
        """Run all three algorithms"""
        if self.current_test_case is None:
            QMessageBox.warning(self, "Warning", "Please select a test case first!")
            return
        
        self.run_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        QApplication.processEvents()
        
        try:
            items = self.current_test_case['items']
            weights = self.current_test_case['weights']
            values = self.current_test_case['values']
            capacity = self.current_test_case['capacity']
            
            # GBFS
            self.progress_bar.setValue(10)
            QApplication.processEvents()
            
            gbfs_result = solve_knapsack_gbfs(items, weights, values, capacity)
            self.results['gbfs'] = gbfs_result
            
            self.progress_bar.setValue(40)
            QApplication.processEvents()
            
            # BPSO
            bpso_result = solve_knapsack_bpso(items, weights, values, capacity,
                                    n_particles=self.bpso_particles.value(),
                                    max_iterations=self.bpso_iterations.value(),
                                    w=self.bpso_w.value(),
                                    c1=self.bpso_c1.value(),
                                    c2=self.bpso_c2.value())
            self.results['bpso'] = bpso_result
            
            self.progress_bar.setValue(70)
            QApplication.processEvents()
            
            # DP
            dp_result = solve_knapsack_dp(items, weights, values, capacity)
            self.results['dp'] = dp_result
            
            self.progress_bar.setValue(90)
            QApplication.processEvents()
            
            # Visualize results
            self.visualize_results()
            
            self.progress_bar.setValue(100)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Execution failed:\n{str(e)}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.run_btn.setEnabled(True)
    
    def visualize_results(self):
        """Generate all visualizations"""
        # Tab 1: Update problem visualization with best solution
        self.visualize_best_solution()
        
        # Tab 2: GBFS State Tree
        self.visualize_gbfs_tree()
        
        # Tab 3: BPSO Swarm
        self.visualize_bpso_swarm()
        
        # Tab 4: BPSO Convergence
        self.visualize_convergence()
        
        # Tab 5: Algorithm Comparison
        self.visualize_comparison()
        
        # Tab 6: Regional Distribution
        self.visualize_regional_distribution()
        
        # Tab 7: Items Detail Table
        self.populate_items_table()
        
        # Tab 8: Solution Summary
        self.populate_solution_table()
    
    def visualize_best_solution(self):
        """Visualize best solution on problem map"""
        if 'bpso' not in self.results or self.current_test_data is None:
            return
        
        try:
            best_solution = self.results['bpso']  # Use BPSO as default
            
            fig = self.canvas_problem.fig
            fig.clear()
            
            self.visualizer.plot_knapsack_solution_map(
                best_solution,
                self.current_test_data,
                save_path=None
            )
            
            # Copy figure
            new_fig = plt.gcf()
            self.canvas_problem.fig = new_fig
            self.canvas_problem.draw()
            
        except Exception as e:
            print(f"Error visualizing solution: {e}")
    
    def visualize_convergence(self):
        """Visualize BPSO convergence"""
        if 'bpso' not in self.results:
            return
        
        try:
            fig = self.canvas_convergence.fig
            fig.clear()
            
            self.visualizer.plot_convergence(self.results['bpso'], save_path=None)
            
            new_fig = plt.gcf()
            self.canvas_convergence.fig = new_fig
            self.canvas_convergence.draw()
            
        except Exception as e:
            print(f"Error visualizing convergence: {e}")
    
    def visualize_comparison(self):
        """Visualize algorithm comparison"""
        if len(self.results) < 3:
            return
        
        try:
            fig = self.canvas_comparison.fig
            fig.clear()
            
            self.visualizer.plot_algorithm_comparison_detailed(
                self.results['gbfs'],
                self.results['bpso'],
                self.results['dp'],
                save_path=None
            )
            
            new_fig = plt.gcf()
            self.canvas_comparison.fig = new_fig
            self.canvas_comparison.draw()
            
        except Exception as e:
            print(f"Error visualizing comparison: {e}")
    
    def populate_solution_table(self):
        """Populate solution details table"""
        if len(self.results) == 0:
            return
        
        try:
            # Prepare data
            data = []
            
            for alg_name in ['gbfs', 'bpso', 'dp']:
                if alg_name in self.results:
                    r = self.results[alg_name]
                    data.append({
                        'Algorithm': alg_name.upper(),
                        'Total Value': f"{r['total_value']:.0f}",
                        'Total Weight': f"{r['total_weight']:.1f}",
                        'Items Selected': len(r['selected_items']),
                        'Execution Time': f"{r['execution_time']:.4f}s",
                        'Feasible': '✅' if r['total_weight'] <= self.current_test_case['capacity'] else '❌'
                    })
            
            # Set table
            self.solution_table.setRowCount(len(data))
            self.solution_table.setColumnCount(6)
            self.solution_table.setHorizontalHeaderLabels(
                ['Algorithm', 'Total Value', 'Total Weight', 'Items Selected', 'Time', 'Feasible']
            )
            
            for i, row_data in enumerate(data):
                for j, (key, value) in enumerate(row_data.items()):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.solution_table.setItem(i, j, item)
            
            self.solution_table.resizeColumnsToContents()
            
        except Exception as e:
            print(f"Error populating table: {e}")
    
    def visualize_gbfs_tree(self):
        """Visualize GBFS flowchart - Google Images style"""
        try:
            fig = self.canvas_gbfs_tree.fig
            fig.clear()
            
            # Draw GBFS flowchart
            ax = fig.add_subplot(111)
            draw_gbfs_flowchart(ax)
            
            # Add result statistics if available
            if 'gbfs' in self.results:
                result = self.results['gbfs']
                stats_text = (
                    f"Current Run Stats:\n"
                    f"Value: {result['total_value']:.0f} | "
                    f"States: {result.get('states_explored', 'N/A')} | "
                    f"Time: {result['execution_time']:.3f}s"
                )
                ax.text(0.5, -0.3, stats_text, transform=ax.transAxes,
                       fontsize=9, ha='center', fontweight='bold',
                       bbox=dict(boxstyle='round', facecolor='#ecf0f1', alpha=0.8))
            
            fig.tight_layout()
            self.canvas_gbfs_tree.draw()
            
        except Exception as e:
            print(f"Error visualizing GBFS flowchart: {e}")
            import traceback
            traceback.print_exc()
    
    def visualize_bpso_swarm(self):
        """Visualize BPSO flowchart - Google Images style"""
        try:
            fig = self.canvas_bpso_swarm.fig
            fig.clear()
            
            # Draw BPSO flowchart
            ax = fig.add_subplot(111)
            draw_bpso_flowchart(ax)
            
            # Add result statistics if available
            if 'bpso' in self.results:
                result = self.results['bpso']
                stats_text = (
                    f"Current Run Stats:\n"
                    f"Value: {result['total_value']:.0f} | "
                    f"Particles: {result.get('n_particles', 'N/A')} | "
                    f"Iterations: {result.get('iterations', 'N/A')} | "
                    f"Time: {result['execution_time']:.3f}s"
                )
                ax.text(0.5, -0.05, stats_text, transform=ax.transAxes,
                       fontsize=9, ha='center', fontweight='bold',
                       bbox=dict(boxstyle='round', facecolor='#ecf0f1', alpha=0.8))
            
            fig.tight_layout()
            self.canvas_bpso_swarm.draw()
            
        except Exception as e:
            print(f"Error visualizing BPSO flowchart: {e}")
            import traceback
            traceback.print_exc()
            # Use BPSO result as default
            best_solution = self.results.get('bpso', self.results.get('gbfs', self.results.get('dp')))
            
            selected_indices = best_solution['selected_indices']
            selected_data = self.current_test_data.iloc[selected_indices]
            
            # Create subplots
            ax1 = fig.add_subplot(2, 2, 1)
            ax2 = fig.add_subplot(2, 2, 2)
            ax3 = fig.add_subplot(2, 2, 3)
            ax4 = fig.add_subplot(2, 2, 4)
            
            # Regional distribution (Pie Chart)
            if 'Segment' in selected_data.columns or 'region' in selected_data.columns:
                region_col = 'Segment' if 'Segment' in selected_data.columns else 'region'
                region_counts = selected_data[region_col].value_counts()
                colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
                ax1.pie(region_counts.values, labels=region_counts.index, autopct='%1.1f%%', 
                       startangle=90, colors=colors[:len(region_counts)])
                ax1.set_title('Regional Distribution', fontweight='bold', fontsize=11)
            else:
                # Fallback: show item count
                ax1.text(0.5, 0.5, f'{len(selected_data)} Items Selected', 
                        ha='center', va='center', fontsize=14, fontweight='bold')
                ax1.set_title('Regional Distribution\n(No region data)', fontweight='bold', fontsize=11)
                ax1.axis('off')
            
            # Category distribution (Bar Chart)
            if 'Category' in selected_data.columns:
                cat_counts = selected_data['Category'].value_counts()
                colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12']
                ax2.bar(range(len(cat_counts)), cat_counts.values, color=colors[:len(cat_counts)])
                ax2.set_xticks(range(len(cat_counts)))
                ax2.set_xticklabels(cat_counts.index, rotation=45, ha='right', fontsize=9)
                ax2.set_title('Category Distribution', fontweight='bold', fontsize=11)
                ax2.set_ylabel('Count', fontsize=10)
                ax2.grid(True, alpha=0.3, axis='y')
            else:
                # Fallback: show value/weight stats
                ax2.bar([0, 1], [selected_data['value'].sum(), selected_data['weight'].sum()], 
                       color=['#2ecc71', '#e74c3c'])
                ax2.set_xticks([0, 1])
                ax2.set_xticklabels(['Total Value', 'Total Weight'], fontsize=9)
                ax2.set_title('Value vs Weight', fontweight='bold', fontsize=11)
                ax2.set_ylabel('Total', fontsize=10)
                ax2.grid(True, alpha=0.3, axis='y')
            
            # Weight vs Value scatter
            ax3.scatter(selected_data['weight'], selected_data['value'], 
                       alpha=0.6, s=100, c='green', edgecolors='black', linewidth=0.5)
            ax3.set_xlabel('Weight', fontsize=10)
            ax3.set_ylabel('Value', fontsize=10)
            ax3.set_title('Weight vs Value (Selected Items)', fontweight='bold', fontsize=11)
            ax3.grid(True, alpha=0.3)
            
            # Value distribution histogram
            ax4.hist(selected_data['value'], bins=min(15, len(selected_data)), 
                    alpha=0.7, color='skyblue', edgecolor='black')
            ax4.set_xlabel('Value', fontsize=10)
            ax4.set_ylabel('Frequency', fontsize=10)
            ax4.set_title('Value Distribution', fontweight='bold', fontsize=11)
            ax4.grid(True, alpha=0.3, axis='y')
            
            fig.tight_layout(pad=2.0)
            self.canvas_regional.draw()
            
        except Exception as e:
            print(f"Error visualizing regional distribution: {e}")
            import traceback
            traceback.print_exc()
    
    def populate_items_table(self):
        """Populate detailed items table"""
        if len(self.results) == 0:
            return
        
        try:
            # Use BPSO result as default
            best_solution = self.results.get('bpso', self.results.get('gbfs', self.results.get('dp')))
            selected_indices = best_solution['selected_indices']
            
            if self.current_test_data is None:
                # Fallback: use basic data
                weights = np.array(self.current_test_case['weights'])
                values = np.array(self.current_test_case['values'])
                
                self.items_table.setRowCount(len(selected_indices))
                self.items_table.setColumnCount(4)
                self.items_table.setHorizontalHeaderLabels(['Index', 'Weight', 'Value', 'Ratio (v/w)'])
                
                for row, idx in enumerate(selected_indices):
                    self.items_table.setItem(row, 0, QTableWidgetItem(str(idx)))
                    self.items_table.setItem(row, 1, QTableWidgetItem(f"{weights[idx]:.1f}"))
                    self.items_table.setItem(row, 2, QTableWidgetItem(f"{values[idx]:.0f}"))
                    self.items_table.setItem(row, 3, QTableWidgetItem(f"{values[idx]/weights[idx]:.2f}"))
            else:
                # Rich data
                selected_data = self.current_test_data.iloc[selected_indices]
                
                cols = ['Index', 'Weight', 'Value', 'Ratio']
                if 'Segment' in selected_data.columns:
                    cols.append('Region')
                if 'Category' in selected_data.columns:
                    cols.append('Category')
                
                self.items_table.setRowCount(len(selected_indices))
                self.items_table.setColumnCount(len(cols))
                self.items_table.setHorizontalHeaderLabels(cols)
                
                for row, (idx, item) in enumerate(zip(selected_indices, selected_data.iterrows())):
                    col = 0
                    self.items_table.setItem(row, col, QTableWidgetItem(str(idx)))
                    col += 1
                    self.items_table.setItem(row, col, QTableWidgetItem(f"{item[1]['weight']:.1f}"))
                    col += 1
                    self.items_table.setItem(row, col, QTableWidgetItem(f"{item[1]['value']:.0f}"))
                    col += 1
                    self.items_table.setItem(row, col, QTableWidgetItem(f"{item[1]['value']/item[1]['weight']:.2f}"))
                    col += 1
                    
                    if 'Segment' in selected_data.columns:
                        self.items_table.setItem(row, col, QTableWidgetItem(str(item[1]['Segment'])))
                        col += 1
                    if 'Category' in selected_data.columns:
                        self.items_table.setItem(row, col, QTableWidgetItem(str(item[1]['Category'])))
            
            self.items_table.resizeColumnsToContents()
            
        except Exception as e:
            print(f"Error populating items table: {e}")
            import traceback
            traceback.print_exc()
    
    def run_chapter3_experiments(self):
        """Run all Chapter 3 experiments"""
        reply = QMessageBox.question(
            self, 
            'Run Chapter 3 Experiments',
            'This will run all experiments for Chapter 3 (3.1.1, 3.1.2, 3.1.3).\n'
            'This may take several minutes.\n\n'
            'Continue?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
        
        # Create progress dialog
        progress = QProgressDialog("Running Chapter 3 Experiments...", "Cancel", 0, 6, self)
        progress.setWindowTitle("Experiments Progress")
        progress.setWindowModality(Qt.WindowModal)
        progress.setMinimumDuration(0)
        progress.setValue(0)
        
        try:
            # Import experiments module
            import sys
            import os
            exp_path = os.path.join(os.path.dirname(__file__), 'experiment')
            if exp_path not in sys.path:
                sys.path.insert(0, exp_path)
            
            from chapter3_experiments_v2 import Chapter3Experiments
            
            experiments = Chapter3Experiments()
            
            # Run experiments
            progress.setLabelText("Running 3.1.1.a: GBFS Parameters...")
            progress.setValue(1)
            QApplication.processEvents()
            if progress.wasCanceled():
                QMessageBox.information(self, "Cancelled", "Experiments cancelled.")
                return
            try:
                experiments.experiment_3_1_1_a_gbfs_parameters()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"3.1.1.a failed: {str(e)}\nContinuing...")
            
            progress.setLabelText("Running 3.1.1.b: BPSO Swarm Size...")
            progress.setValue(2)
            QApplication.processEvents()
            if progress.wasCanceled():
                QMessageBox.information(self, "Cancelled", "Experiments cancelled.")
                return
            try:
                experiments.experiment_3_1_1_b_bpso_swarm_size()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"3.1.1.b failed: {str(e)}\nContinuing...")
            
            progress.setLabelText("Running 3.1.1.c: BPSO Iterations...")
            progress.setValue(3)
            QApplication.processEvents()
            if progress.wasCanceled():
                QMessageBox.information(self, "Cancelled", "Experiments cancelled.")
                return
            try:
                experiments.experiment_3_1_1_c_bpso_iterations()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"3.1.1.c failed: {str(e)}\nContinuing...")
            
            progress.setLabelText("Running 3.1.2: Algorithm Comparison (Single)...")
            progress.setValue(4)
            QApplication.processEvents()
            if progress.wasCanceled():
                QMessageBox.information(self, "Cancelled", "Experiments cancelled.")
                return
            try:
                experiments.experiment_3_1_2_algorithm_comparison_single('Size Medium 50')
            except Exception as e:
                QMessageBox.warning(self, "Error", f"3.1.2 single failed: {str(e)}\nContinuing...")
            
            progress.setLabelText("Running 3.1.2: Algorithm Comparison (All)...")
            progress.setValue(5)
            QApplication.processEvents()
            if progress.wasCanceled():
                QMessageBox.information(self, "Cancelled", "Experiments cancelled.")
                return
            try:
                experiments.experiment_3_1_2_algorithm_comparison_all()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"3.1.2 all failed: {str(e)}\nContinuing...")
            
            progress.setValue(6)
            progress.setLabelText("Experiments completed!")
            
            QMessageBox.information(
                self,
                "Experiments Completed",
                "All Chapter 3 experiments completed!\n\n"
                "Results saved to: results/chapter3/\n\n"
                "Loading results..."
            )
            
            # Auto-load results
            self.load_experiment_results()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Experiment Error",
                f"Failed to run experiments:\n{str(e)}\n\n"
                "Check console for details."
            )
            import traceback
            traceback.print_exc()
        finally:
            progress.close()
    
    def load_experiment_results(self):
        """Load and visualize experiment results from CSV"""
        try:
            import os
            results_dir = 'results/chapter3'
            
            if not os.path.exists(results_dir):
                QMessageBox.warning(
                    self,
                    "No Results",
                    f"Results directory not found: {results_dir}\n\n"
                    "Please run experiments first."
                )
                return
            
            # Find CSV files
            csv_files = [f for f in os.listdir(results_dir) if f.endswith('.csv')]
            
            if not csv_files:
                QMessageBox.warning(
                    self,
                    "No Results",
                    "No CSV result files found.\n\n"
                    "Please run experiments first."
                )
                return
            
            # Let user choose which result to view
            result_file, ok = QInputDialog.getItem(
                self,
                "Select Result File",
                "Choose experiment result to visualize:",
                csv_files,
                0,
                False
            )
            
            if not ok:
                return
            
            # Load and visualize
            filepath = os.path.join(results_dir, result_file)
            df = pd.read_csv(filepath)
            
            fig = self.canvas_experiments.fig
            fig.clear()
            
            # Visualize based on file type
            if '3_1_1' in result_file:
                # Parameter analysis
                self.visualize_parameter_analysis(df, fig, result_file)
            elif '3_1_2' in result_file:
                # Algorithm comparison
                self.visualize_algorithm_comparison_csv(df, fig, result_file)
            elif '3_1_3' in result_file:
                # Data characteristics
                self.visualize_data_characteristics(df, fig, result_file)
            else:
                # Generic table view
                ax = fig.add_subplot(111)
                ax.axis('tight')
                ax.axis('off')
                table_data = df.head(20).values
                table = ax.table(cellText=table_data, colLabels=df.columns,
                               cellLoc='center', loc='center')
                table.auto_set_font_size(False)
                table.set_fontsize(8)
                table.scale(1, 2)
                ax.set_title(f'Results: {result_file}', fontsize=14, fontweight='bold', pad=20)
            
            fig.tight_layout()
            self.canvas_experiments.draw()
            
            # Switch to experiments tab
            self.tabs.setCurrentWidget(self.tab_experiments)
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Load Error",
                f"Failed to load results:\n{str(e)}"
            )
            import traceback
            traceback.print_exc()
    
    def visualize_parameter_analysis(self, df, fig, filename):
        """Visualize parameter impact - GA_TSP style"""
        ax = fig.add_subplot(111)
        
        # Auto-detect column names (handle both formats)
        value_col = 'value' if 'value' in df.columns else 'avg_value'
        value_std_col = 'value_std' if 'value_std' in df.columns else 'std_value'
        
        if 'gbfs' in filename.lower():
            # GBFS: max_states
            param_col = 'max_states'
            ax.plot(df[param_col], df[value_col], 'b-o', linewidth=2, markersize=8, label='Value')
            if value_std_col in df.columns:
                ax.fill_between(df[param_col], 
                               df[value_col] - df[value_std_col], 
                               df[value_col] + df[value_std_col],
                               alpha=0.2, color='blue')
            ax.set_xlabel('Max States', fontsize=12, fontweight='bold')
            ax.set_ylabel('Solution Value', fontsize=12, fontweight='bold')
            ax.set_title('GBFS Parameter Impact', fontsize=14, fontweight='bold')
        
        elif 'swarm' in filename.lower():
            # BPSO: swarm size
            param_col = 'param_value' if 'param_value' in df.columns else 'n_particles'
            ax.plot(df[param_col], df[value_col], 'r-s', linewidth=2, markersize=8, label='Value')
            if value_std_col in df.columns:
                ax.fill_between(df[param_col],
                               df[value_col] - df[value_std_col],
                               df[value_col] + df[value_std_col],
                               alpha=0.2, color='red')
            ax.set_xlabel('Swarm Size', fontsize=12, fontweight='bold')
            ax.set_ylabel('Solution Value', fontsize=12, fontweight='bold')
            ax.set_title('BPSO Parameter Impact: Swarm Size', fontsize=14, fontweight='bold')
        
        elif 'iteration' in filename.lower():
            # BPSO: iterations
            param_col = 'param_value' if 'param_value' in df.columns else 'max_iterations'
            ax.plot(df[param_col], df[value_col], 'g-^', linewidth=2, markersize=8, label='Value')
            if value_std_col in df.columns:
                ax.fill_between(df[param_col],
                               df[value_col] - df[value_std_col],
                               df[value_col] + df[value_std_col],
                               alpha=0.2, color='green')
            ax.set_xlabel('Max Iterations', fontsize=12, fontweight='bold')
            ax.set_ylabel('Solution Value', fontsize=12, fontweight='bold')
            ax.set_title('BPSO Parameter Impact: Iterations', fontsize=14, fontweight='bold')
        
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def visualize_algorithm_comparison_csv(self, df, fig, filename):
        """Visualize algorithm comparison - GA_TSP style"""
        # Create 2x2 subplots
        ax1 = fig.add_subplot(2, 2, 1)
        ax2 = fig.add_subplot(2, 2, 2)
        ax3 = fig.add_subplot(2, 2, 3)
        ax4 = fig.add_subplot(2, 2, 4)
        
        # Auto-detect column names (try all possible formats)
        if 'value' in df.columns:
            value_col = 'value'
        elif 'value_mean' in df.columns:
            value_col = 'value_mean'
        elif 'avg_value' in df.columns:
            value_col = 'avg_value'
        else:
            value_col = df.columns[1]  # Assume 2nd column
        
        if 'time' in df.columns:
            time_col = 'time'
        elif 'time_mean' in df.columns:
            time_col = 'time_mean'
        elif 'avg_time' in df.columns:
            time_col = 'avg_time'
        else:
            time_col = None
        
        # Extract algorithm data
        if 'algorithm' in df.columns:
            algorithms = df['algorithm'].unique()
            values = [df[df['algorithm'] == alg][value_col].mean() for alg in algorithms]
            times = [df[df['algorithm'] == alg][time_col].mean() for alg in algorithms] if time_col else [1e-6] * len(algorithms)
        else:
            # Fallback: assume first 3 rows
            algorithms = ['GBFS', 'BPSO', 'DP']
            values = df[value_col].head(3).tolist() if len(df) >= 3 else df[value_col].tolist()
            times = df[time_col].head(3).tolist() if time_col and len(df) >= 3 else [1e-6] * len(values)
        
        colors = ['#3498db', '#e74c3c', '#2ecc71']
        
        # Plot 1: Value
        ax1.bar(algorithms, values, color=colors[:len(algorithms)])
        ax1.set_title('Solution Value', fontweight='bold', fontsize=11)
        ax1.set_ylabel('Value')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Plot 2: Time
        ax2.bar(algorithms, times, color=colors[:len(algorithms)])
        ax2.set_title('Execution Time', fontweight='bold', fontsize=11)
        ax2.set_ylabel('Time (s)')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Plot 3: Efficiency
        efficiency = [v/max(t, 1e-6) for v, t in zip(values, times)]  # Prevent div by zero
        ax3.bar(algorithms, efficiency, color=colors[:len(algorithms)])
        ax3.set_title('Efficiency (Value/Time)', fontweight='bold', fontsize=11)
        ax3.set_ylabel('Efficiency')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Plot 4: Summary
        summary = "Algorithm Comparison\n" + "="*22 + "\n\n"
        for i, alg in enumerate(algorithms):
            summary += f"{alg}:\n"
            summary += f"  Value: {values[i]:.2f}\n"
            summary += f"  Time:  {times[i]:.4f}s\n"
            summary += f"  Eff:   {efficiency[i]:.2f}\n\n"
        ax4.text(0.05, 0.95, summary, fontsize=9, family='monospace', 
                va='top', transform=ax4.transAxes)
        ax4.axis('off')
    
    def visualize_data_characteristics(self, df, fig, filename):
        """Visualize data characteristics impact"""
        ax = fig.add_subplot(111)
        
        if 'correlation' in df.columns:
            # Group by correlation level
            for alg in df['algorithm'].unique() if 'algorithm' in df.columns else ['GBFS', 'BPSO', 'DP']:
                alg_data = df[df['algorithm'] == alg] if 'algorithm' in df.columns else df
                ax.plot(alg_data['correlation'], alg_data['avg_value'], 'o-', 
                       label=alg, linewidth=2, markersize=8)
            
            ax.set_xlabel('Correlation (w, v)', fontsize=12, fontweight='bold')
            ax.set_ylabel('Average Value', fontsize=12, fontweight='bold')
            ax.set_title('Data Characteristics: Correlation Impact', fontsize=14, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Set app-wide font
    font = QFont('Arial', 10)
    app.setFont(font)
    
    gui = KnapsackGUIEnhanced()
    gui.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
