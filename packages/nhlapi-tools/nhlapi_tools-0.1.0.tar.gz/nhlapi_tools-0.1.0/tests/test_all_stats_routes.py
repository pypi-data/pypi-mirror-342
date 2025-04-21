import pytest
import asyncio
import json
import traceback
from nhl_api.stats.players import StatsPlayers
from nhl_api.stats.teams import StatsTeams
from nhl_api.stats.draft import StatsDraft
from nhl_api.stats.season import StatsSeason
from nhl_api.stats.game import StatsGame
from nhl_api.stats.misc_stats import StatsMisc
from nhl_api.http_client import HttpClient
from nhl_api.config import STATS_BASE_URL

# Helper: provide test arguments for each stats method

def get_test_args(wrapper_class, method_name):
    args_map = {
        # StatsPlayers
        (StatsPlayers, "get_info"): {},
        (StatsPlayers, "get_skater_leaders"): {"attribute": "points"},
        (StatsPlayers, "get_skater_milestones"): {},
        (StatsPlayers, "get_skater_stats"): {
            "report": "summary",
            "cayenne_exp": "seasonId=20232024",
            "limit": 72,
            "start": 17,
            "sort": "points"
        },
        (StatsPlayers, "get_goalie_leaders"): {"attribute": "gaa"},
        (StatsPlayers, "get_goalie_stats"): {
            "report": "summary",
            "cayenne_exp": "seasonId=20232024",
            "limit": 72,
            "start": 15,
            "sort": "wins"
        },
        (StatsPlayers, "get_goalie_milestones"): {},
        # StatsTeams
        (StatsTeams, "get_info"): {},
        (StatsTeams, "get_by_id"): {"team_id": 10},
        (StatsTeams, "get_team_stats"): {"report": "summary", "cayenne_exp": "seasonId=20232024 and gameTypeId=2"},
        (StatsTeams, "get_franchise_info"): {},
        # StatsDraft
        (StatsDraft, "get_draft_info"): {"cayenne_exp": "draftYear=2023"},
        # StatsGame
        (StatsGame, "get_game_info"): {},
        # StatsSeason
        (StatsSeason, "get_component_season"): {},
        (StatsSeason, "get_season_info"): {},
        # StatsMisc
        (StatsMisc, "get_configuration"): {},
        (StatsMisc, "ping"): {},
        (StatsMisc, "get_country_info"): {},
        (StatsMisc, "get_shift_charts"): {"game_id": 2023020204},
        (StatsMisc, "get_glossary"): {},
        (StatsMisc, "get_content_module"): {"template_key": "landing"},
    }
    return args_map.get((wrapper_class, method_name), {})

WRAPPER_METHODS = [
    (StatsPlayers, [
        "get_info",
        "get_skater_leaders",
        "get_skater_milestones",
        "get_skater_stats",
        "get_goalie_leaders",
        "get_goalie_stats",
        "get_goalie_milestones",
    ]),
    (StatsTeams, [
        "get_info",
        "get_by_id",
        "get_team_stats",
        "get_franchise_info",
    ]),
    (StatsGame, [
        "get_game_info",
    ]),
    (StatsDraft, [
        "get_draft_info",
    ]),
    (StatsSeason, [
        "get_component_season",
        "get_season_info",
    ]),
    (StatsMisc, [
        "get_configuration",
        "ping",
        "get_country_info",
        "get_shift_charts",
        "get_glossary",
        "get_content_module",
    ]),
]

@pytest.mark.asyncio
async def test_all_stats_routes():
    """Test every public method in every NHL Stats API stats wrapper class and print the JSON response."""
    client = HttpClient(STATS_BASE_URL)
    total_routes = 0
    called_routes = 0
    failed_routes = 0
    called_route_names = []
    failed_route_names = []
    tracebacks = []
    for wrapper_class, method_names in WRAPPER_METHODS:
        # All stats wrappers require (client, language)
        instance = wrapper_class(client, "en")
        for method_name in method_names:
            total_routes += 1
            method = getattr(instance, method_name, None)
            route_name = f"{wrapper_class.__name__}.{method_name}"
            if method is None:
                print(f"Method {method_name} not found in {wrapper_class.__name__}")
                failed_routes += 1
                failed_route_names.append(route_name)
                continue
            kwargs = get_test_args(wrapper_class, method_name)
            print(f"\nCalling {route_name}({kwargs})")
            try:
                result = await method(**kwargs)
                called_routes += 1
                called_route_names.append(route_name)
                print(json.dumps(result, indent=2, ensure_ascii=False)[:2000])
            except Exception as e:
                print(f"ERROR calling {route_name}: {e}")
                if hasattr(e, 'status_code'):
                    print("Status code:", getattr(e, 'status_code', None))
                if hasattr(e, 'response'):
                    print("Response text:", getattr(e, 'response', None))
                tb = traceback.format_exc()
                tracebacks.append((route_name, tb))
                failed_routes += 1
                failed_route_names.append(route_name)
    print("\n========== NHL Stats API Route Test Summary ==========")
    print(f"Total routes attempted: {total_routes}")
    print(f"Successful routes: {called_routes}")
    print(f"Failed/missing routes: {failed_routes}")
    if called_route_names:
        print(f"\nSuccessful routes:")
        for name in called_route_names:
            print(f"  - {name}")
    if failed_route_names:
        print(f"\nFailed/missing routes:")
        for name in failed_route_names:
            print(f"  - {name}")
    if tracebacks:
        print("\n========== Tracebacks for Failed Routes ==========")
        for route_name, tb in tracebacks:
            print(f"\nTraceback for {route_name}:\n{tb}")
    assert failed_routes == 0, f"{failed_routes} stats routes failed. See output above."
