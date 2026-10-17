#!/usr/bin/env python3
"""把一轮生成的图做成「图 + 设计阐述 + 中英文提示词」对照页（单个 HTML 文件，图片内嵌，可离线打开）。

  python scripts/build_review.py --names A1 B1 C1 --title "Readio · 骨架第 1 轮" \
      --goal "找到一眼读出 R、又带认知意象的骨架" --out output/round1.html

不传 --names 时，收录输出目录里所有带 .json 的图（按生成时间排序）。
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

STAGE = {"skeleton": "骨架阶段 · 单色", "svg": "SVG 重绘", "color": "上色阶段", "other": "其他"}


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
    zh_block = (f'<div class="prompt"><div class="ph"><span>中文提示词</span>'
                f'<button type="button" data-copy="zh{idx}">复制</button></div><p id="zh{idx}">{esc(meta.get("prompt_zh"))}</p></div>'
                if meta.get("prompt_zh") else "")
    en_block = (f'<div class="prompt"><div class="ph"><span>English prompt</span>'
                f'<button type="button" data-copy="en{idx}">复制</button></div><p id="en{idx}" lang="en">{esc(meta.get("prompt_en"))}</p></div>'
                if meta.get("prompt_en") else "")
    if meta.get("svg"):
        en_block += f'<p class="meta">SVG 文件：{esc(Path(meta["svg"]).name)}' + (
            "　颜色：" + esc("，".join(f"{k} {v}" for k, v in meta["colors"].items())) if meta.get("colors") else "") + "</p>"
    return f"""<article class="card">
  <figure class="shot"><img src="{src}" alt="{esc(meta['name'])}">
    <figcaption><span class="tiny"><img src="{src}" alt="" width="32" height="32"></span>
      <span class="tiny"><img src="{src}" alt="" width="16" height="16"></span>32px / 16px 预览</figcaption></figure>
  <div class="body">
    <div class="tag">{esc(meta['name'])} · {esc(STAGE.get(meta.get('stage'), ''))}</div>
    <h2>{esc(title)}</h2>
    {f'<div class="why">{rationale}</div>' if rationale else ''}
    {zh_block}
    {en_block}
    <p class="meta">{esc(meta.get('provider', ''))} · {esc(meta.get('model', ''))} · {esc(meta.get('aspect', ''))}{(' · 参考图：' + esc(refs)) if refs else ''} · {esc(meta.get('created_at', ''))}</p>
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
try{await navigator.clipboard.writeText(el.textContent);b.textContent='已复制'}
catch(e){const r=document.createRange();r.selectNodeContents(el);const s=getSelection();s.removeAllRanges();s.addRange(r);b.textContent='已选中'}
setTimeout(()=>b.textContent=t,1500)}));"""


def main() -> int:
    ap = argparse.ArgumentParser(description="生成图片对照页")
    ap.add_argument("--dir", help="图片与 .json 所在目录（默认取 .env 的 LOGO_OUTPUT_DIR）")
    ap.add_argument("--names", nargs="*", help="要收录的图片名（不含扩展名），按给定顺序排列")
    ap.add_argument("--title", default="Logo 方案对照", help="页面标题")
    ap.add_argument("--goal", default="", help="本轮目标（一句话）")
    ap.add_argument("--notes", default="", help="页尾备注，如上一轮被否定的点、下一步")
    ap.add_argument("--out", help="输出 HTML 路径（默认 <目录>/review.html）")
    args = ap.parse_args()

    d = Path(args.dir).expanduser() if args.dir else cfg.output_dir()
    if args.names:
        metas = []
        for n in args.names:
            j = d / f"{n}.json"
            if not j.exists():
                print(f"✗ 找不到 {j}")
                return 1
            metas.append(json.loads(j.read_text(encoding="utf-8")))
    else:
        metas = sorted((json.loads(p.read_text(encoding="utf-8")) for p in d.glob("*.json")),
                       key=lambda m: m.get("created_at", ""))
    if not metas:
        print(f"✗ {d} 里没有可收录的图片")
        return 1

    cards = "\n".join(card(m, d, i) for i, m in enumerate(metas))
    goal = f'<section class="goal"><div><b>本轮目标：</b>{esc(args.goal)}</div></section>' if args.goal else ""
    notes = "".join(f"<p>{esc(x)}</p>" for x in args.notes.splitlines() if x.strip())
    page = f"""<!doctype html><html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(args.title)}</title><style>{CSS}</style></head>
<body><div class="wrap"><header><h1>{esc(args.title)}</h1><p class="lead">共 {len(metas)} 张。每张图旁边是设计阐述与中英文提示词，提示词可直接复制。</p></header>
{goal}{cards}{f'<section class="notes">{notes}</section>' if notes else ''}</div><script>{JS}</script></body></html>"""
    out = Path(args.out).expanduser() if args.out else d / "review.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"✓ {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
