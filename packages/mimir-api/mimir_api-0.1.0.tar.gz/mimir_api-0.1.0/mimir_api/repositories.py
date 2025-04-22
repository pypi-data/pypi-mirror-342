from typing import Any, Dict, List
from .client import MimirClient


class RepositoriesApi:
    """API methods for working with repositories."""

    def __init__(self, client: MimirClient):
        self._client = client

    async def list(self) -> List[Dict[str, Any]]:
        """List repositories for a user."""
        return await self._client.request(
            method="GET",
            endpoint="/repositories/"
        )