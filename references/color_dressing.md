# Coloring: Dressing a Locked Skeleton in Color

Color is a finishing layer on the skeleton. The user decides the colors; this document covers two things:

- **The engineering of color itself**: what each color can do, and on which backgrounds it runs into trouble.
- **The relation between color and skeleton**: how to color without damaging the skeleton.

Precondition: the skeleton is locked and its monochrome version holds up.

Once the user gives color values, do not proceed one question at a time. Do everything in this order: diagnosis → role assignment → scheme images → a review page for the user to choose. Ask first only if the assignment is ambiguous.

## Contents

1. Input and color diagnosis
2. Role assignment
3. Three schemes × coloring methods
4. Checks
5. Common failures
6. Container preview and delivery

---

## 1. Input and color diagnosis

### Input

- **2–4 color values** (e.g. `#211811`, `#FFF5EF`, `#FF7622`). If there are only descriptions ("deep purple", "warm orange"), give 2–3 candidate values for the user to choose from.
- **Coloring-method preference** (optional): solid, two-color, gradient. If not stated, use the defaults in section 3.
- **Product positioning** (optional): if not given, consider all scenarios.

If the user has no colors:

- If there are product screenshots, take colors from the interface: primary, accent, background.
- Recommend 2–3 sets, each with a clear reason, and let the user choose.
- Avoid colliding with the signature color of a well-known brand (for example Slack's deep purple #4A154B).

### Diagnosis

```bash
python scripts/color_check.py "#211811" "#FFF5EF" "#FF7622"
```

The script outputs each color's lightness, chroma, hue and warmth, its contrast against light and dark desktops, the pairwise contrast, and the hue spacing. Organize the result into a diagnosis table for the user, focusing on the **engineering defects**:

| Question to answer | What to look at |
|---|---|
| Which color suits a large base | Colors with high or low lightness and low chroma; a high-chroma color over a large area feels restless |
| Which color can be the skeleton | At least 3:1 contrast with the base; the pair with the greatest light/dark difference |
| Which color can only be the accent | High-chroma, mid-lightness colors; contrast with light colors is often insufficient |
| Which color cannot be a thin-line foreground | Contrast below 3:1 against the color it sits on |
| Which color "melts" on the desktop | Contrast below 1.5 against a light or dark desktop, so the edge is unclear when used as the base |
| Which two colors can make a gradient | Hue difference ≤ 30°; near-complementary colors cannot |
| Is there pure black | Replace pure black #000000 with a dark color that has a hue (such as warm dark coffee-black #17120C) |

---

## 2. Role assignment

| Role | Function | Usual color | Area |
|---|---|---|---|
| **Canvas** (base) | Carries the large area and decides the first impression. The square base color of the app icon | Very light or very dark, low chroma | Largest |
| **Structure** (skeleton) | Main structure, outer contour, closed loop; secures recognizability at tiny sizes | The color with the greatest contrast against the base | Medium |
| **Accent** (focus) | The first point the eye lands on; controls the flow of the gaze | The brand accent color, high saturation | Small, about 10% |

### The number of colors is decided by the skeleton, not fixed at three

Three roles is a ceiling, not a requirement. First count how many parts of the skeleton can be colored independently, then decide how many colors to use:

| Skeleton | Colors | Assignment |
|---|---|---|
| Only one overall shape (most letter marks and negative-space marks) | **2 colors (default)** | Canvas + structure |
| One genuinely independent part (such as the sprout core inside the counter of a P) | 3 colors | Canvas + structure + accent |
| Needs to be minimal and authoritative, or used for stamps and one-color printing | 1 color | One color for the skeleton, base transparent or following the environment |

If the user gave 3 colors but the skeleton has only one overall shape, **do not force in a third color**. Use the extra color in a different scheme (for example, the bright color is the base only in scheme C), rather than stacking a new layer in the same icon.

### Do not duplicate the symbol and the container

An app icon already has a rounded-square container (the system squircle). If the skeleton **is itself a "solid container + negative space"** (for example an S cut out of a rounded square), then when making the app icon:

- **The container is the base of the icon.** The negative-space shape is cut out of the base, or drawn directly on it.
- **Do not** put a skeleton-colored square on top of the base color. That gives a "box inside a box": a layer of base outside and a layer of skeleton square inside, two containers fighting over which is primary, and the shape itself gets smaller.

Only when the skeleton is an open shape without its own container (such as a P or a starburst) is the base a separate layer outside the skeleton.

How to judge: remove the base color. Does the skeleton still contain an outer frame similar in shape to the icon container? If so, the symbol and the container are duplicated.

### Roles must correspond to the structure of the skeleton

Do not color casually:

- Only a part that is already an **independent boolean part** in the skeleton can have its own accent color. For example, the sprout core can be orange because it is an independent shape; if it is the same stroke as the shell, forcing two colors would cut one stroke into two segments.
- Keep the accent area small rather than large. If the accent color fills the outer ring, the primary/secondary order is disturbed.
- A color with no job is a stray color; delete it.

With an SVG, roles map directly to layers: Canvas = `bg`, Structure = `skeleton`, Accent = `focus`.

---

## 3. Three schemes × coloring methods

### Three schemes (who is the base, who is primary)

| Scheme | Base | Skeleton | Accent | Character | Suited to |
|---|---|---|---|---|---|
| **A Soft and light** | Light | Dark | Bright color as a finishing touch | Paper feel, quiet, humanistic | Default version for reading, learning and tool apps |
| **B Deep and focused** | Dark | Light, reversed | Bright color as the visual center | Premium, immersive | Dark mode, night scenes, premium positioning |
| **C High-energy and striking** | Highly saturated bright color | Dark or light | Light/dark contrast to hold down restlessness | Strong brand penetration | App stores, marketing, needing to be recognized at a glance |

- Produce **only the schemes the colors can support**, and put them on the same review page for comparison:
  - A and B are a light/dark swap of each other. Whenever there is one dark and one light color, both can be produced. B is also the reversed version.
  - C needs a highly saturated color with at least 3:1 contrast against the skeleton color. If there is no such color, do not produce C.
  - In a 2-color plan, C is "high-chroma color as the base + dark or light color as the skeleton", with no extra third layer.
- The accent color in B is a "visual center", not a light source. The logo itself stays flat, with no glow.
- C uses a high-chroma color as the base, and there must be a clear light/dark difference between the skeleton and the accent; if the diagnosis shows the bright color has insufficient contrast with light colors, use a dark skeleton for C.

### Coloring methods (how the color goes onto the skeleton)

Within each scheme, choose one coloring method:

- **Solid**: the skeleton and accent share one color, the whole logo is one color. The most stable.
- **Two-color layers**: one color for the skeleton, one for the accent, with hard edges between the blocks. The most common, and the default.
- **Gradient**: only between close colors.
  - A light/dark change within one hue (dark orange → orange), or between adjacent hues (within about 30°).
  - Do not stretch a gradient between deep cool grey or pure black and a vivid warm color; the middle goes grey and burnt.
  - Do not cross complementary colors (orange → blue); a grey dead zone appears in the middle.
  - The gradient direction follows the momentum of the skeleton (for growth, brighter from bottom to top).
  - Use a dark color with a hue for the dark end, not pure black.

### How to produce the images

- **With an SVG (recommended)**: one command per scheme, with exact colors and an unchanged shape:
  ```bash
  # 3 colors (when the skeleton has an independent accent part)
  python scripts/render_svg.py output/A3.svg --name A3-A --stage color \
    --direction "Scheme A · soft and light" --colors "bg=#FFF5EF,skeleton=#211811,focus=#FF7622"
  # 2 colors (when the skeleton has only one overall shape; omit focus)
  python scripts/render_svg.py output/A3.svg --name A3-C --stage color \
    --direction "Scheme C · high-energy" --colors "bg=#FF7622,skeleton=#211811"
  ```
  If the skeleton brings its own container, first turn the container into a full-canvas `bg` following `svg_redraw.md`, then color.
  For gradients, Claude writes the `<linearGradient>` directly in the SVG, then renders with `render_svg.py`.
- **Without an SVG**: use the image model with the locked skeleton image as `--ref` (section 3 of `prompt_templates.md`). The model may quietly alter the shape, so check against the skeleton image.

---

## 4. Checks

### Four rules that protect the skeleton

1. **Is the skeleton still intact?** Does the outer contour look broken because some segment is too light? Did the model change the shape?
2. **Did the colors follow the structure?** Is any single stroke cut into two colors? Was the accent stolen by another color?
3. **Is the gradient clean?** Any grey, dirty or burnt middle section? Any drift toward yellow away from the brand color?
4. **Does the monochrome version still hold?** The color version is a bonus; it cannot replace the monochrome version.

### Engineering checklist

| Item | Requirement |
|---|---|
| **Contrast** | Skeleton against base ≥ 3:1; parts that contain text ≥ 4.5:1. Verify with the pairwise contrast from `color_check.py` |
| **Text overlay** | Do not place text on combinations below 4.5:1; combinations below 3:1 cannot be foreground and background of each other, only placed adjacent |
| **Edge of a light base** | If the diagnosis shows the base "melts" on a light desktop, add an inner stroke: skeleton color, about 8–12% opacity, about 1/256 of the icon edge in width (about 4px on a 1024 canvas); or use scheme B in that context |
| **Dark mode** | The light base of scheme A is glaring on a dark desktop; use scheme B for dark mode. Newer iOS supports separate dark and tinted icons; tinted icons are converted to greyscale and re-tinted by the system, so the monochrome skeleton must hold up |
| **Minimum-size fallback** | At 16–24px (notifications, settings lists, browser tabs): turn gradients into solid color; remove details and cuts thinner than 2px; if the accent part is so small it vanishes, consider merging it into the skeleton color. Check 16 / 32px with `make_preview.py` |

---

## 5. Common failures

| Symptom | Cause | Fix |
|---|---|---|
| Box inside a box | The skeleton brings its own container (solid square + negative space) and a layer of base color was added outside | Use the skeleton's container directly as the icon base; cut the negative space out of the base |
| Many colors but a messy hierarchy | A layer with no structural basis was forced in to use all 3 colors | Decide the number of colors by the number of independent parts of the skeleton; default to 2 |
| The outer ring looks broken | The outer contour used a light color close to the base | Give the outer contour to the skeleton color; place the light color only on the inside |
| The icon melts into the desktop | Insufficient contrast between base and desktop | An inner stroke, or change scheme |
| Looks like modeling clay or a plaster | An opaque light pink + 3D bevel | Remove the 3D effects; turn the light color into negative space |
| Burnt, like charcoal | A long gradient between a dark color and a vivid color | A dark color with a hue at the dark end, and a shorter gradient |
| Yellowish, like a flame | The highlights drift toward yellow and gold | Brighten within the brand hue only, and state "no shift toward yellow" in the prompt |
| Too hard, like a cage | Too much dark area, the accent isolated | Hard outside, soft inside: dark outer contour, a little yielding on the inside |
| Too soft to be a logo | A light color occupies the outer contour | Give the outer contour back to the skeleton color |
| Restless, glaring | A high-chroma color used as a large base without being held down | In scheme C hold it down with a dark skeleton; or use scheme A/B |
| Impactful but not restrained | The accent area is too large | Pull the accent back to about 10% |
| Like neon or esports | Glow or highlights were added | Keep the logo itself flat; lighting belongs to the display environment |
| Gaudy, like a rainbow | Colors beyond those the user gave were added | Return to the colors the user gave |

---

## 6. Container preview and delivery

Run this on the final image of each scheme:

```bash
python scripts/make_preview.py output/A3-A.png
python scripts/make_preview.py output/A3-B.png
python scripts/make_preview.py output/A3-C.png
```

It generates the app-icon appearance on light and dark desktops, and at 180 / 64 / 32 / 16px. It does not call an API.

Then use `build_review.py` to put the diagnosis, the schemes and the previews on one review page for the user to pick the main version. On delivery, keep every scheme that was produced: the one the user picks is the main version, and B serves as the dark-mode and reversed version.

Effects like glow, frosting and frosted glass belong to the **display environment** (the app-icon container, promotional pages) and are not drawn into the logo itself. When the user needs a showcase image, generate one separately, but the delivered logo itself stays flat.
