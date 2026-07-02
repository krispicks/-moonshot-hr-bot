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
    url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1"

    response = requests.get(url, timeout=10)
    data = response.json()

    game_ids = []

    for date in data.get("dates", []):
        for game in date.get("games", []):
            game_ids.append(game["gamePk"])

    return game_ids


def get_home_run_events(game_pk):
    feed = get_game_feed(game_pk)

    events = []

    all_plays = feed.get("liveData", {}).get("plays", {}).get("allPlays", [])

    for play in all_plays:
        result = play.get("result", {})

        if result.get("event") == "Home Run":

            import json
            print("=" * 60)
            print("HOME RUN FOUND")
            print(json.dumps(play, indent=2))
            print("=" * 60)

            events.append({
                "batter": play["matchup"]["batter"]["fullName"],
                "inning": play["about"]["inning"],
                "half": play["about"]["halfInning"]
            })

    return events
