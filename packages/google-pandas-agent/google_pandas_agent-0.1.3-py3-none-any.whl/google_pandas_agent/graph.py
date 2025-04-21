"""
LangGraph implementation for Google Pandas Agent
"""

from typing import Any
import google.generativeai as genai
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict, Annotated
from google_pandas_agent.prompt import build_prompt
from google_pandas_agent.tools import build_tool_node


class AgentState(TypedDict):
    """State type for the agent graph"""
    messages: Annotated[list, add_messages]
    finished: bool


def build_agent_graph(llm: genai.GenerativeModel, dfs: Any, allow_dangerous_code=False):
    """Build the agent graph with LangGraph"""
    sg = StateGraph(AgentState)

    # tool node
    tool_node = build_tool_node(dfs, allow_dangerous_code)
    sg.add_node("tools", tool_node)

    # chat node
    def chat(state: AgentState) -> AgentState:
        q = state["messages"][-1]  # last user question
        prompt = build_prompt(q, dfs)
        resp = llm.generate_content(prompt)
        return {"messages": [resp.text]}

    sg.add_node("chat", chat)

    # wiring
    sg.add_edge(START, "chat")
    sg.add_edge("chat", "tools")
    sg.add_edge("tools", "chat")
    sg.add_edge("chat", END)  # stop when LLM decides no more tool calls

    return sg.compile() 