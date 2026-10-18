# Skeleton Axioms

The skeleton is the logo itself. This document is the core of the whole skill: it translates the user's emotional, concrete brand needs into a skeleton with **formal inevitability, mathematical order and OS-grade precision**.

The same axioms are used in two ways:

- **Build** (stage 2): derive directions and write prompts.
- **Read** (stage 3): diagnose generated images. Diagnosis is the axioms used in reverse, to see which one was violated.

Each axiom is written in four parts: **definition → how to translate it into a prompt → what a violation looks like → negative words**.

## Contents

1. Axiom one: formal inevitability
2. Axiom two: mathematical order
3. Axiom three: negative defense (block both sides)
4. Closed or open
5. Applying by mark type
6. Diagnosis order
7. Reference samples

---

## 1. Axiom one: formal inevitability

### Definition

- Reject appliqué design: do not hang small decorations outside the main body (a leaf beside a letter, little wings next to a word).
- Do not trace the object itself; extract only its **momentum** in space. The imagery should become a growth momentum that turns directly into the main skeleton and the counter outline: **the edge of the imagery is the contour of the main body**.
- One stroke more is redundancy; one stroke less is collapse. Delete any part that can be removed without affecting the whole.

### Imagery reduction

Translate the product concept into a momentum, then into a structure:

| Concept | Momentum | Common structure |
|---|---|---|
| Growth, sprouting | A single curvature rising from below | An arc rising from the base of the stem, parallel to the inner wall of the shell |
| Thinking, cognition | Concentric, looping, resonating | Concentric arcs, nested rings |
| Connection, collaboration | Tangent, interwoven, interlocking | Two identical units interlocking with central symmetry |
| Speed, efficiency | Open, projecting, accelerating | A symmetric open arc, a wedge |
| Shelter, companionship, immersion | Embracing, containing | A closed outer ring wrapping an inner core |
| Opening, reading | Symmetric unfolding | Two leaves symmetric about a central axis |
| Work, interface | Grid, window, layering | A rounded square with negative-space cuts |

The same concept can have many structures. When deriving directions, make the 3–4 directions genuinely different in structure.

### How to say it in the prompt

- Describe imagery only as geometric shapes: `a rising lens-shaped leaf formed by two intersecting arcs`, not `a sprout with leaves`.
- State the relation between the imagery and the main body explicitly: `the loop of the letter IS the leaf shape`, `the motif forms the counter of the letter`, not `with a leaf next to the letter`.

### What a violation looks like

| It looks like | Cause |
|---|---|
| The sign of a corner café, an essential-oil workshop or an arty flower shop | Concrete details such as branches, veins and twigs were drawn |
| A letter with a small icon stuck on | The imagery hangs beside the main body and has not grown into the structure |
| A floating candle flame | A part has detached from the body and hangs outside it |
| A stray bar or small hook | A stroke that is not inevitable |

### Negative words

```
no illustration, no realistic leaves, no tree branches, no veins, no botanical details,
no decorative add-ons, no floating detached elements, no flame or smoke wisps
```

---

## 2. Axiom two: mathematical order

### 2.1 Modular stroke width

**Definition**: the stems, arcs, chamfers and clearances of the whole mark share one base module w and its fixed multiples (0.5w, 2w). Casual variation in thickness is forbidden.

**Take the middle weight**:

- The standard is that **the outline is still recognizable at 16px**, not that heavier is better.
- Going heavy produces clumsy blocks of color; going thin produces calligraphic incense-stick lines. The answer is in the middle: **medium weight, a closed outline, with a deliberate rhythm of thick and thin**.
- When you need a cut, the cut width is also a multiple of the module; a hairline gap disappears at 16px.

**Prompt**: `uniform stroke width throughout, balanced medium stroke weight`. Do not write `bold`, `thick` or `heavy`, and do not write `thin`, `delicate` or `hairline`; they push the result to the two extremes.

**What a violation looks like**:

| It looks like | Cause |
|---|---|
| Hand-drawn, messy | Stroke width varies from place to place |
| A bulldozer, a heavy sports-streetwear brand | Too heavy; becomes a solid block of color |
| Incense sticks, brush calligraphy, a spa or yoga studio | Too thin; a single line wanders with no structural support |
| Blurs into a lump when shrunk | Relies on thin gaps or fine detail |

### 2.2 Boolean construction

**Definition**: shapes are not traced by feel with a pen; they are cut out of basic forms by **adding, subtracting and intersecting**.

**Basic forms**: circle, rounded rectangle, capsule, squircle. Common derived forms:

- Leaf, lens = the **intersection** of two circles
- Crescent = one circle **minus** another offset circle
- Counter, window = a solid form **minus** an inner shape (negative space)

**What the three operations do**:

| Operation | Effect | Example |
|---|---|---|
| Union | Fuses parts into one whole, or interlocks two units | A stem and a counter arc fused into one |
| Subtraction | Cuts shapes, hollows out counters and makes slits with negative space | An S cut out of a rounded square |
| Intersection | Gives forms pointed at both ends and full in the middle, like leaves and lenses | A sprout |

Boolean operations leave checkable traces: shared edges, consistent radii, circle centers that can be traced back.

**Prompt**: describe the result of the operation, do not write `boolean`:

- `a solid rounded-square tile with the letter cut out of it as negative space`
- `a lens shape formed by the overlap of two equal circles`
- `two identical shapes merged into one continuous form`

**What a violation looks like**: edges that drift, as if traced casually with a pen; parts that share no edges, like a collage.

### 2.3 Continuous curvature

**Definition**:

- Arcs need tension, like a fully drawn bowstring or an industrial fluid section; a soft arc that caves inward looks deflated.
- Parallel strokes come from concentric circles (outer circle R, inner circle R−w).
- **A line meeting an arc must be curvature-continuous (G²), not merely tangent (G¹).** A straight line joined to a standard circular arc is only G¹: the curvature jumps from 0 to 1/R at the tangent point, which reads as a "mechanical dead circle" with a perceptible "joint" at the corner. A G² join lets the curvature change gradually, which is the smoothness of Apple's squircle corner.
- Avoid both ends: the mechanical dead circle, and loose hand-drawn curves.

**Prompt**: image models do not understand G², so write it in a form they can execute:

`smooth continuous-curvature corners like a squircle, no visible joint between straight and curved segments, taut arcs with tension`

**What a violation looks like**:

| It looks like | Cause |
|---|---|
| Soft, deflated | Arcs collapse and circle centers are scattered |
| Stiff, mechanical, like a CAD sketch | A straight line joins a circular arc directly and the corner has a joint |
| Sluggish, hand-drawn | No traceable curves; bent casually |

How to build G² corners when redrawing as SVG is in section 2 of `svg_redraw.md`.

### 2.4 Center of mass and moment balance

**Definition**:

- The visual center of mass sits at the geometric center: it does not lean right and does not hang weightless.
- Positive and negative space are balanced in area.
- For radial or rotational marks, choose the symmetry first (2-fold like FENDI, 3-fold like Chrome, 4-fold like Givenchy, 6-fold like OpenAI), then design the unit.

**Prompt**: `visually centered and balanced, even distribution of positive and negative space`; for symmetric marks, state `with 3-fold rotational symmetry around the center`.

**What a violation looks like**: it seems about to tip or slide to one side; one side is heavy and the other empty.

### 2.5 Momentum in phase

**Definition**: the edges of inner parts run parallel to the inner wall of the shell at an equal distance, with a uniform angle, so the eye travels in one stroke and is not cut off by branching.

**Prompt**: `the inner shape runs parallel to the inner wall at an equal distance, one continuous flowing movement, no branching`.

**What a violation looks like**: the structure is cut into several segments; the eye stops halfway.

---

## 3. Axiom three: negative defense (block both sides)

Negative words work better than adjectives. But **if you block only one side, the model runs to the other**: block thin lines and it gives you clumsy black blocks; block black blocks and it returns to brush lines. So always block both sides together.

| One side: too concrete, too light | The other side: too heavy, too plastic |
|---|---|
| `no illustration, no realistic leaves, no tree branches` | `no chunky heavy blocks, no solid heavy silhouettes` |
| `no calligraphic brush strokes, no ink wash` | `no inflated plastic 3D, no bevel, no glossy rendering` |
| `no hairline strokes, no thin wispy lines` | `no thick clumsy outlines` |
| `no flame, no smoke, no floating wisps` | `no shadows, no glow, no neon` |

Always include:

```
no text, no gradients, no texture, no noise, no extra strokes
```

Color-cast problems (yellowish, gold-tinted) belong to the coloring stage; see `color_dressing.md`. The skeleton stage uses only near-black and off-white, so they do not appear.

**Usage**:

- Round one: include the general negative words for both sides to frame the range.
- Every later round: add more specific negative words against the side the previous round fell to, and keep the negative words of the other side, so the fix does not overcorrect.

---

## 4. Closed or open

There is no absolute ban, but there is an order of judgment: **the topology and mechanics of the shape itself > the brand metaphor > style**. Style decides only "how to open"; it cannot turn a shape that should be closed into an open one.

### Step one: can the shape be open?

| Shape | Can it be open? | Reason |
|---|---|---|
| Letters with a closed counter: O P B D Q A R | Mostly closed | The closed counter is the core feature by which they are recognized. Cut the loop of a P open and it reads as a question mark; open an O and it becomes a C |
| One-sided asymmetric structures | Mostly closed | Without closure it is a cantilever and looks about to fall; closure sends the force back to the stem so it stands stable |
| Axis- or centrally symmetric structures: bell shapes, starbursts, Λ, X, S | Suited to open | Symmetry lets the two sides cancel and pins the center of mass at the center |
| Letters that are open already: C S E F L V | Suited to open | Extend along the existing opening |

**Rule: if it is asymmetric, close it; if it is open, it must be highly symmetric.**

### Step two: should the brand metaphor be open?

| | Closed | Open |
|---|---|---|
| Energy | Cohesive, gestating, protective | Projecting, radiating, outputting |
| Metaphor | Womb, greenhouse, shelter, immersion, safety | Engine, light source, signal, connection, burst |
| Samples | Notion, Apple | Raycast (symmetric bell shape), Claude (centrally symmetric starburst) |

### Additions

- **Two-level closure**: the inner symbol can be open, and the squircle container of the app icon provides the second level of closure.
- **Closure should also feel natural**: curl back and join along the existing momentum; do not force a standard semicircle onto a vertical line.
- **Openness must survive shrinking**: the opening must be large enough; an opening expressed by a thin gap gets smoothed away at 16px.

Case: Poplex once made the loop of its P open, and everyone found it "odd". The P originally has a closed counter and is one-sided asymmetric, so opening it triggered two reactions at once: "can't recognize the letter" and "about to fall". After it was changed back to closed, curling back to the stem along the originally comfortable flow, the problem was solved.

---

## 5. Applying by mark type

| Type | Focus | Common failure |
|---|---|---|
| Letter mark | The letter is readable at first glance; letters with counters are closed; the imagery grows inside the counter or strokes | Read as another symbol; the imagery stuck outside the letter |
| Pure symbol / abstract form | Choose the symmetry and unit first, then array; open structures stand on symmetry | Casual curves; asymmetric and open, so it looks about to fall |
| Wordmark (the whole name) | Uniform strokes; letter spacing even by negative-space area, not physical distance; a focal point on only one letter | Flourishes on every letter |
| Combination mark (symbol + text) | The symbol and the text share stroke width and corner radius | Two geometric languages talking past each other |
| App icon | Check at 16 / 32 / 180px, on light and dark | Reviewed only at large size |

---

## 6. Diagnosis order

1. **Recognition**: can you tell what it is at a glance (the letter or the symbol itself)?
2. **Inevitability** (axiom one): are there concrete details, external decoration or extra strokes?
3. **Topology** (section 4): does the closure or symmetry strategy hold?
4. **Order** (axiom two): is the stroke width uniform and medium? Was it cut by boolean operations? Is the curvature continuous? Is the center of mass stable? Is the line of movement coherent?
5. **Shrinking**: look at 16px and 32px with `make_preview.py`; is it still recognizable?

Output format:

- First say what to keep.
- Then list 1–3 problems, each as "what it looks like → which axiom it violates → the fix".
- Finally say how to adjust the negative words for the next round (axiom three): which side to add, which side to keep.

---

## 7. Reference samples

- **OpenAI**: 6-fold rotational symmetry, equal-width lines.
- **Chrome**: 3-fold symmetry, split by concentric circles and tangents, three equal areas.
- **Figma**: modular circles and semicircles joined together, all corner radii identical.
- **Raycast**: open structure + axis-symmetric bell shape, standing on symmetry.
- **Claude**: open radiation + central symmetry, with the outer container providing the second level of closure.
- **macOS Dock icons**: the symbol itself is almost entirely flat; the precision comes from geometry, and lighting and drop shadow are supplied uniformly by the system container.
