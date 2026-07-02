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
    def get_home_run_events(game_pk):
    """Return all home run events from a game."""
    feed = get_game_feed(game_pk)

    home_runs = []

    plays = feed.get("liveData", {}).get("plays", {}).get("allPlays", [])

    for play in plays:
        result = play.get("result", {})

        if result.get("event") == "Home Run":
            home_runs.append({
                "batter": result.get("description"),
                "inning": play.get("about", {}).get("inning"),
                "half": play.get("about", {}).get("halfInning"),
            })

    return home_runs