#!/usr/bin/env python3
"""
Command line interface for the MCP YouTube Server
"""
import os
import sys
import asyncio
import argparse
from dotenv import load_dotenv

from .server import run_server

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="YouTube Search MCP Server")
    parser.add_argument(
        "--api-key", 
        help="SerpAPI key (alternatively, set SERP_API_KEY environment variable)"
    )
    parser.add_argument(
        "--dotenv", 
        help="Path to .env file containing SERP_API_KEY"
    )
    
    args = parser.parse_args()
    
    # Load environment variables
    if args.dotenv:
        load_dotenv(args.dotenv)
    else:
        load_dotenv()
    
    # Set API key from arguments if provided
    if args.api_key:
        os.environ["SERP_API_KEY"] = args.api_key
    
    # Check if API key is available
    if not os.getenv("SERP_API_KEY"):
        print("Error: SERP_API_KEY not found. Please provide it via command line or .env file.")
        sys.exit(1)
    
    print("Starting YouTube Search MCP Server...")
    
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except Exception as e:
        print(f"Error running server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
