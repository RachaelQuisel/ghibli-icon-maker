# Ghibli Icon Maker

<img src="assets/ghibli-icon-maker.png" width="160" alt="Ghibli Icon Maker icon: a charcoal pen nib on dusty lavender">

Give your ideas a softer look. Create warm charcoal line icons on washed pastel tiles for creative projects, websites, apps, and brands.

## Claude Marketplace submission

- **Submitted:** [Claude Marketplace partner waitlist](https://claude.com/marketplace-partners), October 5, 2026, through XRAY Automation. Confirmation was received.
- **Current status:** Waitlist application confirmed. Directory approval or a public listing has not been verified.
- **Status checked:** October 12, 2026.

### Evidence audit: October 16, 2026

- **Partner waitlist:** Submission confirmation recorded for 2026-10-05, through XRAY Automation. This is retained repository evidence, not a newly inspected confirmation receipt.
- **Plugin directory:** No separate directory submission evidence found.
- **Approved:** Unverified. **Publicly listed:** Unverified. No verified public listing URL is recorded.
- **Verification limit:** The publisher portal requires sign-in. Public searches and the connected mailbox search did not establish approval; missing results are not proof of rejection or non-publication.
- **Next action:** Retrieve the original partner confirmation; check the submitting account for a separate plugin-directory submission before creating one.

The [partner waitlist](https://claude.com/marketplace-partners) is for Claude-powered enterprise products. It is separate from plugin-directory review and GitHub marketplace installation. A waitlist application is not directory approval.


## What it does

- Turns a subject or concept into a simple icon
- Uses the Soft Index visual style: warm linework, muted pastels, and paper texture
- Keeps spacing and line weight consistent across a set
- Makes skill/plugin icons show the specific job they perform
- Includes a recognizable platform logo when the skill/plugin targets a platform
- Uses an aperture detail and an optional decorative accent
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

For a skill/plugin icon, also describe what it builds or does and the platform it targets. The [Airtable Interface Builder example](skills/ghibli-icon-maker/references/images/airtable-interface-builder.png) pairs an Airtable identifier with a window, sidebar, cards and task rows. Its sparkle was removed following user feedback. Platform logos may retain their brand colors while the main drawing keeps the Soft Index style.

The Python renderer requires Pillow. A compatible environment can be started with:

```sh
uv run --with pillow python skills/ghibli-icon-maker/references/render_icons.py
```

Running the reference renderer exports its three model icons and a contact sheet alongside the script. New subjects are authored with its existing geometry and drawing helpers as described in `skills/ghibli-icon-maker/SKILL.md`.

## Files

- `skills/ghibli-icon-maker/SKILL.md`: the skill instructions
- `assets/ghibli-icon-maker.png`: the plugin icon
- `skills/ghibli-icon-maker/references/design-philosophy.md`: the Soft Index style rules
- `skills/ghibli-icon-maker/references/examples.md`: style studies and the approved platform/function example
- `skills/ghibli-icon-maker/references/render_icons.py`: the supplied renderer and model drawings
