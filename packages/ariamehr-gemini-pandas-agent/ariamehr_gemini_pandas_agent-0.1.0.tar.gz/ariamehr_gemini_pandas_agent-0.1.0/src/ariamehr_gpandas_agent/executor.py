"""
Agent Executor implementation for Ariamehr's Gemini Pandas Agent
Created by Ariamehr A
"""

from typing import Any
from google import genai
from ariamehr_gpandas_agent.graph import build_agent_graph


class AgentExecutor:
    """
    Main executor class for Ariamehr's Gemini Pandas Agent.
    Provides a simple interface similar to LangChain's AgentExecutor.
    """

    def __init__(self, graph, question_key: str = "messages"):
        self._graph = graph
        self._question_key = question_key

    def run(self, question: str):
        """Run a single question through the agent"""
        state = self._graph.invoke({self._question_key: [question]})
        return state["messages"][-1]

    def invoke(self, state):
        """Advanced access for streaming/custom state handling"""
        return self._graph.invoke(state)


def create_pandas_dataframe_agent(
    llm: genai.GenerativeModel,
    df: Any,
    *,
    verbose: bool = False,
    allow_dangerous_code: bool = False,
    **kwargs,
) -> AgentExecutor:
    """
    Create a Pandas DataFrame agent powered by Google's Gemini and LangGraph.
    Created by Ariamehr A

    Args:
        llm: A Gemini model instance
        df: A pandas DataFrame or list of DataFrames
        verbose: Enable verbose output
        allow_dangerous_code: Allow potentially unsafe imports in the Python REPL
        **kwargs: Additional arguments passed to the executor

    Returns:
        An AgentExecutor instance that can process natural language queries about the DataFrame
    """
    graph = build_agent_graph(llm, df, allow_dangerous_code=allow_dangerous_code)
    return AgentExecutor(graph) 