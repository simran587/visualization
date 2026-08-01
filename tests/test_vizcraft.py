"""Tests for vizcraft: dataset, scales, palette, and creative charts."""

import sys
import xml.dom.minidom as minidom
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import pytest

import vizcraft as vc
from vizcraft.scales import BandScale, LinearScale, nice_ticks


def _wellformed(svg: vc.SVG) -> str:
    text = svg.to_string()
    minidom.parseString(text)  # raises on malformed XML
    assert text.startswith("<svg") and text.rstrip().endswith("</svg>")
    return text


# -- dataset ---------------------------------------------------------------
def test_load_dataset_shape():
    data = vc.load_tallest_buildings()
    assert len(data) == 31
    assert "building" in data.columns and "height_m" in data.columns


def test_na_floors_is_none():
    data = vc.load_tallest_buildings()
    eiffel = data.filter(lambda r: r["building"] == "Eiffel Tower")[0]
    assert eiffel["floors"] is None
    assert len(data.dropna("floors")) == 30


def test_top_orders_and_limits():
    data = vc.load_tallest_buildings()
    top3 = data.top("height_m", 3)
    assert top3.column("building")[0] == "Burj Khalifa"
    assert top3.column("height_m") == sorted(top3.column("height_m"), reverse=True)


def test_head_and_preview():
    data = vc.load_tallest_buildings()
    head = data.head(5)
    assert len(head) == 5
    assert head.column("building")[0] == "Burj Khalifa"
    # HTML table (for notebooks) and plain-text preview both include the data.
    assert "<table" in head._repr_html_() and "Burj Khalifa" in head._repr_html_()
    assert "Burj Khalifa" in data.preview(5) and "building" in data.preview(5)


def test_groups_split():
    data = vc.load_tallest_buildings()
    g = data.groups("country")
    assert sum(len(ds) for ds in g.values()) == 31
    assert len(g["China"]) >= 2


# -- charts ----------------------------------------------------------------
def test_skyline_wellformed():
    svg = vc.skyline_chart(["A", "B", "C"], [300, 500, 400], title="t", highlight="B", unit=" m")
    text = _wellformed(svg)
    assert "300 m" in text and "<path" in text  # silhouettes are paths


def test_skyline_named_buildings_get_distinct_shapes():
    data = vc.load_tallest_buildings()
    top = data.top("height_m", 6)
    svg = vc.skyline_chart(top.column("building"), top.column("height_m"), highlight="Burj Khalifa")
    text = svg.to_string()
    # Abraj Al-Bait contributes a clock face (circle); the WFC/others contribute paths.
    assert text.count("<path") >= 6
    # Short names appear on the axis.
    assert "Burj Khalifa" in text and "Shanghai Tower" in text


def test_lollipop_alias_points_to_skyline():
    assert vc.lollipop_chart is vc.skyline_chart


def test_bar_chart_wellformed_and_highlight():
    svg = vc.bar_chart(["A", "B", "C"], [300, 500, 400], title="t", highlight="B", unit=" m")
    text = _wellformed(svg)
    assert "500 m" in text and "<rect" in text
    # highlighted bar uses the accent; others use the slate/secondary ink
    assert vc.LIGHT.accent in text


def test_radial_bar_wellformed():
    svg = vc.radial_bar_chart(["A", "B", "C", "D"], [1, 2, 3, 4], title="t", highlight=0)
    text = _wellformed(svg)
    assert "<path" in text  # wedges


def test_bubble_wellformed_and_legend():
    svg = vc.bubble_chart([1, 2, 3], [4, 5, 6], [10, 20, 30],
                          groups=["x", "y", "x"], title="t", size_label="floors")
    text = _wellformed(svg)
    assert "bubble size = floors" in text
    assert "<circle" in text


def test_dumbbell_wellformed():
    svg = vc.dumbbell_chart(["China", "USA"], [300, 320], [632, 541], title="t", unit=" m")
    text = _wellformed(svg)
    # Category names and the tallest value are labeled directly on the towers.
    assert "China" in text and "632 m" in text


def test_beeswarm_no_overlap():
    # Many identical values force the swarm to spread vertically without overlap.
    values = [400] * 12
    svg = vc.beeswarm_chart(values, radius=6, title="t")
    _wellformed(svg)
    # Parse circles and confirm no two data dots overlap.
    import re
    pts = [(float(m[0]), float(m[1])) for m in
           re.findall(r'<circle cx="([\d.]+)" cy="([\d.]+)" r="(?:6|7)"', svg.to_string())]
    assert len(pts) >= 12
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            dx, dy = pts[i][0] - pts[j][0], pts[i][1] - pts[j][1]
            assert (dx * dx + dy * dy) ** 0.5 >= 11.0  # >= ~2r, allow rounding


def test_highlight_unknown_raises():
    with pytest.raises(ValueError):
        vc.lollipop_chart(["A", "B"], [1, 2], highlight="Z")


def test_length_mismatch_raises():
    with pytest.raises(ValueError):
        vc.bubble_chart([1, 2], [1], [1])


def test_end_to_end_from_dataset():
    data = vc.load_tallest_buildings()
    top = data.top("height_m", 10)
    _wellformed(vc.lollipop_chart(top.column("building"), top.column("height_m"), highlight="Burj Khalifa"))


# -- scales / palette ------------------------------------------------------
def test_linear_scale_endpoints():
    s = LinearScale(0, 100, 0, 500)
    assert s(0) == 0 and s(100) == 500 and s(50) == 250


def test_band_scale_within_range():
    b = BandScale(range(3), 0, 300)
    for i in range(3):
        assert 0 <= b.position(i) <= 300


def test_nice_ticks_span():
    ticks = nice_ticks(0, 828, 5)
    assert ticks[0] <= 0 and ticks[-1] >= 828


def test_palette_fixed_order_and_limit():
    assert vc.LIGHT.color(0) == "#3b9dff"      # first slot of the fun palette
    assert vc.LIGHT.color(0) != vc.LIGHT.color(1)
    with pytest.raises(IndexError):
        vc.LIGHT.color(8)


def test_get_theme():
    assert vc.get_theme("dark").name == "dark"
    with pytest.raises(ValueError):
        vc.get_theme("nope")
