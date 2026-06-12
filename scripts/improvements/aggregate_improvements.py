#!/usr/bin/env python3
"""Aggregate raw improvement findings into exactly N items per project.

Reads docs/research/improvements-2026-06/raw/*.json, validates, dedupes,
selects up to TARGET_PER_PROJECT per project, renumbers IDs, and writes
improvements.json (+ gaps.json / rejects.json when applicable).

Idempotent: re-running after adding raw files (e.g. *-r2.json) is safe.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BASE_DIR = REPO_ROOT / "docs" / "research" / "improvements-2026-06"
RAW_DIR = BASE_DIR / "raw"

TARGET_PER_PROJECT = 100
JACCARD_THRESHOLD = 0.6

REQUIRED_FIELDS = (
    "project",
    "dimension",
    "severity",
    "title",
    "description",
    "file_path",
    "recommendation",
)
SEVERITY_ORDER = {"P1": 0, "P2": 1, "P3": 2}
EFFORT_ORDER = {"S": 0, "M": 1, "L": 2}

PROJECT_CODES = {
    "all": "ALL",
    "android-support": "ASUP",
    "Keelim-Knowledge-Vault": "KKV",
    "keelim-plugin": "KPLG",
    "keelim-vercel": "KVCL",
    "rich": "RICH",
    "youtube": "YTB",
    "all-web-ui": "AWUI",
}

_LINE_SUFFIX = re.compile(r"(:\d+)+$")
_TOKEN = re.compile(r"[A-Za-z0-9가-힣]+")


def normalize_path(raw_path: str) -> str:
    return _LINE_SUFFIX.sub("", raw_path.strip()).lstrip("/")


def title_tokens(title: str) -> frozenset[str]:
    return frozenset(t.lower() for t in _TOKEN.findall(title))


def path_exists(norm_path: str) -> bool:
    return (REPO_ROOT / norm_path).exists()


def validate_item(item: dict) -> str | None:
    """Return a rejection reason, or None if the item is valid."""
    for field in REQUIRED_FIELDS:
        value = item.get(field)
        if not isinstance(value, str) or not value.strip():
            return f"missing or empty field: {field}"
    if item["project"] not in PROJECT_CODES:
        return f"unknown project: {item['project']}"
    if item["severity"] not in SEVERITY_ORDER:
        return f"invalid severity: {item['severity']}"
    norm = normalize_path(item["file_path"])
    if not norm:
        return "empty file_path"
    if not path_exists(norm):
        return f"file_path does not exist: {norm}"
    if "http://" in json.dumps(item, ensure_ascii=False) or "https://" in json.dumps(
        item, ensure_ascii=False
    ):
        return "contains remote URL"
    return None


def load_raw_items() -> tuple[list[dict], list[dict]]:
    items: list[dict] = []
    rejects: list[dict] = []
    for raw_file in sorted(RAW_DIR.glob("*.json")):
        try:
            payload = json.loads(raw_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            rejects.append({"source": raw_file.name, "reason": f"unreadable: {exc}"})
            continue
        for entry in payload.get("items", []):
            reason = validate_item(entry) if isinstance(entry, dict) else "not an object"
            if reason:
                rejects.append(
                    {"source": raw_file.name, "reason": reason, "item": entry}
                )
            else:
                items.append({**entry, "_source": raw_file.name})
    return items, rejects


def jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def better(a: dict, b: dict) -> dict:
    """Pick the item to keep when two are duplicates (higher severity wins)."""
    if SEVERITY_ORDER[a["severity"]] <= SEVERITY_ORDER[b["severity"]]:
        return a
    return b


def dedupe(items: list[dict]) -> list[dict]:
    exact_seen: dict[tuple, dict] = {}
    for item in items:
        key = (
            item["project"],
            normalize_path(item["file_path"]),
            title_tokens(item["title"]),
        )
        exact_seen[key] = better(exact_seen[key], item) if key in exact_seen else item

    grouped: dict[tuple, list[dict]] = {}
    for item in exact_seen.values():
        group_key = (item["project"], normalize_path(item["file_path"]))
        grouped.setdefault(group_key, []).append(item)

    kept: list[dict] = []
    for group in grouped.values():
        survivors: list[dict] = []
        for candidate in group:
            cand_tokens = title_tokens(candidate["title"])
            merged = False
            for idx, existing in enumerate(survivors):
                if jaccard(cand_tokens, title_tokens(existing["title"])) >= JACCARD_THRESHOLD:
                    survivors[idx] = better(existing, candidate)
                    merged = True
                    break
            if not merged:
                survivors.append(candidate)
        kept.extend(survivors)
    return kept


def select_for_project(candidates: list[dict]) -> list[dict]:
    """Pick up to TARGET_PER_PROJECT: severity tier -> dimension round-robin -> effort."""
    selected: list[dict] = []
    for severity in ("P1", "P2", "P3"):
        tier = [c for c in candidates if c["severity"] == severity]
        buckets: dict[str, list[dict]] = {}
        for item in tier:
            buckets.setdefault(item["dimension"], []).append(item)
        for bucket in buckets.values():
            bucket.sort(key=lambda i: EFFORT_ORDER.get(i.get("effort", "M"), 1))
        dimension_names = sorted(buckets)
        while len(selected) < TARGET_PER_PROJECT and any(buckets.values()):
            for name in dimension_names:
                if buckets[name] and len(selected) < TARGET_PER_PROJECT:
                    selected.append(buckets[name].pop(0))
        if len(selected) >= TARGET_PER_PROJECT:
            break
    return selected


def renumber(project: str, items: list[dict]) -> list[dict]:
    code = PROJECT_CODES[project]
    ordered = sorted(
        items,
        key=lambda i: (SEVERITY_ORDER[i["severity"]], i["dimension"], i["title"]),
    )
    return [
        {
            "id": f"{code}-{idx:03d}",
            **{k: v for k, v in item.items() if k not in ("id", "_source")},
        }
        for idx, item in enumerate(ordered, start=1)
    ]


def main() -> int:
    if not RAW_DIR.is_dir():
        print(f"raw directory not found: {RAW_DIR}", file=sys.stderr)
        return 1

    items, rejects = load_raw_items()
    deduped = dedupe(items)

    final_items: list[dict] = []
    gaps: list[dict] = []
    project_stats: dict[str, dict] = {}
    for project in PROJECT_CODES:
        candidates = [i for i in deduped if i["project"] == project]
        selected = select_for_project(candidates)
        final_items.extend(renumber(project, selected))
        dims_count: dict[str, int] = {}
        for item in selected:
            dims_count[item["dimension"]] = dims_count.get(item["dimension"], 0) + 1
        project_stats[project] = {
            "selected": len(selected),
            "candidates": len(candidates),
            "dimensions": dims_count,
        }
        if len(selected) < TARGET_PER_PROJECT:
            weak = sorted(dims_count, key=lambda d: dims_count[d])
            gaps.append(
                {
                    "project": project,
                    "shortfall": TARGET_PER_PROJECT - len(selected),
                    "weak_dimensions": weak[:3],
                    "exclude_titles": [i["title"] for i in selected],
                }
            )

    result = {
        "generated": "2026-06-10",
        "target_per_project": TARGET_PER_PROJECT,
        "total": len(final_items),
        "projects": project_stats,
        "items": final_items,
    }
    (BASE_DIR / "improvements.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    gaps_path = BASE_DIR / "gaps.json"
    if gaps:
        gaps_path.write_text(
            json.dumps(gaps, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    elif gaps_path.exists():
        gaps_path.unlink()

    if rejects:
        (BASE_DIR / "rejects.json").write_text(
            json.dumps(rejects, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    print(f"raw items: {len(items)}, rejected: {len(rejects)}, deduped: {len(deduped)}")
    for project, stats in project_stats.items():
        print(f"  {project}: {stats['selected']}/{TARGET_PER_PROJECT} (candidates {stats['candidates']})")
    print(f"total selected: {len(final_items)}")
    if gaps:
        print(f"GAPS — see {gaps_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
