"""Recognizable building silhouettes for the skyline chart.

Each supertall in the bundled dataset gets a distinct, hand-tuned silhouette so
that -- for example -- Burj Khalifa reads as Burj Khalifa (a stepped taper to a
long spire) rather than a plain bar. Shapes are approximations tuned to be
recognizable at a glance, not architectural drawings.

A silhouette is described by a symmetric *profile*: a list of
``(y_fraction, half_width_fraction)`` points from base (0.0) to top (1.0), where
the half-width is a fraction of the building's slot width. :func:`draw_building`
maps a profile into a filled SVG path at a given position and size, plus any
extra detail elements (a clock face, a facade aperture, ...).
"""

from __future__ import annotations

from typing import Callable

# -- symmetric profiles: (y from base 0 -> top 1, half-width fraction) -------
_PROFILES: dict[str, list[tuple[float, float]]] = {
    # Stepped setbacks tapering to a slender spire.
    "Burj Khalifa": [
        (0, .50), (.13, .50), (.13, .43), (.27, .43), (.27, .35), (.42, .35),
        (.42, .28), (.55, .28), (.55, .21), (.67, .21), (.67, .15), (.77, .15),
        (.77, .09), (.85, .09), (.85, .035), (.90, .035), (.90, .014), (1.0, .006),
    ],
    # Faceted taper with a very long, thin spire.
    "Merdeka 118": [
        (0, .44), (.58, .20), (.68, .13), (.72, .05), (.745, .028), (.77, .016), (1.0, .005),
    ],
    # Clock tower: broad shaft, small taper, pinnacle (clock added separately).
    "Abraj Al-Bait Clock Tower": [
        (0, .42), (.64, .40), (.72, .40), (.72, .32), (.80, .32), (.80, .23),
        (.83, .23), (.83, .09), (.87, .09), (.87, .035), (.91, .035), (.91, .014), (1.0, .006),
    ],
    # Long straight taper to a sharp spike.
    "Ping An Finance Center": [
        (0, .40), (.85, .08), (.885, .05), (.90, .02), (1.0, .006),
    ],
    # Smooth convex cone to a point.
    "Lotte World Tower": [
        (0, .40), (.16, .36), (.33, .31), (.50, .25), (.68, .18), (.83, .11), (.93, .055), (1.0, .012),
    ],
    # Obelisk taper, small parapet, tall thin mast.
    "One World Trade Center": [
        (0, .42), (.80, .14), (.80, .028), (.82, .028), (.82, .013), (1.0, .008),
    ],
    # Three setbacks to a flat top.
    "Guangzhou CTF Finance Centre": [
        (0, .42), (.34, .42), (.34, .345), (.60, .345), (.60, .275), (.82, .275), (.82, .215), (1.0, .215),
    ],
    # Gentle concave taper to a soft, rounded tip.
    "Tianjin CTF Finance Centre": [
        (0, .40), (.20, .35), (.42, .29), (.62, .22), (.80, .145), (.90, .09), (.965, .045), (1.0, .018),
    ],
    # China Zun: flared base and top with a narrow waist.
    "CITIC Tower (China Zun)": [
        (0, .44), (.10, .37), (.30, .30), (.50, .255), (.70, .30), (.90, .37), (1.0, .40),
    ],
    # Tapered, slim flat top (aperture added separately).
    "Shanghai World Financial Center": [
        (0, .40), (.5, .30), (.98, .155), (1.0, .145),
    ],
    # Tapered with a stepped, sloped crown.
    "International Commerce Centre": [
        (0, .42), (.76, .16), (.85, .13), (.85, .10), (.93, .075), (.93, .05), (1.0, .028),
    ],
    # Tapered shaft, crown, spire.
    "The Exchange 106": [
        (0, .40), (.72, .15), (.80, .11), (.80, .05), (.82, .028), (1.0, .006),
    ],
    # Super-slim "pencil" slab, slight base flare, flat top.
    "Central Park Tower": [
        (0, .17), (.06, .145), (.06, .135), (1.0, .13),
    ],
}


def _taipei_profile() -> list[tuple[float, float]]:
    """Generate Taipei 101's pedestal + eight flared tiers + pinnacle."""
    prof: list[tuple[float, float]] = [(0, .32), (.10, .32), (.10, .22)]
    y, seg = .13, .083
    for _ in range(8):
        prof.append((y, .15))                 # narrow segment base
        prof.append((y + seg * .92, .235))    # flare outward to the top
        prof.append((y + seg * .92, .15))     # step back in
        y += seg
    prof += [(y, .05), (.99, .006)]           # pinnacle spire
    return prof


_PROFILES["Taipei 101"] = _taipei_profile()


# -- path helpers -----------------------------------------------------------
def _poly(cx: float, base: float, w: float, h: float, profile) -> str:
    """Build a mirrored polygon path 'd' from a symmetric profile."""
    left = [(cx - hw * w, base - yf * h) for yf, hw in profile]
    right = [(cx + hw * w, base - yf * h) for yf, hw in reversed(profile)]
    pts = left + right
    return "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts) + " Z"


def _shanghai(cx, base, w, h, color, surface) -> list[str]:
    """Shanghai Tower: an asymmetric curved taper with a twist and rounded top."""
    off = 0.06 * w
    d = (
        f"M {cx - .42 * w:.2f} {base:.2f} "
        f"C {cx - .34 * w:.2f} {base - .45 * h:.2f} {cx - .18 * w + off:.2f} {base - .78 * h:.2f} "
        f"{cx - .16 * w + off:.2f} {base - .95 * h:.2f} "
        f"Q {cx + off:.2f} {base - 1.0 * h:.2f} {cx + .16 * w + off:.2f} {base - .95 * h:.2f} "
        f"C {cx + .20 * w + off:.2f} {base - .78 * h:.2f} {cx + .34 * w:.2f} {base - .45 * h:.2f} "
        f"{cx + .42 * w:.2f} {base:.2f} Z"
    )
    return [f'<path d="{d}" fill="{color}"/>']


def _with_clock(cx, base, w, h, color, surface) -> list[str]:
    """Abraj Al-Bait: shaft silhouette plus a large clock face."""
    els = [f'<path d="{_poly(cx, base, w, h, _PROFILES["Abraj Al-Bait Clock Tower"])}" fill="{color}"/>']
    cyk, r = base - 0.60 * h, 0.15 * w
    els.append(f'<circle cx="{cx:.2f}" cy="{cyk:.2f}" r="{r:.2f}" fill="{surface}" stroke="{color}" stroke-width="1.5"/>')
    els.append(f'<line x1="{cx:.2f}" y1="{cyk:.2f}" x2="{cx:.2f}" y2="{cyk - r * .6:.2f}" stroke="{color}" stroke-width="1.3"/>')
    els.append(f'<line x1="{cx:.2f}" y1="{cyk:.2f}" x2="{cx + r * .5:.2f}" y2="{cyk:.2f}" stroke="{color}" stroke-width="1.3"/>')
    return els


def _with_aperture(cx, base, w, h, color, surface) -> list[str]:
    """Shanghai World Financial Center: tapered tower with its trapezoidal void."""
    els = [f'<path d="{_poly(cx, base, w, h, _PROFILES["Shanghai World Financial Center"])}" fill="{color}"/>']
    y0, y1 = base - 0.80 * h, base - 0.965 * h
    ap = (f"M {cx - .085 * w:.2f} {y0:.2f} L {cx + .085 * w:.2f} {y0:.2f} "
          f"L {cx + .125 * w:.2f} {y1:.2f} L {cx - .125 * w:.2f} {y1:.2f} Z")
    els.append(f'<path d="{ap}" fill="{surface}"/>')
    return els


# -- registry ---------------------------------------------------------------
SPECIAL: dict[str, Callable] = {
    "Shanghai Tower": _shanghai,
    "Abraj Al-Bait Clock Tower": _with_clock,
    "Shanghai World Financial Center": _with_aperture,
}

# A generic tapered tower with a mast, for any building without a custom shape.
_GENERIC = [(0, .40), (.78, .16), (.80, .05), (.82, .03), (1.0, .01)]

SHORT_NAMES = {
    "Burj Khalifa": "Burj Khalifa",
    "Merdeka 118": "Merdeka 118",
    "Shanghai Tower": "Shanghai Tower",
    "Abraj Al-Bait Clock Tower": "Abraj Al-Bait",
    "Ping An Finance Center": "Ping An",
    "Lotte World Tower": "Lotte World",
    "One World Trade Center": "One WTC",
    "Guangzhou CTF Finance Centre": "Guangzhou CTF",
    "Tianjin CTF Finance Centre": "Tianjin CTF",
    "CITIC Tower (China Zun)": "CITIC / Zun",
    "Taipei 101": "Taipei 101",
    "Shanghai World Financial Center": "Shanghai WFC",
    "International Commerce Centre": "ICC (HK)",
    "The Exchange 106": "Exchange 106",
    "Central Park Tower": "Central Park",
}


def draw_building(name, cx, base, w, h, color, surface) -> list[str]:
    """Return the SVG elements for ``name``'s silhouette at the given box."""
    if name in SPECIAL:
        return SPECIAL[name](cx, base, w, h, color, surface)
    profile = _PROFILES.get(name, _GENERIC)
    return [f'<path d="{_poly(cx, base, w, h, profile)}" fill="{color}"/>']


def short_name(name) -> str:
    return SHORT_NAMES.get(name, str(name))
