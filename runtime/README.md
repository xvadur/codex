# runtime/

Local scripts that turn Notion into versioned artifacts in this repository.

## Quick Start

1. Create `.env` (see `.env.example`) and fill:
   - `NOTION_TOKEN`
   - `NOTION_DAILY_DB_ID`
2. Copy `runtime/config.example.json` to `runtime/config.json` and adjust property names to match your Notion database.
3. Run:
   - `./bin/codex sync` (defaults to yesterday)
   - `./bin/codex briefing` (defaults to today; uses yesterday's synced data)

## Outputs

- Normalized daily JSON: `data/daily/YYYY-MM-DD.json`
- Public daily entry: `life/YYYY/YYYY-MM-DD.md` (generated/updated on sync)
- Briefing: `reports/briefing/YYYY-MM-DD.md`

