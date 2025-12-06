"""
=================================================================================
CHƯƠNG 3: PHÂN TÍCH VÀ ĐÁNH GIÁ - Following GA_TSP Structure
=================================================================================
Tổ chức experiments theo structure:
3.1.1. Ảnh hưởng của tham số (Parameter Impact)
3.1.2. Ảnh hưởng của thuật toán (Algorithm Comparison) 
3.1.3. Ảnh hưởng của dữ liệu (Data Characteristics)

Mỗi experiment sinh ra:
- CSV data file
- Visualization charts (like GA_TSP)
=================================================================================
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import pandas as pd
import time
import json
from src.utils import TestCaseLoader
from src.algorithms import solve_knapsack_gbfs, solve_knapsack_bpso
from src.visualization import AdvancedKnapsackVisualizer


class Chapter3Experiments:
    """Quản lý experiments cho Chương """
    
    def __init__(self, output_dir='results/chapter3'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.loader = TestCaseLoader()
        self.visualizer = AdvancedKnapsackVisualizer()
    
    # =========================================================================
    # 3.1.1. ẢNH HƯỞNG CỦA THAM SỐ (Parameter Impact)
    # =========================================================================
    
    def experiment_3_1_1_a_gbfs_parameters(self):
        """
        Test GBFS với các max_states khác nhau
        
        """
        print("\n" + "="*70)
        print("3.1.1.a: GBFS PARAMETER ANALYSIS - Max States Impact")
        print("="*70)
        
        # Dùng Size Medium 50 làm test case chuẩn
        test_case = self.loader.load_test_case('Size Medium 50')
        items, weights, values, capacity = (
            test_case['items'], test_case['weights'], 
            test_case['values'], test_case['capacity']
        )
        
        print(f"\nTest Case: Size Medium 50")
        print(f"Items: {len(items)}, Capacity: {capacity}\n")
        
        results = []
        max_states_list = [1000, 2000, 3000, 5000, 7000, 10000]
        
        for max_states in max_states_list:
            print(f"Testing max_states = {max_states}...")
            
            # Run 5 times để có mean/std
            runs = []
            for run_id in range(5):
                # Reload test case mỗi lần để tránh mutation
                test_case_run = self.loader.load_test_case('Size Medium 50')
                result = solve_knapsack_gbfs(
                    test_case_run['items'], 
                    test_case_run['weights'], 
                    test_case_run['values'], 
                    test_case_run['capacity'],
                    regions=test_case_run.get('regions'),
                    max_states=max_states
                )
                runs.append(result)
                print(f"  Run {run_id+1}: Value={result['total_value']}, Time={result['execution_time']:.4f}s")
            
            # Aggregate results
            values = [r['total_value'] for r in runs]
            times = [r['execution_time'] for r in runs]
            
            results.append({
                'max_states': max_states,
                'value': np.mean(values),
                'value_std': np.std(values),
                'value_best': max(values),
                'value_worst': min(values),
                'time': np.mean(times),
                'time_std': np.std(times),
                'efficiency': np.mean(values) / np.mean(times)
            })
            
            print(f"  → Mean Value: {np.mean(values):.2f} ± {np.std(values):.2f}")
            print(f"  → Mean Time: {np.mean(times):.4f} ± {np.std(times):.4f}s\n")
        
        # Save CSV
        df = pd.DataFrame(results)
        csv_path = os.path.join(self.output_dir, '3_1_1_a_gbfs_params.csv')
        df.to_csv(csv_path, index=False)
        print(f"✓ Saved CSV: {csv_path}")
        
        # Generate visualization
        fig_path = os.path.join(self.output_dir, '3_1_1_a_gbfs_params.png')
        self.visualizer.plot_gbfs_parameter_impact(df, save_path=fig_path)
        print(f"✓ Saved Chart: {fig_path}")
        
        return df
    
    def experiment_3_1_1_b_bpso_swarm_size(self):
        """
        Test BPSO với các swarm size khác nhau
        
        """
        print("\n" + "="*70)
        print("3.1.1.b: BPSO PARAMETER ANALYSIS - Swarm Size Impact")
        print("="*70)
        
        test_case = self.loader.load_test_case('Size Medium 50')
        items, weights, values, capacity = (
            test_case['items'], test_case['weights'], 
            test_case['values'], test_case['capacity']
        )
        
        print(f"\nTest Case: Size Medium 50")
        print(f"Items: {len(items)}, Capacity: {capacity}\n")
        
        results = []
        swarm_sizes = [10, 20, 30, 50, 70, 100]
        
        for n_particles in swarm_sizes:
            print(f"Testing n_particles = {n_particles}...")
            
            runs = []
            for run_id in range(5):
                # Reload test case mỗi lần
                test_case_run = self.loader.load_test_case('Size Medium 50')
                result = solve_knapsack_bpso(
                    test_case_run['items'],
                    test_case_run['weights'],
                    test_case_run['values'],
                    test_case_run['capacity'],
                    n_particles=n_particles, max_iterations=50
                )
                runs.append(result)
                print(f"  Run {run_id+1}: Value={result['total_value']}, Time={result['execution_time']:.4f}s")
            
            # Aggregate
            values = [r['total_value'] for r in runs]
            times = [r['execution_time'] for r in runs]
            
            # Get best run's history for convergence plot
            best_run = max(runs, key=lambda x: x['total_value'])
            
            results.append({
                'param_value': n_particles,
                'value': np.mean(values),
                'value_std': np.std(values),
                'time': np.mean(times),
                'time_std': np.std(times),
                'best_fitness_history': best_run.get('best_fitness_history', [])
            })
            
            print(f"  → Mean Value: {np.mean(values):.2f} ± {np.std(values):.2f}")
            print(f"  → Mean Time: {np.mean(times):.4f}s\n")
        
        # Save CSV (without history column)
        df_save = pd.DataFrame([{k: v for k, v in r.items() if k != 'best_fitness_history'} 
                               for r in results])
        csv_path = os.path.join(self.output_dir, '3_1_1_b_bpso_swarm_size.csv')
        df_save.to_csv(csv_path, index=False)
        print(f"✓ Saved CSV: {csv_path}")
        
        # Save history to JSON for visualization
        history_data = {
            'experiment': '3_1_1_b_bpso_swarm_size',
            'param_name': 'n_particles',
            'results': [
                {
                    'param_value': r['param_value'],
                    'value': r['value'],
                    'best_fitness_history': r['best_fitness_history']
                }
                for r in results
            ]
        }
        json_path = os.path.join(self.output_dir, '3_1_1_b_bpso_swarm_size_history.json')
        with open(json_path, 'w') as f:
            json.dump(history_data, f, indent=2)
        print(f"✓ Saved History JSON: {json_path}")
        
        # Generate visualization
        df_plot = pd.DataFrame(results)
        fig_path = os.path.join(self.output_dir, '3_1_1_b_bpso_swarm_size.png')
        self.visualizer.plot_bpso_parameter_impact(df_plot, param_name='n_particles', save_path=fig_path)
        print(f"✓ Saved Chart: {fig_path}")
        
        return df_plot
    
    def experiment_3_1_1_c_bpso_iterations(self):
        """Test BPSO với các max_iterations khác nhau"""
        print("\n" + "="*70)
        print("3.1.1.c: BPSO PARAMETER ANALYSIS - Max Iterations Impact")
        print("="*70)
        
        test_case = self.loader.load_test_case('Size Medium 50')
        items, weights, values, capacity = (
            test_case['items'], test_case['weights'], 
            test_case['values'], test_case['capacity']
        )
        
        print(f"\nTest Case: Size Medium 50\n")
        
        results = []
        iterations_list = [20, 30, 50, 70, 100, 150]
        
        for max_iter in iterations_list:
            print(f"Testing max_iterations = {max_iter}...")
            
            runs = []
            for run_id in range(5):
                # Reload test case mỗi lần
                test_case_run = self.loader.load_test_case('Size Medium 50')
                result = solve_knapsack_bpso(
                    test_case_run['items'],
                    test_case_run['weights'],
                    test_case_run['values'],
                    test_case_run['capacity'],
                    regions=test_case_run.get('regions'),
                    n_particles=30, max_iterations=max_iter
                )
                runs.append(result)
            
            values = [r['total_value'] for r in runs]
            times = [r['execution_time'] for r in runs]
            best_run = max(runs, key=lambda x: x['total_value'])
            
            results.append({
                'param_value': max_iter,
                'value': np.mean(values),
                'value_std': np.std(values),
                'time': np.mean(times),
                'time_std': np.std(times),
                'best_fitness_history': best_run.get('best_fitness_history', [])
            })
            
            print(f"  → Mean Value: {np.mean(values):.2f}, Time: {np.mean(times):.4f}s\n")
        
        # Save CSV
        df_save = pd.DataFrame([{k: v for k, v in r.items() if k != 'best_fitness_history'} 
                               for r in results])
        csv_path = os.path.join(self.output_dir, '3_1_1_c_bpso_iterations.csv')
        df_save.to_csv(csv_path, index=False)
        print(f"✓ Saved CSV: {csv_path}")
        
        # Save history to JSON
        history_data = {
            'experiment': '3_1_1_c_bpso_iterations',
            'param_name': 'max_iterations',
            'results': [
                {
                    'param_value': r['param_value'],
                    'value': r['value'],
                    'best_fitness_history': r['best_fitness_history']
                }
                for r in results
            ]
        }
        json_path = os.path.join(self.output_dir, '3_1_1_c_bpso_iterations_history.json')
        with open(json_path, 'w') as f:
            json.dump(history_data, f, indent=2)
        print(f"✓ Saved History JSON: {json_path}")
        
        # Visualize
        df_plot = pd.DataFrame(results)
        fig_path = os.path.join(self.output_dir, '3_1_1_c_bpso_iterations.png')
        self.visualizer.plot_bpso_parameter_impact(df_plot, param_name='max_iterations', save_path=fig_path)
        print(f"✓ Saved Chart: {fig_path}")
        
        return df_plot
    
    def experiment_3_1_1_d_bpso_inertia_weight(self):
        """Test BPSO với các w (inertia weight) khác nhau"""
        print("\n" + "="*70)
        print("3.1.1.d: BPSO PARAMETER ANALYSIS - Inertia Weight (w) Impact")
        print("="*70)
        
        test_case = self.loader.load_test_case('Size Medium 50')
        items, weights, values, capacity, regions = (
            test_case['items'], test_case['weights'], 
            test_case['values'], test_case['capacity'],
            test_case.get('regions')
        )
        
        print(f"\nTest Case: Size Medium 50")
        print(f"Items: {len(items)}, Capacity: {capacity}\n")
        
        results = []
        w_values = [0.3, 0.5, 0.7, 0.9]
        
        for w in w_values:
            print(f"Testing w = {w}...")
            
            runs = []
            for run_id in range(5):
                # Reload để tránh mutation
                test_case_run = self.loader.load_test_case('Size Medium 50')
                result = solve_knapsack_bpso(
                    test_case_run['items'], test_case_run['weights'], 
                    test_case_run['values'], test_case_run['capacity'],
                    regions=test_case_run.get('regions'),
                    n_particles=30, max_iterations=50, w=w
                )
                runs.append(result)
            
            values = [r['total_value'] for r in runs]
            times = [r['execution_time'] for r in runs]
            best_run = max(runs, key=lambda x: x['total_value'])
            
            results.append({
                'param_value': w,
                'value': np.mean(values),
                'value_std': np.std(values),
                'time': np.mean(times),
                'time_std': np.std(times),
                'best_fitness_history': best_run.get('best_fitness_history', [])
            })
            
            print(f"  → Mean Value: {np.mean(values):.2f}, Time: {np.mean(times):.4f}s\n")
        
        # Save CSV
        df_save = pd.DataFrame([{k: v for k, v in r.items() if k != 'best_fitness_history'} 
                               for r in results])
        csv_path = os.path.join(self.output_dir, '3_1_1_d_bpso_w.csv')
        df_save.to_csv(csv_path, index=False)
        print(f"✓ Saved CSV: {csv_path}")
        
        # Save history to JSON
        history_data = {
            'experiment': '3_1_1_d_bpso_w',
            'param_name': 'w',
            'results': [
                {
                    'param_value': r['param_value'],
                    'value': r['value'],
                    'best_fitness_history': r['best_fitness_history']
                }
                for r in results
            ]
        }
        json_path = os.path.join(self.output_dir, '3_1_1_d_bpso_w_history.json')
        with open(json_path, 'w') as f:
            json.dump(history_data, f, indent=2)
        print(f"✓ Saved History JSON: {json_path}")
        
        # Visualize
        df_plot = pd.DataFrame(results)
        fig_path = os.path.join(self.output_dir, '3_1_1_d_bpso_w.png')
        self.visualizer.plot_bpso_parameter_impact(df_plot, param_name='w', save_path=fig_path)
        print(f"✓ Saved Chart: {fig_path}")
        
        return df_plot
    
    # =========================================================================
    # 3.1.2. ẢNH HƯỞNG CỦA THUẬT TOÁN (Algorithm Comparison)
    # =========================================================================
    
    def experiment_3_1_2_algorithm_comparison_single(self, test_case_name='Size Medium 50'):
        """
        So sánh chi tiết GBFS vs BPSO trên 1 test case
        Theo đúng yêu cầu đề tài: Chỉ 2 thuật toán (GBFS và BPSO)
        """
        print("\n" + "="*70)
        print(f"3.1.2: ALGORITHM COMPARISON - {test_case_name}")
        print("="*70)
        
        test_case = self.loader.load_test_case(test_case_name)
        items, weights, values, capacity = (
            test_case['items'], test_case['weights'],
            test_case['values'], test_case['capacity']
        )
        
        print(f"\nTest Case: {test_case_name}")
        print(f"Items: {len(items)}, Capacity: {capacity}\n")
        
        # GBFS - 5 runs
        print("Running GBFS (5 runs)...")
        gbfs_runs = []
        for i in range(5):
            r = solve_knapsack_gbfs(items, weights, values, capacity, max_states=5000)
            gbfs_runs.append(r)
            print(f"  Run {i+1}: Value={r['total_value']}, Time={r['execution_time']:.4f}s")
        
        gbfs_best = max(gbfs_runs, key=lambda x: x['total_value'])
        print(f"→ GBFS Best: {gbfs_best['total_value']}\n")
        
        # BPSO - 5 runs
        print("Running BPSO (5 runs)...")
        bpso_runs = []
        for i in range(5):
            r = solve_knapsack_bpso(items, weights, values, capacity, n_particles=30, max_iterations=50)
            bpso_runs.append(r)
            print(f"  Run {i+1}: Value={r['total_value']}, Time={r['execution_time']:.4f}s")
        
        bpso_best = max(bpso_runs, key=lambda x: x['total_value'])
        print(f"→ BPSO Best: {bpso_best['total_value']}\n")
        
        # Generate comparison visualization (GBFS vs BPSO only)
        fig_path = os.path.join(self.output_dir, f'3_1_2_comparison_{test_case_name.replace(" ", "_")}.png')
        self.visualizer.plot_algorithm_comparison_gbfs_bpso(
            gbfs_best, bpso_best, save_path=fig_path
        )
        print(f"✓ Saved Chart: {fig_path}")
        
        # Summary CSV (GBFS vs BPSO only)
        gbfs_mean = np.mean([r['total_value'] for r in gbfs_runs])
        bpso_mean = np.mean([r['total_value'] for r in bpso_runs])
        
        summary = {
            'algorithm': ['GBFS', 'BPSO'],
            'value_mean': [gbfs_mean, bpso_mean],
            'value_std': [
                np.std([r['total_value'] for r in gbfs_runs]),
                np.std([r['total_value'] for r in bpso_runs])
            ],
            'value_best': [gbfs_best['total_value'], bpso_best['total_value']],
            'time_mean': [
                np.mean([r['execution_time'] for r in gbfs_runs]),
                np.mean([r['execution_time'] for r in bpso_runs])
            ],
            'better_algorithm': 'GBFS' if gbfs_mean > bpso_mean else 'BPSO',
            'improvement_pct': abs((gbfs_mean - bpso_mean) / min(gbfs_mean, bpso_mean)) * 100
        }
        
        df = pd.DataFrame(summary)
        csv_path = os.path.join(self.output_dir, f'3_1_2_comparison_{test_case_name.replace(" ", "_")}.csv')
        df.to_csv(csv_path, index=False)
        print(f"✓ Saved CSV: {csv_path}\n")
        
        return df
    
    def experiment_3_1_2_algorithm_comparison_all(self):
        """So sánh trên tất cả 13 test cases"""
        print("\n" + "="*70)
        print("3.1.2: ALGORITHM COMPARISON - All 13 Test Cases")
        print("="*70)
        
        test_cases = self.loader.list_test_cases()
        results = []
        
        for test_name in test_cases:
            print(f"\n--- {test_name} ---")
            
            test_case = self.loader.load_test_case(test_name)
            items, weights, values, capacity = (
                test_case['items'], test_case['weights'],
                test_case['values'], test_case['capacity']
            )
            
            # GBFS
            gbfs_runs = [solve_knapsack_gbfs(items, weights, values, capacity, max_states=5000) 
                        for _ in range(3)]
            gbfs_values = [r['total_value'] for r in gbfs_runs]
            gbfs_times = [r['execution_time'] for r in gbfs_runs]
            
            # BPSO
            bpso_runs = [solve_knapsack_bpso(items, weights, values, capacity, n_particles=30, max_iterations=50) 
                        for _ in range(3)]
            bpso_values = [r['total_value'] for r in bpso_runs]
            bpso_times = [r['execution_time'] for r in bpso_runs]
            
            # Determine better algorithm
            gbfs_mean = np.mean(gbfs_values)
            bpso_mean = np.mean(bpso_values)
            better_algo = 'GBFS' if gbfs_mean > bpso_mean else 'BPSO'
            
            results.append({
                'test_case': test_name,
                'n_items': len(items),
                'capacity': capacity,
                'gbfs_value': gbfs_mean,
                'gbfs_value_std': np.std(gbfs_values),
                'gbfs_time': np.mean(gbfs_times),
                'bpso_value': bpso_mean,
                'bpso_value_std': np.std(bpso_values),
                'bpso_time': np.mean(bpso_times),
                'better_algorithm': better_algo,
                'improvement_pct': abs((gbfs_mean - bpso_mean) / min(gbfs_mean, bpso_mean)) * 100
            })
            
            print(f"  GBFS: {gbfs_mean:.1f} ± {np.std(gbfs_values):.1f}")
            print(f"  BPSO: {bpso_mean:.1f} ± {np.std(bpso_values):.1f}")
            print(f"  → Better: {better_algo}")
        
        df = pd.DataFrame(results)
        csv_path = os.path.join(self.output_dir, '3_1_2_comparison_all_testcases.csv')
        df.to_csv(csv_path, index=False)
        print(f"\n✓ Saved CSV: {csv_path}")
        
        return df
    
    # =========================================================================
    # 3.1.3. ẢNH HƯỞNG CỦA DỮ LIỆU (Data Characteristics Impact)
    # =========================================================================
    
    def experiment_3_1_3_data_characteristics(self):
        """
        Test ảnh hưởng của đặc điểm dữ liệu:
        - Low correlation vs High correlation
        - High value spread
        - Regional diversity (1 region vs 3 regions)
        """
        print("\n" + "="*70)
        print("3.1.3: DATA CHARACTERISTICS IMPACT ANALYSIS")
        print("="*70)
        
        # Test cases for each characteristic
        test_groups = {
            'low_correlation': 'Data Low Correlation Medium',
            'high_correlation': 'Data High Correlation Medium',
            'high_value': 'Data High Value Medium',
            'region_1': 'Region 1Regions Medium',
            'region_3': 'Region 3Regions Medium'
        }
        
        results_dict = {}
        summary_list = []
        
        for group_name, test_name in test_groups.items():
            print(f"\n--- {group_name.upper()}: {test_name} ---")
            
            test_case = self.loader.load_test_case(test_name)
            items, weights, values, capacity = (
                test_case['items'], test_case['weights'],
                test_case['values'], test_case['capacity']
            )
            
            # Run all 3 algorithms (3 runs each for GBFS/BPSO)
            print("  GBFS...", end=" ")
            gbfs_runs = [solve_knapsack_gbfs(items, weights, values, capacity, max_states=5000) 
                        for _ in range(3)]
            gbfs_values = [r['total_value'] for r in gbfs_runs]
            gbfs_times = [r['execution_time'] for r in gbfs_runs]
            gbfs_best = max(gbfs_runs, key=lambda x: x['total_value'])
            print(f"Mean={np.mean(gbfs_values):.1f}")
            
            print("  BPSO...", end=" ")
            bpso_runs = [solve_knapsack_bpso(items, weights, values, capacity, n_particles=30, max_iterations=50) 
                        for _ in range(3)]
            bpso_values = [r['total_value'] for r in bpso_runs]
            bpso_times = [r['execution_time'] for r in bpso_runs]
            bpso_best = max(bpso_runs, key=lambda x: x['total_value'])
            print(f"Mean={np.mean(bpso_values):.1f}")
            
            # Store for visualization (GBFS vs BPSO only)
            results_dict[group_name] = {
                'gbfs': gbfs_best,
                'bpso': bpso_best
            }
            
            # Determine better algorithm
            gbfs_mean = np.mean(gbfs_values)
            bpso_mean = np.mean(bpso_values)
            
            # Add to summary
            summary_list.append({
                'characteristic': group_name,
                'test_case': test_name,
                'gbfs_value': gbfs_mean,
                'gbfs_time': np.mean(gbfs_times),
                'bpso_value': bpso_mean,
                'bpso_time': np.mean(bpso_times),
                'better_algorithm': 'GBFS' if gbfs_mean > bpso_mean else 'BPSO',
                'improvement_pct': abs((gbfs_mean - bpso_mean) / min(gbfs_mean, bpso_mean)) * 100
            })
        
        # Save CSV
        df = pd.DataFrame(summary_list)
        csv_path = os.path.join(self.output_dir, '3_1_3_data_characteristics.csv')
        df.to_csv(csv_path, index=False)
        print(f"\n✓ Saved CSV: {csv_path}")
        
        # Generate visualization
        fig_path = os.path.join(self.output_dir, '3_1_3_data_characteristics.png')
        self.visualizer.plot_data_characteristics_impact(results_dict, save_path=fig_path)
        print(f"✓ Saved Chart: {fig_path}\n")
        
        return df
    
    # =========================================================================
    # RUN ALL EXPERIMENTS
    # =========================================================================
    
    def run_all_experiments(self):
        """Chạy tất cả experiments cho Chapter 3"""
        print("\n" + "="*80)
        print(" " * 20 + "CHƯƠNG 3: PHÂN TÍCH VÀ ĐÁNH GIÁ")
        print(" " * 15 + "Knapsack Problem - Learning from GA_TSP")
        print("="*80)
        
        experiments = [
            ("3.1.1.a", "GBFS Parameters", self.experiment_3_1_1_a_gbfs_parameters),
            ("3.1.1.b", "BPSO Swarm Size", self.experiment_3_1_1_b_bpso_swarm_size),
            ("3.1.1.c", "BPSO Iterations", self.experiment_3_1_1_c_bpso_iterations),
            ("3.1.1.d", "BPSO Inertia Weight", self.experiment_3_1_1_d_bpso_inertia_weight),
            ("3.1.2", "Algorithm Comparison (Single)", lambda: self.experiment_3_1_2_algorithm_comparison_single('Size Medium 50')),
            ("3.1.2", "Algorithm Comparison (All)", self.experiment_3_1_2_algorithm_comparison_all),
            ("3.1.3", "Data Characteristics", self.experiment_3_1_3_data_characteristics)
        ]
        
        for exp_id, exp_name, exp_func in experiments:
            try:
                print(f"\n{'='*70}")
                print(f"Starting: [{exp_id}] {exp_name}")
                print(f"{'='*70}")
                
                exp_func()
                
                print(f"\n✅ Completed: [{exp_id}] {exp_name}")
            except Exception as e:
                print(f"\n❌ Error in [{exp_id}] {exp_name}: {str(e)}")
                import traceback
                traceback.print_exc()
        
        print("\n" + "="*80)
        print("ALL EXPERIMENTS COMPLETED!")
        print(f"Results saved to: {self.output_dir}/")
        print("="*80)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Chapter 3 Experiments - Following GA_TSP')
    parser.add_argument('--experiment', type=str, default='all',
                       help='Experiment to run: all, 3.1.1a, 3.1.1b, 3.1.1c, 3.1.1d, 3.1.2, 3.1.3')
    
    args = parser.parse_args()
    
    exp_runner = Chapter3Experiments()
    
    if args.experiment == 'all':
        exp_runner.run_all_experiments()
    elif args.experiment == '3.1.1a':
        exp_runner.experiment_3_1_1_a_gbfs_parameters()
    elif args.experiment == '3.1.1b':
        exp_runner.experiment_3_1_1_b_bpso_swarm_size()
    elif args.experiment == '3.1.1c':
        exp_runner.experiment_3_1_1_c_bpso_iterations()
    elif args.experiment == '3.1.1d':
        exp_runner.experiment_3_1_1_d_bpso_inertia_weight()
    elif args.experiment == '3.1.2':
        exp_runner.experiment_3_1_2_algorithm_comparison_single()
        exp_runner.experiment_3_1_2_algorithm_comparison_all()
    elif args.experiment == '3.1.3':
        exp_runner.experiment_3_1_3_data_characteristics()
    else:
        print(f"Unknown experiment: {args.experiment}")
        print("Available: all, 3.1.1a, 3.1.1b, 3.1.1c, 3.1.1d, 3.1.2, 3.1.3")


if __name__ == '__main__':
    main()
