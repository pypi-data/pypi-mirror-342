from typing import Any, Optional
from mcp.server.fastmcp import FastMCP, Context
from mimir_mcp.api_client import ApiClient, load_config


mcp = FastMCP("mimir")
api_client = None


@mcp.tool()
async def list_repos(ctx: Context) -> Any:
    """List repositories for a user."""
    global api_client
    assert api_client
    try:
        response = await api_client.request(
            method="GET",
            endpoint="/repositories/"
        )
        return response
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def agentic_file_search(ctx: Context, query: str, owner: str, name: str, max_results: Optional[int] = 5) -> Any:
    """
    Find relevant files in a repository using natural language search.

    This tool leverages Mimir's preprocessed knowledge base about the repository,
    which contains comprehensive information about file contents, structure, 
    relationships, and semantics. Should typically be prioritzed over vector similarity.
    The AI analyzes this knowledge to identify the most relevant files for your query.

    Args:
        query: Natural language description of what files you're looking for
        owner: Repository owner (username)
        name: Repository name
        max_results: Maximum number of file recommendations to return (default: 5)
    """
    global api_client
    assert api_client
    try:
        endpoint = f"/tools/{owner}/{name}/agentic-file-search"
        response = await api_client.request(
            method="POST",
            endpoint=endpoint,
            data={
                "query": query,
                "max_results": max_results
            }
        )
        return response
    except Exception as e:
        return {"error": str(e)}


def main():
    """Run the Mimir AI MCP server."""
    global api_client

    # initialize API client with config
    config = load_config()
    api_client = ApiClient(config)

    # start the MCP server
    mcp.run()


if __name__ == "__main__":
    main()
