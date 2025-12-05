"""
=================================================================================
CHƯƠNG 3: THỰC NGHIỆM CHI TIẾT  
=================================================================================
Experiments with 13 test cases (70 items each)
=================================================================================
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import pandas as pd
import time
from src.test_case_loader import TestCaseLoader
from src.gbfs_knapsack import solve_gbfs
from src.bpso_knapsack import solve_bpso
from src.dp_knapsack import solve_dp


class Chapter3Experiments:
    """Quản lý tất cả experiments cho Chương 3"""
    
    def __init__(self, output_dir='results/chapter3'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.loader = TestCaseLoader()
    
    # =========================================================================
    # 3.1.1. ẢNH HƯỞNG CỦA THAM SỐ
    # =========================================================================
    
    def experiment_3_1_1_gbfs_parameters(self):
        """Test GBFS với các max_states khác nhau"""
        print("\n" + "="*70)
        print("3.1.1.a: GBFS PARAMETERS")
        print("="*70)
        
        # Dùng size_medium_50 (50 items - test case CHÍNH)
        test_case = self.loader.load_test_case('Size Medium 50')
        items, weights, values, capacity = (
            test_case['items'], test_case['weights'], 
            test_case['values'], test_case['capacity']
        )
        
        print(f"\nTest: Size_Medium_50")
        print(f"Items: {len(items)}, Capacity: {capacity}\n")
        
        results = []
        max_states_values = [1000, 3000, 5000, 10000]
        
        for max_states in max_states_values:
            print(f"Max states: {max_states}")
            runs = []
            for _ in range(3):  # 3 runs
                r = solve_gbfs(items, weights, values, capacity, max_states=max_states)
                runs.append(r)
            
            values_list = [r['total_value'] for r in runs]
            times = [r['execution_time'] for r in runs]
            
            results.append({
                'max_states': max_states,
                'best': max(values_list),
                'mean': np.mean(values_list),
                'std': np.std(values_list),
                'time_mean': np.mean(times),
                'time_std': np.std(times)
            })
            
            print(f"  Best={max(values_list)}, Mean={np.mean(values_list):.1f}, Time={np.mean(times):.2f}s\n")
        
        df = pd.DataFrame(results)
        csv_path = os.path.join(self.output_dir, '3_1_1_a_gbfs_params.csv')
        df.to_csv(csv_path, index=False)
        print(f"✓ Saved: {csv_path}")
        return df
    
    def experiment_3_1_1_bpso_parameters(self):
        """Test BPSO với các parameters khác nhau"""
        print("\n" + "="*70)
        print("3.1.1.b: BPSO PARAMETERS")
        print("="*70)
        
        test_case = self.loader.load_test_case('Size_Medium_50')
        items, weights, values, capacity = (
            test_case['items'], test_case['weights'],
            test_case['values'], test_case['capacity']
        )
        
        print(f"\nTest: Size_Medium_50")
        print(f"Items: {len(items)}, Capacity: {capacity}\n")
        
        results = []
        
        # Test swarm size
        print("--- Swarm Size ---")
        for n_particles in [10, 20, 30, 50]:
            print(f"n_particles: {n_particles}")
            runs = []
            for _ in range(3):
                r = solve_bpso(items, weights, values, capacity, 
                             n_particles=n_particles, max_iterations=50)
                runs.append(r)
            
            values_list = [r['total_value'] for r in runs]
            times = [r['execution_time'] for r in runs]
            
            results.append({
                'parameter': 'n_particles',
                'value': n_particles,
                'best': max(values_list),
                'mean': np.mean(values_list),
                'std': np.std(values_list),
                'time_mean': np.mean(times),
                'time_std': np.std(times)
            })
            
            print(f"  Best={max(values_list)}, Mean={np.mean(values_list):.1f}, Time={np.mean(times):.3f}s\n")
        
        # Test iterations
        print("--- Max Iterations ---")
        for max_iter in [30, 50, 100, 150]:
            print(f"max_iterations: {max_iter}")
            runs = []
            for _ in range(3):
                r = solve_bpso(items, weights, values, capacity,
                             n_particles=20, max_iterations=max_iter)
                runs.append(r)
            
            values_list = [r['total_value'] for r in runs]
            times = [r['execution_time'] for r in runs]
            
            results.append({
                'parameter': 'max_iterations',
                'value': max_iter,
                'best': max(values_list),
                'mean': np.mean(values_list),
                'std': np.std(values_list),
                'time_mean': np.mean(times),
                'time_std': np.std(times)
            })
            
            print(f"  Best={max(values_list)}, Mean={np.mean(values_list):.1f}, Time={np.mean(times):.3f}s\n")
        
        df = pd.DataFrame(results)
        csv_path = os.path.join(self.output_dir, '3_1_1_b_bpso_params.csv')
        df.to_csv(csv_path, index=False)
        print(f"✓ Saved: {csv_path}")
        return df
    
    # =========================================================================
    # 3.1.2. SO SÁNH THUẬT TOÁN
    # =========================================================================
    
    def experiment_3_1_2_algorithm_comparison(self):
        """So sánh GBFS vs BPSO vs DP trên tất cả 13 test cases"""
        print("\n" + "="*70)
        print("3.1.2: ALGORITHM COMPARISON (13 test cases)")
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
            
            print(f"Items: {len(items)}, Capacity: {capacity}")
            
            # GBFS (3 runs)
            print("  GBFS...", end=" ")
            gbfs_runs = []
            for _ in range(3):
                r = solve_gbfs(items, weights, values, capacity, max_states=5000)
                gbfs_runs.append(r)
            gbfs_values = [r['total_value'] for r in gbfs_runs]
            gbfs_times = [r['execution_time'] for r in gbfs_runs]
            print(f"Best={max(gbfs_values)}, Mean={np.mean(gbfs_values):.1f}")
            
            # BPSO (3 runs)
            print("  BPSO...", end=" ")
            bpso_runs = []
            for _ in range(3):
                r = solve_bpso(items, weights, values, capacity, n_particles=20, max_iterations=50)
                bpso_runs.append(r)
            bpso_values = [r['total_value'] for r in bpso_runs]
            bpso_times = [r['execution_time'] for r in bpso_runs]
            print(f"Best={max(bpso_values)}, Mean={np.mean(bpso_values):.1f}")
            
            # DP (với 70 items, DP chạy được)
            print("  DP...", end=" ")
            dp_r = solve_dp(items, weights, values, capacity)
            dp_value = dp_r['total_value']
            dp_time = dp_r['execution_time']
            print(f"Optimal={dp_value}")
            
            # Calculate gaps
            gbfs_gap = (dp_value - np.mean(gbfs_values)) / dp_value * 100
            bpso_gap = (dp_value - np.mean(bpso_values)) / dp_value * 100
            
            results.append({
                'test_case': test_name,
                'n_items': len(items),
                'capacity': capacity,
                'gbfs_best': max(gbfs_values),
                'gbfs_mean': np.mean(gbfs_values),
                'gbfs_std': np.std(gbfs_values),
                'gbfs_time': np.mean(gbfs_times),
                'bpso_best': max(bpso_values),
                'bpso_mean': np.mean(bpso_values),
                'bpso_std': np.std(bpso_values),
                'bpso_time': np.mean(bpso_times),
                'dp_optimal': dp_value,
                'dp_time': dp_time,
                'gbfs_gap_percent': gbfs_gap,
                'bpso_gap_percent': bpso_gap
            })
        
        df = pd.DataFrame(results)
        csv_path = os.path.join(self.output_dir, '3_1_2_algorithm_comparison.csv')
        df.to_csv(csv_path, index=False)
        print(f"\n✓ Saved: {csv_path}")
        
        # Print summary
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        print(f"Average GBFS gap: {df['gbfs_gap_percent'].mean():.2f}%")
        print(f"Average BPSO gap: {df['bpso_gap_percent'].mean():.2f}%")
        print(f"Average GBFS time: {df['gbfs_time'].mean():.2f}s")
        print(f"Average BPSO time: {df['bpso_time'].mean():.3f}s")
        
        return df
    
    # =========================================================================
    # 3.1.3. ẢNH HƯỞNG CỦA DỮ LIỆU
    # =========================================================================
    
    def experiment_3_1_3_data_characteristics(self):
        """Test ảnh hưởng của đặc điểm data: correlation, regions, categories"""
        print("\n" + "="*70)
        print("3.1.3: DATA CHARACTERISTICS")
        print("="*70)
        
        results = []
        
        # Test 1: Regional Diversity (f₂)
        print("\n--- Test 1: Regional Diversity (f₂ = 1, 2, 3, 4) ---")
        regional_tests = [
            'Region 1Regions Medium',  # f₂=1
            'Region 2Regions Medium',  # f₂=2
            'Region 3Regions Medium',  # f₂=3
            'Size Medium 50'  # f₂=4 (test case CHÍNH)
        ]
        
        for test_name in regional_tests:
            test_case = self.loader.load_test_case(test_name)
            items, weights, values, capacity = (
                test_case['items'], test_case['weights'],
                test_case['values'], test_case['capacity']
            )
            n_regions = test_case['metadata']['N_Regions']
            
            print(f"\n{test_name} (f₂={n_regions})")
            
            gbfs_r = solve_gbfs(items, weights, values, capacity, max_states=5000)
            bpso_r = solve_bpso(items, weights, values, capacity, n_particles=20, max_iterations=50)
            dp_r = solve_dp(items, weights, values, capacity)
            
            results.append({
                'characteristic': 'regional_diversity',
                'test_case': test_name,
                'n_regions': n_regions,
                'gbfs_value': gbfs_r['total_value'],
                'gbfs_time': gbfs_r['execution_time'],
                'bpso_value': bpso_r['total_value'],
                'bpso_time': bpso_r['execution_time'],
                'dp_optimal': dp_r['total_value'],
                'dp_time': dp_r['execution_time'],
                'gbfs_gap': (dp_r['total_value'] - gbfs_r['total_value']) / dp_r['total_value'] * 100,
                'bpso_gap': (dp_r['total_value'] - bpso_r['total_value']) / dp_r['total_value'] * 100
            })
            
            print(f"  GBFS={gbfs_r['total_value']}, BPSO={bpso_r['total_value']}, DP={dp_r['total_value']}")
        
        # Test 2: Correlation
        print("\n--- Test 2: Correlation (v,w) ---")
        corr_tests = [
            'Data Low Correlation Medium',   # corr ≈ 0.09
            'Data High Correlation Medium'   # corr ≈ 0.11
        ]
        
        for test_name in corr_tests:
            test_case = self.loader.load_test_case(test_name)
            items, weights, values, capacity = (
                test_case['items'], test_case['weights'],
                test_case['values'], test_case['capacity']
            )
            corr = test_case['metadata']['Correlation_VW']
            
            print(f"\n{test_name} (corr={corr:.3f})")
            
            gbfs_r = solve_gbfs(items, weights, values, capacity, max_states=5000)
            bpso_r = solve_bpso(items, weights, values, capacity, n_particles=20, max_iterations=50)
            dp_r = solve_dp(items, weights, values, capacity)
            
            results.append({
                'characteristic': 'correlation',
                'test_case': test_name,
                'correlation': corr,
                'gbfs_value': gbfs_r['total_value'],
                'gbfs_time': gbfs_r['execution_time'],
                'bpso_value': bpso_r['total_value'],
                'bpso_time': bpso_r['execution_time'],
                'dp_optimal': dp_r['total_value'],
                'dp_time': dp_r['execution_time'],
                'gbfs_gap': (dp_r['total_value'] - gbfs_r['total_value']) / dp_r['total_value'] * 100,
                'bpso_gap': (dp_r['total_value'] - bpso_r['total_value']) / dp_r['total_value'] * 100
            })
            
            print(f"  GBFS={gbfs_r['total_value']}, BPSO={bpso_r['total_value']}, DP={dp_r['total_value']}")
        
        # Test 3: Categories
        print("\n--- Test 3: Categories ---")
        category_tests = [
            'Category Clothing Medium',
            'Category Electronics Medium',
            'Category Food Medium',
            'Category Furniture Medium'
        ]
        
        for test_name in category_tests:
            test_case = self.loader.load_test_case(test_name)
            items, weights, values, capacity = (
                test_case['items'], test_case['weights'],
                test_case['values'], test_case['capacity']
            )
            
            print(f"\n{test_name}")
            
            gbfs_r = solve_gbfs(items, weights, values, capacity, max_states=5000)
            bpso_r = solve_bpso(items, weights, values, capacity, n_particles=20, max_iterations=50)
            dp_r = solve_dp(items, weights, values, capacity)
            
            results.append({
                'characteristic': 'category',
                'test_case': test_name,
                'gbfs_value': gbfs_r['total_value'],
                'gbfs_time': gbfs_r['execution_time'],
                'bpso_value': bpso_r['total_value'],
                'bpso_time': bpso_r['execution_time'],
                'dp_optimal': dp_r['total_value'],
                'dp_time': dp_r['execution_time'],
                'gbfs_gap': (dp_r['total_value'] - gbfs_r['total_value']) / dp_r['total_value'] * 100,
                'bpso_gap': (dp_r['total_value'] - bpso_r['total_value']) / dp_r['total_value'] * 100
            })
            
            print(f"  GBFS={gbfs_r['total_value']}, BPSO={bpso_r['total_value']}, DP={dp_r['total_value']}")
        
        df = pd.DataFrame(results)
        csv_path = os.path.join(self.output_dir, '3_1_3_data_characteristics.csv')
        df.to_csv(csv_path, index=False)
        print(f"\n✓ Saved: {csv_path}")
        return df
    
    # =========================================================================
    # 3.2. TỔNG HỢP
    # =========================================================================
    
    def generate_summary_tables(self):
        """Generate summary table cho tất cả 13 test cases"""
        print("\n" + "="*70)
        print("3.2: SUMMARY TABLE")
        print("="*70)
        
        test_cases = self.loader.list_test_cases()
        summary = []
        
        for test_name in test_cases:
            print(f"\n{test_name}...")
            
            test_case = self.loader.load_test_case(test_name)
            items, weights, values, capacity = (
                test_case['items'], test_case['weights'],
                test_case['values'], test_case['capacity']
            )
            
            # Run 5 times
            gbfs_runs = [solve_gbfs(items, weights, values, capacity, max_states=5000) for _ in range(5)]
            bpso_runs = [solve_bpso(items, weights, values, capacity, n_particles=20, max_iterations=50) for _ in range(5)]
            dp_result = solve_dp(items, weights, values, capacity)
            
            gbfs_values = [r['total_value'] for r in gbfs_runs]
            gbfs_times = [r['execution_time'] for r in gbfs_runs]
            bpso_values = [r['total_value'] for r in bpso_runs]
            bpso_times = [r['execution_time'] for r in bpso_runs]
            
            summary.append({
                'test_case': test_name,
                'n_items': len(items),
                'capacity': capacity,
                'gbfs_best': max(gbfs_values),
                'gbfs_mean': np.mean(gbfs_values),
                'gbfs_std': np.std(gbfs_values),
                'gbfs_time': np.mean(gbfs_times),
                'bpso_best': max(bpso_values),
                'bpso_mean': np.mean(bpso_values),
                'bpso_std': np.std(bpso_values),
                'bpso_time': np.mean(bpso_times),
                'dp_optimal': dp_result['total_value'],
                'dp_time': dp_result['execution_time'],
                'gbfs_gap': (dp_result['total_value'] - np.mean(gbfs_values)) / dp_result['total_value'] * 100,
                'bpso_gap': (dp_result['total_value'] - np.mean(bpso_values)) / dp_result['total_value'] * 100
            })
        
        df = pd.DataFrame(summary)
        csv_path = os.path.join(self.output_dir, '3_2_summary_table.csv')
        df.to_csv(csv_path, index=False)
        print(f"\n✓ Saved: {csv_path}")
        
        # Print formatted
        print("\n" + "="*70)
        print("FINAL SUMMARY")
        print("="*70)
        print(df[['test_case', 'gbfs_mean', 'bpso_mean', 'dp_optimal', 'gbfs_gap', 'bpso_gap']].to_string(index=False))
        
        return df


def main():
    """Chạy tất cả experiments"""
    print("="*70)
    print("CHƯƠNG 3: THỰC NGHIỆM (13 test cases × 70 items)")
    print("="*70)
    
    exp = Chapter3Experiments()
    
    # 3.1.1: Parameters
    print("\n>>> 3.1.1: THAM SỐ")
    exp.experiment_3_1_1_gbfs_parameters()
    exp.experiment_3_1_1_bpso_parameters()
    
    # 3.1.2: Algorithms
    print("\n>>> 3.1.2: THUẬT TOÁN")
    exp.experiment_3_1_2_algorithm_comparison()
    
    # 3.1.3: Data
    print("\n>>> 3.1.3: DỮ LIỆU")
    exp.experiment_3_1_3_data_characteristics()
    
    # 3.2: Summary
    print("\n>>> 3.2: TỔNG HỢP")
    exp.generate_summary_tables()
    
    print("\n" + "="*70)
    print("✅ ALL CHAPTER 3 EXPERIMENTS COMPLETED!")
    print("="*70)


if __name__ == '__main__':
    main()
