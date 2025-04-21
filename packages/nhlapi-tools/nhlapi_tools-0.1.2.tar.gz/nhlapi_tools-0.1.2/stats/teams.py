"""
Endpoints related to Teams (api.nhle.com/stats/rest/{lang}/team/*, etc.)
"""

import typing as t
from .base import StatsEndpointCategory

# Common report names can be defined as constants if desired
# e.g., TEAM_SUMMARY_REPORT = "summary"


class StatsTeams(StatsEndpointCategory):
    """Handles Stats API endpoints related to team information, stats, and franchises."""

    async def get_info(self) -> t.Dict[str, t.Any]:
        """
        Retrieve list of all teams.
        Ref: https://api.nhle.com/stats/rest/{lang}/team

        Returns:
            Dictionary containing a list of teams and total count.
        """
        return await self._get("/team")

    async def get_by_id(self, team_id: int) -> t.Dict[str, t.Any]:
        """
        Retrieve information for a specific team by ID.
        Ref: https://api.nhle.com/stats/rest/{lang}/team/id/{id}

        Args:
            team_id: The numeric ID of the team.

        Returns:
            Dictionary containing information for the specified team.
        """
        # Note: The documentation shows {id} but it likely refers to the team ID.
        # The endpoint structure might actually be part of a cayenneExp on /team,
        # or this path is correct. Needs testing. Assuming path for now.
        # path = f"/team/id/{team_id}" # This path seems less likely for REST/stats
        # Let's assume it's filtered via cayenneExp on the main /team endpoint
        params = {"cayenneExp": f"id={team_id}"}
        return await self._get("/team", params=params)
        # If the above doesn't work, try the path approach:
        # path = f"/team/id/{team_id}"
        # return await self._get(path)

    async def get_team_stats(
        self,
        report: str,
        cayenne_exp: t.Optional[str] = None,  # Usually Required for meaningful data
        is_aggregate: t.Optional[bool] = None,
        is_game: t.Optional[bool] = None,
        fact_cayenne_exp: t.Optional[str] = None,
        include: t.Optional[str] = None,
        exclude: t.Optional[str] = None,
        sort: t.Optional[str] = None,
        dir: t.Optional[str] = None,
        start: t.Optional[int] = None,
        limit: t.Optional[int] = None,
    ) -> t.Dict[str, t.Any]:
        """
        Retrieve team stats for a specific report, filtered by cayenneExp.
        Ref: https://api.nhle.com/stats/rest/{lang}/team/{report}

        Args:
            report: The name of the report (e.g., "summary", "powerplay", "penaltykill", "realtime").
            cayenne_exp: Filter expression (e.g., "seasonId=20232024 and gameTypeId=2", "teamId=10"). Usually required.
            is_aggregate: Aggregate results (boolean).
            is_game: Filter by game (boolean).
            fact_cayenne_exp: Additional filter expression.
            include: Fields to include.
            exclude: Fields to exclude.
            sort: Field to sort by (e.g., "points", "wins", "goalsFor").
            dir: Sort direction ("ASC" or "DESC").
            start: Pagination start index.
            limit: Pagination limit (-1 for all).

        Returns:
            Dictionary containing team stats for the specified report and filters.
        """
        params = {}
        if cayenne_exp:
            params["cayenneExp"] = cayenne_exp  # Often required
        if is_aggregate is not None:
            params["isAggregate"] = str(is_aggregate).lower()
        if is_game is not None:
            params["isGame"] = str(is_game).lower()
        if fact_cayenne_exp:
            params["factCayenneExp"] = fact_cayenne_exp
        if include:
            params["include"] = include
        if exclude:
            params["exclude"] = exclude
        if sort:
            params["sort"] = sort
        if dir:
            params["dir"] = dir
        if start is not None:
            params["start"] = start
        if limit is not None:
            params["limit"] = limit

        path = f"/team/{report}"
        return await self._get(path, params=params)

    async def get_franchise_info(self) -> t.Dict[str, t.Any]:
        """
        Retrieve list of all franchises.
        Ref: https://api.nhle.com/stats/rest/{lang}/franchise

        Returns:
            Dictionary containing franchise data.
        """
        return await self._get("/franchise")
