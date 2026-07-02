import os
import discord
import mlb

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")


class Bot(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")

        if CHANNEL_ID:
            ch = self.get_channel(int(CHANNEL_ID))
            if ch:
                await ch.send("✅ DingerHQ bot is online!")

        await mlb.start(self)


intents = discord.Intents.default()
client = Bot(intents=intents)

client.run(TOKEN)
