"""Module to build image from template"""

from datetime import datetime, timedelta
from PIL import Image, ImageOps, ImageFont, ImageDraw, ImageColor


def generate_image(
    username: str,
    colour: str,
    timestamp: datetime,
    avatar: Image.Image,
    meme: Image.Image,
) -> Image.Image:
    """Builds image response"""

    avatar_size = (50, 50)
    template_offset = (405, 684)  # Top left corner of the template box
    thumbnail_spacing_buffer = (20, 20)
    username_offset = concat_tuples(
        template_offset, (avatar_size[0] + 35, thumbnail_spacing_buffer[1])
    )

    avatar = avatar.resize(avatar_size)
    scaled_size = (avatar.size[0] * 3, avatar.size[1] * 3)
    mask = Image.new("L", scaled_size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + scaled_size, fill=255)
    mask = mask.resize(avatar.size, resample=Image.Resampling.LANCZOS)
    avatar.putalpha(mask)

    thumbnail = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
    thumbnail.putalpha(mask)
    template = Image.open("./resources/images/template.png")

    template.paste(
        thumbnail, concat_tuples(template_offset, thumbnail_spacing_buffer), thumbnail
    )
    username_font = ImageFont.truetype("./resources/fonts/whitney-medium.ttf", 16)
    username_text = username[:20] + (username[20:] and "...")

    ImageDraw.Draw(template).text(
        xy=username_offset,
        text=username_text,
        fill=ImageColor.getcolor(f"{colour}", "RGB"),
        font=username_font,
    )

    ImageDraw.Draw(template).text(
        xy=concat_tuples(
            username_offset,
            (int(username_font.getlength(username_text)), 0),
            username_font.getmetrics(),
        ),
        text=format_time(timestamp),
        fill=ImageColor.getcolor("#AAAAAA", "RGB"),
        font=ImageFont.truetype("./resources/fonts/whitney-medium.ttf", 12),
    )
    template.paste(
        ImageOps.cover(meme, (275, 275)), concat_tuples(username_offset, (0, 25))
    )
    return template


def concat_tuples(*args: tuple[int, int]) -> tuple[int, int]:
    """Adds all values from N tuples to a single tuple"""
    return tuple[int, int](map(sum, zip(*args)))


def format_time(timestamp: datetime) -> str:
    """Helper function to pretty print timestamp"""
    time = timestamp.strftime("%H:%M")
    if timestamp.date() == datetime.today().date():
        return f"Today at {time}"
    if timestamp.date() == datetime.today().date() - timedelta(-1):
        return f"Yesterday at {time}"
    return timestamp.strftime(f"%d/%m/%Y, {time}")
