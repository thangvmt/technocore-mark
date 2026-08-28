"""Lockups: the mark plus the name, as one object.

The wordmark is Space Mono Bold, the brand's own display face, outlined
straight from the font binary. It is not new artwork and it is not redrawn:
the outlines below are the font's, unmodified except for a uniform scale.
"""
from __future__ import annotations

import pathlib
from dataclasses import dataclass

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

from technocore_mark import (ACCENT, BASE, BLOCK, BLUE, ELECTRIC_GREEN,
                             GREY, ICE_WHITE, Mark, out_dir)

from textpath import _find

FONT = _find("SpaceMono-Bold.ttf")
WORD = "TECHNOCORE"
GAP = BLOCK * 1.50                # mark to word, in block units
CLEAR = BLOCK * 4.0               # 4X on every side, X = one block


@dataclass(frozen=True)
class Wordmark:
    text: str = WORD
    cap: float = 313.72           # set to the mark's body height by the caller

    def _font(self) -> TTFont:
        return TTFont(FONT)

    def outline(self) -> tuple[str, float]:
        """Return (path data, advance width) with the cap height as asked."""
        font = self._font()
        upem = font["head"].unitsPerEm
        cap_units = font["OS/2"].sCapHeight
        scale = self.cap / cap_units
        glyphs = font.getGlyphSet()
        cmap = font.getBestCmap()
        parts, pen_x = [], 0.0
        for ch in self.text:
            name = cmap[ord(ch)]
            g = glyphs[name]
            pen = SVGPathPen(glyphs)
            # y flips: font space is up-positive, SVG is down-positive, and the
            # baseline sits at the cap height below the top of the box.
            g.draw(TransformPen(pen, (scale, 0, 0, -scale, pen_x, self.cap)))
            d = pen.getCommands()
            if d:
                parts.append(d)
            pen_x += g.width * scale
        return "".join(parts), pen_x


LOCKUPS = {
    # name:            (word ink,  mark ink,        ground)
    "primary": (BASE, ACCENT, ICE_WHITE),
    "reverse": (ICE_WHITE, ACCENT, BASE),
    "print-alternate": (BASE, BLUE, ICE_WHITE),
    "product": (BASE, ELECTRIC_GREEN, ICE_WHITE),
    "one-color-base": (BASE, BASE, ICE_WHITE),
    "one-color-ice": (ICE_WHITE, ICE_WHITE, BASE),
}


def lockup_svg(word_ink: str, mark_ink: str, ground: str | None,
               clear: float = CLEAR) -> str:
    m = Mark()
    word = Wordmark(cap=m.body)
    d, adv = word.outline()
    w = clear * 2 + m.size + GAP + adv
    h = clear * 2 + m.size
    bg = f'<rect width="{w:.4f}" height="{h:.4f}" fill="{ground}"/>' if ground else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.4f} {h:.4f}">'
        f"{bg}"
        f'<g transform="translate({clear:.4f},{clear:.4f})">'
        f'<path fill="{mark_ink}" fill-rule="evenodd" d="{m.path()}"/>'
        f'<g transform="translate({m.size + GAP:.4f},0)">'
        f'<path fill="{word_ink}" d="{d}"/></g></g></svg>'
    )


if __name__ == "__main__":
    out = out_dir()
    out.mkdir(exist_ok=True)
    for name, (wi, mi, gr) in LOCKUPS.items():
        (out / f"technocore_lockup_{name}.svg").write_text(lockup_svg(wi, mi, gr))
    print("wrote", len(LOCKUPS), "lockups to", out)
