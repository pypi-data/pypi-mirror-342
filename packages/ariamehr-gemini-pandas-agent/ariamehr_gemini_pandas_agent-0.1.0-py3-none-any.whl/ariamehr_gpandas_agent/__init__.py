"""
Ariamehr's Gemini Pandas Agent - A Google-native alternative to LangChain's create_pandas_dataframe_agent
Created by Ariamehr A
"""

from importlib.metadata import version as _v
from .executor import create_pandas_dataframe_agent  # public symbol

__all__ = ["create_pandas_dataframe_agent"]
__version__ = _v(__name__) 