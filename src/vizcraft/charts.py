"""Creative chart renderers.

Five non-standard chart types, each returning an :class:`~vizcraft.svg.SVG`:

* :func:`skyline_chart`   -- a skyline of recognizable building silhouettes
  (also exported as ``lollipop_chart``, the name it evolved from)
* :func:`radial_bar_chart` -- magnitude fanned around a circle
* :func:`bubble_chart`    -- three/four numerics at once (x, y, size, color)
* :func:`dumbbell_chart`  -- a low->high range per category
* :func:`beeswarm_chart`  -- a value distribution as non-overlapping dots

Deliberately no pie, heatmap, or table. Shared style: recessive gridlines and
axes, one accent color for emphasis with muted gray for the rest, and text in
ink tokens (never the mark color).
"""

from __future__ import annotations

import math
from typing import Mapping, Sequence

from .buildings import draw_building, short_name
from .palette import Theme, get_theme
from .scales import BandScale, LinearScale
from .svg import SVG

_TITLE_X = 26


def _format_number(value, decimals=None) -> str:
    if value is None:
        return ""
    if decimals is not None:
        return f"{value:,.{decimals}f}"
    return f"{int(value):,}" if float(value).is_integer() else f"{value:,.1f}"


def _header(svg: SVG, theme: Theme, title, subtitle) -> None:
    if title:
        svg.text(_TITLE_X, 32, title, font_size=19, font_weight="700",
                 fill=theme.text_primary, text_anchor="start")
    if subtitle:
        svg.text(_TITLE_X, 53, subtitle, font_size=13, fill=theme.text_secondary, text_anchor="start")


def _legend(svg: SVG, theme: Theme, entries, x, y) -> None:
    cursor = x
    for label, color in entries:
        svg.circle(cursor + 6, y - 4, 6, fill=color)
        svg.text(cursor + 16, y, str(label), font_size=12.5, fill=theme.text_secondary, text_anchor="start")
        cursor += 26 + 7.4 * len(str(label))


def _polar(cx, cy, r, angle):
    return cx + r * math.cos(angle), cy + r * math.sin(angle)


# ---------------------------------------------------------------------------
def skyline_chart(
    labels: Sequence, values: Sequence[float], *,
    title=None, subtitle=None, highlight=None, unit="", decimals=None,
    width=None, height=680, theme="light",
) -> SVG:
    """A skyline: each value stands on a ground line as a recognizable building
    silhouette, scaled to its true height (see :mod:`vizcraft.buildings`).

    ``labels`` should be building names so each gets its own silhouette; unknown
    names fall back to a generic tower. ``highlight`` (a name or index) paints
    one building in the accent color and the rest in a neutral slate.
    """
    theme = get_theme(theme)
    if len(labels) != len(values):
        raise ValueError("labels and values must be the same length")
    n = len(labels)
    col_w = 68
    axis_left, right_pad = 52, 18
    if width is None:
        width = axis_left + right_pad + n * col_w
    top, name_area = 84, 108
    ground_y = height - name_area
    plot_top = top + 34                    # headroom above the tallest for its label

    svg = SVG(width, height, background=theme.surface, title=title or "Skyline")
    _header(svg, theme, title, subtitle)

    hi = _resolve_highlight(highlight, labels)
    vmax = max(values) if values else 1
    y = LinearScale(0, vmax, ground_y, plot_top)          # value -> pixel (up)
    band = BandScale(range(n), axis_left, width - right_pad, padding=0.12)

    # Faint height reference lines with metre labels on the left.
    for t in y.ticks(5):
        if t <= 0 or t > vmax:
            continue  # skip zero and any tick above the tallest building
        ty = y(t)
        svg.line(axis_left, ty, width - right_pad, ty, stroke=theme.grid, stroke_width=1)
        svg.text(axis_left - 6, ty + 4, _format_number(t), font_size=10.5,
                 fill=theme.axis_label, text_anchor="end")

    slate = theme.text_secondary
    for i, (label, value) in enumerate(zip(labels, values)):
        cx = band.center(i)
        bw = band.bandwidth
        bh = ground_y - y(value)
        color = theme.accent if (hi is None or i == hi) else slate
        for el in draw_building(label, cx, ground_y, bw, bh, color, theme.surface):
            svg.raw(el)
        # Height label above each tower.
        svg.text(cx, ground_y - bh - 9, f"{_format_number(value, decimals)}{unit}",
                 font_size=10, font_weight="600" if (hi is not None and i == hi) else "400",
                 fill=theme.text_primary if (hi is not None and i == hi) else theme.text_secondary,
                 text_anchor="middle")
        # Building name, rotated below the ground line.
        ny = ground_y + 12
        svg.text(cx, ny, short_name(label), font_size=11, fill=theme.text_secondary,
                 text_anchor="end", transform=f"rotate(-90 {cx:.1f} {ny})")

    svg.line(axis_left, ground_y, width - right_pad, ground_y, stroke=theme.axis, stroke_width=2)
    return svg


# The skyline is the evolution of what began as the lollipop chart; keep the old
# name working for callers that still use it.
lollipop_chart = skyline_chart


def bar_chart(
    labels: Sequence, values: Sequence[float], *,
    title=None, subtitle=None, highlight=None, highlight_color=None, unit="", decimals=None,
    width=780, height=None, theme="light",
) -> SVG:
    """A straight horizontal bar chart -- the checklist-ideal form for ranked
    magnitude: bars start at zero (ruler-accurate), category names read left to
    right, values are labeled directly, and ``highlight`` paints one bar in the
    accent while the rest recede to a neutral slate. ``highlight_color`` overrides
    the accent for the highlighted bar.
    """
    theme = get_theme(theme)
    if len(labels) != len(values):
        raise ValueError("labels and values must be the same length")
    n = len(labels)
    top, bottom_pad, row_h = 84, 46, 30
    if height is None:
        height = top + n * row_h + bottom_pad
    left = min(300, max(90, 8 * max((len(str(l)) for l in labels), default=8)))
    right = width - 92
    hi = _resolve_highlight(highlight, labels)

    svg = SVG(width, height, background=theme.surface, title=title or "Bar chart")
    _header(svg, theme, title, subtitle)

    x = LinearScale(0, max(values) if values else 1, left, right)
    band = BandScale(range(n), top, height - bottom_pad, padding=0.34)
    # Muted vertical gridlines with value ticks along the bottom.
    for t in x.ticks(5):
        tx = x(t)
        svg.line(tx, top, tx, height - bottom_pad, stroke=theme.grid, stroke_width=1)
        svg.text(tx, height - bottom_pad + 18, _format_number(t), font_size=11,
                 fill=theme.axis_label, text_anchor="middle")

    slate = theme.text_secondary
    accent = highlight_color or theme.accent
    for i, (label, value) in enumerate(zip(labels, values)):
        by = band.position(i)
        bw = max(1.0, x(value) - left)
        color = accent if (hi is None or i == hi) else slate
        svg.rect(left, by, bw, band.bandwidth, rx=3, fill=color)
        svg.text(left - 10, by + band.bandwidth / 2 + 4, str(label),
                 font_size=12.5, fill=theme.text_secondary, text_anchor="end")
        svg.text(x(value) + 8, by + band.bandwidth / 2 + 4, f"{_format_number(value, decimals)}{unit}",
                 font_size=11.5, font_weight="600", fill=theme.text_primary, text_anchor="start")

    svg.line(left, top, left, height - bottom_pad, stroke=theme.axis, stroke_width=1.5)
    return svg


def radial_bar_chart(
    labels: Sequence, values: Sequence[float], *,
    title=None, subtitle=None, highlight=None, unit="", decimals=None,
    width=720, height=720, theme="light", start_deg=-90, sweep_deg=360,
) -> SVG:
    """Radial (polar) bar chart: each category is a wedge whose outer radius
    encodes its value, fanned around a circle."""
    theme = get_theme(theme)
    if len(labels) != len(values):
        raise ValueError("labels and values must be the same length")
    n = len(labels)
    hi = _resolve_highlight(highlight, labels)

    svg = SVG(width, height, background=theme.surface, title=title or "Radial bar chart")
    _header(svg, theme, title, subtitle)

    cx, cy = width / 2, height / 2 + 26
    # A small hub keeps the wedge lengths close to proportional-from-zero.
    r_inner = min(width, height) * 0.06
    r_outer = min(width, height) * 0.40
    rscale = LinearScale(0, max(values) if values else 1, r_inner, r_outer)

    # Reference rings at nice values (skip any above the tallest building).
    vmax = max(values) if values else 1
    for t in rscale.ticks(4):
        if t <= 0 or t > vmax:
            continue
        rr = rscale(t)
        svg.circle(cx, cy, rr, fill="none", stroke=theme.grid, stroke_width=1)
        svg.text(cx, cy - rr - 3, _format_number(t), font_size=10, fill=theme.axis_label, text_anchor="middle")

    start = math.radians(start_deg)
    total = math.radians(sweep_deg)
    slice_a = total / n
    gap = slice_a * 0.16
    for i, (label, value) in enumerate(zip(labels, values)):
        a0 = start + i * slice_a + gap / 2
        a1 = start + (i + 1) * slice_a - gap / 2
        ro = rscale(value)
        color = theme.accent if (hi is None or i == hi) else theme.muted
        svg.path(_wedge(cx, cy, r_inner, ro, a0, a1), fill=color, stroke=theme.surface, stroke_width=1)
        mid = (a0 + a1) / 2
        deg = math.degrees(mid)
        flip = 90 < (deg % 360) < 270
        rot = deg + 180 if flip else deg
        anchor = "end" if flip else "start"
        # Name label just past the wedge, rotated to read outward.
        lx, ly = _polar(cx, cy, ro + 12, mid)
        svg.text(lx, ly, str(label), font_size=10.5, fill=theme.text_secondary,
                 text_anchor=anchor, transform=f"rotate({rot:.1f} {lx:.1f} {ly:.1f})",
                 dominant_baseline="middle")
        # Direct value label inside the wedge tip (so exact values are readable).
        vx, vy = _polar(cx, cy, ro - 16, mid)
        svg.text(vx, vy, f"{_format_number(value, decimals)}{unit}", font_size=9.5, font_weight="600",
                 fill=theme.surface, text_anchor="middle",
                 transform=f"rotate({rot:.1f} {vx:.1f} {vy:.1f})", dominant_baseline="middle")

    svg.circle(cx, cy, r_inner, fill=theme.surface, stroke=theme.axis, stroke_width=1)
    return svg


def bubble_chart(
    x_values: Sequence[float], y_values: Sequence[float], sizes: Sequence[float], *,
    groups: Sequence | None = None, highlight_group=None, highlight_color=None,
    group_palette=None, labels: Sequence | None = None,
    annotate: Sequence | None = None, x_label=None, y_label=None,
    title=None, subtitle=None, size_label=None, x_tick_format=None,
    width=820, height=560, theme="light", max_radius=34,
) -> SVG:
    """Bubble chart: x vs y with bubble *area* encoding ``sizes`` and optional
    color by ``groups``.

    ``x_tick_format`` is an optional callable ``value -> str`` for the x axis
    (e.g. ``str(int(v))`` for years, which should not be comma-grouped).
    ``annotate`` is a list of ``labels`` values whose bubbles are labeled
    directly on the chart. ``highlight_group`` switches to a *focus* palette:
    the named group is drawn in the accent color and every other group recedes
    to a neutral gray (highlighting one key pattern, and legible in black & white).
    ``group_palette`` is an optional list of hex colors assigned to the groups
    in first-seen order (overriding the theme's categorical palette) -- use it to
    pick a colorblind-friendly set for the categories.
    """
    theme = get_theme(theme)
    if not (len(x_values) == len(y_values) == len(sizes)):
        raise ValueError("x_values, y_values and sizes must be the same length")
    groups = list(groups) if groups is not None else [None] * len(x_values)
    labels = list(labels) if labels is not None else [None] * len(x_values)
    annotate_set = set(annotate or [])
    fmt_x = x_tick_format or _format_number

    top, left, right, bottom = 104, 66, width - 26, height - 58
    svg = SVG(width, height, background=theme.surface, title=title or "Bubble chart")
    _header(svg, theme, title, subtitle)

    def pad(lo, hi):
        d = (hi - lo) * 0.08 or 1
        return lo - d, hi + d
    xlo, xhi = pad(min(x_values), max(x_values))
    ylo, yhi = pad(min(y_values), max(y_values))
    sx = LinearScale(xlo, xhi, left, right)
    sy = LinearScale(min(0, ylo), yhi, bottom, top)
    smax = max(sizes) or 1
    rad = lambda s: max(4, math.sqrt(s / smax) * max_radius)

    for t in sy.ticks(5):
        ty = sy(t)
        if ty < top - 1 or ty > bottom + 1:
            continue  # skip ticks that fall outside the plot area
        svg.line(left, ty, right, ty, stroke=theme.grid, stroke_width=1)
        svg.text(left - 8, ty + 4, _format_number(t), font_size=11, fill=theme.axis_label, text_anchor="end")
    for t in sx.ticks(6):
        tx = sx(t)
        if left - 1 <= tx <= right + 1:
            svg.text(tx, bottom + 18, fmt_x(t), font_size=11, fill=theme.axis_label, text_anchor="middle")

    focus = highlight_group is not None
    group_keys = [g for g in groups if g is not None]
    if group_palette:
        cmap, gi = {}, 0
        for g in group_keys:
            if g not in cmap:
                cmap[g] = group_palette[gi % len(group_palette)]
                gi += 1
    else:
        cmap = theme.color_map(group_keys)

    accent = highlight_color or theme.accent

    def bubble_color(g):
        if focus:
            return accent if g == highlight_group else theme.muted
        return cmap.get(g, theme.accent)

    # Largest bubbles first so small ones stay visible on top. In focus mode,
    # draw the muted group first so the accent bubbles sit above them.
    idx = sorted(range(len(x_values)), key=lambda i: sizes[i], reverse=True)
    if focus:
        idx = [i for i in idx if groups[i] != highlight_group] + \
              [i for i in idx if groups[i] == highlight_group]
    order = idx
    for i in order:
        color = bubble_color(groups[i])
        svg.circle(sx(x_values[i]), sy(y_values[i]), rad(sizes[i]), fill=color,
                   fill_opacity=0.6 if focus else 0.62, stroke=color, stroke_width=1.4)
    # Direct labels on notable bubbles (secondary encoding beyond color).
    for i in range(len(x_values)):
        if labels[i] in annotate_set:
            bx, by = sx(x_values[i]), sy(y_values[i])
            svg.text(bx, by - rad(sizes[i]) - 6, str(labels[i]), font_size=11, font_weight="600",
                     fill=theme.text_primary, text_anchor="middle")

    if focus:
        _legend(svg, theme, [(highlight_group, accent), ("other", theme.muted)], left, 78)
    elif any(g is not None for g in groups):
        _legend(svg, theme, list(cmap.items()), left, 78)
    if x_label:
        svg.text((left + right) / 2, height - 14, x_label, font_size=12.5, fill=theme.text_secondary, text_anchor="middle")
    if y_label:
        yc = (top + bottom) / 2
        svg.text(18, yc, y_label, font_size=12.5, fill=theme.text_secondary, text_anchor="middle",
                 transform=f"rotate(-90 18 {yc})")
    if size_label:
        svg.text(right, 78, f"bubble size = {size_label}", font_size=11.5,
                 fill=theme.axis_label, text_anchor="end")
    svg.line(left, bottom, right, bottom, stroke=theme.axis, stroke_width=1.5)
    return svg


def dumbbell_chart(
    categories: Sequence, low: Sequence[float], high: Sequence[float], *,
    low_label="shortest", high_label="tallest", highlight=None, highlight_color=None,
    title=None, subtitle=None, unit="", decimals=None, width=None, height=None, theme="light",
) -> SVG:
    """Horizontal dumbbell chart: for each category (a row), a connector line
    joins a ``low`` and a ``high`` value, with a dot at each end (an open circle
    for the shortest, a filled dot for the tallest).

    The value axis runs horizontally and category names read down the left.
    ``highlight`` (a category name or index) switches to a focus palette: that
    dumbbell is drawn in the accent color and the rest recede to a neutral gray;
    otherwise dumbbells are colored per category. ``highlight_color`` overrides
    the accent for the highlighted dumbbell (e.g. a maroon distinct from another
    chart's accent).
    """
    theme = get_theme(theme)
    if not (len(categories) == len(low) == len(high)):
        raise ValueError("categories, low and high must be the same length")
    n = len(categories)
    hi_idx = _resolve_highlight(highlight, categories)
    top, bottom_pad, row_h = 84, 48, 42
    if height is None:
        height = top + n * row_h + bottom_pad
    left = min(300, max(90, 8 * max((len(str(c)) for c in categories), default=8)))
    right = width if width is not None else 780
    right = right - 96  # room for the tallest value label
    plot_right = right

    svg = SVG(width or 780, height, background=theme.surface, title=title or "Dumbbell chart")
    _header(svg, theme, title, subtitle)

    x = LinearScale(0, max(high) if high else 1, left, plot_right)
    band = BandScale(range(n), top, height - bottom_pad, padding=0.5)
    # Muted vertical gridlines with value ticks along the bottom.
    for t in x.ticks(5):
        tx = x(t)
        svg.line(tx, top, tx, height - bottom_pad, stroke=theme.grid, stroke_width=1)
        svg.text(tx, height - bottom_pad + 18, _format_number(t), font_size=11,
                 fill=theme.axis_label, text_anchor="middle")

    for i, (cat, lo, hi) in enumerate(zip(categories, low, high)):
        cy = band.center(i)
        xlo, xhi = x(lo), x(hi)
        accent = highlight_color or theme.accent
        color = (theme.color(i) if hi_idx is None
                 else accent if i == hi_idx else theme.muted)
        # Dumbbell: connector with an open circle at the shortest and a filled
        # dot at the tallest.
        svg.line(xlo, cy, xhi, cy, stroke=color, stroke_width=3.5, stroke_linecap="round")
        svg.circle(xlo, cy, 7, fill=theme.surface, stroke=color, stroke_width=2.5)     # shortest
        svg.circle(xhi, cy, 7.5, fill=color, stroke=theme.surface, stroke_width=1.5)   # tallest
        # Category name on the left; value labels just outside each dot.
        svg.text(left - 12, cy + 4, str(cat), font_size=12.5, fill=theme.text_secondary, text_anchor="end")
        svg.text(xlo - 11, cy + 4, f"{_format_number(lo, decimals)}{unit}",
                 font_size=10.5, fill=theme.text_secondary, text_anchor="end")
        svg.text(xhi + 12, cy + 4, f"{_format_number(hi, decimals)}{unit}",
                 font_size=11.5, font_weight="600", fill=theme.text_primary, text_anchor="start")

    svg.line(left, top, left, height - bottom_pad, stroke=theme.axis, stroke_width=1.5)
    return svg


def beeswarm_chart(
    values: Sequence[float], *, groups: Sequence | None = None,
    labels: Sequence | None = None, highlight_labels: Sequence | None = None,
    highlight_color=None, x_label=None, title=None, subtitle=None, radius=6,
    width=840, height=420, theme="light",
) -> SVG:
    """Beeswarm plot: every value is a dot placed along one axis, nudged
    vertically so dots never overlap -- a distribution you can see point by point."""
    theme = get_theme(theme)
    n = len(values)
    groups = list(groups) if groups is not None else [None] * n
    labels = list(labels) if labels is not None else [None] * n
    hi_set = set(highlight_labels or [])

    top, left, right = 100, 40, width - 30
    axis_y = (top + height - 50) / 2 + 10
    svg = SVG(width, height, background=theme.surface, title=title or "Beeswarm plot")
    _header(svg, theme, title, subtitle)

    lo, hi = min(values), max(values)
    d = (hi - lo) * 0.05 or 1
    x = LinearScale(lo - d, hi + d, left, right)
    for t in x.ticks(6):
        tx = x(t)
        svg.line(tx, top, tx, height - 40, stroke=theme.grid, stroke_width=1)
        svg.text(tx, height - 22, _format_number(t), font_size=11, fill=theme.axis_label, text_anchor="middle")

    cmap = theme.color_map([g for g in groups if g is not None])
    placed: list[tuple[float, float]] = []
    step = radius + 1
    order = sorted(range(n), key=lambda i: values[i])
    for i in order:
        px = x(values[i])
        py = _swarm_y(px, axis_y, placed, radius, step, top + 6, height - 52)
        placed.append((px, py))
        is_hi = labels[i] in hi_set
        # With no groups, dots are a single neutral hue (one accent for the
        # highlighted few) -- one color to read in black & white.
        base = cmap.get(groups[i]) if groups[i] is not None else theme.muted
        color = (highlight_color or theme.accent) if is_hi else base
        svg.circle(px, py, radius + (1 if is_hi else 0), fill=color, fill_opacity=0.82,
                   stroke=theme.surface, stroke_width=1.2)
        if is_hi and labels[i] is not None:
            svg.text(px, py - radius - 6, str(labels[i]), font_size=11, font_weight="600",
                     fill=theme.text_primary, text_anchor="middle")

    if any(g is not None for g in groups):
        _legend(svg, theme, list(cmap.items()), left, 76)
    if x_label:
        svg.text((left + right) / 2, height - 6, x_label, font_size=12.5, fill=theme.text_secondary, text_anchor="middle")
    return svg


# -- helpers ----------------------------------------------------------------
def _swarm_y(px, center, placed, radius, step, y_min, y_max):
    """Find a y near ``center`` at column ``px`` that doesn't collide."""
    min_d2 = (2 * radius) ** 2
    neighbors = [p for p in placed if abs(p[0] - px) < 2 * radius]
    k = 0
    while True:
        for offset in ((0,) if k == 0 else (k * step, -k * step)):
            y = center + offset
            if y < y_min or y > y_max:
                continue
            if all((px - nx) ** 2 + (y - ny) ** 2 >= min_d2 for nx, ny in neighbors):
                return y
        k += 1
        if k * step > (y_max - y_min):
            return center  # fallback: give up and stack at center


def _wedge(cx, cy, ri, ro, a0, a1) -> str:
    large = 1 if (a1 - a0) > math.pi else 0
    x0, y0 = _polar(cx, cy, ro, a0)
    x1, y1 = _polar(cx, cy, ro, a1)
    xi1, yi1 = _polar(cx, cy, ri, a1)
    xi0, yi0 = _polar(cx, cy, ri, a0)
    return (f"M {x0:.2f} {y0:.2f} A {ro:.2f} {ro:.2f} 0 {large} 1 {x1:.2f} {y1:.2f} "
            f"L {xi1:.2f} {yi1:.2f} A {ri:.2f} {ri:.2f} 0 {large} 0 {xi0:.2f} {yi0:.2f} Z")


def _resolve_highlight(highlight, labels):
    if highlight is None:
        return None
    if isinstance(highlight, int) and not isinstance(highlight, bool):
        return highlight
    labels = list(labels)
    if highlight in labels:
        return labels.index(highlight)
    raise ValueError(f"highlight {highlight!r} is not an index or one of the labels")
