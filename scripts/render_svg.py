#!/usr/bin/env python3
"""Render the SVG redrawn by Claude to PNG, compare it side by side with the original generated image, or color it directly by layer. Calls no API.

SVG conventions (follow them when redrawing so coloring can be exact per part):
  <rect id="bg" .../>      background (optional)
  <g id="skeleton">...</g> skeleton layer: main structure, outer contour
  <g id="focus">...</g>    accent layer: parts that need their own color (optional)
  The monochrome version always uses currentColor or #1A1A1A.

Usage:
  # Render and compare with the original (stage 3.5)
  python scripts/render_svg.py output/A3.svg --source output/A3.png --name A3-svg --direction "A3 · SVG redraw"
  # Color by layer (stage 4, exact values)
  python scripts/render_svg.py output/A3.svg --name A3-svg-c1 --stage color \
      --colors "skeleton=#17120C,focus=#FF7622,bg=#FAF7F2"
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _config as cfg  # noqa: E402

HEX = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


def render(svg_text: str, size: int) -> bytes:
    import resvg_py
    data = resvg_py.svg_to_bytes(svg_string=svg_text, width=size, height=size,
                                 shape_rendering="geometric_precision")
    return bytes(data)


def apply_colors(svg_text: str, colors: dict[str, str]) -> str:
    """Inject styles that color the SVG by layer: #skeleton / #focus / #bg."""
    rules = []
    for layer, color in colors.items():
        rules.append(f"#{layer}{{fill:{color};color:{color}}}")
        rules.append(f"#{layer} *{{fill:{color};color:{color}}}")
    style = "<style>" + "".join(rules) + "</style>"
    return re.sub(r"(<svg\b[^>]*>)", r"\1" + style, svg_text, count=1)


def parse_colors(raw: str) -> dict[str, str]:
    out = {}
    for item in filter(None, (x.strip() for x in raw.split(","))):
        k, _, v = item.partition("=")
        k, v = k.strip(), v.strip()
        if not k or not HEX.match(v):
            raise ValueError(f"colors must be written as layer=#RRGGBB, got: {item}")
        out[k] = v
    return out


def _font(px: int):
    from PIL import ImageFont
    for name in ("PingFang.ttc", "NotoSansCJK-Regular.ttc", "msyh.ttc", "Arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, px)
        except OSError:
            continue
    return ImageFont.load_default()


def compare(source: Path, png: bytes, size: int) -> bytes:
    from PIL import Image, ImageChops, ImageDraw
    a = Image.open(source).convert("L").resize((size, size))
    b = Image.open(io.BytesIO(png)).convert("RGBA")
    bg = Image.new("RGBA", b.size, "white")
    b = Image.alpha_composite(bg, b).convert("L").resize((size, size))
    diff = ImageChops.difference(a, b).point(lambda v: 255 if v > 60 else 0)
    overlay = Image.merge("RGB", (a, b, b))  # original leans red, SVG leans cyan, coincident areas are grey
    sheet = Image.new("RGB", (size * 3 + 40, size + 40), "white")
    d = ImageDraw.Draw(sheet)
    for i, (im, label) in enumerate([(a.convert("RGB"), "Original"), (b.convert("RGB"), "SVG redraw"),
                                     (overlay, "Overlay: red = original only, cyan = SVG only")]):
        sheet.paste(im, (i * (size + 20), 40))
        d.text((i * (size + 20) + 4, 10), label, fill="black", font=_font(16))
    ratio = sum(diff.histogram()[255:]) / (size * size)
    buf = io.BytesIO()
    sheet.save(buf, "PNG")
    print(f"  Contour difference ratio: {ratio:.1%} (a redraw corrects irregularities in the original, so it need not be 0)")
    return buf.getvalue()


def main() -> int:
    ap = argparse.ArgumentParser(description="Render an SVG, compare with the original, color by layer")
    ap.add_argument("svg", help="path of the SVG file")
    ap.add_argument("--name", help="output file name prefix (defaults to the SVG file name)")
    ap.add_argument("--size", type=int, default=1024, help="render size, default 1024")
    ap.add_argument("--source", help="original generated image, for side-by-side comparison")
    ap.add_argument("--colors", default="", help='color by layer, e.g. "skeleton=#17120C,focus=#FF7622,bg=#FAF7F2"')
    ap.add_argument("--stage", default="svg", choices=["svg", "color"], help="stage to record")
    ap.add_argument("--direction", default="", help="direction name (used on the review page)")
    ap.add_argument("--rationale", default="", help="description (used on the review page)")
    ap.add_argument("--out-dir", help="output folder (defaults to LOGO_OUTPUT_DIR in .env)")
    args = ap.parse_args()

    svg_path = Path(args.svg).expanduser()
    if not svg_path.is_file():
        print(f"✗ SVG not found: {svg_path}")
        return 1
    out_dir = Path(args.out_dir).expanduser() if args.out_dir else cfg.output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    name = args.name or svg_path.stem
    svg_text = svg_path.read_text(encoding="utf-8")

    colors = {}
    if args.colors:
        try:
            colors = parse_colors(args.colors)
        except ValueError as e:
            print(f"✗ {e}")
            return 1
        missing = [k for k in colors if f'id="{k}"' not in svg_text]
        if missing:
            print(f"! The SVG has no layer with these ids, so their colors will not apply: {', '.join(missing)}")
        svg_text = apply_colors(svg_text, colors)
        (out_dir / f"{name}.svg").write_text(svg_text, encoding="utf-8")
        print(f"✓ {out_dir / f'{name}.svg'}")

    try:
        png = render(svg_text, args.size)
    except Exception as e:  # noqa: BLE001
        print(f"✗ Render failed: {e}")
        return 1
    png_path = out_dir / f"{name}.png"
    png_path.write_bytes(png)
    print(f"✓ {png_path}")

    meta = {"name": name, "image": png_path.name, "stage": args.stage, "direction": args.direction,
            "rationale": args.rationale, "provider": "svg", "model": "Claude redraw",
            "svg": str(svg_path if not colors else out_dir / f"{name}.svg"), "colors": colors,
            "refs": [args.source] if args.source else [], "prompt_en": "", "prompt_zh": "",
            "aspect": "1:1", "created_at": datetime.now().isoformat(timespec="seconds")}
    png_path.with_suffix(".json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.source:
        src = Path(args.source).expanduser()
        if src.is_file():
            cmp_path = out_dir / f"{name}-compare.png"
            cmp_path.write_bytes(compare(src, png, min(args.size, 512)))
            print(f"✓ {cmp_path}")
        else:
            print(f"! Original not found, skipping comparison: {src}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
