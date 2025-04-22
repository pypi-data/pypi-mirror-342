from typing import Any, Dict, Optional
from .client import MimirClient


class ToolsAPI:
    """API methods for working with repository tools."""

    def __init__(self, client: MimirClient):
        self._client = client

    async def agentic_file_search(
        self,
        owner: str,
        name: str,
        query: str,
        max_results: Optional[int] = 5
    ) -> Dict[str, Any]:
        """
        Find relevant files in a repository using natural language search.

        Args:
            owner: Repository owner (username)
            name: Repository name
            query: Natural language description of what files you're looking for
            max_results: Maximum number of file recommendations to return (default: 5)
        """
        endpoint = f"/tools/{owner}/{name}/agentic-file-search"
        return await self._client.request(
            method="POST",
            endpoint=endpoint,
            data={
                "query": query,
                "max_results": max_results
            }
        )

    async def vector_search(
        self,
        owner: str,
        name: str,
        query: str,
        max_results: Optional[int] = 5
    ) -> Dict[str, Any]:
        """
        Find code snippets with high vector similarity to the query.

        Args:
            owner: Repository owner (username)
            name: Repository name
            query: Search query to find similar code snippets
            max_results: Maximum number of results to return (default: 5)
        """
        endpoint = f"/tools/{owner}/{name}/vector-search"
        return await self._client.request(
            method="POST",
            endpoint=endpoint,
            data={
                "query": query,
                "max_results": max_results
            }
        )

    async def text_search(
        self,
        owner: str,
        name: str,
        query: str,
        max_results: Optional[int] = 20,
        case_sensitive: Optional[bool] = False,
        file_pattern: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search for text patterns across the codebase (similar to grep).

        Args:
            owner: Repository owner (username)
            name: Repository name
            query: Text or regex pattern to search for in the codebase
            max_results: Maximum number of files to return (default: 20)
            case_sensitive: Whether the search should be case-sensitive (default: False)
            file_pattern: Optional regex pattern to filter which files to search
        """
        endpoint = f"/tools/{owner}/{name}/text-search"
        return await self._client.request(
            method="POST",
            endpoint=endpoint,
            data={
                "query": query,
                "max_results": max_results,
                "case_sensitive": case_sensitive,
                "file_pattern": file_pattern
            }
        )

    async def read_file(
        self,
        owner: str,
        name: str,
        path: str
    ) -> Dict[str, Any]:
        """
        Read the contents of a specified file in the repository.

        Args:
            owner: Repository owner (username)
            name: Repository name
            path: Path to the file to read
        """
        endpoint = f"/tools/{owner}/{name}/read-file"
        return await self._client.request(
            method="POST",
            endpoint=endpoint,
            data={
                "path": path
            }
        )

    async def list_directory(
        self,
        owner: str,
        name: str,
        path: str
    ) -> Dict[str, Any]:
        """
        List files and directories in the specified path.

        Args:
            owner: Repository owner (username)
            name: Repository name
            path: Path to the directory to list. Use '/' for root.
        """
        endpoint = f"/tools/{owner}/{name}/list-directory"
        return await self._client.request(
            method="POST",
            endpoint=endpoint,
            data={
                "path": path
            }
        )