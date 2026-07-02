import asyncio
import requests
import os

CHANNEL_ID = os.getenv("CHANNEL_ID")

seen = set()

async def start(client):
    while True:
        try:
            url = "https://statsapi.mlb.com/api/v1.1/game/changes?updatedSince=60"
            games = requests.get(url, timeout=10).json()

            channel = client.get_channel(int(CHANNEL_ID))

            if channel:
                await channel.send("⚾ MLB API connected successfully!")

            await asyncio.sleep(3600)

        except Exception as e:
            print(e)
            await asyncio.sleep(30)
