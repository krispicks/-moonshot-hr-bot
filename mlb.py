import requests

BASE_URL = "https://statsapi.mlb.com/api/v1.1"


def get_live_games():
    url = f"{BASE_URL}/game/changes?updatedSince=1"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def get_game_feed(game_pk):
    url = f"{BASE_URL}/game/{game_pk}/feed/live"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def get_today_game_ids():
    data = get_live_games()

    game_ids = []

    for game in data.get("games", []):
        game_ids.append(game["gamePk"])

    return game_ids


def get_home_run_events(game_pk):
    feed = get_game_feed(game_pk)

    home_runs = []

    plays = (
        feed.get("liveData", {})
        .get("plays", {})
        .get("allPlays", [])
    )

    for play in plays:
        result = play.get("result", {})

        if result.get("event") == "Home Run":
            home_runs.append({
                "batter": result.get("description"),
                "inning": play.get("about", {}).get("inning"),
                "half": play.get("about", {}).get("halfInning"),
            })

    return home_runs