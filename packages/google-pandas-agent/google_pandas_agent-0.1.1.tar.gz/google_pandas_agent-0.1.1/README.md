# Google Pandas Agent

A Google-native alternative to LangChain's create_pandas_dataframe_agent, powered by Gemini and LangGraph.

## Installation

```bash
pip install google-pandas-agent
```

## Quick Start

```python
import pandas as pd
import google.generativeai as genai
from google_pandas_agent import create_pandas_dataframe_agent

# Configure Gemini
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-2.0-pro")

# Load your data
df = pd.read_csv("your_data.csv")

# Create the agent
agent = create_pandas_dataframe_agent(model, df, allow_dangerous_code=False)

# Ask questions about your data
response = agent.run("What is the average value in column X?")
print(response)
```

## Features

- 🚀 Powered by Google's Gemini API and LangGraph
- 🔒 Secure Python AST-based code execution
- 📊 Support for single or multiple DataFrames
- 🎯 Simple, LangChain-compatible interface
- 🛡️ Safe by default with optional dangerous code allowance

## Security Note

By default, the agent runs in a secure mode that prevents potentially dangerous imports. If you need to allow specific imports, use `allow_dangerous_code=True`, but be aware of the security implications.

## License

MIT License - see LICENSE file for details.

## Authors

- Ariamehr Maleki (ariamehr.mai@gmail.com)
- Frank Roh (frankagilepm@gmail.com)
- Darren North (denorth222@gmail.com)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 