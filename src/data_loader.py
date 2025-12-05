"""
=================================================================================
MODULE: Data Loader
=================================================================================
Load và chuẩn bị dữ liệu từ sales_data.xlsx để tạo test cases
cho bài toán Knapsack
=================================================================================
"""

import pandas as pd
import numpy as np
import os
from typing import Tuple, List, Dict


class SalesDataLoader:
    """Load và transform sales data thành Knapsack problem instances"""
    
    def __init__(self, excel_path='data/sales_data.xlsx'):
        """
        Khởi tạo data loader
        
        Args:
            excel_path: Đường dẫn tới file Excel
        """
        if not os.path.exists(excel_path):
            # Thử đường dẫn tương đối từ thư mục hiện tại
            current_dir = os.path.dirname(os.path.abspath(__file__))
            excel_path = os.path.join(current_dir, '..', 'data', 'sales_data.xlsx')
        
        self.df = pd.read_excel(excel_path)
        self._preprocess_data()
    
    def _preprocess_data(self):
        """Tiền xử lý dữ liệu"""
        # Loại bỏ null values
        self.df = self.df.dropna()
        
        # Đảm bảo các cột số là numeric
        numeric_cols = ['Sales_Amount', 'Quantity_Sold', 'Unit_Cost', 'Unit_Price']
        for col in numeric_cols:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        self.df = self.df.dropna()
        
        # Tính thêm cột Profit
        self.df['Profit'] = self.df['Sales_Amount'] - (self.df['Unit_Cost'] * self.df['Quantity_Sold'])
        self.df['Value_Weight_Ratio'] = self.df['Sales_Amount'] / (self.df['Unit_Cost'] * self.df['Quantity_Sold'])
    
    def create_problem_instance(self, df_subset, capacity_ratio=0.5, use_profit=False):
        """
        Tạo một instance của bài toán Knapsack từ subset data
        
        Args:
            df_subset: DataFrame subset
            capacity_ratio: Tỷ lệ capacity so với tổng trọng lượng (0-1)
            use_profit: Dùng Profit thay vì Sales_Amount làm value
        
        Returns:
            (items, weights, values, capacity)
        """
        items = []
        weights = []
        values = []
        
        for idx, row in df_subset.iterrows():
            # Item name: Transaction_ID + Category abbreviation
            item_name = f"T{row['Transaction_ID']}_{row['Product_Category'][:3]}"
            items.append(item_name)
            
            # Weight: Total cost (Unit_Cost * Quantity)
            weight = int(row['Unit_Cost'] * row['Quantity_Sold'])
            weights.append(weight)
            
            # Value: Sales_Amount hoặc Profit
            if use_profit:
                value = max(0, int(row['Profit']))  # Không cho giá trị âm
            else:
                value = int(row['Sales_Amount'])
            values.append(value)
        
        # Tính capacity
        total_weight = sum(weights)
        capacity = int(total_weight * capacity_ratio)
        
        return items, weights, values, capacity
    
    def get_problem_by_region(self, region, capacity_ratio=0.5, max_items=50):
        """
        Tạo problem cho một region cụ thể
        
        Args:
            region: 'North', 'South', 'East', 'West'
            capacity_ratio: Tỷ lệ capacity
            max_items: Số items tối đa (default 50 để nhanh)
        
        Returns:
            (items, weights, values, capacity, description)
        """
        df_region = self.df[self.df['Region'] == region]
        
        # SAMPLE nhỏ để tránh quá chậm
        if len(df_region) > max_items:
            df_region = df_region.sample(n=max_items, random_state=42)
        
        items, weights, values, capacity = self.create_problem_instance(df_region, capacity_ratio)
        
        description = f"Region {region} - {len(items)} items (sampled from {len(self.df[self.df['Region'] == region])})"
        return items, weights, values, capacity, description
    
    def get_problem_by_category(self, category, capacity_ratio=0.5, max_items=50):
        """
        Tạo problem cho một product category
        
        Args:
            category: 'Electronics', 'Clothing', 'Food', 'Furniture'
            capacity_ratio: Tỷ lệ capacity
            max_items: Số items tối đa (default 50)
        
        Returns:
            (items, weights, values, capacity, description)
        """
        df_cat = self.df[self.df['Product_Category'] == category]
        
        # SAMPLE nhỏ để tránh quá chậm
        if len(df_cat) > max_items:
            df_cat = df_cat.sample(n=max_items, random_state=42)
        
        items, weights, values, capacity = self.create_problem_instance(df_cat, capacity_ratio)
        
        description = f"Category {category} - {len(items)} items (sampled from {len(self.df[self.df['Product_Category'] == category])})"
        return items, weights, values, capacity, description
    
    def get_problem_by_size(self, size='medium', capacity_ratio=0.5):
        """
        Tạo problem với kích thước khác nhau
        
        Args:
            size: 'small' (15-25), 'medium' (30-50), 'large' (60-80)
            capacity_ratio: Tỷ lệ capacity
        
        Returns:
            (items, weights, values, capacity, description)
        """
        # Size thực tế hợp lý cho GUI và experiments
        size_map = {
            'small': 20,    # Nhanh, cho demo
            'medium': 40,   # Vừa phải, cho thí nghiệm
            'large': 70     # Lớn nhưng vẫn chạy được DP
        }
        
        n_items = size_map.get(size, 40)
        df_sample = self.df.sample(n=min(n_items, len(self.df)), random_state=42)
        
        items, weights, values, capacity = self.create_problem_instance(df_sample, capacity_ratio)
        
        description = f"Size {size.upper()} - {len(items)} items"
        return items, weights, values, capacity, description
    
    def get_all_test_cases(self):
        """
        Tạo tất cả test cases để thực nghiệm
        
        Returns:
            Dict mapping test_name -> (items, weights, values, capacity, description)
        """
        test_cases = {}
        
        # 1. By Region
        for region in ['North', 'South', 'East', 'West']:
            try:
                result = self.get_problem_by_region(region, capacity_ratio=0.5)
                test_cases[f'region_{region.lower()}'] = result
            except:
                pass
        
        # 2. By Category
        for category in ['Electronics', 'Clothing', 'Food', 'Furniture']:
            try:
                result = self.get_problem_by_category(category, capacity_ratio=0.5)
                test_cases[f'category_{category.lower()}'] = result
            except:
                pass
        
        # 3. By Size
        for size in ['small', 'medium', 'large', 'xlarge']:
            result = self.get_problem_by_size(size, capacity_ratio=0.5)
            test_cases[f'size_{size}'] = result
        
        # 4. By Capacity ratio
        for ratio, name in [(0.3, 'tight'), (0.5, 'medium'), (0.7, 'loose')]:
            df_sample = self.df.sample(n=50, random_state=42)
            items, weights, values, capacity = self.create_problem_instance(df_sample, capacity_ratio=ratio)
            description = f"Capacity {name.upper()} ({ratio*100:.0f}%) - {len(items)} items"
            test_cases[f'capacity_{name}'] = (items, weights, values, capacity, description)
        
        return test_cases
    
    def print_statistics(self):
        """In thống kê dữ liệu"""
        print("="*60)
        print("SALES DATA STATISTICS")
        print("="*60)
        print(f"Total Transactions: {len(self.df)}")
        print(f"\nRegions: {', '.join(self.df['Region'].unique())}")
        print(f"Categories: {', '.join(self.df['Product_Category'].unique())}")
        print(f"\nSales Amount Range: ${self.df['Sales_Amount'].min():.2f} - ${self.df['Sales_Amount'].max():.2f}")
        print(f"Avg Sales Amount: ${self.df['Sales_Amount'].mean():.2f}")
        print("="*60)


def load_data(excel_path='data/sales_data.xlsx'):
    """
    Wrapper function để load data
    
    Returns:
        SalesDataLoader instance
    """
    return SalesDataLoader(excel_path)
