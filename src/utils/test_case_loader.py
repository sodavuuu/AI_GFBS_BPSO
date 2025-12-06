"""
=================================================================================
MODULE: Data Loader V2
=================================================================================
Load test cases from pre-generated CSV files in data/test_cases/

STRATEGY:
- Load from 30 pre-generated test case files (not runtime sampling)
- Each test case: 100-200 items, capacity=15% total quantity
- Scenarios: Region (4×3), Category (4×3), Mixed (2×3)
- Names match with data_generator output

=================================================================================
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from pathlib import Path


class TestCaseLoader:
    """Load test cases from CSV files"""
    
    def __init__(self, test_cases_dir='data/test_cases'):
        self.test_cases_dir = Path(test_cases_dir)
        
        # Load summary file
        summary_path = self.test_cases_dir / 'test_cases_summary.csv'
        if summary_path.exists():
            self.summary = pd.read_csv(summary_path)
            print(f"✅ Loaded {len(self.summary)} test cases from {test_cases_dir}/")
        else:
            raise FileNotFoundError(
                f"⚠️  Summary file not found at {summary_path}\n"
                f"Please run: python src/data_generator.py"
            )
    
    def list_test_cases(self) -> List[str]:
        """Get list of all available test case names"""
        return self.summary['Name'].tolist()
    
    def get_test_case_info(self, name: str) -> Dict:
        """Get information about a test case"""
        row = self.summary[self.summary['Name'] == name]
        if len(row) == 0:
            raise ValueError(f"Test case '{name}' not found")
        return row.iloc[0].to_dict()
    
    def load_test_case(self, name: str, capacity_ratio: float = None) -> Dict:
        """
        Load a test case by name
        
        Args:
            name: Test case name (e.g., 'Region_North_small')
            capacity_ratio: Override capacity (default: use pre-calculated 15%)
        
        Returns:
            Dict with keys: items, weights, values, capacity, ...
        """
        # Get file info
        try:
            info = self.get_test_case_info(name)
            filepath = self.test_cases_dir / info['File']
        except (KeyError, ValueError) as e:
            raise ValueError(f"Failed to load test case '{name}': {e}")
        
        # Load CSV
        if not filepath.exists():
            raise FileNotFoundError(f"Test case file not found: {filepath}")
        
        df = pd.read_csv(filepath)
        
        # Extract data
        items = [f"Item_{i+1}" for i in range(len(df))]
        weights = df['Quantity'].values.tolist()
        values = df['Total'].values.tolist()
        
        # Extract Region and Category (for Multi-Objective)
        regions = df['Region'].values.tolist() if 'Region' in df.columns else [None] * len(df)
        categories = df['Category'].values.tolist() if 'Category' in df.columns else [None] * len(df)
        
        # Capacity
        if capacity_ratio is not None:
            capacity = int(sum(weights) * capacity_ratio)
        else:
            capacity = int(info['Capacity'])
        
        return {
            'items': items,
            'weights': weights,
            'values': values,
            'regions': regions,
            'categories': categories,
            'capacity': capacity,
            'n_items': len(items),
            'test_case_name': name,
            'file': info['File'],
            'type': info['Type'],
            'size': info['Size'],
            'total_weight': sum(weights),
            'total_value': sum(values),
            'avg_value': np.mean(values),
            'correlation': np.corrcoef(weights, values)[0, 1],
            'n_regions': int(info['N_Regions']),
            'n_categories': int(info['N_Categories'])
        }
    
    def load_by_region(self, region: str, size: str = 'medium') -> Dict:
        """
        Load test case by region
        
        Args:
            region: 'North', 'South', 'East', 'West'
            size: 'small', 'medium', 'large'
        """
        name = f'Region_{region}_{size}'
        return self.load_test_case(name)
    
    def load_by_category(self, category: str, size: str = 'medium') -> Dict:
        """
        Load test case by category
        
        Args:
            category: 'Clothing', 'Electronics', 'Food', 'Furniture'
            size: 'small', 'medium', 'large'
        """
        name = f'Category_{category}_{size}'
        return self.load_test_case(name)
    
    def load_diverse(self, size: str = 'medium') -> Dict:
        """Load diverse test case (balanced across regions)"""
        name = f'Diverse_{size}'
        return self.load_test_case(name)
    
    def load_high_value(self, size: str = 'medium') -> Dict:
        """Load high-value test case"""
        name = f'High_Value_{size}'
        return self.load_test_case(name)
    
    def get_all_test_cases(self, size: str = 'medium') -> List[Dict]:
        """Get all test cases of a specific size"""
        test_cases = []
        for name in self.list_test_cases():
            if name.endswith(f'_{size}'):
                try:
                    tc = self.load_test_case(name)
                    test_cases.append(tc)
                except Exception as e:
                    print(f"⚠️  Failed to load {name}: {e}")
        return test_cases
    
    def print_summary(self):
        """Print summary of all test cases"""
        print("\n" + "="*80)
        print("TEST CASES SUMMARY")
        print("="*80)
        
        # Group by type and size
        for test_type in ['region', 'category', 'mixed']:
            type_cases = self.summary[self.summary['Type'] == test_type]
            if len(type_cases) > 0:
                print(f"\n{test_type.upper()}:")
                for _, row in type_cases.iterrows():
                    print(f"  - {row['Name']}: {row['N_Items']} items, "
                          f"capacity={row['Capacity']}, "
                          f"correlation={row['Correlation_VW']:.3f}")


def load_data():
    """Convenience function to load test case loader"""
    return TestCaseLoader()


# Backward compatibility with old code
class SalesDataLoader(TestCaseLoader):
    """Alias for backward compatibility"""
    
    def __init__(self, excel_path='data/sales_data.xlsx'):
        # Ignore excel_path, use test cases instead
        super().__init__()
        print("⚠️  Note: Now using pre-generated test cases from data/test_cases/")
    
    def get_problem_by_region(self, region, capacity_ratio=0.5, max_items=None):
        """Load region test case (medium size by default)"""
        return self.load_by_region(region, size='medium')
    
    def get_problem_by_category(self, category, capacity_ratio=0.5, max_items=None):
        """Load category test case (medium size by default)"""
        return self.load_by_category(category, size='medium')
    
    def get_problem_by_size(self, size='medium', capacity_ratio=0.5):
        """Load diverse test case with specified size"""
        return self.load_diverse(size=size)


if __name__ == '__main__':
    # Test
    loader = TestCaseLoader()
    loader.print_summary()
    
    # Test load
    print("\n" + "="*80)
    print("TEST LOADING")
    print("="*80)
    
    tc = loader.load_by_region('North', 'medium')
    print(f"\n✓ Loaded: {tc['test_case_name']}")
    print(f"  Items: {tc['n_items']}, Capacity: {tc['capacity']}")
    print(f"  Total value: ${tc['total_value']:.2f}")
    print(f"  Correlation: {tc['correlation']:.3f}")
