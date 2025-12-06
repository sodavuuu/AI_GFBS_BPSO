"""
Step-by-step visualization for GBFS and BPSO algorithms
Shows actual item selection process (not flowcharts)
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Circle


def visualize_gbfs_selection_steps(canvas, result, test_data, test_case):
    """
    Visualize GBFS greedy selection step-by-step
    Like TSP showing cities being selected in order
    """
    fig = canvas.fig
    fig.clear()
    
    selected_indices = result['selected_indices']
    
    # Create 2x2 layout
    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2)
    ax3 = fig.add_subplot(2, 2, 3)
    ax4 = fig.add_subplot(2, 2, 4)
    
    # Plot 1: Weight vs Value scatter with selection order
    ax1.scatter(test_data['weight'], test_data['value'], 
               s=100, alpha=0.3, c='gray', edgecolors='black', linewidth=0.5, label='Not Selected')
    
    # Show selected items with order numbers
    for order, idx in enumerate(selected_indices, 1):
        item = test_data.iloc[idx]
        ax1.scatter(item['weight'], item['value'], 
                   s=200, alpha=0.8, c='green', edgecolors='darkgreen', linewidth=2)
        ax1.text(item['weight'], item['value'], str(order), 
                ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    
    ax1.set_xlabel('Weight', fontsize=10, fontweight='bold')
    ax1.set_ylabel('Value', fontsize=10, fontweight='bold')
    ax1.set_title('GBFS Selection Order (Greedy by Ratio)', fontsize=10, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=8)
    
    # Plot 2: Selection sequence (value over order)
    selected_values = [test_data.iloc[idx]['value'] for idx in selected_indices]
    selected_weights = [test_data.iloc[idx]['weight'] for idx in selected_indices]
    ax2.plot(range(1, len(selected_values)+1), selected_values, 'g-o', linewidth=2, markersize=8)
    ax2.set_xlabel('Selection Order', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Item Value', fontsize=10, fontweight='bold')
    ax2.set_title('Value of Each Selected Item', fontsize=10, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Cumulative weight capacity usage
    cumulative_weight = []
    total = 0
    for w in selected_weights:
        total += w
        cumulative_weight.append(total)
    
    capacity = test_case['capacity']
    ax3.plot(range(1, len(cumulative_weight)+1), cumulative_weight, 'b-o', linewidth=2, markersize=8, label='Cumulative Weight')
    ax3.axhline(y=capacity, color='red', linestyle='--', linewidth=2, label=f'Capacity: {capacity}')
    ax3.fill_between(range(1, len(cumulative_weight)+1), 0, cumulative_weight, alpha=0.3, color='blue')
    ax3.set_xlabel('Selection Order', fontsize=10, fontweight='bold')
    ax3.set_ylabel('Weight', fontsize=10, fontweight='bold')
    ax3.set_title('Cumulative Weight vs Capacity', fontsize=10, fontweight='bold')
    ax3.legend(fontsize=8)
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Ratio ranking (why these items were selected)
    test_data['ratio'] = test_data['value'] / test_data['weight']
    sorted_items = test_data.sort_values('ratio', ascending=False)
    
    colors = ['green' if i in selected_indices else 'lightgray' for i in sorted_items.index[:20]]
    top_20 = sorted_items.head(20)
    
    ax4.barh(range(len(top_20)), top_20['ratio'], color=colors, edgecolor='black')
    ax4.set_yticks(range(len(top_20)))
    ax4.set_yticklabels([f'Item {i}' for i in top_20.index], fontsize=8)
    ax4.set_xlabel('Value/Weight Ratio', fontsize=10, fontweight='bold')
    ax4.set_title('Top 20 Items by Ratio (Green = Selected)', fontsize=10, fontweight='bold')
    ax4.grid(True, alpha=0.3, axis='x')
    ax4.invert_yaxis()
    
    fig.tight_layout()
    canvas.draw()


def visualize_bpso_swarm_behavior(canvas, result, test_data=None):
    """
    Visualize BPSO swarm behavior
    Shows particle movement and convergence
    """
    fig = canvas.fig
    fig.clear()
    
    # Create 2x2 layout
    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2)
    ax3 = fig.add_subplot(2, 2, 3)
    ax4 = fig.add_subplot(2, 2, 4)
    
    # Plot 1: Convergence with best/avg
    if 'convergence' in result and 'best_fitness' in result['convergence']:
        best_history = result['convergence']['best_fitness']
        iterations = range(1, len(best_history) + 1)
        
        ax1.plot(iterations, best_history, 'b-', linewidth=2.5, label='Best Fitness', 
                marker='o', markersize=4, markevery=max(1, len(best_history)//15))
        
        if 'avg_fitness' in result['convergence']:
            avg_history = result['convergence']['avg_fitness']
            ax1.plot(iterations, avg_history, color='red', linewidth=1.5, alpha=0.7,
                    label='Avg Fitness', linestyle='--', marker='s', markersize=3,
                    markevery=max(1, len(avg_history)//15))
        
        ax1.set_xlabel('Iteration', fontsize=10, fontweight='bold')
        ax1.set_ylabel('Fitness', fontsize=10, fontweight='bold')
        ax1.set_title('BPSO Convergence', fontsize=10, fontweight='bold')
        ax1.legend(fontsize=8)
        ax1.grid(True, alpha=0.3)
        
        # Annotate final
        final_val = best_history[-1]
        ax1.annotate(f'Final: {final_val:.0f}',
                    xy=(len(best_history), final_val),
                    xytext=(-50, 15), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                    arrowprops=dict(arrowstyle='->', lw=1.5),
                    fontsize=9, fontweight='bold')
    
    # Plot 2: Diversity (best - avg) over time
    if 'convergence' in result and 'best_fitness' in result['convergence'] and 'avg_fitness' in result['convergence']:
        best_history = result['convergence']['best_fitness']
        avg_history = result['convergence']['avg_fitness']
        diversity = [abs(best - avg) for best, avg in zip(best_history, avg_history)]
        iterations = range(1, len(diversity) + 1)
        
        ax2.plot(iterations, diversity, 'purple', linewidth=2, marker='o', markersize=3)
        ax2.fill_between(iterations, 0, diversity, alpha=0.3, color='purple')
        ax2.set_xlabel('Iteration', fontsize=10, fontweight='bold')
        ax2.set_ylabel('Best - Average', fontsize=10, fontweight='bold')
        ax2.set_title('Swarm Diversity (Exploration)', fontsize=10, fontweight='bold')
        ax2.grid(True, alpha=0.3)
    
    # Plot 3: Selected items visualization (if we have item data)
    if test_data is not None and len(test_data) > 0:
        selected_indices = result['selected_indices']
        
        ax3.scatter(test_data['weight'], test_data['value'],
                   s=80, alpha=0.3, c='gray', edgecolors='black', linewidth=0.5, label='Not Selected')
        
        selected_items = test_data.iloc[selected_indices]
        ax3.scatter(selected_items['weight'], selected_items['value'],
                   s=150, alpha=0.8, c='blue', edgecolors='darkblue', linewidth=2, label='Selected by BPSO')
        
        ax3.set_xlabel('Weight', fontsize=10, fontweight='bold')
        ax3.set_ylabel('Value', fontsize=10, fontweight='bold')
        ax3.set_title('BPSO Selected Items', fontsize=10, fontweight='bold')
        ax3.legend(fontsize=8)
        ax3.grid(True, alpha=0.3)
    
    # Plot 4: Parameter influence diagram
    ax4.axis('off')
    
    # Draw swarm influence diagram (like your reference image)
    # Current position
    x_current = Circle((0.3, 0.3), 0.08, facecolor='black', edgecolor='black', linewidth=2)
    ax4.add_patch(x_current)
    ax4.text(0.3, 0.15, r'$x_i(k)$', ha='center', fontsize=11, fontweight='bold', transform=ax4.transAxes)
    ax4.text(0.3, 0.05, 'Current', ha='center', fontsize=8, transform=ax4.transAxes)
    
    # Personal best
    p_best = Circle((0.65, 0.5), 0.08, facecolor='blue', edgecolor='blue', linewidth=2)
    ax4.add_patch(p_best)
    ax4.text(0.65, 0.35, r'$p_i^{best}$', ha='center', fontsize=11, fontweight='bold', color='blue', transform=ax4.transAxes)
    ax4.text(0.65, 0.25, 'Personal Best', ha='center', fontsize=8, color='blue', transform=ax4.transAxes)
    
    # Global best
    g_best = Circle((0.2, 0.7), 0.08, facecolor='red', edgecolor='red', linewidth=2)
    ax4.add_patch(g_best)
    ax4.text(0.2, 0.55, r'$g^{best}$', ha='center', fontsize=11, fontweight='bold', color='red', transform=ax4.transAxes)
    ax4.text(0.2, 0.45, 'Global Best', ha='center', fontsize=8, color='red', transform=ax4.transAxes)
    
    # Next position
    x_next = Circle((0.5, 0.65), 0.08, facecolor='black', edgecolor='black', linewidth=2)
    ax4.add_patch(x_next)
    ax4.text(0.5, 0.8, r'$x_i(k+1)$', ha='center', fontsize=11, fontweight='bold', transform=ax4.transAxes)
    
    # Arrows
    # Inertia (green)
    arrow1 = FancyArrowPatch((0.3, 0.38), (0.42, 0.58),
                            arrowstyle='->', mutation_scale=20, linewidth=2.5,
                            color='green', linestyle='--', transform=ax4.transAxes)
    ax4.add_patch(arrow1)
    ax4.text(0.32, 0.52, r'$w \cdot v_i(k)$', fontsize=9, color='green', fontweight='bold', transform=ax4.transAxes)
    
    # Cognitive (blue)
    arrow2 = FancyArrowPatch((0.38, 0.35), (0.57, 0.45),
                            arrowstyle='->', mutation_scale=20, linewidth=2,
                            color='blue', linestyle='--', transform=ax4.transAxes)
    ax4.add_patch(arrow2)
    ax4.text(0.52, 0.38, r'$c_1$', fontsize=8, color='blue', fontweight='bold', transform=ax4.transAxes)
    
    # Social (red)
    arrow3 = FancyArrowPatch((0.26, 0.38), (0.28, 0.62),
                            arrowstyle='->', mutation_scale=20, linewidth=2,
                            color='red', linestyle='--', transform=ax4.transAxes)
    ax4.add_patch(arrow3)
    ax4.text(0.18, 0.5, r'$c_2$', fontsize=8, color='red', fontweight='bold', transform=ax4.transAxes)
    
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.set_title('BPSO Swarm Influence', fontsize=10, fontweight='bold', transform=ax4.transAxes, y=0.98)
    
    fig.tight_layout()
    canvas.draw()
