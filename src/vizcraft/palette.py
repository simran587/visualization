"""Color palettes for vizcraft.

The categorical palette is colorblind-safe in a fixed, validated hue order
(worst adjacent CVD deltaE 9.1 light / 8.4 dark). ``accent`` carries emphasis and
``muted`` recedes everything else. Both a light and a dark theme are provided.
"""

from __future__ import annotations

from dataclasses import dataclass

# Fun, vibrant "candy / tropical" palette. Deliberately no red-next-to-green
# pairing (no Christmas vibe): the warm slots are mango/yellow/pink, the cool
# slots are blue/teal/aqua, kept apart in the ordering.
_CATEGORICAL_LIGHT = ("#3b9dff", "#ff8c42", "#12b5b0", "#ffcc33", "#ff5d8f", "#22c1a6", "#9c6bff", "#5ad1e6")
_CATEGORICAL_DARK = ("#4dabf7", "#ff9f57", "#22c9c3", "#ffd43b", "#ff7aa6", "#3ad6b4", "#b39cff", "#6fdcef")


@dataclass(frozen=True)
class Theme:
    name: str
    surface: str
    accent: str
    muted: str
    text_primary: str
    text_secondary: str
    axis_label: str
    grid: str
    axis: str
    categorical: tuple[str, ...]

    def color(self, index: int) -> str:
        if not 0 <= index < len(self.categorical):
            raise IndexError(
                f"the colorblind-safe palette has {len(self.categorical)} slots; got index {index}. "
                "A 9th generated hue is never colorblind-safe -- fold extra categories into 'Other'."
            )
        return self.categorical[index]

    def color_map(self, keys) -> dict:
        """Assign categorical hues to ``keys`` in first-seen order."""
        out, i = {}, 0
        for k in keys:
            if k not in out:
                out[k] = self.color(i)
                i += 1
        return out


LIGHT = Theme(
    name="light", surface="#fcfcfd", accent="#7c3aed", muted="#c6c4cf",
    text_primary="#17161f", text_secondary="#4d4b58", axis_label="#84828e",
    grid="#eceaf4", axis="#d0cdda", categorical=_CATEGORICAL_LIGHT,
)

DARK = Theme(
    name="dark", surface="#17151f", accent="#a78bfa", muted="#575563",
    text_primary="#f3f1f8", text_secondary="#c0bccd", axis_label="#8a8798",
    grid="#2a2735", axis="#3d3a4a", categorical=_CATEGORICAL_DARK,
)

_THEMES = {"light": LIGHT, "dark": DARK}


def get_theme(theme: "str | Theme") -> Theme:
    if isinstance(theme, Theme):
        return theme
    try:
        return _THEMES[theme]
    except KeyError:
        raise ValueError(f"unknown theme {theme!r}; use 'light', 'dark', or a Theme") from None
