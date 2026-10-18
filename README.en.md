# Modern Logo Design

[简体中文](README.md) | **English**

A skill for designing modern product logos: **skeleton first, color later**. Translating fuzzy brand ideas into marks with Bauhaus inevitability, mathematical order, high-order curvature tension, and OS-grade craft.

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

> 💡 **Model Note (Personal Preference)**:
> - **Prompt Generation**: If you are hesitating between Claude and Gemini, we personally lean toward recommending Gemini models as the conversational Agent; to some degree, its prompts tend to offer richer spatial and conceptual imagination.
> - **Image Generation**: Supports Gemini, ChatGPT, Doubao, and other compatible models (simply select the corresponding provider in your setup).

## How to Converge on Your Desired Mark (Iteration Techniques)

Great logos are rarely hit in a single lottery roll. They are the result of disciplined, stepwise convergence: "derive skeleton → diagnose defects → control-variable micro-tweaks". If initial candidates fall short of your vision, we recommend two practical methods:

### Method 1: Screenshot Reference Logos & Specify Exactly What You Approve
Provide 1–2 screenshots of existing logos that embody the vibe you want. **Avoid simply saying "make it like this"**. Instead, explicitly break down which specific elements you approve:
- "I like how these two strokes interlock to create airy negative space."
- "I like the taut, upright curvature of this outer squircle corner."
- "I appreciate the generous whitespace-to-mark ratio."
Tell the AI: *"Extract this geometric momentum and structural relationship from the reference, but do not copy the literal graphics."* Let AI leverage mature structural geometry rather than superficial mimicry.

### Method 2: Use "Physical Adjectives" Instead of Vague Taste Words
When evaluating drafts, avoid subjective, high-dimensional words like "not premium enough", "lacks vibe", or "looks dated"—AI cannot tune concrete geometric parameters from taste words.
Consult `references/skeleton_axioms.md` to translate your feeling into observable, physical dimensions:
- **Tight vs. Loose**: Is the internal counter or negative-space slit too cramped or too dispersed?
- **Thick vs. Thin**: Is the primary stroke too skeletal (hairline fragility) or too bulky (clunky blockiness)?
- **Heavy vs. Light**: Is the visual center of gravity floating too high, or sinking too low?
- **Sharp vs. Soft**: Are the vertices abrupt mechanical right-angles (needing G² squircle continuity), or slack like casual hand-drawings (needing arc tension)?
Instruct the AI in physical terms (e.g., *"The lower half feels too bottom-heavy; widen the clearance by 15% and apply micro-radiuses to all vertices"*). When diagnosing problems, **use low-dimensional physical language**; avoid subjective taste words like "looks bad" or "not premium".

## Quick Start

### 1. Setup (~2 minutes)

**Step 1: Download into the skills directory**

```bash
git clone https://github.com/LillyLiuJun/modern-logo-design.git ~/.claude/skills/modern-logo-design
```

**Step 2: Install dependencies and create the config file**

```bash
cd ~/.claude/skills/modern-logo-design
pip install -r requirements.txt
cp .env.example .env
```

**Step 3: Open `.env`, pick one image provider, and fill in only its key**

`IMAGE_PROVIDER` can be `gemini`, `openai` (ChatGPT) or `doubao`; the matching keys are `GEMINI_API_KEY`, `OPENAI_API_KEY` and `DOUBAO_API_KEY`.

For example, with Gemini:

```ini
IMAGE_PROVIDER=gemini
GEMINI_API_KEY=your key
```

Leave the other fields alone. Only fill in `*_API_BASE_URL` if you use a third-party relay.

**Check it (optional)**

```bash
python scripts/check_env.py
```

When you see "environment ready", you're set. You can skip this step: the skill checks automatically before the first image generation and tells you what's missing.

### 2. Start Designing

In your Agent terminal (taking Poplex as an example):

> Design a logo for "Poplex":
> 
> - **Name**: Poplex (capital P).
> - **Category & Context**: An iOS English-learning app for adults who want to use English in daily life. Positioning: *build language from your life*. It turns what you come across in your day into your own English, and is opened every day.
> - **What to convey**: Growth, accumulation, quiet restraint, a bookish editorial feel. Avoid the usual learning-app clichés: checkmarks, speech bubbles, A–Z letters, globes, light bulbs.
> - **Mark type**: Pure symbol. I'd like to see this kind of "growth" imagery first, using elements made from the letter P and a sprout.
> - **Existing material (optional)**: A few app screenshots and the current P + ink-dot mark, as tonal reference rather than something to copy.
> - **Regarding color**: Color is optional. If you give brand colors upfront (e.g. warm paper `#FBF8F5`, brand orange `#FF7622`, ink `#2A2320`), they are used when generating. If color gets in the way of judging the shape, switch back to monochrome, or keep refining color in stage 4.

These five points map one-to-one onto the skill's "Stage 1: Brief", so writing them all upfront avoids follow-up questions. For anything you haven't decided, just write "unsure, you recommend".

The skill will deduce 3–4 distinct structural directions, enter the skeleton stage, and assemble interactive HTML review pages at each round for visual comparison and diagnosis.

## Layout

```
modern-logo-design/
├── SKILL.md                    # Workflow (stages 0–4)
├── README.md / README.en.md    # Chinese / English docs
├── LICENSE                     # MIT License
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

## Contributing

Issues and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is licensed under the [MIT License](LICENSE).

