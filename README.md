# Ghibli Icon Maker

<img src="assets/ghibli-icon-maker.png" width="160" alt="Ghibli Icon Maker icon: a charcoal pen nib on dusty lavender">

Give your ideas a softer look. Create warm charcoal line icons on washed pastel tiles for creative projects, websites, apps, and brands.

## What it does

- Turns a subject or concept into a simple icon
- Uses the Soft Index visual style: warm linework, muted pastels, and paper texture
- Keeps spacing and line weight consistent across a set
- Adds a small sparkle and aperture detail
- Produces a 1024 by 1024 RGBA PNG with transparent tile corners

## Install in Claude Code

```
/plugin marketplace add RachaelQuisel/ghibli-icon-maker
/plugin install ghibli-icon-maker
```

The skill registry is fixed at session start, so the skill becomes available in your next session.

## Use

```text
/ghibli-icon-maker:ghibli-icon-maker
Create an icon of an open book for my reading project.
Use a warm, calm mood and a muted palette.
```

Provide the subject, the name the icon will carry, and the mood. The skill uses the supplied renderer, checks the resulting image, and presents it for feedback.

The Python renderer requires Pillow. A compatible environment can be started with:

```sh
uv run --with pillow python references/render_icons.py
```

Running the reference renderer exports its three model icons and a contact sheet alongside the script. New subjects are authored with its existing geometry and drawing helpers as described in `SKILL.md`.

## Files

- `SKILL.md`: the skill instructions
- `agents/openai.yaml`: Codex display name, prompts, and icon references
- `assets/ghibli-icon-maker.png`: the plugin icon
- `references/design-philosophy.md`: the Soft Index style rules
- `references/examples.md`: the three model icon descriptions
- `references/render_icons.py`: the supplied renderer and model drawings
