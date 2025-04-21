"""
Endpoints for the api-web.nhle.com API.
"""

from .players import Players
from .teams import Teams
from .schedule import Schedule
from .game import Game
from .playoff import Playoff
from .draft import Draft
from .misc import Misc
from .other_web import OtherWeb

__all__ = [
    "Players",
    "Teams",
    "Schedule",
    "Game",
    "Playoff",
    "Draft",
    "Misc",
    "OtherWeb",
]
