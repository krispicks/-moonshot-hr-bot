import requests

def get_todays_games():
    url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1"
    response = requests.get(url, timeout=10)
    return response.json()
