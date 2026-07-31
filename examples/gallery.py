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

    # 1. Lollipop -- 15 tallest, Burj Khalifa highlighted.
    top15 = data.top("height_m", 15)
    charts.append(("lollipop_tallest", vc.lollipop_chart(
        top15.column("building"), top15.column("height_m"),
        title="The 15 tallest buildings on Earth",
        subtitle="Structural height in metres", highlight="Burj Khalifa", unit=" m",
    )))

    # 2. Radial bar -- top 14 fanned around a circle.
    top14 = data.top("height_m", 14)
    charts.append(("radial_tallest", vc.radial_bar_chart(
        top14.column("building"), top14.column("height_m"),
        title="A skyline in the round", subtitle="14 tallest, height in metres",
        highlight="Burj Khalifa", unit=" m",
    )))

    # 3. Bubble -- year vs height, size = floors, color = use type.
    b = data.dropna("floors")
    charts.append(("bubble_year_height", vc.bubble_chart(
        b.column("year_completed"), b.column("height_m"), b.column("floors"),
        groups=b.column("use_type"),
        x_label="Year completed", y_label="Height (metres)", size_label="floors",
        x_tick_format=lambda v: str(int(v)),  # years, not comma-grouped
        title="Taller, busier, and mostly built this century",
        subtitle="Each bubble is a building; larger = more floors",
    )))

    # 4. Dumbbell -- shortest-to-tallest range per country (>=2 buildings).
    cats, lo, hi = [], [], []
    for country, ds in data.groups("country").items():
        heights = ds.column("height_m")
        if len(heights) >= 2:
            cats.append(country); lo.append(min(heights)); hi.append(max(heights))
    order = sorted(range(len(cats)), key=lambda i: hi[i], reverse=True)
    charts.append(("dumbbell_country_range", vc.dumbbell_chart(
        [cats[i] for i in order], [lo[i] for i in order], [hi[i] for i in order],
        low_label="shortest", high_label="tallest",
        title="How far apart are each country's giants?",
        subtitle="Shortest to tallest building per country (metres)", unit=" m",
    )))

    # 5. Beeswarm -- the height distribution, tallest few named.
    charts.append(("beeswarm_heights", vc.beeswarm_chart(
        data.column("height_m"), groups=data.column("use_type"),
        labels=data.column("building"),
        highlight_labels=["Burj Khalifa", "Merdeka 118"],
        x_label="Height (metres)",
        title="Most of these cluster between 300 and 550 metres",
        subtitle="One dot per building, colored by use type",
    )))

    # 6. Dark-mode lollipop.
    charts.append(("lollipop_tallest_dark", vc.lollipop_chart(
        top15.column("building"), top15.column("height_m"),
        title="The 15 tallest buildings on Earth",
        subtitle="Structural height in metres", highlight="Burj Khalifa",
        unit=" m", theme="dark",
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
