import os
import discord
import alerts
import graphics

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")


class Bot(discord.Client):
    watch_started = False

    async def on_ready(self):
        print(f"Logged in as {self.user}", flush=True)

        ch = None

        if CHANNEL_ID:
            try:
                ch = await self.fetch_channel(int(CHANNEL_ID))
                print(f"Channel: {ch}", flush=True)

            except Exception as e:
                print(f"Failed to fetch channel: {e}", flush=True)

        if ch and not self.watch_started:
            self.watch_started = True
            self.loop.create_task(alerts.watch_home_runs(self, ch))
        else:
            print("No valid channel found.", flush=True)

    async def on_message(self, message):
        # Ignore messages from the bot itself
        if message.author == self.user:
            return

        print(f"Received message: {message.content}", flush=True)

        # Test command
       if message.content.lower() == "!testhr":
           print("TESTHR COMMAND RAN", flush=True)

            filename = graphics.create_home_run_graphic(
                player="Aaron Judge",
                player_id=592450,
                team="New York Yankees",
                distance=437,
                exit_velocity=112.3,
                launch_angle=28,
                inning=4,
                half="Top",
                away_score=5,
                home_score=2,
            )

            await message.channel.send(file=discord.File(filename))


intents = discord.Intents.default()
intents.message_content = True

client = Bot(intents=intents)

client.run(TOKEN)