from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

try:
    from theme import TEAM_THEMES
except Exception:
    TEAM_THEMES = {}

WIDTH = 1200
HEIGHT = 675

def _font(size, bold=False):
    try:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
        return ImageFont.truetype(name, size)
    except Exception:
        return ImageFont.load_default()

def _headshot(player_id):
    url = (
        f"https://img.mlbstatic.com/mlb-photos/image/upload/"
        f"w_300,q_auto:best/v1/people/{player_id}/headshot/67/current"
    )
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        img = Image.open(BytesIO(r.content)).convert("RGBA")
        return img.resize((320,320))
    except Exception:
        return None

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
    theme = TEAM_THEMES.get(team, TEAM_THEMES.get("default", {
        "primary": (200,30,30),
        "secondary": (255,255,255),
        "text": (255,255,255),
    }))

    image = Image.new("RGB", (WIDTH, HEIGHT), (18,18,22))
    draw = ImageDraw.Draw(image)

    # header
    draw.rectangle((0,0,WIDTH,95), fill=(15,15,15))
    draw.line((0,95,WIDTH,95), fill=(255,215,0), width=4)

    title = _font(54, True)
    big = _font(62, True)
    normal = _font(34)
    small = _font(28)

    draw.text((40,18), "HOME RUN", fill="white", font=title)
    draw.text((40,72), "DingerHQ LIVE", fill=(220,220,220), font=small)

    # headshot
    hs = _headshot(player_id)
    if hs:
        image.paste(hs, (820,160), hs)

    draw.text((50,120), player.upper(), fill=theme["secondary"], font=big)
    draw.text((50,180), team, fill="white", font=normal)

    stats = [
    ("DISTANCE", f"{distance} ft"),
    ("EXIT VELOCITY", f"{exit_velocity} MPH"),
    ("LAUNCH ANGLE", f"{launch_angle}°"),
    ("INNING", f"{half.title()} {inning}"),
    ("SCORE", f"{away_score} - {home_score}"),
]

y = 270

for label, value in stats:
    draw.rounded_rectangle(
        (35, y - 10, 780, y + 52),
        radius=18,
        fill=(32, 32, 38),
        outline=theme["secondary"],
        width=2,
    )

    draw.text((60, y), label, fill="white", font=small)
    draw.text((390, y), str(value), fill=theme["secondary"], font=small)

    y += 70

    draw.text((40,620), "Powered by DingerHQ", fill=(180,180,180), font=small)

    out = "home_run.png"
    image.save(out)
    return out
