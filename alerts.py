import asyncio
import mlb
import cache
import discord
import graphics

startup_complete = False


async def watch_home_runs(bot, channel):
    global startup_complete

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

                    # Skip anything we've already seen
                    if cache.already_posted(game_pk, play_id):
                        continue

                    # Startup Sync
                    if not startup_complete:
                        cache.mark_posted(game_pk, play_id)
                        print(
                            f"Startup sync: ignoring old HR {game_pk}-{play_id}",
                            flush=True,
                        )
                        continue

                    cache.mark_posted(game_pk, play_id)

                    print("New home run. Waiting for Statcast...", flush=True)

                    updated_hr = hr

                    # Wait up to 30 seconds for Statcast data
                    for _ in range(6):
                        await asyncio.sleep(5)

                        updated_home_runs = mlb.get_home_run_events(game_pk)

                        found = next(
                            (
                                x
                                for x in updated_home_runs
                                if x["play_id"] == play_id
                            ),
                            None,
                        )

                        if found:
                            updated_hr = found

                            if (
                                updated_hr["distance"] != "N/A"
                                and updated_hr["exit_velocity"] != "N/A"
                                and updated_hr["launch_angle"] != "N/A"
                            ):
                                print("Statcast data found!", flush=True)
                                break

                    filename = graphics.create_home_run_graphic(
                        player=updated_hr["batter"],
                        player_id=updated_hr["player_id"],
                        team=updated_hr["team"],

                        stadium=updated_hr["stadium"],
                        pitcher=updated_hr["pitcher"],
                        pitch_type=updated_hr["pitch_type"],
                        pitch_speed=updated_hr["pitch_speed"],

                        distance=updated_hr["distance"],
                        exit_velocity=updated_hr["exit_velocity"],
                        launch_angle=updated_hr["launch_angle"],

                        inning=updated_hr["inning"],
                        half=updated_hr["half"],

                        away_score=updated_hr["away_score"],
                        home_score=updated_hr["home_score"],
                    )

                    await channel.send(
                        file=discord.File(filename)
                    )

                    print(f"Posted: {game_pk}-{play_id}", flush=True)

            if not startup_complete and game_ids:
                startup_complete = True
                print(
                    "✅ Startup sync complete. Watching for NEW home runs only.",
                    flush=True,
                )

        except Exception as e:
            print(f"Error in watch_home_runs(): {e}", flush=True)

        await asyncio.sleep(15)