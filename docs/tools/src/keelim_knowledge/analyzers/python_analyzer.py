from __future__ import annotations

import re
from pathlib import Path

from keelim_knowledge.models import AnalysisArtifact, KnowledgeEdge, KnowledgeNode


ROUTER_PREFIX_RE = re.compile(r'APIRouter\(\s*prefix\s*=\s*["\']([^"\']+)["\']')
ROUTE_DECORATOR_RE = re.compile(r"@router\.(get|post|put|patch|delete)\(\s*['\"]([^'\"]+)['\"]")
SERVICE_IMPORT_RE = re.compile(
    r"from\s+app\.services\.([a-zA-Z0-9_\.]+)\s+import\s+(.+?)(?:\n\s*\n|$)",
    re.S,
)


def _service_symbols(raw: str) -> list[str]:
    cleaned = raw.replace("(", "").replace(")", "").replace("\\", "")
    symbols: list[str] = []
    for chunk in cleaned.replace("\n", ",").split(","):
        symbol = chunk.strip()
        if not symbol:
            continue
        symbol = symbol.split(" as ", 1)[0].strip()
        if symbol:
            symbols.append(symbol)
    return symbols


class PythonAnalyzer:
    subproject = "rich"

    def analyze(self, root: str | Path) -> AnalysisArtifact:
        root_path = Path(root)
        nodes: list[KnowledgeNode] = []
        edges: list[KnowledgeEdge] = []

        for api_file in root_path.glob("app/api/**/*.py"):
            text = api_file.read_text(encoding="utf-8")
            prefix_match = ROUTER_PREFIX_RE.search(text)
            prefix = prefix_match.group(1) if prefix_match else ""

            imported_services: list[str] = []
            for service_match in SERVICE_IMPORT_RE.finditer(text):
                module_name = service_match.group(1)
                symbols = _service_symbols(service_match.group(2))
                for symbol in symbols:
                    service_id = f"rich:service:{module_name}.{symbol}"
                    imported_services.append(service_id)
                    nodes.append(
                        KnowledgeNode(
                            id=service_id,
                            node_type="Service",
                            name=f"{module_name}.{symbol}",
                            path=f"rich/app/services/{module_name.replace('.', '/')}.py",
                        )
                    )

            for method, route in ROUTE_DECORATOR_RE.findall(text):
                full_path = f"{prefix}{route}"
                endpoint_id = f"rich:endpoint:{method.lower()}:{full_path}"
                nodes.append(
                    KnowledgeNode(
                        id=endpoint_id,
                        node_type="APIEndpoint",
                        name=f"{method.upper()} {full_path}",
                        path=str(api_file.relative_to(root_path)),
                    )
                )
                edges.append(
                    KnowledgeEdge(
                        id=f"edge:{endpoint_id}:module",
                        relation_type="PROVIDES",
                        source="subproject:rich",
                        target=endpoint_id,
                    )
                )
                for service_id in imported_services:
                    edges.append(
                        KnowledgeEdge(
                            id=f"edge:{endpoint_id}:uses:{service_id}",
                            relation_type="USES",
                            source=endpoint_id,
                            target=service_id,
                        )
                    )

        return AnalysisArtifact(subproject=self.subproject, nodes=nodes, edges=edges)
