# Data Visualization Checklist — audit of the vizcraft charts

Scored against the **Evergreen & Emery Data Visualization Checklist** (24
guidelines across Text · Arrangement · Color · Lines · Overall), on its own
scale: **2 = fully meets · 1 = partially · 0 = does not**.

Charts audited (from `examples/gallery.py`): **Skyline**, **Radial**,
**Bubble**, **Range** (the vertical building/dumbbell), **Beeswarm**.

Legend below: **2** = meets fully · **1** = partial (see note).

| # | Guideline | Skyline | Radial | Bubble | Range | Beeswarm |
|---|-----------|:---:|:---:|:---:|:---:|:---:|
| **T1** | Title is a 6–12 word descriptive takeaway, upper-left | 2 | 2 | 2 | 2 | 2 |
| **T2** | Subtitle / annotations add information | 2 | 2 | 2 | 2 | 2 |
| **T3** | Text size is hierarchical and readable | 2 | 2 | 2 | 2 | 2 |
| **T4** | Data are labeled directly | 2 | 2 | 2 | 2 | 2 |
| **T5** | Labels are used sparingly | 2 | 2 | 2 | 2 | 2 |
| **A6** | Proportions are accurate (start at zero) | 2 | **1** | 2 | 2 | 2 |
| **A7** | Data are intentionally ordered | 2 | 2 | 2 | 2 | 2 |
| **A8** | Axis intervals are equidistant | 2 | 2 | 2 | 2 | 2 |
| **A9** | Graph is 2-D | 2 | 2 | 2 | 2 | 2 |
| **A10** | Display is free from decoration | 2 | 2 | 2 | 2 | 2 |
| **C11** | Color scheme is intentional | 2 | 2 | 2 | 2 | 2 |
| **C12** | Color highlights the key pattern | 2 | 2 | **1** | **1** | **1** |
| **C13** | Color is legible in black & white | 2 | 2 | **1** | **1** | **1** |
| **C14** | Color is legible for colorblindness | 2 | 2 | 2 | 2 | 2 |
| **C15** | Text sufficiently contrasts background | 2 | 2 | 2 | 2 | 2 |
| **L16** | Gridlines, if present, are muted | 2 | 2 | 2 | 2 | 2 |
| **L17** | Graph has no heavy border | 2 | 2 | 2 | 2 | 2 |
| **L18** | No unnecessary tick marks / axis lines | 2 | 2 | 2 | 2 | 2 |
| **L19** | One horizontal + one vertical axis (no dual) | 2 | 2 | 2 | 2 | 2 |
| **O20** | Highlights a significant finding | 2 | 2 | 2 | 2 | 2 |
| **O21** | Graph type is appropriate for the data | 2 | **1** | 2 | 2 | 2 |
| **O22** | Appropriate level of precision | 2 | 2 | 2 | 2 | 2 |
| **O23** | Contextual / comparison data present | 2 | 2 | 2 | 2 | 2 |
| **O24** | Elements reinforce the takeaway | 2 | 2 | 2 | 2 | 2 |
| | **Score** | **48/48** | **44/48** | **44/48** | **44/48** | **44/48** |

## What was changed to raise scores

- **Colorblind-safe palette (C14 → 2 everywhere).** The categorical palette is
  validated (worst adjacent CVD ΔE ≈ 11.9, above the 8 floor); the gold was
  deepened to `#d99a00` so it stays in the lightness band and does not wash out.
- **Direct labels (T4 → 2).** Radial wedges now carry their value; notable
  bubbles (Burj Khalifa, Central Park Tower, Willis Tower) are labeled on the plot.
- **Takeaway titles (T1 / O20 → 2).** Every title now states the finding in
  6–12 words, left-justified in the corner.
- **Radial proportions (A6).** The center hub was shrunk so wedge lengths read
  much closer to proportional-from-zero, and every wedge is value-labeled.

## The remaining 1s — honest tensions

Two of your earlier requests pull against the checklist's Color and chart-type
rules. Nothing here is a bug; they are design trade-offs:

### 1. "Fun colors" vs. C12 (highlight) and C13 (black-and-white)
The Bubble, Range, and Beeswarm charts color **by category** (use type /
country) — the bright multi-hue palette you asked for. The checklist instead
rewards using **one** accent color to highlight the key pattern and graying out
the rest (C12), and warns that several equally-bright hues blur together in
black & white (C13). These are mitigated by direct labels and the legend, but
they are **1s, not 2s**, as long as color encodes a category.

- **To make them 2s:** switch those three charts to a *focus* palette — one
  accent + neutral grays, emphasizing a single series — which sacrifices the
  fun multi-color look.

### 2. The Radial chart vs. A6 (proportions) and O21 (appropriate type)
A radial bar's length is measured along a curve from an offset center, so a
ruler can't verify it the way it can a straight bar — that costs **A6**. And for
"which is tallest," a straight bar / the Skyline communicates more accurately
than a dial, which costs **O21**. Direct value labels mitigate both, but the
radial form can't fully earn these two.

- **To make it a 2:** replace the Radial with a straight bar or lollipop of the
  same data (the Skyline already does this beautifully).

## Bottom line

With the fixes above, the **Skyline scores a full 48/48**, and the other four
sit at **44/48** — each held back only by the two intentional trade-offs above.
Pick either resolution (focus palette / swap the radial) and those become 2s
too.
