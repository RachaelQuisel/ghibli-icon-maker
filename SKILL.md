---
name: "ghibli-icon-maker"
description: "Create hand-drawn icons for creative projects, apps, and brands in the Soft Index style: warm charcoal line art on washed pastel grounds inside a squircle tile. Use when the user asks for an icon or logo mark in this style, or mentions Ghibli Icon Maker."
---

# Ghibli Icon Maker

## Purpose
Generate a new icon that looks like it belongs with the existing Soft Index set: a single hand-drawn contour in warm charcoal, floating on a washed pastel ground inside a squircle tile.

## Workflow
1. Get the brief: the subject or concept, the name it will carry, and the mood. One icon per subject.
2. Read `references/design-philosophy.md` for the movement's rules.
3. Study `references/render_icons.py` for the technique. Reuse its geometry helpers (`squircle`, `arc`, `circle`, `seg`, `bez`, `rrect`, `sparkle`), the `soften()` hand-wobble, and the `Sheet` API (`paint`, `stroke`, `dot`) exactly as written. Do not reinvent the renderer.
4. Author one new drawing function following the three existing ones as patterns. See `references/examples.md` for what each model icon does.
5. Pick a fresh palette from the dust family: a washed top/bottom gradient pair, a glow tint, and a wash tint. Blush, clay, mauve, cooled blue-grey, sage. Never saturated, and never repeat a sibling icon's palette within the same set.
6. Render at 1024x1024 and read the output image yourself before showing the user. Copy `render_icons.py` to a working folder first, because it writes PNGs next to itself. Run it with `uv run --no-project --with pillow python render_icons.py`, because Pillow is not installed system-wide. For a directory submission, run the PNG through publish-a-plugin's `scripts/shrink_icon.py`, because the three model renders came out at 744-798 KiB and the observed ceiling is about 750 KiB.
7. Present the icon and iterate on feedback.

## Output Contract
- 1024x1024 PNG, RGBA, squircle mask with a softly feathered edge.
- Ink is warm charcoal `(62, 52, 46)`, never pure black. Stroke weight constant at `0.0248` of tile width across every icon in a set.
- Subject is one continuous contour occupying roughly a third of the tile, optically centered, never touching an edge.
- One small aperture detail (dot, notch, tick) gives the eye a landing place; one sparkle accent sits top-right.
- Paper grain is laid over the finished tile so line and ground share one surface.
- File is named `<slug>.png`.

## Operating Rules
1. Outline only. No fills, no shadows, no depth cues, no gradients on the linework.
2. Keep stroke weight identical across a set; vary rhythm through spacing, never line thickness.
3. Closed contours stay closed; open contours end on round caps.
4. When in doubt, simplify. Restraint held longer beats another detail.
5. Always visually verify the render before presenting. If it looks constructed rather than drawn, adjust the `soften()` amplitude, not the geometry.
