import os
import discord
import alerts

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")


class Bot(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")

        ch = None

        if CHANNEL_ID:
            ch = self.get_channel(int(CHANNEL_ID))
            print(f"Channel: {ch}")

            if ch:
                await ch.send("✅ DingerHQ bot is online!")

        print("Starting HR watcher...")
        await alerts.watch_home_runs(self, ch)


intents = discord.Intents.default()

client = Bot(intents=intents)

client.run(TOKEN)