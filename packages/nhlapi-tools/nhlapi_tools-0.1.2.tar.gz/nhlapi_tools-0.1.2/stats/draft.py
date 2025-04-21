"""
Endpoints related to Draft information (api.nhle.com/stats/rest/{lang}/draft)
"""

import typing as t
from .base import StatsEndpointCategory


class StatsDraft(StatsEndpointCategory):
    """Handles Stats API endpoints related to draft information."""

    async def get_draft_info(
        self,
        cayenne_exp: t.Optional[str] = None,
        sort: t.Optional[str] = None,
        limit: t.Optional[int] = None,
    ) -> t.Dict[str, t.Any]:
        """
        Retrieve draft information, potentially filtered.
        Ref: https://api.nhle.com/stats/rest/{lang}/draft

        Args:
            cayenne_exp: Optional filter expression (e.g., "draftYear=2023").
            sort: Optional field to sort by (e.g., "pickOverall").
            limit: Optional limit.

        Returns:
            Dictionary containing draft data.
        """
        params = {}
        if cayenne_exp:
            params["cayenneExp"] = cayenne_exp
        if sort:
            params["sort"] = sort
        if limit is not None:
            params["limit"] = limit
        return await self._get("/draft", params=params)
