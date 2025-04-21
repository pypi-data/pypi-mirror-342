"""
Endpoints for the api.nhle.com/stats/rest API.
"""
from .players import StatsPlayers
from .teams import StatsTeams
from .draft import StatsDraft
from .season import StatsSeason
from .game import StatsGame
from .misc_stats import StatsMisc

__all__ = [
    "StatsPlayers",
    "StatsTeams",
    "StatsDraft",
    "StatsSeason",
    "StatsGame",
    "StatsMisc",
]