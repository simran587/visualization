"""Render every creative chart from the bundled tallest-buildings dataset.

Run from the repository root::

    python examples/gallery.py [output_dir]

Writes SVGs and an index.html to ``output_dir`` (default: ``examples/output``).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import vizcraft as vc


def main(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    data = vc.load_tallest_buildings()
    charts = []

    # 1. Skyline -- 15 tallest as recognizable silhouettes, Burj Khalifa highlighted.
    top15 = data.top("height_m", 15)
    charts.append(("lollipop_tallest", vc.skyline_chart(
        top15.column("building"), top15.column("height_m"),
        title="Burj Khalifa still towers far above the next tallest",
        subtitle="The 15 tallest buildings, each drawn to scale as its own silhouette · metres",
        highlight="Burj Khalifa", unit=" m",
    )))

    # 2. Bar -- a different question: how many of the top 31 each country has.
    counts = [(country, len(ds)) for country, ds in data.groups("country").items()]
    counts.sort(key=lambda kv: kv[1], reverse=True)
    counts = counts[:8]
    charts.append(("bar_by_country", vc.bar_chart(
        [c for c, _ in counts], [n for _, n in counts],
        title="China holds more of the world's tallest than anywhere else",
        subtitle="Number of buildings among the 31 tallest, by country",
        highlight="China",
    )))

    # 3. Bubble -- year vs height, size = floors; focus on mixed-use towers.
    b = data.dropna("floors")
    charts.append(("bubble_year_height", vc.bubble_chart(
        b.column("year_completed"), b.column("height_m"), b.column("floors"),
        groups=b.column("use_type"), highlight_group="mixed-use", labels=b.column("building"),
        annotate=["Burj Khalifa", "Central Park Tower", "Willis Tower (Sears Tower)"],
        x_label="Year completed", y_label="Height (metres)", size_label="floors",
        x_tick_format=lambda v: str(int(v)),  # years, not comma-grouped
        title="The very tallest towers are almost all mixed-use",
        subtitle="Each bubble is a building; larger = more floors · mixed-use in purple",
    )))

    # 4. Dumbbell -- shortest-to-tallest range per country; focus on the UAE.
    cats, lo, hi = [], [], []
    for country, ds in data.groups("country").items():
        heights = ds.column("height_m")
        if len(heights) >= 2:
            cats.append(country); lo.append(min(heights)); hi.append(max(heights))
    order = sorted(range(len(cats)), key=lambda i: hi[i], reverse=True)
    charts.append(("dumbbell_country_range", vc.dumbbell_chart(
        [cats[i] for i in order], [lo[i] for i in order], [hi[i] for i in order],
        low_label="shortest", high_label="tallest", highlight="United Arab Emirates",
        title="The UAE spans the widest range of any country here",
        subtitle="Shortest to tallest building per country, in metres", unit=" m",
    )))

    # 5. Beeswarm -- the height distribution; single hue, tallest few named.
    charts.append(("beeswarm_heights", vc.beeswarm_chart(
        data.column("height_m"),
        labels=data.column("building"),
        highlight_labels=["Burj Khalifa", "Merdeka 118"],
        x_label="Height (metres)",
        title="Most of these cluster between 300 and 550 metres",
        subtitle="One dot per building; the two outliers are named",
    )))

    names = []
    for name, svg in charts:
        svg.save(out_dir / f"{name}.svg")
        print(f"wrote {name}.svg")
        names.append(name)
    _write_index(out_dir, names)
    print(f"\nOpen {out_dir / 'index.html'} to view the gallery.")


def _write_index(out_dir: Path, names) -> None:
    blocks = "\n".join(
        f'  <figure><img src="{n}.svg" alt="{n}" style="max-width:100%"></figure>' for n in names
    )
    html = (
        "<!doctype html><meta charset='utf-8'><title>vizcraft gallery</title>"
        "<style>body{font-family:system-ui,sans-serif;margin:2rem;background:#f4f4f2}"
        "figure{margin:0 0 2rem;background:#fff;padding:1rem;border-radius:10px;"
        "box-shadow:0 1px 5px rgba(0,0,0,.08)}</style>"
        "<h1>vizcraft &mdash; creative charts</h1>\n" + blocks
    )
    (out_dir / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "output"
    main(target)
