"""
Endpoints related to Players (api-web.nhle.com/v1/player/*, etc.)
"""
import typing as t
from .base import WebEndpointCategory

class Players(WebEndpointCategory):
    """Handles endpoints related to player information, stats, and leaders."""

    # === Players ===
    async def get_game_log(self, player_id: int, season: int, game_type: int) -> t.Dict[str, t.Any]:
        """
        Retrieve the game log for a specific player, season, and game type.
        Ref: https://api-web.nhle.com/v1/player/{player}/game-log/{season}/{game-type}

        Args:
            player_id: The NHL player ID.
            season: Season in YYYYYYYY format (e.g., 20232024).
            game_type: Game type (2 for regular season, 3 for playoffs).

        Returns:
            Dictionary containing the player's game log data.
        """
        path = f"/v1/player/{player_id}/game-log/{season}/{game_type}"
        return await self._get(path)

    async def get_landing(self, player_id: int) -> t.Dict[str, t.Any]:
        """
        Retrieve landing page summary information for a specific player.
        Ref: https://api-web.nhle.com/v1/player/{player}/landing

        Args:
            player_id: The NHL player ID.

        Returns:
            Dictionary containing the player's landing page data.
        """
        path = f"/v1/player/{player_id}/landing"
        return await self._get(path)

    async def get_game_log_now(self, player_id: int) -> t.Dict[str, t.Any]:
        """
        Retrieve the game log for a specific player as of the current moment (current season/game type).
        Ref: https://api-web.nhle.com/v1/player/{player}/game-log/now

        Args:
            player_id: The NHL player ID.

        Returns:
            Dictionary containing the player's current game log data.
        """
        path = f"/v1/player/{player_id}/game-log/now"
        return await self._get(path)

    # === Skaters ===
    async def get_skater_stats_leaders_current(self, categories: t.Optional[str] = None, limit: t.Optional[int] = None) -> t.Dict[str, t.Any]:
        """
        Retrieve current skater stats leaders.
        Ref: https://api-web.nhle.com/v1/skater-stats-leaders/current

        Args:
            categories: Optional comma-separated string of stat categories (e.g., "goals,assists").
            limit: Optional number of leaders to return (-1 for all).

        Returns:
            Dictionary containing current skater leaders.
        """
        params = {}
        if categories:
            params['categories'] = categories
        if limit is not None:
            params['limit'] = limit
        return await self._get("/v1/skater-stats-leaders/current", params=params)

    async def get_skater_stats_leaders_by_season(self, season: int, game_type: int, categories: t.Optional[str] = None, limit: t.Optional[int] = None) -> t.Dict[str, t.Any]:
        """
        Retrieve skater stats leaders for a specific season and game type.
        Ref: https://api-web.nhle.com/v1/skater-stats-leaders/{season}/{game-type}

        Args:
            season: Season in YYYYYYYY format (e.g., 20232024).
            game_type: Game type (2 for regular season, 3 for playoffs).
            categories: Optional comma-separated string of stat categories (e.g., "goals,assists").
            limit: Optional number of leaders to return (-1 for all).

        Returns:
            Dictionary containing skater leaders for the specified season/type.
        """
        params = {}
        if categories:
            params['categories'] = categories
        if limit is not None:
            params['limit'] = limit
        path = f"/v1/skater-stats-leaders/{season}/{game_type}"
        return await self._get(path, params=params)

    # === Goalies ===
    async def get_goalie_stats_leaders_current(self, categories: t.Optional[str] = None, limit: t.Optional[int] = None) -> t.Dict[str, t.Any]:
        """
        Retrieve current goalie stats leaders.
        Ref: https://api-web.nhle.com/v1/goalie-stats-leaders/current

        Args:
            categories: Optional comma-separated string of stat categories (e.g., "wins,savePctg").
            limit: Optional number of leaders to return (-1 for all).

        Returns:
            Dictionary containing current goalie leaders.
        """
        params = {}
        if categories:
            params['categories'] = categories
        if limit is not None:
            params['limit'] = limit
        return await self._get("/v1/goalie-stats-leaders/current", params=params)

    async def get_goalie_stats_leaders_by_season(self, season: int, game_type: int, categories: t.Optional[str] = None, limit: t.Optional[int] = None) -> t.Dict[str, t.Any]:
        """
        Retrieve goalie stats leaders for a specific season and game type.
        Ref: https://api-web.nhle.com/v1/goalie-stats-leaders/{season}/{game-type}

        Args:
            season: Season in YYYYYYYY format (e.g., 20232024).
            game_type: Game type (2 for regular season, 3 for playoffs).
            categories: Optional comma-separated string of stat categories (e.g., "wins,savePctg").
            limit: Optional number of leaders to return (-1 for all).

        Returns:
            Dictionary containing goalie leaders for the specified season/type.
        """
        params = {}
        if categories:
            params['categories'] = categories
        if limit is not None:
            params['limit'] = limit
        path = f"/v1/goalie-stats-leaders/{season}/{game_type}"
        return await self._get(path, params=params)

    # === Player Spotlight ===
    async def get_player_spotlight(self) -> t.Dict[str, t.Any]:
        """
        Retrieve information about players currently in the "spotlight".
        Ref: https://api-web.nhle.com/v1/player-spotlight

        Returns:
            Dictionary containing player spotlight data.
        """
        return await self._get("/v1/player-spotlight")