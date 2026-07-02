import discord

def home_run_embed(player, team, distance, exit_velocity):
    embed = discord.Embed(
        title="💣 HOME RUN!",
        description=f"**{player}** just went yard!",
        color=0xff2d55,
    )

    embed.add_field(name="👤 Player", value=player, inline=True)
    embed.add_field(name="🧢 Team", value=team, inline=True)
    embed.add_field(name="📏 Distance", value=f"{distance} ft", inline=True)
    embed.add_field(name="🔥 Exit Velocity", value=f"{exit_velocity} mph", inline=True)

    embed.set_footer(text="🚀 Moonshot HR Bot")

    return embed