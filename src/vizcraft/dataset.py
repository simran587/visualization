"""A tiny in-memory tabular dataset -- just enough to feed the charts.

Dependency-free: column names plus row dicts, with the operations the charts
need. Numeric cells are parsed to ``int``/``float`` on load; blanks and ``NA``
become ``None`` so missing data is explicit.
"""

from __future__ import annotations

import csv
from importlib import resources
from pathlib import Path
from typing import Any, Callable, Sequence

_NA = {"", "na", "n/a", "nan", "null", "none"}


def _coerce(value: str) -> Any:
    if value is None or value.strip().lower() in _NA:
        return None
    value = value.strip()
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


class Dataset:
    def __init__(self, rows: Sequence[dict], columns: Sequence[str] | None = None):
        self.rows: list[dict] = [dict(r) for r in rows]
        self.columns = list(columns) if columns is not None else (list(self.rows[0].keys()) if self.rows else [])

    @classmethod
    def from_csv(cls, path: "str | Path", coerce: bool = True) -> "Dataset":
        with open(path, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            columns = list(reader.fieldnames or [])
            rows = [{k: (_coerce(v) if coerce else v) for k, v in raw.items()} for raw in reader]
        return cls(rows, columns)

    def __len__(self):
        return len(self.rows)

    def __iter__(self):
        return iter(self.rows)

    def __getitem__(self, i):
        return self.rows[i]

    def column(self, name: str) -> list:
        self._require(name)
        return [r.get(name) for r in self.rows]

    def unique(self, name: str) -> list:
        self._require(name)
        seen: dict = {}
        for r in self.rows:
            seen.setdefault(r.get(name), None)
        return list(seen.keys())

    def head(self, n: int = 5) -> "Dataset":
        return Dataset(self.rows[:n], self.columns)

    def filter(self, predicate: Callable[[dict], bool]) -> "Dataset":
        return Dataset([r for r in self.rows if predicate(r)], self.columns)

    def dropna(self, *names: str) -> "Dataset":
        for n in names:
            self._require(n)
        return Dataset([r for r in self.rows if all(r.get(n) is not None for n in names)], self.columns)

    def sort_by(self, name: str, reverse: bool = False) -> "Dataset":
        self._require(name)
        return Dataset(sorted(self.rows, key=lambda r: (r.get(name) is None, r.get(name)), reverse=reverse), self.columns)

    def top(self, name: str, n: int) -> "Dataset":
        return self.dropna(name).sort_by(name, reverse=True).head(n)

    def groups(self, key: str) -> dict[Any, "Dataset"]:
        """Split into ``{key_value: Dataset}`` preserving first-seen order."""
        self._require(key)
        out: dict[Any, list] = {}
        for r in self.rows:
            out.setdefault(r.get(key), []).append(r)
        return {k: Dataset(v, self.columns) for k, v in out.items()}

    def _require(self, name: str) -> None:
        if name not in self.columns:
            raise KeyError(f"unknown column {name!r}; available columns: {self.columns}")

    def __repr__(self):  # pragma: no cover
        return f"Dataset(rows={len(self.rows)}, columns={self.columns})"

    def _repr_html_(self, max_rows: int = 50) -> str:
        """Render as an HTML table so ``data.head()`` displays in Jupyter/Colab."""
        from html import escape

        def cell(v):
            return "" if v is None else escape(str(v))

        header = "".join(f"<th style='text-align:left;padding:3px 10px'>{escape(str(c))}</th>"
                         for c in self.columns)
        body = []
        for r in self.rows[:max_rows]:
            tds = "".join(f"<td style='padding:3px 10px'>{cell(r.get(c))}</td>" for c in self.columns)
            body.append(f"<tr>{tds}</tr>")
        more = ("" if len(self.rows) <= max_rows
                else f"<div style='color:#888;font-size:12px;margin-top:4px'>… {len(self.rows) - max_rows} more rows</div>")
        return (
            "<table style='border-collapse:collapse;font-family:system-ui,sans-serif;font-size:13px'>"
            f"<thead><tr style='border-bottom:1px solid #ccc'>{header}</tr></thead>"
            f"<tbody>{''.join(body)}</tbody></table>{more}"
        )

    def preview(self, n: int = 5) -> str:
        """A plain-text table of the first ``n`` rows (for the console)."""
        rows = self.rows[:n]
        widths = {c: max(len(str(c)), *(len(str(r.get(c, ""))) for r in rows)) if rows else len(str(c))
                  for c in self.columns}
        line = lambda vals: "  ".join(str(v).ljust(widths[c]) for c, v in zip(self.columns, vals))
        out = [line(self.columns), line(["-" * widths[c] for c in self.columns])]
        for r in rows:
            out.append(line(["" if r.get(c) is None else r.get(c) for c in self.columns]))
        return "\n".join(out)


def load_tallest_buildings() -> Dataset:
    """Load the bundled ``tallest_buildings.csv`` (31 tallest structures).

    Columns: ``rank``, ``building``, ``city``, ``country``, ``height_m``,
    ``height_ft``, ``year_completed``, ``floors``, ``use_type``. The Eiffel
    Tower's ``floors`` is ``None`` (it is a tower, not a floored building).
    """
    src = resources.files("vizcraft").joinpath("datasets", "tallest_buildings.csv")
    with resources.as_file(src) as path:
        return Dataset.from_csv(path)
