from __future__ import annotations

import os
from pathlib import Path

from keelim_knowledge.graph.loader import load_workspace
from keelim_knowledge.graph.neo4j_client import Neo4jClient
from keelim_knowledge.graph.validator import validate_workspace


def populate_workspace(config_path: str | Path) -> dict[str, int | str]:
    config_path = Path(config_path).resolve()
    result = validate_workspace(config_path)
    if not result.is_valid:
        raise ValueError("Validation failed; fix workspace issues before populate.")

    graph = load_workspace(config_path)
    client = Neo4jClient.from_env(
        uri=os.environ.get("NEO4J_URI", "bolt://localhost:7687"),
        user=os.environ.get("NEO4J_USER", "neo4j"),
        password=os.environ.get("NEO4J_PASSWORD", "neo4j"),
    )
    with client:
        client.ensure_indexes({entry.node.node_type for entry in graph.node_entries})
        for entry in graph.node_entries:
            client.upsert_node(entry.node.node_type, entry.node.to_mapping())
        for entry in graph.edge_entries:
            client.upsert_edge(
                entry.edge.relation_type,
                entry.edge.source,
                entry.edge.target,
                entry.edge.to_mapping(),
            )

    return {
        "nodes": len(graph.node_entries),
        "edges": len(graph.edge_entries),
        "knowledge_root": str(graph.knowledge_root),
    }
