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
    """
    fig = canvas.fig
    fig.clear()
    
    selected_indices = result['selected_indices']
    
    # Create 2x2 layout
    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2)
    ax3 = fig.add_subplot(2, 2, 3)
    ax4 = fig.add_subplot(2, 2, 4)
    
    # Plot 1: Weight vs Value scatter with selection order and arrows
    ax1.scatter(test_data['weight'], test_data['value'], 
               s=100, alpha=0.3, c='gray', edgecolors='black', linewidth=0.5, label='Chưa chọn')
    
    # Draw arrows connecting selected items in order
    selected_positions = []
    for order, idx in enumerate(selected_indices, 1):
        item = test_data.iloc[idx]
        selected_positions.append((item['weight'], item['value']))
        
        # Draw arrow from previous item (if not first)
        if order > 1:
            prev_x, prev_y = selected_positions[order-2]
            curr_x, curr_y = item['weight'], item['value']
            ax1.annotate('', xy=(curr_x, curr_y), xytext=(prev_x, prev_y),
                        arrowprops=dict(arrowstyle='->', lw=2, color='darkgreen', alpha=0.6))
        
        # Show selected items with order numbers
        ax1.scatter(item['weight'], item['value'], 
                   s=200, alpha=0.8, c='green', edgecolors='darkgreen', linewidth=2)
        ax1.text(item['weight'], item['value'], str(order), 
                ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    
    ax1.set_xlabel('Trọng lượng', fontsize=10, fontweight='bold')
    ax1.set_ylabel('Giá trị', fontsize=10, fontweight='bold')
    ax1.set_title('Thứ tự lựa chọn của GBFS (Tham lam theo tỷ lệ)', fontsize=10, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=8)
    
    # Plot 2: Selection sequence (value over order)
    selected_values = [test_data.iloc[idx]['value'] for idx in selected_indices]
    selected_weights = [test_data.iloc[idx]['weight'] for idx in selected_indices]
    ax2.plot(range(1, len(selected_values)+1), selected_values, 'g-o', linewidth=2, markersize=8)
    ax2.set_xlabel('Thứ tự lựa chọn', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Giá trị vật phẩm', fontsize=10, fontweight='bold')
    ax2.set_title('Giá trị của từng vật phẩm được chọn', fontsize=10, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Cumulative weight capacity usage
    cumulative_weight = []
    total = 0
    for w in selected_weights:
        total += w
        cumulative_weight.append(total)
    
    capacity = test_case['capacity']
    ax3.plot(range(1, len(cumulative_weight)+1), cumulative_weight, 'b-o', linewidth=2, markersize=8, label='Trọng lượng tích lũy')
    ax3.axhline(y=capacity, color='red', linestyle='--', linewidth=2, label=f'Sức chứa: {capacity}')
    ax3.fill_between(range(1, len(cumulative_weight)+1), 0, cumulative_weight, alpha=0.3, color='blue')
    ax3.set_xlabel('Thứ tự lựa chọn', fontsize=10, fontweight='bold')
    ax3.set_ylabel('Trọng lượng', fontsize=10, fontweight='bold')
    ax3.set_title('Trọng lượng tích lũy vs Sức chứa', fontsize=10, fontweight='bold')
    ax3.legend(fontsize=8)
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Ratio ranking (why these items were selected)
    test_data['ratio'] = test_data['value'] / test_data['weight']
    sorted_items = test_data.sort_values('ratio', ascending=False)
    
    colors = ['green' if i in selected_indices else 'lightgray' for i in sorted_items.index[:20]]
    top_20 = sorted_items.head(20)
    
    ax4.barh(range(len(top_20)), top_20['ratio'], color=colors, edgecolor='black')
    ax4.set_yticks(range(len(top_20)))
    ax4.set_yticklabels([f'Vật phẩm {i}' for i in top_20.index], fontsize=8)
    ax4.set_xlabel('Tỷ lệ Giá trị/Trọng lượng', fontsize=10, fontweight='bold')
    ax4.set_title('Top 20 vật phẩm theo tỷ lệ (Xanh = Đã chọn)', fontsize=10, fontweight='bold')
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
    
    # Create 2x2 layout for better visibility (top-left empty)
    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2)
    ax3 = fig.add_subplot(2, 1, 2)  # Bottom full width
    
    # Plot 1: Convergence with best/avg
    if 'convergence' in result and 'best_fitness' in result['convergence']:
        best_history = result['convergence']['best_fitness']
        iterations = range(1, len(best_history) + 1)
        
        ax1.plot(iterations, best_history, 'b-', linewidth=2.5, label='Độ thích nghi tốt nhất', 
                marker='o', markersize=4, markevery=max(1, len(best_history)//15))
        
        if 'avg_fitness' in result['convergence']:
            avg_history = result['convergence']['avg_fitness']
            ax1.plot(iterations, avg_history, color='red', linewidth=1.5, alpha=0.7,
                    label='Độ thích nghi trung bình', linestyle='--', marker='s', markersize=3,
                    markevery=max(1, len(avg_history)//15))
        
        ax1.set_xlabel('Vòng lặp', fontsize=10, fontweight='bold')
        ax1.set_ylabel('Độ thích nghi', fontsize=10, fontweight='bold')
        ax1.set_title('Hội tụ của BPSO', fontsize=11, fontweight='bold')
        ax1.legend(fontsize=9)
        ax1.grid(True, alpha=0.3)
        
        # Annotate final
        final_val = best_history[-1]
        ax1.annotate(f'Cuối: {final_val:.0f}',
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
        ax2.set_xlabel('Vòng lặp', fontsize=10, fontweight='bold')
        ax2.set_ylabel('Tốt nhất - Trung bình', fontsize=10, fontweight='bold')
        ax2.set_title('Đa dạng bầy đàn (Khám phá)', fontsize=11, fontweight='bold')
        ax2.grid(True, alpha=0.3)
    
    # Plot 3: Selected items with convergence path and swarm concept (bottom full width)
    if test_data is not None and len(test_data) > 0:
        selected_indices = result['selected_indices']
        
        ax3.scatter(test_data['weight'], test_data['value'],
                   s=80, alpha=0.3, c='gray', edgecolors='black', linewidth=0.5, label='Chưa chọn')
        
        selected_items = test_data.iloc[selected_indices]
        
        # Draw connection lines between selected items to show swarm behavior
        if len(selected_items) > 1:
            # Connect items based on value (high to low)
            sorted_selected = selected_items.sort_values('value', ascending=False)
            for i in range(len(sorted_selected)-1):
                x1, y1 = sorted_selected.iloc[i]['weight'], sorted_selected.iloc[i]['value']
                x2, y2 = sorted_selected.iloc[i+1]['weight'], sorted_selected.iloc[i+1]['value']
                ax3.plot([x1, x2], [y1, y2], 'b--', alpha=0.3, linewidth=1)
        
        ax3.scatter(selected_items['weight'], selected_items['value'],
                   s=150, alpha=0.8, c='blue', edgecolors='darkblue', linewidth=2, label='Được chọn bởi BPSO')
        
        # Highlight best item (global best concept)
        if len(selected_items) > 0:
            best_item = selected_items.loc[selected_items['value'].idxmax()]
            ax3.scatter(best_item['weight'], best_item['value'],
                       s=300, alpha=1.0, c='red', edgecolors='darkred', linewidth=3, 
                       marker='*', label='Tốt nhất toàn cục', zorder=5)
        
        ax3.set_xlabel('Trọng lượng', fontsize=11, fontweight='bold')
        ax3.set_ylabel('Giá trị', fontsize=11, fontweight='bold')
        ax3.set_title('Không gian giải pháp của BPSO', fontsize=12, fontweight='bold')
        ax3.legend(fontsize=10, loc='best')
        ax3.grid(True, alpha=0.3)
    
    fig.tight_layout()
    canvas.draw()
