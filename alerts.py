import asyncio
import requests
import embeds
import cache

async def watch_home_runs(bot, channel):
    print("Watching for home runs...")

    while True:
        try:
            print("Checking MLB API...")
            # We'll add the live HR detection logic next.
        except Exception as e:
            print(e)

        await asyncio.sleep(15)
