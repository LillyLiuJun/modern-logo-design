"""共享配置：从 skill 目录下的 .env 读取图像模型设置。

每家模型用同一套命名：<前缀>_API_KEY / <前缀>_API_BASE_URL / <前缀>_MODEL。
IMAGE_PROVIDER 决定默认用哪一家；系统环境变量优先于 .env。
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
except ImportError:  # check_env.py 会单独报告缺少依赖
    pass


@dataclass(frozen=True)
class ProviderInfo:
    key: str          # gemini / openai / doubao
    label: str        # 给用户看的名字
    prefix: str       # 环境变量前缀
    default_model: str
    default_base_url: str  # 官方地址（留空表示由 SDK 决定）


PROVIDERS = {
    "gemini": ProviderInfo("gemini", "Gemini（Nano Banana）", "GEMINI", "gemini-3.1-flash-image-preview", ""),
    "openai": ProviderInfo("openai", "ChatGPT（OpenAI 图像模型）", "OPENAI", "gpt-image-2", ""),
    "doubao": ProviderInfo("doubao", "豆包（火山方舟 Seedream）", "DOUBAO", "doubao-seedream-4-0-250828",
                           "https://ark.cn-beijing.volces.com/api/v3"),
}


def _env(name: str) -> str:
    return os.getenv(name, "").strip()


def provider_name(override: str | None = None) -> str:
    name = (override or _env("IMAGE_PROVIDER") or "gemini").lower()
    if name not in PROVIDERS:
        raise ValueError(f"IMAGE_PROVIDER 只能是 {' / '.join(PROVIDERS)}，现在是：{name}")
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
            f"没有找到 {info(name).prefix}_API_KEY。请把 {SKILL_DIR / '.env.example'} 复制为 .env，"
            f"并填入 {info(name).label} 的 key。"
        )
