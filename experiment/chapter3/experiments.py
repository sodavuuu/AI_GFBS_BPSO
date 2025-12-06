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
from src.utils import TestCaseLoader
from src.algorithms import solve_knapsack_gbfs, solve_knapsack_bpso, solve_knapsack_dp
from src.visualization import AdvancedKnapsackVisualizer


class Chapter3Experiments:
    """Quản lý experiments cho Chương 3 - Theo phong cách GA_TSP"""
    
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
        Tương tự GA_TSP test population size impact
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
        print(f"Vật phẩm: {len(items)}, Sức chứa: {capacity}\n")
        
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
                    max_states=max_states
                )
                runs.append(result)
                print(f"  Chạy {run_id+1}: Giá trị={result['total_value']}, Time={result['execution_time']:.4f}s")
            
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
            
            print(f"  → Trung bình Giá trị: {np.mean(values):.2f} ± {np.std(values):.2f}")
            print(f"  → Trung bình Time: {np.mean(times):.4f} ± {np.std(times):.4f}s\n")
        
        # Save CSV
        df = pd.DataFrame(results)
        csv_path = os.path.join(self.output_dir, '3_1_1_a_gbfs_params.csv')
        df.to_csv(csv_path, index=False)
        print(f"✓ Đã lưu CSV: {csv_path}")
        
        # Generate visualization
        fig_path = os.path.join(self.output_dir, '3_1_1_a_gbfs_params.png')
        self.visualizer.plot_gbfs_parameter_impact(df, save_path=fig_path)
        print(f"✓ Đã lưu Chart: {fig_path}")
        
        return df
    
    def experiment_3_1_1_b_bpso_swarm_size(self):
        """
        Test BPSO với các swarm size khác nhau
        Tương tự GA_TSP test population size
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
        print(f"Vật phẩm: {len(items)}, Sức chứa: {capacity}\n")
        
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
                print(f"  Chạy {run_id+1}: Giá trị={result['total_value']}, Time={result['execution_time']:.4f}s")
            
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
            
            print(f"  → Trung bình Giá trị: {np.mean(values):.2f} ± {np.std(values):.2f}")
            print(f"  → Trung bình Time: {np.mean(times):.4f}s\n")
        
        # Save CSV (without history column)
        df_save = pd.DataFrame([{k: v for k, v in r.items() if k != 'best_fitness_history'} 
                               for r in results])
        csv_path = os.path.join(self.output_dir, '3_1_1_b_bpso_swarm_size.csv')
        df_save.to_csv(csv_path, index=False)
        print(f"✓ Đã lưu CSV: {csv_path}")
        
        # Generate visualization
        df_plot = pd.DataFrame(results)
        fig_path = os.path.join(self.output_dir, '3_1_1_b_bpso_swarm_size.png')
        self.visualizer.plot_bpso_parameter_impact(df_plot, param_name='n_particles', save_path=fig_path)
        print(f"✓ Đã lưu Chart: {fig_path}")
        
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
            
            print(f"  → Trung bình Giá trị: {np.mean(values):.2f}, Time: {np.mean(times):.4f}s\n")
        
        # Save
        df_save = pd.DataFrame([{k: v for k, v in r.items() if k != 'best_fitness_history'} 
                               for r in results])
        csv_path = os.path.join(self.output_dir, '3_1_1_c_bpso_iterations.csv')
        df_save.to_csv(csv_path, index=False)
        print(f"✓ Đã lưu CSV: {csv_path}")
        
        # Visualize
        df_plot = pd.DataFrame(results)
        fig_path = os.path.join(self.output_dir, '3_1_1_c_bpso_iterations.png')
        self.visualizer.plot_bpso_parameter_impact(df_plot, param_name='max_iterations', save_path=fig_path)
        print(f"✓ Đã lưu Chart: {fig_path}")
        
        return df_plot
    
    def experiment_3_1_1_d_bpso_inertia_weight(self):
        """Test BPSO với các w (inertia weight) khác nhau"""
        print("\n" + "="*70)
        print("3.1.1.d: BPSO PARAMETER ANALYSIS - Inertia Weight (w) Impact")
        print("="*70)
        
        test_case = self.loader.load_test_case('Size Medium 50')
        items, weights, values, capacity = (
            test_case['items'], test_case['weights'], 
            test_case['values'], test_case['capacity']
        )
        
        print(f"\nTest Case: Size Medium 50\n")
        
        results = []
        w_values = [0.3, 0.5, 0.7, 0.9]
        
        for w in w_values:
            print(f"Testing w = {w}...")
            
            runs = []
            for run_id in range(5):
                result = solve_knapsack_bpso(items, weights, values, capacity, 
                                   n_particles=30, max_iterations=50, w=w)
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
            
            print(f"  → Trung bình Giá trị: {np.mean(values):.2f}\n")
        
        # Save
        df_save = pd.DataFrame([{k: v for k, v in r.items() if k != 'best_fitness_history'} 
                               for r in results])
        csv_path = os.path.join(self.output_dir, '3_1_1_d_bpso_w.csv')
        df_save.to_csv(csv_path, index=False)
        print(f"✓ Đã lưu CSV: {csv_path}")
        
        # Visualize
        df_plot = pd.DataFrame(results)
        fig_path = os.path.join(self.output_dir, '3_1_1_d_bpso_w.png')
        self.visualizer.plot_bpso_parameter_impact(df_plot, param_name='w', save_path=fig_path)
        print(f"✓ Đã lưu Chart: {fig_path}")
        
        return df_plot
    
    # =========================================================================
    # 3.1.2. ẢNH HƯỞNG CỦA THUẬT TOÁN (Algorithm Comparison)
    # =========================================================================
    
    def experiment_3_1_2_algorithm_comparison_single(self, test_case_name='Size Medium 50'):
        """
        So sánh chi tiết GBFS vs BPSO vs DP trên 1 test case
        Tương tự GA_TSP so sánh mutations/crossovers
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
        print(f"Vật phẩm: {len(items)}, Sức chứa: {capacity}\n")
        
        # GBFS - 5 runs
        print("Running GBFS (5 runs)...")
        gbfs_runs = []
        for i in range(5):
            r = solve_knapsack_gbfs(items, weights, values, capacity, max_states=5000)
            gbfs_runs.append(r)
            print(f"  Chạy {i+1}: Giá trị={r['total_value']}, Time={r['execution_time']:.4f}s")
        
        gbfs_best = max(gbfs_runs, key=lambda x: x['total_value'])
        print(f"→ GBFS Tốt nhất: {gbfs_best['total_value']}\n")
        
        # BPSO - 5 runs
        print("Running BPSO (5 runs)...")
        bpso_runs = []
        for i in range(5):
            r = solve_knapsack_bpso(items, weights, values, capacity, n_particles=30, max_iterations=50)
            bpso_runs.append(r)
            print(f"  Chạy {i+1}: Giá trị={r['total_value']}, Time={r['execution_time']:.4f}s")
        
        bpso_best = max(bpso_runs, key=lambda x: x['total_value'])
        print(f"→ BPSO Tốt nhất: {bpso_best['total_value']}\n")
        
        # DP - 1 run (deterministic)
        print("Running DP...")
        dp_result = solve_knapsack_dp(items, weights, values, capacity)
        print(f"  DP: Giá trị={dp_result['total_value']}, Time={dp_result['execution_time']:.4f}s")
        print(f"→ DP (Tối ưu): {dp_result['total_value']}\n")
        
        # Generate comparison visualization
        fig_path = os.path.join(self.output_dir, f'3_1_2_comparison_{test_case_name.replace(" ", "_")}.png')
        self.visualizer.plot_algorithm_comparison_detailed(
            gbfs_best, bpso_best, dp_result, save_path=fig_path
        )
        print(f"✓ Đã lưu Chart: {fig_path}")
        
        # Summary CSV
        summary = {
            'algorithm': ['GBFS', 'BPSO', 'DP'],
            'value_mean': [
                np.mean([r['total_value'] for r in gbfs_runs]),
                np.mean([r['total_value'] for r in bpso_runs]),
                dp_result['total_value']
            ],
            'value_std': [
                np.std([r['total_value'] for r in gbfs_runs]),
                np.std([r['total_value'] for r in bpso_runs]),
                0
            ],
            'time_mean': [
                np.mean([r['execution_time'] for r in gbfs_runs]),
                np.mean([r['execution_time'] for r in bpso_runs]),
                dp_result['execution_time']
            ],
            'pct_optimal': [
                (np.mean([r['total_value'] for r in gbfs_runs]) / dp_result['total_value']) * 100,
                (np.mean([r['total_value'] for r in bpso_runs]) / dp_result['total_value']) * 100,
                100.0
            ]
        }
        
        df = pd.DataFrame(summary)
        csv_path = os.path.join(self.output_dir, f'3_1_2_comparison_{test_case_name.replace(" ", "_")}.csv')
        df.to_csv(csv_path, index=False)
        print(f"✓ Đã lưu CSV: {csv_path}\n")
        
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
            
            # DP
            dp_r = solve_knapsack_dp(items, weights, values, capacity)
            
            results.append({
                'test_case': test_name,
                'n_items': len(items),
                'capacity': capacity,
                'gbfs_value': np.mean(gbfs_values),
                'gbfs_time': np.mean(gbfs_times),
                'bpso_value': np.mean(bpso_values),
                'bpso_time': np.mean(bpso_times),
                'dp_value': dp_r['total_value'],
                'dp_time': dp_r['execution_time'],
                'gbfs_pct_optimal': (np.mean(gbfs_values) / dp_r['total_value']) * 100,
                'bpso_pct_optimal': (np.mean(bpso_values) / dp_r['total_value']) * 100
            })
            
            print(f"  GBFS: {np.mean(gbfs_values):.1f} ({(np.mean(gbfs_values)/dp_r['total_value'])*100:.1f}%)")
            print(f"  BPSO: {np.mean(bpso_values):.1f} ({(np.mean(bpso_values)/dp_r['total_value'])*100:.1f}%)")
            print(f"  DP:   {dp_r['total_value']:.1f} (100%)")
        
        df = pd.DataFrame(results)
        csv_path = os.path.join(self.output_dir, '3_1_2_comparison_all_testcases.csv')
        df.to_csv(csv_path, index=False)
        print(f"\n✓ Đã lưu CSV: {csv_path}")
        
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
            print(f"Trung bình={np.mean(gbfs_values):.1f}")
            
            print("  BPSO...", end=" ")
            bpso_runs = [solve_knapsack_bpso(items, weights, values, capacity, n_particles=30, max_iterations=50) 
                        for _ in range(3)]
            bpso_values = [r['total_value'] for r in bpso_runs]
            bpso_times = [r['execution_time'] for r in bpso_runs]
            bpso_best = max(bpso_runs, key=lambda x: x['total_value'])
            print(f"Trung bình={np.mean(bpso_values):.1f}")
            
            print("  DP...", end=" ")
            dp_r = solve_knapsack_dp(items, weights, values, capacity)
            print(f"Giá trị={dp_r['total_value']}")
            
            # Store for visualization
            results_dict[group_name] = {
                'gbfs': gbfs_best,
                'bpso': bpso_best,
                'dp': dp_r
            }
            
            # Add to summary
            summary_list.append({
                'characteristic': group_name,
                'test_case': test_name,
                'gbfs_value': np.mean(gbfs_values),
                'gbfs_time': np.mean(gbfs_times),
                'bpso_value': np.mean(bpso_values),
                'bpso_time': np.mean(bpso_times),
                'dp_value': dp_r['total_value'],
                'dp_time': dp_r['execution_time'],
                'gbfs_pct_optimal': (np.mean(gbfs_values) / dp_r['total_value']) * 100,
                'bpso_pct_optimal': (np.mean(bpso_values) / dp_r['total_value']) * 100
            })
        
        # Save CSV
        df = pd.DataFrame(summary_list)
        csv_path = os.path.join(self.output_dir, '3_1_3_data_characteristics.csv')
        df.to_csv(csv_path, index=False)
        print(f"\n✓ Đã lưu CSV: {csv_path}")
        
        # Generate visualization
        fig_path = os.path.join(self.output_dir, '3_1_3_data_characteristics.png')
        self.visualizer.plot_data_characteristics_impact(results_dict, save_path=fig_path)
        print(f"✓ Đã lưu Chart: {fig_path}\n")
        
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
            ("3.1.3", "Đặc điểm dữ liệu", self.experiment_3_1_3_data_characteristics)
        ]
        
        for exp_id, exp_name, exp_func in experiments:
            try:
                print(f"\n{'='*70}")
                print(f"Starting: [{exp_id}] {exp_name}")
                print(f"{'='*70}")
                
                exp_func()
                
                print(f"\n✅ Completed: [{exp_id}] {exp_name}")
            except Exception as e:
                print(f"\n❌ Lỗi in [{exp_id}] {exp_name}: {str(e)}")
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
