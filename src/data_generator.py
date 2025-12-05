"""
=================================================================================
MODULE: Data Generator
=================================================================================
Tạo các file test cases từ sales_data.xlsx (1000 giao dịch)

STRATEGY (học từ GA_TSP):
- Không dùng hết 1000 items (quá chậm)
- Tạo 10+ scenarios khác nhau, mỗi scenario 20 items
- Lưu thành CSV files để tái sử dụng
- Mỗi scenario có ý nghĩa riêng để test thuật toán

SCENARIOS:
1. Region-based (4): North, South, East, West
2. Category-based (4): Clothing, Electronics, Food, Furniture  
3. Mixed scenarios (2): High-value, Diverse
4. Size-based (3): Small (100), Medium (150), Large (200)

OUTPUT: data/test_cases/*.csv
=================================================================================
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path


class DataGenerator:
    """Generate test case files from sales_data.xlsx"""
    
    def __init__(self, excel_path='data/sales_data.xlsx'):
        self.df = pd.read_excel(excel_path)
        self.output_dir = Path('data/test_cases')
        self.output_dir.mkdir(exist_ok=True)
        
        print(f"✅ Loaded {len(self.df)} transactions from {excel_path}")
        print(f"   Columns: {self.df.columns.tolist()}")
        
        # Rename for consistency with code
        self.df = self.df.rename(columns={
            'Quantity_Sold': 'Quantity',
            'Sales_Amount': 'Total',
            'Product_Category': 'Category'
        })
    
    def generate_all_scenarios(self):
        """
        Generate test case scenarios - REVISED for Multi-Objective
        Focus on regional diversity (f₂ = number of regions)
        """
        scenarios = []
        
        print("\n" + "="*80)
        print("GENERATING TEST CASE FILES - MULTI-OBJECTIVE (f₂ = Regional Diversity)")
        print("="*80)
        
        # 1. SIZE - Balanced 4 regions (3 scenarios)
        print("\n1. SIZE (Balanced 4 regions):")
        for size, n_items in [('small', 100), ('medium', 150), ('large', 200)]:
            scenario = self._create_diverse_scenario(n_items, size)
            scenarios.append(scenario)
        
        # 2. REGIONAL DIVERSITY - Test f₂ (3 scenarios: 1, 2, 3 regions)
        # Note: 4 regions already covered by diverse_medium
        print("\n2. REGIONAL DIVERSITY (Test f₂):")
        scenario = self._create_n_regions_scenario(1, 150, 'medium')  # f₂ = 1
        scenarios.append(scenario)
        scenario = self._create_n_regions_scenario(2, 150, 'medium')  # f₂ = 2
        scenarios.append(scenario)
        scenario = self._create_n_regions_scenario(3, 150, 'medium')  # f₂ = 3
        scenarios.append(scenario)
        
        # 3. CATEGORY - 4 regions each (4 scenarios)
        print("\n3. CATEGORY (4 regions each):")
        for category in ['Clothing', 'Electronics', 'Food', 'Furniture']:
            scenario = self._create_category_balanced_scenario(category, 150, 'medium')
            scenarios.append(scenario)
        
        # 4. DATA CHARACTERISTICS - 4 regions (3 scenarios)
        print("\n4. DATA CHARACTERISTICS (4 regions):")
        scenario = self._create_correlation_scenario('low', 0.1, 150, 'medium')
        scenarios.append(scenario)
        scenario = self._create_correlation_scenario('high', 0.7, 150, 'medium')
        scenarios.append(scenario)
        scenario = self._create_high_value_balanced_scenario(150, 'medium')
        scenarios.append(scenario)
        
        print(f"\n✅ Generated {len(scenarios)} test case files")
        return scenarios
    
    def _create_region_scenario(self, region, n_items, size):
        """Create test case for specific region"""
        df_region = self.df[self.df['Region'] == region]
        
        if len(df_region) > n_items:
            df_subset = df_region.sample(n=n_items, random_state=42)
        else:
            df_subset = df_region
        
        # Calculate capacity (15% of total quantity)
        capacity = int(df_subset['Quantity'].sum() * 0.15)
        
        # Save to CSV
        filename = f'region_{region.lower()}_{size}.csv'
        filepath = self.output_dir / filename
        df_subset.to_csv(filepath, index=False)
        
        print(f"   ✓ {filename}: {len(df_subset)} items, capacity={capacity}")
        
        return {
            'name': f'Region_{region}_{size}',
            'file': filename,
            'n_items': len(df_subset),
            'capacity': capacity,
            'type': 'region',
            'region': region,
            'size': size
        }
    
    def _create_category_scenario(self, category, n_items, size):
        """Create test case for specific category"""
        df_category = self.df[self.df['Category'] == category]
        
        if len(df_category) > n_items:
            df_subset = df_category.sample(n=n_items, random_state=42)
        else:
            df_subset = df_category
        
        capacity = int(df_subset['Quantity'].sum() * 0.15)
        
        filename = f'category_{category.lower()}_{size}.csv'
        filepath = self.output_dir / filename
        df_subset.to_csv(filepath, index=False)
        
        print(f"   ✓ {filename}: {len(df_subset)} items, capacity={capacity}")
        
        return {
            'name': f'Category_{category}_{size}',
            'file': filename,
            'n_items': len(df_subset),
            'capacity': capacity,
            'type': 'category',
            'category': category,
            'size': size
        }
    
    def _create_high_value_scenario(self, n_items, size):
        """Create test case with high-value transactions"""
        median_value = self.df['Total'].median()
        df_high_value = self.df[self.df['Total'] > median_value]
        
        if len(df_high_value) > n_items:
            df_subset = df_high_value.sample(n=n_items, random_state=42)
        else:
            df_subset = df_high_value
        
        capacity = int(df_subset['Quantity'].sum() * 0.15)
        
        filename = f'mixed_high_value_{size}.csv'
        filepath = self.output_dir / filename
        df_subset.to_csv(filepath, index=False)
        
        print(f"   ✓ {filename}: {len(df_subset)} items, capacity={capacity}")
        
        return {
            'name': f'High_Value_{size}',
            'file': filename,
            'n_items': len(df_subset),
            'capacity': capacity,
            'type': 'mixed',
            'subtype': 'high_value',
            'size': size
        }
    
    def _create_diverse_scenario(self, n_items, size):
        """Create test case with balanced distribution across 4 regions"""
        # Sample equally from each region
        n_per_region = n_items // 4
        
        df_list = []
        for region in ['North', 'South', 'East', 'West']:
            df_region = self.df[self.df['Region'] == region]
            if len(df_region) >= n_per_region:
                df_sampled = df_region.sample(n=n_per_region, random_state=42)
            else:
                df_sampled = df_region
            df_list.append(df_sampled)
        
        df_subset = pd.concat(df_list, ignore_index=True)
        
        capacity = int(df_subset['Quantity'].sum() * 0.15)
        
        filename = f'balanced_4regions_{size}.csv'
        filepath = self.output_dir / filename
        df_subset.to_csv(filepath, index=False)
        
        print(f"   ✓ {filename}: {len(df_subset)} items, capacity={capacity}, f₂=4")
        
        return {
            'name': f'Balanced_4Regions_{size}',
            'file': filename,
            'n_items': len(df_subset),
            'capacity': capacity,
            'type': 'balanced',
            'size': size
        }
    
    def _create_n_regions_scenario(self, n_regions, n_items, size):
        """Create test case with specific number of regions (for testing f₂)"""
        regions = ['North', 'South', 'East', 'West'][:n_regions]
        n_per_region = n_items // n_regions
        
        df_list = []
        for region in regions:
            df_region = self.df[self.df['Region'] == region]
            if len(df_region) >= n_per_region:
                df_sampled = df_region.sample(n=n_per_region, random_state=42)
            else:
                df_sampled = df_region
            df_list.append(df_sampled)
        
        df_subset = pd.concat(df_list, ignore_index=True)
        capacity = int(df_subset['Quantity'].sum() * 0.15)
        
        filename = f'region_{n_regions}regions_{size}.csv'
        filepath = self.output_dir / filename
        df_subset.to_csv(filepath, index=False)
        
        print(f"   ✓ {filename}: {len(df_subset)} items, capacity={capacity}, f₂={n_regions}")
        
        return {
            'name': f'Region_{n_regions}Regions_{size}',
            'file': filename,
            'n_items': len(df_subset),
            'capacity': capacity,
            'type': 'regional',
            'size': size
        }
    
    def _create_category_balanced_scenario(self, category, n_items, size):
        """Create test case for category with balanced 4 regions"""
        df_category = self.df[self.df['Category'] == category]
        
        # Sample from 4 regions
        n_per_region = n_items // 4
        df_list = []
        for region in ['North', 'South', 'East', 'West']:
            df_region_cat = df_category[df_category['Region'] == region]
            if len(df_region_cat) >= n_per_region:
                df_list.append(df_region_cat.sample(n=n_per_region, random_state=42))
            else:
                df_list.append(df_region_cat)
        
        df_subset = pd.concat(df_list, ignore_index=True)
        capacity = int(df_subset['Quantity'].sum() * 0.15)
        
        filename = f'category_{category.lower()}_{size}.csv'
        filepath = self.output_dir / filename
        df_subset.to_csv(filepath, index=False)
        
        print(f"   ✓ {filename}: {len(df_subset)} items, capacity={capacity}, 4 regions")
        
        return {
            'name': f'Category_{category}_{size}',
            'file': filename,
            'n_items': len(df_subset),
            'capacity': capacity,
            'type': 'category',
            'category': category,
            'size': size
        }
    
    def _create_high_value_balanced_scenario(self, n_items, size):
        """Create test case with high-value items, balanced 4 regions"""
        median_value = self.df['Total'].median()
        df_high = self.df[self.df['Total'] > median_value]
        
        n_per_region = n_items // 4
        df_list = []
        for region in ['North', 'South', 'East', 'West']:
            df_region = df_high[df_high['Region'] == region]
            if len(df_region) >= n_per_region:
                df_list.append(df_region.sample(n=n_per_region, random_state=42))
            else:
                df_list.append(df_region)
        
        df_subset = pd.concat(df_list, ignore_index=True)
        capacity = int(df_subset['Quantity'].sum() * 0.15)
        
        filename = f'data_high_value_{size}.csv'
        filepath = self.output_dir / filename
        df_subset.to_csv(filepath, index=False)
        
        print(f"   ✓ {filename}: {len(df_subset)} items, capacity={capacity}, high-value, 4 regions")
        
        return {
            'name': f'Data_HighValue_{size}',
            'file': filename,
            'n_items': len(df_subset),
            'capacity': capacity,
            'type': 'data_char',
            'subtype': 'high_value',
            'size': size
        }
    
    def _create_correlation_scenario(self, corr_type: str, target_corr: float, n_items: int, size: str):
        """Create scenario with correlation (v,w) mong muốn, balanced 4 regions"""
        # Tính correlation cho từng subset và chọn subset phù hợp
        best_subset = None
        best_corr_diff = float('inf')
        
        for _ in range(100):  # Try 100 random samples
            n_per_region = n_items // 4
            df_list = []
            for region in ['North', 'South', 'East', 'West']:
                df_region = self.df[self.df['Region'] == region]
                if len(df_region) >= n_per_region:
                    df_sampled = df_region.sample(n=n_per_region, random_state=None)
                else:
                    df_sampled = df_region
                df_list.append(df_sampled)
            
            df_sample = pd.concat(df_list, ignore_index=True)
            corr = np.corrcoef(df_sample['Quantity'], df_sample['Total'])[0, 1]
            
            if abs(corr - target_corr) < best_corr_diff:
                best_corr_diff = abs(corr - target_corr)
                best_subset = df_sample.copy()
        
        capacity = int(best_subset['Quantity'].sum() * 0.15)
        actual_corr = np.corrcoef(best_subset['Quantity'], best_subset['Total'])[0, 1]
        
        filename = f'data_{corr_type}_correlation_{size}.csv'
        filepath = self.output_dir / filename
        best_subset.to_csv(filepath, index=False)
        
        print(f"   ✓ {filename}: {len(best_subset)} items, capacity={capacity}, corr={actual_corr:.3f}, 4 regions")
        
        return {
            'name': f'Data_{corr_type.capitalize()}Correlation_{size}',
            'file': filename,
            'n_items': len(best_subset),
            'capacity': capacity,
            'type': 'data_char',
            'subtype': f'{corr_type}_correlation',
            'size': size
        }
    
    def create_summary_file(self, scenarios):
        """Create summary file with all test cases"""
        summary_data = []
        
        for scenario in scenarios:
            # Load CSV to get actual statistics
            filepath = self.output_dir / scenario['file']
            df = pd.read_csv(filepath)
            
            summary_data.append({
                'Name': scenario['name'],
                'File': scenario['file'],
                'Type': scenario['type'],
                'Size': scenario['size'],
                'N_Items': len(df),
                'Capacity': scenario['capacity'],
                'Total_Quantity': df['Quantity'].sum(),
                'Total_Value': df['Total'].sum(),
                'Avg_Value': df['Total'].mean(),
                'Correlation_VW': df['Quantity'].corr(df['Total']),
                'N_Regions': df['Region'].nunique(),
                'N_Categories': df['Category'].nunique()
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_path = self.output_dir / 'test_cases_summary.csv'
        summary_df.to_csv(summary_path, index=False)
        
        print(f"\n✅ Created summary file: {summary_path}")
        print(f"\n{summary_df.to_string(index=False)}")
        
        return summary_df


def main():
    """Generate all test case files"""
    generator = DataGenerator()
    scenarios = generator.generate_all_scenarios()
    summary = generator.create_summary_file(scenarios)
    
    print("\n" + "="*80)
    print("✅ COMPLETE! All test case files generated in data/test_cases/")
    print("="*80)
    print(f"Total scenarios: {len(scenarios)}")
    print(f"Files location: data/test_cases/")
    print(f"Summary file: data/test_cases/test_cases_summary.csv")


if __name__ == '__main__':
    main()
