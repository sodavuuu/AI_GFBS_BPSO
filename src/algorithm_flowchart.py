"""
=================================================================================
ALGORITHM FLOWCHART VISUALIZER - Following Google Images Style
=================================================================================
Tạo flowchart diagram cho GBFS và BPSO giống như trong ảnh Google search
=================================================================================
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np


class AlgorithmFlowchart:
    """Vẽ flowchart cho GBFS và BPSO theo style ảnh Google"""
    
    @staticmethod
    def draw_gbfs_flowchart(ax):
        """
        Vẽ GBFS flowchart - Greedy Best First Search
        Giống ảnh: Start → Initialize → Loop → Expand → Goal Check → End
        """
        ax.clear()
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 12)
        ax.axis('off')
        
        # Title
        ax.text(5, 11.5, 'Greedy Best-First Search Algorithm', 
               fontsize=16, fontweight='bold', ha='center',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#3498db', 
                        edgecolor='black', linewidth=2, alpha=0.9),
               color='white')
        
        # Color scheme
        start_color = '#2ecc71'  # Green
        process_color = '#3498db'  # Blue
        decision_color = '#f39c12'  # Orange
        end_color = '#e74c3c'  # Red
        
        # Node 1: START
        start = FancyBboxPatch((4, 10), 2, 0.7, boxstyle="round,pad=0.1",
                               facecolor=start_color, edgecolor='black', linewidth=2)
        ax.add_patch(start)
        ax.text(5, 10.35, 'START', fontsize=12, fontweight='bold', ha='center', va='center')
        
        # Arrow down
        ax.annotate('', xy=(5, 9.5), xytext=(5, 10),
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        
        # Node 2: Initialize (Priority Queue, Visited Set)
        init = FancyBboxPatch((3, 8.8), 4, 0.6, boxstyle="round,pad=0.1",
                             facecolor=process_color, edgecolor='black', linewidth=2)
        ax.add_patch(init)
        ax.text(5, 9.1, 'Initialize Priority Queue', fontsize=10, ha='center', va='center', color='white')
        ax.text(5, 8.95, 'Add start state', fontsize=8, ha='center', va='center', color='white', style='italic')
        
        # Arrow down
        ax.annotate('', xy=(5, 8.3), xytext=(5, 8.8),
                   arrowprops=dict(arrowstops='->', lw=2, color='black'))
        
        # Node 3: Queue Empty? (Decision Diamond)
        diamond_x = [5, 6.2, 5, 3.8, 5]
        diamond_y = [8.3, 7.5, 6.7, 7.5, 8.3]
        ax.fill(diamond_x, diamond_y, facecolor=decision_color, edgecolor='black', linewidth=2)
        ax.text(5, 7.5, 'Queue\nEmpty?', fontsize=9, fontweight='bold', ha='center', va='center')
        
        # Arrow right (Yes → Fail)
        ax.annotate('Yes', xy=(6.5, 7.5), xytext=(6.2, 7.5),
                   fontsize=8, ha='left', va='center', fontweight='bold')
        ax.annotate('', xy=(7.5, 7.5), xytext=(6.5, 7.5),
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        fail = FancyBboxPatch((7.5, 7.2), 1.5, 0.6, boxstyle="round,pad=0.1",
                             facecolor=end_color, edgecolor='black', linewidth=2)
        ax.add_patch(fail)
        ax.text(8.25, 7.5, 'FAIL', fontsize=10, fontweight='bold', ha='center', va='center', color='white')
        
        # Arrow down (No)
        ax.annotate('No', xy=(5, 6.5), xytext=(5, 6.7),
                   fontsize=8, ha='center', va='top', fontweight='bold')
        ax.annotate('', xy=(5, 6.2), xytext=(5, 6.5),
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        
        # Node 4: Pop best node (lowest h(n))
        pop = FancyBboxPatch((3, 5.5), 4, 0.6, boxstyle="round,pad=0.1",
                            facecolor=process_color, edgecolor='black', linewidth=2)
        ax.add_patch(pop)
        ax.text(5, 5.8, 'Pop node with best h(n)', fontsize=10, ha='center', va='center', color='white')
        ax.text(5, 5.65, '(heuristic value)', fontsize=7, ha='center', va='center', color='white', style='italic')
        
        # Arrow down
        ax.annotate('', xy=(5, 5.0), xytext=(5, 5.5),
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        
        # Node 5: Goal Test? (Decision Diamond)
        diamond2_x = [5, 6.2, 5, 3.8, 5]
        diamond2_y = [5.0, 4.2, 3.4, 4.2, 5.0]
        ax.fill(diamond2_x, diamond2_y, facecolor=decision_color, edgecolor='black', linewidth=2)
        ax.text(5, 4.2, 'Goal\nReached?', fontsize=9, fontweight='bold', ha='center', va='center')
        
        # Arrow right (Yes → Success)
        ax.annotate('Yes', xy=(6.5, 4.2), xytext=(6.2, 4.2),
                   fontsize=8, ha='left', va='center', fontweight='bold', color='green')
        ax.annotate('', xy=(7.5, 4.2), xytext=(6.5, 4.2),
                   arrowprops=dict(arrowstyle='->', lw=2.5, color='green'))
        success = FancyBboxPatch((7.5, 3.9), 1.5, 0.6, boxstyle="round,pad=0.1",
                                facecolor=start_color, edgecolor='black', linewidth=2)
        ax.add_patch(success)
        ax.text(8.25, 4.2, 'SUCCESS', fontsize=10, fontweight='bold', ha='center', va='center', color='white')
        
        # Arrow down (No)
        ax.annotate('No', xy=(5, 3.2), xytext=(5, 3.4),
                   fontsize=8, ha='center', va='top', fontweight='bold')
        ax.annotate('', xy=(5, 2.9), xytext=(5, 3.2),
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        
        # Node 6: Expand neighbors
        expand = FancyBboxPatch((3, 2.2), 4, 0.6, boxstyle="round,pad=0.1",
                               facecolor=process_color, edgecolor='black', linewidth=2)
        ax.add_patch(expand)
        ax.text(5, 2.5, 'Generate successors', fontsize=10, ha='center', va='center', color='white')
        ax.text(5, 2.35, 'Add to queue (sorted by h)', fontsize=7, ha='center', va='center', color='white', style='italic')
        
        # Arrow back up (Loop)
        ax.annotate('', xy=(2.5, 7.5), xytext=(2.5, 2.5),
                   arrowprops=dict(arrowstyle='->', lw=2, color='gray', linestyle='dashed'))
        ax.annotate('', xy=(3.8, 7.5), xytext=(2.5, 7.5),
                   arrowprops=dict(arrowstyle='->', lw=2, color='gray', linestyle='dashed'))
        ax.text(1.8, 5, 'Loop', fontsize=9, rotation=90, va='center', 
               fontweight='bold', color='gray')
        
        # Legend - Key Features
        ax.text(0.5, 1.5, 'Key Features:', fontsize=10, fontweight='bold')
        ax.text(0.5, 1.2, '• Heuristic: h(n) = estimated cost to goal', fontsize=8)
        ax.text(0.5, 0.95, '• Greedy: always expand best h(n)', fontsize=8)
        ax.text(0.5, 0.7, '• Not optimal: may miss better paths', fontsize=8)
        ax.text(0.5, 0.45, '• Fast: explores fewer nodes', fontsize=8)
        
        # Complexity box
        complexity = FancyBboxPatch((6.5, 0.3), 3, 1.3, boxstyle="round,pad=0.15",
                                   facecolor='#ecf0f1', edgecolor='#34495e', linewidth=2)
        ax.add_patch(complexity)
        ax.text(8, 1.4, 'Complexity', fontsize=10, fontweight='bold', ha='center')
        ax.text(8, 1.1, 'Time: O(b^m)', fontsize=9, ha='center', family='monospace')
        ax.text(8, 0.85, 'Space: O(b^m)', fontsize=9, ha='center', family='monospace')
        ax.text(8, 0.55, 'b=branching, m=depth', fontsize=7, ha='center', style='italic')
    
    @staticmethod
    def draw_bpso_flowchart(ax):
        """
        Vẽ BPSO flowchart - Binary Particle Swarm Optimization
        Giống ảnh: Initialize Swarm → Evaluate → Update → Check Convergence
        """
        ax.clear()
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 14)
        ax.axis('off')
        
        # Title
        ax.text(6, 13.3, 'Binary Particle Swarm Optimization', 
               fontsize=16, fontweight='bold', ha='center',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#e74c3c', 
                        edgecolor='black', linewidth=2, alpha=0.9),
               color='white')
        
        # Color scheme
        start_color = '#2ecc71'
        process_color = '#e74c3c'  # Red (BPSO theme)
        decision_color = '#f39c12'
        update_color = '#9b59b6'  # Purple
        
        # Node 1: START
        start = FancyBboxPatch((5, 12), 2, 0.7, boxstyle="round,pad=0.1",
                               facecolor=start_color, edgecolor='black', linewidth=2)
        ax.add_patch(start)
        ax.text(6, 12.35, 'START', fontsize=12, fontweight='bold', ha='center', va='center')
        
        # Arrow
        ax.annotate('', xy=(6, 11.5), xytext=(6, 12),
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        
        # Node 2: Initialize Swarm
        init = FancyBboxPatch((4, 10.7), 4, 0.7, boxstyle="round,pad=0.1",
                             facecolor=process_color, edgecolor='black', linewidth=2)
        ax.add_patch(init)
        ax.text(6, 11.15, 'Initialize Swarm', fontsize=11, ha='center', va='center', 
               color='white', fontweight='bold')
        ax.text(6, 10.92, 'N particles, random positions', fontsize=8, ha='center', 
               va='center', color='white', style='italic')
        
        # Arrow
        ax.annotate('', xy=(6, 10.2), xytext=(6, 10.7),
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        
        # Node 3: Evaluate Fitness
        eval_box = FancyBboxPatch((4, 9.5), 4, 0.6, boxstyle="round,pad=0.1",
                                 facecolor=process_color, edgecolor='black', linewidth=2)
        ax.add_patch(eval_box)
        ax.text(6, 9.8, 'Evaluate fitness f(x)', fontsize=10, ha='center', va='center', 
               color='white', fontweight='bold')
        ax.text(6, 9.62, 'for each particle', fontsize=8, ha='center', va='center', 
               color='white', style='italic')
        
        # Arrow
        ax.annotate('', xy=(6, 9.0), xytext=(6, 9.5),
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        
        # Node 4: Update Personal Best (pBest)
        pbest = FancyBboxPatch((0.5, 8.3), 3, 0.6, boxstyle="round,pad=0.1",
                              facecolor=update_color, edgecolor='black', linewidth=2)
        ax.add_patch(pbest)
        ax.text(2, 8.6, 'Update pBest', fontsize=9, ha='center', va='center', 
               color='white', fontweight='bold')
        ax.text(2, 8.42, 'if f(x) > f(pBest)', fontsize=7, ha='center', va='center', 
               color='white', style='italic')
        
        # Node 5: Update Global Best (gBest)
        gbest = FancyBboxPatch((8.5, 8.3), 3, 0.6, boxstyle="round,pad=0.1",
                              facecolor=update_color, edgecolor='black', linewidth=2)
        ax.add_patch(gbest)
        ax.text(10, 8.6, 'Update gBest', fontsize=9, ha='center', va='center', 
               color='white', fontweight='bold')
        ax.text(10, 8.42, 'best of all pBest', fontsize=7, ha='center', va='center', 
               color='white', style='italic')
        
        # Arrows to update boxes
        ax.annotate('', xy=(3.5, 8.6), xytext=(6, 9.0),
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))
        ax.annotate('', xy=(8.5, 8.6), xytext=(6, 9.0),
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))
        
        # Arrows down from update boxes
        ax.annotate('', xy=(2, 7.5), xytext=(2, 8.3),
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))
        ax.annotate('', xy=(10, 7.5), xytext=(10, 8.3),
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))
        ax.annotate('', xy=(6, 7.5), xytext=(2, 7.5),
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))
        ax.annotate('', xy=(6, 7.5), xytext=(10, 7.5),
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))
        
        # Node 6: Update Velocity
        velocity = FancyBboxPatch((4, 6.7), 4, 0.7, boxstyle="round,pad=0.1",
                                 facecolor=process_color, edgecolor='black', linewidth=2)
        ax.add_patch(velocity)
        ax.text(6, 7.15, 'Update Velocity', fontsize=10, ha='center', va='center', 
               color='white', fontweight='bold')
        ax.text(6, 6.88, 'v = w*v + c1*r1*(pBest-x) + c2*r2*(gBest-x)', 
               fontsize=7, ha='center', va='center', color='white', family='monospace')
        
        # Arrow
        ax.annotate('', xy=(6, 6.2), xytext=(6, 6.7),
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        
        # Node 7: Update Position (Binary)
        position = FancyBboxPatch((4, 5.4), 4, 0.7, boxstyle="round,pad=0.1",
                                 facecolor=process_color, edgecolor='black', linewidth=2)
        ax.add_patch(position)
        ax.text(6, 5.85, 'Update Position (Binary)', fontsize=10, ha='center', 
               va='center', color='white', fontweight='bold')
        ax.text(6, 5.58, 'x = 1 if sigmoid(v) > rand() else 0', 
               fontsize=7, ha='center', va='center', color='white', family='monospace')
        
        # Arrow
        ax.annotate('', xy=(6, 4.9), xytext=(6, 5.4),
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        
        # Node 8: Convergence Check (Decision Diamond)
        diamond_x = [6, 7.5, 6, 4.5, 6]
        diamond_y = [4.9, 3.9, 2.9, 3.9, 4.9]
        ax.fill(diamond_x, diamond_y, facecolor=decision_color, edgecolor='black', linewidth=2)
        ax.text(6, 3.9, 'Max\nIterations\nor\nConverged?', fontsize=8, 
               fontweight='bold', ha='center', va='center')
        
        # Arrow left (No → Loop back)
        ax.annotate('No', xy=(3.5, 3.9), xytext=(4.5, 3.9),
                   fontsize=9, ha='right', va='center', fontweight='bold')
        ax.annotate('', xy=(3, 3.9), xytext=(3.5, 3.9),
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        ax.annotate('', xy=(3, 10.5), xytext=(3, 3.9),
                   arrowprops=dict(arrowstyle='->', lw=2, color='gray', linestyle='dashed'))
        ax.annotate('', xy=(4, 10.5), xytext=(3, 10.5),
                   arrowprops=dict(arrowstyle='->', lw=2, color='gray', linestyle='dashed'))
        ax.text(2.3, 7, 'Loop', fontsize=10, rotation=90, va='center', 
               fontweight='bold', color='gray')
        
        # Arrow down (Yes)
        ax.annotate('Yes', xy=(6, 2.7), xytext=(6, 2.9),
                   fontsize=9, ha='center', va='top', fontweight='bold', color='green')
        ax.annotate('', xy=(6, 2.2), xytext=(6, 2.7),
                   arrowprops=dict(arrowstyle='->', lw=2.5, color='green'))
        
        # Node 9: Return Best Solution
        end = FancyBboxPatch((4.5, 1.5), 3, 0.6, boxstyle="round,pad=0.1",
                            facecolor=start_color, edgecolor='black', linewidth=2)
        ax.add_patch(end)
        ax.text(6, 1.8, 'Return gBest', fontsize=11, ha='center', va='center', 
               color='white', fontweight='bold')
        
        # Arrow to END
        ax.annotate('', xy=(6, 0.9), xytext=(6, 1.5),
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        end_node = FancyBboxPatch((5, 0.3), 2, 0.5, boxstyle="round,pad=0.1",
                                 facecolor=start_color, edgecolor='black', linewidth=2)
        ax.add_patch(end_node)
        ax.text(6, 0.55, 'END', fontsize=11, fontweight='bold', ha='center', va='center')
        
        # Legend - Parameters box (right side)
        param_box = FancyBboxPatch((8.5, 0.3), 3.2, 2.2, boxstyle="round,pad=0.15",
                                  facecolor='#ecf0f1', edgecolor='#34495e', linewidth=2)
        ax.add_patch(param_box)
        ax.text(10.1, 2.3, 'BPSO Parameters', fontsize=10, fontweight='bold', ha='center')
        ax.text(8.7, 1.95, 'w  = inertia (0.7)', fontsize=8, ha='left', family='monospace')
        ax.text(8.7, 1.7, 'c₁ = cognitive (2.0)', fontsize=8, ha='left', family='monospace')
        ax.text(8.7, 1.45, 'c₂ = social (2.0)', fontsize=8, ha='left', family='monospace')
        ax.text(8.7, 1.2, 'r₁, r₂ = random[0,1]', fontsize=8, ha='left', family='monospace')
        ax.text(10.1, 0.85, 'Binary: sigmoid(v)', fontsize=8, ha='center', 
               style='italic', fontweight='bold')
        ax.text(10.1, 0.55, 'x ∈ {0,1}', fontsize=9, ha='center', family='monospace')


def draw_gbfs_flowchart(ax):
    """Wrapper function"""
    AlgorithmFlowchart.draw_gbfs_flowchart(ax)


def draw_bpso_flowchart(ax):
    """Wrapper function"""
    AlgorithmFlowchart.draw_bpso_flowchart(ax)
