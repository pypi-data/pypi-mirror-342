"""
Endpoints related to League and Team Schedules (api-web.nhle.com/v1/schedule/*, etc.)
"""
import typing as t
import datetime
from .base import WebEndpointCategory
from ..utils import format_date

class Schedule(WebEndpointCategory):
    """Handles endpoints related to league-wide and team-specific schedules."""

    # === Team Schedule ===
    async def get_team_season_schedule_now(self, team_tricode: str) -> t.Dict[str, t.Any]:
        """
        Retrieve the current season schedule for a specific team.
        Ref: https://api-web.nhle.com/v1/club-schedule-season/{team}/now

        Args:
            team_tricode: The three-letter team code (e.g., "TOR", "EDM").

        Returns:
            Dictionary containing the team's current season schedule.
        """
        path = f"/v1/club-schedule-season/{team_tricode.upper()}/now"
        return await self._get(path)

    async def get_team_season_schedule(self, team_tricode: str, season: int) -> t.Dict[str, t.Any]:
        """
        Retrieve the season schedule for a specific team and season.
        Ref: https://api-web.nhle.com/v1/club-schedule-season/{team}/{season}

        Args:
            team_tricode: The three-letter team code (e.g., "TOR", "EDM").
            season: Season in YYYYYYYY format (e.g., 20232024).

        Returns:
            Dictionary containing the team's schedule for the specified season.
        """
        path = f"/v1/club-schedule-season/{team_tricode.upper()}/{season}"
        return await self._get(path)

    async def get_team_month_schedule_now(self, team_tricode: str) -> t.Dict[str, t.Any]:
        """
        Retrieve the monthly schedule for a specific team for the current month.
        Ref: https://api-web.nhle.com/v1/club-schedule/{team}/month/now

        Args:
            team_tricode: The three-letter team code (e.g., "TOR", "EDM").

        Returns:
            Dictionary containing the team's schedule for the current month.
        """
        path = f"/v1/club-schedule/{team_tricode.upper()}/month/now"
        return await self._get(path)

    async def get_team_month_schedule(self, team_tricode: str, month: str) -> t.Dict[str, t.Any]:
        """
        Retrieve the monthly schedule for a specific team and month.
        Ref: https://api-web.nhle.com/v1/club-schedule/{team}/month/{month}

        Args:
            team_tricode: The three-letter team code (e.g., "TOR", "EDM").
            month: Month in YYYY-MM format (e.g., "2023-11").

        Returns:
            Dictionary containing the team's schedule for the specified month.
        """
        # Add validation for YYYY-MM format if desired
        path = f"/v1/club-schedule/{team_tricode.upper()}/month/{month}"
        return await self._get(path)

    async def get_team_week_schedule(self, team_tricode: str, date: t.Union[str, datetime.date]) -> t.Dict[str, t.Any]:
        """
        Retrieve the weekly schedule for a specific team containing the specified date.
        Ref: https://api-web.nhle.com/v1/club-schedule/{team}/week/{date}

        Args:
            team_tricode: The three-letter team code (e.g., "TOR", "EDM").
            date: Date string in YYYY-MM-DD format or a datetime.date object.

        Returns:
            Dictionary containing the team's weekly schedule around the given date.
        """
        formatted_date = format_date(date)
        path = f"/v1/club-schedule/{team_tricode.upper()}/week/{formatted_date}"
        return await self._get(path)

    async def get_team_week_schedule_now(self, team_tricode: str) -> t.Dict[str, t.Any]:
        """
        Retrieve the weekly schedule for a specific team for the current week.
        Ref: https://api-web.nhle.com/v1/club-schedule/{team}/week/now

        Args:
            team_tricode: The three-letter team code (e.g., "TOR", "EDM").

        Returns:
            Dictionary containing the team's schedule for the current week.
        """
        path = f"/v1/club-schedule/{team_tricode.upper()}/week/now"
        return await self._get(path)

    # === League Schedule Information ===
    async def get_schedule_now(self) -> t.Dict[str, t.Any]:
        """
        Retrieve the current league-wide schedule (usually today's games).
        Ref: https://api-web.nhle.com/v1/schedule/now

        Returns:
            Dictionary containing the current league schedule.
        """
        return await self._get("/v1/schedule/now")

    async def get_schedule_by_date(self, date: t.Union[str, datetime.date]) -> t.Dict[str, t.Any]:
        """
        Retrieve the league-wide schedule for a specific date.
        Ref: https://api-web.nhle.com/v1/schedule/{date}

        Args:
            date: Date string in YYYY-MM-DD format or a datetime.date object.

        Returns:
            Dictionary containing the league schedule for the specified date.
        """
        formatted_date = format_date(date)
        path = f"/v1/schedule/{formatted_date}"
        return await self._get(path)

    # === Schedule Calendar ===
    async def get_schedule_calendar_now(self) -> t.Dict[str, t.Any]:
        """
        Retrieve the schedule calendar overview for the current month.
        Ref: https://api-web.nhle.com/v1/schedule-calendar/now

        Returns:
            Dictionary representing the current schedule calendar.
        """
        return await self._get("/v1/schedule-calendar/now")

    async def get_schedule_calendar_by_date(self, date: t.Union[str, datetime.date]) -> t.Dict[str, t.Any]:
        """
        Retrieve the schedule calendar overview for the month containing the specified date.
        Ref: https://api-web.nhle.com/v1/schedule-calendar/{date}

        Args:
            date: Date string in YYYY-MM-DD format or a datetime.date object.

        Returns:
            Dictionary representing the schedule calendar for the specified month.
        """
        formatted_date = format_date(date)
        path = f"/v1/schedule-calendar/{formatted_date}"
        return await self._get(path)