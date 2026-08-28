"""Read the FLOP Chip master and recover the grid it was drawn on.

Nothing here is estimated. The path is walked, its anchor points are clustered
into grid lines, and the constants fall out of the spacing between them.
"""
from __future__ import annotations

import pathlib
import re
import urllib.request
from dataclasses import dataclass

MASTER_URL = "https://flop.finance/assets/flop-chip-favicon.svg"
VENDORED = pathlib.Path(__file__).parent / "chip_master.txt"
TOKEN = re.compile(r"([MmLlHhVvCcSsQqTtAaZz])|(-?\d*\.?\d+(?:[eE][-+]?\d+)?)")
HTTP_TIMEOUT_SECONDS = 30
# flop.finance sits behind a CDN that refuses urllib's default agent with a 403.
USER_AGENT = "technocore-mark-verify/1.0 (+https://github.com/thangvmt/technocore-mark)"


def fetch_master(timeout: int = HTTP_TIMEOUT_SECONDS) -> tuple[str, str, str]:
    """(viewBox, path data, source). Falls back to the vendored copy offline."""
    try:
        request = urllib.request.Request(MASTER_URL, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(request, timeout=timeout) as response:
            svg = response.read().decode("utf-8")
        view = re.search(r'viewBox="([^"]+)"', svg).group(1)
        data = max(re.findall(r'<path[^>]*\sd="([^"]+)"', svg), key=len)
        return view, data, MASTER_URL
    except Exception:
        view, data = VENDORED.read_text().split("\n")
        return view, data, f"{VENDORED.name} (offline)"


def anchors(data: str) -> list[tuple[float, float]]:
    return [point for _, point, _ in walk(data)]


def walk(data: str) -> list[tuple[str, tuple[float, float], tuple[float, float]]]:
    """(command, absolute end point, delta) for every segment.

    Only on-curve points are recorded; control points are not grid evidence.
    The deltas are what the corner radius is read from."""
    tokens = [c or n for c, n in TOKEN.findall(data)]
    points: list[tuple[str, tuple[float, float], tuple[float, float]]] = []
    index, command = 0, ""
    x = y = start_x = start_y = 0.0
    previous_x = previous_y = 0.0

    def number() -> float:
        nonlocal index
        value = float(tokens[index])
        index += 1
        return value

    while index < len(tokens):
        if tokens[index].isalpha():
            command = tokens[index]
            index += 1
            if command in "Zz":
                x, y = start_x, start_y
                points.append(("Z", (x, y), (x - previous_x, y - previous_y)))
                previous_x, previous_y = x, y
                continue
        relative = command.islower()
        letter = command.upper()
        if letter == "M":
            nx, ny = number(), number()
            x, y = (x + nx, y + ny) if relative else (nx, ny)
            start_x, start_y = x, y
            command = "l" if relative else "L"
        elif letter == "L":
            nx, ny = number(), number()
            x, y = (x + nx, y + ny) if relative else (nx, ny)
        elif letter == "H":
            nx = number()
            x = x + nx if relative else nx
        elif letter == "V":
            ny = number()
            y = y + ny if relative else ny
        elif letter in "CS":
            values = [number() for _ in range(6 if letter == "C" else 4)]
            ex, ey = values[-2], values[-1]
            x, y = (x + ex, y + ey) if relative else (ex, ey)
        else:
            raise ValueError(f"unhandled path command {letter}")
        points.append((letter, (x, y), (x - previous_x, y - previous_y)))
        previous_x, previous_y = x, y
    return points


def lines(values: list[float], tolerance: float = 1.2, min_hits: int = 5) -> list[float]:
    """Cluster coordinates into grid lines, keeping only well-attested ones."""
    groups: list[list[float]] = []
    for value in sorted(values):
        if groups and value - groups[-1][-1] <= tolerance:
            groups[-1].append(value)
        else:
            groups.append([value])
    return [round(sum(g) / len(g), 2) for g in groups if len(g) >= min_hits]


@dataclass(frozen=True)
class Grid:
    block: float          # the inner block, the consistent one
    gutter: float         # the inner gutter
    radius: float         # the one corner radius in the artwork
    outer_blocks: tuple[float, ...]
    width: float
    height: float

    @property
    def gutter_ratio(self) -> float:
        return self.gutter / self.block

    @property
    def radius_ratio(self) -> float:
        return self.radius / self.block

    @property
    def out_of_square(self) -> float:
        return abs(self.width - self.height) / self.width


def measure(data: str) -> Grid:
    points = anchors(data)
    xs, ys = [p[0] for p in points], [p[1] for p in points]
    gx, gy = lines(xs), lines(ys)
    spans = [round(b - a, 2) for a, b in zip(gx, gx[1:])]
    # Column spans and gutters alternate along the row of grid lines. The
    # gutters are the short ones; the blocks are what is left.
    gutters = sorted(s for s in spans if s < 40)
    blocks = sorted(s for s in spans if s >= 40)
    inner_gutter = round(sum(gutters[-2:]) / 2, 2) if len(gutters) >= 2 else gutters[0]
    inner_block = min(blocks)
    radius = _corner_radius(data)
    return Grid(
        block=inner_block,
        gutter=inner_gutter,
        radius=radius,
        outer_blocks=tuple(b for b in blocks if b > inner_block + 1),
        width=round(max(xs) - min(xs), 2),
        height=round(max(ys) - min(ys), 2),
    )


def _corner_radius(data: str) -> float:
    """A rounded corner is a cubic whose end point moves by the radius in both
    axes. Collect those, and take the value that repeats most."""
    quarters = [
        round(abs(dx), 2)
        for letter, _, (dx, dy) in walk(data)
        if letter in "CS" and abs(abs(dx) - abs(dy)) < 0.05 and abs(dx) > 1
    ]
    if not quarters:
        raise ValueError("no quarter-arc corners found")
    return max(set(quarters), key=quarters.count)
