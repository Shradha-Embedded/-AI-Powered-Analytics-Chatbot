import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

class SQLAgent:
    def __init__(self, schema_info):
        self.llm = ChatOpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            model="gpt-4",
            temperature=0
        )
        self.schema_info = schema_info
        self.schema_context = self._build_schema_context()

    def _build_schema_context(self):
        context = "Database Schema:\n\n"
        for table, columns in self.schema_info.items():
            context += f"Table: {table}\n"
            for col in columns:
                context += f" - {col['column']} ({col['type']})\n"
            context += "\n"
        return context

    def natural_language_to_sql(self, user_query):
        system_prompt = f"""
        You are a SQL expert. Convert natural language questions to PostgreSQL queries.
        
        {self.schema_context}
        
        Return only the SQL query, no explanations.
        """
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Convert this to SQL: {user_query}")
        ]
        
        response = self.llm(messages)
        sql_query = response.content.strip()
        
        if sql_query.startswith('```sql'):
            sql_query = sql_query[6:]
        if sql_query.endswith('```'):
            sql_query = sql_query[:-3]
            
        return sql_query.strip()

    def validate_sql_safety(self, sql_query):
        dangerous_ops = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER']
        sql_upper = sql_query.upper()
        
        for op in dangerous_ops:
            if op in sql_upper:
                return False, f"Dangerous operation: {op}"
        
        return True, "Safe query"

    def get_sample_queries(self):
        return [
            "Show me revenue by region",
            "Top 5 products by sales",
            "Monthly sales trends"
        ]