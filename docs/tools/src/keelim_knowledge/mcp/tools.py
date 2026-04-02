from __future__ import annotations

from collections import deque
import json
import os
from pathlib import Path

from keelim_knowledge.graph.loader import load_workspace
from keelim_knowledge.graph.neo4j_client import Neo4jClient
from keelim_knowledge.graph.validator import validate_workspace


def _graph_maps(config_path: str | Path):
    graph = load_workspace(config_path)
    nodes = {entry.node.id: entry.node for entry in graph.node_entries}
    outgoing: dict[str, list] = {}
    incoming: dict[str, list] = {}
    for entry in graph.edge_entries:
        outgoing.setdefault(entry.edge.source, []).append(entry.edge)
        incoming.setdefault(entry.edge.target, []).append(entry.edge)
    return graph, nodes, outgoing, incoming


def _runtime_client() -> Neo4jClient | None:
    try:
        return Neo4jClient.from_env(
            uri=os.environ.get("NEO4J_URI", "bolt://localhost:7687"),
            user=os.environ.get("NEO4J_USER", "neo4j"),
            password=os.environ.get("NEO4J_PASSWORD", "neo4j"),
        )
    except Exception:
        return None


def _node_mapping(row: dict) -> dict:
    metadata = row.get("metadata_json")
    return {
        "id": row["id"],
        "node_type": row["node_type"],
        "name": row["name"],
        "path": row.get("path", ""),
        "metadata": json.loads(metadata or "{}"),
    }


def _find_nodes_by_label(label: str, pattern: str) -> list[dict]:
    client = _runtime_client()
    if client is None:
        return []
    with client:
        rows = client.run_query(
            f"""
            MATCH (n:{label})
            WHERE toLower(n.name) CONTAINS toLower('{pattern.replace("'", "\\'")}')
               OR toLower(n.id) CONTAINS toLower('{pattern.replace("'", "\\'")}')
            RETURN n.id AS id,
                   labels(n)[0] AS node_type,
                   n.name AS name,
                   n.path AS path,
                   n.metadata_json AS metadata_json
            ORDER BY n.name ASC
            """
        )
    return [_node_mapping(row) for row in rows]


def list_subprojects(config_path: str | Path) -> list[dict]:
    client = _runtime_client()
    if client is not None:
        with client:
            rows = client.run_query(
                """
                MATCH (n:Subproject)
                RETURN n.id AS id,
                       labels(n)[0] AS node_type,
                       n.name AS name,
                       n.path AS path,
                       n.metadata_json AS metadata_json
                ORDER BY n.name ASC
                """
            )
        return [_node_mapping(row) for row in rows]
    graph, _, _, _ = _graph_maps(config_path)
    return [
        entry.node.to_mapping()
        for entry in graph.node_entries
        if entry.node.node_type == "Subproject"
    ]


def find_entity(config_path: str | Path, name: str) -> list[dict]:
    runtime_matches = _find_nodes_by_label("DomainEntity", name)
    if runtime_matches:
        return runtime_matches
    graph, _, _, _ = _graph_maps(config_path)
    lowered = name.lower()
    return [
        entry.node.to_mapping()
        for entry in graph.node_entries
        if entry.node.node_type == "DomainEntity" and lowered in entry.node.name.lower()
    ]


def find_endpoint(config_path: str | Path, pattern: str) -> list[dict]:
    runtime_matches = _find_nodes_by_label("APIEndpoint", pattern)
    if runtime_matches:
        return runtime_matches
    graph, _, _, _ = _graph_maps(config_path)
    lowered = pattern.lower()
    return [
        entry.node.to_mapping()
        for entry in graph.node_entries
        if entry.node.node_type == "APIEndpoint" and lowered in entry.node.name.lower()
    ]


def get_neighbors(config_path: str | Path, node_id: str) -> list[dict]:
    client = _runtime_client()
    if client is not None:
        with client:
            rows = client.run_query(
                f"""
                MATCH (src {{id: '{node_id}'}})-[rel]->(dst)
                RETURN 'outgoing' AS direction,
                       rel.id AS edge_id,
                       type(rel) AS relation_type,
                       src.id AS source,
                       dst.id AS target,
                       dst.id AS id,
                       labels(dst)[0] AS node_type,
                       dst.name AS name,
                       dst.path AS path,
                       dst.metadata_json AS metadata_json
                UNION
                MATCH (src)-[rel]->(dst {{id: '{node_id}'}})
                RETURN 'incoming' AS direction,
                       rel.id AS edge_id,
                       type(rel) AS relation_type,
                       src.id AS source,
                       dst.id AS target,
                       src.id AS id,
                       labels(src)[0] AS node_type,
                       src.name AS name,
                       src.path AS path,
                       src.metadata_json AS metadata_json
                """
            )
        return [
            {
                "direction": row["direction"],
                "edge": {
                    "id": row["edge_id"],
                    "relation_type": row["relation_type"],
                    "from": row["source"],
                    "to": row["target"],
                },
                "node": _node_mapping(row),
            }
            for row in rows
        ]
    _, nodes, outgoing, incoming = _graph_maps(config_path)
    neighbors = []
    for edge in outgoing.get(node_id, []):
        neighbors.append(
            {
                "direction": "outgoing",
                "edge": edge.to_mapping(),
                "node": nodes[edge.target].to_mapping(),
            }
        )
    for edge in incoming.get(node_id, []):
        neighbors.append(
            {
                "direction": "incoming",
                "edge": edge.to_mapping(),
                "node": nodes[edge.source].to_mapping(),
            }
        )
    return neighbors


def find_path(config_path: str | Path, source_id: str, target_id: str, max_hops: int = 5) -> list[str]:
    client = _runtime_client()
    if client is not None:
        capped = max(1, min(int(max_hops), 8))
        with client:
            rows = client.run_query(
                f"""
                MATCH (src {{id: '{source_id}'}}), (dst {{id: '{target_id}'}})
                MATCH path = shortestPath((src)-[*..{capped}]->(dst))
                RETURN [node IN nodes(path) | node.id] AS path_ids
                """
            )
        if rows:
            return rows[0].get("path_ids", [])
    _, _, outgoing, _ = _graph_maps(config_path)
    queue = deque([(source_id, [source_id])])
    seen = {source_id}
    while queue:
        node_id, path = queue.popleft()
        if node_id == target_id:
            return path
        if len(path) > max_hops:
            continue
        for edge in outgoing.get(node_id, []):
            if edge.target in seen:
                continue
            seen.add(edge.target)
            queue.append((edge.target, [*path, edge.target]))
    return []


def trace_data_flow(config_path: str | Path, entity_name: str) -> dict:
    client = _runtime_client()
    if client is not None:
        with client:
            payload = client.analyze_entity_impact(entity_name)
        if payload.get("entity") is None:
            return {"entity": None, "neighbors": []}
        return {
            "entity": payload["entity"],
            "neighbors": payload["direct_impacts"],
            "api_chains": payload["api_chains"],
            "storage": payload["storage"],
        }
    matches = find_entity(config_path, entity_name)
    if not matches:
        return {"entity": None, "neighbors": []}
    entity = matches[0]
    neighbors = get_neighbors(config_path, entity["id"])
    return {"entity": entity, "neighbors": neighbors}


def check_graph_health(config_path: str | Path) -> dict:
    result = validate_workspace(config_path)
    return {"is_valid": result.is_valid, "issues": result.issues, "warnings": result.warnings}


def analyze_entity_impact(config_path: str | Path, entity_name: str, max_hops: int = 3) -> dict:
    client = Neo4jClient.from_env(
        uri=os.environ.get("NEO4J_URI", "bolt://localhost:7687"),
        user=os.environ.get("NEO4J_USER", "neo4j"),
        password=os.environ.get("NEO4J_PASSWORD", "neo4j"),
    )
    with client:
        return client.analyze_entity_impact(entity_name, max_hops=max_hops)


def find_service(config_path: str | Path, name: str) -> list[dict]:
    runtime_matches = _find_nodes_by_label("Service", name)
    if runtime_matches:
        return runtime_matches
    graph, _, _, _ = _graph_maps(config_path)
    lowered = name.lower()
    return [
        entry.node.to_mapping()
        for entry in graph.node_entries
        if entry.node.node_type == "Service" and lowered in entry.node.name.lower()
    ]


def find_bounded_context(config_path: str | Path, name: str) -> list[dict]:
    runtime_matches = _find_nodes_by_label("BoundedContext", name)
    if runtime_matches:
        return runtime_matches
    graph, _, _, _ = _graph_maps(config_path)
    lowered = name.lower()
    return [
        entry.node.to_mapping()
        for entry in graph.node_entries
        if entry.node.node_type == "BoundedContext" and lowered in entry.node.name.lower()
    ]


def find_workflow(config_path: str | Path, name: str) -> list[dict]:
    runtime_matches = _find_nodes_by_label("DomainWorkflow", name)
    if runtime_matches:
        return runtime_matches
    graph, _, _, _ = _graph_maps(config_path)
    lowered = name.lower()
    return [
        entry.node.to_mapping()
        for entry in graph.node_entries
        if entry.node.node_type == "DomainWorkflow" and lowered in entry.node.name.lower()
    ]
