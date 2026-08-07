"""Add editable appVersion callout to the CXO architecture diagram."""

from PIL import Image, ImageDraw, ImageFont

IMAGE_PATH = "docs/architecture/SA_Guild_Architecture_Diagram.png"

im = Image.open(IMAGE_PATH).convert("RGBA")
overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# Badge placement — Config Delivery column, below GitLab step
x, y, w, h = 885, 395, 310, 52
radius = 10
fill = (245, 243, 255, 245)
stroke = (124, 58, 237, 255)

draw.rounded_rectangle((x, y, x + w, y + h), radius=radius, fill=fill, outline=stroke, width=2)

try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
except OSError:
    font = ImageFont.load_default()
    font_small = font

draw.text((x + 14, y + 6), "Chart.yaml · appVersion editable", fill=(76, 29, 149, 255), font=font)
draw.text((x + 14, y + 28), "Dev/QA raw chart — in-place version edits", fill=(107, 70, 193, 255), font=font_small)

im = Image.alpha_composite(im, overlay)
im.convert("RGB").save(IMAGE_PATH, quality=95)
print(f"Updated {IMAGE_PATH}")
