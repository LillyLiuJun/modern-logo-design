"""Doubao image models (Volcengine Ark Seedream).

Endpoint: POST {base}/images/generations, Bearer auth.
Reference images go into the image field as data URIs (data:image/png;base64,...); several may be passed.
The "AI generated" watermark is off by default and base64 is requested, so official image links cannot expire.
Different versions support different parameters: when the model rejects an optional parameter, it is removed and the request retried.
"""
from __future__ import annotations

import base64
import mimetypes
from pathlib import Path

import _config as cfg
from providers import GenResult

NAME = "doubao"

# Aspect ratio -> pixel size of about 2K (Seedream accepts "WIDTHxHEIGHT").
SIZES = {"1:1": "2048x2048", "4:3": "2304x1728", "3:4": "1728x2304", "16:9": "2560x1440",
         "9:16": "1440x2560", "3:2": "2496x1664", "2:3": "1664x2496"}
# Parameters that can be dropped without affecting generation; removed automatically if the model does not support them.
OPTIONAL = ("watermark", "response_format", "size")


def _data_uri(p: Path) -> str:
    mime = mimetypes.guess_type(p.name)[0] or "image/png"
    return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"


def verify() -> str:
    raise NotImplementedError("Doubao has no validation endpoint that avoids generating an image; the key is validated on the first generation")


def _post(body: dict):
    import requests

    url = cfg.effective_base_url(NAME).rstrip("/") + "/images/generations"
    return requests.post(url, json=body, timeout=300,
                         headers={"Authorization": f"Bearer {cfg.api_key(NAME)}", "Content-Type": "application/json"})


def _error(r) -> RuntimeError:
    hint = ""
    if "InvalidEndpointOrModel" in r.text:
        hint = ("\n  Hint: the key is valid, but this model is not enabled or the ID is wrong. Enable Seedream under "
                "\"Activation Management\" in the Volcengine Ark console, then set DOUBAO_MODEL in .env to the model ID shown "
                "there (an inference endpoint ID such as ep-xxxx also works).")
    elif r.status_code in (401, 403):
        hint = "\n  Hint: the key is invalid or lacks permission. Check DOUBAO_API_KEY."
    return RuntimeError(f"HTTP {r.status_code}: {r.text[:500]}{hint}")


def generate(prompt: str, refs: list[Path], aspect: str, size: str, quality: str) -> GenResult:
    import requests

    cfg.require_key(NAME)
    body = {
        "model": cfg.model(NAME),
        "prompt": prompt,
        "size": SIZES.get(aspect, "2K"),
        "response_format": "b64_json",
        "watermark": False,
    }
    if refs:
        uris = [_data_uri(r) for r in refs]
        body["image"] = uris[0] if len(uris) == 1 else uris

    for _ in range(len(OPTIONAL) + 1):
        r = _post(body)
        if r.status_code == 400:
            try:
                param = (r.json().get("error") or {}).get("param", "")
            except ValueError:
                param = ""
            if param in OPTIONAL and param in body:
                print(f"  ! The current model does not support the parameter {param}; removed it and retrying")
                body.pop(param)
                continue
        break
    if r.status_code >= 400:
        raise _error(r)
    data = r.json()
    if data.get("error"):
        raise RuntimeError(str(data["error"])[:500])

    out = GenResult()
    for d in data.get("data") or []:
        if d.get("b64_json"):
            out.images.append((base64.b64decode(d["b64_json"]), "image/jpeg"))
        elif d.get("url"):
            img = requests.get(d["url"], timeout=120)
            img.raise_for_status()
            out.images.append((img.content, img.headers.get("Content-Type", "image/jpeg")))
        if d.get("error"):
            out.texts.append(str(d["error"]))
    return out
