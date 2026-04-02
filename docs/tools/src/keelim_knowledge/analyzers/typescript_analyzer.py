from __future__ import annotations

import re
from pathlib import Path

from keelim_knowledge.models import AnalysisArtifact, KnowledgeEdge, KnowledgeNode


TABLE_RE = re.compile(
    r"export\s+const\s+([A-Za-z0-9_]+)\s*=\s*pgTable\(\s*['\"]([^'\"]+)['\"]\s*,\s*\{(?P<body>.*?)\}\s*\)",
    re.S,
)
COLUMN_RE = re.compile(r"([A-Za-z0-9_]+)\s*:\s*[A-Za-z0-9_]+\(\s*['\"]([^'\"]+)['\"]")
ROUTE_METHOD_RE = re.compile(r"export\s+async\s+function\s+(GET|POST|PUT|PATCH|DELETE)\s*\(")


def _singularize(name: str) -> str:
    if name.endswith("ies") and len(name) > 3:
        return name[:-3] + "y"
    if name.endswith("s") and len(name) > 1:
        return name[:-1]
    return name


def _route_from_page(path: Path) -> str:
    parts = [part for part in path.parts if not (part.startswith("(") and part.endswith(")"))]
    return "/" + "/".join(parts[:-1]) if parts[:-1] else "/"


def _route_from_api(path: Path) -> str:
    parts = [part for part in path.parts if not (part.startswith("(") and part.endswith(")"))]
    return "/api/" + "/".join(parts[1:-1]) if len(parts) > 2 else "/api"


class TypeScriptAnalyzer:
    subproject = "keelim-vercel"

    def analyze(self, root: str | Path) -> AnalysisArtifact:
        root_path = Path(root)
        nodes: list[KnowledgeNode] = []
        edges: list[KnowledgeEdge] = []
        known_tables: dict[str, dict[str, str]] = {}

        db_path = root_path / "lib" / "db.ts"
        if db_path.exists():
            text = db_path.read_text(encoding="utf-8")
            for _, table_name, body in TABLE_RE.findall(text):
                table_id = f"keelim-vercel:table:{table_name}"
                known_tables[table_name] = {
                    "table_id": table_id,
                    "entity_id": f"entity:{_singularize(table_name)}",
                }
                nodes.append(
                    KnowledgeNode(
                        id=table_id,
                        node_type="DatabaseTable",
                        name=table_name,
                        path=str(db_path.relative_to(root_path)),
                    )
                )
                edges.append(
                    KnowledgeEdge(
                        id=f"edge:subproject:keelim-vercel:{table_name}",
                        relation_type="CONTAINS",
                        source="subproject:keelim-vercel",
                        target=table_id,
                    )
                )
                for _, column_name in COLUMN_RE.findall(body):
                    column_id = f"column:{table_name}:{column_name}"
                    nodes.append(
                        KnowledgeNode(
                            id=column_id,
                            node_type="TableColumn",
                            name=f"{table_name}.{column_name}",
                            path=str(db_path.relative_to(root_path)),
                            metadata={"table": table_name, "column_name": column_name},
                        )
                    )
                    edges.append(
                        KnowledgeEdge(
                            id=f"edge:{column_id}:stored-in:{table_id}",
                            relation_type="STORED_IN",
                            source=column_id,
                            target=table_id,
                        )
                    )

        for page_path in root_path.glob("app/**/page.tsx"):
            route = _route_from_page(page_path.relative_to(root_path / "app"))
            screen_id = f"keelim-vercel:screen:{route}"
            nodes.append(
                KnowledgeNode(
                    id=screen_id,
                    node_type="UIScreen",
                    name=route,
                    path=str(page_path.relative_to(root_path)),
                )
            )

        for route_path in root_path.glob("app/api/**/route.ts"):
            endpoint = _route_from_api(route_path.relative_to(root_path / "app"))
            route_text = route_path.read_text(encoding="utf-8")
            methods = ROUTE_METHOD_RE.findall(route_text)
            endpoint_id = f"keelim-vercel:endpoint:route:{endpoint}"
            nodes.append(
                KnowledgeNode(
                    id=endpoint_id,
                    node_type="APIEndpoint",
                    name=endpoint,
                    path=str(route_path.relative_to(root_path)),
                )
            )
            resource = endpoint.split("/")[2] if len(endpoint.split("/")) > 2 else ""
            table_info = known_tables.get(resource)
            if table_info and methods:
                relation_type = {
                    "GET": "READS",
                    "POST": "WRITES",
                    "PUT": "WRITES",
                    "PATCH": "WRITES",
                    "DELETE": "DELETES",
                }[methods[0]]
                edges.append(
                    KnowledgeEdge(
                        id=f"edge:{endpoint_id}:{relation_type.lower()}:{table_info['entity_id']}",
                        relation_type=relation_type,
                        source=endpoint_id,
                        target=table_info["entity_id"],
                    )
                )
                edges.append(
                    KnowledgeEdge(
                        id=f"edge:{endpoint_id}:accesses:{table_info['table_id']}",
                        relation_type="ACCESSES",
                        source=endpoint_id,
                        target=table_info["table_id"],
                    )
                )

        return AnalysisArtifact(subproject=self.subproject, nodes=nodes, edges=edges)
