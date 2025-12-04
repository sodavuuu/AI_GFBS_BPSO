"""
DEMO: Test nhanh hệ thống với dataset random nhỏ
"""
from simpleai.search import greedy

from config import DATASET_CONFIG, GBFS_CONFIG, BPSO_CONFIG
from knapsack_problem import (
    KnapsackGBFS, 
    generate_dataset, 
    analyze_dataset,
    solve_optimal_dp
)
from bpso_solver import BPSOSolver


def main():
    print("\n" + "="*70)
    print("DEMO - TEST HỆ THỐNG GBFS vs BPSO")
    print("="*70)
    
    # Generate dataset
    print("\n[1/4] Sinh dataset random (15 items)...")
    items = generate_dataset(
        n_items=15,
        max_value=100,
        max_weight=50,
        capacity=200,
        seed=42,
        dataset_type='random'
    )
    
    analyze_dataset(items, 200)
    
    # Optimal
    print("\n[2/4] Giải optimal bằng DP...")
    optimal_value, optimal_items = solve_optimal_dp(items, 200)
    print(f"Optimal value: {optimal_value}")
    
    # GBFS
    print("\n[3/4] Chạy GBFS (SimpleAI)...")
    problem = KnapsackGBFS(items, 200)
    result = greedy(problem, graph_search=True)
    gbfs_info = problem.get_solution_info(result.state)
    
    print(f"\nGBFS Result:")
    print(f"  Value: {gbfs_info['total_value']}")
    print(f"  Weight: {gbfs_info['total_weight']}/200")
    print(f"  States explored: {gbfs_info['states_explored']}")
    
    # BPSO
    print("\n[4/4] Chạy BPSO...")
    bpso = BPSOSolver(items, 200, n_particles=20, max_iterations=50)
    bpso_info = bpso.solve(verbose=False)
    
    print(f"\nBPSO Result:")
    print(f"  Value: {bpso_info['total_value']}")
    print(f"  Weight: {bpso_info['total_weight']}/200")
    
    # Summary
    print("\n" + "="*70)
    print("KẾT QUẢ TỔNG HỢP")
    print("="*70)
    print(f"\n{'Algorithm':<15} {'Value':>10} {'Weight':>10} {'Gap':>10}")
    print("-" * 50)
    
    gbfs_gap = ((optimal_value - gbfs_info['total_value']) / optimal_value * 100)
    bpso_gap = ((optimal_value - bpso_info['total_value']) / optimal_value * 100)
    
    print(f"{'Optimal':<15} {optimal_value:>10} {'-':>10} {'-':>10}")
    print(f"{'GBFS':<15} {gbfs_info['total_value']:>10} {gbfs_info['total_weight']:>10} {gbfs_gap:>9.2f}%")
    print(f"{'BPSO':<15} {bpso_info['total_value']:>10} {bpso_info['total_weight']:>10} {bpso_gap:>9.2f}%")
    
    print("\n🏆 WINNER:")
    if gbfs_info['total_value'] > bpso_info['total_value']:
        print("   GBFS wins!")
    elif bpso_info['total_value'] > gbfs_info['total_value']:
        print("   BPSO wins!")
    else:
        print("   TIE!")
    
    print("\n✅ DEMO hoàn thành!")
    print("   Chạy: python main.py để test với các dataset khác")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
