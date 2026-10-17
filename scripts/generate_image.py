#!/usr/bin/env python3
"""调用图像模型生成 logo 图。支持 Gemini / ChatGPT（OpenAI）/ 豆包（火山方舟）。

  骨架阶段（文生图）：
    python scripts/generate_image.py --name A1 --prompt-file A1.en.txt --prompt-zh-file A1.zh.txt
  上色阶段（传入已确认的骨架图，锁定形状）：
    python scripts/generate_image.py --name A1-color --stage color --ref output/A1.png --prompt-file c.en.txt
  临时换一家模型：
    python scripts/generate_image.py --provider doubao ...

每张图旁边写一个同名 .json，记录中英文提示词、模型、参考图等，供对照页使用。
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
    ap = argparse.ArgumentParser(description="生成 logo 图像")
    ap.add_argument("--provider", choices=list(cfg.PROVIDERS), help="本次使用的模型（默认取 .env 的 IMAGE_PROVIDER）")
    ap.add_argument("--prompt", help="英文提示词（发送给模型）")
    ap.add_argument("--prompt-file", help="从文件读取英文提示词")
    ap.add_argument("--prompt-zh", default="", help="中文提示词（只用于记录与展示）")
    ap.add_argument("--prompt-zh-file", help="从文件读取中文提示词")
    ap.add_argument("--direction", default="", help="方向名称，如「A · 屏幕负空间」，用于对照页")
    ap.add_argument("--rationale", default="", help="设计阐述（用于对照页）")
    ap.add_argument("--rationale-file", help="从文件读取设计阐述")
    ap.add_argument("--ref", action="append", default=[], help="参考图路径，可重复；上色阶段传入已确认的骨架图")
    ap.add_argument("--name", default="logo", help="文件名前缀，如 A1、B2-color")
    ap.add_argument("--n", type=int, default=1, help="同一提示词生成几张（默认 1，每张单独请求）")
    ap.add_argument("--aspect", default="1:1", help="画幅比例，默认 1:1")
    ap.add_argument("--size", default="1K", help="Gemini 分辨率 1K/2K/4K，默认 1K（其他模型按画幅自动选尺寸）")
    ap.add_argument("--quality", default="", help="仅 OpenAI：low / medium / high / auto")
    ap.add_argument("--out-dir", help="输出目录（默认取 .env 的 LOGO_OUTPUT_DIR）")
    ap.add_argument("--stage", default="skeleton", choices=["skeleton", "color", "other"], help="记录所处阶段")
    ap.add_argument("--dry-run", action="store_true", help="只打印请求内容，不调用 API")
    args = ap.parse_args()

    try:
        pname = cfg.provider_name(args.provider)
    except ValueError as e:
        print(f"✗ {e}")
        return 2
    prompt = read_text(args.prompt, args.prompt_file)
    if not prompt:
        ap.error("需要 --prompt 或 --prompt-file")
    prompt_zh = read_text(args.prompt_zh, args.prompt_zh_file)
    rationale = read_text(args.rationale, args.rationale_file)
    refs = [Path(r).expanduser() for r in args.ref]
    for r in refs:
        if not r.is_file():
            ap.error(f"找不到参考图：{r}")
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
    print(f"使用 {cfg.info(pname).label} · {model}")

    saved = 0
    for i in range(1, args.n + 1):
        label = args.name if args.n == 1 else f"{args.name}-{i}"
        t0 = time.time()
        try:
            res = mod.generate(prompt, refs, args.aspect, args.size, args.quality)
        except Exception as e:  # noqa: BLE001
            print(f"✗ {label} 生成失败：{e}")
            continue
        if not res.images:
            print(f"✗ {label} 没有返回图片。" + (f" 模型回复：{' '.join(res.texts)[:300]}" if res.texts else ""))
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

    print(f"完成 {saved}/{args.n}")
    return 0 if saved else 1


if __name__ == "__main__":
    sys.exit(main())
