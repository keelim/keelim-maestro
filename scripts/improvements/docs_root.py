"""Resolve the operator's local documentation archive, never a checkout path."""

import os
import sys
from pathlib import Path


def archive_root(repo_root: Path) -> Path:
    configured = os.environ.get("KEELIM_DOCS_DIR")
    path = Path(configured).expanduser() if configured else Path.home() / "Desktop" / "docs"
    root = path.resolve()
    repo_root = repo_root.resolve()
    if root == repo_root or repo_root in root.parents or root in repo_root.parents:
        raise SystemExit("KEELIM_DOCS_DIR must be a separate directory outside the workspace.")
    return root


def archive_path(root: Path, *parts: str) -> Path:
    path = root.joinpath(*parts)
    if root not in path.resolve().parents:
        raise SystemExit("Documentation archive path escapes its root.")
    return path


def missing_archive_input(path: Path) -> int:
    explicit = bool(os.environ.get("KEELIM_DOCS_DIR"))
    kind = "ERROR" if explicit else "SKIP"
    print(f"{kind}: archived input not found: {path}", file=sys.stderr)
    return 1 if explicit else 0
