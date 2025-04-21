# Google Pandas Agent

A Google-native alternative to LangChain's create_pandas_dataframe_agent, powered by Google's Gemini models and LangGraph.

## Features

- Query pandas DataFrames using natural language
- Powered by Google's Gemini models
- Simple, intuitive interface
- Type-safe implementation
- Comprehensive error handling
- Support for multiple DataFrames

## Installation

```bash
pip install google-pandas-agent
```

## Requirements

- Python >= 3.10
- pandas >= 2.2
- google-generativeai >= 0.8.5
- langgraph >= 0.3.21

## Quick Start

```python
import pandas as pd
import google.generativeai as genai
from google_pandas_agent import create_pandas_dataframe_agent

# Initialize Gemini
genai.configure(api_key='your-api-key')  # Get your API key from Google Cloud Console
model = genai.GenerativeModel('gemini-pro')

# Create a sample DataFrame
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'London', 'Paris']
})

# Create the agent
agent = create_pandas_dataframe_agent(model, df)

# Ask questions about your data
response = agent.chat("What is the average age?")
print(response)

# You can also use multiple DataFrames
df2 = pd.DataFrame({
    'City': ['New York', 'London', 'Paris'],
    'Country': ['USA', 'UK', 'France']
})

agent = create_pandas_dataframe_agent(model, [df, df2])
response = agent.chat("Show me people's names along with their countries")
print(response)
```

## API Reference

### create_pandas_dataframe_agent

```python
def create_pandas_dataframe_agent(
    llm: genai.GenerativeModel,
    df: Union[pd.DataFrame, List[pd.DataFrame]],
    *,
    verbose: bool = False,
    allow_dangerous_code: bool = False,
    **kwargs,
) -> AgentExecutor
```

Creates an agent that can answer questions about pandas DataFrames.

#### Parameters

- `llm`: A Gemini model instance (must be initialized with `genai.GenerativeModel`)
- `df`: A pandas DataFrame or list of DataFrames
- `verbose`: Enable verbose output (default: False)
- `allow_dangerous_code`: Allow potentially unsafe imports in the Python REPL (default: False)
- `**kwargs`: Additional arguments passed to the executor

#### Returns

An `AgentExecutor` instance that can process natural language queries about the DataFrame(s)

### AgentExecutor

The main class for executing queries against DataFrames.

#### Methods

- `chat(question: str) -> str`: Process a natural language query and return the response
- `run(question: str) -> str`: Alias for chat()
- `invoke(state: dict) -> dict`: Advanced method for custom state handling

## Common Issues and Solutions

1. **Import Error**: If you get an error about missing dependencies, make sure you have all required packages installed:
   ```bash
   pip install "google-pandas-agent[all]"
   ```

2. **API Key Error**: Make sure to configure your Google API key before creating the model:
   ```python
   genai.configure(api_key='your-api-key')
   ```

3. **Model Error**: Ensure you're using the correct model name ('gemini-pro'):
   ```python
   model = genai.GenerativeModel('gemini-pro')
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- Ariamehr Maleki (ariamehr.mai@gmail.com)
- Frank Roh (frankagilepm@gmail.com)
- Darren North (denorth222@gmail.com) 