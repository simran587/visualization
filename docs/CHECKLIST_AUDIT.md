# Data Visualization Checklist — audit of the vizcraft charts

Scored against the **Evergreen & Emery Data Visualization Checklist** (24
guidelines across Text · Arrangement · Color · Lines · Overall), on its own
scale: **2 = fully meets · 1 = partially · 0 = does not**.

Charts audited (from `examples/gallery.py`): **Skyline**, **Bar**, **Bubble**,
**Range** (the vertical building/dumbbell), **Beeswarm**.

| # | Guideline | Skyline | Bar | Bubble | Range | Beeswarm |
|---|-----------|:---:|:---:|:---:|:---:|:---:|
| **T1** | Title is a 6–12 word descriptive takeaway, upper-left | 2 | 2 | 2 | 2 | 2 |
| **T2** | Subtitle / annotations add information | **1** | **1** | 2 | **1** | 2 |
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
| | **Score** | **47/48** | **47/48** | **46/48** | **45/48** | **48/48** |

## Two intentional trade-offs shape these scores

**1. Decluttered text (T2).** Per the "so what?" guideline (O20), the charts were
stripped to the finding: each keeps only its takeaway **title** plus the
essentials to read values (axis labels, value labels, legend). Subtitles and
extra caption lines were removed. Because guideline **T2** specifically rewards a
*subtitle or annotation*, the charts that have no callout annotation — **Skyline,
Bar, Range** — score **T2 = 1**. The **Bubble** and **Beeswarm** charts keep
direct callout labels (named buildings / outliers), which count as annotations,
so they stay **T2 = 2**.

**2. Multi-color palettes (C12 / C13).** The **Bubble** and **Range** charts
color **by category** (use type / country) to stay colorful, rather than the
checklist's one-accent "focus" style. That costs each **C12** (highlight a single
pattern) and **C13** (bright hues blur in black & white). The Bubble palette
still **avoids the red-green and yellow-blue colorblind-confusion pairs** (blue /
orange / teal / pink), so **C14 stays a 2**.

## Everything else is a 2

Across all five charts: takeaway titles, direct value labels, zero baselines,
intentional ordering, equidistant axes, 2-D, no chartjunk, intentional and
colorblind-safe color, high-contrast text, muted gridlines, no borders, no
redundant ticks, single axis pair, a stated finding, appropriate chart type and
precision, and comparison context.

## Notes

- Want the Skyline/Bar/Range back to full marks? Re-adding a one-line subtitle
  (or a single annotation callout) restores **T2 = 2** — a small amount of the
  text that was just removed.
- `radial_bar_chart` remains in the library for the circular look; it is not in
  the audited gallery because the radial form can't earn A6 (proportions) or O21
  (appropriate type).
