---
name: modern-logo-design
description: Design a modern logo for a product. Translates fuzzy, divergent, concrete brand ideas into engineering-grade prompts and vector skeletons with Bauhaus inevitability, mathematical order, high-order curvature tension and OS-grade craft. First generates pure monochrome skeleton candidates; once a skeleton is locked, applies color and generates app-icon container previews. Every round produces a review page with the images, the design rationale and the prompts. Use when the user wants to make or revise a logo, or asks why a logo does not feel modern or premium enough. Works in any language; reply in the user's language.
---

# Modern Logo Design

Core purpose: translate the user's emotional, divergent, concrete brand ideas into a logo with **Bauhaus inevitability, modern mathematical order, high-order curvature tension and OS-grade craft**. The translation rests on the three axioms in `references/skeleton_axioms.md`: formal inevitability, mathematical order (module, boolean construction, continuous curvature, center-of-mass balance) and negative defense. The same axioms are used to derive directions, write prompts and diagnose generated images.

**Reply in the user's language.** The instructions in this file are in English; the conversation, design rationales and review-page text follow the user.

The whole process: **skeleton first, color later**.

- The **skeleton** is the identity of the logo. Strip away all color, lighting and background; it must still hold up in a single color.
- **Color** is a finishing layer applied to a locked skeleton, using the colors the user chose, as long as it does not damage the skeleton.

Never introduce color during the skeleton stage, and never color before the skeleton is locked. This rule comes from practice: color problems are often skeleton problems in disguise ("the black is too heavy" is really an inconsistent stroke width). Coloring first mixes the two kinds of problem together, and every fix makes things worse.

## References

| When to read | File |
|---|---|
| Stage 2 (deriving directions) and stage 3 (diagnosis); the core document | `references/skeleton_axioms.md` |
| Stage 3.5 (redrawing as SVG) | `references/svg_redraw.md` |
| Stage 4 (coloring) | `references/color_dressing.md` |
| Every time you write a prompt | `references/prompt_templates.md` |

## Process overview

```
Stage 0    Setup              Check the image API; if it is not configured, guide the user and stop
Stage 1    Brief              Product name, category, what to express, mark type
Stage 2    Monochrome matrix  Derive 3–4 directions → monochrome images → review page
Stage 3    Select & refine    Diagnose → local tweaks → the user locks 1 skeleton
Stage 3.5  SVG redraw         Claude redraws the skeleton as precise vector by the axioms (recommended, skippable)
Stage 4    Color & deliver    Color diagnosis → role assignment → A/B/C schemes → container preview
```

Image models handle "exploring imagery" (stages 2 and 3). Claude handles "precise execution" (stages 3.5 and 4).

At the end of every stage, wait for the user's confirmation before moving on. The user can step back to an earlier stage at any time.

---

## Stage 0: Setup

**Whenever you run a script from this skill**: if the skill directory contains a `.venv`, use `<skill dir>/.venv/bin/python` (on Windows, `.venv\Scripts\python`); otherwise use `python3`. Dependencies are installed in `.venv`, so the system Python reports missing packages. Read every `python` in the commands below with this rule applied.

Before the first image generation in a session, run:

```bash
python <skill dir>/scripts/check_env.py
```

- If you see "Environment ready": continue.
- If there is a ✗: do not call the generation script. Tell the user what to do:
  1. `pip install -r requirements.txt`
  2. `cp .env.example .env`
  3. In `.env`, set `IMAGE_PROVIDER` (gemini / openai / doubao) and fill in that provider's `*_API_KEY`; if using a relay, also fill in `*_API_BASE_URL`
  4. Run `check_env.py` again

**The user's key goes only into `.env`. Never repeat it in the conversation or write it to any other file.**

## Stage 1: Brief

Ask in a single round, with short questions. Do not ask about anything you can already tell from the context.

1. **Name** (required)
2. **Category and context**: what it does and who it is for
3. **What to convey**: one or two keywords (e.g. growth, thinking, connection, efficiency)
4. **Mark type**: letter mark (which letter) / pure symbol / wordmark / unsure (you recommend)
5. **Existing material** (optional): current logo, product screenshots, reference images

**Do not proactively ask about color at this stage.** If the user gave colors upfront, use them when generating. If color gets in the way of judging the shape, switch back to monochrome, or keep refining color in stage 4.

If there are product screenshots, look at them first. Whether the product is quiet and humanistic or high-energy and tool-like affects the choice of directions and, later, the colors.

## Stage 2: Monochrome skeleton matrix

Read `references/skeleton_axioms.md` first.

### 2.1 Derive directions

Derive **3–4 structurally distinct** directions, not one structure with different parameters. For each direction, state:

- **Imagery reduction**: what motion the concept is distilled into (e.g. growth → a single upward curvature)
- **Structure**: which base shapes and how they combine (boolean add/subtract, symmetry)
- **Closed or open**, and why (following the decision order in the axioms document)
- **Risk**: where this direction is most likely to fail

List the directions to the user in text and ask "Shall I generate images for these directions?" Skip the confirmation if the user said to go straight to images.

### 2.2 Generate images

Write the prompts from the skeleton template in `references/prompt_templates.md`: **monochrome, flat, no gradients, no lighting effects**. Generate 1 image per direction (more if the user asks). Before generating, tell the user how many images this round will produce and that it uses API quota.

```bash
python scripts/generate_image.py --name A1 --stage skeleton \
  --direction "A · direction name" --rationale-file A1.why.txt \
  --prompt-file A1.en.txt --prompt-zh-file A1.zh.txt
```

`--prompt-file` is the English prompt sent to the model. `--prompt-zh-file` is an optional translation of it into the user's language, stored for display on the review page (the flag keeps its historical name).

Always put long text in a temporary file and pass it with `--*-file`, to avoid command-line escaping problems.

### 2.3 Review page

```bash
python scripts/build_review.py --names A1 B1 C1 --title "<name> · Skeleton round 1" \
  --goal "<goal of this round>" --out output/<name>-round1.html
```

Hand the review page to the user (publish it as a web page if you can, otherwise send the HTML file). In the conversation, write only a one-sentence judgment per direction and your recommendation; do not repeat the page.

**After you see the generated images, first diagnose them yourself against the axioms.** Models often fail to draw the structure the prompt asks for (for example, two cards drawn as one tube). Say honestly what was not drawn; do not describe the result as better than it is.

## Stage 3: Select and refine

1. The user picks a direction or gives feedback. Restate it first: "What you approve is X; what you want to change is Y."
2. Following the diagnosis order in `skeleton_axioms.md`, find 1–3 key problems. For each, write "what it looks like → which axiom it violates → the fix".
3. Change only one variable per round. Use the image the user picked last round as `--ref`, and state clearly in the prompt what to keep and what to change. Adjust negative words by axiom three: add words against the side the last round fell to and keep the other side, so the fix does not overcorrect.
4. Check small sizes with `make_preview.py`:
   ```bash
   python scripts/make_preview.py output/A2.png
   ```
   A skeleton that is unrecognizable at 16px or 32px cannot be locked.
5. Move on only when the user explicitly says the skeleton is settled. Record the locked image as the skeleton baseline (e.g. `A3.png`).

When the user says it "feels right but can't say why", first find which axiom the comfort comes from, protect it, then change other things.

## Stage 3.5: SVG redraw

Read `references/svg_redraw.md` first.

1. Ask the user: "Shall I redraw this skeleton as a precise SVG? Coloring can then use exact color values and the shape will not change." If they only want a quick look, skip this and color with the image model in stage 4.
2. Write the SVG by the drawing conventions: a 1024 canvas, layer ids fixed as `bg` / `skeleton` / `focus`, an opening comment stating the module w, corner radii and other base values, corners drawn by the G² rule (no plain circular-arc corners), boolean subtraction with `mask` and intersection with `clipPath`.
3. Render it and compare with the original:
   ```bash
   python scripts/render_svg.py output/A3.svg --source output/A3.png \
     --name A3-svg --direction "A3 · SVG redraw" --rationale "<module and corrections>"
   ```
   Open `A3-svg-compare.png` and read the overlay: red = only in the original, cyan = only in the SVG. Correct in the order "position → proportion → detail", usually 2–3 rounds.
4. Run `make_preview.py` on the rendered image to check small sizes.
5. Put the original and the redraw on the review page and explain which irregularities you corrected. Once the user confirms, this SVG is the final skeleton.

## Stage 4: Color and deliver

Read `references/color_dressing.md` first.

Once the user gives color values, do all the following steps in one go instead of asking one question at a time. Ask first only if the role assignment is ambiguous.

1. **Collect colors**: 2–4 color values. Colors already given in stage 1 are used first; if they do not work, adjust them in this step. If the user has no colors, recommend 2–3 sets based on the product screenshots, each with its reasoning, and let the user choose.
2. **Color diagnosis**:
   ```bash
   python scripts/color_check.py "#211811" "#FFF5EF" "#FF7622"
   ```
   Organize the result into a diagnosis table: what each color is good for, which ones cannot be used for thin lines, which ones melt into the desktop, which ones can carry a gradient.
3. **Role assignment**: Canvas (base) / Structure (skeleton) / Accent (focus). The skeleton decides the number of colors: if it is a single overall shape, default to 2 colors (canvas + structure); add an accent color only if the skeleton has parts that are genuinely independent. If the skeleton brings its own container (a solid square with negative space), that container is the icon base; do not wrap another layer around it, to avoid a box inside a box.
4. **Scheme images**: A soft and light (light background), B deep and focused (dark background, reversed), C high-energy and striking (bright background). Produce only the schemes the colors can support: A/B need one dark and one light color; C needs a highly saturated color with at least 3:1 contrast against the skeleton color. If the user wants a gradient, follow the gradient rules.
   - **With an SVG (recommended)**: one `render_svg.py --colors` command per scheme, no API call, the shape does not change. Claude writes the `<linearGradient>` in the SVG for gradients.
   - **Without an SVG**: use the image model with the locked skeleton image as `--ref`, and state explicitly in the prompt "the shape stays exactly the same, only the colors change". The model may quietly alter the shape, so check against the skeleton image.
5. **Checks**: the four rules that protect the skeleton, plus the engineering checklist (contrast, text overlay, inner stroke on light backgrounds, dark mode, minimum-size fallback).
6. **Container preview**: run `make_preview.py` for each scheme.
7. **Review page**: put the diagnosis, the schemes and the previews on one page so the user can pick the main version.
8. **Showcase image (optional)**: if the user wants a promotional image, hand the finished PNG to the image model as a reference (section 4 of `prompt_templates.md`). The logo itself stays flat.
9. **Deliver**: monochrome SVG, color SVGs and PNGs for each scheme (main version, plus B as the dark-mode and reversed version), the previews and the final review page; tell the user where the files are.

---

## Communication principles

- The user's descriptions are often feelings (too hard, too soft, not modern, dirty). Translate them into concrete axiom problems before acting.
- In each round, say what stays before saying what changes.
- When you are unsure of a direction, ask the user with 2–3 concrete options instead of guessing repeatedly.
- Say how many images you will generate before each generation, and do not generate too many at once.
- Say "generated" only after a script has actually run successfully.

## Scripts

| Script | Purpose | Calls an API |
|---|---|---|
| `scripts/check_env.py` | Check the environment and keys (`--all` shows all three providers) | Validation only, no images |
| `scripts/generate_image.py` | Generate images; records prompts and rationale in a sibling `.json` | Yes |
| `scripts/build_review.py` | Build the review page: images + rationale + prompts | No |
| `scripts/render_svg.py` | Render an SVG, compare with the original, color by layer | No |
| `scripts/color_check.py` | Color diagnosis: lightness, chroma, warmth, contrast, gradient feasibility | No |
| `scripts/make_preview.py` | App-icon container preview (light / dark / multiple sizes) | No |

Common `generate_image.py` options: `--provider` to switch model for one run, `--ref` for reference images (repeatable), `--aspect` for aspect ratio, `--n` for the number of images, `--dry-run` to inspect the request without calling the API.
