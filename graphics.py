from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests
from io import BytesIO
import os
try:
    from theme import TEAM_THEMES
except Exception:
    TEAM_THEMES = {}

WIDTH = 1200
HEIGHT = 675

def _stadium_background():
    stadium_dir = "assets/stadiums"

    if os.path.isdir(stadium_dir):
        for filename in os.listdir(stadium_dir):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                path = os.path.join(stadium_dir, filename)

                bg = Image.open(path).convert("RGB")
                bg = bg.resize((WIDTH, HEIGHT))
                bg = bg.filter(ImageFilter.GaussianBlur(8))
                return bg

    return Image.new("RGB", (WIDTH, HEIGHT), (18, 18, 22))

def _font(size, bold=False):
    try:
        if bold:
            return ImageFont.truetype(
                "assets/assets/fonts/BebasNeue-Regular.ttf",
                size
            )
        else:
            return ImageFont.truetype(
                "assets/assets/fonts/BebasNeue-Regular.ttf",
                size
            )
    except Exception:
        try:
            name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
            return ImageFont.truetype(name, size)
        except Exception:
            return ImageFont.load_default()

TEAM_LOGOS = {
    "Arizona Diamondbacks": "IMG_5991",
    "Atlanta Braves": "IMG_5998",
    "Athletics": "IMG_6018",
    "Baltimore Orioles": "IMG_6001",
    "Boston Red Sox": "IMG_5999",
    "Chicago Cubs": "IMG_6002",
    "Chicago White Sox": "IMG_6003",
    "Cincinnati Reds": "IMG_6004",
    "Cleveland Guardians": "IMG_6005",
    "Colorado Rockies": "IMG_6006",
    "Detroit Tigers": "IMG_6007",
    "Houston Astros": "IMG_6008",
    "Kansas City Royals": "IMG_6009",
    "Los Angeles Angels": "IMG_6010",
    "Los Angeles Dodgers": "IMG_6011",
    "Miami Marlins": "IMG_6012",
    "Milwaukee Brewers": "IMG_6013",
    "Minnesota Twins": "IMG_6015",
    "New York Mets": "IMG_6016",
    "New York Yankees": "IMG_6017",
    "Philadelphia Phillies": "IMG_6020",
    "Pittsburgh Pirates": "IMG_6021",
    "San Diego Padres": "IMG_6022",
    "San Francisco Giants": "IMG_6023",
    "Seattle Mariners": "IMG_6024",
    "St. Louis Cardinals": "IMG_6025",
    "Tampa Bay Rays": "IMG_6026",
    "Texas Rangers": "IMG_6027",
    "Toronto Blue Jays": "IMG_6028",
    "Washington Nationals": "IMG_6029",
}

def _team_logo(team):
    abbr = TEAM_LOGOS.get(team)

    if not abbr:
        return None

    path = os.path.join("assets", "logos", f"{abbr}.png")

    try:
        logo = Image.open(path).convert("RGBA")
        return logo.resize((110, 110))
    except Exception:
        return None
        

def _headshot(player_id):
    url = (
        f"https://img.mlbstatic.com/mlb-photos/image/upload/"
        f"w_300,q_auto:best/v1/people/{player_id}/headshot/67/current"
    )

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()

        img = Image.open(BytesIO(r.content)).convert("RGBA")
        return img.resize((420, 420))

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

    theme = TEAM_THEMES.get(
        team,
        {
            "primary": (200, 30, 30),
            "secondary": (255, 215, 0),
            "text": (255, 255, 255),
        },
    )

    image = _stadium_background()

    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 140))
    image = Image.alpha_composite(
        image.convert("RGBA"),
        overlay
    ).convert("RGB")

    draw = ImageDraw.Draw(image)

    # Header
    draw.rectangle((0, 0, WIDTH, 110), fill=(12, 12, 12))
    draw.line((0, 110, WIDTH, 110), fill=theme["primary"], width=5)

    title = _font(68, True)
    big = _font(62, True)
    normal = _font(34)
    small = _font(28)

    draw.text((35, 8), "🚀 HOME RUN ALERT", fill=theme["secondary"], font=title)
    draw.text((40, 76), "POWERED BY DINGERHQ", fill=(185,185,185), font=small)
    # Player headshot
    hs = _headshot(player_id)

    if hs:
        hs = hs.resize((350, 350))
        image.paste(hs, (40, 120), hs)

    # Team logo
    logo = _team_logo(team)

    if logo:
        logo = logo.resize((180,180))
        logo.putalpha(55)
        image.paste(logo, (960, 20), logo)

    # Player info
    name_font = _font(72, True)
    team_font = _font(34)

    draw.text(
         (620, 145),   # moved right
         player.upper(),
         fill=theme["secondary"],
         font=name_font,
         anchor="mm",
    )

    draw.text(
        (620, 205),   # moved right
        team,
        fill="white",
        font=team_font,
        anchor="mm",
    )

    cards = [
        ("DISTANCE", f"{distance} FT", 420, 290),
        ("EXIT VELO", f"{exit_velocity} MPH", 700, 290),
        ("LAUNCH", f"{launch_angle}°", 420, 430),
        ("INNING", f"{half.upper()} {inning}", 700, 430),
    ]

    for title, value, x, y in cards:

        draw.rounded_rectangle(
            (x, y, x + 250, y + 110),
            radius=22,
            fill=(22, 22, 28),
            outline=theme["primary"],
            width=3,
        )

        draw.text(
            (x + 20, y + 18),
            title,
            fill=(160, 160, 160),
            font=_font(22, True),
        )

        draw.text(
            (x + 20, y + 56),
            value,
            fill="white",
            font=_font(36, True),
        )

    draw.rounded_rectangle(
        (420, 565, 1110, 635),
        radius=18,
        fill=(20, 20, 25),
        outline=theme["primary"],
        width=3,
    )

    draw.text(
        (450, 582),
        f"{away_score}   •   {half.upper()} {inning}   •   {home_score}",
        fill="white",
        font=_font(32, True),
    )

    draw.text(
        (40, 630),
        "⚾ Powered by DingerHQ",
        fill=(170, 170, 170),
        font=small,
    )

    filename = "home_run.png"
    image.save(filename)

    return filename
