#!/usr/bin/env python3
"""Build a review page from one round of images: image + design rationale + prompts (English and translation). A single HTML file with embedded images that opens offline.

  python scripts/build_review.py --names A1 B1 C1 --title "Readio · Skeleton round 1" \
      --goal "Find a skeleton that reads as R at a glance and carries a cognition motif" --out output/round1.html

Without --names, every image that has a .json in the output folder is included (sorted by creation time).
"""
from __future__ import annotations

import argparse
import base64
import html
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _config as cfg  # noqa: E402

STAGE = {"skeleton": "Skeleton stage · monochrome", "svg": "SVG redraw", "color": "Color stage", "other": "Other"}


def embed(img_path: Path, max_side: int = 768) -> str:
    try:
        from PIL import Image
        im = Image.open(img_path)
        im.thumbnail((max_side, max_side))
        buf = io.BytesIO()
        im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB").save(buf, "PNG")
        data, mime = buf.getvalue(), "image/png"
    except Exception:  # noqa: BLE001
        data, mime = img_path.read_bytes(), "image/png"
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"


def esc(s: str) -> str:
    return html.escape(s or "")


def card(meta: dict, img_dir: Path, idx: int) -> str:
    img = img_dir / meta["image"]
    src = embed(img) if img.exists() else ""
    title = meta.get("direction") or meta["name"]
    rationale = "".join(f"<p>{esc(line)}</p>" for line in (meta.get("rationale") or "").splitlines() if line.strip())
    refs = ", ".join(Path(r).name for r in meta.get("refs") or [])
    zh_block = (f'<div class="prompt"><div class="ph"><span>Prompt (translation)</span>'
                f'<button type="button" data-copy="zh{idx}">Copy</button></div><p id="zh{idx}">{esc(meta.get("prompt_zh"))}</p></div>'
                if meta.get("prompt_zh") else "")
    en_block = (f'<div class="prompt"><div class="ph"><span>Prompt (English, sent to the model)</span>'
                f'<button type="button" data-copy="en{idx}">Copy</button></div><p id="en{idx}" lang="en">{esc(meta.get("prompt_en"))}</p></div>'
                if meta.get("prompt_en") else "")
    if meta.get("svg"):
        en_block += f'<p class="meta">SVG file: {esc(Path(meta["svg"]).name)}' + (
            "  Colors: " + esc("，".join(f"{k} {v}" for k, v in meta["colors"].items())) if meta.get("colors") else "") + "</p>"
    return f"""<article class="card">
  <figure class="shot"><img src="{src}" alt="{esc(meta['name'])}">
    <figcaption><span class="tiny"><img src="{src}" alt="" width="32" height="32"></span>
      <span class="tiny"><img src="{src}" alt="" width="16" height="16"></span>32px / 16px preview</figcaption></figure>
  <div class="body">
    <div class="tag">{esc(meta['name'])} · {esc(STAGE.get(meta.get('stage'), ''))}</div>
    <h2>{esc(title)}</h2>
    {f'<div class="why">{rationale}</div>' if rationale else ''}
    {zh_block}
    {en_block}
    <p class="meta">{esc(meta.get('provider', ''))} · {esc(meta.get('model', ''))} · {esc(meta.get('aspect', ''))}{(' · Reference: ' + esc(refs)) if refs else ''} · {esc(meta.get('created_at', ''))}</p>
  </div></article>"""


CSS = """
:root{--bg:#F5F4F1;--surface:#FFFFFF;--fg:#1A1A1A;--muted:#6B6A66;--line:#DDDAD3;--accent:#2F5BD3}
@media (prefers-color-scheme:dark){:root{--bg:#151514;--surface:#1E1E1C;--fg:#EDEBE6;--muted:#A3A19B;--line:#34332F;--accent:#8EA8F0;color-scheme:dark}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 system-ui,-apple-system,"PingFang SC","Noto Sans SC",sans-serif;padding:32px 16px 48px}
.wrap{max-width:1040px;margin:0 auto;display:grid;gap:24px}
h1{font-size:1.6rem;margin:0 0 6px}
.lead{margin:0;color:var(--muted);max-width:65ch}
.goal{border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:12px 0;display:grid;gap:4px;font-size:.92rem}
.card{display:grid;grid-template-columns:300px 1fr;gap:24px;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:20px}
.shot{margin:0;display:grid;gap:8px;align-content:start}
.shot>img{width:100%;height:auto;border-radius:6px;border:1px solid var(--line)}
figcaption{font-size:.8rem;color:var(--muted);display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.tiny img{display:block;border:1px solid var(--line)}
.body{min-width:0;display:grid;gap:10px;align-content:start}
.tag{font-size:.75rem;letter-spacing:.04em;color:var(--muted)}
h2{margin:0;font-size:1.15rem}
.why p{margin:0 0 4px}
.prompt{border:1px solid var(--line);border-radius:6px}
.ph{display:flex;justify-content:space-between;align-items:center;padding:6px 10px;border-bottom:1px solid var(--line);font-size:.75rem;color:var(--muted)}
.prompt p{margin:0;padding:10px;font-size:.84rem;white-space:pre-wrap;word-break:break-word}
.prompt p[lang]{font-family:ui-monospace,Menlo,monospace;font-size:.78rem}
button{font:inherit;font-size:.75rem;color:var(--fg);background:transparent;border:1px solid var(--line);border-radius:4px;padding:2px 10px;cursor:pointer}
.meta{margin:0;font-size:.75rem;color:var(--muted)}
.notes{font-size:.92rem;border-top:1px solid var(--line);padding-top:12px}
@media (max-width:760px){.card{grid-template-columns:1fr}.shot{max-width:300px}}
"""
JS = """document.querySelectorAll('button[data-copy]').forEach(b=>b.addEventListener('click',async()=>{
const el=document.getElementById(b.dataset.copy),t=b.textContent;
try{await navigator.clipboard.writeText(el.textContent);b.textContent='Copied'}
catch(e){const r=document.createRange();r.selectNodeContents(el);const s=getSelection();s.removeAllRanges();s.addRange(r);b.textContent='Selected'}
setTimeout(()=>b.textContent=t,1500)}));"""


def main() -> int:
    ap = argparse.ArgumentParser(description="Build the image review page")
    ap.add_argument("--dir", help="folder containing the images and .json files (defaults to LOGO_OUTPUT_DIR in .env)")
    ap.add_argument("--names", nargs="*", help="image names to include (without extension), in the given order")
    ap.add_argument("--title", default="Logo review", help="page title")
    ap.add_argument("--goal", default="", help="goal of this round (one sentence)")
    ap.add_argument("--notes", default="", help="footer notes, e.g. what was rejected last round, next steps")
    ap.add_argument("--out", help="output HTML path (default <folder>/review.html)")
    args = ap.parse_args()

    d = Path(args.dir).expanduser() if args.dir else cfg.output_dir()
    if args.names:
        metas = []
        for n in args.names:
            j = d / f"{n}.json"
            if not j.exists():
                print(f"✗ Not found: {j}")
                return 1
            metas.append(json.loads(j.read_text(encoding="utf-8")))
    else:
        metas = sorted((json.loads(p.read_text(encoding="utf-8")) for p in d.glob("*.json")),
                       key=lambda m: m.get("created_at", ""))
    if not metas:
        print(f"✗ No images to include in {d}")
        return 1

    cards = "\n".join(card(m, d, i) for i, m in enumerate(metas))
    goal = f'<section class="goal"><div><b>Goal of this round:</b>{esc(args.goal)}</div></section>' if args.goal else ""
    notes = "".join(f"<p>{esc(x)}</p>" for x in args.notes.splitlines() if x.strip())
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(args.title)}</title><style>{CSS}</style></head>
<body><div class="wrap"><header><h1>{esc(args.title)}</h1><p class="lead">{len(metas)} image(s). Each image comes with its design rationale and prompts (English and translation); prompts can be copied directly.</p></header>
{goal}{cards}{f'<section class="notes">{notes}</section>' if notes else ''}</div><script>{JS}</script></body></html>"""
    out = Path(args.out).expanduser() if args.out else d / "review.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"✓ {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
