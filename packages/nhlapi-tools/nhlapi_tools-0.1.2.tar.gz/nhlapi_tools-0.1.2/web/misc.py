"""
Miscellaneous Endpoints from api-web.nhle.com
"""

import typing as t
from .base import WebEndpointCategory


class Misc(WebEndpointCategory):
    """Handles miscellaneous endpoints like metadata, location, etc."""

    # === Meta ===
    async def get_meta_info(
        self,
        players: t.Optional[str] = None,
        teams: t.Optional[str] = None,
        season_states: t.Optional[str] = None,
    ) -> t.Dict[str, t.Any]:
        """
        Retrieve meta information, potentially filtered by players, teams, or season states.
        Ref: https://api-web.nhle.com/v1/meta

        Args:
            players: Optional comma-separated string of player IDs.
            teams: Optional comma-separated string of team tricodes.
            season_states: Optional filter for season states (exact values unknown).

        Returns:
            Dictionary containing meta information.
        """
        params = {}
        if players:
            params["players"] = players
        if teams:
            params["teams"] = teams
        if season_states:
            params["seasonStates"] = season_states  # Parameter name from docs
        return await self._get("/v1/meta", params=params)

    async def get_meta_game_info(self, game_id: int) -> t.Dict[str, t.Any]:
        """
        Retrieve meta information specific to a game.
        Ref: https://api-web.nhle.com/v1/meta/game/{game-id}

        Args:
            game_id: The NHL Game ID.

        Returns:
            Dictionary containing game-specific metadata.
        """
        path = f"/v1/meta/game/{game_id}"
        return await self._get(path)

    async def get_location(self) -> t.Dict[str, t.Any]:
        """
        Returns the country code the webserver detects for the user.
        Ref: https://api-web.nhle.com/v1/location

        Returns:
            Dictionary containing location information (e.g., country code).
        """
        return await self._get("/v1/location")

    # === Postal Lookup ===
    async def get_postal_code_info(self, postal_code: str) -> t.Dict[str, t.Any]:
        """
        Retrieves location/market information based on a postal code.
        Ref: https://api-web.nhle.com/v1/postal-lookup/{postalCode}

        Args:
            postal_code: The postal or ZIP code string.

        Returns:
            Dictionary containing information related to the postal code.
        """
        path = f"/v1/postal-lookup/{postal_code}"
        return await self._get(path)

    # Removed get_openapi_spec as this endpoint does not exist and always returns 404.
