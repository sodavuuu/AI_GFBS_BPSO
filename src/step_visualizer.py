"""
=================================================================================
MODULE: Step-by-Step Visualizer
=================================================================================
Visualize algorithm execution step by step with interactive controls
=================================================================================
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import numpy as np
from typing import Dict, List


class StepByStepVisualizer:
    """
    Visualize algorithm execution step by step
    
    Features:
    - Show current state
    - Highlight selected items
    - Display capacity utilization
    - Show step description
    """
    
    def __init__(self, figsize=(16, 10)):
        self.figsize = figsize
        self.fig = None
        self.axes = None
    
    def visualize_gbfs_step(self, step_data: Dict, items: List[str], 
                           weights: np.ndarray, values: np.ndarray) -> plt.Figure:
        """
        Visualize one GBFS step
        
        Args:
            step_data: Step information from GBFSStepTracker
            items: List of item names
            weights: Item weights
            values: Item values
        
        Returns:
            Matplotlib figure
        """
        self.fig = plt.figure(figsize=self.figsize)
        gs = GridSpec(3, 3, figure=self.fig, hspace=0.3, wspace=0.3)
        
        # Title
        step_type = step_data.get('type', 'unknown')
        iteration = step_data.get('iteration', 0)
        message = step_data.get('message', '')
        
        self.fig.suptitle(
            f"GBFS - Step {iteration} ({step_type.upper()})\n{message}",
            fontsize=14, fontweight='bold'
        )
        
        # 1. Items scatter plot (show all items, highlight selected)
        ax1 = self.fig.add_subplot(gs[0, :2])
        self._plot_items_scatter(ax1, step_data, items, weights, values)
        
        # 2. Capacity bar
        ax2 = self.fig.add_subplot(gs[0, 2])
        self._plot_capacity_bar(ax2, step_data)
        
        # 3. Selected items table
        ax3 = self.fig.add_subplot(gs[1, :2])
        self._plot_selected_table(ax3, step_data, items, weights, values)
        
        # 4. Available items table
        ax4 = self.fig.add_subplot(gs[1, 2])
        self._plot_available_table(ax4, step_data, items, weights, values)
        
        # 5. Statistics
        ax5 = self.fig.add_subplot(gs[2, :])
        self._plot_statistics(ax5, step_data, items, weights, values)
        
        return self.fig
    
    def visualize_bpso_step(self, step_data: Dict, items: List[str],
                           weights: np.ndarray, values: np.ndarray,
                           capacity: float) -> plt.Figure:
        """
        Visualize one BPSO step
        
        Args:
            step_data: Step information from BPSOStepTracker
            items: List of item names
            weights: Item weights
            values: Item values
            capacity: Knapsack capacity
        
        Returns:
            Matplotlib figure
        """
        self.fig = plt.figure(figsize=self.figsize)
        gs = GridSpec(2, 3, figure=self.fig, hspace=0.3, wspace=0.3)
        
        iteration = step_data.get('iteration', 0)
        message = step_data.get('message', '')
        
        self.fig.suptitle(
            f"BPSO - Iteration {iteration}\n{message}",
            fontsize=14, fontweight='bold'
        )
        
        # 1. Fitness distribution
        ax1 = self.fig.add_subplot(gs[0, 0])
        self._plot_fitness_distribution(ax1, step_data)
        
        # 2. Best solution visualization
        ax2 = self.fig.add_subplot(gs[0, 1:])
        self._plot_best_solution(ax2, step_data, items, weights, values, capacity)
        
        # 3. Convergence curve
        ax3 = self.fig.add_subplot(gs[1, :2])
        self._plot_convergence_partial(ax3, step_data)
        
        # 4. Statistics table
        ax4 = self.fig.add_subplot(gs[1, 2])
        self._plot_bpso_stats(ax4, step_data)
        
        return self.fig
    
    def _plot_items_scatter(self, ax, step_data, items, weights, values):
        """Plot all items with selected ones highlighted"""
        state = step_data.get('state', [])
        considering = step_data.get('considering', -1)
        available = step_data.get('available_items', [])
        
        # Plot all items
        ax.scatter(weights, values, s=100, alpha=0.3, color='gray', 
                  label='Not selected', zorder=1)
        
        # Highlight selected items
        if state:
            selected_w = [weights[i] for i in state]
            selected_v = [values[i] for i in state]
            ax.scatter(selected_w, selected_v, s=200, alpha=0.8, 
                      color='green', marker='s', label='Selected', zorder=3)
        
        # Highlight considering item
        if considering >= 0:
            ax.scatter(weights[considering], values[considering], s=300, 
                      alpha=0.9, color='red', marker='*', 
                      label='Considering', zorder=4)
        
        # Highlight available items
        if available:
            avail_w = [weights[i] for i in available if i != considering]
            avail_v = [values[i] for i in available if i != considering]
            ax.scatter(avail_w, avail_v, s=150, alpha=0.5, 
                      color='orange', label='Available', zorder=2)
        
        ax.set_xlabel('Weight', fontsize=11)
        ax.set_ylabel('Value', fontsize=11)
        ax.set_title('Items Distribution', fontsize=12, fontweight='bold')
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)
    
    def _plot_capacity_bar(self, ax, step_data):
        """Plot capacity utilization bar"""
        current_weight = step_data.get('weight', 0)
        capacity = step_data.get('capacity', 1)
        
        percentage = (current_weight / capacity) * 100
        
        # Vertical bar
        ax.barh(0, percentage, height=0.5, color='green' if percentage <= 100 else 'red', 
               alpha=0.7, edgecolor='black', linewidth=2)
        ax.set_xlim(0, 120)
        ax.set_ylim(-0.5, 0.5)
        ax.axvline(x=100, color='red', linestyle='--', linewidth=2, label='Max Capacity')
        
        # Text
        ax.text(percentage/2, 0, f'{percentage:.1f}%', 
               ha='center', va='center', fontsize=12, fontweight='bold')
        ax.text(percentage + 5, 0, f'{current_weight:.0f}/{capacity:.0f}', 
               ha='left', va='center', fontsize=10)
        
        ax.set_yticks([])
        ax.set_xlabel('Capacity Usage (%)', fontsize=11)
        ax.set_title('Capacity Utilization', fontsize=12, fontweight='bold')
        ax.legend(loc='upper right', fontsize=9)
    
    def _plot_selected_table(self, ax, step_data, items, weights, values):
        """Plot table of selected items"""
        ax.axis('off')
        
        state = step_data.get('state', [])
        
        if not state:
            ax.text(0.5, 0.5, 'No items selected yet', 
                   ha='center', va='center', fontsize=12, style='italic')
            ax.set_title('Selected Items', fontsize=12, fontweight='bold', pad=10)
            return
        
        # Prepare table data
        table_data = []
        for i in state:
            table_data.append([
                items[i][:20],  # Truncate long names
                f'{weights[i]:.1f}',
                f'{values[i]:.1f}',
                f'{values[i]/weights[i]:.2f}'
            ])
        
        # Create table
        table = ax.table(
            cellText=table_data,
            colLabels=['Item', 'Weight', 'Value', 'Ratio'],
            cellLoc='center',
            loc='center',
            colColours=['lightblue'] * 4
        )
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2)
        
        ax.set_title('Selected Items', fontsize=12, fontweight='bold', pad=10)
    
    def _plot_available_table(self, ax, step_data, items, weights, values):
        """Plot table of available items"""
        ax.axis('off')
        
        available = step_data.get('available_items', [])
        
        if not available:
            ax.text(0.5, 0.5, 'No items available', 
                   ha='center', va='center', fontsize=12, style='italic')
            ax.set_title('Available Items', fontsize=12, fontweight='bold', pad=10)
            return
        
        # Show top 5 by ratio
        ratios = [(i, values[i]/weights[i]) for i in available]
        ratios.sort(key=lambda x: x[1], reverse=True)
        top_5 = ratios[:5]
        
        table_data = []
        for i, ratio in top_5:
            table_data.append([
                items[i][:15],
                f'{ratio:.2f}'
            ])
        
        table = ax.table(
            cellText=table_data,
            colLabels=['Item', 'Ratio'],
            cellLoc='center',
            loc='center',
            colColours=['lightyellow'] * 2
        )
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2)
        
        ax.set_title(f'Top Available ({len(available)} total)', 
                    fontsize=12, fontweight='bold', pad=10)
    
    def _plot_statistics(self, ax, step_data, items, weights, values):
        """Plot current statistics"""
        ax.axis('off')
        
        current_value = step_data.get('value', 0)
        current_weight = step_data.get('weight', 0)
        capacity = step_data.get('capacity', 0)
        n_selected = len(step_data.get('state', []))
        n_available = len(step_data.get('available_items', []))
        
        stats_text = f"""
        Current Statistics:
        • Items Selected: {n_selected} / {len(items)}
        • Items Available: {n_available}
        • Total Value: {current_value:.1f}
        • Total Weight: {current_weight:.1f} / {capacity:.1f}
        • Capacity Used: {(current_weight/capacity)*100:.1f}%
        • Average Ratio: {(current_value/current_weight if current_weight > 0 else 0):.2f}
        """
        
        ax.text(0.5, 0.5, stats_text, ha='center', va='center', 
               fontsize=11, family='monospace',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    def _plot_fitness_distribution(self, ax, step_data):
        """Plot fitness distribution of particles"""
        fitness = step_data.get('fitness', [])
        
        if len(fitness) == 0:
            return
        
        ax.hist(fitness, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        ax.axvline(x=step_data.get('gbest_fitness', 0), color='red', 
                  linestyle='--', linewidth=2, label='Global Best')
        ax.axvline(x=step_data.get('avg_fitness', 0), color='green', 
                  linestyle='--', linewidth=2, label='Average')
        
        ax.set_xlabel('Fitness', fontsize=10)
        ax.set_ylabel('Count', fontsize=10)
        ax.set_title('Fitness Distribution', fontsize=11, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_best_solution(self, ax, step_data, items, weights, values, capacity):
        """Plot best solution found so far"""
        gbest_position = step_data.get('gbest_position', [])
        
        if len(gbest_position) == 0:
            return
        
        selected_indices = np.where(gbest_position == 1)[0]
        
        if len(selected_indices) == 0:
            ax.text(0.5, 0.5, 'No items in best solution', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Best Solution', fontsize=11, fontweight='bold')
            return
        
        # Plot items
        ax.scatter(weights, values, s=80, alpha=0.3, color='gray')
        
        selected_w = weights[selected_indices]
        selected_v = values[selected_indices]
        ax.scatter(selected_w, selected_v, s=150, alpha=0.8, 
                  color='green', marker='s')
        
        # Statistics
        total_w = np.sum(selected_w)
        total_v = np.sum(selected_v)
        
        ax.set_xlabel('Weight', fontsize=10)
        ax.set_ylabel('Value', fontsize=10)
        ax.set_title(f'Best Solution: {len(selected_indices)} items, ' +
                    f'V={total_v:.0f}, W={total_w:.0f}/{capacity:.0f}',
                    fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3)
    
    def _plot_convergence_partial(self, ax, step_data):
        """Plot convergence up to current iteration"""
        # This would need access to all previous steps
        # For now, just show current values
        iteration = step_data.get('iteration', 0)
        gbest_fitness = step_data.get('gbest_fitness', 0)
        avg_fitness = step_data.get('avg_fitness', 0)
        
        ax.text(0.5, 0.5, 
               f'Iteration: {iteration}\n' +
               f'Best Fitness: {gbest_fitness:.1f}\n' +
               f'Avg Fitness: {avg_fitness:.1f}',
               ha='center', va='center', fontsize=12,
               transform=ax.transAxes,
               bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
        
        ax.set_title('Current Progress', fontsize=11, fontweight='bold')
        ax.axis('off')
    
    def _plot_bpso_stats(self, ax, step_data):
        """Plot BPSO statistics"""
        ax.axis('off')
        
        stats_text = f"""
        BPSO Statistics:
        
        Iteration: {step_data.get('iteration', 0)}
        
        Best Fitness: {step_data.get('gbest_fitness', 0):.1f}
        Avg Fitness: {step_data.get('avg_fitness', 0):.1f}
        
        Particles: {len(step_data.get('fitness', []))}
        """
        
        ax.text(0.5, 0.5, stats_text, ha='center', va='center',
               fontsize=10, family='monospace',
               bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
