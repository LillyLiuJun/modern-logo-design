"""图像模型适配层。每个模块提供：

    generate(prompt, refs, aspect, size, quality) -> GenResult
    verify() -> str            # 在线验证，不出图；不支持时抛 NotImplementedError

refs 为空 = 文生图；有参考图 = 以参考图为基础修改（上色阶段锁定骨架）。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from importlib import import_module


@dataclass
class GenResult:
    images: list[tuple[bytes, str]] = field(default_factory=list)  # (数据, mime)
    texts: list[str] = field(default_factory=list)                 # 模型附带的文字回复


def load(name: str):
    module = {"gemini": "gemini", "openai": "openai_images", "doubao": "doubao"}[name]
    return import_module(f"providers.{module}")
