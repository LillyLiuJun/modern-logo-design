#!/usr/bin/env python3
"""色彩诊断：输入 2–4 个色值，输出明度、彩度、色相、冷暖、两两对比度和工程风险提示。

不调用 API，不依赖第三方库。

用法：
  python scripts/color_check.py "#211811" "#FFF5EF" "#FF7622"
  python scripts/color_check.py 211811 FFF5EF FF7622 --json
"""
from __future__ import annotations

import argparse
import json
import math
import sys

# 桌面与容器参考色：浅色桌面近白，深色桌面近黑
LIGHT_DESKTOP = "#FFFFFF"
DARK_DESKTOP = "#1C1C1E"


def parse_hex(s: str) -> tuple[int, int, int]:
    s = s.strip().lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) != 6:
        raise ValueError(f"不是有效色值：{s}")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def _lin(c: float) -> float:
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def rel_luminance(rgb) -> float:
    r, g, b = (_lin(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b) -> float:
    la, lb = rel_luminance(a), rel_luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def oklch(rgb) -> tuple[float, float, float]:
    r, g, b = (_lin(c) for c in rgb)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (x ** (1 / 3) if x > 0 else 0.0 for x in (l, m, s))
    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    A = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    B = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    C = math.hypot(A, B)
    h = math.degrees(math.atan2(B, A)) % 360
    return L, C, h


def temperature(C: float, h: float) -> str:
    if C < 0.008:
        return "中性"
    pre = "微" if C < 0.03 else ""
    # OKLCH 色相：约 0–110 红橙黄、330–360 品红偏暖；140–300 绿青蓝偏冷
    if h < 110 or h >= 330:
        return pre + "暖"
    if 140 <= h < 300:
        return pre + "冷"
    return "中性"


def lightness_label(L: float) -> str:
    if L < 0.35:
        return "深"
    if L < 0.8:
        return "中"
    return "浅"


def chroma_label(C: float) -> str:
    if C < 0.03:
        return "近无彩"
    if C < 0.1:
        return "低彩"
    if C < 0.17:
        return "中彩"
    return "高彩"


def diagnose(hexes: list[str]) -> dict:
    colors = []
    for hx in hexes:
        rgb = parse_hex(hx)
        L, C, h = oklch(rgb)
        hx_n = "#%02X%02X%02X" % rgb
        on_light = contrast(rgb, parse_hex(LIGHT_DESKTOP))
        on_dark = contrast(rgb, parse_hex(DARK_DESKTOP))
        notes = []
        if on_light < 1.5:
            notes.append("在浅色桌面上会融化：做底板时需要内描边或改用深色底")
        if on_dark < 1.5:
            notes.append("在深色桌面上会融化：做底板时边界看不清")
        if C >= 0.17 and 0.55 <= L <= 0.8:
            notes.append("高彩中明度：适合焦点，大面积使用会浮躁；与浅色对比通常不足，不宜做浅底上的细线")
        if C < 0.03 and L < 0.3 and hx_n in ("#000000",):
            notes.append("纯黑：建议换成带色相的深色")
        colors.append({
            "hex": hx_n,
            "oklch": {"L": round(L, 3), "C": round(C, 3), "h": round(h, 1)},
            "明度": lightness_label(L),
            "彩度": chroma_label(C),
            "冷暖": temperature(C, h),
            "对比度_浅色桌面": round(on_light, 2),
            "对比度_深色桌面": round(on_dark, 2),
            "提示": notes,
        })

    pairs = []
    for i in range(len(colors)):
        for j in range(i + 1, len(colors)):
            a, b = colors[i]["hex"], colors[j]["hex"]
            cr = contrast(parse_hex(a), parse_hex(b))
            if cr >= 4.5:
                use = "可放文字和细线"
            elif cr >= 3:
                use = "可做图形，不放文字"
            else:
                use = "不能互为前景/背景，只能相邻"
            pairs.append({"a": a, "b": b, "对比度": round(cr, 2), "用法": use})

    # 色相间距（只看有彩色）
    chromatic = [c for c in colors if c["oklch"]["C"] >= 0.03]
    hue_notes = []
    for i in range(len(chromatic)):
        for j in range(i + 1, len(chromatic)):
            d = abs(chromatic[i]["oklch"]["h"] - chromatic[j]["oklch"]["h"])
            d = min(d, 360 - d)
            if d <= 30:
                txt = "相邻色相，可以做渐变"
            elif d >= 150:
                txt = "接近互补，不能做渐变（中间会发灰）"
            else:
                txt = "色相跨度较大，渐变需谨慎"
            hue_notes.append({"a": chromatic[i]["hex"], "b": chromatic[j]["hex"], "色相差": round(d, 1), "说明": txt})

    return {"colors": colors, "pairs": pairs, "hue": hue_notes}


def print_report(r: dict) -> None:
    print("色值        L     C      h      明度 彩度   冷暖   对浅桌面 对深桌面")
    for c in r["colors"]:
        o = c["oklch"]
        print(f"{c['hex']}  {o['L']:.3f} {o['C']:.3f} {o['h']:6.1f}  {c['明度']}   {c['彩度']:<4} {c['冷暖']:<4} "
              f"{c['对比度_浅色桌面']:>6}  {c['对比度_深色桌面']:>6}")
    print()
    for c in r["colors"]:
        for n in c["提示"]:
            print(f"! {c['hex']} {n}")
    print("\n两两对比度（WCAG）")
    for p in r["pairs"]:
        print(f"  {p['a']} / {p['b']}  {p['对比度']:>5}  {p['用法']}")
    if r["hue"]:
        print("\n色相关系")
        for h in r["hue"]:
            print(f"  {h['a']} / {h['b']}  相差 {h['色相差']}°  {h['说明']}")


def main() -> int:
    ap = argparse.ArgumentParser(description="色彩诊断（不调用 API）")
    ap.add_argument("colors", nargs="+", help="2–4 个色值，如 #211811")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    a = ap.parse_args()
    if not 1 <= len(a.colors) <= 6:
        print("请输入 2–4 个色值", file=sys.stderr)
        return 2
    try:
        r = diagnose(a.colors)
    except ValueError as e:
        print(f"✗ {e}", file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print_report(r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
