from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO


def create_home_run_graphic(
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
    width = 1200
    height = 675

    image = Image.new("RGB", (width, height), (20, 20, 25))
    draw = ImageDraw.Draw(image)

    try:
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 58)
        font = ImageFont.truetype("DejaVuSans.ttf", 34)
    except:
        title_font = ImageFont.load_default()
        font = ImageFont.load_default()

    draw.text((40, 30), "🚀 HOME RUN", fill="white", font=title_font)

    # Download player headshot
    try:
        url = f"https://img.mlbstatic.com/mlb-photos/image/upload/w_213,q_auto:best/v1/people/{player_id}/headshot/67/current"

        response = requests.get(url, timeout=10)

        headshot = Image.open(BytesIO(response.content)).convert("RGB")
        headshot = headshot.resize((170, 170))

        image.paste(headshot, (980, 35))
    except:
        pass

    stats = [
        ("Player", player),
        ("Team", team),
        ("Distance", f"{distance} ft"),
        ("Exit Velocity", f"{exit_velocity} MPH"),
        ("Launch Angle", f"{launch_angle}°"),
        ("Inning", f"{half} {inning}"),
        ("Score", f"{away_score} - {home_score}")
    ]

    y = 150

    for label, value in stats:
        draw.text((60, y), label, fill="white", font=font)
        draw.text((320, y), str(value), fill=(255, 80, 80), font=font)
        y += 60

    filename = "home_run.png"
    image.save(filename)

    return filename