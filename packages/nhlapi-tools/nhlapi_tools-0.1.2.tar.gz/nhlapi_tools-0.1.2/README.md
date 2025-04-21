# NHL API Python Wrapper

An asynchronous Python wrapper for the official (but undocumented) NHL APIs:
`api-web.nhle.com` and `api.nhle.com/stats/rest`.

**Note:** This library interacts with APIs that are not officially documented or supported by the NHL. Use at your own risk. API changes may break this library without notice.

## Features

- Async Python wrapper for both the NHL Web API (`api-web.nhle.com`) and Stats API (`api.nhle.com/stats/rest`).
- Two main clients:
  - `NHLWebClient`: For web endpoints (players, teams, schedule, games, playoffs, drafts, misc, other web).
  - `NHLStatsClient`: For stats endpoints (players, teams, draft, season, game, misc).
- Easy-to-use endpoint categories as attributes (e.g., `client.players`, `client.teams`).
- Custom exception handling for API errors.

## Installation

```bash
pip install nhlapi-tools # Or clone and pip install .
```

Or for development:
```bash
git clone https://github.com/brrainey13/nhl-api.git
cd nhl-api
pip install -e .
```

## Basic Usage (api-web.nhle.com)

```python
import asyncio
from nhl_api import NHLWebClient
from nhl_api.exceptions import NHLAPIError

async def main():
    async with NHLWebClient() as client:
        try:
            # Get player landing info (Auston Matthews)
            player_info = await client.players.get_landing(player_id=8477934)
            print(f"Player: {player_info['firstName']['default']} {player_info['lastName']['default']}")
            print(f"Team: {player_info['currentTeamAbbrev']}")
            print(f"Position: {player_info['position']}")

            # Get today's standings
            standings = await client.teams.get_standings_now()
            print(f"\nStandings Date: {standings['standingsDate']}")

            # Get game log for Connor McDavid, 2023-2024 Regular Season
            game_log = await client.players.get_game_log(
                player_id=8478402,
                season=20232024,
                game_type=2 # 2=Regular Season, 3=Playoffs
            )
            print(f"\nMcDavid Game Log (First 5 Games):")
            for game in game_log['gameLog'][:5]:
                print(f"  Date: {game['gameDate']}, Opp: {game['opponentAbbrev']}, G: {game['goals']}, A: {game['assists']}")

            # Get schedule for a specific date
            schedule = await client.schedule.get_schedule_by_date(date="2023-11-10")
            print(f"\nSchedule for 2023-11-10:")
            for date_info in schedule['gameWeek']:
                if date_info['date'] == "2023-11-10":
                    for game in date_info['games']:
                        print(f"  {game['awayTeam']['abbrev']} @ {game['homeTeam']['abbrev']} ({game['gameTypeDescription']}) - State: {game['gameState']}")
        except NHLAPIError as e:
            print(f"API Error: Status={e.status_code}, Message={e.message}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())

## Basic Usage (api.nhle.com/stats/rest)

```python
import asyncio
from nhl_api import NHLStatsClient

async def main():
    async with NHLStatsClient() as stats_client:
        # Get skater points leaders
        leaders = await stats_client.players.get_skater_leaders("points")
        print("Top points leader:", leaders['data'][0]['player']['fullName'])

        # Get team stats
        team_stats = await stats_client.teams.get_team_stats(team_id=10)
        print("Team stats:", team_stats)

if __name__ == "__main__":
    asyncio.run(main())

## Endpoint Categories

**NHLWebClient**
- `players`: Player info, stats, game logs, bios, etc.
- `teams`: Team info, rosters, standings.
- `schedule`: Schedules, calendar.
- `game`: Game scores, events, boxscores.
- `playoff`: Playoff info.
- `draft`: Draft info.
- `misc`: Miscellaneous endpoints.
- `other_web`: Other endpoints (season, where to watch, odds, etc.)

**NHLStatsClient**
- `players`: Stats leaders, skater/goalie stats, bios.
- `teams`: Team stats, franchise info.
- `draft`: Draft picks, history.
- `season`: Season info.
- `game`: Game stats, summaries.
- `misc`: Miscellaneous endpoints.

## Error Handling

All API errors raise `NHLAPIError` or a subclass. Example:

```python
from nhl_api.exceptions import NHLAPIError
try:
    ... # API call
except NHLAPIError as e:
    print(f"API Error: Status={e.status_code}, Message={e.message}")
```

## Requirements

- Python 3.8+
- `httpx` (see `requirements-dev.txt` for dev dependencies)

## Further Documentation

- See [`nhl_api.md`](./nhl_api.md) for detailed endpoint and usage documentation.
- The code is documented with docstrings.

## Contributing

Pull requests and issues are welcome! Please open an issue for bugs or feature requests.

---

**Disclaimer:** This project is not affiliated with or endorsed by the NHL. The APIs are undocumented and may change or break without notice.