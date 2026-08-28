"""Three submission boards, composed in SVG. All text is outlined, so a board
renders identically with no font installed anywhere."""
from __future__ import annotations

import pathlib

from technocore_lockup import GAP, Wordmark
from technocore_mark import (ACCENT, BASE, BLOCK, BLUE, ELECTRIC_GREEN, GREY,
                             GUTTER, ICE_WHITE, PITCH, RADIUS, TAIL_LEGS,
                             TAIL_REACH, Mark, out_dir)
from textpath import advance, text_path

HERE = pathlib.Path(__file__).parent
CHIP_VB, CHIP_D = (HERE / "chip_master.txt").read_text().split("\n")
CHIP_X, CHIP_Y, CHIP_W, _ = (float(v) for v in CHIP_VB.split())
MARK = Mark()
WORD_ADV = Wordmark(cap=MARK.body).outline()[1]
LOCKUP_W = MARK.size + GAP + WORD_ADV     # at cap == MARK.body

# The aperture and its channel, in the Chip's own coordinates. Read off the
# master path, used only to crop a magnified view of the delivered artwork.
APERTURE_CROP = (232.0, 392.0, 392.0)


def label(x, y, text, size=22, fill=ICE_WHITE, anchor="start", opacity=1.0, bold=False):
    return text_path(x, y, text, size, fill, anchor, opacity, bold)


def mark_at(x, y, h, ink=ACCENT):
    k = h / MARK.size
    return (f'<g transform="translate({x:.2f},{y:.2f}) scale({k:.5f})">'
            f'<path fill="{ink}" fill-rule="evenodd" d="{MARK.path()}"/></g>')


def chip_at(x, y, h, ink=ACCENT, opacity=1.0):
    k = h / CHIP_W
    return (f'<g opacity="{opacity}" transform="translate({x:.2f},{y:.2f}) '
            f'scale({k:.5f}) translate({-CHIP_X:.2f},{-CHIP_Y:.2f})">'
            f'<path fill="{ink}" d="{CHIP_D}"/></g>')


def chip_crop_at(x, y, h, ink=ACCENT):
    """A magnified window onto the master file. Nothing is redrawn.

    A nested <svg> clips to its own viewport, which every renderer honours;
    clip-path is not universally applied by thumbnailers.
    """
    cx, cy, cw = APERTURE_CROP
    return (f'<svg x="{x:.2f}" y="{y:.2f}" width="{h:.2f}" height="{h:.2f}" '
            f'viewBox="{cx:.2f} {cy:.2f} {cw:.2f} {cw:.2f}">'
            f'<path fill="{ink}" d="{CHIP_D}"/></svg>')


def lockup_at(x, y, cap, word_ink, mark_ink):
    d, _ = Wordmark(cap=MARK.body).outline()
    k = cap / MARK.body
    return (f'<g transform="translate({x:.2f},{y:.2f}) scale({k:.5f})">'
            f'<path fill="{mark_ink}" fill-rule="evenodd" d="{MARK.path()}"/>'
            f'<g transform="translate({MARK.size + GAP:.2f},0)">'
            f'<path fill="{word_ink}" d="{d}"/></g></g>')


def cap_to_fit(width: float) -> float:
    """Cap height for a lockup that is `width` wide, artwork only."""
    return width * MARK.body / LOCKUP_W


def cap_in_box(box_w: float) -> tuple[float, float]:
    """Cap height and padding for a lockup that holds its 4X clear space.

    X is one block, so the box must carry 8 blocks of air plus the artwork.
    Solving box_w = (cap / body) * (8 * BLOCK + LOCKUP_W) gives both at once.
    """
    cap = box_w * MARK.body / (8 * BLOCK + LOCKUP_W)
    return cap, 4 * BLOCK * cap / MARK.body


def board(w, h, ground, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">'
            f'<rect width="{w}" height="{h}" fill="{ground}"/>{body}</svg>')


# ---------------------------------------------------------------- board 1 ---
def hero() -> str:
    W, H = 1600, 900
    cap = cap_to_fit(1080)
    lw, lh = LOCKUP_W * cap / MARK.body, MARK.size * cap / MARK.body
    body = (
        lockup_at((W - lw) / 2, H / 2 - lh / 2 - 40, cap, ICE_WHITE, ACCENT)
        # the domain is a tagline: it sits outside the 4X clear space and is
        # not locked to the mark, per V1.0
        + label(W / 2, H / 2 - lh / 2 - 40 + lh + 4 * BLOCK * cap / MARK.body + 26,
                "technocore.chat", 26, GREY, "middle")
        + label(W / 2, H - 112, "THE APERTURE, MADE A PLACE", 24, ACCENT, "middle", bold=True)
        + label(W / 2, H - 66, "FLOP is the chip. The hole in it is where inference",
                21, ICE_WHITE, "middle", 0.60)
        + label(W / 2, H - 36, "passes through. Technocore is that hole, made a place.",
                21, ICE_WHITE, "middle", 0.60)
    )
    return board(W, H, BASE, body)


# ---------------------------------------------------------------- board 2 ---
def derivation() -> str:
    W, H = 1600, 900
    size, y = 300, 296
    xs = [140, 650, 1160]
    arrow = ('<path d="M{0:.1f},{1:.1f} h80" stroke="{2}" stroke-width="3" fill="none"/>'
             '<path d="M{3:.1f},{1:.1f} l-15,-9 v18 z" fill="{2}"/>')
    caps = [("FLOP Chip", "master file, unaltered", ICE_WHITE),
            ("its aperture", "magnified from that same file", ICE_WHITE),
            ("Technocore", "that shape, at nine blocks", ACCENT)]
    body = label(60, 96, "DERIVATION", 22, ACCENT, bold=True) + label(
        60, 146, "One move, and it is their move.", 32, ICE_WHITE, bold=True)
    body += chip_at(xs[0], y, size)
    body += chip_crop_at(xs[1], y, size)
    body += f'<rect x="{xs[1]}" y="{y}" width="{size}" height="{size}" fill="none" stroke="{GREY}" stroke-width="2"/>'
    body += mark_at(xs[2], y, size)
    for i in (0, 1):
        body += arrow.format(xs[i] + size + 34, y + size / 2, GREY, xs[i] + size + 114)
    for x, (a, b, ink) in zip(xs, caps):
        body += label(x, y + size + 62, a, 23, ink) + label(x, y + size + 96, b, 19, GREY)
    body += label(60, H - 96, "design.md calls it “one block-sized aperture at the centre”.",
                  20, ICE_WHITE, opacity=0.62)
    body += label(60, H - 62, "The delivered art is wider than that, and it has a 45° channel:",
                  20, ICE_WHITE, opacity=0.62)
    body += label(60, H - 28, "the geometry of a bubble. The chip already had a mouth.",
                  20, ACCENT, opacity=0.9)
    return board(W, H, BASE, body)


# ---------------------------------------------------------------- board 3 ---
def system() -> str:
    W, H = 1600, 1100
    body = label(60, 96, "CONSTRUCTION, LOCKUPS, SIZES", 22, ACCENT, bold=True)

    # left: construction
    gx, gy, gh = 96, 168, 300
    k = gh / MARK.size
    t, bb = TAIL_REACH * k, MARK.body * k
    for i in range(3):
        for j in range(3):
            body += (f'<rect x="{gx + t + j * PITCH * k:.2f}" y="{gy + i * PITCH * k:.2f}" '
                     f'width="{BLOCK * k:.2f}" height="{BLOCK * k:.2f}" fill="none" '
                     f'stroke="{ICE_WHITE}" stroke-opacity="0.45" stroke-width="1" '
                     f'stroke-dasharray="4 4"/>')
    body += mark_at(gx, gy, gh)
    body += label(gx + t + bb / 2, gy - 22, "3 blocks", 17, GREY, "middle")
    body += label(gx + t + bb + 18, gy + bb + 34, "45° tail", 17, ACCENT)
    for n, line in enumerate([
            f"block {BLOCK:.0f} · gutter {GUTTER:.2f} · pitch {PITCH:.2f}",
            f"radius {RADIUS:.2f}, the Chip's one corner radius — everywhere",
            f"tail legs {TAIL_LEGS / BLOCK:.2f} block, "
            f"reach {TAIL_REACH / BLOCK:.2f} block"]):
        body += label(gx, gy + gh + 70 + n * 34, line, 18, ACCENT if n == 2 else GREY)

    # right: sizes
    rx = 760
    body += label(rx, 186, "MINIMUM 24px — the aperture still shows", 19, ICE_WHITE)
    sx = rx
    for px in (96, 64, 40, 24):
        body += mark_at(sx, 218 + (96 - px), px)
        body += label(sx + px / 2, 356, str(px), 16, GREY, "middle")
        sx += px + 54

    # right: palette
    body += label(rx, 430, "PALETTE, MATCHED BY VALUE", 19, ICE_WHITE)
    sw = 0
    for name, hexv in [("Base", BASE), ("Ice", ICE_WHITE), ("Accent", ACCENT),
                       ("Blue", BLUE), ("Green", ELECTRIC_GREEN), ("Grey", GREY)]:
        body += (f'<rect x="{rx + sw}" y="452" width="118" height="64" fill="{hexv}" '
                 f'stroke="{GREY}" stroke-width="1"/>'
                 + label(rx + sw, 540, name, 16, GREY)
                 + label(rx + sw, 562, hexv, 15, ICE_WHITE, opacity=0.55))
        sw += 134
    body += label(rx, 626, "TWO INKS. THE WORD MARK STAYS NEUTRAL.", 19, ICE_WHITE)
    body += label(rx, 660, "The mark carries the colour, exactly as the Chip does.", 18, GREY)

    # bottom: the two everyday lockups, sized to their boxes
    box_w = 700
    cap, pad = cap_in_box(box_w)
    lh = MARK.size * cap / MARK.body
    for bx, ground, wi, note in [
            (60, ICE_WHITE, BASE, "PRIMARY — Base word, Accent mark, on Ice White"),
            (840, BASE, ICE_WHITE, "REVERSE — Ice White word, Accent mark, on Base only")]:
        stroke = f' stroke="{GREY}" stroke-width="1"' if ground == BASE else ""
        body += (f'<rect x="{bx}" y="760" width="{box_w}" height="{lh + pad * 2:.1f}" '
                 f'fill="{ground}"{stroke}/>')  # pad == 4X on every side
        body += lockup_at(bx + pad, 760 + pad, cap, wi, ACCENT)
        body += label(bx, 760 + lh + pad * 2 + 40, note, 18, GREY)
    body += label(60, H - 34,
                  "Clear space 4X on every side, X = one block. "
                  "Print alternate swaps the mark to Blue.", 18, ICE_WHITE, opacity=0.62)
    return board(W, H, BASE, body)


if __name__ == "__main__":
    out = out_dir()
    out.mkdir(exist_ok=True)
    for name, fn in [("01_hero", hero), ("02_derivation", derivation), ("03_system", system)]:
        (out / f"board_{name}.svg").write_text(fn())
    print(f"3 boards; lockup aspect {LOCKUP_W / MARK.size:.2f}:1")
