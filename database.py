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
        self.engine = create_engine(self.connection_string)
        self.mock_mode = False

    def execute_query(self, query):
        if self.mock_mode:
            # Return sample data for demo
            sample_data = pd.DataFrame({
                'region_name': ['North America', 'Europe', 'Asia Pacific'],
                'total_revenue': [150000, 120000, 98000]
            })
            return sample_data, None
        
        try:
            df = pd.read_sql_query(query, self.engine)
            return df, None
        except Exception as e:
            return None, str(e)
