"""
Base class for all api.nhle.com/stats/rest endpoint categories.
"""
import typing as t
if t.TYPE_CHECKING:
    from ..http_client import HttpClient # Avoid circular import

class StatsEndpointCategory:
    """Base class providing access to the HTTP client and language setting."""
    def __init__(self, client: 'HttpClient', language: str):
        self._client = client
        self._language = language # Store the language code (e.g., 'en')

    async def _get(self, path: str, params: t.Optional[t.Dict[str, t.Any]] = None) -> t.Dict[str, t.Any]:
        """
        Helper method to perform a GET request via the client, prepending the language code.
        """
        # Prepend the language code to the path for Stats API requests
        lang_path = f"/{self._language}{path}"
        return await self._client.get(lang_path, params=params)

    # You might add helper methods here later for common parameter patterns,
    # like building cayenneExp strings, if needed.