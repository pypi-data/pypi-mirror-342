"""
Miscellaneous Endpoints from api.nhle.com/stats/rest
"""

import typing as t
from .base import StatsEndpointCategory


class StatsMisc(StatsEndpointCategory):
    """Handles miscellaneous Stats API endpoints like config, ping, country, etc."""

    async def get_configuration(self) -> t.Dict[str, t.Any]:
        """
        Retrieve configuration information for the Stats API.
        Ref: https://api.nhle.com/stats/rest/{lang}/config

        Returns:
            Dictionary containing configuration data.
        """
        return await self._get("/config")

    async def ping(self) -> t.Dict[str, t.Any]:
        """
        Ping the Stats API server to check connectivity.
        Ref: https://api.nhle.com/stats/rest/ping
        Note: This endpoint does not use the language prefix.

        Returns:
            Dictionary containing ping response (usually a timestamp or simple message).
        """
        # This specific endpoint doesn't use the language prefix
        # We call the client's get method directly, bypassing our language-prepending _get
        return await self._client.get("/ping")

    async def get_country_info(self) -> t.Dict[str, t.Any]:
        """
        Retrieve a list of countries.
        Ref: https://api.nhle.com/stats/rest/{lang}/country

        Returns:
            Dictionary containing a list of countries.
        """
        return await self._get("/country")

    async def get_shift_charts(self, game_id: int) -> t.Dict[str, t.Any]:
        """
        Retrieve shift charts for a specific game.
        Ref: https://api.nhle.com/stats/rest/{lang}/shiftcharts?cayenneExp=gameId={game_id}

        Args:
            game_id: The NHL Game ID (e.g., 2023020204).

        Returns:
            Dictionary containing shift chart data for the specified game.
        """
        params = {"cayenneExp": f"gameId={game_id}"}
        return await self._get("/shiftcharts", params=params)

    async def get_glossary(self) -> t.Dict[str, t.Any]:
        """
        Retrieve the glossary of statistical terms.
        Ref: https://api.nhle.com/stats/rest/{lang}/glossary

        Returns:
            Dictionary containing glossary terms and definitions.
        """
        return await self._get("/glossary")

    async def get_content_module(self, template_key: str) -> t.Dict[str, t.Any]:
        """
        Retrieve content module information for a specific template key.
        Ref: https://api.nhle.com/stats/rest/{lang}/content/module/{templateKey}

        Args:
            template_key: The key/name of the content template (e.g., "overview").

        Returns:
            Dictionary containing content module data.
        """
        path = f"/content/module/{template_key}"
        return await self._get(path)
