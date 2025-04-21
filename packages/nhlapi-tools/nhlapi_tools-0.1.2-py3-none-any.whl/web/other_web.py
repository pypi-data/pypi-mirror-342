"""
Remaining endpoints for the api-web.nhle.com API that didn't fit other categories.
"""

import typing as t
import datetime
from .base import WebEndpointCategory
from ..utils import format_date


class OtherWeb(WebEndpointCategory):
    """Handles remaining endpoints like Season, WhereToWatch, Network, Odds."""

    # === Where to Watch ===
    async def get_where_to_watch(
        self, include: t.Optional[str] = None
    ) -> t.Dict[str, t.Any]:
        """
        Retrieve information about streaming/broadcast options.
        Ref: https://api-web.nhle.com/v1/where-to-watch

        Args:
            include: Optional query parameter (purpose unclear from docs).

        Returns:
            Dictionary containing where-to-watch information.
        """
        params = {}
        if include:
            params["include"] = include
        return await self._get("/v1/where-to-watch", params=params)

    # === Network ===
    async def get_tv_schedule_by_date(
        self, date: t.Union[str, datetime.date]
    ) -> t.Dict[str, t.Any]:
        """
        Retrieve the TV broadcast schedule for a specific date.
        Ref: https://api-web.nhle.com/v1/network/tv-schedule/{date}

        Args:
            date: Date string in YYYY-MM-DD format or a datetime.date object.

        Returns:
            Dictionary containing the TV schedule for the specified date.
        """
        formatted_date = format_date(date)
        path = f"/v1/network/tv-schedule/{formatted_date}"
        return await self._get(path)

    async def get_tv_schedule_now(self) -> t.Dict[str, t.Any]:
        """
        Retrieve the current TV broadcast schedule.
        Ref: https://api-web.nhle.com/v1/network/tv-schedule/now

        Returns:
            Dictionary containing the current TV schedule.
        """
        return await self._get("/v1/network/tv-schedule/now")

    # === Odds ===
    async def get_partner_game_odds_now(self, country_code: str) -> t.Dict[str, t.Any]:
        """
        Retrieve partner betting odds for games in a specific country as of now.
        Ref: https://api-web.nhle.com/v1/partner-game/{country-code}/now

        Args:
            country_code: Two-letter country code (e.g., "US", "CA").

        Returns:
            Dictionary containing current partner game odds.
        """
        path = f"/v1/partner-game/{country_code.upper()}/now"
        return await self._get(path)

    # === Season ===
    async def get_seasons(self) -> t.List[int]:
        """
        Retrieve a list of all season IDs (YYYYYYYY format).
        Ref: https://api-web.nhle.com/v1/season

        Returns:
            A list of integers representing season IDs.
        """
        # Assuming the response is directly a list of integers based on description
        response = await self._get("/v1/season")
        if isinstance(response, list):
            return response
        else:
            # Handle unexpected format, maybe raise an error or return empty list
            # For now, let's assume it might be nested if not a direct list
            return response.get("seasons", [])  # Example guess if nested
