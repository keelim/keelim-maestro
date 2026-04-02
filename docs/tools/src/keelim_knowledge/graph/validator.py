from __future__ import annotations

from pathlib import Path

import yaml

from keelim_knowledge.graph.loader import load_workspace
from keelim_knowledge.models import ValidationResult


def _schema_sets(config_path: Path) -> tuple[set[str], set[str]]:
    schema_path = config_path.parent / "schema.yaml"
    if not schema_path.exists():
        return set(), set()
    raw = yaml.safe_load(schema_path.read_text(encoding="utf-8")) or {}
    return set(raw.get("node_types", [])), set(raw.get("relation_types", []))


def validate_workspace(config_path: str | Path) -> ValidationResult:
    config_path = Path(config_path).resolve()
    graph = load_workspace(config_path)
    result = ValidationResult()
    allowed_node_types, allowed_relation_types = _schema_sets(config_path)

    seen_nodes: dict[str, str] = {}
    for entry in graph.node_entries:
        existing = seen_nodes.get(entry.node.id)
        if existing is not None:
            result.issues.append(f"duplicate node id: {entry.node.id}")
        else:
            seen_nodes[entry.node.id] = str(entry.source_path)
        if allowed_node_types and entry.node.node_type not in allowed_node_types:
            result.issues.append(f"unsupported node type: {entry.node.node_type}")
        if entry.node.node_type == "TableColumn":
            if "table" not in entry.node.metadata:
                result.issues.append(f"missing table metadata for column node: {entry.node.id}")
            if "column_name" not in entry.node.metadata:
                result.issues.append(f"missing column_name metadata for column node: {entry.node.id}")

    available_nodes = set(seen_nodes)
    seen_edges: set[str] = set()
    for entry in graph.edge_entries:
        if entry.edge.id in seen_edges:
            result.issues.append(f"duplicate edge id: {entry.edge.id}")
        else:
            seen_edges.add(entry.edge.id)
        if allowed_relation_types and entry.edge.relation_type not in allowed_relation_types:
            result.issues.append(f"unsupported relation type: {entry.edge.relation_type}")
        if entry.edge.source not in available_nodes:
            result.issues.append(f"missing source node: {entry.edge.source}")
        if entry.edge.target not in available_nodes:
            result.issues.append(f"missing target node: {entry.edge.target}")

    return result
