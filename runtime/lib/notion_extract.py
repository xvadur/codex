def _rich_text_to_plain(rich_text):
    parts = []
    for rt in rich_text or []:
        if isinstance(rt, dict):
            parts.append(rt.get("plain_text", "") or "")
    return "".join(parts).strip()


def extract_property(props, name):
    if not props or not name or name not in props:
        return None
    p = props.get(name) or {}
    ptype = p.get("type")
    if ptype == "title":
        return _rich_text_to_plain(p.get("title"))
    if ptype == "rich_text":
        return _rich_text_to_plain(p.get("rich_text"))
    if ptype == "select":
        sel = p.get("select")
        return sel.get("name") if isinstance(sel, dict) else None
    if ptype == "multi_select":
        ms = p.get("multi_select") or []
        return [x.get("name") for x in ms if isinstance(x, dict) and x.get("name")]
    if ptype == "number":
        return p.get("number")
    if ptype == "date":
        d = p.get("date")
        return d.get("start") if isinstance(d, dict) else None
    if ptype == "checkbox":
        return p.get("checkbox")
    return None


def _block_text(block):
    t = block.get("type")
    obj = block.get(t) or {}
    if t in ("paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item", "numbered_list_item", "quote", "callout"):
        return _rich_text_to_plain(obj.get("rich_text"))
    if t == "to_do":
        text = _rich_text_to_plain(obj.get("rich_text"))
        checked = bool(obj.get("checked"))
        return f"[{'x' if checked else ' '}] {text}".strip()
    if t == "code":
        # Keep as a single line; the renderer can decide whether to format.
        text = _rich_text_to_plain(obj.get("rich_text"))
        lang = obj.get("language") or ""
        return f"[code:{lang}] {text}".strip()
    return None


def blocks_to_plaintext(blocks):
    lines = []
    for b in blocks or []:
        txt = _block_text(b)
        if txt:
            lines.append(txt)
    return "\n".join(lines).strip()


def blocks_to_tasks(blocks):
    tasks = []
    for b in blocks or []:
        if b.get("type") != "to_do":
            continue
        obj = b.get("to_do") or {}
        text = _rich_text_to_plain(obj.get("rich_text"))
        if not text:
            continue
        tasks.append(
            {
                "text": text,
                "done": bool(obj.get("checked")),
            }
        )
    return tasks

