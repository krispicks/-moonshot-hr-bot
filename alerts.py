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

            print(f"Found {len(game_ids)} games")

            for game_pk in game_ids:

                home_runs = mlb.get_home_run_events(game_pk)

                print(f"Game {game_pk}: {len(home_runs)} home runs found")

                for hr in home_runs:

                    play_id = hr["play_id"]

                    # Skip if we've already posted this HR
                    if cache.already_posted(game_pk, play_id):
                        continue

                    embed = embeds.home_run_embed(
                        player=hr["batter"],
                        team=hr["team"],
                        distance=hr["distance"],
                        exit_velocity=hr["exit_velocity"],
                        launch_angle=hr["launch_angle"],
                        inning=hr["inning"],
                        half=hr["half"],
                        away_score=hr["away_score"],
                        home_score=hr["home_score"],
                    )

                    await channel.send(embed=embed)

                    # Remember we've posted it
                    cache.mark_posted(game_pk, play_id)

        except Exception as e:
            print(f"Error in watch_home_runs(): {e}", flush=True)

        await asyncio.sleep(15)