#!/usr/bin/env python3
"""Create or verify the durable improvement-item progress ledger.

The ledger is root-owned coordination state for the 2026-06 improvement
backlog. It mirrors the stable 800-item inventory generated under
docs/research/improvements-2026-06 and preserves per-item progress fields when
re-run during long goal execution.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = REPO_ROOT / "docs" / "research" / "improvements-2026-06"
SOURCE_JSON = SOURCE_DIR / "improvements.json"
VIEWER_HTML = REPO_ROOT / "docs" / "research" / "improvement-items-viewer-2026-06.html"
OUTPUT_JSON = REPO_ROOT / "docs" / "ops" / "improvement-items-progress-2026-06.json"
OUTPUT_MD = REPO_ROOT / "docs" / "ops" / "improvement-items-progress-2026-06.md"

PROJECT_WAVES = {
    "android-support": 1,
    "all-web-ui": 1,
    "keelim-plugin": 1,
    "keelim-vercel": 2,
    "youtube": 2,
    "Keelim-Knowledge-Vault": 2,
    "rich": 3,
    "all": 3,
}
PROJECT_ORDER = {project: index for index, project in enumerate(PROJECT_WAVES)}
STATUS_VALUES = ("todo", "assigned", "in_progress", "verified", "blocked", "needs_consumer_check")

DIMENSION_SLUGS = {
    "N+1 쿼리": "n-plus-one-query",
    "번들 크기": "bundle-size",
    "불필요한 use client": "client-component",
    "이미지 최적화": "image-optimization",
    "캐싱 미활용": "cache",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify existing ledger without writing.")
    parser.add_argument(
        "--set-task-status",
        nargs=2,
        metavar=("TASK_ID", "STATUS"),
        help="Set all items in a task unit to STATUS and rewrite the ledgers.",
    )
    parser.add_argument(
        "--set-item-status",
        nargs=2,
        metavar=("ITEM_ID", "STATUS"),
        help="Set one backlog item to STATUS and rewrite the ledgers.",
    )
    parser.add_argument(
        "--print-task-prompt",
        metavar="TASK_ID",
        help="Print a self-contained worker prompt for a task unit.",
    )
    parser.add_argument("--owner", help="Owner/subagent label to record with --set-task-status.")
    parser.add_argument(
        "--verification-command",
        action="append",
        default=[],
        help="Verification command to append when using --set-item-status.",
    )
    parser.add_argument(
        "--verification-result",
        help="Verification result/evidence text when using --set-item-status.",
    )
    parser.add_argument(
        "--changed-file",
        action="append",
        default=[],
        help="Changed file path to append when using --set-item-status.",
    )
    parser.add_argument("--blocked-reason", help="Blocker text when using --set-item-status blocked.")
    return parser.parse_args()


def slug(value: str) -> str:
    value = DIMENSION_SLUGS.get(value, value)
    cleaned = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return cleaned or "misc"


def load_source_items() -> list[dict[str, Any]]:
    payload = json.loads(SOURCE_JSON.read_text(encoding="utf-8"))
    items = payload.get("items")
    if not isinstance(items, list):
        raise SystemExit(f"{SOURCE_JSON} does not contain an items list")
    return items


def load_existing_items() -> dict[str, dict[str, Any]]:
    if not OUTPUT_JSON.exists():
        return {}
    payload = json.loads(OUTPUT_JSON.read_text(encoding="utf-8"))
    return {item["id"]: item for item in payload.get("items", []) if isinstance(item, dict)}


def task_sort_key(task: dict[str, Any]) -> tuple[int, int, int, str]:
    return (
        task["wave"],
        PROJECT_ORDER.get(task["project"], 99),
        -task["p1"],
        task["dimension"],
    )


def build_ledger(items: list[dict[str, Any]], existing: dict[str, dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        grouped[(item["project"], item["dimension"])].append(item)

    tasks = []
    ordered_groups = sorted(
        grouped.items(),
        key=lambda entry: (
            PROJECT_WAVES.get(entry[0][0], 9),
            PROJECT_ORDER.get(entry[0][0], 99),
            entry[0][1],
        ),
    )
    for index, ((project, dimension), task_items) in enumerate(ordered_groups, start=1):
        counts = Counter(item["severity"] for item in task_items)
        task_id = f"T{index:02d}-{slug(project)}-{slug(dimension)}"
        tasks.append(
            {
                "task_id": task_id,
                "wave": PROJECT_WAVES.get(project, 9),
                "project": project,
                "dimension": dimension,
                "total": len(task_items),
                "p1": counts.get("P1", 0),
                "p2": counts.get("P2", 0),
                "status": "todo",
            }
        )
    tasks.sort(key=task_sort_key)
    task_id_by_key = {(task["project"], task["dimension"]): task["task_id"] for task in tasks}

    ledger_items = []
    for item in sorted(
        items,
        key=lambda value: (
            PROJECT_WAVES.get(value["project"], 9),
            PROJECT_ORDER.get(value["project"], 99),
            task_id_by_key[(value["project"], value["dimension"])],
            0 if value["severity"] == "P1" else 1,
            value["id"],
        ),
    ):
        prior = existing.get(item["id"], {})
        status = prior.get("status", "todo")
        if status not in STATUS_VALUES:
            status = "todo"
        ledger_items.append(
            {
                "id": item["id"],
                "project": item["project"],
                "dimension": item["dimension"],
                "severity": item["severity"],
                "effort": item.get("effort", "M"),
                "task_id": task_id_by_key[(item["project"], item["dimension"])],
                "status": status,
                "owner": prior.get("owner"),
                "title": item["title"],
                "file_path": item["file_path"],
                "verification_commands": prior.get("verification_commands", []),
                "verification_result": prior.get("verification_result"),
                "changed_files": prior.get("changed_files", []),
                "blocked_reason": prior.get("blocked_reason"),
                "last_updated": prior.get("last_updated"),
            }
        )

    ledger = {
        "version": 1,
        "source": {
            "viewer": str(VIEWER_HTML.relative_to(REPO_ROOT)),
            "inventory": str(SOURCE_JSON.relative_to(REPO_ROOT)),
            "rawDir": str((SOURCE_DIR / "raw").relative_to(REPO_ROOT)),
        },
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "statusValues": list(STATUS_VALUES),
        "counts": {},
        "taskUnits": tasks,
        "items": ledger_items,
    }
    refresh_counts_and_task_statuses(ledger)
    return ledger


def derive_task_status(statuses: list[str]) -> str:
    if not statuses:
        return "todo"
    counts = Counter(statuses)
    if counts["verified"] == len(statuses):
        return "verified"
    if counts["blocked"] == len(statuses):
        return "blocked"
    for status in ("in_progress", "needs_consumer_check", "assigned"):
        if counts[status]:
            return status
    if counts["verified"] or counts["blocked"]:
        return "in_progress"
    return "todo"


def refresh_counts_and_task_statuses(ledger: dict[str, Any]) -> None:
    items = ledger["items"]
    task_statuses: dict[str, list[str]] = defaultdict(list)
    for item in items:
        task_statuses[item["task_id"]].append(item["status"])

    for task in ledger["taskUnits"]:
        task["status"] = derive_task_status(task_statuses.get(task["task_id"], []))

    item_statuses = Counter(item["status"] for item in items)
    severity_counts = Counter(item["severity"] for item in items)
    project_counts: dict[str, dict[str, int]] = {}
    for item in items:
        entry = project_counts.setdefault(item["project"], {"total": 0, "P1": 0, "P2": 0})
        entry["total"] += 1
        entry[item["severity"]] = entry.get(item["severity"], 0) + 1

    ledger["counts"] = {
        "total": len(items),
        "bySeverity": dict(sorted(severity_counts.items())),
        "byStatus": {status: item_statuses.get(status, 0) for status in STATUS_VALUES},
        "byProject": project_counts,
    }


def apply_task_status(
    ledger: dict[str, Any],
    task_id: str,
    status: str,
    owner: str | None,
    verification_commands: list[str],
    verification_result: str | None,
    changed_files: list[str],
    blocked_reason: str | None,
) -> None:
    if status not in STATUS_VALUES:
        raise SystemExit(f"invalid status {status!r}; expected one of {', '.join(STATUS_VALUES)}")
    known_task_ids = {task["task_id"] for task in ledger["taskUnits"]}
    if task_id not in known_task_ids:
        raise SystemExit(f"unknown task_id {task_id!r}")
    timestamp = datetime.now(timezone.utc).isoformat()
    changed = 0
    for item in ledger["items"]:
        if item["task_id"] == task_id:
            item["status"] = status
            if owner:
                item["owner"] = owner
            if verification_commands:
                item["verification_commands"] = append_unique(
                    item.get("verification_commands", []), verification_commands
                )
            if verification_result:
                item["verification_result"] = verification_result
            if changed_files:
                item["changed_files"] = append_unique(item.get("changed_files", []), changed_files)
            if blocked_reason:
                item["blocked_reason"] = blocked_reason
            elif status != "blocked":
                item["blocked_reason"] = None
            item["last_updated"] = timestamp
            changed += 1
    if changed == 0:
        raise SystemExit(f"task_id {task_id!r} has no items")
    refresh_counts_and_task_statuses(ledger)


def append_unique(values: list[str], additions: list[str]) -> list[str]:
    result = list(values)
    seen = set(result)
    for value in additions:
        if value and value not in seen:
            result.append(value)
            seen.add(value)
    return result


def apply_item_status(
    ledger: dict[str, Any],
    item_id: str,
    status: str,
    owner: str | None,
    verification_commands: list[str],
    verification_result: str | None,
    changed_files: list[str],
    blocked_reason: str | None,
) -> None:
    if status not in STATUS_VALUES:
        raise SystemExit(f"invalid status {status!r}; expected one of {', '.join(STATUS_VALUES)}")
    timestamp = datetime.now(timezone.utc).isoformat()
    for item in ledger["items"]:
        if item["id"] != item_id:
            continue
        item["status"] = status
        if owner:
            item["owner"] = owner
        if verification_commands:
            item["verification_commands"] = append_unique(
                item.get("verification_commands", []), verification_commands
            )
        if verification_result:
            item["verification_result"] = verification_result
        if changed_files:
            item["changed_files"] = append_unique(item.get("changed_files", []), changed_files)
        if blocked_reason:
            item["blocked_reason"] = blocked_reason
        elif status != "blocked":
            item["blocked_reason"] = None
        item["last_updated"] = timestamp
        refresh_counts_and_task_statuses(ledger)
        return
    raise SystemExit(f"unknown item id {item_id!r}")


def render_markdown(ledger: dict[str, Any]) -> str:
    counts = ledger["counts"]
    lines = [
        "# Improvement Items Progress — 2026-06",
        "",
        "Durable `/goal` ledger for completing every P1/P2 item from the June 2026 improvement backlog.",
        "",
        f"- Source viewer: `{ledger['source']['viewer']}`",
        f"- Source inventory: `{ledger['source']['inventory']}`",
        f"- Raw task inventory: `{ledger['source']['rawDir']}`",
        f"- Total: {counts['total']} · P1 {counts['bySeverity'].get('P1', 0)} · P2 {counts['bySeverity'].get('P2', 0)}",
        "",
        "## Status",
        "",
        "| status | count |",
        "|---|---:|",
    ]
    for status, count in counts["byStatus"].items():
        lines.append(f"| `{status}` | {count} |")

    lines.extend(["", "## Task Queue", "", "| wave | task | project | dimension | total | P1 | P2 | status |", "|---:|---|---|---|---:|---:|---:|---|"])
    for task in ledger["taskUnits"]:
        lines.append(
            f"| {task['wave']} | `{task['task_id']}` | `{task['project']}` | `{task['dimension']}` | "
            f"{task['total']} | {task['p1']} | {task['p2']} | `{task['status']}` |"
        )

    lines.extend(
        [
            "",
            "## Completion Rules",
            "",
            "- Mark an item `verified` only after a repo-local test, build, lint, static check, or documented manual evidence covers it.",
            "- Keep implementation inside the owning child repo after reading that repo's `AGENTS.md`.",
            "- Do not touch archived `toto` or excluded `quant`.",
            "- Run `bun run report:baseline` before and after the aggregate run.",
            "- Run `bun run report:shared-ui` whenever `all-web-ui` public contracts or `keelim-vercel`/`rich` shared UI consumers change.",
        ]
    )
    return "\n".join(lines) + "\n"


def validate_ledger(ledger: dict[str, Any], source_items: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    source_ids = {item["id"] for item in source_items}
    ledger_ids = [item.get("id") for item in ledger.get("items", [])]
    if len(ledger_ids) != len(source_ids):
        errors.append(f"ledger item count {len(ledger_ids)} != source item count {len(source_ids)}")
    if len(set(ledger_ids)) != len(ledger_ids):
        errors.append("ledger contains duplicate item ids")
    missing = source_ids - set(ledger_ids)
    extra = set(ledger_ids) - source_ids
    if missing:
        errors.append(f"ledger missing ids: {', '.join(sorted(missing)[:10])}")
    if extra:
        errors.append(f"ledger has extra ids: {', '.join(sorted(extra)[:10])}")
    for item in ledger.get("items", []):
        if item.get("status") not in STATUS_VALUES:
            errors.append(f"{item.get('id')}: invalid status {item.get('status')}")
    task_ids = {task["task_id"] for task in ledger.get("taskUnits", [])}
    for item in ledger.get("items", []):
        if item.get("task_id") not in task_ids:
            errors.append(f"{item.get('id')}: unknown task_id {item.get('task_id')}")
    return errors


def print_task_prompt(ledger: dict[str, Any], task_id: str) -> int:
    task = next((task for task in ledger["taskUnits"] if task["task_id"] == task_id), None)
    if not task:
        print(f"unknown task_id {task_id}", file=sys.stderr)
        return 1
    items = [item for item in ledger["items"] if item["task_id"] == task_id]
    ids = ", ".join(item["id"] for item in items)
    source_hint = f"docs/research/improvements-2026-06/improvements.json filtered by task_id {task_id}"
    raw_hint = f"docs/research/improvements-2026-06/raw/{task['project']}-{slug(task['dimension'])}.json"
    print(
        f"""You are a subagent for the active Ultragoal run in {REPO_ROOT}.
Task: handle {task_id} for project `{task['project']}`, dimension `{task['dimension']}`.

Source inventory: {source_hint}
Potential raw analysis file: {raw_hint} when present; if raw IDs differ, map by title/file_path and report final ledger IDs.
Final selected ledger IDs ({len(items)}): {ids}

Scope:
- Work only inside `{task['project']}`.
- Read root `AGENTS.md` and `{task['project']}/AGENTS.md` before editing.
- Preserve existing dirty work and never revert unrelated changes.
- Do not edit root ledger files, `.omx/ultragoal`, archived `toto`, excluded `quant`, or sibling repos.

Required output:
- Backlog IDs handled, changed files, verification commands/results, and blockers if any.
- Mark nothing complete yourself; the leader updates ledgers and Ultragoal checkpoints from your evidence.
"""
    )
    return 0


def main() -> int:
    args = parse_args()
    source_items = load_source_items()
    if args.check and (args.set_task_status or args.set_item_status or args.print_task_prompt):
        raise SystemExit("--check cannot be combined with other actions")
    if args.set_task_status and args.set_item_status:
        raise SystemExit("--set-task-status and --set-item-status are mutually exclusive")
    if args.check:
        if not OUTPUT_JSON.exists() or not OUTPUT_MD.exists():
            print("FAIL: progress ledger files are missing")
            return 1
        ledger = json.loads(OUTPUT_JSON.read_text(encoding="utf-8"))
        errors = validate_ledger(ledger, source_items)
        if errors:
            print("FAIL")
            for error in errors:
                print(f"  - {error}")
            return 1
        print(
            "OK: "
            f"{ledger['counts']['total']} items, "
            f"{len(ledger['taskUnits'])} task units, "
            f"{ledger['counts']['byStatus'].get('verified', 0)} verified"
        )
        return 0

    ledger = build_ledger(source_items, load_existing_items())
    if args.print_task_prompt:
        return print_task_prompt(ledger, args.print_task_prompt)
    if args.set_task_status:
        task_id, status = args.set_task_status
        apply_task_status(
            ledger,
            task_id,
            status,
            args.owner,
            args.verification_command,
            args.verification_result,
            args.changed_file,
            args.blocked_reason,
        )
    if args.set_item_status:
        item_id, status = args.set_item_status
        apply_item_status(
            ledger,
            item_id,
            status,
            args.owner,
            args.verification_command,
            args.verification_result,
            args.changed_file,
            args.blocked_reason,
        )
    OUTPUT_JSON.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(render_markdown(ledger), encoding="utf-8")
    print(f"wrote {OUTPUT_JSON.relative_to(REPO_ROOT)}")
    print(f"wrote {OUTPUT_MD.relative_to(REPO_ROOT)}")
    print(f"{ledger['counts']['total']} items across {len(ledger['taskUnits'])} task units")
    return 0


if __name__ == "__main__":
    sys.exit(main())
