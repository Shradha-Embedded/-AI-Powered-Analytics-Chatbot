import os
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.connection_string = os.getenv('DATABASE_URL')
        self.engine = create_engine(self.connection_string)

    def execute_query(self, query):
        """Execute SQL query and return results as DataFrame"""
        try:
            df = pd.read_sql_query(query, self.engine)
            return df, None
        except Exception as e:
            return None, str(e)

    def get_schema_info(self):
        """Get database schema information for LangChain"""
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
            return None

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