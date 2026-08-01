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
| **C12** | Color highlights the key pattern | 2 | 2 | **1** | **1** | 2 |
| **C13** | Color is legible in black & white | 2 | 2 | **1** | **1** | 2 |
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
| | **Score** | **48/48** | **48/48** | **44/48** | **44/48** | **48/48** |

## The two 44/48 charts — a deliberate color choice

The **Bubble** and **Range** charts color **by category** (use type / country) so
the palette stays colorful, rather than the checklist's preferred one-accent
"focus" style. That costs each of them **C12** (color highlighting a single key
pattern) and **C13** (several equally-bright hues blur together in black &
white). Both are mitigated by direct labels, but they are **1s, not 2s**, by
design.

- The Bubble palette deliberately **avoids the red-green and yellow-blue
  colorblind-confusion pairs** (blue / orange / teal / pink — no yellow beside
  the blue, no red beside a green), so **C14 stays a 2**.
- To make either a strict 48/48, switch it back to a focus palette (one accent +
  gray) — at the cost of the multi-color look.

## The three 48/48 charts

Skyline, Bar, and Beeswarm each use one accent color over neutral grays — one
clear emphasis (Burj Khalifa, China, the two outliers), legible in black & white
— and meet every other guideline: takeaway titles, direct labels, zero
baselines, ordered data, muted gridlines, no borders, colorblind-safety,
appropriate precision, and comparison context.

## Notes

- `radial_bar_chart` remains in the library for the circular look; it is not in
  the audited gallery because the radial form can't earn A6 (proportions) or O21
  (appropriate type).
- The Range chart's tallest-tower value label was moved clear of the caption.
