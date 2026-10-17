#!/usr/bin/env python3
"""把 Claude 重绘的 SVG 渲染成 PNG，可与原生成图并排对比，也可按图层直接上色。不调用 API。

SVG 约定（重绘时遵守，上色才能精确到部件）：
  <rect id="bg" .../>      背景（可选）
  <g id="skeleton">...</g> 骨架层：主结构、外轮廓
  <g id="focus">...</g>    焦点层：需要单独上色的部件（可选）
  单色版一律用 currentColor 或 #1A1A1A。

用法：
  # 渲染并与原图对比（阶段 3.5）
  python scripts/render_svg.py output/A3.svg --source output/A3.png --name A3-svg --direction "A3 · SVG 重绘"
  # 按图层上色（阶段 4，精确色值）
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
    """在 SVG 里注入按图层上色的样式：#skeleton / #focus / #bg。"""
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
            raise ValueError(f"颜色格式应为 层名=#RRGGBB，收到：{item}")
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
    overlay = Image.merge("RGB", (a, b, b))  # 原图偏红、SVG 偏青，重合处为灰
    sheet = Image.new("RGB", (size * 3 + 40, size + 40), "white")
    d = ImageDraw.Draw(sheet)
    for i, (im, label) in enumerate([(a.convert("RGB"), "原生成图"), (b.convert("RGB"), "SVG 重绘"),
                                     (overlay, "叠加：红=只在原图 青=只在 SVG")]):
        sheet.paste(im, (i * (size + 20), 40))
        d.text((i * (size + 20) + 4, 10), label, fill="black", font=_font(16))
    ratio = sum(diff.histogram()[255:]) / (size * size)
    buf = io.BytesIO()
    sheet.save(buf, "PNG")
    print(f"  轮廓差异像素占比：{ratio:.1%}（重绘本来就会修正原图的不规整，差异不必为 0）")
    return buf.getvalue()


def main() -> int:
    ap = argparse.ArgumentParser(description="渲染 SVG、与原图对比、按图层上色")
    ap.add_argument("svg", help="SVG 文件路径")
    ap.add_argument("--name", help="输出文件名前缀（默认同 SVG 文件名）")
    ap.add_argument("--size", type=int, default=1024, help="渲染尺寸，默认 1024")
    ap.add_argument("--source", help="原生成图，用于并排对比")
    ap.add_argument("--colors", default="", help='按图层上色，如 "skeleton=#17120C,focus=#FF7622,bg=#FAF7F2"')
    ap.add_argument("--stage", default="svg", choices=["svg", "color"], help="记录所处阶段")
    ap.add_argument("--direction", default="", help="方向名称（用于对照页）")
    ap.add_argument("--rationale", default="", help="说明（用于对照页）")
    ap.add_argument("--out-dir", help="输出目录（默认取 .env 的 LOGO_OUTPUT_DIR）")
    args = ap.parse_args()

    svg_path = Path(args.svg).expanduser()
    if not svg_path.is_file():
        print(f"✗ 找不到 SVG：{svg_path}")
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
            print(f"! SVG 里没有这些图层 id，对应颜色不会生效：{', '.join(missing)}")
        svg_text = apply_colors(svg_text, colors)
        (out_dir / f"{name}.svg").write_text(svg_text, encoding="utf-8")
        print(f"✓ {out_dir / f'{name}.svg'}")

    try:
        png = render(svg_text, args.size)
    except Exception as e:  # noqa: BLE001
        print(f"✗ 渲染失败：{e}")
        return 1
    png_path = out_dir / f"{name}.png"
    png_path.write_bytes(png)
    print(f"✓ {png_path}")

    meta = {"name": name, "image": png_path.name, "stage": args.stage, "direction": args.direction,
            "rationale": args.rationale, "provider": "svg", "model": "Claude 重绘",
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
            print(f"! 找不到原图，跳过对比：{src}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
