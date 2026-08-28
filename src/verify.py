#!/usr/bin/env python3
"""Check this entry against the brand it claims to follow, live.

Fetches the FLOP Chip master from flop.finance, recovers the grid it was drawn
on, and compares that to the constants this mark is generated from. Then checks
that the published artwork is what this code produces, and that the copy on
Technocore still matches.

    python3 src/verify.py

Exit code 0 if every check passes.
"""
from __future__ import annotations

import hashlib
import re
import sys
import urllib.request

import technocore_mark as mk
from chip import USER_AGENT, fetch_master, measure

NOTE_URL = "https://technocore.chat/kv/technocore-logo/tatthang"
TOLERANCE = 0.001                 # the clustering step rounds to 0.01 of a unit
WIDTH = 34


def row(label: str, detail: str, verdict: str = "") -> None:
    print(f"  {label:<{WIDTH}} {detail}" + (f"   {verdict}" if verdict else ""))


def close(a: float, b: float) -> bool:
    return abs(a - b) <= TOLERANCE


def fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", "replace")


def main() -> int:
    failures: list[str] = []

    print("\nFLOP Chip master")
    view, data, source = fetch_master()
    row("source", source)
    if "offline" in source:
        print("\n  Offline: the grid below comes from the vendored copy, so this run\n"
              "  proves the generator is self-consistent but not that it still\n"
              "  agrees with the live file.\n")
    grid = measure(data)
    row("inner block / gutter / radius", f"{grid.block} / {grid.gutter} / {grid.radius}")

    print("\nConstants this mark is generated from")
    checks = [
        ("gutter / block", grid.gutter_ratio, mk.GUTTER / mk.BLOCK),
        ("radius / block", grid.radius_ratio, mk.RADIUS / mk.BLOCK),
    ]
    for label, measured, used in checks:
        ok = close(measured, used)
        row(label, f"master {measured:.5f}   generator {used:.5f}",
            "PASS" if ok else "FAIL")
        if not ok:
            failures.append(label)

    print("\nWhat the master itself is not consistent about")
    row("outer columns", f"{', '.join(str(b) for b in grid.outer_blocks)} against inner {grid.block}",
        "NOTE")
    row("octagon extent", f"{grid.width} x {grid.height}, {grid.out_of_square * 100:.2f}% out of square",
        "NOTE")
    print("  This mark is built on the inner grid, which is the consistent one.")

    print("\nPublished artwork")
    svg = mk.Mark().svg(mk.ACCENT)
    digest = hashlib.sha256(svg.encode("utf-8")).hexdigest()
    shipped = (mk.out_dir() / "technocore_mark_accent.svg")
    if shipped.exists():
        same = shipped.read_text(encoding="utf-8") == svg
        row("dist/technocore_mark_accent.svg", f"sha256 {digest[:16]}",
            "PASS" if same else "FAIL")
        if not same:
            failures.append("shipped artwork differs from generator output")
    else:
        row("dist/technocore_mark_accent.svg", "missing, run technocore_mark.py", "FAIL")
        failures.append("shipped artwork missing")

    print("\nCopy living on Technocore")
    try:
        # a GET on a note prepends the server's untrusted-content banner, so
        # check for the artwork inside the reply rather than hashing the reply
        body = fetch(NOTE_URL)
        present = svg in body
        row(NOTE_URL.replace("https://", ""), f"{len(body)} chars returned",
            "PASS" if present else "STALE")
        if not present:
            failures.append("published note does not carry this build")
            print("  The note no longer carries this exact build. Either it was "
                  "not\n  republished after a change, or someone overwrote it: "
                  "/kv is\n  world-writable by design, which is the whole reason "
                  "the hash is\n  signed into an owned room instead.")
    except Exception as error:
        row(NOTE_URL.replace("https://", ""), f"unreachable ({type(error).__name__})", "SKIP")

    print()
    if failures:
        print(f"FAILED: {len(failures)} check(s) — " + "; ".join(failures) + "\n")
        return 1
    print("All checks passed.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
