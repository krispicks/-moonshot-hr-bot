import os
import asyncio
import discord
import mlb
import alerts
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

posted_home_runs = set()


class Bot(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")

        if CHANNEL_ID:
            ch = self.get_channel(int(CHANNEL_ID))
            if ch:
                await ch.send("✅ DingerHQ bot is online!")

        while True:
            try:
                games = mlb.get_live_games()
                print(games)
            except Exception as e:
                print(e)

            await asyncio.sleep(15)


intents = discord.Intents.default()

client = Bot(intents=intents)

client.run(TOKEN)
