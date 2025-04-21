from typing import Any, Optional
from mcp.server.fastmcp import FastMCP, Context
from mimir_mcp.api_client import ApiClient, load_config


mcp = FastMCP("mimir")
api_client = None


@mcp.tool()
async def list_repositories(ctx: Context) -> Any:
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


@mcp.tool()
async def vector_search(ctx: Context, query: str, owner: str, name: str, max_results: Optional[int] = 5) -> Any:
    """
    Find code snippets with high vector similarity to the query.

    This tool performs a vector similarity search across code embeddings to find
    relevant code snippets for a given query. It's particularly useful for finding
    specific code implementations, variables, or function definitions based on
    semantic similarity rather than exact text matches.

    Args:
        query: Search query to find similar code snippets
        owner: Repository owner (username)
        name: Repository name
        max_results: Maximum number of results to return (default: 5)
    """
    global api_client
    assert api_client
    try:
        endpoint = f"/tools/{owner}/{name}/vector-search"
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


@mcp.tool()
async def text_search(ctx: Context, query: str, owner: str, name: str,
                      max_results: Optional[int] = 20,
                      case_sensitive: Optional[bool] = False,
                      file_pattern: Optional[str] = None) -> Any:
    """
    Search for text patterns across the codebase (similar to grep).

    This tool performs a text-based search across all files in the repository,
    finding line-by-line matches for the specified query string or pattern.

    Args:
        query: Text or regex pattern to search for in the codebase
        owner: Repository owner (username)
        name: Repository name
        max_results: Maximum number of files to return (default: 20)
        case_sensitive: Whether the search should be case-sensitive (default: False)
        file_pattern: Optional regex pattern to filter which files to search
    """
    global api_client
    assert api_client
    try:
        endpoint = f"/tools/{owner}/{name}/text-search"
        response = await api_client.request(
            method="POST",
            endpoint=endpoint,
            data={
                "query": query,
                "max_results": max_results,
                "case_sensitive": case_sensitive,
                "file_pattern": file_pattern
            }
        )
        return response
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def read_file(ctx: Context, path: str, owner: str, name: str) -> Any:
    """
    Read the contents of a specified file in the repository.

    Args:
        path: Path to the file to read
        owner: Repository owner (username)
        name: Repository name
    """
    global api_client
    assert api_client
    try:
        endpoint = f"/tools/{owner}/{name}/read-file"
        response = await api_client.request(
            method="POST",
            endpoint=endpoint,
            data={
                "path": path
            }
        )
        return response
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def list_directory(ctx: Context, path: str, owner: str, name: str) -> Any:
    """
    List files and directories in the specified path.

    Args:
        path: Path to the directory to list. Use '/' for root.
        owner: Repository owner (username)
        name: Repository name
    """
    global api_client
    assert api_client
    try:
        endpoint = f"/tools/{owner}/{name}/list-directory"
        response = await api_client.request(
            method="POST",
            endpoint=endpoint,
            data={
                "path": path
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
