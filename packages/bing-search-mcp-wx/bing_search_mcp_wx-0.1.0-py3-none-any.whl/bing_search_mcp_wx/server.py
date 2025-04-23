from datetime import datetime, timedelta
import sys
from typing import Any, Dict, Tuple, Optional
from mcp.server.fastmcp import FastMCP
import json
import requests
from urllib.parse import quote

class SharedClient:
    def __init__(self, base_url):
        self.session = requests.Session()
        self.session.headers.update({'Base-URL': base_url})

    def get(self, endpoint, **kwargs):
        url = self.session.headers['Base-URL'] + endpoint
        return self.session.get(url, **kwargs)

# Initialize FastMCP server
mcp = FastMCP("bing-search")

# Constants
BING_API_KEY = ""
sys.stdout.reconfigure(encoding='utf-8')
# Update mcp initialization to accept apikeys
def initialize_mcp(apiKey: str):
    """Initialize the MCP server with the provided API keys.
    
    Args:
        apiKey: API Id for Bing API
    """
    global BING_API_KEY
    BING_API_KEY = apiKey

def encode_json_utf8(data: Any) -> str:
    """Encode data as JSON with UTF-8."""
    try:
        # First convert to JSON string
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        print(f"Error encoding to UTF-8: {str(e)}")
        return "Error encoding response data"

# Initialize Bing client
bing_client = SharedClient("https://www.bing.com")


@mcp.tool()
def bing_search(query: str, result_count: int = 10) -> str:
    """Search Bing with the given query and return web results.

    Args:
        query: The search query string
        result_count: Number of results to return (default: 10)
    """
    try:
        # Process query string with proper UTF-8 and URL encoding for Chinese characters  
        processed_query = query.strip().replace(" ", "+")
        # Prepare endpoint with query parameters
        endpoint = (f"/api/v7/search?"
                   f"q={processed_query}&"
                   f"count={result_count}&"
                   f"mkt=en-US&"
                   f"responseFilter=webpages&"
                   f"setLang=en&"
                   f"appId={BING_API_KEY}")
        
        # Add required headers
        headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        # Make request using SharedClient
        response = bing_client.get(endpoint, headers=headers)

        if response.status_code == 200:
            data = response.json()
            results = data.get("webPages", {}).get("value", [])
            return encode_json_utf8(results)
        else:
            error_msg = f"API request failed with status {response.status_code}"
            return json.dumps({
            "error": error_msg,
            "timestamp": datetime.now().isoformat()
        }, indent=2)
            
    except Exception as e:
        error_msg = f"Failed to fetch data: {str(e)}"
        return json.dumps({
            "error": error_msg,
            "timestamp": datetime.now().isoformat()
        }, indent=2)
        
    
