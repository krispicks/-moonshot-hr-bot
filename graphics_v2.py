from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import requests
from io import BytesIO

WIDTH = 1200
HEIGHT = 675


def _font(size, bold=False):
    try:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
        return ImageFont.truetype(name, size)
    except Exception:
        return ImageFont.load_default()


def _stadium_background():
    stadium_dir = "assets/stadiums"

    if os.path.isdir(stadium_dir):
        files = [
            f for f in os.listdir(stadium_dir)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]

        if files:
            path = os.path.join(stadium_dir, files[0])

            bg = Image.open(path).convert("RGB")
            bg = bg.resize((WIDTH, HEIGHT))
            bg = bg.filter(ImageFilter.GaussianBlur(5))

            return bg

    return Image.new("RGB", (WIDTH, HEIGHT), (12, 12, 18))


def _headshot(player_id):
    url = (
        f"https://img.mlbstatic.com/mlb-photos/image/upload/"
        f"w_600,q_auto:best/v1/people/{player_id}/headshot/67/current"
    )

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()

        img = Image.open(BytesIO(r.content)).convert("RGBA")
        return img.resize((420, 420))

    except Exception:
        return None


def create_home_run_graphic(player_id=None):

    image = _stadium_background()

    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 145))
    image = Image.alpha_composite(
        image.convert("RGBA"),
        overlay
    ).convert("RGB")

    draw = ImageDraw.Draw(image)

    # ===========================
    # HEADER
    # ===========================

    draw.rectangle((0, 0, WIDTH, 80), fill=(15, 15, 18))

    # ===========================
    # PLAYER PANEL
    # ===========================

    draw.rectangle((0, 80, 420, 585), fill=(18, 18, 22))

    # ===========================
    # INFO PANEL
    # ===========================

    draw.rectangle((420, 80, WIDTH, 585), fill=(20, 20, 25))

    # ===========================
    # STAT BAR
    # ===========================

    draw.rectangle((0, 585, WIDTH, 625), fill=(28, 28, 35))

    # ===========================
    # SCOREBOARD
    # ===========================

    draw.rectangle((0, 625, WIDTH, HEIGHT), fill=(15, 15, 18))

    title = _font(56, True)
    normal = _font(26)
    home_run_font = _font(130, True)

    draw.text((25, 15), "DingerHQ LIVE", fill="white", font=title)

    draw.text(
        (610, 135),
        "HOME\nRUN",
        fill=(245, 245, 245),
        font=home_run_font,
    )

    draw.text(
        (900, 28),
        "Powered by DingerHQ",
        fill="white",
        font=normal,
    )

    # ===========================
    # PLAYER HEADSHOT
    # ===========================

    if player_id:
        headshot = _headshot(player_id)

        if headshot:
            image.paste(headshot, (20, 120), headshot)

    image.save("preview.png")

    return "preview.png"