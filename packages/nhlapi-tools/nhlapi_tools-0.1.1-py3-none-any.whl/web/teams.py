"""
Endpoints related to Teams (api-web.nhle.com/v1/standings/*, etc.)
"""
import typing as t
import datetime
from .base import WebEndpointCategory
from ..utils import format_date

class Teams(WebEndpointCategory):
    """Handles endpoints related to team standings, stats, rosters, and prospects."""

    # === Standings ===
    async def get_standings_now(self) -> t.Dict[str, t.Any]:
        """
        Retrieve the standings as of the current moment.
        Ref: https://api-web.nhle.com/v1/standings/now

        Returns:
            Dictionary containing current standings data.
        """
        return await self._get("/v1/standings/now")

    async def get_standings_by_date(self, date: t.Union[str, datetime.date]) -> t.Dict[str, t.Any]:
        """
        Retrieve the standings for a specific date.
        Ref: https://api-web.nhle.com/v1/standings/{date}

        Args:
            date: Date string in YYYY-MM-DD format or a datetime.date object.

        Returns:
            Dictionary containing standings data for the specified date.
        """
        formatted_date = format_date(date)
        path = f"/v1/standings/{formatted_date}"
        return await self._get(path)

    async def get_standings_season_info(self) -> t.Dict[str, t.Any]:
        """
        Retrieves information for each season's standings structure (e.g., available types).
        Ref: https://api-web.nhle.com/v1/standings-season

        Returns:
            Dictionary containing metadata about standings seasons.
        """
        return await self._get("/v1/standings-season")

    # === Stats ===
    async def get_club_stats_now(self, team_tricode: str) -> t.Dict[str, t.Any]:
        """
        Retrieve current statistics for a specific club.
        Ref: https://api-web.nhle.com/v1/club-stats/{team}/now

        Args:
            team_tricode: The three-letter team code (e.g., "TOR", "EDM").

        Returns:
            Dictionary containing the team's current stats.
        """
        path = f"/v1/club-stats/{team_tricode.upper()}/now"
        return await self._get(path)

    async def get_club_stats_season_summary(self, team_tricode: str) -> t.Dict[str, t.Any]:
        """
        Returns an overview of the stats seasons/gametypes played for a specific club.
        Ref: https://api-web.nhle.com/v1/club-stats-season/{team}

        Args:
            team_tricode: The three-letter team code (e.g., "TOR", "EDM").

        Returns:
            Dictionary summarizing the seasons and game types with stats.
        """
        path = f"/v1/club-stats-season/{team_tricode.upper()}"
        return await self._get(path)

    async def get_club_stats_by_season(self, team_tricode: str, season: int, game_type: int) -> t.Dict[str, t.Any]:
        """
        Retrieve the stats for a specific team, season, and game type.
        Ref: https://api-web.nhle.com/v1/club-stats/{team}/{season}/{game-type}

        Args:
            team_tricode: The three-letter team code (e.g., "TOR", "EDM").
            season: Season in YYYYYYYY format (e.g., 20232024).
            game_type: Game type (2 for regular season, 3 for playoffs).

        Returns:
            Dictionary containing team stats for the specified season/type.
        """
        path = f"/v1/club-stats/{team_tricode.upper()}/{season}/{game_type}"
        return await self._get(path)

    async def get_team_scoreboard_now(self, team_tricode: str) -> t.Dict[str, t.Any]:
        """
        Retrieve the scoreboard (recent/upcoming games) for a specific team as of the current moment.
        Ref: https://api-web.nhle.com/v1/scoreboard/{team}/now

        Args:
            team_tricode: The three-letter team code (e.g., "TOR", "EDM").

        Returns:
            Dictionary containing the team's scoreboard data.
        """
        path = f"/v1/scoreboard/{team_tricode.upper()}/now"
        return await self._get(path)

    # === Roster ===
    async def get_roster_now(self, team_tricode: str) -> t.Dict[str, t.Any]:
        """
        Retrieve the roster for a specific team as of the current moment.
        Ref: https://api-web.nhle.com/v1/roster/{team}/current

        Args:
            team_tricode: The three-letter team code (e.g., "TOR", "EDM").

        Returns:
            Dictionary containing the team's current roster.
        """
        path = f"/v1/roster/{team_tricode.upper()}/current"
        return await self._get(path)

    async def get_roster_by_season(self, team_tricode: str, season: int) -> t.Dict[str, t.Any]:
        """
        Retrieve the roster for a specific team and season.
        Ref: https://api-web.nhle.com/v1/roster/{team}/{season}

        Args:
            team_tricode: The three-letter team code (e.g., "TOR", "EDM").
            season: Season in YYYYYYYY format (e.g., 20232024).

        Returns:
            Dictionary containing the team's roster for the specified season.
        """
        path = f"/v1/roster/{team_tricode.upper()}/{season}"
        return await self._get(path)

    async def get_roster_season_summary(self, team_tricode: str) -> t.Dict[str, t.Any]:
        """
        Seems to just return a list of all of the seasons that the team played.
        Ref: https://api-web.nhle.com/v1/roster-season/{team}

        Args:
            team_tricode: The three-letter team code (e.g., "TOR", "EDM").

        Returns:
            Dictionary containing a list of seasons the team existed.
        """
        path = f"/v1/roster-season/{team_tricode.upper()}"
        return await self._get(path)

    # === Prospects ===
    async def get_prospects(self, team_tricode: str) -> t.Dict[str, t.Any]:
        """
        Retrieve prospects for a specific team.
        Ref: https://api-web.nhle.com/v1/prospects/{team}

        Args:
            team_tricode: The three-letter team code (e.g., "TOR", "EDM").

        Returns:
            Dictionary containing the team's prospect data.
        """
        path = f"/v1/prospects/{team_tricode.upper()}"
        return await self._get(path)