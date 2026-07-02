import requests

def get_live_games():
    url = "https://statsapi.mlb.com/api/v1.1/game/changes?updatedSince=1"
    response = requests.get(url, timeout=10)
    return response.json()

def get_game_feed(game_pk):
    url = f"https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live"
    response = requests.get(url, timeout=10)
    return response.json()
