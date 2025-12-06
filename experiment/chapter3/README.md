# Chapter 3 Experiments

This directory contains all experiments for Chapter 3: Analysis and Evaluation.

## Structure

- `experiments.py`: Main script to run all Chapter 3 experiments
- `3.1.1_Parameter_Analysis.ipynb`: Parameter impact analysis (GBFS & BPSO)
- `3.1.2_Algorithm_Comparison.ipynb`: Algorithm comparison (GBFS vs BPSO)
- `3.1.3_Data_Characteristics.ipynb`: Data characteristics analysis

## Experiments

### 3.1.1 Parameter Impact
- **3.1.1.a**: GBFS max_states parameter
- **3.1.1.b**: BPSO swarm size (n_particles)
- **3.1.1.c**: BPSO iterations (max_iterations)
- **3.1.1.d**: BPSO inertia weight (w)

### 3.1.2 Algorithm Comparison
- Compare GBFS vs BPSO on single test case (Size Medium 50)
- Compare GBFS vs BPSO across all 13 test cases
- Performance metrics: value, time, stability

### 3.1.3 Data Characteristics
- Analyze performance on different data types
- Low vs High correlation
- High value spread
- Regional diversity (1 vs 3 regions)

## Running Experiments

```bash
# Run all experiments
python3 main.py --regenerate

# Run specific experiment interactively
python3 main.py --experiments
# Then select: 1 (3.1.1.a), 2 (3.1.1.b), 3 (3.1.1.c), 4 (3.1.1.d), etc.
```

## Output Files

All results are saved to `../../results/chapter3/`:
- CSV files: Data tables
- PNG files: Visualization charts
- JSON files: BPSO convergence history (for 3.1.1.b, 3.1.1.c, 3.1.1.d)
