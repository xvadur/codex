# Notion Integration

This runtime reads a "Daily" database in Notion and generates:

- `data/daily/YYYY-MM-DD.json` (normalized)
- `life/YYYY/YYYY-MM-DD.md` (public artifact)
- `reports/briefing/YYYY-MM-DD.md` (morning briefing)

## Credentials

Environment variables (use `.env`, never commit it):

- `NOTION_TOKEN`: internal integration token
- `NOTION_DAILY_DB_ID`: the database ID for your daily entries

## Property Mapping

Notion databases vary; mapping lives in `runtime/config.json` (or falls back to `runtime/config.example.json`):

- `date_property` (default: `Date`) must be a Notion `date` property storing `YYYY-MM-DD`
- `title_property` (default: `Name`) is the title property
- Optional:
  - `mood_property` (number/select)
  - `energy_property` (number/select)
  - `tags_property` (multi_select)

## Commands

- `./bin/codex sync` (yesterday)
- `./bin/codex sync 2026-02-05`
- `./bin/codex briefing` (today, from yesterday's synced JSON)

