"""Image-provider adapter layer. Each module provides:

    generate(prompt, refs, aspect, size, quality) -> GenResult
    verify() -> str            # online validation, no image generated; raises NotImplementedError if unsupported

Empty refs = text-to-image; with reference images = edit based on them (locks the skeleton in the coloring stage).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from importlib import import_module


@dataclass
class GenResult:
    images: list[tuple[bytes, str]] = field(default_factory=list)  # (data, mime)
    texts: list[str] = field(default_factory=list)                 # text replies attached by the model


def load(name: str):
    module = {"gemini": "gemini", "openai": "openai_images", "doubao": "doubao"}[name]
    return import_module(f"providers.{module}")
