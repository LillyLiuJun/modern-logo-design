"""Gemini (Nano Banana). Reference images are sent directly with the request."""
from __future__ import annotations

import mimetypes
from pathlib import Path

import _config as cfg
from providers import GenResult

NAME = "gemini"


def _client():
    from google import genai
    from google.genai import types

    cfg.require_key(NAME)
    kwargs = {"api_key": cfg.api_key(NAME)}
    if cfg.base_url(NAME):
        kwargs["http_options"] = types.HttpOptions(base_url=cfg.base_url(NAME))
    return genai.Client(**kwargs)


def verify() -> str:
    m = _client().models.get(model=cfg.model(NAME))
    return getattr(m, "name", cfg.model(NAME))


def generate(prompt: str, refs: list[Path], aspect: str, size: str, quality: str) -> GenResult:
    from google.genai import types

    client = _client()
    contents = [types.Part.from_bytes(data=r.read_bytes(), mime_type=mimetypes.guess_type(r.name)[0] or "image/png")
                for r in refs]
    contents.append(types.Part.from_text(text=prompt))

    image_cfg = {"aspect_ratio": aspect}
    gsize = {"1K": "1K", "2K": "2K", "4K": "4K"}.get(size.upper()) if size else None
    if gsize:
        image_cfg["image_size"] = gsize
    resp = client.models.generate_content(
        model=cfg.model(NAME),
        contents=contents,
        config=types.GenerateContentConfig(response_modalities=["IMAGE"], image_config=types.ImageConfig(**image_cfg)),
    )
    out = GenResult()
    for cand in resp.candidates or []:
        for part in (cand.content.parts if cand.content else None) or []:
            if part.inline_data and part.inline_data.data:
                out.images.append((part.inline_data.data, part.inline_data.mime_type or "image/png"))
            elif part.text:
                out.texts.append(part.text)
    return out
