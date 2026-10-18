"""ChatGPT image models (OpenAI Images API).

Without reference images it uses images.generate; with reference images it uses images.edit (up to 16 references).
GPT image models always return base64.
"""
from __future__ import annotations

import base64
from contextlib import ExitStack
from pathlib import Path

import _config as cfg
from providers import GenResult

NAME = "openai"

# Aspect ratio -> size. Standard sizes are supported by all GPT image models; other ratios are left to the model.
SIZES = {"1:1": "1024x1024", "3:2": "1536x1024", "2:3": "1024x1536"}
MIME = {"png": "image/png", "jpeg": "image/jpeg", "webp": "image/webp"}


def _client():
    from openai import OpenAI

    cfg.require_key(NAME)
    kwargs = {"api_key": cfg.api_key(NAME)}
    if cfg.base_url(NAME):
        kwargs["base_url"] = cfg.base_url(NAME)
    return OpenAI(**kwargs)


def verify() -> str:
    m = _client().models.retrieve(cfg.model(NAME))
    return getattr(m, "id", cfg.model(NAME))


def generate(prompt: str, refs: list[Path], aspect: str, size: str, quality: str) -> GenResult:
    client = _client()
    params = {"model": cfg.model(NAME), "prompt": prompt, "n": 1, "output_format": "png",
              "size": SIZES.get(aspect, "auto")}
    if quality:
        params["quality"] = quality
    if refs:
        with ExitStack() as stack:
            files = [stack.enter_context(open(r, "rb")) for r in refs]
            resp = client.images.edit(image=files if len(files) > 1 else files[0], **params)
    else:
        resp = client.images.generate(**params)

    out = GenResult()
    mime = MIME.get(getattr(resp, "output_format", None) or "png", "image/png")
    for d in resp.data or []:
        if getattr(d, "b64_json", None):
            out.images.append((base64.b64decode(d.b64_json), mime))
        if getattr(d, "revised_prompt", None):
            out.texts.append(d.revised_prompt)
    return out
