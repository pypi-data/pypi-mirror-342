"""
Endpoints related to Game Information (api-web.nhle.com/v1/score/*, /v1/gamecenter/* etc.)
"""

import typing as t
import datetime
from .base import WebEndpointCategory
from ..utils import format_date


class Game(WebEndpointCategory):
    """Handles endpoints related to game scores, events, boxscores, etc."""

    # === Daily Scores ===
    async def get_scores_now(self) -> t.Dict[str, t.Any]:
        """
        Retrieve daily scores as of the current moment (usually today's games).
        Ref: https://api-web.nhle.com/v1/score/now

        Returns:
            Dictionary containing current score data.
        """
        return await self._get("/v1/score/now")

    async def get_scores_by_date(
        self, date: t.Union[str, datetime.date]
    ) -> t.Dict[str, t.Any]:
        """
        Retrieve daily scores for a specific date.
        Ref: https://api-web.nhle.com/v1/score/{date}

        Args:
            date: Date string in YYYY-MM-DD format or a datetime.date object.

        Returns:
            Dictionary containing score data for the specified date.
        """
        formatted_date = format_date(date)
        path = f"/v1/score/{formatted_date}"
        return await self._get(path)

    async def get_scoreboard_now(self) -> t.Dict[str, t.Any]:
        """
        Retrieve the overall scoreboard as of the current moment. Similar to get_scores_now.
        Ref: https://api-web.nhle.com/v1/scoreboard/now

        Returns:
            Dictionary containing current scoreboard data.
        """
        return await self._get("/v1/scoreboard/now")

    # === Game Events (Gamecenter) ===
    async def get_play_by_play(self, game_id: int) -> t.Dict[str, t.Any]:
        """
        Retrieve play-by-play information for a specific game.
        Ref: https://api-web.nhle.com/v1/gamecenter/{game-id}/play-by-play

        Args:
            game_id: The NHL Game ID.

        Returns:
            Dictionary containing the game's play-by-play data.
        """
        path = f"/v1/gamecenter/{game_id}/play-by-play"
        return await self._get(path)

    async def get_landing(self, game_id: int) -> t.Dict[str, t.Any]:
        """
        Retrieve landing page summary information for a specific game.
        Ref: https://api-web.nhle.com/v1/gamecenter/{game-id}/landing

        Args:
            game_id: The NHL Game ID.

        Returns:
            Dictionary containing the game's landing page data (summary, rosters, etc.).
        """
        path = f"/v1/gamecenter/{game_id}/landing"
        return await self._get(path)

    async def get_boxscore(self, game_id: int) -> t.Dict[str, t.Any]:
        """
        Retrieve boxscore information for a specific game.
        Ref: https://api-web.nhle.com/v1/gamecenter/{game-id}/boxscore

        Args:
            game_id: The NHL Game ID.

        Returns:
            Dictionary containing the game's boxscore data.
        """
        path = f"/v1/gamecenter/{game_id}/boxscore"
        return await self._get(path)

    async def get_game_story(self, game_id: int) -> t.Dict[str, t.Any]:
        """
        Retrieve game story (recap, articles) information for a specific game.
        Ref: https://api-web.nhle.com/v1/wsc/game-story/{game-id}

        Args:
            game_id: The NHL Game ID.

        Returns:
            Dictionary containing game story content.
        """
        # Note: Path uses /wsc/ prefix
        path = f"/v1/wsc/game-story/{game_id}"
        return await self._get(path)

    # === Game Replays === (Moved from Misc to Game as they are game-specific)
    async def get_goal_replay(self, game_id: int, event_id: int) -> t.Dict[str, t.Any]:
        """
        Retrieves goal replay information (video links, etc.) for a specific game event.
        Ref: https://api-web.nhle.com/v1/ppt-replay/goal/{game-id}/{event-number}

        Args:
            game_id: The NHL Game ID.
            event_id: The event number (eventId from play-by-play) within the game.

        Returns:
            Dictionary containing goal replay details.
        """
        path = f"/v1/ppt-replay/goal/{game_id}/{event_id}"
        return await self._get(path)

    async def get_play_replay(self, game_id: int, event_id: int) -> t.Dict[str, t.Any]:
        """
        Retrieves general play replay information for a specific game event.
        Ref: https://api-web.nhle.com/v1/ppt-replay/{game-id}/{event-number}

        Args:
            game_id: The NHL Game ID.
            event_id: The event number (eventId from play-by-play) within the game.

        Returns:
            Dictionary containing play replay details. Might be similar/identical to goal replay for goals.
        """
        path = f"/v1/ppt-replay/{game_id}/{event_id}"
        return await self._get(path)

    # === Additional Game Content === (Moved from Misc)
    async def get_game_right_rail(self, game_id: int) -> t.Dict[str, t.Any]:
        """
        Retrieves sidebar content typically shown in the game center view.
        Ref: https://api-web.nhle.com/v1/gamecenter/{game-id}/right-rail

        Args:
            game_id: The NHL Game ID.

        Returns:
            Dictionary containing right rail content modules.
        """
        path = f"/v1/gamecenter/{game_id}/right-rail"
        return await self._get(path)

    async def get_wsc_play_by_play(self, game_id: int) -> t.Dict[str, t.Any]:
        """
        Retrieves WSC (World Showcase?) play-by-play information. May differ from standard PBP.
        Ref: https://api-web.nhle.com/v1/wsc/play-by-play/{game-id}

        Args:
            game_id: The NHL Game ID.

        Returns:
            Dictionary containing WSC play-by-play data.
        """
        # Note: Path uses /wsc/ prefix
        path = f"/v1/wsc/play-by-play/{game_id}"
        return await self._get(path)
