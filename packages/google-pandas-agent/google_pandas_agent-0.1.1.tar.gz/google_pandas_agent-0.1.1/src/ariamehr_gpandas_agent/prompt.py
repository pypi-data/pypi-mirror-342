"""
Prompt templates and utilities for Ariamehr's Gemini Pandas Agent
Created by Ariamehr Maleki
"""

from __future__ import annotations
import pandas as pd
from typing import List, Any

PREFIX = """\
You are an expert data analyst using Ariamehr's Gemini Pandas Agent. You have access to a Python REPL that can
execute pandas code on a pre‑loaded DataFrame(s). Use the tool to run code;
then think and reply with the answer, not the code.

Follow this protocol:
• When you need to compute, call the tool with valid python.
• The tool returns the result.
• Then write a concise answer for the user.
"""

SUFFIX = """\
Begin!

Question: {question}
{agent_scratchpad}"""

def _df_head_preview(dfs: Any, rows: int = 5) -> str:
    """Generate a preview of the DataFrame(s) head"""
    buf: List[str] = []
    if isinstance(dfs, (list, tuple)):
        for i, d in enumerate(dfs, 1):
            buf.append(f"df{i} head():\n{d.head(rows)}\n")
    else:
        buf.append(f"df head():\n{dfs.head(rows)}\n")
    return "\n".join(buf)

def build_prompt(question: str, dfs: Any, rows: int = 5) -> str:
    """Build the complete prompt with DataFrame preview"""
    preview = _df_head_preview(dfs, rows)
    return f"{PREFIX}\n{preview}\n{SUFFIX.format(question=question, agent_scratchpad='')}" 