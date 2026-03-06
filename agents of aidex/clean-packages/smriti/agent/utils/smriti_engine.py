#!/usr/bin/env python3
"""Smriti chronicler utility: version stamping + release note generation."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
SMRITI_DIR = ROOT / ".smriti"
HISTORY_DIR = SMRITI_DIR / "history"
CHRONICLE_PATH = HISTORY_DIR / "chronicle.json"
CONFIG_PATH = SMRITI_DIR / "smriti.config.json"
RELEASE_DIR = ROOT / "docs" / "release-notes"


def _now_utc_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def _run_git(args: List[str]) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()


def ensure_bootstrap() -> None:
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    RELEASE_DIR.mkdir(parents=True, exist_ok=True)

    if not CONFIG_PATH.exists():
        config = {
            "project_name": ROOT.name,
            "env_mode": "dev",
            "version_scheme": "YYYY.MM.DD.NNNN",
            "mudra": {"placement": "footer", "visible_in_prod": False},
        }
        CONFIG_PATH.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")

    if not CHRONICLE_PATH.exists():
        chronicle = {
            "version": "1.0.0",
            "project": ROOT.name,
            "entries": [],
        }
        CHRONICLE_PATH.write_text(json.dumps(chronicle, indent=2) + "\n", encoding="utf-8")


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: Dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def generate_stamp() -> str:
    ensure_bootstrap()
    today = dt.datetime.now().strftime("%Y.%m.%d")
    chronicle = load_json(CHRONICLE_PATH)
    entries = chronicle.get("entries", [])
    sequence = 1
    if entries:
        last_stamp = str(entries[-1].get("stamp", ""))
        if last_stamp.count(".") == 3:
            last_date = ".".join(last_stamp.split(".")[:3])
            if last_date == today:
                try:
                    sequence = int(last_stamp.split(".")[-1]) + 1
                except ValueError:
                    sequence = 1
    return f"{today}.{sequence:04d}"


def changed_files(base: str | None, staged: bool) -> List[str]:
    if base:
        out = _run_git(["diff", "--name-only", f"{base}..HEAD"])
    elif staged:
        out = _run_git(["diff", "--cached", "--name-only"])
    else:
        out = _run_git(["status", "--porcelain"])
        files: List[str] = []
        for line in out.splitlines():
            if not line:
                continue
            files.append(line[3:])
        return sorted(list(dict.fromkeys(files)))
    return [line for line in out.splitlines() if line]


def git_summary(base: str | None, staged: bool) -> Dict[str, int]:
    if base:
        out = _run_git(["diff", "--shortstat", f"{base}..HEAD"])
    elif staged:
        out = _run_git(["diff", "--cached", "--shortstat"])
    else:
        out = _run_git(["diff", "--shortstat"])
    summary = {"files": 0, "insertions": 0, "deletions": 0}
    for part in out.split(","):
        p = part.strip()
        if " file" in p:
            summary["files"] = int(p.split()[0])
        elif " insertion" in p:
            summary["insertions"] = int(p.split()[0])
        elif " deletion" in p:
            summary["deletions"] = int(p.split()[0])
    return summary


def write_release_note(stamp: str, base: str | None, staged: bool, title: str | None) -> Path:
    ensure_bootstrap()
    files = changed_files(base=base, staged=staged)
    summary = git_summary(base=base, staged=staged)
    heading = title or f"Rishika Release {stamp}"
    date_str = dt.date.today().isoformat()
    out_path = RELEASE_DIR / f"{date_str}-{stamp}.md"

    lines = [
        f"# {heading}",
        "",
        f"- Stamp: `{stamp}`",
        f"- Date: `{date_str}`",
        f"- Scope: `{('git diff ' + base + '..HEAD') if base else ('staged changes' if staged else 'working tree changes')}`",
        f"- Diff summary: `{summary['files']} files changed, {summary['insertions']} insertions, {summary['deletions']} deletions`",
        "",
        "## Changed Files",
        "",
    ]
    if files:
        lines.extend([f"- `{f}`" for f in files])
    else:
        lines.append("- No changed files detected in selected scope.")

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- Validate API contracts in `Readme.md` after release-note generation.",
            "- Confirm security-sensitive changes with a reviewer before production promotion.",
        ]
    )

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path


def append_chronicle(stamp: str, release_note: str, env: str, author: str) -> None:
    ensure_bootstrap()
    chronicle = load_json(CHRONICLE_PATH)
    entries = chronicle.setdefault("entries", [])
    entries.append(
        {
            "stamp": stamp,
            "timestamp": _now_utc_iso(),
            "env": env,
            "author": author,
            "release_note": release_note,
        }
    )
    save_json(CHRONICLE_PATH, chronicle)


def set_env_mode(mode: str) -> None:
    ensure_bootstrap()
    config = load_json(CONFIG_PATH)
    config["env_mode"] = mode
    save_json(CONFIG_PATH, config)


def cmd_init(_: argparse.Namespace) -> None:
    ensure_bootstrap()
    print(f"Initialized Smriti in {SMRITI_DIR}")


def cmd_stamp(_: argparse.Namespace) -> None:
    print(generate_stamp())


def cmd_release_notes(args: argparse.Namespace) -> None:
    stamp = args.stamp or generate_stamp()
    path = write_release_note(stamp=stamp, base=args.base, staged=args.staged, title=args.title)
    append_chronicle(stamp=stamp, release_note=str(path.relative_to(ROOT)), env=args.env, author=args.author)
    print(path)


def cmd_promote(args: argparse.Namespace) -> None:
    set_env_mode(args.env)
    print(f"Updated env_mode to {args.env}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Smriti chronicler utility")
    sub = p.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Initialize .smriti structure")
    p_init.set_defaults(func=cmd_init)

    p_stamp = sub.add_parser("stamp", help="Generate next temporal version stamp")
    p_stamp.set_defaults(func=cmd_stamp)

    p_rel = sub.add_parser("release-notes", help="Generate release note markdown from git state")
    p_rel.add_argument("--stamp", help="Version stamp override")
    p_rel.add_argument("--base", help="Git base ref (example: origin/main)")
    p_rel.add_argument("--staged", action="store_true", help="Use staged diff")
    p_rel.add_argument("--title", help="Release title")
    p_rel.add_argument("--env", default="dev", choices=["dev", "prod"], help="Entry environment")
    p_rel.add_argument("--author", default="Smriti Agent", help="Chronicle author")
    p_rel.set_defaults(func=cmd_release_notes)

    p_promote = sub.add_parser("promote", help="Set environment mode in smriti.config.json")
    p_promote.add_argument("--env", required=True, choices=["dev", "prod"])
    p_promote.set_defaults(func=cmd_promote)

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
