#!/usr/bin/env python3
"""Draw the Miami Bee Rescue mark, favicons and the 1200x630 share image.

    pip install Pillow
    python3 tools/brand_images.py

Writes assets/mark.png, assets/mark-{32,48,180,192,512}.png,
assets/mark-apple.png and assets/og.jpg. Everything is drawn from
geometric shapes and text; no photographs are used.
"""
import math, os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

GRAPHITE = (27, 29, 33)
GRAPHITE_2 = (43, 46, 53)
MARIGOLD = (245, 183, 0)
LIMESTONE = (247, 243, 234)
PALE_GOLD = (255, 224, 138)

FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]
FONT_PATHS_REG = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/Library/Fonts/Arial.ttf",
    "C:/Windows/Fonts/arial.ttf",
]


def load_font(paths, size):
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def draw_mark(size):
    """Square mark: graphite field, two Deco arches, three rays, a bee."""
    k = 8  # supersample
    S = size * k
    img = Image.new("RGB", (S, S), GRAPHITE)
    d = ImageDraw.Draw(img)
    u = S / 64.0

    def arch(inset, width):
        # vertical sides from y=56 up to the arch spring line, then a half circle
        left, right = inset * u, (64 - inset) * u
        r = (right - left) / 2
        cx, cy = S / 2, 34 * u
        d.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=MARIGOLD, width=int(width * u))
        d.line([left + width * u / 2, cy, left + width * u / 2, 56 * u], fill=MARIGOLD, width=int(width * u))
        d.line([right - width * u / 2, cy, right - width * u / 2, 56 * u], fill=MARIGOLD, width=int(width * u))

    arch(8, 4)
    arch(16, 2.5)
    for x0, y0, x1, y1 in ((32, 10, 32, 16), (15, 17, 19, 21.5), (49, 17, 45, 21.5)):
        d.line([x0 * u, y0 * u, x1 * u, y1 * u], fill=MARIGOLD, width=int(2.5 * u))
    # wings (rotated ellipses drawn on a temp layer)
    for angle, cx in ((-28, 25), (28, 39)):
        w = Image.new("RGBA", (int(14 * u), int(9 * u)), (0, 0, 0, 0))
        ImageDraw.Draw(w).ellipse([0, 0, w.width - 1, w.height - 1], fill=LIMESTONE + (255,))
        w = w.rotate(-angle, expand=True, resample=Image.BICUBIC)
        img.paste(w, (int(cx * u - w.width / 2), int(31 * u - w.height / 2)), w)
    d.ellipse([25 * u, 31.5 * u, 39 * u, 50.5 * u], fill=MARIGOLD)
    for y, x0, x1 in ((38, 25.4, 38.6), (43.5, 25.6, 38.4), (48.6, 27, 37)):
        d.line([x0 * u, y * u, x1 * u, y * u], fill=GRAPHITE, width=int(2.4 * u))
    return img.resize((size, size), Image.LANCZOS)


def draw_og():
    W, H, k = 1200, 630, 2
    img = Image.new("RGB", (W * k, H * k), GRAPHITE)
    d = ImageDraw.Draw(img)
    # sunburst rays from below the bottom edge
    cx, cy = W * k * 0.78, H * k * 1.15
    for i in range(0, 180, 9):
        a0, a1 = math.radians(180 + i), math.radians(180 + i + 4)
        R = W * k * 1.5
        d.polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)), (cx + R * math.cos(a1), cy + R * math.sin(a1))],
                  fill=GRAPHITE_2)
    # stepped gold base
    d.rectangle([0, (H - 10) * k, W * k, H * k], fill=MARIGOLD)
    x = 0
    while x < W * k:
        d.rectangle([x, (H - 22) * k, x + 56 * k, (H - 14) * k], fill=MARIGOLD)
        x += 80 * k
    mark = draw_mark(300).resize((300 * k, 300 * k), Image.LANCZOS)
    img.paste(mark, (80 * k, 150 * k))
    d.rectangle([80 * k - 6 * k, 150 * k - 6 * k, 380 * k + 6 * k, 450 * k + 6 * k], outline=MARIGOLD, width=4 * k)
    big = load_font(FONT_PATHS, 84 * k)
    mid = load_font(FONT_PATHS_REG, 38 * k)
    tag = load_font(FONT_PATHS, 26 * k)
    d.text((440 * k, 150 * k), "MIAMI", font=big, fill=MARIGOLD)
    d.text((440 * k, 245 * k), "Bee Rescue", font=big, fill=(255, 255, 255))
    d.text((442 * k, 360 * k), "Live honey bee removal across", font=mid, fill=LIMESTONE)
    d.text((442 * k, 408 * k), "Miami-Dade County", font=mid, fill=LIMESTONE)
    d.rectangle([442 * k, 482 * k, 828 * k, 534 * k], fill=MARIGOLD)
    d.text((462 * k, 492 * k), "(786) 442-2496  ·  24/7", font=tag, fill=GRAPHITE)
    return img.resize((W, H), Image.LANCZOS)


def main():
    os.makedirs(ASSETS, exist_ok=True)
    big = draw_mark(512)
    big.save(os.path.join(ASSETS, "mark-512.png"), optimize=True)
    big.save(os.path.join(ASSETS, "mark.png"), optimize=True)
    for n in (32, 48, 180, 192):
        draw_mark(n).save(os.path.join(ASSETS, f"mark-{n}.png"), optimize=True)
    # apple touch icon: mark inset on a graphite margin so iOS corner rounding keeps the arch
    apple = Image.new("RGB", (180, 180), GRAPHITE)
    apple.paste(draw_mark(160), (10, 10))
    apple.save(os.path.join(ASSETS, "mark-apple.png"), optimize=True)
    draw_og().save(os.path.join(ASSETS, "og.jpg"), quality=86, optimize=True, progressive=True)
    print("wrote mark-*.png and og.jpg to", ASSETS)


if __name__ == "__main__":
    main()
