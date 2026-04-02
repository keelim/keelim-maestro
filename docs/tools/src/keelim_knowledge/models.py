from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


def _extra_metadata(
    raw: dict[str, Any],
    reserved: set[str],
) -> dict[str, Any]:
    return {key: value for key, value in raw.items() if key not in reserved}


@dataclass(slots=True)
class KnowledgeNode:
    id: str
    node_type: str
    name: str
    path: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, raw: dict[str, Any]) -> "KnowledgeNode":
        reserved = {"id", "node_type", "type", "name", "path", "metadata"}
        metadata = dict(raw.get("metadata", {}))
        metadata.update(_extra_metadata(raw, reserved))
        return cls(
            id=str(raw["id"]),
            node_type=str(raw.get("node_type") or raw.get("type")),
            name=str(raw["name"]),
            path=str(raw.get("path", "")),
            metadata=metadata,
        )

    def to_mapping(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "id": self.id,
            "node_type": self.node_type,
            "name": self.name,
        }
        if self.path:
            payload["path"] = self.path
        if self.metadata:
            payload["metadata"] = self.metadata
        return payload


@dataclass(slots=True)
class KnowledgeEdge:
    id: str
    relation_type: str
    source: str
    target: str
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, raw: dict[str, Any]) -> "KnowledgeEdge":
        reserved = {
            "id",
            "relation_type",
            "type",
            "source",
            "from",
            "target",
            "to",
            "metadata",
        }
        metadata = dict(raw.get("metadata", {}))
        metadata.update(_extra_metadata(raw, reserved))
        source = raw.get("source", raw.get("from"))
        target = raw.get("target", raw.get("to"))
        if source is None or target is None:
            raise ValueError("KnowledgeEdge mapping requires source/from and target/to")
        relation_type = str(raw.get("relation_type") or raw.get("type"))
        edge_id = str(raw.get("id") or f"edge:{source}:{relation_type}:{target}")
        return cls(
            id=edge_id,
            relation_type=relation_type,
            source=str(source),
            target=str(target),
            metadata=metadata,
        )

    def to_mapping(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "id": self.id,
            "relation_type": self.relation_type,
            "from": self.source,
            "to": self.target,
        }
        if self.metadata:
            payload["metadata"] = self.metadata
        return payload


@dataclass(slots=True)
class AnalysisArtifact:
    subproject: str
    nodes: list[KnowledgeNode] = field(default_factory=list)
    edges: list[KnowledgeEdge] = field(default_factory=list)

    def to_mapping(self) -> dict[str, Any]:
        return {
            "subproject": self.subproject,
            "nodes": [node.to_mapping() for node in self.nodes],
            "edges": [edge.to_mapping() for edge in self.edges],
        }


@dataclass(slots=True)
class NodeEntry:
    node: KnowledgeNode
    source_path: Path
    origin: str


@dataclass(slots=True)
class EdgeEntry:
    edge: KnowledgeEdge
    source_path: Path
    origin: str


@dataclass(slots=True)
class WorkspaceGraph:
    config_path: Path
    knowledge_root: Path
    config: dict[str, Any]
    node_entries: list[NodeEntry]
    edge_entries: list[EdgeEntry]


@dataclass(slots=True)
class ValidationResult:
    issues: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.issues
