"""豆包图像模型（火山方舟 Seedream）。

接口：POST {base}/images/generations，Bearer 鉴权。
参考图以 data URI（data:image/png;base64,...）放进 image 字段，可传多张。
默认关闭「AI 生成」水印，要求返回 base64，避免官方图片链接过期。
不同版本支持的参数不同：可选参数被模型拒绝时，自动去掉后重试。
"""
from __future__ import annotations

import base64
import mimetypes
from pathlib import Path

import _config as cfg
from providers import GenResult

NAME = "doubao"

# 画幅 → 约 2K 的像素尺寸（Seedream 接受「宽x高」）。
SIZES = {"1:1": "2048x2048", "4:3": "2304x1728", "3:4": "1728x2304", "16:9": "2560x1440",
         "9:16": "1440x2560", "3:2": "2496x1664", "2:3": "1664x2496"}
# 去掉也不影响出图的参数；模型不支持时自动去掉。
OPTIONAL = ("watermark", "response_format", "size")


def _data_uri(p: Path) -> str:
    mime = mimetypes.guess_type(p.name)[0] or "image/png"
    return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"


def verify() -> str:
    raise NotImplementedError("豆包没有不出图的验证接口，第一次出图时会验证 key")


def _post(body: dict):
    import requests

    url = cfg.effective_base_url(NAME).rstrip("/") + "/images/generations"
    return requests.post(url, json=body, timeout=300,
                         headers={"Authorization": f"Bearer {cfg.api_key(NAME)}", "Content-Type": "application/json"})


def _error(r) -> RuntimeError:
    hint = ""
    if "InvalidEndpointOrModel" in r.text:
        hint = ("\n  提示：key 有效，但这个模型还没开通或 ID 不对。请在火山方舟控制台「开通管理」开通 Seedream，"
                "再把 .env 里的 DOUBAO_MODEL 改成控制台显示的模型 ID（也可以填推理接入点 ID，形如 ep-xxxx）。")
    elif r.status_code in (401, 403):
        hint = "\n  提示：key 无效或没有权限，请检查 DOUBAO_API_KEY。"
    return RuntimeError(f"HTTP {r.status_code}：{r.text[:500]}{hint}")


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
                print(f"  ! 当前模型不支持参数 {param}，已去掉后重试")
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
