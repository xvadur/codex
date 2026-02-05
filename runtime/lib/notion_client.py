import json
import os
import urllib.request
import urllib.error


NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"


class NotionError(RuntimeError):
    pass


def _headers():
    token = os.environ.get("NOTION_TOKEN")
    if not token:
        raise NotionError("missing env NOTION_TOKEN")
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "codex-life-runtime/1.0",
    }


def _request(method, path, body=None):
    url = f"{NOTION_API}{path}"
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url, data=data, method=method, headers=_headers())
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        msg = e.read().decode("utf-8", errors="replace")
        raise NotionError(f"notion http {e.code}: {msg}") from e
    except urllib.error.URLError as e:
        raise NotionError(f"notion url error: {e}") from e


def query_database(db_id, filter_obj=None, sorts=None, page_size=10):
    body = {"page_size": page_size}
    if filter_obj:
        body["filter"] = filter_obj
    if sorts:
        body["sorts"] = sorts
    return _request("POST", f"/databases/{db_id}/query", body=body)


def list_block_children(block_id, start_cursor=None, page_size=100):
    qs = f"?page_size={page_size}"
    if start_cursor:
        qs += f"&start_cursor={start_cursor}"
    return _request("GET", f"/blocks/{block_id}/children{qs}")

