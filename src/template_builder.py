from datetime import datetime, timedelta
from PIL import Image, ImageOps, ImageFont, ImageDraw, ImageColor

def build_template(username: str, colour: str, timestamp: datetime, avatar: Image, meme: Image) -> Image:
    # Sizes
    avatar_size = (50, 50)
    meme_size = (275, 275)
    template_offset = (405, 684) # Top left corner of the template box
    thumbnail_spacing_buffer = (20, 20)
    username_offset = concat_tuples(template_offset, (avatar_size[0] + 35, thumbnail_spacing_buffer[1]))

    avatar = avatar.resize(avatar_size)
    scaled_size = (avatar.size[0] * 3, avatar.size[1] * 3)
    mask = Image.new('L', scaled_size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + scaled_size, fill=255)
    mask = mask.resize(avatar.size, resample=Image.Resampling.LANCZOS)
    avatar.putalpha(mask)

    thumbnail = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
    thumbnail.putalpha(mask)
    template = Image.open("../resources/images/template.png")

    template.paste(thumbnail, concat_tuples(template_offset, thumbnail_spacing_buffer), thumbnail)

    draw = ImageDraw.Draw(template)

    username_font = ImageFont.truetype("../resources/fonts/whitney-medium.ttf", 16)
    username_color = ImageColor.getcolor("#{}".format(colour), "RGB")

    timestamp_font = ImageFont.truetype("../resources/fonts/whitney-medium.ttf", 12)
    timestamp_colour = ImageColor.getcolor("#AAAAAA", "RGB")

    time = timestamp.strftime("%H:%M")
    if timestamp.date() == datetime.today().date():
        date = "Today at "
    elif timestamp.date()  == datetime.today().date() - timedelta(-1):
        date = "Yesterday at "
    else:
        date = timestamp.strftime("%d/%m/%Y, ")

    username_text = username[:20] + (username[20:] and '...')

    draw.text(
        username_offset,
        username_text,
        username_color,
        font=username_font)

    draw.text(
        concat_tuples(username_offset, (username_font.getlength(username_text), 0), username_font.getmetrics()),
              date + time,
              timestamp_colour,
              font=timestamp_font)
    template.paste(ImageOps.cover(meme, meme_size), concat_tuples(username_offset, (0, 25)))
    return template

def concat_tuples(*args: ()) -> ():
    return tuple(map(sum, zip(*args)))