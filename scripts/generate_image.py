#!/usr/bin/env python3
"""Generate logo images with an image model. Supports Gemini / ChatGPT (OpenAI) / Doubao (Volcengine Ark).

  Skeleton stage (text-to-image):
    python scripts/generate_image.py --name A1 --prompt-file A1.en.txt --prompt-zh-file A1.zh.txt
  Color stage (pass the confirmed skeleton image to lock the shape):
    python scripts/generate_image.py --name A1-color --stage color --ref output/A1.png --prompt-file c.en.txt
  Switch provider for one run:
    python scripts/generate_image.py --provider doubao ...

A sibling .json is written next to every image, recording the English and translated prompts, the model, reference images and so on, for the review page.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _config as cfg  # noqa: E402
import providers  # noqa: E402


def sniff_ext(data: bytes, mime: str) -> str:
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return ".png"
    if data[:3] == b"\xff\xd8\xff":
        return ".jpg"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return ".webp"
    return {"image/jpeg": ".jpg", "image/webp": ".webp"}.get(mime, ".png")


def read_text(value: str | None, file: str | None) -> str:
    if file:
        return Path(file).expanduser().read_text(encoding="utf-8").strip()
    return (value or "").strip()


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate logo images")
    ap.add_argument("--provider", choices=list(cfg.PROVIDERS), help="provider for this run (defaults to IMAGE_PROVIDER in .env)")
    ap.add_argument("--prompt", help="English prompt (sent to the model)")
    ap.add_argument("--prompt-file", help="read the English prompt from a file")
    ap.add_argument("--prompt-zh", default="", help="translation of the prompt in the user's language (recorded and displayed only)")
    ap.add_argument("--prompt-zh-file", help="read the translated prompt from a file")
    ap.add_argument("--direction", default="", help="direction name, e.g. \"A · screen negative space\", used on the review page")
    ap.add_argument("--rationale", default="", help="design rationale (used on the review page)")
    ap.add_argument("--rationale-file", help="read the design rationale from a file")
    ap.add_argument("--ref", action="append", default=[], help="reference image path, repeatable; in the color stage pass the confirmed skeleton image")
    ap.add_argument("--name", default="logo", help="file name prefix, e.g. A1, B2-color")
    ap.add_argument("--n", type=int, default=1, help="how many images for the same prompt (default 1, one request each)")
    ap.add_argument("--aspect", default="1:1", help="aspect ratio, default 1:1")
    ap.add_argument("--size", default="1K", help="Gemini resolution 1K/2K/4K, default 1K (other providers pick a size from the aspect ratio)")
    ap.add_argument("--quality", default="", help="OpenAI only: low / medium / high / auto")
    ap.add_argument("--out-dir", help="output folder (defaults to LOGO_OUTPUT_DIR in .env)")
    ap.add_argument("--stage", default="skeleton", choices=["skeleton", "color", "other"], help="stage to record")
    ap.add_argument("--dry-run", action="store_true", help="print the request only, do not call the API")
    args = ap.parse_args()

    try:
        pname = cfg.provider_name(args.provider)
    except ValueError as e:
        print(f"✗ {e}")
        return 2
    prompt = read_text(args.prompt, args.prompt_file)
    if not prompt:
        ap.error("--prompt or --prompt-file is required")
    prompt_zh = read_text(args.prompt_zh, args.prompt_zh_file)
    rationale = read_text(args.rationale, args.rationale_file)
    refs = [Path(r).expanduser() for r in args.ref]
    for r in refs:
        if not r.is_file():
            ap.error(f"reference image not found: {r}")
    out_dir = Path(args.out_dir).expanduser() if args.out_dir else cfg.output_dir()
    model = cfg.model(pname)
    base = cfg.base_url(pname) or "official"

    if args.dry_run:
        print(json.dumps({"provider": pname, "model": model, "base_url": base, "refs": [str(r) for r in refs],
                          "aspect": args.aspect, "size": args.size, "quality": args.quality, "n": args.n,
                          "out_dir": str(out_dir), "prompt_en": prompt, "prompt_zh": prompt_zh},
                         ensure_ascii=False, indent=2))
        return 0

    try:
        cfg.require_key(pname)
        mod = providers.load(pname)
    except Exception as e:  # noqa: BLE001
        print(f"✗ {e}")
        return 2
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Using {cfg.info(pname).label} · {model}")

    saved = 0
    for i in range(1, args.n + 1):
        label = args.name if args.n == 1 else f"{args.name}-{i}"
        t0 = time.time()
        try:
            res = mod.generate(prompt, refs, args.aspect, args.size, args.quality)
        except Exception as e:  # noqa: BLE001
            print(f"✗ {label} generation failed: {e}")
            continue
        if not res.images:
            print(f"✗ {label} returned no image." + (f" Model reply: {' '.join(res.texts)[:300]}" if res.texts else ""))
            continue
        data, mime = res.images[0]
        img_path = out_dir / f"{label}{sniff_ext(data, mime)}"
        img_path.write_bytes(data)
        meta = {
            "name": label, "image": img_path.name, "stage": args.stage,
            "direction": args.direction, "rationale": rationale, "provider": pname, "model": model,
            "base_url": base, "aspect": args.aspect, "size": args.size, "quality": args.quality,
            "refs": [str(r) for r in refs], "prompt_en": prompt, "prompt_zh": prompt_zh,
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "seconds": round(time.time() - t0, 1), "model_text": res.texts,
        }
        img_path.with_suffix(".json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✓ {img_path}")
        saved += 1

    print(f"Done {saved}/{args.n}")
    return 0 if saved else 1


if __name__ == "__main__":
    sys.exit(main())
