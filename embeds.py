import discord


def home_run_embed(
    player,
    player_id,
    team,
    distance,
    exit_velocity,
    launch_angle,
    inning,
    half,
    away_score,
    home_score,
):
    embed = discord.Embed(
        title="🚀 HOME RUN",
        color=discord.Color.red()
    )

    # Official MLB player headshot
    headshot = (
        f"https://img.mlbstatic.com/mlb-photos/image/upload/"
        f"w_213,q_auto:best/v1/people/{player_id}/headshot/67/current"
    )

    embed.set_thumbnail(url=headshot)

    embed.add_field(
        name="👤 Player",
        value=player,
        inline=False
    )

    embed.add_field(
        name="🏟️ Team",
        value=team,
        inline=False
    )

    embed.add_field(
        name="📏 Distance",
        value=f"{distance} ft",
        inline=True
    )

    embed.add_field(
        name="🚀 Exit Velocity",
        value=f"{exit_velocity} MPH",
        inline=True
    )

    embed.add_field(
        name="📈 Launch Angle",
        value=f"{launch_angle}°",
        inline=True
    )

    embed.add_field(
        name="🕒 Inning",
        value=f"{half.title()} {inning}",
        inline=True
    )

    embed.add_field(
        name="⚾ Score",
        value=f"{away_score} - {home_score}",
        inline=False
    )

    embed.set_footer(text="DingerHQ • Live MLB Home Run Alerts")

    return embed