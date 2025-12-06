#!/usr/bin/env python3
"""
Quick launcher for Knapsack Solver GUI
Run this file to start the application
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from gui.main_gui import main

if __name__ == '__main__':
    main()
