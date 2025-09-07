import pandas as pd
import json
import os
from datetime import datetime
import logging

class PowerBIManager:
    def __init__(self):
        self.mock_mode = True
        self.datasets_created = []
        self.base_url = "https://app.powerbi.com"
        
        logging.info("Power BI Manager initialized in mock mode")

    def test_connection(self):
        return True

    def create_dataset_from_dataframe(self, df, dataset_name, table_name="QueryResults"):
        if df is None or df.empty:
            return None
        
        try:
            mock_dataset_id = f"mock_dataset_{len(self.datasets_created) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            dataset_info = {
                'id': mock_dataset_id,
                'name': dataset_name,
                'table_name': table_name,
                'created_at': datetime.now().isoformat(),
                'row_count': len(df),
                'columns': list(df.columns)
            }
            
            self.datasets_created.append(dataset_info)
            logging.info(f"Mock Power BI dataset created: {mock_dataset_id}")
            
            return mock_dataset_id
            
        except Exception as e:
            logging.error(f"Error creating mock dataset: {str(e)}")
            return None

    def get_embed_url(self, dataset_id):
        demo_url = "https://app.powerbi.com/view?r=eyJrIjoiZjE2YjY5ZDQtZTY5NC00ZGI3LWE3ZGQtMzQ4YWY0MjkxZjU5IiwidCI6IjhlOTVhNzlhLWJlNDAtNGRjNi1hYzRhLTZhYzFlODM5YWM4ZSIsImMiOjN9"
        return demo_url

    def generate_dashboard_summary(self, dataset_id):
        dataset_info = self.get_dataset_info(dataset_id)
        if not dataset_info:
            return "Dataset not found"
        
        summary = f"""
📊 Power BI Dashboard Summary for: {dataset_info['name']}

📈 Dataset Overview:
- Created: {dataset_info['created_at']}
- Rows: {dataset_info['row_count']:,}
- Columns: {len(dataset_info['columns'])}

📋 Available Columns:
{chr(10).join([f"• {col}" for col in dataset_info['columns']])}
        """
        
        return summary.strip()

    def get_dataset_info(self, dataset_id):
        for dataset in self.datasets_created:
            if dataset['id'] == dataset_id:
                return dataset.copy()
        return None