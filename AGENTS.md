# Agent Instructions (codex)

This repository is a personal "life log runtime". The default output is plain text Markdown committed to git.

## Core Principles

- Personal is allowed: relationship/sex/money topics are allowed; treat them neutrally and pragmatically.
- Security is non-negotiable: never store secrets, passwords, tokens, private keys, raw IDs, or anything that would enable account takeover.
- Prefer summaries over raw dumps: when ingesting content (chat logs, exports, emails), summarize and extract structure.
- Every change should be reversible: prefer additive commits; avoid destructive git operations.

## Collaboration Workflow

- Ask clarifying questions when format/intent is ambiguous, but if unclear, proceed with the minimal safe default.
- For any network action (push/pull/fetch, API calls), ask/obtain explicit permission if the environment requires it.
- Keep commits small and describable. Use conventional-ish messages:
  - `chore: ...`, `docs: ...`, `feat: ...`, `fix: ...`
- Do not rewrite git history unless the user explicitly requests it.

## Repository Layout

- `life/`: the public life log (Markdown). Default is daily notes.
- `life/templates/`: templates used by scripts.
- `life/private/`: local-only notes (MUST be gitignored).
- `runtime/`: scripts and tooling that generate/validate entries.
- `docs/`: human-readable documentation for the workflow.

## Logging Format (Default)

- Daily entry path: `life/YYYY/YYYY-MM-DD.md`
- Use YAML frontmatter at the top with at least:
  - `date` (YYYY-MM-DD)
  - `tags` (list)
  - `mood` (optional)
  - `privacy` one of: `public`, `redacted`, `private`
- Body should prefer:
  - `## Summary`
  - `## Timeline`
  - `## Notes`
  - `## Decisions`
  - `## Tasks`

## Redaction Policy

If/when you decide to publish a redacted artifact, replace sensitive strings with bracketed placeholders:

- Names: `[PERSON: first-name]` or `[PERSON]` if uncertain
- Addresses: `[ADDRESS]`
- Phone/email: `[PHONE]`, `[EMAIL]`
- Accounts: `[ACCOUNT]`, `[TOKEN]`, `[SECRET]`
- Exact location: use city/region only; if needed: `[LOCATION: approximate]`

If the user asks to store credentials/secrets, keep them out of git entirely (use `.env`, OS keychain, or the Codex auth store).
