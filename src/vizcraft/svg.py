"""Minimal SVG document builder.

Zero dependencies: every chart is assembled from these primitives into a plain
string of SVG markup. Coordinates follow the SVG convention (y grows downward).
Text content and attribute values are XML-escaped.
"""

from __future__ import annotations

from typing import Iterable
from xml.sax.saxutils import escape, quoteattr


def _attrs(attrs: dict) -> str:
    parts = []
    for key, value in attrs.items():
        if value is None:
            continue
        name = key.replace("_", "-")
        parts.append(f"{name}={quoteattr(str(value))}")
    return (" " + " ".join(parts)) if parts else ""


class SVG:
    """Accumulates SVG elements and serializes them into a full document."""

    def __init__(self, width: float, height: float, background: str | None = None, title: str | None = None):
        self.width = width
        self.height = height
        self.background = background
        self.accessible_title = title
        self._elements: list[str] = []

    def rect(self, x, y, width, height, *, rx: float | None = None, **attrs) -> "SVG":
        self._elements.append(f"<rect{_attrs({'x': x, 'y': y, 'width': width, 'height': height, 'rx': rx, **attrs})}/>")
        return self

    def line(self, x1, y1, x2, y2, **attrs) -> "SVG":
        self._elements.append(f"<line{_attrs({'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, **attrs})}/>")
        return self

    def circle(self, cx, cy, r, **attrs) -> "SVG":
        self._elements.append(f"<circle{_attrs({'cx': cx, 'cy': cy, 'r': r, **attrs})}/>")
        return self

    def path(self, d: str, **attrs) -> "SVG":
        self._elements.append(f"<path{_attrs({'d': d, **attrs})}/>")
        return self

    def polyline(self, points: Iterable[tuple[float, float]], **attrs) -> "SVG":
        pts = " ".join(f"{x},{y}" for x, y in points)
        self._elements.append(f"<polyline{_attrs({'points': pts, **attrs})}/>")
        return self

    def text(self, x, y, content: str, **attrs) -> "SVG":
        self._elements.append(f"<text{_attrs({'x': x, 'y': y, **attrs})}>{escape(str(content))}</text>")
        return self

    def group(self, markup: str, **attrs) -> "SVG":
        self._elements.append(f"<g{_attrs(attrs)}>{markup}</g>")
        return self

    def raw(self, markup: str) -> "SVG":
        self._elements.append(markup)
        return self

    def to_string(self) -> str:
        header = (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{self.width}" height="{self.height}" '
            f'viewBox="0 0 {self.width} {self.height}" role="img" '
            f'font-family="system-ui, -apple-system, \'Segoe UI\', sans-serif">'
        )
        body = []
        if self.accessible_title is not None:
            body.append(f"<title>{escape(self.accessible_title)}</title>")
        if self.background is not None:
            body.append(f'<rect x="0" y="0" width="{self.width}" height="{self.height}" fill="{self.background}"/>')
        body.extend(self._elements)
        return header + "".join(body) + "</svg>"

    def __str__(self) -> str:  # pragma: no cover
        return self.to_string()

    def save(self, path) -> None:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(self.to_string())
