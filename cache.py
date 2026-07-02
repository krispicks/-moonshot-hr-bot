posted_home_runs = set()

def already_posted(game_pk, play_id):
    key = f"{game_pk}-{play_id}"

    if key in posted_home_runs:
        return True

    posted_home_runs.add(key)
    return False
