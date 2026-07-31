"""Color palettes for vizcraft.

The categorical palette is colorblind-safe in a fixed, validated hue order
(worst adjacent CVD deltaE 9.1 light / 8.4 dark). ``accent`` carries emphasis and
``muted`` recedes everything else. Both a light and a dark theme are provided.
"""

from __future__ import annotations

from dataclasses import dataclass

_CATEGORICAL_LIGHT = ("#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948")
_CATEGORICAL_DARK = ("#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300", "#9085e9", "#e66767")


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
    name="light", surface="#fcfcfb", accent="#2a78d6", muted="#c4c2ba",
    text_primary="#141414", text_secondary="#4c4b47", axis_label="#7a7973",
    grid="#ecece6", axis="#c9c8bf", categorical=_CATEGORICAL_LIGHT,
)

DARK = Theme(
    name="dark", surface="#161620", accent="#4f9bf0", muted="#565564",
    text_primary="#f4f5fa", text_secondary="#bdbdcb", axis_label="#8a8a99",
    grid="#282836", axis="#3a3a4a", categorical=_CATEGORICAL_DARK,
)

_THEMES = {"light": LIGHT, "dark": DARK}


def get_theme(theme: "str | Theme") -> Theme:
    if isinstance(theme, Theme):
        return theme
    try:
        return _THEMES[theme]
    except KeyError:
        raise ValueError(f"unknown theme {theme!r}; use 'light', 'dark', or a Theme") from None
