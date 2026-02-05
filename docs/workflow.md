# Workflow

This repo is intended to capture a long-running personal log as versioned Markdown.

## Day-to-Day

1. Create a daily entry:
   - `./bin/codex new`
2. Edit the created file in `life/YYYY/YYYY-MM-DD.md`.
3. Commit:
   - `git add life/YYYY/YYYY-MM-DD.md`
   - `git commit -m "life: YYYY-MM-DD"`

## Notion-First (Recommended)

If Notion is your source-of-truth, capture everything in your Notion Daily page and let the runtime generate artifacts here.

1. Configure Notion env:
   - copy `.env.example` to `.env` and fill values
   - verify property mapping in `runtime/config.json`
2. Every night (automation): `./bin/codex sync`
3. Every morning (automation): `./bin/codex briefing`

## Privacy

- Public content belongs in `life/`.
- Sensitive content belongs in `life/private/` and must remain untracked (gitignored).
- If a topic is sensitive but you still want a public trace, use `privacy: redacted` and placeholders.

## Structure

- Daily entries are canonical.
- Longer topics can be linked from a daily entry and stored under `life/topics/<slug>.md` (optional).
