# Prompt Templates

The English prompt is what gets sent to the model. A translation into the user's language is optional and used only for display on the review page (`--prompt-zh` / `--prompt-zh-file`); keep its content identical to the English prompt.

## Writing principles

How each axiom translates into a prompt is described in the "Prompt" part of each section of `skeleton_axioms.md`. This file holds only the writing principles and the full templates.

- **Describe visible shapes; do not pile up adjectives.** "Two equal-width rounded bands interlocking with 180° symmetry around the center to form an S" is far more useful than "a premium, modern, tense S".
- **Write the result of a boolean operation, not the jargon.** Write `cut out as negative space` or `formed by the overlap of two circles`, not `boolean geometry`.
- **Write curvature in a form the model can execute.** Write `continuous-curvature corners like a squircle, no visible joint`, not `G2`.
- **Block negative words on both sides.** If you block only one side, the model drifts to the other (axiom three).
- **Avoid words that trigger an illustration style**: botanical, delicate, organic lines, anatomical, realistic, detailed.
- **Do not write bold / thick / heavy, and do not write thin / slender / hairline.** They push the result to one end of the pendulum. Use `balanced medium stroke weight`.
- **Describe one structure at a time.** Conflicting requests (closed and open at once) make the model draw randomly.
- **Use no color names in the skeleton stage**, only "near-black + pure white / off-white". If the user gave colors upfront, you may replace `#1A1A1A` and `#F7F7F5` in the templates below with the user's color values; if the result is poor, go back to the defaults.

---

## 1. Skeleton template (stages 2 and 3)

```
Minimal modern brand mark: <object and structure, described as visible shapes>.
Construction: built from circles, rounded rectangles and capsules that are merged, cut and overlapped, <result of the boolean operation, e.g. the counter cut out as negative space>; uniform stroke width throughout, balanced medium stroke weight; parallel strokes from concentric curves; smooth continuous-curvature corners like a squircle, no visible joint between straight and curved segments; taut arcs with tension; visually centered and balanced; <closed form or symmetry type>.
Single flat color: near-black #1A1A1A on plain off-white #F7F7F5 background. Centered with generous margin. Highly legible at 16 pixels.
No text, no illustration, no realistic objects, no decorative add-ons, no floating detached elements, no calligraphic brush strokes, no hairline strokes, no chunky heavy blocks, no inflated plastic 3D, no bevel, no gradients, no shadows, no glow, no texture, no extra strokes. Flat vector logo, crisp edges.
```

### Examples (the structure part)

- Closed letter mark: `an upright vertical stem with a smooth arc that rises over the inner shape and loops back down to rejoin the stem near two-thirds height, forming a fully closed counter`
- Central symmetry: `two identical rounded bands interlocking with 180-degree point symmetry around the center`
- Negative space: `a solid rounded-square tile with the letter cut out of it as negative space`
- Concentric loop: `two concentric arcs nested inside the bowl of the letter, same stroke width, evenly spaced`

---

## 2. Skeleton refinement template (stage 3, with a reference image)

```
Keep the reference mark exactly as it is: same overall silhouette, same proportions, same stroke width, same position. Only change: <one change only>.
Single flat color: near-black #1A1A1A on plain off-white #F7F7F5. No gradients, no shadows, no 3D, no glow, no texture. Flat vector logo, crisp edges.
```

Add `--ref output/<previous version>.png` when calling the script.

---

## 3. Coloring templates (stage 4, with a reference image)

### Solid / two-color
```
Recolor the reference mark only. Keep the shape exactly identical: same silhouette, proportions, stroke width, gaps and position. Do not add, remove or reshape anything.
Colors: <part A> in <color name> (<value>); <part B> in <color name> (<value>); background <color name> (<value>).
Solid flat fills with hard edges between colors. No other colors, no gradients, no shadows, no 3D, no glow, no texture.
```

### Gradient
```
Recolor the reference mark only. Keep the shape exactly identical. <part> uses a smooth gradient from <color 1> (<value>) to <color 2> (<value>), running <direction, e.g. from bottom to top>, staying within the same hue family with no grey, brown or muddy midtones and no shift toward yellow. <other parts> in solid <color> (<value>). Background <color> (<value>). No other colors, no shadows, no 3D, no glow, no texture.
```

---

## 4. Showcase template (optional)

Use only when the user wants a promotional image. The logo itself stays perfectly flat; any lighting belongs to the background only.

```
Place the reference mark, unchanged and perfectly flat, at the center of <scene, e.g. a softly lit off-white studio surface with a subtle warm ambient glow behind it>. Keep the mark's shape and colors exactly identical. Generous empty space. No text.
```

---

## 5. Negative words

The full two-sided negative word list and how to use it are in section 3 of `skeleton_axioms.md` (axiom three). In short:

- In the first round, block both sides.
- In each later round, add more specific words against the side the previous round fell to, and keep the other side, so the fix does not overcorrect.
- For letter marks, add `no letters other than <letter>`.
