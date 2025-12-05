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
        title = QLabel("🎒 KNAPSACK SOLVER")
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
        problem_group = QGroupBox("📋 Problem Definition")
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
        test_group = QGroupBox("📂 Test Case Selection")
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
        params_group = QGroupBox("⚙️ Algorithm Parameters")
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
        
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)
        
        # ===== RUN BUTTON =====
        self.run_btn = QPushButton("🚀 RUN ALL ALGORITHMS")
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
        self.tabs.addTab(self.tab_problem, "📍 Problem Visualization")
        
        # Tab 2: BPSO Convergence
        self.tab_convergence = QWidget()
        self.tab_convergence_layout = QVBoxLayout(self.tab_convergence)
        self.canvas_convergence = MatplotlibCanvas(width=14, height=10)
        self.tab_convergence_layout.addWidget(self.canvas_convergence)
        self.tabs.addTab(self.tab_convergence, "📈 BPSO Convergence")
        
        # Tab 3: Algorithm Comparison
        self.tab_comparison = QWidget()
        self.tab_comparison_layout = QVBoxLayout(self.tab_comparison)
        self.canvas_comparison = MatplotlibCanvas(width=14, height=10)
        self.tab_comparison_layout.addWidget(self.canvas_comparison)
        self.tabs.addTab(self.tab_comparison, "⚖️ Algorithm Comparison")
        
        # Tab 4: Solution Details
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
        
        self.tabs.addTab(self.tab_solution, "📊 Solution Details")
        
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
                                    w=self.bpso_w.value())
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
        
        # Tab 2: BPSO Convergence
        self.visualize_convergence()
        
        # Tab 3: Algorithm Comparison
        self.visualize_comparison()
        
        # Tab 4: Solution table
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
