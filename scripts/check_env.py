#!/usr/bin/env python3
"""Check the runtime environment: Python, dependencies, .env, the selected provider's key, and online validation (no image is generated).

  python scripts/check_env.py                    # check the provider selected by IMAGE_PROVIDER in .env
  python scripts/check_env.py --provider openai  # check a specific provider
  python scripts/check_env.py --all              # list the configuration status of all three providers
  python scripts/check_env.py --offline          # skip online validation
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
    ap = argparse.ArgumentParser(description="Check the image-provider environment of the logo skill")
    ap.add_argument("--provider", choices=list(cfg.PROVIDERS))
    ap.add_argument("--all", action="store_true", help="list the configuration status of all providers")
    ap.add_argument("--offline", action="store_true", help="skip online validation")
    args = ap.parse_args()
    problems = 0

    v = sys.version_info
    print(f"{OK if v >= (3, 9) else BAD} Python {v.major}.{v.minor}" + ("" if v >= (3, 9) else ", 3.9 or newer is required"))
    problems += v < (3, 9)
    for mod, pkg in COMMON:
        ok = has(mod)
        print(f"{OK if ok else BAD} {pkg}")
        problems += not ok

    if cfg.ENV_PATH.exists():
        print(f"{OK} Found {cfg.ENV_PATH}")
    else:
        print(f"{BAD} No .env. Run: cp {cfg.SKILL_DIR / '.env.example'} {cfg.ENV_PATH}")
        problems += 1

    try:
        current = cfg.provider_name(args.provider)
    except ValueError as e:
        print(f"{BAD} {e}")
        return 1
    print(f"{OK} Current provider: {cfg.info(current).label}")
    print(f"{OK} Output folder: {cfg.output_dir()}")

    targets = list(cfg.PROVIDERS) if args.all else [current]
    for name in targets:
        inf = cfg.info(name)
        print(f"\n[{inf.label}]{'  <- current' if name == current and args.all else ''}")
        local_bad = 0
        for mod, pkg in DEPS[name]:
            ok = has(mod)
            print(f"  {OK if ok else BAD} {pkg}")
            local_bad += not ok
        if cfg.key_is_set(name):
            print(f"  {OK} {inf.prefix}_API_KEY is set (...{cfg.api_key(name)[-4:]})")
        else:
            print(f"  {BAD if name == current else SKIP} {inf.prefix}_API_KEY is not set")
            local_bad += 1
        bu = cfg.base_url(name)
        if bu and not bu.startswith(("http://", "https://")):
            print(f"  {BAD} {inf.prefix}_API_BASE_URL must start with https://: {bu}")
            local_bad += 1
        else:
            print(f"  {OK} Endpoint: {bu or (inf.default_base_url or 'official default')}")
        print(f"  {OK} Model: {cfg.model(name)}")
        if name == current:
            problems += local_bad

        if name == current and not local_bad and not args.offline:
            try:
                mod = __import__("providers").load(name)
                print(f"  {OK} Online validation passed: {mod.verify()}")
            except NotImplementedError as e:
                print(f"  {SKIP} Online validation skipped: {e}")
            except Exception as e:  # noqa: BLE001
                print(f"  {BAD} Online validation failed: {e}")
                print("    Common causes: wrong key, wrong model name, no network, or a relay that does not support the validation endpoint.")
                problems += 1

    if problems:
        print(f"\nFound {problems} problem(s); fix them and run again. For missing dependencies run: pip install -r {cfg.SKILL_DIR / 'requirements.txt'}")
        return 1
    print("\nEnvironment ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
