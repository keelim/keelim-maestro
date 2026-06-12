#!/usr/bin/env python3
"""Verify selected Knowledge Vault frontmatter fixes for the improvement ledger."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
VAULT_ROOT = REPO_ROOT / "Keelim-Knowledge-Vault"

REQUIRED_FIELDS = {
    "Index.md": ["title", "type", "scope", "updated", "tags"],
    "AI/index.md": ["title", "type", "domain", "updated", "tags", "aliases"],
    "Android/index.md": ["title", "type", "domain", "updated", "tags", "aliases"],
    "AI/keelim-ai/index.md": ["title", "type", "domain", "updated", "tags", "aliases"],
    "Android/sources/Android 17 앱 호환성 체크리스트 메모.md": [
        "title",
        "type",
        "source_type",
        "domain",
        "confidence",
        "checked",
        "tags",
    ],
    "Android/Version/Android 17.md": [
        "title",
        "type",
        "platform",
        "version",
        "api_level",
        "tags",
    ],
    "AI/keelim-ai/sources/Anthropic Founder Playbook 요약.md": [
        "title",
        "type",
        "domain",
        "publisher",
        "published",
        "checked",
        "tags",
    ],
    "Books/Books.md": ["title", "type", "domain", "updated", "tags", "aliases"],
    "Code/Code.md": ["title", "type", "domain", "updated", "tags"],
    "Language/Kotlin/Compose/Jetpack Compose 2026년 4월 릴리스.md": [
        "title",
        "type",
        "published",
        "checked",
        "tags",
    ],
    "Computer Science/index.md": ["title", "type", "domain", "updated", "tags", "aliases"],
    "KMP/25.12.21/1.md": ["title", "type", "domain", "session_date", "tags", "aliases"],
    "AI/keelim-ai/concepts/LLM Wiki 아키텍처.md": ["title", "type", "domain", "updated", "tags"],
    "omx_wiki/android-17-app-compatibility-readiness.md": [
        "title",
        "tags",
        "created",
        "updated",
        "created_at",
        "updated_at",
        "schemaVersion",
    ],
    "omx_wiki/index.md": ["title", "type", "domain", "page_count", "updated", "schemaVersion", "tags"],
    "omx_wiki/log.md": ["title", "type", "domain", "date_format", "updated", "tags"],
    "service/index.md": ["title", "type", "domain", "updated", "tags"],
}


def parse_frontmatter(relative_path: str) -> dict[str, str]:
    text = (VAULT_ROOT / relative_path).read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"{relative_path}: missing opening frontmatter marker")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError(f"{relative_path}: missing closing frontmatter marker") from exc
    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.startswith(" "):
            continue
        key, separator, value = line.partition(":")
        if separator:
            fields[key.strip()] = value.strip()
    return fields


def main() -> int:
    failures: list[str] = []
    for relative_path, required_fields in REQUIRED_FIELDS.items():
        try:
            fields = parse_frontmatter(relative_path)
        except ValueError as exc:
            failures.append(str(exc))
            continue
        for field in required_fields:
            if field not in fields or not fields[field]:
                failures.append(f"{relative_path}: missing {field}")

    android17 = parse_frontmatter("omx_wiki/android-17-app-compatibility-readiness.md")
    if "T" in android17.get("created", "") or "T" in android17.get("updated", ""):
        failures.append("omx_wiki/android-17-app-compatibility-readiness.md: created/updated still use timestamps")

    if failures:
        print("Frontmatter verification failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"OK: {len(REQUIRED_FIELDS)} Knowledge Vault frontmatter targets verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
