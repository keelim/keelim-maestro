#!/usr/bin/env python3
"""Verify selected Knowledge Vault automation fixes for the improvement ledger."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
VAULT_ROOT = REPO_ROOT / "Keelim-Knowledge-Vault"


def run(command: list[str], expect_code: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=VAULT_ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode != expect_code:
        raise AssertionError(
            f"{' '.join(command)} exited {result.returncode}, expected {expect_code}\n{result.stdout}"
        )
    return result


def read(path: str) -> str:
    return (VAULT_ROOT / path).read_text(encoding="utf-8")


def main() -> int:
    link_json = json.loads(run(["bash", "scripts/check-backlinks.sh", "--json"]).stdout)
    if not link_json.get("ok") or link_json.get("failures"):
        raise AssertionError("vault-wide backlink JSON check reported failures")
    run(["bash", "scripts/check-backlinks.sh", "--file", "Index.md"])

    resurface_json = json.loads(
        run(["bash", "scripts/resurface.sh", "--check", "--json", "--max-stale", "9999"]).stdout
    )
    if "staleHighValue" not in resurface_json or not isinstance(resurface_json["candidates"], list):
        raise AssertionError("resurface JSON output does not contain expected fields")
    run(["bash", "scripts/resurface.sh", "--check", "--max-stale", "0"], expect_code=1)

    schema = read("schema/LLM Wiki 운영 스키마.md")
    for needle in [
        "bash scripts/check-backlinks.sh",
        "bash scripts/resurface.sh --check --max-stale N",
        "## Required frontmatter",
        "`type`",
    ]:
        if needle not in schema:
            raise AssertionError(f"schema missing {needle}")

    template = read("schema/LLM Wiki 노트 템플릿.md")
    for needle in ["type: domain-index", "type: source-summary", "type: lint-pass", "broken_links: {count}"]:
        if needle not in template:
            raise AssertionError(f"template missing {needle}")

    core_plugins = json.loads(read(".obsidian/core-plugins.json"))
    if core_plugins.get("properties") is not True:
        raise AssertionError("Obsidian properties plugin is not enabled")
    templates = json.loads(read(".obsidian/templates.json"))
    if templates.get("folder") != "schema":
        raise AssertionError("Obsidian templates folder is not schema")

    workspace = json.loads(read(".obsidian/workspace.json"))
    workspace_text = json.dumps(workspace, ensure_ascii=False)
    if "copilot-chat-view" in workspace_text or "copilot:Open Copilot Chat" in workspace_text:
        raise AssertionError("workspace still contains inactive Copilot state")
    missing_recent = [entry for entry in workspace.get("lastOpenFiles", []) if not (VAULT_ROOT / entry).exists()]
    if missing_recent:
        raise AssertionError(f"workspace has missing lastOpenFiles entries: {missing_recent[:5]}")

    print("OK: Knowledge Vault automation checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
