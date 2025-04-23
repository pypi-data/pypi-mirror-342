import argparse
from .server import mcp, initialize_mcp

def main():
    parser = argparse.ArgumentParser(description="Bing Search MCP(MSN Weather)")

    parser.add_argument('--apikey', type=str, required=True, help="Bing API ID")
    args = parser.parse_args()
    
    # Initialize mcp with the provided API key
    initialize_mcp(args.apikey)
    # Run the server
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()