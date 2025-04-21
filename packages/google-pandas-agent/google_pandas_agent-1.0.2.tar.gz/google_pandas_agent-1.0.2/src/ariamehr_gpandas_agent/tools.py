"""
Pandas AST Tool implementation for Ariamehr's Gemini Pandas Agent
Created by Ariamehr Maleki
"""

from typing import Any, Dict
import pandas as pd
from langgraph.prebuilt import ToolNode
from langgraph.tools.python import PythonAstREPLTool


class PandasAstTool(PythonAstREPLTool):
    """
    REPL tool seeded with a `df` or list/tuple of DataFrames.
    Executable code runs in an isolated namespace containing:
        - the DataFrame(s) bound to simple names: df, df1, df2, ...
        - pandas imported as `pd`
    
    Created by Ariamehr A
    """

    def __init__(self, dfs: Any, allow_dangerous_code: bool = False):
        self._locals: Dict[str, Any] = {"pd": pd}
        if isinstance(dfs, (list, tuple)):
            for i, d in enumerate(dfs, 1):
                self._locals[f"df{i}"] = d
            self._locals["df"] = dfs[0]
        else:
            self._locals["df"] = dfs

        super().__init__(
            scope=self._locals,
            name="python_repl_ast",
            description=(
                "Execute Python AST code on pandas DataFrames that are already "
                "loaded into variables (df, df1, df2, ...). "
                "Return ONLY plain‑text, never markdown."
            ),
            allowed_imports=["pandas", "numpy"],
            allow_unsafe_imports=allow_dangerous_code,  # off by default
        )


def build_tool_node(dfs, allow_dangerous_code=False) -> ToolNode:
    """Build a tool node with the PandasAstTool"""
    repl = PandasAstTool(dfs, allow_dangerous_code=allow_dangerous_code)
    return ToolNode([repl]) 