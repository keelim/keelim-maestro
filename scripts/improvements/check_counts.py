#!/usr/bin/env python3
"""Verify improvements.json and report-input.json invariants before delivery.

Checks:
- per-project count == target (100), total == projects * target
- IDs unique, severity in {P1,P2,P3}, file_path exists
- report-input tables row counts match improvements.json
- no remote URLs anywhere
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BASE_DIR = REPO_ROOT / "docs" / "research" / "improvements-2026-06"

EXPECTED_PROJECTS = (
    "all",
    "android-support",
    "Keelim-Knowledge-Vault",
    "keelim-plugin",
    "keelim-vercel",
    "rich",
    "youtube",
    "all-web-ui",
)
TARGET = 100
_LINE_SUFFIX = re.compile(r"(:\d+)+$")


def main() -> int:
    errors: list[str] = []

    improvements = json.loads((BASE_DIR / "improvements.json").read_text(encoding="utf-8"))
    items = improvements["items"]

    counts: dict[str, int] = {}
    seen_ids: set[str] = set()
    for item in items:
        counts[item["project"]] = counts.get(item["project"], 0) + 1
        if item["id"] in seen_ids:
            errors.append(f"duplicate id: {item['id']}")
        seen_ids.add(item["id"])
        if item["severity"] not in ("P1", "P2", "P3"):
            errors.append(f"{item['id']}: invalid severity {item['severity']}")
        norm = _LINE_SUFFIX.sub("", item["file_path"]).lstrip("/")
        if not (REPO_ROOT / norm).exists():
            errors.append(f"{item['id']}: file_path missing {norm}")

    for project in EXPECTED_PROJECTS:
        actual = counts.get(project, 0)
        if actual != TARGET:
            errors.append(f"{project}: {actual} items (expected {TARGET})")
    expected_total = len(EXPECTED_PROJECTS) * TARGET
    if len(items) != expected_total:
        errors.append(f"total {len(items)} (expected {expected_total})")

    report_path = BASE_DIR / "report-input.json"
    if report_path.exists():
        report = json.loads(report_path.read_text(encoding="utf-8"))
        table_rows = {t["title"].split(" — ")[0]: len(t["rows"]) for t in report.get("tables", [])}
        for project, count in counts.items():
            if table_rows.get(project) != count:
                errors.append(
                    f"report table for {project}: {table_rows.get(project)} rows (expected {count})"
                )
        blob = json.dumps(report, ensure_ascii=False)
        if "http://" in blob or "https://" in blob:
            errors.append("report-input.json contains remote URL")
    else:
        errors.append("report-input.json not found")

    if errors:
        print("FAIL")
        for line in errors[:50]:
            print(f"  - {line}")
        if len(errors) > 50:
            print(f"  ... and {len(errors) - 50} more")
        return 1
    print(f"OK — {len(items)} items, {len(counts)} projects, all invariants hold")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
