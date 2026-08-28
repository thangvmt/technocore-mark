"""Text as outlines, so a board renders the same everywhere with no font installed."""
from __future__ import annotations

import pathlib

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = pathlib.Path(__file__).parent

def _find(name: str) -> pathlib.Path:
    """Fonts live beside the source in the working tree and in ../fonts in the
    published repo. Look in both rather than hard-coding one layout."""
    for candidate in (HERE / name, HERE.parent / "fonts" / name):
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"{name} not found beside {HERE} or in ../fonts")

FACES = {False: _find("SpaceMono-Regular.ttf"), True: _find("SpaceMono-Bold.ttf")}
_CACHE: dict[bool, TTFont] = {}


def _face(bold: bool) -> TTFont:
    if bold not in _CACHE:
        _CACHE[bold] = TTFont(FACES[bold])
    return _CACHE[bold]


def advance(text: str, size: float, bold: bool = False) -> float:
    font = _face(bold)
    k = size / font["head"].unitsPerEm
    glyphs, cmap = font.getGlyphSet(), font.getBestCmap()
    return sum(glyphs[cmap[ord(c)]].width for c in text if ord(c) in cmap) * k


def text_path(x: float, y: float, text: str, size: float, fill: str,
              anchor: str = "start", opacity: float = 1.0, bold: bool = False) -> str:
    """Outlined text. y is the baseline, matching SVG <text> semantics."""
    font = _face(bold)
    k = size / font["head"].unitsPerEm
    glyphs, cmap = font.getGlyphSet(), font.getBestCmap()
    adv = advance(text, size, bold)
    dx = {"start": 0.0, "middle": -adv / 2, "end": -adv}[anchor]
    parts, pen_x = [], 0.0
    for ch in text:
        if ord(ch) not in cmap:
            continue
        g = glyphs[cmap[ord(ch)]]
        pen = SVGPathPen(glyphs)
        g.draw(TransformPen(pen, (k, 0, 0, -k, pen_x, 0)))
        d = pen.getCommands()
        if d:
            parts.append(d)
        pen_x += g.width * k
    return (f'<g transform="translate({x + dx:.2f},{y:.2f})">'
            f'<path fill="{fill}" fill-opacity="{opacity}" d="{"".join(parts)}"/></g>')
