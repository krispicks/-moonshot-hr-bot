import requests


def get_live_games():
    url = "https://statsapi.mlb.com/api/v1.1/game/changes?updatedSince=1"
    response = requests.get(url, timeout=10)
    return response.json()


def get_game_feed(game_pk):
    url = f"https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live"
    response = requests.get(url, timeout=10)
    return response.json()


def get_today_game_ids():
    games = get_live_games()

    game_ids = []

    for game in games.get("games", []):
        game_ids.append(game["gamePk"])

    return game_ids


def get_home_run_events(game_pk):
    feed = get_game_feed(game_pk)

    events = []

    all_plays = feed.get("liveData", {}).get("plays", {}).get("allPlays", [])

    for play in all_plays:
        result = play.get("result", {})

        if result.get("event") == "Home Run":
            events.append({
                "batter": play["matchup"]["batter"]["fullName"],
                "inning": play["about"]["inning"],
                "half": play["about"]["halfInning"]
            })

    return events