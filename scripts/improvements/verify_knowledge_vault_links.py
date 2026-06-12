#!/usr/bin/env python3
"""Verify selected Knowledge Vault linking fixes for the improvement ledger."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
VAULT_ROOT = REPO_ROOT / "Keelim-Knowledge-Vault"

MODIFIED_FILES = [
    "Index.md",
    "AI/index.md",
    "Android/index.md",
    "omx_wiki/index.md",
    "omx_wiki/anthropic-founder-playbook-ai-native-startup.md",
    "omx_wiki/google-io-2026-android-platform-update-memo.md",
    "omx_wiki/포켓몬-온톨로지-학습-프로그램-리서치.md",
    "AI/keelim-ai/concepts/AI 네이티브 스타트업 운영 패턴.md",
    "AI/keelim-ai/sources/포켓몬 온톨로지 학습 프로그램 리서치.md",
    "log.md",
]

SELECTED_LINK_CHECKS = {
    "KKV-063": (
        "AI/index.md",
        "[[omx_wiki/anthropic-founder-playbook-ai-native-startup]]",
        "omx_wiki/anthropic-founder-playbook-ai-native-startup.md",
        "[[AI/keelim-ai/concepts/AI 네이티브 스타트업 운영 패턴]]",
    ),
    "KKV-064": (
        "Android/index.md",
        "[[omx_wiki/google-io-2026-android-platform-update-memo]]",
        "omx_wiki/google-io-2026-android-platform-update-memo.md",
        "[[Android/index]]",
    ),
    "KKV-065": ("Index.md", "[[log|Vault log]]", "log.md", "[[Index]]"),
    "KKV-066": (
        "Index.md",
        "[[omx_wiki/index|omx_wiki index]]",
        "omx_wiki/index.md",
        "[[Index]]",
    ),
    "KKV-067": ("AI/index.md", "[[workflow]]", "workflow.md", "[[AI/index]]"),
    "KKV-068": (
        "AI/index.md",
        "[[omx_wiki/포켓몬-온톨로지-학습-프로그램-리서치]]",
        "omx_wiki/포켓몬-온톨로지-학습-프로그램-리서치.md",
        "[[AI/keelim-ai/sources/포켓몬 온톨로지 학습 프로그램 리서치]]",
    ),
}


def read_vault_file(relative_path: str) -> str:
    return (VAULT_ROOT / relative_path).read_text(encoding="utf-8")


def wikilink_target(link: str) -> str:
    return link.split("|", 1)[0].split("#", 1)[0].strip()


def target_exists(target: str, all_markdown_files: list[Path]) -> bool:
    if not target:
        return True
    exact_path = VAULT_ROOT / f"{target}.md"
    if exact_path.exists():
        return True
    basename = f"{Path(target).name}.md"
    return any(path.name == basename for path in all_markdown_files)


def main() -> int:
    all_markdown_files = list(VAULT_ROOT.rglob("*.md"))
    unresolved: list[tuple[str, str]] = []

    for relative_path in MODIFIED_FILES:
        text = read_vault_file(relative_path)
        for raw_link in re.findall(r"\[\[([^\]]+)\]\]", text):
            target = wikilink_target(raw_link)
            if not target_exists(target, all_markdown_files):
                unresolved.append((relative_path, raw_link))

    if unresolved:
        print("UNRESOLVED wikilinks:")
        for relative_path, raw_link in unresolved:
            print(f"- {relative_path}: [[{raw_link}]]")
        return 1

    for item_id, (inbound_file, inbound_link, outbound_file, outbound_link) in SELECTED_LINK_CHECKS.items():
        inbound_text = read_vault_file(inbound_file)
        outbound_text = read_vault_file(outbound_file)
        if inbound_link not in inbound_text:
            print(f"{item_id}: missing inbound {inbound_link} in {inbound_file}")
            return 1
        if outbound_link not in outbound_text:
            print(f"{item_id}: missing outbound {outbound_link} in {outbound_file}")
            return 1

    print("OK: Knowledge Vault selected linking checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
