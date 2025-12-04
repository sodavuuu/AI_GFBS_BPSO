"""
Configuration cho hệ thống Knapsack với SimpleAI
"""

# Dataset Configuration
DATASET_CONFIG = {
    'n_items': 15,
    'max_value': 100,
    'max_weight': 50,
    'capacity': 200,
    'seed': 42
}

# GBFS Configuration
GBFS_CONFIG = {
    'graph_search': True,  # Tránh lặp lại state
    'viewer': None  # Không hiển thị tree
}

# BPSO Configuration
BPSO_CONFIG = {
    'n_particles': 20,
    'max_iterations': 50,
    'w': 0.7,
    'c1': 1.5,
    'c2': 1.5,
    'v_max': 6.0
}
