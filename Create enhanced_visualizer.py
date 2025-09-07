# enhanced_visualizer.py - Advanced local visualizations
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import streamlit as st

class EnhancedVisualizer:
    def __init__(self):
        self.color_palette = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#FFB347']
    
    def create_dashboard_style_viz(self, df, query_type="general"):
        """Create professional dashboard-style visualizations"""
        
        if df.empty:
            return None
        
        # Detect data types
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        date_cols = df.select_dtypes(include=['datetime']).columns.tolist()
        
        # Create appropriate visualization based on data structure
        if self._is_revenue_data(df):
            return self._create_revenue_dashboard(df)
        elif self._is_time_series(df):
            return self._create_time_series_chart(df)
        elif len(numeric_cols) >= 1 and len(categorical_cols) >= 1:
            return self._create_category_analysis(df, categorical_cols[0], numeric_cols[0])
        else:
            return self._create_generic_chart(df)
    
    def _is_revenue_data(self, df):
        """Detect if this is revenue-related data"""
        revenue_keywords = ['revenue', 'sales', 'income', 'profit', 'earnings']
        return any(keyword in col.lower() for col in df.columns for keyword in revenue_keywords)
    
    def _is_time_series(self, df):
        """Detect if this is time series data"""
        date_keywords = ['date', 'time', 'month', 'year', 'day']
        return any(keyword in col.lower() for col in df.columns for keyword in date_keywords)
    
    def _create_revenue_dashboard(self, df):
        """Create a revenue-focused dashboard"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Revenue Overview', 'Top Performers', 'Trend Analysis', 'Distribution'),
            specs=[[{"type": "bar"}, {"type": "pie"}],
                   [{"type": "scatter"}, {"type": "histogram"}]]
        )
        
        # Main bar chart
        if 'revenue' in df.columns.str.lower():
            revenue_col = [col for col in df.columns if 'revenue' in col.lower()][0]
            category_col = df.select_dtypes(include=['object']).columns[0] if len(df.select_dtypes(include=['object']).columns) > 0 else df.columns[0]
            
            fig.add_trace(
                go.Bar(x=df[category_col], y=df[revenue_col], 
                      marker_color=self.color_palette[0]),
                row=1, col=1
            )
            
            # Pie chart for distribution
            fig.add_trace(
                go.Pie(labels=df[category_col], values=df[revenue_col],
                      marker_colors=self.color_palette[:len(df)]),
                row=1, col=2
            )
        
        fig.update_layout(
            height=600,
            title_text="📊 Revenue Analytics Dashboard",
            showlegend=False
        )
        
        return fig
    
    def _create_time_series_chart(self, df):
        """Create time series visualization"""
        date_col = df.select_dtypes(include=['datetime']).columns[0] if len(df.select_dtypes(include=['datetime']).columns) > 0 else None
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if date_col and numeric_cols:
            fig = px.line(df, x=date_col, y=numeric_cols[0], 
                         title=f"📈 {numeric_cols[0]} Over Time",
                         color_discrete_sequence=self.color_palette)
        else:
            fig = px.line(df, y=numeric_cols[0] if numeric_cols else df.columns[0],
                         title="📈 Trend Analysis",
                         color_discrete_sequence=self.color_palette)
        
        fig.update_layout(height=500)
        return fig
    
    def _create_category_analysis(self, df, cat_col, num_col):
        """Create category-based analysis"""
        # Sort by values for better visualization
        df_sorted = df.sort_values(num_col, ascending=False)
        
        fig = px.bar(df_sorted, x=cat_col, y=num_col,
                    title=f"📊 {num_col} by {cat_col}",
                    color=num_col,
                    color_continuous_scale='Viridis')
        
        fig.update_layout(
            height=500,
            xaxis_tickangle=-45
        )
        
        return fig
    
    def _create_generic_chart(self, df):
        """Create a generic chart for any data"""
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if len(numeric_cols) >= 2:
            fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1],
                           title=f"📊 {numeric_cols[1]} vs {numeric_cols[0]}",
                           color_discrete_sequence=self.color_palette)
        elif len(numeric_cols) == 1:
            fig = px.histogram(df, x=numeric_cols[0],
                             title=f"📊 Distribution of {numeric_cols[0]}",
                             color_discrete_sequence=self.color_palette)
        else:
            # For non-numeric data, create a count plot
            first_col = df.columns[0]
            counts = df[first_col].value_counts()
            fig = px.bar(x=counts.index, y=counts.values,
                        title=f"📊 Count of {first_col}",
                        color_discrete_sequence=self.color_palette)
        
        fig.update_layout(height=500)
        return fig
    
    def create_summary_metrics(self, df):
        """Create summary metrics cards"""
        metrics = []
        numeric_cols = df.select_dtypes(include=['number']).columns
        
        for col in numeric_cols[:4]:  # Show top 4 metrics
            total = df[col].sum()
            avg = df[col].mean()
            metrics.append({
                'name': col.title(),
                'total': f"{total:,.0f}",
                'average': f"{avg:,.0f}",
                'max': f"{df[col].max():,.0f}",
                'min': f"{df[col].min():,.0f}"
            })
        
        return metrics