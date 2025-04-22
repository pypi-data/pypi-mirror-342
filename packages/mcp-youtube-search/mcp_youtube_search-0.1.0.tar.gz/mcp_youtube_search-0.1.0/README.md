# MCP YouTube Search

A Python package for searching YouTube videos via SerpAPI, with an MCP server implementation.

## Installation

Install from PyPI:

```bash
pip install mcp-youtube-search
```

## Requirements

- Python 3.11+
- SerpAPI API key (get one at [serpapi.com](https://serpapi.com/))

## Usage

### Set your API key

You can set your SerpAPI API key in one of two ways:

1. Set it as an environment variable:
   ```bash
   export SERP_API_KEY="your_api_key_here"
   ```

2. Or create a `.env` file with the following content:
   ```
   SERP_API_KEY=your_api_key_here
   ```

### As a Python library

```python
from mcp_youtube_search.search import YouTubeSearch

# Initialize with API key
search = YouTubeSearch(api_key="your_api_key_here")  # or omit to use env var

# Search for videos
results = search.search("python tutorial", max_results=5)

# Process results
for video in results["results"]:
    print(f"Title: {video['title']}")
    print(f"Link: {video['link']}")
    print(f"Channel: {video['channel']}")
    print(f"Views: {video['views']}")
    print(f"Duration: {video['duration']}")
    print(f"Published: {video['published_date']}")
    print("---")
```

### As a command-line tool

Search for videos:

```bash
mcp-youtube-search search "python tutorial" --max-results 5
```

Run as an MCP server:

```bash
mcp-youtube-search server
```

### MCP Server Integration

The package can be used as an MCP server for integration with AI assistants:

```python
from mcp_youtube_search.mcp_server import run_server

# Run the server with an optional API key (or use env var)
run_server(api_key="your_api_key_here")
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 