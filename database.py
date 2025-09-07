import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

try:
    import psycopg2
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False

class DatabaseManager:
    def __init__(self):
        if not PSYCOPG2_AVAILABLE:
            self.mock_mode = True
            return
        
        self.connection_string = os.getenv('DATABASE_URL')
        if self.connection_string:
            self.engine = create_engine(self.connection_string)
            self.mock_mode = False
        else:
            self.mock_mode = True

    def execute_query(self, query):
        """Execute SQL query and return results as DataFrame"""
        if self.mock_mode:
            # Return sample data for demo
            sample_data = pd.DataFrame({
                'region_name': ['North America', 'Europe', 'Asia Pacific', 'Latin America'],
                'total_revenue': [150000, 120000, 98000, 75000],
                'units_sold': [1500, 1200, 980, 750]
            })
            return sample_data, None
        
        try:
            df = pd.read_sql_query(query, self.engine)
            return df, None
        except Exception as e:
            return None, str(e)

    def get_schema_info(self):
        """Get database schema information for LangChain"""
        if self.mock_mode:
            # Return mock schema for demo
            return {
                'regions': [
                    {'column': 'region_id', 'type': 'integer'},
                    {'column': 'region_name', 'type': 'varchar'}
                ],
                'products': [
                    {'column': 'product_id', 'type': 'integer'},
                    {'column': 'product_name', 'type': 'varchar'},
                    {'column': 'category', 'type': 'varchar'}
                ],
                'sales_data': [
                    {'column': 'sale_id', 'type': 'integer'},
                    {'column': 'region_id', 'type': 'integer'},
                    {'column': 'product_id', 'type': 'integer'},
                    {'column': 'sale_date', 'type': 'date'},
                    {'column': 'revenue', 'type': 'numeric'},
                    {'column': 'forecast', 'type': 'numeric'},
                    {'column': 'units_sold', 'type': 'integer'}
                ]
            }
        
        schema_query = """
        SELECT
            table_name,
            column_name,
            data_type,
            is_nullable
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
        """
        
        df, error = self.execute_query(schema_query)
        if error:
            return self.get_schema_info()  # Fallback to mock schema

        schema_info = {}
        for _, row in df.iterrows():
            table = row['table_name']
            if table not in schema_info:
                schema_info[table] = []
            schema_info[table].append({
                'column': row['column_name'],
                'type': row['data_type']
            })
        return schema_info
