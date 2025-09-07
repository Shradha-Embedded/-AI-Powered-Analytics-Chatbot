import os
from dotenv import load_dotenv

load_dotenv()

class SQLAgent:
    def __init__(self, schema_info):
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
        """Convert natural language to SQL query - Demo version with predefined queries"""
        query_lower = user_query.lower()
        
        # Predefined SQL queries for common questions
        if "revenue by region" in query_lower:
            return "SELECT region_name, SUM(total_revenue) as total_revenue FROM sales_data s JOIN regions r ON s.region_id = r.region_id GROUP BY region_name ORDER BY total_revenue DESC;"
        
        elif "top" in query_lower and ("product" in query_lower or "5" in query_lower):
            return "SELECT product_name, SUM(total_revenue) as total_revenue FROM sales_data s JOIN products p ON s.product_id = p.product_id GROUP BY product_name ORDER BY total_revenue DESC LIMIT 5;"
        
        elif "monthly" in query_lower and ("trend" in query_lower or "sales" in query_lower):
            return "SELECT DATE_TRUNC('month', sale_date) as month, SUM(total_revenue) as monthly_revenue FROM sales_data GROUP BY DATE_TRUNC('month', sale_date) ORDER BY month;"
        
        elif "actual" in query_lower and "forecast" in query_lower:
            return "SELECT SUM(total_revenue) as actual_revenue, SUM(forecast) as forecast_revenue, SUM(total_revenue) - SUM(forecast) as variance FROM sales_data;"
        
        elif "category" in query_lower:
            return "SELECT category, SUM(total_revenue) as category_revenue FROM sales_data s JOIN products p ON s.product_id = p.product_id GROUP BY category ORDER BY category_revenue DESC;"
        
        else:
            # Default query for any other question
            return "SELECT region_name, total_revenue, units_sold FROM sales_data s JOIN regions r ON s.region_id = r.region_id LIMIT 10;"

    def validate_sql_safety(self, sql_query):
        """Validate SQL for safety"""
        dangerous_ops = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER']
        sql_upper = sql_query.upper()
        
        for op in dangerous_ops:
            if op in sql_upper:
                return False, f"Dangerous operation: {op}"
        
        return True, "Safe query"

    def get_sample_queries(self):
        """Return sample queries"""
        return [
            "Show me revenue by region",
            "What are the top 5 products by sales?",
            "Show monthly sales trends",
            "Compare actual vs forecast revenue"
        ]
