posted_home_runs = set()


def already_posted(game_pk, play_id):
    key = f"{game_pk}-{play_id}"
    return key in posted_home_runs


def mark_posted(game_pk, play_id):
    key = f"{game_pk}-{play_id}"
    posted_home_runs.add(key)