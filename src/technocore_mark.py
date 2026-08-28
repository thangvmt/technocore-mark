"""Technocore mark — generated, not drawn.

Every number here is either measured on the delivered FLOP Chip master
(docs/brand/official/Chip/svg/flop_Chip_Accent.svg, served unaltered as
flop.finance/assets/flop-chip-favicon.svg) or quoted from FLOP Logo & Usage
Standards V1.0 as republished in DESIGN.md. Nothing is eyeballed.

Run this file and the mark is reproduced byte for byte.
"""
from __future__ import annotations

from dataclasses import dataclass

# --- measured on the Chip master --------------------------------------------
# Recovered by walking the master path and clustering its anchor points, not by
# eye: see verify.py, which re-derives all of this from the live file.
#
# The delivered artwork is not uniform. Its inner blocks measure 115.27 with
# 10.22 gutters; the two outer columns come back ~2.3% wider, and the octagon
# is 496.06 wide by 485.06 tall for a mark the standard calls "eight modules
# square". This mark is built on the INNER grid, which is the consistent one.
BLOCK = 100.0
GUTTER = BLOCK * 0.08857          # 10.21 / 115.27, inner gutter over inner block
PITCH = BLOCK + GUTTER
RADIUS = BLOCK * 0.24855          # 28.65 / 115.27, the Chip's one corner radius

# --- the one improvisation, stated in block units ---------------------------
TAIL_LEGS = BLOCK * 0.60          # where the tail meets the body, both edges
TAIL_REACH = BLOCK * 0.50         # how far it runs at 45 degrees

# --- palette, matched by value and never by eye -----------------------------
BASE = "#0A1128"
GREY = "#5C6670"
BLUE = "#0466C8"
ACCENT = "#00B4D8"
ELECTRIC_GREEN = "#32D74B"
ICE_WHITE = "#F5F7FA"


def _round_rect(x: float, y: float, w: float, h: float, r: float) -> str:
    """A rounded rectangle as an explicit subpath, clockwise."""
    return (
        f"M{x + r:.4f},{y:.4f} H{x + w - r:.4f} A{r:.4f},{r:.4f} 0 0 1 {x + w:.4f},{y + r:.4f} "
        f"V{y + h - r:.4f} A{r:.4f},{r:.4f} 0 0 1 {x + w - r:.4f},{y + h:.4f} "
        f"H{x + r:.4f} A{r:.4f},{r:.4f} 0 0 1 {x:.4f},{y + h - r:.4f} "
        f"V{y + r:.4f} A{r:.4f},{r:.4f} 0 0 1 {x + r:.4f},{y:.4f} Z"
    )


@dataclass(frozen=True)
class Mark:
    """The Technocore mark: the Chip's aperture, made a place."""

    cells: int = 3

    @property
    def body(self) -> float:
        return self.cells * BLOCK + (self.cells - 1) * GUTTER

    @property
    def size(self) -> float:
        return self.body + TAIL_REACH

    def outline(self) -> str:
        """Body and tail as one closed contour.

        The tail's legs land on straight edge, past the corner radius, so the
        union is exact: the lower-left corner is replaced, not overlapped.
        """
        t, b, r, legs = TAIL_REACH, self.body, RADIUS, TAIL_LEGS
        return (
            f"M{t + r:.4f},0 H{t + b - r:.4f} A{r:.4f},{r:.4f} 0 0 1 {t + b:.4f},{r:.4f} "
            f"V{b - r:.4f} A{r:.4f},{r:.4f} 0 0 1 {t + b - r:.4f},{b:.4f} "
            f"H{t + legs:.4f} L0,{b + t:.4f} L{t:.4f},{b - legs:.4f} "
            f"V{r:.4f} A{r:.4f},{r:.4f} 0 0 1 {t + r:.4f},0 Z"
        )

    def voids(self) -> list[str]:
        """Gutters and the aperture, as subpaths that never overlap.

        Even-odd fill toggles, so two crossing gutters would put ink back at
        every crossing. The vertical gutters run the full height; the
        horizontal ones are cut into one segment per column, which leaves the
        crossings open exactly as they are on the Chip.
        """
        t, b = TAIL_REACH, self.body
        out = []
        for i in range(1, self.cells):
            x = t + i * PITCH - GUTTER
            out.append(f"M{x:.4f},0 H{x + GUTTER:.4f} V{b:.4f} H{x:.4f} Z")
            y = i * PITCH - GUTTER
            for j in range(self.cells):
                x0 = t + j * PITCH
                out.append(f"M{x0:.4f},{y:.4f} H{x0 + BLOCK:.4f} "
                           f"V{y + GUTTER:.4f} H{x0:.4f} Z")
        centre = (self.cells - 1) // 2 + 1 if self.cells % 2 == 0 else self.cells // 2
        cx, cy = t + centre * PITCH, centre * PITCH
        out.append(_round_rect(cx, cy, BLOCK, BLOCK, RADIUS))
        return out

    def path(self) -> str:
        return self.outline() + "".join(self.voids())

    def svg(self, ink: str = ACCENT, ground: str | None = None) -> str:
        s = self.size
        bg = f'<rect width="{s:.4f}" height="{s:.4f}" fill="{ground}"/>' if ground else ""
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s:.4f} {s:.4f}">'
            f"{bg}"
            f'<path fill="{ink}" fill-rule="evenodd" d="{self.path()}"/>'
            f"</svg>"
        )

    def icon_svg(self, ink: str = ACCENT, ground: str | None = None,
                 occupancy: float = 0.78) -> str:
        """Boxed for an app icon or favicon. 78% per V1.0 section two."""
        s = self.size
        box = s / occupancy
        off = (box - s) / 2
        bg = f'<rect width="{box:.4f}" height="{box:.4f}" fill="{ground}"/>' if ground else ""
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {box:.4f} {box:.4f}">'
            f"{bg}"
            f'<g transform="translate({off:.4f},{off:.4f})">'
            f'<path fill="{ink}" fill-rule="evenodd" d="{self.path()}"/></g></svg>'
        )


def favicon16(ink: str = ACCENT, ground: str | None = None) -> str:
    """The hand-tuned 16 px cut V1.0 asks for below 24 px.

    Scaling the geometry down closes the aperture and the mark reads as a lump.
    So this one is laid out on the pixel grid instead: blocks of 3, gutters of
    1, and a three-step tail. Same object, drawn for the pixels it lands on.
    """
    px, gap, span = 3, 1, 3 * 3 + 2 * 1     # 11 px body
    left, top = 4, 1
    on = [[False] * 16 for _ in range(16)]
    for row in range(3):
        for col in range(3):
            if row == 1 and col == 1:
                continue                     # the aperture stays open
            for dy in range(px):
                for dx in range(px):
                    on[top + row * (px + gap) + dy][left + col * (px + gap) + dx] = True
    for step in range(3):                    # the tail, one pixel per step at 45
        row = top + span + step
        for dx in range(px):
            on[row][left - 1 - step + dx] = True

    rects = "".join(
        f'<rect x="{x}" y="{y}" width="1" height="1"/>'
        for y, line in enumerate(on) for x, cell in enumerate(line) if cell
    )
    bg = f'<rect width="16" height="16" fill="{ground}"/>' if ground else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" '
            f'shape-rendering="crispEdges">{bg}<g fill="{ink}">{rects}</g></svg>')


def out_dir() -> "pathlib.Path":
    """dist/ sits beside the source in the working tree and one level up in the
    published repo. Prefer an existing one over creating a second."""
    import pathlib
    here = pathlib.Path(__file__).parent
    up = here.parent / "dist"
    return up if up.is_dir() else here / "dist"


if __name__ == "__main__":
    out = out_dir()
    out.mkdir(exist_ok=True)
    m = Mark()
    for name, ink in [("accent", ACCENT), ("blue", BLUE), ("green", ELECTRIC_GREEN),
                      ("base", BASE), ("ice", ICE_WHITE)]:
        (out / f"technocore_mark_{name}.svg").write_text(m.svg(ink))
    (out / "technocore_icon.svg").write_text(m.icon_svg(ACCENT, BASE))
    (out / "technocore_favicon_16.svg").write_text(favicon16(ACCENT))
    print(f"mark is {m.size:.2f} square, body {m.body:.2f}, wrote {out}")
