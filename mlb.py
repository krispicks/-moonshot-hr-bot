def get_home_run_events(game_pk):
    feed = get_game_feed(game_pk)

    events = []

    all_plays = feed.get("liveData", {}).get("plays", {}).get("allPlays", [])

    for play in all_plays:
        result = play.get("result", {})

        if result.get("event") == "Home Run":

            # TEMP: Print the full home run data to Render logs
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
