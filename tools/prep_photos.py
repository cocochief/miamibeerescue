#!/usr/bin/env python3
"""Make web-ready copies of your own job photos.

    pip install Pillow
    python3 tools/prep_photos.py ~/Desktop/job-photos

For every JPEG/PNG/HEIC-converted image in the folder, writes two copies into
assets/photos/: <name>-1600.jpg and <name>-800.jpg. Each copy is rotated
upright, resized, re-encoded and saved WITHOUT metadata, so GPS coordinates,
camera serials and timestamps never reach the website.

Use only photos you took yourself on Miami-Dade jobs, with the owner's okay
when a house number, face or plate is visible.
"""
import os, re, sys
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(ROOT, "assets", "photos")
WIDTHS = (1600, 800)
EXTS = (".jpg", ".jpeg", ".png")


def clean_name(path):
    base = os.path.splitext(os.path.basename(path))[0].lower()
    return re.sub(r"[^a-z0-9]+", "-", base).strip("-") or "photo"


def prepare(src):
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        name = clean_name(src)
        for w in WIDTHS:
            copy = im.copy()
            if copy.width > w:
                copy = copy.resize((w, round(copy.height * w / copy.width)), Image.LANCZOS)
            out = os.path.join(DEST, f"{name}-{w}.jpg")
            # a fresh save with no exif= argument drops all metadata
            copy.save(out, "JPEG", quality=82, optimize=True, progressive=True)
            print("wrote", os.path.relpath(out, ROOT))


def main():
    if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
        sys.exit("usage: python3 tools/prep_photos.py <folder of photos>")
    os.makedirs(DEST, exist_ok=True)
    found = [os.path.join(sys.argv[1], f) for f in sorted(os.listdir(sys.argv[1])) if f.lower().endswith(EXTS)]
    if not found:
        sys.exit("no .jpg/.jpeg/.png files found (convert HEIC photos to JPEG first)")
    for f in found:
        prepare(f)


if __name__ == "__main__":
    main()
