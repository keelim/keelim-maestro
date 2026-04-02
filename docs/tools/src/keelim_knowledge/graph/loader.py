from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from keelim_knowledge.models import EdgeEntry, KnowledgeEdge, KnowledgeNode, NodeEntry, WorkspaceGraph


def _load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _iter_relationship_records(raw: Any) -> list[dict[str, Any]]:
    if raw is None:
        return []
    if isinstance(raw, list):
        return [dict(item) for item in raw]
    if isinstance(raw, dict) and isinstance(raw.get("relationships"), list):
        return [dict(item) for item in raw["relationships"]]
    raise ValueError(f"Unsupported relationship payload shape: {type(raw)!r}")


def load_workspace(config_path: str | Path) -> WorkspaceGraph:
    config_path = Path(config_path).resolve()
    knowledge_root = config_path.parent
    config = _load_yaml(config_path) or {}

    node_entries: list[NodeEntry] = []
    edge_entries: list[EdgeEntry] = []

    nodes_root = knowledge_root / "nodes"
    if nodes_root.exists():
        for node_path in sorted(nodes_root.rglob("*.yaml")):
            raw = _load_yaml(node_path)
            if not raw:
                continue
            node_entries.append(
                NodeEntry(
                    node=KnowledgeNode.from_mapping(dict(raw)),
                    source_path=node_path,
                    origin="manual",
                )
            )

    relationships_root = knowledge_root / "relationships"
    if relationships_root.exists():
        for edge_path in sorted(relationships_root.rglob("*.yaml")):
            raw = _load_yaml(edge_path)
            for record in _iter_relationship_records(raw):
                edge_entries.append(
                    EdgeEntry(
                        edge=KnowledgeEdge.from_mapping(record),
                        source_path=edge_path,
                        origin="manual",
                    )
                )

    generated_root = knowledge_root / "generated"
    if generated_root.exists():
        for artifact_path in sorted(generated_root.rglob("*.json")):
            raw = json.loads(artifact_path.read_text(encoding="utf-8"))
            for node_record in raw.get("nodes", []):
                node_entries.append(
                    NodeEntry(
                        node=KnowledgeNode.from_mapping(dict(node_record)),
                        source_path=artifact_path,
                        origin="generated",
                    )
                )
            for edge_record in raw.get("edges", []):
                edge_entries.append(
                    EdgeEntry(
                        edge=KnowledgeEdge.from_mapping(dict(edge_record)),
                        source_path=artifact_path,
                        origin="generated",
                    )
                )

    return WorkspaceGraph(
        config_path=config_path,
        knowledge_root=knowledge_root,
        config=config,
        node_entries=node_entries,
        edge_entries=edge_entries,
    )
