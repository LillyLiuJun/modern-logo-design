#!/usr/bin/env python3
"""Put the logo into an app-icon container (squircle) and preview it on light and dark backgrounds at several sizes.

Calls no API; composed locally, uses no quota. Used in stage 3 to check legibility at small sizes and in stage 4 to check the finished mark.

  python scripts/make_preview.py output/A1.png
  python scripts/make_preview.py output/A1-color.png --out output/A1-color-preview.png
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

LIGHT, DARK = (242, 242, 240), (28, 28, 30)


def squircle_mask(size: int, n: float = 5.0, ss: int = 4) -> Image.Image:
    """Mask of the squircle |x|^n + |y|^n = 1, antialiased with 4x supersampling."""
    big = size * ss
    mask = Image.new("L", (big, big), 0)
    px = mask.load()
    r = big / 2
    for y in range(big):
        ny = abs((y + 0.5 - r) / r) ** n
        if ny > 1:
            continue
        xr = (1 - ny) ** (1 / n) * r
        x0, x1 = int(r - xr), int(r + xr)
        for x in range(max(0, x0), min(big, x1 + 1)):
            px[x, y] = 255
    return mask.resize((size, size), Image.LANCZOS)


def icon(logo: Image.Image, size: int) -> Image.Image:
    tile = logo.convert("RGB").resize((size, size), Image.LANCZOS)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(tile, (0, 0), squircle_mask(size))
    return out


def font(px: int):
    for name in ("PingFang.ttc", "NotoSansCJK-Regular.ttc", "Arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, px)
        except OSError:
            continue
    return ImageFont.load_default()


def panel(logo: Image.Image, bg: tuple, label: str) -> Image.Image:
    W, H = 900, 420
    p = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(p)
    fg = (40, 40, 40) if bg == LIGHT else (220, 220, 220)
    d.text((24, 18), label, fill=fg, font=font(18))
    big = icon(logo, 256)
    shadow = Image.new("RGBA", (296, 296), (0, 0, 0, 0))
    shadow.paste((0, 0, 0, 70 if bg == LIGHT else 140), (20, 28), squircle_mask(256))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    p.paste(shadow, (24, 84), shadow)
    p.paste(big, (44, 96), big)
    x = 360
    for s in (180, 64, 32, 16):  # home screen / settings / menu bar / favicon
        ic = icon(logo, s)
        y = 96 + (256 - s) // 2
        p.paste(ic, (x, y), ic)
        d.text((x, 370), f"{s}px", fill=fg, font=font(14))
        x += s + 40
    return p


def main() -> int:
    ap = argparse.ArgumentParser(description="App-icon container preview (composed locally, no API call)")
    ap.add_argument("image", help="path of the logo image")
    ap.add_argument("--out", help="output path (default <name>-preview.png)")
    args = ap.parse_args()
    src = Path(args.image).expanduser()
    if not src.is_file():
        print(f"✗ Image not found: {src}")
        return 1
    logo = Image.open(src)
    sheet = Image.new("RGB", (900, 840))
    sheet.paste(panel(logo, LIGHT, "Light mode"), (0, 0))
    sheet.paste(panel(logo, DARK, "Dark mode"), (0, 420))
    out = Path(args.out).expanduser() if args.out else src.with_name(src.stem + "-preview.png")
    sheet.save(out)
    print(f"✓ {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
