"""
Agent Executor implementation for Google Pandas Agent
"""

from typing import Any, Union, List
import pandas as pd
import google.generativeai as genai
from google_pandas_agent.graph import build_agent_graph


class AgentExecutor:
    """
    Main executor class for Google Pandas Agent.
    Provides a simple interface similar to LangChain's AgentExecutor.
    """

    def __init__(self, graph, question_key: str = "messages"):
        self._graph = graph
        self._question_key = question_key

    def run(self, question: str) -> str:
        """Run a single question through the agent"""
        state = self._graph.invoke({self._question_key: [question]})
        return state["messages"][-1]

    def chat(self, question: str) -> str:
        """Alias for run() to maintain compatibility"""
        return self.run(question)

    def invoke(self, state: dict) -> dict:
        """Advanced access for streaming/custom state handling"""
        return self._graph.invoke(state)


def create_pandas_dataframe_agent(
    llm: genai.GenerativeModel,
    df: Union[pd.DataFrame, List[pd.DataFrame]],
    *,
    verbose: bool = False,
    allow_dangerous_code: bool = False,
    **kwargs,
) -> AgentExecutor:
    """
    Create a Pandas DataFrame agent powered by Google's Gemini and LangGraph.

    Args:
        llm: A Gemini model instance (must be initialized with genai.GenerativeModel)
        df: A pandas DataFrame or list of DataFrames
        verbose: Enable verbose output
        allow_dangerous_code: Allow potentially unsafe imports in the Python REPL
        **kwargs: Additional arguments passed to the executor

    Returns:
        An AgentExecutor instance that can process natural language queries about the DataFrame

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
    # Validate inputs
    if not isinstance(llm, genai.GenerativeModel):
        raise TypeError("llm must be an instance of google.generativeai.GenerativeModel")
    
    if isinstance(df, pd.DataFrame):
        dfs = [df]
    elif isinstance(df, list) and all(isinstance(d, pd.DataFrame) for d in df):
        dfs = df
    else:
        raise TypeError("df must be a pandas DataFrame or a list of DataFrames")

    graph = build_agent_graph(llm, dfs, allow_dangerous_code=allow_dangerous_code)
    return AgentExecutor(graph) 