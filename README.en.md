# Modern Logo Design

[简体中文](README.md) | **English**

A Claude skill for designing modern product logos: **skeleton first, color later**. Translating fuzzy brand ideas into marks with Bauhaus inevitability, mathematical order, high-order curvature tension, and OS-grade craft.

<p align="center">
  <img src="assets/example_svg_s_office.svg" width="240" alt="Example: rounded square with a negative-space S">
</p>
<p align="center"><sub>Example: rounded square with a negative-space S, redrawn as precise vector in stage 3.5</sub></p>

## Core Value Proposition: The First Principles of Logo Design

A logo is not an illustration or a decorative sticker—it is a distinct design object governed by intrinsic structural laws.

This skill translates intuitive, divergent brand ideas into the **inevitable first principles of authentic logos**:

- **Bauhaus Inevitability**: Every stroke is essential—one stroke more is redundancy; one stroke less is collapse. Imagery becomes the contour, not external decoration.
- **Mathematical Order**: All stems, arcs, and clearances share a strict baseline module $w$, built from disciplined boolean geometry.
- **High-Order Curvature (G²)**: Continuous curvature transitions (squircles) and taut arcs eliminate abrupt mechanical joints.
- **OS-Grade Durability**: **Skeleton first, color later**. The mark must stand resolute in pure monochrome and remain razor-sharp at 16px.

## What it does

Give it your product background. The skill derives imagery, generates candidates, helps you pick and refine one, applies color, and delivers a vector logo plus app-icon previews. You confirm at the end of every stage, and can step back at any time.

```
Stage 0    Setup              Check the image API
Stage 1    Brief              Product name, category, what to express, mark type
Stage 2    Monochrome matrix  Derive 3–4 directions → monochrome images → review page
Stage 3    Select & refine    Diagnose → local tweaks → lock 1 skeleton
Stage 3.5  SVG redraw         Claude redraws the skeleton as precise vector (recommended)
Stage 4    Color & deliver    Color diagnosis → role assignment → A/B/C schemes → app-icon preview
```

Three image providers are supported: **Gemini (Nano Banana)**, **ChatGPT (OpenAI image models)**, and **Doubao (Volcengine Ark Seedream)**.

> 💡 **Usage Note**:
> - **Prompt Generation**: We recommend using Gemini models for the conversational Agent, as its prompts tend to offer richer spatial and conceptual imagination.
> - **Image Generation**: Supports Gemini, ChatGPT, Doubao, and other compatible models (simply select the corresponding provider in your setup).

> The skill itself talks to you in Chinese. Prompts are stored in both Chinese and English.

## Quick start

1. Install and configure the API as described below (about 2 minutes).
2. Open Claude Code and say:

   > Design a logo for "XX"

3. Once you see the "environment ready" message, the skill walks you through the rest.

## Install

**1. Get the code**

Put it in Claude's skills directory (`~/.claude/skills/` on macOS / Linux, `%USERPROFILE%\.claude\skills\` on Windows).

The repository is private, so you must be signed in to GitHub first. Using `gh` is the easiest way:

```bash
gh auth login        # skip if already signed in
gh repo clone LillyLiuJun/modern-logo-design ~/.claude/skills/modern-logo-design
```

Or with plain git (requires access to the repository):

```bash
git clone https://github.com/LillyLiuJun/modern-logo-design.git ~/.claude/skills/modern-logo-design
```

**2. Install dependencies and create the config file**

```bash
cd ~/.claude/skills/modern-logo-design
pip install -r requirements.txt
cp .env.example .env
```

**3. Fill in the API settings and verify** (next section)

## Configure the API

Edit `.env`: choose the default provider with `IMAGE_PROVIDER`, then fill in only that provider's settings.

| Provider | `IMAGE_PROVIDER` | Required | Optional | Default model |
|---|---|---|---|---|
| Gemini (Nano Banana) | `gemini` | `GEMINI_API_KEY` | `GEMINI_API_BASE_URL`, `GEMINI_MODEL` | `gemini-3.1-flash-image-preview` |
| ChatGPT (OpenAI) | `openai` | `OPENAI_API_KEY` | `OPENAI_API_BASE_URL`, `OPENAI_MODEL` | `gpt-image-2` |
| Doubao (Seedream) | `doubao` | `DOUBAO_API_KEY` | `DOUBAO_API_BASE_URL`, `DOUBAO_MODEL` | `doubao-seedream-4-0-250828` |

Minimal example (Gemini):

```ini
IMAGE_PROVIDER=gemini
GEMINI_API_KEY=your_api_key_here
```

**Third-party relay**: set `*_API_BASE_URL` to the address your provider gives you. OpenAI relays usually end with `/v1`, Doubao relays with `/api/v3`; follow your provider's docs for Gemini. Leave it empty to use the official endpoint.

**Doubao note**: enable a Seedream model in the Volcengine Ark console and create a key under "API Key Management". Set `DOUBAO_MODEL` to a model ID you have enabled; newer versions (4.5, 5.0, …) are listed in the console.

**Other settings**: `LOGO_OUTPUT_DIR` sets where images are saved (default: `output/` inside the skill folder).

`.env` and `output/` are listed in `.gitignore` and will not be committed.

### Verify the setup

```bash
python scripts/check_env.py           # check the selected provider and validate the key online (no image generated, no image quota used)
python scripts/check_env.py --all     # show the status of all three providers
```

When you see the "environment ready" message you're good to go. Doubao has no key-validation endpoint that avoids generating an image, so its key is only validated on the first generation.

## Scripts

Claude normally runs these for you. Use them directly if you want manual control.

### Generate images

```bash
# Skeleton stage: text-only prompts
python scripts/generate_image.py --name A1 --prompt-file A1.en.txt --prompt-zh-file A1.zh.txt

# Color stage: pass the confirmed skeleton to lock the shape
python scripts/generate_image.py --name A1-color --stage color --ref output/A1.png --prompt-file c.en.txt

# Switch provider for one run
python scripts/generate_image.py --provider doubao --name A1 --prompt "..."

# Inspect the request without calling the API
python scripts/generate_image.py --dry-run --prompt "..."
```

Each image gets a sibling `.json` recording the Chinese and English prompts, the model, and any reference images.

### Other tools (none call an API)

```bash
# Review page: images + design rationale + Chinese/English prompts (only assembles the page)
python scripts/build_review.py --names A1 B1 C1 --title "Name · Skeleton round 1" --out output/round1.html

# SVG: render and compare with the source image / recolor by layer
python scripts/render_svg.py output/A3.svg --source output/A3.png --name A3-svg
python scripts/render_svg.py output/A3.svg --name A3-c1 --colors "skeleton=#17120C,focus=#FF7622,bg=#FAF7F2"

# Color diagnosis: lightness, chroma, warmth, pairwise contrast, gradient suitability
python scripts/color_check.py "#211811" "#FFF5EF" "#FF7622"

# App-icon preview: light / dark backgrounds at 180 / 64 / 32 / 16 px
python scripts/make_preview.py output/A1.png
```

## Troubleshooting

| Symptom | What to do |
|---|---|
| `check_env.py` reports an invalid key | Make sure the key belongs to the provider selected by `IMAGE_PROVIDER`, and that `.env` sits in the skill's root folder |
| 404 with a relay address | Check the URL suffix: `/v1` for OpenAI, `/api/v3` for Doubao |
| Doubao says the model isn't enabled | Enable it in the Ark console and set `DOUBAO_MODEL` to an enabled ID |
| Clone fails with a permission error | The repo is private: run `gh auth login` and make sure your account has access |

## Layout

```
modern-logo-design/
├── SKILL.md                    # Workflow (stages 0–4)
├── README.md / README.en.md    # Chinese / English docs
├── .env.example                # API config template
├── requirements.txt
├── assets/
│   └── example_svg_s_office.svg  # SVG redraw example
├── references/
│   ├── skeleton_axioms.md      # Skeleton axioms: derivation and diagnosis
│   ├── svg_redraw.md           # SVG redraw: conventions, steps, comparison, coloring
│   ├── color_dressing.md       # Coloring: diagnosis, roles, three schemes, checks
│   └── prompt_templates.md     # Chinese/English prompt templates
└── scripts/
    ├── _config.py              # Reads .env
    ├── check_env.py            # Environment check
    ├── generate_image.py       # Image generation
    ├── build_review.py         # Review page
    ├── render_svg.py           # SVG render, compare, per-layer coloring
    ├── color_check.py          # Color diagnosis
    ├── make_preview.py         # App-icon preview
    └── providers/              # Provider connectors
        ├── gemini.py
        ├── openai_images.py
        └── doubao.py
```
