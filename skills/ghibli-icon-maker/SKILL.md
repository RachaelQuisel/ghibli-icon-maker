---
name: "ghibli-icon-maker"
description: "Create hand-drawn icons for creative projects, apps, and brands in the Soft Index style: warm charcoal line art on washed pastel grounds inside a squircle tile. Use when the user asks for an icon or logo mark in this style, or mentions Ghibli Icon Maker."
---

# Ghibli Icon Maker

## Purpose
Generate a new icon that looks like it belongs with the existing Soft Index set: a clear hand-drawn subject in warm charcoal, floating on a washed pastel ground inside a squircle tile.

## Platform and function recognition

- For a skill or plugin associated with a specific platform, include that platform's recognizable logo as a secondary identifier. Prefer supplied or official brand assets; preserve their geometry and colors rather than inventing a similar-looking symbol.
- Make the main illustration specifically show what the skill builds or does. For Airtable Interface Builder, a window with a sidebar, cards and task rows made the purpose clear. A platform logo alone does not explain the job.
- Keep the logo separate from the main drawing, with breathing room and enough size to remain recognizable in a thumbnail. Use no platform logo for a platform-neutral skill.
- Authentic logo colors and filled logo shapes are a limited exception to the muted, outline-only style. A few functional interior details and optional decorative accents are also allowed. These exceptions take precedence over the original studies in `references/design-philosophy.md`; retain the Soft Index ground, ink, spacing and texture.

## Workflow
1. Get the brief: the name, subject or concept, and mood. For a skill/plugin icon, also identify what it builds or does and its related platform if any. Choose one coherent main illustration that communicates that subject or job.
2. Read `references/design-philosophy.md` for the movement's rules.
3. Study `references/render_icons.py` for the technique. Reuse its geometry helpers (`squircle`, `arc`, `circle`, `seg`, `bez`, `rrect`, `sparkle`), the `soften()` hand-wobble, and the `Sheet` API (`paint`, `stroke`, `dot`) exactly as written. Do not reinvent the renderer.
4. Inspect the bundled PNG references linked from [references/examples.md](references/examples.md), then author one new drawing function following the existing ones as patterns. Use the images to match contour, spacing, palette, and paper texture. For platform-specific skill/plugin icons, study the Airtable Interface Builder example for platform recognition and a concrete depiction of the job.
5. Pick a fresh palette from the dust family: a washed top/bottom gradient pair, a glow tint, and a wash tint. Blush, clay, mauve, cooled blue-grey, sage. Keep the tile and main drawing muted; preserve a platform logo's authentic colors. Never repeat a sibling icon's palette within the same set.
6. Render at 1024x1024 and read the output image yourself before showing the user. Copy `render_icons.py` to a working folder first, because it writes PNGs next to itself. Run it with `uv run --no-project --with pillow python render_icons.py`, because Pillow is not installed system-wide. For a directory submission, run the PNG through publish-a-plugin's `scripts/shrink_icon.py`, because the three model renders came out at 744-798 KiB and the observed ceiling is about 750 KiB.
7. Check the full-size icon and a small thumbnail: the subject/job should be recognizable, as should the platform identifier when present. Present the icon and iterate on feedback, keeping requested removals such as the sparkle removed.

## Output Contract
- 1024x1024 PNG, RGBA, squircle mask with a softly feathered edge.
- Ink is warm charcoal `(62, 52, 46)`, never pure black. Stroke weight constant at `0.0248` of tile width across every icon in a set.
- Subject is one coherent main illustration occupying roughly a third of the tile, optically centered, never touching an edge. Use a few interior details when needed to make its function clear.
- One small aperture detail (dot, notch, tick) gives the eye a landing place. A sparkle is optional; omit it when it competes with the subject or platform logo, or when the user asks.
- Paper grain is laid over the finished tile so line and ground share one surface.
- File is named `<slug>.png`.

## Operating Rules
1. Main illustration: outline only, with no fills, shadows, depth cues or gradients on the linework. An authentic platform logo may retain its filled shapes and brand colors; do not apply hand-wobble to its geometry.
2. Keep stroke weight identical across a set; vary rhythm through spacing, never line thickness.
3. Closed contours stay closed; open contours end on round caps.
4. When in doubt, simplify. Restraint held longer beats another detail.
5. Always visually verify the render before presenting. If the main drawing looks constructed rather than drawn, adjust its `soften()` amplitude, not the geometry. Preserve platform logo geometry.
