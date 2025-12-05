"""
=================================================================================
KNAPSACK SOLVER - Interactive GUI
=================================================================================
Clean GUI inspired by GA_TSP structure
Left panel: Controls | Right panel: Interactive Visualization
=================================================================================
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import numpy as np

from src.gbfs_knapsack import solve_knapsack_gbfs
from src.bpso_knapsack import solve_knapsack_bpso
from src.dp_knapsack import solve_knapsack_dp
from src.test_case_loader import TestCaseLoader
from src.algorithm_visualizer import AlgorithmVisualizer


class InteractiveCanvas(FigureCanvasQTAgg):
    """Interactive matplotlib canvas with click support"""
    
    item_clicked = pyqtSignal(int)  # Signal when item is clicked
    
    def __init__(self, parent=None, width=8, height=6, dpi=100):
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)
        
        # Interactive state
        self.clickable = False
        self.item_positions = []
        self.selected_items = set()
        
        # Connect mouse click
        self.mpl_connect('button_press_event', self.on_click)
    
    def on_click(self, event):
        """Handle mouse click on items"""
        if not self.clickable or event.inaxes != self.ax:
            return
        
        # Find nearest item
        min_dist = float('inf')
        clicked_idx = -1
        
        for idx, (x, y) in enumerate(self.item_positions):
            # Calculate distance in data coordinates
            dist = np.sqrt((event.xdata - x)**2 + (event.ydata - y)**2)
            if dist < min_dist:
                min_dist = dist
                clicked_idx = idx
        
        # Toggle selection if close enough
        if clicked_idx >= 0 and min_dist < 50:  # Threshold
            if clicked_idx in self.selected_items:
                self.selected_items.remove(clicked_idx)
            else:
                self.selected_items.add(clicked_idx)
            
            self.item_clicked.emit(clicked_idx)
    
    def set_clickable(self, clickable, positions=None):
        """Enable/disable click interaction"""
        self.clickable = clickable
        if positions is not None:
            self.item_positions = positions


class MatplotlibCanvas(FigureCanvasQTAgg):
    """Simple matplotlib canvas for Qt"""
    def __init__(self, parent=None, width=8, height=6, dpi=100):
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)


class KnapsackSolverGUI(QMainWindow):
    """Main GUI window - inspired by GA_TSP vietnam_tsp_travel.py"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Knapsack Solver: GBFS vs BPSO vs DP")
        self.setGeometry(100, 100, 1400, 800)
        
        # Data
        self.loader = TestCaseLoader()
        self.current_test_case = None
        self.results = {}
        self.manual_selection = set()  # Manual item selection
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI components"""
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        
        # Left panel: Controls (30%)
        left_panel = self.create_control_panel()
        layout.addWidget(left_panel, 3)
        
        # Right panel: Visualization (70%)
        right_panel = self.create_visualization_panel()
        layout.addWidget(right_panel, 7)
    
    def create_control_panel(self):
        """Left control panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Title
        title = QLabel("CONTROLS")
        title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # Test case selection
        layout.addWidget(QLabel("Test Case:"))
        self.test_case_combo = QComboBox()
        test_cases = self.loader.list_test_cases()
        self.test_case_combo.addItems(test_cases)
        self.test_case_combo.currentTextChanged.connect(self.on_test_case_changed)
        layout.addWidget(self.test_case_combo)
        
        # Test case info
        self.info_label = QLabel()
        self.info_label.setStyleSheet("background: #f0f0f0; padding: 10px; border-radius: 5px;")
        layout.addWidget(self.info_label)
        
        layout.addWidget(QLabel("\nAlgorithm Parameters:"))
        
        # GBFS parameters
        layout.addWidget(QLabel("GBFS Max States:"))
        self.gbfs_states = QSpinBox()
        self.gbfs_states.setRange(1000, 20000)
        self.gbfs_states.setValue(5000)
        self.gbfs_states.setSingleStep(1000)
        layout.addWidget(self.gbfs_states)
        
        # BPSO parameters
        layout.addWidget(QLabel("BPSO Particles:"))
        self.bpso_particles = QSpinBox()
        self.bpso_particles.setRange(10, 100)
        self.bpso_particles.setValue(30)
        self.bpso_particles.setSingleStep(10)
        layout.addWidget(self.bpso_particles)
        
        layout.addWidget(QLabel("BPSO Iterations:"))
        self.bpso_iterations = QSpinBox()
        self.bpso_iterations.setRange(50, 500)
        self.bpso_iterations.setValue(100)
        self.bpso_iterations.setSingleStep(50)
        layout.addWidget(self.bpso_iterations)
        
        layout.addWidget(QLabel(""))
        
        # Manual selection controls
        manual_label = QLabel("Manual Selection:")
        manual_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(manual_label)
        
        # Clear selection button
        self.clear_btn = QPushButton("Clear Selection")
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                padding: 8px;
                font-size: 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_manual_selection)
        layout.addWidget(self.clear_btn)
        
        layout.addWidget(QLabel(""))
        
        # Run button
        self.run_btn = QPushButton("Run All Algorithms")
        self.run_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 15px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.run_btn.clicked.connect(self.run_algorithms)
        layout.addWidget(self.run_btn)
        
        # Progress
        self.progress_label = QLabel()
        layout.addWidget(self.progress_label)
        
        # Results table
        layout.addWidget(QLabel("\nResults:"))
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(['Algorithm', 'Value', 'Time (s)', 'Items'])
        self.results_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.results_table)
        
        layout.addStretch()
        
        # Initialize with first test case
        self.on_test_case_changed(self.test_case_combo.currentText())
        
        return panel
    
    def create_visualization_panel(self):
        """Right visualization panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Title
        title = QLabel("VISUALIZATION")
        title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Tab 1: Items Distribution (Interactive!)
        self.canvas_items = InteractiveCanvas(self, width=8, height=6)
        self.canvas_items.item_clicked.connect(self.on_item_clicked)
        self.tabs.addTab(self.canvas_items, "Items (Click to Select)")
        
        # Tab 2: GBFS State Tree
        self.canvas_gbfs = MatplotlibCanvas(self, width=8, height=6)
        self.tabs.addTab(self.canvas_gbfs, "GBFS Tree")
        
        # Tab 3: BPSO Swarm
        self.canvas_bpso_swarm = MatplotlibCanvas(self, width=8, height=6)
        self.tabs.addTab(self.canvas_bpso_swarm, "BPSO Swarm")
        
        # Tab 4: BPSO Convergence
        self.canvas_bpso_conv = MatplotlibCanvas(self, width=8, height=6)
        self.tabs.addTab(self.canvas_bpso_conv, "BPSO Convergence")
        
        # Tab 5: DP Table
        self.canvas_dp = MatplotlibCanvas(self, width=8, height=6)
        self.tabs.addTab(self.canvas_dp, "DP Table")
        
        # Tab 6: Comparison
        self.canvas_comparison = MatplotlibCanvas(self, width=8, height=6)
        self.tabs.addTab(self.canvas_comparison, "Comparison")
        
        layout.addWidget(self.tabs)
        
        return panel
    
    def on_test_case_changed(self, test_case_name):
        """Load test case"""
        try:
            self.current_test_case = self.loader.load_test_case(test_case_name)
            
            # Validate test case has required keys
            if not all(key in self.current_test_case for key in ['items', 'weights', 'values', 'capacity']):
                raise KeyError("Test case missing required keys")
            
            # Update info
            tc = self.current_test_case
            info_text = f"""
            <b>Items:</b> {len(tc['items'])}<br>
            <b>Capacity:</b> {tc['capacity']}<br>
            <b>Total Weight:</b> {sum(tc['weights']):.0f}<br>
            <b>Total Value:</b> {sum(tc['values']):.0f}
            """
            self.info_label.setText(info_text)
            
            # Clear manual selection when changing test case
            self.manual_selection = set()
            if hasattr(self, 'canvas_items'):
                self.canvas_items.selected_items = set()
            
            # Visualize items
            self.visualize_items()
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load test case: {e}")
    
    def visualize_items(self):
        """Visualize items distribution with manual selection"""
        if self.current_test_case is None:
            return
        
        if not hasattr(self, 'canvas_items'):
            return  # Canvas not initialized yet
        
        ax = self.canvas_items.ax
        ax.clear()
        
        tc = self.current_test_case
        weights = np.array(tc['weights'])
        values = np.array(tc['values'])
        
        # Plot unselected items
        unselected_mask = np.ones(len(weights), dtype=bool)
        if self.manual_selection:
            unselected_mask[list(self.manual_selection)] = False
        
        ax.scatter(weights[unselected_mask], values[unselected_mask], 
                  s=100, alpha=0.5, color='lightgray', edgecolors='black',
                  label='Available', picker=5)
        
        # Plot selected items
        if self.manual_selection:
            selected_indices = list(self.manual_selection)
            ax.scatter(weights[selected_indices], values[selected_indices],
                      s=150, alpha=0.8, color='green', marker='s',
                      edgecolors='black', linewidths=2,
                      label=f'Selected ({len(selected_indices)})', picker=5)
            
            # Show selection stats
            total_weight = np.sum(weights[selected_indices])
            total_value = np.sum(values[selected_indices])
            capacity_pct = (total_weight / tc['capacity']) * 100
            
            stats_text = f"Selection: {len(selected_indices)} items\n"
            stats_text += f"Value: {total_value:.0f} | Weight: {total_weight:.0f}/{tc['capacity']} ({capacity_pct:.1f}%)"
            
            ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
                   verticalalignment='top', fontsize=10,
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        ax.set_xlabel('Weight', fontsize=12)
        ax.set_ylabel('Value', fontsize=12)
        ax.set_title(f"Items Distribution - {tc['name']} (Click to Select/Deselect)", 
                    fontsize=14, fontweight='bold')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
        
        # Enable interaction
        positions = list(zip(weights, values))
        self.canvas_items.set_clickable(True, positions)
        
        self.canvas_items.draw()
    
    def on_item_clicked(self, item_idx):
        """Handle item click - toggle selection"""
        # Sync with canvas selection
        self.manual_selection = self.canvas_items.selected_items.copy()
        
        # Redraw
        self.visualize_items()
        
        # Show message
        tc = self.current_test_case
        if item_idx in self.manual_selection:
            self.progress_label.setText(
                f"✓ Selected: {tc['items'][item_idx]} "
                f"(W={tc['weights'][item_idx]:.0f}, V={tc['values'][item_idx]:.0f})"
            )
        else:
            self.progress_label.setText(
                f"✗ Deselected: {tc['items'][item_idx]}"
            )
    
    def clear_manual_selection(self):
        """Clear all manual selections"""
        self.manual_selection = set()
        self.canvas_items.selected_items = set()
        self.visualize_items()
        self.progress_label.setText("🗑️ Selection cleared")
    
    def run_algorithms(self):
        """Run all three algorithms"""
        if self.current_test_case is None:
            return
        
        tc = self.current_test_case
        self.results = {}
        
        try:
            # GBFS
            self.progress_label.setText("Running GBFS...")
            QApplication.processEvents()
            self.results['GBFS'] = solve_knapsack_gbfs(
                tc['items'], tc['weights'], tc['values'], tc['capacity'],
                max_states=self.gbfs_states.value()
            )
            
            # BPSO
            self.progress_label.setText("Running BPSO...")
            QApplication.processEvents()
            self.results['BPSO'] = solve_knapsack_bpso(
                tc['items'], tc['weights'], tc['values'], tc['capacity'],
                n_particles=self.bpso_particles.value(),
                max_iterations=self.bpso_iterations.value()
            )
            
            # DP
            self.progress_label.setText("Running DP...")
            QApplication.processEvents()
            self.results['DP'] = solve_knapsack_dp(
                tc['items'], tc['weights'], tc['values'], tc['capacity']
            )
            
            self.progress_label.setText("✅ Complete!")
            
            # Update displays
            self.update_results_table()
            self.visualize_all_results()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Algorithm failed: {e}\n{str(e.__traceback__)}")
            self.progress_label.setText("❌ Failed")
    
    def update_results_table(self):
        """Update results table"""
        self.results_table.setRowCount(len(self.results))
        
        for i, (algo, result) in enumerate(self.results.items()):
            self.results_table.setItem(i, 0, QTableWidgetItem(algo))
            self.results_table.setItem(i, 1, QTableWidgetItem(f"{result['total_value']:.1f}"))
            self.results_table.setItem(i, 2, QTableWidgetItem(f"{result['execution_time']:.4f}"))
            self.results_table.setItem(i, 3, QTableWidgetItem(str(len(result['selected_items']))))
    
    def visualize_all_results(self):
        """Visualize results in all tabs"""
        if not self.results:
            return
        
        # GBFS Tree
        if 'GBFS' in self.results:
            AlgorithmVisualizer.visualize_gbfs_tree(
                self.canvas_gbfs.ax, self.results['GBFS'], max_nodes=30
            )
            self.canvas_gbfs.draw()
        
        # BPSO Swarm (show first and last iteration)
        if 'BPSO' in self.results:
            AlgorithmVisualizer.visualize_bpso_swarm(
                self.canvas_bpso_swarm.ax, self.results['BPSO'], iteration_idx=-1
            )
            self.canvas_bpso_swarm.draw()
            
            AlgorithmVisualizer.visualize_bpso_convergence(
                self.canvas_bpso_conv.ax, self.results['BPSO']
            )
            self.canvas_bpso_conv.draw()
        
        # DP Table
        if 'DP' in self.results:
            AlgorithmVisualizer.visualize_dp_table(
                self.canvas_dp.ax, self.results['DP'], show_values=True
            )
            self.canvas_dp.draw()
        
        # Comparison
        self.visualize_comparison()
    
    def visualize_comparison(self):
        """Visualize algorithm comparison"""
        if not self.results:
            return
        
        ax = self.canvas_comparison.ax
        ax.clear()
        
        tc = self.current_test_case
        weights = np.array(tc['weights'])
        values = np.array(tc['values'])
        
        # Plot all items
        ax.scatter(weights, values, s=80, alpha=0.3, color='gray', label='Not selected')
        
        # Plot selected items for each algorithm
        colors = {'GBFS': 'blue', 'BPSO': 'red', 'DP': 'green'}
        markers = {'GBFS': 'o', 'BPSO': 's', 'DP': '^'}
        
        for algo, result in self.results.items():
            indices = result['selected_indices']
            if indices:
                sel_w = weights[indices]
                sel_v = values[indices]
                ax.scatter(sel_w, sel_v, s=150, alpha=0.7, 
                          color=colors[algo], marker=markers[algo], 
                          label=f"{algo} ({result['total_value']:.0f})", 
                          edgecolors='black', linewidths=1.5)
        
        ax.set_xlabel('Weight', fontsize=12)
        ax.set_ylabel('Value', fontsize=12)
        ax.set_title('Algorithm Comparison - Selected Items', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        self.canvas_comparison.draw()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern style
    window = KnapsackSolverGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
