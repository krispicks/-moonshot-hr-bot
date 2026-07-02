import asyncio
import mlb
import cache
import discord
import graphics


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

                    print(f"DEBUG play_id={play_id}, player={hr['batter']}", flush=True)
                    print(f"Checking game={game_pk}, play_id={play_id}", flush=True)

                    if cache.already_posted(game_pk, play_id):
                        print("Already posted. Skipping.", flush=True)
                        continue

                    # Mark immediately to stop duplicate posts
                    cache.mark_posted(game_pk, play_id)

                    print("New home run. Waiting for Statcast...", flush=True)

                    await asyncio.sleep(8)

                    updated_home_runs = mlb.get_home_run_events(game_pk)

                    updated_hr = next(
                        (x for x in updated_home_runs if x["play_id"] == play_id),
                        hr
                    )

                    filename = graphics.create_home_run_graphic(
                        player=updated_hr["batter"],
                        player_id=updated_hr["player_id"],
                        team=updated_hr["team"],
                        distance=updated_hr["distance"],
                        exit_velocity=updated_hr["exit_velocity"],
                        launch_angle=updated_hr["launch_angle"],
                        inning=updated_hr["inning"],
                        half=updated_hr["half"],
                        away_score=updated_hr["away_score"],
                        home_score=updated_hr["home_score"],
                    )

                    await channel.send(file=discord.File(filename))

                    print(f"Posted: {game_pk}-{play_id}", flush=True)

        except Exception as e:
            print(f"Error in watch_home_runs(): {e}", flush=True)

        await asyncio.sleep(15)