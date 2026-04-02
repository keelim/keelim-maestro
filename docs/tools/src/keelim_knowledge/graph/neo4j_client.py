from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


@dataclass
class Neo4jClient:
    uri: str
    user: str
    password: str
    _driver: Any = None

    @classmethod
    def from_env(cls, uri: str, user: str, password: str) -> "Neo4jClient":
        try:
            from neo4j import GraphDatabase
        except ImportError as exc:  # pragma: no cover - optional runtime dependency
            raise RuntimeError(
                "neo4j package is not installed. Install it before using populate/query."
            ) from exc
        client = cls(uri=uri, user=user, password=password)
        client._driver = GraphDatabase.driver(uri, auth=(user, password))
        return client

    def __enter__(self) -> "Neo4jClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def close(self) -> None:
        if self._driver is not None:
            self._driver.close()

    def ensure_indexes(self, labels: set[str]) -> None:
        if self._driver is None:
            return
        with self._driver.session() as session:
            for label in sorted(labels):
                session.run(
                    f"CREATE INDEX IF NOT EXISTS FOR (n:{label}) ON (n.id)"
                ).consume()

    def upsert_node(self, label: str, payload: dict[str, Any]) -> None:
        if self._driver is None:
            return
        params = {
            "id": payload["id"],
            "name": payload["name"],
            "path": payload.get("path", ""),
            "metadata_json": json.dumps(payload.get("metadata", {}), ensure_ascii=False),
        }
        with self._driver.session() as session:
            session.run(
                f"""
                MERGE (n:{label} {{id: $id}})
                SET n.name = $name,
                    n.path = $path,
                    n.metadata_json = $metadata_json
                """,
                params,
            ).consume()

    def upsert_edge(self, relation_type: str, source: str, target: str, payload: dict[str, Any]) -> None:
        if self._driver is None:
            return
        with self._driver.session() as session:
            session.run(
                f"""
                MATCH (src {{id: $source}})
                MATCH (dst {{id: $target}})
                MERGE (src)-[r:{relation_type} {{id: $id}}]->(dst)
                SET r.metadata_json = $metadata_json
                """,
                {
                    "source": source,
                    "target": target,
                    "id": payload["id"],
                    "metadata_json": json.dumps(payload.get("metadata", {}), ensure_ascii=False),
                },
            ).consume()

    def run_query(self, query: str) -> list[dict[str, Any]]:
        if self._driver is None:
            return []
        with self._driver.session() as session:
            result = session.run(query)
            return [dict(record) for record in result]

    def analyze_entity_impact(self, entity_name: str, max_hops: int = 3) -> dict[str, Any]:
        if self._driver is None:
            return {"entity": None, "direct_impacts": [], "api_chains": [], "storage": []}
        max_hops = max(1, min(int(max_hops), 6))
        with self._driver.session() as session:
            entity_row = session.run(
                """
                MATCH (entity:DomainEntity)
                WHERE toLower(entity.name) = toLower($value) OR toLower(entity.id) = toLower($value)
                RETURN entity.id AS id,
                       entity.name AS name,
                       entity.path AS path,
                       entity.metadata_json AS metadata_json
                LIMIT 1
                """,
                {"value": entity_name},
            ).single()
            if entity_row is None:
                return {"entity": None, "direct_impacts": [], "api_chains": [], "storage": []}

            entity = {
                "id": entity_row["id"],
                "name": entity_row["name"],
                "path": entity_row["path"],
                "metadata": json.loads(entity_row["metadata_json"] or "{}"),
            }
            storage_rows = session.run(
                """
                MATCH (:DomainEntity {id: $entity_id})-[:STORED_IN]->(table:DatabaseTable)
                OPTIONAL MATCH (column:TableColumn)-[:STORED_IN]->(table)
                RETURN table.id AS table_id,
                       table.name AS table_name,
                       collect(DISTINCT column.name) AS columns
                """,
                {"entity_id": entity["id"]},
            )
            direct_rows = session.run(
                """
                MATCH (source)-[rel]->(:DomainEntity {id: $entity_id})
                WHERE type(rel) IN ['READS', 'WRITES', 'DELETES', 'IMPLEMENTS', 'ACCESSES']
                RETURN source.id AS id,
                       source.name AS name,
                       labels(source)[0] AS node_type,
                       type(rel) AS relation_type
                UNION
                MATCH (:DomainEntity {id: $entity_id})-[rel]->(target)
                WHERE type(rel) IN ['STORED_IN', 'GOVERNED_BY', 'BELONGS_TO', 'TRIGGERS']
                RETURN target.id AS id,
                       target.name AS name,
                       labels(target)[0] AS node_type,
                       type(rel) AS relation_type
                """,
                {"entity_id": entity["id"]},
            )
            api_rows = session.run(
                f"""
                MATCH path=(upstream:APIEndpoint)-[:CALLS_API*1..{max_hops}]->(downstream:APIEndpoint)-[rel]->(:DomainEntity {{id: $entity_id}})
                WHERE type(rel) IN ['READS', 'WRITES', 'DELETES', 'ACCESSES']
                RETURN DISTINCT upstream.id AS upstream_id,
                       upstream.name AS upstream_name,
                       downstream.id AS downstream_id,
                       downstream.name AS downstream_name,
                       type(rel) AS terminal_relation,
                       length(path) AS hops,
                       [node IN nodes(path) | {{id: node.id, name: node.name, node_type: labels(node)[0]}}] AS chain
                ORDER BY hops ASC, upstream_name ASC
                """,
                {"entity_id": entity["id"]},
            )

            return {
                "entity": entity,
                "storage": [dict(row) for row in storage_rows],
                "direct_impacts": [dict(row) for row in direct_rows],
                "api_chains": [dict(row) for row in api_rows],
                "max_hops": max_hops,
            }
