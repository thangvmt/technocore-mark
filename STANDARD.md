# Technocore Mark — Usage Standard v1.0

A product mark for technocore.chat, built inside FLOP Logo & Usage Standards
V1.0. Written to that document's structure so the two can sit side by side.

Its closing rule is the one this entry took most seriously: **anything not shown
in it is unapproved — ask before improvising.** Section 9 below names every
place this mark improvised, and why.

---

## 1. The idea

FLOP is the chip. The aperture is where inference passes through it.
**Technocore is that aperture, made a place.**

The delivered Chip master carries more than DESIGN.md describes. The prose says
*"one block-sized aperture at the centre"*; the artwork has a rounded square
about 1.36 blocks wide with a **45° channel** running out to the lower-left
corner. A rounded square with a 45° tail is the geometry of a bubble.

The chip already had a mouth. This mark is what comes out of it.

## 2. Construction

Everything sits on the Chip's own grid, measured on the master file rather than
estimated.

| | Value | Where it comes from |
|---|---|---|
| Block | 100 | normalised |
| Gutter | 6.86 | 8.09 / 117.94, measured between adjacent blocks |
| Pitch | 106.86 | block + gutter |
| Radius | 21 | 28.65 / 136.42, the Chip's aperture radius |
| Field | 3 × 3 blocks | body 313.72 square |
| Tail | legs 0.60 block, reach 0.50 block, at 45° | see section 9 |

**One radius governs the whole mark**, and it is the Chip's. Body corners,
aperture corners: the same 21.

The centre block is the aperture. It **always shows the ground behind it** —
never fill it, never put a letter, dot or image in it. Gutter crossings stay
open, as they do on the Chip.

## 3. Clear space

**4X on every side, where X is one block.** Measured from the artwork, not from
the file's bounding box — the tail is artwork, so it sets the lower-left edge.
Nothing enters it: not type, not a rule, not a fold, not the trim.

4X is a minimum. Give it more room whenever you can.

## 4. Minimum sizes

| | Minimum |
|---|---|
| Lockup | 200 px wide |
| Mark alone | 24 px |

At 24 px the aperture still reads. Below it the aperture closes and the mark
becomes a lump — use a hand-tuned 16 px favicon only where a platform demands
one. Below 200 px use the one-color version.

In a square icon box the mark occupies **78%** of the box width, optically
centred, per V1.0 section two. Do not crop it to the edge, do not round it
further, do not pre-empt the platform's mask.

## 5. The word mark

**Space Mono Bold**, the brand's own display face, at the font's natural
advance. It is set, never drawn: this mark introduces no new letterforms.

Cap height equals the mark's **body** height, so the mark and the word share one
cap line, exactly as the Chip does with FLOP. The tail hangs below the baseline
like a descender. The gap between mark and word is 1.5 blocks.

## 6. Approved lockups

| Lockup | Word mark | Mark | Where |
|---|---|---|---|
| **Primary** | Base | Accent | Ice White or paper. The default in every medium |
| **Reverse** | Ice White | Accent | On Base only — never on Blue, Grey or a photograph |
| **Print alternate** | Base | Blue | Single-pass print where Accent shifts |
| **Product** | Base | Electric Green | Product surfaces and internal tooling only |
| **One-color** | Base *or* Ice White | same | Engraving, single-ink, anything under 200 px |

There are no others.

## 7. The one colour rule

**The word mark takes the neutral that contrasts the ground — Base on light,
Ice White on dark — and no other colour ever. The mark carries the colour.**

Never swap that relationship. Never put three inks in one lockup. Never mix
Accent and Electric Green. Never set a two-tone lockup on a ground other than
Base. Accent on Ice White is not approved at any size.

Colours are matched by hex value, never by eye.

## 8. Misuse

None of this may ship: stretching, condensing or uneven scaling; rotation;
shadow, glow, bevel or outline; two accents or a coloured word mark; swapping
the colours so the word carries the colour; filling the aperture; using the mark
as a frame, bullet, pattern tile or container; mirroring or flipping; reduced
opacity as a watermark; cropping to a corner; locking a tagline, product name or
year to it; re-exporting from a screenshot or slide.

The domain **technocore.chat** is a tagline. It may sit on the same page. It may
not be locked to the mark, and it stays outside the 4X clear space.

## 9. Where this improvised, and why

V1.0 says to ask rather than improvise. Three decisions were not derivable from
the published system, and here they are, in the open:

1. **Rounded corners on the body instead of 45° cuts.** The Chip cuts its
   corners; this mark rounds them. Cutting them would have produced a second
   octagon, and a product mark that is a smaller copy of the parent icon is not
   a product mark. The radius used is not invented: it is the Chip's own
   aperture radius, which is the one soft measurement the system already owns.

2. **The tail's proportions.** Legs 0.60 block, reach 0.50 block. The Chip's
   channel is constant-width; a tapering tail reads at 24 px where a channel
   does not. Everything else about it — the 45°, the direction, the fact that it
   leaves at the lower-left corner — is quoted from the Chip.

3. **The gap between mark and word**, at 1.5 blocks. V1.0 publishes clear space
   but not internal lockup spacing, so this is a proportion, not a rule.

Everything else in this document is either measured from the master file or
lifted from V1.0 unchanged. If any of the three is wrong for the system, they
are each a one-line change in the generator.

## 10. Provenance

The mark is **generated, not drawn**. `technocore_mark.py` emits the SVG from
the constants in section 2; `technocore_lockup.py` outlines the word mark
straight from the Space Mono binary. Change a constant, re-run, and every
deliverable moves together. The machine is the art.

The mark also lives on Technocore itself:

```
GET https://technocore.chat/kv/technocore-logo/tatthang
```

Notes there are world-writable, so a note alone proves nothing about who wrote
it. The signed line in `/r/d-tatthang` carries the SHA-256 of the bytes, and
that room accepts writes only from its owner's key. Rehash the note, strip the
server's untrusted-content banner, and compare.

```
sha256  049e670e0f377241f28667300683cca2617ad11dfef54331fabea193d84c5200
did:key z6MkmzyBxvrSZveZv5YhZhfwUYQYv5LDgt5NuqVrBe5vXvPA
```
