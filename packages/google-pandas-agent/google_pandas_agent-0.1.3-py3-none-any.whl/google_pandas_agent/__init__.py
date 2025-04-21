"""
Google Pandas Agent - A Google-native alternative to LangChain's create_pandas_dataframe_agent

This package provides a simple interface for querying pandas DataFrames using natural language,
powered by Google's Gemini models and LangGraph.

Example:
    >>> import pandas as pd
    >>> import google.generativeai as genai
    >>> from google_pandas_agent import create_pandas_dataframe_agent
    >>> 
    >>> # Initialize Gemini
    >>> genai.configure(api_key='your-api-key')
    >>> model = genai.GenerativeModel('gemini-pro')
    >>> 
    >>> # Create a sample DataFrame
    >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': ['x', 'y', 'z']})
    >>> 
    >>> # Create the agent
    >>> agent = create_pandas_dataframe_agent(model, df)
    >>> 
    >>> # Ask questions
    >>> response = agent.chat("How many rows are in the DataFrame?")
    >>> print(response)
"""

try:
    import google.generativeai as genai
except ImportError:
    raise ImportError(
        "google-generativeai is required to use google-pandas-agent. "
        "Please install it with: pip install google-generativeai>=0.8.5"
    )

try:
    import pandas as pd
except ImportError:
    raise ImportError(
        "pandas is required to use google-pandas-agent. "
        "Please install it with: pip install pandas>=2.2"
    )

try:
    import langgraph
except ImportError:
    raise ImportError(
        "langgraph is required to use google-pandas-agent. "
        "Please install it with: pip install langgraph>=0.3.21"
    )

from importlib.metadata import version as _v
from .executor import create_pandas_dataframe_agent, AgentExecutor  # public symbols

__all__ = ["create_pandas_dataframe_agent", "AgentExecutor"]
__version__ = _v(__name__) 