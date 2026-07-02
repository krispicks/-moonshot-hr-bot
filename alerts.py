import asyncio
import asyncio
import mlb
import embeds
import cache
async def watch_home_runs(bot, channel):
    print("Watching for home runs...")

    while True:
    try:
        game_ids = mlb.get_today_game_ids()

        for game_pk in game_ids:
            feed = mlb.get_game_feed(game_pk)
            print(f"Checking game {game_pk}")

    except Exception as e:
        print(f"Error: {e}")

    await asyncio.sleep(15)