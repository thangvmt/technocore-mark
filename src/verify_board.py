#!/usr/bin/env python3
"""Render verify.py's own output as board 04.

Kept separate from boards.py because this one reaches the network: it is a
picture of a real run, not an illustration of one.
"""
from __future__ import annotations

import contextlib
import io
import pathlib

import verify
from technocore_mark import ACCENT, BASE, ELECTRIC_GREEN, GREY, ICE_WHITE, out_dir
from textpath import advance, text_path

FONT_SIZE, LINE_HEIGHT = 19.0, 30.0
PAD, TOP, WIDTH = 46, 92, 1500
CHROME = "#151D32"
WINDOW = "#0B1226"


def run() -> list[str]:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        verify.main()
    lines = [line.rstrip() for line in buffer.getvalue().split("\n")]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return lines


def render(lines: list[str]) -> str:
    height = TOP + len(lines) * LINE_HEIGHT + PAD + 20
    body = (f'<rect width="{WIDTH}" height="{height}" rx="10" fill="{WINDOW}"/>'
            f'<rect width="{WIDTH}" height="52" rx="10" fill="{CHROME}"/>'
            f'<rect y="42" width="{WIDTH}" height="10" fill="{CHROME}"/>')
    for i, dot in enumerate(["#FF453A", "#F2B441", ELECTRIC_GREEN]):
        body += f'<circle cx="{28 + i * 26}" cy="26" r="7" fill="{dot}" fill-opacity="0.85"/>'
    body += text_path(WIDTH / 2, 33, "python3 src/verify.py", 17, GREY, "middle")

    for i, line in enumerate(lines):
        y = TOP + i * LINE_HEIGHT
        verdict = next((v for v in ("PASS", "NOTE", "FAIL", "SKIP")
                        if line.strip().endswith(v)), None)
        if verdict:
            head = line[:line.rindex(verdict)]
            ink = {"PASS": ELECTRIC_GREEN, "NOTE": ACCENT,
                   "FAIL": "#FF453A", "SKIP": GREY}[verdict]
            body += text_path(PAD, y, head, FONT_SIZE, ICE_WHITE, opacity=0.85)
            body += text_path(PAD + advance(head, FONT_SIZE), y, verdict,
                              FONT_SIZE, ink, bold=True)
        else:
            heading = bool(line) and not line.startswith(" ")
            body += text_path(PAD, y, line, FONT_SIZE,
                              ICE_WHITE if heading else GREY,
                              opacity=1.0 if heading else 0.78, bold=heading)

    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {WIDTH} {height}">{body}</svg>')


if __name__ == "__main__":
    out = out_dir()
    out.mkdir(exist_ok=True)
    target = out / "board_04_verify.svg"
    target.write_text(render(run()))
    print("wrote", target)
