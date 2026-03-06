#!/usr/bin/env python3
"""Sync ENG completion certificate to GitHub issue/project review status."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def build_comment(cert: dict, task_id: str) -> str:
    tr = cert.get("traceability", {})
    checks = cert.get("acceptance_checks", [])
    checks_lines = []
    for item in checks:
        checks_lines.append(f"- {item.get('check')}: {item.get('result')}")

    cmds = cert.get("commands_run", [])
    cmd_lines = []
    for item in cmds:
        cmd_lines.append(f"- `{item.get('command')}` -> {item.get('exit_code')}")

    note = cert.get("architect_clarification_note")
    note_block = f"\nArchitect note: {note}\n" if note else ""

    return (
        f"### {task_id} Completion Sync\n"
        f"Status: `{cert.get('status')}`\n"
        f"Traceability: BR `{tr.get('BR_ID')}`, ERS `{tr.get('ERS_ID')}`, Epic `{tr.get('Epic_Ref')}`, Screen `{tr.get('Screen')}`\n\n"
        f"Acceptance checks:\n" + "\n".join(checks_lines) + "\n\n"
        f"Commands:\n" + "\n".join(cmd_lines) + "\n"
        + note_block
    )


def all_checks_pass_or_na(cert: dict) -> bool:
    for check in cert.get("acceptance_checks", []):
        if check.get("result") not in {"pass", "na"}:
            return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True)
    parser.add_argument("--issue", required=True)
    parser.add_argument("--status", required=True, choices=["completed", "blocked", "partial"])
    parser.add_argument("--certificate", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    cert_path = Path(args.certificate)
    cert = json.loads(cert_path.read_text(encoding="utf-8"))
    comment = build_comment(cert, args.task)

    if args.dry_run:
        print(comment)
        return 0

    run(["gh", "issue", "comment", args.issue, "--body", comment])

    if args.status == "completed" and all_checks_pass_or_na(cert):
        run(["gh", "issue", "edit", args.issue, "--add-label", "status:ready-for-review"])

        project_id = os.getenv("GH_PROJECT_ID")
        status_field_id = os.getenv("GH_PROJECT_STATUS_FIELD_ID")
        ready_option_id = os.getenv("GH_PROJECT_READY_OPTION_ID")
        item_id = os.getenv("GH_PROJECT_ITEM_ID")

        if project_id and status_field_id and ready_option_id and item_id:
            mutation = (
                "mutation($project:ID!, $item:ID!, $field:ID!, $option:String!) {"
                " updateProjectV2ItemFieldValue(input:{projectId:$project,itemId:$item,fieldId:$field,"
                "value:{singleSelectOptionId:$option}}){projectV2Item{id}} }"
            )
            run(
                [
                    "gh",
                    "api",
                    "graphql",
                    "-f",
                    f"query={mutation}",
                    "-f",
                    f"project={project_id}",
                    "-f",
                    f"item={item_id}",
                    "-f",
                    f"field={status_field_id}",
                    "-f",
                    f"option={ready_option_id}",
                ]
            )

    return 0


if __name__ == "__main__":
    sys.exit(main())
