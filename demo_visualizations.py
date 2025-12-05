"""
=================================================================================
DEMO ADVANCED VISUALIZATIONS
=================================================================================
Quick demo to test all visualization functions
Run this to verify charts work correctly before running full experiments
=================================================================================
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.test_case_loader import TestCaseLoader
from src.gbfs_knapsack import solve_gbfs
from src.bpso_knapsack import solve_bpso
from src.dp_knapsack import solve_dp
from src.advanced_visualizer import AdvancedKnapsackVisualizer


def demo_1_gbfs_parameters():
    """Demo GBFS parameter impact visualization"""
    print("\n" + "="*70)
    print("DEMO 1: GBFS Parameter Impact")
    print("="*70)
    
    loader = TestCaseLoader()
    visualizer = AdvancedKnapsackVisualizer()
    
    # Load test case
    test_case = loader.load_test_case('Size Medium 50')
    items = test_case['items']
    weights = test_case['weights']
    values = test_case['values']
    capacity = test_case['capacity']
    
    print(f"Test Case: Size Medium 50 ({len(items)} items)\n")
    
    # Test different max_states
    results = []
    for max_states in [1000, 2000, 3000, 5000]:
        print(f"Testing max_states = {max_states}...", end=" ")
        
        r = solve_gbfs(items, weights, values, capacity, max_states=max_states)
        
        results.append({
            'max_states': max_states,
            'value': r['total_value'],
            'value_std': 0,  # Demo: no variance
            'value_best': r['total_value'],
            'value_worst': r['total_value'],
            'time': r['execution_time'],
            'time_std': 0,
            'efficiency': r['total_value'] / r['execution_time']
        })
        
        print(f"Value={r['total_value']}, Time={r['execution_time']:.4f}s")
    
    df = pd.DataFrame(results)
    
    # Generate chart
    print("\nGenerating chart...")
    fig = visualizer.plot_gbfs_parameter_impact(df, save_path='demo_gbfs_params.png')
    print("✓ Saved: demo_gbfs_params.png")
    plt.close(fig)


def demo_2_bpso_parameters():
    """Demo BPSO parameter impact visualization"""
    print("\n" + "="*70)
    print("DEMO 2: BPSO Parameter Impact (Swarm Size)")
    print("="*70)
    
    loader = TestCaseLoader()
    visualizer = AdvancedKnapsackVisualizer()
    
    test_case = loader.load_test_case('Size Medium 50')
    items = test_case['items']
    weights = test_case['weights']
    values = test_case['values']
    capacity = test_case['capacity']
    
    print(f"Test Case: Size Medium 50\n")
    
    # Test different swarm sizes
    results = []
    for n_particles in [10, 20, 30]:
        print(f"Testing n_particles = {n_particles}...", end=" ")
        
        r = solve_bpso(items, weights, values, capacity, 
                      n_particles=n_particles, max_iterations=30)
        
        results.append({
            'param_value': n_particles,
            'value': r['total_value'],
            'value_std': 0,
            'time': r['execution_time'],
            'time_std': 0,
            'best_fitness_history': r.get('best_fitness_history', [])
        })
        
        print(f"Value={r['total_value']}, Time={r['execution_time']:.4f}s")
    
    df = pd.DataFrame(results)
    
    # Generate chart
    print("\nGenerating chart...")
    fig = visualizer.plot_bpso_parameter_impact(df, param_name='n_particles', 
                                                save_path='demo_bpso_swarm.png')
    print("✓ Saved: demo_bpso_swarm.png")
    plt.close(fig)


def demo_3_algorithm_comparison():
    """Demo algorithm comparison visualization"""
    print("\n" + "="*70)
    print("DEMO 3: Algorithm Comparison")
    print("="*70)
    
    loader = TestCaseLoader()
    visualizer = AdvancedKnapsackVisualizer()
    
    test_case = loader.load_test_case('Size Medium 50')
    items = test_case['items']
    weights = test_case['weights']
    values = test_case['values']
    capacity = test_case['capacity']
    
    print(f"Test Case: Size Medium 50\n")
    
    # GBFS
    print("Running GBFS...", end=" ")
    gbfs_result = solve_gbfs(items, weights, values, capacity, max_states=5000)
    print(f"Value={gbfs_result['total_value']}, Time={gbfs_result['execution_time']:.4f}s")
    
    # BPSO
    print("Running BPSO...", end=" ")
    bpso_result = solve_bpso(items, weights, values, capacity, 
                            n_particles=30, max_iterations=30)
    print(f"Value={bpso_result['total_value']}, Time={bpso_result['execution_time']:.4f}s")
    
    # DP
    print("Running DP...", end=" ")
    dp_result = solve_dp(items, weights, values, capacity)
    print(f"Value={dp_result['total_value']}, Time={dp_result['execution_time']:.4f}s")
    
    # Generate chart
    print("\nGenerating chart...")
    fig = visualizer.plot_algorithm_comparison_detailed(
        gbfs_result, bpso_result, dp_result, 
        save_path='demo_comparison.png'
    )
    print("✓ Saved: demo_comparison.png")
    plt.close(fig)


def demo_4_data_characteristics():
    """Demo data characteristics impact visualization"""
    print("\n" + "="*70)
    print("DEMO 4: Data Characteristics Impact")
    print("="*70)
    
    loader = TestCaseLoader()
    visualizer = AdvancedKnapsackVisualizer()
    
    # Test on different data characteristics
    test_cases = {
        'low_correlation': 'Data Low Correlation Medium',
        'high_correlation': 'Data High Correlation Medium',
    }
    
    results_dict = {}
    
    for char_name, test_name in test_cases.items():
        print(f"\n--- {char_name.upper()} ---")
        
        test_case = loader.load_test_case(test_name)
        items = test_case['items']
        weights = test_case['weights']
        values = test_case['values']
        capacity = test_case['capacity']
        
        # Run algorithms
        print("  GBFS...", end=" ")
        gbfs_r = solve_gbfs(items, weights, values, capacity, max_states=3000)
        print(f"{gbfs_r['total_value']}")
        
        print("  BPSO...", end=" ")
        bpso_r = solve_bpso(items, weights, values, capacity, n_particles=20, max_iterations=30)
        print(f"{bpso_r['total_value']}")
        
        print("  DP...", end=" ")
        dp_r = solve_dp(items, weights, values, capacity)
        print(f"{dp_r['total_value']}")
        
        results_dict[char_name] = {
            'gbfs': gbfs_r,
            'bpso': bpso_r,
            'dp': dp_r
        }
    
    # Generate chart
    print("\nGenerating chart...")
    fig = visualizer.plot_data_characteristics_impact(results_dict, 
                                                      save_path='demo_data_chars.png')
    print("✓ Saved: demo_data_chars.png")
    plt.close(fig)


def demo_5_solution_map():
    """Demo solution map visualization"""
    print("\n" + "="*70)
    print("DEMO 5: Solution Map Visualization")
    print("="*70)
    
    loader = TestCaseLoader()
    visualizer = AdvancedKnapsackVisualizer()
    
    test_case = loader.load_test_case('Region 3Regions Medium')
    items = test_case['items']
    weights = test_case['weights']
    values = test_case['values']
    capacity = test_case['capacity']
    
    print(f"Test Case: Region 3Regions Medium\n")
    
    # Run BPSO to get solution
    print("Running BPSO...", end=" ")
    result = solve_bpso(items, weights, values, capacity, n_particles=30, max_iterations=30)
    print(f"Value={result['total_value']}, Items={len(result['selected_items'])}")
    
    # Load full data with regions
    info = loader.get_test_case_info('Region 3Regions Medium')
    filepath = loader.test_cases_dir / info['File']
    items_df = pd.read_csv(filepath)
    items_df['name'] = [f"Item_{i+1}" for i in range(len(items_df))]
    items_df['weight'] = items_df['Quantity']
    items_df['value'] = items_df['Total']
    if 'Segment' in items_df.columns:
        items_df['region'] = items_df['Segment']
    
    # Add capacity to result
    result['capacity'] = capacity
    
    # Generate chart
    print("Generating chart...")
    fig = visualizer.plot_knapsack_solution_map(result, items_df, 
                                                save_path='demo_solution_map.png')
    print("✓ Saved: demo_solution_map.png")
    plt.close(fig)


def main():
    """Run all demos"""
    print("\n" + "="*80)
    print(" " * 25 + "VISUALIZATION DEMOS")
    print(" " * 20 + "Testing Advanced Visualizer")
    print("="*80)
    
    demos = [
        ("1. GBFS Parameters", demo_1_gbfs_parameters),
        ("2. BPSO Parameters", demo_2_bpso_parameters),
        ("3. Algorithm Comparison", demo_3_algorithm_comparison),
        ("4. Data Characteristics", demo_4_data_characteristics),
        ("5. Solution Map", demo_5_solution_map)
    ]
    
    for demo_name, demo_func in demos:
        try:
            demo_func()
        except Exception as e:
            print(f"\n❌ Error in {demo_name}: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*80)
    print("DEMO COMPLETED!")
    print("\nGenerated files:")
    print("  - demo_gbfs_params.png")
    print("  - demo_bpso_swarm.png")
    print("  - demo_comparison.png")
    print("  - demo_data_chars.png")
    print("  - demo_solution_map.png")
    print("="*80)


if __name__ == '__main__':
    main()
