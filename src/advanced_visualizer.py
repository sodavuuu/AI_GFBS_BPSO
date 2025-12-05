"""
=================================================================================
ADVANCED VISUALIZATION - Inspired by GA_TSP
=================================================================================
Tạo visualization cho Section 3.2 - Phân tích và Đánh giá
Học từ GA_TSP:
- Convergence plots chi tiết
- Parameter impact analysis
- Algorithm behavior visualization
- Data characteristics impact

Mục tiêu: Thể hiện rõ ảnh hưởng của 3.1.1, 3.1.2, 3.1.3
=================================================================================
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import seaborn as sns
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 12)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 11


class AdvancedKnapsackVisualizer:
    """Advanced visualization cho Knapsack - Learning from GA_TSP"""
    
    def __init__(self, figsize=(16, 12)):
        self.figsize = figsize
        self.colors = {
            'gbfs': '#3498db',      # Blue
            'bpso': '#e74c3c',      # Red
            'dp': '#2ecc71',        # Green
            'bpso_v': '#9b59b6',    # Purple (BPSO variant)
            'feasible': '#27ae60',
            'infeasible': '#c0392b'
        }
    
    # =========================================================================
    # 3.1.1. ẢNH HƯỞNG CỦA THAM SỐ (Parameter Impact)
    # =========================================================================
    
    def plot_gbfs_parameter_impact(self, results_df: pd.DataFrame, save_path=None):
        """
        Vẽ ảnh hưởng của tham số GBFS (max_states)
        Tương tự như GA_TSP vẽ ảnh hưởng của population size
        
        Args:
            results_df: DataFrame với columns [max_states, value, time, convergence_gen]
        """
        fig = plt.figure(figsize=(16, 10))
        gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)
        
        # Plot 1: Value vs Max States (như GA_TSP vẽ fitness vs population)
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.plot(results_df['max_states'], results_df['value'], 
                marker='o', linewidth=2, markersize=8, color=self.colors['gbfs'])
        ax1.fill_between(results_df['max_states'], results_df['value'], 
                         alpha=0.3, color=self.colors['gbfs'])
        ax1.set_xlabel('Max States (Depth Limit)', fontweight='bold')
        ax1.set_ylabel('Total Value', fontweight='bold')
        ax1.set_title('GBFS: Impact of Max States on Solution Quality', fontweight='bold', pad=15)
        ax1.grid(True, alpha=0.3)
        
        # Thêm annotation cho best value
        best_idx = results_df['value'].idxmax()
        ax1.annotate(f'Best: {results_df.loc[best_idx, "value"]:.0f}\n@{results_df.loc[best_idx, "max_states"]} states',
                    xy=(results_df.loc[best_idx, 'max_states'], results_df.loc[best_idx, 'value']),
                    xytext=(20, 20), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        # Plot 2: Time vs Max States
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.plot(results_df['max_states'], results_df['time'], 
                marker='s', linewidth=2, markersize=8, color='#e67e22')
        ax2.fill_between(results_df['max_states'], results_df['time'], 
                         alpha=0.3, color='#e67e22')
        ax2.set_xlabel('Max States', fontweight='bold')
        ax2.set_ylabel('Execution Time (seconds)', fontweight='bold')
        ax2.set_title('GBFS: Computational Cost vs Max States', fontweight='bold', pad=15)
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Efficiency (Value/Time ratio)
        ax3 = fig.add_subplot(gs[1, 0])
        efficiency = results_df['value'] / results_df['time']
        ax3.bar(results_df['max_states'], efficiency, color=self.colors['gbfs'], alpha=0.7, edgecolor='black')
        ax3.set_xlabel('Max States', fontweight='bold')
        ax3.set_ylabel('Efficiency (Value/Time)', fontweight='bold')
        ax3.set_title('GBFS: Solution Efficiency Analysis', fontweight='bold', pad=15)
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Plot 4: Summary table
        ax4 = fig.add_subplot(gs[1, 1])
        ax4.axis('off')
        
        summary_data = [
            ['Metric', 'Best', 'Worst', 'Range'],
            ['Value', f"{results_df['value'].max():.0f}", f"{results_df['value'].min():.0f}", 
             f"{results_df['value'].max() - results_df['value'].min():.0f}"],
            ['Time (s)', f"{results_df['time'].min():.3f}", f"{results_df['time'].max():.3f}", 
             f"{results_df['time'].max() - results_df['time'].min():.3f}"],
            ['Efficiency', f"{efficiency.max():.0f}", f"{efficiency.min():.0f}", 
             f"{efficiency.max() - efficiency.min():.0f}"]
        ]
        
        table = ax4.table(cellText=summary_data, cellLoc='center', loc='center',
                         colWidths=[0.25, 0.25, 0.25, 0.25])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)
        
        # Style header
        for i in range(4):
            table[(0, i)].set_facecolor('#3498db')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        plt.suptitle('3.1.1.a: GBFS Parameter Analysis - Max States Impact', 
                    fontsize=16, fontweight='bold', y=0.98)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_bpso_parameter_impact(self, results_df: pd.DataFrame, param_name='n_particles', save_path=None):
        """
        Vẽ ảnh hưởng của tham số BPSO (n_particles, max_iterations, w, c1, c2)
        Như GA_TSP vẽ ảnh hưởng của mutation rate, population size
        
        Args:
            results_df: DataFrame với columns [param_value, value, time, convergence_iter, best_fitness_history]
            param_name: 'n_particles', 'max_iterations', 'w', 'c1', 'c2'
        """
        param_labels = {
            'n_particles': 'Swarm Size (Number of Particles)',
            'max_iterations': 'Max Iterations',
            'w': 'Inertia Weight (w)',
            'c1': 'Cognitive Coefficient (c₁)',
            'c2': 'Social Coefficient (c₂)'
        }
        
        fig = plt.figure(figsize=(16, 10))
        gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)
        
        param_col = 'param_value'
        
        # Plot 1: Convergence curves for different parameter values
        ax1 = fig.add_subplot(gs[0, :])
        
        for idx, row in results_df.iterrows():
            history = row.get('best_fitness_history', [])
            if len(history) > 0:
                label = f"{param_labels.get(param_name, param_name)} = {row[param_col]}"
                ax1.plot(history, linewidth=2, marker='o', markersize=4, 
                        markevery=max(1, len(history)//10), label=label, alpha=0.8)
        
        ax1.set_xlabel('Iteration', fontweight='bold')
        ax1.set_ylabel('Best Fitness', fontweight='bold')
        ax1.set_title(f'BPSO: Convergence Comparison - {param_labels.get(param_name, param_name)}', 
                     fontweight='bold', pad=15)
        ax1.legend(loc='best', frameon=True, shadow=True)
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Final value vs parameter
        ax2 = fig.add_subplot(gs[1, 0])
        ax2.plot(results_df[param_col], results_df['value'], 
                marker='o', linewidth=2.5, markersize=10, color=self.colors['bpso'])
        ax2.fill_between(results_df[param_col], results_df['value'], 
                         alpha=0.3, color=self.colors['bpso'])
        ax2.set_xlabel(param_labels.get(param_name, param_name), fontweight='bold')
        ax2.set_ylabel('Final Best Value', fontweight='bold')
        ax2.set_title('Solution Quality vs Parameter', fontweight='bold', pad=15)
        ax2.grid(True, alpha=0.3)
        
        # Highlight best
        best_idx = results_df['value'].idxmax()
        ax2.scatter(results_df.loc[best_idx, param_col], results_df.loc[best_idx, 'value'],
                   s=300, c='gold', marker='*', edgecolors='black', linewidths=2, zorder=5)
        
        # Plot 3: Convergence speed (iterations to reach 95% of final value)
        ax3 = fig.add_subplot(gs[1, 1])
        
        convergence_speeds = []
        for idx, row in results_df.iterrows():
            history = row.get('best_fitness_history', [])
            if len(history) > 0:
                final_val = history[-1]
                target = 0.95 * final_val
                conv_iter = next((i for i, v in enumerate(history) if v >= target), len(history))
                convergence_speeds.append(conv_iter)
            else:
                convergence_speeds.append(0)
        
        results_df['convergence_speed'] = convergence_speeds
        
        bars = ax3.bar(results_df[param_col].astype(str), convergence_speeds, 
                      color=self.colors['bpso'], alpha=0.7, edgecolor='black', linewidth=1.5)
        
        # Color code: faster = greener
        max_speed = max(convergence_speeds)
        for bar, speed in zip(bars, convergence_speeds):
            bar.set_color(plt.cm.RdYlGn_r(speed / max_speed))
        
        ax3.set_xlabel(param_labels.get(param_name, param_name), fontweight='bold')
        ax3.set_ylabel('Iterations to Reach 95% of Final Value', fontweight='bold')
        ax3.set_title('Convergence Speed Analysis', fontweight='bold', pad=15)
        ax3.grid(True, alpha=0.3, axis='y')
        
        plt.suptitle(f'3.1.1.b: BPSO Parameter Analysis - {param_labels.get(param_name, param_name)} Impact', 
                    fontsize=16, fontweight='bold', y=0.98)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    # =========================================================================
    # 3.1.2. ẢNH HƯỞNG CỦA THUẬT TOÁN (Algorithm Comparison)
    # =========================================================================
    
    def plot_algorithm_comparison_detailed(self, gbfs_result: Dict, bpso_result: Dict, 
                                          dp_result: Dict, bpso_variant_result: Dict = None, 
                                          save_path=None):
        """
        So sánh chi tiết 3 thuật toán (hoặc 4 nếu có BPSO variant)
        Như GA_TSP so sánh các mutations/crossover/selection
        
        Args:
            gbfs_result: Dict từ solve_gbfs()
            bpso_result: Dict từ solve_bpso()
            dp_result: Dict từ solve_dp()
            bpso_variant_result: Dict từ BPSO variant (optional)
        """
        fig = plt.figure(figsize=(18, 12))
        gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.35)
        
        # Prepare data
        algorithms = []
        values = []
        times = []
        colors_list = []
        
        algorithms.append('GBFS')
        values.append(gbfs_result['total_value'])
        times.append(gbfs_result['execution_time'])
        colors_list.append(self.colors['gbfs'])
        
        algorithms.append('BPSO')
        values.append(bpso_result['total_value'])
        times.append(bpso_result['execution_time'])
        colors_list.append(self.colors['bpso'])
        
        algorithms.append('DP')
        values.append(dp_result['total_value'])
        times.append(dp_result['execution_time'])
        colors_list.append(self.colors['dp'])
        
        if bpso_variant_result:
            algorithms.append('BPSO-V')
            values.append(bpso_variant_result['total_value'])
            times.append(bpso_variant_result['execution_time'])
            colors_list.append(self.colors['bpso_v'])
        
        # Plot 1: Value comparison (bar chart)
        ax1 = fig.add_subplot(gs[0, 0])
        bars1 = ax1.bar(algorithms, values, color=colors_list, alpha=0.8, edgecolor='black', linewidth=2)
        ax1.set_ylabel('Total Value', fontweight='bold', fontsize=12)
        ax1.set_title('Solution Quality Comparison', fontweight='bold', pad=15, fontsize=13)
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar, val in zip(bars1, values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:.0f}',
                    ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        # Plot 2: Time comparison (bar chart with log scale)
        ax2 = fig.add_subplot(gs[0, 1])
        bars2 = ax2.bar(algorithms, times, color=colors_list, alpha=0.8, edgecolor='black', linewidth=2)
        ax2.set_ylabel('Execution Time (seconds)', fontweight='bold', fontsize=12)
        ax2.set_title('Computational Cost Comparison', fontweight='bold', pad=15, fontsize=13)
        ax2.set_yscale('log')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Add time labels
        for bar, t in zip(bars2, times):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{t:.3f}s',
                    ha='center', va='bottom', fontweight='bold', fontsize=9)
        
        # Plot 3: Efficiency (Value/Time)
        ax3 = fig.add_subplot(gs[0, 2])
        efficiency = [v/t for v, t in zip(values, times)]
        bars3 = ax3.bar(algorithms, efficiency, color=colors_list, alpha=0.8, edgecolor='black', linewidth=2)
        ax3.set_ylabel('Efficiency (Value/Time)', fontweight='bold', fontsize=12)
        ax3.set_title('Algorithm Efficiency', fontweight='bold', pad=15, fontsize=13)
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Highlight best efficiency
        best_eff_idx = efficiency.index(max(efficiency))
        bars3[best_eff_idx].set_edgecolor('gold')
        bars3[best_eff_idx].set_linewidth(4)
        
        # Plot 4: BPSO Convergence (if available)
        ax4 = fig.add_subplot(gs[1, :2])
        
        if 'best_fitness_history' in bpso_result:
            history = bpso_result['best_fitness_history']
            ax4.plot(history, linewidth=2.5, color=self.colors['bpso'], label='BPSO Standard', marker='o', markersize=5, markevery=max(1, len(history)//15))
            
            if bpso_variant_result and 'best_fitness_history' in bpso_variant_result:
                history_v = bpso_variant_result['best_fitness_history']
                ax4.plot(history_v, linewidth=2.5, color=self.colors['bpso_v'], label='BPSO Variant', marker='s', markersize=5, markevery=max(1, len(history_v)//15))
            
            # Add GBFS and DP as horizontal lines
            ax4.axhline(y=gbfs_result['total_value'], color=self.colors['gbfs'], 
                       linestyle='--', linewidth=2, label='GBFS (Greedy)')
            ax4.axhline(y=dp_result['total_value'], color=self.colors['dp'], 
                       linestyle='--', linewidth=2, label='DP (Optimal)')
            
            ax4.set_xlabel('Iteration', fontweight='bold', fontsize=12)
            ax4.set_ylabel('Best Fitness', fontweight='bold', fontsize=12)
            ax4.set_title('Convergence Analysis: BPSO vs Baselines', fontweight='bold', pad=15, fontsize=13)
            ax4.legend(loc='best', frameon=True, shadow=True, fontsize=10)
            ax4.grid(True, alpha=0.3)
        else:
            ax4.text(0.5, 0.5, 'No convergence data available', 
                    ha='center', va='center', fontsize=14, transform=ax4.transAxes)
        
        # Plot 5: Quality vs Time scatter
        ax5 = fig.add_subplot(gs[1, 2])
        
        for i, (alg, val, t, c) in enumerate(zip(algorithms, values, times, colors_list)):
            ax5.scatter(t, val, s=500, c=c, marker='o', edgecolors='black', 
                       linewidths=2, alpha=0.8, label=alg, zorder=5)
            ax5.annotate(alg, (t, val), xytext=(10, 10), textcoords='offset points',
                        fontsize=11, fontweight='bold')
        
        ax5.set_xlabel('Execution Time (seconds)', fontweight='bold', fontsize=12)
        ax5.set_ylabel('Total Value', fontweight='bold', fontsize=12)
        ax5.set_title('Quality vs Speed Trade-off', fontweight='bold', pad=15, fontsize=13)
        ax5.set_xscale('log')
        ax5.grid(True, alpha=0.3)
        
        # Plot 6: Comparison table
        ax6 = fig.add_subplot(gs[2, :])
        ax6.axis('off')
        
        table_data = [['Algorithm', 'Value', 'Time (s)', 'Efficiency', '% of Optimal', 'Ranking']]
        
        optimal_value = dp_result['total_value']
        
        for alg, val, t in zip(algorithms, values, times):
            eff = val / t
            pct_optimal = (val / optimal_value) * 100
            table_data.append([
                alg,
                f"{val:.0f}",
                f"{t:.4f}",
                f"{eff:.0f}",
                f"{pct_optimal:.2f}%",
                "★" * (4 - algorithms.index(alg))  # Simple ranking
            ])
        
        table = ax6.table(cellText=table_data, cellLoc='center', loc='center',
                         colWidths=[0.15, 0.15, 0.15, 0.15, 0.15, 0.15])
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1, 2.5)
        
        # Style header
        for i in range(6):
            table[(0, i)].set_facecolor('#34495e')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        # Color code rows
        for i in range(1, len(table_data)):
            for j in range(6):
                if i % 2 == 0:
                    table[(i, j)].set_facecolor('#ecf0f1')
        
        plt.suptitle('3.1.2: Algorithm Comparison - GBFS vs BPSO vs DP (vs BPSO-Variant)', 
                    fontsize=18, fontweight='bold', y=0.98)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    # =========================================================================
    # 3.1.3. ẢNH HƯỞNG CỦA DỮ LIỆU (Data Characteristics Impact)
    # =========================================================================
    
    def plot_data_characteristics_impact(self, results_dict: Dict[str, Dict], save_path=None):
        """
        Vẽ ảnh hưởng của đặc điểm dữ liệu
        
        Args:
            results_dict: {
                'low_correlation': {'gbfs': {...}, 'bpso': {...}, 'dp': {...}},
                'high_correlation': {'gbfs': {...}, 'bpso': {...}, 'dp': {...}},
                'high_value': {'gbfs': {...}, 'bpso': {...}, 'dp': {...}}
            }
        """
        fig = plt.figure(figsize=(18, 12))
        gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.35)
        
        data_types = list(results_dict.keys())
        algorithms = ['gbfs', 'bpso', 'dp']
        
        # Prepare data for plotting
        values_by_algo = {alg: [] for alg in algorithms}
        times_by_algo = {alg: [] for alg in algorithms}
        
        for data_type in data_types:
            for alg in algorithms:
                if alg in results_dict[data_type]:
                    values_by_algo[alg].append(results_dict[data_type][alg]['total_value'])
                    times_by_algo[alg].append(results_dict[data_type][alg]['execution_time'])
                else:
                    values_by_algo[alg].append(0)
                    times_by_algo[alg].append(0)
        
        # Plot 1: Value comparison across data types
        ax1 = fig.add_subplot(gs[0, :])
        
        x = np.arange(len(data_types))
        width = 0.25
        
        for i, alg in enumerate(algorithms):
            offset = (i - 1) * width
            bars = ax1.bar(x + offset, values_by_algo[alg], width, 
                          label=alg.upper(), alpha=0.8, edgecolor='black')
        
        ax1.set_ylabel('Total Value', fontweight='bold', fontsize=12)
        ax1.set_title('Solution Quality: Impact of Data Characteristics', fontweight='bold', pad=15, fontsize=13)
        ax1.set_xticks(x)
        ax1.set_xticklabels([dt.replace('_', ' ').title() for dt in data_types])
        ax1.legend(loc='best', frameon=True, shadow=True)
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Plot 2: Time comparison across data types
        ax2 = fig.add_subplot(gs[1, :])
        
        for i, alg in enumerate(algorithms):
            offset = (i - 1) * width
            bars = ax2.bar(x + offset, times_by_algo[alg], width, 
                          label=alg.upper(), alpha=0.8, edgecolor='black')
        
        ax2.set_ylabel('Execution Time (seconds)', fontweight='bold', fontsize=12)
        ax2.set_title('Computational Cost: Impact of Data Characteristics', fontweight='bold', pad=15, fontsize=13)
        ax2.set_xticks(x)
        ax2.set_xticklabels([dt.replace('_', ' ').title() for dt in data_types])
        ax2.legend(loc='best', frameon=True, shadow=True)
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.set_yscale('log')
        
        # Plot 3: Performance degradation analysis
        ax3 = fig.add_subplot(gs[2, 0])
        
        # Calculate degradation from best case (low_correlation) to worst case
        if 'low_correlation' in data_types and 'high_correlation' in data_types:
            idx_low = data_types.index('low_correlation')
            idx_high = data_types.index('high_correlation')
            
            degradation = []
            for alg in algorithms:
                val_low = values_by_algo[alg][idx_low]
                val_high = values_by_algo[alg][idx_high]
                if val_low > 0:
                    deg = ((val_low - val_high) / val_low) * 100
                    degradation.append(deg)
                else:
                    degradation.append(0)
            
            bars = ax3.bar([a.upper() for a in algorithms], degradation, 
                          color=['#e74c3c' if d > 10 else '#f39c12' if d > 5 else '#27ae60' for d in degradation],
                          alpha=0.8, edgecolor='black', linewidth=2)
            
            ax3.set_ylabel('Performance Degradation (%)', fontweight='bold', fontsize=11)
            ax3.set_title('Sensitivity to Data Correlation', fontweight='bold', pad=15, fontsize=12)
            ax3.grid(True, alpha=0.3, axis='y')
            
            # Add value labels
            for bar, deg in zip(bars, degradation):
                height = bar.get_height()
                ax3.text(bar.get_x() + bar.get_width()/2., height,
                        f'{deg:.1f}%',
                        ha='center', va='bottom', fontweight='bold')
        
        # Plot 4: Algorithm ranking by data type
        ax4 = fig.add_subplot(gs[2, 1:])
        ax4.axis('off')
        
        # Create ranking table
        ranking_data = [['Data Type'] + [a.upper() for a in algorithms]]
        
        for i, data_type in enumerate(data_types):
            row_data = [data_type.replace('_', ' ').title()]
            
            # Get values for this data type
            vals = [values_by_algo[alg][i] for alg in algorithms]
            
            # Rank (1 = best)
            sorted_indices = np.argsort(vals)[::-1]
            ranks = [''] * len(algorithms)
            for rank, idx in enumerate(sorted_indices):
                ranks[idx] = f"{rank + 1}. {vals[idx]:.0f}"
            
            row_data.extend(ranks)
            ranking_data.append(row_data)
        
        table = ax4.table(cellText=ranking_data, cellLoc='center', loc='center',
                         colWidths=[0.25, 0.25, 0.25, 0.25])
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1, 2.5)
        
        # Style header
        for i in range(4):
            table[(0, i)].set_facecolor('#2c3e50')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        plt.suptitle('3.1.3: Data Characteristics Impact Analysis', 
                    fontsize=18, fontweight='bold', y=0.98)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    # =========================================================================
    # KNAPSACK-SPECIFIC VISUALIZATIONS (Inspired by GA_TSP map)
    # =========================================================================
    
    def plot_knapsack_solution_map(self, solution: Dict, items_data: pd.DataFrame, save_path=None):
        """
        Vẽ "map" của solution - Thay vì map địa lý như TSP, 
        ta vẽ visualization của items được chọn
        
        Visualization:
        - Capacity utilization (bar chart như map route)
        - Regional diversity (pie chart)
        - Item selection (scatter plot: weight vs value)
        
        Args:
            solution: Dict from algorithm (selected_items, total_value, total_weight)
            items_data: DataFrame with columns [name, weight, value, region, category]
        """
        fig = plt.figure(figsize=(16, 10))
        gs = GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.35)
        
        selected_items = solution['selected_items']
        capacity = solution.get('capacity', 0)
        total_weight = solution['total_weight']
        total_value = solution['total_value']
        
        # Filter selected items data
        selected_data = items_data[items_data['name'].isin(selected_items)]
        unselected_data = items_data[~items_data['name'].isin(selected_items)]
        
        # Plot 1: Item selection map (scatter: weight vs value)
        ax1 = fig.add_subplot(gs[0, :2])
        
        # Unselected items (gray)
        ax1.scatter(unselected_data['weight'], unselected_data['value'], 
                   s=100, c='lightgray', alpha=0.3, edgecolors='gray', 
                   linewidths=0.5, label='Not Selected')
        
        # Selected items (colored by region)
        if 'region' in selected_data.columns:
            regions = selected_data['region'].unique()
            region_colors = plt.cm.Set3(np.linspace(0, 1, len(regions)))
            
            for i, region in enumerate(regions):
                region_data = selected_data[selected_data['region'] == region]
                ax1.scatter(region_data['weight'], region_data['value'], 
                           s=300, c=[region_colors[i]], alpha=0.8, 
                           edgecolors='black', linewidths=2, 
                           label=f'Region {region}', marker='o')
        else:
            ax1.scatter(selected_data['weight'], selected_data['value'], 
                       s=300, c=self.colors['feasible'], alpha=0.8, 
                       edgecolors='black', linewidths=2, label='Selected')
        
        ax1.set_xlabel('Weight', fontweight='bold', fontsize=12)
        ax1.set_ylabel('Value', fontweight='bold', fontsize=12)
        ax1.set_title('Item Selection Map: Weight vs Value', fontweight='bold', pad=15, fontsize=13)
        ax1.legend(loc='best', frameon=True, shadow=True)
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Capacity utilization
        ax2 = fig.add_subplot(gs[0, 2])
        
        utilization = (total_weight / capacity) * 100 if capacity > 0 else 0
        remaining = 100 - utilization
        
        colors_util = [self.colors['feasible'] if utilization <= 100 else self.colors['infeasible'], 'lightgray']
        wedges, texts, autotexts = ax2.pie([utilization, remaining], 
                                           labels=['Used', 'Remaining'], 
                                           autopct='%1.1f%%',
                                           startangle=90, colors=colors_util,
                                           textprops={'fontweight': 'bold', 'fontsize': 11})
        
        ax2.set_title(f'Capacity Utilization\n{total_weight:.1f} / {capacity:.1f}', 
                     fontweight='bold', pad=15, fontsize=13)
        
        # Plot 3: Regional diversity (if available)
        ax3 = fig.add_subplot(gs[1, 0])
        
        if 'region' in selected_data.columns:
            region_counts = selected_data['region'].value_counts()
            
            ax3.bar(region_counts.index.astype(str), region_counts.values, 
                   color=region_colors[:len(region_counts)], alpha=0.8, 
                   edgecolor='black', linewidth=2)
            
            ax3.set_xlabel('Region', fontweight='bold', fontsize=12)
            ax3.set_ylabel('Number of Items', fontweight='bold', fontsize=12)
            ax3.set_title('Regional Diversity Distribution', fontweight='bold', pad=15, fontsize=13)
            ax3.grid(True, alpha=0.3, axis='y')
        else:
            ax3.text(0.5, 0.5, 'No regional data', ha='center', va='center', 
                    fontsize=14, transform=ax3.transAxes)
        
        # Plot 4: Value contribution by category (if available)
        ax4 = fig.add_subplot(gs[1, 1])
        
        if 'category' in selected_data.columns:
            category_values = selected_data.groupby('category')['value'].sum().sort_values(ascending=False)
            
            ax4.barh(category_values.index, category_values.values, 
                    color=self.colors['bpso'], alpha=0.7, edgecolor='black', linewidth=1.5)
            
            ax4.set_xlabel('Total Value', fontweight='bold', fontsize=12)
            ax4.set_title('Value Contribution by Category', fontweight='bold', pad=15, fontsize=13)
            ax4.grid(True, alpha=0.3, axis='x')
        else:
            ax4.text(0.5, 0.5, 'No category data', ha='center', va='center', 
                    fontsize=14, transform=ax4.transAxes)
        
        # Plot 5: Summary statistics
        ax5 = fig.add_subplot(gs[1, 2])
        ax5.axis('off')
        
        summary_data = [
            ['Metric', 'Value'],
            ['Total Items', f"{len(selected_items)}"],
            ['Total Value', f"{total_value:.0f}"],
            ['Total Weight', f"{total_weight:.1f}"],
            ['Capacity', f"{capacity:.1f}"],
            ['Utilization', f"{utilization:.1f}%"],
            ['Avg Value/Item', f"{total_value/len(selected_items):.1f}" if len(selected_items) > 0 else "0"],
            ['Avg Weight/Item', f"{total_weight/len(selected_items):.1f}" if len(selected_items) > 0 else "0"]
        ]
        
        table = ax5.table(cellText=summary_data, cellLoc='left', loc='center',
                         colWidths=[0.5, 0.5])
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1, 2)
        
        # Style
        for i in range(2):
            table[(0, i)].set_facecolor('#2c3e50')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        plt.suptitle('Knapsack Solution Visualization (Inspired by GA_TSP Map)', 
                    fontsize=16, fontweight='bold', y=0.98)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig


def demo_visualizations():
    """Demo function to show how to use advanced visualizer"""
    print("Advanced Knapsack Visualizer - Inspired by GA_TSP")
    print("=" * 70)
    print("\nUsage examples:")
    print("\n1. GBFS Parameter Impact:")
    print("   visualizer.plot_gbfs_parameter_impact(results_df)")
    print("\n2. BPSO Parameter Impact:")
    print("   visualizer.plot_bpso_parameter_impact(results_df, 'n_particles')")
    print("\n3. Algorithm Comparison:")
    print("   visualizer.plot_algorithm_comparison_detailed(gbfs, bpso, dp)")
    print("\n4. Data Characteristics Impact:")
    print("   visualizer.plot_data_characteristics_impact(results_dict)")
    print("\n5. Solution Map:")
    print("   visualizer.plot_knapsack_solution_map(solution, items_df)")


if __name__ == '__main__':
    demo_visualizations()
