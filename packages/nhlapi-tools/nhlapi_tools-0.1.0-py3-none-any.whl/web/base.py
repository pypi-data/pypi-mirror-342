"""
Base class for all api-web.nhle.com endpoint categories.
"""
import typing as t
if t.TYPE_CHECKING:
    from ..http_client import HttpClient # Avoid circular import

class WebEndpointCategory:
    """Base class providing access to the HTTP client."""
    def __init__(self, client: 'HttpClient'):
        self._client = client

    async def _get(self, path: str, params: t.Optional[t.Dict[str, t.Any]] = None) -> t.Dict[str, t.Any]:
        """Helper method to perform a GET request via the client."""
        return await self._client.get(path, params=params)