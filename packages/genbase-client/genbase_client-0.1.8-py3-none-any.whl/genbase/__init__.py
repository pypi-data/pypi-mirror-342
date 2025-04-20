# In client/src/genbase/__init__.py
from .base_agent import BaseAgent, tool, collect_tools
from .types import AgentContext, IncludeOptions, ProfileStoreFilter, ProfileStoreRecord


__version__ = "0.1.0"

__all__ = [
    "BaseAgent",
    "tool",
    "collect_tools",
    "AgentContext",
    "IncludeOptions",
    "ProfileStoreFilter",
    "ProfileStoreRecord",
    "__version__",
]