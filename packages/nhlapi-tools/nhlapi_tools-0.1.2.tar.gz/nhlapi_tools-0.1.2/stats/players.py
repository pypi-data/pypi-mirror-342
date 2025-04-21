"""
Endpoints related to Players (api.nhle.com/stats/rest/{lang}/players/*, etc.)
"""

import typing as t
from .base import StatsEndpointCategory

# Common report names can be defined as constants if desired
# e.g., SKATER_SUMMARY_REPORT = "summary"


class StatsPlayers(StatsEndpointCategory):
    """Handles Stats API endpoints related to player information, stats, leaders, and milestones."""

    AVAILABLE_REPORT_TYPES = [
        "summary",
        "bios",
        "faceoffpercentages",
        "faceoffwins",
        "goalsForAgainst",
        "realtime",
        "penalties",
        "penaltykill",
        "penaltyShots",
        "powerplay",
        "puckPossessions",
        "summaryshooting",
        "percentages",
        "scoringRates",
        "scoringpergame",
        "shootout",
        "shottype",
        "timeonice",
    ]
    """
    List of available report types for skater/goalie stats endpoints.
    """

    # === Generic Player Info ===
    async def get_info(self) -> t.Dict[str, t.Any]:
        """
        Retrieve general player information (list).
        Ref: https://api.nhle.com/stats/rest/{lang}/players

        Returns:
            Dictionary containing a list of players and total count.
        """
        return await self._get("/players")

    # === Skaters ===
    async def get_skater_leaders(self, attribute: str) -> t.Dict[str, t.Any]:
        """
        Retrieve skater leaders for a specific attribute.
        Ref: https://api.nhle.com/stats/rest/{lang}/leaders/skaters/{attribute}

        Args:
            attribute: The skater attribute to get leaders for (e.g., "points", "goals", "assists").

        Returns:
            Dictionary containing skater leaders for the specified attribute.
        """
        path = f"/leaders/skaters/{attribute}"
        return await self._get(path)

    async def get_skater_milestones(self) -> t.Dict[str, t.Any]:
        """
        Retrieve skater milestones.
        Ref: https://api.nhle.com/stats/rest/{lang}/milestones/skaters

        Returns:
            Dictionary containing skater milestone data.
        """
        return await self._get("/milestones/skaters")

    async def get_skater_stats(
        self,
        report: str,
        cayenne_exp: str,  # Required for most reports
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
        Retrieve skater stats for a specific report, filtered by cayenneExp.
        Ref: https://api.nhle.com/stats/rest/{lang}/skater/{report}

        Args:
            report: The name of the report (e.g., "summary", "bios", "realtime", "faceoffwins", etc.).
            cayenne_exp: REQUIRED filter expression (e.g., "seasonId=20232024 and gameTypeId=2", "playerId=8478402").
                         See API docs or experiment for syntax.
            is_aggregate: Aggregate results (boolean).
            is_game: Filter by game (boolean).
            fact_cayenne_exp: Additional filter expression.
            include: Fields to include.
            exclude: Fields to exclude.
            sort: Field to sort by (e.g., "points", "goals").
            dir: Sort direction ("ASC" or "DESC").
            start: Pagination start index.
            limit: Pagination limit (-1 for all).

        Returns:
            Dictionary containing skater stats for the specified report and filters.
        """
        params = {"cayenneExp": cayenne_exp}  # Required param
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

        path = f"/skater/{report}"
        return await self._get(path, params=params)

    # === Goalies ===
    async def get_goalie_leaders(self, attribute: str) -> t.Dict[str, t.Any]:
        """
        Retrieve goalie leaders for a specific attribute.
        Ref: https://api.nhle.com/stats/rest/{lang}/leaders/goalies/{attribute}

        Args:
            attribute: The goalie attribute to get leaders for (e.g., "gaa", "wins", "savePct").

        Returns:
            Dictionary containing goalie leaders for the specified attribute.
        """
        path = f"/leaders/goalies/{attribute}"
        return await self._get(path)

    async def get_goalie_stats(
        self,
        report: str,
        cayenne_exp: str,  # Required for most reports
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
        Retrieve goalie stats for a specific report, filtered by cayenneExp.
        Ref: https://api.nhle.com/stats/rest/{lang}/goalie/{report}

        Args:
            report: The name of the report (e.g., "summary", "bios", "realtime", etc.).
            cayenne_exp: REQUIRED filter expression (e.g., "seasonId=20232024 and gameTypeId=2", "playerId=8479394").
                         See API docs or experiment for syntax.
            is_aggregate: Aggregate results (boolean).
            is_game: Filter by game (boolean).
            fact_cayenne_exp: Additional filter expression.
            include: Fields to include.
            exclude: Fields to exclude.
            sort: Field to sort by (e.g., "wins", "gaa").
            dir: Sort direction ("ASC" or "DESC").
            start: Pagination start index.
            limit: Pagination limit (-1 for all).

        Returns:
            Dictionary containing goalie stats for the specified report and filters.
        """
        params = {"cayenneExp": cayenne_exp}  # Required param
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

        path = f"/goalie/{report}"
        return await self._get(path, params=params)

    async def get_goalie_milestones(self) -> t.Dict[str, t.Any]:
        """
        Retrieve goalie milestones.
        Ref: https://api.nhle.com/stats/rest/{lang}/milestones/goalies

        Returns:
            Dictionary containing goalie milestone data.
        """
        return await self._get("/milestones/goalies")
