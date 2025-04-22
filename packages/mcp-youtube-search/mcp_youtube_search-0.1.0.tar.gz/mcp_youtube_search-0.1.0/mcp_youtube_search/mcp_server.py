"""
MCP server implementation for YouTube search.
"""

import asyncio
import json
import os
from typing import Dict, List

# MCP Server Imports
from mcp import types as mcp_types
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio

# ADK Tool Imports
from google.adk.tools.function_tool import FunctionTool
# ADK <-> MCP Conversion Utility
from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type

from .search import YouTubeSearch

class YouTubeSearchMCPServer:
    """
    MCP server implementation for YouTube search functionality.
    """
    
    def __init__(self, api_key=None, server_name="youtube-search-mcp-server", server_version="0.1.0"):
        """
        Initialize the YouTube search MCP server.
        
        Args:
            api_key: SerpAPI key (optional, can be set via environment variable)
            server_name: Name of the MCP server
            server_version: Version of the MCP server
        """
        self.api_key = api_key or os.getenv("SERP_API_KEY")
        self.server_name = server_name
        self.server_version = server_version
        
        # Initialize search functionality
        self.search_client = YouTubeSearch(api_key=self.api_key)
        
        # Create ADK tool
        self.youtube_search_tool = FunctionTool(self._search_youtube)
        
        # Create a named MCP Server instance
        self.app = Server(self.server_name)
        
        # Register handlers
        self.app.list_tools()(self.list_tools)
        self.app.call_tool()(self.call_tool)
    
    async def _search_youtube(self, search_query: str, max_results: int = 10) -> Dict:
        """
        YouTube search function implementation for ADK Tool.
        
        Args:
            search_query: The query string to search for
            max_results: Maximum number of results to return
            
        Returns:
            Dictionary with search results
        """
        return self.search_client.search(search_query, max_results)
    
    async def list_tools(self) -> list[mcp_types.Tool]:
        """
        MCP handler to list available tools.
        
        Returns:
            List of available tools
        """
        mcp_tool_schema = adk_to_mcp_tool_type(self.youtube_search_tool)
        return [mcp_tool_schema]

    async def call_tool(self, name: str, arguments: dict) -> list[mcp_types.TextContent | mcp_types.ImageContent | mcp_types.EmbeddedResource]:
        """
        MCP handler to execute a tool call.
        
        Args:
            name: Name of the tool to call
            arguments: Arguments to pass to the tool
            
        Returns:
            List of content objects with the tool's response
        """
        if name == self.youtube_search_tool.name:
            try:
                # Execute the ADK tool's run_async method
                adk_response = await self.youtube_search_tool.run_async(
                    args=arguments,
                    tool_context=None,  # No ADK context available here
                )
                
                # Always return the JSON response
                response_text = json.dumps(adk_response, indent=2)
                return [mcp_types.TextContent(type="text", text=response_text)]

            except Exception as e:
                error_text = json.dumps({"error": f"Failed to execute tool '{name}': {str(e)}"})
                return [mcp_types.TextContent(type="text", text=error_text)]
        else:
            error_text = json.dumps({"error": f"Tool '{name}' not implemented."})
            return [mcp_types.TextContent(type="text", text=error_text)]
    
    async def run(self):
        """
        Run the MCP server over standard input/output.
        """
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.app.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name=self.app.name,
                    server_version=self.server_version,
                    capabilities=self.app.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )

def run_server(api_key=None):
    """
    Helper function to run the MCP server.
    
    Args:
        api_key: SerpAPI key (optional)
    """
    server = YouTubeSearchMCPServer(api_key=api_key)
    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        pass  # Exit cleanly on Ctrl+C
    except Exception as e:
        print(f"MCP Server encountered an error: {e}") 