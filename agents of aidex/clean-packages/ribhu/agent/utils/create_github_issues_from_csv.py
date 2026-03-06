#!/usr/bin/env python3
"""
Create GitHub Issues from a CSV backlog file.

- Python 3.9+ compatible (stdlib only)
- Dry-run by default
- Creates missing labels automatically
- Skips duplicate titles by default

Usage examples:
  export GITHUB_TOKEN=ghp_xxx
    python3 .aidex/ribhu/utils/create_github_issues_from_csv.py
    python3 .aidex/ribhu/utils/create_github_issues_from_csv.py --execute
    python3 .aidex/ribhu/utils/create_github_issues_from_csv.py --execute --limit 5
"""

import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Dict, List, Optional

API_BASE = "https://api.github.com"
RETRYABLE_HTTP = {500, 502, 503, 504}


def _request(
    method: str,
    path: str,
    token: str,
    payload: Optional[dict] = None,
    retries: int = 3,
    retry_delay: float = 1.0,
) -> dict:
    url = API_BASE + path
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "sample-project-issue-importer",
    }
    body = None
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    last_error: Optional[Exception] = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(url=url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as err:
            err_body = err.read().decode("utf-8", errors="replace")
            try:
                err_json = json.loads(err_body)
            except Exception:
                err_json = {"message": err_body}
            if err.code in RETRYABLE_HTTP and attempt < retries:
                time.sleep(retry_delay * (attempt + 1))
                continue
            raise RuntimeError(f"HTTP {err.code} {method} {path}: {err_json}") from err
        except urllib.error.URLError as err:
            last_error = err
            if attempt < retries:
                time.sleep(retry_delay * (attempt + 1))
                continue
            raise RuntimeError(f"URL error {method} {path}: {err}") from err

    if last_error is not None:
        raise RuntimeError(f"Request failed {method} {path}: {last_error}")
    raise RuntimeError(f"Request failed {method} {path}")


def _label_color(name: str) -> str:
    key = name.lower()
    if key.startswith("br:"):
        return "5319e7"
    if key.startswith("ers:"):
        return "1d76db"
    if key.startswith("screen:"):
        return "0e8a16"
    if key in {"eng-task", "backend", "frontend", "ai", "storage", "test", "ops", "ingestion"}:
        return "fbca04"
    return "d4c5f9"


def ensure_label(owner: str, repo: str, token: str, name: str) -> None:
    payload = {
        "name": name,
        "color": _label_color(name),
        "description": "Auto-created by sample-project issue importer",
    }
    try:
        _request("POST", f"/repos/{owner}/{repo}/labels", token, payload)
    except RuntimeError as exc:
        text = str(exc)
        if "HTTP 422" in text and "already_exists" in text:
            return
        if "HTTP 422" in text:
            return
        raise


def issue_exists(owner: str, repo: str, token: str, title: str) -> bool:
    query = f'repo:{owner}/{repo} is:issue in:title "{title}"'
    q = urllib.parse.quote(query, safe="")
    data = _request("GET", f"/search/issues?q={q}&per_page=1", token)
    return int(data.get("total_count", 0)) > 0


def labels_missing_in_error(exc: Exception) -> bool:
    text = str(exc).lower()
    return "label" in text and ("validation" in text or "invalid" in text or "does not exist" in text)


def parse_labels(raw: str) -> List[str]:
    if not raw:
        return ["eng-task"]
    return [x.strip() for x in raw.split("|") if x.strip()]


def build_issue_body(row: Dict[str, str]) -> str:
    lines = [
        "## Traceability",
        f"- BR_ID: {row.get('BR_ID', '').strip()}",
        f"- ERS_ID: {row.get('ERS_ID', '').strip()}",
        f"- Epic_Ref: {row.get('Epic_Ref', '').strip()}",
        f"- Screen: {row.get('Screen', '').strip()}",
        "",
        "## Planning",
        f"- Depends_On: {row.get('Depends_On', '').strip() or 'none'}",
        f"- Size: {row.get('Size', '').strip()}",
        f"- Estimate_points: {row.get('Estimate_points', '').strip()}",
        f"- Planned_Pushes: {row.get('Planned_Pushes', '').strip()}",
        f"- Push_Cadence: {row.get('Push_Cadence', '').strip()}",
        "",
        "## Acceptance",
        row.get("Acceptance", "").strip(),
        "",
        "## Type",
        row.get("Type", "ENG Task").strip(),
    ]
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create GitHub issues from backlog CSV")
    parser.add_argument("--csv", default=".aidex/ribhu/github_task_backlog.csv", help="Path to backlog CSV")
    parser.add_argument("--owner", default="enkayxyz", help="GitHub owner")
    parser.add_argument("--repo", default="sample-project", help="GitHub repo")
    parser.add_argument("--token-env", default="GITHUB_TOKEN", help="Env var containing GitHub token")
    parser.add_argument("--execute", action="store_true", help="Actually create issues (default is dry-run)")
    parser.add_argument("--allow-duplicates", action="store_true", help="Allow duplicate titles")
    parser.add_argument("--limit", type=int, default=0, help="Only process first N rows")
    args = parser.parse_args()

    token = os.environ.get(args.token_env, "").strip()
    if not token:
        print(f"ERROR: Missing token. Set {args.token_env} in environment.")
        return 2

    if not os.path.exists(args.csv):
        print(f"ERROR: CSV not found: {args.csv}")
        return 2

    with open(args.csv, "r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))

    if args.limit and args.limit > 0:
        rows = rows[: args.limit]

    mode = "EXECUTE" if args.execute else "DRY-RUN"
    print(f"Mode: {mode}")
    print(f"Repo: {args.owner}/{args.repo}")
    print(f"Rows: {len(rows)}")
    print("-" * 80)

    created = 0
    skipped = 0

    for idx, row in enumerate(rows, start=1):
        issue_id = row.get("Issue_ID", "").strip()
        title_part = row.get("Title", "").strip()
        title = f"{issue_id}: {title_part}" if issue_id else title_part
        if not title:
            print(f"[{idx}] SKIP missing title")
            skipped += 1
            continue

        labels = parse_labels(row.get("Labels", ""))

        if not args.allow_duplicates:
            try:
                if issue_exists(args.owner, args.repo, token, title):
                    print(f"[{idx}] SKIP duplicate title: {title}")
                    skipped += 1
                    continue
            except Exception as exc:
                print(f"[{idx}] WARN duplicate check failed for '{title}': {exc}")

        print(f"[{idx}] {title}")
        print(f"     labels={labels}")

        if not args.execute:
            continue

        for label in labels:
            try:
                ensure_label(args.owner, args.repo, token, label)
            except Exception as exc:
                print(f"     WARN label ensure failed for '{label}': {exc}")

        payload = {
            "title": title,
            "body": build_issue_body(row),
            "labels": labels,
        }

        try:
            result = _request("POST", f"/repos/{args.owner}/{args.repo}/issues", token, payload)
            url = result.get("html_url", "")
            number = result.get("number", "")
            print(f"     CREATED #{number} {url}")
            created += 1
            time.sleep(0.2)
        except Exception as exc:
            if labels and labels_missing_in_error(exc):
                print("     WARN issue create failed due labels; retrying without labels")
                payload_no_labels = {
                    "title": title,
                    "body": build_issue_body(row),
                }
                try:
                    result = _request("POST", f"/repos/{args.owner}/{args.repo}/issues", token, payload_no_labels)
                    url = result.get("html_url", "")
                    number = result.get("number", "")
                    print(f"     CREATED (no-labels) #{number} {url}")
                    created += 1
                    time.sleep(0.2)
                    continue
                except Exception as exc2:
                    print(f"     ERROR creating '{title}' without labels: {exc2}")
            else:
                print(f"     ERROR creating '{title}': {exc}")

    print("-" * 80)
    print(f"Done. created={created} skipped={skipped} total_processed={len(rows)}")
    if not args.execute:
        print("Dry-run only. Re-run with --execute to create issues.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
