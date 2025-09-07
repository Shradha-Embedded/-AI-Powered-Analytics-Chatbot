# AI Analytics Chatbot

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.28.0-red.svg)
![LangChain](https://img.shields.io/badge/langchain-v0.0.350-green.svg)
![OpenAI](https://img.shields.io/badge/openai-gpt4-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

An intelligent chatbot that converts natural language questions into SQL queries, generates interactive visualizations, and provides AI-driven business insights using OpenAI GPT-4, LangChain, and Streamlit.

## 🎯 Features

- **Natural Language to SQL**: Convert questions like "Show me revenue by region" into PostgreSQL queries
- **Interactive Visualizations**: Automatic chart generation with Plotly (bar charts, line charts, scatter plots)
- **AI Business Insights**: GPT-4 powered analysis and actionable business recommendations
- **Real-time Analytics**: Instant query processing and results display
- **Dashboard Integration**: Power BI mock dashboard creation and export
- **Data Export**: Download results as CSV and JSON files
- **Query History**: Track and reuse previous queries
- **Safety Validation**: Prevents dangerous SQL operations

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI/ML**: LangChain, OpenAI GPT-4
- **Database**: PostgreSQL, SQLAlchemy
- **Visualization**: Plotly, Pandas
- **BI Integration**: Power BI REST API
- **Environment**: Python 3.8+

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-analytics-chatbot.git
   cd ai-analytics-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

4. **Initialize the database**
   ```bash
   psql -U your_username -d postgres -f database_setup.sql
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 📊 Usage Examples

### Sample Questions You Can Ask

- "Show me total revenue by region"
- "What are the top 5 products by sales volume?"
- "Compare actual vs forecast revenue for last quarter"
- "Which region has the best performance this year?"
- "Show me monthly sales trends"
- "Products with revenue above average"

### Expected Output

The chatbot will:
1. Convert your question to SQL automatically
2. Execute the query on your database
3. Display results in interactive charts
4. Generate 3 AI-powered business insights
5. Offer dashboard creation and data export options

## 📁 Project Structure

```
ai-analytics-chatbot/
├── app.py                 # Main Streamlit application
├── database.py           # Database connection and query execution
├── sql_agent.py          # Natural language to SQL conversion
├── powerbi_manager.py    # Power BI integration (mock version)
├── insight_generator.py  # AI-powered business insights
├── requirements.txt      # Python dependencies
├── database_setup.sql    # Database schema and sample data
├── .env.example         # Environment variables template
├── .gitignore          # Git exclusions
└── README.md           # Project documentation
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following:

```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=postgresql://username:password@localhost:5432/analytics_demo
```

### Database Schema

The application expects these PostgreSQL tables:
- `regions` - Geographic regions
- `products` - Product catalog  
- `sales_data` - Sales transactions with revenue and forecast data

Run `database_setup.sql` to create the schema with sample data.

## 🎨 Screenshots

### Main Interface
![Main Interface](https://via.placeholder.com/800x400?text=AI+Analytics+Chatbot+Interface)

### Query Results with Insights
![Results](https://via.placeholder.com/800x400?text=Query+Results+and+AI+Insights)

## 🌐 Live Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

**Try it live**: [AI Analytics Chatbot Demo](https://your-app-url.streamlit.app)

## 🔄 API Integration

The system can be extended to work with various databases and BI tools:

```python
from sql_agent import SQLAgent
from database import DatabaseManager

# Initialize components
db = DatabaseManager()
agent = SQLAgent(db.get_schema_info())

# Convert natural language to SQL
sql = agent.natural_language_to_sql("Show me revenue by region")
results, error = db.execute_query(sql)
```

## 🚀 Deployment

### Streamlit Cloud
1. Push your code to GitHub
2. Connect your repository to [Streamlit Cloud](https://share.streamlit.io)
3. Add environment variables in the dashboard
4. Deploy with one click

### Docker
```bash
docker build -t ai-analytics-chatbot .
docker run -p 8501:8501 --env-file .env ai-analytics-chatbot
```

### Local Development
```bash
streamlit run app.py --server.runOnSave true
```

## 🛡️ Security Features

- Environment variables for sensitive data
- SQL injection prevention through parameterized queries
- Input validation and sanitization
- Query safety validation (blocks dangerous operations)
- API rate limiting and error handling

## 🔍 Troubleshooting

### Common Issues

**Database Connection Errors**
- Check your `DATABASE_URL` format
- Verify PostgreSQL is running
- Confirm database and tables exist

**OpenAI API Issues**
- Verify your API key is valid
- Check your usage quota
- Ensure you have GPT-4 access

**Import Errors**
- Run `pip install -r requirements.txt`
- Check Python version (3.8+ required)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
pip install black flake8 pytest
black .                    # Format code
flake8 .                  # Run linter
pytest                    # Run tests
```

## 📈 Roadmap

- [ ] Multi-database support (MySQL, SQLite, BigQuery)
- [ ] Advanced chart types and customization
- [ ] User authentication and access control
- [ ] Scheduled report generation
- [ ] Email/Slack notifications
- [ ] Voice input capabilities
- [ ] Mobile responsive design improvements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments


- [LangChain](https://langchain.com) for SQL generation framework
- [Streamlit](https://streamlit.io) for the web application framework
- [Plotly](https://plotly.com) for interactive visualizations


## 🏷️ GitHub Topics/Tags

Add these topics to your GitHub repository for better discoverability:

```
ai
chatbot
streamlit
langchain
openai
gpt-4
sql
analytics
business-intelligence
python
data-visualization
natural-language-processing
plotly
postgresql
power-bi
dashboard
data-science
machine-learning
artificial-intelligence
database-queries
business-analytics
```

---

**Built with  by [shradha](https://github.com/Shradha-Embedded)**

[![GitHub stars](https://img.shields.io/github/stars/yourusername/ai-analytics-chatbot.svg?style=social&label=Star)](https://github.com/yourusername/ai-analytics-chatbot)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/ai-analytics-chatbot.svg?style=social&label=Fork)](https://github.com/yourusername/ai-analytics-chatbot/fork)