import argparse
from .server import mcp, initialize_mcp

def main():
    parser = argparse.ArgumentParser(description="MSN Weather MCP Server")

    parser.add_argument('--wxapikey', type=str, required=True, help="MSN Weather API Key")
    parser.add_argument('--autosuggestapikey', type=str, required=True, help="Autosuggest API Key")
    args = parser.parse_args()
    
    # Initialize mcp with the provided API key
    initialize_mcp(args.wxapikey, args.autosuggestapikey)
    # Run the server
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()