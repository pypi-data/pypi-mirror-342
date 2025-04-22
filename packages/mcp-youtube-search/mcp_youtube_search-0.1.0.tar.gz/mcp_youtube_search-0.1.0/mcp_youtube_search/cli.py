"""
Command-line interface for MCP YouTube Search.
"""

import argparse
import os
from dotenv import load_dotenv
from . import __version__
from .search import YouTubeSearch
from .mcp_server import run_server

def main():
    """
    Main entry point for the CLI.
    """
    # Load environment variables
    load_dotenv()
    
    # Create parser
    parser = argparse.ArgumentParser(
        description='MCP YouTube Search - Search YouTube videos or run as an MCP server'
    )
    parser.add_argument(
        '--version', 
        action='version', 
        version=f'%(prog)s {__version__}'
    )
    
    # Add API key argument
    parser.add_argument(
        '--api-key', 
        help='SerpAPI key (defaults to SERP_API_KEY environment variable)'
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Add 'search' command
    search_parser = subparsers.add_parser('search', help='Search YouTube videos')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument(
        '--max-results', 
        type=int, 
        default=10, 
        help='Maximum number of results to return'
    )
    search_parser.add_argument(
        '--language', 
        default='en', 
        help='Language code (e.g., "en" for English)'
    )
    search_parser.add_argument(
        '--country', 
        default='us', 
        help='Country code (e.g., "us" for United States)'
    )
    
    # Add 'server' command
    server_parser = subparsers.add_parser('server', help='Run as an MCP server')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Get API key
    api_key = args.api_key or os.getenv('SERP_API_KEY')
    if not api_key:
        print("Error: SerpAPI key is required. Provide it with --api-key or set SERP_API_KEY environment variable.")
        exit(1)
    
    # Execute command
    if args.command == 'search':
        # Create search client
        search_client = YouTubeSearch(api_key=api_key)
        
        # Perform search
        results = search_client.search(
            query=args.query, 
            max_results=args.max_results,
            language=args.language,
            country=args.country
        )
        
        # Print results
        print(f"Found {results.get('count', 0)} results for '{args.query}':")
        for i, video in enumerate(results.get('results', []), 1):
            print(f"\n{i}. {video['title']}")
            print(f"   Channel: {video['channel']}")
            print(f"   URL: {video['link']}")
            print(f"   Duration: {video['duration']}")
            print(f"   Views: {video['views']}")
            print(f"   Published: {video['published_date']}")
    
    elif args.command == 'server':
        print(f"Starting MCP YouTube Search server (v{__version__})...")
        run_server(api_key=api_key)
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main() 