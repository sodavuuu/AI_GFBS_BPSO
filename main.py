#!/usr/bin/env python3
"""
=================================================================================
KNAPSACK SOLVER - MAIN ENTRY POINT
=================================================================================
Multi-Objective 0/1 Knapsack Problem Solver
- Algorithms: GBFS (Greedy Best-First Search) & BPSO (Binary PSO)
- GUI: Interactive visualization and testing
- Experiments: Chapter 3 analysis and data generation

Usage:
    python3 main.py              # Launch GUI (default)
    python3 main.py --gui        # Launch GUI
    python3 main.py --experiments # Run Chapter 3 experiments
    python3 main.py --regenerate  # Regenerate all experiment data
=================================================================================
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def launch_gui():
    """Launch the GUI application"""
    from gui.main_gui import main
    print("\n🚀 Launching Knapsack Solver GUI...")
    print("="*70)
    main()


def run_experiments():
    """Run Chapter 3 experiments interactively"""
    from experiment.chapter3.experiments import Chapter3Experiments
    
    print("\n" + "="*80)
    print("CHAPTER 3 EXPERIMENTS - GBFS & BPSO Analysis")
    print("="*80)
    
    exp = Chapter3Experiments()
    
    # Menu
    print("\n📊 Available experiments:")
    print("  1. 3.1.1.a - GBFS Parameter Analysis (Max States)")
    print("  2. 3.1.1.b - BPSO Swarm Size Analysis")
    print("  3. 3.1.1.c - BPSO Iterations Analysis")
    print("  4. 3.1.1.d - BPSO Inertia Weight Analysis")
    print("  5. 3.1.2   - Algorithm Comparison (Single test case)")
    print("  6. 3.1.2   - Algorithm Comparison (All test cases)")
    print("  7. 3.1.3   - Data Characteristics Analysis")
    print("  8. Run ALL experiments")
    print("  0. Exit")
    
    while True:
        try:
            choice = input("\n🔢 Select experiment (0-8): ").strip()
            
            if choice == '0':
                print("\n👋 Exiting...")
                break
            elif choice == '1':
                exp.experiment_3_1_1_a_gbfs_parameters()
            elif choice == '2':
                exp.experiment_3_1_1_b_bpso_swarm_size()
            elif choice == '3':
                exp.experiment_3_1_1_c_bpso_iterations()
            elif choice == '4':
                exp.experiment_3_1_1_d_bpso_inertia_weight()
            elif choice == '5':
                exp.experiment_3_1_2_algorithm_comparison_single()
            elif choice == '6':
                exp.experiment_3_1_2_algorithm_comparison_all()
            elif choice == '7':
                exp.experiment_3_1_3_data_characteristics()
            elif choice == '8':
                exp.run_all_experiments()
                break
            else:
                print("❌ Invalid choice. Please select 0-8.")
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user. Exiting...")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


def regenerate_all_data():
    """Regenerate all experiment data"""
    from experiment.chapter3.experiments import Chapter3Experiments
    
    print("\n" + "="*80)
    print(" " * 20 + "REGENERATING ALL EXPERIMENT DATA")
    print(" " * 15 + "TRUE GBFS + BPSO Implementation")
    print("="*80)
    
    exp = Chapter3Experiments()
    
    experiments = [
        ("3.1.1.a", "GBFS Parameters (max_states)", exp.experiment_3_1_1_a_gbfs_parameters),
        ("3.1.1.b", "BPSO Swarm Size", exp.experiment_3_1_1_b_bpso_swarm_size),
        ("3.1.1.c", "BPSO Iterations", exp.experiment_3_1_1_c_bpso_iterations),
        ("3.1.1.d", "BPSO Inertia Weight", exp.experiment_3_1_1_d_bpso_inertia_weight),
        ("3.1.2", "Algorithm Comparison (Single)", lambda: exp.experiment_3_1_2_algorithm_comparison_single('Size Medium 50')),
        ("3.1.2", "Algorithm Comparison (All)", exp.experiment_3_1_2_algorithm_comparison_all),
        ("3.1.3", "Data Characteristics", exp.experiment_3_1_3_data_characteristics),
    ]
    
    results = []
    for exp_id, exp_name, exp_func in experiments:
        print(f"\n{'='*80}")
        print(f"Running {exp_id}: {exp_name}")
        print('='*80)
        
        try:
            exp_func()
            results.append((exp_id, exp_name, "✅ SUCCESS"))
            print(f"\n✅ {exp_id} completed successfully")
        except Exception as e:
            results.append((exp_id, exp_name, f"❌ FAILED: {str(e)}"))
            print(f"\n❌ {exp_id} failed: {e}")
            import traceback
            traceback.print_exc()
    
    # Summary
    print("\n" + "="*80)
    print(" " * 25 + "REGENERATION SUMMARY")
    print("="*80)
    
    for exp_id, exp_name, status in results:
        print(f"{exp_id:8s} | {exp_name:35s} | {status}")
    
    success_count = sum(1 for _, _, s in results if "SUCCESS" in s)
    print("="*80)
    print(f"Completed: {success_count}/{len(results)} experiments")
    
    if success_count == len(results):
        print("\n🎉 ALL DATA REGENERATED SUCCESSFULLY!")
        print("\nNext steps:")
        print("1. Open notebooks in experiment/chapter3/")
        print("2. Run all cells to verify outputs")
        print("3. Review visualizations")
    else:
        print("\n⚠️  Some experiments failed - check errors above")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Knapsack Solver - Multi-Objective Optimization',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main.py                    # Launch GUI (default)
  python3 main.py --gui              # Launch GUI
  python3 main.py --experiments      # Run experiments interactively
  python3 main.py --regenerate       # Regenerate all data
        """
    )
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--gui', action='store_true', 
                      help='Launch GUI application (default)')
    group.add_argument('--experiments', action='store_true',
                      help='Run Chapter 3 experiments interactively')
    group.add_argument('--regenerate', action='store_true',
                      help='Regenerate all experiment data')
    
    args = parser.parse_args()
    
    # Default to GUI if no args
    if not (args.experiments or args.regenerate):
        args.gui = True
    
    # Execute based on arguments
    if args.gui:
        launch_gui()
    elif args.experiments:
        run_experiments()
    elif args.regenerate:
        regenerate_all_data()


if __name__ == '__main__':
    main()
