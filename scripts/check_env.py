#!/usr/bin/env python3
"""检查运行环境：Python、依赖、.env、所选模型的 key，以及在线验证（不出图）。

  python scripts/check_env.py                    # 检查 .env 里 IMAGE_PROVIDER 选的那一家
  python scripts/check_env.py --provider openai  # 检查指定的一家
  python scripts/check_env.py --all              # 列出三家的配置状态
  python scripts/check_env.py --offline          # 不做在线验证
"""
from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _config as cfg  # noqa: E402

OK, BAD, SKIP = "✓", "✗", "–"
DEPS = {
    "gemini": [("google.genai", "google-genai")],
    "openai": [("openai", "openai")],
    "doubao": [("requests", "requests")],
}
COMMON = [("dotenv", "python-dotenv"), ("PIL", "Pillow")]


def has(mod: str) -> bool:
    try:
        importlib.import_module(mod)
        return True
    except ImportError:
        return False


def main() -> int:
    ap = argparse.ArgumentParser(description="检查 logo skill 的图像模型环境")
    ap.add_argument("--provider", choices=list(cfg.PROVIDERS))
    ap.add_argument("--all", action="store_true", help="列出所有模型的配置状态")
    ap.add_argument("--offline", action="store_true", help="跳过在线验证")
    args = ap.parse_args()
    problems = 0

    v = sys.version_info
    print(f"{OK if v >= (3, 9) else BAD} Python {v.major}.{v.minor}" + ("" if v >= (3, 9) else "，需要 3.9 或更高"))
    problems += v < (3, 9)
    for mod, pkg in COMMON:
        ok = has(mod)
        print(f"{OK if ok else BAD} {pkg}")
        problems += not ok

    if cfg.ENV_PATH.exists():
        print(f"{OK} 找到 {cfg.ENV_PATH}")
    else:
        print(f"{BAD} 没有 .env。请运行：cp {cfg.SKILL_DIR / '.env.example'} {cfg.ENV_PATH}")
        problems += 1

    try:
        current = cfg.provider_name(args.provider)
    except ValueError as e:
        print(f"{BAD} {e}")
        return 1
    print(f"{OK} 当前模型：{cfg.info(current).label}")
    print(f"{OK} 输出目录：{cfg.output_dir()}")

    targets = list(cfg.PROVIDERS) if args.all else [current]
    for name in targets:
        inf = cfg.info(name)
        print(f"\n[{inf.label}]{'  ← 当前' if name == current and args.all else ''}")
        local_bad = 0
        for mod, pkg in DEPS[name]:
            ok = has(mod)
            print(f"  {OK if ok else BAD} {pkg}")
            local_bad += not ok
        if cfg.key_is_set(name):
            print(f"  {OK} {inf.prefix}_API_KEY 已设置（…{cfg.api_key(name)[-4:]}）")
        else:
            print(f"  {BAD if name == current else SKIP} {inf.prefix}_API_KEY 未设置")
            local_bad += 1
        bu = cfg.base_url(name)
        if bu and not bu.startswith(("http://", "https://")):
            print(f"  {BAD} {inf.prefix}_API_BASE_URL 应以 https:// 开头：{bu}")
            local_bad += 1
        else:
            print(f"  {OK} 接口地址：{bu or (inf.default_base_url or '官方默认')}")
        print(f"  {OK} 模型：{cfg.model(name)}")
        if name == current:
            problems += local_bad

        if name == current and not local_bad and not args.offline:
            try:
                mod = __import__("providers").load(name)
                print(f"  {OK} 在线验证通过：{mod.verify()}")
            except NotImplementedError as e:
                print(f"  {SKIP} 跳过在线验证：{e}")
            except Exception as e:  # noqa: BLE001
                print(f"  {BAD} 在线验证失败：{e}")
                print("    常见原因：key 填错、模型名不对、网络不通、中转地址不支持该验证接口。")
                problems += 1

    if problems:
        print(f"\n发现 {problems} 个问题，修复后再运行一次。缺依赖请运行：pip install -r {cfg.SKILL_DIR / 'requirements.txt'}")
        return 1
    print("\n环境就绪。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
