"""
YouTube search functionality using SerpAPI.
"""

import os
from typing import Dict, List, Optional
from serpapi import GoogleSearch

class YouTubeSearch:
    """
    A class to search for YouTube videos using SerpAPI.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the YouTube search with SerpAPI key.
        
        Args:
            api_key: SerpAPI key. If not provided, looks for SERP_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv("SERP_API_KEY")
        if not self.api_key:
            raise ValueError("SerpAPI key is required. Provide it as an argument or set SERP_API_KEY environment variable.")
    
    def search(self, query: str, max_results: int = 10, language: str = "en", country: str = "us") -> Dict:
        """
        Search for YouTube videos.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            language: Language code (e.g., 'en' for English)
            country: Country code (e.g., 'us' for United States)
            
        Returns:
            Dictionary containing search results and metadata
        """
        if not query or not isinstance(query, str):
            return {"error": "Invalid search query"}
        
        # Configure SerpAPI parameters
        params = {
            "api_key": self.api_key,
            "engine": "youtube",
            "search_query": query,
            "hl": language,
            "gl": country
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
            for video in video_results[:max_results]:
                formatted_video = {
                    "title": video.get("title", "Unknown"),
                    "link": video.get("link", ""),
                    "channel": video.get("channel", {}).get("name", "Unknown channel"),
                    "views": video.get("views", "Unknown"),
                    "published_date": video.get("published_date", "Unknown"),
                    "duration": video.get("length", "Unknown"),
                    "thumbnail": video.get("thumbnail", {}).get("static", "No thumbnail available"),
                    "description": video.get("description", "No description available")
                }
                formatted_videos.append(formatted_video)
            
            # Return the structured data
            return {
                "results": formatted_videos,
                "count": len(formatted_videos),
                "search_query": query
            }
                
        except Exception as e:
            return {"error": f"YouTube search failed: {str(e)}"}