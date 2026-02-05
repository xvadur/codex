#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
from pathlib import Path

from runtime.lib.notion_client import NotionError, list_block_children, query_database
from runtime.lib.notion_extract import blocks_to_plaintext, blocks_to_tasks, extract_property


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_config():
    cfg_path = REPO_ROOT / "runtime" / "config.json"
    if not cfg_path.exists():
        cfg_path = REPO_ROOT / "runtime" / "config.example.json"
    return json.loads(cfg_path.read_text(encoding="utf-8"))


def parse_date(s):
    return dt.date.fromisoformat(s)


def default_target_date(today=None):
    today = today or dt.date.today()
    return today - dt.timedelta(days=1)


def notion_db_id(cfg):
    env_name = cfg["notion"].get("daily_db_id_env", "NOTION_DAILY_DB_ID")
    val = os.environ.get(env_name)
    if not val:
        raise RuntimeError(f"missing env {env_name}")
    return val


def fetch_daily_page(cfg, target_date):
    db_id = notion_db_id(cfg)
    date_prop = cfg["notion"].get("date_property", "Date")
    date_str = target_date.isoformat()

    # Filter: Date property equals YYYY-MM-DD.
    filter_obj = {"property": date_prop, "date": {"equals": date_str}}
    res = query_database(db_id, filter_obj=filter_obj, page_size=5)
    results = res.get("results") or []
    if not results:
        raise RuntimeError(f"no Notion daily page for {date_str} (property '{date_prop}')")
    if len(results) > 1:
        # Pick the first; keep deterministic.
        pass
    return results[0]


def fetch_all_blocks(page_id):
    blocks = []
    cursor = None
    while True:
        res = list_block_children(page_id, start_cursor=cursor)
        blocks.extend(res.get("results") or [])
        if not res.get("has_more"):
            break
        cursor = res.get("next_cursor")
        if not cursor:
            break
    return blocks


def normalize(cfg, page, blocks, target_date):
    props = page.get("properties") or {}

    title_prop = cfg["notion"].get("title_property", "Name")
    mood_prop = cfg["notion"].get("mood_property", "Mood")
    energy_prop = cfg["notion"].get("energy_property", "Energy")
    tags_prop = cfg["notion"].get("tags_property", "Tags")
    privacy_prop = cfg["notion"].get("privacy_property", "Privacy")

    title = extract_property(props, title_prop) or target_date.isoformat()
    mood = extract_property(props, mood_prop)
    energy = extract_property(props, energy_prop)
    tags = extract_property(props, tags_prop) or []
    privacy = extract_property(props, privacy_prop)

    plain = blocks_to_plaintext(blocks)
    tasks = blocks_to_tasks(blocks)

    return {
        "date": target_date.isoformat(),
        "title": title,
        "mood": mood,
        "energy": energy,
        "tags": tags,
        "privacy": privacy,
        "notion": {
            "page_id": page.get("id"),
            "url": page.get("url"),
        },
        "raw_text": plain,
        "tasks": tasks,
    }


def render_md(cfg, daily):
    date = daily["date"]
    tags = daily.get("tags") or cfg["render"].get("default_tags", [])
    privacy = daily.get("privacy") or cfg["render"].get("default_privacy", "public")

    lines = []
    lines.append("---")
    lines.append(f"date: {date}")
    lines.append("tags: " + json.dumps(tags, ensure_ascii=True))
    if daily.get("mood") is not None:
        lines.append(f"mood: {daily['mood']}")
    if daily.get("energy") is not None:
        lines.append(f"energy: {daily['energy']}")
    lines.append(f"privacy: {privacy}")
    lines.append("---")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("## Timeline")
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    if cfg["render"].get("include_raw_notion_text", True):
        raw = (daily.get("raw_text") or "").strip()
        if raw:
            lines.append("### Raw Capture (Notion)")
            lines.append("")
            lines.append(raw)
            lines.append("")
    lines.append("## Decisions")
    lines.append("")
    lines.append("## Tasks")
    lines.append("")
    tasks = daily.get("tasks") or []
    if tasks:
        for t in tasks:
            box = "x" if t.get("done") else " "
            lines.append(f"- [{box}] {t.get('text','').strip()}")
    else:
        lines.append("- [ ]")
    lines.append("")
    return "\n".join(lines)


def write_outputs(daily, md, overwrite=False):
    date = daily["date"]
    yyyy = date[0:4]

    data_dir = REPO_ROOT / "data" / "daily"
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / f"{date}.json").write_text(json.dumps(daily, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

    life_dir = REPO_ROOT / "life" / yyyy
    life_dir.mkdir(parents=True, exist_ok=True)
    md_path = life_dir / f"{date}.md"
    if md_path.exists() and not overwrite:
        return str(md_path)
    md_path.write_text(md, encoding="utf-8")
    return str(md_path)


def main():
    ap = argparse.ArgumentParser(description="Sync yesterday (default) from Notion into JSON + Markdown.")
    ap.add_argument("--date", help="Target date (YYYY-MM-DD). Defaults to yesterday.")
    ap.add_argument("--overwrite", action="store_true", help="Overwrite existing life/YYYY/YYYY-MM-DD.md")
    args = ap.parse_args()

    cfg = load_config()
    target = parse_date(args.date) if args.date else default_target_date()

    try:
        page = fetch_daily_page(cfg, target)
        blocks = fetch_all_blocks(page["id"])
        daily = normalize(cfg, page, blocks, target)
    except NotionError as e:
        raise SystemExit(f"error: {e}")

    md = render_md(cfg, daily)
    out = write_outputs(daily, md, overwrite=args.overwrite)
    print(out)


if __name__ == "__main__":
    main()

