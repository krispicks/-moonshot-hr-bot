import asyncio
import mlb
import embeds
import cache

async def watch_home_runs(bot, channel):
    print("watch_home_runs() started")

    while True:
        print("Loop running")

        try:
            print("Getting today's games...")
            game_ids = mlb.get_today_game_ids()
            print(f"Found {len(game_ids)} games: {game_ids}")

            for game_pk in game_ids:
                home_runs = mlb.get_home_run_events(game_pk)

                for hr in home_runs:
                    play_id = f"{hr['batter']}-{hr['inning']}-{hr['half']}"

                    if cache.already_posted(game_pk, play_id):
                        continue

                    embed = embeds.home_run_embed(
                        player=hr["batter"],
                        team="Unknown",
                        distance="N/A",
                        exit_velocity="N/A",
                    )

                    await channel.send(embed=embed)

        except Exception as e:
            print(f"Error: {e}")

        await asyncio.sleep(15)