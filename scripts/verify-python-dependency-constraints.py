#!/usr/bin/env python3
"""Verify shared Python dependency constraints across uv workspace members."""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - only for older system Python.
    print(
        "This script requires Python 3.11+. Run it with: "
        "uv run python scripts/verify-python-dependency-constraints.py",
        file=sys.stderr,
    )
    raise SystemExit(2)


ROOT = Path(__file__).resolve().parents[1]
ROOT_PYPROJECT = ROOT / "pyproject.toml"
NAME_RE = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)(?:\[[^\]]+\])?\s*(.*)$")


@dataclass(frozen=True)
class DependencyDeclaration:
    package: str
    specifier: str
    member: str
    location: str
    raw: str
    path: Path


def load_toml(path: Path) -> dict:
    with path.open("rb") as file:
        return tomllib.load(file)


def canonical_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def normalize_specifier(specifier: str) -> str:
    return re.sub(r"\s+", "", specifier.strip()) or "*"


def parse_requirement(raw: str) -> tuple[str, str]:
    requirement = raw.split(";", 1)[0].strip()

    if " @ " in requirement:
        name, source = requirement.split(" @ ", 1)
        return canonical_name(name.split("[", 1)[0].strip()), f"@ {source.strip()}"

    match = NAME_RE.match(requirement)
    if not match:
        raise ValueError(f"Unsupported dependency declaration: {raw!r}")

    name, specifier = match.groups()
    return canonical_name(name), normalize_specifier(specifier)


def iter_requirement_strings(data: dict) -> list[tuple[str, str]]:
    items: list[tuple[str, str]] = []

    project = data.get("project", {})
    for raw in project.get("dependencies", []):
        if isinstance(raw, str):
            items.append(("project.dependencies", raw))

    for extra, dependencies in project.get("optional-dependencies", {}).items():
        for raw in dependencies:
            if isinstance(raw, str):
                items.append((f"project.optional-dependencies.{extra}", raw))

    for group, dependencies in data.get("dependency-groups", {}).items():
        for raw in dependencies:
            if isinstance(raw, str):
                items.append((f"dependency-groups.{group}", raw))

    tool_uv = data.get("tool", {}).get("uv", {})
    for raw in tool_uv.get("dev-dependencies", []):
        if isinstance(raw, str):
            items.append(("tool.uv.dev-dependencies", raw))

    for raw in data.get("build-system", {}).get("requires", []):
        if isinstance(raw, str):
            items.append(("build-system.requires", raw))

    return items


def expand_workspace_members(root_data: dict) -> list[Path]:
    members = root_data.get("tool", {}).get("uv", {}).get("workspace", {}).get("members", [])
    paths: list[Path] = []

    for member in members:
        if not isinstance(member, str):
            continue

        matches = sorted(ROOT.glob(member)) if any(char in member for char in "*?[") else [ROOT / member]
        for path in matches:
            pyproject = path / "pyproject.toml"
            if pyproject.is_file():
                paths.append(path)

    return paths


def collect_member_declarations(member_path: Path) -> list[DependencyDeclaration]:
    pyproject = member_path / "pyproject.toml"
    data = load_toml(pyproject)
    declarations: list[DependencyDeclaration] = []

    for location, raw in iter_requirement_strings(data):
        package, specifier = parse_requirement(raw)
        declarations.append(
            DependencyDeclaration(
                package=package,
                specifier=specifier,
                member=member_path.name,
                location=location,
                raw=raw,
                path=pyproject,
            )
        )

    return declarations


def root_constraints(root_data: dict) -> dict[str, str]:
    constraints: dict[str, str] = {}
    for raw in root_data.get("tool", {}).get("uv", {}).get("constraint-dependencies", []):
        if not isinstance(raw, str):
            continue
        package, specifier = parse_requirement(raw)
        constraints[package] = specifier
    return constraints


def describe(declaration: DependencyDeclaration) -> str:
    path = declaration.path.relative_to(ROOT)
    return f"{declaration.member}: {path} [{declaration.location}] {declaration.raw!r}"


def main() -> int:
    root_data = load_toml(ROOT_PYPROJECT)
    constraints = root_constraints(root_data)
    member_paths = expand_workspace_members(root_data)

    declarations_by_package: dict[str, list[DependencyDeclaration]] = defaultdict(list)
    for member_path in member_paths:
        for declaration in collect_member_declarations(member_path):
            declarations_by_package[declaration.package].append(declaration)

    failures: list[str] = []
    shared_packages: list[str] = []

    for package, declarations in sorted(declarations_by_package.items()):
        members = {declaration.member for declaration in declarations}
        if len(members) < 2:
            continue

        shared_packages.append(package)
        expected = constraints.get(package)
        if expected is None:
            failures.append(
                f"{package}: shared by {', '.join(sorted(members))}, "
                "but missing from root tool.uv.constraint-dependencies."
            )
            continue

        for declaration in declarations:
            if declaration.specifier != expected:
                failures.append(
                    f"{package}: expected {expected!r} from root constraint, "
                    f"found {declaration.specifier!r} in {describe(declaration)}"
                )

    for package, expected in sorted(constraints.items()):
        for declaration in declarations_by_package.get(package, []):
            if declaration.specifier != expected:
                failures.append(
                    f"{package}: root constraint {expected!r} does not match "
                    f"{describe(declaration)}"
                )

    if failures:
        print("Python dependency constraint drift detected:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print("OK: Python dependency constraints are aligned.")
    print("Workspace members:", ", ".join(path.name for path in member_paths))
    print("Shared direct packages:", ", ".join(shared_packages) if shared_packages else "(none)")
    print(
        "Root constraints:",
        ", ".join(f"{package}{specifier}" for package, specifier in sorted(constraints.items()))
        if constraints
        else "(none)",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
