"""
Endpoints related to the NHL Draft (api-web.nhle.com/v1/draft/*)
"""
import typing as t
from .base import WebEndpointCategory

# Prospect category constants for get_rankings_by_prospect_category
NA_SKATER = 1
INTL_SKATER = 2
NA_GOALIE = 3
INTL_GOALIE = 4

class Draft(WebEndpointCategory):
    """Handles endpoints related to draft rankings, trackers, and picks."""

    async def get_rankings_now(self) -> t.Dict[str, t.Any]:
        """
        Retrieve current draft prospect rankings by category.
        Ref: https://api-web.nhle.com/v1/draft/rankings/now

        Returns:
            Dictionary containing current draft rankings.
        """
        return await self._get("/v1/draft/rankings/now")

    async def get_rankings_by_prospect_category(self, season_year: int, prospect_category: int) -> t.Dict[str, t.Any]:
        """
        Retrieve draft prospect rankings for a specific season and category.
        Ref: https://api-web.nhle.com/v1/draft/rankings/{season}/{prospect_category}

        Args:
            season_year: The year of the draft (e.g., 2023).
            prospect_category: The category code (1=NA Skater, 2=Intl Skater, 3=NA Goalie, 4=Intl Goalie).
                               Use constants like draft.NA_SKATER.

        Returns:
            Dictionary containing draft rankings for the specified category.
        """
        path = f"/v1/draft/rankings/{season_year}/{prospect_category}"
        return await self._get(path)

    async def get_tracker_picks_now(self) -> t.Dict[str, t.Any]:
        """
        Retrieve current draft tracker information (likely most recent picks).
        Ref: https://api-web.nhle.com/v1/draft-tracker/picks/now

        Returns:
            Dictionary containing current draft tracker data.
        """
        return await self._get("/v1/draft-tracker/picks/now")

    async def get_picks_now(self) -> t.Dict[str, t.Any]:
        """
        Retrieve the most recent draft picks information. Similar to tracker_picks_now.
        Ref: https://api-web.nhle.com/v1/draft/picks/now

        Returns:
            Dictionary containing recent draft pick data.
        """
        return await self._get("/v1/draft/picks/now")

    async def get_picks_by_season(self, season_year: int, round_number: t.Union[int, str] = 'all') -> t.Dict[str, t.Any]:
        """
        Retrieve a list of draft picks for a specific season and optionally a specific round.
        Ref: https://api-web.nhle.com/v1/draft/picks/{season}/{round}

        Args:
            season_year: The year of the draft (e.g., 2023).
            round_number: The round number (1-7) or 'all' for all rounds. Defaults to 'all'.

        Returns:
            Dictionary containing draft picks for the specified season/round.
        """
        path = f"/v1/draft/picks/{season_year}/{round_number}"
        return await self._get(path)