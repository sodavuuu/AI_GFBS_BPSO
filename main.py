"""
MAIN SCRIPT: So sánh GBFS (SimpleAI) và BPSO cho 0/1 Knapsack
"""
import sys
from simpleai.search import greedy, astar

from config import DATASET_CONFIG, GBFS_CONFIG, BPSO_CONFIG
from knapsack_problem import (
    KnapsackGBFS, 
    generate_dataset, 
    analyze_dataset,
    solve_optimal_dp
)
from bpso_solver import BPSOSolver


def print_header(title: str):
    """In header đẹp"""
    print("\n" + "="*70)
    print(f"{title:^70}")
    print("="*70)


def compare_solutions(gbfs_result, bpso_result, optimal_value=None, optimal_items=None, capacity=None):
    """So sánh kết quả GBFS và BPSO"""
    print_header("SO SÁNH KẾT QUẢ")
    
    # Table header
    print(f"\n{'Metric':<25} {'GBFS':>15} {'BPSO':>15} {'Optimal':>15}")
    print("-" * 70)
    
    # Value
    gbfs_val = gbfs_result['total_value']
    bpso_val = bpso_result['total_value']
    opt_val = optimal_value if optimal_value else "N/A"
    print(f"{'Total Value':<25} {gbfs_val:>15} {bpso_val:>15} {opt_val:>15}")
    
    # Weight
    cap = capacity if capacity else gbfs_result.get('capacity', 'N/A')
    gbfs_weight = f"{gbfs_result['total_weight']}/{cap}"
    bpso_weight = f"{bpso_result['total_weight']}/{cap}"
    if optimal_items and capacity:
        opt_weight = sum(item[1] for i, item in enumerate(gbfs_result.get('all_items', [])) if i in optimal_items)
        opt_weight_str = f"{opt_weight}/{cap}"
    else:
        opt_weight_str = "N/A"
    print(f"{'Total Weight':<25} {gbfs_weight:>15} {bpso_weight:>15} {opt_weight_str:>15}")
    
    # Items selected
    print(f"{'Items Selected':<25} {gbfs_result['n_items_selected']:>15} {bpso_result['n_items_selected']:>15} {len(optimal_items) if optimal_items else 'N/A':>15}")
    
    # Iterations/States
    gbfs_explored = gbfs_result['states_explored']
    bpso_iter = bpso_result['iterations']
    print(f"{'States/Iterations':<25} {gbfs_explored:>15} {bpso_iter:>15} {'N/A':>15}")
    
    print("-" * 70)
    
    # Gap to optimal
    if optimal_value:
        gbfs_gap = ((optimal_value - gbfs_val) / optimal_value * 100) if optimal_value > 0 else 0
        bpso_gap = ((optimal_value - bpso_val) / optimal_value * 100) if optimal_value > 0 else 0
        
        print(f"\n{'Gap to Optimal':<25} {gbfs_gap:>14.2f}% {bpso_gap:>14.2f}%")
    
    # Winner
    print("\n🏆 WINNER:")
    if gbfs_val > bpso_val:
        print(f"   GBFS wins với value cao hơn {gbfs_val - bpso_val}")
    elif bpso_val > gbfs_val:
        print(f"   BPSO wins với value cao hơn {bpso_val - gbfs_val}")
    else:
        print(f"   TIE - Cả hai đều đạt value = {gbfs_val}")
    
    print("\n" + "="*70)


def main():
    """Main function"""
    print_header("HỆ THỐNG SO SÁNH GBFS VÀ BPSO")
    print("Sử dụng SimpleAI library cho GBFS")
    
    # Chọn dataset type
    print("\nChọn loại dataset:")
    print("1. Random (cân bằng)")
    print("2. High Correlation (v-w tương quan cao)")
    print("3. Outlier (có items bẫy)")
    print("4. Similar Ratio (v/w gần nhau)")
    
    choice = input("\nNhập lựa chọn (1-4, mặc định 1): ").strip()
    
    dataset_types = {
        '1': 'random',
        '2': 'high_correlation',
        '3': 'outlier',
        '4': 'similar_ratio'
    }
    
    dataset_type = dataset_types.get(choice, 'random')
    
    # Generate dataset
    print_header("BƯỚC 1: SINH DATASET")
    print(f"\nDataset type: {dataset_type}")
    
    items = generate_dataset(
        n_items=DATASET_CONFIG['n_items'],
        max_value=DATASET_CONFIG['max_value'],
        max_weight=DATASET_CONFIG['max_weight'],
        capacity=DATASET_CONFIG['capacity'],
        seed=DATASET_CONFIG['seed'],
        dataset_type=dataset_type
    )
    
    analyze_dataset(items, DATASET_CONFIG['capacity'])
    
    # Solve with DP (optimal)
    optimal_value = None
    optimal_items = None
    
    if DATASET_CONFIG['n_items'] <= 25:
        print_header("BƯỚC 2: GIẢI OPTIMAL (DYNAMIC PROGRAMMING)")
        try:
            optimal_value, optimal_items = solve_optimal_dp(items, DATASET_CONFIG['capacity'])
            print(f"\nOptimal value: {optimal_value}")
            print(f"Items selected: {len(optimal_items)}")
            selected_names = [items[i][0] for i in optimal_items]
            print(f"Items: {', '.join(selected_names)}")
        except Exception as e:
            print(f"\n⚠ Không thể giải DP: {e}")
    else:
        print("\n⚠ Dataset quá lớn, bỏ qua optimal solution")
    
    # Solve with GBFS
    print_header("BƯỚC 3: GIẢI BẰNG GBFS (SIMPLEAI)")
    
    problem = KnapsackGBFS(items, DATASET_CONFIG['capacity'])
    
    print("\nĐang chạy GBFS...")
    result = greedy(problem, graph_search=GBFS_CONFIG['graph_search'])
    
    gbfs_info = problem.get_solution_info(result.state)
    
    print(f"\n{'='*70}")
    print("KẾT QUẢ GBFS")
    print(f"{'='*70}")
    print(f"Total value: {gbfs_info['total_value']}")
    print(f"Total weight: {gbfs_info['total_weight']}/{gbfs_info['capacity']}")
    print(f"Items selected: {gbfs_info['n_items_selected']}")
    print(f"Items: {', '.join(gbfs_info['items'])}")
    print(f"States explored: {gbfs_info['states_explored']}")
    print(f"Max depth: {gbfs_info['max_depth']}")
    print(f"{'='*70}")
    
    # Solve with BPSO
    print_header("BƯỚC 4: GIẢI BẰNG BPSO")
    
    bpso = BPSOSolver(
        items=items,
        capacity=DATASET_CONFIG['capacity'],
        n_particles=BPSO_CONFIG['n_particles'],
        max_iterations=BPSO_CONFIG['max_iterations'],
        w=BPSO_CONFIG['w'],
        c1=BPSO_CONFIG['c1'],
        c2=BPSO_CONFIG['c2'],
        v_max=BPSO_CONFIG['v_max']
    )
    
    bpso_info = bpso.solve(verbose=True)
    
    # Store all items for comparison
    gbfs_info['all_items'] = items
    
    # Compare
    compare_solutions(gbfs_info, bpso_info, optimal_value, optimal_items, DATASET_CONFIG['capacity'])
    
    # Analysis
    print_header("PHÂN TÍCH")
    
    print("\n📊 GBFS (Greedy Best First Search):")
    print(f"   - Sử dụng heuristic: Fractional Knapsack Bound")
    print(f"   - States explored: {gbfs_info['states_explored']}")
    print(f"   - Kết quả: {gbfs_info['total_value']}")
    
    if optimal_value:
        gap = ((optimal_value - gbfs_info['total_value']) / optimal_value * 100) if optimal_value > 0 else 0
        print(f"   - Gap to optimal: {gap:.2f}%")
        if gap < 5:
            print("   ✅ Rất tốt! Gần optimal")
        elif gap < 15:
            print("   ⚠ Khá tốt, có thể cải thiện")
        else:
            print("   ❌ Kém, bị local optimum")
    
    print("\n📊 BPSO (Binary Particle Swarm Optimization):")
    print(f"   - Population-based metaheuristic")
    print(f"   - Iterations: {bpso_info['iterations']}")
    print(f"   - Kết quả: {bpso_info['total_value']}")
    
    if optimal_value:
        gap = ((optimal_value - bpso_info['total_value']) / optimal_value * 100) if optimal_value > 0 else 0
        print(f"   - Gap to optimal: {gap:.2f}%")
        if gap < 5:
            print("   ✅ Rất tốt! Gần optimal")
        elif gap < 15:
            print("   ⚠ Khá tốt, có thể cải thiện")
        else:
            print("   ❌ Kém, có thể bị early convergence")
    
    print("\n💡 KẾT LUẬN:")
    
    if dataset_type == 'random':
        print("   Dataset cân bằng → Cả 2 thuật toán thường hoạt động tốt")
    elif dataset_type == 'high_correlation':
        print("   Dataset có correlation cao → GBFS có thể gặp khó (tie-breaking)")
        print("   BPSO có thể tốt hơn vì explore rộng")
    elif dataset_type == 'outlier':
        print("   Dataset có outliers → Cả 2 đều dễ bị trap")
        print("   GBFS dễ bị greedy trap, BPSO cần nhiều iterations")
    elif dataset_type == 'similar_ratio':
        print("   Dataset có v/w ratio gần nhau → GBFS gặp tie-breaking issue")
        print("   BPSO ít bị ảnh hưởng vì không dùng heuristic trực tiếp")
    
    print("\n" + "="*70)
    print("HOÀN THÀNH!")
    print("="*70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Đã dừng bởi người dùng")
    except Exception as e:
        print(f"\n\n❌ LỖI: {e}")
        import traceback
        traceback.print_exc()
