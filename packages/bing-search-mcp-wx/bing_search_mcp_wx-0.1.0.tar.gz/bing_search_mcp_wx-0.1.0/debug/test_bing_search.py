import asyncio
import sys
import os
from dotenv import load_dotenv
from bing_search_mcp_wx.server import initialize_mcp, mcp, bing_search
# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

async def test_bing_search():
    """Test the bing_search functionality with different parameters."""
    # Get API key from environment variable
    api_key = os.getenv("BING_API_KEY")
    if not api_key:
        print("Error: BING_API_KEY environment variable not found")
        sys.exit(1)

    # Initialize MCP with API key
    initialize_mcp(api_key)

    try:
        # Test 1: Basic search
        print("\nTest 1: Basic search with default parameters")
        result = bing_search("上海")
        print(f"Basic search results:\n{result}\n")

        # Test 2: Search with custom result count
        #print("\nTest 2: Search with 5 results")
        result = bing_search("Tokyo", result_count=5)
        #result = await web_search()
        #print(f"Search result:\n{result}\n")

    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    # Run the async test function
    asyncio.run(test_bing_search())