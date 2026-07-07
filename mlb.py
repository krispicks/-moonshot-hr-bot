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

    all_plays = (
        feed.get("liveData", {})
        .get("plays", {})
        .get("allPlays", [])
    )

    for play in all_plays:

        result = play.get("result", {})

        if result.get("event") != "Home Run":
            continue

        hit = play.get("hitData", {})

        print("HIT DATA:", hit, flush=True)

        # Batting team
        if play["about"]["halfInning"].lower() == "top":
            team = (
                feed.get("gameData", {})
                .get("teams", {})
                .get("away", {})
                .get("name", "Unknown")
            )
        else:
            team = (
                feed.get("gameData", {})
                .get("teams", {})
                .get("home", {})
                .get("name", "Unknown")
            )

        away_score = result.get("awayScore", 0)
        home_score = result.get("homeScore", 0)

        # Stadium
        stadium = (
            feed.get("gameData", {})
            .get("venue", {})
            .get("name", "Unknown Stadium")
        )

        # Pitcher
        pitcher = (
            play.get("matchup", {})
            .get("pitcher", {})
            .get("fullName", "Unknown")
        )

        # Pitch Data
        pitch_data = play.get("pitchData", {})

        pitch_type = pitch_data.get(
            "typeDescription",
            "Unknown"
        )

        pitch_speed = pitch_data.get(
            "startSpeed",
            "N/A"
        )

        events.append({

            "play_id": (
                f"{play['matchup']['batter']['id']}_"
                f"{play['about']['inning']}_"
                f"{play['about']['halfInning']}_"
                f"{away_score}_"
                f"{home_score}"
            ),

            # Player
            "player_id": play["matchup"]["batter"]["id"],
            "batter": play["matchup"]["batter"]["fullName"],
            "team": team,

            # Game
            "inning": play["about"]["inning"],
            "half": play["about"]["halfInning"],
            "away_score": away_score,
            "home_score": home_score,

            # Stadium
            "stadium": stadium,

            # Pitcher
            "pitcher": pitcher,

            # Pitch Data
            "pitch_type": pitch_type,
            "pitch_speed": pitch_speed,

            # Statcast
            "distance": hit.get("totalDistance", "N/A"),
            "exit_velocity": hit.get("launchSpeed", "N/A"),
            "launch_angle": hit.get("launchAngle", "N/A"),
        })

    return events