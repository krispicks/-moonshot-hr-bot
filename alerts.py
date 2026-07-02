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

            for game_pk in game_ids:
                home_runs = mlb.get_home_run_events(game_pk)

                print(f"Game {game_pk}: {len(home_runs)} home runs found", flush=True)

                for hr in home_runs:

                    # Use MLB play_id if available, otherwise fall back
                    play_id = str(
                        hr.get(
                            "play_id",
                            f"{hr['batter']}-{hr['inning']}-{hr['half']}"
                        )
                    )

                    # Skip if already posted
                    if cache.already_posted(game_pk, play_id):
                        continue

                    embed = embeds.home_run_embed(
                        player=hr.get("batter", "Unknown"),
                        team=hr.get("team", "Unknown"),
                        distance=hr.get("distance", "N/A"),
                        exit_velocity=hr.get("exit_velocity", "N/A"),
                    )

                    await channel.send(embed=embed)

                    # Mark as posted so it isn't sent again
                    cache.mark_posted(game_pk, play_id)

        except Exception as e:
            print(f"Error: {e}", flush=True)

        await asyncio.sleep(15)