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
            system_prompt = """You are a business analyst. Generate exactly 3 actionable business insights. Format as: 1. insight 2. insight 3. insight"""
            user_prompt = f"Query: {original_query}\nData: {df.head(3).to_string()}\nGenerate 3 business insights."
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self.llm(messages)
            insights = self._parse_insights(response.content)
            return insights
            
        except Exception as e:
            return self._get_fallback_insights(df, original_query)

    def _parse_insights(self, response_text):
        lines = response_text.strip().split('\n')
        insights = []
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith('1.') or line.startswith('2.') or line.startswith('3.')):
                insight = line[2:].strip()
                if insight:
                    insights.append(insight)
        
        if len(insights) < 3:
            insights.extend(self._get_fallback_insights(None, "")[:3-len(insights)])
        
        return insights[:3]

    def _get_fallback_insights(self, df, query):
        return [
            "Analyze trends over time to identify growth opportunities.",
            "Focus on top-performing segments to maximize ROI.",
            "Monitor key metrics regularly for performance tracking."
        ]
