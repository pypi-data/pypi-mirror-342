"""
Endpoints related to Games (api.nhle.com/stats/rest/{lang}/game, etc.)
"""

import typing as t
from .base import StatsEndpointCategory


class StatsGame(StatsEndpointCategory):
    """Handles Stats API endpoints related to game information."""

    async def get_game_info(
        self, cayenne_exp: t.Optional[str] = None
    ) -> t.Dict[str, t.Any]:
        """
        Retrieve general game information, potentially filtered.
        Ref: https://api.nhle.com/stats/rest/{lang}/game

        Args:
            cayenne_exp: Optional filter expression (e.g., "gameId=2023020204").

        Returns:
            Dictionary containing game data.
        """
        params = {}
        if cayenne_exp:
            params["cayenneExp"] = cayenne_exp
        return await self._get("/game", params=params)
