from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

WIDTH = 1200
HEIGHT = 675


def _font(size, bold=False):
    try:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
        return ImageFont.truetype(name, size)
    except:
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

    return Image.new("RGB", (WIDTH, HEIGHT), (12,12,18))

def create_home_run_graphic():

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

    draw.text((25, 15), "DingerHQ LIVE", fill="white", font=title)
    draw.text((960, 28), "Powered by DingerHQ", fill="white", font=normal)

    image.save("preview.png")

    return "preview.png"