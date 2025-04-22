# InsightAI

A powerful open-source library that enables natural language conversations with data using Large Language Models (LLMs). Perfect for data analysis, research, and insights generation with zero-code requirements.

## 🚀 Key Features

- **Natural Language Interface**: Ask questions about your data in plain English
- **Multiple Model Support**: Works with OpenAI, Groq, and other LLM providers
- **Smart Data Analysis**: Automatic code generation for data analysis and visualization
- **Error Handling**: Built-in debugging and error correction mechanisms
- **Detailed Logging**: Comprehensive logging of all LLM interactions and costs
- **SQL Support**: Native support for SQL databases and queries
- **Customizable**: Configurable model settings and prompt templates

## 📦 Installation

```bash
pip install insightai
```

## 🔑 Configuration

### Required API Keys

```bash
# Required environment variables
export OPENAI_API_KEY="your-openai-api-key"
export GROQ_API_KEY="your-groq-api-key"
```

### Optional Configuration Files

1. **LLM_CONFIG.json** - Configure model settings per agent:
```json
{
    "agent": "Code Generator",
    "details": {
        "model": "gpt-4o-mini",
        "provider": "openai",
        "max_tokens": 2000,
        "temperature": 0
    }
}
```

2. **PROMPT_TEMPLATES.json** - Customize agent prompts

## 💡 Usage Examples

### Basic Usage with DataFrame

```python
import pandas as pd
from insightai import InsightAI

# Load your data
df = pd.read_csv('sales_data.csv')

# Initialize InsightAI
insight = InsightAI(df, debug=False)

# Single question
insight.pd_agent_converse("What is the total revenue by product category?")

# Interactive mode
insight.pd_agent_converse()
```

### SQL Database Analysis

```python
from insightai import InsightAI

# Initialize with SQLite database
insight = InsightAI(db_path='database.db')

# Analyze your data
insight.pd_agent_converse("Show me the top 10 customers by order value")
```

## 🔧 Advanced Configuration

### Constructor Parameters

```python
InsightAI(
    df=None,                    # DataFrame object
    db_path=None,              # Path to SQL database
    max_conversations=4,        # Number of conversation pairs to remember
    debug=False,               # Enable debugging mode
    exploratory=True,          # Enable exploratory analysis
    df_ontology=False          # Enable data ontology support
)
```

### Supported LLM Providers

- OpenAI
  - GPT-4
  - GPT-3.5-turbo
- Groq
  - LLama-70B
  - Mixtral-8x7B

## 📊 Example Output

### Data Analysis
```python
Question: "Analyze the sales trend over the last 6 months"

# Generated Analysis
1. Monthly Sales Trend
2. Top Products by Revenue
3. Regional Performance
4. Growth Rate Analysis
```

### SQL Query
```python
Question: "Find customers who spent over $1000"

# Generated SQL
SELECT 
    c.customer_name,
    SUM(o.total_amount) as total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id
HAVING total_spent > 1000
ORDER BY total_spent DESC;
```

## 📝 Logging

All interactions are logged in `insightai_consolidated_log.json`:

```json
{
    "chain_id": "1234567890",
    "details": {
        "model": "gpt-4o-mini",
        "tokens_used": 1500,
        "cost": 0.03,
        "duration": "2.3s"
    }
}
```

## 🗂️ Project Structure

```
insightai/
  ├── __init__.py
  ├── insightai.py          # Main class implementation
  ├── models.py             # LLM provider integrations
  ├── prompts.py           # System prompts
  ├── utils.py             # Utility functions
  ├── log_manager.py       # Logging system
  ├── output_manager.py    # Output formatting
  ├── reg_ex.py           # Regular expressions
  ├── func_calls.py       # Function definitions
  └── groq_models.py      # Groq-specific implementation
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

### Development Setup

```bash
git clone https://github.com/LeoRigasaki/InSightAI.git
cd insightai
pip install -e ".[dev]"
```

## ⚠️ Known Limitations

- Token limits based on model selection
- Rate limiting from API providers
- Memory constraints for large datasets

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

## 🙏 Acknowledgments

- Special thanks to [pgalko](https://github.com/pgalko/BambooAI) for the original inspiration and foundation
- OpenAI for API access
- Groq for high-performance inference
- Open-source community contributions