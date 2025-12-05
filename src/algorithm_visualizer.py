"""
=================================================================================
ALGORITHM VISUALIZER - Specialized visualizations for each algorithm
=================================================================================
GBFS: State Expansion Tree
BPSO: Particle Swarm Movement + Convergence
DP: Dynamic Programming Table with Backtracking Path
=================================================================================
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from sklearn.decomposition import PCA
import networkx as nx


class AlgorithmVisualizer:
    """Specialized visualizations for each algorithm"""
    
    @staticmethod
    def visualize_gbfs_tree(ax, result, max_nodes=50):
        """
        GBFS State Expansion Tree Visualization
        Shows how GBFS explores states using heuristic guidance
        """
        ax.clear()
        
        if 'state_tree' not in result or not result['state_tree']:
            ax.text(0.5, 0.5, 'No state tree data available', 
                   ha='center', va='center', fontsize=12)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            return
        
        # Build tree structure
        G = nx.DiGraph()
        state_tree = result['state_tree'][:max_nodes]  # Limit nodes
        
        # Add root
        root = tuple()
        G.add_node(root, label='∅', h=0)
        
        # Add edges from state_tree
        for parent, action, child, h_val in state_tree:
            if parent not in G:
                parent_label = ','.join(map(str, parent)) if parent else '∅'
                G.add_node(parent, label=parent_label, h=0)
            
            if child not in G:
                child_label = ','.join(map(str, child)) if len(child) <= 3 else f"{len(child)} items"
                G.add_node(child, label=child_label, h=h_val)
            
            G.add_edge(parent, child, action=action)
        
        # Layout
        pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.3, 
                              arrows=True, arrowsize=10, 
                              edge_color='gray', width=1.5)
        
        # Draw nodes with heuristic values
        node_colors = []
        labels = {}
        
        for node in G.nodes():
            h_val = G.nodes[node]['h']
            node_colors.append(h_val)
            label = G.nodes[node]['label']
            labels[node] = f"{label}\nh={h_val:.1f}"
        
        # Normalize colors
        if node_colors:
            max_h = max(node_colors) if max(node_colors) > 0 else 1
            node_colors = [h/max_h for h in node_colors]
        
        # Draw
        nx.draw_networkx_nodes(G, pos, ax=ax, 
                              node_color=node_colors,
                              cmap='YlOrRd',
                              node_size=800,
                              alpha=0.8)
        
        nx.draw_networkx_labels(G, pos, labels, ax=ax,
                               font_size=7, font_weight='bold')
        
        # Highlight final state
        final_state = tuple(sorted(result['selected_indices']))
        if final_state in G:
            nx.draw_networkx_nodes(G, pos, nodelist=[final_state],
                                  node_color='green', node_size=1000,
                                  alpha=0.8, ax=ax)
        
        ax.set_title('GBFS State Expansion Tree\n(Nodes colored by heuristic value)', 
                    fontsize=11, fontweight='bold')
        ax.axis('off')
        
        # Add legend
        ax.text(0.02, 0.98, f'States explored: {result["states_explored"]}\n'
                           f'Final value: {result["total_value"]:.0f}',
               transform=ax.transAxes, fontsize=9,
               verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    @staticmethod
    def visualize_bpso_swarm(ax, result, iteration_idx=0):
        """
        BPSO Particle Swarm Visualization
        Shows particles moving in search space (PCA projected to 2D)
        """
        ax.clear()
        
        if 'particle_history' not in result or not result['particle_history']:
            ax.text(0.5, 0.5, 'No particle history available\n(Run BPSO algorithm first)', 
                   ha='center', va='center', fontsize=12)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            return
        
        # Get data for specific iteration
        particle_history = result['particle_history']
        iteration_idx = min(iteration_idx, len(particle_history) - 1)
        
        if iteration_idx < 0:
            iteration_idx = len(particle_history) - 1  # Use last iteration
        
        iteration, positions, gbest_pos = particle_history[iteration_idx]
        
        # Project to 2D using PCA
        n_particles = positions.shape[0]
        n_dims = positions.shape[1]
        
        if n_dims < 2:
            # Not enough dimensions
            ax.text(0.5, 0.5, 'Problem dimension too small for visualization', 
                   ha='center', va='center', fontsize=10)
            ax.axis('off')
            return
        
        try:
            pca = PCA(n_components=2)
            positions_2d = pca.fit_transform(positions)
            gbest_2d = pca.transform(gbest_pos.reshape(1, -1))[0]
        except Exception as e:
            ax.text(0.5, 0.5, f'PCA projection failed: {str(e)}', 
                   ha='center', va='center', fontsize=10)
            ax.axis('off')
            return
        
        # Color by diversity (distance from gbest)
        distances = np.linalg.norm(positions_2d - gbest_2d, axis=1)
        
        # Plot particles
        scatter = ax.scatter(positions_2d[:, 0], positions_2d[:, 1],
                           c=distances, cmap='viridis', s=100, 
                           alpha=0.6, edgecolors='black', linewidth=0.5)
        
        # Plot gbest
        ax.scatter(gbest_2d[0], gbest_2d[1], 
                  c='red', marker='*', s=500, 
                  edgecolors='darkred', linewidth=2,
                  label='Global Best', zorder=10)
        
        # Add velocity vectors (simplified - just show direction to gbest)
        for i in range(min(10, n_particles)):  # Show only 10 vectors
            dx = gbest_2d[0] - positions_2d[i, 0]
            dy = gbest_2d[1] - positions_2d[i, 1]
            ax.arrow(positions_2d[i, 0], positions_2d[i, 1],
                    dx * 0.1, dy * 0.1,
                    head_width=0.3, head_length=0.2,
                    fc='gray', ec='gray', alpha=0.3)
        
        ax.set_title(f'BPSO Particle Swarm (Iteration {iteration})\n'
                    f'PCA projection to 2D space',
                    fontsize=11, fontweight='bold')
        ax.set_xlabel('Principal Component 1', fontsize=9)
        ax.set_ylabel('Principal Component 2', fontsize=9)
        ax.legend(loc='upper right', fontsize=9)
        ax.grid(True, alpha=0.3)
        
        # Colorbar - use figure instead of plt
        try:
            fig = ax.get_figure()
            cbar = fig.colorbar(scatter, ax=ax)
            cbar.set_label('Distance from gBest', fontsize=9)
        except Exception:
            pass  # Skip colorbar if error
        
        # Stats
        variance = f"{pca.explained_variance_ratio_[0]:.1%}" if len(pca.explained_variance_ratio_) > 0 else "N/A"
        ax.text(0.02, 0.98, f'Particles: {n_particles}\n'
                           f'Best fitness: {result.get("total_value", 0):.0f}\n'
                           f'PC1 variance: {variance}',
               transform=ax.transAxes, fontsize=9,
               verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    
    @staticmethod
    def visualize_bpso_convergence(ax, result):
        """
        BPSO Convergence Curve
        Shows how fitness improves over iterations
        """
        ax.clear()
        
        if 'convergence' not in result:
            ax.text(0.5, 0.5, 'No convergence data available', 
                   ha='center', va='center', fontsize=12)
            ax.axis('off')
            return
        
        conv = result['convergence']
        iterations = range(len(conv['best_fitness']))
        
        # Plot
        ax.plot(iterations, conv['best_fitness'], 
               label='Best Fitness', linewidth=2.5, color='#2ecc71')
        ax.plot(iterations, conv['avg_fitness'],
               label='Avg Fitness', linewidth=1.5, 
               color='#3498db', linestyle='--', alpha=0.7)
        
        # Fill area
        ax.fill_between(iterations, conv['best_fitness'], conv['avg_fitness'],
                       alpha=0.2, color='lightblue')
        
        ax.set_xlabel('Iteration', fontsize=10, fontweight='bold')
        ax.set_ylabel('Fitness Value', fontsize=10, fontweight='bold')
        ax.set_title('BPSO Convergence Curve', fontsize=11, fontweight='bold')
        ax.legend(loc='lower right', fontsize=9)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # Highlight final
        final_val = conv['best_fitness'][-1]
        ax.scatter(len(iterations)-1, final_val, 
                  color='red', s=100, zorder=10, marker='o')
        ax.annotate(f'{final_val:.0f}', 
                   xy=(len(iterations)-1, final_val),
                   xytext=(10, 10), textcoords='offset points',
                   fontsize=9, fontweight='bold',
                   bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7),
                   arrowprops=dict(arrowstyle='->', color='red'))
    
    @staticmethod
    def visualize_dp_table(ax, result, show_values=True):
        """
        DP Table Visualization with Backtracking Path
        Shows the dynamic programming table and solution path
        """
        ax.clear()
        
        if 'dp_table' not in result:
            ax.text(0.5, 0.5, 'No DP table available', 
                   ha='center', va='center', fontsize=12)
            ax.axis('off')
            return
        
        dp_table = result['dp_table']
        n, capacity = dp_table.shape
        
        # Limit visualization size
        max_display = 15
        if n > max_display or capacity > max_display:
            # Sample the table
            row_step = max(1, n // max_display)
            col_step = max(1, capacity // max_display)
            dp_display = dp_table[::row_step, ::col_step]
            show_values = False  # Too dense
        else:
            dp_display = dp_table
            row_step = 1
            col_step = 1
        
        # Draw heatmap
        im = ax.imshow(dp_display, cmap='YlGnBu', aspect='auto', 
                      interpolation='nearest', alpha=0.8)
        
        # Add values if table is small enough
        if show_values and dp_display.shape[0] <= 12 and dp_display.shape[1] <= 12:
            for i in range(dp_display.shape[0]):
                for j in range(dp_display.shape[1]):
                    val = dp_display[i, j]
                    color = 'white' if val > dp_display.max() * 0.6 else 'black'
                    ax.text(j, i, f'{val}', ha='center', va='center',
                           color=color, fontsize=7, fontweight='bold')
        
        # Highlight backtrack path
        if 'backtrack_path' in result:
            path_coords = []
            for row, col, item in result['backtrack_path']:
                # Convert to display coordinates
                display_row = row // row_step
                display_col = col // col_step
                if 0 <= display_row < dp_display.shape[0] and 0 <= display_col < dp_display.shape[1]:
                    path_coords.append((display_col, display_row))
                    
                    # Mark if item was taken
                    if item >= 0:
                        rect = patches.Rectangle((display_col-0.4, display_row-0.4), 
                                                 0.8, 0.8,
                                                 linewidth=2, edgecolor='red',
                                                 facecolor='none')
                        ax.add_patch(rect)
            
            # Draw path
            if len(path_coords) > 1:
                path_array = np.array(path_coords)
                ax.plot(path_array[:, 0], path_array[:, 1], 
                       color='red', linewidth=2, marker='o',
                       markersize=4, alpha=0.6, label='Solution Path')
        
        # Labels
        ax.set_xlabel('Capacity', fontsize=10, fontweight='bold')
        ax.set_ylabel('Items', fontsize=10, fontweight='bold')
        ax.set_title('Dynamic Programming Table\n(Backtrack path in red)', 
                    fontsize=11, fontweight='bold')
        
        # Colorbar - use figure instead of plt
        try:
            fig = ax.get_figure()
            cbar = fig.colorbar(im, ax=ax)
            cbar.set_label('Value', fontsize=9)
        except Exception:
            pass  # Skip colorbar if error
        
        # Stats
        ax.text(1.15, 0.02, f'Optimal value: {result.get("total_value", 0)}\n'
                            f'Items selected: {len(result.get("selected_indices", []))}\n'
                            f'Table size: {n-1}×{capacity}',
               transform=ax.transAxes, fontsize=9,
               verticalalignment='bottom',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        if len(path_coords) > 1:
            ax.legend(loc='upper left', fontsize=8)
    
    @staticmethod
    def visualize_bit_vector(ax, result, algorithm='GBFS'):
        """
        Bit Vector Visualization - shows selected items as binary string
        Common visualization for all algorithms
        """
        ax.clear()
        
        if 'selected_indices' not in result:
            ax.text(0.5, 0.5, 'No solution available', 
                   ha='center', va='center', fontsize=12)
            ax.axis('off')
            return
        
        # Determine problem size
        if algorithm == 'GBFS' and 'state_tree' in result and result['state_tree']:
            n = max(max(state[2]) if state[2] else 0 for state in result['state_tree']) + 1
        else:
            n = max(result['selected_indices']) + 1 if result['selected_indices'] else 1
        
        # Create bit vector
        bit_vector = [0] * n
        for idx in result['selected_indices']:
            if idx < n:
                bit_vector[idx] = 1
        
        # Visualize
        colors = ['lightgray' if b == 0 else 'green' for b in bit_vector]
        
        # Draw squares
        square_size = min(0.8, 8 / n)
        for i, (bit, color) in enumerate(zip(bit_vector, colors)):
            rect = patches.Rectangle((i, 0), square_size, square_size,
                                     linewidth=2, edgecolor='black',
                                     facecolor=color, alpha=0.7)
            ax.add_patch(rect)
            
            # Add bit value
            ax.text(i + square_size/2, square_size/2, str(bit),
                   ha='center', va='center', fontsize=10, fontweight='bold')
            
            # Add item index
            ax.text(i + square_size/2, -0.2, f'i{i}',
                   ha='center', va='center', fontsize=8, color='gray')
        
        ax.set_xlim(-0.5, n)
        ax.set_ylim(-0.5, 1.5)
        ax.set_aspect('equal')
        ax.axis('off')
        
        ax.set_title(f'{algorithm} Solution - Bit Vector Representation\n'
                    f'(Green = Selected, Gray = Not selected)',
                    fontsize=11, fontweight='bold')
        
        # Stats box
        selected_count = sum(bit_vector)
        ax.text(0.5, 1.3, f'Selected: {selected_count}/{n} items  |  '
                         f'Value: {result["total_value"]:.0f}  |  '
                         f'Weight: {result["total_weight"]:.0f}',
               ha='center', fontsize=9,
               bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
