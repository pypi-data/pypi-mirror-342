import pytest
import asyncio
from nhl_api import NHLWebClient

@pytest.mark.asyncio
async def test_web_client_context():
    """Test that NHLWebClient can be used as an async context manager and exposes endpoints."""
    async with NHLWebClient() as client:
        assert hasattr(client, "players")
        assert hasattr(client, "teams")
        assert hasattr(client, "schedule")

@pytest.mark.asyncio
async def test_get_standings_now(monkeypatch):
    """Test teams.get_standings_now() with a mocked response."""
    class MockTeams:
        async def get_standings_now(self):
            return {
                'standingsDateTimeUtc': '2025-04-19T20:29:46Z',
                'standings': [
                    {'teamAbbrev': {'default': 'WPG'}, 'points': 116},
                    {'teamAbbrev': {'default': 'WSH'}, 'points': 111},
                ]
            }
    async with NHLWebClient() as client:
        monkeypatch.setattr(client, "teams", MockTeams())
        standings = await client.teams.get_standings_now()
        assert standings['standings'][0]['teamAbbrev']['default'] == 'WPG'
        assert standings['standings'][1]['points'] == 111

@pytest.mark.asyncio
async def test_players_get_landing(monkeypatch):
    """Test players.get_landing with a mocked response."""
    class MockPlayers:
        async def get_landing(self, player_id):
            return {'firstName': {'default': 'Auston'}, 'lastName': {'default': 'Matthews'}}
    async with NHLWebClient() as client:
        monkeypatch.setattr(client, "players", MockPlayers())
        player = await client.players.get_landing(8477934)
        assert player['firstName']['default'] == 'Auston'
        assert player['lastName']['default'] == 'Matthews'
