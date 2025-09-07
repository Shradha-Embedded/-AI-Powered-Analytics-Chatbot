import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import pandas as pd
from dotenv import load_dotenv
import logging

load_dotenv()

class InsightGenerator:
    def __init__(self):
        try:
            self.llm = ChatOpenAI(
                api_key=os.getenv('OPENAI_API_KEY'),
                model="gpt-4",
                temperature=0.3
            )
            logging.info("AI Insight Generator initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize InsightGenerator: {str(e)}")
            self.llm = None

    def generate_insights(self, df, original_query):
        if df is None or df.empty:
            return ["No data available for analysis."]
        
        if not self.llm:
            return self._get_fallback_insights(df, original_query)
        
        try:
            data_summary = self._prepare_data_summary(df)
            
            system_prompt = """
            You are a business analyst AI. Analyze the provided data and generate exactly 3 actionable business insights.
            
            Guidelines:
            1. Focus on practical, actionable recommendations
            2. Identify trends, patterns, or opportunities
            3. Keep insights concise (1-2 sentences each)
            4. Use business terminology
            
            Format your response as exactly 3 insights, numbered 1-3.
            """

            user_prompt = f"""
            Original Query: {original_query}
            
            Data Summary:
            {data_summary}
            
            Sample Data:
            {df.head(10).to_string()}
            
            Generate 3 specific, actionable business insights based on this data.
            """

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]

            response = self.llm(messages)
            insights = self._parse_insights(response.content)
            
            logging.info(f"Generated {len(insights)} AI insights")
            return insights
            
        except Exception as e:
            logging.error(f"Error generating AI insights: {str(e)}")
            return self._get_fallback_insights(df, original_query)

    def _prepare_data_summary(self, df):
        summary = f"Dataset Overview: {df.shape[0]} rows, {df.shape[1]} columns\n\n"
        
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            summary += "NUMERIC METRICS:\n"
            for col in numeric_cols:
                stats = df[col].describe()
                summary += f"• {col}: avg={stats['mean']:.2f}, min={stats['min']:.2f}, max={stats['max']:.2f}\n"
        
        categorical_cols = df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            summary += "\nCATEGORICAL DATA:\n"
            for col in categorical_cols:
                unique_count = df[col].nunique()
                summary += f"• {col}: {unique_count} unique values\n"
        
        return summary

    def _parse_insights(self, response_text):
        lines = response_text.strip().split('\n')
        insights = []
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith('1.') or line.startswith('2.') or line.startswith('3.')):
                insight = line[2:].strip()
                insights.append(insight)
        
        if len(insights) < 3:
            insights.extend(self._get_fallback_insights(None, "")[:3-len(insights)])
        
        return insights[:3]

    def _get_fallback_insights(self, df, query):
        return [
            "Analyze trends over time to identify growth opportunities and optimize resource allocation.",
            "Focus on top-performing segments while investigating underperforming areas for improvement potential.",
            "Establish regular monitoring and benchmarking processes to track progress against targets."
        ]