import streamlit as st
import plotly.express as px
import pandas as pd
import logging
from datetime import datetime

# Import our custom modules
try:
    from database import DatabaseManager
    from sql_agent import SQLAgent
    from powerbi_manager import PowerBIManager
    from insight_generator import InsightGenerator
except ImportError as e:
    st.error(f"Import Error: {e}")
    st.stop()

# Configure Streamlit page
st.set_page_config(
    page_title="AI Analytics Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'query_history' not in st.session_state:
    st.session_state.query_history = []

@st.cache_resource
def init_components():
    try:
        db = DatabaseManager()
        schema_info = db.get_schema_info()
        if not schema_info:
            st.error("Failed to retrieve database schema.")
            return None, None, None, None
        
        sql_agent = SQLAgent(schema_info)
        powerbi = PowerBIManager()
        insight_gen = InsightGenerator()
        
        return db, sql_agent, powerbi, insight_gen
        
    except Exception as e:
        st.error(f"Failed to initialize components: {str(e)}")
        return None, None, None, None

def create_visualization(df):
    if df is None or df.empty:
        return None
    
    try:
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if len(categorical_cols) >= 1 and len(numeric_cols) >= 1:
            fig = px.bar(
                df,
                x=categorical_cols[0],
                y=numeric_cols[0],
                title=f"{numeric_cols[0]} by {categorical_cols[0]}"
            )
            return fig
        elif len(numeric_cols) >= 2:
            fig = px.scatter(
                df,
                x=numeric_cols[0],
                y=numeric_cols[1],
                title=f"{numeric_cols[1]} vs {numeric_cols[0]}"
            )
            return fig
        else:
            return None
            
    except Exception as e:
        st.error(f"Error creating visualization: {str(e)}")
        return None

def main():
    st.title("🤖 AI-Powered Analytics Chatbot")
    st.markdown("Ask questions about your data in plain English!")
    
    # Initialize components
    with st.spinner("Initializing system components..."):
        db, sql_agent, powerbi, insight_gen = init_components()
    
    if not all([db, sql_agent, powerbi, insight_gen]):
        st.error("Failed to initialize required components.")
        st.stop()
    
    # Sidebar with sample queries
    with st.sidebar:
        st.header("📝 Sample Queries")
        
        sample_queries = [
            "Show me revenue by region",
            "What are the top 5 products by sales?",
            "Compare actual vs forecast revenue",
            "Show monthly sales trends"
        ]
        
        for query in sample_queries:
            if st.button(query, key=f"sample_{hash(query)}"):
                st.session_state.user_query = query
    
    # Main interface
    user_query = st.text_input(
        "Ask your question:",
        value=st.session_state.get('user_query', ''),
        placeholder="e.g., Show me revenue by region"
    )
    
    if st.button("🔍 Analyze", type="primary"):
        if user_query:
            # Add to history
            if user_query not in st.session_state.query_history:
                st.session_state.query_history.append(user_query)
            
            with st.spinner("Processing your query..."):
                try:
                    # Convert natural language to SQL
                    sql_query = sql_agent.natural_language_to_sql(user_query)
                    
                    # Validate SQL for safety
                    is_safe, safety_msg = sql_agent.validate_sql_safety(sql_query)
                    
                    if not is_safe:
                        st.error(f"Query Safety Check Failed: {safety_msg}")
                        st.stop()
                    
                    # Display generated SQL
                    with st.expander("🔧 Generated SQL Query"):
                        st.code(sql_query, language='sql')
                    
                    # Execute query
                    df, error = db.execute_query(sql_query)
                    
                    if error:
                        st.error(f"Database Error: {error}")
                        
                    elif df is not None and not df.empty:
                        st.success(f"✅ Query executed successfully! Found {len(df)} records.")
                        
                        # Create layout for results
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.subheader("📊 Results")
                            
                            # Create and display visualization
                            fig = create_visualization(df)
                            if fig:
                                st.plotly_chart(fig, use_container_width=True)
                            
                            # Show data table
                            st.subheader("📋 Data Table")
                            st.dataframe(df, use_container_width=True)
                            
                            # Data download
                            csv = df.to_csv(index=False)
                            st.download_button(
                                label="📥 Download as CSV",
                                data=csv,
                                file_name=f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                mime="text/csv"
                            )
                        
                        with col2:
                            st.subheader("🧠 AI Insights")
                            
                            # Generate AI insights
                            with st.spinner("Generating insights..."):
                                insights = insight_gen.generate_insights(df, user_query)
                            
                            for i, insight in enumerate(insights, 1):
                                st.write(f"**{i}.** {insight}")
                            
                            st.divider()
                            
                            # Power BI integration
                            st.subheader("📈 Dashboard")
                            
                            if st.button("Create Dashboard"):
                                with st.spinner("Creating dashboard..."):
                                    dataset_id = powerbi.create_dataset_from_dataframe(
                                        df,
                                        f"Analytics_{user_query[:20]}",
                                        "QueryResults"
                                    )
                                    
                                    if dataset_id:
                                        st.success("✅ Dashboard created!")
                                        embed_url = powerbi.get_embed_url(dataset_id)
                                        st.markdown(f"🔗 [View Dashboard]({embed_url})")
                                    else:
                                        st.error("❌ Failed to create dashboard")
                    
                    else:
                        st.warning("No data found for your query.")
                        
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()