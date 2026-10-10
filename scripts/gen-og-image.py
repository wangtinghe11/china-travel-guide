#!/usr/bin/env python3
"""Generate the China Travel Guide OG default image (1200x630 PNG)."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)

# Background: vertical gradient (deep navy -> blue)
top = (26, 26, 46)      # #1a1a2e
bottom = (15, 52, 96)   # #0f3460
for y in range(H):
    t = y / (H - 1)
    r = int(top[0] + (bottom[0] - top[0]) * t)
    g = int(top[1] + (bottom[1] - top[1]) * t)
    b = int(top[2] + (bottom[2] - top[2]) * t)
    d.line([(0, y), (W, y)], fill=(r, g, b))

# Accent bar (brand red #c8102e)
d.rectangle([0, H - 12, W, H], fill=(200, 16, 46))

# Title
try:
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 76)
    sub_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
except Exception:
    title_font = ImageFont.load_default()
    sub_font = ImageFont.load_default()

title = "China Travel Guide"
sub = "Visa · Payments · Rail · 10 Cities"

# Center title
bbox = d.textbbox((0, 0), title, font=title_font)
tw = bbox[2] - bbox[0]
d.text(((W - tw) / 2, 220), title, font=title_font, fill=(255, 255, 255))

# Subtitle
bbox2 = d.textbbox((0, 0), sub, font=sub_font)
tw2 = bbox2[2] - bbox2[0]
d.text(((W - tw2) / 2, 340), sub, font=sub_font, fill=(200, 16, 46))

# Tagline
tag = "Honest, practical guides for first-time visitors to China"
tag_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
bbox3 = d.textbbox((0, 0), tag, font=tag_font)
tw3 = bbox3[2] - bbox3[0]
d.text(((W - tw3) / 2, 430), tag, font=tag_font, fill=(220, 220, 220))

img.save("/root/china_travel_guide/public/images/og-default.png", "PNG")
print("saved og-default.png", img.size)
