"""
=================================================================================
KNAPSACK SOLVER - UNIFIED GUI (Version 2.0)
=================================================================================
Combines best features from both previous GUIs:
1. Interactive item selection (click to select)
2. Algorithm visualization (show selection process)
3. Chapter 3 experiments integration
=================================================================================
Problem: Multi-Objective 0/1 Knapsack
- Objective 1: Maximize total value
- Objective 2: Maximize regional diversity
- Constraint: Total weight ≤ Capacity

Algorithms:
- GBFS (Greedy Best-First Search): Fast heuristic
- BPSO (Binary Particle Swarm Optimization): Metaheuristic
=================================================================================
"""

import sys
import os
import numpy as np
import pandas as pd
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

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
from src.algorithms import solve_knapsack_gbfs, solve_knapsack_bpso
from src.visualization import (
    visualize_gbfs_selection_steps,
    visualize_bpso_swarm_behavior,
    AdvancedKnapsackVisualizer
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
            self.progress.emit(f"Running {self.algorithm}...")
            
            # Extract item names, weights, values, regions
            item_names = [item['name'] for item in self.items]
            weights = [item['weight'] for item in self.items]
            values = [item['value'] for item in self.items]
            regions = [item.get('region') for item in self.items]  # May be None
            
            if self.algorithm == "GBFS":
                result = solve_knapsack_gbfs(
                    item_names, weights, values, self.capacity,
                    regions=regions,
                    max_states=self.params.get('max_states', 5000)
                )
            elif self.algorithm == "BPSO":
                result = solve_knapsack_bpso(
                    item_names, weights, values, self.capacity,
                    regions=regions,
                    n_particles=self.params.get('n_particles', 30),
                    max_iterations=self.params.get('max_iterations', 50),
                    w=self.params.get('w', 0.7),
                    c1=self.params.get('c1', 2.0),
                    c2=self.params.get('c2', 2.0)
                )
            else:
                raise ValueError(f"Unknown algorithm: {self.algorithm}")
            
            result['algorithm'] = self.algorithm
            self.finished.emit(result)
            
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            self.progress.emit(f"Error: {str(e)}")
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
        self.visualizer = AdvancedKnapsackVisualizer()  # Shared visualizer
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
        self.setWindowTitle('Knapsack Solver - Multi-Objective Optimization (GBFS | BPSO)')
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
                font-family: Arial, sans-serif;
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
                         "f1: Revenue  |  f2: Regional Diversity")
        subtitle.setStyleSheet("font-size: 10px; color: #7f8c8d; padding: 3px;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        # === PROBLEM DEFINITION ===
        problem_group = QGroupBox("Problem Definition")
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
        testcase_group = QGroupBox("Test Case Selection")
        testcase_layout = QVBoxLayout()
        
        testcase_layout.addWidget(QLabel("Select Test Case:"))
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
        params_group = QGroupBox("Algorithm Parameters")
        params_layout = QVBoxLayout()
        
        # GBFS
        params_layout.addWidget(QLabel("GBFS:"))
        gbfs_layout = QHBoxLayout()
        gbfs_layout.addWidget(QLabel("Max States:"))
        self.gbfs_max_states = QSpinBox()
        self.gbfs_max_states.setRange(1000, 20000)
        self.gbfs_max_states.setValue(5000)
        self.gbfs_max_states.setSingleStep(1000)
        gbfs_layout.addWidget(self.gbfs_max_states)
        params_layout.addLayout(gbfs_layout)
        
        # BPSO
        params_layout.addWidget(QLabel("BPSO:"))
        
        bpso_particles_layout = QHBoxLayout()
        bpso_particles_layout.addWidget(QLabel("Particles:"))
        self.bpso_particles = QSpinBox()
        self.bpso_particles.setRange(10, 100)
        self.bpso_particles.setValue(30)
        bpso_particles_layout.addWidget(self.bpso_particles)
        params_layout.addLayout(bpso_particles_layout)
        
        bpso_iter_layout = QHBoxLayout()
        bpso_iter_layout.addWidget(QLabel("Iterations:"))
        self.bpso_iterations = QSpinBox()
        self.bpso_iterations.setRange(10, 200)
        self.bpso_iterations.setValue(50)
        bpso_iter_layout.addWidget(self.bpso_iterations)
        params_layout.addLayout(bpso_iter_layout)
        
        bpso_w_layout = QHBoxLayout()
        bpso_w_layout.addWidget(QLabel("Inertia (w):"))
        self.bpso_w = QDoubleSpinBox()
        self.bpso_w.setRange(0.1, 1.0)
        self.bpso_w.setValue(0.7)
        self.bpso_w.setSingleStep(0.1)
        bpso_w_layout.addWidget(self.bpso_w)
        params_layout.addLayout(bpso_w_layout)
        
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)
        
        # === ACTION BUTTONS ===
        buttons_group = QGroupBox("Actions")
        buttons_layout = QVBoxLayout()
        
        self.run_all_btn = QPushButton("RUN ALL ALGORITHMS")
        self.run_all_btn.setStyleSheet("""
            background-color: #27ae60;
            color: white;
            font-size: 12px;
            padding: 10px;
        """)
        self.run_all_btn.clicked.connect(self.run_all_algorithms)
        buttons_layout.addWidget(self.run_all_btn)
        
        self.run_chapter3_btn = QPushButton("RUN CHAPTER 3 EXPERIMENTS")
        self.run_chapter3_btn.setStyleSheet("""
            background-color: #e67e22;
            color: white;
            font-size: 11px;
        """)
        self.run_chapter3_btn.clicked.connect(self.run_chapter3_experiments)
        buttons_layout.addWidget(self.run_chapter3_btn)
        
        self.export_btn = QPushButton("EXPORT RESULTS")
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
        
        # Tab 1: GBFS Algorithm Flow
        self.tab_gbfs = self.create_gbfs_tab()
        self.tabs.addTab(self.tab_gbfs, "GBFS Flow")
        
        # Tab 2: BPSO Algorithm
        self.tab_bpso = self.create_bpso_tab()
        self.tabs.addTab(self.tab_bpso, "BPSO Swarm")
        
        # Tab 4: Algorithm Comparison
        self.tab_comparison = self.create_comparison_tab()
        self.tabs.addTab(self.tab_comparison, "Comparison")
        
        # Tab 5: Regional Analysis
        self.tab_regional = self.create_regional_tab()
        self.tabs.addTab(self.tab_regional, "Regional")
        
        # Tab 6: Solution Details
        self.tab_solution = self.create_solution_tab()
        self.tabs.addTab(self.tab_solution, "Details")
        
        # Tab 7: Chapter 3 Results
        self.tab_chapter3 = self.create_chapter3_tab()
        self.tabs.addTab(self.tab_chapter3, "Chapter 3")
        
        # Set default tab to first one (GBFS Flow)
        self.tabs.setCurrentIndex(0)
        
        layout.addWidget(self.tabs)
        
        return panel
    
    # =========================================================================
    # TAB CREATION
    # =========================================================================
    
    def create_gbfs_tab(self):
        """Tab 1: GBFS algorithm flow"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        info = QLabel("GBFS Selection Process: Greedy selection by value/weight ratio")
        info.setStyleSheet("background-color: #e8f5e9; padding: 8px;")
        layout.addWidget(info)
        
        self.gbfs_fig = Figure(figsize=(12, 9), facecolor='white')
        self.gbfs_canvas = FigureCanvas(self.gbfs_fig)
        self.gbfs_canvas.fig = self.gbfs_fig  # Add fig attribute
        layout.addWidget(self.gbfs_canvas)
        
        return tab
    
    def create_bpso_tab(self):
        """Tab 3: BPSO swarm behavior"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        info = QLabel("BPSO Convergence & Swarm Behavior")
        info.setStyleSheet("background-color: #e3f2fd; padding: 8px;")
        layout.addWidget(info)
        
        self.bpso_fig = Figure(figsize=(12, 9), facecolor='white')
        self.bpso_canvas = FigureCanvas(self.bpso_fig)
        self.bpso_canvas.fig = self.bpso_fig  # Add fig attribute
        layout.addWidget(self.bpso_canvas)
        
        return tab
    
    def create_comparison_tab(self):
        """Tab 5: Algorithm comparison"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        info = QLabel("GBFS vs BPSO - Performance Comparison")
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
        """Tab 7: Solution details table - Both GBFS and BPSO"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        info = QLabel("Detailed Solution - Selected Items")
        info.setStyleSheet("background-color: #e0f2f1; padding: 8px;")
        layout.addWidget(info)
        
        # GBFS Table
        gbfs_label = QLabel("🔍 GBFS (Greedy Best-First Search) - Selected Items")
        gbfs_label.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px; font-weight: bold;")
        layout.addWidget(gbfs_label)
        
        self.gbfs_solution_table = QTableWidget()
        self.gbfs_solution_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #bdc3c7;
                font-size: 10px;
            }
            QHeaderView::section {
                background-color: #388E3C;
                color: white;
                padding: 5px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.gbfs_solution_table)
        
        # BPSO Table
        bpso_label = QLabel("🐝 BPSO (Binary Particle Swarm Optimization) - Selected Items")
        bpso_label.setStyleSheet("background-color: #2196F3; color: white; padding: 5px; font-weight: bold;")
        layout.addWidget(bpso_label)
        
        self.bpso_solution_table = QTableWidget()
        self.bpso_solution_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #bdc3c7;
                font-size: 10px;
            }
            QHeaderView::section {
                background-color: #1976D2;
                color: white;
                padding: 5px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.bpso_solution_table)
        
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
            "3.1.1.d - BPSO Inertia Weight",
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
                if 'Region' in self.test_data_df.columns:
                    # Map region names to numbers
                    region_map = {}
                    for i, r in enumerate(self.test_data_df['Region'].unique()):
                        region_map[r] = i + 1
                    self.test_data_df['region'] = self.test_data_df['Region'].map(region_map)
                else:
                    self.test_data_df['region'] = 1
            
            # Update problem info
            self.update_problem_info(test_name, info)
            
            # Update test case info
            self.update_testcase_info(info)
            
            # Clear previous results
            self.results = {}
            
            self.statusBar().showMessage(f'Loaded: {test_name}')
            
        except Exception as e:
            import traceback
            error_msg = f"Failed to load test case:\n{str(e)}\n\n{traceback.format_exc()}"
            QMessageBox.warning(self, "Error", error_msg)
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
        text = f"""Items: {info['N_Items']} | Capacity: {info['Capacity']} | Regions: {info['N_Regions']} | Total Value: {int(info['Total_Value'])}"""
        self.testcase_info.setText(text)
    
    
    def run_all_algorithms(self):
        """Run all three algorithms"""
        if self.current_test_case is None:
            QMessageBox.warning(self, "Warning", "Please select a test case first!")
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
            }
        }
        
        # Prepare items in correct format for algorithms
        items_for_algo = []
        for idx, row in self.test_data_df.iterrows():
            item_dict = {
                'name': f'Item_{idx}',
                'weight': row['weight'],
                'value': row['value']
            }
            # Add region if available
            if 'Region' in row:
                item_dict['region'] = row['Region']
            elif 'region' in row:
                item_dict['region'] = row['region']
            items_for_algo.append(item_dict)
        
        # Run algorithms sequentially
        algorithms = ['GBFS', 'BPSO']
        
        try:
            for algo in algorithms:
                self.statusBar().showMessage(f'Running {algo}...')
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
            QMessageBox.critical(self, "Error", f"Algorithm execution failed:\n{str(e)}")
            self.run_all_btn.setEnabled(True)
            self.progress_bar.setVisible(False)
    def on_algorithm_progress(self, message):
        """Handle algorithm progress update"""
        self.statusBar().showMessage(message)
    
    def on_algorithm_finished(self, result):
        """Handle algorithm completion"""
        if 'error' in result:
            QMessageBox.critical(self, "Error", f"Algorithm failed:\n{result['error']}")
            return
        
        algo = result['algorithm']
        self.results[algo] = result
        
        self.statusBar().showMessage(f'{algo} completed: Value={result.get("total_value", 0)}')
        
        # If all algorithms done (only GBFS and BPSO now)
        if len(self.results) == 2:
            self.run_all_btn.setEnabled(True)
            self.progress_bar.setVisible(False)
            
            # Update visualizations
            self.update_all_visualizations()
            
            self.statusBar().showMessage("All algorithms completed!")
            
            # Keep current tab (don't auto-switch)
    
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
            print(f"Error updating visualizations: {e}")
    
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
            print(f"Error visualizing GBFS: {e}")
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
            print(f"Error visualizing BPSO: {e}")
            import traceback
            traceback.print_exc()
    
    def visualize_comparison(self):
        """Compare GBFS and BPSO algorithms"""
        if len(self.results) < 2:
            return
        
        try:
            fig = self.comparison_canvas.fig
            fig.clear()
            
            # Create comparison plot
            algorithms = ['GBFS', 'BPSO']
            values = [self.results[a]['total_value'] for a in algorithms]
            times = [self.results[a]['execution_time'] for a in algorithms]
            
            # Two subplots
            ax1 = fig.add_subplot(121)
            colors = ['#27ae60', '#3498db']
            ax1.bar(algorithms, values, color=colors, alpha=0.7)
            ax1.set_ylabel('Total Value')
            ax1.set_title('Solution Quality')
            ax1.grid(True, alpha=0.3)
            
            ax2 = fig.add_subplot(122)
            ax2.bar(algorithms, times, color=colors, alpha=0.7)
            ax2.set_ylabel('Time (seconds)')
            ax2.set_title('Execution Time')
            ax2.grid(True, alpha=0.3)
            
            fig.tight_layout()
            self.comparison_canvas.draw()
            
        except Exception as e:
            print(f"Error visualizing comparison: {e}")
    
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
            
            colors_algo = {'GBFS': '#27ae60', 'BPSO': '#3498db'}
            
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
            
            ax1.set_xlabel('Region', fontsize=10, fontweight='bold')
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
                           s=60, alpha=0.5, c=[cmap(i)], label=f'Region {region}',
                           edgecolors='black', linewidth=0.5)
            
            ax3.set_xlabel('Weight', fontsize=10, fontweight='bold')
            ax3.set_ylabel('Value', fontsize=10, fontweight='bold')
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
                               s=120, alpha=0.8, c=[cmap(i)], label=f'Region {region}',
                               edgecolors='black', linewidth=2)
            
            ax4.set_xlabel('Weight', fontsize=10, fontweight='bold')
            ax4.set_ylabel('Value', fontsize=10, fontweight='bold')
            ax4.set_title(f'{best_algo} Selection by Region', fontsize=11, fontweight='bold')
            ax4.legend(fontsize=8, loc='best', ncol=2)
            ax4.grid(True, alpha=0.3)
            
            fig.tight_layout()
            self.regional_canvas.draw()
            
        except Exception as e:
            print(f"Error visualizing regional: {e}")
            import traceback
            traceback.print_exc()
    
    def populate_solution_table(self):
        """Populate solution details table for both GBFS and BPSO"""
        if len(self.results) == 0:
            return
        
        try:
            # Populate GBFS table
            if 'GBFS' in self.results:
                self._populate_single_table(
                    self.gbfs_solution_table, 
                    self.results['GBFS'], 
                    'GBFS'
                )
            
            # Populate BPSO table
            if 'BPSO' in self.results:
                self._populate_single_table(
                    self.bpso_solution_table, 
                    self.results['BPSO'], 
                    'BPSO'
                )
            
        except Exception as e:
            print(f"Error populating table: {e}")
    
    def _populate_single_table(self, table, result, algo_name):
        """Helper to populate a single solution table"""
        selected_items = result['selected_items']
        
        # Setup table
        table.setRowCount(len(selected_items))
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels([
            'Item ID', 'Weight', 'Value', 'Region', 'Ratio', 'Algorithm'
        ])
        
        # Populate rows
        for i, item_name in enumerate(selected_items):
            # Get item index
            idx = int(item_name.split('_')[1])
            row = self.test_data_df.iloc[idx]
            
            table.setItem(i, 0, QTableWidgetItem(item_name))
            table.setItem(i, 1, QTableWidgetItem(str(row['weight'])))
            table.setItem(i, 2, QTableWidgetItem(str(row['value'])))
            table.setItem(i, 3, QTableWidgetItem(str(row.get('region', 'N/A'))))
            
            ratio = row['value'] / row['weight'] if row['weight'] > 0 else 0
            table.setItem(i, 4, QTableWidgetItem(f"{ratio:.2f}"))
            table.setItem(i, 5, QTableWidgetItem(algo_name))
        
        table.resizeColumnsToContents()
    
    def run_chapter3_experiments(self):
        """Run Chapter 3 experiments using experiments.py"""
        reply = QMessageBox.question(self, "Chapter 3 Experiments",
                               "This will run all experiments for Chapter 3.\n"
                               "It may take several minutes.\n\n"
                               "Results will be saved in results/chapter3/\n\n"
                               "Continue?",
                               QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                # Import và chạy experiments
                from experiment.chapter3.experiments import Chapter3Experiments
                
                self.status_text.append("\n" + "="*70)
                self.status_text.append("Starting Chapter 3 Experiments...")
                self.status_text.append("="*70)
                
                exp_runner = Chapter3Experiments()
                exp_runner.run_all_experiments()
                
                self.status_text.append("\n✅ All experiments completed!")
                self.status_text.append("Results saved in results/chapter3/")
                
                # Load và hiển thị experiment hiện tại
                self.load_experiment_result(self.exp_combo.currentText())
                
                QMessageBox.information(self, "Success",
                                      "All experiments completed successfully!\n\n"
                                      "Check results/chapter3/ for outputs.")
            except Exception as e:
                import traceback
                error_msg = f"Error running experiments:\n{str(e)}\n\n{traceback.format_exc()}"
                self.status_text.append(f"\n❌ Error: {str(e)}")
                QMessageBox.critical(self, "Error", error_msg)
    
    def load_experiment_result(self, exp_name):
        """Load and display experiment result PNG from experiments.py"""
        try:
            fig = self.chapter3_canvas.fig
            fig.clear()
            
            results_dir = Path(__file__).parent.parent / 'results' / 'chapter3'
            
            # Map experiment names to PNG files (generated by experiments.py)
            exp_files = {
                "3.1.1.a - GBFS Parameters": "3_1_1_a_gbfs_params.png",
                "3.1.1.b - BPSO Swarm Size": "3_1_1_b_bpso_swarm_size.png",
                "3.1.1.c - BPSO Iterations": "3_1_1_c_bpso_iterations.png",
                "3.1.1.d - BPSO Inertia Weight": "3_1_1_d_bpso_w.png",
                "3.1.2 - Algorithm Comparison": "3_1_2_comparison_Size_Medium_50.png",
                "3.1.3 - Data Characteristics": "3_1_3_data_characteristics.png"
            }
            
            if exp_name not in exp_files:
                ax = fig.add_subplot(111)
                ax.text(0.5, 0.5, f'Unknown experiment: {exp_name}',
                       ha='center', va='center', fontsize=14)
                ax.axis('off')
                self.chapter3_canvas.draw()
                return
            
            png_file = results_dir / exp_files[exp_name]
            
            if not png_file.exists():
                ax = fig.add_subplot(111)
                ax.text(0.5, 0.5, f'PNG not found:\n{png_file.name}\n\nPlease run:\npython3 main.py --regenerate',
                       ha='center', va='center', fontsize=12, color='red')
                ax.axis('off')
                self.chapter3_canvas.draw()
                return
            
            # Load and display PNG (same as generated by experiments.py)
            from PIL import Image
            import numpy as np
            
            img = Image.open(png_file)
            ax = fig.add_subplot(111)
            ax.imshow(np.array(img))
            ax.axis('off')
            ax.set_title(exp_name, fontsize=14, fontweight='bold', pad=10)
            
            fig.tight_layout()
            self.chapter3_canvas.draw()
            
        except Exception as e:
            import traceback
            print(f"Error loading experiment: {e}")
            traceback.print_exc()
            
            fig = self.chapter3_canvas.fig
            fig.clear()
            ax = fig.add_subplot(111)
            ax.text(0.5, 0.5, f'Error loading PNG:\n{str(e)}',
                   ha='center', va='center', fontsize=12, color='red')
            ax.axis('off')
            self.chapter3_canvas.draw()
                
            fig.tight_layout()
            self.chapter3_canvas.draw()
            
        except Exception as e:
            import traceback
            print(f"Error loading experiment: {e}")
            traceback.print_exc()
            
            fig = self.chapter3_canvas.fig
            fig.clear()
            ax = fig.add_subplot(111)
            ax.text(0.5, 0.5, f'Error loading experiment:\\n{str(e)}',
                   ha='center', va='center', fontsize=12, color='red')
            self.chapter3_canvas.draw()
    
    def export_results(self):
        """Export results to CSV"""
        if len(self.results) == 0:
            QMessageBox.warning(self, "Warning", "No results to export!")
            return
        
        try:
            # Create results DataFrame
            data = []
            for algo, result in self.results.items():
                data.append({
                    'Algorithm': algo,
                    'Total Value': result['total_value'],
                    'Total Weight': result['total_weight'],
                    'Region Coverage': result.get('region_coverage', 0),
                    'Items Selected': len(result['selected_items']),
                    'Execution Time': result['execution_time']
                })
            
            df = pd.DataFrame(data)
            
            # Save to CSV
            output_path = Path('results') / 'latest_results.csv'
            output_path.parent.mkdir(exist_ok=True)
            df.to_csv(output_path, index=False)
            
            QMessageBox.information(self, "Success", 
                                   f"Results exported to:\n{output_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Export failed:\n{str(e)}")


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
    app.setFont(font)
    
    # Create and show GUI
    gui = KnapsackSolverGUI()
    gui.show()
    
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())
