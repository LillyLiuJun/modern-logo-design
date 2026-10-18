"""Shared config: reads the image-provider settings from the .env in the skill folder.

Every provider uses the same naming: <PREFIX>_API_KEY / <PREFIX>_API_BASE_URL / <PREFIX>_MODEL.
IMAGE_PROVIDER decides which one is the default; system environment variables take priority over .env.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = SKILL_DIR / ".env"
PLACEHOLDER_KEYS = {"", "your_api_key_here"}

try:
    from dotenv import load_dotenv
    load_dotenv(ENV_PATH, override=False)
except ImportError:  # check_env.py reports missing dependencies separately
    pass


@dataclass(frozen=True)
class ProviderInfo:
    key: str          # gemini / openai / doubao
    label: str        # name shown to the user
    prefix: str       # environment variable prefix
    default_model: str
    default_base_url: str  # official address (empty means the SDK decides)


PROVIDERS = {
    "gemini": ProviderInfo("gemini", "Gemini (Nano Banana)", "GEMINI", "gemini-3.1-flash-image-preview", ""),
    "openai": ProviderInfo("openai", "ChatGPT (OpenAI image models)", "OPENAI", "gpt-image-2", ""),
    "doubao": ProviderInfo("doubao", "Doubao (Volcengine Ark Seedream)", "DOUBAO", "doubao-seedream-4-0-250828",
                           "https://ark.cn-beijing.volces.com/api/v3"),
}


def _env(name: str) -> str:
    return os.getenv(name, "").strip()


def provider_name(override: str | None = None) -> str:
    name = (override or _env("IMAGE_PROVIDER") or "gemini").lower()
    if name not in PROVIDERS:
        raise ValueError(f"IMAGE_PROVIDER must be one of {' / '.join(PROVIDERS)}, got: {name}")
    return name


def info(name: str) -> ProviderInfo:
    return PROVIDERS[name]


def api_key(name: str) -> str:
    return _env(f"{info(name).prefix}_API_KEY")


def base_url(name: str) -> str:
    return _env(f"{info(name).prefix}_API_BASE_URL")


def effective_base_url(name: str) -> str:
    return base_url(name) or info(name).default_base_url


def model(name: str) -> str:
    return _env(f"{info(name).prefix}_MODEL") or info(name).default_model


def key_is_set(name: str) -> bool:
    return api_key(name) not in PLACEHOLDER_KEYS


def output_dir() -> Path:
    raw = _env("LOGO_OUTPUT_DIR") or "output"
    p = Path(raw).expanduser()
    return p if p.is_absolute() else SKILL_DIR / p


def require_key(name: str) -> None:
    if not key_is_set(name):
        raise RuntimeError(
            f"{info(name).prefix}_API_KEY not found. Copy {SKILL_DIR / '.env.example'} to .env "
            f"and fill in your {info(name).label} key."
        )
