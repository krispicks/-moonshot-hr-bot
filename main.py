import os
import discord
import alerts

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")


class Bot(discord.Client):

    async def on_ready(self):
        print(f"Logged in as {self.user}", flush=True)

        ch = None

        if CHANNEL_ID:
            try:
                ch = await self.fetch_channel(int(CHANNEL_ID))
                print(f"Channel: {ch}", flush=True)



            except Exception as e:
                print(f"Failed to fetch channel: {e}", flush=True)

        

        if ch:
            await alerts.watch_home_runs(self, ch)
        else:
            print("No valid channel found.", flush=True)


intents = discord.Intents.default()

client = Bot(intents=intents)

client.run(TOKEN)