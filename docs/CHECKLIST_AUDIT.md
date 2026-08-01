# Data Visualization Checklist — audit of the vizcraft charts

Scored against the **Evergreen & Emery Data Visualization Checklist** (24
guidelines across Text · Arrangement · Color · Lines · Overall), on its own
scale: **2 = fully meets · 1 = partially · 0 = does not**.

Charts audited (from `examples/gallery.py`): **Skyline**, **Bar**, **Bubble**,
**Range** (the vertical building/dumbbell), **Beeswarm**.

| # | Guideline | Skyline | Bar | Bubble | Range | Beeswarm |
|---|-----------|:---:|:---:|:---:|:---:|:---:|
| **T1** | Title is a 6–12 word descriptive takeaway, upper-left | 2 | 2 | 2 | 2 | 2 |
| **T2** | Subtitle / annotations add information | 2 | 2 | 2 | 2 | 2 |
| **T3** | Text size is hierarchical and readable | 2 | 2 | 2 | 2 | 2 |
| **T4** | Data are labeled directly | 2 | 2 | 2 | 2 | 2 |
| **T5** | Labels are used sparingly | 2 | 2 | 2 | 2 | 2 |
| **A6** | Proportions are accurate (start at zero) | 2 | 2 | 2 | 2 | 2 |
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
| **O21** | Graph type is appropriate for the data | 2 | 2 | 2 | 2 | 2 |
| **O22** | Appropriate level of precision | 2 | 2 | 2 | 2 | 2 |
| **O23** | Contextual / comparison data present | 2 | 2 | 2 | 2 | 2 |
| **O24** | Elements reinforce the takeaway | 2 | 2 | 2 | 2 | 2 |
| | **Score** | **48/48** | **48/48** | **44/48** | **44/48** | **44/48** |

## What was changed to raise scores

- **Swapped the radial dial for a straight `bar_chart`.** A radial bar's length
  can't be ruler-verified and a dial isn't the clearest form for "which is
  tallest," which cost the old radial **A6** and **O21**. The straight bar starts
  at zero, labels every value, and highlights Burj Khalifa — a full **48/48**.
  (`radial_bar_chart` is still in the library if you want the circular look.)
- **Colorblind-safe palette (C14 = 2 everywhere).** Validated (worst adjacent
  CVD ΔE ≈ 11.9); the gold was deepened to `#d99a00` so it stays in the
  lightness band and does not wash out.
- **Direct labels (T4 = 2).** Notable bubbles (Burj Khalifa, Central Park Tower,
  Willis Tower) are labeled on the plot.
- **Takeaway titles (T1 / O20 = 2).** Every title states the finding in 6–12
  words, left-justified in the corner.

## The remaining 1s — a deliberate choice

The Bubble, Range, and Beeswarm charts color **by category** (use type /
country) using the bright multi-hue palette — kept on purpose. The checklist
instead rewards using **one** accent color to highlight the key pattern and
graying out the rest (**C12**), and warns that several equally-bright hues blur
together in black & white (**C13**). Both are mitigated here by direct labels
and the legend, but they remain **1s** as long as color encodes a category.

- **To turn them into 2s:** recolor those three with a *focus* palette — one
  accent + neutral grays — which would sacrifice the multi-color look. This was
  considered and declined in favor of the brighter design.

## Bottom line

**Skyline and Bar both score a full 48/48.** Bubble, Range, and Beeswarm sit at
**44/48**, held back only by the intentional choice to keep the fun categorical
colors (C12 / C13). Everything else — titles, direct labels, proportions,
ordering, muted gridlines, no borders, colorblind-safety, precision, and
comparison context — is at full marks across all five charts.
