# SVG Redraw: Turning the Locked Skeleton into Precise Vector

Image models output bitmaps, in which stroke width, corner radius and symmetry are only "roughly right". Once the skeleton is locked, Claude redraws it as SVG by the skeleton axioms:

- Stroke width, corner radius and clearance are truly unified to one module.
- Arcs come from true concentric circles, and symmetry is true symmetry.
- It scales without limit and can be handed straight to developers and designers.
- Coloring fills exact color values by layer, no longer relying on the model to "guess colors", and the model cannot change the shape.

A redraw does not trace every pixel of the original. The irregularities in the original (strokes that vary in width, inconsistent corner radii) are exactly what should be corrected.

## Contents

1. When to do it
2. Drawing conventions
3. Redraw steps
4. Comparison and iteration
5. Coloring by layer
6. Example

---

## 1. When to do it

After stage 3 ends and the user says "the skeleton is settled", before coloring (stage 3.5).

Ask first: "Shall I redraw this skeleton as a precise SVG? Coloring will then use exact color values and the shape will not change." If the user only wants a single image to look at, skip it and color with the image model.

---

## 2. Drawing conventions

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
  <!-- module w = 74; corner radius R = 60; ... (state every base value in the comment) -->
  <rect id="bg" width="1024" height="1024" fill="#F7F7F5"/>
  <g id="skeleton" fill="#1A1A1A"> … main structure, outer contour … </g>
  <g id="focus" fill="#1A1A1A"> … parts that need their own color (omit if none) … </g>
</svg>
```

- **Canvas**: `viewBox="0 0 1024 1024"`, the mark centered with a 20%–25% margin around it.
- **Fixed layer ids**: `bg`, `skeleton`, `focus`. The coloring script fills colors by these three ids. In the monochrome version, all layers use `#1A1A1A`.
- **`bg` is the app-icon container** and is always a full-canvas square (the system crops it to a squircle). If the skeleton itself is "solid container + negative space" (for example an S cut out of a rounded square), do not draw another square on `bg`: use `bg` directly as the container, draw the negative-space shape in `skeleton`, and scale the S to a size that suits an icon. Otherwise a box inside a box appears after coloring.
- **Write the module in a comment**: at the start of the SVG, state w, the corner radius and the key clearances; every coordinate is derived from them.
- **Use only shapes with a lineage**: `circle`, straight segments `H` `V` `L` in a `path`, circular arcs `A` (for concentric arcs and full-circle segments), and G² corners `C` built by the rule below. Do not draw free Béziers dragged out by feel.
- **Corners must be curvature-continuous (G²)**: a straight line meeting a circular arc is only G¹, so the corner has a "joint" and looks like a mechanical dead circle. The `rx` of a `rect` is also this kind of circular-arc corner, so draw squares with rounded corners using a `path` as well. How to draw a G² corner:
  - Replace the circular arc of radius R with a single cubic Bézier `C`.
  - Place the start and end points on the two edges, about **2.3R** from the corner point.
  - **Put both control points on the corner point.**

  This makes the curvature 0 at both ends of the corner, so it meets the straight lines seamlessly; the position of the deepest point of the corner is the same as for an arc of radius R. For a softer corner, increase 2.3R.

  Example: going from the top edge `(x1, y)` to the right edge, with the corner point at `(xc, y)` and R = 40: `H xc-92 C xc y, xc y, xc y+92`.
- **Boolean operations**:
  - Add (union): put several shapes in the same `<g>`.
  - Subtract (difference / negative space): use a `<mask>`; white is kept, black is cut away.
  - Intersect: use a `<clipPath>` to clip one shape to another (for example two circles intersecting to give a leaf).
  - Closed rings: use a compound path with `fill-rule="evenodd"` (outer contour + inner contour).
- **Lines**: you may use `stroke` to draw equal-width channels with width = w. Corners follow the G² rule above; no sharp corners.
- **Round coordinates**: prefer integers, or integer multiples of the module.
- **Do not write**: filters, shadows, gradients (in the monochrome stage), text, external images.

---

## 3. Redraw steps

1. **Read the original**: understand the structure and estimate the key dimensions (position and size of the outer frame, stroke width, corner radius, position of each segment). The original may be a thumbnail, so convert coordinates to the 1024 canvas.
2. **Fix the module**: choose a w so that the main dimensions are multiples or simple fractions of w.
3. **Write the SVG**: follow the conventions, and state the base values in the comment.
4. **Render and compare** (see section 4).
5. **Iterate**: fix one class of problem per round (position → proportion → detail), usually 2–3 rounds.
6. **Check small sizes**: run `make_preview.py` on the rendered PNG.
7. **Show the user**: put the redraw next to the original on the review page and explain which irregularities you corrected.

---

## 4. Comparison and iteration

```bash
python scripts/render_svg.py output/A3.svg --source output/A3.png \
  --name A3-svg --direction "A3 · SVG redraw" --rationale "module w=74, uniform corner radius 50"
```

This produces three things:

- `A3-svg.png`: the rendered image
- `A3-svg-compare.png`: original / redraw / overlay, side by side. In the overlay, **red = only in the original, cyan = only in the SVG**, grey-black = coincident
- `A3-svg.json`: the record used by the review page

Always open the comparison image and look at it. Common cases:

- Large patches of red or cyan, shifted → the overall position or proportion is wrong (for example, the height of the title bar of the comparison image was included in the coordinates).
- Only a thin ring of red or cyan along the edges → the position is right and only stroke width or corner radius is off.
- The differences concentrate where the original was irregular → this is the correction a redraw should make; do not chase it.

The script prints a "contour difference ratio", for reference only: once it drops below 5%, the structure usually matches.

---

## 5. Coloring by layer

Once the skeleton SVG is settled, stage 4 colors the SVG first: the colors are exact, the shape does not change, and no API quota is used:

```bash
python scripts/render_svg.py output/A3.svg --name A3-c1 --stage color \
  --direction "A3 · two-color" --colors "skeleton=#17120C,focus=#FF7622,bg=#FAF7F2"
```

- It outputs the colored `A3-c1.svg` and `A3-c1.png`.
- Write colors as `layer=#RRGGBB`, separated by commas. A layer that is not in the SVG is reported.
- **Gradients**: the script handles only solid colors. For a gradient, Claude writes the `<linearGradient>` directly in the SVG, chooses colors and direction by the rules in `color_dressing.md`, and renders with `render_svg.py` (without `--colors`).
- To get a showcase image with lighting and material, hand the rendered PNG to the image model as a reference image (section 4 of `prompt_templates.md`).

---

## 6. Example

`assets/example_svg_s_office.svg`: an S cut out of a rounded square with negative space. It demonstrates layer ids, the module comment and boolean subtraction with `mask`. Note that this example's corners are still circular arcs (G¹); it serves only as a reference for how the structure is written. In an actual redraw, draw corners by the G² rule in section 2.
