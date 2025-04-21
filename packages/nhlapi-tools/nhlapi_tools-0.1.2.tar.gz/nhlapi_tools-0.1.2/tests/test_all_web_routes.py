import pytest
import json
from nhl_api.web.teams import Teams
from nhl_api.web.schedule import Schedule
from nhl_api.web.game import Game
from nhl_api.web.playoff import Playoff
from nhl_api.web.other_web import OtherWeb
from nhl_api.web.misc import Misc
from nhl_api.web.players import Players
from nhl_api.web.draft import Draft
from nhl_api.http_client import HttpClient
from nhl_api.config import WEB_BASE_URL
import traceback


def get_valid_game_id():
    """Return a recent valid NHL game ID for testing endpoints like get_landing."""
    # Use the confirmed valid game ID from user: 2024030141
    return 2024030141


def get_test_args(wrapper_class, method_name):
    # Disambiguate overloaded method names by class
    if wrapper_class.__name__ == "Players" and method_name == "get_landing":
        return {"player_id": 8477934}
    if wrapper_class.__name__ == "Game" and method_name == "get_landing":
        return {"game_id": get_valid_game_id()}
    args_map = {
        "get_standings_now": {},
        "get_standings_by_date": {"date": "2024-04-15"},
        "get_standings_season_info": {},
        "get_club_stats_now": {"team_tricode": "TOR"},
        "get_club_stats_season_summary": {"team_tricode": "TOR"},
        "get_club_stats_by_season": {
            "team_tricode": "TOR",
            "season": "20232024",
            "game_type": 2,
        },
        "get_team_scoreboard_now": {"team_tricode": "TOR"},
        "get_roster_now": {"team_tricode": "TOR"},
        "get_roster_by_season": {"team_tricode": "TOR", "season": "20232024"},
        "get_roster_season_summary": {"team_tricode": "TOR"},
        "get_prospects": {"team_tricode": "TOR"},
        "get_team_season_schedule_now": {"team_tricode": "TOR"},
        "get_team_season_schedule": {"team_tricode": "TOR", "season": "20232024"},
        "get_team_month_schedule_now": {"team_tricode": "TOR"},
        "get_team_month_schedule": {"team_tricode": "TOR", "month": "2024-04"},
        "get_team_week_schedule": {"team_tricode": "TOR", "date": "2024-04-15"},
        "get_team_week_schedule_now": {"team_tricode": "TOR"},
        "get_schedule_now": {},
        "get_schedule_by_date": {"date": "2024-04-15"},
        "get_schedule_calendar_now": {},
        "get_schedule_calendar_by_date": {"date": "2024-04-15"},
        "get_scores_by_date": {"date": "2024-04-15"},
        "get_play_by_play": {"game_id": get_valid_game_id()},
        "get_boxscore": {"game_id": get_valid_game_id()},
        "get_game_story": {"game_id": get_valid_game_id()},
        "get_goal_replay": {"game_id": get_valid_game_id(), "event_id": 1},
        "get_play_replay": {"game_id": get_valid_game_id(), "event_id": 1},
        "get_game_right_rail": {"game_id": get_valid_game_id()},
        "get_wsc_play_by_play": {"game_id": get_valid_game_id()},
        "get_series_carousel": {"season": 20232024},
        "get_series_schedule": {"season": 20232024, "series_letter": "A"},
        "get_bracket": {"year": 2024},
        "get_series_metadata": {"year": 2023, "series_letter": "A"},
        "get_where_to_watch": {},
        "get_tv_schedule_by_date": {"date": "2024-04-15"},
        "get_tv_schedule_now": {},
        "get_partner_game_odds_now": {"country_code": "US"},
        "get_seasons": {},
        "get_meta_info": {},
        "get_meta_game_info": {"game_id": get_valid_game_id()},
        "get_location": {},
        "get_postal_code_info": {"postal_code": "10001"},
        "get_game_log": {"player_id": 8477934, "season": 20232024, "game_type": 2},
        "get_game_log_now": {"player_id": 8477934},
        "get_skater_stats_leaders_current": {},
        "get_skater_stats_leaders_by_season": {"season": 20232024, "game_type": 2},
        "get_goalie_stats_leaders_current": {},
        "get_goalie_stats_leaders_by_season": {"season": 20232024, "game_type": 2},
        "get_player_spotlight": {},
        "get_rankings_now": {},
        "get_rankings_by_prospect_category": {
            "season_year": 2023,
            "prospect_category": 1,
        },
        "get_tracker_picks_now": {},
        "get_picks_now": {},
        "get_picks_by_season": {"season_year": 2023, "round_number": "all"},
    }
    return args_map.get(method_name, {})


WRAPPER_METHODS = [
    (
        Teams,
        [
            "get_standings_now",
            "get_standings_by_date",
            "get_standings_season_info",
            "get_club_stats_now",
            "get_club_stats_season_summary",
            "get_club_stats_by_season",
            "get_team_scoreboard_now",
            "get_roster_now",
            "get_roster_by_season",
            "get_roster_season_summary",
            "get_prospects",
        ],
    ),
    (
        Schedule,
        [
            "get_team_season_schedule_now",
            "get_team_season_schedule",
            "get_team_month_schedule_now",
            "get_team_month_schedule",
            "get_team_week_schedule",
            "get_team_week_schedule_now",
            "get_schedule_now",
            "get_schedule_by_date",
            "get_schedule_calendar_now",
            "get_schedule_calendar_by_date",
        ],
    ),
    (
        Game,
        [
            "get_scores_now",
            "get_scores_by_date",
            "get_scoreboard_now",
            "get_play_by_play",
            "get_landing",
            "get_boxscore",
            "get_game_story",
            "get_goal_replay",
            "get_play_replay",
            "get_game_right_rail",
            "get_wsc_play_by_play",
        ],
    ),
    (
        Playoff,
        [
            "get_series_carousel",
            "get_series_schedule",
            "get_bracket",
            "get_series_metadata",
        ],
    ),
    (
        OtherWeb,
        [
            "get_where_to_watch",
            "get_tv_schedule_by_date",
            "get_tv_schedule_now",
            "get_partner_game_odds_now",
            "get_seasons",
        ],
    ),
    (
        Misc,
        [
            "get_meta_info",
            "get_meta_game_info",
            "get_location",
            "get_postal_code_info",
        ],
    ),
    (
        Players,
        [
            "get_game_log",
            "get_landing",
            "get_game_log_now",
            "get_skater_stats_leaders_current",
            "get_skater_stats_leaders_by_season",
            "get_goalie_stats_leaders_current",
            "get_goalie_stats_leaders_by_season",
            "get_player_spotlight",
        ],
    ),
    (
        Draft,
        [
            "get_rankings_now",
            "get_rankings_by_prospect_category",
            "get_tracker_picks_now",
            "get_picks_now",
            "get_picks_by_season",
        ],
    ),
]


@pytest.mark.asyncio
async def test_all_web_routes():
    """Test every public method in every NHL API web wrapper class and print the JSON response."""
    client = HttpClient(WEB_BASE_URL)
    total_routes = 0
    called_routes = 0
    failed_routes = 0
    called_route_names = []
    failed_route_names = []
    tracebacks = []
    for wrapper_class, method_names in WRAPPER_METHODS:
        instance = wrapper_class(client)
        for method_name in method_names:
            total_routes += 1
            method = getattr(instance, method_name, None)
            route_name = f"{wrapper_class.__name__}.{method_name}"
            if method is None:
                print(f"Method {method_name} not found in {wrapper_class.__name__}")
                failed_routes += 1
                failed_route_names.append(route_name)
                continue
            # Use new arg mapping
            kwargs = get_test_args(wrapper_class, method_name)
            # Optionally skip known 404s
            if route_name == "Misc.get_openapi_spec":
                print(f"Skipping {route_name} (known 404)")
                continue
            print(f"\nCalling {route_name}({kwargs})")
            try:
                result = await method(**kwargs)
                called_routes += 1
                called_route_names.append(route_name)
                print(json.dumps(result, indent=2, ensure_ascii=False)[:2000])
            except Exception as e:
                print(f"ERROR calling {route_name}: {e}")
                if hasattr(e, "status_code"):
                    print("Status code:", getattr(e, "status_code", None))
                if hasattr(e, "response"):
                    print("Response text:", getattr(e, "response", None))
                tb = traceback.format_exc()
                tracebacks.append((route_name, tb))
                failed_routes += 1
                failed_route_names.append(route_name)
    print("\n========== NHL API Web Route Test Summary ==========")
    print(f"Total routes attempted: {total_routes}")
    print(f"Successful routes: {called_routes}")
    print(f"Failed/missing routes: {failed_routes}")
    if called_route_names:
        print("\nSuccessful routes:")
        for name in called_route_names:
            print(f"  - {name}")
    if failed_route_names:
        print("\nFailed/missing routes:")
        for name in failed_route_names:
            print(f"  - {name}")
    if tracebacks:
        print("\n========== Tracebacks for Failed Routes ==========")
        for route_name, tb in tracebacks:
            print(f"\nTraceback for {route_name}:\n{tb}")
