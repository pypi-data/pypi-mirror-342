"""
Endpoints related to Playoff Information (api-web.nhle.com/v1/playoff-series/*, etc.)
"""

import typing as t
from .base import WebEndpointCategory


class Playoff(WebEndpointCategory):
    """Handles endpoints related to playoff series, schedules, and brackets."""

    # === Overview ===
    async def get_series_carousel(self, season: int) -> t.Dict[str, t.Any]:
        """
        Retrieve an overview/summary of each playoff series for a season.
        Ref: https://api-web.nhle.com/v1/playoff-series/carousel/{season}/

        Args:
            season: Season in YYYYYYYY format (e.g., 20232024). Note: Endpoint requires trailing slash.

        Returns:
            Dictionary containing data for the playoff series carousel.
        """
        path = f"/v1/playoff-series/carousel/{season}/"  # Note trailing slash
        return await self._get(path)

    # === Schedule ===
    async def get_series_schedule(
        self, season: int, series_letter: str
    ) -> t.Dict[str, t.Any]:
        """
        Retrieve the schedule for a specific playoff series.
        Ref: https://api-web.nhle.com/v1/schedule/playoff-series/{season}/{series_letter}/

        Args:
            season: Season in YYYYYYYY format (e.g., 20232024).
            series_letter: Single letter identifying the series (e.g., "A", "B", ...). Note: Endpoint requires trailing slash.

        Returns:
            Dictionary containing the schedule for the specified playoff series.
        """
        path = f"/v1/schedule/playoff-series/{season}/{series_letter.lower()}/"  # Note trailing slash, ensure lowercase
        return await self._get(path)

    # === Bracket ===
    async def get_bracket(self, year: int) -> t.Dict[str, t.Any]:
        """
        Retrieve the playoff bracket structure for a specific year.
        Ref: https://api-web.nhle.com/v1/playoff-bracket/{year}

        Args:
            year: The ending year of the season (e.g., 2023 for the 2022-2023 season playoffs).

        Returns:
            Dictionary representing the playoff bracket.
        """
        path = f"/v1/playoff-bracket/{year}"
        return await self._get(path)

    # === Metadata (Moved from Misc) ===
    async def get_series_metadata(
        self, year: int, series_letter: str
    ) -> t.Dict[str, t.Any]:
        """
        Retrieve metadata for a specific playoff series.
        Ref: https://api-web.nhle.com/v1/meta/playoff-series/{year}/{series_letter}

        Args:
            year: The ending year of the season (e.g., 2023 for the 2022-2023 season playoffs).
            series_letter: Single letter identifying the playoff series (e.g., "A", "B", ...).

        Returns:
            Dictionary containing metadata for the specified playoff series.
        """
        path = f"/v1/meta/playoff-series/{year}/{series_letter.lower()}"
        return await self._get(path)
