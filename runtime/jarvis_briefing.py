#!/usr/bin/env python3
import argparse
import datetime as dt
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def parse_date(s):
    return dt.date.fromisoformat(s)


def load_daily_json(d):
    p = REPO_ROOT / "data" / "daily" / f"{d.isoformat()}.json"
    if not p.exists():
        raise SystemExit(f"error: missing {p} (run ./bin/codex sync first)")
    return json.loads(p.read_text(encoding="utf-8"))


def default_today():
    return dt.date.today()


def briefing_for(today, yesterday_daily):
    ydate = yesterday_daily.get("date")
    title = f"Morning Briefing: {today.isoformat()} (from {ydate})"

    mood = yesterday_daily.get("mood")
    energy = yesterday_daily.get("energy")
    tags = yesterday_daily.get("tags") or []
    tasks = yesterday_daily.get("tasks") or []

    open_tasks = [t for t in tasks if not t.get("done")]
    done_tasks = [t for t in tasks if t.get("done")]

    lines = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append("## Signals")
    lines.append("")
    if mood is not None:
        lines.append(f"- Mood: {mood}")
    if energy is not None:
        lines.append(f"- Energy: {energy}")
    if tags:
        lines.append("- Themes: " + ", ".join(tags))
    if mood is None and energy is None and not tags:
        lines.append("- (no structured signals captured)")
    lines.append("")
    lines.append("## Yesterday Recap (Raw)")
    lines.append("")
    raw = (yesterday_daily.get("raw_text") or "").strip()
    lines.append(raw if raw else "(no raw text captured)")
    lines.append("")
    lines.append("## Tasks")
    lines.append("")
    if open_tasks:
        lines.append("Open:")
        for t in open_tasks:
            lines.append(f"- [ ] {t.get('text','').strip()}")
    else:
        lines.append("Open:")
        lines.append("- (none)")
    lines.append("")
    if done_tasks:
        lines.append("Done:")
        for t in done_tasks:
            lines.append(f"- [x] {t.get('text','').strip()}")
        lines.append("")
    lines.append("## Today Focus (Fill Manually)")
    lines.append("")
    lines.append("- Top 1 outcome:")
    lines.append("- Top 3 tasks:")
    lines.append("- One risk to watch:")
    lines.append("")
    return "\n".join(lines)


def write_report(today, content):
    out_dir = REPO_ROOT / "reports" / "briefing"
    out_dir.mkdir(parents=True, exist_ok=True)
    p = out_dir / f"{today.isoformat()}.md"
    p.write_text(content + "\n", encoding="utf-8")
    return str(p)


def main():
    ap = argparse.ArgumentParser(description="Generate a morning briefing for today from yesterday's synced JSON.")
    ap.add_argument("--date", help="Today's date (YYYY-MM-DD). Defaults to today.")
    args = ap.parse_args()

    today = parse_date(args.date) if args.date else default_today()
    yesterday = today - dt.timedelta(days=1)
    yd = load_daily_json(yesterday)
    content = briefing_for(today, yd)
    out = write_report(today, content)
    print(out)


if __name__ == "__main__":
    main()

