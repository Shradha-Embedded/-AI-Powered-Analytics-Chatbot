import pandas as pd
import logging

class InsightGenerator:
    def __init__(self):
        """Demo version - no OpenAI required"""
        self.demo_mode = True
        logging.info("Insight Generator initialized in demo mode")

    def generate_insights(self, df, original_query):
        """Generate business insights - Demo version with predefined insights"""
        if df is None or df.empty:
            return ["No data available for analysis."]
        
        query_lower = original_query.lower()
        
        # Generate insights based on query type and data
        if "revenue by region" in query_lower:
            return [
                "North America leads with the highest revenue performance, indicating strong market presence and customer adoption.",
                "Consider expanding successful North American strategies to underperforming regions like Latin America for growth opportunities.",
                "Implement region-specific marketing campaigns to leverage the revenue distribution patterns identified in the data."
            ]
        
        elif "top" in query_lower and "product" in query_lower:
            return [
                "Electronics category dominates sales performance, suggesting strong demand for technology products in your market.",
                "Focus inventory and marketing investments on top-performing products to maximize ROI and customer satisfaction.",
                "Analyze successful product features to inform future product development and category expansion strategies."
            ]
        
        elif "monthly" in query_lower and ("trend" in query_lower or "sales" in query_lower):
            return [
                "Monthly sales show seasonal patterns that can be leveraged for strategic planning and inventory management.",
                "Identify peak months to optimize staffing, marketing spend, and supply chain operations for maximum efficiency.",
                "Use trend data to set realistic quarterly targets and allocate resources during high and low-demand periods."
            ]
        
        elif "forecast" in query_lower:
            return [
                "Forecast accuracy varies by region, indicating opportunities to improve prediction models and planning processes.",
                "Regions with consistent forecast performance can serve as models for improving prediction accuracy elsewhere.",
                "Regular forecast review meetings should be implemented to adjust strategies based on actual vs predicted performance."
            ]
        
        else:
            # General insights for any other query
            return [
                f"Data analysis reveals {len(df)} records with clear performance patterns across different segments.",
                "Focus on top-performing areas while investigating underperforming segments for improvement opportunities.",
                "Implement regular monitoring dashboards to track these metrics and identify trends early for strategic advantage."
            ]

    def generate_insight_summary(self, insights):
        """Generate a formatted summary of insights"""
        if not insights:
            return "No insights available."
        
        summary = "Key Business Insights:\n\n"
        for i, insight in enumerate(insights, 1):
            summary += f"{i}. {insight}\n\n"
        
        return summary

    def get_insight_categories(self, insights):
        """Categorize insights by type"""
        return {
            'performance': insights[:1] if insights else [],
            'opportunities': insights[1:2] if len(insights) > 1 else [],
            'recommendations': insights[2:] if len(insights) > 2 else []
        }
