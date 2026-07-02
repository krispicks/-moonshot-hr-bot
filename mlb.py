import requests

BASE_URL = "https://statsapi.mlb.com/api/v1"


def get_schedule():
    """Return today's MLB schedule."""
    url = f"{BASE_URL}/schedule?sportId=1"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def get_game_feed(game_pk):
    """Return the live feed for one game."""
    url = f"{BASE_URL}/game/{game_pk}/feed/live"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def get_today_game_ids():
    """Return a list of today's game IDs."""
    schedule = get_schedule()

    game_ids = []

    for date in schedule.get("dates", []):
        for game in date.get("games", []):
            game_ids.append(game["gamePk"])

    return game_ids