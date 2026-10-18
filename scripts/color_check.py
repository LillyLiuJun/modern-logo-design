#!/usr/bin/env python3
"""Color diagnosis: give 2–4 color values; outputs lightness, chroma, hue, warmth, pairwise contrast and engineering risk notes.

Calls no API and needs no third-party library.

Usage:
  python scripts/color_check.py "#211811" "#FFF5EF" "#FF7622"
  python scripts/color_check.py 211811 FFF5EF FF7622 --json
"""
from __future__ import annotations

import argparse
import json
import math
import sys

# Reference desktop colors: near-white for a light desktop, near-black for a dark one
LIGHT_DESKTOP = "#FFFFFF"
DARK_DESKTOP = "#1C1C1E"


def parse_hex(s: str) -> tuple[int, int, int]:
    s = s.strip().lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) != 6:
        raise ValueError(f"not a valid color value: {s}")
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
        return "neutral"
    pre = "slightly " if C < 0.03 else ""
    # OKLCH hue: about 0–110 red/orange/yellow and 330–360 magenta are warm; 140–300 green/cyan/blue are cool
    if h < 110 or h >= 330:
        return pre + "warm"
    if 140 <= h < 300:
        return pre + "cool"
    return "neutral"


def lightness_label(L: float) -> str:
    if L < 0.35:
        return "dark"
    if L < 0.8:
        return "mid"
    return "light"


def chroma_label(C: float) -> str:
    if C < 0.03:
        return "achromatic"
    if C < 0.1:
        return "low"
    if C < 0.17:
        return "medium"
    return "high"


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
            notes.append("melts on a light desktop: as a base it needs an inner stroke or a dark base instead")
        if on_dark < 1.5:
            notes.append("melts on a dark desktop: as a base its edge is unclear")
        if C >= 0.17 and 0.55 <= L <= 0.8:
            notes.append("high chroma, mid lightness: suits an accent, restless over a large area; contrast with light colors is usually insufficient, so avoid thin lines on a light base")
        if C < 0.03 and L < 0.3 and hx_n in ("#000000",):
            notes.append("pure black: replace with a dark color that has a hue")
        colors.append({
            "hex": hx_n,
            "oklch": {"L": round(L, 3), "C": round(C, 3), "h": round(h, 1)},
            "lightness": lightness_label(L),
            "chroma": chroma_label(C),
            "warmth": temperature(C, h),
            "contrast_light_desktop": round(on_light, 2),
            "contrast_dark_desktop": round(on_dark, 2),
            "notes": notes,
        })

    pairs = []
    for i in range(len(colors)):
        for j in range(i + 1, len(colors)):
            a, b = colors[i]["hex"], colors[j]["hex"]
            cr = contrast(parse_hex(a), parse_hex(b))
            if cr >= 4.5:
                use = "fine for text and thin lines"
            elif cr >= 3:
                use = "fine for shapes, not for text"
            else:
                use = "cannot be foreground/background of each other, only adjacent"
            pairs.append({"a": a, "b": b, "contrast": round(cr, 2), "use": use})

    # Hue spacing (chromatic colors only)
    chromatic = [c for c in colors if c["oklch"]["C"] >= 0.03]
    hue_notes = []
    for i in range(len(chromatic)):
        for j in range(i + 1, len(chromatic)):
            d = abs(chromatic[i]["oklch"]["h"] - chromatic[j]["oklch"]["h"])
            d = min(d, 360 - d)
            if d <= 30:
                txt = "adjacent hues, can make a gradient"
            elif d >= 150:
                txt = "near-complementary, cannot make a gradient (the middle goes grey)"
            else:
                txt = "wide hue span, be careful with a gradient"
            hue_notes.append({"a": chromatic[i]["hex"], "b": chromatic[j]["hex"], "hue_diff": round(d, 1), "note": txt})

    return {"colors": colors, "pairs": pairs, "hue": hue_notes}


def print_report(r: dict) -> None:
    print("Color       L     C      h      Light  Chroma     Warmth          vs light  vs dark")
    for c in r["colors"]:
        o = c["oklch"]
        print(f"{c['hex']}  {o['L']:.3f} {o['C']:.3f} {o['h']:6.1f}  {c['lightness']:<5}  {c['chroma']:<10} {c['warmth']:<15} "
              f"{c['contrast_light_desktop']:>6}  {c['contrast_dark_desktop']:>8}")
    print()
    for c in r["colors"]:
        for n in c["notes"]:
            print(f"! {c['hex']} {n}")
    print("\nPairwise contrast (WCAG)")
    for p in r["pairs"]:
        print(f"  {p['a']} / {p['b']}  {p['contrast']:>5}  {p['use']}")
    if r["hue"]:
        print("\nHue relations")
        for h in r["hue"]:
            print(f"  {h['a']} / {h['b']}  differ by {h['hue_diff']}°  {h['note']}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Color diagnosis (no API call)")
    ap.add_argument("colors", nargs="+", help="2–4 color values, e.g. #211811")
    ap.add_argument("--json", action="store_true", help="output JSON")
    a = ap.parse_args()
    if not 1 <= len(a.colors) <= 6:
        print("Please give 2–4 color values", file=sys.stderr)
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
