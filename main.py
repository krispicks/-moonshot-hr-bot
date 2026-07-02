import os
import discord
import mlb

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")


class Bot(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")

        games = mlb.get_todays_games()
        print("Connected to MLB API!")

        dates = games.get("dates", [])

        if dates:
            print(f"Today's games: {len(dates[0]['games'])}")
        else:
            print("No games today.")

        if CHANNEL_ID:
            ch = self.get_channel(int(CHANNEL_ID))
            if ch:
                await ch.send("✅ DingerHQ bot is online.")


intents = discord.Intents.default()

client = Bot(intents=intents)

client.run(TOKEN)
