"""vizcraft -- a zero-dependency library of creative SVG charts.

Beyond the usual bars and pies: lollipop, radial bar, bubble, dumbbell, and
beeswarm charts, each rendering to plain SVG with a colorblind-safe palette and
light/dark themes. Ships with the tallest-buildings dataset.

    import vizcraft as vc

    data = vc.load_tallest_buildings()
    top = data.top("height_m", 15)
    vc.lollipop_chart(
        top.column("building"), top.column("height_m"),
        title="The 15 tallest buildings on Earth",
        highlight="Burj Khalifa", unit=" m",
    ).save("tallest.svg")

Public API:

* Data:   :class:`Dataset`, :func:`load_tallest_buildings`
* Charts: :func:`lollipop_chart`, :func:`radial_bar_chart`, :func:`bubble_chart`,
          :func:`dumbbell_chart`, :func:`beeswarm_chart`
* Theming: :data:`LIGHT`, :data:`DARK`, :func:`get_theme`
"""

from __future__ import annotations

from .charts import (
    bar_chart,
    beeswarm_chart,
    bubble_chart,
    dumbbell_chart,
    lollipop_chart,
    radial_bar_chart,
    skyline_chart,
)
from .dataset import Dataset, load_tallest_buildings
from .palette import DARK, LIGHT, Theme, get_theme
from .svg import SVG

__version__ = "0.1.1"

__all__ = [
    "Dataset",
    "load_tallest_buildings",
    "skyline_chart",
    "lollipop_chart",
    "bar_chart",
    "radial_bar_chart",
    "bubble_chart",
    "dumbbell_chart",
    "beeswarm_chart",
    "SVG",
    "Theme",
    "LIGHT",
    "DARK",
    "get_theme",
    "__version__",
]
