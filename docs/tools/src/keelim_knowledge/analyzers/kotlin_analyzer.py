from __future__ import annotations

import re
from pathlib import Path

from keelim_knowledge.models import AnalysisArtifact, KnowledgeEdge, KnowledgeNode


MODULE_RE = re.compile(r'"(:[^"]+)"')


def _module_slug(module_name: str) -> str:
    return module_name.lstrip(":").replace(":", "-")


def _module_path(module_name: str) -> str:
    return "/".join(("all", *module_name.lstrip(":").split(":")))


class KotlinAnalyzer:
    subproject = "all"

    def analyze(self, root: str | Path) -> AnalysisArtifact:
        root_path = Path(root)
        settings_path = root_path / "settings.gradle.kts"
        text = settings_path.read_text(encoding="utf-8")
        modules = MODULE_RE.findall(text)

        nodes: list[KnowledgeNode] = []
        edges: list[KnowledgeEdge] = []

        for module_name in modules:
            slug = _module_slug(module_name)
            module_id = f"all:module:{slug}"
            nodes.append(
                KnowledgeNode(
                    id=module_id,
                    node_type="Module",
                    name=module_name,
                    path=_module_path(module_name),
                )
            )
            edges.append(
                KnowledgeEdge(
                    id=f"edge:subproject:all:{slug}",
                    relation_type="CONTAINS",
                    source="subproject:all",
                    target=module_id,
                )
            )
            if module_name.startswith(":feature:") or module_name.startswith(":app-"):
                screen_id = f"all:screen:{slug}"
                nodes.append(
                    KnowledgeNode(
                        id=screen_id,
                        node_type="UIScreen",
                        name=module_name,
                        path=_module_path(module_name),
                    )
                )
                edges.append(
                    KnowledgeEdge(
                        id=f"edge:{module_id}:renders:{screen_id}",
                        relation_type="CONTAINS",
                        source=module_id,
                        target=screen_id,
                    )
                )

        return AnalysisArtifact(subproject=self.subproject, nodes=nodes, edges=edges)
