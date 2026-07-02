import asyncio
import mlb
import embeds
import cache


async def watch_home_runs(bot, channel):
    print("watch_home_runs() started", flush=True)

    while True:
        try:
            print("Getting today's games...", flush=True)

            game_ids = mlb.get_today_game_ids()

            print(f"Found {len(game_ids)} games", flush=True)

            for game_pk in game_ids:

                home_runs = mlb.get_home_run_events(game_pk)

                print(f"Game {game_pk}: {len(home_runs)} home runs found", flush=True)

                for hr in home_runs:

                    play_id = hr["play_id"]

                    if cache.already_posted(game_pk, play_id):
                       