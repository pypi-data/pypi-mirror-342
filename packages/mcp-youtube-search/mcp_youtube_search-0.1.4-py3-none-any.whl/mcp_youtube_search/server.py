#!/usr/bin/env python3
"""
YouTube Search MCP Server

An MCP server that implements YouTube search functionality using Google's Agent Developer Kit (ADK) wrapper.
"""
import asyncio
import json
import os
from dotenv import load_dotenv
from typing import Dict, List
from serpapi import GoogleSearch

# MCP Server Imports
from mcp import types as mcp_types # Use alias to avoid conflict with genai.types
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio

# ADK Tool Imports
from google.adk.tools.function_tool import FunctionTool
# ADK <-> MCP Conversion Utility
from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type

# --- Load Environment Variables ---
load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")

# --- Define YouTube Search Function for ADK Tool ---
async def search_youtube(search_query: str, max_results: int = 10) -> Dict:
    """Search for YouTube videos using SerpAPI's YouTube integration.
    Returns a dictionary containing a list of video results.
    """
    
    if not SERP_API_KEY:
        return {"error": "SERP_API_KEY not configured"}
    
    # Validate input
    if not search_query or not isinstance(search_query, str):
        return {"error": "Invalid search query"}
    
    # Configure SerpAPI parameters
    params = {
        "api_key": SERP_API_KEY,
        "engine": "youtube",
        "search_query": search_query,
        "hl": "en",
        "gl": "us"
    }
    
    try:
        # Run the search
        search = GoogleSearch(params)
        results = search.get_dict()
        
        # Process and format the results
        if "error" in results:
            return {"error": results["error"]}
        
        video_results = results.get("video_results", [])
        if not video_results:
            return {"results": [], "message": "No videos found for this search"}
        
        formatted_videos = []
        for video in video_results[:max_results]:  # Limit to specified max results
            formatted_video = {
                "title": video.get("title", "Unknown"),
                "link": video.get("link", ""),
                "channel": video.get("channel", {}).get("name", "Unknown channel"),
                "views": video.get("views", "Unknown"), # Keep raw views data
                "published_date": video.get("published_date", "Unknown"),
                "duration": video.get("length", "Unknown"),
                "thumbnail": video.get("thumbnail", {}).get("static", "No thumbnail available"),
                "description": video.get("description", "No description available")
            }
            formatted_videos.append(formatted_video)
        
        # Return only the structured data
        return {
            "results": formatted_videos,
            "count": len(formatted_videos),
            "search_query": search_query
        }
            
    except Exception as e:
        return {"error": f"YouTube search failed: {str(e)}"}

# --- Prepare the ADK Tool ---
print("Initializing ADK YouTube search tool...")
youtube_search_tool = FunctionTool(search_youtube)
print(f"ADK tool '{youtube_search_tool.name}' initialized.")
# --- End ADK Tool Prep ---

# --- MCP Server Setup ---
print("Creating MCP Server instance...")
# Create a named MCP Server instance
app = Server("youtube-search-mcp-server")

# Implement the MCP server's list_tools handler
@app.list_tools()
async def list_tools() -> list[mcp_types.Tool]:
    """MCP handler to list available tools."""
    mcp_tool_schema = adk_to_mcp_tool_type(youtube_search_tool)
    return [mcp_tool_schema]

# Implement the MCP server's call_tool handler
@app.call_tool()
async def call_tool(
    name: str, arguments: dict
) -> list[mcp_types.TextContent | mcp_types.ImageContent | mcp_types.EmbeddedResource]:
    """MCP handler to execute a tool call."""

    if name == youtube_search_tool.name:
        try:
            # Execute the ADK tool's run_async method
            adk_response = await youtube_search_tool.run_async(
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

# --- MCP Server Runner ---
async def run_server():
    """Runs the MCP server over standard input/output."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=app.name,
                server_version="0.1.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        pass # Exit cleanly on Ctrl+C
    except Exception as e:
        print(f"MCP Server encountered an error: {e}")
# --- End MCP Server ---