"""Scales map data values into pixel coordinates."""

from __future__ import annotations

import math
from typing import Sequence


class LinearScale:
    """Map a numeric ``[domain_min, domain_max]`` onto a pixel ``[range_min, range_max]``."""

    def __init__(self, domain_min: float, domain_max: float, range_min: float, range_max: float):
        if domain_min == domain_max:
            domain_min -= 0.5
            domain_max += 0.5
        self.domain_min = domain_min
        self.domain_max = domain_max
        self.range_min = range_min
        self.range_max = range_max

    def scale(self, value: float) -> float:
        t = (value - self.domain_min) / (self.domain_max - self.domain_min)
        return self.range_min + t * (self.range_max - self.range_min)

    def __call__(self, value: float) -> float:
        return self.scale(value)

    def ticks(self, count: int = 5) -> list[float]:
        return nice_ticks(self.domain_min, self.domain_max, count)


class BandScale:
    """Evenly spaced positions for a list of categories, with inner padding."""

    def __init__(self, categories: Sequence, range_min: float, range_max: float, padding: float = 0.2):
        self.categories = list(categories)
        self.range_min = range_min
        self.range_max = range_max
        n = max(1, len(self.categories))
        self.step = (range_max - range_min) / n
        self.bandwidth = self.step * (1 - padding)
        self._index = {c: i for i, c in enumerate(self.categories)}

    def position(self, category) -> float:
        i = self._index[category]
        return self.range_min + i * self.step + (self.step - self.bandwidth) / 2

    def center(self, category) -> float:
        return self.position(category) + self.bandwidth / 2


def nice_ticks(lo: float, hi: float, count: int = 5) -> list[float]:
    """Return ~``count`` rounded, evenly spaced tick values spanning ``[lo, hi]``."""
    if count < 1:
        raise ValueError("count must be >= 1")
    if lo == hi:
        return [lo]
    if lo > hi:
        lo, hi = hi, lo
    span = _nice(hi - lo, False)
    step = _nice(span / (count - 1), True)
    nice_lo = math.floor(lo / step) * step
    nice_hi = math.ceil(hi / step) * step
    ticks, value = [], nice_lo
    while value <= nice_hi + step / 2:
        ticks.append(round(value, 10))
        value += step
    return ticks


def _nice(value: float, round_result: bool) -> float:
    if value == 0:
        return 0
    exp = math.floor(math.log10(abs(value)))
    frac = abs(value) / (10 ** exp)
    if round_result:
        nice = 1 if frac < 1.5 else 2 if frac < 3 else 5 if frac < 7 else 10
    else:
        nice = 1 if frac <= 1 else 2 if frac <= 2 else 5 if frac <= 5 else 10
    return nice * (10 ** exp)
