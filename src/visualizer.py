"""
=================================================================================
VISUALIZATION MODULE - Real-time Charts như GA_TSP
=================================================================================
Tạo charts trực quan cho Multi-Objective Knapsack:
- Convergence plots (BPSO)
- Algorithm comparison
- Trade-off charts (f₁ vs f₂)
- Performance metrics
=================================================================================
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
import seaborn as sns
import numpy as np
import pandas as pd
from typing import List, Dict
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10


class KnapsackVisualizer:
    """Visualization cho Knapsack problem"""
    
    def __init__(self, figsize=(14, 10)):
        self.figsize = figsize
        self.colors = sns.color_palette("husl", 8)
    
    # =========================================================================
    # 1. CONVERGENCE PLOT (như GA_TSP)
    # =========================================================================
    
    def plot_convergence(self, bpso_result: Dict, save_path=None):
        """
        Vẽ convergence plot cho BPSO
        - Best fitness qua các iterations
        - Average fitness
        - Feasibility rate
        """
        fig, axes = plt.subplots(2, 1, figsize=(12, 8))
        
        fitness_history = bpso_result.get('best_fitness_history', [])
        avg_fitness_history = bpso_result.get('avg_fitness_history', [])
        iterations = list(range(1, len(fitness_history) + 1))
        
        # Plot 1: Fitness convergence
        ax1 = axes[0]
        ax1.plot(iterations, fitness_history, 'b-', linewidth=2, label='Best Fitness')
        ax1.plot(iterations, avg_fitness_history, 'g--', linewidth=1.5, label='Avg Fitness', alpha=0.7)
        ax1.fill_between(iterations, fitness_history, avg_fitness_history, alpha=0.2, color='blue')
        
        ax1.set_xlabel('Iteration', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Fitness Value', fontsize=12, fontweight='bold')
        ax1.set_title('BPSO Convergence Plot', fontsize=14, fontweight='bold')
        ax1.legend(loc='lower right', fontsize=10)
        ax1.grid(True, alpha=0.3)
        
        # Annotate final value
        final_fitness = fitness_history[-1]
        ax1.annotate(f'Final: {final_fitness:.2f}',
                    xy=(len(iterations), final_fitness),
                    xytext=(len(iterations)*0.7, final_fitness*0.95),
                    arrowprops=dict(arrowstyle='->', color='red', lw=2),
                    fontsize=11, color='red', fontweight='bold')
        
        # Plot 2: Improvement rate
        ax2 = axes[1]
        improvements = [0] + [fitness_history[i] - fitness_history[i-1] 
                             for i in range(1, len(fitness_history))]
        ax2.bar(iterations, improvements, color='orange', alpha=0.6, label='Fitness Improvement')
        ax2.axhline(y=0, color='red', linestyle='--', linewidth=1)
        ax2.set_xlabel('Iteration', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Fitness Improvement', fontsize=12, fontweight='bold')
        ax2.set_title('Iteration-wise Improvement', fontsize=14, fontweight='bold')
        ax2.legend(loc='upper right')
        ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    # =========================================================================
    # 2. SOLUTION VISUALIZATION
    # =========================================================================
    
    def plot_solution(self, items, weights, values, solution, capacity, title="Solution", save_path=None):
        """
        Vẽ solution:
        - Items được chọn (xanh) vs không chọn (đỏ)
        - Weight vs Value scatter
        - Capacity usage bar
        """
        fig = plt.figure(figsize=(14, 10))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        selected_indices = [i for i, x in enumerate(solution) if x == 1]
        not_selected_indices = [i for i, x in enumerate(solution) if x == 0]
        
        # Plot 1: Weight vs Value scatter
        ax1 = fig.add_subplot(gs[0, :])
        
        # Not selected (red)
        ax1.scatter([weights[i] for i in not_selected_indices],
                   [values[i] for i in not_selected_indices],
                   s=100, c='red', alpha=0.4, label='Not Selected', marker='o')
        
        # Selected (green)
        ax1.scatter([weights[i] for i in selected_indices],
                   [values[i] for i in selected_indices],
                   s=150, c='green', alpha=0.7, label='Selected', marker='s')
        
        ax1.set_xlabel('Weight', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Value', fontsize=12, fontweight='bold')
        ax1.set_title(f'{title} - Items Selection', fontsize=14, fontweight='bold')
        ax1.legend(loc='upper right', fontsize=11)
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Capacity usage
        ax2 = fig.add_subplot(gs[1, 0])
        
        total_weight = sum(weights[i] for i in selected_indices)
        used_percent = (total_weight / capacity) * 100
        
        bars = ax2.barh(['Capacity'], [total_weight], color='green', alpha=0.7, height=0.5)
        ax2.barh(['Capacity'], [capacity - total_weight], left=[total_weight], 
                color='lightgray', alpha=0.5, height=0.5)
        
        ax2.set_xlim(0, capacity * 1.1)
        ax2.set_xlabel('Weight', fontsize=12, fontweight='bold')
        ax2.set_title(f'Capacity Usage: {used_percent:.1f}%', fontsize=12, fontweight='bold')
        
        # Add text
        ax2.text(total_weight/2, 0, f'{total_weight:.0f}', 
                ha='center', va='center', fontsize=11, fontweight='bold', color='white')
        ax2.text(total_weight + (capacity-total_weight)/2, 0, f'{capacity-total_weight:.0f}', 
                ha='center', va='center', fontsize=11, fontweight='bold')
        
        # Plot 3: Value distribution
        ax3 = fig.add_subplot(gs[1, 1])
        
        total_value = sum(values[i] for i in selected_indices)
        max_possible_value = sum(values)
        value_percent = (total_value / max_possible_value) * 100
        
        bars = ax3.barh(['Value'], [total_value], color='blue', alpha=0.7, height=0.5)
        ax3.barh(['Value'], [max_possible_value - total_value], left=[total_value],
                color='lightgray', alpha=0.5, height=0.5)
        
        ax3.set_xlim(0, max_possible_value * 1.1)
        ax3.set_xlabel('Value', fontsize=12, fontweight='bold')
        ax3.set_title(f'Value Obtained: {value_percent:.1f}%', fontsize=12, fontweight='bold')
        
        ax3.text(total_value/2, 0, f'{total_value:.0f}', 
                ha='center', va='center', fontsize=11, fontweight='bold', color='white')
        
        # Plot 4: Summary stats
        ax4 = fig.add_subplot(gs[2, :])
        ax4.axis('off')
        
        stats_text = f"""
        📊 SOLUTION SUMMARY
        {'='*70}
        Items Selected:     {len(selected_indices)} / {len(items)}
        Total Value:        {total_value:,.2f}
        Total Weight:       {total_weight:,.2f} / {capacity:,.2f} ({used_percent:.1f}%)
        Avg Value/Item:     {total_value/len(selected_indices):.2f}
        Efficiency:         {total_value/total_weight:.2f} (value/weight)
        {'='*70}
        """
        
        ax4.text(0.5, 0.5, stats_text, 
                ha='center', va='center',
                fontsize=11, family='monospace',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
        
        plt.suptitle(title, fontsize=16, fontweight='bold', y=0.995)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    # =========================================================================
    # 3. ALGORITHM COMPARISON
    # =========================================================================
    
    def plot_algorithm_comparison(self, results_df: pd.DataFrame, save_path=None):
        """
        So sánh GBFS vs BPSO vs DP
        - Gap % với optimal
        - Time comparison
        - Best/Mean/Std
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Plot 1: Gap % comparison
        ax1 = axes[0, 0]
        x = np.arange(len(results_df))
        width = 0.35
        
        ax1.bar(x - width/2, results_df['gbfs_gap_percent'], width, 
               label='GBFS', color='steelblue', alpha=0.8)
        ax1.bar(x + width/2, results_df['bpso_gap_percent'], width,
               label='BPSO', color='coral', alpha=0.8)
        
        ax1.set_xlabel('Test Cases', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Gap % from Optimal', fontsize=11, fontweight='bold')
        ax1.set_title('Algorithm Gap Analysis', fontsize=12, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(results_df['test_case'], rotation=45, ha='right', fontsize=8)
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Plot 2: Time comparison (log scale)
        ax2 = axes[0, 1]
        
        ax2.bar(x - width/2, results_df['gbfs_time'], width,
               label='GBFS', color='steelblue', alpha=0.8)
        ax2.bar(x + width/2, results_df['bpso_time'], width,
               label='BPSO', color='coral', alpha=0.8)
        
        ax2.set_xlabel('Test Cases', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Time (seconds)', fontsize=11, fontweight='bold')
        ax2.set_title('Execution Time Comparison', fontsize=12, fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels(results_df['test_case'], rotation=45, ha='right', fontsize=8)
        ax2.set_yscale('log')
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Plot 3: Best vs Mean values
        ax3 = axes[1, 0]
        
        ax3.plot(x, results_df['gbfs_mean'], 'o-', label='GBFS Mean', 
                color='steelblue', linewidth=2, markersize=8)
        ax3.plot(x, results_df['bpso_mean'], 's-', label='BPSO Mean',
                color='coral', linewidth=2, markersize=8)
        ax3.plot(x, results_df['dp_optimal'], '^--', label='DP Optimal',
                color='green', linewidth=2, markersize=8, alpha=0.7)
        
        ax3.set_xlabel('Test Cases', fontsize=11, fontweight='bold')
        ax3.set_ylabel('Fitness Value', fontsize=11, fontweight='bold')
        ax3.set_title('Solution Quality Comparison', fontsize=12, fontweight='bold')
        ax3.set_xticks(x)
        ax3.set_xticklabels(results_df['test_case'], rotation=45, ha='right', fontsize=8)
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Summary statistics
        ax4 = axes[1, 1]
        ax4.axis('off')
        
        summary_text = f"""
        📊 OVERALL STATISTICS
        {'='*50}
        
        GBFS:
          Avg Gap:      {results_df['gbfs_gap_percent'].mean():.2f}%
          Avg Time:     {results_df['gbfs_time'].mean():.3f}s
          Best Case:    {results_df['gbfs_gap_percent'].min():.2f}% gap
          
        BPSO:
          Avg Gap:      {results_df['bpso_gap_percent'].mean():.2f}%
          Avg Time:     {results_df['bpso_time'].mean():.3f}s
          Best Case:    {results_df['bpso_gap_percent'].min():.2f}% gap
          
        DP (Optimal):
          Avg Time:     {results_df['dp_time'].mean():.3f}s
        
        {'='*50}
        Winner: {'GBFS' if results_df['gbfs_gap_percent'].mean() < results_df['bpso_gap_percent'].mean() else 'BPSO'}
        """
        
        ax4.text(0.5, 0.5, summary_text,
                ha='center', va='center',
                fontsize=10, family='monospace',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
        
        plt.suptitle('Algorithm Comparison Dashboard', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    # =========================================================================
    # 4. MULTI-OBJECTIVE TRADE-OFF (f₁ vs f₂)
    # =========================================================================
    
    def plot_regional_diversity_tradeoff(self, results_df: pd.DataFrame, save_path=None):
        """
        Vẽ trade-off giữa f₁ (revenue) và f₂ (regional diversity)
        """
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Filter regional diversity test cases
        regional_tests = results_df[results_df['test_case'].str.contains('Region_|Size_Large')]
        
        if 'n_regions' not in regional_tests.columns:
            # Add n_regions manually
            regional_tests = regional_tests.copy()
            regional_tests['n_regions'] = regional_tests['test_case'].apply(
                lambda x: 1 if '1regions' in x.lower() else
                         2 if '2regions' in x.lower() else
                         3 if '3regions' in x.lower() else 4
            )
        
        # Plot 1: Fitness vs f₂
        ax1 = axes[0]
        
        for algo, color, marker in [('gbfs', 'steelblue', 'o'), ('bpso', 'coral', 's')]:
            ax1.plot(regional_tests['n_regions'], 
                    regional_tests[f'{algo}_mean'],
                    marker=marker, linestyle='-', linewidth=2, markersize=10,
                    label=algo.upper(), color=color, alpha=0.7)
        
        ax1.plot(regional_tests['n_regions'], 
                regional_tests['dp_optimal'],
                marker='^', linestyle='--', linewidth=2, markersize=10,
                label='DP (Optimal)', color='green', alpha=0.7)
        
        ax1.set_xlabel('Regional Diversity (f₂)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Fitness Value (f₁)', fontsize=12, fontweight='bold')
        ax1.set_title('Trade-off: Revenue vs Diversity', fontsize=14, fontweight='bold')
        ax1.set_xticks([1, 2, 3, 4])
        ax1.set_xticklabels(['1 region', '2 regions', '3 regions', '4 regions'])
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Gap % vs f₂
        ax2 = axes[1]
        
        for algo, color, marker in [('gbfs', 'steelblue', 'o'), ('bpso', 'coral', 's')]:
            ax2.plot(regional_tests['n_regions'],
                    regional_tests[f'{algo}_gap_percent'],
                    marker=marker, linestyle='-', linewidth=2, markersize=10,
                    label=algo.upper(), color=color, alpha=0.7)
        
        ax2.set_xlabel('Regional Diversity (f₂)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Gap % from Optimal', fontsize=12, fontweight='bold')
        ax2.set_title('Algorithm Performance vs Diversity', fontsize=14, fontweight='bold')
        ax2.set_xticks([1, 2, 3, 4])
        ax2.set_xticklabels(['1 region', '2 regions', '3 regions', '4 regions'])
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.suptitle('Multi-Objective Trade-off Analysis', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {save_path}")
        else:
            plt.show()
        
        plt.close()


# =================================================================================
# UTILITY FUNCTIONS
# =================================================================================

def create_results_dashboard(results_df, output_dir='results/visualizations'):
    """Tạo dashboard với tất cả charts"""
    os.makedirs(output_dir, exist_ok=True)
    
    viz = KnapsackVisualizer()
    
    print("\n📊 Creating visualization dashboard...")
    
    # 1. Algorithm comparison
    print("  1. Algorithm comparison...")
    viz.plot_algorithm_comparison(
        results_df,
        save_path=f"{output_dir}/01_algorithm_comparison.png"
    )
    
    # 2. Regional diversity trade-off
    print("  2. Regional diversity trade-off...")
    viz.plot_regional_diversity_tradeoff(
        results_df,
        save_path=f"{output_dir}/02_regional_tradeoff.png"
    )
    
    print(f"\n✅ Dashboard saved to: {output_dir}/")


if __name__ == '__main__':
    # Test with sample data
    print("Visualization module loaded successfully!")
