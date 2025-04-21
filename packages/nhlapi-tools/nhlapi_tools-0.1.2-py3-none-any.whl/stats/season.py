"""
Endpoints related to Seasons (api.nhle.com/stats/rest/{lang}/season, etc.)
"""

import typing as t
from .base import StatsEndpointCategory


class StatsSeason(StatsEndpointCategory):
    """Handles Stats API endpoints related to season information."""

    async def get_component_season(self) -> t.Dict[str, t.Any]:
        """
        Retrieve component season information.
        Ref: https://api.nhle.com/stats/rest/{lang}/componentSeason

        Returns:
            Dictionary containing component season data.
        """
        return await self._get("/componentSeason")

    async def get_season_info(self) -> t.Dict[str, t.Any]:
        """
        Retrieve general season information (list of seasons).
        Ref: https://api.nhle.com/stats/rest/{lang}/season

        Returns:
            Dictionary containing a list of seasons.
        """
        return await self._get("/season")
