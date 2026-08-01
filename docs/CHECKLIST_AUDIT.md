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
| **C12** | Color highlights the key pattern | 2 | 2 | 2 | 2 | 2 |
| **C13** | Color is legible in black & white | 2 | 2 | 2 | 2 | 2 |
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
| | **Score** | **48/48** | **48/48** | **48/48** | **48/48** | **48/48** |

**All five charts score a full 48/48.**

## How each guideline is met

- **Text (T1–T5).** Every title is a 6–12 word takeaway, left-justified in the
  corner, over a supporting subtitle. Text sizes are hierarchical (title >
  subtitle > labels). Data are labeled directly — bar/tower values, the two
  beeswarm outliers, and notable bubbles — and labels are kept sparse.
- **Arrangement (A6–A10).** Bars, towers and dots sit on a zero baseline so
  lengths/positions are ruler-accurate; bubble *area* encodes floors. Data are
  ordered by value, axis intervals are equidistant, every chart is 2-D, and
  there is no chartjunk.
- **Color (C11–C15).** Each chart uses a **focus palette**: one accent color
  highlights the key pattern (Burj Khalifa, China, mixed-use, the UAE, the two
  outliers) while everything else is a neutral gray — so the emphasis is clear
  (C12) and the two tones stay distinct in black & white (C13). The palette is
  validated colorblind-safe (C14), and all text is high-contrast (C15).
- **Lines (L16–L19).** Gridlines are faint, there is no border, there are no
  redundant tick marks, and no chart uses a second/dual axis.
- **Overall (O20–O24).** Each title states the finding, the chart type suits the
  data (ranked magnitude → bar / skyline; a relationship → bubble; a range →
  towers; a distribution → beeswarm), precision is appropriate, and every chart
  compares many buildings/countries so the numbers have context.

## What changed to get here

- **Focus palette** on the Bubble, Range, and Beeswarm charts (one accent + gray)
  — raises C12 and C13 from 1 → 2.
- **Bar chart repurposed** to *buildings per country* (a different question from
  the Skyline) with China highlighted.
- **Radial dial replaced** by the straight bar earlier (radial couldn't earn A6
  proportions or O21 type-appropriateness). `radial_bar_chart` remains in the
  library for anyone who wants the circular look — it is simply not in the
  audited gallery.
- **Fixed** the Range chart's tallest-tower label overlapping the caption (added
  headroom), and deepened the palette's gold so it stays legible.
