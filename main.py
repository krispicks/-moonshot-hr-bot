import os
import asyncio
import discord

import mlb
from embeds import home_run_embed

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

posted_home_runs = set()


async def watch_games():
    await client.wait_until_ready()

    channel = client.get_channel(CHANNEL_ID)

    while not client.is_closed():
        try:
            game_ids = mlb.get_today_game_ids()

            for game_pk in game_ids:
                home_runs = mlb.get_home_run_events(game_pk)

                for hr in home_runs:
                    key = (
                        hr["batter"],
                        hr["inning"],
                        hr["half"],
                    )

                    if key in posted_home_runs:
                        continue

                    posted_home_runs.add(key)

                    embed = home_run_embed(
                        player=hr["batter"],
                        team="Unknown",
                        distance="N/A",
                        exit_velocity="N/A",
                    )

                    await channel.send(embed=embed)

        except Exception as e:
            print(e)

        await asyncio.sleep(15)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    print("🚀 Moonshot HR Bot is online!")

    client.loop.create_task(watch_games())


client.run(TOKEN)