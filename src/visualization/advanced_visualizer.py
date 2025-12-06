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
import json

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
        ax1.set_xlabel('Số trạng thái tối đa', fontweight='bold')  # Shorter label
        ax1.set_ylabel('Tổng giá trị', fontweight='bold')
        ax1.set_title('GBFS: Ảnh hưởng Max States đến chất lượng', fontweight='bold', pad=10)  # Shorter, less pad
        ax1.grid(True, alpha=0.3)
        
        # Thêm annotation cho best value - đặt góc trên bên trái để tránh che
        best_idx = results_df['value'].idxmax()
        ax1.annotate(f'Tốt nhất: {results_df.loc[best_idx, "value"]:.0f}\n@{results_df.loc[best_idx, "max_states"]} states',
                    xy=(results_df.loc[best_idx, 'max_states'], results_df.loc[best_idx, 'value']),
                    xytext=(-80, -30), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.8),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.3'),
                    fontsize=9)
        
        # Plot 2: Time vs Max States
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.plot(results_df['max_states'], results_df['time'], 
                marker='s', linewidth=2, markersize=8, color='#e67e22')
        ax2.fill_between(results_df['max_states'], results_df['time'], 
                         alpha=0.3, color='#e67e22')
        ax2.set_xlabel('Số trạng thái tối đa', fontweight='bold')
        ax2.set_ylabel('Thời gian thực thi (giây)', fontweight='bold')
        ax2.set_title('GBFS: Chi phí tính toán vs Max States', fontweight='bold', pad=15)
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Efficiency (Value/Time ratio) - Scale to K (thousands)
        ax3 = fig.add_subplot(gs[1, 0])
        efficiency = results_df['value'] / results_df['time'] / 1000  # Scale to thousands
        
        # Set bar width based on data spacing
        bar_width = (results_df['max_states'].max() - results_df['max_states'].min()) / len(results_df) * 0.6
        ax3.bar(results_df['max_states'], efficiency, width=bar_width, 
                color=self.colors['gbfs'], alpha=0.7, edgecolor='black', linewidth=1.5)
        ax3.set_xlabel('Số trạng thái tối đa', fontweight='bold')
        ax3.set_ylabel('Hiệu suất (K Giá trị/s)', fontweight='bold')
        ax3.set_title('GBFS: Phân tích hiệu suất giải pháp', fontweight='bold', pad=15)
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Plot 4: Summary table
        ax4 = fig.add_subplot(gs[1, 1])
        ax4.axis('off')
        
        summary_data = [
            ['Chỉ số', 'Tốt nhất', 'Tệ nhất', 'Khoảng'],
            ['Giá trị', f"{results_df['value'].max():.0f}", f"{results_df['value'].min():.0f}", 
             f"{results_df['value'].max() - results_df['value'].min():.0f}"],
            ['Thời gian (s)', f"{results_df['time'].min():.3f}", f"{results_df['time'].max():.3f}", 
             f"{results_df['time'].max() - results_df['time'].min():.3f}"],
            ['Hiệu suất (K)', f"{efficiency.max():.1f}", f"{efficiency.min():.1f}", 
             f"{efficiency.max() - efficiency.min():.1f}"]
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
        
        plt.suptitle('3.1.1.a: Phân tích tham số GBFS - Ảnh hưởng Max States', 
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
            
        Note: Nếu best_fitness_history không có trong results_df, sẽ tìm file JSON tương ứng
        """
        param_labels = {
            'n_particles': 'Kích thước bầy đàn (Số hạt)',
            'max_iterations': 'Số vòng lặp tối đa',
            'w': 'Trọng số quán tính (w)',
            'c1': 'Hệ số nhận thức (c₁)',
            'c2': 'Hệ số xã hội (c₂)'
        }
        
        # Try to load history from JSON if not in DataFrame
        if 'best_fitness_history' not in results_df.columns or \
           results_df['best_fitness_history'].iloc[0] is None or \
           (isinstance(results_df['best_fitness_history'].iloc[0], float) and 
            pd.isna(results_df['best_fitness_history'].iloc[0])):
            
            # Try to find JSON file
            if save_path:
                base_dir = os.path.dirname(save_path)
                base_name = os.path.basename(save_path).replace('.png', '_history.json')
                json_path = os.path.join(base_dir, base_name)
                
                if os.path.exists(json_path):
                    print(f"  → Loading history from {json_path}")
                    with open(json_path, 'r') as f:
                        history_data = json.load(f)
                    
                    # Merge history into DataFrame
                    for idx, row in results_df.iterrows():
                        for hist_item in history_data['results']:
                            if hist_item['param_value'] == row['param_value']:
                                results_df.at[idx, 'best_fitness_history'] = hist_item['best_fitness_history']
                                break
        
        fig = plt.figure(figsize=(16, 12))  # Tăng height để tránh overlap
        gs = GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.3)  # Tăng hspace
        
        param_col = 'param_value'
        
        # Plot 1: Convergence curves for different parameter values
        ax1 = fig.add_subplot(gs[0, :])
        
        has_history = False
        for idx, row in results_df.iterrows():
            history = row.get('best_fitness_history', [])
            if len(history) > 0 and isinstance(history, (list, np.ndarray)):
                has_history = True
                label = f"{param_labels.get(param_name, param_name)} = {row[param_col]}"
                # Convert normalized fitness (0-1) to approximate actual value
                # Scale by observed final value for better visualization
                actual_value = row.get('value', max(history) if len(history) > 0 else 1)
                if max(history) > 0:
                    scaled_history = [h * actual_value / max(history) for h in history]
                else:
                    scaled_history = history
                ax1.plot(scaled_history, linewidth=2, marker='o', markersize=4, 
                        markevery=max(1, len(scaled_history)//10), label=label, alpha=0.8)
        
        ax1.set_xlabel('Vòng lặp', fontweight='bold')
        ax1.set_ylabel('Giá trị tốt nhất (ước lượng)', fontweight='bold')
        ax1.set_title(f'BPSO: So sánh hội tụ - {param_labels.get(param_name, param_name)}', 
                     fontweight='bold', pad=15)
        if has_history:
            ax1.legend(loc='lower right', frameon=True, shadow=True, fontsize=9)
        else:
            # If no history data, show message
            ax1.text(0.5, 0.5, 'Không có dữ liệu hội tụ\n(History không được lưu trong CSV)',
                    ha='center', va='center', fontsize=12, transform=ax1.transAxes,
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Final value vs parameter
        ax2 = fig.add_subplot(gs[1, 0])
        ax2.plot(results_df[param_col], results_df['value'], 
                marker='o', linewidth=2.5, markersize=10, color=self.colors['bpso'])
        ax2.fill_between(results_df[param_col], results_df['value'], 
                         alpha=0.3, color=self.colors['bpso'])
        ax2.set_xlabel(param_labels.get(param_name, param_name), fontweight='bold')
        ax2.set_ylabel('Giá trị cuối cùng tốt nhất', fontweight='bold')
        ax2.set_title('Chất lượng giải pháp vs Tham số', fontweight='bold', pad=15)
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
        max_speed = max(convergence_speeds) if convergence_speeds else 1
        if max_speed > 0:
            for bar, speed in zip(bars, convergence_speeds):
                bar.set_color(plt.cm.RdYlGn_r(speed / max_speed))
        
        ax3.set_xlabel(param_labels.get(param_name, param_name), fontweight='bold')
        ax3.set_ylabel('Số vòng lặp để đạt 95% giá trị cuối', fontweight='bold')
        ax3.set_title('Phân tích tốc độ hội tụ', fontweight='bold', pad=15)
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Shorter title to avoid overlap
        title_map = {
            'n_particles': '3.1.1.b: BPSO - Ảnh hưởng Kích thước Bầy đàn',
            'max_iterations': '3.1.1.c: BPSO - Ảnh hưởng Số Vòng lặp',
            'w': '3.1.1.d: BPSO - Ảnh hưởng Trọng số Quán tính (w)'
        }
        title = title_map.get(param_name, f'3.1.1: BPSO - {param_labels.get(param_name, param_name)}')
        plt.suptitle(title, fontsize=16, fontweight='bold', y=0.99)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    # =========================================================================
    # 3.1.2. ẢNH HƯỞNG CỦA THUẬT TOÁN (Algorithm Comparison)
    # =========================================================================
    
    def plot_algorithm_comparison_gbfs_bpso(self, gbfs_result: Dict, bpso_result: Dict, save_path=None):
        """
        So sánh GBFS vs BPSO only (2 algorithms)
        
        Args:
            gbfs_result: Dict từ solve_knapsack_gbfs()
            bpso_result: Dict từ solve_knapsack_bpso()
            save_path: Path để save figure
        """
        fig, axes = plt.subplots(1, 3, figsize=(16, 5))
        
        algorithms = ['GBFS', 'BPSO']
        values = [gbfs_result['total_value'], bpso_result['total_value']]
        times = [gbfs_result['execution_time'], bpso_result['execution_time']]
        colors = [self.colors['gbfs'], self.colors['bpso']]
        
        # Plot 1: Solution Quality
        axes[0].bar(algorithms, values, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
        axes[0].set_ylabel('Total Value', fontweight='bold')
        axes[0].set_title('Solution Quality\n(Higher is Better)', fontweight='bold')
        axes[0].grid(True, alpha=0.3, axis='y')
        for i, val in enumerate(values):
            axes[0].text(i, val, f'{val:.0f}', ha='center', va='bottom', fontweight='bold')
        
        # Plot 2: Execution Time
        axes[1].bar(algorithms, [t*1000 for t in times], color=colors, alpha=0.7, edgecolor='black', linewidth=2)
        axes[1].set_ylabel('Time (ms)', fontweight='bold')
        axes[1].set_title('Computational Cost\n(Lower is Better)', fontweight='bold')
        axes[1].set_yscale('log')
        axes[1].grid(True, alpha=0.3, axis='y')
        for i, t in enumerate(times):
            axes[1].text(i, t*1000, f'{t*1000:.2f}ms', ha='center', va='bottom', fontweight='bold')
        
        # Plot 3: Trade-off Scatter
        for i, algo in enumerate(algorithms):
            axes[2].scatter(times[i]*1000, values[i], s=400, color=colors[i], 
                          alpha=0.7, edgecolors='black', linewidth=2, label=algo)
            axes[2].annotate(algo, xy=(times[i]*1000, values[i]), 
                           xytext=(10, 10), textcoords='offset points', fontweight='bold')
        axes[2].set_xlabel('Time (ms, log scale)', fontweight='bold')
        axes[2].set_ylabel('Total Value', fontweight='bold')
        axes[2].set_title('Quality vs Speed\n(Top-Left is Best)', fontweight='bold')
        axes[2].set_xscale('log')
        axes[2].grid(True, alpha=0.3)
        axes[2].legend()
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.show()
        return fig
    
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
        ax1.set_ylabel('Tổng giá trị', fontweight='bold', fontsize=12)
        ax1.set_title('So sánh chất lượng giải pháp', fontweight='bold', pad=15, fontsize=13)
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
        ax2.set_ylabel('Thời gian thực thi (giây)', fontweight='bold', fontsize=12)
        ax2.set_title('So sánh chi phí tính toán', fontweight='bold', pad=15, fontsize=13)
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
        ax3.set_ylabel('Hiệu suất (Giá trị/Thời gian)', fontweight='bold', fontsize=12)
        ax3.set_title('Hiệu suất thuật toán', fontweight='bold', pad=15, fontsize=13)
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
                       linestyle='--', linewidth=2, label='GBFS (Tham lam)')
            ax4.axhline(y=dp_result['total_value'], color=self.colors['dp'], 
                       linestyle='--', linewidth=2, label='DP (Tối ưu)')
            
            ax4.set_xlabel('Vòng lặp', fontweight='bold', fontsize=12)
            ax4.set_ylabel('Độ thích nghi tốt nhất', fontweight='bold', fontsize=12)
            ax4.set_title('Phân tích hội tụ: BPSO vs Baseline', fontweight='bold', pad=15, fontsize=13)
            ax4.legend(loc='best', frameon=True, shadow=True, fontsize=10)
            ax4.grid(True, alpha=0.3)
        else:
            ax4.text(0.5, 0.5, 'Không có dữ liệu hội tụ', 
                    ha='center', va='center', fontsize=14, transform=ax4.transAxes)
        
        # Plot 5: Quality vs Time scatter
        ax5 = fig.add_subplot(gs[1, 2])
        
        for i, (alg, val, t, c) in enumerate(zip(algorithms, values, times, colors_list)):
            ax5.scatter(t, val, s=500, c=c, marker='o', edgecolors='black', 
                       linewidths=2, alpha=0.8, label=alg, zorder=5)
            ax5.annotate(alg, (t, val), xytext=(10, 10), textcoords='offset points',
                        fontsize=11, fontweight='bold')
        
        ax5.set_xlabel('Thời gian thực thi (giây)', fontweight='bold', fontsize=12)
        ax5.set_ylabel('Tổng giá trị', fontweight='bold', fontsize=12)
        ax5.set_title('Đánh đổi giữa chất lượng và tốc độ', fontweight='bold', pad=15, fontsize=13)
        ax5.set_xscale('log')
        ax5.grid(True, alpha=0.3)
        
        # Plot 6: Comparison table
        ax6 = fig.add_subplot(gs[2, :])
        ax6.axis('off')
        
        table_data = [['Thuật toán', 'Giá trị', 'Thời gian (s)', 'Hiệu suất', '% Tối ưu', 'Xếp hạng']]
        
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
        
        plt.suptitle('3.1.2: So sánh thuật toán - GBFS vs BPSO vs DP (vs BPSO-Biến thể)', 
                    fontsize=18, fontweight='bold', y=0.98)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    # =========================================================================
    # 3.1.3. ẢNH HƯỞNG CỦA DỮ LIỆU (Data Characteristics Impact)
    # =========================================================================
    
    def plot_data_characteristics_impact(self, results_dict: Dict[str, Dict], save_path=None):
        """
        Vẽ ảnh hưởng của đặc điểm dữ liệu (GBFS vs BPSO only)
        
        Args:
            results_dict: {
                'low_correlation': {'gbfs': {...}, 'bpso': {...}},
                'high_correlation': {'gbfs': {...}, 'bpso': {...}},
                'high_value': {'gbfs': {...}, 'bpso': {...}}
            }
        """
        fig = plt.figure(figsize=(18, 12))
        gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.35)
        
        data_types = list(results_dict.keys())
        algorithms = ['gbfs', 'bpso']  # Only 2 algorithms now
        
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
        width = 0.35  # Wider bars for 2 algorithms
        
        for i, alg in enumerate(algorithms):
            offset = (i - 0.5) * width  # Center bars for 2 algorithms
            bars = ax1.bar(x + offset, values_by_algo[alg], width, 
                          label=alg.upper(), alpha=0.8, edgecolor='black',
                          color=self.colors[alg])
        
        ax1.set_ylabel('Tổng giá trị', fontweight='bold', fontsize=12)
        ax1.set_title('Solution Quality: Impact of Data Characteristics', fontweight='bold', pad=15, fontsize=13)
        ax1.set_xticks(x)
        ax1.set_xticklabels([dt.replace('_', ' ').title() for dt in data_types])
        ax1.legend(loc='best', frameon=True, shadow=True)
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Plot 2: Time comparison across data types
        ax2 = fig.add_subplot(gs[1, :])
        
        for i, alg in enumerate(algorithms):
            offset = (i - 0.5) * width  # Center bars for 2 algorithms
            bars = ax2.bar(x + offset, times_by_algo[alg], width, 
                          label=alg.upper(), alpha=0.8, edgecolor='black',
                          color=self.colors[alg])
        
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
        
        # Create ranking table (2 algorithms only)
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
        
        # Table with 3 columns (1 data type + 2 algorithms)
        table = ax4.table(cellText=ranking_data, cellLoc='center', loc='center',
                         colWidths=[0.33, 0.33, 0.33])
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1, 2.5)
        
        # Style header (3 columns now)
        for i in range(3):
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
                   linewidths=0.5, label='Không được chọn')
        
        # Selected items (colored by region)
        if 'region' in selected_data.columns:
            regions = selected_data['region'].unique()
            region_colors = plt.cm.Set3(np.linspace(0, 1, len(regions)))
            
            for i, region in enumerate(regions):
                region_data = selected_data[selected_data['region'] == region]
                ax1.scatter(region_data['weight'], region_data['value'], 
                           s=300, c=[region_colors[i]], alpha=0.8, 
                           edgecolors='black', linewidths=2, 
                           label=f'Vùng {region}', marker='o')
        else:
            ax1.scatter(selected_data['weight'], selected_data['value'], 
                       s=300, c=self.colors['feasible'], alpha=0.8, 
                       edgecolors='black', linewidths=2, label='Đã chọn')
        
        ax1.set_xlabel('Trọng lượng', fontweight='bold', fontsize=12)
        ax1.set_ylabel('Giá trị', fontweight='bold', fontsize=12)
        ax1.set_title('Bản đồ lựa chọn vật phẩm: Trọng lượng vs Giá trị', fontweight='bold', pad=15, fontsize=13)
        ax1.legend(loc='best', frameon=True, shadow=True)
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Capacity utilization
        ax2 = fig.add_subplot(gs[0, 2])
        
        utilization = (total_weight / capacity) * 100 if capacity > 0 else 0
        remaining = 100 - utilization
        
        colors_util = [self.colors['feasible'] if utilization <= 100 else self.colors['infeasible'], 'lightgray']
        wedges, texts, autotexts = ax2.pie([utilization, remaining], 
                                           labels=['Đã sử dụng', 'Còn lại'], 
                                           autopct='%1.1f%%',
                                           startangle=90, colors=colors_util,
                                           textprops={'fontweight': 'bold', 'fontsize': 11})
        
        ax2.set_title(f'Sử dụng sức chứa\n{total_weight:.1f} / {capacity:.1f}', 
                     fontweight='bold', pad=15, fontsize=13)
        
        # Plot 3: Regional diversity (if available)
        ax3 = fig.add_subplot(gs[1, 0])
        
        if 'region' in selected_data.columns:
            region_counts = selected_data['region'].value_counts()
            
            ax3.bar(region_counts.index.astype(str), region_counts.values, 
                   color=region_colors[:len(region_counts)], alpha=0.8, 
                   edgecolor='black', linewidth=2)
            
            ax3.set_xlabel('Vùng', fontweight='bold', fontsize=12)
            ax3.set_ylabel('Số lượng vật phẩm', fontweight='bold', fontsize=12)
            ax3.set_title('Phân bố đa dạng theo vùng', fontweight='bold', pad=15, fontsize=13)
            ax3.grid(True, alpha=0.3, axis='y')
        else:
            ax3.text(0.5, 0.5, 'Không có dữ liệu vùng', ha='center', va='center', 
                    fontsize=14, transform=ax3.transAxes)
        
        # Plot 4: Value contribution by category (if available)
        ax4 = fig.add_subplot(gs[1, 1])
        
        if 'category' in selected_data.columns:
            category_values = selected_data.groupby('category')['value'].sum().sort_values(ascending=False)
            
            ax4.barh(category_values.index, category_values.values, 
                    color=self.colors['bpso'], alpha=0.7, edgecolor='black', linewidth=1.5)
            
            ax4.set_xlabel('Tổng giá trị', fontweight='bold', fontsize=12)
            ax4.set_title('Đóng góp giá trị theo danh mục', fontweight='bold', pad=15, fontsize=13)
            ax4.grid(True, alpha=0.3, axis='x')
        else:
            ax4.text(0.5, 0.5, 'Không có dữ liệu danh mục', ha='center', va='center', 
                    fontsize=14, transform=ax4.transAxes)
        
        # Plot 5: Summary statistics
        ax5 = fig.add_subplot(gs[1, 2])
        ax5.axis('off')
        
        summary_data = [
            ['Chỉ số', 'Giá trị'],
            ['Tổng số vật phẩm', f"{len(selected_items)}"],
            ['Tổng giá trị', f"{total_value:.0f}"],
            ['Tổng trọng lượng', f"{total_weight:.1f}"],
            ['Sức chứa', f"{capacity:.1f}"],
            ['Sử dụng', f"{utilization:.1f}%"],
            ['Giá trị TB/vật', f"{total_value/len(selected_items):.1f}" if len(selected_items) > 0 else "0"],
            ['Trọng lượng TB/vật', f"{total_weight/len(selected_items):.1f}" if len(selected_items) > 0 else "0"]
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
        
        plt.suptitle('Trực quan hóa giải pháp Knapsack', 
                    fontsize=16, fontweight='bold', y=0.98)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    # =========================================================================
    # 3.1.2. ALGORITHM COMPARISON
    # =========================================================================
    
    def plot_algorithm_comparison(self, df_comparison: pd.DataFrame, title=None, save_path=None):
        """
        Comprehensive algorithm comparison visualization
        Like GA_TSP comparing GA vs RLGA vs GA+SA
        
        Args:
            df_comparison: DataFrame with columns [algorithm, value_mean, value_std, time_mean, pct_optimal]
        """
        fig = plt.figure(figsize=(16, 12))
        gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.35)
        
        algorithms = df_comparison['algorithm'].tolist()
        colors = [self.colors.get(algo.lower(), '#95a5a6') for algo in algorithms]
        
        # Plot 1: Solution Quality Comparison (Bar chart)
        ax1 = fig.add_subplot(gs[0, 0])
        values = df_comparison['value_mean'].values
        bars = ax1.bar(algorithms, values, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
        
        # Add value labels on bars
        for bar, val in zip(bars, values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:.0f}', ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        ax1.set_ylabel('Tổng giá trị', fontsize=11, fontweight='bold')
        ax1.set_title('So sánh chất lượng giải pháp', fontsize=12, fontweight='bold', pad=10)
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Plot 2: Computational Cost (Log scale)
        ax2 = fig.add_subplot(gs[0, 1])
        times = df_comparison['time_mean'].values
        bars = ax2.bar(algorithms, times, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
        
        for bar, t in zip(bars, times):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{t:.4f}s', ha='center', va='bottom', fontweight='bold', fontsize=9)
        
        ax2.set_ylabel('Thời gian thực thi (giây)', fontsize=11, fontweight='bold')
        ax2.set_title('So sánh chi phí tính toán', fontsize=12, fontweight='bold', pad=10)
        ax2.set_yscale('log')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Plot 3: Algorithm Efficiency (Value/Time)
        ax3 = fig.add_subplot(gs[0, 2])
        efficiency = values / np.maximum(times, 1e-10)
        bars = ax3.bar(algorithms, efficiency, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
        ax3.set_ylabel('Hiệu suất (Giá trị/Thời gian)', fontsize=11, fontweight='bold')
        ax3.set_title('Hiệu suất thuật toán', fontsize=12, fontweight='bold', pad=10)
        ax3.grid(True, alpha=0.3, axis='y')
        ax3.set_yscale('log')
        
        # Plot 4: Quality vs Speed Trade-off (Scatter)
        ax4 = fig.add_subplot(gs[1, :2])
        for i, algo in enumerate(algorithms):
            ax4.scatter(times[i], values[i], s=500, c=colors[i], 
                       edgecolors='black', linewidth=2, alpha=0.8, label=algo)
            ax4.text(times[i], values[i], algo, ha='center', va='center',
                    fontsize=10, fontweight='bold', color='white')
        
        ax4.set_xlabel('Thời gian thực thi (giây)', fontsize=12, fontweight='bold')
        ax4.set_ylabel('Tổng giá trị', fontsize=12, fontweight='bold')
        ax4.set_title('Đánh đổi Chất lượng vs Tốc độ', fontsize=13, fontweight='bold', pad=15)
        ax4.set_xscale('log')
        ax4.legend(loc='best', fontsize=10, frameon=True, shadow=True)
        ax4.grid(True, alpha=0.3)
        
        # Plot 5: Summary Table
        ax5 = fig.add_subplot(gs[1, 2])
        ax5.axis('off')
        
        summary_data = [['Thuật toán', 'Giá trị', 'Thời gian (s)', 'Hiệu suất', '% Tối ưu', 'Xếp hạng']]
        
        # Sort by value for ranking
        sorted_df = df_comparison.sort_values('value_mean', ascending=False)
        for rank, (_, row) in enumerate(sorted_df.iterrows(), 1):
            emoji = '🥇' if rank == 1 else '🥈' if rank == 2 else '🥉'
            summary_data.append([
                row['algorithm'],
                f"{row['value_mean']:.0f}",
                f"{row['time_mean']:.4f}",
                f"{row['value_mean']/row['time_mean']:.0f}",
                f"{row['pct_optimal']:.2f}%",
                f"{emoji}"
            ])
        
        table = ax5.table(cellText=summary_data, cellLoc='center', loc='center',
                         colWidths=[0.15, 0.15, 0.15, 0.15, 0.20, 0.10])
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2.5)
        
        # Style header
        for i in range(6):
            table[(0, i)].set_facecolor('#2c3e50')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        # Highlight winner
        table[(1, 0)].set_facecolor('#fff9c4')
        
        # Add overall title
        if title:
            plt.suptitle(title, fontsize=16, fontweight='bold', y=0.98)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    # =========================================================================
    # 3.1.3. DATA CHARACTERISTICS IMPACT (Alternative DataFrame-based version)
    # =========================================================================
    
    def plot_data_characteristics_impact_from_df(self, df_data: pd.DataFrame, title=None, save_path=None):
        """
        Analyze impact of data characteristics on algorithm performance (DataFrame version)
        
        Args:
            df_data: DataFrame with columns [characteristic, test_case, gbfs_value, gbfs_time, 
                                             bpso_value, bpso_time, dp_value, dp_time, 
                                             gbfs_pct_optimal, bpso_pct_optimal]
        """
        fig = plt.figure(figsize=(18, 12))
        gs = GridSpec(3, 2, figure=fig, hspace=0.35, wspace=0.3)
        
        # Get unique characteristics
        characteristics = df_data['characteristic'].unique()
        
        # Plot 1: Solution Quality by Characteristic
        ax1 = fig.add_subplot(gs[0, :])
        x = np.arange(len(characteristics))
        width = 0.25
        
        gbfs_values = [df_data[df_data['characteristic']==c]['gbfs_value'].mean() for c in characteristics]
        bpso_values = [df_data[df_data['characteristic']==c]['bpso_value'].mean() for c in characteristics]
        dp_values = [df_data[df_data['characteristic']==c]['dp_value'].mean() for c in characteristics]
        
        ax1.bar(x - width, gbfs_values, width, label='GBFS', color=self.colors['gbfs'], alpha=0.8, edgecolor='black')
        ax1.bar(x, bpso_values, width, label='BPSO', color=self.colors['bpso'], alpha=0.8, edgecolor='black')
        ax1.bar(x + width, dp_values, width, label='DP', color=self.colors['dp'], alpha=0.8, edgecolor='black')
        
        ax1.set_xlabel('Đặc điểm dữ liệu', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Tổng giá trị', fontsize=12, fontweight='bold')
        ax1.set_title('Chất lượng giải pháp: Ảnh hưởng của đặc điểm dữ liệu', fontsize=14, fontweight='bold', pad=15)
        ax1.set_xticks(x)
        ax1.set_xticklabels([c.replace('_', ' ').title() for c in characteristics], rotation=15, ha='right')
        ax1.legend(fontsize=11, loc='upper left')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Plot 2: Computational Cost by Characteristic
        ax2 = fig.add_subplot(gs[1, :])
        
        gbfs_times = [df_data[df_data['characteristic']==c]['gbfs_time'].mean() for c in characteristics]
        bpso_times = [df_data[df_data['characteristic']==c]['bpso_time'].mean() for c in characteristics]
        dp_times = [df_data[df_data['characteristic']==c]['dp_time'].mean() for c in characteristics]
        
        ax2.bar(x - width, gbfs_times, width, label='GBFS', color=self.colors['gbfs'], alpha=0.8, edgecolor='black')
        ax2.bar(x, bpso_times, width, label='BPSO', color=self.colors['bpso'], alpha=0.8, edgecolor='black')
        ax2.bar(x + width, dp_times, width, label='DP', color=self.colors['dp'], alpha=0.8, edgecolor='black')
        
        ax2.set_xlabel('Đặc điểm dữ liệu', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Thời gian thực thi (giây)', fontsize=12, fontweight='bold')
        ax2.set_title('Chi phí tính toán: Ảnh hưởng của đặc điểm dữ liệu', fontsize=14, fontweight='bold', pad=15)
        ax2.set_yscale('log')
        ax2.set_xticks(x)
        ax2.set_xticklabels([c.replace('_', ' ').title() for c in characteristics], rotation=15, ha='right')
        ax2.legend(fontsize=11, loc='upper left')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Plot 3: Performance Degradation (% from optimal)
        ax3 = fig.add_subplot(gs[2, 0])
        
        gbfs_degradation = [100 - df_data[df_data['characteristic']==c]['gbfs_pct_optimal'].mean() 
                           for c in characteristics]
        bpso_degradation = [100 - df_data[df_data['characteristic']==c]['bpso_pct_optimal'].mean() 
                           for c in characteristics]
        
        x_pos = np.arange(len(characteristics))
        bars1 = ax3.bar(x_pos - 0.2, gbfs_degradation, 0.4, label='GBFS', 
                       color='#e74c3c', alpha=0.7, edgecolor='black')
        bars2 = ax3.bar(x_pos + 0.2, bpso_degradation, 0.4, label='BPSO', 
                       color='#c0392b', alpha=0.7, edgecolor='black')
        
        # Add percentage labels
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                if height > 0.5:  # Only show if significant
                    ax3.text(bar.get_x() + bar.get_width()/2., height,
                            f'{height:.1f}%', ha='center', va='bottom', fontsize=8)
        
        ax3.set_xlabel('Đặc điểm dữ liệu', fontsize=11, fontweight='bold')
        ax3.set_ylabel('Độ suy giảm hiệu suất (%)', fontsize=11, fontweight='bold')
        ax3.set_title('Độ nhạy cảm với tương quan dữ liệu', fontsize=12, fontweight='bold', pad=10)
        ax3.set_xticks(x_pos)
        ax3.set_xticklabels([c.replace('_', ' ').title() for c in characteristics], 
                           rotation=30, ha='right', fontsize=9)
        ax3.legend(fontsize=10)
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Plot 4: Summary Table
        ax4 = fig.add_subplot(gs[2, 1])
        ax4.axis('off')
        
        table_data = [['Loại dữ liệu', 'GBFS', 'BPSO', 'DP']]
        for c in characteristics:
            subset = df_data[df_data['characteristic'] == c]
            table_data.append([
                c.replace('_', ' ').title(),
                f"{subset['gbfs_pct_optimal'].mean():.2f}%",
                f"{subset['bpso_pct_optimal'].mean():.2f}%",
                "100.00%"
            ])
        
        table = ax4.table(cellText=table_data, cellLoc='center', loc='center',
                         colWidths=[0.35, 0.2, 0.2, 0.2])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2.5)
        
        # Style header
        for i in range(4):
            table[(0, i)].set_facecolor('#2c3e50')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        if title:
            plt.suptitle(title, fontsize=16, fontweight='bold', y=0.98)
        
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
