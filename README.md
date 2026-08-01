# vizcraft

A **zero-dependency** Python library of **creative** SVG charts — the ones you
don't get out of the box. No matplotlib, no pandas, no compiled extensions:
pure standard-library Python that emits portable SVG. Ships with the
tallest-buildings dataset so you can render something interesting immediately.

Chart types, **deliberately no pie, heatmap, or table**:

| Function | What it's for |
|---|---|
| `skyline_chart` | a to-scale skyline where each value is its own recognizable building silhouette (also aliased `lollipop_chart`) |
| `bar_chart` | a straight, checklist-ideal horizontal bar chart for ranked magnitude |
| `bubble_chart` | three–four numerics at once: x, y, bubble size, and color |
| `dumbbell_chart` | a low→high range per category, as a dumbbell (two dots + connector) |
| `beeswarm_chart` | a value distribution as non-overlapping dots |
| `radial_bar_chart` | magnitude fanned around a circle (available, but see the checklist audit) |

Every chart uses a bright, fun palette, one **accent** color for emphasis
with **muted** gray for the rest, and works in `light` or `dark` themes.

## Gallery

All rendered from the bundled `tallest_buildings.csv`.

### Skyline — the 15 tallest buildings, to scale
Each building stands on a ground line, scaled to its true height, and drawn as
its **own recognizable silhouette**: Burj Khalifa's stepped taper and spire,
Taipei 101's tiers, Shanghai Tower's twist, China Zun's waist, the Shanghai WFC
aperture, the Abraj clock face, Central Park's pencil slab, and more.

![The 15 tallest buildings as recognizable to-scale silhouettes](docs/charts/lollipop_tallest.png)

### Bar — how many of the tallest each country holds
A straight horizontal bar chart (a different question from the skyline): the
count of top-31 buildings per country, with China highlighted. Bars start at
zero, names read left to right, values are labeled directly.

![Horizontal bar chart of buildings per country, China highlighted](docs/charts/bar_by_country.png)

### Bubble — year vs height, size = floors
Mixed-use towers are highlighted in the accent color and everything else recedes
to gray, so the finding ("the very tallest are almost all mixed-use") reads at a
glance.

![Bubble chart of year completed versus height, mixed-use highlighted](docs/charts/bubble_year_height.png)

### Dumbbell — each country's shortest-to-tallest range
A horizontal dumbbell: for each country a connector joins its shortest (open
circle) and tallest (filled dot) building. The UAE — the widest range — is
highlighted in the accent color and the rest recede to gray.

![Horizontal dumbbell chart of each country's shortest-to-tallest building range](docs/charts/dumbbell_country_range.png)

### Beeswarm — the height distribution, dot by dot
One dot per building; the two outliers (Burj Khalifa, Merdeka 118) are
highlighted and named.

![Beeswarm plot of building heights with the two outliers named](docs/charts/beeswarm_heights.png)

> Every chart also supports `theme="dark"` (see the **Theming** section). These
> images live in [`docs/charts/`](docs/charts) and are regenerated from the SVGs
> produced by `python examples/gallery.py`. Charts are stripped to the
> **finding** (title) plus the essentials, and each uses a one-accent focus
> palette. On the [Data Visualization Checklist audit](docs/CHECKLIST_AUDIT.md)
> four charts score **48/48**; only the Bar chart is a point short (no subtitle).

## Run it in Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/simran587/visualization/blob/claude/visualization-library-dataset-ei5m7t/examples/vizcraft_demo.ipynb)

The notebook [`examples/vizcraft_demo.ipynb`](examples/vizcraft_demo.ipynb)
`pip install`s vizcraft and renders the **Skyline** and **Dumbbell** charts
inline. Open it in Colab (badge above) and choose **Runtime → Run all**.

## Installation

```bash
# from a clone
pip install -e .

# or straight from GitHub (what the Colab notebook uses)
pip install "git+https://github.com/simran587/visualization.git@claude/visualization-library-dataset-ei5m7t"
```

> If the repo is **private**, a Colab/`pip` install from GitHub needs a token:
> `git+https://<TOKEN>@github.com/...` (or make the repo public).

### Displaying a chart in a notebook

```python
import vizcraft as vc
from IPython.display import SVG, display

data = vc.load_tallest_buildings()
top = data.top("height_m", 15)
chart = vc.skyline_chart(top.column("building"), top.column("height_m"),
                         highlight="Burj Khalifa", unit=" m",
                         title="Burj Khalifa still towers far above the next tallest")
display(SVG(chart.to_string()))   # renders inline in Jupyter / Colab
```

## Quick start

```python
import vizcraft as vc

data = vc.load_tallest_buildings()          # bundled dataset (31 buildings)
top = data.top("height_m", 15)              # 15 tallest, ordered

vc.skyline_chart(
    top.column("building"), top.column("height_m"),
    title="The 15 tallest buildings on Earth, to scale",
    subtitle="Each drawn as its own silhouette",
    highlight="Burj Khalifa", unit=" m",
).save("skyline.svg")
```

Every chart function returns an `SVG` object with `.save(path)` and
`.to_string()`.

## The bundled dataset

`load_tallest_buildings()` returns 31 rows — the world's tallest buildings and
structures:

| column | example | notes |
|---|---|---|
| `rank` | `1` | 1–31 |
| `building` | `Burj Khalifa` | name |
| `city`, `country` | `Dubai`, `United Arab Emirates` | categorical |
| `height_m`, `height_ft` | `828`, `2717` | numeric |
| `year_completed` | `2010` | temporal |
| `floors` | `163` | numeric — `Eiffel Tower` is `None` (it's a tower) |
| `use_type` | `mixed-use` | categorical |

The tiny `Dataset` helper covers what the charts need: `column`, `unique`,
`filter`, `dropna`, `sort_by`, `top`, and `groups`.

## More examples

```python
import vizcraft as vc
data = vc.load_tallest_buildings()

# Straight bar chart — the 14 tallest, ranked
top14 = data.top("height_m", 14)
vc.bar_chart(top14.column("building"), top14.column("height_m"),
             highlight="Burj Khalifa", unit=" m",
             title="Burj Khalifa outreaches the next thirteen giants").save("bar.svg")

# Bubble — year vs height, bubble size = floors, color = use type
b = data.dropna("floors")
vc.bubble_chart(
    b.column("year_completed"), b.column("height_m"), b.column("floors"),
    groups=b.column("use_type"),
    x_label="Year completed", y_label="Height (m)", size_label="floors",
    x_tick_format=lambda v: str(int(v)),     # years, not comma-grouped
    title="Taller, busier, and mostly built this century",
).save("bubble.svg")

# Dumbbell — each country's shortest-to-tallest range
cats, lo, hi = [], [], []
for country, ds in data.groups("country").items():
    h = ds.column("height_m")
    if len(h) >= 2:
        cats.append(country); lo.append(min(h)); hi.append(max(h))
vc.dumbbell_chart(cats, lo, hi, low_label="shortest", high_label="tallest",
                  unit=" m", title="How far apart are each country's giants?").save("dumbbell.svg")

# Beeswarm — the height distribution, tallest few named
vc.beeswarm_chart(data.column("height_m"), groups=data.column("use_type"),
                  labels=data.column("building"),
                  highlight_labels=["Burj Khalifa", "Merdeka 118"],
                  x_label="Height (m)",
                  title="Most cluster between 300 and 550 metres").save("beeswarm.svg")
```

## Render the full gallery

```bash
python examples/gallery.py       # writes SVGs + index.html to examples/output/
```

Open `examples/output/index.html` in a browser to see one of every chart type
rendered from the bundled dataset (light and dark).

> **Note:** SVGs are drawn by the library, but GitHub shows `.html`/`.svg` files
> as source — open the generated files locally (or via GitHub Pages) to see them
> rendered.

## Theming

Pass `theme="light"` (default) or `theme="dark"` to any chart, or a custom
`vizcraft.Theme`.

## Project structure

```
visualization/
├── src/vizcraft/
│   ├── __init__.py         # public API
│   ├── charts.py           # skyline / bar / bubble / dumbbell / beeswarm / radial
│   ├── buildings.py        # recognizable building silhouettes for the skyline
│   ├── dataset.py          # Dataset + load_tallest_buildings()
│   ├── palette.py          # colorblind-safe light & dark themes
│   ├── scales.py           # linear + band scales, nice ticks
│   ├── svg.py              # zero-dependency SVG builder
│   └── datasets/
│       └── tallest_buildings.csv
├── examples/gallery.py
├── tests/
├── README.md
├── pyproject.toml
└── LICENSE
```

## Development

```bash
pip install -e ".[dev]"
pytest
```
