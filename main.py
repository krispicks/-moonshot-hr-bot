import os
import asyncio
import discord

TOKEN=os.getenv('DISCORD_TOKEN')
CHANNEL_ID=os.getenv('CHANNEL_ID')

class Bot(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
        if CHANNEL_ID:
            ch=self.get_channel(int(CHANNEL_ID))
            if ch:
                await ch.send('✅ DingerHQ bot is online.')
        while True:
            # TODO: Poll MLB StatsAPI and post new home runs.
            await asyncio.sleep(15)

client=Bot(intents=discord.Intents.default())
client.run(TOKEN)
