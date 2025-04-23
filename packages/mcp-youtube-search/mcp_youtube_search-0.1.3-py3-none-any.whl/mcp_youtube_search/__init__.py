"""
MCP YouTube Search Server - A YouTube search server for AI agents using MCP.
"""

__version__ = "0.1.3"

from .server import run_server, search_youtube

__all__ = ["run_server", "search_youtube"]
