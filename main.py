from PIL import Image, ImageOps, ImageFont, ImageDraw, ImageColor

# Discord background is 3, 3, 4
# Use this green idk 0a 7c 2a
rawBackground = Image.open("./resources/images/background.png")
background = rawBackground.resize((420, 330))
template = Image.open("./resources/images/reposter.png")
avatar = Image.open("./resources/images/avatar.png")
meme = Image.open("./resources/images/meme2.jpg")
avatar = avatar.resize((50, 50))
scaled_size = (avatar.size[0] * 3, avatar.size[1] * 3)
mask = Image.new('L', scaled_size, 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0) + scaled_size, fill=255)
mask = mask.resize(avatar.size, resample= Image.Resampling.LANCZOS)
avatar.putalpha(mask)

thumbnail = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
thumbnail.putalpha(mask)

background.paste(thumbnail, (15, 15), thumbnail)

draw = ImageDraw.Draw(background)

username = "Bernie Madoff"
username_font = ImageFont.truetype("./resources/fonts/whitney-medium.ttf", 16)
username_color = ImageColor.getcolor("#ffffff", "RGB")

timestamp = "Today at 22:04"
timestamp_font = ImageFont.truetype("./resources/fonts/whitney-medium.ttf", 12)
timestamp_colour = ImageColor.getcolor("#AAAAAA", "RGB")

username_coords = (thumbnail.size[0] + 30, 15)
draw.text(username_coords, username, username_color, font=username_font)
print(username_font.getlength(username))
draw.text((username_coords[0] + username_font.getlength(username) + 10, username_coords[1] + 4), timestamp, timestamp_colour, font=timestamp_font)
background.paste(ImageOps.cover(meme, (275,275)), (80, 40))

template.paste(background, (400, template.size[1]-background.size[1]))
template.save("test.png")
